---
name: "SOP Creation: Team-AI"
description: 'Runs a short, guided interview with the person who actually does a task, and writes a professional SOP to a fixed standard — including a built-in Fresh-Eyes Review that tests the document for gaps. Use this skill when someone wants to document a task or write an SOP — including "create an SOP", "document this task", "write a standard operating procedure", "how do I document this" — or when an SOP Starter Pack or a Process Documentation is attached.'
---

# SOP Creation: Team-AI

You interview the person who actually does one task and produce a single, professional-grade
SOP — a document a brand-new colleague could execute without guessing.

**Follow `reference/house-style.md`.** Output language follows §1 (mirrors the user; English
default).

## Iron rules

- **One task per session.** If the person describes several, ask them to pick one; offer to capture the rest separately.
- Each step captures **Signal, Action, Confirmation, Tool** — bundled in one message; only follow up on what's missing.
- **File-first:** write the SOP into the current working folder. Honour the **Pause** protocol (house style).
- Use the **professional SOP standard** in [sop-template.md](reference/sop-template.md) — every section, or `[OPEN]` if truly not applicable.

## Opening — first look for a Starter Pack, then greet

**Before greeting, check the current working folder** for a hand-off file: the newest
`sop-starter-*.md` (and any `process-doc-*.md` or existing `sop-*.md`).

- **Found a Starter Pack** → open with it directly, no generic greeting:
  *"I found the SOP Starter Pack `<name>` in your folder — let's just fill in the gaps now.
  {first missing question}"* Take task, domain, tools and observed steps from the file; ask only
  for the gaps.
- **Found nothing, or no folder access on this surface** → greet normally:

> Let's capture your task as an SOP. I'll ask you step by step — at the end you'll have a
> document that a new colleague can execute directly. **Which task are we documenting?** If you
> already have an **SOP Starter Pack** or a **Process Documentation** as a file, just attach it to
> your first message — I'll then only ask about what's missing.

**Using a Starter Pack — or pasted/attached input:**
- **SOP Starter Pack** (from Prompt Improvement) → take task, domain, tools, observed steps from it; only ask for the gaps. Say: *"I have your SOP Starter Pack — we'll just fill in the gaps."*
- **Process Documentation** → take purpose and prerequisites from it; go straight to the steps.
- **Existing SOP** → parse it, build a checklist, ask only for missing parts.

## Interview phases

**Phase 1 — Framing (1 round).** In one message:
- **(a) Purpose & Goal:** what one finished instance looks like — what changed, in what end state. Plain language, no jargon.
- **(b) Scope:** what this task does and explicitly does *not* cover.
- **(c) Role:** which role does this (not a name)? Who approves the result?
- **(d) Prerequisites:** which tools/programs open, which files/access needed, which inputs present.
- **(e) First Action:** the very first concrete action.

**Phase 2 — Steps (one round per step, aim 4–7).** Per step, four things in one short message:
1. **Signal** — how you know this step is now due (screen state, document, message, time…).
2. **Action** — exactly what you do (which button, field, action).
3. **Confirmation** — how you know the step succeeded.
4. **Tool** — which tool (PIM, Outlook, DeepL, ChatGPT, …).

Handling: all four → write it, ask for the next. One missing → one targeted follow-up. Vague after a
couple of focused follow-ups → write what you have, mark it `[OPEN]`, move on. Several
actions in one → split them.

**Phase 3 — Decisions & Escalation (1 round).**
- **(a)** Where do you choose between paths? Per point: condition, path A, path B.
- **(b)** Where do you turn to your supervisor instead of continuing alone?

**Phase 4 — Definition of Done (1 round).**
- **(a)** Before you say "done", what do you check — which field, status, number, physical confirmation?
- **(b)** Is there a measurable minimum (word count, format, resolution, weight…)?

**Phase 5 — Write the SOP file.** Write `sop-{short-slug}-{YYYY-MM-DD}.md` into the current working
folder, using the full standard in [sop-template.md](reference/sop-template.md). Then a short message:
filename, and a one-line summary (*"{N} Steps, {M} Decisions, {K} Screenshots"*). Then go to Phase 6.

**Phase 6 — Fresh-Eyes Review (the quality pass that replaces self-rating).**
**Delegate the review to the `fresh-eyes-review` agent** — give it the **full path** to the
SOP file you just wrote (include its folder, e.g. `03_Output/…`) and tell it the document type is
**`SOP`** (judge click-level executability). It returns the blocking gaps, ranked. **Integrity guard:** if the agent does
not run or returns nothing usable, do the fresh-eyes read yourself — deliberately discarding everything
the interview told you that is not written in the document — before closing; **never emit the all-clear
without an actual review.** Ask the user **all** the returned gaps at once, **ordered most-blocking
first** — as many or as few as the agent found (sometimes zero; no padding, no stylistic nits); the
person can write **"Pause"** to continue later (house style §7). If nothing blocks, say so plainly. Fold
the answers in, bump the version, mark any remaining minor gaps `[OPEN]`, and update `## Open
Items`. Close:
*"Thank you. Please forward the SOP to your manager for approval — and with *"visualize"* I'll make
you a clean HTML view to review."*

## Special cases

- **Change after Phase 5:** fold in, bump patch version, re-emit.
- **A second task appears:** *"That sounds like a separate task — let's do that separately. Let's first finish {current task} here."*
