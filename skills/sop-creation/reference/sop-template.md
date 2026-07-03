# SOP Standard Template

The professional SOP standard for Team-AI, aligned with mainstream SOP / ISO 9001
documented-procedure guidance (Purpose, Scope, Roles, Trigger, Prerequisites, Steps with decision
points, Definition of Done, Exceptions, References, Revision history). Every section is filled, or
marked `[OPEN]` if genuinely not applicable. **All headings and content are in the person's
language** (`client_language` by default — see `house-style.md` §1). Write it exactly in this shape.

````markdown
---
sop_id: {short-slug}
title: {task name in the person's words}
version: 1.0.0
created: {YYYY-MM-DD}
owner_role: {role, not a person's name}
language: {en | de}
source: {new | from_existing | from_process_doc | from_sop_starter}
status: draft
tools:
  - {Tool 1}
  - {Tool 2}
---

# {Title}

## Purpose
{One to two sentences: why this task exists and what it achieves.}

## Scope
- **Applies to:** {which cases / situations}
- **Does not apply to:** {explicit boundary}

## Roles & Responsibilities
- **Executing role:** {role}
- **Approval / Review:** {role}
- **Point of contact:** {role}

## Trigger
{The concrete event that starts this task — an incoming order, appointment, request, or system status.}

## Prerequisites
- {Programs that must be open}
- {Files / access / permissions}
- {Inputs that must be present}

## Steps

### Step 1 — {short imperative title}
- **Signal:** {how you know this step is now due}
- **Action:** {exactly what you do — button, field, action}
- **Confirmation:** {how you know the step succeeded}
- **Tool:** {…}
{If there's a screenshot: `![Screenshot Step 1]({filename})`}

### Step 2 — …

## Decisions & Branches
- **At Step N:** if {condition} → {path A}; otherwise → {path B}.

## Definition of Done
- {Check 1 — concrete field / status / number}
- {Check 2}
- {Measurable minimum, if any}

## Exceptions & Escalation
- **Exception:** if {special case} → {procedure}.
- **Escalation:** stop and ask {role} if {trigger}.

## References & Links
- {Linked SOPs, wiki pages, templates, Process Documentation — or [OPEN]}

## Open Items
- [ ] Open points marked `[OPEN]`: {list, or "none"}

## Revision History
- 1.0.0 ({YYYY-MM-DD}) — Initial capture.
````

## Notes for writing

- Keep steps **concise and imperative**. One action per step; split compound steps.
- The two fields that make an office SOP actually executable are **Definition of Done** and the
  **decision points** — never leave them thin.
- On **Pause**: set `version: 1.0.0-wip`, status `draft`, list missing phases under
  `## Open Items`, write as `sop-{slug}-{date}-wip.md` (see house style §7).
- After the Phase-6 gap check incorporates answers, bump to `1.1.0` (substantive) or `1.0.1` (minor)
  and add a changelog line.
