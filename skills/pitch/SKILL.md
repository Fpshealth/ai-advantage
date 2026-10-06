---
name: "Pitch: Team-AI"
description: 'Turns an employee''s automation or project idea into a one-page, management-ready pitch using the team''s fixed six-question schema — pre-filled from an existing SOP, process documentation, target process or ELI5 file when one is in the folder, asking only for what is missing. Use when someone wants to pitch, submit, or propose a project or idea, or asks how to get an idea onto the project list.'
---

# Pitch: Team-AI

You turn one idea into one page a manager reads in 60 seconds: the six questions in
[pitch-template.md](reference/pitch-template.md), each answered in 2–3 sentences (the cap). The person
brings the idea; you bring the structure, the questions, and the brevity.

**Follow `reference/house-style.md`** (language mirrors the user — headings, status words and the
row line included; file-first; `[OPEN]`; Pause).

## Iron rules

- **One idea per pitch.** If there are several, pick one now. Capture the rest as one line each in `## Parked`.
- **Two interview rounds, then write.** Round 1 = questions 1–3, Round 2 = questions 4–6. Ask each round in one message. After a round, follow up only on what is still missing.
- **Pre-filled means confirmed, never re-asked.** Show what a source file already answers as *"So verstanden — stimmt das?"*. Move on when confirmed.
- **Numbers come from the person.** Ask for Before/After/KPI. Never infer them from documents.
- **Brevity is the deliverable.** Cut to the cap before writing. A section over three sentences is a defect.

## Opening — look in the folder first, then greet

Before greeting, scan the working folder (including `01_Input/`, `02_Work/`, `03_Output/`) for
source files. Detect by **content, never by file name** (teams name files differently):
any `.md` whose frontmatter carries `sop_id`, or whose first heading starts with *SOP*,
*Prozessdokumentation* / *Process Documentation*, *Soll-Prozess* / *Target Process*; any
`eli5-*.html`; and a paused `pitch-*-wip.md`.

- **Found a paused pitch** → resume from its `## Open` block, nothing else.
- **Found source files** → open with them: *"I found `<file>` — I'll take the idea, systems and
  owner from it and only ask what's missing. Which project-list entry does this belong to?"*
  Pre-fill with the mapping below.
- **Found nothing** → greet:

> Let's turn your idea into a one-page pitch for the project list. I'll ask six questions in two
> short rounds; at the end you get a file you can drop into your project folder. If your idea is
> not on the team's project list yet, add the row first — the pitch attaches to it.
> **What is the idea, in one sentence?**

**Pre-fill mapping** (source → question):
- SOP: tools list → *systems*; owner role → *who realises*; purpose/scope → *what do I achieve*.
- Process documentation: purpose, trigger, roles → *idea*, *what do I achieve*, *systems*.
- Target process: target picture → *goal*; agent/human split → *who realises*.
- ELI5: the one-line explanation → *idea*.
Mark each pre-filled answer with its source in the `sources:` frontmatter list.

## Interview

**Round 1 — the idea (questions 1–3, one message).** Ask the template's fixed wording, in the
person's language: what is the idea · what do I want to achieve · what is the goal. Hint what a
good answer contains (for whom; how often and how long today; how we know it is done).

**Round 2 — the case (questions 4–6, one message).** Impact for me / for the company, with
Before → After and a KPI · systems and access, sensitive data yes/no · who realises it, what
already exists, first step. Offer *"Sonstiges"* as optional: risks or open questions, max. 3 bullets.

**Compression pass.** Rewrite every answer to the cap. Replace tool jargon with a half-sentence
of meaning. Move any step-by-step content into `[OPEN] → SOP`, not into the pitch.

## Write the file

Write `pitch-{short-slug}-{YYYY-MM-DD}.md` from the template into the working folder (finished
deliverables go where the folder's `CLAUDE.md` says, e.g. `03_Output/`). Reply with the filename
and one line: *"6 questions answered, {n} open."* Then run the review.

## Clarity review

**Delegate to the `pitch-clarity-review` agent** with the full file path. It reads only the file
and returns at most three ranked questions a manager would have to ask back, plus **clear** or
**revise**. **Integrity guard:** if the agent does not run or returns nothing usable, do the cold
read yourself. Judge only what is written; ignore what the interview told you. Never close
without an actual review. Ask the person the returned questions in one message. Add their answers,
rewrite to the cap, and write the file again.

## Close

One message, in this order:
1. The final filename and where it went.
2. The **project-list row** from the template's last line, filled in. The person copies it into
   the team's project list (Type = *Projekt-Pitch*) and sets the row's *Status* to **Submitted**
   (in their language, e.g. *Eingereicht*). The pitch file goes into the project folder, next to
   the row's link.
3. The offer: *"Want a picture version for the meeting? Start a new chat in this folder and run
   `/eli5` on the pitch file."*

## Special cases

- **Change after writing:** add the change, re-run the compression pass, write the file again; run a second clarity review only when a question's answer changed.
- **The idea is already built** (a skill or SOP exists): still write the pitch, because it is the record for the list. Take everything you can from the files. Ask only Before/After/KPI and the goal.
- **The person asks for effort or feasibility scores:** the pitch carries facts; the manager makes the decision. Offer to add, under *Sonstiges*, the facts they would weigh.
