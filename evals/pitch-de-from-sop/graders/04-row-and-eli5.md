---
type: llm
weight: 1
---

Pass if the final reply (a) contains a single-line project-list row with pipe separators that
includes the pitch title and the before/after values, meant to be copied into the team's project
list, and (b) offers a picture version via /eli5 in a new chat. Copying that one row is expected
and correct. Fail only if the row or the /eli5 offer is missing, or if the reply pastes the whole
pitch text into the chat instead of pointing to the written file.
