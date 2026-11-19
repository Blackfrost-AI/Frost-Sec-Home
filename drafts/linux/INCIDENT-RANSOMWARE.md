---
pack_id: linux-incident-ransomware
os: linux
os_versions: ["Ubuntu 22.04/24.04 LTS", "Fedora 40+", "Arch (rolling)"]
shell: bash
privilege: user
pack_type: incident
safety_core_version: 3
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Linux — ransomware incident (preserve, contain, get help)

For a CONFIRMED incident: a ransom note plus many files with a strange new
ending. Not sure yet? Verify first (Step 1) — one odd file is not an
incident. No cleanup here. Deleting anything makes recovery harder. Paying
does not guarantee your files back.

## Step 0 — confirm this is the right pack

Ask: "Are you on Linux, and do you see a ransom message plus many renamed
files?" Wrong OS → name the right pack. Signs unconfirmed → Step 1 first.

```command
cat /etc/os-release
```

```card
CARD L-INC-00
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

1. What do you delete during an incident? (Nothing.)
2. What gets unplugged besides the network? (Backup drives.)
3. Who handles decryption? (Professionals, not you.)

## Step 1 — verify the pattern (look-only, only if unconfirmed)

The PATH slot byte-matches the folder path the user pasted; reject symbols
like ; | & $ ` or quotes.

```command
ls -la <PATH: folder path pasted by the user, from step 0> | head -20
```

```card
CARD L-INC-01
COMMAND: ls -la <PATH: folder path pasted by the user, from step 0> | head -20
TIER: T0
NORMAL LOOKS LIKE: ordinary names; a lone .part/.crdownload = unfinished download, NOT ransomware — say so plainly, stop the incident path.
SUSPICIOUS LOOKS LIKE: many files sharing a new ending PLUS a note like READ_ME/RECOVER/DECRYPT (confirmed) — Step 2.
CANNOT TELL WHEN: mixed or unclear — one clarifying question; never declare an incident on a guess.
EXIT CODES / EXPECTED WARNINGS: paste only the first 20 lines.
NEXT IF SUSPICIOUS: Step 2.
NEVER CONCLUDE: "one weird extension = ransomware".
```

## Step 2 — contain (guided, user's hands, urgent)

One instruction at a time, no commands:
1. Disconnect the network: unplug Ethernet, or turn off Wi-Fi (network menu
   > off). This stops spread to other devices and shares.
2. UNPLUG EXTERNAL AND BACKUP DRIVES NOW — ransomware encrypts attached
   backups too. A connected backup drive is in danger this minute.
3. Pause cloud sync (Dropbox/Nextcloud/Google Drive clients — tray icon >
   pause/quit) so encrypted copies do not overwrite good cloud versions.
   Unmount network shares if any (file manager > eject/unmount).
4. Files VISIBLY changing right now: hold the power button to shut down.
   Otherwise leave the PC on — memory can hold clues and keys.
5. Delete nothing: not the note, not encrypted files. No "cleaner" tools.
   Do not pay.

```card
CARD L-INC-02
COMMAND: GUI: network off > unplug backup drives > pause cloud sync > power decision
TIER: T0
NORMAL LOOKS LIKE: user confirms each action, in order.
SUSPICIOUS LOOKS LIKE: n/a — containment is always right here.
CANNOT TELL WHEN: user cannot do a step — note it, continue; partial containment beats none.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "clean the malware first" — preservation before cleanup, by professionals.
```

## Step 3 — recovery paths (guided, hope with honesty)

In order:
1. Cloud version history: from a DIFFERENT, clean device, check the cloud
   service's website (Dropbox/Nextcloud/Google Drive keep older versions).
   Restore pre-encryption copies there, not onto the infected PC.
2. Backups: if a backup drive was UNPLUGGED before the incident, it may hold
   clean copies. Do not connect it to the infected PC — a professional
   should handle recovery from it. Snapshot-based setups (btrfs/ZFS) may
   have pre-incident snapshots — a professional checks those.
3. The user can look up the note's family themselves in a browser at No More
   Ransom (nomoreransom.org) and ID Ransomware — some families have free
   decryptors. Their manual step, not the assistant's.
4. None of these? A professional incident responder is next. Be honest:
   without backups or a decryptor, recovery may not be possible. Never
   promise outcomes. Never advise paying.

```card
CARD L-INC-03
COMMAND: GUI: cloud versions / unplugged backups / user-only decryptor lookup
TIER: T0
NORMAL LOOKS LIKE: pre-encryption versions found — restore to a CLEAN device or after professional cleanup.
SUSPICIOUS LOOKS LIKE: n/a.
CANNOT TELL WHEN: no backups, no versions — say so honestly; professional help.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: professional help.
NEVER CONCLUDE: "paying will get the files back" — often not, and it funds further attacks.
```

## Report

Fill the REPORT SKELETON with INCIDENT ACTIVE. HANDOFF: this needs a
professional; the report is the record to hand them (times, note text, the
new ending, what was unplugged and when). No further packs on this PC until
a human expert says it is clean.
