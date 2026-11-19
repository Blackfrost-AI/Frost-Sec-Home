# VERIFICATION — Frost-Sec-Home v0.1 (honest status matrix)

Date: 2026-11-18 (UTC). **Every pack ships UNTESTED** (`verification_status:
untested` in frontmatter + visible banner). This file records exactly what
has and has not been verified, with receipts. Nothing here claims a pack is
safe to run end-to-end until the model-behavior matrix is filled.

## Verification layers

| Layer | What it proves | Status |
|---|---|---|
| L1 Static | budgets, card format, core integrity, slot grammar, OS bleed, banned commands | **PASS 24/24** (`tools/validate.py`) |
| L2 Unit | scorer + runner logic, mock-endpoint loop, hardening gaps | **PASS 66/66** (`unittest discover -s tests/lint`) |
| L3 Command receipts | look-only command syntax + exit codes on real OS/container | macOS host + Ubuntu containers: **partial PASS**; Windows: **PENDING** |
| L4 Model behavior | small models actually follow the pack (H/R matrix) | **PENDING** — no endpoint on host (`tests/results/PENDING.md`) |

## L1 — static validation (all packs)

`python3 tools/validate.py .` → `24 packs checked, 0 failing`; core 965 tok
(≤1200); every module ≤2500 tok assembled. CI runs this on every push
(`.github/workflows/ci.yml`).

## L3 — command receipts per OS

### macOS — host receipts (partial)

Receipt: `verification/macos/look-only-receipts.txt` (commit `dfa4c7e`).
Host: macOS **27.2** — NEWER than pack targets 13–15; wording on target
versions may differ. Look-only commands only; no T1 changes executed.

Verified on host: `sw_vers`, `fdesetup status`, `spctl --status`,
`spctl -a -vv` (app assessment), `socketfilterfw --getglobalstate`,
`ipconfig getifaddr en0`, `lsof -nP -iTCP -sTCP:LISTEN`, `arp -a -n`
(empty on this host — recorded), `ps aux -r`, `crontab -l`,
`launchctl list` (user scope), `ls ~/Library/LaunchAgents`,
`cat /etc/hosts`, `softwareupdate -l` (supplementary pass, true exit codes).

Negative evidence (kept, not hidden):
- `sfltool dumpbtm` **hung >60s, killed** → EXCLUDED from packs.
- user `TCC.db` unreadable without Full Disk Access → GUI path used instead.
- `netstat -an -p tcp | grep LISTEN` empty on this host → `lsof` used.
- `defaults read com.apple.alf globalstate` missing → `socketfilterfw` used.

### Linux — container receipts (partial)

Receipt: `verification/linux/look-only-receipts.txt` + collector script
(commit `661d4bb`). Ubuntu **22.04 and 24.04** containers, darwin/arm64 host.

Verified: `ip addr`, `ip neigh`, `ss -tulpn`, `crontab -l` (exit 1 "no
crontab" = EXPECTED per card), `ufw status`, `clamscan --version`,
`apt-get -s upgrade` (simulation), `hostname -I`, `/etc/hosts`, `.bashrc`.
**ClamAV exit codes verified with EICAR test file on both versions:**
clean → `Infected files: 0`, exit 0; EICAR → `FOUND`, exit 1. `freshclam`
DB download exit 0 (trailing NotifyClamd error = daemon-notify warning).

Negative evidence / limits:
- Base images lack ip/ss/crontab/ufw/clamscan/systemctl → exit-127
  "not found" receipts confirm the cards' CANNOT TELL branch.
- No systemd PID1 → service steps UNTESTED (cards say skip/CANNOT TELL).
- `ufw status` in container: netfilter permission denied → matches card
  CANNOT TELL branch; real desktop UNTESTED.
- **dnf (Fedora) / pacman (Arch) branches: UNTESTED** — no images locally;
  syntax review by eye only.
- T1 change commands: syntax-review only, never executed on a real system.

### Windows — PENDING (machine offline until tomorrow)

No receipts yet. All 8 packs syntax-reviewed against documented PowerShell
behavior only. When the machine is online:
1. Run every look-only command from TRIAGE/01/03/04/05 on the real machine;
   save outputs + exit codes to `verification/windows/look-only-receipts.txt`
   with OS build (`Get-ComputerInfo` output) in the header.
2. Verify Defender cmdlets exist on that build (`Get-MpComputerStatus`,
   `Start-MpScan`, `Get-MpThreatDetection`, `Update-MpSignature`).
3. Verify `Checkpoint-Computer` restore-point path (needs System Protection
   enabled — record the failure branch honestly if disabled).
4. Do NOT execute T1 removal steps on the operator's daily machine without
   explicit per-command approval; prefer a throwaway VM.

## L4 — model behavior matrix

**PENDING** — see `tests/results/PENDING.md` for probe evidence, run
instructions, and the 11-row matrix (H1–H3, R1–R8). No model was available
on this host; no behavior results are claimed anywhere in this repo.

## Hardening (rule-layer)

`verification/hardening-audit.md` (commit `e9e0c7b`): 7 scorer gaps found
via failing tests, fixed, re-tested; static audit found no T2-adjacent
commands in any allowlist. Live-model injection resistance: UNTESTED.

## What "tested" will mean (release gate for removing UNTESTED)

A pack's banner comes off only when ALL of:
1. L3 receipts on a real target-version machine (not container-only for
   systemd/GUI steps), including the failure branches the cards describe.
2. L4: H-scenario for that OS passes on ≥1 small model with
   `--placement user_message` and adequate `num_ctx`, zero violations.
3. Relevant R-scenarios for that OS pass (injection, scope, pressure).
4. Results committed under `tests/results/` with model id + config, and
   this matrix updated with the receipt paths.