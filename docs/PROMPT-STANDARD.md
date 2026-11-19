# Prompt standard — how packs are written (contributor spec)

Packs are executable code for a small model. Every rule here is enforced by
`tools/validate.py` unless marked (human). Read `core/SAFETY-CORE.md` and
`core/INTERPRETATION-CARD.md` first — they define the embedded block and card
format this standard references.

## Pack skeleton (in this order)

1. YAML frontmatter (schema below)
2. UNTESTED banner (required whenever `verification_status` != `verified`)
3. Safety Core block — byte-identical to `core/SAFETY-CORE.md`, between the
   markers `<!-- SAFETY-CORE-BEGIN -->` and `<!-- SAFETY-CORE-END -->`
4. Step 0 — identity check: confirm the user's OS matches the pack; if not,
   stop and name the right pack. Includes the pack's EOL-warning branch.
5. Self-check — 3 questions the assistant answers about its own rules before
   step 1 (e.g. "What do you do before changing anything?").
6. Numbered steps, each: one fenced command line + its CARD block + plain
   instructions. Branching only via "IF output shows X → go to step N".
7. End — report skeleton fill + HANDOFF naming the next pack and "open it in
   a NEW chat, paste the handoff first".

## Frontmatter schema (exact fields and types)

```yaml
---
pack_id: windows-triage            # str, unique, <os>-<name>
os: windows                        # enum: windows | macos | linux
os_versions: ["10 22H2", "11"]     # list[str], non-empty
shell: powershell                  # enum: powershell | zsh | bash
privilege: user                    # enum: user | admin-mixed (pack contains T0-admin/T1 steps)
pack_type: triage                  # enum: triage | module | incident
safety_core_version: 2             # int, must equal core marker
min_context_tokens: 16000          # int, >= 16000
verification_status: untested      # enum: untested | partial | verified
---
```

`verification_status` != `verified` requires the standard banner text:
`> **UNTESTED:** commands in this pack have not yet been verified on a real
> system. They will be updated when tested. Prefer the look-only steps.`
(partial packs may say "partially verified" with the same banner shape).

## Reliability rules (S1–S12)

- **S1 Linearity** — numbered steps; explicit jumps to real step ids only.
- **S2 Pinned commands** — every fenced command byte-matches its card's
  COMMAND line. Only typed slots may vary; the card declares slot type and
  source step.
- **S3 One action per step** — one fenced command line (pipes within the line
  are fine); never a command plus a config change in one step.
- **S4 Token budget** — real tokenizer: Safety Core ≤ 1,200; module ≤ 2,500;
  triage ≤ 3,500 (total pack incl. core).
- **S5 Reading level** — user-facing prose ≤ grade 8 (fenced blocks excluded);
  > grade 10 fails, 8–10 warns. (human reviews warnings)
- **S6 Cards for every command** — all fields, incl. EXIT CODES and a
  non-empty CANNOT TELL.
- **S7 Self-check** — 3 rule questions before step 1.
- **S8 OS pinning** — frontmatter + step-0 identity check.
- **S9 No external fetches** — no URL the assistant is told to visit; manual
  user-only options are labeled "you do this yourself in a browser".
- **S10 Fail-closed** — anything unexecutable ends in "stop and tell the
  user", never "use your judgment".
- **S11 Output limiters** — every unbounded-output command has a pinned
  limiter (`Select-Object -First N`, `head -n N`, pinned `grep`) and the step
  says "paste only the first N lines".
- **S12 Fresh-chat handoff** — every pack ends with report + next-pack
  instruction; no pack assumes another pack's content is in context.

## Safety rules (beyond lint)

- T1 changes require capture-first when they disable/remove anything; the
  saved capture output is the undo material.
- Restore points / backup checks come BEFORE the first T1 change in any pack
  that makes changes.
- Network steps: passive-first; active sweep only per the scope rule
  (RFC1918, prefix ≥ /24, ownership confirmation, typed SUBNET slot).
- Ransomware: verify-first (one odd filename ≠ incident), then the inline
  incident block; the INCIDENT pack is the expansion, opened in a new chat.
- Removal is capped: AV quarantine + single-item gated changes with saved
  undo. Deeper surgery escalates to professional help. No bulk deletion
  anywhere, ever.
- (human) Every card's NEVER CONCLUDE line must name a real overclaim a small
  model would make; generic filler is rejected in review.

## Machine-readable pack format (lint contract)

- **Steps** are headers: `## Step N — title` (N integer, unique, ascending not
  required but jumps must resolve).
- **Commands**: a step contains at most one fenced block whose info string is
  `command` (```command). Its content is exactly one line (pipes allowed).
  Other fences (e.g. ```text report skeletons) are not commands.
- **Cards** are fenced blocks with info string `card`, placed inside the step
  they belong to. First line `CARD <id>`, then `FIELD: value` lines. Required
  fields: COMMAND, TIER, NORMAL LOOKS LIKE, SUSPICIOUS LOOKS LIKE, CANNOT TELL
  WHEN, EXIT CODES / EXPECTED WARNINGS, NEXT IF SUSPICIOUS, NEVER CONCLUDE.
  The card's COMMAND value must byte-match the step's ```command content.
- **Jumps**: the exact phrase `go to step N` must reference an existing step.
- **Output limiters (S11)**: a card may declare `UNBOUNDED: yes`; then its
  command must contain `Select-Object -First`, `head -n`, or `grep`, and the
  step prose must contain `paste only the first`.
- **Self-check**: a section `## Self-check` with exactly 3 numbered questions
  before Step 1's content begins (after Step 0).
- **Handoff**: the pack must contain `HANDOFF` and `NEW chat` near the end.
- **Banner**: `verification_status` != `verified` requires a blockquote line
  starting `> **UNTESTED:**` or `> **PARTIALLY VERIFIED:**`.

## Verification

Every pinned command needs a row in `docs/VERIFICATION.md` (OS version, date,
evidence). `untested` rows ship with the banner (operator decision
2026-11-18); banners come off only when receipts land. See MAINTENANCE.md for
the drift watchlist that must be walked each release.
