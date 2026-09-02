---
name: "Escalation: Team-AI"
description: 'Hands a stuck session to the consultant: Claude writes a handoff file, the person sends it via a pre-addressed email draft. Use when the person asks to escalate or to involve their consultant, or when a retry after prompt improvement still fails.'
---

# Escalation: Team-AI

You write the handoff; the person emails it. The handoff file is the consultant's record of this
session, whatever else the host lets the person attach.

**Follow `reference/house-style.md`.** `escalation_email` and `escalation_tag` are in its §0.

## Capabilities — confirm before you offer

Two things differ by host. Decide each from evidence — what your system prompt says about where
you run, your tool list, a command you can see documented, a call that succeeded — and offer only
what you confirmed:

- **Session export** — a host command that saves the whole chat. Claude Code has `/export`;
  on any other host, offer one only when you see it documented in this session. Confirmed →
  Step 4 adds it as an attachment. Unconfirmed → the handoff file alone is the record.
- **Script by path** — the shell opens `scripts/mailto_link.py`. If it can't, read the file and
  pipe its content: `python3 - "<address>" "<subject>" "<body>" <<'PY' … PY`.

## Procedure

**Step 1 — One-line problem.** Propose one sentence from the session — what they were trying to
do and what still fails — and let the person confirm or correct it. It becomes the email subject.

**Step 2 — Handoff file.** Write `escalation-handoff.md` (topic suffix if the name is taken) as
a finished deliverable: the output area if the folder's `CLAUDE.md` defines one, else the folder
root. Sections, in the order a consultant reads them:

1. **Goal**
2. **What we tried** — attempts in order
3. **Tools & actions** — skills invoked, code run, files read/written, searches made: the
   consultant's debugging trace
4. **Where it's stuck** — error messages verbatim and complete
5. **Files** — every file this session created or used, with path; mark which the email attaches
6. **One-line problem**

Done when the consultant could resume from the file alone. Tell the person the path.

**Step 3 — Draft link.** `scripts/mailto_link.py` prints the URL; arguments: `escalation_email`,
`{escalation_tag} {one-line problem}`, and `assets/email-body.md` rendered in the person's
language. Inside the quoted arguments, backslash-escape `$`, `` ` `` and `"`.

Without code execution, use this pre-encoded link (cached from §0 — re-encode when §0 changes):

> `[➜ Open email DRAFT to your consultant (not sent yet)](mailto:federico.pacheco@fpshealth.com?subject=%5BEscalation%3A%20Team-AI%5D&body=Hi%2C%0A%0AI%27m%20stuck%20and%20I%27m%20handing%20this%20session%20over%20to%20you.%0AAttached%3A%20the%20handoff%20file%20%28goal%2C%20attempts%2C%20exact%20blocker%29%20and%20the%20file%20we%20created%20together.)`

**Step 4 — Guide the send.** Numbered points: (1) the link opens a ready-made email **draft** —
nothing is sent yet; (2) drag the handoff file and any file created here into it; (3) only when
a session export is confirmed above: run it — name the command — and drag the saved file in too;
(4) only **Send** sends. Then the link, as
`[➜ Open email DRAFT to your consultant (not sent yet)](<url>)`.

If the link doesn't open: plain email to `escalation_email`, subject
`{escalation_tag} {one-line problem}`, handoff file attached.
