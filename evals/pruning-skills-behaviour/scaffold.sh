#!/usr/bin/env bash
# Places the bloated fixture skill in the run's working directory.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p fixture-skill
cp "$HERE/fixture/SKILL.md" fixture-skill/SKILL.md
