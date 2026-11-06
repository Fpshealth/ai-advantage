# Interview

The person does the work every day; you know the schema (`schema/capture.schema.json`). Ask so that every core field gets a
real answer, an uploaded file, or an honest open question. Plan for about 45 minutes; a bigger
process may take longer, and the person may pause at any time.

**Before the first question.**
- One task or process per session. If the person names several, pick one with them and list
  the others under `candidates` (Prozessdokumentation) or tell them to start a new session.
- If the person shares an existing document, or a draft of this capture exists (a `document.json`
  in the work folder or a published draft Artifact), read it first, run `check.py` on it, and ask
  only what is still open. This is also how a paused capture resumes.
  List each source under `basis` (source, its date, what it covers) and mark contradictions
  (see below).
- Choose the depth from the first answers: one person, one task = `sop`; several roles or
  handoffs = `prozessdokumentation`. Say which you chose.

**Order.**
1. Frame: trigger, result, done check, "nicht für".
2. Walk-through: let the person tell the steps in their own order. If the first answer is
   under about three sentences, ask for a walk-through of the last real run. Ask about what
   actually happens, not what should happen. Park complaints and ideas until the walk-through
   is done.
3. Per step: the tool, the role, why, and "Woran merkst du, dass es geklappt hat?". If the step
   waits for something (a ticket, a mail, a time, another role), ask what it waits for and put it
   in `waits_for`: an automation hooks in at exactly that point. If Claude
   or a script runs a step, set `executor` to `claude` or `skript`; minutes are asked only for
   steps a person does. Where a
   system is opened, ask where and how (address, app, menu path) and who grants access. Never
   ask for passwords.
4. Files: ask for one real input file and one real output file, and screenshots where a step
   happens in a system. Read the layout (columns, fields, an example row) from the file
   yourself and ask the person only to confirm it. Do not ask the person to describe a layout.
5. Checks and problems. First derive field checks from each real file yourself (empty values,
   format such as digits or length, ranges such as price above cost, matches between files such
   as a key present in both) and list them under `checks`, marked in `inferred`. For each file
   that goes into a system, ask what else the import changes and whether one record can match
   several. Then ask: what is checked against what, right vs wrong, the last concrete
   incident and what they did, decisions.
6. What changes per run, what stays fixed, and the rules a solution must always respect (law,
   data protection, brand), asked once. "keine" with a reason is a valid answer.
7. Numbers: time per run, lead time, how often, the error rate of the process itself, and,
   where others deliver inputs, how often those inputs are faulty (`input_defect_rate`). Give
   the source of each number.
8. Outside parties (a supplier, an agency, another department), in both depths: at which step
   they get something, what, and what comes back (`external`).
9. Prozessdokumentation only: roles and handoffs (what is passed on, to whom, in which form:
   file, mail, ticket or verbal, and what comes back), what is already automated or was tried,
   the process owner (the role that decides about changes, not the document owner), for whom,
   and what would be missing if the process stopped. Then pain points.

**How to ask.**
- One question per message, in the person's language, in their words. Never name a method
  (SIPOC, DMAIC, value stream) and translate jargon.
- Push back once on a vague answer. If it stays vague, write what you have, mark the field
  `{"open": …, "ask": <Rolle>}` and move on.
- A fact only another role knows becomes an open question with `ask`. Do not make the person
  guess it.
- Every value you derived instead of heard goes into `inferred`.

**Contradictions.** Compare every source (documents, files, answers) yourself. Where two
disagree, record it under `conflicts` and ask one targeted question. Do not show the person the
comparison.

**Lookup tables.** Mappings, lists of codes or categories, sort orders, keyword lists, limits
and rename rules go into `reference`, so the builder gets them as checked data and not only as
page text. When a source document or script holds such a table, copy it in full, row by row.
Never shorten it to examples: a builder needs every row.

**Pause.** On "Pause", "Stopp" or "später": save `document.json` as it is, run `check.py`, write
the page and publish it as a draft Artifact if you can, and tell the person how many points are
still open. On return, read that draft and ask only those.

**After the reader test.** Sort every guess it returns:
- A page defect (the fact is in the core but unclear on the page): fix the page, no question.
- A fact the person knows: ask it, most blocking first.
- A fact another role knows: an open question with `ask`.
- A layout or value a file would show: ask for the file.
Ask the person only Blocking guesses they can answer in one line. Everything else stays on the
page as an open question.

**Close.** Give the person the link, the number of steps, checks and open questions, and who
must answer what. If publishing fails, keep `document.json` and the page in the work folder and
say so.

