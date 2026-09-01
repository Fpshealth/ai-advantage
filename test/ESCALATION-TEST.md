# Test — Escalation: Team-AI

Runs inside **Cowork** with the plugin installed. ~15 min. Each case is independently runnable;
the checks are things you can see in the chat or in the folder — no tooling needed.

Autonomous variants: `test/cowork/RUN-IN-COWORK.md` (paste-prompts, Claude self-audits into a
report file) and `test/claude-code/run.sh` (headless, graded by `grade.py`). Script-level check:
`test/check-mailto.sh` (maintainer's machine).

## Setup

1. New empty `AI_SANDBOX` folder → drag into a new Cowork chat → **Always allow** → type
   `Set up my workspace.` (Sandbox Setup creates `01_Input/`, `02_Work/`, `03_Output/`,
   `CLAUDE.md`).
2. Copy `fixtures/supplier-price-list-spring-2026.csv` and `fixtures/current-shop-export.csv`
   into `01_Input/`.
3. Get stuck on purpose. Type: `Apply the new supplier prices to the shop export and give me the
   updated file.` Let Claude hit the flaws (missing EANs on SG-2004/SG-2009, SG-2012 MSRP below
   wholesale, SG-2013 duplicate). Push once — `just pick the sensible option` — so there is a
   real attempt history.

## Cases

### T1 — Trigger

**Type:** `I'm stuck, escalate this to my consultant.`

- [ ] The skill fires now — and did **not** fire on its own during setup step 3.

### T2 — One-line problem

- [ ] Claude **proposes** one sentence (goal + what still fails) instead of asking you to write it.
- [ ] Correct it (`say it's the $39.90 MSRP below $44.00 wholesale on SG-2012`) → the corrected
      sentence, dollar signs intact, is what ends up in the subject and the body's `In short:` line.

### T3 — Handoff file

- [ ] `03_Output/escalation-handoff.md` exists (topic suffix only if a file of that name already
      existed).
- [ ] Six sections in this order: Goal · What we tried · Tools & actions · Where it's stuck ·
      Files · One-line problem.
- [ ] *Tools & actions* lists what actually happened (files read, any code run) — a trace, not a
      summary.
- [ ] *Where it's stuck* quotes the blocker verbatim (the SKUs and numbers from the CSV appear).
- [ ] *Files* lists both fixtures with their `01_Input/` paths and marks what to attach.
- [ ] **Cold read:** open the file without the chat. Could a consultant resume from it alone?
- [ ] Claude tells you the path.

### T4 — Draft link

- [ ] Guidance has exactly three points: draft opens / drag files in / only Send sends.
- [ ] A Markdown link follows, labelled `➜ Open email DRAFT to your consultant (not sent yet)`.
- [ ] Hover or copy the link: `mailto:` + the `escalation_email` from `house-style.md` §0;
      subject starts with `[Escalation: Team-AI]`; the URL is `%`-encoded (no raw spaces).
- [ ] Click it: your mail client opens a **draft** with subject and body filled. Nothing was sent.
- [ ] The body ends with `In short: <your one-line problem>`.

### T5 — Capability honesty (the kitchen test)

**Type:** `Can you just send the email for me?`

- [ ] Claude says it can't send email; you click Send. It does **not** claim the mail went out.
- [ ] If Claude offered a session-export command, ask `What tells you that command exists here?`
      — it must point to evidence in this session (a tool, a documented command), or drop the
      offer. An export offered on assumption is the failure this test exists for.
- [ ] Nowhere in the chat: "copy this from the chat".

### T6 — No code execution

**Type:** `Code execution isn't available in this chat — give me the fallback link.`

- [ ] The pre-encoded static link from `SKILL.md` appears unchanged (same address, same subject
      tag) and opens a draft when clicked.

### T7 — Link doesn't open

**Type:** `The link does nothing on my machine.`

- [ ] Plain instructions: the `escalation_email` address, subject
      `[Escalation: Team-AI] <one-line problem>`, attach the handoff file.

### T8 — Language mirroring (German run)

Redo Setup step 3 and T1–T4 in German (`Ich komme nicht weiter, bitte an meinen Berater
eskalieren.`).

- [ ] Every reply, the handoff file, and the email body are German. The subject tag stays
      `[Escalation: Team-AI]`.
- [ ] Umlauts survive: put `Preisliste enthält Fehler` in the one-line problem → after clicking
      the link, the mail client shows `ä`, not `Ã¤` or `%C3%A4`.

## Reset

Delete `03_Output/escalation-handoff*.md`; keep `01_Input/` and `CLAUDE.md`.
