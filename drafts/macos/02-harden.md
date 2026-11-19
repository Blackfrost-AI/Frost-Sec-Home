---
pack_id: macos-harden
os: macos
os_versions: ["13 Ventura", "14 Sonoma", "15 Sequoia"]
shell: zsh
privilege: admin-mixed
pack_type: module
safety_core_version: 3
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# macOS — harden (small, approved changes)

First a backup net (Time Machine), then changes — each needs your YES.
Nothing deletes files or disables security.
## Step 0 — confirm this is the right pack

Ask: "Are you on a Mac?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
sw_vers
```

```card
CARD M-HAR-00
COMMAND: sw_vers
TIER: T0
NORMAL LOOKS LIKE: macOS 13.x or newer.
SUSPICIOUS LOOKS LIKE: 12 or older (medium) — upgrade first (01 pack).
CANNOT TELL WHEN: command not found — not a Mac; stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 01-verify-and-update.md.
NEVER CONCLUDE: "old version means infected".
```
## Self-check

1. What comes before any change? (A backup net — Step 1.)
2. What does FileVault protect against? (Theft of the powered-off Mac.)
3. One YES covers how many commands? (One.)

## Step 1 — backup net: Time Machine (guided, T1)

No restore points on macOS; Time Machine is the way back. FULL APPROVAL.
WHAT: auto backups to an external drive. WHY: recovery net. RISK: first
backup slow; drive fills. UNDO: same screen, stop. Wait for YES; guide:

```card
CARD M-HAR-01
COMMAND: GUI: System Settings > General > Time Machine > Add Backup Disk > choose drive > Set Up Disk
TIER: T1
NORMAL LOOKS LIKE: drive appears, backup starts, auto-backup On.
SUSPICIOUS LOOKS LIKE: no drive — say so plainly; proceed-with-explicit-warning only.
CANNOT TELL WHEN: setup fails — NEEDS A HUMAN if the drive errors.
EXIT CODES / EXPECTED WARNINGS: "erase the disk?" — drive WILL BE ERASED; user confirms nothing needed on it. Recommend encrypt backup On.
NEXT IF SUSPICIOUS: stop or proceed-with-warning.
NEVER CONCLUDE: "no backup = skip safety" — informed choice only.
```

## Step 2 — FileVault (T1)

Check first (look-only):

```command
fdesetup status
```

```card
CARD M-HAR-02
COMMAND: fdesetup status
TIER: T0
NORMAL LOOKS LIKE: "FileVault is On." — skip to Step 3.
SUSPICIOUS LOOKS LIKE: "FileVault is Off" (medium) — Step 2b.
CANNOT TELL WHEN: errors.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: Step 2b.
NEVER CONCLUDE: "off means data already stolen".
```

2b (guided, T1). FULL APPROVAL. WHAT: encrypt the disk. WHY: lost/stolen
powered-off Mac stays unreadable. RISK: first encryption takes hours; LOST
RECOVERY KEY = LOST DATA. UNDO: same screen, Turn Off. Wait for YES; guide:

```card
CARD M-HAR-03
COMMAND: GUI: System Settings > Privacy & Security > FileVault > Turn On > choose recovery method
TIER: T1
NORMAL LOOKS LIKE: "FileVault is turned on for disk..." — background.
SUSPICIOUS LOOKS LIKE: greyed out (policy) — NEEDS A HUMAN.
CANNOT TELL WHEN: layout differs — stop, never improvise.
EXIT CODES / EXPECTED WARNINGS: recovery: iCloud OR written key stored OFF this Mac. Say twice: no key + no iCloud = no recovery.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "slows the Mac forever" — one-time cost.
```

## Step 3 — Gatekeeper (T1-admin)

Look-only check:

```command
spctl --status
```

```card
CARD M-HAR-04
COMMAND: spctl --status
TIER: T0
NORMAL LOOKS LIKE: "assessments enabled" — skip to Step 4.
SUSPICIOUS LOOKS LIKE: "assessments disabled" (high) — Step 3b.
CANNOT TELL WHEN: errors.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: Step 3b.
NEVER CONCLUDE: "disabled means infected" — often user choice.
```

3b (T1-admin). SHORT APPROVAL for admin Terminal (START-HERE), then FULL
APPROVAL. WHAT: re-enable Gatekeeper AND app firewall (one command, one
YES). WHY: block unsigned apps + unwanted incoming connections. RISK:
unsigned apps stop opening (right-click > Open excepts one); apps re-ask
network permission. UNDO: `sudo spctl --global-disable`; socketfilterfw
`--setglobalstate off`. Wait for YES.

```command
sudo spctl --global-enable && sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
```

```card
CARD M-HAR-05
COMMAND: sudo spctl --global-enable && sudo /usr/libexec/ApplicationFirewall/socketfilterfw --setglobalstate on
TIER: T1
NORMAL LOOKS LIKE: "Firewall is enabled."; Steps 3+4 confirm both.
SUSPICIOUS LOOKS LIKE: errors twice — stop, NEEDS A HUMAN.
CANNOT TELL WHEN: sudo unavailable.
EXIT CODES / EXPECTED WARNINGS: password prompt (blind) = NORMAL.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "both on = nothing bad can run" — layers, not guarantees.
```

## Step 4 — verify firewall (look-only)

```command
/usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

```card
CARD M-HAR-06
COMMAND: /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
TIER: T0
NORMAL LOOKS LIKE: "Firewall is enabled. (State = 1)".
SUSPICIOUS LOOKS LIKE: still disabled after 3b (medium) — re-run 3b once, fresh YES; still failing → NEEDS A HUMAN.
CANNOT TELL WHEN: errors.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "firewall off = hacked" — exposed, not evidence.
```

## Report

Fill the REPORT SKELETON: changes + undo. HANDOFF:
`packs/macos/03-network-check.md` in a NEW chat, HANDOFF state first.
