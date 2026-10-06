---
name: "Sandbox Setup: Team-AI"
description: 'Sets up the safe work area for Claude inside the folder that has already been granted: creates the three subfolders 01_Input, 02_Work, and 03_Output, and writes the CLAUDE.md rules file. Use this skill when someone wants to set up their sandbox, workspace, or work folders, or asks to run setup.'
---

# Sandbox Setup: Team-AI

You turn the folder the person has **already granted you** into the Team-AI work area: three
subfolders and a `CLAUDE.md` rules file.

**Follow `reference/house-style.md`.**

## Before creating anything

You can act only inside the granted folder. The person creates that top folder: a **new,
empty** folder named `AI_SANDBOX`, which they drag into a Cowork chat and allow.

If it's unclear that the granted folder is new and empty, or if it looks like a real working
folder with the person's actual files in it, ask first. Have them create and grant a fresh
folder instead.

## What to create

Leave anything that already exists untouched. Report it; do not replace it.

1. **Three subfolders:** `01_Input/`, `02_Work/`, `03_Output/`.
2. **`CLAUDE.md`** in the folder root, with the exact content of
   [sandbox-claude-template.md](reference/sandbox-claude-template.md). If one already exists,
   show what would change and ask before replacing it.
3. **`01_Input/_README.md`** — one short note, in the person's language: only **copies** belong
   here, never originals; Claude reads in `01_Input`, works in `02_Work`, delivers to
   `03_Output`.

## Confirm

Close with a short message in the person's language: what you created, plus the daily flow —
copy (never move) files into `01_Input`, then start a skill or describe the task, and find the
results in `03_Output`. The rules live in `CLAUDE.md`; do not repeat them in chat.
