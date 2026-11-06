---
name: fps
description: 'Entry point for creating a build-ready document: an SOP, a Prozessdokumentation or a project pitch. Asks what the person wants to create, then leads them through the matching playbook with the built-in completeness check. Use for /fps, or when someone wants to document a task or a process, write an SOP, or pitch or submit a project idea.'
---

# fps

You lead one person through one document. The person says what to create. You open the matching
playbook and run its steps in order. Follow `reference/house-style.md` (language, tone, no
colleague names).

## Pick the playbook

| The person wants to | Playbook |
|---|---|
| document one task (SOP) or a whole process across roles (Prozessdokumentation) | `playbooks/ablauf-dokumentieren.md` |
| propose a project or an idea (Pitch) | `playbooks/pitch.md` |

If the first message does not say which, ask one question: "Was möchtest du erstellen: eine SOP
(eine Aufgabe, eine Person), eine Prozessdokumentation (ein Ablauf über mehrere Rollen) oder einen
Pitch (eine Projektidee)?" If the person is unsure between SOP and Prozessdokumentation, choose
`ablauf-dokumentieren`; it sets the depth from the first answers.

One document per run. If the person names two tasks or two ideas, pick one with them and offer a
new chat for each of the others.

## Run the playbook

1. Open the playbook file. Copy its numbered steps into your task list, word for word.
2. Tell the person in two sentences what will happen and roughly how long it takes.
3. Run the steps in order. A step you skip stays in the list with `skip: <reason>`.
4. Never mark the document done until `scripts/check.py` exits 0 on it. The check is part of
   writing the document, not an option.

Run every script by its full path inside this skill folder. If the shell cannot open the skill
folder, copy `scripts/`, `schema/`, `template/` and `reference/` together into the work folder and
run them from there.

## Everyday tools

These are separate skills. Offer one when it fits. They are not playbook steps (except
`sharpen`, step 1 of the pitch).

| Skill | When |
|---|---|
| `in-your-own-words` | Before any larger task, so Claude restates the goal first. Fewer rounds, fewer tokens. |
| `sharpen` | A task feels vague or too small. |
| `eli5`, `clear-explanation` | Someone needs a topic or a finished document explained. |
| `handoff` | The chat gets long. Continue in a fresh chat. |
| `escalation` | Stuck after a second try. Send the session to the consultant. |
| `process-exploration` | Someone wants to rethink a process, not document it as it is. |
