---
pack_id: windows-verify-update
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

# Windows — verify and update

Making sure your PC gets security updates is the single most protective thing
you can do. This pack checks your version, your Defender signature freshness,
and your Windows Update state, then walks you through installing updates.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Windows PC?" If macOS or Linux, stop and name the right
pack (`packs/macos/01-verify-and-update.md` or `packs/linux/01-verify-and-update.md`).
Then run this look-only command (it can take up to a minute — normal):

```command
Get-ComputerInfo | Select-Object WindowsProductName, OsBuildNumber
```

```card
CARD W-UPD-00
COMMAND: Get-ComputerInfo | Select-Object WindowsProductName, OsBuildNumber
TIER: T0
NORMAL LOOKS LIKE: Windows 11 (build 22000+) or Windows 10 22H2 (build 19045).
SUSPICIOUS LOOKS LIKE: Windows 10 at any build (high, exposure not infection): support ended 2025-10-14 and the ESU extra-update period ended 2026-10-13. Say plainly: unless Microsoft extended ESU again, this PC no longer gets security updates; the fix is upgrading to Windows 11 or a supported system, not scanning harder. Build below 19045 on Win10 (high): years of fixes missing.
CANNOT TELL WHEN: Server edition or command error — this pack is for home PCs; stop and say so.
EXIT CODES / EXPECTED WARNINGS: progress bar for 30-60 seconds is normal.
NEXT IF SUSPICIOUS: record NEEDS A HUMAN (upgrade decision) and continue.
NEVER CONCLUDE: "out of date means infected" — exposed is not compromised.
```

## Self-check

1. What must happen before any T1 change?
2. What do you do if a needed command is not in this pack?
3. What must every verdict cite?

## Step 1 — are Defender's signatures fresh? (look-only)

```command
Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated, AntivirusSignatureVersion
```

```card
CARD W-UPD-01
COMMAND: Get-MpComputerStatus | Select-Object AntivirusSignatureLastUpdated, AntivirusSignatureVersion
TIER: T0
NORMAL LOOKS LIKE: signature date within the last 7 days.
SUSPICIOUS LOOKS LIKE: older than 14 days (medium) — updates are not getting through; Step 2's update path usually fixes this.
CANNOT TELL WHEN: command error, or another antivirus is in charge (passive mode) — ask which antivirus the user installed; its own update state is what matters then.
EXIT CODES / EXPECTED WARNINGS: none expected.
NEXT IF SUSPICIOUS: Step 2 (update path).
NEVER CONCLUDE: "old signatures mean malware is present" — it means detection is behind.
```

## Step 2 — install Windows updates (guided, T1)

This is a T1 change done through the Windows Settings app, not a command.
Use the FULL APPROVAL with COMMAND shown as the exact click path below.
WHAT: install pending Windows security updates. WHY: close known security
holes. RISK: the PC may need a restart; save work first; a bad update can
rarely cause problems — Windows keeps the previous state for uninstall.
UNDO: Settings > Windows Update > Update history > Uninstall updates.
Wait for YES, then guide one click at a time:

1. Click Start, then the gear icon (Settings).
2. Click Windows Update.
3. Click Check for updates. Wait for the list.
4. If updates are listed: click Download & install (or Install now).
5. If a restart is offered: tell the user to save all work, then click
   Restart now. Wait for them to come back before continuing.

```card
CARD W-UPD-02
COMMAND: GUI: Settings > Windows Update > Check for updates > Download & install
TIER: T1
NORMAL LOOKS LIKE: "You're up to date" after checking, or updates install and a restart completes.
SUSPICIOUS LOOKS LIKE: updates repeatedly fail with an error code (medium) — note the exact code; two failures in a row = stop per Safety Core and say this needs a human.
CANNOT TELL WHEN: Windows Update says "managed by your organization" on a home PC — CANNOT TELL, note it.
EXIT CODES / EXPECTED WARNINGS: "Some updates need a restart" is normal, not an error.
NEXT IF SUSPICIOUS: stop after two failures; NEEDS A HUMAN with the error code.
NEVER CONCLUDE: "up to date means safe" — it means patched, which is different.
```

## Report

Fill the REPORT SKELETON. HANDOFF: if protection looked off in triage or
signatures were stale and updates are now installed, next pack is
`packs/windows/02-harden.md`; otherwise `packs/windows/03-network-check.md`.
Open it in a NEW chat and paste the HANDOFF state block first.
