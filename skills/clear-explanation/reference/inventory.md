# Inventory

`inventory.md` sits next to the page. `scripts/lint.py` checks its format.

## The inventory table

One table with these 7 columns, in this order:

| Column | The answer |
|---|---|
| Name | the one name the page uses for it, everywhere |
| Is | what it literally is: a file that holds X, a program that does Y, the person who decides Z |
| Made by, from | who or what creates or changes it, and from which input |
| Current | what starts a change (a person running something, a schedule, another system) |
| Lives | where it is |
| Status | exists, planned, unknown, or open |
| Source | the file and line, document or person the row comes from, as a link where it has one |

Status says only whether the thing exists; a fact about today, such as "23 MB" or "never", goes in Is or Current. An empty cell is a lookup to do now. When the sources have no answer, write "open" and the question; the page states it at that point ("The repo does not record at what time of day.").

In the HTML, wrap the first definition of each Name in `<dfn>`, with the same words as the Name cell. Each `<dfn>` is an inventory Name, and each Name gets one `<dfn>`. Keep the category name a definition gave something (a "session record", a "fixture"); a new word for it later makes the reader ask if it is a new thing.

## The picture plan

Under the inventory, a second table `| Section | Kind | Caption or reason |`: one row per `<h2>`, with the heading text exactly. Kinds:

- **screenshot**: a real screen the reader will see or click
- **real output**: a file listing, a log, a value as the system prints it
- **diagram**: where things live, what flows where, or what differs between options
- **animation**: an order over time, or one change that moves through stages
- **none**: with the reason a sentence says it as fast. "I cannot capture it" is not a reason.

The caption is the one thing the reader must remember from the picture.

## Sources as links

Make every source a link the reader can open in one step:

- a web page: its URL
- a document in SharePoint, OneDrive or another connected source: its share URL
- a file in the input area: its relative path, for example `01_Input/price-list.csv`

Also write the file name as visible text, because the reader may not have access to the link. A person stays plain text, by role (house style §2). A meeting stays plain text with its date.
