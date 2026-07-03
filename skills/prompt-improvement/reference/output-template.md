# Output Template for "Prompt Improvement: Team-AI"

The answer to the person has exactly these four sections, in this order.

## Section 1: Quick diagnosis

One or two sentences. Example:

> **Diagnosis:** You asked Claude for a customer email, but without a tone, an example, or a clear
> approach. The answer came out generic because **Tone (2)**, **Examples (4)**, and
> **Instructions (6)** were missing, and the **Background (3)** was unclear.

## Section 2: The 10 points with confidence

Per point: number, name, label, one-sentence value, and for 🟡/❌ a concrete follow-up question.

```
**1. Task & Role** ✅ Clear
Claude should write an email to a customer — a complaint about an outdoor backpack with a broken buckle.

**2. Tone & Behavior** ❌ Missing
No tone defined.
*Please add: friendly and accommodating (Summit Gear's default), or more brisk and factual?*

**3. Background** 🟡 Uncertain
Claude probably doesn't know Summit Gear. I'm assuming: online outdoor-gear retailer, 30-day
returns, no reason needed.
*Please confirm: is that right, or are there special rules for a manufacturing defect?*

**4. Examples** ❌ Missing
No example answer in the chat.
*Please add: do you have an older reply to a similar case that you liked? Paste it in as an example.*

**5. Prior History** ✅ Clear
Not relevant — new case.

**6. Instructions & Rules** ❌ Missing
No approach, no rules given.
*Please add: should Claude first analyze the request, then choose a solution, then write it up?
Any fixed rules (e.g. never promise delivery dates)?*

**7. The Content Now** ✅ Clear
The customer's email (inserted below in the prompt as <content>).

**8. Output Format** 🟡 Uncertain
Probably a complete email with subject line, salutation, body, sign-off. I'm assuming that.
*Please confirm: just the email body, or a subject line too? Last name or first name?*

**9. Important Rules (Reminder)** ✅ Clear
Added a brief closing rule (no delivery dates, no admission of fault).

**10. Start the Task** ✅ Clear
Clear starting signal at the end of the prompt.
```

## Section 3: The improved prompt

A single Markdown code block. The relevant building blocks with XML tags in the order of the
framework; optional, not-relevant building blocks (5 History) are left out. For ❌ building blocks,
use the placeholder `[PLEASE ADD: ...]`. Building block 10 is the instruction at the end (no tag).
Example:

````
```
<task>
You are a customer service representative at Summit Gear, an online outdoor-gear retailer. You are writing a reply to a complaint.
</task>

<tone>
[PLEASE ADD: friendly and accommodating OR brisk and factual?]
</tone>

<background>
Summit Gear is an online outdoor-gear retailer. We offer returns within 30 days, no reason needed.
[PLEASE CONFIRM: is that right? Any special rule for a manufacturing defect?]
</background>

<examples>
[PLEASE ADD: paste in an older, good reply to a similar case as a template]
</examples>

<instructions>
1. Read the customer's request in full.
2. Identify the core problem.
3. Choose the right solution (return / repair / replacement).
4. Write the reply in the defined tone.
</instructions>

<content>
[INSERT THE ACTUAL CUSTOMER EMAIL HERE]
</content>

<format>
A complete email with subject line, salutation (using last name), three paragraphs (empathy, solution, closing), sign-off.
[PLEASE CONFIRM: is that right?]
</format>

<important>
Never promise a specific delivery date. Never admit fault.
</important>

Now write the reply email to the customer.
```
````

## Section 4: Next steps

Exactly these two steps, clearly separated (do not change the wording). After that, **you wait**
until the person comes back — questions about SOP or escalation only come once they've reported
whether it worked.

> **1. Review & correct.** Open the file `prompt-improvement-….md` in your folder. Go through the
> 10 points — wherever it says `🟡` or `❌`, I guessed or something is missing. Add it directly in
> the file.
>
> **2. Try it in a new chat.** Copy the finished prompt from the file, open **a new chat in the
> same folder**, paste it in, and let Claude do the task. *(Why new? A fresh chat gives Claude a
> clean starting point — the result will be better.)* **Come back here afterward** and tell me
> whether the result was better this time.
