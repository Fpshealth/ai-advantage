---
type: regex
pattern: "hold all findings"
flags: i
match: not_contains
weight: 1
target:
  source: file
  path: fixture-skill/SKILL.md
---
