---
type: llm
focus: trace
weight: 2
---

Find the Write (or Edit) tool call that produced the pitch-*.md file and judge its content. Pass if
the file contains, in this order, headings or bold labels matching the six fixed German questions:
"Was ist die Idee des Projekts", "Was bezwecke ich damit", "Was ist das Ziel", "Welchen Impact hat
das Resultat", "Welche Systeme sind involviert", "Wer wird oder soll das Projekt realisieren" — and
every answer is at most five sentences. Fail if a question is missing, reordered, or any answer
runs longer than five sentences.
