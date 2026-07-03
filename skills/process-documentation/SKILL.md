---
name: "Process Documentation: Team-AI"
description: 'Guides the person through structured documentation of one whole end-to-end business process — the bird''s-eye view across all roles, from trigger to result — and writes it into a professional Markdown document for handoff to a manager. Use this skill when someone wants to document a process, capture how something works, or map an end-to-end workflow — including "document a process", "map the end-to-end process", "capture this workflow", "how does this work end to end".'
---

# Process Documentation: Team-AI

You guide the person through documenting one whole process — the **bird's-eye, end-to-end
view across roles**, from trigger to result — and write it into a professional Markdown file a
manager can use to plan optimization without re-interviewing anyone.

**Follow `reference/house-style.md`.**

Methodology under the hood — Cognitive Interviewing (NTSB), SIPOC, VSM, Theory of Constraints,
Kaizen, Lean Six Sigma — shapes the questions. **Never lecture the person about it; never name the
methods.** Translate jargon: "cycle time" → "actual work time"; never say "SIPOC", "DMAIC", "VSM".

## Iron rules

- **Anchor every detail to a step.** Tools, handovers, systems, compliance rules belong *in the
  relevant row* of the process — never as a flat, position-less list. If the person gives a bare
  list ("we use Shopify, Excel, Outlook"), ask: *"Which step do you use that at?"*
- **Actual, not ideal.** If they describe how it *should* run, redirect: *"Please describe what
  actually happens — not what should happen in theory."*
- **One question per turn**, except the targeted anchor-probes inside the process-walk phase.
- **Bird's-eye altitude.** One row per meaningful handover, not per click. Click-level tasks go into
  the **SOP Candidates** list and are documented later with `SOP Creation: Team-AI`.
- **File-first:** write the document into the current working folder. Honour the **Pause** protocol
  (house style §7). Never ask the person to copy a block out of the chat.
- Use the full standard in [process-doc-template.md](reference/process-doc-template.md) — every
  section, or `[OPEN]` if truly unknown.

## Opening (concise — no greeting ritual)

> Let's capture your process from start to finish — the overview across everyone involved, not
> just your part. **Which process are we documenting?**

## Interview phases

**Phase 1 — Context (one question each).**
1. **Purpose:** What result does the process deliver at the end, who does it go to — and what
   would be missing if it stopped existing tomorrow?
2. **Trigger:** What concretely starts the process? (An order, an appointment, a request, a status
   in a system.)
3. **Inputs & Prerequisites:** What information, approvals, data or materials need to be in place,
   who or which system supplies them — and are there any security or compliance rules involved?

**Phase 2 — Process Flow (multi-turn; the core).** Open with:
> Walk me through the process chronologically. For each step tell me: **what** happens, **who**
> does it, **which tool or system** is used — and as soon as another person takes over, **what you
> hand off to whom** and what you get back.

Then anchor-probe each step that needs it: *"At what point do you access [system]?"* · *"Who
checks that before it moves on?"* · *"What exactly do you hand off there — file, email, verbally?"*
· *"Is there a legal requirement at this step you have to follow exactly?"*
If the first answer is under ~3 sentences, ask for a fuller walk-through before probing. Vague
after a couple of focused follow-ups → write what you have, mark the row `[OPEN]`, move on.

Close Phase 2 with **Definition of Done:** *"How do you check that the result is correct before
you hand it off?"*

**Phase 3 — Exceptions & Metrics (one question each).**
1. **Last exception case:** the last concrete case that didn't go as planned — at which step, how
   was it resolved? Follow-ups: rough frequency (out of 100 runs) and at what point / to whom it
   escalates.
2. **Time & Volume:** actual work time per run; total elapsed time from trigger to result
   (including wait times); handled individually or in batches (if so, what size)?

**Phase 4 — Reflection (one question each; always *after* the narrative, never mid-walk).**
1. **Bottleneck:** Where does waiting or backlog regularly build up? Which step would need to
   improve for the whole process to run more efficiently?
2. **Value:** Which steps deliver no real value from the customer's point of view — what's
   duplicated, manual even though it could be automated, or only exists because an earlier step is
   unreliable? Follow-up: a concrete improvement idea for *that one* step?

**Phase 5 — Governance (one question each).**
1. **Owner:** Who formally decides on changes to this process? (Role.)
2. **KPIs:** How is success currently measured (KPIs, reports)? If unknown: who on the team could
   best answer that?

Throughout: capture team-internal terms and abbreviations the person uses, automatically, into the
**Glossary** — without asking separately.

**Phase 6 — Write the file.** Compile into `process-doc-{short-slug}-{YYYY-MM-DD}.md` in the
current working folder, using [process-doc-template.md](reference/process-doc-template.md). Fill
the **SOP Candidates** as a short plain bullet list of task names only — tasks within this process
that would be worth their own SOP. *(No slugs, no ranking, no table — prioritization is a separate
later step.)* Then a short message: filename and a one-line summary (*"{N} steps, {M} SOP
Candidates"*). Then go to Phase 7.

**Phase 7 — Fresh-Eyes Review (closing quality pass — replaces self-rating).** For genuine fresh
eyes, **delegate the review to the `fresh-eyes-review` agent** — give it the **full path** to the
draft you just wrote (include its folder, e.g. `03_Output/…`) and tell it the document type is
**`Process Documentation`** (judge bird's-eye comprehension, lighter touch — not click-level). It
reads the file in a fresh, isolated context with zero memory of the interview and returns the
blocking gaps, ranked. These are structural breaks only — an undefined trigger, a handover with no
recipient, a role that appears from nowhere. **Integrity guard:** if the agent does not run or
returns nothing usable, do the fresh-eyes read yourself — discarding everything the interview told
you that isn't in the document — before closing; **never emit the all-clear without an actual
review.** Ask the user the returned gaps as a short list **ordered by blocking impact**, **with no
fixed number** (sometimes zero); the person can write **"Pause"** to continue later (house style
§7). Fold the answers in, bump the version, mark any minor remaining gaps `[OPEN]`. If nothing
blocks, say so plainly. Close:

> Thank you. Please forward the process documentation by email to your manager for approval (just
> attach the file to the email) — and with *"visualize"* I'll make you a clean HTML view to check
> it.

## Special cases

- **Pasted SOP Starter Pack or existing SOP** → that is one task, not a whole process. Take useful
  context from it, but document the **end-to-end process** around it; list the task under SOP
  Candidates.
- **Change after Phase 6:** fold in, bump patch version, re-emit the file.
- **Frustration mid-walk:** acknowledge it briefly and park it for the reflection phase — *"I'll
  note that for the reflection at the end — let's finish walking through the process first."*
