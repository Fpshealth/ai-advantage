---
name: "Clear Explanation: Team-AI"
description: Explain a system, process, decision or concept to an intelligent reader who is new to it. Use when writing an explainer, guide, handbook or report that explains how something works.
disable-model-invocation: true
---

# Clear explanation

**Follow `reference/house-style.md`.** Page language follows §1. Files go where §3 says. People
appear by role (§2), never by name.

**Outcome:** an intelligent reader who is new to the subject reads the page once. The page gives them enough context and depth that, after reading, they can explain the system to someone else, run or use it, and see when it breaks.

This is hard because you have more context than the reader. Each source you touched or learned from while you worked has a definition in your head and none in theirs. So the work has three parts: define clearly what the page explains and write the facts down first, write a deep explainer rich in context that hands each fact to the reader, and let a script and a fresh reader prove its quality.

Build the page, its images and `inventory.md` together in one folder in the work area. When step 3 passes, copy the page and its images to the output area.

## 1. Collect the facts

Read the sources first: the files the person gives you or names (in the input area, or in a connected source such as SharePoint; a `pitch-*.md` is one: then the page explains the pitched idea and links the pitch), the documents and data linked from them, and the person's own answers. Ask the person what they want to explain and who will read it. Then, before any prose, write `inventory.md` next to the page: one row per thing the reader will meet (a file, program, data source, role, decision or key number). Fill each cell from a source, or mark it open and state the open question in the page at that point. [reference/inventory.md](reference/inventory.md) gives the columns, the picture plan and the link forms for sources.

## 2. Write the red thread

The page is one path through the system, and every part of it serves the outcome:

- It starts with the problem, then one paragraph on the whole system that the reader could repeat to their boss.
- Each section answers one question the reader would ask, and opens with that question.
- The order is such that nothing is used before it is explained. Define each thing literally where it first appears, and use the same name for it everywhere.
- Where the sources have one, a real case (real values, real output) runs through every section to its end. The case comes first, the general rule after it.
- Each claim gives its reason, its status (verified, someone's claim, inferred or open) and a source the reader can click.
- Show the real thing wherever a visual is faster than a sentence: a screenshot, real output, a diagram or a step-through. [reference/pictures.md](reference/pictures.md) says how to get and embed each kind.
- The length follows what the reader must do afterwards. Material that serves none of it goes to an appendix.

Then apply [reference/writing-rules.md](reference/writing-rules.md).

## 3. Prove it

The page is done when both checks pass. Do not hand it over before.

1. **Format.** From this skill's folder, run:

   `python3 scripts/lint.py <file.html> --render --shots <dir> [--old <previous.html>]`

   If `uv` is installed, put `uv run --python 3.13 --with playwright` in front. If the shell cannot open `scripts/lint.py`, read the file and pipe its content: `python3 - <file.html> --render --shots <dir> <<'PY' … PY`. Without Playwright the script skips the diagram text-size check and the figure PNGs, and says so in a `note` line.

   The script is the list of format rules; its docstring names each one. Fix every FAIL line until the last line is `PASS`. Fix the page or the inventory to match the sources, never the check. Lines that start with `note` do not fail; use them for the writing-rules pass.

2. **Understanding.** You cannot judge your own page for a newcomer, so a fresh subagent (Opus, where you can choose the model) reads it as [reference/cold-read.md](reference/cold-read.md) describes. The page passes at `Verdict: PASS`. Check each finding against the source before you fix it, then run step 1 again. Stop after three rounds in total.

Report each blocking finding that is still open as an open issue, and each non-blocking finding you did not fix as a note.

## When a reader asks a question

A question such as "What is this?" shows where the page failed that reader. Check the answer in the inventory and its source, answer the reader, and fix the passage so the next reader does not need to ask.
