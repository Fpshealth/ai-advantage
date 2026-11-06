---
type: llm
focus: trace
weight: 2
---

Find the last Write or Edit of document.json in the trace. Pass if it has depth
"prozessdokumentation", the three roles Kundenservice, Lager and Buchhaltung, at least two handoffs
each naming what is passed on and what comes back, and a process owner given as a role. Fail if any
of these is missing or a person's name is used instead of a role.
