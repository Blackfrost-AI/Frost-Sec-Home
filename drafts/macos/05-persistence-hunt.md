---
pack_id: macos-persistence-hunt
os: macos
os_versions: ["13 Ventura", "14 Sonoma", "15 Sequoia"]
shell: zsh
privilege: user
pack_type: module
safety_core_version: 3
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# macOS — persistence hunt (what starts itself)

Launch agents/daemons, login items, cron, hosts file. Look-only; suspicious
items get verified, never deleted on a hunch. Many legit programs live here.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Mac?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
sw_vers
```

```card
CARD M-PER-00
COMMAND: sw_vers
TIER: T0
NORMAL LOOKS LIKE: macOS 13.x or newer.
SUSPICIOUS LOOKS LIKE: none — identity only.
CANNOT TELL WHEN: command not found — not a Mac; stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: anything from identity alone.
```

## Self-check

1. Where do per-user startup items live? (~/Library/LaunchAgents.)
2. What does a plist's ProgramArguments tell you? (What actually runs.)
3. What do you do with a suspicious item? (Record + verify; gated disable in 06.)

## Step 1 — your startup items (look-only)

```command
ls -la ~/Library/LaunchAgents
```

```card
CARD M-PER-01
COMMAND: ls -la ~/Library/LaunchAgents
TIER: T0
NORMAL LOOKS LIKE: plist files named like com.vendor.product — updaters, sync tools. Dozens is normal.
SUSPICIOUS LOOKS LIKE: random-string names, or plists pointing into /tmp, /Users/Shared, hidden folders (medium) — Step 3 reads one.
CANNOT TELL WHEN: "No such file or directory" — NORMAL, folder may not exist.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "many items = infected" — normal Macs have many.
```

## Step 2 — system-wide startup items (look-only)

```command
ls -la /Library/LaunchAgents /Library/LaunchDaemons
```

```card
CARD M-PER-02
COMMAND: ls -la /Library/LaunchAgents /Library/LaunchDaemons
TIER: T0
NORMAL LOOKS LIKE: vendor-named plists — security tools, drivers, updaters.
SUSPICIOUS LOOKS LIKE: random-string names or unknown vendors (medium) — Step 3.
CANNOT TELL WHEN: errors — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "unknown vendor = malware" — small legit vendors exist.
```

## Step 3 — read ONE item's definition (look-only)

The PATH slot byte-matches the plist path from Step 1 or 2.

```command
plutil -p <PATH: plist path from step 1 or 2, from step 1>
```

```card
CARD M-PER-03
COMMAND: plutil -p <PATH: plist path from step 1 or 2, from step 1>
TIER: T0
NORMAL LOOKS LIKE: ProgramArguments points into /Applications or /Library for a known product; RunAtLoad true is normal.
SUSPICIOUS LOOKS LIKE: program in /tmp, /Users/Shared, or a random-name binary (medium/high) — record; gated disable in 06-removal-and-recovery.md (NEW chat).
CANNOT TELL WHEN: unreadable plist — CANNOT TELL; do not guess contents.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 06-removal-and-recovery.md (NEW chat).
NEVER CONCLUDE: "RunAtLoad = malicious" — it just means start at login.
```

## Step 4 — login items (guided, read-only)

```card
CARD M-PER-04
COMMAND: GUI: System Settings > General > Login Items & Extensions — read-only
TIER: T0
NORMAL LOOKS LIKE: apps the user recognizes; "Allow in the Background" helpers from known vendors.
SUSPICIOUS LOOKS LIKE: unknown item, especially "item from unidentified developer" (medium) — record; user may toggle it Off themselves (their click, reversible).
CANNOT TELL WHEN: pane differs by version — note it, move on.
EXIT CODES / EXPECTED WARNINGS: macOS 13 names it "Login Items".
NEXT IF SUSPICIOUS: record; 06 if confirmed.
NEVER CONCLUDE: "unknown login item = malware" — verify first.
```

## Step 5 — cron jobs (look-only)

```command
crontab -l
```

```card
CARD M-PER-05
COMMAND: crontab -l
TIER: T0
NORMAL LOOKS LIKE: "crontab: no crontab for <user>" — most users have none.
SUSPICIOUS LOOKS LIKE: entries the user never created, especially curl/wget piping to sh (high) — record; NEEDS A HUMAN.
CANNOT TELL WHEN: errors other than "no crontab" — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: "no crontab for" exits 1 — EXPECTED, not a failure.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "cron exists = infected" — admins use cron legitimately.
```

## Step 6 — hosts file (look-only)

```command
cat /etc/hosts
```

```card
CARD M-PER-06
COMMAND: cat /etc/hosts
TIER: T0
NORMAL LOOKS LIKE: localhost lines (127.0.0.1, ::1) and maybe a few user-added blocks.
SUSPICIOUS LOOKS LIKE: entries redirecting apple.com, icloud.com, or update domains elsewhere (high) — possible tampering; NEEDS A HUMAN.
CANNOT TELL WHEN: unfamiliar entries the user may have added — ask before judging.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "custom hosts = malware" — ad-blocking uses it too.
```

## Report

Fill the REPORT SKELETON. HANDOFF: confirmed-suspicious item →
`packs/macos/06-removal-and-recovery.md`; else `packs/macos/04-malware-scan.md`
if not yet run. NEW chat, HANDOFF first.
