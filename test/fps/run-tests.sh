#!/usr/bin/env bash
# Tests for skills/fps/scripts/check.py: core check and page check.
# Run from anywhere; no arguments. PYTHON=python3.9 picks the interpreter.
set -uo pipefail

ROOT=$(cd "$(dirname "$0")/../.." && pwd)
SKILL="$ROOT/skills/fps"
CHECK="$SKILL/scripts/check.py"
PY=${PYTHON:-python3}
T=$(mktemp -d)
trap 'rm -rf "$T"' EXIT
pass=0
fail=0

ok() { echo "PASS $1"; pass=$((pass + 1)); }
bad() { echo "FAIL $1: $2"; fail=$((fail + 1)); }

# expect <name> <exit code> <text in output or empty> <check.py args...>
expect() {
  local name=$1 code=$2 want=$3
  shift 3
  "$PY" "$CHECK" "$@" >"$T/out" 2>&1
  local got=$?
  if [ "$got" != "$code" ]; then
    bad "$name" "exit $got, expected $code"; sed 's/^/    /' "$T/out" | head -12; return
  fi
  if [ -n "$want" ] && ! grep -qF -- "$want" "$T/out"; then
    bad "$name" "output lacks: $want"; sed 's/^/    /' "$T/out" | head -12; return
  fi
  ok "$name"
}

# has <name> <file> <text> [count]: the file contains the text (exactly count times, if given)
has() {
  local n
  n=$(grep -oF -- "$3" "$2" | wc -l | tr -d ' ')
  if [ "$n" = 0 ] || { [ -n "${4:-}" ] && [ "$n" != "$4" ]; }; then
    bad "$1" "$(basename "$2") has \"$3\" $n times"
  else
    ok "$1"
  fi
}

lacks() {
  if grep -qF -- "$3" "$2"; then bad "$1" "$(basename "$2") still has \"$3\""; else ok "$1"; fi
}

# Fixtures: the generic SOP and Prozessdokumentation in test/fps/fixtures, already schema v2.
# Every case runs on a copy in a temp folder, because check.py writes the stamp into the page.
# gen.py builds a page from the starter template with every value in plain markers, one marker
# per list item and per other top-level key, each inside a fixed section. It is written without
# check.py, so it tests check.py.
FIX="$ROOT/test/fps/fixtures"

cat >"$T/gen.py" <<'EOF'
import html, json, re, sys
doc = json.load(open(sys.argv[1], encoding="utf-8"))
SECTION = {}
for sid, keys in {
    "kurz": "title summary highlight basis owner date purpose process_owner not_for",
    "rahmen": "trigger result done_check sharepoint_folder",
    "systeme": "systems security",
    "vorbereiten": "prepare",
    "rollen": "roles handoffs",
    "schritte": "steps picture decisions",
    "pruefen": "checks",
    "probleme": "exceptions help last_incident pain_points",
    "dateien": "files screenshots",
    "zahlen": "metrics variation automated_or_tried candidates",
    "offen": "open_points terms",
}.items():
    for k in keys.split():
        SECTION[k] = sid
bodies = {}
out = None
def leaves(v, path):
    if isinstance(v, dict):
        for k, x in v.items():
            leaves(x, path + [k])
    elif isinstance(v, list):
        for i, x in enumerate(v, 1):
            leaves(x, path + [str(i)])
    elif not isinstance(v, bool):
        p = ".".join(path)
        real = path[0] == "screenshots" and path[-1] == "file" and doc["screenshots"][int(path[1]) - 1]["kind"] == "echt"
        if real or path[-1] == "preview":
            out.append('<img data-leaf="%s" src="%s" alt="">' % (p, html.escape(v)))
        else:
            out.append('<p data-leaf="%s">%s</p>' % (p, html.escape(str(v))))
for key, v in doc.items():
    if key == "inferred":
        continue
    out = bodies.setdefault(SECTION.get(key, "kurz"), [])
    for i, item in (enumerate(v, 1) if isinstance(v, list) else [(None, v)]):
        p = key if i is None else "%s.%d" % (key, i)
        out.append('<div data-core="%s">' % p)
        leaves(item, p.split("."))
        if any(q == p or q.startswith(p + ".") for q in doc.get("inferred", [])):
            out.append("<em>abgeleitet</em>")
        out.append("</div>")
page = open(sys.argv[2], encoding="utf-8").read()
if doc["depth"] == "sop":
    page = re.sub(r'<!--[^>]*-->\s*<section data-section="rollen">.*?</section>\s*', "", page, flags=re.S)
page = re.sub(r'(<section data-section="(\w+)">.*?)(</section>)',
              lambda m: m.group(1) + "\n".join(bodies.get(m.group(2), [])) + m.group(3), page, flags=re.S)
open(sys.argv[3], "w", encoding="utf-8").write(page)
EOF

for ex in sop prozessdoku; do
  cp -R "$FIX/$ex" "$T/$ex"
  "$PY" "$T/gen.py" "$T/$ex/document.json" "$SKILL/template/capture.html" "$T/$ex/full.html"
done
SOP="$T/sop"
PD="$T/prozessdoku"
page() { [ "$1" = full ] || cp "$SOP/full.html" "$SOP/$1.html"; [ $# -lt 2 ] || perl -CSD -i -ne "$2" "$SOP/$1.html"; echo "$SOP/$1.html"; }

expect "core: SOP passes" 0 "GEPRÜFT: vollständig" "$SOP/document.json"
expect "core: Prozessdoku passes" 0 "GEPRÜFT: vollständig" "$PD/document.json"
expect "core: known-bad capture fails" 1 "NICHT VOLLSTÄNDIG" "$FIX/known-bad.json"
expect "core: known-bad capture names the dash cell" 1 "Auslöser: ist leer oder nur „–“." "$FIX/known-bad.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["trigger"]=""; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/empty.json"
expect "core: emptied required field fails" 1 "Auslöser: ist leer" "$SOP/empty.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["screenshots"]=[]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/noshots.json"
expect "core: zero screenshots fails" 1 "Screenshots: es gibt keinen Screenshot" "$SOP/noshots.json"
expect "usage: no arguments" 2 "Aufruf"
expect "usage: page file missing" 2 "Aufruf" "$SOP/document.json" "$SOP/nope.html"

expect "page: full SOP passes" 0 "GEPRÜFT: vollständig" "$SOP/document.json" "$(page full)"
has "page: files map has document.json" "$T/out" "\"document.json\": \"$SOP/document.json\""
has "page: files map has the real screenshot" "$T/out" "\"img/03-preise.png\": \"$SOP/img/03-preise.png\""
has "page: green stamp written once" "$SOP/full.html" 'class="stamp ok"><b>Geprüft: vollständig</b> ' 1
has "page: green stamp counts open questions" "$SOP/full.html" 'Fragen offen · Schema v2 · ' 1
expect "page: full Prozessdoku passes" 0 "\"img/02-retoure.png\"" "$PD/document.json" "$PD/full.html"

expect "page: missing why of one step fails" 1 "Seite › Schritt 3 › Warum: fehlt auf der Seite oder steht nicht wörtlich im Marker data-core=\"steps.3.why\"." \
  "$SOP/document.json" "$(page nowhy 'print unless /data-leaf="steps\.3\.why"/')"
has "page: red stamp lists the missing why" "$SOP/nowhy.html" "Schritt 3 › Warum"
has "page: red stamp written once" "$SOP/nowhy.html" 'class="stamp bad"><b>Nicht vollständig</b><ol><li>' 1
expect "page: missing why of steps 1-3 is one line" 1 "Seite › Schritte 1–3 › Warum: fehlt auf der Seite oder steht nicht wörtlich im Marker data-core=\"steps.<Nr>.why\"." \
  "$SOP/document.json" "$(page nowhy3 'print unless /data-leaf="steps\.[123]\.why"/')"
expect "page: reworded value fails" 1 "Seite › Auslöser: fehlt auf der Seite" \
  "$SOP/document.json" "$(page reword 's/(data-leaf="trigger">)\S+/$1Irgendwann/; print')"
expect "page: marker typo fails" 1 "den Marker data-core=\"triger\" gibt es in document.json nicht" \
  "$SOP/document.json" "$(page typo 's/data-core="trigger"/data-core="triger"/; print')"
expect "page: missing real screenshot fails" 1 "Seite › Screenshot 3 › Datei: das Bild „img/03-preise.png“ fehlt" \
  "$SOP/document.json" "$(page noimg 'print unless /src="img\/03-preise\.png"/')"
expect "page: img file not next to the page fails" 1 "das Bild „img/fehlt.jpg“ gibt es nicht" \
  "$SOP/document.json" "$(page ghost 's/<main>/<main><img src="img\/fehlt.jpg" alt="">/; print')"
expect "page: steps.1 does not cover steps.10" 1 "Seite › Schritt 10 › Was du tust" \
  "$SOP/document.json" "$(page ten 's/data-core="steps\.10"/data-core="steps.1"/; print')"
expect "page: text inside <script> does not count" 1 "Seite › Auslöser: fehlt" \
  "$SOP/document.json" "$(page script 's/<p (data-leaf="trigger">.*)<\/p>/<script>$1<\/script>/; print')"
expect "page: a fact in a hidden element does not count" 1 "Seite › Auslöser: fehlt" \
  "$SOP/document.json" "$(page hid 's/<div data-core="trigger">/<div hidden><div data-core="trigger">/; s/(data-core="trigger">.*?<\/div>)/$1<\/div>/; print')"
expect "page: a fact under display:none does not count" 1 "Seite › Auslöser: fehlt" \
  "$SOP/document.json" "$(page dnone 's/<div data-core="trigger">/<div data-core="trigger" style="display: none">/; print')"
expect "page: entities, nbsp, plain quotes and case pass" 0 "GEPRÜFT: vollständig" \
  "$SOP/document.json" "$(page typo2 'if (/^<p /) { s/(?<=>)([^<]*)/my $t = uc $1; $t =~ s{ }{&nbsp;}g; $t =~ s{[\x{201E}\x{201C}]}{&quot;}g; $t =~ s{\x{2013}}{&ndash;}g; $t/e } print')"
expect "page: a marker on the img itself counts" 0 "GEPRÜFT: vollständig" \
  "$SOP/document.json" "$(page selfimg 's/data-core="screenshots\.3"/data-core="screenshots.3.caption"/; s/data-leaf="screenshots\.3\.file"/data-core="screenshots.3.file"/; print')"
expect "page: text after an img marker does not count" 1 "Seite › Auslöser: fehlt" \
  "$SOP/document.json" "$(page afterimg 's/<div data-core="trigger">/<div><img data-core="trigger" src="img\/03-preise.png" alt="">/; print')"
expect "page: a fact inside the stamp slot does not count" 1 "Seite › Auslöser: fehlt" \
  "$SOP/document.json" "$(page instamp 's/<!--stamp-->.*?<!--\/stamp-->//; s/<p (data-leaf="trigger">.*)<\/p>/<!--stamp--><p $1<\/p><!--\/stamp-->/; print')"
expect "page: missing stamp slot fails" 1 "Stempel-Platz" \
  "$SOP/document.json" "$(page nostamp 's/<!--stamp-->.*?<!--\/stamp-->//; print')"

flip=$(page flip 's/data-core="trigger"/data-core="trigger-x"/; print')
expect "stamp: broken page gets red" 1 "" "$SOP/document.json" "$flip"
has "stamp: red after fail" "$flip" 'class="stamp bad"' 1
perl -i -pe 's/trigger-x/trigger/' "$flip"
expect "stamp: fixed page passes" 0 "" "$SOP/document.json" "$flip"
has "stamp: green replaces red" "$flip" 'class="stamp' 1
lacks "stamp: no red left" "$flip" 'stamp bad'

expect "page: missing section fails" 1 "Seite: der Abschnitt „Prüfschritte“ fehlt" \
  "$SOP/document.json" "$(page nosec 's/data-section="pruefen"/class="pruefen"/; print')"
expect "page: duplicate section fails" 1 "„Prüfschritte“ (data-section=\"pruefen\") steht 2-mal" \
  "$SOP/document.json" "$(page dupsec 's/data-section="probleme"/data-section="pruefen"/; print')"
expect "page: sections out of order fail" 1 "die Abschnitte stehen nicht in der festen Reihenfolge" \
  "$SOP/document.json" "$(page order 's/data-section="pruefen"/data-section="X"/; s/data-section="probleme"/data-section="pruefen"/; s/data-section="X"/data-section="probleme"/; print')"
expect "page: unknown section id fails" 1 "den Abschnitt data-section=\"extra\" gibt es nicht" \
  "$SOP/document.json" "$(page unknown 's/data-section="zahlen"/data-section="extra"/; print')"
expect "page: rollen in an SOP fails" 1 "gehört nur in eine Prozessdokumentation" \
  "$SOP/document.json" "$(page rollensop 's/(<section data-section="schritte">)/<section data-section="rollen"><h2>Rollen und Übergaben<\/h2><\/section>\n$1/; print')"
perl -CSD -ne 'print unless /data-section="rollen"/' "$PD/full.html" >"$PD/norollen.html"
expect "page: rollen missing in a Prozessdokumentation fails" 1 "Seite: der Abschnitt „Rollen und Übergaben“ fehlt" "$PD/document.json" "$PD/norollen.html"

"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["inferred"]=["steps.99.tool"]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/badinf.json"
expect "core: inferred path that does not exist fails" 1 "„steps.99.tool“ gibt es in document.json nicht" "$SOP/badinf.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["inferred"]=["steps.2"]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/groupinf.json"
expect "core: inferred path may point to a group" 0 "GEPRÜFT: vollständig" "$SOP/groupinf.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["systems"][0]["steps"]=[1,99]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/badsys.json"
expect "core: systems.steps pointing to step 99 fails" 1 "System 1 › In Schritten: verweist auf Schritt 99, den es nicht gibt" "$SOP/badsys.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); s=d["steps"][0]; s["executor"]="claude"; s.pop("minutes"); json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/claude.json"
expect "core: a step run by Claude needs no minutes" 0 "GEPRÜFT: vollständig" "$SOP/claude.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); s=d["steps"][0]; s["executor"]="person"; s.pop("minutes"); json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/person.json"
expect "core: a step run by a person needs minutes" 1 "Schritt 1 › Minuten: fehlt" "$SOP/person.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["steps"][0].pop("minutes"); json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/nominutes.json"
expect "core: a step without executor needs minutes" 1 "Schritt 1 › Minuten: fehlt" "$SOP/nominutes.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["steps"][0]["why"]={"open":"Warum so?","ask":"Grafik"}; d["not_for"]={"open":"Wofür nicht?"}; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/openwhy.json"
expect "core: why and not_for may be open questions" 0 "GEPRÜFT: vollständig" "$SOP/openwhy.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["reference"]=[{"title":"Umbenennung","rows":[["alt","neu"],[""]]}]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/badref.json"
expect "core: an empty reference cell fails" 1 "ist leer" "$SOP/badref.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["external"]=[{"party":"Lieferant","step":99,"receives":"Anfrage","returns":{"open":"Was kommt zurück?"}}]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/badext.json"
expect "core: an external party at step 99 fails" 1 "verweist auf Schritt 99, den es nicht gibt" "$SOP/badext.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["external"]=[{"party":"Lieferant","step":1,"receives":"Anfrage","returns":{"open":"Was kommt zurück?"}}]; d["metrics"]["input_defect_rate"]={"value":"ca. 50 %","source":"Team","estimate":True}; d["basis"]=[{"source":"Interview","date":"2026-11-05","covers":"alles"}]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/newfields.json"
expect "core: external party, input defect rate and a source list pass" 0 "GEPRÜFT: vollständig" "$SOP/newfields.json"
"$PY" -c 'import json,sys; d=json.load(open(sys.argv[1])); d["basis"]=[{"source":""}]; json.dump(d,open(sys.argv[2],"w"))' "$SOP/document.json" "$SOP/badbasis.json"
expect "core: a source with no name fails" 1 "Grundlage" "$SOP/badbasis.json"

expect "page: inferred fact with abgeleitet in its marker passes" 0 "GEPRÜFT: vollständig" "$SOP/document.json" "$(page infok)"
expect "page: inferred fact without abgeleitet fails" 1 "„steps.1.tool“ ist abgeleitet, aber kein Marker dafür enthält das Wort „abgeleitet“" \
  "$SOP/document.json" "$(page noinf 'print unless /<em>abgeleitet<\/em>/')"
expect "page: abgeleitet in an unrelated marker does not count" 1 "„steps.1.tool“ ist abgeleitet" \
  "$SOP/document.json" "$(page otherinf 's/<em>abgeleitet<\/em>//; s/(<div data-core="trigger">)/$1<em>Abgeleitet<\/em>/; print')"
expect "page: abgeleitet in a covering ancestor marker counts" 0 "GEPRÜFT: vollständig" \
  "$SOP/document.json" "$(page ancinf 's/<em>abgeleitet<\/em>//; s/(<div data-core="steps.1">)/$1<em>Abgeleitet<\/em>/; print')"

echo "$pass passed, $fail failed"
[ "$fail" = 0 ]
