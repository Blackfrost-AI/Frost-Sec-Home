---
pack_id: windows-incident-ransomware
os: windows
os_versions: ["10 22H2", "11"]
shell: powershell
privilege: user
pack_type: incident
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Windows — ransomware incident (preserve, contain, get help)

This pack is for a CONFIRMED incident: a ransom note plus many files with a
strange new ending. Not sure yet? Verify first (Step 1) — one odd file is
not an incident. No cleanup here: deleting anything makes recovery harder.
Paying does not guarantee your files back.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Windows PC, and do you see a ransom message plus many
renamed files?" Wrong OS → name the right pack. Ask the user to paste the
exact folder path where the renamed files are. Signs unconfirmed → Step 1
before anything else.

## Self-check

1. What do you delete during an incident? (Answer: nothing.)
2. What gets unplugged besides the network?
3. Who handles decryption and negotiation? (Answer: professionals, not you.)

## Step 1 — verify the pattern (look-only, only if unconfirmed)

The PATH slot keeps its quotes and byte-matches the folder path pasted in
step 0 (spaces fine); reject ; | & $ ` " ' or newlines.

```command
Get-ChildItem "<PATH: folder path pasted by the user, from step 0>" | Select-Object -First 20 Name, Length, LastWriteTime
```

```card
CARD W-INC-01
COMMAND: Get-ChildItem "<PATH: folder path pasted by the user, from step 0>" | Select-Object -First 20 Name, Length, LastWriteTime
TIER: T0
NORMAL LOOKS LIKE: ordinary names; a lone .crdownload/.tmp = unfinished download, NOT ransomware — say so plainly and stop the incident path.
SUSPICIOUS LOOKS LIKE: many files sharing a new ending PLUS a note like READ_ME/RECOVER/DECRYPT (confirmed incident) — continue to Step 2.
CANNOT TELL WHEN: mixed or unclear — ask one clarifying question; do not declare an incident on a guess.
EXIT CODES / EXPECTED WARNINGS: paste only the first 20 lines; access-denied rows are normal.
NEXT IF SUSPICIOUS: Step 2.
NEVER CONCLUDE: "one weird extension = ransomware".
```

## Step 2 — contain (guided, user's hands, urgent)

Guide in this order, one instruction at a time, no commands:
1. Unplug the network cable, or turn off Wi-Fi (Settings > Network & internet
   > Wi-Fi off). This stops spread to other devices.
2. UNPLUG EXTERNAL AND BACKUP DRIVES NOW — ransomware encrypts attached
   backups too. If a backup drive is connected, it is in danger this minute.
3. Pause OneDrive/Dropbox/Google Drive sync (their tray icons > pause) so
   encrypted copies do not overwrite good cloud versions.
4. If files are VISIBLY changing/encrypting right now: hold the power button
   to shut down. Otherwise leave the PC on — memory can hold clues and keys.
5. Do not delete the note, the encrypted files, or anything else. Do not run
   "cleaner" tools. Do not pay.

```card
CARD W-INC-02
COMMAND: GUI: unplug network > unplug backup drives > pause cloud sync > power decision
TIER: T0
NORMAL LOOKS LIKE: user confirms each action done, in order.
SUSPICIOUS LOOKS LIKE: n/a — containment is always right here.
CANNOT TELL WHEN: user cannot do a step — note it, continue with the rest; partial containment beats none.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "we should clean the malware first" — preservation comes before any cleanup, by professionals.
```

## Step 3 — recovery paths (guided, hope with honesty)

Explain plainly, in this order:
1. Cloud version history: OneDrive/Dropbox/Google Drive keep older versions
   of files on their WEBSITES (not the synced folder). From a DIFFERENT,
   clean device, the user can check and restore pre-encryption versions.
2. File History / Previous Versions: right-click a folder > Properties >
   Previous Versions — if backups ran before the incident, copies may exist.
3. The user can look up the note's family at No More Ransom
   (nomoreransom.org) and ID Ransomware — some families have free
   decryptors. Their own manual step, not the assistant's.
4. If none of these exist: a professional incident responder is the next
   step. Be honest: without backups or a decryptor, recovery may not be
   possible. Do not promise outcomes. Never advise paying.

```card
CARD W-INC-03
COMMAND: GUI: cloud version history / Previous Versions / user-only decryptor lookup
TIER: T0
NORMAL LOOKS LIKE: some pre-encryption versions found — restore them to a CLEAN device or after professional cleanup, not onto the infected PC.
SUSPICIOUS LOOKS LIKE: n/a.
CANNOT TELL WHEN: no backups, no versions — say so honestly; route to professional help.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: professional help.
NEVER CONCLUDE: "paying will get the files back" — it often does not, and funds further attacks.
```

## Report

Fill the REPORT SKELETON with INCIDENT ACTIVE. HANDOFF: this incident needs a
professional; the report is the record to hand them (times, note text, the
new ending, what was unplugged and when). No further packs run on this PC
until a human expert says it is clean.
