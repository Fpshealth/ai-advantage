---
name: "Escalation: Team-AI"
description: 'Guides a person to escalate a stuck session to their consultant – Claude writes a complete handoff file from full session context (goal, attempts, tools used, exact errors), then the person sends it with a pre-filled email to the consultant''s configured address (see house-style.md §0). The handoff file is the entire escalation record — Cowork has no session export. Use this skill when the person explicitly wants to escalate, or when a second attempt still doesn''t fit after prompt improvement. English triggers: "escalate", "send this to my consultant", "I need help from my consultant", "still doesn''t work after the retry".'
---

# Escalation: Team-AI

When a person wants to hand a stuck session to their consultant, **you write the handoff**: a
context file the consultant can act on, from your full view of this session. The person then
emails it in two clicks. Cowork has no session export (`/export` is a Claude Code feature and
does nothing here), so the handoff file is the only record the consultant gets.

**Follow `reference/house-style.md`** — especially §1: everything the person sees is in their
language.

## Rules

- The email address is the `escalation_email` configured in `house-style.md` §0.


## Procedure

**Step 1 — One-line problem.** Ask the person for a single sentence: what were they trying to
do, and what still doesn't work? That sentence becomes the email subject.

**Step 2 — Write the handoff file.** Write `03_Output/escalation-handoff.md` (add a short topic
suffix if one already exists), in the person's language:

1. **Goal** — one short paragraph.
2. **What we tried** — the attempts in order, one line each.
3. **Tools & actions** — what you actually did: skills invoked, code run, files read/written,
   searches made — one line each. This is the consultant's debugging trace.
4. **Where it's stuck** — the exact blocker; error messages **verbatim**, complete.
5. **Files** — every file created or used in this session, with its sandbox path; mark which
   ones the email will attach.
6. **One-line problem** — the sentence from Step 1.

Aim for one page; two only if the error output needs the space. Tell the person what you wrote
and where.

**Step 3 — Guide the email.** In the person's language, walk them through three steps: (1) the
link below opens a ready-made email **draft** to their consultant — nothing is sent yet; (2)
drag the **handoff file** from `03_Output` (and any file created here) into the email; (3) only
clicking **Send** sends it.

**Step 4 — The pre-addressed link.** Build it with this exact command — hand-encoding mailto
links silently breaks umlauts. Change only the quoted arguments (the problem sentence, the
`escalation_email` from §0) and, if the conversation isn't in English, translate the `body` text
inside the script to the person's language. The Python runs inline via the heredoc; plugin
script files are not available in the Cowork code-execution sandbox.

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

Output the printed link verbatim. Directly above it, warn in the person's language: the link
only opens a **draft** — the consultant receives nothing until the person clicks **Send**.

If code execution is unavailable, use this pre-verified static link instead (the specifics are
in the handoff file anyway):

> `[➜ Open email DRAFT to your consultant (not sent yet)](mailto:federico.pacheco@fpshealth.com?subject=%5BEscalation%3A%20Team-AI%5D&body=Hi%2C%0A%0AI%27m%20stuck%20and%20I%27m%20handing%20this%20session%20over%20to%20you.%0AAttached%3A%20the%20handoff%20file%20%28goal%2C%20attempts%2C%20exact%20blocker%29%20and%20the%20file%20we%20created%20together.)`

If the link doesn't open at all: a plain email to the `escalation_email` address, subject
*"{escalation_tag} {one-line problem}"*, handoff file attached.
