---
sop_id: SOP-EK-004
title: Lieferantenpreise in den Shop-Export übernehmen
version: 1.0
created: 2026-05-20
owner_role: Einkauf
language: de
source: new
status: approved
tools: [Excel, Shop-Backend, Lieferanten-Preisliste (CSV), E-Mail]
---

# SOP: Lieferantenpreise in den Shop-Export übernehmen

## Zweck & Ziel
Neue Lieferantenpreise werden zweimal im Jahr (Frühjahr/Herbst) in den Shop-Export übernommen, damit Verkaufspreise und Einkaufspreise im Shop stimmen. Fertig ist die Aufgabe, wenn der aktualisierte Export ohne Fehler ins Shop-Backend importiert wurde.

## Geltungsbereich
Gilt für alle Artikel des Hauptlieferanten. Nicht enthalten: Aktionspreise und Bundles.

## Voraussetzungen
Excel geöffnet, Lieferanten-Preisliste als CSV im Eingangsordner, aktueller Shop-Export als CSV, Zugang zum Shop-Backend.

## Schritte
1. Preisliste öffnen und auf Dubletten und fehlende EAN prüfen (Filter in Excel). Auffälligkeiten per E-Mail an den Lieferanten.
2. Per SVERWEIS die neuen Einkaufspreise in den Shop-Export ziehen.
3. UVP gegen Einkaufspreis prüfen; jede Zeile mit UVP unter EK markieren und dem Einkaufsleiter melden.
4. Export als CSV speichern und im Shop-Backend importieren; Import-Protokoll auf Fehler prüfen.

## Definition of Done
Import-Protokoll ohne Fehlerzeilen; Stichprobe von fünf Artikeln im Shop zeigt die neuen Preise.
