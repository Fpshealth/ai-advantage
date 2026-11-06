#!/usr/bin/env bash
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
mkdir -p 01_Input 02_Work 03_Output
cp "$REPO/test/fixtures/sop-lieferantenpreise-2026-05-20.md" "$REPO"/test/fixtures/*.csv 01_Input/
cp "$REPO/skills/sandbox-setup/reference/sandbox-claude-template.md" CLAUDE.md
