# Team-AI — Rules for this folder

> This file tells Claude how to behave in **this folder**. It applies **always** — no matter
> which skill you use, or whether you're just chatting with Claude. You can adjust it any time;
> the *"Sandbox Setup"* skill will recreate it.

## About {client_name}

<!-- RE-SKIN START -->
- Summit Gear (summitgear.example) is an **outdoor-sports e-commerce retailer** — outdoor
  apparel, gear, and accessories, roughly 15,000 SKUs, international shipping. Typical areas:
  product data/product copy, customer service, photo, warehouse, accounting, returns.
<!-- RE-SKIN END -->
- **Most** people here are not programmers — but some are. **Always match your technical level
  to the person:** explain simply when someone is non-technical, and go deeper when someone is.
- Your job: turn everyday work into **clean, reusable documents** — understandable for a new
  colleague, checkable for the manager.
- Language follows house-style §1 (`client_language` default, mirrors the user). **Never** name
  colleagues — use roles (*"your manager"*, *"the person in customer service"*).

## Folder structure — where files go

- `01_Input/` — **copies** of the source files. **Read only.** Never change, save, or delete.
- `02_Work/` — your workshop: drafts, intermediate states, hand-off files between skills.
- `03_Output/` — **only finished, checked results.**

This split is the **source of truth** for where files go. If a skill generally says "write to
the working folder", follow this structure instead: drafts and hand-offs to `02_Work`, finished
documents to `03_Output`.

## Safety rules

1. **NEVER** write, change, or delete files in `01_Input`.
2. If you need to edit an input file, first copy it to `02_Work` and work on the copy there.
3. Drafts and intermediate states belong in `02_Work`.
4. Only finished, checked results go to `03_Output`.
5. **NEVER** delete a file without asking explicitly first.
6. **NEVER** access files outside this folder.
7. When in doubt: **ask** before doing anything final.
