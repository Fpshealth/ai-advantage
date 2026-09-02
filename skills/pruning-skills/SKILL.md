---
name: pruning-skills
description: Prune an existing skill down to the lines that change agent behaviour, and re-fit it to the current model. Use when a skill feels bloated or wordy, or after a model release.
---

Read the whole skill, then name the **target model** — the model running this pass, unless told otherwise. Every judgement below is relative to that model's defaults.

This skill uses the vocabulary of `mattpocock-skills:writing-for-agents` (read it and its `SKILL-MECHANICS.md` first) — _no-op, sediment, duplication, negation, leading word_ — and adds one word: **fluff** is any sentence that does not change what the agent _does_ versus the target's default. Fluff spends context load and buries the lines that matter.

## Pass 1 — form

Apply the four writing-for-agents lenses: every rule states a positive target, every step ends on a checkable completion criterion, each meaning lives in one place, leading words do the anchoring. Done when every rule and step passes all four.

## Pass 2 — the no-op cut

Sentence by sentence, in isolation: does this change what the agent does? If not, delete the whole sentence — never trim words from it. Cut on sight:

- **Sediment** — provenance, dates, war stories: "Source: X (2026-…)", "the first version had to be rebuilt".
- **No-op** — a quote from the source the rule already restates; a dangling reference the agent has no context for ("the IMP-005 lesson").
- **Duplication** — a "why this matters" sentence before the rule that says it; a decorative tail after it; a list re-enumerated from the table above; a referenced doc restated beside its pointer.
- **Negation without provenance** — "don't generate blindly", "never skip X" tied to no named failure. It makes the unwanted behaviour available; rewrite as the positive target.
- **Defense without evidence** — an absolute guarding a failure nobody has seen ("even if asked to use another"). A rule earns its place through a field incident.
- **Raised non-issue** — "anywhere is fine, including OneDrive". Naming a settled question keeps it alive.
- **Description bloat** — procedure in the `description:` field. It loads every session; it carries trigger conditions only.

Where a sentence half-passes, rewrite instead of deleting: two sentences saying one thing become one; a sentence gesturing at an idea becomes its leading word.

Keep, even when short:

- Rules, gates, and completion criteria.
- Tool and command names, path conventions, output formats.
- Context only the author holds — audience, environment, quality bar.
- A leading-word anchor (`Reacting is cheap; specifying is expensive`).
- One example per abstract rule. Not five.

Done when every remaining sentence changes behaviour.

## Pass 3 — model fit

Some lines exist only to correct one model's habit: shouting, forbidding, spelling out steps. Find each one and ask who it was written for. Open the target's "Behavioral shifts" notes (`claude-api` skill, `shared/model-migration.md`) and check:

- The habit is not in the notes → cut the line.
- The habit is in the notes → keep the line and write the reason next to it.
- The notes ask for a line the skill lacks → add it.

Lines that protect a business or legal constraint stay regardless. Re-fitting adds text; a rising word count is a valid result.

Done when every such line has a reason next to it or is gone.

## Verify and report

Grep the wider system for each cut string before deleting it; where a trigger or behaviour eval exists, run it before and after.

Report each cut as _quote → failure-mode name_, each model-fit keep or add with its owner, and word count before → after. List the lines you nearly cut and why you kept them, so the user can push further.
