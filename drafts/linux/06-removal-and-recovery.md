---
pack_id: linux-removal-recovery
os: linux
os_versions: ["Ubuntu 22.04/24.04 LTS", "Fedora 40+", "Arch (rolling)"]
shell: bash
privilege: admin-mixed
pack_type: module
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Linux — removal and recovery (careful, gated, reversible)

CONFIRMED findings only. Every change: full approval, one at a time, saved
capture as undo. Never bulk-delete. Quarantine = reversible move, not erase.
Ransomware → INCIDENT-RANSOMWARE.md.

## Step 0 — confirm this is the right pack

Ask: "Are you on Linux?" If not, name the right pack. Ask what was confirmed
(verified ClamAV detection or autostart item); have the user paste the exact
file path(s). Nothing confirmed → stop; no speculative cleanup.

```command
cat /etc/os-release
```

```card
CARD L-REM-00
COMMAND: cat /etc/os-release
TIER: T0
NORMAL LOOKS LIKE: NAME/VERSION_ID lines.
SUSPICIOUS LOOKS LIKE: none — identity only.
CANNOT TELL WHEN: file missing — ask; unknown → stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: anything from identity alone.
```

## Self-check

1. What must exist before any change? (Backup or explicit warning.)
2. Where does a quarantined file go? (~/frost-sec-quarantine — recoverable.)
3. When does this pack refuse and hand off? (Ransomware signs; recurrence.)

## Step 1 — backup net first (guided, T1)

FULL APPROVAL. WHAT: confirm a recent backup. WHY: the way back. RISK:
none — checking. UNDO: it is the undo. Wait for YES; guide: check the
backup tool/drive. If none: say so plainly; continue only with informed
YES — no rollback net.

```card
CARD L-REM-01
COMMAND: GUI: backup tool/drive — check latest backup date
TIER: T1
NORMAL LOOKS LIKE: backup within a day or two.
SUSPICIOUS LOOKS LIKE: no backup / very old (medium) — offer to back up now first.
CANNOT TELL WHEN: none configured — explicit informed YES to proceed without a net.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: back up, then continue.
NEVER CONCLUDE: "no backup = skip the net silently".
```

## Step 2 — quarantine ONE confirmed file (T1, move not delete)

Only a file the user verified. FULL APPROVAL. WHAT: create a locked
quarantine folder, move this one file in. WHY: unusable but recoverable.
RISK: if needed, move it back. UNDO: move back from
~/frost-sec-quarantine (guided). Wait for YES.

```command
mkdir -p ~/frost-sec-quarantine && chmod 700 ~/frost-sec-quarantine && mv -n "<PATH: confirmed file path, from step 0>" ~/frost-sec-quarantine/
```

```card
CARD L-REM-02
COMMAND: mkdir -p ~/frost-sec-quarantine && chmod 700 ~/frost-sec-quarantine && mv -n "<PATH: confirmed file path, from step 0>" ~/frost-sec-quarantine/
TIER: T1
NORMAL LOOKS LIKE: no output; file inside ~/frost-sec-quarantine.
SUSPICIOUS LOOKS LIKE: "Permission denied" (medium) — system file; stop, NEEDS A HUMAN; never sudo rm.
CANNOT TELL WHEN: errors twice — stop, NEEDS A HUMAN.
EXIT CODES / EXPECTED WARNINGS: none. `-n` never overwrites: still in place = name collision — stop; rename with today's date, retry once.
NEXT IF SUSPICIOUS: stop, NEEDS A HUMAN.
NEVER CONCLUDE: "quarantined = gone forever" — recoverable until the user decides.
```

## Step 3 — disable ONE confirmed autostart item (capture first)

Only an item verified in the persistence pack. TWO gated actions, each
with its own YES.
3a (look-only capture — the undo):

```command
cat "<PATH: verified .desktop path, from step 0>"
```

```card
CARD L-REM-03
COMMAND: cat "<PATH: verified .desktop path, from step 0>"
TIER: T0
NORMAL LOOKS LIKE: contents print. User saves them as frost-sec-undo-item.txt — the undo.
SUSPICIOUS LOOKS LIKE: n/a — capture step.
CANNOT TELL WHEN: file not found — stop; disable nothing.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 3b only after the capture is saved.
NEVER CONCLUDE: "rebuild from memory" — the saved copy is the only undo.
```

3b (T1). FULL APPROVAL. WHAT: move this one .desktop to quarantine. WHY:
verified suspicious. RISK: if legit, that app stops auto-starting. UNDO:
move back from ~/frost-sec-quarantine (guided). Wait for YES.

```command
mv -n "<PATH: verified .desktop path, from step 0>" ~/frost-sec-quarantine/
```

```card
CARD L-REM-04
COMMAND: mv -n "<PATH: verified .desktop path, from step 0>" ~/frost-sec-quarantine/
TIER: T1
NORMAL LOOKS LIKE: no output; file in quarantine; gone after next login.
SUSPICIOUS LOOKS LIKE: permission denied (medium) — system location; stop, NEEDS A HUMAN.
CANNOT TELL WHEN: errors twice — stop, NEEDS A HUMAN.
EXIT CODES / EXPECTED WARNINGS: none. `-n` never overwrites: still in place = name collision — stop; rename with today's date, retry once.
NEXT IF SUSPICIOUS: stop, NEEDS A HUMAN.
NEVER CONCLUDE: "moved = deleted" — sits in quarantine, recoverable.
```

Systemd service instead? NEEDS A HUMAN — .desktop items only here; never
disable or delete unit files.

## Step 4 — if it comes back

Item reappears or spreads: stop — NEEDS A HUMAN. No mass deletion. Record
what returned, when, where.

## Report

Fill the REPORT SKELETON: changes, captures, undo. HANDOFF: re-run
`packs/linux/04-malware-scan.md` (NEW chat) to confirm; anything unclear →
NEEDS A HUMAN. Ransomware signs → INCIDENT-RANSOMWARE.md, NEW chat.
