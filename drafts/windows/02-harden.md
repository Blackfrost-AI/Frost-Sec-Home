---
pack_id: windows-harden
os: windows
os_versions: ["10 22H2", "11"]
shell: powershell
privilege: admin-mixed
pack_type: module
safety_core_version: 4
min_context_tokens: 16000
verification_status: untested
---
> **UNTESTED:** commands in this pack have not yet been verified on a real system. They will be updated when tested. Prefer the look-only steps.

{{SAFETY_CORE}}

# Windows — harden (turn on the protections that should be on)

First a restore point (a way back), then changes — each needs your YES.

## Step 0 — confirm this is the right pack

Ask: "Are you on a Windows PC?" If not, stop and name the right pack.

## Self-check

1. What must exist before the first change in this pack?
2. How many commands does one YES authorize?
3. What does "managed by your organization" mean here?

## Step 1 — restore point FIRST (T1)

FULL APPROVAL. WHAT: a restore point. WHY: a way back. RISK: a little disk,
a minute. UNDO: it is the undo. Wait for YES.

```command
Checkpoint-Computer -Description "Frost-Sec-Home before hardening"
```

```card
CARD W-HAR-01
COMMAND: Checkpoint-Computer -Description "Frost-Sec-Home before hardening"
TIER: T1
NORMAL LOOKS LIKE: no output after ~a minute = created.
SUSPICIOUS LOOKS LIKE: none; see expected refusals below.
CANNOT TELL WHEN: other errors — continue only with informed YES — no rollback net.
EXIT CODES / EXPECTED WARNINGS: (1) "System protection is disabled" / "restore point creation is disabled" = OFF — Step 1b. (2) A point from the last 24h = NORMAL; it is your net, continue. Neither counts toward the two-errors stop.
NEXT IF SUSPICIOUS: Step 1b if protection is off.
NEVER CONCLUDE: "refusal means hardening is impossible" — both refusals have normal paths.
```

## Step 1b — enable System Protection (guided, T1, only if Step 1 refused)

FULL APPROVAL. WHAT: enable System Protection on C:. WHY: restore points
need it. RISK: a few GB disk. UNDO: same screen, Disable. Wait for YES;
guide the clicks; then repeat Step 1 with a fresh YES.

```card
CARD W-HAR-02
COMMAND: GUI: Start > "Create a restore point" > C: drive > Configure > "Turn on system protection" > OK > OK
TIER: T1
NORMAL LOOKS LIKE: Protection On for C:; Step 1 then succeeds.
SUSPICIOUS LOOKS LIKE: option greyed out (policy) — stop, NEEDS A HUMAN.
CANNOT TELL WHEN: window differs — stop, never improvise.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "no restore point means skip safety" — proceed-with-warning only.
```

## Step 2 — firewall check (look-only)

```command
Get-NetFirewallProfile | Select-Object Name, Enabled
```

```card
CARD W-HAR-03
COMMAND: Get-NetFirewallProfile | Select-Object Name, Enabled
TIER: T0
NORMAL LOOKS LIKE: Domain/Private/Public all True.
SUSPICIOUS LOOKS LIKE: any profile Enabled: False (medium/high) — Step 3.
CANNOT TELL WHEN: errors — note it.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: Step 3.
NEVER CONCLUDE: "firewall off means hacked" — it means exposed.
```

## Step 3 — turn the firewall on (T1, only if a profile is off)

FIRST save Step 2's list — it is the undo. FULL APPROVAL. WHAT: enable all
profiles (`-All`; True stays True). WHY: block unwanted connections. RISK:
an app may re-ask port permission. UNDO: only profiles that were False,
one per YES: `Set-NetFirewallProfile -Name <profile> -Enabled False`.
NEVER `-All -Enabled False`. Wait for YES.

```command
Set-NetFirewallProfile -All -Enabled True
```

```card
CARD W-HAR-04
COMMAND: Set-NetFirewallProfile -All -Enabled True
TIER: T1
NORMAL LOOKS LIKE: no output = done; re-run Step 2 to confirm.
SUSPICIOUS LOOKS LIKE: error (medium) — policy-managed; stop, NEEDS A HUMAN.
CANNOT TELL WHEN: errors twice — stop.
EXIT CODES / EXPECTED WARNINGS: none.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "firewall on means nothing gets in" — reduced exposure, not a guarantee.
```

## Step 4 — Defender real-time protection (guided, T1)

Tamper Protection blocks PowerShell here — do it by hand. FULL APPROVAL.
WHAT: real-time protection On. WHY: catch malware as it runs. RISK: Defender
may quarantine a flagged file. UNDO: same screen, toggle off. Wait for YES.

```card
CARD W-HAR-05
COMMAND: GUI: Start > "Windows Security" > Virus & threat protection > Manage settings > Real-time protection On
TIER: T1
NORMAL LOOKS LIKE: shows On. ALSO NORMAL: another antivirus registered, Defender passive — leave it.
SUSPICIOUS LOOKS LIKE: switches refuse to move, no other antivirus (medium) — policy or tampering; NEEDS A HUMAN.
CANNOT TELL WHEN: layout differs — stop, never improvise.
EXIT CODES / EXPECTED WARNINGS: "managed by your organization" on a home PC = CANNOT TELL. Refused switch with Tamper Protection On = self-protection.
NEXT IF SUSPICIOUS: NEEDS A HUMAN.
NEVER CONCLUDE: "greyed switch means infection" — usually policy.
```

## Step 5 — account and lock check (guided look-only)

Guide the card's three panes, read-only. Admin daily account? Standard is
safer — recommendation only; never change accounts here.

```card
CARD W-HAR-06
COMMAND: GUI: Settings > Accounts / Sign-in options / Lock screen — read-only
TIER: T0
NORMAL LOOKS LIKE: standard daily account; sign-in on wake; lock within 10 min.
SUSPICIOUS LOOKS LIKE: admin daily account + no lock (low) — recommendations only.
CANNOT TELL WHEN: pane not found — note it.
EXIT CODES / EXPECTED WARNINGS: pane names vary by version.
NEXT IF SUSPICIOUS: recommendations in the report.
NEVER CONCLUDE: "admin account means compromised" — hygiene risk.
```

## Report

Fill the REPORT SKELETON: changes + undo. HANDOFF:
`packs/windows/03-network-check.md` in a NEW chat, HANDOFF state first.
