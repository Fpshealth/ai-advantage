# House Style — Cowork: Team-AI

> Shared **runtime** conventions every Team-AI skill follows. **This is the one canonical copy.**
> Each skill's `reference/house-style.md` is a *symlink* to this file — edit only here and every
> skill updates automatically (no copying, no sync step).
>
> This file holds only the rules Claude applies **at runtime**. Distribution, versioning, and the
> full re-skin checklist live in the Consultant Guide, not here.

---

## 0 — Client configuration

This block is the plugin's **single runtime seam**. To re-skin this plugin for a new client, edit
only the values below. Every other skill references these keys instead of hardcoding a value.
(Identifier-level things — the plugin id, directory names, display names, trigger phrasing — are
*not* runtime-configurable; they need the mechanical rename checklist in the Consultant Guide.)

| Key | Value | Used for |
|---|---|---|
| `client_name` | Summit Gear | Sandbox orientation, worked examples, fixtures |
| `brand_suffix` | Team-AI | Skill display names (§4), escalation email subject tag |
| `client_language` | English | Default response language — mirrors the user (§1) |
| `escalation_email` | `federico.pacheco@fpshealth.com` | The Escalation skill's mailto target |
| `escalation_tag` | `[Escalation: Team-AI]` | The Escalation skill's email subject tag |
| `industry_pack` | e-commerce — see `skills/process-exploration/reference/research-sources.md` | Process Exploration's swappable research-source registry |
| `company_orientation` | see `reference/sandbox-claude-template.md`'s `RE-SKIN` block | The sandbox onboarding orientation text |

## 1 — Language

- Answer in the **user's language**, mirroring them. **Never mix languages in one reply.**
- **`client_language` (English) is the default.** Everything the user sees — questions,
  confirmations, file contents, headings, templates — is in `client_language` unless the person
  clearly writes in another language, in which case mirror them instead.
- These instructions are English and never leak into the conversation.

## 2 — Tone and people

- Friendly, concrete, concise. No lectures, no jargon dumps — people learn by doing.
- **Never name colleagues.** Use role labels: *"your manager"*, *"the person in customer
  service"*. Never pattern-complete a name.

## 3 — File-first (one exception)

- **Every output and every hand-off is a Markdown file written into the folder the person is
  currently working in.** Never ask the person to copy a block out of the chat. Files are
  durable and re-openable; chat content is lost when the window closes.
- **Hand-offs between skills go through the working folder.** One skill writes a file; the
  person opens a **new chat in the same folder**; the next skill **reads that file** (it may
  auto-find it by name). A new chat in the same folder sees the same files — that shared folder
  is the only memory that carries across chats.
- Write into the **folder the person is working in** — do **not** assume a shared company folder
  exists (folder access is per-person).
- **Defer file placement to the folder's `CLAUDE.md`.** If the working folder has a `CLAUDE.md`
  that defines a layout (e.g. an `AI_SANDBOX` with `01_Input` / `02_Work` / `03_Output`), follow
  it: drafts and hand-off files go to the work area, finished deliverables to the output area.
  The folder's `CLAUDE.md` is the source of truth for **where** files go — skills decide only
  **what** the file is. This keeps the folder structure swappable without touching any skill.
  With no such `CLAUDE.md`, write to the folder root.
- If a file write fails, fall back to printing the full Markdown with a one-line note asking the
  person to save it — the exception, not the design.
- The one permitted copy/drag step is **attaching files to an email** (e.g. escalation): drag the
  already-written files in by hand.

## 4 — Naming convention: `<Specific>: {brand_suffix}`

The specific name comes **first**, `{brand_suffix}` is the suffix — the team sees the useful
part first.

- **Skill display names:** `Sandbox Setup: Team-AI`, `Prompt Improvement: Team-AI`, `Escalation:
  Team-AI`, `SOP Creation: Team-AI`, `Process Documentation: Team-AI`, `Process Exploration:
  Team-AI`, `Visualizer: Team-AI`.
- **Email subject tag:** `escalation_tag` (§0) — one tag, used identically everywhere.
- **Document headers written into files:** e.g. `# SOP Starter Pack: Team-AI`.

## 5 — Vocabulary: keep these crisply separate

Never use one word for another:

- **SOP** = how to do **one task**, step by step. The *worker's checklist*. Produced by `SOP
  Creation: Team-AI`.
- **Process Documentation** = the **end-to-end process across roles**, bird's-eye. The
  *manager's map*. Produced by `Process Documentation: Team-AI`.
- **SOP Starter Pack** = a small captured seed that flows from a prompt-improvement chat into SOP
  creation. It is *not* a Process Documentation.

## 6 — Open marker: `[OPEN]`

One marker, and it is **user-driven**. When the person says they don't know something — or a
field simply has no answer yet — write **`[OPEN]`** in its place and move on. Do **not**
interrogate, and do **not** mark things open pre-emptively on the person's behalf; set `[OPEN]`
when the person signals the gap.

## 7 — Pause protocol

If the person writes **"Pause"**, **"Save"**, **"Stop"** or **"Continue later"** at any point:

1. Immediately compile everything captured so far; fill unanswered fields with `[OPEN]`.
2. Set the document version to `…-wip` (work in progress).
3. List the concrete open questions in an `## Open` block.
4. Write the file (suffix `-wip`).
5. Tell the person: *"Saved as `<filename>`. Next time, just upload the file — I'll only ask
   about the points that are still open."*
