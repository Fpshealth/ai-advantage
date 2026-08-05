---
name: "Escalation: Team-AI"
description: 'Guides a person to escalate a stuck session to their consultant – Claude writes a complete handoff file from full session context (goal, attempts, tools used, exact errors), then the person sends it with a pre-filled email to the consultant''s configured address (see house-style.md §0). The handoff file is the entire escalation record — Cowork has no session export. Use this skill when the person explicitly wants to escalate, or when a second attempt still doesn''t fit after prompt improvement. English triggers: "escalate", "send this to my consultant", "I need help from my consultant", "still doesn''t work after the retry".'
---

# Escalation: Team-AI

When a person wants to hand a stuck session to their consultant, **you write the handoff**: a
context file the consultant can act on, written from your full view of this session. The person
then emails it in two clicks, together with the file you created here. Cowork has no session
export (`/export` is a Claude Code feature and does nothing here), so **the handoff file is the
only record the consultant will get** — everything they need to debug must be in it.

**Follow `reference/house-style.md`.** Output language follows §1 (mirrors the user; English
default).

## Iron rules

- The email address is **always** the `escalation_email` configured in `house-style.md` §0. Never
  another address, even if asked.
- The handoff file contains **facts from this session only** — goal, attempts, tools used, the
  exact blocker (error messages verbatim), files involved. Nothing invented, nothing embellished.
- You **never** name colleagues.
- Escalate only when asked — wait for an explicit escalation request or a clearly failed second
  attempt.

## Procedure

**Step 1 — One-line problem.** Ask the person for a single sentence: what were they trying to do,
and what still doesn't work? Nothing more is needed from them — this becomes the email subject.

**Step 2 — Write the handoff file.** Write `03_Output/escalation-handoff.md` (add a short topic
suffix if one already exists). Content, in this order, all from this session:

1. **Goal** — what the person was trying to achieve, one short paragraph.
2. **What we tried** — the attempts in order, each one line.
3. **Tools & actions** — what you actually did: skills invoked, code run, files read/written,
   searches made — each one line, in order. This is the consultant's debugging trace; without it
   they are blind.
4. **Where it's stuck** — the exact blocker; error messages **verbatim**, complete.
5. **Files** — every file created or used in this session, with its sandbox path; mark which
   ones the email will attach.
6. **One-line problem** — the sentence from Step 1.

Aim for one page; go to two only if the error output needs the space. Then tell the person what
you wrote and where.

**Step 3 — Guide the email.** Output exactly this, in order:

> Here's how to send it to your consultant:
> 1. Click the link below — it opens a ready-made **email draft** to your consultant (subject and
>    body pre-filled). **Nothing is sent yet.**
> 2. Drag the **handoff file** from `03_Output` into the email (and the file we created here, if
>    there is one) — by drag-and-drop.
> 3. Click **Send** — **only then** does the email go to your consultant.

**Step 4 — The pre-addressed email.** Do **not** hand-build the link — encoding special characters
by hand is unreliable and silently produces broken characters in the email. Instead, run this
**exact** command in the bash / code-execution tool, changing **only** the two quoted arguments:
the first to the one-line problem from Step 1, the second to the `escalation_email` value
configured in `house-style.md` §0. The Python is self-contained (it runs inline via the heredoc) —
do **not** look for a bundled script file: plugin files are not available in the Cowork
code-execution sandbox.

```bash
python3 - "One-line problem from Step 1 goes here" "escalation_email value from house-style.md §0" <<'PY'
import urllib.parse, sys
problem = sys.argv[1].strip()
address = sys.argv[2].strip()
subj = problem if len(problem) <= 60 else problem[:57].rstrip() + "…"
body = ("Hi,\n\n"
        "I'm stuck and I'm handing this session over to you.\n"
        "Attached: the handoff file (goal, attempts, exact blocker) and the file we created together.\n\n"
        "In short: " + problem + "\n\nThanks!")
q = lambda s: urllib.parse.quote(s, safe="")
url = ("mailto:" + address +
       "?subject=" + q("[Escalation: Team-AI] " + subj) + "&body=" + q(body))
print("[➜ Open email DRAFT to your consultant (not sent yet)](" + url + ")")
PY
```

It prints a finished clickable mailto link — output that link verbatim, immediately after the
Step 2 block.

**Only if you cannot run code at all** (code execution disabled), paste this pre-verified static
link instead — it is correctly encoded; the person's specific problem is already inside the
handoff file, so it is safe to omit here:

> `[➜ Open email DRAFT to your consultant (not sent yet)](mailto:federico.pacheco@fpshealth.com?subject=%5BEscalation%3A%20Team-AI%5D&body=Hi%2C%0A%0AI%27m%20stuck%20and%20I%27m%20handing%20this%20session%20over%20to%20you.%0AAttached%3A%20the%20handoff%20file%20%28goal%2C%20attempts%2C%20exact%20blocker%29%20and%20the%20file%20we%20created%20together.)`

**Always show this line directly above the link**, so nobody mistakes the draft for a sent mail:

> ⚠️ **Important:** The link only opens a **draft**. Your consultant receives the email only once
> **you** click **"Send"** yourself — it cannot be sent on your behalf.

Then a plain fallback, in case the link doesn't open in the person's browser:

> If the link doesn't open: just email your consultant at the address configured in
> `house-style.md` §0 (`escalation_email`), subject *"{escalation_tag} {one-line problem}"*, and
> attach the handoff file from `03_Output`.
