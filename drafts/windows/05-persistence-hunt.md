---
pack_id: windows-persistence-hunt
os: windows
os_versions: ["10 22H2", "11"]
shell: powershell
privilege: user
pack_type: module
safety_core_version: 3
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Windows — persistence hunt (what starts automatically)

Startup items: malware and many legit programs alike. Look-only pack;
suspicious items get verified, never deleted on a hunch. Unsigned ≠ malicious.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Windows PC?" If not, stop and name the right pack.

## Self-check

1. What verdict do you give an unsigned but plausible startup item?
2. Where does a suspicious item route — and where does it NEVER go?
3. What is the most common cause of fake "virus" popups in a browser?

## Step 1 — startup commands (look-only)

```command
Get-CimInstance Win32_StartupCommand | Select-Object -First 30 Name, Command, Location
```

```card
CARD W-PER-01
COMMAND: Get-CimInstance Win32_StartupCommand | Select-Object -First 30 Name, Command, Location
TIER: T0
NORMAL LOOKS LIKE: entries from Program Files (updaters, cloud sync, audio/graphics tools). Many are normal.
SUSPICIOUS LOOKS LIKE: a command running an .exe from Temp/AppData with a random name (medium) — Step 3 verifies; never delete here.
CANNOT TELL WHEN: empty output (no startup entries) — NORMAL; or errors — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "lots of startup items = infected" — normal PCs have many.
```

## Step 2 — scheduled tasks beyond Microsoft's (look-only)

```command
Get-ScheduledTask | Where-Object {$_.TaskPath -notlike "\Microsoft*"} | Select-Object -First 30 TaskName, TaskPath, State
```

```card
CARD W-PER-02
COMMAND: Get-ScheduledTask | Where-Object {$_.TaskPath -notlike "\Microsoft*"} | Select-Object -First 30 TaskName, TaskPath, State
TIER: T0
NORMAL LOOKS LIKE: tasks from installed software (updaters, backup tools). Even odd-looking names are often legit.
SUSPICIOUS LOOKS LIKE: a task whose action runs an .exe from Temp/AppData at every logon (medium) — CANNOT TELL until Step 3 reads its details; unsigned ≠ malware.
CANNOT TELL WHEN: you cannot see the action from this list — that is exactly why Step 3 exists; do not guess.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "unknown task name = malware" — verify the action path first.
```

## Step 3 — read one task's details (look-only)

Pick the suspicious TaskName from Step 2. Slot byte-matches that name;
quotes or symbols like ; | & $ ` → refuse and stop.

```command
Get-ScheduledTask -TaskName <NAME: task name byte-matching step 2 output, from step 2> | Select-Object -ExpandProperty Actions
```

```card
CARD W-PER-03
COMMAND: Get-ScheduledTask -TaskName <NAME: task name byte-matching step 2 output, from step 2> | Select-Object -ExpandProperty Actions
TIER: T0
NORMAL LOOKS LIKE: Execute in Program Files for a known product.
SUSPICIOUS LOOKS LIKE: Execute in Temp/AppData/random-name.exe (medium/high) — record; handoff to 06-removal-and-recovery.md (NEW chat) for gated, capture-first disable.
CANNOT TELL WHEN: name mismatch — re-check the exact name once; still failing = CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 06-removal-and-recovery.md (NEW chat).
NEVER CONCLUDE: "suspicious path = delete it now" — removal is a separate gated pack.
```

## Step 4 — hosts file (look-only)

```command
Get-Content C:\Windows\System32\drivers\etc\hosts
```

```card
CARD W-PER-04
COMMAND: Get-Content C:\Windows\System32\drivers\etc\hosts
TIER: T0
NORMAL LOOKS LIKE: only comment lines starting with # (the default file), possibly localhost entries.
SUSPICIOUS LOOKS LIKE: lines redirecting well-known sites (banks, update servers) to odd IPs (high) — record; NEEDS A HUMAN; do not edit in this pack.
CANNOT TELL WHEN: access denied — CANNOT TELL, note it.
EXIT CODES / EXPECTED WARNINGS: an almost-empty file is NORMAL.
NEXT IF SUSPICIOUS: report NEEDS A HUMAN.
NEVER CONCLUDE: "hosts entries mean infection" — some users add legit blocks.
```

## Step 5 — browser extensions and notification scams (guided)

The most common "you have a virus!" popup is a website NOTIFICATION the user
once allowed — not an infection. Guide: (1) in the browser, open
Settings > Privacy and security > Site settings > Notifications (Chrome/Edge
wording varies); remove any site the user does not recognize. (2) Open the
extensions page (chrome://extensions or edge://extensions); remove anything
the user did not install. These are the user's own clicks, one at a time.

```card
CARD W-PER-05
COMMAND: GUI: browser notification settings + extensions page — user removes unknown entries
TIER: T0
NORMAL LOOKS LIKE: only extensions the user recognizes; no unknown notification senders.
SUSPICIOUS LOOKS LIKE: unknown extension or notification sender (low/medium) — removing it usually ends the fake alerts; if alerts continue, route to 04-malware-scan.md (NEW chat).
CANNOT TELL WHEN: browser differs from these menus — guide by meaning, note the difference.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 04-malware-scan.md if symptoms persist.
NEVER CONCLUDE: "scare popup = ransomware" — check notifications first.
```

Registry Run-key item instead: capture the exact key with `reg query`
(guided, save output), then Task Manager > Startup apps > right-click >
Disable — same screen reverses it. Never delete registry values.

## Report

Fill the REPORT SKELETON. HANDOFF: confirmed-suspicious item →
`packs/windows/06-removal-and-recovery.md`; else
`packs/windows/04-malware-scan.md` if not yet scanned. NEW chat, HANDOFF first.
