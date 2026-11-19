# Report template — canonical long form

Every pack ends by filling this shape in plain words. The same shape doubles
as the HANDOFF between packs: the user pastes it, with the next pack, into a
fresh chat.

```
SECURITY CHECK-UP REPORT — <pack name> — <date>

MACHINE
- System: <OS + version, from step 0>
- Protection: <AV/firewall state found, with CARD id>

WHAT I CHECKED
- <step id>: <one-line result> — <NORMAL | SUSPICIOUS | CANNOT TELL> (CARD <id>)
- ...

WHAT I CHANGED (only if the user said YES)
- <change>: undo = <saved capture location or exact undo step>

WHAT NEEDS A HUMAN
- <anything SUSPICIOUS or CANNOT TELL that this pack could not resolve>
- <anything outside this pack's scope>

HANDOFF (paste this block with the next pack, in a NEW chat)
- Next pack: <exact filename>
- State: <5 lines max — OS/version, protection state, open findings with
  card ids, changes made + undo pointers, incident status if any>
```

Rules:
- Every finding line cites its CARD id. No card, no verdict.
- "Nothing found" is written as "nothing found by these checks", never
  "your computer is clean/safe".
- The HANDOFF state block is ≤ 5 lines so it fits any small model's window.
- If incident status is active, HANDOFF says INCIDENT ACTIVE and routes to
  INCIDENT-RANSOMWARE.md only.
