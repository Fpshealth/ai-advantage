# Process Documentation Standard (Template)

The professional bird's-eye standard for a **Process Documentation**. Every section is filled, or
marked `[OPEN]` if genuinely unknown. Write it exactly in this shape.

````markdown
---
process_id: {short-slug}
title: {Process name in the person's own words}
version: 1.0.0
created: {YYYY-MM-DD}
created_by: {Name, if given — else [OPEN]}
process_owner: {Role, not a person's name}
review_cycle: {e.g. annually | on change | [OPEN]}
language: {en | de}
status: draft
---

# Process Documentation: {Title}

## Purpose
{Two to four sentences, enough to fully understand the process's overarching purpose: what result
it delivers, who it's handed to, what business purpose it serves for the team, and what would be
missing if it stopped existing tomorrow. Clear and free of jargon.}

## Scope
- **Applies to:** {which cases / which part of the process}
- **Does not apply to:** {explicit boundary — what is deliberately out of scope, or [OPEN]}

## Trigger
{The concrete event that starts the process — an incoming order, an appointment, a request, a
status in a system.}

## Inputs & Prerequisites
- **Information / approvals / materials needed:** {…}
- **Sources / who or which system supplies them:** {…}
- **Security or compliance rules:** {e.g. data protection — or [OPEN]}

## Process Flow
| Step | What happens | Who (role) | Tool / System | Handoff to |
|---|---|---|---|---|
| 1 | … | … | … | … |
| 2 | … | … | … | … |

## Decisions & Branches
- **At step N:** if {condition} → {path A}; else → {path B}.

## Definition of Done
- {How it's confirmed the result is correct before handing it off.}
- {Measurable minimum, if any.}

## Exceptions & Escalation
- **Last concrete incident:** {from the case described}
- **Typical resolution:** {…}
- **Occurrence frequency (rough estimate):** {e.g. "about 5 out of 100 runs"}
- **Escalation:** stop and ask {role} if {trigger}.

## Bottleneck & Lean Reflection (brief)
- **Where waiting or backlog regularly builds up:** {from the bottleneck question}
- **Steps with no real customer value / duplicated / unnecessarily manual work:** {…}
- **Employee's improvement idea:** {concrete idea, if given}

## Metrics (KPIs)
- **Current measurement / reports:** {from the KPI question}
- **If not known — contact person:** {role who can answer}
- **Active processing time per run / total lead time / mode:** {individual or batch, with size}

## SOP Candidates
<!-- Tasks within this process that would be worth their own SOP. Just a short list of task names
— no prioritization. Prioritization is a separate, later step. -->
- {Task 1}
- {Task 2}

## Glossary
- **{Term / abbreviation}:** {Explanation — captured automatically from the conversation}

## Revision History
- 1.0.0 ({YYYY-MM-DD}) — Initial capture.
````

## Notes for writing

- Keep the step rows bird's-eye: one row per meaningful handover, not per click. For click-level
  detail, that task belongs in the **SOP Candidates** list and is documented later with
  `SOP Creation: Team-AI`.
- **Anchor everything to a step.** Tools, handovers, systems and compliance rules live *in the
  relevant row* of the Process Flow table — never as a detached list.
- The two fields that make this doc useful for later optimization are **Definition of Done** and
  the short **Bottleneck & Lean Reflection** — never leave them thin.
- On **Pause**: set `version: 1.0.0-wip`, status `draft`, list missing phases under an `## Open`
  block, write as `process-doc-{slug}-{date}-wip.md` (house style §7).
- After the gap check folds in answers, bump to `1.1.0` (substantive) or `1.0.1` (minor) and add a
  changelog line.
