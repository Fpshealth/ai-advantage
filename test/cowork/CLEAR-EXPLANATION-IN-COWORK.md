# Autonomous run — Clear Explanation: Team-AI in Cowork

One paste. Claude reports what the Cowork VM can run, then builds a short explainer. ~10 min.

**Setup:** sandbox set up (`Set up my workspace.`), `test/fixtures/*.csv` copied into `01_Input/`.

## Step 1 — Explicit start

Type `/` and pick **Clear Explanation**. Check: the skill does NOT start when you only write
"explain how the price import works" in a new chat without picking it.

## Step 2 — Paste as one message after picking the skill

```
Explain how the supplier price list in 01_Input/supplier-price-list-spring-2026.csv updates 01_Input/current-shop-export.csv, for a new colleague in purchasing. Treat my answers as "open" if you need any.

Before you start, and again at the end, write 03_Output/clear-explanation-test-report.md with one line per check, PASS or FAIL, quoting the evidence (the exact command and its last output lines):
1. python3 opened scripts/lint.py by path. Quote the command and the first error if it failed.
2. If 1 failed: piping the file via stdin worked. Quote the command.
3. uv is installed (`uv --version`), and Playwright imports (`python3 -c "import playwright"`).
4. lint.py ended with PASS on the final page. Quote the last 3 lines.
5. A fresh subagent did the cold read. Quote its verdict line.
6. The page, its images and inventory.md were built in 02_Work; the page and images are in 03_Output.
7. No step asked me to take a screenshot.
```

## Your part

Open the report. Lines 1–3 decide whether the "piped" fallback and the Playwright note are
ever needed in Cowork. Any FAIL in 4–7 → send the report to your consultant.
