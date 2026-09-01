#!/usr/bin/env bash
# One-command entry to the plugin's eval suite. Sets the early-access switch for this run only
# (no settings change needed) and prints a PASS/FAIL summary at the end.
#
#   evals/run.sh list                  cases in this suite
#   evals/run.sh pilot <case>          one case, one run, no baseline arm  (~1-2 min)  — after editing a skill
#   evals/run.sh full [case-glob]      every case (or matching), 3 runs, with/without baseline → Δ — before a version bump
#   evals/run.sh open                  open the newest report.html
# pilot/full first run the free structural checks (test/check-references.sh, test/check-mailto.sh).
# Run cases one at a time: two runs started in the same second collide on results/<timestamp>/.
#
# Extra flags after the mode are passed straight to `claude plugin eval` (e.g. --runs 2).
set -uo pipefail
cd "$(dirname "$0")/.."
export CLAUDE_CODE_WALNUT_SPIRE=1
COMMON=(--scaffold --no-publish)
# Operator grant per case: the case's own allowed_tools/disallowed_tools do NOT restrict anything —
# a tool granted here is callable. A case tagged `no-bash` in case.yaml gets no Bash (the no-code rung).
grant() { if grep -q "no-bash" "evals/$1/case.yaml" 2>/dev/null; then echo "Write Edit"; else echo "Bash Write Edit"; fi; }
cases() { for d in evals/*/; do if [ -f "$d/case.yaml" ] || [ -f "$d/prompt.md" ]; then basename "$d"; fi; done; }
mode=${1:-help}; shift || true

pregate() {  # free structural checks before any paid run
  local ok=0
  for chk in test/check-references.sh test/check-mailto.sh; do bash "$chk" || ok=1; done
  [ "$ok" -eq 0 ] || { echo "pre-gate failed — fix before spending a run"; exit 1; }
}

summarize() {  # $1 = json path
python3 - "$1" <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
print(f"\n== {d['durationSeconds']} s · est. ${d['costUsd']:.2f} usage · claude {d['claudeVersion']} ==")
worst = 1.0
if not d["cases"]:
    print("RESULT: NO CASES LOADED — see the error above"); sys.exit(1)
for c in d["cases"]:
    arms = c["arms"]
    for arm, runs in arms.items():
        if not runs: continue
        scores = [r["score"] for r in runs]
        avg = sum(scores) / len(scores)
        if arm == "with": worst = min(worst, avg)
        print(f"{c['name']:<28} {arm:<8} score {avg:.2f}  ({len(runs)} run{'s' if len(runs)!=1 else ''})")
        for r in runs:
            for g in r["graders"]:
                if not g["passed"] and g.get("scored", True):
                    print(f"    FAIL {g['name']}: {g.get('explanation','')[:110]}")
    w = arms.get("with", []); wo = arms.get("without", [])
    if w and wo:
        delta = sum(r["score"] for r in w)/len(w) - sum(r["score"] for r in wo)/len(wo)
        print(f"{'':<28} Δ (with − without) = {delta:+.2f}")
print("RESULT:", "ALL PASS" if worst >= 1.0 else "FAILURES — open the report")
PY
}

case "$mode" in
  list)
    cases ;;
  pilot)
    c=${1:?usage: evals/run.sh pilot <case>}; shift
    pregate
    out="evals/results/pilot-$c-$(date +%Y%m%d-%H%M%S).json"
    claude plugin eval . --case "$c" --runs 1 --ablation none "${COMMON[@]}" --allow-tools $(grant "$c") --json "$out" "$@"
    rc=$?; [ -f "$out" ] && summarize "$out"; exit $rc ;;
  full)
    glob=${1:-}; [ -n "$glob" ] && shift
    pregate
    rc=0  # one invocation per case: per-case tool grant, and no results/<timestamp>/ collision
    for c in $(cases); do
      [ -n "$glob" ] && [[ "$c" != $glob ]] && continue
      out="evals/results/full-$c-$(date +%Y%m%d-%H%M%S).json"
      claude plugin eval . --case "$c" --ablation with-without --judge-model sonnet "${COMMON[@]}" --allow-tools $(grant "$c") --json "$out" "$@" || rc=1
      [ -f "$out" ] && summarize "$out"
    done
    exit $rc ;;
  open)
    r=$(ls -t evals/results/*/report.html 2>/dev/null | head -1)
    [ -n "$r" ] && open "$r" && echo "$r" || echo "no report yet" ;;
  *)
    sed -n '2,10p' "$0" ;;
esac
