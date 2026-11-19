"""Static validator for Frost-Sec-Home packs (Prompt Standard S1-S12 + schema).

Usage: python3 tools/validate.py <repo-root>
Exit 0 when every pack passes; exit 1 with a per-pack violation report otherwise.

check_pack(path) -> list[Violation] is importable for tests.
"""
from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass

import yaml

from token_budget import count_text

CORE_BEGIN = "<!-- SAFETY-CORE-BEGIN -->"
CORE_END = "<!-- SAFETY-CORE-END -->"

BUDGETS = {"module": 2500, "triage": 3500, "incident": 2500}
CORE_BUDGET = 1200

SCHEMA = {
    "pack_id": str,
    "os": {"windows", "macos", "linux"},
    "os_versions": list,
    "shell": {"powershell", "zsh", "bash"},
    "privilege": {"user", "admin-mixed"},
    "pack_type": {"triage", "module", "incident"},
    "safety_core_version": int,
    "min_context_tokens": int,
    "verification_status": {"untested", "partial", "verified"},
}

CARD_FIELDS = [
    "COMMAND",
    "TIER",
    "NORMAL LOOKS LIKE",
    "SUSPICIOUS LOOKS LIKE",
    "CANNOT TELL WHEN",
    "EXIT CODES / EXPECTED WARNINGS",
    "NEXT IF SUSPICIOUS",
    "NEVER CONCLUDE",
]

# Banned patterns — matched ONLY in command position (inside ```command fences).
BANNED = [
    (r"\brm\s+(-[a-zA-Z]*\s+)*-rf\b", "rm -rf"),
    (r"Remove-Item[^\n]*-Recurse[^\n]*-Force|Remove-Item[^\n]*-Force[^\n]*-Recurse", "Remove-Item -Recurse -Force"),
    (r"\bdiskpart\b", "diskpart"),
    (r"^\s*format\s", "format"),
    (r"\bdd\b[^\n]*\bof=/dev/", "dd of=/dev/"),
    (r"chmod\s+-R\s+777", "chmod -R 777"),
    (r"curl[^\n]*\|\s*(ba)?sh", "curl | sh"),
    (r"\biwr\b[^\n]*\|\s*iex|Invoke-WebRequest[^\n]*\|\s*Invoke-Expression", "iwr | iex"),
    (r"--remove\b", "--remove"),
    (r"\bdel\s+/[fsq]", "del /f /s /q"),
    (r"pacman\s+-Sy\b(?![^\n]*-u)", "bare pacman -Sy"),
]

OS_MARKERS = {
    "windows": [
        r"\bGet-[A-Z]\w+", r"\bSet-[A-Z]\w+", r"\bStart-[A-Z]\w+",
        r"\bRemove-[A-Z]\w+", r"\bNew-[A-Z]\w+", r"\bCheckpoint-Computer\b",
    ],
    "macos": [
        r"\blaunchctl\b", r"\bspctl\b", r"\bcsrutil\b", r"\bfdesetup\b",
        r"\bsocketfilterfw\b", r"\bsw_vers\b", r"\bsoftwareupdate\b",
        r"\bplutil\b", r"\bipconfig\s+getifaddr\b",
    ],
    "linux": [
        r"\bapt(-get)?\s", r"\bdnf\s", r"\bpacman\s", r"\bufw\s",
        r"\bsystemctl\b", r"\bclamscan\b", r"\bfreshclam\b", r"\bss\s+-",
        r"\bdpkg\b", r"\brpm\s+-V", r"\bchmod\b", r"\bchown\b",
        r"\bcrontab\b", r"\bip\s+(addr|neigh)\b",
    ],
}

SLOT_RE = re.compile(r"<(PID|PATH|SUBNET):([^>]*)>")
STEP_RE = re.compile(r"^## Step (\d+)\b", re.M)
JUMP_RE = re.compile(r"go to step (\d+)")
FENCE_RE = re.compile(r"^```(\w*)\n(.*?)^```", re.M | re.S)


@dataclass
class Violation:
    code: str
    detail: str

    def __str__(self):
        return f"{self.code}: {self.detail}"


def _frontmatter(text: str):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    try:
        return yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None


def _check_frontmatter(fm, out):
    if not isinstance(fm, dict):
        out.append(Violation("FRONTMATTER_INVALID", "missing or unparseable frontmatter"))
        return
    for key, spec in SCHEMA.items():
        if key not in fm:
            out.append(Violation("FRONTMATTER_INVALID", f"missing field {key}"))
            continue
        val = fm[key]
        if isinstance(spec, set):
            if val not in spec:
                out.append(Violation("FRONTMATTER_INVALID", f"{key}={val!r} not in {sorted(spec)}"))
        elif spec is list:
            if not isinstance(val, list) or not val or not all(isinstance(x, str) for x in val):
                out.append(Violation("FRONTMATTER_INVALID", f"{key} must be a non-empty list[str]"))
        elif spec is int:
            if not isinstance(val, int):
                out.append(Violation("FRONTMATTER_INVALID", f"{key} must be int"))
        elif spec is str:
            if not isinstance(val, str) or not val:
                out.append(Violation("FRONTMATTER_INVALID", f"{key} must be non-empty str"))
    if isinstance(fm.get("min_context_tokens"), int) and fm["min_context_tokens"] < 16000:
        out.append(Violation("FRONTMATTER_INVALID", "min_context_tokens must be >= 16000"))


def _parse_card(body: str):
    fields = {}
    cid = None
    for line in body.strip().splitlines():
        m = re.match(r"^CARD (\S+)$", line.strip())
        if m:
            cid = m.group(1)
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            fields[k.strip()] = v.strip()
    return cid, fields


def check_pack(path: str) -> list[Violation]:
    out: list[Violation] = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    # tests create packs in temp dirs; fall back to the real repo core
    core_path = os.path.join(repo_root, "core", "SAFETY-CORE.md")
    if not os.path.exists(core_path):
        core_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core", "SAFETY-CORE.md")
    with open(core_path, encoding="utf-8") as f:
        core = f.read()

    fm = _frontmatter(text)
    _check_frontmatter(fm, out)
    fm = fm if isinstance(fm, dict) else {}

    # Safety Core block byte-identical
    m = re.search(re.escape(CORE_BEGIN) + r"\n(.*?)\n?" + re.escape(CORE_END), text, re.S)
    if not m:
        out.append(Violation("CORE_MISSING", "no SAFETY-CORE-BEGIN/END block"))
    else:
        block = m.group(1)
        if block.rstrip("\n") != core.rstrip("\n"):
            out.append(Violation("CORE_MUTATED", "embedded Safety Core differs from core/SAFETY-CORE.md"))
    core_tokens = count_text(core)["total"]
    if core_tokens > CORE_BUDGET:
        out.append(Violation("CORE_OVER_BUDGET", f"core {core_tokens} > {CORE_BUDGET}"))

    # Banner requirement
    status = fm.get("verification_status")
    if status in ("untested", "partial"):
        if not re.search(r"^> \*\*(UNTESTED|PARTIALLY VERIFIED):\*\*", text, re.M):
            out.append(Violation("BANNER_MISSING", f"verification_status={status} requires the standard banner"))

    # Token budget
    budget = BUDGETS.get(fm.get("pack_type", "module"), 2500)
    total = count_text(text)["total"]
    if total > budget:
        out.append(Violation("OVER_BUDGET", f"{total} tokens > {budget} for pack_type={fm.get('pack_type')}"))

    # Steps, fences, cards
    steps = {int(n) for n in STEP_RE.findall(text)}
    step_spans = [(int(mm.group(1)), mm.start()) for mm in STEP_RE.finditer(text)]

    def step_of(pos):
        cur = None
        for n, s in step_spans:
            if s <= pos:
                cur = n
        return cur

    fences = list(FENCE_RE.finditer(text))
    cmd_fences = [f for f in fences if f.group(1) == "command"]
    card_fences = [f for f in fences if f.group(1) == "card"]

    cards_by_step = {}
    for f in card_fences:
        cid, fields = _parse_card(f.group(2))
        st = step_of(f.start())
        if cid is None:
            out.append(Violation("CARD_FIELD_MISSING", "card without CARD <id> line"))
            continue
        for req in CARD_FIELDS:
            if req not in fields or not fields[req]:
                out.append(Violation("CARD_FIELD_MISSING", f"{cid}: missing/empty {req}"))
        if fields.get("TIER") not in ("T0", "T0-admin", "T1"):
            out.append(Violation("CARD_FIELD_MISSING", f"{cid}: bad TIER {fields.get('TIER')!r}"))
        cards_by_step.setdefault(st, []).append((cid, fields, f))

    for f in cmd_fences:
        cmd = f.group(2).strip("\n")
        st = step_of(f.start())
        if len(cmd.splitlines()) != 1:
            out.append(Violation("MULTI_COMMAND_STEP", f"step {st}: fenced command must be one line"))
        # banned patterns in command position only
        for pat, label in BANNED:
            if re.search(pat, cmd, re.M):
                out.append(Violation("BANNED_PATTERN", f"step {st}: {label}"))
        # cross-OS bleed
        os_name = fm.get("os")
        for other, markers in OS_MARKERS.items():
            if other == os_name:
                continue
            for pat in markers:
                if re.search(pat, cmd):
                    out.append(Violation("OS_BLEED", f"step {st}: {other} marker in {os_name} pack: {cmd[:60]}"))
                    break
        # card match
        matching = [(cid, fld) for cid, fld, _ in cards_by_step.get(st, []) if fld.get("COMMAND") == cmd]
        if not matching:
            out.append(Violation("CMD_CARD_MISMATCH", f"step {st}: no card COMMAND byte-matches {cmd[:60]!r}"))
        else:
            cid, fld = matching[0]
            # typed slots need a source step
            for slot in SLOT_RE.finditer(cmd):
                if "from step" not in slot.group(2):
                    out.append(Violation("SLOT_SOURCE_MISSING", f"{cid}: slot <{slot.group(1)}> lacks 'from step N'"))
                else:
                    src = re.search(r"from step (\d+)", slot.group(2))
                    if src and int(src.group(1)) not in steps:
                        out.append(Violation("BROKEN_JUMP", f"{cid}: slot source step {src.group(1)} does not exist"))
            # unbounded output needs limiter + paste instruction
            if fld.get("UNBOUNDED", "").lower() == "yes":
                has_limiter = ("Select-Object -First" in cmd) or ("head -n" in cmd) or ("grep" in cmd)
                if not has_limiter:
                    out.append(Violation("LIMITER_MISSING", f"{cid}: UNBOUNDED command without limiter"))
                span_end = step_spans[[n for n, _ in step_spans].index(st) + 1][1] if st is not None and [n for n, _ in step_spans].index(st) + 1 < len(step_spans) else len(text)
                span_start = dict(step_spans).get(st, 0)
                if "paste only the first" not in text[span_start:span_end].lower():
                    out.append(Violation("LIMITER_MISSING", f"{cid}: step prose lacks 'paste only the first N lines'"))

    # every command fence must have a card in its step (covered above); every card needs a command fence
    cmd_steps = {step_of(f.start()) for f in cmd_fences}
    for st, cards in cards_by_step.items():
        if st not in cmd_steps:
            for cid, _, _ in cards:
                out.append(Violation("CMD_CARD_MISMATCH", f"{cid}: card in step {st} has no command fence"))

    # jumps
    for j in JUMP_RE.finditer(text):
        if int(j.group(1)) not in steps:
            out.append(Violation("BROKEN_JUMP", f"go to step {j.group(1)} — no such step"))

    # self-check: 3 numbered questions
    sc = re.search(r"^## Self-check\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not sc or len(re.findall(r"^\d+\.", sc.group(1), re.M)) != 3:
        out.append(Violation("SELF_CHECK_MISSING", "need ## Self-check with exactly 3 numbered questions"))

    # handoff
    if "HANDOFF" not in text or "NEW chat" not in text:
        out.append(Violation("HANDOFF_MISSING", "pack must end with HANDOFF + NEW chat instruction"))

    return out


def main(root: str) -> int:
    packs_dir = os.path.join(root, "packs")
    failures = 0
    checked = 0
    for dirpath, _, files in os.walk(packs_dir):
        for fn in sorted(files):
            if not fn.endswith(".md"):
                continue
            path = os.path.join(dirpath, fn)
            checked += 1
            vs = check_pack(path)
            rel = os.path.relpath(path, root)
            if vs:
                failures += 1
                print(f"FAIL {rel}")
                for v in vs:
                    print(f"  {v}")
            else:
                print(f"PASS {rel}")
    # core budget check even when no packs exist yet
    core_path = os.path.join(root, "core", "SAFETY-CORE.md")
    if os.path.exists(core_path):
        with open(core_path, encoding="utf-8") as f:
            t = count_text(f.read())["total"]
        if t > CORE_BUDGET:
            failures += 1
            print(f"FAIL core/SAFETY-CORE.md: {t} tokens > {CORE_BUDGET}")
        else:
            print(f"PASS core/SAFETY-CORE.md ({t} tokens)")
    print(f"\n{checked} packs checked, {failures} failing")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
