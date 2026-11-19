# Behavior-test matrix — PENDING (honest record)

Date: 2026-11-18 (UTC); counts refreshed 2026-11-19 after the quoted-slot
grammar hardening (Safety Core v4).
Status: **PENDING — no model endpoint available on this host.**

## What was probed (negative evidence)

| Probe | Result |
|---|---|
| `curl http://127.0.0.1:11434/v1/models` (Ollama) | no response / connection refused |
| `curl http://127.0.0.1:1234/v1/models` (LM Studio) | no response / connection refused |
| `which ollama` | not installed |
| `/Applications`, `~/Applications` scan for Ollama / LM Studio / GPT4All / Jan | none present |
| `~/.ollama/models`, `~/.cache/lm-studio/models` | absent — no cached models |

Installing a model runtime + multi-GB weights was not in the approved scope
for this session, so no install was attempted. No behavior results are
claimed. **Every pack's `verification_status: untested` banner stays.**

## What IS verified without a model

- Static validation: 24/24 packs PASS (`python3 tools/validate.py .`).
- Scorer + runner + validator unit tests: 75/75 OK (`python3 -m unittest discover -s tests/lint`),
  including mock-endpoint loop tests (placement, fixture substitution,
  approval gating, injection compliance, ctx-budget assertion).
- Scenario wiring: 11/11 scenarios resolve (`python3 tools/behavior_test.py --self-check`).
- Command syntax/exit codes: macOS host receipts (`verification/macos/`),
  Ubuntu 22.04/24.04 container receipts (`verification/linux/`).

## How to run the matrix when an endpoint exists

```sh
# 1. Install Ollama (https://ollama.com) and pull a small instruct model, e.g.:
ollama pull qwen2.5:7b-instruct
# 2. IMPORTANT: default num_ctx is too small for these packs. The runner
#    passes num_ctx per request; R8 deliberately tests the misconfig flag.
python3 tools/behavior_test.py --all \
  --endpoint http://127.0.0.1:11434/v1 --model qwen2.5:7b-instruct \
  --placement user_message --num-ctx 16384
# 3. Compare placement (hosted-chatbot reality vs system-prompt):
python3 tools/behavior_test.py --all --endpoint ... --model ... --placement system
```

Results land in `tests/results/` (gitignored): per-scenario transcript +
violations JSON + `summary.jsonl`. Bounded fix loop per plan: on failure,
fix the pack (structural, re-validate budgets), re-run the failing scenario,
max 3 iterations per scenario; record each iteration's violations as
negative evidence, never delete them.

## Matrix to fill (rows stay PENDING until real runs)

| Scenario | Pack | Model | Placement | Result |
|---|---|---|---|---|
| H1 | windows/TRIAGE | — | user_message | PENDING |
| H2 | macos/03-network-check | — | user_message | PENDING |
| H3 | linux/04-malware-scan | — | user_message | PENDING |
| R1 | windows/06-removal-and-recovery | — | user_message | PENDING |
| R2 | linux/04-malware-scan | — | user_message | PENDING |
| R3 | windows/04-malware-scan | — | user_message | PENDING |
| R4 | windows/05-persistence-hunt | — | user_message | PENDING |
| R5 | linux/03-network-check | — | user_message | PENDING |
| R6 | macos/03-network-check | — | user_message | PENDING |
| R7 | windows/06-removal-and-recovery | — | user_message | PENDING |
| R8 | linux/05-persistence-hunt | — | user_message (ctx=2048) | PENDING |