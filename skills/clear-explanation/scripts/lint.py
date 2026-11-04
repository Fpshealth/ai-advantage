"""Verify an HTML explainer and the inventory.md next to it. Usage:
lint.py FILE.html [--old OLD.html] [--render] [--width WINDOW_PX] [--shots DIR]

Fails (exit 1) on:
- page: a <title> not 2-4 words; no summary paragraph before the first <h2>; an <h2> section
  whose first sentence is not a question; a term used before its <dfn> or defined twice
- links and images: a broken #anchor; a link present in --old but gone; a local image that is
  missing, has no alt text or is a data: URI
- pictures: an <h2> section with no <figure> and no data-no-picture reason; a reason that says
  the picture could not be made; a <figure> without <figcaption> or without a picture in it
- motion: autoplay or setInterval; a <video> without controls; a figure with buttons but not
  Back and Next; a stepper or @keyframes without a prefers-reduced-motion rule
- diagrams: a Mermaid or inline SVG diagram whose text renders below 11 px, and diagrams
  present without --render (the size check did not run). Without Playwright installed,
  --render prints a note and skips the size check.
- inventory.md: missing; columns not as in reference/inventory.md; an empty cell; a Status that is not
  exists, planned, unknown or open; a Name twice; no picture plan, or a plan that does not
  match the <h2> sections and their figures
- names: a <dfn> that is not an inventory Name, or an inventory Name with no <dfn>
--shots DIR saves a PNG of every <figure> as rendered, for the cold read.
Reports without failing: dashes, mid-sentence colons and sentence length (see the unslop skill).
The last line is PASS or FAIL (count).
After changing a check, run the fixture tests in the repo: test/clear-explanation/run.py.
"""
import argparse, html, os, re, sys

MIN_PX = 11
COLUMNS = ['name', 'is', 'madebyfrom', 'current', 'lives', 'status', 'source']
KINDS = {'screenshot', 'real output', 'diagram', 'animation', 'none'}
NOT_A_REASON = re.compile(r"\b(cannot|can't|could not|couldn't|unable|no access|todo|tbd|to come"
                          r"|kann nicht|konnte nicht|kein zugriff|nicht möglich|folgt)\b", re.I)
EMPTY = {'', '-', '\u2013', '\u2014', '?', 'tbd', 'todo', 'n/a'}


def strip(s, keep_dfn=False):
    s = re.sub(r'<(style|script|pre)[^>]*>.*?</\1>', ' ', s, flags=re.S)
    s = re.sub(r'<code[^>]*>.*?</code>', ' ', s, flags=re.S)
    if keep_dfn:
        s = re.sub(r'<dfn[^>]*>', '\x01', s).replace('</dfn>', '\x02')
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s)))


def body(s):
    m = re.search(r'<main[^>]*>(.*)</main>', s, re.S) or re.search(r'<body[^>]*>(.*)</body>', s, re.S)
    return m.group(1) if m else s


def terms(s):
    t = strip(body(s), keep_dfn=True)
    plain, out, seen, shift = t.replace('\x01', '').replace('\x02', ''), [], set(), 0
    for m in re.finditer('\x01(.*?)\x02', t):
        term, pos = m.group(1).strip(), m.start() - shift
        shift += 2
        if not term:
            continue
        if term.lower() in seen:
            out.append(f'DUP dfn {term!r}')
            continue
        seen.add(term.lower())
        u = re.search(r'(?<![\w-])' + re.escape(term) + r'(?![\w-])', plain, re.I)
        if u and u.start() < pos - 1:
            out.append(f'EARLY {term!r} used before its <dfn>: ...{plain[max(0, u.start() - 60):u.start() + 60]}...')
    return len(seen), out


def links(s, old):
    ids = set(re.findall(r'id="([^"]+)"', s))
    out = [f'BROKEN anchor #{h}' for h in re.findall(r'href="#([^"]+)"', s) if h not in ids]
    if old:
        url = lambda x: set(re.findall(r'href="(https?://[^"]+)"', x))
        out += [f'LOST link {u}' for u in sorted(url(old) - url(s))]
    return out


def images(path, s):
    out, base = [], os.path.dirname(os.path.abspath(path))
    for tag in re.findall(r'<(?:img|video|source)\b[^>]*>', s):
        src = re.search(r'\bsrc="([^"]+)"', tag)
        if src and src.group(1).startswith('data:'):
            out.append(f'DATA URI image {tag[:60]}: save it as a file next to the HTML')
        elif src and not re.match(r'(https?:|//)', src.group(1)) and not os.path.exists(os.path.join(base, src.group(1))):
            out.append(f'MISSING image file {src.group(1)}')
        if tag.startswith('<img') and not re.search(r'\balt="[^"]+"', tag):
            out.append(f'NO ALT {tag[:100]}')
    return out


def sections(s):
    """(heading text, section html, data-no-picture reason or None) per <h2>."""
    parts = re.split(r'(<h2\b[^>]*>)', body(s))
    out = []
    for i in range(1, len(parts), 2):
        reason = re.search(r'data-no-picture="([^"]*)"', parts[i])
        out.append((strip(parts[i + 1].split('</h2>')[0]).strip(), parts[i + 1], reason and reason.group(1)))
    return out


def pictures(s):
    out = []
    for name, sec, reason in sections(s):
        for f in re.findall(r'<figure\b.*?</figure>', sec, re.S):
            if '<figcaption' not in f:
                out.append(f'NO CAPTION figure in section {name[:60]!r}')
            if not re.search(r'<(img|svg|video|pre|table|canvas|button)\b|class="mermaid"|role="img"', f):
                out.append(f'EMPTY figure in section {name[:60]!r}: it has no image, diagram, output or stepper')
        if '<figure' not in sec and reason is None:
            out.append(f'NO PICTURE in section {name[:60]!r}: add a <figure> or <h2 data-no-picture="reason">')
        elif reason is not None and (not reason.strip() or NOT_A_REASON.search(reason)):
            out.append(f'BAD REASON data-no-picture={reason!r} in section {name[:60]!r}: get the picture (reference/pictures.md)')
    return out


def page(s):
    out = []
    t = re.search(r'<title>(.*?)</title>', s.split('<body')[0], re.S)
    n = len(strip(t.group(1)).split()) if t else 0
    if not 2 <= n <= 4:
        out.append(f'TITLE has {n} words; use a name of 2-4 words')
    top = re.split(r'<h2\b', body(s).split('</h1>', 1)[-1], maxsplit=1)[0]
    if not any(len(strip(p).split()) >= 40 for p in re.findall(r'<p\b.*?</p>', top, re.S)):
        out.append('NO SUMMARY before the first <h2>: add one paragraph (40+ words) on the whole system')
    for name, sec, _ in sections(s):
        text = strip(sec.split('</h2>', 1)[-1]).strip()
        first = re.match(r'.*?[.?!:](?=\s|$)', text)
        if not first or not first.group(0).endswith('?'):
            out.append(f'NO QUESTION opens section {name[:60]!r}: start it with the reader\'s question')
    return out


def motion(s):
    out = []
    if re.search(r'<(video|audio)\b[^>]*\bautoplay\b', s) or 'setInterval' in s:
        out.append('AUTOPLAY found (autoplay attribute or setInterval): let the reader step with Back/Next')
    out += [f'NO CONTROLS {v[:80]}' for v in re.findall(r'<video\b[^>]*>', s) if not re.search(r'\bcontrols\b', v)]
    steppers = [f for f in re.findall(r'<figure\b.*?</figure>', body(s), re.S) if '<button' in f]
    for f in steppers:
        labels = {strip(x).strip().lower() for x in re.findall(r'<button\b[^>]*>(.*?)</button>', f, re.S)}
        if not {'back', 'next'} <= labels:
            out.append(f'NO BACK/NEXT in stepper figure (buttons: {sorted(labels)})')
    if (steppers or '@keyframes' in s) and 'prefers-reduced-motion' not in s:
        out.append('NO REDUCED MOTION: add @media (prefers-reduced-motion: reduce) that shows all steps without motion')
    return out


def norm(x):
    return re.sub(r'\s+', ' ', x).strip().strip('.:?').lower()


def table(lines):
    return [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if not re.match(r'^\|[\s:|-]+\|$', l.strip())]


def inventory(path, s):
    """Check inventory.md next to the HTML and match it against the page."""
    inv = os.path.join(os.path.dirname(os.path.abspath(path)), 'inventory.md')
    if not os.path.exists(inv):
        return [f'NO INVENTORY {inv}: write it before the prose (reference/inventory.md)']
    blocks, cur = [], []
    for l in open(inv, encoding='utf-8').read().splitlines() + ['']:
        if l.strip().startswith('|'):
            cur.append(l)
        elif cur:
            blocks, cur = blocks + [table(cur)], []
    rows = next((b for b in blocks if b and norm(b[0][0]) == 'name'), None)
    plan = next((b for b in blocks if b and norm(b[0][0]) == 'section'), None)
    out = []
    if not rows:
        return ['NO INVENTORY TABLE in inventory.md: a table whose first column is Name']
    if [re.sub(r'[^a-z]', '', c.lower()) for c in rows[0]] != COLUMNS:
        out.append(f'COLUMNS {rows[0]}: use Name | Is | Made by, from | Current | Lives | Status | Source')
    names = {}
    for r in rows[1:]:
        name = r[0]
        for col, cell in zip(rows[0], r + [''] * (len(rows[0]) - len(r))):
            if cell.lower() in EMPTY:
                out.append(f'EMPTY cell {col!r} in row {name!r}: fill it from a source or write "open" and the question')
        status = r[5] if len(r) > 5 else ''
        if status and status.lower() not in EMPTY and not re.search(r'\b(exist\w*|planned|unknown|open)\b', status, re.I):
            out.append(f'STATUS {status!r} in row {name!r}: write exists, planned, unknown or open')
        if norm(name) in names:
            out.append(f'DUP Name {name!r} in inventory.md')
        names[norm(name)] = name
    dfns = {norm(strip(d)): strip(d).strip() for d in re.findall(r'<dfn\b[^>]*>(.*?)</dfn>', body(s), re.S)}
    out += [f'DRIFT <dfn>{d}</dfn> is not an inventory Name: rename it or add the row' for k, d in dfns.items() if k not in names]
    out += [f'NO DFN for inventory Name {n!r}: wrap its first use in <dfn>, or rename the row to the name the page uses'
            for k, n in names.items() if k not in dfns]
    if not plan:
        return out + ['NO PLAN in inventory.md: add | Section | Kind | Caption or reason | with one row per <h2>']
    heads = {norm(name): (name, reason) for name, _, reason in sections(s)}
    seen = set()
    for r in plan[1:]:
        sec, kind, cap = (r + ['', '', ''])[:3]
        seen.add(norm(sec))
        if norm(sec) not in heads:
            out.append(f'PLAN row {sec!r} matches no <h2> on the page')
            continue
        if kind.lower() not in KINDS:
            out.append(f'PLAN kind {kind!r} for {sec!r}: use one of {sorted(KINDS)}')
        if cap.lower() in EMPTY or (kind.lower() == 'none' and NOT_A_REASON.search(cap)):
            out.append(f'PLAN caption or reason {cap!r} for {sec!r}: write the takeaway, or for none a real reason')
        reason = heads[norm(sec)][1]
        if kind.lower() == 'none' and reason is None:
            out.append(f'PLAN says none for {sec!r} but the <h2> has no data-no-picture reason')
        elif kind.lower() not in ('none', '') and reason is not None:
            out.append(f'PLAN says {kind} for {sec!r} but the <h2> says data-no-picture')
    out += [f'PLAN has no row for section {n!r}' for k, (n, _) in heads.items() if k not in seen]
    return out


def prose(s):
    t = strip(re.sub(r'</?(p|li|td|th|tr|h[1-6]|div|br|dt|dd|figcaption)\b', r'. \g<0>', body(s)))
    notes = [f'DASH em {t.count(chr(0x2014))}, en {t.count(chr(0x2013))}']
    notes += [f'COLON? ...{t[max(0, m.start() - 40):m.end() + 20]}...' for m in re.finditer(r'[a-z]\w*: [a-z]\w+', t)][:15]
    sents = [x for x in re.split(r'(?<=[.!?])\s+', t) if len(x.split()) > 2]
    if sents:
        n = [len(x.split()) for x in sents]
        notes.append(f'SENTENCES {len(n)}, mean {sum(n) / len(n):.1f} words, over 30 words: {sum(k > 30 for k in n)}')
        notes += [f'LONG ({len(x.split())}) {x[:140]}...' for x in sorted(sents, key=lambda x: -len(x.split()))[:3] if len(x.split()) > 30]
    return notes


def diagrams(path, s, render, width, shots):
    blocks = [html.unescape(b) for b in re.findall(r'<(?:pre|div) class="mermaid"[^>]*>(.*?)</(?:pre|div)>', s, re.S)]
    out = [f'MERMAID {i} is left-to-right; draw it top-down unless --render shows text at {MIN_PX} px or more'
           for i, b in enumerate(blocks) if re.search(r'^\s*(graph|flowchart)\s+(LR|RL)', b, re.M)]
    svgs = len(re.findall(r'<svg\b', body(s)))
    if not (blocks or svgs or shots):
        return out, []
    if not (render or shots):
        return out, [f'RENDER skipped: {len(blocks)} Mermaid and {svgs} SVG diagram(s); run with --render to check text size']
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return out + [f'RENDER skipped: Playwright is not installed, so {len(blocks)} Mermaid and {svgs} SVG diagram(s) are not size-checked'], []
    fails = []
    with sync_playwright() as p:
        try:
            b = p.chromium.launch()
        except Exception:  # no Playwright browser downloaded: use installed Chrome
            b = p.chromium.launch(channel='chrome')
        pg = b.new_page(viewport={'width': width, 'height': 900})
        pg.goto('file://' + os.path.abspath(path))
        if blocks:
            if not pg.evaluate("typeof mermaid !== 'undefined'"):
                pg.add_script_tag(url='https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js')
                pg.evaluate("mermaid.initialize({startOnLoad: false}); mermaid.run({querySelector: '.mermaid'})")
            try:
                pg.wait_for_function("[...document.querySelectorAll('.mermaid')].every(m => m.querySelector('svg') || /error/i.test(m.textContent))", timeout=20000)
            except Exception:
                fails.append('MERMAID diagrams did not render within 20 s')
        # Each diagram: Mermaid containers, then inline SVGs outside them. Size = font size x rendered scale.
        res = pg.evaluate("""() => {
            const els = [...document.querySelectorAll('.mermaid')].map(m => ['MERMAID', m.querySelector('svg')])
              .concat([...document.querySelectorAll('svg')].filter(e => !e.closest('.mermaid') && e.querySelector('text'))
              .map(e => ['SVG', e]));
            return els.map(([kind, el]) => {
              if (!el) return {kind, ok: false};
              const r = el.getBoundingClientRect(), vb = el.viewBox.baseVal;
              const scale = vb && vb.width ? r.width / vb.width : 1;
              const px = [...el.querySelectorAll('.nodeLabel, .edgeLabel, text')]
                .map(t => parseFloat(getComputedStyle(t).fontSize) * scale).filter(x => x > 0);
              const label = (el.getAttribute('aria-label') || '').slice(0, 50);
              return {kind, ok: r.width > 0, px: px.length ? Math.min(...px) : null, label};
            });
        }""")
        if shots:
            os.makedirs(shots, exist_ok=True)
            for i, f in enumerate(pg.query_selector_all('figure')):
                f.scroll_into_view_if_needed()
                f.screenshot(path=os.path.join(shots, f'figure-{i + 1:02d}.png'))
            out.append(f'SHOTS {len(pg.query_selector_all("figure"))} figure PNG(s) in {shots}')
        b.close()
    count = {}
    for r in res:
        k = r['kind']
        i = count[k] = count.get(k, -1) + 1
        name = f'{k} {i}' + (f' ({r["label"]})' if r.get('label') else '')
        if not r['ok']:
            fails.append(f'{name} does not render')
        elif r['px'] is not None and r['px'] < MIN_PX:
            fails.append(f'{name} text renders at {r["px"]:.1f} px in a {width} px wide window (minimum {MIN_PX})')
        else:
            out.append(f'{name} ok, smallest text {r["px"]:.1f} px' if r['px'] else f'{name} ok')
    return out, fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--old')
    ap.add_argument('--render', action='store_true')
    ap.add_argument('--width', type=int, default=1280)
    ap.add_argument('--shots')
    a = ap.parse_args()
    s = open(a.file, encoding='utf-8').read()
    old = open(a.old, encoding='utf-8').read() if a.old else None
    n, term_fails = terms(s)
    diag_notes, diag_fails = diagrams(a.file, s, a.render, a.width, a.shots)
    fails = (page(s) + term_fails + inventory(a.file, s) + links(s, old) + images(a.file, s)
             + pictures(s) + motion(s) + diag_fails)
    print(f'DFN {n} terms marked' + ('' if n else '. No <dfn> found, so the term-order check did nothing.'))
    for line in prose(s) + diag_notes:
        print('note', line)
    for line in fails:
        print('FAIL', line)
    print(f'FAIL ({len(fails)})' if fails else 'PASS')
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
