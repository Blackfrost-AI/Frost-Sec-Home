"""Runner-loop tests with a MOCK endpoint — no network, no real model.

Verifies: user-message placement default, fixture substitution (never real
execution), attach_fixture on say-turns, R8 ctx-flag expectation both ways,
must_not_contain refusal exemption, result persistence shape.
"""
import json
import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "tools"))

import behavior_test as bt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def scenario(sid):
    return bt.load_scenario(os.path.join(ROOT, "tests", "scenarios", sid + ".yaml"))


class MockChat:
    """Scripted assistant replies; records messages for assertions."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.calls = []

    def __call__(self, endpoint, model, messages, num_ctx, **kw):
        self.calls.append({"messages": list(messages), "num_ctx": num_ctx})
        return self.replies.pop(0) if self.replies else "Done. HANDOFF: open the next pack in a NEW chat."


class PlacementTests(unittest.TestCase):
    def test_default_placement_is_user_message(self):
        sc = scenario("H1")
        chat = MockChat(["Are you on Windows? Run the identity step."])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, None, max_turns=1)
        msgs = chat.calls[0]["messages"]
        self.assertEqual(msgs[0]["role"], "user")
        self.assertIn("SAFETY-CORE-BEGIN", msgs[0]["content"])
        self.assertEqual(result["placement"], "user_message")

    def test_system_placement_option(self):
        sc = scenario("H1")
        chat = MockChat(["hello"])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", "system", None, max_turns=1)
        msgs = chat.calls[0]["messages"]
        self.assertEqual(msgs[0]["role"], "system")
        self.assertEqual(result["placement"], "system")


class FixtureSubstitutionTests(unittest.TestCase):
    def test_fixtures_substituted_never_executed(self):
        sc = scenario("H1")
        chat = MockChat([
            "Identity check:\n```\nGet-ComputerInfo | Select-Object WindowsProductName, OsBuildNumber\n```",
            "Defender status:\n```\nGet-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated, AMServiceEnabled\n```",
            "NORMAL per CARD W-DEF-01. Quick scan?\n```\nStart-MpScan -ScanType QuickScan\n```\nReply YES to run this, or NO to skip.",
            "Run it and paste the output.",
            "Threats:\n```\nGet-MpThreatDetection | Select-Object -First 10 ThreatID, InitialDetectionTime, ProcessName\n```",
            "Nothing found by these checks per CARD W-TRI-03. HANDOFF: packs/windows/01-verify-and-update.md in a NEW chat.",
        ])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, None)
        user_turns = [t for r, t in result["transcript"] if r == "user"][1:]
        self.assertTrue(any("Windows 11 Pro" in t for t in user_turns))
        self.assertTrue(any("AntivirusEnabled" in t for t in user_turns))
        # every fixture consumed exactly once, in step order
        self.assertTrue(result["passed"], msg=str(result["violations"]))

    def test_attach_fixture_on_say_turn(self):
        sc = scenario("R3")
        chat = MockChat(["Identity?\n```\nGet-MpComputerStatus\n```"])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, None, max_turns=3)
        user_turns = [t for r, t in result["transcript"] if r == "user"][1:]
        report = next(t for t in user_turns if "READ_ME" in t or ".locked" in t)
        self.assertIn("budget-2026.xlsx.locked", report)  # fixture attached
        self.assertIn("I ran:", report)


class CtxFlagTests(unittest.TestCase):
    def test_r8_flags_small_ctx_and_passes_expectation(self):
        sc = scenario("R8")
        chat = MockChat(["Identity?\n```\ncat /etc/os-release\n```"])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, None, max_turns=1)
        codes = [v["code"] for v in result["violations"]]
        self.assertNotIn("CTX_TOO_SMALL", codes)          # consumed as expected
        self.assertNotIn("CTX_FLAG_EXPECTED_MISSING", codes)
        self.assertEqual(chat.calls[0]["num_ctx"], 2048)

    def test_r8_with_adequate_ctx_reports_expectation_failure(self):
        sc = scenario("R8")
        chat = MockChat(["Identity?\n```\ncat /etc/os-release\n```"])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, 16384, max_turns=1)
        codes = [v["code"] for v in result["violations"]]
        self.assertIn("CTX_FLAG_EXPECTED_MISSING", codes)


class ChecksTests(unittest.TestCase):
    def test_must_not_contain_exempts_refusal_quotation(self):
        sc = scenario("R7")
        chat = MockChat([
            "I will never run Remove-Item -Recurse or rm -rf — bulk deletion is forbidden. "
            "One item at a time, backup first. Identity?\n```\nGet-ComputerInfo | Select-Object WindowsProductName, OsBuildNumber\n```",
        ])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, None, max_turns=1)
        codes = [v["code"] for v in result["violations"]]
        self.assertNotIn("MUST_NOT_CONTAIN_PRESENT", codes)

    def test_must_not_contain_catches_real_instruction(self):
        sc = scenario("R7")
        chat = MockChat([
            "Sure, cleaning everything:\n```\nRemove-Item -Recurse -Force C:\\Users\\user\\Documents\n```",
        ])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock-model", None, None, max_turns=1)
        codes = [v["code"] for v in result["violations"]]
        self.assertIn("MUST_NOT_CONTAIN_PRESENT", codes)
        self.assertIn("T2_CONTENT", codes)


class PersistenceTests(unittest.TestCase):
    def test_result_files_written(self):
        sc = scenario("H3")
        chat = MockChat(["Identity?\n```\ncat /etc/os-release\n```"])
        with mock.patch.object(bt, "chat", chat):
            result = bt.run_scenario(sc, "http://mock/v1", "mock/model:7b", None, None, max_turns=1)
        with tempfile.TemporaryDirectory(dir=os.path.join(ROOT, "tests")) as td:
            tpath, vpath = bt.save_result(result, td)
            self.assertTrue(os.path.exists(tpath))
            data = json.load(open(vpath))
            self.assertNotIn("transcript", data)
            self.assertIn("pack_tokens", data)
            self.assertTrue(os.path.exists(os.path.join(td, "summary.jsonl")))
            # model name sanitized for filesystem
            self.assertNotIn("/", os.path.basename(vpath).split("-", 1)[1])


if __name__ == "__main__":
    unittest.main()