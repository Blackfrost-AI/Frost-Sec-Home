# Threat Model — what Frost-Sec-Home protects against, and what it cannot

This document is the honest boundary of the project. The README repeats the
short version; packs reference these limits inline.

## Who this is for

A home user with a personal Windows, macOS, or Linux computer who is not
technical, using an AI assistant (ideally a small local model) as a guided
pair of hands. The user's own network is in scope; nothing else is.

## What the packs defend against (design targets)

1. **Commodity malware** that built-in tooling can detect: Windows Defender,
   macOS XProtect / XProtect Remediator, ClamAV on Linux.
2. **Misconfiguration** — the most common real-world home risk: protection
   turned off, firewall off, no updates, weak login/lock settings, admin
   account used for daily work.
3. **Unwanted persistence** — startup items, scheduled tasks, launch agents,
   cron jobs, and services that a user did not choose, surfaced for review
   with strong false-positive guardrails.
4. **Ransomware incidents** — early recognition, evidence preservation,
   containment (network + backup drives + cloud sync), and routing to
   recovery paths and professional help. Not decryption promises.
5. **Social-engineering false alarms** — browser notification scams and fake
   "your PC is infected" popups are explicitly recognized as the common
   non-infection they are.
6. **AI-assistant mistakes** — the packs themselves are hardened against a
   small model inventing commands, overclaiming infection, complying with
   injected instructions in tool output, or acting without approval.

## What the packs explicitly do NOT defend against

- **Rootkits, bootkits, firmware/UEFI implants.** Built-in userland checks
  cannot see these. A clean result never rules them out.
- **Targeted attackers** (someone specifically after this user), zero-days,
  and supply-chain compromise of trusted software.
- **Compromise of the AI assistant itself** — a malicious or jailbroken model
  is outside what prompt text can fully control. The user-side rail (only run
  code-block commands after YES) is the backstop, and it is imperfect.
- **Network equipment compromise** beyond a guided checklist (router password,
  firmware update prompt, WPA2/WPA3 check). No router exploitation, no ISP-side
  checks, no IoT deep inspection in v1.
- **Data already exfiltrated.** Detection of past theft is generally not
  possible with these checks; packs say so rather than implying otherwise.
- **Physical access attacks** (someone at the keyboard, evil-maid).

## Trust assumptions

- The operating system's built-in tools are assumed trustworthy. If the OS is
  deeply compromised, its own reports cannot be trusted — packs note this
  limit where it matters (e.g., "found nothing ≠ guaranteed clean").
- The user is assumed honest about owning the network being checked, and is
  asked to confirm it. The packs refuse public ranges regardless.
- Local-model use keeps system data on the machine. Hosted-chatbot use shares
  every pasted output with the provider — disclosed, never hidden.

## Escalation rule

Anything beyond the design targets — confirmed ransomware, suspected rootkit,
repeat reinfection, a targeted-attack story — ends in: stop, preserve evidence,
get professional help. The packs are a first-response and hygiene tool, not an
incident-response firm.
