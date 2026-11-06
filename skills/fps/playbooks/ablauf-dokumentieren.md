# Playbook: Ablauf dokumentieren (SOP or Prozessdokumentation)

One playbook for both. The depth follows the work: one person, one task = `sop`; several roles
or handoffs = `prozessdokumentation`. Both write the same two files: `document.json` (the core
facts, `schema/capture.schema.json`) and `capture.html` (the page around them).

1. **Frame.** Confirm the one task or process. Look for a draft: a `document.json` in the work
   folder, a published draft Artifact, or an old SOP or process document the person shares. If
   one exists, read it and run step 3 on it first, so you ask only what is open. Choose the depth
   and say which you chose.
2. **Interview.** Follow `reference/interview.md`. Describe what actually happens, not the ideal.
   Write every answer into `document.json` as you go. Ask for one real input file, one real
   output file and a screenshot at each key step.
3. **Check the core.** `python3 <skill-folder>/scripts/check.py document.json`. On exit 1, ask
   the listed questions one at a time, update `document.json`, and run it again until exit 0.
4. **Draw the picture.** Prozessdokumentation: write an editable draw.io swimlane,
   `ablauf.drawio`, next to `document.json`: one lane per role, one box per step with its number,
   one labelled arrow per handoff. Follow `reference/drawio-patterns.md`. Set `picture.drawio` to
   it. SOP: offer the same as a plain left-to-right flow; on yes, do the same.
5. **Write the page.** Copy `template/capture.html` to `capture.html` next to `document.json` and
   write it per `reference/page-contract.md`.
6. **Check the page.** `python3 <skill-folder>/scripts/check.py document.json capture.html`. It
   checks the diagram, writes the stamp and prints the `files` map. Fix and rerun until exit 0.
7. **Fresh review.** Start a fresh subagent with `reference/rubric-capture.md` as its brief and
   only the path of `capture.html`, never this chat. Sort its findings per
   `reference/interview.md` ("After the reader test"), then run step 6 again. At most two rounds.
   If no subagent can run, review the page yourself against the rubric, write both tables to
   `reader-test.md` next to the page, give the number of Blocking rows, and tell the person
   "Keine unabhängige Prüfung gelaufen". Never call the page reviewed without a real review.
8. **Publish.** Publish `capture.html` as one Artifact with the printed `files` map. Put the link
   in the Beitragsliste row of this capture (one row per capture). Share the Artifact with the
   consultant's email address (see the Hub for the sharing rule). If publishing fails, keep the
   files in the work folder and say so.
9. **Close.** Tell the person the link, the stamp (`vollständig` or `Entwurf` with N open
   questions), and who must answer which question. The document is build-ready only when
   `check.py --final document.json capture.html` exits 0: no open questions, a real screenshot,
   and real input and output files.

**Pause** at any step: see `reference/interview.md`.
