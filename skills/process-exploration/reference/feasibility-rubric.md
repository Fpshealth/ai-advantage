# Feasibility Rubric (the feasibility / AI-opportunity gate)

The explorer's **final phase**: it takes the redesigned process and asks, per surviving step, *who or
what should do this* and *is it actually ready to be handed to an AI agent?*

**Runs only after the interrogation playbook.** A step that was already labelled **cut** is gone — you
do not tag deleted work. Only **stays**, **merge** and **automation-candidate** steps reach this rubric.
Never discuss automation for a step that has not cleared the elimination gate.

**Output follows the person's language (English by default, per house-style.md §1).** The tag emojis and
their labels are user-facing.

## Step 1 — Tag every surviving step (exactly one tag)

| Tag | Meaning | When |
|---|---|---|
| **🧠 Human decides** | A human owns this — judgment, taste, relationship, accountability. | Judgment, accountability, customer relationship, creative final call. |
| **✨ AI assists** | AI prepares, drafts or suggests; a human reviews and decides. | Draft, suggestion, research-support, first draft. |
| **🤖 AI takes over** | AI does it end-to-end; a human only spot-checks. | Clearly-defined, rule-based step with a testable outcome. |

Every surviving step gets **exactly one** tag — no step left untagged, no step with two.

## Step 2 — Agent-readiness check (for every 🤖 and ✨ step)

A tag of 🤖 or ✨ is a *claim* that an agent could do the work. Test the claim before believing it. A
step is **agent-ready** only when all three are true:

| Criterion | Question | Met when … |
|---|---|---|
| **Inputs explicit** | Is everything the step needs already there — as a nameable file, field or parameter? | no silent "you just know" input, no knowledge that lives only in one person's head. |
| **Parameterized** | Are the inputs described as placeholders, not one hardcoded case? | `{{sku}}` instead of a specific item number baked in. |
| **Success testable** | Can you *objectively* check whether the result is correct? | a checkable criterion ("all required fields filled", "image resolution ≥ X"), not "looks good". |

## Step 3 — Be honest, not optimistic

If a 🤖 or ✨ step fails any of the three criteria, **do not quietly downgrade it and move on, and do not
pretend it is ready.** Mark it **`[OPEN]`** with the one thing missing, e.g.:

> *Step 4 (🤖) — `[OPEN]`: the "matching product photo" input isn't parameterized yet. Needs clarifying
> before automation: how does the agent know which photo belongs to which item?*

## Step 4 — Facilitation note (don't force AI)

If a step is best served by **plain automation** (a rule, a template, a macro) rather than an AI agent,
say so. A good plain-language way to put it to the person:

> *"A simple rule could handle this step too — it doesn't need AI. Is the extra effort really worth it
> here, or should we solve it more simply?"*

## What this phase hands on

The tagged, readiness-checked step list flows straight into the **AI-Tags** section of
[target-process-template.md](target-process-template.md), and any `[OPEN]` step becomes a blocking item
for the Gap Check with fresh context to surface.
