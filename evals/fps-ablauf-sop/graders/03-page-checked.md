---
type: llm
focus: trace
weight: 2
---

Pass if the trace shows a Bash call that ran check.py with TWO arguments (a document.json and an
HTML page) and that call's output starts with "GEPRÜFT: vollständig" or "GEPRÜFT: Entwurf". Fail if check.py was only run on
the JSON, or never passed with a page, or the agent edited the stamp in the page by hand.
