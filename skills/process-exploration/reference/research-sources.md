# External Research — Engine & Source Registry (powers Mode 3)

Mode 3 (Benchmark) is **always external research — never model knowledge and never a static
lookup**. This file is the engine: a tiered, tool-detecting research routine plus a curated
registry of high-impact e-commerce sources.

> **Re-skin seam:** this file is the swappable per-client research-source registry referenced as
> `industry_pack` in `house-style.md` §0. Everything below is the e-commerce example instance —
> replace the source registry (not the tier engine above it) when re-skinning for a different
> industry.

**Output follows the person's language (English by default, per house-style.md §1).** This file is
instructions to the Mode 3 sub-agent; everything it returns to the person follows that rule, with
sources named.

## The tiers (use the richest one available)

The Mode 3 sub-agent **detects which tools are present** and runs on the highest tier it can. On a
bare Cowork run it stays on Tier A **and says so** — never a silent capability gap.

### Tier A — Self-serve (always available, the floor)
Native web search/fetch against the source registry below. This is the floor: every Mode 3 run,
even in a plain Cowork session with no local tools, returns externally-sourced, attributed
patterns. Never fall back below this to model knowledge.

### Tier B — Deep / facilitated (the consultant's research environment)
When the richer tools are detected, enrich Tier A with:
- **`/last30days`** — live social + market pulse (Reddit, X, YouTube, HN, …) for *what is changing
  right now* in a topic.
- **`notebooklm-cli`** — deep multi-source notebook research. **Verify success by source-count
  delta, not by exit code or "Imported N" output** (the [[notebooklm-cli]] skill rule). After a
  multi-query run, `notebooklm source clean -n <id> -y` to collapse duplicates.

These are illustrative examples of what a consultant's research environment might contain, not
hard requirements — the tier is defined by "richer, facilitated tooling beyond plain web search,"
whatever form that takes for a given consultant.

Ingest both as a structured research-input file and fold their findings into the patterns. Tools
like `notebooklm-cli` are local, auth-bound setups that will **not** exist in a typical client's
Cowork session — so Tier B is **facilitated by design** (the consultant runs it), cleanly matching
the "both self-serve + facilitated" split. Whether Tier B auto-runs on detection or only on
explicit request is an open question — default to **explicit** to control cost and latency.

### Tier declaration (mandatory)
Every Mode 3 finding set states the tier it ran on, in plain language, e.g.:
> *"Research at the self-serve level (web sources). Deeper research with live market pulse and
> NotebookLM would need the consultant's environment."*

## Source registry (e-commerce)

High-impact sources and which tool researches each. **This v1 list is a starting point — the
first real Mode-3 job is to research and expand this very registry** (see *Dogfood*, below).

| Source | For | Preferred tier |
|---|---|---|
| **Baymard Institute** | UX, catalog, and checkout research; large usability-study base. | A (Web) |
| **PIM/DAM playbooks** — Akeneo, inriver, Salsify, Pimcore | Product-data workflows, catalog/assortment logic, onboarding. | A (Web) |
| **GS1** | Product-data standards (GTIN, classification) — the data substrate. | A (Web) |
| **Practical Ecommerce / eCommerceFuel** | Operational tactics from real merchants' perspective. | A (Web) |
| **McKinsey / BCG — Retail Operations** | Process and cost benchmarks, industry figures. | A (Web) |
| **Outdoor-gear / apparel retail sources** | Industry-adjacent (seasonal assortment, catalog, gear categories). | A (Web), B for current developments |
| **Live tools** — `/last30days`, `notebooklm-cli` | "What's changing right now?" — fresher than any static source. | B (facilitated) |

## What a good Mode 3 finding looks like

Not "others do it differently," but step-bound and attributed:
> *Pattern: Instead of preparing every item's data manually up front, leading retailers pull
> catalog data directly from the PIM and only then filter down to the selection that's actually
> needed. → Would compress the process's early data-preparation steps down to the items that make
> it through to the final selection.
> Source: Akeneo PIM playbook, catalog publishing.*

Each pattern names: **what others do**, **why it works**, **which of the process's steps it
changes**, **source**. Never present a pattern you cannot attribute.

## Dogfood — build the registry by running it

The **first real job** for Mode 3 is to research and validate/expand this registry using the
consultant's research environment (e.g. `notebooklm-cli` + `/last30days`) — i.e. build the registry
by running the mechanism it documents. Until that pass happens, treat the table above as a
provisional v1, not a closed list, and say so when it is the only basis for a finding.
