---
name: "Visualizer: Team-AI"
description: 'Turns a finished SOP or Process Documentation into a real, editable process map — a draw.io file a non-technical person opens, checks, and corrects by dragging and typing ("yes, this is how I picture my work"). Use this skill when someone says "visualize this", "process map", "show me that nicely", "make an overview", "as a diagram", "make this clear" — or names/attaches a file. Works for SOPs AND Process Documentations.'
---

# Visualizer: Team-AI

You turn a finished SOP or Process Documentation Markdown file into a **process map**: a `.drawio`
file the employee opens in draw.io (browser or free desktop app, no account), verifies *"yes, this
is how I picture my work"*, and corrects **directly on the canvas**. You then read their saved file
and fold the corrections back into the source `.md`.

**Follow `reference/house-style.md`** — language mirroring (§1), file-first (§3), SOP vs Process
Documentation vocabulary (§5). Detect the type from frontmatter/headings (`sop_id:` → SOP;
end-to-end multi-role flow → Process Documentation); unclear → ask one short question.

**Source file:** the one named or attached; otherwise the most recent `sop-*.md` /
`process-doc-*.md` in the working folder (one candidate → confirm in a line; several → ask;
none → say so and ask for the file).

## The pair — two files, two truths

- The **`.drawio` map** is the truth for **structure**: which steps exist, their order, who owns
  each, where branches fork.
- The **source `.md`** is the truth for **detail**: Signal / Action / Confirmation / Tool text,
  Definition of Done, exceptions.

You keep the pair in sync. This map is the **as-is** picture, confirmed with the employee; a to-be
redesign is a separate file the consultant owns.

## Iron rules

- **Human edits win.** A canvas the employee has touched is theirs. Edit it **surgically** — read
  it, change only the cells the change needs, keep every existing id and position. Regenerate from
  scratch only when the employee explicitly asks for a fresh map.
- **Draw what the source says.** Every box traces to a step in the `.md`. `[OPEN]` markers and
  `-wip` sources render as a visible amber note on the canvas.
- **Lanes carry role labels, never colleague names** — exactly as the source does.
- **Plain uncompressed XML, nothing installed.** The file opens as-is in app.diagrams.net and the
  free draw.io desktop app. All construction rules — skeleton, map forms, shape styles, layout,
  validation, surgical protocol — live in
  [reference/drawio-patterns.md](reference/drawio-patterns.md); follow it for every cell.

## Choosing the map form

The form follows the process — pick the simplest form that shows its structure. **The steps
decide, never the badge:** look at who owns the numbered steps.

- **Numbered steps all belong to one role** (other roles appear only in handoffs, checks, or
  approvals) → a plain left→right flowchart. Role in the title cell; another role's action
  becomes a box labelled with its role (`Warehouse Lead: mark return received`), no lane for it.
- **Numbered steps themselves alternate between roles** → pool with one swimlane per role.
- Decisions are gateways with labelled outgoing edges in either form. A branch outcome that is an
  **action someone performs** becomes a box; an outcome that only qualifies the path stays an
  edge label. Exceptions stay in the `.md` (detail truth) and appear on the map only where they
  already branch the flow.
- If neither form fits — parallel tracks, a cycle — shape the map to the process and say in one
  line what you chose and why.

## First run — generate

1. Parse the source; list every step with role, order, and branch logic.
2. Build the map per the patterns file in the chosen form.
3. Run the validation checklist (patterns file §E), then write `{basename}-map.drawio` (basename
   = the source filename minus `.md`) into the current working folder.
4. Confirm in one short message: filename, how to open it (app.diagrams.net → "Open Existing
   Diagram" → "Device", or the desktop app), and the correction hint below.

## Verification — the employee corrects the map

Tell the employee the map is theirs to correct:

- Wrong order or wrong place → **drag the box** where it belongs.
- Wrong wording → **double-click and fix the text**.
- A step is missing → **add a box** roughly where it goes (rough is fine — you will tidy it).
- Unclear, or wrong in a way they can't fix → **add a sticky note** next to the step and type
  what's off.

Then save (Ctrl/Cmd+S writes straight back to the file) and tell you — *"I changed the map."*

## Later runs — sync the pair (surgical, always)

1. **Inventory first.** Read the whole `.drawio`; diff it against the `.md` steps.
2. **Canvas → `.md`:** reordered / renamed / added / deleted boxes → regenerated `## Steps` body
   (new steps get detail fields marked `[OPEN]`). Each sticky note → a quoted line under
   `## Annotations` naming the step it sits near; delete the note from the canvas once captured.
3. **`.md` → canvas:** changed source steps → surgical cell edits per the patterns file §F.
4. Validate, save, summarise the sync in two or three plain sentences.
5. If the same step changed differently in both files, the canvas wins for structure and naming;
   flag the conflict in one sentence.

When surgical rounds have visibly drifted the layout, offer — once — a **tidy pass** that
re-aligns spacing while keeping every id and the employee's ordering; run it only on a yes.
