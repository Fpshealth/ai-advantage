---
name: "Sandbox Setup: Team-AI"
description: 'Sets up the safe work area for Claude inside the folder that has already been granted: creates the three subfolders 01_Input, 02_Work, and 03_Output, and writes the CLAUDE.md rules file with safety and filing rules. Use this skill when someone wants to set up their workspace or folders — triggers: "set up the sandbox", "set up my workspace", "create the work folders", "set up AI_SANDBOX", "run setup". IMPORTANT: this skill cannot create the top-level AI_SANDBOX folder itself — the person must first manually create it outside any cloud-sync folder (e.g. OneDrive) and grant it in Cowork.'
---

# Sandbox Setup: Team-AI

You turn the folder the person has **already granted you** into the safe Team-AI work area: three
subfolders and a `CLAUDE.md` rules file.

**Follow `reference/house-style.md`.** Output is in the user's language by default (English, per
`client_language`); these instructions are English.

## The hard limit you must respect (and explain)

You can only act **inside the folder the person has dragged into the chat and allowed** — you **cannot**
create that top folder yourself. So the manual first steps stay with the person:

1. They create a **new, empty** folder named `AI_SANDBOX`, **outside any cloud-sync folder** (e.g.
   OneDrive, Dropbox, Google Drive) — what matters is that it's a **dedicated new** folder, **not** one
   of their real working folders.
2. They drag it into a Cowork chat and click **"Always allow."**
3. *Then* they run this skill.

If it is **not clear that you have write access to a suitable folder** — or the folder looks like a real
working folder with the person's actual files in it — **stop and ask** before creating anything:

> Before I start: I'll set everything up **inside the folder you just granted me**. Is this a **new,
> empty** folder you created just for working with me (and **not** one of your real working folders)?
> If yes, I'll go ahead and create the three subfolders and the rules file now. If no, please create a
> folder like that first and drag it into the chat window.

## What to create

Create these inside the granted folder. **Never overwrite or delete anything that already exists** —
if a subfolder or file is already there, keep it and report it instead of replacing it.

1. **Three subfolders** (skip any that already exist):
   - `01_Input/`
   - `02_Work/`
   - `03_Output/`

2. **`CLAUDE.md`** in the folder root — write it with the exact content of
   [sandbox-claude-template.md](reference/sandbox-claude-template.md).
   - If a `CLAUDE.md` already exists, do **not** silently overwrite it. Show what would change and ask:
     *"There's already a `CLAUDE.md` in this folder. Should I replace it with the current Team-AI
     version, or leave it as is?"*

3. **A short reminder in `01_Input/`** — write `01_Input/_README.md` with one line so the rule is
   visible right where files get dropped (skip if it already exists):

   ```markdown
   # Copies only here — never originals.
   Claude only reads here. Editing happens in `02_Work`, finished work lands in `03_Output`.
   ```

## After creating — confirm and point to the next step

Write a short message: what you created, and the daily flow. Do **not** dump the rules back into
the chat.

> **Done — your workspace is set up.** I've created:
> `01_Input/` (copies go here, read-only) · `02_Work/` (workshop) · `03_Output/` (finished results) ·
> `CLAUDE.md` (the rules I'll follow automatically from now on).
>
> **Here's how you'll work from now on:** Copy the files you want me to work with into `01_Input`
> (always **copy**, never move). Then start a skill — *"SOP Creation"*, *"Process Documentation"*,
> *"Prompt Improvement"* — or just describe your task to me. You'll find the finished result in
> `03_Output`.

## Safety

- Act **only** inside the granted folder; never touch anything outside it.
- Never delete or overwrite existing files without asking first.
- If a write fails, say so plainly and tell the person what to create by hand — do not pretend
  it worked.
