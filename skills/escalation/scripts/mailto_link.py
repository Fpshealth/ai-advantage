#!/usr/bin/env python3
"""Print a UTF-8-safe mailto URL. Hand-encoded mailto links break umlauts; this doesn't.

Usage:  mailto_link.py <address> <subject> <body>
Also runs from stdin (no file access needed):  python3 - <address> <subject> <body> <<'PY' ... PY
"""
import sys
import urllib.parse

address, subject, body = (a.strip() for a in sys.argv[1:4])
q = lambda s: urllib.parse.quote(s, safe="")
print(f"mailto:{address}?subject={q(subject)}&body={q(body)}")
