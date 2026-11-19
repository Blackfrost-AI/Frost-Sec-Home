---
pack_id: linux-verify-update
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

# Linux — verify and update

Confirm your distribution, then install security updates with your YES.
Pick the ONE command line for your package family (Step 0 tells you which):
apt = Ubuntu/Debian, dnf = Fedora, pacman = Arch. Never mix families.

## Step 0 — confirm this is the right pack

Ask: "Are you on Linux?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
cat /etc/os-release
```

```card
CARD L-UPD-00
COMMAND: cat /etc/os-release
TIER: T0
NORMAL LOOKS LIKE: NAME/VERSION_ID lines; note the family (apt/dnf/pacman).
SUSPICIOUS LOOKS LIKE: end-of-life version (medium) — upgrade the release, not just packages.
CANNOT TELL WHEN: file missing — ask which distro; if unknown, stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: upgrade recommendation.
NEVER CONCLUDE: "old version means infected".
```

## Self-check

1. Which steps contact update servers? (1 and 2.)
2. What does dnf exit code 100 mean? (Updates exist — success.)
3. What must the user do before a big upgrade? (Save work; have a backup.)

## Step 1 — list available updates (T1)

FULL APPROVAL. WHAT: refresh package lists and show what would upgrade.
WHY: see known holes before closing them. RISK: network use; simulate mode
changes nothing. UNDO: none needed. Wait for YES. Your family's line:

```command
sudo apt-get update && apt-get -s upgrade
```

```card
CARD L-UPD-01
COMMAND: sudo apt-get update && apt-get -s upgrade
TIER: T1
NORMAL LOOKS LIKE: "0 upgraded" or a list. Fedora: `dnf check-update`. Arch: `checkupdates`.
SUSPICIOUS LOOKS LIKE: security updates pending (medium) — Step 2.
CANNOT TELL WHEN: network errors — CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: dnf check-update exits 100 when updates exist = SUCCESS. checkupdates may be absent on Arch (pacman-contrib) = CANNOT TELL, offer `pacman -Qu` after a sync.
NEXT IF SUSPICIOUS: Step 2.
NEVER CONCLUDE: "empty list = fully secure" — one channel checked.
```

## Step 2 — install updates (T1, may need restart)

FULL APPROVAL. WHAT: download and install the listed updates. WHY: close
known holes. RISK: minutes of work; kernel updates need a RESTART to take
effect — save work first. UNDO: none — updates are not rolled back here.
Wait for YES; confirm work saved. Your family's line:

```command
sudo apt-get upgrade
```

```card
CARD L-UPD-02
COMMAND: sudo apt-get upgrade
TIER: T1
NORMAL LOOKS LIKE: packages download and set up; "0 upgraded" if current. Fedora: `sudo dnf upgrade`. Arch: `sudo pacman -Syu`.
SUSPICIOUS LOOKS LIKE: repeated failures or held-back packages (medium) — stop after two tries; NEEDS A HUMAN. Never force with --allow-downgrades or similar.
CANNOT TELL WHEN: hangs >30 min — CANNOT TELL; do not power off mid-install.
EXIT CODES / EXPECTED WARNINGS: sudo password (blind) = NORMAL. "restart required" notices = EXPECTED; restart when the user is ready. Arch -Syu is a full sync+upgrade — never partial upgrades.
NEXT IF SUSPICIOUS: stop, NEEDS A HUMAN.
NEVER CONCLUDE: "restart means it broke" — planned.
```

## Step 3 — automatic security updates (guided, T1)

FULL APPROVAL. WHAT: enable automatic security updates. WHY: patches arrive
without remembering. RISK: occasional restart notices. UNDO: same setting,
off. Wait for YES. Ubuntu/Debian: guide `sudo apt-get install
unattended-upgrades` then `sudo dpkg-reconfigure -plow unattended-upgrades`
(answer Yes). Fedora: `sudo dnf install dnf-automatic` then `sudo systemctl
enable --now dnf-automatic-install.timer`. Arch: no official auto-updater —
recommend a weekly manual `pacman -Syu` habit instead; never install AUR
auto-updaters in this pack.

```card
CARD L-UPD-03
COMMAND: GUI: distro auto-update setup (unattended-upgrades / dnf-automatic) — guided
TIER: T1
NORMAL LOOKS LIKE: service/timer enabled; Ubuntu shows it in Software & Updates > Updates.
SUSPICIOUS LOOKS LIKE: enable fails twice — NEEDS A HUMAN.
CANNOT TELL WHEN: unfamiliar distro — recommend the manual weekly habit instead.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "auto-update on = never check again" — verify monthly.
```

## Report

Fill the REPORT SKELETON: updates installed, settings changed + undo.
HANDOFF: `packs/linux/02-harden.md` in a NEW chat, HANDOFF state first.
