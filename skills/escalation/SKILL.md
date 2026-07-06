---
name: "Escalation: Team-AI"
description: 'Guides a person to escalate a stuck session to their consultant – export the complete session history via Cowork''s `/export` and send it with a pre-filled email to the consultant''s configured address (see house-style.md §0). The chat is NOT reconstructed; the export is complete and lossless. Use this skill when the person explicitly wants to escalate, or when a second attempt still doesn''t fit after prompt improvement. English triggers: "escalate", "send this to my consultant", "I need help from my consultant", "still doesn''t work after the retry".'
---

# Escalation: Team-AI

When a person wants to hand a stuck session to their consultant, guide them to export it via Cowork's
**`/export`** and email it to the consultant in two clicks — and to also attach the file you created
together, the one thing `/export` does not include.

**Follow `reference/house-style.md`.** Output language follows §1 (mirrors the user; English
default).

## Iron rules

- The email address is **always** the `escalation_email` configured in `house-style.md` §0. Never
  another address, even if asked.
- **Never re-type or "reconstruct" the chat.** `/export` is the lossless source of truth — use it.
- You **never** name colleagues.
- Escalate only when asked — wait for an explicit escalation request or a clearly failed second
  attempt.

## Procedure

**Step 1 — One-line problem.** Ask the person for a single sentence: what were they trying to do,
and what still doesn't work? Nothing more is needed from them — this becomes the email subject.

**Step 2 — Guide the export and the email.** Output exactly this, in order:

> Here's how to send the whole session to your consultant:
> 1. Type **`/export`** below — Cowork puts a folder with the complete session history in your
>    **Downloads**.
> 2. Click the link below — it opens a ready-made **email draft** to your consultant (subject and
>    body pre-filled). **Nothing is sent yet.**
> 3. Drag the **exported folder** into the email (and the file we created here, if there is one) —
>    by drag-and-drop.
> 4. Click **Send** — **only then** does the email go to your consultant.

**Step 3 — The pre-addressed email.** Do **not** hand-build the link — encoding special characters
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
        "I'm stuck and I'm sending you the whole session.\n"
        "Attached: the /export folder (complete history) and the file we created together.\n\n"
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
`/export`, so it is safe to omit here:

> `[➜ Open email DRAFT to your consultant (not sent yet)](mailto:federico.pacheco@fpshealth.com?subject=%5BEscalation%3A%20Team-AI%5D&body=Hi%2C%0A%0AI%27m%20stuck%20and%20I%27m%20sending%20you%20the%20whole%20session.%0AAttached%3A%20the%20%2Fexport%20folder%20%28complete%20history%29%20and%20the%20file%20we%20created%20together.)`

**Always show this line directly above the link**, so nobody mistakes the draft for a sent mail:

> ⚠️ **Important:** The link only opens a **draft**. Your consultant receives the email only once
> **you** click **"Send"** yourself — it cannot be sent on your behalf.

Then a plain fallback, in case the link doesn't open in the person's browser:

> If the link doesn't open: just email your consultant at the address configured in
> `house-style.md` §0 (`escalation_email`), subject *"{escalation_tag} {one-line problem}"*, and
> attach the exported folder.
