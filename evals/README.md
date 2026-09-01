# Eval suite for cowork-team-ai

Regression tests for the plugin's skills, run with Claude Code's built-in harness `claude plugin eval`
(early access — needs `CLAUDE_CODE_WALNUT_SPIRE=1` in the environment or `~/.claude/settings.json` → `env`;
without it the command prints "currently in early access" and runs nothing).

One folder per case: `case.yaml` (prompt + setup), optional `scaffold.sh` (builds the AI_SANDBOX layout
the skills expect), `graders/*.md` (one check per file). Results land in `results/<timestamp>/`
(gitignored): `report.html` for humans, `aggregate-result.json` for machines.

## Running

Cheap pilot while editing a skill (one case, one run, no baseline arm, ~1–2 min):

```bash
claude plugin eval . --case escalation-de --runs 1 --ablation none --scaffold \
  --allow-tools Bash Write Edit --no-publish
```

Before a version bump (all cases, 3 runs, with/without baseline → read Δ):

```bash
claude plugin eval . --scaffold --allow-tools Bash Write Edit --judge-model sonnet --no-publish
```

- `--scaffold` is required for cases that have a `scaffold.sh`; it runs that script as you.
- `--allow-tools` is the operator grant for gated tools; a case's `allowed_tools` alone is not enough.
- `--judge-model` must differ from the model the case runs on (a model prefers its own output).
- Exit code 0 = every case at or above `--threshold` (default 1.0); 1 = something failed; 2 = cost cap hit.
- The `$` figures in reports are token estimates at API list price; on a Claude subscription they count
  against usage, not a card.

## Cases

| Case | Skill | What it proves | Gate check |
|---|---|---|---|
| `escalation-de` | escalation | German user stuck on a price update: handoff file written, mailto with correct subject tag, umlaut URL-encoded, never claims "sent", skill actually invoked, German draft guidance | `mailto-subject-tag` — only the skill supplies the tag |

First run 2026-09-01: 6/6 graders, 76 s, single arm.

## Conventions

- Grade properties, not one means ("umlaut survives in the URL", not "static link used verbatim").
- Rulers before tasters: `regex`/`file_exists`/`tool_used` wherever a machine can decide; `llm` (weight 2) only for judgement.
- Every skill gets at least one gate check — a grader that fails when the skill's own guidance is removed.
- Checks that need a person mid-run (interactive slash commands, clicking the mail link) live in
  `../test/cowork/` as paste-prompt self-audits, not here.
- Case names stay stable so stored results line up; a case with Δ ≈ 0 over 3 runs is removed and noted here.
