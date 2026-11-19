---
pack_id: linux-harden
os: linux
os_versions: ["Ubuntu 22.04/24.04 LTS", "Fedora 40+", "Arch (rolling)"]
shell: bash
privilege: admin-mixed
pack_type: module
safety_core_version: 3
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Linux — harden (small, approved changes)

First a backup net, then changes — each needs your YES. Nothing deletes
files or disables security. Pick your family's line: apt/dnf/pacman.

## Step 0 — confirm this is the right pack

Ask: "Are you on Linux?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
cat /etc/os-release
```

```card
CARD L-HAR-00
COMMAND: cat /etc/os-release
TIER: T0
NORMAL LOOKS LIKE: NAME/VERSION_ID; note the family.
SUSPICIOUS LOOKS LIKE: end-of-life version (medium) — upgrade first (01 pack).
CANNOT TELL WHEN: file missing — ask; unknown distro → stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 01-verify-and-update.md.
NEVER CONCLUDE: "old version means infected".
```

## Self-check

1. What comes before any change? (A backup net — Step 1.)
2. What is the ONE risk of enabling ufw remotely? (Locking yourself out of SSH.)
3. One YES covers how many commands? (One.)

## Step 1 — backup net (guided, T1)

Linux has no universal restore point. FULL APPROVAL. WHAT: set up a backup
of personal files to an external drive. WHY: the way back. RISK: first
backup slow; drive fills. UNDO: stop the backup job. Wait for YES; guide:
Ubuntu GNOME: Settings/Apps > Backups (Déjà Dup) > choose drive > schedule.
Other desktops: their backup tool, or the user's own `rsync` habit — their
choice. No drive available: say so plainly; continue only with explicit
informed YES that there is no rollback net. Never skip silently.

```card
CARD L-HAR-01
COMMAND: GUI: Backups (Déjà Dup) or distro backup tool > external drive > schedule
TIER: T1
NORMAL LOOKS LIKE: backup job configured, first run starts.
SUSPICIOUS LOOKS LIKE: no drive — proceed-with-explicit-warning only.
CANNOT TELL WHEN: tool missing — recommend the user's own copy habit; note the gap.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: stop or proceed-with-warning.
NEVER CONCLUDE: "no backup = skip safety" — informed choice only.
```

## Step 2 — firewall (T1-admin)

Check first (look-only):

```command
sudo ufw status
```

```card
CARD L-HAR-02
COMMAND: sudo ufw status
TIER: T0-admin
NORMAL LOOKS LIKE: "Status: active" — skip to Step 3. Fedora: `sudo firewall-cmd --state` shows "running".
SUSPICIOUS LOOKS LIKE: "Status: inactive" (medium) — Step 2b.
CANNOT TELL WHEN: command not found — Fedora uses firewalld (usually on by default); containers/netfilter errors = CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: password prompt (blind) = NORMAL.
NEXT IF SUSPICIOUS: Step 2b.
NEVER CONCLUDE: "off means hacked" — exposed, not evidence.
```

2b (T1-admin). FULL APPROVAL. WHAT: enable ufw with default-deny incoming.
WHY: block unwanted connections. RISK: IF THE USER CONNECTS TO THIS PC VIA
SSH, enabling without an allow rule LOCKS THEM OUT — ask first; if yes, run
`sudo ufw allow ssh` as its own approved command BEFORE enabling. UNDO:
`sudo ufw disable`. Wait for YES.

```command
sudo ufw enable
```

```card
CARD L-HAR-03
COMMAND: sudo ufw enable
TIER: T1
NORMAL LOOKS LIKE: "Firewall is active and enabled on system startup".
SUSPICIOUS LOOKS LIKE: errors twice — stop, NEEDS A HUMAN.
CANNOT TELL WHEN: netfilter permission errors (containers) — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: "Command may disrupt existing ssh connections" warning = EXPECTED; the ssh allow rule must already be in place.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "firewall on = invisible" — reduced exposure, not a guarantee.
```

## Step 3 — full-disk encryption check (look-only)

```command
lsblk -f
```

```card
CARD L-HAR-04
COMMAND: lsblk -f
TIER: T0
NORMAL LOOKS LIKE: partitions listed; crypto_LUKS rows = encrypted.
SUSPICIOUS LOOKS LIKE: no LUKS on a laptop (low/medium) — recommendation: encrypt at NEXT reinstall; converting in place is risky, not done here.
CANNOT TELL WHEN: lsblk missing — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: recommendation in report.
NEVER CONCLUDE: "no encryption = stolen data" — risk if lost, not evidence.
```

## Step 4 — screen lock + sharing review (guided, T0)

```card
CARD L-HAR-05
COMMAND: GUI: Settings > Privacy/Power (lock ≤ 5 min) + `systemctl is-enabled ssh` — read-only
TIER: T0
NORMAL LOOKS LIKE: lock on; ssh disabled unless used on purpose.
SUSPICIOUS LOOKS LIKE: no lock (low); ssh on without the user knowing why (medium) — recommendations; unrecognized remote access → NEEDS A HUMAN.
CANNOT TELL WHEN: desktop differs — note it, move on; "Failed to get unit file state" = not installed = NORMAL.
EXIT CODES / EXPECTED WARNINGS: systemctl absent = CANNOT TELL for that part.
NEXT IF SUSPICIOUS: recommendations in report.
NEVER CONCLUDE: "ssh on = compromised".
```

## Report

Fill the REPORT SKELETON: changes + undo. HANDOFF:
`packs/linux/03-network-check.md` in a NEW chat, HANDOFF state first.
