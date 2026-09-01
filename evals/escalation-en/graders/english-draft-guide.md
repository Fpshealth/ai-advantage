---
type: llm
weight: 2
---

Pass if the final reply is written in English, tells the user that clicking the link opens an email
draft with subject and body pre-filled, and that nothing is sent until they press Send themselves.
Fail if user-facing sentences are in another language, if the reply implies the email has already
been sent, or if no link-click guidance is given.
