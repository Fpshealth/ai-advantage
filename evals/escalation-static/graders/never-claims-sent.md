---
type: regex
pattern: "(E-?Mail|Mail) (wurde|ist) (gesendet|verschickt)|ich habe (?:(?!nicht)[^.!?\n])* (gesendet|verschickt)"
flags: i
match: not_contains
weight: 1
---
