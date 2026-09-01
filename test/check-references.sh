#!/usr/bin/env bash
# Structural check for the plugin's reference files. Run from anywhere; no arguments.
#
# Guards the two failure classes that broke the plugin in the field (2026-08-05):
#   1. A SKILL.md pointing at a reference file that does not exist inside its own
#      skill folder (skills are self-contained after install — the plugin cache
#      copies each skill folder as-is, so a file only present at repo root is
#      unreachable from the skill's point of view on some clients).
#   2. Symlinks inside skills/ — symlink handling in the plugin cache and in the
#      Enterprise "Sync from GitHub" path is not battle-hardened (see
#      anthropics/claude-code#53948) and Windows extraction often turns symlinks
#      into text stubs. Shared files are therefore materialized as real copies,
#      and this check keeps the copies byte-identical to the canonical file in
#      reference/ at the repo root.

set -euo pipefail
cd "$(dirname "$0")/.."

fail=0

# 1. No symlinks anywhere under skills/
while IFS= read -r link; do
  echo "FAIL symlink not allowed in skills/: $link"
  fail=1
done < <(find skills -type l)

# 2. Every reference/<file>.md mentioned in a SKILL.md exists as a regular file
#    inside that same skill folder
for skill_md in skills/*/SKILL.md; do
  sk_dir=$(dirname "$skill_md")
  while IFS= read -r ref; do
    if [ ! -f "$sk_dir/$ref" ]; then
      echo "FAIL missing reference: $sk_dir/$ref (mentioned in $skill_md)"
      fail=1
    fi
  done < <(grep -o 'reference/[A-Za-z0-9._-]*\.md' "$skill_md" | sort -u)
  while IFS= read -r ref; do
    if [ ! -f "$sk_dir/$ref" ]; then
      echo "FAIL missing script: $sk_dir/$ref (mentioned in $skill_md)"
      fail=1
    fi
  done < <(grep -o 'scripts/[A-Za-z0-9._-]*\.[a-z]*' "$skill_md" | sort -u)
  while IFS= read -r ref; do
    if [ ! -f "$sk_dir/$ref" ]; then
      echo "FAIL missing asset: $sk_dir/$ref (mentioned in $skill_md)"
      fail=1
    fi
  done < <(grep -o 'assets/[A-Za-z0-9._-]*\.[a-z]*' "$skill_md" | sort -u)
done

# 3. Per-skill copies of canonical shared files match the repo-root originals
for canon in reference/*.md; do
  base=$(basename "$canon")
  for copy in skills/*/reference/"$base"; do
    [ -e "$copy" ] || continue
    if ! cmp -s "$canon" "$copy"; then
      echo "FAIL copy drifted from canon: $copy != $canon"
      fail=1
    fi
  done
done

if [ "$fail" -eq 0 ]; then
  echo "OK — all skill references resolve, no symlinks, no drift."
fi
exit "$fail"
