---
pack_id: macos-verify-update
os: macos
os_versions: ["13 Ventura", "14 Sonoma", "15 Sequoia"]
shell: zsh
privilege: admin-mixed
pack_type: module
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# macOS — verify and update

Confirm your Mac's version, then install security updates with your YES.
macOS has no built-in backup tool command here — Time Machine setup is
guided in the harden pack. Updates first, always.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Mac?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
sw_vers
```

```card
CARD M-UPD-00
COMMAND: sw_vers
TIER: T0
NORMAL LOOKS LIKE: macOS 13.x or newer.
SUSPICIOUS LOOKS LIKE: 12 or older (medium) — out of support; upgrade is the fix, not patches.
CANNOT TELL WHEN: command not found — not a Mac; stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: upgrade recommendation.
NEVER CONCLUDE: "old version means infected".
```

## Self-check

1. Which steps contact Apple's servers? (1 and 2.)
2. What must the user save before a macOS upgrade? (Their work; a backup.)
3. What does a failed update check mean? (CANNOT TELL — never "up to date".)

## Step 1 — list available updates (T1)

FULL APPROVAL. WHAT: ask Apple's servers which updates exist. WHY: security
patches close known holes. RISK: network use, minutes of waiting; changes
nothing. UNDO: none needed — listing only. Wait for YES.

```command
softwareupdate --list
```

```card
CARD M-UPD-01
COMMAND: softwareupdate --list
TIER: T1
NORMAL LOOKS LIKE: "No new software available." or a numbered list.
SUSPICIOUS LOOKS LIKE: security updates pending (medium) — Step 2 or System Settings.
CANNOT TELL WHEN: network errors — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: "Finding available software" + wait = NORMAL.
NEXT IF SUSPICIOUS: Step 2.
NEVER CONCLUDE: "empty list = fully secure" — one channel checked.
```

## Step 2 — install updates (T1, may restart)

Prefer the guided path: System Settings > General > Software Update >
Update Now — the user sees progress and restart prompts. Command path only
if the user asks. FULL APPROVAL. WHAT: download and install the listed
updates. WHY: close known holes. RISK: minutes to an hour; MAY RESTART —
save all work first. UNDO: none — updates are not rolled back here. Wait
for YES; confirm work saved.

```command
sudo softwareupdate --install --all --restart
```

```card
CARD M-UPD-02
COMMAND: sudo softwareupdate --install --all --restart
TIER: T1
NORMAL LOOKS LIKE: download/install progress, then restart if needed.
SUSPICIOUS LOOKS LIKE: repeated failures (medium) — stop after two tries; NEEDS A HUMAN.
CANNOT TELL WHEN: hangs >30 min — CANNOT TELL; do not force-power-off mid-install.
EXIT CODES / EXPECTED WARNINGS: sudo asks for the login password (typed blind) = NORMAL. Restart is EXPECTED.
NEXT IF SUSPICIOUS: stop, NEEDS A HUMAN.
NEVER CONCLUDE: "restart means it broke" — planned restart.
```

## Step 3 — automatic updates on (guided, T1)

FULL APPROVAL. WHAT: turn on automatic updates. WHY: patches arrive without
remembering. RISK: occasional restart prompts. UNDO: same screen, off.
Wait for YES, then guide:

```card
CARD M-UPD-03
COMMAND: GUI: System Settings > General > Software Update > Automatic Updates (i) > all toggles On
TIER: T1
NORMAL LOOKS LIKE: "Download new updates when available", "Install macOS updates", "Install security responses" all On.
SUSPICIOUS LOOKS LIKE: toggles greyed out (policy) — CANNOT TELL; NEEDS A HUMAN.
CANNOT TELL WHEN: layout differs — stop, never improvise.
EXIT CODES / EXPECTED WARNINGS: wording varies slightly by version.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "auto-update on = never needs checking" — still verify monthly.
```

## Step 4 — XProtect freshness (look-only)

```command
system_profiler SPInstallHistoryDataType | grep -A3 XProtectPlistConfigData | head -8
```

```card
CARD M-UPD-04
COMMAND: system_profiler SPInstallHistoryDataType | grep -A3 XProtectPlistConfigData | head -8
TIER: T0
NORMAL LOOKS LIKE: recent Apple entries — XProtect updates silently.
SUSPICIOUS LOOKS LIKE: newest entry years old (low) — Step 3 settings.
CANNOT TELL WHEN: empty/errors — CANNOT TELL; other update channels exist.
EXIT CODES / EXPECTED WARNINGS: ~30 seconds = NORMAL. Paste only the first 8 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "XProtect current = no malware".
```

## Report

Fill the REPORT SKELETON: updates installed, settings changed + undo.
HANDOFF: `packs/macos/02-harden.md` in a NEW chat, HANDOFF state first.
