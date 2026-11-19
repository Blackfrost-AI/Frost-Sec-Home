# Testing — how Frost-Sec-Home packs are verified

Four layers, weakest claim first. A pack is never called "tested" on the
strength of one layer. Current status: [VERIFICATION.md](../VERIFICATION.md).

## L1 — static validation (every commit, CI-enforced)

```sh
python3 tools/validate.py .
```

Checks: token budgets (module ≤2500 assembled, Safety Core ≤1200), card
format + required fields, COMMAND byte-match against the step's command
fence, slot grammar + source-step provenance, tier labels, OS bleed,
banned (T2) commands, Safety Core integrity (byte-identical in every pack),
UNTESTED banner + frontmatter agreement. CI: `.github/workflows/ci.yml`.

## L2 — unit tests (every commit)

```sh
python3 -m unittest discover -s tests/lint
```

75 tests: validator rules (incl. quoted PATH/NAME slots and core-version
match), token budgeting, behavior scorer (allowlist with
typed-slot substitution — PATH/NAME values always inside double quotes,
spaces legal inside quotes, shell metacharacters refused — approval gating
incl. T0-admin, injection
compliance, T2 in commands and prose, privacy solicitation, stop conditions,
two-steps-ahead, verdict citation, context budget), and the runner loop
against a mock endpoint (placement, fixture substitution, result files).

## L3 — command receipts (per OS, real machine or container)

Look-only commands from the packs are executed on a real target and their
output + exit codes saved under `verification/<os>/`. Failure branches are
recorded as negative evidence, never deleted. T1 (change-making) commands
are syntax-reviewed only unless run on a disposable machine with explicit
approval. See `verification/macos/`, `verification/linux/` (collector script
included), and the Windows checklist in VERIFICATION.md.

## L4 — model behavior matrix (the real test)

```sh
python3 tools/behavior_test.py --self-check          # wiring only, no model
python3 tools/behavior_test.py --all \
  --endpoint http://127.0.0.1:11434/v1 --model <small-instruct-model> \
  --placement user_message --num-ctx 16384
```

- Scenarios: `tests/scenarios/` — H1–H3 (healthy machines) and R1–R8
  (red-team: injection in output/filenames, ransomware + pay pressure,
  ambiguous findings under user pressure, foreign/public network scans,
  bulk-delete demands, out-of-allowlist requests, deliberate `num_ctx`
  misconfiguration).
- Fixtures are **substituted for execution** — the harness never runs a
  real command; the model believes the user pasted the output.
- Default placement is `user_message` (hosted-chatbot reality);
  `--placement system` available for comparison.
- Scorer: substitution-aware allowlist, one-YES-one-command approval gate,
  stop-condition latches, verdict-with-card-citation, T2/prose-T2,
  injection compliance, privacy, context-budget assertion.
- Results: `tests/results/` (gitignored) — transcript + violations JSON per
  run, `summary.jsonl` rows. Current state: **PENDING**, see
  `tests/results/PENDING.md` (no endpoint was available at build time).

### Bounded fix loop

On a failing scenario: fix the pack structurally (dedupe/relocate, never
wordsmith past the budget), re-run `validate.py`, re-run the failing
scenario. Max 3 iterations per scenario; every iteration's violations are
kept as negative evidence. If it still fails, the pack keeps its UNTESTED
banner and the failure is recorded — no silent retries until green.

## Release gate

A pack's UNTESTED banner is removed only when L3 receipts exist on a real
target-version machine AND the relevant L4 scenarios pass on at least one
small model with adequate context. Full criteria: VERIFICATION.md.