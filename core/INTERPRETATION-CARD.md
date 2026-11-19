# Interpretation card format

Every command in every pack carries a card. The card is how a small model
interprets output without improvising: it matches what it sees against written
examples. The card's COMMAND line **is** the allowlist entry — lint checks that
every fenced command in the pack byte-matches its card.

## Format

```
CARD <id>
COMMAND: <exact pinned command — byte-identical to the fenced block in the step>
TIER: <T0 | T0-admin | T1>
NORMAL LOOKS LIKE: <concrete example output or values>
SUSPICIOUS LOOKS LIKE: <concrete signals, each with severity>
CANNOT TELL WHEN: <conditions, including limited visibility without elevation>
EXIT CODES / EXPECTED WARNINGS: <non-zero exits or stderr text that are healthy>
NEXT IF SUSPICIOUS: <exact step id — look-only, or a T1 gate>
NEVER CONCLUDE: <the overclaim this card prevents>
```

Field rules:
- **id**: pack-local, stable, referenced by scenarios and reports (e.g. `W-DEF-01`).
- **COMMAND**: one line. Typed slots use the Safety Core syntax and must name
  their source step: `<PID: digits only, from step 4>`.
- **NORMAL / SUSPICIOUS**: concrete values, not adjectives. "AntivirusEnabled:
  True" beats "looks healthy".
- **CANNOT TELL WHEN**: mandatory, never empty. If a command can run with
  limited visibility (no admin), say so here — limited view is CANNOT TELL,
  never NORMAL.
- **EXIT CODES / EXPECTED WARNINGS**: mandatory. Many healthy results look
  like failures; write them down or the stop rule misfires.
- **NEXT IF SUSPICIOUS**: a real step id in the same pack. Suspicion routes to
  more looking or a gated change — never straight to deletion.
- **NEVER CONCLUDE**: the specific false verdict this card exists to prevent.

## Worked example 1 — Windows Defender status (passive mode is NORMAL)

```
CARD W-DEF-01
COMMAND: Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled, AntivirusSignatureLastUpdated, AMServiceEnabled
TIER: T0
NORMAL LOOKS LIKE: AntivirusEnabled: True, RealTimeProtectionEnabled: True, signature date within the last 7 days. ALSO NORMAL: AntivirusEnabled: False while another antivirus product is registered (Defender is in passive mode) — ask step 3 which antivirus the user installed.
SUSPICIOUS LOOKS LIKE: AntivirusEnabled: False AND no other antivirus installed (high); signature older than 14 days (medium).
CANNOT TELL WHEN: command errors (Defender service missing/disabled by policy) — do not assume clean.
EXIT CODES / EXPECTED WARNINGS: none expected; any error = CANNOT TELL, go to step 3.
NEXT IF SUSPICIOUS: step 3 (identify installed antivirus), then the harden pack's gated enable steps.
NEVER CONCLUDE: "AntivirusEnabled: False means you are infected" — it usually means another antivirus is in charge, or protection was turned off. Neither is proof of malware.
```

## Worked example 2 — dnf check-update (exit 100 is healthy)

```
CARD L-UPD-02
COMMAND: dnf check-update
TIER: T0
NORMAL LOOKS LIKE: exit code 0 with "No packages marked for update" (fully patched), OR exit code 100 with a list of packages (updates available — normal, not an error).
SUSPICIOUS LOOKS LIKE: security-relevant packages (kernel, openssl, glibc, browser) many versions behind (medium) — route to the gated update step.
CANNOT TELL WHEN: network errors, repo errors, or the command is not found (wrong distro branch).
EXIT CODES / EXPECTED WARNINGS: exit 100 = updates exist, NOT a failure. Do not count it toward the two-errors stop rule.
NEXT IF SUSPICIOUS: step 5 (gated update install, T1).
NEVER CONCLUDE: "exit code 100 means the update check failed" — it means updates are waiting.
```

## Worked example 3 — unprivileged lsof (limited view is CANNOT TELL)

```
CARD M-NET-03
COMMAND: lsof -i -P -n | grep LISTEN | head -n 40
TIER: T0
NORMAL LOOKS LIKE: a short list of listeners owned by the user (e.g. a local dev server). grep exit 1 with no output = nothing listening for this user = NORMAL.
SUSPICIOUS LOOKS LIKE: a listener the user does not recognize, owned by the user, on an unusual port (low/medium) — go to step 6 to identify the process.
CANNOT TELL WHEN: run without sudo — system daemons (the interesting listeners) are invisible. A short or empty list here is NOT proof the machine has no listeners. Offer the T0-admin sudo variant.
EXIT CODES / EXPECTED WARNINGS: grep exit 1 = empty result = healthy. lsof may print permission warnings to stderr — normal without sudo.
NEXT IF SUSPICIOUS: step 6 (identify process, look-only).
NEVER CONCLUDE: "no listeners found" from an unprivileged run — you only saw your own processes.
```
