# Example: Catalog Spread (Target-Process Exploration, Worked)

The canonical worked example baked into this skill — the ~$75,000-per-year catalog process, run
through the full funnel in **Mode 1 (From Docs)**. It is the highest-ROI Summit Gear case, so a real
Mode-1 run on the As-Is document should land **materially close to this**.

Source As-Is document: `As-Is Process — Catalog Spread` (from a recent operations review). Output is
English.

---

## Starting Point (from the As-Is doc)

The catalog is a printed, single-market product. Per brand and spread, today **three separately
prepared strands** — a spreadsheet, text files, image files — are **fully manually** assembled and sent
to an external layout studio, which produces the finished spread through several correction rounds.
Lever: ~$75,000/year in external layout costs.

As-is steps: **1** Catalog plan · **2** Fill spread table · **3** Write catalog copy · **4** Prepare
image files · **5** Send data package to layout studio · **6** Create layout · **7** Correction rounds ·
**8** Approval & print.

---

## Explore — what the doc reveals

- Three input strands that get reassembled externally (a media break).
- The layout is **already fairly fixed** (a set of standard variants) — it's composed, not designed
  freely. That's a strong signal for automatability.
- The "source of truth" lives in the text files; a lot gets written that never makes it into the
  catalog.

## Filter — the interrogation (ESIA: eliminate before you automate)

| As-is step | Question that applies | Label | Reasoning |
|---|---|---|---|
| 3 Copy for *all* items | Gate 6 + 8: *"What would the customer be missing if…?"* / *"Built for 100 or for 10,000?"* | **merge / streamline** | The catalog team today prepares far more copy than actually gets printed. Only the items that are actually printed need catalog copy — the rest is **historical baggage**, not an essential step. |
| 4 Images against the table | Gate 5: *"Two steps in one pass?"* | **merge** | Image and copy assignment both follow the same table — they can be pulled together from the PIM/table instead of running as two separate strands. |
| 5 Bundle data package externally | Gate 4: *"Does this only compensate for a weakness elsewhere?"* | **cut** | Exists only because the layout happens externally. Falls away once the draft is generated internally and automatically. |
| 6 Create layout (external) | Gate 1: *"Would you invent this from scratch today?"* | **automation-candidate** | Fixed layout + structured inputs = an ideal case for an AI agent with an Adobe connection. |
| 7 Correction rounds | Gate 7: *"How often does a correction loop trigger?"* | **merge / shorten** | Several serial external rounds shrink to one internal draft-optimization pass by the design team. |
| 1 Catalog plan · 2 Table | — | **stays** | Planning and structural decisions stay with a human. |
| 8 Approval & print | — | **stays** | Final approval is a deliberate human decision. |

**Key insight (covers exactly the problem a recent operations review surfaced):** "Preparing all items
upfront when only a fraction make it into the catalog" is **unnecessary, historically grown complexity —
nothing the process actually needs.**

## Define — the Target Process (excerpt, agent-ready)

```markdown
---
process_id: target-catalog-spread
title: Catalog Spread (Target)
version: 1.0.0
mode: from-docs
based_on: process-doc-catalog-spread.md
status: draft
---

## Inputs (parameterized)
- `{{brand_name}}` · `{{spread_count}}`
- `{{catalog_item_selection}}` — only the items that actually get printed (filtered in the PIM)

### Step 1 — Catalog plan & spread table
- Action: Set `{{spread_count}}` per brand, fill the table at the spread level.
- Constraint: MUST — image type (model/product shot) and carryover/new set per position.
- AI Tag: 🧠 Human decides

### Step 2 — Pull catalog data from the PIM (catalog selection only)
- Action: Pull copy + images for `{{catalog_item_selection}}` together from the PIM.
- Constraint: MUST — only printed items; no upfront prep of the full assortment.
- On Failure: missing copy/image → flag the item `[OPEN]`, don't guess.
- AI Tag: ✨ AI assists

### Step 3 — Generate the spread draft automatically
- Action: Agent composes a draft from the table + copy + images following a fixed layout variant
  (Adobe via MCP).
- Constraint: SHOULD — use one of the existing layout variants.
- Success testable: all required positions filled, copy ≤ line limit, image resolution ≥ print minimum.
- AI Tag: 🤖 AI takes over — `[OPEN]`: image-to-item mapping not yet parameterized.

### Step 4 — Design team refines the draft, approval
- Action: Design team polishes the draft instead of laying it out from scratch; leadership approves.
- AI Tag: 🧠 Human decides
```

**Impact:** the external layout strand (steps 5–7 in the as-is) largely disappears — the central lever
behind the ~$75,000/year. The one honest `[OPEN]` (image-to-item mapping) is exactly the question to
clarify in the next automation review session — cleanly flagged instead of glossed over.
