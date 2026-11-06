#!/usr/bin/env python3
"""Check a capture (document.json) or a pitch brief (brief.json) against its schema plus the rules a
schema cannot express. The document's "schema" field picks the schema file. With a page, also check
that every core fact stands word for word inside its data-core marker, and write the result into the
page's stamp slot.

Usage: python3 check.py [--final] <document.json> [page.html]
Exit 0 = all parts there (a draft while questions are open), 1 = something is missing, 2 = wrong call.
--final also fails on open questions, a missing real screenshot, missing real files and (brief)
missing evidence: the gates before a document counts as build-ready or a brief is submitted.
Prints a German list the interview can ask from; with a page and exit 0 also the Artifact `files`
map as JSON.
Python standard library only (3.9+).
"""
import datetime
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import unquote

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_DIR = os.path.join(HERE, "..", "schema")
SCHEMAS = {"ablauf-dokumentieren/capture/v2": "capture.schema.json", "fps/brief/v1": "brief.schema.json"}
DEFAULT_SCHEMA = "ablauf-dokumentieren/capture/v2"

FILLERS = {"-", "–", "—", "n/a", "na", "k.a.", "k. a.", "keine angabe", "nicht genannt",
           "tbd", "?", "...", "…", "offen"}
TYPE_DE = {"string": "Text", "integer": "ganze Zahl", "boolean": "ja/nein",
           "object": "Gruppe von Feldern", "array": "Liste"}
MAX_STEPS = 20


# ---------- minimal JSON-Schema validator (the subset capture.schema.json uses) ----------

class Err:
    def __init__(self, path, kind, schema, detail=""):
        self.path, self.kind, self.schema, self.detail = list(path), kind, schema, detail


def resolve(root, s):
    while "$ref" in s:
        ref = s["$ref"]
        target = root
        for part in ref.lstrip("#/").split("/"):
            target = target[part]
        merged = dict(target)
        merged.update({k: v for k, v in s.items() if k != "$ref"})
        s = merged
    return s


def type_ok(t, v):
    return {"string": isinstance(v, str),
            "integer": isinstance(v, int) and not isinstance(v, bool),
            "boolean": isinstance(v, bool),
            "object": isinstance(v, dict),
            "array": isinstance(v, list)}[t]


def validate(root, s, v, path):
    s = resolve(root, s)
    errs = []
    if "oneOf" in s:
        errs += one_of(root, s, v, path)
    if "const" in s and v != s["const"]:
        errs.append(Err(path, "const", s))
    if "enum" in s and v not in s["enum"]:
        errs.append(Err(path, "enum", s))
    if "type" in s and not type_ok(s["type"], v):
        return errs + [Err(path, "type", s, s["type"])]
    if isinstance(v, str):
        if len(v.strip()) < s.get("minLength", 0):
            errs.append(Err(path, "empty", s))
        if "pattern" in s and not re.search(s["pattern"], v):
            errs.append(Err(path, "pattern", s))
    if isinstance(v, list):
        if len(v) < s.get("minItems", 0):
            errs.append(Err(path, "minItems", s, s["minItems"]))
        if "items" in s:
            for i, item in enumerate(v):
                errs += validate(root, s["items"], item, path + [i])
    if isinstance(v, dict):
        props = s.get("properties", {})
        for key in s.get("required", []):
            if key not in v:
                errs.append(Err(path + [key], "missing", s))
        for key, item in v.items():
            if key in props:
                errs += validate(root, props[key], item, path + [key])
            elif s.get("additionalProperties") is False:
                errs.append(Err(path + [key], "unknown", s))
    for sub in s.get("allOf", []):
        errs += validate(root, sub, v, path)
    if "if" in s:
        branch = "else" if validate(root, s["if"], v, path) else "then"
        errs += validate(root, s.get(branch, {}), v, path)
    return errs


def one_of(root, s, v, path):
    branches = [resolve(root, b) for b in s["oneOf"]]
    results = [validate(root, b, v, path) for b in branches]
    if any(not r for r in results):
        return []

    def score(b):
        if "type" in b and not type_ok(b["type"], v):
            return -1
        if isinstance(v, dict):
            props = b.get("properties", {})
            hit = sum(1 for k in v if k in props)
            const_hit = sum(1 for k, p in props.items() if "const" in p and v.get(k) == p["const"])
            return hit + 10 * const_hit
        return 0

    scores = [score(b) for b in branches]
    best = max(range(len(branches)), key=lambda i: scores[i])
    if scores[best] <= 0 and not (isinstance(v, str) and scores[best] == 0):
        return [Err(path, "oneOf", s)]
    return results[best]


# ---------- German labels from the schema ----------

def schema_at(root, path, data):
    """Walk the schema along a data path. Return (labels, leaf_schema)."""
    s = resolve(root, root)
    labels, node = [], data
    for part in path:
        if isinstance(part, int):
            item_name = s.get("x-item", "Eintrag")
            nr = part + 1
            if isinstance(node, list) and part < len(node) and isinstance(node[part], dict) \
                    and isinstance(node[part].get("nr"), int):
                nr = node[part]["nr"]
            if labels:
                labels[-1] = "%s %d" % (item_name, nr)
            else:
                labels.append("%s %d" % (item_name, nr))
            s = resolve(root, s.get("items", {}))
        else:
            sub = None
            candidates = [s] + [resolve(root, b) for b in s.get("oneOf", [])]
            for c in candidates:
                if part in c.get("properties", {}):
                    sub = c["properties"][part]
                    break
            if sub is None:
                return labels + ["„%s“" % part], {}
            title = sub.get("title") or resolve(root, sub).get("title") or part
            labels.append(title)
            s = resolve(root, sub)
            s = dict(s, title=title, **({"x-frage": sub["x-frage"]} if "x-frage" in sub else {}))
        node = node[part] if isinstance(node, (dict, list)) and _has(node, part) else None
    return labels, s


def _has(node, part):
    if isinstance(node, list):
        return isinstance(part, int) and part < len(node)
    return part in node


def where(root, path, data):
    labels, _ = schema_at(root, path, data)
    return " › ".join(labels) if labels else "Dokument"


def message(root, e, data):
    labels, leaf = schema_at(root, e.path, data)
    place = " › ".join(labels) if labels else "Dokument"
    own = e.schema.get("x-fehler")
    if e.kind == "missing":
        text = "fehlt"
    elif e.kind == "empty":
        text = "ist leer oder nur „–“"
    elif e.kind == "unknown":
        return "%s: unbekanntes Feld. Tippfehler? Erlaubt sind nur die Felder aus dem Schema." % place, None
    elif e.kind == "type":
        text = "hat die falsche Form (erwartet: %s)" % TYPE_DE.get(e.detail, e.detail)
    elif e.kind == "minItems":
        text = own or ("ist leer" if e.detail == 1 else "braucht mindestens %d Einträge" % e.detail)
    elif e.kind == "oneOf":
        text = own or leaf.get("x-fehler") or "hat die falsche Form"
    else:
        text = own or "hat einen ungültigen Wert"
    frage = leaf.get("x-frage") or e.schema.get("x-frage")
    return "%s: %s." % (place, text), frage


# ---------- rules the schema cannot express ----------

def walk_strings(v, path):
    if isinstance(v, str):
        yield path, v
    elif isinstance(v, dict):
        for k, x in v.items():
            yield from walk_strings(x, path + [k])
    elif isinstance(v, list):
        for i, x in enumerate(v):
            yield from walk_strings(x, path + [i])


def is_filler(text):
    t = text.strip().lower()
    return t == "" or t in FILLERS or re.fullmatch(r"[-–—\s.]+", t) is not None


def rules(root, doc, base_dir):
    errors, warnings = [], []  # errors: (path, text, frage)
    steps = doc.get("steps") if isinstance(doc.get("steps"), list) else []
    step_role = {s.get("nr"): s.get("role") for s in steps if isinstance(s, dict)}

    for path, text in walk_strings(doc, []):
        if is_filler(text):
            errors.append((path, "ist leer oder nur „%s“" % text.strip() if text.strip() else "ist leer", None))

    nrs = [s.get("nr") for s in steps if isinstance(s, dict)]
    if nrs and nrs != list(range(1, len(nrs) + 1)):
        errors.append((["steps"], "die Nummern müssen 1, 2, 3 … in dieser Reihenfolge lauten (jetzt: %s)"
                       % ", ".join(str(n) for n in nrs), None))
    if len(steps) > MAX_STEPS:
        warnings.append("Schritte: %d Schritte (Richtwert höchstens %d). Lassen sich Schritte zusammenfassen?"
                        % (len(steps), MAX_STEPS))

    def need_step(path, nr):
        if "steps" in doc and isinstance(nr, int) and nr not in step_role:
            errors.append((path, "verweist auf Schritt %d, den es nicht gibt" % nr,
                           "Zu welchem Schritt gehört das?"))

    for i, shot in enumerate(doc.get("screenshots") or []):
        if not isinstance(shot, dict):
            continue
        need_step(["screenshots", i, "step"], shot.get("step"))
        if shot.get("kind") == "echt" and isinstance(shot.get("file"), str) and shot["file"].strip():
            if not os.path.isfile(os.path.join(base_dir, shot["file"])):
                errors.append((["screenshots", i, "file"], "die Bilddatei „%s“ gibt es nicht" % shot["file"],
                               "Bitte lade den Screenshot hoch oder korrigiere den Dateinamen."))
    for i, sysm in enumerate(doc.get("systems") or []):
        nrs_used = sysm.get("steps") if isinstance(sysm, dict) else None
        bad = [n for n in nrs_used if isinstance(n, int) and n not in step_role] if isinstance(nrs_used, list) else []
        if bad:
            errors.append((["systems", i, "steps"],
                           "verweist auf %s, den es nicht gibt" % ", ".join("Schritt %d" % n for n in bad),
                           "In welchen Schritten benutzt du dieses System?"))
    known = doc_paths(doc)
    for i, p in enumerate(doc.get("inferred") or []):
        if isinstance(p, str) and p.strip() and p.strip() not in known:
            errors.append((["inferred", i], "„%s“ gibt es in document.json nicht" % p.strip(),
                           "Welche Angabe ist gemeint? Pfade sehen so aus: trigger, steps.3.tool, checks.2.wrong."))
    for i, c in enumerate(doc.get("checks") or []):
        if isinstance(c, dict) and "step" in c:
            need_step(["checks", i, "step"], c["step"])

    files = doc.get("files") if isinstance(doc.get("files"), dict) else {}
    for group in ("inputs", "outputs"):
        for i, f in enumerate(files.get(group) or []):
            if isinstance(f, dict) and isinstance(f.get("preview"), str) and f["preview"].strip():
                if not os.path.isfile(os.path.join(base_dir, f["preview"])):
                    errors.append((["files", group, i, "preview"],
                                   "die Bilddatei „%s“ gibt es nicht" % f["preview"], None))

    for i, e in enumerate(doc.get("external") or []):
        if isinstance(e, dict):
            need_step(["external", i, "step"], e.get("step"))

    for i, h in enumerate(doc.get("handoffs") or []):
        if not isinstance(h, dict):
            continue
        need_step(["handoffs", i, "from_step"], h.get("from_step"))
        need_step(["handoffs", i, "to_step"], h.get("to_step"))
        target = step_role.get(h.get("to_step"))
        if target and h.get("to_role") and target != h["to_role"]:
            errors.append((["handoffs", i, "to_role"],
                           "sagt „%s“, aber Schritt %s macht die Rolle „%s“" % (h["to_role"], h["to_step"], target),
                           "An welche Rolle geht die Arbeit wirklich?"))
        source = step_role.get(h.get("from_step"))
        if source and target and source == target:
            warnings.append("%s: Von- und An-Schritt haben dieselbe Rolle „%s“. Ist das wirklich eine Übergabe?"
                            % (where(root, ["handoffs", i], doc), source))

    if doc.get("depth") == "prozessdokumentation" and isinstance(doc.get("roles"), list):
        names = [r.get("name") for r in doc["roles"] if isinstance(r, dict)]
        for s in steps:
            if isinstance(s, dict) and s.get("role") and s["role"] not in names:
                errors.append((["steps", steps.index(s), "role"],
                               "„%s“ steht nicht in der Liste der Rollen" % s["role"],
                               "Ist das eine eigene Rolle? Dann ergänze sie unter Rollen."))
        received = {h.get("to_role") for h in doc.get("handoffs") or [] if isinstance(h, dict)}
        first = steps[0].get("role") if steps and isinstance(steps[0], dict) else None
        for i, name in enumerate(names):
            if name not in {s.get("role") for s in steps if isinstance(s, dict)}:
                warnings.append("Rolle „%s“ macht keinen Schritt." % name)
            elif name != first and name not in received:
                errors.append((["roles", i], "„%s“ bekommt von keiner anderen Rolle eine Übergabe" % name,
                               "Von wem bekommt „%s“ die Arbeit, was genau, und in welcher Form?" % name))

    for path, text in walk_strings(doc, []):
        _, leaf = schema_at(root, path, doc)
        limit = leaf.get("x-max")
        if limit and len(text) > limit:
            warnings.append("%s: %d Zeichen (Richtwert %d). Lässt es sich kürzer sagen?"
                            % (where(root, path, doc), len(text), limit))

    roles_doing = sorted({s.get("role") for s in steps if isinstance(s, dict) and isinstance(s.get("role"), str)})
    if doc.get("depth") == "sop" and len(roles_doing) > 1:
        warnings.append("Tiefe: in dieser SOP machen %d Rollen Schritte (%s). Ist es eine Prozessdokumentation?"
                        % (len(roles_doing), ", ".join(roles_doing)))

    folder = doc.get("sharepoint_folder")
    if isinstance(folder, str) and re.search(r"[<\[]", folder):
        warnings.append("SharePoint-Ordner: enthält noch Platzhalter (%s). Bitte Person und Beitragsliste-ID eintragen."
                        % folder)
    return errors, warnings


def compress(places):
    """['Schritt 1 › Minuten', 'Schritt 2 › Minuten'] -> ['Schritte 1–2 › Minuten']"""
    groups, order = {}, []
    for p in places:
        m = re.match(r"(Schritt) (\d+)( › .*)$", p)
        key = (m.group(1), m.group(3)) if m else (p, None)
        if key not in groups:
            groups[key] = []
            order.append(key)
        if m:
            groups[key].append(int(m.group(2)))
    out = []
    for key in order:
        nums = sorted(set(groups[key]))
        if key[1] is None:
            out.append(key[0])
        elif len(nums) == 1:
            out.append("Schritt %d%s" % (nums[0], key[1]))
        else:
            runs, start = [], nums[0]
            for a, b in zip(nums, nums[1:] + [None]):
                if b != a + 1:
                    runs.append("%d" % a if start == a else "%d–%d" % (start, a))
                    start = b
            out.append("Schritte %s%s" % (", ".join(runs), key[1]))
    return out


def group_steps(errors):
    """Merge 'Schritt N › Feld: text.' lines that differ only in N into one line."""
    out, index = [], {}
    for text, frage in errors:
        m = re.match(r"(Schritt \d+ › [^:]+): (.*)$", text)
        if not m:
            out.append([[text], None, frage])
            continue
        place = m.group(1)
        key = (re.sub(r"^Schritt \d+", "", place), m.group(2), frage)
        if key in index:
            out[index[key]][0].append(place)
        else:
            index[key] = len(out)
            out.append([[place], m.group(2), frage])
    return [(("%s: %s" % (", ".join(compress(places)), rest)) if rest is not None else places[0], frage)
            for places, rest, frage in out]


# ---------- the page: every core fact inside its data-core marker ----------

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
SECTIONS = [("kurz", "Kurz gesagt"), ("rahmen", "Wann, was, wann fertig"),
            ("systeme", "Systeme und Zugang"), ("vorbereiten", "Vorher bereitlegen"),
            ("rollen", "Rollen und Übergaben"), ("schritte", "Schritte"), ("pruefen", "Prüfschritte"),
            ("probleme", "Wenn etwas schiefgeht"), ("dateien", "Echte Dateien"),
            ("zahlen", "Zahlen und Aufwand"), ("offen", "Noch offen")]
STAMP = re.compile(r"(<!--stamp-->)(.*?)(<!--/stamp-->)", re.DOTALL)
TYPOGRAPHY = str.maketrans({"„": '"', "“": '"', "”": '"', "″": '"', "‚": "'", "‘": "'", "’": "'",
                            "–": "-", "—": "-"})


def norm(text):
    return re.sub(r"\s+", "", text.casefold().translate(TYPOGRAPHY))


def dotted(path):
    return ".".join(str(p + 1) if isinstance(p, int) else p for p in path)


def core_leaves(root, doc):
    """[(path, path_str, kind, value)] for every fact the page must show; kind is "text" or "img"."""
    leaves = []

    def walk(v, path):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x, path + [k])
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, path + [i])
        elif isinstance(v, bool) or path[:1] in (["schema"], ["inferred"]):
            return
        elif isinstance(v, (int, float)):
            if path[-1] == "value":
                leaves.append((path, dotted(path), "text", str(v)))
        elif isinstance(v, str):
            leaf = schema_at(root, path, doc)[1]
            if "enum" in leaf or "const" in leaf:
                return
            real_shot = len(path) == 3 and path[0] == "screenshots" and path[2] == "file" \
                and doc["screenshots"][path[1]].get("kind") == "echt"
            kind = "img" if real_shot or path[-1] == "preview" else "text"
            leaves.append((path, dotted(path), kind, v))

    walk(doc, [])
    return leaves


def doc_paths(v, prefix=""):
    """Every dotted path in the document. A marker on a choice field or on a group is no typo."""
    out = set()
    items = v.items() if isinstance(v, dict) else enumerate(v, 1) if isinstance(v, list) else []
    for k, x in items:
        p = "%s.%s" % (prefix, k) if prefix else str(k)
        out.add(p)
        out |= doc_paths(x, p)
    return out


HIDING = re.compile(r"display:none|visibility:hidden|font-size:0(?![.\d]*[1-9])")


def hides_content(tag, attrs, hidden_classes):
    """A fact in hidden markup is not on the page for the reader, so it must not count. That covers
    inline styles, a class a <style> rule hides, and a collapsed <details>."""
    style = re.sub(r"\s", "", (attrs.get("style") or "").lower())
    classes = set((attrs.get("class") or "").split())
    return ("hidden" in attrs or attrs.get("aria-hidden") == "true" or bool(HIDING.search(style))
            or bool(classes & hidden_classes) or (tag == "details" and "open" not in attrs))


def hidden_classes_in(css):
    css = re.sub(r"\s", "", css.lower())
    out = set()
    for selectors, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if HIDING.search(body):
            out |= set(re.findall(r"^\.([\w-]+)$", s)[0] for s in selectors.split(",") if re.match(r"^\.[\w-]+$", s))
    return out


class Page(HTMLParser):
    """For each element with data-core: its paths, its normalized text and the img srcs inside it."""

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.stack, self.marks, self.srcs, self.text, self.hidden = [], [], [], [], 0
        self.sections, self.hidden_classes, self.section_starts = [], set(), []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        mark = None
        if a.get("data-section"):
            self.sections.append((a["data-section"].strip(), self.getpos()[0]))
            self.section_starts.append((a["data-section"].strip(), len(self.text)))
        if a.get("data-core"):
            mark = {"paths": a["data-core"].split(), "start": len(self.text), "end": None,
                    "imgs": [], "line": self.getpos()[0]}
            self.marks.append(mark)
        hides = tag in ("script", "style", "template") or hides_content(tag, a, self.hidden_classes)
        if tag == "img" and a.get("src") and not (self.hidden or hides):
            self.srcs.append(a["src"])
            for m in self.marks:
                if m["end"] is None:
                    m["imgs"].append(a["src"])
        if tag in VOID:
            if mark:
                mark["end"] = len(self.text)
            return
        if hides:
            self.hidden += 1
        self.stack.append((tag, mark, hides))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag not in [t for t, _, _ in self.stack]:
            return
        while True:
            t, mark, hides = self.stack.pop()
            if hides:
                self.hidden -= 1
            if mark:
                mark["end"] = len(self.text)
            if t == tag:
                return

    def handle_data(self, data):
        if self.stack and self.stack[-1][0] == "style":
            self.hidden_classes |= hidden_classes_in(data)
        if not self.hidden:
            self.text.append(data)

    def close(self):
        HTMLParser.close(self)
        for m in self.marks:
            end = len(self.text) if m["end"] is None else m["end"]
            m["text"] = norm("".join(self.text[m["start"]:end]))
        self.section_text = {}
        bounds = self.section_starts + [(None, len(self.text))]
        for (sid, start), (_, end) in zip(bounds, bounds[1:]):
            self.section_text[sid] = self.section_text.get(sid, "") + norm("".join(self.text[start:end]))


def clean_src(src):
    return src[2:] if src.startswith("./") else src


def is_local(src):
    return not re.match(r"^([a-zA-Z][a-zA-Z0-9+.-]*:|/)", src)


def check_sections(root, doc, page):
    """The fixed sections: each id once, in order; rollen only in a Prozessdokumentation."""
    errors = []
    sections = [tuple(s) for s in root.get("x-sections", SECTIONS)]
    is_pd = doc.get("depth") == "prozessdokumentation" or "x-sections" in root
    wanted = [sid for sid, _ in sections if is_pd or sid != "rollen"]
    heading = dict(sections)
    found = [sid for sid, _ in page.sections]
    for sid, line in page.sections:
        if sid not in heading:
            errors.append(("Seite, Zeile %d: den Abschnitt data-section=\"%s\" gibt es nicht. Erlaubt sind: %s."
                           % (line, sid, ", ".join(s for s, _ in sections)), None))
    for sid in wanted:
        n = found.count(sid)
        if n == 0:
            errors.append(("Seite: der Abschnitt „%s“ fehlt. Setze <section data-section=\"%s\"> mit der "
                           "Überschrift „%s“ an die richtige Stelle." % (heading[sid], sid, heading[sid]), None))
        elif n > 1:
            errors.append(("Seite: der Abschnitt „%s“ (data-section=\"%s\") steht %d-mal. Er darf nur einmal vorkommen."
                           % (heading[sid], sid, n), None))
    if not is_pd and "rollen" in found and "x-sections" not in root:
        errors.append(("Seite: der Abschnitt „Rollen und Übergaben“ (data-section=\"rollen\") gehört nur in eine "
                       "Prozessdokumentation. Entferne ihn aus der SOP.", None))
    present = [sid for sid in wanted if sid in found]
    order = []
    for sid in found:
        if sid in present and sid not in order:
            order.append(sid)
    if order != present:
        errors.append(("Seite: die Abschnitte stehen nicht in der festen Reihenfolge. Richtig ist: %s."
                       % ", ".join(wanted), None))
    return errors


def open_questions(v):
    if isinstance(v, dict):
        if isinstance(v.get("open"), str):
            yield v["open"]
        for x in v.values():
            yield from open_questions(x)
    elif isinstance(v, list):
        for x in v:
            yield from open_questions(x)


def check_open_list(doc, page):
    """Every open question also stands in the section "offen", so the reader sees all gaps in one place."""
    listed = getattr(page, "section_text", {}).get("offen", "")
    missing = [q for q in dict.fromkeys(open_questions(doc)) if norm(q) not in listed]
    if not missing:
        return []
    shown = "; ".join("„%s“" % q for q in missing[:3]) + (" und %d weitere" % (len(missing) - 3) if len(missing) > 3 else "")
    return [("Seite: %d offene Frage(n) steht nicht im Abschnitt „Noch offen“ (%s). Liste dort jede offene Frage, "
             "die den Bau blockierenden zuerst." % (len(missing), shown), None)]


def check_inferred(doc, page):
    """Every inferred fact must say "abgeleitet" inside a marker that covers it."""
    errors = []
    known = doc_paths(doc)
    for p in doc.get("inferred") or []:
        p = p.strip() if isinstance(p, str) else ""
        if p not in known:
            continue
        covering = [m for m in page.marks if any(p == q or p.startswith(q + ".") for q in m["paths"])]
        if not any("abgeleitet" in m["text"] for m in covering):
            errors.append(("Seite › Abgeleitet: „%s“ ist abgeleitet, aber kein Marker dafür enthält das Wort "
                           "„abgeleitet“. Schreibe z. B. „abgeleitet, bitte bestätigen“ in den Marker data-core=\"%s\"."
                           % (p, p), None))
    return errors


def check_page(root, doc, page_path):
    """Return (errors [(text, frage)], local img srcs). The stamp slot is blanked before parsing,
    so an old stamp never counts as page text."""
    with open(page_path, encoding="utf-8") as fh:
        source = fh.read()
    errors = []
    if not STAMP.search(source):
        errors.append(("Seite: der Stempel-Platz <!--stamp--><!--/stamp--> fehlt. Übernimm ihn aus "
                       "template/capture.html, direkt am Anfang von <div class=\"wrap\">.", None))
    page = Page()
    page.feed(STAMP.sub(r"\1\3", source))
    page.close()
    if not isinstance(doc, dict):
        return errors, []
    errors += check_sections(root, doc, page)

    step_lines, other = {}, []
    for path, path_str, kind, value in core_leaves(root, doc):
        covering = [m for m in page.marks
                    if any(path_str == p or path_str.startswith(p + ".") for p in m["paths"])]
        if kind == "img":
            if any(clean_src(value) == clean_src(src) for m in covering for src in m["imgs"]):
                continue
            rest = "das Bild „%s“ fehlt auf der Seite oder steht nicht im Marker" % value
        else:
            if any(norm(value) in m["text"] for m in covering):
                continue
            rest = "fehlt auf der Seite oder steht nicht wörtlich im Marker"
        labels = schema_at(root, path, doc)[0]
        if path[0] == "steps" and len(path) > 2:
            key = (" › ".join(labels[1:]), rest, dotted(path[2:]))
            step_lines.setdefault(key, []).append((labels[0], path[1] + 1))
        else:
            other.append(("Seite › %s: %s data-core=\"%s\"." % (" › ".join(labels), rest, path_str), None))
    for (field, rest, tail), hits in step_lines.items():
        place = compress(["%s › %s" % (label, field) for label, _ in hits])[0]
        nr = str(hits[0][1]) if len(hits) == 1 else "<Nr>"
        errors.append(("Seite › %s: %s data-core=\"steps.%s.%s\"." % (place, rest, nr, tail), None))
    errors += other

    known = doc_paths(doc)
    for m in page.marks:
        for p in m["paths"]:
            if p not in known:
                errors.append(("Seite, Zeile %d: den Marker data-core=\"%s\" gibt es in document.json nicht. "
                               "Tippfehler? Pfade sehen so aus: trigger, steps.3.why, checks.2.wrong."
                               % (m["line"], p), None))

    errors += check_inferred(doc, page)
    errors += check_open_list(doc, page)

    local = []
    for src in page.srcs:
        if not is_local(src) or clean_src(src) in local:
            continue
        local.append(clean_src(src))
        if not os.path.isfile(os.path.join(os.path.dirname(page_path), unquote(re.split(r"[?#]", src)[0]))):
            errors.append(("Seite: das Bild „%s“ gibt es nicht im Ordner der Seite." % src,
                           "Liegt die Datei neben der Seite, und stimmt der Pfad?"))
    return errors, local


def stamp_html(result):
    if result["ok"] and not result["open"]:
        return '<div class="stamp ok"><b>Geprüft: vollständig</b> baufertig · Schema v%s · %s</div>' % (
            result["version"], result["date"])
    if result["ok"]:
        return '<div class="stamp draft"><b>Geprüft: Entwurf</b> %s · Schema v%s · %s</div>' % (
            open_text(result["open"]), result["version"], result["date"])
    items = []
    for text, frage in result["errors"]:
        q = '<br><span class="q">Frage: „%s“</span>' % html.escape(frage) if frage else ""
        items.append("<li>%s%s</li>" % (html.escape(text), q))
    return '<div class="stamp bad"><b>Nicht vollständig</b><ol>%s</ol></div>' % "".join(items)


def write_stamp(page_path, result):
    with open(page_path, encoding="utf-8") as fh:
        source = fh.read()
    new = STAMP.sub(lambda m: m.group(1) + stamp_html(result) + m.group(3), source, count=1)
    if new != source:
        with open(page_path, "w", encoding="utf-8") as fh:
            fh.write(new)


# ---------- entry points ----------

def diagram_file(doc):
    """The draw.io file of a capture (picture.drawio) or a brief (today.diagram), or None."""
    pic = doc.get("picture") if isinstance(doc.get("picture"), dict) else {}
    today = doc.get("today") if isinstance(doc.get("today"), dict) else {}
    f = pic.get("drawio") or today.get("diagram")
    if isinstance(f, dict) and isinstance(f.get("path"), str) and f.get("status") != "platzhalter":
        return f["path"]
    return None


def check_diagram(doc, base_dir):
    """Return (errors [(text, frage)], note or None). The diagram must open in draw.io, have a box for
    every step (its label starts with the step number) and, in a Prozessdokumentation, a lane per role."""
    rel = diagram_file(doc)
    if not rel:
        return [], None
    path = os.path.join(base_dir, rel)
    if not os.path.isfile(path):
        return [("Bild: die draw.io-Datei „%s“ gibt es nicht neben document.json." % rel,
                 "Liegt die draw.io-Datei im selben Ordner, und stimmt der Name?")], None
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        return [("Bild: „%s“ ist keine gültige draw.io-Datei (%s)." % (rel, exc), None)], None
    cells = [c for c in tree.iter("mxCell") if c.get("vertex") == "1"]
    if tree.getroot().tag not in ("mxfile", "mxGraphModel") or not cells:
        return [("Bild: „%s“ ist keine gültige draw.io-Datei (keine Kästen gefunden)." % rel, None)], None
    labels = [norm(re.sub(r"<[^>]+>", " ", html.unescape(c.get("value") or ""))) for c in cells]
    errors = []
    for s in doc.get("steps") or []:
        nr = s.get("nr") if isinstance(s, dict) else None
        if isinstance(nr, int) and not any(re.match(r"^%d\b" % nr, l) for l in labels):
            errors.append(("Bild: Schritt %d hat keinen Kasten in „%s“ (die Beschriftung beginnt mit der Nummer)." % (nr, rel), None))
    lanes = 0
    if doc.get("depth") == "prozessdokumentation":
        for r in doc.get("roles") or []:
            name = r.get("name") if isinstance(r, dict) else None
            if isinstance(name, str) and name.strip():
                if norm(name) in labels:
                    lanes += 1
                else:
                    errors.append(("Bild: die Rolle „%s“ hat keine Bahn in „%s“." % (name, rel), None))
    if errors:
        return errors, None
    return [], "Diagramm geprüft: %s (%d Kästen, %d Bahnen)" % (rel, len(cells) - lanes, lanes)


def final_gates(root, doc):
    """The gates before a document counts as build-ready (capture) or may be submitted (brief)."""
    errors = []
    if not isinstance(doc, dict):
        return errors
    n = count_open(doc)
    if n:
        errors.append(("Final: %s. Beantworte sie oder kläre sie mit der genannten Rolle." % open_text(n), None))
    shots = [s for s in doc.get("screenshots") or [] if isinstance(s, dict)]
    if not any(s.get("kind") == "echt" for s in shots) and not doc.get("no_screen_reason"):
        errors.append(("Final: kein echter Screenshot. Mindestens einer aus dem System, in dem die Arbeit passiert.",
                       "Kannst du einen Screenshot vom wichtigsten Schritt machen?"))
    files = doc.get("files") if isinstance(doc.get("files"), dict) else {}
    for key, label in (("inputs", "Eingabedatei"), ("outputs", "Ergebnisdatei")):
        if not any(isinstance(f, dict) and f.get("status") in ("abgelegt", "lokal") for f in files.get(key) or []):
            errors.append(("Final: keine echte %s, nur Platzhalter." % label,
                           "Kannst du eine echte %s hochladen?" % label))
    ev = doc.get("evidence")
    if isinstance(ev, dict):
        real = [k for k in ("frequency", "time", "errors", "cost") if isinstance(ev.get(k), dict) and "value" in ev[k]]
        if not real:
            errors.append(("Final: keine Evidenz. Mindestens eins von Häufigkeit, Zeit, Fehlern oder Kosten als Zahl.",
                           "Wie oft passiert es, und wie viel Zeit kostet es ungefähr?"))
    return errors


def check_core(root, doc_path):
    """Return (doc or None, errors [(text, frage)], warnings [text])."""
    try:
        with open(doc_path, encoding="utf-8") as fh:
            doc = json.load(fh)
    except ValueError as exc:
        return None, [("document.json ist kein gültiges JSON: %s" % exc, None)], []

    seen, errors = set(), []

    def add(path, text, frage):
        key = tuple(path)
        if key in seen:
            return
        seen.add(key)
        errors.append((text, frage))

    if not isinstance(doc, dict):
        add([], "Dokument: muss eine Gruppe von Feldern sein.", None)
        rule_errs, warnings = [], []
    else:
        rule_errs, warnings = rules(root, doc, os.path.dirname(os.path.abspath(doc_path)))
    for path, text, frage in rule_errs:
        if text.startswith("ist leer"):
            add(path, "%s: %s." % (where(root, path, doc), text), frage or schema_at(root, path, doc)[1].get("x-frage"))
    for e in validate(root, root, doc, []):
        text, frage = message(root, e, doc)
        add(e.path, text, frage)
    for path, text, frage in rule_errs:
        if not text.startswith("ist leer"):
            errors.append(("%s: %s." % (where(root, path, doc), text), frage))
    return doc, group_steps(errors), warnings


def count_open(doc):
    """Distinct open questions the reader still has to answer: each {"open": …} text and each open
    point's question, counted once even when several fields carry the same question."""
    if not isinstance(doc, dict):
        return 0
    rest = {k: v for k, v in doc.items() if k != "open_points"}
    texts = {norm(q) for q in open_questions(rest)}
    for p in doc.get("open_points") or []:
        if isinstance(p, dict) and isinstance(p.get("question"), str):
            texts.add(norm(p["question"]))
        else:
            texts.add(repr(p))
    return len(texts)


def open_text(n):
    return "1 Frage offen" if n == 1 else "%d Fragen offen" % n


def load_schema(doc_path):
    """Return (schema, error or None), picked by the document's "schema" field."""
    try:
        with open(doc_path, encoding="utf-8") as fh:
            sid = json.load(fh).get("schema", DEFAULT_SCHEMA)
    except (ValueError, AttributeError):
        sid = DEFAULT_SCHEMA
    name = SCHEMAS.get(sid) if isinstance(sid, str) else None
    error = None
    if not name:
        error = ("Schema-Kennung: unbekanntes Schema „%s“. Bekannt sind: %s." % (sid, ", ".join(SCHEMAS)), None)
        name = SCHEMAS[DEFAULT_SCHEMA]
    with open(os.path.join(SCHEMA_DIR, name), encoding="utf-8") as fh:
        return json.load(fh), error


def run(doc_path, page_path=None, final=False):
    """Return {"ok", "errors": [(text, frage)], "warnings": [text], "notes", "date", "version", "files"}.
    With a page, also check the page, write the stamp into it, and fill "files" on success."""
    root, schema_error = load_schema(doc_path)
    if schema_error:
        result = {"ok": False, "errors": [schema_error], "warnings": [], "notes": [], "open": 0, "final": final,
                  "date": datetime.date.today().isoformat(), "version": "?", "files": {}}
        if page_path:
            write_stamp(page_path, result)
        return result
    doc, errors, warnings = check_core(root, doc_path)
    notes = []
    if isinstance(doc, dict):
        diagram_errors, note = check_diagram(doc, os.path.dirname(os.path.abspath(doc_path)))
        errors = errors + diagram_errors
        notes += [note] if note else []
        if final:
            errors = errors + final_gates(root, doc)
    files = {}
    if page_path:
        page_errors, srcs = check_page(root, doc, page_path)
        errors = errors + page_errors
        files = {os.path.basename(doc_path): doc_path}
        for src in srcs:
            files[src] = os.path.join(os.path.dirname(page_path), unquote(re.split(r"[?#]", src)[0]))
        rel = diagram_file(doc) if isinstance(doc, dict) else None
        if rel and notes:
            files[rel] = os.path.join(os.path.dirname(os.path.abspath(doc_path)), rel)
    result = {"ok": not errors, "errors": errors, "warnings": warnings, "notes": notes, "final": final,
              "open": count_open(doc),
              "date": datetime.date.today().isoformat(), "version": root["x-version"], "files": files}
    if page_path:
        write_stamp(page_path, result)
    return result


def report(result):
    lines = []
    if result["ok"] and not result["open"]:
        lines.append("GEPRÜFT: vollständig · baufertig · Schema v%s · %s" % (result["version"], result["date"]))
    elif result["ok"]:
        lines.append("GEPRÜFT: Entwurf · %s · Schema v%s · %s · noch nicht baufertig (check.py --final)"
                     % (open_text(result["open"]), result["version"], result["date"]))
    else:
        n = len(result["errors"])
        lines.append("NICHT VOLLSTÄNDIG: %s · Schema v%s · %s"
                     % ("1 Punkt fehlt oder ist falsch" if n == 1 else "%d Punkte fehlen oder sind falsch" % n,
                        result["version"], result["date"]))
        for i, (text, frage) in enumerate(result["errors"], 1):
            lines.append("%d. %s" % (i, text))
            if frage:
                lines.append("   Frage: „%s“" % frage)
    lines.extend(result.get("notes") or [])
    if result["warnings"]:
        lines.append("Hinweise (blockieren nicht):")
        lines.extend("- " + w for w in result["warnings"])
    if result["ok"] and result["files"]:
        lines.append("files-Map für die Artifact-Veröffentlichung:")
        lines.append(json.dumps(result["files"], ensure_ascii=False, indent=2))
    return "\n".join(lines)


def main(argv):
    final = "--final" in argv
    argv = [a for a in argv if a != "--final"]
    if len(argv) not in (2, 3) or (len(argv) == 3 and not os.path.isfile(argv[2])):
        print("Aufruf: python3 check.py [--final] <document.json> [seite.html]", file=sys.stderr)
        return 2
    result = run(argv[1], argv[2] if len(argv) == 3 else None, final)
    print(report(result))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
