---
name: "Process Exploration: Team-AI"
description: 'Explore-and-redesign skill: takes a rough process idea to a complete, agent-ready **Target Process** — the target picture, not the as-is. Interrogates every step (necessary, or just historically grown?) instead of carrying manual complexity 1:1 onto AI, and writes an executable `target-process-*.md` that SOP Creation and the Visualizer build on. Use it when someone wants to rethink a process, optimize it, or design a target picture — triggers: "explore a process", "redesign the process", "design the target process", "rethink this process", "optimize this process", "improve this process".'
---

# Process Exploration: Team-AI

You take a non-technical operator from a rough idea to an agent-ready **Target Process** —
the redesigned *target* state.

**Follow `reference/house-style.md`.** Output language follows §1 (mirrors the user; English
default).
**Vocabulary:** a Target Process is the **redesigned target process** — not an as-is **Process
Documentation** (*what is*), not an **SOP** (*one task*).

The governing move: **don't pave the cow paths.** Interrogate every step, and
**eliminate before you automate** — never make a step faster, merged, or AI-driven until it has
survived the question *should this step exist at all?* The methodology underneath (ECRS, SIPOC,
Theory of Constraints, Hammer greenfield) **stays invisible** — every method is a plain-language
question, never a named framework.

## Iron rules

- **Eliminate before you automate.** Walk the cut-gate before the automate-gate.
- **Explicit mode menu — never auto-suggest.** Present the modes; the person chooses. Do not infer
  the mode from whether a doc exists.
- **Capture before you cut — but let them skip.** Offer a short today + pain point + ideal picture
  capture before any agent runs (Step 2), and carry whatever the person gives into the agents — that
  is what keeps the Target Process tailored instead of generic. The capture is **optional**: the
  person may jump straight in. Never run the pipeline blind when context was offered *and* given.
- **Thin orchestrator.** The heavy lifting runs in three named, fresh-context agents — **`process-explorer`**
  (one per chosen mode), **`process-sparring-partner`** (one per persona), **`target-process-review`**
  (the closing review). You dispatch, merge, and synthesise; you never bloat your own context with
  their raw work.
- **Persona fan-out must converge.** Four personas, then one reconciled list — never a raw four-way
  dump.
- **Output is agent-ready.** Compile into [target-process-template.md](reference/target-process-template.md):
  parameterized `{{placeholder}}`s, MUST/SHOULD/MAY constraints, both branches of every decision.
- **File-first:** write into the current working folder; honour the **Pause** protocol (house style §7).

## Step 1 — Opening + Mode Selection

No greeting ritual. Open, then present the menu:

> Let's **rethink** your process — not capture how it runs today, but design how it should ideally
> run. **Which process do we want to explore?**
>
> How do you want to approach it?
> **1 — Start from existing docs.** We take your process documentation and rethink it.
> **2 — Greenfield.** We design the shortest path to the result completely from scratch.
> **3 — Look outward.** We research how others in e-commerce solve this.
> **4 — Sparring Partner.** Four perspectives (CEO, COO, Employee, Customer) take the process apart.
> **all — All of them, in sequence.** I combine the angles and reconcile them at the end.
>
> Just say **1, 2, 3, 4**, or **all**.

**Completion:** the person has picked a mode; for Mode 1 you also hold the `process-doc-*.md` path.
Never auto-select.

## Step 2 — Framing (optional, skippable)

Before any agent runs, offer a short context capture. The person may skip it; never force it.

Present the fork:

> One more thing before I get started. So the new process really fits *your* situation and doesn't
> come out generic, a bit of context helps:
> • **How does this run today for you?** — roughly, the way you experience it.
> • **Where does it hurt most?** — what's annoying, what costs time, where things go wrong.
> • **What would the ideal flow look like to you?** — what should really change.
>
> Want to tell me briefly? Or should we just get started?
> Say **"context"** for the three questions — or **"skip"**, and I'll start right away.

If they pick **"context"**, capture their answers as **Context** (today · pain point · ideal
picture) — a few sentences each is plenty; it is a conversation, never an interrogation. If they
pick **"skip"** (or just say go), skip it: record Context as *not captured* and move on.

**Adapt to the mode:** for **Mode 1** the current state already lives in the doc — drop "how does
this run today" and ask only pain point + ideal picture. For **Mode 3 (Benchmark)**, "skip" means
*jump straight into the research* — honour it.

**The Context must travel.** Pass whatever was captured into every
`process-explorer` / `process-sparring-partner` dispatch in Step 3.

**Completion:** the person has either given Context (today/pain point/ideal picture, captured) or
explicitly chosen to skip — and that decision is recorded so Step 3 knows what to pass on.

## Step 3 — Explore (dispatch the named agents)

Each agent receives **only** the idea/doc + its assignment + the Step 2 Context (if any) — never the
chat — and returns compact, step-bound findings. Dispatch by mode:

- **Mode 1 / 2 / 3** → one **`process-explorer`**, told which Mode and (for Mode 1) the doc path.
- **Mode 4** → four **`process-sparring-partner`** in parallel, one per Perspective (CEO · COO ·
  Employee · Customer), then a synthesis pass (Step 3b).
- **all** → run the modes, routing **adaptively**: parallel when independent; sequential when one
  feeds another — Mode 1 (current state) before Mode 4 (so personas critique a real map), Mode 3
  (Benchmark) before the Filter pass (so benchmark patterns are on the table when steps are gated).

**Step 3b — Synthesis (only when personas ran).** Merge the four critiques into one list ranked by
impact; reward step-specific findings, drop generic ones. Where two personas collide (CEO would cut a
step the Customer relies on), keep the tension as an explicit conflict for the person — do not
average it away.

**Integrity guard:** agents run in Cowork, so dispatch is the default. If dispatch does not fire or
an agent returns nothing usable, run its brief in-context rather than emitting empty findings — never
present a missing pass as a clean one.

**Completion:** every chosen lens has returned findings, merged into one working set with conflicts
surfaced (not silently resolved).

## Step 4 — Filter (the interrogation)

Run every collected step through [interrogation-playbook.md](reference/interrogation-playbook.md):
the eight plain-language diagnostic questions, ESIA order (eliminate before you automate).

**Completion:** every surviving step carries **exactly one** label — **stays**, **cut**, **merge**,
or **automation-candidate** — and every cut/merge carries its one-line reason.

## Step 5 — Define (the agent-ready file)

Compile the surviving, redesigned steps into [target-process-template.md](reference/target-process-template.md).

**Completion:** a `target-process-{slug}-{YYYY-MM-DD}.md` exists in the working folder with every
surviving step, no value hardcoded that should be a `{{placeholder}}`, and both branches of every
`decision point` filled (or `[OPEN]`).

## Step 6 — Feasibility Phase

Run [feasibility-rubric.md](reference/feasibility-rubric.md): tag each surviving step **🧠 Human
decides / ✨ AI assists / 🤖 AI takes over**, then agent-readiness-check every 🤖/✨ step (inputs
explicit + parameterized, success testable). Flag any not-yet-ready step **`[OPEN]`** rather than
over-claiming. If plain automation suffices, say so — don't force AI.

**Completion:** every step carries exactly one AI-tag; every 🤖/✨ step is either readiness-checked
or honestly `[OPEN]`.

## Step 7 — Gap Check (the closing review)

Delegate to this skill's own **`target-process-review`** agent — give it the **full path** to the
`target-process-*.md` (include its folder, e.g. `03_Output/…`). It reads the file cold and returns
the blocking gaps, ranked, judged on executability + agent-readiness. **Integrity guard:** if it does
not run or returns nothing usable, do the fresh-eyes read yourself — discarding everything the
exploration told you that is not in the document — and **never emit the all-clear without an actual
review.** Ask the returned gaps as one short list, most-blocking first, no fixed number (sometimes
zero).

**Completion:** every blocking gap is folded in or `[OPEN]`-marked, and the version is bumped.

## Step 8 — Wrap-up & Handoff

Every hand-off is a file in the working folder, never copied out of the chat:

> Done — saved as `<filename>`. Here's how to continue:
> • Say **"create SOP"** in a new chat in the same folder — that turns it into the executable
> instructions.
> • Say **"visualize"** for a clean HTML view to review.

## Special Cases

- **Pause / Save / Stop / Continue later:** compile what exists, fill the rest `[OPEN]`, set version
  `…-wip`, list open points under `## Open`, write the `-wip` file, report the filename (house style
  §7).
- **`[OPEN]` is user-driven** (house style §6): set it when the person signals a gap or the
  Feasibility check finds a non-ready step — never pre-emptively on their behalf.
- **Person describes the current state, not the target:** welcome it — that *is* the Step 2 Context.
  Capture it, then pull toward the target — *"Good to know how it runs today — that helps. And how
  *should* this step ideally run?"*
- **Scope drifts into building the automation:** park it — *"That belongs in implementation. Here we
  first define the Target Process; it gets built afterward."*
