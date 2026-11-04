"""Prove the clear-explanation verifier. Usage (from the repo root):
uv run --python 3.13 --with playwright python3 test/clear-explanation/run.py [--update]

1. Each folder in fixtures/ must give exactly the FAIL lines in its expected.txt (--update rewrites them).
2. Each mutation copies fixtures/good, breaks one thing, and must give exactly the listed FAIL tags.
"""
import os, re, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, '..', '..', 'skills', 'clear-explanation', 'scripts', 'lint.py')
FIX = os.path.join(HERE, 'fixtures')

# (name, file, regex, replacement, FAIL tags expected in order)
MUTATIONS = [
    ('title too long', 'explainer.html', r'<title>.*?</title>', '<title>How the nightly photo backup works</title>', ['TITLE']),
    ('no summary', 'explainer.html', r'(</h1>\n)<p>.*?</p>', r'\1', ['NO SUMMARY'] + ['NO DFN'] * 4),
    ('section opens without question', 'explainer.html', r'What happens on one real night\? ', '', ['NO QUESTION']),
    ('term used before dfn', 'explainer.html', r'every night, so', 'every night with a backup disk, so', ['EARLY']),
    ('dfn not in inventory', 'explainer.html', r'<dfn>log file</dfn>', '<dfn>log</dfn>', ['DRIFT', 'NO DFN']),
    ('broken anchor', 'explainer.html', r'</main>', '<a href="#nowhere">x</a></main>', ['BROKEN']),
    ('missing image', 'explainer.html', r'log\.png', 'gone.png', ['MISSING']),
    ('no alt', 'explainer.html', r' alt="[^"]*"', '', ['NO ALT']),
    ('data URI image', 'explainer.html', r'src="log\.png"', 'src="data:image/png;base64,AAAA"', ['DATA URI']),
    ('section without picture', 'explainer.html', r' data-no-picture="[^"]*"', '', ['PLAN', 'NO PICTURE']),
    ('bad no-picture reason', 'explainer.html', r'one sentence says it as fast', 'cannot capture it', ['BAD REASON']),
    ('figure without caption', 'explainer.html', r'<figcaption>Only photos.*?</figcaption>', '', ['NO CAPTION']),
    ('empty figure', 'explainer.html', r'<img [^>]*>', '<p>Screenshot to come</p>', ['EMPTY figure']),
    ('autoplay', 'explainer.html', r'go\(i\+1\);\}\)\(\);', 'go(i+1);setInterval(()=>go(i+1),2000);})();', ['AUTOPLAY']),
    ('video without controls', 'explainer.html', r'</main>', '<video src="log.png" muted></video></main>', ['NO CONTROLS']),
    ('stepper without Back', 'explainer.html', r'>Back<', '>Prev<', ['NO BACK/NEXT']),
    ('no reduced motion', 'explainer.html', r'@media \(prefers-reduced-motion: reduce\)\{.*?\}\}', '', ['NO REDUCED MOTION']),
    ('diagram text too small', 'explainer.html', r'font-size="18"', 'font-size="7"', ['SVG']),
    ('no inventory', 'inventory.md', None, None, ['NO INVENTORY']),
    ('wrong columns', 'inventory.md', r'\| Lives \| Status', '| Status | Lives', ['COLUMNS']),
    ('empty cell', 'inventory.md', r'\| crontab -l \|', '| — |', ['EMPTY cell']),
    ('bad status', 'inventory.md', r'\| exists \| backup\.sh', '| 2 KB | backup.sh', ['STATUS']),
    ('duplicate Name', 'inventory.md', r'\| log file \| text', '| backup disk | text', ['DUP Name', 'DRIFT']),
    ('no picture plan', 'inventory.md', r'## Picture plan.*', '', ['NO PLAN']),
    ('plan kind invalid', 'inventory.md', r'\| real output \|', '| photo |', ['PLAN']),
    ('plan none but figure', 'inventory.md', r'\| diagram \|', '| none |', ['PLAN']),
    ('German question passes', 'explainer.html', r'What happens on one real night\? ', 'Was passiert in einer echten Nacht? ', []),
    ('German no-picture excuse', 'explainer.html', r'one sentence says it as fast', 'kein Zugriff auf den Bildschirm', ['BAD REASON']),
    ('plan row missing', 'inventory.md', r'\| One night \|[^\n]*\n', '', ['PLAN']),
]


def fails(html, render=True):
    r = subprocess.run([sys.executable, LINT, html] + (['--render'] if render else []), capture_output=True, text=True)
    lines = r.stdout.splitlines()
    last = lines[-1] if lines else r.stderr
    assert (r.returncode == 0) == (last == 'PASS'), f'exit code {r.returncode} disagrees with last line {last!r}'
    return [l[5:] for l in lines if l.startswith('FAIL ') and not re.match(r'FAIL \(\d+\)$', l)]


def main():
    bad = 0
    for name in sorted(os.listdir(FIX)):
        exp_path = os.path.join(FIX, name, 'expected.txt')
        got = fails(os.path.join(FIX, name, 'explainer.html'))
        if '--update' in sys.argv:
            open(exp_path, 'w', encoding='utf-8').write(''.join(l + '\n' for l in got))
        exp = open(exp_path, encoding='utf-8').read().splitlines() if os.path.exists(exp_path) else []
        ok = got == exp
        bad += not ok
        print(f'{"ok  " if ok else "BAD "} fixture {name}: {len(got)} FAIL' + ('' if ok else f'\n  expected {exp}\n  got      {got}'))
    for name, f, pat, rep, tags in MUTATIONS:
        d = tempfile.mkdtemp()
        for x in os.listdir(os.path.join(FIX, 'good')):
            if x != 'expected.txt':
                shutil.copy(os.path.join(FIX, 'good', x), d)
        p = os.path.join(d, f)
        if pat is None:
            os.remove(p)
        else:
            s = open(p, encoding='utf-8').read()
            t = re.sub(pat, rep, s, count=1, flags=re.S)
            assert t != s, f'mutation {name!r} changed nothing'
            open(p, 'w', encoding='utf-8').write(t)
        got = fails(os.path.join(d, 'explainer.html'), )
        ok = [g.split(' ')[0] for g in got] == [t.split(' ')[0] for t in tags] and all(g.startswith(t) for g, t in zip(got, tags))
        bad += not ok
        print(f'{"ok  " if ok else "BAD "} mutation {name}' + ('' if ok else f'\n  expected tags {tags}\n  got {got}'))
        shutil.rmtree(d)
    print('PASS' if not bad else f'FAIL ({bad})')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
