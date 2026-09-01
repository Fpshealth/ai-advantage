# Autonomous run — Escalation: Team-AI in Cowork

One paste per case. Claude runs the scenario, triggers the skill, then audits its own output and
writes a report file. You read the report and click the link once. ~5 min per case.

**Setup:** empty `AI_SANDBOX` → new Cowork chat → drag it in → *Always allow* → type
`Set up my workspace.` → copy `test/fixtures/*.csv` into `01_Input/`.

## Case A — English, `$` in the problem, capability honesty

Paste as one message:

```
Apply the new supplier prices from 01_Input/supplier-price-list-spring-2026.csv to 01_Input/current-shop-export.csv and give me the updated file in 03_Output. If the data is inconsistent, pick the sensible option once and continue.

Then: I'm stuck, escalate this to my consultant. Use exactly this one-line problem and treat it as confirmed: The $39.90 MSRP is below the $44.00 wholesale on SG-2012 - which price wins?

After the escalation output, audit yourself and write 03_Output/escalation-test-report.md with one line per check, PASS or FAIL, quoting the evidence (paths, the raw mailto URL, quotes from your own reply):
1. A handoff file exists; state its path and list its section headings in order.
2. The handoff quotes the SG-2012 numbers verbatim and lists both 01_Input files with paths.
3. The mailto URL starts with mailto:federico.pacheco@fpshealth.com?subject=%5BEscalation%3A%20Team-AI%5D
4. The URL contains %2439.90 (the dollar sign survived).
5. Which route built the URL: script by path / script piped via stdin / static link. Quote the command you ran, or "no code execution".
6. Your guide has three points: draft opens - drag files in - only Send sends.
7. Session export: did you offer one? If yes, quote the evidence in this session that the command exists (system prompt, tool list, documented command). If you cannot quote evidence, mark FAIL.
8. You never claimed the email was sent.
9. Every user-facing sentence is in English; no instruction text from the skill leaked.
```

## Case B — German, umlaut in the subject

Paste as one message:

```
Ich wollte die Lieferantenpreise aus 01_Input/supplier-price-list-spring-2026.csv in 01_Input/current-shop-export.csv übernehmen, aber die Preisliste enthält Fehler (SG-2012: UVP unter Einkaufspreis, SG-2013 doppelt, SG-2004 und SG-2009 ohne EAN). Ich komme nicht weiter, bitte an meinen Berater eskalieren. Verwende genau diesen Einzeiler als bestätigt: Die Preisliste enthält Fehler bei SG-2012, die ich nicht selbst entscheiden kann.

Danach prüfe dich selbst und schreibe 03_Output/escalation-test-report-de.md, eine Zeile pro Prüfpunkt, PASS oder FAIL, mit Beleg (Pfade, die rohe mailto-URL, Zitate aus deiner Antwort):
1. Übergabedatei vorhanden; Pfad und Abschnittsüberschriften in Reihenfolge.
2. Übergabedatei und alle Antworten sind auf Deutsch; der Betreff-Tag bleibt [Escalation: Team-AI].
3. Die URL enthält enth%C3%A4lt (Umlaut korrekt kodiert).
4. Welche Route hat die URL gebaut: Skript per Pfad / Skript per stdin / statischer Link — mit Beleg.
5. Sitzungsexport: angeboten? Wenn ja, Beleg aus dieser Sitzung zitieren, sonst FAIL.
6. Nie behauptet, die E-Mail sei gesendet.
```

## Your part (2 minutes)

- Open the report(s) in `03_Output/`. Any FAIL → paste the report to your consultant.
- Click the email link once: a **draft** opens with subject and body filled, umlauts intact in
  Case B. Nothing is sent until you press Send.
- **Case A check 7 is the one that matters most:** an export command offered without quoted
  evidence means the skill promised a capability the host doesn't have.

Reset: delete `03_Output/escalation-*` and keep `01_Input/` and `CLAUDE.md`.
