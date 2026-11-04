# Cold read

How to run it: start a fresh Opus subagent and give it only the page and its pictures: the PNGs from `--shots`, every image file the page shows, and one PNG per animation step (click Next in Playwright and screenshot each step). Without Playwright there are no PNGs: give the image files and say in `<images>` that the diagrams appear only as SVG code in the page. Give it no repository and no conversation, because the real reader has neither, and it reads HTML as text, so it sees pictures only as images. Round 1 uses the cold-read brief below. If the verdict is FAIL, later rounds use the check-read brief at the end, with only the findings and the sections you changed.

## Cold-read brief

Replace `<path>`, `<goal>` and `<images>`, then pass the whole brief as the prompt.

---

You are the reader of the document at `<path>`. You are intelligent and new to the subject. Your goal: `<goal>` (default: after reading, explain the system to someone else, run it, and see when it breaks). Read only this file and these images: `<images>` (screenshots of the page's pictures as they render, and the image files it shows). Open nothing else and search nothing, because the real reader has nothing else. Judge every picture from its image, not from its HTML source.

Read the whole document once, in order, as a learner. At the first appearance of every thing it names (a file, program, tool, data source, person, role, number, decision), ask:

1. What is this, literally? A name, a figure of speech or a category label does not answer it.
2. Who or what makes or changes it, and from what?
3. How current is it? Does it update by itself? When, and what triggers it?
4. Does it exist today, or is it planned?
5. Is it the same thing as another name in the text? Does this word mean something different from where it was defined? Does the text put it in a category that an earlier definition excludes?

Also ask:

- For every claim: what is the reason, and how does the text know (a linked source, someone's claim, an inference, a guess)?
- For every instruction: could you carry it out on a computer with nothing set up, starting from the place the text names? Does it say who acts, or does it rely on an "I" or "we" the text never names?
- For every section: which question does it answer, and does it answer it?
- For every analogy: which literal statement does it stand for, and where does it break?
- For every diagram or screenshot: can you read its text, and what should you remember from it?
- For every animation: can you follow each step, and does each step say what changed?
- For every section without a picture: would a screenshot, a diagram, real output or a step-through have shown it faster than the text did? Report each one as a finding with the question "picture".

Then judge the document against this rubric. Each row is PASS or FAIL, with a quote as evidence:

| # | Rubric item |
|---|---|
| R1 | The paragraph before the first section says what the whole system is, so that you could repeat it to your boss. |
| R2 | Each section opens with a question a newcomer would ask, and the section answers it. |
| R3 | One real case (real names, values or output) appears in every section and reaches its end. |
| R4 | Each thing is defined literally in the sentence where it first appears, and keeps one name. |
| R5 | Each claim gives its reason and its status: a linked source, someone's claim, an inference, or open. |
| R6 | You can read the text in every picture, and each caption says what to remember from it. |
| R7 | Each animation shows the whole picture first, and each step says what changed. |
| R8 | You could carry out every instruction on a computer with nothing set up. |

Write N/A for a row with nothing to judge (no animation, no instruction).

Report in this format:

## Verdict: PASS or FAIL
FAIL if any finding is blocking. A rubric row can FAIL on non-blocking findings only; the verdict is then PASS.

## Rubric
| # | PASS, FAIL or N/A | Quote |
|---|---|---|

## First place I got lost
Quote the passage exactly and say what you were missing.

## Findings
| # | Exact quote (max 20 words) | Question (1-5, claim, instruction, section, analogy, picture) | What I cannot answer from the text | Blocking |
|---|---|---|---|---|

Blocking means a reader with the goal above cannot go on, or would believe something false. Report every finding. Quote exactly, so the writer can find the passage.

## What works
Up to five points, each with a quote.

---

## Check-read brief

Replace `<findings>`, `<sections>` and `<images>`, then pass the whole brief as the prompt.

---

You check fixes to a document that a first reader found problems in. The findings: `<findings>`. The changed sections, as they are now: `<sections>`. Screenshots of their pictures: `<images>`. Read only these, because you check the fixes, not the whole document again. Open nothing else and search nothing.

For each finding, quote the changed text and say Fixed or Not fixed. Then read the changed sections as a learner, with the questions of the cold read, and report each new problem that the fix brought in.

Report in this format:

## Verdict: PASS or FAIL
FAIL if any finding is Not fixed and blocking, or any new finding is blocking.

## Earlier findings
| # | Fixed or Not fixed | Quote of the changed text |
|---|---|---|

## New findings
| # | Exact quote (max 20 words) | What I cannot answer from the text | Blocking |
|---|---|---|---|
