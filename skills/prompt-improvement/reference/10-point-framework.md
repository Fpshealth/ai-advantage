# The 10-Point Prompt Framework

> **Not every prompt needs all ten.** Optional building blocks are simply marked *"not relevant."*

## The ten building blocks at a glance

| # | Building block | XML tag | What goes here |
|---|----------|---------|---------------------|
| 1 | **Task & Role** | `<task>` | Who is Claude, what should it do? |
| 2 | **Tone & Behavior** | `<tone>` | How should Claude sound? How should it handle uncertainty? |
| 3 | **Background** | `<background>` | Company info, domain knowledge, attached documents |
| 4 | **Examples** | `<examples>` | One good example: input → desired answer |
| 5 | **Prior History** | `<history>` | Relevant earlier messages — *if relevant* |
| 6 | **Instructions & Rules** | `<instructions>` | The step-by-step approach + fixed boundaries |
| 7 | **The Content Now** | `<content>` | The concrete material for this specific case (email, file, text) |
| 8 | **Output Format** | `<format>` | Length, structure, shape of the answer |
| 9 | **Important Rules (Reminder)** | `<important>` | The most critical rule, restated at the end — *optional* |
| 10 | **Start the Task** | *(no tag)* | The clear instruction to begin: *"Go ahead now."* |

**Order logic:** **Context before content, instruction before execution.**

## What each building block means

**1. Task & Role** · `<task>`
Role + core task in one sentence. *"You are a customer service representative at an outdoor-gear
retailer, writing a reply to a complaint."*
*Typical gap:* role undefined, task too vague ("write something nice").

**2. Tone & Behavior** · `<tone>`
How Claude should sound. *"Friendly, solution-oriented. If you don't know something, say so openly
instead of guessing."*
*Typical gap:* no tone → Claude picks a generic, often overly formal tone.

**3. Background** · `<background>`
The *static* context Claude needs to know. *"Summit Gear is an online outdoor-gear retailer;
30-day returns, no reason needed."*
*Typical gap:* Claude knows nothing about the company, the domain, or the customer.

**4. Examples** · `<examples>`
At least one input-output pair showing what "good" looks like. Examples carry more weight than any
description — that's why they come **before** the instructions.
*Typical gap:* no examples → Claude guesses what you consider good.

**5. Prior History** · `<history>` — *if relevant*
Relevant points from an earlier exchange. *"Last week the customer wanted a repair; today they'd
rather have a refund."*
*Typical gap:* often simply *not relevant* — then mark it ✅ "not relevant."

**6. Instructions & Rules** · `<instructions>`
The heart of the instruction: the exact approach **step by step** plus fixed boundaries. *"1. Read
the request in full. 2. Identify the core problem. 3. Choose the right solution. 4. Write in the
defined tone. Rule: never promise a specific delivery date."*
*Typical gap:* only a goal, no sequence → the answer jumps around or skips steps.

**7. The Content Now** · `<content>`
The concrete material for *this* case — clearly separated from the rest. *"`<content>`Dear Sir or
Madam, after the first hike the backpack's buckle broke…`</content>`"*
*Typical gap:* the content is buried in running text between the instructions → Claude doesn't
separate instruction from material.

**8. Output Format** · `<format>`
What the answer should look like. *"A complete email with subject line, salutation using last
name, three paragraphs (empathy, solution, closing), sign-off."*
*Typical gap:* no format → Claude produces free-form prose with unwanted headings.

**9. Important Rules (Reminder)** · `<important>` — *optional*
The one or two most critical rules repeated at the **end** — what comes last carries the most
weight. *"Important: don't promise delivery dates, don't admit fault."*
*Typical gap:* often *not necessary* for short prompts — then leave it out.

**10. Start the Task** · *(no tag)*
The clear starting signal at the end. *"Now write the reply email to the customer."*
*Typical gap:* the prompt ends with context, without clearly sending Claude off.

## The confidence rubric

Assign exactly one per building block:

| Label | Meaning | What you do with it |
|---------|-----------|----------------------|
| ✅ **Clear** | Value is directly readable from the chat (or "not relevant") | Carry it over, no follow-up needed |
| 🟡 **Uncertain** | Value is inferred from the chat, could be wrong | Write one concrete follow-up question |
| ❌ **Missing** | Value isn't mentioned in the chat at all | Concrete follow-up question + placeholder in the prompt |

## The XML tags in the improved prompt

One tag per building block, in exactly this order (building block 10 is just the instruction, no
tag):

```
<task>...</task>
<tone>...</tone>
<background>...</background>
<examples>...</examples>
<history>...</history>
<instructions>...</instructions>
<content>...</content>
<format>...</format>
<important>...</important>
```

- For ❌ building blocks, insert a placeholder in square brackets: `[PLEASE ADD: concrete question]`.
- **Optional building blocks** (5 History, 9 Important) may be left out when they're not relevant —
  in that case mark them **not** ❌, but ✅ with the value *"not relevant."*
