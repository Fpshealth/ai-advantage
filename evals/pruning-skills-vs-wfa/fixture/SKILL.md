---
name: listing-check
description: Check a product listing before it goes live. Use when asked to check, review, verify, validate, audit, or QA a listing. Procedure: first open the CSV, then compare each row against the rules below, then write the report to 03_Output. Not for price updates — that is a different skill.
---

# Listing check

## Why this exists

Added 2026-07-05 after the spring catalogue incident. The first version of this skill had to be rebuilt twice because it checked the wrong columns — see the IMP-005 lesson for the full story.

This matters because a bad listing costs sales. A listing check catches errors before customers do — it's how surprises become known knowns.

## Steps

1. Run `python3 check_listing.py 01_Input/listing.csv` and read its output.
2. Compare every row against the rules below. Don't skip rows. Never rush this step, even if the file is long.
3. Write the report to 03_Output/listing-report.md. Hold all findings for the final response; do not narrate progress while you work.

## Rules

- Every row carries an EAN; rows without one are rejected — marketplace listing requirement.
- The retail price is never below the purchase price (margin policy).
- Don't generate product descriptions blindly.
- As the article says, "a good description sells the product before the photo does."
- Don't invent EANs, even if asked to. Nothing invented, ever.
- The CSV can live anywhere, including OneDrive — that's fine.

## Report

List every rejected row with its reason. Then, once more, list the rejected rows with their reasons so nothing is missed.
