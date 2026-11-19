# Pre-release review — v0.1.0 (reviewer subagent, 2026-11-19)

Status: **FIXES COMPLETE — v0.1.0 release-blocking findings all landed and
re-verified** (24/24 packs PASS, 75/75 unit tests OK, 11/11 scenario wiring
OK, core v4 at 965 tokens — token-neutral vs v3). Deferred items are listed
below with the UNTESTED banners still in force. This file is the durable
disposition record for the pre-tag review. Full reviewer report archived in
the session spill file
`agent-call_b5c03179ce2a4c46834443f1.txt`; findings reproduced below with
dispositions. "Fixed in v0.1.0" means the fix landed before the tag;
"v0.1.1" means deliberately deferred with the UNTESTED banners still in force.

## BLOCKER

- **B1 — Remove-MpThreat approval promised reversibility Defender does not
  guarantee** (windows/06 Step 2: "WHY: supported, reversible" + UNDO Restore).
  Severe threats can be deleted outright; no Restore entry.
  → **Fixed in v0.1.0**: approval + card now say quarantine is usual but some
  threats are deleted outright and Restore may be unavailable.

## SHOULD-FIX

- **S1 — PATH slots unquoted while quoting was banned** → spaces deadlock or
  split-arg misfire (`mv` can move an unintended sibling).
  → **Fixed in v0.1.0**: Safety Core v4 grammar — PATH and NAME slots are
  always quoted in the command (`"<PATH: …>"`); the substituted value keeps
  the quotes, may contain spaces, must never contain `; | & $ ` " '` or
  newlines. Validator gains SLOT_QUOTE_MISSING; scorer matches the quoted
  template and checks the inner value. All affected drafts updated.
- **S2 — slot provenance "from step 0" pointed at an identity-only step.**
  → **Fixed in v0.1.0**: every affected Step 0 now explicitly asks the user
  to paste the exact confirmed path/name, so "from step 0" is true.
- **S3 — Windows firewall UNDO (`-Enabled False` on -All) would disable
  profiles that were already on.**
  → **Fixed in v0.1.0**: UNDO restores the per-profile state captured in
  Step 2; heading/prose reconciled with `-All` semantics.
- **S4 — `sudo ufw allow ssh` prose-only (no fence/card); untyped `<unit>`
  slot in linux/06 prose; custom SSH port lockout.**
  → **Fixed in v0.1.0**: allow-ssh gets its own fence + CARD L-HAR-02b (T1)
  with a custom-port stop branch; linux/06 systemd-service removal is scoped
  out ("NEEDS A HUMAN; this pack covers .desktop items only") removing the
  untyped prose-only T1 entirely. `ufw enable` stays T1 (a change needs FULL
  approval; the sudo password prompt is documented in the card) — deliberate.
- **S5 — quarantine `mv` can clobber a same-named earlier item.**
  → **Fixed in v0.1.0**: `mv -n` + collision branch (stop; rename with a date
  suffix as a guided step) in linux/06 and macos/06.
- **S6 — scorer floor lower than ideal** (paragraph-scoped refusal exemption,
  YES banking, provenance accepts any prior user text, weak R7 assertions,
  narrow T2 regexes). → **v0.1.1.** Docs already call the scorer a floor.
- **S7 — UNBOUNDED limiter lint dormant (opt-in, zero declarations).**
  → **v0.1.1** (declare limiters or default-on with bounded allowlist).
- **S8 — one-YES-one-command vs `&&` chains.** → **v0.1.1**: define "one
  fenced pipeline = one approvable unit" in PROMPT-STANDARD/Core, or split.
- **S9 — PENDING.md stale "52/52" (actual 75 after v4 guards) + date mismatch.**
  → **Fixed in v0.1.0**: count refreshed everywhere (PENDING, VERIFICATION,
  TESTING, README); date note added.
- **S10 — LICENSE-CONTENT attribution placeholder URL.**
  → **Fixed in v0.1.0**: attribution by project name; no placeholder URL.
- **S11 — THREAT-MODEL overclaims scam-recognition coverage (Windows-only).**
  → **v0.1.1** (scope the claim or add mac/linux guided steps).

## NICE-TO-HAVE (all → v0.1.1)

- N1 letter-suffixed steps invisible to runner self_check parsing.
- N2 CI: add `--self-check`, pin pyyaml/tiktoken.
- N3 prose-scan warning tier for banned commands.
- N4 Checkpoint-Computer <24h point may predate the infection — one clause.
- N5 `launchctl unload && mv` partial-state on unload error (deprecated
  command acknowledged in MAINTENANCE.md).

## Verified clean by the reviewer (evidence-based)

UNTESTED consistency 24/24; cross-pack handoffs resolve; ransomware
containment ordering correct in all three INCIDENT packs; reboot warning
(Start-MpWDOScan) and FileVault key warnings present; receipts honest about
host-newer-than-target and EICAR exit codes; core injection byte-identical.