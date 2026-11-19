---
pack_id: macos-removal-recovery
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

# macOS — removal and recovery (careful, gated, reversible)

CONFIRMED findings only. Every change: full approval, one at a time, saved
capture as undo. Never bulk-delete or `rm -rf`. Ransomware (note + renamed
files) → INCIDENT-RANSOMWARE.md.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Mac?" If not, name the right pack. Ask what was confirmed
(rejected app signature or suspicious launch item); have the user paste the
exact app/plist path(s). Nothing confirmed → stop; no speculative cleanup.

```command
sw_vers
```

```card
CARD M-REM-00
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

1. What must exist before any change? (Time Machine backup or explicit warning.)
2. Where does a removed app go first? (Trash — recoverable.)
3. When does this pack refuse and hand off? (Ransomware signs.)

## Step 1 — backup net first (guided, T1)

FULL APPROVAL. WHAT: confirm a recent Time Machine backup. WHY: the way
back. RISK: none — checking. UNDO: it is the undo. Wait for YES; guide:
System Settings > General > Time Machine — latest backup date recent. If
none: say so plainly; continue only with explicit informed YES that there
is no rollback net.

```card
CARD M-REM-01
COMMAND: GUI: System Settings > General > Time Machine — check latest backup date
TIER: T1
NORMAL LOOKS LIKE: backup within a day or two.
SUSPICIOUS LOOKS LIKE: no backup / very old (medium) — offer Back Up Now first (their click).
CANNOT TELL WHEN: no drive — explicit informed YES to proceed without a net.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: Back Up Now, then continue.
NEVER CONCLUDE: "no backup = skip the net silently".
```

## Step 2 — quarantine ONE confirmed app (T1, Trash not delete)

Only an app confirmed in the malware pack (rejected signature + user never
installed it). FULL APPROVAL. WHAT: move this one app to Trash. WHY: Trash
is reversible; deletion is not. RISK: if legit, restore from Trash. UNDO:
Trash > right-click > Put Back. Wait for YES.

```command
mv -n "<PATH: confirmed app path, from step 0>" ~/.Trash/
```

```card
CARD M-REM-02
COMMAND: mv -n "<PATH: confirmed app path, from step 0>" ~/.Trash/
TIER: T1
NORMAL LOOKS LIKE: no output; app in Trash, gone from /Applications.
SUSPICIOUS LOOKS LIKE: "Permission denied" (medium) — Finder drag to Trash (asks password) instead of sudo rm.
CANNOT TELL WHEN: errors twice — stop, NEEDS A HUMAN.
EXIT CODES / EXPECTED WARNINGS: none. `-n` never overwrites: app still in place = name collision in Trash — stop; rename with today's date, retry once.
NEXT IF SUSPICIOUS: Finder path, or stop.
NEVER CONCLUDE: "Trash = gone forever" — empty Trash only when sure, days later.
```

## Step 3 — disable ONE confirmed launch item (capture first)

Only an item verified in the persistence pack. TWO gated actions, each with
its own YES.
3a (look-only capture — the undo):

```command
plutil -p "<PATH: verified plist path, from step 0>"
```

```card
CARD M-REM-03
COMMAND: plutil -p "<PATH: verified plist path, from step 0>"
TIER: T0
NORMAL LOOKS LIKE: definition prints. User saves it as frost-sec-undo-item.txt — the undo.
SUSPICIOUS LOOKS LIKE: n/a — capture step.
CANNOT TELL WHEN: file not found — stop; disable nothing.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 3b only after the capture is saved.
NEVER CONCLUDE: "rebuild from memory" — the saved copy is the only undo.
```

3b (T1). FULL APPROVAL. WHAT: unload this one plist, move it to Trash. WHY:
verified suspicious. RISK: if legit, that helper stops starting. UNDO: Put
Back + re-login (guided). Wait for YES.

```command
launchctl unload "<PATH: verified plist path, from step 0>" && mv -n "<PATH: verified plist path, from step 0>" ~/.Trash/
```

```card
CARD M-REM-04
COMMAND: launchctl unload "<PATH: verified plist path, from step 0>" && mv -n "<PATH: verified plist path, from step 0>" ~/.Trash/
TIER: T1
NORMAL LOOKS LIKE: no output; plist in Trash; gone after re-login.
SUSPICIOUS LOOKS LIKE: "Unload failed" / permission denied (medium) — system location; guided Finder drag to Trash (password prompt), never sudo rm.
CANNOT TELL WHEN: errors twice — stop, NEEDS A HUMAN.
EXIT CODES / EXPECTED WARNINGS: "service not loaded" = already off — NORMAL. `-n` never overwrites: still in place = name collision — stop; rename with today's date, retry once.
NEXT IF SUSPICIOUS: guided Finder path, or stop.
NEVER CONCLUDE: "unloaded = deleted" — file sits in Trash, recoverable.
```

Login item instead? System Settings > General > Login Items — user toggles
Off (their click, same screen reverses).

## Step 4 — if it comes back

Item reappears or spreads: stop — beyond this pack, NEEDS A HUMAN. No mass
deletion. Record what returned, when, where.

## Report

Fill the REPORT SKELETON: changes, captures, undo. HANDOFF: re-run
`packs/macos/04-malware-scan.md` (NEW chat) to confirm; anything unclear →
NEEDS A HUMAN. Ransomware signs → INCIDENT-RANSOMWARE.md, NEW chat.
