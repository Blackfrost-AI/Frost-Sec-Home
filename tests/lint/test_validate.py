"""Failing-first tests for tools/validate.py (Task 4).

Run: python3 -m unittest discover -s tests/lint -v
Each test builds a minimal pack in a temp dir and asserts the validator
catches (or accepts) exactly one condition.
"""
import os
import sys
import tempfile
import unittest

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools"))

import validate  # noqa: E402

CORE = open(os.path.join(REPO, "core", "SAFETY-CORE.md")).read()

FRONTMATTER = """---
pack_id: windows-test
os: windows
os_versions: ["11"]
shell: powershell
privilege: user
pack_type: module
safety_core_version: 3
min_context_tokens: 16000
verification_status: verified
---
"""

BANNER = "> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.\n"


def card(cid="W-T-01", command="Get-Date", tier="T0", extra=""):
    return (
        f"```card\nCARD {cid}\nCOMMAND: {command}\nTIER: {tier}\n"
        "NORMAL LOOKS LIKE: a date\nSUSPICIOUS LOOKS LIKE: nothing\n"
        "CANNOT TELL WHEN: command errors\n"
        "EXIT CODES / EXPECTED WARNINGS: none\n"
        "NEXT IF SUSPICIOUS: step 0\nNEVER CONCLUDE: anything\n"
        f"{extra}```\n"
    )


def make_pack(body="", frontmatter=FRONTMATTER, core=CORE, banner=""):
    return (
        frontmatter
        + banner
        + "\n<!-- SAFETY-CORE-BEGIN -->\n"
        + core
        + "\n<!-- SAFETY-CORE-END -->\n\n"
        + "## Step 0 — identity\nConfirm the OS is Windows; if not, stop.\n\n"
        + "## Self-check\n1. What do you do before changing anything?\n"
        + "2. What are the tiers?\n3. What do you do when unsure?\n\n"
        + body
        + "\n## Report\nFill the report. HANDOFF: next pack, open it in a NEW chat.\n"
    )


GOOD_BODY = (
    "## Step 1 — look at the date\nShow the command, wait for output.\n\n"
    "```command\nGet-Date\n```\n\n" + card()
)


class PackChecks(unittest.TestCase):
    def check(self, text, expect_code=None, expect_absent=False):
        with tempfile.TemporaryDirectory(dir=REPO) as td:
            p = os.path.join(td, "pack.md")
            with open(p, "w") as f:
                f.write(text)
            violations = validate.check_pack(p)
            codes = [v.code for v in violations]
            if expect_absent:
                self.assertNotIn(expect_code, codes, f"unexpected {expect_code}: {codes}")
            else:
                self.assertIn(expect_code, codes, f"missing {expect_code}: {codes}")
            return codes

    def test_good_pack_passes(self):
        with tempfile.TemporaryDirectory(dir=REPO) as td:
            p = os.path.join(td, "pack.md")
            with open(p, "w") as f:
                f.write(make_pack(GOOD_BODY))
            self.assertEqual(validate.check_pack(p), [])

    def test_mutated_safety_core_detected(self):
        bad_core = CORE.replace("One YES = one command.", "One YES = many commands.")
        self.check(make_pack(GOOD_BODY, core=bad_core), "CORE_MUTATED")

    def test_fenced_command_not_matching_card(self):
        body = GOOD_BODY.replace("```command\nGet-Date\n```", "```command\nGet-Date -Format s\n```")
        self.check(make_pack(body), "CMD_CARD_MISMATCH")

    def test_banned_pattern_in_command_position(self):
        body = (
            "## Step 1 — bad\n\n```command\nrm -rf /home/user\n```\n\n"
            + card(command="rm -rf /home/user")
        )
        self.check(make_pack(body), "BANNED_PATTERN")

    def test_banned_word_in_prose_not_flagged(self):
        body = GOOD_BODY + "\nNever use the format command or rm -rf; we do not delete.\n"
        self.check(make_pack(body), "BANNED_PATTERN", expect_absent=True)

    def test_cross_os_bleed(self):
        body = (
            "## Step 1 — wrong OS\n\n```command\nchmod 755 /tmp/x\n```\n\n"
            + card(command="chmod 755 /tmp/x")
        )
        self.check(make_pack(body), "OS_BLEED")

    def test_broken_jump(self):
        body = GOOD_BODY + "\nIF output shows X, go to step 99.\n"
        self.check(make_pack(body), "BROKEN_JUMP")

    def test_missing_card_field(self):
        c = card().replace("EXIT CODES / EXPECTED WARNINGS: none\n", "")
        body = "## Step 1 — look\n\n```command\nGet-Date\n```\n\n" + c
        self.check(make_pack(body), "CARD_FIELD_MISSING")

    def test_missing_limiter_on_unbounded(self):
        body = (
            "## Step 1 — long list\n\n```command\nGet-ScheduledTask\n```\n\n"
            + card(command="Get-ScheduledTask", extra="UNBOUNDED: yes\n")
        )
        self.check(make_pack(body), "LIMITER_MISSING")

    def test_unbounded_with_limiter_ok(self):
        cmd = "Get-ScheduledTask | Select-Object -First 30"
        body = (
            "## Step 1 — long list\nPaste only the first 30 lines.\n\n"
            f"```command\n{cmd}\n```\n\n"
            + card(command=cmd, extra="UNBOUNDED: yes\n")
        )
        self.check(make_pack(body), "LIMITER_MISSING", expect_absent=True)

    def test_over_budget_pack(self):
        filler = "\nWord " * 4000  # > 2500 tokens of prose
        body = GOOD_BODY + filler
        self.check(make_pack(body), "OVER_BUDGET")

    def test_substitution_without_source_step(self):
        cmd = "Stop-Process -Id <PID: digits only>"
        body = (
            "## Step 1 — stop\n\n```command\n" + cmd + "\n```\n\n"
            + card(command=cmd, tier="T1")
        )
        self.check(make_pack(body), "SLOT_SOURCE_MISSING")

    def test_substitution_with_source_step_ok(self):
        cmd = "Stop-Process -Id <PID: digits only, from step 1>"
        body = (
            "## Step 1 — stop\n\n```command\n" + cmd + "\n```\n\n"
            + card(command=cmd, tier="T1")
        )
        # self-reference to own step is legal (value read earlier in same step flow)
        self.check(make_pack(body), "SLOT_SOURCE_MISSING", expect_absent=True)

    def test_untested_without_banner(self):
        fm = FRONTMATTER.replace("verification_status: verified", "verification_status: untested")
        self.check(make_pack(GOOD_BODY, frontmatter=fm), "BANNER_MISSING")

    def test_untested_with_banner_ok(self):
        fm = FRONTMATTER.replace("verification_status: verified", "verification_status: untested")
        self.check(make_pack(GOOD_BODY, frontmatter=fm, banner=BANNER), "BANNER_MISSING", expect_absent=True)

    def test_bad_frontmatter_field(self):
        fm = FRONTMATTER.replace("os: windows", "os: plan9")
        self.check(make_pack(GOOD_BODY, frontmatter=fm), "FRONTMATTER_INVALID")

    def test_missing_self_check(self):
        text = make_pack(GOOD_BODY).replace("## Self-check", "## Something Else")
        self.check(text, "SELF_CHECK_MISSING")


if __name__ == "__main__":
    unittest.main()
