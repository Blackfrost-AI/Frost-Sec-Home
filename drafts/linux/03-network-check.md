---
pack_id: linux-network-check
os: linux
os_versions: ["Ubuntu 22.04/24.04 LTS", "Fedora 40+", "Arch (rolling)"]
shell: bash
privilege: admin-mixed
pack_type: module
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Linux — network check (home network only)

YOUR network only: your address, devices your PC has talked to, what this
PC listens on. Passive first. Never scan networks you do not own.

## Step 0 — confirm this is the right pack

Ask: "Are you on Linux?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
cat /etc/os-release
```

```card
CARD L-NET-00
COMMAND: cat /etc/os-release
TIER: T0
NORMAL LOOKS LIKE: NAME/VERSION_ID lines.
SUSPICIOUS LOOKS LIKE: none — identity only.
CANNOT TELL WHEN: file missing — ask which distro; unknown → stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: anything from identity alone.
```

## Self-check

1. Which step asks about network ownership? (Step 2.)
2. What happens to a neighbor's /24 request? (Refused — not yours.)
3. What does an empty neighbor table prove? (Nothing — "no recent talk".)

## Step 1 — your network address (look-only)

```command
ip addr
```

```card
CARD L-NET-01
COMMAND: ip addr
TIER: T0
NORMAL LOOKS LIKE: one home address (192.168.x.x/24, 10.x.x.x/24) on eth/wlan; lo normal.
SUSPICIOUS LOOKS LIKE: none — facts only.
CANNOT TELL WHEN: command not found — offer `hostname -I` once. Only 169.254/127 rows = not on a network; stop the network part.
EXIT CODES / EXPECTED WARNINGS: docker0/veth interfaces NORMAL; use the physical one. Paste only the first 30 lines.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: "private address means safe".
```

## Step 2 — ownership confirmation (ask)

Compute the home range (192.168.1.23/24 → 192.168.1.0/24). SCOPE RULE:
active steps need a private range (192.168.x, 10.x, 172.16-31.x) AND /24 or
smaller. Bigger (dorm /22, CGNAT 100.64.x): passive-only; explain why. Say:
"I will only look at YOUR home network, range <computed range>. Do you own
it? Reply YES." NO/unsure → stop the inventory; Step 4 (this PC only) is
still fine. Never accept a user-typed range.

## Step 3 — devices your PC has talked to (passive)

```command
ip neigh
```

```card
CARD L-NET-02
COMMAND: ip neigh
TIER: T0
NORMAL LOOKS LIKE: a few rows — router (.1), own devices; REACHABLE/STALE normal. Passive list.
SUSPICIOUS LOOKS LIKE: unrecognized device (low) — check the router list (Step 5); phones randomize addresses.
CANNOT TELL WHEN: empty — NORMAL; recent talk only. Command missing = CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: FAILED rows NORMAL. Paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 5.
NEVER CONCLUDE: "unknown device = hacker" — verify via the router.
```

## Step 4 — what is listening on this PC (T0-admin)

SHORT APPROVAL: look-only; sudo shows every process. Without it some rows
hide the owner = partial view = CANNOT TELL.

```command
sudo ss -tulpn
```

```card
CARD L-NET-03
COMMAND: sudo ss -tulpn
TIER: T0-admin
NORMAL LOOKS LIKE: modest list; 127.0.0.1:631 = printing, 53 = local DNS, own dev servers — normal.
SUSPICIOUS LOOKS LIKE: unknown process on 0.0.0.0 or * (medium) — Step 4b identifies first.
CANNOT TELL WHEN: command not found — offer `netstat -tulpn` once if present.
EXIT CODES / EXPECTED WARNINGS: password prompt NORMAL. Paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 4b.
NEVER CONCLUDE: "a listener means infected" — many are normal services.
```

## Step 4b — name the owning process (look-only)

```command
ps -p <PID: digits only, from step 4> -o pid,comm,args
```

```card
CARD L-NET-04
COMMAND: ps -p <PID: digits only, from step 4> -o pid,comm,args
TIER: T0
NORMAL LOOKS LIKE: known program (/usr/bin, /usr/lib, snap/flatpak paths).
SUSPICIOUS LOOKS LIKE: random name from /tmp, /var/tmp, /dev/shm (medium) — 05-persistence-hunt.md (NEW chat).
CANNOT TELL WHEN: process gone — do not chase with invented commands.
EXIT CODES / EXPECTED WARNINGS: empty output = it exited — normal.
NEXT IF SUSPICIOUS: 05-persistence-hunt.md (NEW chat).
NEVER CONCLUDE: "unfamiliar name = malware".
```

## Step 5 — router check (guided, user's own browser)

Open the router address from Step 3 (usually .1) in a browser; checks are
the card's list, changes are the user's clicks. Never type the router
password into chat.

```card
CARD L-NET-05
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
`packs/linux/05-persistence-hunt.md`; else `packs/linux/04-malware-scan.md`.
NEW chat, HANDOFF state first.
