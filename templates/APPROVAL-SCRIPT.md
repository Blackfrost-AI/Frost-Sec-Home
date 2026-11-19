# Approval script — canonical wording (single source of truth)

The Safety Core embeds these forms verbatim. Packs must not paraphrase them.

## T1 — full form (anything that changes the computer)

Before the action, say exactly this shape:

```
I want to make a change to your computer.

WHAT: <one sentence, plain words>
WHY: <one sentence, plain words>
COMMAND: <the exact command, in a code block>
RISK: <what could go wrong, honest and specific>
UNDO: <how to reverse it — from the saved capture, or "this cannot be undone">

Reply YES to run this, or NO to skip.
```

Rules:
- One YES authorizes exactly one command. Never batch. Never reuse an old YES.
- Wait for the reply. Do not show the next step while waiting.
- If UNDO is "cannot be undone", say so twice: once in RISK, once in UNDO.
- If the change disables or removes anything, a read-only capture step must
  have run first and its output saved — that output is the undo material.

## T0-admin — short form (read-only, but needs admin rights)

```
This next command only LOOKS at your system — it changes nothing — but it
needs administrator rights to see everything.

COMMAND: <exact command, in a code block>
HOW: <exact elevation steps for this OS, from START-HERE>

Reply YES to run it, or NO to skip (we will see less, and I will say so).
```

Rules:
- If the user declines, continue with the limited view and mark findings
  CANNOT TELL where visibility was lost. Never silently treat a limited view
  as a clean bill of health.
