---
name: "Handoff: Team-AI"
description: 'Writes a short handoff file so the work continues in a fresh Cowork session without carrying the whole chat history. Use when the person wants to start a new session but keep the progress, when a session has grown long, after a long break, or when they ask for a handoff or "Übergabe", or to "take the progress along".'
argument-hint: "What will the next session be used for?"
---

# Handoff: Team-AI

Adapted from Matt Pocock's `handoff` skill (MIT, github.com/mattpocock/skills).

Every message in a session re-sends the whole history, so a long session gets more expensive with
each turn. A handoff lets the person close this session and start fresh: the new session reads a
few lines instead of the full chat.

**Follow `reference/house-style.md`.**

## Procedure

**Step 1 — Next session's focus.** If the person passed an argument, that is the focus. Otherwise
ask one question: what should the next session do? Tailor the handoff to that focus and leave out
what it doesn't need.

**Step 2 — Write the file.** Name it `handoff-<short-topic>.md`, in the person's language (German:
`uebergabe-<thema>.md`, e.g. `uebergabe-retouren-sop.md`). Save it to the work area if the folder's `CLAUDE.md` defines one
(`02_Work`), else the folder root. Write it in the person's language. At most about 20 lines, in this order:

1. **Goal** — the overall result this work is heading for
2. **Next session** — the focus from Step 1
3. **Status** — what is done, what is not
4. **Decisions** — each with its reason, so the next session doesn't reopen them; if the chat gives no reason, write `[OPEN]`, never guess one
5. **Open items** — in the order to tackle them
6. **Files** — every relevant file by path; reference, never copy its content
7. **Suggested skills** — which skills the next session should start with, if any

Not a retelling of the chat. Leave out passwords, access data and customer personal data.

**Step 3 — Hand over.** Tell the person, in short points: (1) the file's path; (2) open it, check
it and correct it if needed; (3) start a new session **in the same folder**, so it finds the file; choose the model there
first and keep effort at Medium unless the task needs more;
(4) paste this as the first message:

> Read `<path>` and continue with the open items.

(Give this line in the person's language with the real path, e.g. „Lies `02_Work/uebergabe-retouren-sop.md` und mach bei den offenen Punkten weiter.")
