# Interrogation Playbook (the filter engine)

The shared interrogation that **every** mode feeds into. The methodology underneath —
ECRS, SIPOC, Theory of Constraints, the Mansar/Reijers redesign heuristics, essential-vs-accidental
complexity — **shapes the questions but is never named to the person.** Every method is a plain
question.

**Output follows the person's language (English by default, per house-style.md §1).** The structural
prose is English; every question and label the person sees follows that same rule.

## The one ordering rule: eliminate before you automate

Walk each step through the gates **in this order** — and never jump ahead to automation before a step
has cleared the elimination gate. (This is ESIA — *Eliminate → Simplify →
Integrate → Automate* — but the person only ever experiences it as the question order.)

1. **Cut?** Could the step disappear entirely without the customer or the result suffering?
2. **Simplify?** If it must stay — can it be made simpler, with fewer inputs or fewer hand-offs?
3. **Merge?** Could it be merged with a neighbouring step, done by one person in one go?
4. **Automate?** *Only now* — and only for steps that survived 1–3 — ask whether a tool or an
   AI agent could take it over. (The 🧠/✨/🤖 tagging in [feasibility-rubric.md](feasibility-rubric.md)
   runs at this gate, never earlier.)

## The eight diagnostic questions

Ask these per step (or per cluster of steps) to drive the gates above. **Never show the method name in
brackets** — it is here only so the engine knows what each question is doing.

1. *"If you joined the team fresh today, with none of the history — which of these steps would you
   never have invented in the first place?"*
   *(Greenfield → reveals historical baggage.)*
2. *"At which single step does work most often pile up, or wait longest for the next one?"*
   *(Bottleneck — the step that sets the pace of the whole process.)*
3. *"Who receives the output of this step — and do they actually need it, or do we only do it because
   we've always done it this way?"*
   *(Customer anchor — every step must have a real recipient.)*
4. *"Does this step only compensate for a weakness somewhere else — a gap in a system, or poor
   upstream work from another team?"*
   *(Essential vs. historical — steps like this disappear once you fix the root cause.)*
5. *"Could two of these steps be done by one person in one pass, if they had the right tool?"*
   *(Merge candidate — hand-offs cost time and create errors.)*
6. *"What would the customer concretely be missing if we dropped this step entirely?"*
   *(Elimination gate — if the honest answer is "nothing," the step is a candidate for cutting.)*
7. *"How often does this step trigger a correction loop or a special case?"*
   *(Quality gate — steps that constantly generate rework are rarely healthy.)*
8. *"Is this process built for 100 units, or for 10,000?"*
   *(Scale stress-test — what runs fine at small volumes breaks at large ones. Especially important
   for catalog/PIM.)*

## Label every step

After the gates, every step that is still part of the redesigned process carries exactly **one** label.
Use these labels verbatim in the working document:

- **stays** — essential, continues unchanged in the target process.
- **cut** — dropped with no replacement (Gate 1/6). Note briefly *why* it's dispensable.
- **merge** — folds into a neighbouring step (Gate 3/5). Note *which one*.
- **automation-candidate** — still necessary, but a tool or an AI could take it over
  (Gate 4). Gets classified further with 🧠/✨/🤖 in the Feasibility phase.

A step that survives every gate and has no automation potential is simply **stays** — that is a valid,
common outcome. Do not force a label just to look productive.

## Notes for running it

- Run the gates **on the redesigned shape, not the as-is list.** In Mode 2 (Greenfield) there may be
  no as-is at all — then the questions test whether each *proposed* step earns its place.
- Surface conflicts, don't resolve them silently. If Gate 6 says "cut" but the person insists the
  step is legally required, that is a real tension — note it and ask, rather than deciding for them.
- Keep the methodology invisible. If the person asks *why* you're asking, answer in plain terms
  ("I want to find out which steps are genuinely necessary and which only exist out of habit") —
  never with a framework name.
