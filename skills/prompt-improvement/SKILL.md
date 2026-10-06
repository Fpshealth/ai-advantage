---
name: "Prompt Improvement: Team-AI"
description: 'Helps a team member improve a prompt when Claude''s answer wasn''t helpful. Analyzes the chat, fills in the 10-point prompt framework (Anthropic Prompting 101) with a confidence label per point, and writes an improved prompt to a file. Recognizes recurring tasks and — once the person confirms the better result — creates an SOP Starter Pack as a file. Use when the person is unhappy with an answer, feels misunderstood, or asks to improve a prompt or get a better result.'
---

# Prompt Improvement: Team-AI

Help the person turn a weak prompt into one that gets a good result next time. Read the chat so
far. Fill the whole **10-point prompt framework** and give each point a confidence label.
[10-point-framework.md](reference/10-point-framework.md) has the full list, the XML tags and the
confidence rubric.

**Follow `reference/house-style.md`** (language, file-first, naming). Key points repeated here:

- Mirror the person's language; **English by default** (`client_language`). Instructions are
  English; output follows the person's language unless they clearly write in another language.
- Follow house-style.md §2 (tone and people).
- **File-first:** write the improved prompt as a file into the current working folder.

## Iron rules

- Do **not** ask questions before you build. Fill all 10 points yourself, label their confidence,
  and let the person correct the file.
- Output **all 10 points**, even the obvious ones: the person learns from the full list.
- Write the improved prompt as **one single XML-tagged block**, in Anthropic's recommended order.
- **Quality gate** (see *Procedure* step 5): only after the person has actually tried the improved
  prompt, ask whether it worked better and whether the task recurs.

## The 10-point framework

Use this output order:

1. **Task & Role** · 2. **Tone & Behavior** · 3. **Background** ·
4. **Examples** · 5. **Prior History** (if relevant) · 6. **Instructions & Rules** ·
7. **The Content Now** · 8. **Output Format** ·
9. **Important Rules (Reminder)** (optional) · 10. **Start the Task**

## Confidence labels (one per point)

- ✅ **Clear** — directly extractable from the chat, high confidence.
- 🟡 **Uncertain** — inferred from the chat, please confirm.
- ❌ **Missing** — not mentioned, please add.

For 🟡 and ❌, write one **concrete follow-up question** the person can answer in a sentence.

## Procedure

**Step 1 — Scan the chat.** Read every message from the person, every Claude reply, and any
attachments referenced. Note internally: original task, what Claude delivered, why it
disappointed (too generic, wrong domain, wrong tone, wrong format, hallucinated details…).

**Step 2 — Diagnosis.** One or two sentences: what was wrong, which of the 10 points was
thinnest.

**Step 3 — Fill the 10 points.** Per point: confidence label, your reading, and for
🟡/❌ a concrete follow-up question. Use the format in [output-template.md](reference/output-template.md).

**Step 4 — Build the improved prompt and write it to a file.** Build one Markdown code block with
the relevant points in XML tags, in this order: `<task>`, `<tone>`, `<background>`,
`<examples>`, `<history>`, `<instructions>`, `<content>`, `<format>`, `<important>`. Point 10 is
the closing instruction, with no tag. For ❌ points, insert `[PLEASE ADD: …]` placeholders. If
an optional point (5 History, 9 Important) is not relevant, drop it. **Write the file** into the
current working folder as `prompt-improvement-{short-slug}-{YYYY-MM-DD}.md` (diagnosis + the 10
points + the prompt block). Tell the person the filename. Show the prompt block in the chat so they
can copy it.

**Step 5 — Send them to test it, then stop.** Say exactly:

> Go through the 10 points in the file. Wherever it says `🟡` or `❌`, I guessed or something is
> missing — correct it directly in the file. Then copy the prompt, open **a new chat in the same
> folder**, and send it to Claude. **Come back here afterward and tell me whether the result was
> better this time.**

Do **not** ask the two gate questions yet. Wait for the person to come back.

**Step 6 — Only after the person reports back:**

- **If they say it worked better** → ask the single recurring question: *"Nice! Do you do this
  task regularly?"*
  - **If yes** → write an **SOP Starter Pack** file (see below) and point them to SOP Creation.
  - **If no** → close warmly: *"Great, then we're done here."*
- **If they say it still doesn't fit** → point them to escalation: *"Type `escalate` — I'll show
  you how to send the whole session to your consultant with `/export`."*

## Writing the SOP Starter Pack (only when the person confirmed: better result **and** recurring)

Write a file into the current working folder named `sop-starter-{short-slug}-{YYYY-MM-DD}.md`:

````markdown
# SOP Starter Pack: Team-AI

> Automatically captured from a prompt-improvement chat. Handoff to "SOP Creation: Team-AI".

- **Task:** {task name in the person's words}
- **Domain:** {e.g. customer service, product data, photography, bookkeeping — or [not yet clear]}
- **Tools used:** {from the chat, or [not yet clear]}
- **Observed steps:** {what can be read from the chat; gaps marked [not yet clear — captured in the SOP interview]}
- **Confirmed result:** {one sentence on why the improved prompt gave a better result}
- **Improved prompt:** see `prompt-improvement-{slug}-{date}.md`
````

Then tell the person: *"I've put an SOP Starter Pack as the file `<name>` in the same folder. Open
**a new chat in the same folder** and type "create SOP" — SOP Creation will find the file
automatically and only ask you about what's still missing. At the end you'll have the finished SOP
document."*

## What you do not do

- Do not escalate yourself: that is the `Escalation: Team-AI` skill, only when the person asks.
- Do not invent anything in the SOP Starter Pack. Keep gaps marked open.
