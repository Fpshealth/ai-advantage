---
type: llm
weight: 2
---

Pass if the final reply (a) lists the cuts it made and labels each with a failure-mode name such as
sediment, no-op, duplication, negation, defense-without-evidence, raised-non-issue or description-bloat,
and (b) states the word count before and after the edit. Fail if cuts are described without such labels,
or if no before/after word count appears.
