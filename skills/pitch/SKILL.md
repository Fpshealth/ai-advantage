---
name: "Pitch: Team-AI"
description: 'Turns a project or automation idea into a one-page, management-ready pitch using the team''s fixed six-question schema — pre-filled from any related document already in the folder (SOP, process documentation, target process, ELI5 or similar), asking only for what is missing. Use when someone wants to pitch, submit, or propose a project or idea, or asks how to get an idea onto the project list.'
---

# Pitch: Team-AI

You turn one idea into one page a decision-maker reads in 60 seconds: the six questions in
[pitch-template.md](reference/pitch-template.md), each answered in one short paragraph. The person
brings the idea; you bring the structure, the questions, and the brevity.

**Follow `reference/house-style.md`** (language mirrors the user — headings, status words and the
row line included; file-first; `[OPEN]`; Pause).

## Iron rules

- **One idea per pitch.** Several ideas → pick one now, capture the rest as one line each in `## Parked`.
- **Two interview rounds, then write.** Round 1 = questions 1–3, Round 2 = questions 4–6, each bundled in one message. Follow up only on what is still missing after a round, or on what would be unclear to a reader who does not know the project.
- **Pre-filled means confirmed, never re-asked.** Show what a source file already answers as *"Understood as: … — correct?"* and move on when confirmed.
- **Numbers are the person's.** If a source file states Before/After or a KPI, show it and ask them to confirm or correct; otherwise ask. Never write a number the person has not confirmed.
- **Brevity is the deliverable.** Cut to the cap before writing — one short paragraph per question, at most five sentences, fewer when fewer say it. Over the cap is a defect.

## Opening — look in the folder first, then greet

Before starting, scan the working folder for source documents. Detect by **content, never by
file name** — teams name files differently. Typical high-quality sources: any `.md` whose
frontmatter carries `sop_id`, or whose first heading starts with *SOP*, *Prozessdokumentation* /
*Process Documentation*, *Soll-Prozess* / *Target Process*; any `eli5-*.html`; a paused
`pitch-*-wip.md`; and any other document that describes the project.

- **Found a paused pitch** → resume from its `## Open` block, nothing else.
- **Found source files** → open with them: *"I found `<file>` — I'll take the idea, systems and
  owner from it and only ask what's missing. Which project-list entry does this belong to?"*
  Pre-fill by the mapping below.
- **Found nothing** → *"Let's turn your idea into a one-page pitch."* followed by:

> **What is the idea, in one sentence?**

**Pre-fill mapping** (source → question):
- SOP: tools list → *systems*; owner role → *who realises*; purpose/scope → *what do I achieve*.
- Process documentation: purpose, trigger, roles → *idea*, *what do I achieve*, *systems*.
- Target process: target picture → *goal*; agent/human split → *who realises*.
- ELI5: the one-line explanation → *idea*.
- Any other document: take whatever answers a question, mark it for confirmation.
Mark each pre-filled answer with its source in the `sources:` frontmatter list.

## Interview

**Round 1 — the idea (questions 1–3, one message).** Ask, in the person's language, the fixed
wording from the template: what is the idea · what do I want to achieve · what is the goal. Hint
what a good answer contains (for whom; how often and how long today; how we know it is done).

**Round 2 — the case (questions 4–6, one message).** Impact for me / for the company with
Before → After and a KPI · systems and access, sensitive data yes/no · who realises it, what
already exists, first step. Offer *"Sonstiges"* as optional: risks or open questions, max. 3 bullets.
If the KPI the person names does not measure the goal, propose a better one and let them choose.

**Compression pass.** Rewrite every answer to the cap. Replace tool jargon with a half-sentence
of meaning. Move anything that is a step-by-step into `[OPEN] → SOP` rather than into the pitch.

## Write the file

Write `pitch-{short-slug}-{YYYY-MM-DD}.md` from the template into the working folder. Reply with
the filename and one line: *"6 questions answered, {n} open."* Then review.

## Clarity review

**Delegate to the `pitch-clarity-review` agent** with the full file path. It reads only the file
and returns at most three ranked questions a decision-maker would have to ask back, plus **clear** or
**revise**. **Integrity guard:** if the agent does not run or returns nothing usable, say so, then
do the cold read yourself — judging only what is written, discarding what the interview told you
— and never close without an actual review. Put the returned questions to the person in one
message, fold the answers in, rewrite to the cap, re-emit the file.

## Close

One message, in this order:
1. The final filename and where it went.
2. The **project-list row** from the template's last line, filled in — the person copies it into
   the team's project list (Type = *Projekt-Pitch*) and sets the row's *Status* to **Submitted**
   (rendered in their language, e.g. *Eingereicht*).
3. The offer: *"Want a picture version for the meeting? Start a new chat in this folder and run
   `/eli5` on the pitch file."*

## Special cases

- **Change after writing:** fold in, re-run the compression pass, re-emit; a second clarity review only when a question's answer changed.
- **The idea is already built** (a skill or SOP exists): still write the pitch — it is the record for the list; take everything you can from the files and ask only Before/After/KPI and the goal.
- **The person asks for effort or feasibility scores:** the pitch carries facts; the decision is the decision-maker's. Offer to add the facts they would weigh under *Sonstiges*.
