#!/usr/bin/env bash
# Places the bloated fixture skill plus Matt Pocock's writing-for-agents text in the run's working directory.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p fixture-skill writing-for-agents
cp "$HERE/fixture/SKILL.md" fixture-skill/SKILL.md
cp "$HERE/fixture/writing-for-agents.md" writing-for-agents/SKILL.md
cp "$HERE/fixture/SKILL-MECHANICS.md" writing-for-agents/SKILL-MECHANICS.md
