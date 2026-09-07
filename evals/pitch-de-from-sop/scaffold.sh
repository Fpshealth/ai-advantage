#!/usr/bin/env bash
# Builds the AI_SANDBOX layout the skills expect, with one finished SOP already in 03_Output.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
mkdir -p 01_Input 02_Work 03_Output
cp "$REPO/test/fixtures/sop-lieferantenpreise-2026-05-20.md" 03_Output/
cp "$REPO/skills/sandbox-setup/reference/sandbox-claude-template.md" CLAUDE.md
