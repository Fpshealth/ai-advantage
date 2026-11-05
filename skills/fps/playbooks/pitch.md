# Playbook: Pitch (problem first)

The pitch is a brief for a decision-maker: the problem, today's work and the real files come
first, the idea last. It is two files: `brief.json` (the core facts, `schema/brief.schema.json`)
and `brief.html` (the page). One idea per brief. If the person has two, pick one with them and
offer a new chat for the other.

1. **Sharpen.** Run the `sharpen` skill on the person's idea. Use its four answers to find
   opportunities, to challenge today's process ("Muss dieser Schritt überhaupt sein?") and to
   develop a more ambitious solution. Show the sharpened version and let the person choose. The
   choice is theirs.
2. **Beitragsliste row.** Ask for the row's ID. If there is none, ask the person to add the row
   first (Typ `Projekt-Pitch`, Status `Entwurf`). Until then the ID is an open question.
3. **Today's process.** Find the capture of the work this idea changes: a link the person gives,
   a capture Artifact, or a `document.json` in the folder. Read it and take over the trigger,
   roles, systems, files, checks, numbers and its draw.io picture. Show what you took over and
   ask "Stimmt das so?". If no capture exists, offer to run `playbooks/ablauf-dokumentieren.md`
   first, and write the brief with `capture` as an open question if the person declines.
4. **Fill the core.** Write `brief.json` section by section, problem first. Each number keeps
   its source ("Team-Angabe", "aus der Ablauf-Doku", "Schätzung"). A number found in a document
   is shown for confirmation, not asked again. If the KPI does not measure the goal, propose a
   better one. Ask "Was würde fehlen, wenn diese Arbeit morgen wegfällt?". The idea is optional
   and stays a rough sketch.
5. **Check the core.** `python3 <skill-folder>/scripts/check.py brief.json`. Ask what it lists,
   one question at a time, and run it again until exit 0.
6. **Write the page.** Copy `template/capture.html` to `brief.html` and write it per
   `reference/page-contract.md` with the brief sections. Each section is one short paragraph,
   at most five sentences; the whole brief fits about two screens. The `visualizer` skill can
   draw the picture of today's process if the capture has none.
7. **Check the page.** `python3 <skill-folder>/scripts/check.py brief.json brief.html`. Fix and
   rerun until exit 0.
8. **Fresh review.** Start a fresh subagent with `reference/rubric-brief.md` as its brief and
   only the path of `brief.html`. At least one round, at most three questions back to the person
   per round. If no subagent can run, review it yourself against the rubric and say "Keine
   unabhängige Prüfung gelaufen".
9. **Publish and submit.** Publish `brief.html` as one Artifact with the printed `files` map, link
   it in the Beitragsliste row and share it with the consultant's email address. The status
   stays `entwurf` until `check.py --final brief.json brief.html` exits 0 (gates: evidence, a real
   input and output file, a real screenshot, no open questions). Then set `status` to
   `eingereicht`, rerun the check and update the row. The Geschäftsführung sets `genehmigt` or
   `abgelehnt` with a reason (`rejection_reason`).
10. **Close.** Give the link, the status, the open questions with who answers them, and what must
    happen before the brief can be submitted.
