---
pack_id: linux-persistence-hunt
os: linux
os_versions: ["Ubuntu 22.04/24.04 LTS", "Fedora 40+", "Arch (rolling)"]
shell: bash
privilege: user
pack_type: module
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Linux — persistence hunt (what starts itself)

Autostart, systemd, cron, shell profiles, hosts. Look-only; verify suspicious
items, never delete on a hunch.

## Step 0 — confirm this is the right pack

Ask: "Are you on Linux?" If not, stop and name the right pack. Then run
(look-only) and paste:

```command
cat /etc/os-release
```

```card
CARD L-PER-00
COMMAND: cat /etc/os-release
TIER: T0
NORMAL LOOKS LIKE: NAME/VERSION_ID lines.
SUSPICIOUS LOOKS LIKE: none — identity only.
CANNOT TELL WHEN: file missing — ask; unknown → stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: n/a.
NEVER CONCLUDE: anything from identity alone.
```

## Self-check

1. Where do autostart entries live? (~/.config/autostart.)
2. What does Exec= tell you? (What actually runs.)
3. What do you do with a suspicious item? (Record + verify; gated disable in 06.)

## Step 1 — your autostart entries (look-only)

```command
ls -la ~/.config/autostart
```

```card
CARD L-PER-01
COMMAND: ls -la ~/.config/autostart
TIER: T0
NORMAL LOOKS LIKE: .desktop files for known apps.
SUSPICIOUS LOOKS LIKE: random-name .desktop files (medium) — Step 3 reads one.
CANNOT TELL WHEN: "No such file or directory" — NORMAL.
EXIT CODES / EXPECTED WARNINGS: paste only the first 30 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "many entries = infected".
```

## Step 2 — enabled system services (look-only)

```command
systemctl list-unit-files --state=enabled | head -25
```

```card
CARD L-PER-02
COMMAND: systemctl list-unit-files --state=enabled | head -25
TIER: T0
NORMAL LOOKS LIKE: distro services (NetworkManager, cups, ssh if used) — dozens normal.
SUSPICIOUS LOOKS LIKE: random-name service (medium) — Step 3 reads it.
CANNOT TELL WHEN: "not booted with systemd" (containers/WSL1) — skip this step, say so.
EXIT CODES / EXPECTED WARNINGS: paste only the first 25 lines.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "unknown service = malware" — many legit helpers exist.
```

## Step 3 — read ONE suspicious item (look-only)

Autostart .desktop from Step 1. PATH keeps its quotes and byte-matches that
path (spaces fine); reject ; | & $ ` " ' or newlines.

```command
cat "<PATH: .desktop path from step 1>"
```

```card
CARD L-PER-03
COMMAND: cat "<PATH: .desktop path from step 1>"
TIER: T0
NORMAL LOOKS LIKE: Exec= points to a known program (/usr/bin, /opt, snap).
SUSPICIOUS LOOKS LIKE: Exec= from /tmp, /var/tmp, /dev/shm, or curl-pipe-sh (medium/high) — record.
CANNOT TELL WHEN: unreadable — do not guess contents.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 06 (NEW chat).
NEVER CONCLUDE: "autostart = malicious" — just start at login.
```

Service unit from Step 2 instead:

```command
systemctl cat "<NAME: unit name from step 2>"
```

```card
CARD L-PER-04
COMMAND: systemctl cat "<NAME: unit name from step 2>"
TIER: T0
NORMAL LOOKS LIKE: ExecStart= in /usr/bin or /usr/lib for a known product.
SUSPICIOUS LOOKS LIKE: ExecStart= in /tmp or random-name binary (medium/high) — record.
CANNOT TELL WHEN: unit not found — re-check the name once, then CANNOT TELL.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: 06 (NEW chat).
NEVER CONCLUDE: "enabled = malicious".
```

## Step 4 — cron jobs (look-only)

```command
crontab -l
```

```card
CARD L-PER-05
COMMAND: crontab -l
TIER: T0
NORMAL LOOKS LIKE: "no crontab for <user>" — most desktop users have none.
SUSPICIOUS LOOKS LIKE: entries the user never created, esp. curl-pipe-sh (high) — NEEDS A HUMAN.
CANNOT TELL WHEN: command not found — cron not installed; note it.
EXIT CODES / EXPECTED WARNINGS: "no crontab for" exits 1 — EXPECTED.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "cron exists = infected" — admins use it.
```

## Step 5 — shell profile + hosts file (look-only)

```command
tail -5 ~/.bashrc
```

```card
CARD L-PER-06
COMMAND: tail -5 ~/.bashrc
TIER: T0
NORMAL LOOKS LIKE: prompt/alias lines or tool init blocks (nvm, pyenv).
SUSPICIOUS LOOKS LIKE: appended lines downloading/executing remote code (high) — NEEDS A HUMAN.
CANNOT TELL WHEN: file missing — NORMAL.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "custom bashrc = malware" — users customize it.
```

```command
cat /etc/hosts
```

```card
CARD L-PER-07
COMMAND: cat /etc/hosts
TIER: T0
NORMAL LOOKS LIKE: localhost lines, maybe user-added blocks.
SUSPICIOUS LOOKS LIKE: entries redirecting update or bank domains (high) — NEEDS A HUMAN.
CANNOT TELL WHEN: unfamiliar entries — ask before judging.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "custom hosts = malware" — ad-blocking uses it too.
```

## Report

Fill the REPORT SKELETON. HANDOFF: confirmed-suspicious item →
`packs/linux/06-removal-and-recovery.md`; else `packs/linux/04-malware-scan.md`.
NEW chat, HANDOFF first.
