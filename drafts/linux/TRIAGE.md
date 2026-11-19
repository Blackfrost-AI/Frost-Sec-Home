---
pack_id: linux-triage
os: linux
os_versions: ["Ubuntu 22.04/24.04 LTS", "Fedora 40+", "Arch (rolling)"]
shell: bash
privilege: user
pack_type: triage
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Linux triage — your first security check-up

First look at your Linux PC: which distribution, firewall, ransomware signs,
then — only with your YES — an update check and a look at what is running.
Ends by naming the next pack.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Linux PC (Ubuntu, Fedora, Arch, or similar)?" If Windows
or Mac, stop: open `packs/windows/TRIAGE.md` or `packs/macos/TRIAGE.md`.
Then have them run this in a terminal and paste the output:

```command
cat /etc/os-release
```

```card
CARD L-TRI-00
COMMAND: cat /etc/os-release
TIER: T0
NORMAL LOOKS LIKE: NAME/VERSION_ID lines — Ubuntu, Fedora, Debian, Arch, etc. Note the family: apt (Ubuntu/Debian), dnf (Fedora), pacman (Arch).
SUSPICIOUS LOOKS LIKE: very old version (medium) — no more security updates; upgrade is the fix.
CANNOT TELL WHEN: file missing — unusual distro; ask which one, adapt package steps or stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: upgrade recommendation in report.
NEVER CONCLUDE: "old version means infected" — exposed, not infected.
```

## Self-check

1. Which step needs a full YES first? (Step 3, the update check.)
2. What do you do at the first ransomware sign?
3. What does "firewall active" prove? (Filtering on — not "no malware".)

## Step 1 — firewall status (look-only)

Ubuntu/Debian use ufw; Fedora uses firewalld. Run the one for your family
(from Step 0); if the command is missing, that is CANNOT TELL, not "off".

```command
sudo ufw status
```

```card
CARD L-TRI-01
COMMAND: sudo ufw status
TIER: T0-admin
NORMAL LOOKS LIKE: "Status: active" with a few rules.
SUSPICIOUS LOOKS LIKE: "Status: inactive" (medium) — harden pack enables it with approval.
CANNOT TELL WHEN: "command not found" — not ufw-based; Fedora: `sudo firewall-cmd --state` instead; errors in containers/servers without netfilter rights = CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: sudo password prompt (typed blind) = NORMAL. "you must be root" errors = need admin terminal.
NEXT IF SUSPICIOUS: handoff to 02-harden.md.
NEVER CONCLUDE: "firewall off means hacked" — exposed, not evidence.
```

## Step 2 — ransomware signs (ask, no command)

Ask: "Do you see a message demanding money to unlock files, or many files
with a strange new ending?" If YES to both signs: INCIDENT BLOCK now, then
`packs/linux/INCIDENT-RANSOMWARE.md` in a NEW chat. One odd file is not an
incident — the INCIDENT pack verifies.

## Step 3 — check for updates (T1, needs your YES)

T1: it contacts your distro's update servers. FULL APPROVAL. WHAT: refresh
the package list and show what would upgrade. WHY: patches close known
holes. RISK: network use; changes nothing (simulate mode). UNDO: none
needed. Wait for YES. Run the line for your family:

```command
sudo apt-get update && apt-get -s upgrade
```

```card
CARD L-TRI-02
COMMAND: sudo apt-get update && apt-get -s upgrade
TIER: T1
NORMAL LOOKS LIKE: "0 upgraded, 0 newly installed" or a short list. Fedora: `dnf check-update`; Arch: `checkupdates` (no sudo).
SUSPICIOUS LOOKS LIKE: many security updates pending (medium) — 01 pack installs with approval.
CANNOT TELL WHEN: network errors — CANNOT TELL, not "up to date".
EXIT CODES / EXPECTED WARNINGS: dnf check-update exits 100 when updates EXIST — that is SUCCESS, not failure. apt -s = simulate, installs nothing.
NEXT IF SUSPICIOUS: 01-verify-and-update.md.
NEVER CONCLUDE: "nothing listed means fully patched" — one channel checked.
```

## Step 4 — what is running hardest (look-only)

```command
ps aux --sort=-%cpu | head -12
```

```card
CARD L-TRI-03
COMMAND: ps aux --sort=-%cpu | head -12
TIER: T0
NORMAL LOOKS LIKE: known programs (browser, desktop, terminal); busy while working is normal.
SUSPICIOUS LOOKS LIKE: random-name process from /tmp, /var/tmp, or /dev/shm eating CPU (medium) — 05-persistence-hunt.md identifies it.
CANNOT TELL WHEN: unfamiliar names — not proof; check before judging.
EXIT CODES / EXPECTED WARNINGS: paste only the first 12 lines.
NEXT IF SUSPICIOUS: 05-persistence-hunt.md (NEW chat).
NEVER CONCLUDE: "high CPU = malware" — compiles and backups do that too.
```

## Step 5 — lock screen + remote access review (guided, T0)

Read-only review; recommendations only, never changes here:

```card
CARD L-TRI-04
COMMAND: GUI: Settings > Privacy/Power (screen lock) + `systemctl is-enabled ssh` in terminal — read-only
TIER: T0
NORMAL LOOKS LIKE: screen locks ≤ 5 min; ssh disabled unless the user uses it on purpose.
SUSPICIOUS LOOKS LIKE: no lock (low); ssh enabled and the user never set it up (medium) — recommendations; unrecognized remote access → NEEDS A HUMAN.
CANNOT TELL WHEN: settings differ by desktop (GNOME/KDE) — note it, move on; "Failed to get unit file state" = ssh not installed = NORMAL.
EXIT CODES / EXPECTED WARNINGS: systemctl absent (containers) = CANNOT TELL for that part.
NEXT IF SUSPICIOUS: recommendations in report.
NEVER CONCLUDE: "ssh on means compromised" — could be their own setup.
```

## Report

Fill the REPORT SKELETON. HANDOFF:
- Ransomware signs → `packs/linux/INCIDENT-RANSOMWARE.md` (NEW chat).
- Firewall off / updates pending → `packs/linux/02-harden.md` or `01-verify-and-update.md`.
- Suspicious process → `packs/linux/05-persistence-hunt.md`.
- All calm → `packs/linux/03-network-check.md`.
NEW chat, HANDOFF state first.
