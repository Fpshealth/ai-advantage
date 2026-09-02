---
name: pruning-skills
description: Use when tightening, pruning, condensing, or fluff-cutting an EXISTING skill — stripping it down to purely operational content that changes agent behaviour. Invoke whenever a skill feels bloated, wordy, verbose, or "full of fluff"; when asked to make a skill leaner, tighter, or more concise; to strip provenance, war-stories, restatements, or dead references; to audit a skill (new or old) for redundancy against skill-writing doctrine; or to re-fit a skill to a new model after a release. Runs as the concision and model-fit pass after writing-for-agents. Not for authoring a skill from scratch — that's skill-creator.
---

# Pruning skills — cut a skill down to what changes behaviour

A skill's only job is to make the agent take the same operating steps every run. Every sentence that doesn't change what the agent *does* is **fluff**: it spends context load and buries the lines that matter. This skill strips an existing skill to operational bone.

**REQUIRED BACKGROUND: writing-for-agents** (the mattpocock-skills plugin skill; successor of writing-great-skills). It defines the terms used below — *no-op, sediment, sprawl, duplication, negation, leading word*. That skill says what good looks like; this one assumes the skill is already carrying fluff and goes hunting. Don't restate its doctrine here.

## The pass

1. **Read the whole skill first, and name the target model** (default: the model running this pass). You can't spot a duplication, a dangling reference, or a re-enumerated list from a fragment.
2. **Phase 1 — doctrine check.** Run the writing-for-agents lenses: is each rule a positive target (not a negation)? Does every step end on a checkable completion criterion? Is each meaning in one place? Are leading words doing the anchoring? Fix form problems here.
3. **Phase 2 — the no-op cut.** Go sentence by sentence with the test below. This is the aggressive pass a plain doctrine review skips.
4. **Phase 3 — model fit.** Read every "Behavioral shifts (prompt-tunable)" section for the target in the `claude-api` skill's `shared/model-migration.md`. For each surviving emphasis marker, prohibition, or step script: which failure, on which model, did it prevent, and do the target's sections still list it? Unowned → cut. Still listed → keep, with the reason beside it. Listed as newly needed for the target → add.
5. **Verify.** Grep the wider system for each cut string before deleting it; where a trigger or behaviour eval exists, run it before and after.
6. **Report** each cut by its failure-mode name, with a word-count delta.

**The no-op test (per sentence, in isolation):** does this change what the agent *does* versus its default behaviour? "Default" means the target model's default. If no → **delete the whole sentence**, don't trim words from it. Be aggressive; most prose that fails should go, not be reworded.

## Cut on sight

| Smell | Why it's fluff | Name |
|---|---|---|
| Provenance & dates — "Source: X (2026-…)", "added 2026-07-05" | History, not instruction | sediment |
| War stories — "the first version had to be rebuilt", "proven when…" | Narrates the past; changes no behaviour | sediment |
| Appeal-to-source quotes — "the article says '…'" | The rule beside it already states the behaviour | no-op |
| Dangling references — "the IMP-005 lesson", "the color-grading case" | The agent has no context for it; it cues nothing | no-op |
| Motivating restatements — a "why this matters" sentence before the rule that already says it | Same meaning twice | duplication |
| Decorative tails — "— it's how surprises become known knowns" | Ornaments a purpose already stated | duplication |
| Re-enumeration of a list or table printed just above | Same content, second copy | duplication |
| Prohibitions with no provenance — "don't generate blindly", "never skip X" tied to no named failure | Names the unwanted behaviour and makes it available | negation |
| Defensive absolutes for unobserved failures — "even if asked to use another", "nothing invented" | Guards an imagined scenario; a rule earns its place through a field incident | defense-without-evidence |
| Naming a non-issue — "anywhere is fine, including OneDrive" | Keeps a settled question alive as a topic; unmentioned = no issue | raised-non-issue |
| Procedure detail in the `description:` field | Descriptions load into every session and carry triggering conditions only; procedure lives in the body | description-bloat |
| Restating a referenced doc beside its pointer — "follow X — especially §1: …" | The pointer suffices; the content's home is the referenced doc | duplication |

## Keep — over-pruning is the opposite failure

- **Rules, gates, and completion criteria** — the checkable done-conditions.
- **Tool and command names, file-path conventions, concrete output formats** — the operational specifics.
- **Context only the author holds** — audience, environment facts, the quality bar.
- **Prohibitions with provenance** — a business or compliance constraint, or a failure the target model's notes still list — paired with their positive target and reason.
- **Lines the target's notes ask for.** Re-fitting to a new model adds text too; a word count that rises is a valid result.
- **Leading-word anchors even when short.** A six-word line that ties a pattern back to the model's priors (`Reacting is cheap; specifying is expensive`) earns its tokens — that's signal, not fluff.
- **One example** where it makes an abstract rule concrete. Not five.

## Rewrite, don't only delete

- Negation → the positive target ("don't generate blindly" → "first teach the quality dimensions, then let him direct").
- Two sentences saying one thing → one.
- A sentence gesturing at an idea → its leading word.

## Report

List each cut: the trimmed quote → its failure-mode label. List each model-fit keep or add with the failure it owns. Close with **word count before → after (% change)**. Surface the lines you nearly cut but kept, with why — so the user can decide whether to push further.
