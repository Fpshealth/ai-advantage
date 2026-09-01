#!/usr/bin/env python3
"""grade.py <en|de|static> <sandbox-dir> <result-text-file> — asserts on the escalation output."""
import glob, json, os, re, subprocess, sys

mode, sandbox, result_path = sys.argv[1:4]
result = open(result_path, encoding="utf-8").read() if os.path.exists(result_path) else ""
repo = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
skill = open(os.path.join(repo, "skills/escalation/SKILL.md"), encoding="utf-8").read()
static_url = re.search(r"\((mailto:[^)]+)\)", skill).group(1)

fails = []
def check(name, ok, evidence=""):
    print(("  PASS " if ok else "  FAIL ") + name + (f"  [{evidence}]" if evidence and not ok else ""))
    if not ok: fails.append(name)

handoffs = glob.glob(os.path.join(sandbox, "**", "escalation-handoff*.md"), recursive=True)
check("exactly one handoff file", len(handoffs) == 1, f"found {len(handoffs)}")
handoff = open(handoffs[0], encoding="utf-8").read() if handoffs else ""
if handoffs:
    loc = os.path.relpath(os.path.dirname(handoffs[0]), sandbox)
    if loc != "03_Output": print(f"  WARN handoff placed in {loc}/ (expected 03_Output/)")
check("handoff has >= 5 sections", len(re.findall(r"^#{1,3} ", handoff, re.M)) >= 5)
check("handoff quotes the blocker (SG-2012)", "SG-2012" in handoff)
check("handoff lists the input file", "supplier-price-list-spring-2026.csv" in handoff)

urls = re.findall(r"mailto:[^)\s>]+", result)
url = urls[0] if urls else ""
check("mailto link present", bool(url))
check("address + subject tag correct", url.startswith("mailto:federico.pacheco@fpshealth.com?subject=%5BEscalation%3A%20Team-AI%5D"), url[:80])
check("URL fully encoded", url != "" and not re.search(r"[ À-ɏ\[\]]", url))
check("guide says draft / not sent", re.search(r"draft|entwurf", result, re.I) is not None)
check("guide says only Send sends", re.search(r"\bsend\b|senden|absenden", result, re.I) is not None)
check("no claim the email was sent", re.search(r"(email|e-mail|mail) (has been|was) sent|ich habe .* gesendet", result, re.I) is None)

if mode == "en":
    check("$ survives encoding (%2439.90)", "%2439.90" in url, url[-120:])
    check("Claude Code route: /export offered", "/export" in result)
    check("handoff has tools trace section", re.search(r"tools|actions", handoff, re.I) is not None)
    # cold read by a fresh model: could a consultant resume from the file alone?
    prompt = ("You are a consultant receiving this handoff file from a client's stuck AI session. "
              "Judge ONLY the file. Answer with JSON {\"resumable\": true|false, \"missing\": [..]} — "
              "resumable=true if you could take over without asking the client anything.\n\n---\n" + handoff)
    try:
        out = subprocess.run(["claude", "-p", "--output-format", "json", "--max-turns", "1",
                              "--disallowedTools", "Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill", "Agent"],
                             input=prompt, capture_output=True, text=True, timeout=180).stdout
        verdict = json.loads(out).get("result", "")
        m = re.search(r"\{.*\}", verdict, re.S)
        v = json.loads(m.group(0)) if m else {}
        check("cold read: consultant could resume", v.get("resumable") is True, str(v.get("missing"))[:200])
    except Exception as e:
        check("cold read: consultant could resume", False, f"grader error: {e}")
elif mode == "de":
    check("umlaut encoded (enth%C3%A4lt)", "enth%C3%A4lt" in url, url[-160:])
    check("handoff is German", re.search(r"Preisliste|Ziel|Dateien", handoff) is not None)
    check("reply is German", re.search(r"Entwurf|Berater", result) is not None)
elif mode == "static":
    check("no-code rung: static link verbatim, or hand-encoded umlaut survives",
          static_url in result or "enth%C3%A4lt" in url, url[-160:])
    check("reply is German", re.search(r"Entwurf|Berater", result) is not None)

print(f"  -> {mode}: {len(fails)} failure(s)")
sys.exit(1 if fails else 0)
