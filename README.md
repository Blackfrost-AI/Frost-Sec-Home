# Frost-Sec-Home

**Personal computer security check-ups you can run by pasting a prompt into an AI assistant.**
For Windows, macOS, and Linux. Written for people who are not technical.

> **v0.1.0 — all packs UNTESTED.** Honest first release: the packs are careful
> drafts with strong safety rails, but they have not yet been verified
> end-to-end with real AI models on real machines. Read [VERIFICATION.md](VERIFICATION.md)
> and the [Pack status](#pack-status) table before using anything. Prefer the
> look-only steps until testing lands.

## What this is

Frost-Sec-Home is a library of carefully written instruction documents ("packs").
You pick your operating system, paste one pack into an AI chat (a local model on
your own computer, or a hosted chatbot), and the assistant walks you through a
security check-up, one small step at a time:

1. **Triage** — a quick first look: is your protection on, is anything obviously wrong?
2. **Verify & update** — make sure your system gets security updates.
3. **Harden** — turn on the protections that should already be on.
4. **Network check** — look at the devices on your own home network.
5. **Malware scan** — run your system's built-in scanner and understand the results.
6. **Persistence hunt** — look at what starts automatically when you log in.
7. **Removal & recovery** — safely quarantine or remove confirmed threats, with undo.
8. **Ransomware incident** — a special pack for when files are being held hostage.

The packs are written so that even a **small AI model** can follow them without
doing anything dangerous: every command is pinned word-for-word, every result
has a written "what this means" card, and anything that changes your computer
requires your explicit YES first.

## What this is NOT

- Not an app, not a scanner, not an antivirus product. It is text that guides an
  AI assistant, which guides you.
- Not a guarantee. A clean result means "nothing found by these checks", not
  "provably safe". See [docs/THREAT-MODEL.md](docs/THREAT-MODEL.md).
- Not a replacement for professional help in a serious incident. The packs will
  tell you when to stop and get a human expert.

## Quickstart (3 steps)

1. Open the START-HERE file for your system — it shows you exactly how to open
   the tool you'll paste commands into, and how to set up your AI chat:
   [Windows](START-HERE/windows.md) · [macOS](START-HERE/macos.md) · [Linux](START-HERE/linux.md)
2. Copy the whole **TRIAGE** pack for your system from `packs/<your-os>/TRIAGE.md`
   and paste it into your AI chat as your first message.
3. Follow the assistant one step at a time. When it asks you to run something,
   it will show the exact command and wait for your YES.

**Your safety rail (works even if the AI misbehaves):** only run a command that
the assistant shows you in a code block *after* you replied YES. If it suggests
anything else — anything not printed in the pack — stop and close the chat.

## Privacy: local vs hosted AI

- **Local model** (Ollama, LM Studio, or similar on your own computer): your
  system information stays on your machine. This is the private path, and the
  packs are designed for small local models.
- **Hosted chatbot** (any web-based AI service): everything you paste — command
  output, file names, folder listings — goes to that company's servers. The packs
  never ask for passwords or document contents, but you should still know this.
  If that is not acceptable to you, use a local model.

Frost-Sec-Home itself has no telemetry, no accounts, and sends nothing anywhere.

## Pack status

Honesty first: a pack is only as good as its testing. This table is the truth
about what has been verified on real systems.

| Pack set | Status | What has been checked |
|---|---|---|
| Windows | **UNTESTED** | Commands written and reviewed, not yet run on a real Windows PC (machine offline at build time). Verification next; packs updated when tested. |
| macOS | **UNTESTED** (partial receipts) | Look-only commands verified on the build host (macOS 27.2, newer than pack targets 13–15). Change-making steps and model behavior untested. |
| Linux | **UNTESTED** (partial receipts) | Command syntax + exit codes verified in Ubuntu 22.04/24.04 containers (incl. ClamAV/EICAR). Real-desktop, Fedora/Arch, and model behavior untested. |

"Partial receipts" means some commands were run and their outputs saved
(`verification/`), **not** that the pack was tested end-to-end. Every pack
carries a visible UNTESTED banner. Treat these as careful drafts, and prefer
the look-only steps until testing lands.

What IS fully verified at v0.1.0: the safety tooling — 24/24 packs pass
static validation, 75/75 unit tests pass, and the behavior-test harness is
ready to run the moment a model endpoint exists (see
[docs/TESTING.md](docs/TESTING.md)).

## Repository layout

- `START-HERE/` — plain-language setup for each OS (start here, really)
- `core/` — the Safety Core rules embedded in every pack, and the card format
- `packs/<os>/` — the prompt packs you paste (TRIAGE first, then modules)
- `templates/` — report and approval wording used by the packs
- `tests/` — red-team scenarios, synthetic outputs, and the test harness
- `tools/` — validator, token budget, pack assembler, behavior-test runner
- `verification/` — command receipts and the hardening audit (real evidence)
- `docs/` — threat model, prompt standard, testing, maintenance
- `VERIFICATION.md` — the honest status matrix and the release gate

## For contributors

Packs are treated as executable code: read [docs/PROMPT-STANDARD.md](docs/PROMPT-STANDARD.md),
run `python3 tools/validate.py .` and `python3 -m unittest discover -s tests/lint`
before every commit, and see [docs/TESTING.md](docs/TESTING.md) for the
behavior-test matrix. Nothing ships without passing lint; behavior-test
results are recorded with every release. Drafts live in `drafts/<os>/` and
are assembled into `packs/` with `python3 tools/assemble_pack.py <draft> <pack>`
(the Safety Core is injected between BEGIN/END markers — never edit it inside
a pack).

## Licenses

- Prompt content (packs, core, templates, docs): **CC BY 4.0** — see [LICENSE-CONTENT](LICENSE-CONTENT).
- Tooling (`tools/`, `tests/`): **MIT** — see [LICENSE-TOOLS](LICENSE-TOOLS).
