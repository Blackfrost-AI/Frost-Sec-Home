---
pack_id: windows-network-check
os: windows
os_versions: ["10 22H2", "11"]
shell: powershell
privilege: admin-mixed
pack_type: module
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Windows — network check (home network only)

YOUR network only: your address, devices your PC has talked to, what on this
PC listens. Passive first. Never scan networks you do not own or public
ranges.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Windows PC?" If not, stop and name the right pack.

## Self-check

1. Which networks may this pack ever look at?
2. What must the user confirm before any device inventory?
3. What does a limited (non-admin) view let you conclude?

## Step 1 — your address (look-only)

```command
Get-NetIPAddress -AddressFamily IPv4 | Select-Object IPAddress, PrefixLength, InterfaceAlias
```

```card
CARD W-NET-01
COMMAND: Get-NetIPAddress -AddressFamily IPv4 | Select-Object IPAddress, PrefixLength, InterfaceAlias
TIER: T0
NORMAL LOOKS LIKE: one home address (192.168.x.x / 10.x.x.x), PrefixLength 24 (16-32 ok), on Wi-Fi/Ethernet.
SUSPICIOUS LOOKS LIKE: none — this step only gathers facts.
CANNOT TELL WHEN: only 169.254 or 127.0.0.1 rows — not really on a network; stop the network part.
EXIT CODES / EXPECTED WARNINGS: extra rows (virtual adapters) normal; use Wi-Fi/Ethernet.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: "private address means safe" — just an address.
```

Compute the home range (192.168.1.23/24 → 192.168.1.0/24). SCOPE RULE:
active steps need a private range (192.168.x, 10.x, 172.16-31.x) AND /24 or
smaller. Bigger (dorm /22, CGNAT 100.64.x): passive-only; explain why.

## Step 2 — ownership confirmation (ask)

Say: "I will only look at YOUR home network, range <computed range>. Do you
own or manage it? Reply YES." NO/unsure → stop the inventory; Step 4 (this
PC only) is still fine. Never accept a user-typed public range.

## Step 3 — devices your PC has talked to (passive)

```command
Get-NetNeighbor -AddressFamily IPv4 | Select-Object -First 30 IPAddress, LinkLayerAddress, State
```

```card
CARD W-NET-02
COMMAND: Get-NetNeighbor -AddressFamily IPv4 | Select-Object -First 30 IPAddress, LinkLayerAddress, State
TIER: T0
NORMAL LOOKS LIKE: a few rows — router (.1), own devices, .255 broadcasts. Passive list.
SUSPICIOUS LOOKS LIKE: unrecognized device (low) — check the router list (Step 5); phones randomize addresses; not proof.
CANNOT TELL WHEN: empty table — NORMAL; recent talk only.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 5.
NEVER CONCLUDE: "unknown device = hacker" — verify via the router.
```

## Step 4 — what is listening on this PC (T0-admin)

SHORT APPROVAL: look-only; admin PowerShell sees every process (START-HERE
has steps). Without admin: partial view = CANNOT TELL.

```command
Get-NetTCPConnection -State Listen | Select-Object -First 30 LocalAddress, LocalPort, OwningProcess
```

```card
CARD W-NET-03
COMMAND: Get-NetTCPConnection -State Listen | Select-Object -First 30 LocalAddress, LocalPort, OwningProcess
TIER: T0-admin
NORMAL LOOKS LIKE: modest list; 135/139/445 = Windows sharing, 5357/5358 = discovery — normal at home.
SUSPICIOUS LOOKS LIKE: unusual high port owned by Temp/AppData random-name process (medium) — Step 4b identifies first.
CANNOT TELL WHEN: no admin (partial view) or errors.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 4b.
NEVER CONCLUDE: "port 445 open means infected" — Windows sharing; firewall decides exposure.
```

## Step 4b — name the owning process (look-only)

The PID slot byte-matches Step 4's OwningProcess number.

```command
Get-Process -Id <PID: digits only, from step 4> | Select-Object Name, Path
```

```card
CARD W-NET-04
COMMAND: Get-Process -Id <PID: digits only, from step 4> | Select-Object Name, Path
TIER: T0
NORMAL LOOKS LIKE: known program (browser, game, updater) under Program Files.
SUSPICIOUS LOOKS LIKE: random name from Temp/AppData (medium) — route to 05-persistence-hunt.md (NEW chat).
CANNOT TELL WHEN: process gone or access denied — do not chase with invented commands.
EXIT CODES / EXPECTED WARNINGS: "Cannot find a process with the process identifier" = it exited — normal.
NEXT IF SUSPICIOUS: 05-persistence-hunt.md (NEW chat).
NEVER CONCLUDE: "unfamiliar name = malware" — many legit tools are unfamiliar.
```

## Step 5 — router checklist (guided, manual)

Guide in a browser: open the router address from Step 3 (usually .1). The
card lists the checks; changes are the user's clicks. Never type the router
password into chat.

```card
CARD W-NET-05
COMMAND: GUI: browser > router address from step 3 > password / firmware / WPA2-WPA3 / device list
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
`packs/windows/05-persistence-hunt.md`; else `packs/windows/04-malware-scan.md`.
NEW chat, HANDOFF state first.
