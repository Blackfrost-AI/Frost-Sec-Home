---
pack_id: windows-removal-recovery
os: windows
os_versions: ["10 22H2", "11"]
shell: powershell
privilege: admin-mixed
pack_type: module
safety_core_version: 3
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Windows — removal and recovery

CONFIRMED findings only. Every change: full approval, one at a time, saved
capture as undo. Never bulk-delete. Ransomware (note + many renamed files)
→ stop, use INCIDENT-RANSOMWARE.md.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Windows PC?" If not, name the right pack. Ask what was
confirmed (Defender detection or verified suspicious startup item). Nothing
confirmed → stop; no speculative cleanup.

## Self-check

1. What must be saved before disabling anything?
2. How many threats does Remove-MpThreat act on — and what does the approval say?
3. When does this pack refuse to act and hand off to INCIDENT?

## Step 1 — restore point first (T1)

FULL APPROVAL. WHAT: a restore point before changes. WHY: a way back. RISK:
a little disk, a minute. UNDO: it is the undo. Wait for YES.

```command
Checkpoint-Computer -Description "Frost-Sec-Home before removal"
```

```card
CARD W-REM-01
COMMAND: Checkpoint-Computer -Description "Frost-Sec-Home before removal"
TIER: T1
NORMAL LOOKS LIKE: no output after ~a minute = created.
SUSPICIOUS LOOKS LIKE: none.
CANNOT TELL WHEN: other errors — continue only with explicit informed YES that there is no rollback net.
EXIT CODES / EXPECTED WARNINGS: "protection disabled" → harden pack's Step 1b path or proceed-with-warning; "already created in last 24h" = NORMAL, that point is the net. Neither is a failure.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: "refusal means skip the safety net silently".
```

## Step 2 — Defender remediation (T1, ALL active threats)

`Remove-MpThreat` remediates ALL active threats Defender lists — no
per-threat switch. FULL APPROVAL. WHAT: quarantine/remove every active
threat (read the scan findings first; approval must say ALL). WHY:
supported, reversible. RISK: false-positive files quarantined too. UNDO:
Windows Security > Virus & threat protection > Protection history > item >
Restore. Wait for YES.

```command
Remove-MpThreat
```

```card
CARD W-REM-02
COMMAND: Remove-MpThreat
TIER: T1
NORMAL LOOKS LIKE: no output or success line; re-check with Step 2b.
SUSPICIOUS LOOKS LIKE: remediation errors for a threat (medium) — TRIAGE Step 5.
CANNOT TELL WHEN: no active threats listed — nothing to do; never run "just in case".
EXIT CODES / EXPECTED WARNINGS: none expected.
NEXT IF SUSPICIOUS: TRIAGE Step 5 (NEW chat).
NEVER CONCLUDE: "removes only the one threat we discussed" — ALL active threats; the approval must say so.
```

## Step 2b — verify remediation (look-only)

```command
Get-MpThreat | Select-Object -First 10 ThreatName, IsActive
```

```card
CARD W-REM-03
COMMAND: Get-MpThreat | Select-Object -First 10 ThreatName, IsActive
TIER: T0
NORMAL LOOKS LIKE: no rows or all IsActive: False — remediation held.
SUSPICIOUS LOOKS LIKE: any IsActive: True (high) — TRIAGE Step 5 offline scan (NEW chat); still active after it → NEEDS A HUMAN.
CANNOT TELL WHEN: command errors.
EXIT CODES / EXPECTED WARNINGS: empty output NORMAL. Paste only the first 10 lines.
NEXT IF SUSPICIOUS: TRIAGE Step 5 (NEW chat).
NEVER CONCLUDE: "one clean re-check = permanently clean" — watch for recurrence.
```

## Step 3 — disable ONE verified item (capture first)

Only an item verified suspicious in the persistence pack. TWO gated actions,
each with its own YES. Slots byte-match the verified task name.

3a (look-only capture — the undo material):
```command
schtasks /query /tn <NAME: verified task name, from step 0> /xml
```

```card
CARD W-REM-04
COMMAND: schtasks /query /tn <NAME: verified task name, from step 0> /xml
TIER: T0
NORMAL LOOKS LIKE: XML prints. User saves it as frost-sec-undo-task.txt — the undo.
SUSPICIOUS LOOKS LIKE: n/a — capture step.
CANNOT TELL WHEN: task not found — stop; disable nothing.
EXIT CODES / EXPECTED WARNINGS: none expected.
NEXT IF SUSPICIOUS: 3b only after the capture is saved.
NEVER CONCLUDE: "rebuild the task from memory" — the saved XML is the only undo.
```

3b (T1). FULL APPROVAL. WHAT: disable this one task. WHY: verified
suspicious. RISK: if legit, it stops auto-starting. UNDO: Task Scheduler >
import saved XML (guided). Wait for YES.

```command
schtasks /change /tn <NAME: verified task name, from step 0> /disable
```

```card
CARD W-REM-05
COMMAND: schtasks /change /tn <NAME: verified task name, from step 0> /disable
TIER: T1
NORMAL LOOKS LIKE: "SUCCESS: The parameters of scheduled task ... have been changed."
SUSPICIOUS LOOKS LIKE: access denied (medium) — offer SHORT APPROVAL elevation, retry once.
CANNOT TELL WHEN: errors twice — stop, NEEDS A HUMAN.
EXIT CODES / EXPECTED WARNINGS: none expected.
NEXT IF SUSPICIOUS: stop after two failures.
NEVER CONCLUDE: "disabled = deleted" — the task exists, switched off; that is the point.
```

Registry Run-key item instead: capture the exact key with `reg query`
(guided, save output), then Task Manager > Startup apps > right-click >
Disable — same screen reverses it. Never delete registry values.

## Report

Fill the REPORT SKELETON: changes, captures, undo. HANDOFF: re-run
`packs/windows/04-malware-scan.md` (NEW chat) to confirm; still active or
unclear → NEEDS A HUMAN. Ransomware signs → INCIDENT-RANSOMWARE.md, NEW chat.
