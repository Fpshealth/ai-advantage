# Target Process Standard (Template)

Write the output exactly in this shape. **Use no framework vocabulary in it.** Fill every section, or
mark it `[OPEN]` if genuinely unknown. **Write all headings and content in the person's language**
(`client_language` by default — see `house-style.md` §1).

Two rules make this template agent-ready rather than prose:
- **No hardcoded values — parameterize.** Write `{{item_number}}`, `{{brand_name}}`, never a
  concrete SKU or price. The values are supplied at run time; the process is the template.
- **Constraints are MUST / SHOULD / MAY** (the RFC-2119 triple): **MUST** = mandatory; **SHOULD**
  = strong default, deviate only with reason; **MAY** = optional. An agent reads these as hard vs.
  soft rules.

````markdown
---
process_id: target-{short-slug}
title: {Target process name in clear words}
version: 1.0.0
created: {YYYY-MM-DD}
process_owner: {Role, not a person's name}
mode: {from-docs | greenfield | benchmark | sparring-partner | all}
based_on: {Process-Doc filename, if Mode 1 — else [OPEN]}
status: draft
---

# Target Process: {Title}

## Overview
{Two to four sentences: what result the new process delivers, for whom, and how it differs from
today's process — the one sentence that carries the core of the redesign.}

## Actors & Systems
- **Roles:** {which roles are involved — roles only, no names}
- **Systems / Tools:** {PIM, Drive, Adobe Suite, … — anchored per step, here just the overview}

## Inputs (parameterized)
<!-- Placeholders, not fixed values. The executing agent or human fills these in at run time. -->
- `{{input_1}}` — {what it is, where it comes from}
- `{{input_2}}` — {…}

## Steps
<!-- One block per step. Action · System · Constraint (MUST/SHOULD/MAY) · Result Artifact · On Failure. -->

### Step 1 — {short label}
- **Action:** {what is done — one clear action}
- **System:** {tool/system for exactly this step}
- **Constraint:** {MUST/SHOULD/MAY …} — {the rule that applies here}
- **Result Artifact:** {what exists at the end of this step — file, record, status}
- **On Failure:** {what happens if the step fails — fallback or who it goes back to}
- **AI Tag:** {🧠 Human decides | ✨ AI assists | 🤖 AI takes over} {or `[OPEN]` if not yet decided}

### Step 2 — {…}
{same schema}

## Decision Points
<!-- Both branches are mandatory — an agent must know what to do in EVERY case. -->
- **At Step N:** IF {condition} THEN {path A} ELSE {path B}.

## Subprocess Boundaries
{Where this process ends and another begins — clean cuts instead of one mega-process. Which
parts are deliberately handed off, and to which process.}

## Success Criteria (testable)
- [ ] {a checkable, objectively verifiable criterion — not "looks good"}
- [ ] {…}

## Handoffs
- **Inbound:** {what this process expects, from whom/which system}
- **Outbound:** {what it hands off, to whom/which next process}

## Boundaries (always / ask first / never)
- **Always allowed:** {what the executing agent may do without asking}
- **Ask first:** {what needs sign-off from the responsible role}
- **Never:** {what the agent does under no circumstances}

## Example
{One worked-through example run with real values plugged in — shows what the placeholders look
like filled in concretely, without baking them into the process itself.}

## AI Tags (Overview)
| Step | Tag | Agent-ready? |
|---|---|---|
| 1 | {🧠/✨/🤖} | {yes | `[OPEN]`: {what's missing}} |

## Revision History
- 1.0.0 ({YYYY-MM-DD}) — Initial capture from {Mode}.
````

## Notes for writing

- **Parameterize relentlessly.** If you see a concrete value that varies per run, replace it with a
  `{{placeholder}}` and list it under **Inputs**.
- **Both branches, always.** Fill both branches of every **decision point**, or mark the missing one
  `[OPEN]`. A decision point with only the THEN side is not agent-ready: an agent that hits the ELSE
  case stalls.
- **Testable success only.** Push for a checkable criterion. "The spread looks right" is not one an
  agent can check. If none exists yet, mark it `[OPEN]` honestly.
- Carry the **AI Tags** over from [feasibility-rubric.md](feasibility-rubric.md). Don't re-derive
  them here.
- On **Pause**: set `version: 1.0.0-wip`, status `draft`, list open points under an `## Open`
  block, write as `target-process-{slug}-{date}-wip.md` (house style §7).
- File naming: `target-process-{short-slug}-{YYYY-MM-DD}.md`.
