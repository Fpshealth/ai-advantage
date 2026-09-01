---
type: llm
weight: 2
---

Pass if the final reply is written in German, tells the user that clicking the link opens an email
draft (Entwurf) with subject and body pre-filled, and that nothing is sent until they press Send
themselves. Fail if any user-facing sentence is in English, or if the reply implies the email has
already been sent, or if no link-click guidance is given.
