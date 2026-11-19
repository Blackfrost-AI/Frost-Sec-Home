# START HERE — Linux

**Status: UNTESTED.** These packs have not yet been verified end-to-end on a
real Linux desktop. Command syntax and exit codes were checked in Ubuntu
22.04 and 24.04 containers (see `verification/linux/look-only-receipts.txt`),
but full behavior on real desktops is untested; Fedora/Arch branches are
syntax-review only. They will be updated when tested. Prefer the look-only
steps.

## What this is

Paste-one-chat-at-a-time instruction packs that turn a small AI assistant
into a careful security helper for your Linux PC. The assistant shows you
one command at a time, you run it in a terminal and paste the output back,
and it interprets the result using built-in answer cards. It asks before
anything that changes your system. It never deletes files on a guess.

## What you need

- A Linux desktop: Ubuntu/Debian (apt), Fedora (dnf), or Arch (pacman).
  The packs ask which one first and use only your family's commands.
- An AI chat app that can run a pack of this size (16k context minimum).
  **Ollama users:** the default context (2048–4096) silently truncates these
  packs — set `num_ctx` to at least 16000, or the safety rules get cut off.
- A terminal (Ctrl+Alt+T on most desktops).
- For admin steps (marked T0-admin/T1): sudo access. The password prompt
  shows nothing while typing — that is normal. Type it and press Enter.

## How to use a pack

1. Open the pack file (start with `packs/linux/TRIAGE.md`).
2. Copy the ENTIRE file into a NEW chat as your first message.
3. Follow the assistant one step at a time. Run only the command it shows,
   paste only what it asks for (usually the first N lines).
4. When a step says T1, the assistant must ask and you must reply YES —
   one YES covers exactly one command. "YES to everything" is not accepted.
5. At the end it fills a report and names the next pack. Open that pack in
   a NEW chat, pasting the HANDOFF state block first. One pack per chat —
   long chats overflow the model's memory and it starts forgetting rules.

## The packs

| Pack | What it does |
|---|---|
| TRIAGE.md | First check-up: distro, firewall, ransomware signs |
| 01-verify-and-update.md | Package updates, automatic security updates |
| 02-harden.md | Backup net, ufw firewall, encryption check, lock |
| 03-network-check.md | Your address, home devices, listeners, router |
| 04-malware-scan.md | ClamAV install (approved), signatures, home scan |
| 05-persistence-hunt.md | Autostart, systemd units, cron, bashrc, hosts |
| 06-removal-and-recovery.md | Gated, reversible quarantine of confirmed items |
| INCIDENT-RANSOMWARE.md | Preserve, contain, recover — never pay |

## Hard rules (the packs enforce these; you should too)

- Look-only steps need no approval. Changes need your YES, one at a time.
- Nothing is permanently deleted: files move to ~/frost-sec-quarantine.
- Never paste passwords into the chat. sudo prompts are typed blind.
- Never scan a network you do not own — not the neighbor's, not a café's.
- Enabling a firewall on a PC you reach via SSH: allow ssh FIRST, or you
  lock yourself out. The packs ask about this.
- Ransomware signs (note + many renamed files): stop, unplug backup drives,
  pause cloud sync, open the INCIDENT pack. Never pay, never delete.
- If the assistant ever suggests `rm -rf`, mass deletion, piping curl to
  sh, or skipping approvals: stop. That is not this pack.

## If something goes wrong

- A command errors twice: stop that step, tell the assistant, move on.
- "command not found": your system may lack that tool — that is CANNOT
  TELL, not "all clear". The assistant should say so.
- The assistant forgets rules mid-chat: the chat got too long. Start a NEW
  chat with the next pack and the HANDOFF block.
- You quarantined something by mistake: move it back from
  ~/frost-sec-quarantine (the assistant guides you).
- Real incident: the report the assistant fills is what you hand a
  professional. Keep it.
