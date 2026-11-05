# Page contract

This contract covers both pages: `capture.html` (core in `document.json`, template
`template/capture.html`) and `brief.html` (core in `brief.json`, template `template/brief.html`).
The page is in the person's language and written for a reader who never saw the interview. Its layout, headings, order and length are
yours. Explain the why, give the context the person told you, and connect the steps. These rules
are fixed:

1. **Every core fact is on the page, word for word.** Copy each text value from `document.json`
   exactly. You may add sentences before and after it, but do not reword it. If the wording is
   wrong, change `document.json` first.
2. **Every core fact sits inside its marker.** Put `data-core="<path>"` on the element that holds
   the fact. The path uses the JSON keys, joined with dots; list positions count from 1:
   `trigger`, `metrics.lead_time`, `steps.3.why`, `checks.2.wrong`, `files.outputs.1.path`.
   A marker also covers everything below it, so one `data-core="steps.3"` on a step card covers
   that step's action, why, tool and so on, if their texts are inside the card. One element can
   carry several paths, separated by spaces.
   - Every text value counts, also `date`, `source`, `please_confirm`, and each file's `path`
     and `description`.
   - An open question (`{"open": …}`) is a fact. Show its question, `reason` and `ask` (who
     answers) at the place where the fact belongs, for example in the step. List every open
     question again in the section `offen` (brief: `offen`), the ones that block the build first.
     `check.py` fails the page otherwise.
   - One gap, one open question. If several fields lack the same fact, ask it once and let the
     other fields point to that question.
   - A number value (`{"value": 12, …}`) needs its number, note and source inside the marker.
   - Text in hidden markup (`hidden`, `aria-hidden="true"`, `display:none`, `<script>`) does
     not count. The reader must see every fact.
   - A real screenshot or a file preview is an `<img>` whose `src` is the file from
     `document.json`, inside the marker of that screenshot or file.
   - Choice fields (`depth`, `kind`, `status`, `mode`, `estimate`) and step numbers need no
     marker. Show them in words where they help.
3. **Use the fixed sections, in this order.** Every capture has these sections (a brief has the
   sections in `template/brief.html`), each as
   `<section data-section="<id>">` with its heading, in this order. A builder or colleague
   always finds each part in the same place. Inside a section, length, prose or tables, and
   pictures are yours.

   | id | Heading |
   |---|---|
   | `kurz` | Kurz gesagt |
   | `rahmen` | Wann, was, wann fertig |
   | `systeme` | Systeme und Zugang |
   | `vorbereiten` | Vorher bereitlegen |
   | `rollen` | Rollen und Übergaben (only in a Prozessdokumentation) |
   | `schritte` | Schritte |
   | `pruefen` | Prüfschritte |
   | `probleme` | Wenn etwas schiefgeht |
   | `dateien` | Echte Dateien |
   | `zahlen` | Zahlen und Aufwand |
   | `offen` | Noch offen |

4. **Show what Claude inferred.** Every path listed in `inferred` is a fact Claude derived and
   nobody said. Its marker must also contain the word "abgeleitet", so the reader knows to
   confirm it.
5. **Leave the stamp slot alone.** The template has `<!--stamp-->…<!--/stamp-->`. Only `check.py`
   writes it: green "Geprüft: vollständig · baufertig" (no open question), amber "Geprüft: Entwurf
   · N Fragen offen", or a red list of what is missing.
6. **Show the picture.** If the document has a draw.io file (`picture.drawio` or `today.diagram`),
   draw the same boxes and lanes on the page as an inline `<svg>` inside `data-core="picture"`
   (brief: `data-core="today.diagram"`) and link the `.drawio` file there, so the reader can open
   and edit it. `check.py` checks the file and adds it to the `files` map.
7. **Brief pages** use the brief sections from `template/brief.html`, problem first. Each section
   is one short paragraph, at most five sentences; the whole brief fits about two screens.
