---
name: skill-discovery
description: Search GitHub (live, via gh) and the SkillsMP index for agent skills matching a stated need; returns a ranked recommendation. Installing is a separate explicit step.
disable-model-invocation: true
---

# Skill Discovery

## Workflow

1. Clarify the need if vague: domain, task, target harness.
2. Run both search nets below.
3. Merge and dedupe; treat stars as a trust signal, not a cutoff.
4. Read the SKILL.md frontmatter of the top candidates.
5. Present a ranked table with a one-line fit reason each. The run ends here; installing starts only on an explicit pick.

## Net 1 — Live GitHub via gh

Requires authenticated `gh` (`gh auth status`); if unavailable, run Net 2 alone and say so.

Search repos by topic:

```bash
for t in claude-skills claude-code-skills agent-skills skill-md; do
  gh search repos --topic=$t --sort=stars --limit=25 --json fullName,description,stargazersCount
done
```

Catch untagged repos via code search, then stars via one GraphQL query:

```bash
repos=$(gh search code "<keyword>" --filename SKILL.md --limit 50 --json repository | jq -r '.[].repository.nameWithOwner' | sort -u)
query="{ "
i=0
while IFS= read -r repo; do
  owner="${repo%/*}"; name="${repo#*/}"
  query+="r$i: repository(owner: \"$owner\", name: \"$name\") { nameWithOwner stargazerCount description } "
  i=$((i+1))
done <<< "$repos"
query+="}"
gh api graphql -f query="$query" --jq '.data | to_entries[] | "\(.value.stargazerCount)\t\(.value.nameWithOwner) - \(.value.description // "no desc")"' | sort -t$'\t' -k1 -rn
```

## Net 2 — SkillsMP index

```bash
curl -s "https://skillsmp.com/api/v1/skills/search?q=<url-encoded-query>" | python3 -c "
import json,sys
d=json.load(sys.stdin)['data']
for s in d['skills']:
    print(s['stars'], '|', s['name'], '|', s['author'], '|', s['description'][:120], '|', s['githubUrl'])"
```

Free tier: 50 requests/day. On failure, say so and continue with Net 1 alone.

## Inspect a candidate

```bash
gh api repos/<owner>/<repo>/contents/<path>/SKILL.md --jq '.content' | base64 -d
```

For collection repos, list skills first:

```bash
gh api repos/<owner>/<repo>/contents/<skills-dir> --jq '.[].name'
```

## Output

Table: | Skill | Repo (★) | Fit for the need | Link |

Offer: view a candidate's full SKILL.md · refine the search · install.

## Install (only on explicit request)

Gate first: read the candidate's entire SKILL.md and any bundled scripts; flag install commands, network calls, and `-y`/global flags; check the repo license. Install only after the gate passes.

With git available (Claude Code): sparse-checkout keeps the skill tracked and updatable:

```bash
git clone --no-checkout --depth 1 --filter=blob:none https://github.com/<owner>/<repo> ~/.claude/skill-sources/<repo-name>
cd ~/.claude/skill-sources/<repo-name>
git sparse-checkout init --cone
git sparse-checkout set <path/to/skill-folder>
git checkout
ln -s ~/.claude/skill-sources/<repo-name>/<path>/<skill> ~/.claude/skills/<skill>
```

Without git tooling (e.g. Cowork): download the skill folder and place it in that environment's skills directory.
