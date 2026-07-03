# Test Scenario — Cowork: Team-AI (End-to-End)

A single, coherent walkthrough that exercises **all six skills** and the full handoff chain in
the order a real Summit Gear employee would hit them. This scenario predates Process Exploration
(a seventh skill) — it intentionally stays to the original six-skill chain; adding a
process-exploration step is out of scope for this test unit.

- **Who runs this:** the plugin maintainer, or anyone QA-ing the plugin before a release.
- **Where it runs:** Claude Cowork (desktop), with this plugin installed.
- **How long:** ~30–45 min for the full chain; each step is independently runnable.
- **What it proves:** every skill triggers on its documented English phrases, writes the right
  file to the right folder, hands off correctly to the next skill, and respects the house-style
  guardrails.

---

## The storyline

**Summit Gear** is an **outdoor-sports e-commerce retailer** — backpacks, tents, sleeping bags,
hiking and trail footwear, outdoor apparel, headlamps, multitools, hydration gear — roughly
15,000 SKUs, shipping internationally. A new supplier price list for the spring range has
arrived. Someone in **Product Data / Merchandising** (role label — never a real name) has to get
the new prices into the shop, write down how it's done so a new colleague could repeat it, and
the team lead wants the whole end-to-end **"Assortment Update"** process mapped. Along the way
the price list turns out to have **data errors**, which the employee can't resolve alone — so
they escalate.

This single thread naturally walks through:

```
1. Sandbox Setup: Team-AI          → set up the safe work area
2. Prompt Improvement: Team-AI     → fix the vague "update the prices in the table" prompt → SOP Starter Pack
3. SOP Creation: Team-AI           → step-by-step SOP for "Update Prices" (uses the Starter Pack)
4. Process Documentation: Team-AI  → the end-to-end "Assortment Update" across roles
5. Visualizer: Team-AI             → HTML view of the SOP and the Process Documentation for the team lead
6. Escalation: Team-AI             → the price list has errors → send to the consultant
```

---

## The test data (in `fixtures/`)

| File | What it is | Used in step |
|---|---|---|
| `supplier-price-list-spring-2026.csv` | New supplier price list, English `,`-CSV. **Contains deliberate flaws** (see below). | 3, 6 |
| `current-shop-export.csv` | Current shop product export (English headers, `,`-CSV) to update against. | 3 |
| `weak-prompt-chat-example.md` | A transcript of a weak prompt + disappointing reply. | 2 |

**The deliberate flaws in the price list** (these drive the SOP's decision points and the escalation):
- `SG-2004` (TrailForge Aircore Carbon Trekking Poles) and `SG-2009` (Cascadia Alpha Insulated
  Trail Jacket) — **missing EAN**.
- `SG-2012` (Beacon Peak Nova 400 Rechargeable Headlamp) — **MSRP ($39.90) is below the wholesale
  price ($44.00)** → negative margin, clearly a data error.
- `SG-2013` (Ironclad Trailmaster 16-Function Multitool) — **duplicate row** (same SKU twice).

> A tester should *not* be told about these up front when role-playing — discovering them is the
> point.

### Where to get more / different test data

Synthetic is preferable for tests (no licensing, no real PII). Good sources:
- **Mockaroo** (`mockaroo.com`) — generate custom CSVs (SKU, EAN, price…) with realistic types;
  free tier covers this.
- **Faker** (Python/JS library) — programmatic synthetic catalogs if you want to regenerate at
  scale.
- Real-ish samples (for shape/realism reference): [Bright Data e-commerce dataset samples (GitHub)](https://github.com/luminati-io/eCommerce-dataset-samples), [Kaggle "eCommerce Products"](https://www.kaggle.com/datasets/mewbius/ecommerce-products), [Open Data Bay product catalogue CSV](https://www.opendatabay.com/data/consumer/6fe4ad9f-670f-4d58-99a8-43dcae8d2926).
- For realism, keep US/English conventions: comma separator, decimal points, columns like
  `Wholesale_USD`/`MSRP_USD`/`EAN`, realistic 13-digit EANs.

---

## Step 0 — Setup

1. Create a **new, empty** folder named `AI_SANDBOX`, **outside any cloud-sync folder** (e.g.
   OneDrive, Dropbox, Google Drive) — just not a real working folder.
2. Open Cowork → new chat → drag `AI_SANDBOX` in → **"Always allow."**
3. Keep the `fixtures/` files handy to copy in when a step asks for them.

---

## Step 1 — Sandbox Setup: Team-AI

**Type:** `Set up my workspace.`

**Expected:** creates `01_Input/`, `02_Work/`, `03_Output/`, a root `CLAUDE.md`, and
`01_Input/_README.md`.

✅ **Check**
- [ ] The three subfolders + `CLAUDE.md` + `_README.md` exist.
- [ ] `CLAUDE.md` content matches `reference/sandbox-claude-template.md` (safety rules + folder
      routing + Summit Gear orientation).
- [ ] **Idempotency / safety:** run it a second time → it must **ask before overwriting** the
      existing `CLAUDE.md`, not silently clobber it.
- [ ] Reply is in the person's language (English default), friendly, no instruction text leaked.

---

## Step 2 — Prompt Improvement: Team-AI

Copy `fixtures/weak-prompt-chat-example.md` into a **new chat**, then **type:**
`The answer doesn't help me — can you improve my prompt?`

**Expected:** writes `prompt-improvement-update-prices-<date>.md` into `02_Work/` (diagnosis +
10-point framework with confidence labels + an XML-tagged improved prompt).

✅ **Check**
- [ ] It **builds the improved prompt immediately** — it does **not** ask "what didn't you like?"
      first.
- [ ] Optional framework points it can't fill are marked **"not relevant"** (✅), not ❌.
- [ ] It does **not** ask the SOP/escalation gate questions yet.
- [ ] Now role-play coming back: **type** `Yes, that worked — and yes, I do this often.`
      → it should now offer the SOP path and write `sop-starter-update-prices-<date>.md` to
      `02_Work/`, with unknown fields marked open (nothing invented).

---

## Step 3 — SOP Creation: Team-AI

Copy `fixtures/supplier-price-list-spring-2026.csv` and `current-shop-export.csv` into
`01_Input/`. Open a **new chat in the same folder** and **type:** `Create an SOP`

**Expected:** it **auto-finds** the `sop-starter-*.md` from Step 2, opens *with* it (no generic
greeting), asks only for the gaps, then writes `sop-update-prices-<date>.md` to `03_Output/`.

✅ **Check**
- [ ] Opens by referencing the found Starter Pack by name. *(Handoff works.)*
- [ ] Interview captures Signal/Action/Confirmation/Tool per step; one task only.
- [ ] **Phase 6 gap check** delegates to the `fresh-eyes-review` agent, passing the full
      `03_Output/…` path + type `SOP`; the agent reads **only** that draft (not the interview) and
      returns ranked blocking gaps — e.g. "what do you do with rows that have no EAN?" — **no
      fixed number, no style nits**. If delegation doesn't fire, the integrity guard runs the
      fresh-eyes read inline rather than emitting a false all-clear.
- [ ] The document is called an "SOP", never a "Process Documentation".
- [ ] **Pause test:** mid-interview, **type** `Pause` → it writes a `-wip` file with `[OPEN]`
      markers and an `## Open` block, and tells you how to resume.

---

## Step 4 — Process Documentation: Team-AI

Open a **new chat in the same folder** and **type:**
`I'd like to document our Assortment Update process.`

Role-play a multi-role flow when interviewed, e.g.: *Purchasing gets the supplier list →
Product Data enters prices & EANs → the Photo team adds missing product images → the team lead
approves → it goes live.* Mention at least one exception (*"if the EAN is missing, it goes back
to Purchasing"*) and use some in-house jargon — e.g. the **PIM** (product information management
system) and an internal shorthand like the **"hot list"** for urgent SKUs — to test the Glossary.

**Expected:** writes `process-doc-assortment-update-<date>.md` to `03_Output/` (bird's-eye step
table, bottleneck/value reflection, KPIs, Glossary, **SOP Candidates** list).

✅ **Check**
- [ ] Method names never leak — you should **never** see "SIPOC/DMAIC/VSM" in the conversation.
- [ ] Step table is **one row per handover, not per click** (bird's-eye, not a worker checklist).
- [ ] "Update Prices" appears in the **SOP Candidates** list (plain bullets, no ranking/table).
- [ ] In-house terms you used (e.g. "PIM", "hot list") are captured in the Glossary.
- [ ] **Phase 7 gap check** delegates to the `fresh-eyes-review` agent with the full `03_Output/…`
      path + type `Process Documentation`; the review is **bird's-eye** (structural breaks only —
      undefined trigger, handover with no recipient, role from nowhere), **lighter** than the SOP
      review, no fixed number. Integrity guard runs the inline read if delegation doesn't fire.

---

## Step 5 — Visualizer: Team-AI

Open a **new chat in the same folder** and **type:** `Visualize this.`

Because there are now **two** candidates (the SOP and the Process Documentation in
`03_Output/`), it should ask which. Run it **twice** — once per file.

**Expected:** writes `sop-update-prices-<date>-visualization.html` and
`process-doc-assortment-update-<date>-visualization.html` next to their sources.

✅ **Check**
- [ ] It **asks which file** when multiple candidates exist. *(Disambiguation.)*
- [ ] The HTML **opens offline** by double-click — **no CDN, no Mermaid, no framework JS, no
      network fonts/images**.
- [ ] Correct badge: "SOP" vs "Process Documentation".
- [ ] Any `[OPEN]` markers render as visible amber tags; nothing is hidden or invented.
- [ ] **Annotations loop:** add an `## Annotations` section to the source `.md`, re-run → it
      renders as a card.

---

## Step 6 — Escalation: Team-AI

The price list errors (missing EANs, the `SG-2012` negative margin, the `SG-2013` duplicate) are
a real blocker the employee can't decide alone. Open a **new chat in the same folder** and
**type:** `I'm stuck here, I need to escalate this to my consultant.`

**Expected:** guides you to run Cowork's `/export`, then produces a clickable `mailto:` link to
the configured escalation address (`escalation_email`, `house-style.md` §0) with subject
`[Escalation: Team-AI] …` and a pre-filled body; reminds you to drag both the `/export` and your
working file into the email.

✅ **Check**
- [ ] Email address is **exactly** the configured `escalation_email` — even if you try to give
      another, it refuses.
- [ ] It does **not** reconstruct or re-type the chat — it relies on `/export`.
- [ ] Subject line ≤ ~60 chars, body in the person's language (English default).
- [ ] It did **not** escalate on its own earlier — only when you asked.

---

## Full handoff chain (what should end up where)

```
01_Input/   supplier-price-list-spring-2026.csv, current-shop-export.csv          (read-only)
02_Work/    prompt-improvement-*.md, sop-starter-*.md                            (drafts/handoffs)
03_Output/  sop-update-prices-*.md, process-doc-assortment-update-*.md,
            *-visualization.html                                                 (finished)
CLAUDE.md   (routes the above; from Step 1)
```

Handoffs: Step 2 → `sop-starter-*.md` → Step 3. Step 4 → SOP Candidates → (future Step 3 runs).
Steps 3 & 4 → Step 5 (visualize). Steps 2/3 → Step 6 (drag-attach to email).

---

## Cross-cutting house-style checks (any step)

- [ ] **No colleague names** ever appear — only role labels.
- [ ] **No language mixing** in a single reply — everything user-facing follows the person's
      language (English default).
- [ ] Every result is a **file** written to the folder — never "here's the text, copy it from
      chat".
- [ ] `01_Input/` files are **never modified** — Claude works on copies in `02_Work/`.

---

## Reset between runs

Delete the `02_Work/` and `03_Output/` contents and any generated `.html`; keep `01_Input/`
fixtures and `CLAUDE.md`. Or just delete the whole `AI_SANDBOX` and start from Step 0 to also
re-test setup.
