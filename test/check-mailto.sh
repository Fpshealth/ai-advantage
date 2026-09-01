#!/usr/bin/env bash
# Script-level check for skills/escalation/scripts/mailto_link.py. Run from anywhere; no arguments.
#   1. Same output by path and via stdin (the Cowork heredoc form).
#   2. Umlauts and newlines are %-encoded and round-trip.
#   3. The static fallback link in SKILL.md still matches escalation_email in house-style §0.
set -euo pipefail
cd "$(dirname "$0")/.."
script=skills/escalation/scripts/mailto_link.py
addr="a@b.c"; subj="[Escalation: Team-AI] Preisliste enthält Fehler"; body=$'Hallo,\n\nÜbergabe.'
by_path=$(python3 "$script" "$addr" "$subj" "$body")
by_stdin=$(python3 - "$addr" "$subj" "$body" < "$script")
fail=0
[ "$by_path" = "$by_stdin" ] || { echo "FAIL path/stdin output differs"; fail=1; }
case "$by_path" in
  "mailto:a@b.c?subject=%5BEscalation%3A%20Team-AI%5D%20Preisliste%20enth%C3%A4lt%20Fehler&body=Hallo%2C%0A%0A%C3%9Cbergabe.") ;;
  *) echo "FAIL unexpected encoding: $by_path"; fail=1 ;;
esac
email=$(grep -o '`escalation_email` | `[^`]*`' reference/house-style.md | sed 's/.*| `//; s/`$//')
grep -q "mailto:$email?" skills/escalation/SKILL.md || { echo "FAIL static link address != escalation_email ($email)"; fail=1; }
dollar=$(python3 "$script" "$addr" 'MSRP $39.90' 'x')
[ "$dollar" = "mailto:a@b.c?subject=MSRP%20%2439.90&body=x" ] || { echo "FAIL dollar sign lost: $dollar"; fail=1; }
[ "$fail" -eq 0 ] && echo "OK — mailto_link.py encodes correctly; static link matches §0."
exit "$fail"
