---
name: "Visualizer: Team-AI"
description: 'Turns a finished SOP or Process Documentation into a clean, branded, single self-contained HTML page a non-technical person can visually check — and correct directly in the page ("yes, this is how I picture my work"). Use this skill when someone says "visualize this", "HTML view", "show me that nicely", "make an overview", "as a webpage", "make this clear" — or names/attaches a file. Works for SOPs AND Process Documentations.'
---

# Visualizer: Team-AI

You turn a finished SOP or Process Documentation Markdown file into a clean, branded, **single
self-contained HTML file** so a non-technical employee can visually verify *"yes, this is how I
picture my work."* The page is **lightly interactive**: the employee can mark each step *correct /
unclear / incorrect*, drag-reorder steps, and fix step text in place. Every change is emitted as
**paste-ready Markdown for the source `.md`** — the page never writes files itself and never saves
silently. The source Markdown stays the single source of truth (see Annotation).

**Follow `reference/house-style.md`.** Output language follows §1 (mirrors the user; English
default). **Vocabulary:** detect whether the source is an **SOP** or a **Process Documentation**
and label it correctly — never swap the words (house style §5).

## Iron rules

- **HTML-first, no Mermaid.** No diagram libraries, no CDN, no external dependencies. One file, inline CSS.
  Steps are rendered as a simple vertical numbered flow using plain HTML/CSS (boxes + CSS arrows).
- **Contained JS only (no framework, no network).** The page carries exactly **one inline `<script>`**: vanilla
  DOM, no CDN, no framework, no fonts/images fetched remotely, **no `fetch`/XHR**. Its only job is the verify /
  reorder / edit affordances and assembling paste-ready Markdown. Hard limits: the page must open offline by
  double-click, must **degrade gracefully** (with JavaScript disabled it is a clean read-only render with **no
  dangling controls**), and must **print cleanly**. All interactive chrome is *injected by the script on load*, so
  JS-off never leaves dead buttons behind.
- **The page never mutates the source.** Interactive edits accumulate **client-side only** and are emitted as
  (a) a regenerated `## Steps` body and/or (b) an appended `## Annotations` block for the employee to paste over
  / under the source. No hidden parallel state; the `.md` stays the single truth.
- **File-first (house style §3):** write the HTML into the **current working folder**. Never paste the page into chat.
- **Render what the source says.** You do **not** invent or "improve" content when building the page. (Re-ordering
  and editing happen *in the browser, by the employee* — never by you at render time.) If a section is missing,
  render its placeholder ("— still open —"); do not fabricate.
- **Never name colleagues** — the source already uses role labels; preserve them as-is.
- Use the canonical skeleton in [html-template.md](reference/html-template.md). Fill every `{{placeholder}}`.

## Choosing the source file

The person says **"visualize"**, optionally naming or attaching a file.

1. **File named or attached** → use it.
2. **No file named** → look in the current working folder for the most recent `sop-*.md` or `process-doc-*.md`.
   - **Exactly one obvious candidate** → confirm in one line: *"I'll visualize `<filename>` — does that work?"*
   - **Several candidates** → list them briefly and ask which one.
   - **None found** → say so plainly: *"I don't see an SOP or Process Documentation here to visualize.
     Name the file or attach it."*

## Detecting the document type

Read the source frontmatter and headings:

- **SOP** — frontmatter has `sop_id:` / `owner_role:`, headings like `## Steps`, `## Definition of Done`,
  `## Decisions & Branches`. Set the header badge to **SOP**.
- **Process Documentation** — describes an end-to-end flow across multiple roles (bird's-eye / manager's map),
  typically `process-doc-*.md`. Set the header badge to **Process Documentation**.
- **Unclear** → ask one short question rather than guessing.

## Building the HTML

1. Parse the source frontmatter (`title`/`version`/`owner_role`/`created` or the Process-Doc equivalents
   `title`/`version`/`process_owner`/`created`) and the Markdown sections.
2. Open [html-template.md](reference/html-template.md) and fill the placeholders:
   - `{{TITLE}}`, `{{TYPE_BADGE}}` (`SOP` or `Process Documentation`), `{{VERSION}}`, `{{ROLE}}`, `{{DATE}}`.
   - `{{DOCTYPE}}` — the machine value `sop` or `process-doc` on `<body data-doctype>`. **Required:** the script
     reads it to choose reorder semantics and the writeback shape (Process Documentation adds a `- **Role:**` bullet).
   - `{{PURPOSE}}`, `{{SCOPE}}`, `{{PREREQUISITES}}`, `{{DECISIONS}}`, `{{DOD}}`,
     `{{EXCEPTIONS}}`, `{{REFERENCES}}` — each rendered as a card; missing → "— still open —".
   - `{{STEPS}}` — render `## Steps` as the vertical numbered flow (one `<div class="step" data-step>` per
     step, with **Signal / Action / Confirmation / Tool** as labelled `.field` rows). **Put `data-field="Signal"`
     etc. on every value span** — the script reads these to regenerate Markdown. CSS arrow between boxes, never after
     the last.
   - **Optional `Why` row:** if a step supplies a `Why:` value, add one
     `.field.why` row. Omit it entirely when absent — never an empty box. (This is the TWI "Key Point + Reason"
     line; it surfaces logic errors during verification.)
   - **Optional screenshot slot:** if a step supplies an image value that is an inline base64 data-URI, render
     `<img class="step-shot" src="…">`. **Inline data-URIs only** — never an `http(s)://` URL or a file path
     (would break the offline single-file rule). Absent / not-a-data-URI → render no `<img>`.
   - For a **Process Documentation**, render the process stages/roles into the same flow structure (one box per
     stage, role shown as a `<span class="role-tag">` *and* mirrored on `data-role="…"` so it survives export), and
     hide SOP-only cards that don't apply.
   - Escape any `<`, `>`, `&` from the source so the page renders literally.
   - The "Does this look right?", "Read Aloud & Confirm", and apply-panel UI strings are already in the template
     — leave them intact, only inject the source basename into `{{SOURCE_FILE}}`.
3. **Write the file** as `{{basename-of-source}}-visualization.html` into the current working folder
   (e.g. `sop-returns-2026-05-31.md` → `sop-returns-2026-05-31-visualization.html`). Overwrite on re-run.
4. Confirm in one short message: filename + a one-line note that it opens by double-clicking, and the
   **correction hint** (below) — that the person can check and fix steps right in the page.

## Annotation — how the person verifies and corrects (important)

The whole point is that people can **check and improve** the visual. There are two paths; both keep the source
`.md` as the single truth.

**In-page (the easy path, when JavaScript is on).** The page itself lets the employee:
- mark each step **correct / unclear / incorrect** (a note box opens for *unclear* / *incorrect*),
- **drag-reorder** steps (SOP: within the role · Process Documentation: stages, keeping role tags + hand-offs), and
- **fix step text** in place.

When they click **"Apply changes"** the page assembles **paste-ready Markdown**: a regenerated `## Steps`
body (if they reordered/edited) and/or an appended `## Annotations` block (if they flagged steps). They copy the
block into the source `.md`, save, and say *"visualize"* again. **The page writes nothing itself and saves
nothing without that explicit click** — mirror this when you describe it.

**By hand (the fallback, and what happens with JavaScript off).** Open the source `.md`, add/extend `## Annotations`
at the bottom in plain language, save, and ask Claude to *"visualize"* again. The footer titled **"Does this look
right?"** spells out exactly these steps and is the read-only fallback.

**Writeback contract.** The exact writeback shape (regenerated `## Steps` body, `## Annotations` block, and the
`data-field`/`data-doctype` contract) is defined once in `html-template.md` — never restate it here; if you
change one, update the other.

- If the source already has an `## Annotations` section, render it as a clearly-marked card at the bottom (so the
  person sees their own notes) — you only *render* it; the in-page flow *appends* new flags below it and never
  overwrites it; the SOP/Process-Documentation skill is what folds notes back into the body.
- A printed copy carries a **"Read Aloud & Confirm"** sheet (one confirm line per step + sign-off slots) for
  two-person read-and-confirm — the strongest verification evidence. It appears only in print, never on screen.
- **Hypothesis** (the browser annotation tool the team uses) is **only for hosted explainer pages**, not for these
  per-run local files — it targets stable web URLs, not local `file://` outputs. Do not suggest it here.

Closing line example:
> *Done: `{{filename}}`. Double-click opens the view in the browser. You can check each step right there
> (correct / unclear / incorrect), reorder them, or fix the text — and clicking "Apply changes" gives
> you a finished text for the source file. Prefer by hand? Write your correction under `## Annotations`,
> save — and just tell me "visualize" again.*

## Special cases

- **Source is `-wip` / has `[OPEN]` markers:** render them visibly (small amber tag),
  so the reader sees what is still open — do not hide unfinished parts.
- **Source not found or unreadable:** ask for the file; never invent content to fill the page.
- **Re-run after edits:** just rebuild and overwrite the same `-visualization.html` — no version suffix needed.
