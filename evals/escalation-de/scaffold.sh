#!/usr/bin/env bash
# Builds the AI_SANDBOX layout the skills expect, in the run's working directory.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/../.." && pwd)"
mkdir -p 01_Input 02_Work 03_Output
cp "$REPO"/test/fixtures/*.csv 01_Input/
cp "$REPO/skills/sandbox-setup/reference/sandbox-claude-template.md" CLAUDE.md
