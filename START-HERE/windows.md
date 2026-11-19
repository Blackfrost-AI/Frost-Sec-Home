# START HERE — Windows

This page gets you ready in about 5 minutes. No experience needed.

## 1. Pick your AI assistant

The packs work with any chat-style AI. Two options:

- **Private option (recommended): a local model.** Install Ollama
  (ollama.com) or LM Studio (lmstudio.ai), then download a small instruct
  model — for example `qwen2.5:7b-instruct` in Ollama. Everything stays on
  your PC.
  **Important setting:** these tools often default to a small memory window
  that silently cuts off long prompts. In Ollama, set the context length to
  at least 16000 (in LM Studio: "Context Length" = 16384). If you use
  `ollama run`, create a Modelfile with `PARAMETER num_ctx 16384` — the
  default 2048/4096 will truncate the packs.
- **Hosted option: a web chatbot.** Works, but know this: everything you
  paste (command output, file names) goes to that company's servers. The
  packs never ask for passwords or document contents, but the output itself
  is still shared. If that's not okay for you, use the local option.

## 2. Open PowerShell (where you'll paste commands)

1. Click the **Start** button.
2. Type `powershell`.
3. Click **Windows PowerShell** in the results.
4. A blue (or black) text window opens. This is where commands go.

**Some steps need administrator rights.** When a pack step says T0-admin or
asks for elevation: close PowerShell, click Start, type `powershell`,
**right-click** Windows PowerShell, choose **Run as administrator**, click
Yes on the prompt. The window title will say "Administrator".

## 3. Paste your first pack

1. Open `packs/windows/TRIAGE.md` in this repo (any text editor, or on the
   website click the file and the "raw" view).
2. Select ALL of it (Ctrl+A), copy (Ctrl+C).
3. Paste it into your AI chat as your FIRST message (Ctrl+V), send.
4. The assistant will walk you through one step at a time. When it shows a
   command in a code block: click the block's copy button (or select and
   Ctrl+C), click into PowerShell, right-click to paste, press Enter.
5. Copy the output (select it, Ctrl+C) and paste it back to the assistant.

## Your safety rail — read this once, remember it forever

**Only run a command that the assistant shows you in a code block AFTER you
replied YES.** If it suggests anything else — a command not printed in the
pack, a download, "just trust me" — stop. Close the chat. Nothing in these
packs ever needs you to run something the pack didn't print.

Also: the packs are a careful draft until their status table in the README
says verified. Prefer the look-only steps while a pack is UNTESTED.

## What to expect

- Triage takes ~10 minutes. It ends by telling you which pack to open next.
- **Each new pack goes in a NEW chat**, with the handoff summary pasted
  first. This keeps the safety rules inside the AI's memory.
- Nothing changes on your PC without your explicit YES, one command at a
  time.
