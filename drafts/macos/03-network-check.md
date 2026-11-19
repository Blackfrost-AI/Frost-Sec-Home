---
pack_id: macos-network-check
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

# macOS — network check (home network only)

YOUR network only: your address, devices your Mac has talked to, what on this
Mac listens. Passive first. Never scan networks you do not own or public
ranges.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Mac?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
sw_vers
```

```card
CARD M-NET-00
COMMAND: sw_vers
TIER: T0
NORMAL LOOKS LIKE: macOS 13.x or newer.
SUSPICIOUS LOOKS LIKE: none — this step only confirms identity.
CANNOT TELL WHEN: command not found — not a Mac; stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: anything from this step alone.
```

## Self-check

1. Which step asks about network ownership? (Step 2.)
2. What happens to a neighbor's /24 request? (Refused — not yours.)
3. What does an empty ARP table prove? (Nothing — only "no recent talk".)

## Step 1 — your network address (look-only)

```command
ipconfig getifaddr en0
```

```card
CARD M-NET-01
COMMAND: ipconfig getifaddr en0
TIER: T0
NORMAL LOOKS LIKE: one home address like 192.168.x.x or 10.x.x.x.
SUSPICIOUS LOOKS LIKE: none — facts only.
CANNOT TELL WHEN: empty output — en0 may be unused; try `ipconfig getifaddr en1` once; still empty = not on a network, stop the network part.
EXIT CODES / EXPECTED WARNINGS: empty output exits non-zero — EXPECTED when that interface is down, not a crash.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: "private address means safe".
```

## Step 2 — ownership confirmation (ask)

Say: "I will only look at YOUR home network, the one this Mac is on. Do you
own or manage it? Reply YES to continue." NO or unsure → stop the device
inventory; Step 4 (this Mac only) is still fine. Never accept a user-typed
range — especially someone else's network, even a private-looking one.
macOS here assumes a typical home /24; anything bigger (dorm, CGNAT):
passive-only, explain why.

## Step 3 — devices your Mac has talked to (passive)

```command
arp -a -n
```

```card
CARD M-NET-02
COMMAND: arp -a -n
TIER: T0
NORMAL LOOKS LIKE: a few rows — router (.1), own devices, .255 broadcasts. Passive list, not a scan.
SUSPICIOUS LOOKS LIKE: unrecognized device (low) — check the router list (Step 5); phones randomize addresses; not proof.
CANNOT TELL WHEN: empty table — NORMAL; recent talk only.
EXIT CODES / EXPECTED WARNINGS: "(incomplete)" rows = NORMAL. Paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 5.
NEVER CONCLUDE: "unknown device = hacker" — verify via the router.
```

## Step 4 — what is listening on this Mac (look-only)

```command
lsof -nP -iTCP -sTCP:LISTEN
```

```card
CARD M-NET-03
COMMAND: lsof -nP -iTCP -sTCP:LISTEN
TIER: T0
NORMAL LOOKS LIKE: ControlCe/rapportd (AirPlay), your own dev servers on 127.0.0.1 — normal.
SUSPICIOUS LOOKS LIKE: unknown process listening on *:port (medium) — Step 4b identifies it first.
CANNOT TELL WHEN: without sudo you see only YOUR processes — partial view = CANNOT TELL, never "all clear"; offer SHORT APPROVAL for `sudo lsof -nP -iTCP -sTCP:LISTEN` for the full view.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 4b.
NEVER CONCLUDE: "a listener means infected" — many are normal services.
```

## Step 4b — name the owning process (look-only)

The PID slot byte-matches Step 4's PID number, digits only.

```command
ps -p <PID: digits only, from step 4> -o pid,comm
```

```card
CARD M-NET-04
COMMAND: ps -p <PID: digits only, from step 4> -o pid,comm
TIER: T0
NORMAL LOOKS LIKE: known program path (/Applications, /usr/libexec, homebrew).
SUSPICIOUS LOOKS LIKE: random name from /tmp or /Users/Shared (medium) — 05-persistence-hunt.md (NEW chat).
CANNOT TELL WHEN: process gone — do not chase with invented commands.
EXIT CODES / EXPECTED WARNINGS: empty output = it exited — normal.
NEXT IF SUSPICIOUS: 05-persistence-hunt.md (NEW chat).
NEVER CONCLUDE: "unfamiliar name = malware".
```

## Step 5 — router check (guided, user's own browser)

Guide in a browser: open the router address from Step 3 (usually .1). The
card lists the checks; changes are the user's clicks. Never type the router
password into chat.

```card
CARD M-NET-05
COMMAND: GUI: browser > router address > admin password / firmware / Wi-Fi security / device list
TIER: T0
NORMAL LOOKS LIKE: unique admin password, current firmware, WPA2/WPA3, known devices.
SUSPICIOUS LOOKS LIKE: sticker password (medium), WEP/Open (high), unknown device also in Step 3 (medium) — recommendations; NEEDS A HUMAN for the last one.
CANNOT TELL WHEN: cannot log in — note it, never guess.
EXIT CODES / EXPECTED WARNINGS: pages vary; absent menu → skip, say so.
NEXT IF SUSPICIOUS: recommendations.
NEVER CONCLUDE: "router fine = network safe" — checklist, not audit.
```

## Report

Fill the REPORT SKELETON. HANDOFF: suspicious listener/process →
`packs/macos/05-persistence-hunt.md`; else `packs/macos/04-malware-scan.md`.
NEW chat, HANDOFF state first.
