---
pack_id: macos-triage
os: macos
os_versions: ["13 Ventura", "14 Sonoma", "15 Sequoia"]
shell: zsh
privilege: user
pack_type: triage
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# macOS triage — your first security check-up

First look at your Mac: version, built-in protection (FileVault, Gatekeeper,
XProtect), ransomware signs, then — only with your YES — an update check and
a look at what is running. Ends by naming the next pack.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Mac?" If unsure: Apple menu > About This Mac. If Windows
or Linux, stop: open `packs/windows/TRIAGE.md` or `packs/linux/TRIAGE.md`.

Then have them run this in Terminal (START-HERE/macos.md shows how) and paste
the output:

```command
sw_vers
```

```card
CARD M-TRI-00
COMMAND: sw_vers
TIER: T0
NORMAL LOOKS LIKE: ProductName: macOS, ProductVersion: 13.x or newer.
SUSPICIOUS LOOKS LIKE: 12 or older (medium) — no more security updates; upgrade via System Settings > General > Software Update.
CANNOT TELL WHEN: command not found — not a Mac; stop, name the right pack.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: upgrade recommendation in report.
NEVER CONCLUDE: "old macOS means infected" — exposed, not infected.
```

## Self-check

1. Which step needs a full YES first? (Step 3, the update check.)
2. What do you do at the first ransomware sign?
3. What does "Gatekeeper enabled" prove? (App checks on — not "no malware".)

## Step 1 — built-in protection (look-only)

Three commands, one at a time; paste each output before the next.

```command
fdesetup status
```

```card
CARD M-TRI-01
COMMAND: fdesetup status
TIER: T0
NORMAL LOOKS LIKE: "FileVault is On."
SUSPICIOUS LOOKS LIKE: "FileVault is Off" (medium) — disk not encrypted; the harden pack turns it on with approval.
CANNOT TELL WHEN: errors — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: handoff to 02-harden.md.
NEVER CONCLUDE: "FileVault off means stolen data" — risk if the Mac is lost, not evidence.
```

```command
spctl --status
```

```card
CARD M-TRI-02
COMMAND: spctl --status
TIER: T0
NORMAL LOOKS LIKE: "assessments enabled" — Gatekeeper checks apps.
SUSPICIOUS LOOKS LIKE: "assessments disabled" (high) — unsigned apps can run; harden pack re-enables with approval.
CANNOT TELL WHEN: errors — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: handoff to 02-harden.md.
NEVER CONCLUDE: "Gatekeeper on means no malware" — signed malware exists.
```

```command
system_profiler SPInstallHistoryDataType | grep -A3 XProtectPlistConfigData | head -8
```

```card
CARD M-TRI-03
COMMAND: system_profiler SPInstallHistoryDataType | grep -A3 XProtectPlistConfigData | head -8
TIER: T0
NORMAL LOOKS LIKE: XProtectPlistConfigData rows, Source: Apple, recent dates — the silent antivirus updates itself.
SUSPICIOUS LOOKS LIKE: no rows, or newest entry years old (low) — check Software Update settings (01 pack).
CANNOT TELL WHEN: output empty or errors — CANNOT TELL; XProtect may update via a different channel.
EXIT CODES / EXPECTED WARNINGS: can take ~30 seconds; that is NORMAL. Paste only the first 8 lines.
NEXT IF SUSPICIOUS: 01-verify-and-update.md.
NEVER CONCLUDE: "XProtect replaces careful habits" — it is one layer.
```

## Step 2 — ransomware signs (ask, no command)

Ask: "Do you see a message demanding money to unlock files, or many files
with a strange new ending?" If YES to both signs: INCIDENT BLOCK now, then
`packs/macos/INCIDENT-RANSOMWARE.md` in a NEW chat. One odd file is not an
incident — the INCIDENT pack verifies.

## Step 3 — check for updates (T1, needs your YES)

T1: it contacts Apple's update servers and can take minutes. FULL APPROVAL.
WHAT: list available macOS updates. WHY: patches close known holes. RISK:
none to files; uses network. UNDO: none needed — listing only. Wait for YES.

```command
softwareupdate --list
```

```card
CARD M-TRI-04
COMMAND: softwareupdate --list
TIER: T1
NORMAL LOOKS LIKE: "No new software available." or a list of updates.
SUSPICIOUS LOOKS LIKE: security updates pending (medium) — install via System Settings > Software Update (01 pack guides).
CANNOT TELL WHEN: network errors — CANNOT TELL, not "up to date".
EXIT CODES / EXPECTED WARNINGS: "Finding available software" then a wait = NORMAL. Can take minutes.
NEXT IF SUSPICIOUS: 01-verify-and-update.md.
NEVER CONCLUDE: "no updates listed means fully patched" — only Apple's catalog was checked.
```

## Step 4 — what is running hardest (look-only)

```command
ps aux -r | head -12
```

```card
CARD M-TRI-05
COMMAND: ps aux -r | head -12
TIER: T0
NORMAL LOOKS LIKE: known apps (browser, WindowServer, Terminal); high CPU while working is normal.
SUSPICIOUS LOOKS LIKE: random-name process from /tmp, /Users/Shared, or a hidden folder eating CPU (medium) — 05-persistence-hunt.md identifies it.
CANNOT TELL WHEN: unfamiliar names — not proof; check before judging.
EXIT CODES / EXPECTED WARNINGS: paste only the first 12 lines.
NEXT IF SUSPICIOUS: 05-persistence-hunt.md (NEW chat).
NEVER CONCLUDE: "high CPU = malware" — video calls and backups do that too.
```

## Step 5 — lock screen + sharing review (guided, T0)

Read-only review; recommendations only, never changes here:

```card
CARD M-TRI-06
COMMAND: GUI: System Settings > Lock Screen / General > Sharing — read-only
TIER: T0
NORMAL LOOKS LIKE: password after sleep ≤ 1 min; only needed sharing On.
SUSPICIOUS LOOKS LIKE: no password on wake (low); Screen Sharing/Remote Login On without the user knowing why (medium) — recommendations; unrecognized remote access → NEEDS A HUMAN.
CANNOT TELL WHEN: pane not found — note it, move on.
EXIT CODES / EXPECTED WARNINGS: pane names vary by version.
NEXT IF SUSPICIOUS: recommendations in report.
NEVER CONCLUDE: "sharing on means compromised" — could be their own setup.
```

## Report

Fill the REPORT SKELETON. HANDOFF:
- Ransomware signs → `packs/macos/INCIDENT-RANSOMWARE.md` (NEW chat).
- Protection off / updates pending → `packs/macos/02-harden.md` or `01-verify-and-update.md`.
- Suspicious process → `packs/macos/05-persistence-hunt.md`.
- All calm → `packs/macos/03-network-check.md`.
NEW chat, HANDOFF state first.
