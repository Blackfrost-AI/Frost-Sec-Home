# START HERE — macOS

**Status: UNTESTED.** These packs have not yet been verified end-to-end on a
real Mac. They are written from documented macOS behavior and will be
updated when tested. Prefer the look-only steps; be extra careful with
anything marked T1.

## What this is

Paste-one-chat-at-a-time instruction packs that turn a small AI assistant
into a careful security helper for your Mac. The assistant shows you one
command at a time, you run it in Terminal and paste the output back, and it
interprets the result using built-in answer cards. It asks before anything
that changes your Mac. It never deletes files on a guess.

## What you need

- A Mac running macOS 13 Ventura or newer.
- An AI chat app that can run a pack of this size (16k context minimum).
  **Ollama users:** the default context (2048–4096) silently truncates these
  packs — set `num_ctx` to at least 16000, or the safety rules get cut off.
- Terminal: press Command+Space, type `Terminal`, press Return.
- For admin steps (marked T1-admin): you need an administrator account.
  Terminal asks for your login password; typing shows nothing — that is
  normal. Type it and press Return.

## How to use a pack

1. Open the pack file (start with `packs/macos/TRIAGE.md`).
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
| TRIAGE.md | First check-up: version, protection, ransomware signs |
| 01-verify-and-update.md | macOS updates, automatic updates, XProtect |
| 02-harden.md | Time Machine, FileVault, Gatekeeper, firewall, lock |
| 03-network-check.md | Your address, home devices, listeners, router |
| 04-malware-scan.md | XProtect check, app review, signature verify |
| 05-persistence-hunt.md | Launch items, login items, cron, hosts file |
| 06-removal-and-recovery.md | Gated, reversible removal of confirmed items |
| INCIDENT-RANSOMWARE.md | Preserve, contain, recover — never pay |

## Hard rules (the packs enforce these; you should too)

- Look-only steps need no approval. Changes need your YES, one at a time.
- Nothing is permanently deleted: apps and items go to Trash first.
- Never paste passwords into the chat. Terminal prompts are typed blind.
- Never scan a network you do not own — not the neighbor's, not a café's.
- Ransomware signs (note + many renamed files): stop, unplug backup drives,
  pause cloud sync, open the INCIDENT pack. Never pay, never delete.
- If the assistant ever suggests `sudo rm -rf`, mass deletion, disabling
  Gatekeeper/SIP, or skipping approvals: stop. That is not this pack.

## If something goes wrong

- A command errors twice: stop that step, tell the assistant, move on.
- The assistant forgets rules mid-chat: the chat got too long. Start a NEW
  chat with the next pack and the HANDOFF block.
- You removed something by mistake: Trash > right-click > Put Back.
- Real incident: the report the assistant fills is what you hand a
  professional. Keep it.
