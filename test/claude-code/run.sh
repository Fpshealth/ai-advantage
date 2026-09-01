#!/usr/bin/env bash
# Autonomous Claude Code test for skills/escalation. Run from anywhere; optional args select cases
# (default: all three), e.g. `run.sh en static`.
# Needs: claude CLI logged in. Costs a few API calls. Sandboxes live under $ESCALATION_TEST_DIR
# (default: a fresh mktemp dir) and are kept for inspection.
#   en     two turns: attempt the price update, then escalate (tests $-escaping, /export route, cold read)
#   de     one turn, German (tests language mirroring, umlaut encoding)
#   static one turn, German, Bash disallowed (tests the no-code rung: static link, or a hand-encoded
#          link whose umlaut survives)
set -uo pipefail
cd "$(dirname "$0")/../.."
REPO=$PWD
WORK=${ESCALATION_TEST_DIR:-$(mktemp -d "${TMPDIR:-/tmp}/escalation-test.XXXX")}
FLAGS=(--plugin-dir "$REPO" --output-format json --dangerously-skip-permissions --max-turns 40)

mk_sandbox() {
  local d="$WORK/$1"; mkdir -p "$d/01_Input" "$d/02_Work" "$d/03_Output"
  cp test/fixtures/*.csv "$d/01_Input/"
  cp skills/sandbox-setup/reference/sandbox-claude-template.md "$d/CLAUDE.md"
  echo "$d"
}
# run <sandbox> <outfile-base> [claude args...] <prompt>  → prints session_id
# The prompt goes in via stdin: variadic flags like --disallowedTools would swallow a trailing argument.
run() {
  local d=$1 out=$2; shift 2
  local prompt=${@: -1}; set -- "${@:1:$#-1}"
  (cd "$d" && printf '%s' "$prompt" | claude -p "${FLAGS[@]}" "$@" > "$out.json" 2> "$out.err")
  python3 - "$out" <<'PY'
import json, sys
p = sys.argv[1]
try:
    d = json.load(open(p + ".json"))
except Exception as e:
    open(p + ".txt", "w").write(""); print(""); sys.exit(0)
open(p + ".txt", "w").write(d.get("result", ""))
print(d.get("session_id", ""))
PY
}

fail=0
CASES=${*:-en de static}
want() { case " $CASES " in *" $1 "*) return 0;; *) return 1;; esac; }

want en && {
echo "== en (two turns) =="
d=$(mk_sandbox en)
sid=$(run "$d" "$WORK/en-1" "Apply the new supplier prices from 01_Input/supplier-price-list-spring-2026.csv to 01_Input/current-shop-export.csv and give me the updated file in 03_Output. If something in the data is inconsistent, pick the sensible option and continue.")
run "$d" "$WORK/en-2" --resume "$sid" "I'm stuck, escalate this to my consultant. Non-interactive run (I will resume this Claude Code session interactively afterwards): use exactly this one-line problem and treat it as confirmed: The \$39.90 MSRP is below the \$44.00 wholesale on SG-2012 - which price wins?" > /dev/null
python3 test/claude-code/grade.py en "$d" "$WORK/en-2.txt" || fail=1
}

want de && {
echo "== de (one turn) =="
d=$(mk_sandbox de)
run "$d" "$WORK/de" "Ich wollte die neuen Lieferantenpreise aus 01_Input/supplier-price-list-spring-2026.csv in 01_Input/current-shop-export.csv übernehmen, aber die Preisliste enthält Fehler (SG-2012: UVP 39,90 unter Einkaufspreis 44,00; SG-2013 doppelt; SG-2004 und SG-2009 ohne EAN). Ich komme nicht weiter, bitte an meinen Berater eskalieren. Nicht-interaktiver Lauf: verwende genau diesen Einzeiler als bestätigt: Die Preisliste enthält Fehler bei SG-2012, die ich nicht selbst entscheiden kann." > /dev/null
python3 test/claude-code/grade.py de "$d" "$WORK/de.txt" || fail=1
}

want static && {
echo "== static (German, Bash disallowed) =="
d=$(mk_sandbox static)
run "$d" "$WORK/static" --disallowedTools Bash "Ich wollte die Lieferantenpreise aus 01_Input/supplier-price-list-spring-2026.csv in 01_Input/current-shop-export.csv übernehmen, aber die Preisliste enthält Fehler (SG-2012: UVP 39,90 unter Einkaufspreis 44,00; SG-2013 doppelt; SG-2004 und SG-2009 ohne EAN). Ich komme nicht weiter, bitte an meinen Berater eskalieren. Nicht-interaktiver Lauf: verwende genau diesen Einzeiler als bestätigt: Die Preisliste enthält Fehler bei SG-2012, die ich nicht selbst entscheiden kann." > /dev/null
python3 test/claude-code/grade.py static "$d" "$WORK/static.txt" || fail=1
}

echo; echo "Sandboxes and transcripts: $WORK"
[ "$fail" -eq 0 ] && echo "ALL PASS" || echo "FAILURES — see above"
exit "$fail"
