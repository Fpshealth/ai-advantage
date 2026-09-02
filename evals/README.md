# Eval suite for cowork-team-ai

Regression tests for the plugin's skills, run with Claude Code's built-in harness `claude plugin eval`
(early access — needs `CLAUDE_CODE_WALNUT_SPIRE=1` in the environment or `~/.claude/settings.json` → `env`;
without it the command prints "currently in early access" and runs nothing).

One folder per case: `case.yaml` (prompt + setup), optional `scaffold.sh` (builds the AI_SANDBOX layout
the skills expect), `graders/*.md` (one check per file). Results land in `results/<timestamp>/`
(gitignored): `report.html` for humans, `aggregate-result.json` for machines.

## Running

Shortest path — `evals/run.sh` sets the early-access switch for its own run and prints a PASS/FAIL summary:

```bash
evals/run.sh list                 # cases
evals/run.sh pilot escalation-de  # one case, one run, no baseline (after a skill edit)
evals/run.sh full                 # all cases, 3 runs, with/without → Δ (before a version bump)
evals/run.sh open                 # newest report.html
```

The underlying commands, for when you want the flags yourself. Cheap pilot (one case, one run, no baseline arm, ~1–2 min):

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
| `escalation-en` | escalation | Same blocker in English, `$` prices: `%2439.90` survives encoding; the handoff file has a Tools/Actions section and quotes SKU + both prices, both input files and the one-line problem (the old "cold read" as mechanical checks); English draft guidance | `mailto-subject-tag` |
| `escalation-static` | escalation | German, **no Bash granted** (tag `no-bash` → `run.sh` withholds it): the no-code rung must still yield the static SKILL.md link verbatim or a hand-encoded link with `enth%C3%A4lt`; `no-bash-called` proves Bash was really unavailable | `no-code-rung` — the static link exists only in the skill |

| `pruning-skills-behaviour` | pruning-skills | Planted fixture skill with one instance of each cut-on-sight smell plus three load-bearing lines: date stamp, IMP-005 reference, "hold all findings" line and OneDrive non-issue are cut from the file; EAN rule, purchase-price rule and `check_listing.py` survive; reply labels cuts by failure-mode name with a word-count delta | `report-labels` — the failure-mode vocabulary exists only in the skill |
First runs 2026-09-01, single arm, one run each: `de` 6/6 in 76 s · `en` 10/10 in 68 s · `static` 6/6 in 83 s.
Pilot 2026-09-02: `pruning-skills-behaviour` 9/9 in 101 s.
These three replace `test/claude-code/run.sh` (`de`, `en`, `static`); the old two-turn `en` is a single turn that states the
earlier turn's outcome as confirmed — `context.history_file` needs a real Claude Code session transcript, a written JSONL fails.

## Conventions

- Grade properties, not one means ("umlaut survives in the URL", not "static link used verbatim").
- Rulers before tasters: `regex`/`file_exists`/`tool_used` wherever a machine can decide; `llm` (weight 2) only for judgement.
- Every skill gets at least one gate check — a grader that fails when the skill's own guidance is removed.
- Checks that need a person mid-run (interactive slash commands, clicking the mail link) live in
  `../test/cowork/` as paste-prompt self-audits, not here.
- Case names stay stable so stored results line up; a case with Δ ≈ 0 over 3 runs is removed and noted here.
- A case's `allowed_tools` / `disallowed_tools` restrict nothing — whatever `--allow-tools` grants is callable. `run.sh` grants
  `Bash Write Edit` per case and withholds Bash for cases tagged `no-bash`; that is the only way to test the no-code rung.
- `target:` is accepted on `regex` graders only (`last_message` default, `trace`, `files`, `{source: file, path: <exact path>}` — no globs);
  an `llm` grader always judges the final reply. "Tool never called" = `tool_used` with `min: 0, max: 0`, never a regex over `trace`
  (the trace lists every available tool).
- Run cases one at a time (`run.sh` does): two runs started in the same second collide on `results/<timestamp>/`.
- `run.sh pilot|full` first runs the free structural checks `../test/check-references.sh` and `../test/check-mailto.sh`.
