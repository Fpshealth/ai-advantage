# Changelog — Cowork: Team-AI (plugin)

All notable changes to the plugin as a whole. Per-skill history lives in the consultant's own
version control, if any.

> **Versioning:** the plugin carries no explicit `version` field in `plugin.json` or
> `marketplace.json`. Claude Code falls back to the git commit SHA (or a fixed reference for a
> non-git distribution), so there is no manual bump. The version headings below are human
> release notes / milestones, not the installed version string.

## [1.1.1] — Field fixes: sandbox setup, OneDrive guidance, export guidance, self-contained references

### Fixed
- `sandbox-setup`: restored `reference/sandbox-claude-template.md` inside the skill folder —
  the CLAUDE.md template the skill writes was lost in the port from the Bobshop plugin, so
  setup could not complete.
- `sandbox-setup`: the "no cloud-sync folders" rule now explains itself and steers to a safe
  local path. Cowork on Windows cannot reliably mount OneDrive Files-On-Demand folders
  (anthropics/claude-code#25293) and writing into them risks silent file truncation (#62140) —
  the skill now says why, warns that corporate Desktop/Documents are often OneDrive-synced
  (Known Folder Move), suggests `C:\Users\<name>\AI_SANDBOX`, and stops with a friendly
  redirect when the granted folder path is cloud-synced.
- `escalation`: export guidance is resilient to current Cowork builds — `/export` typed in the
  composer, with the Ctrl+K/⌘K palette and session ⋯ menu → Export as fallbacks; "exported
  folder" corrected to the archive Cowork actually produces; static mailto fallback re-encoded.
- All per-skill `reference/house-style.md` files are now real copies instead of git symlinks;
  symlinks do not reliably survive every distribution path (plugin-cache symlink regressions,
  Windows extraction turning links into text stubs).

### Added
- `test/check-references.sh` — structural check: every `SKILL.md` reference resolves inside
  its own skill folder, no symlinks under `skills/`, per-skill copies stay byte-identical to
  the `reference/` canon.

## [1.1.0] — Add pruning-skills and skill-discovery

### Added
- `skills/pruning-skills` — concision pass for tightening an existing skill to purely
  operational content.
- `skills/skill-discovery` — searches GitHub and the SkillsMP index for candidate skills;
  user-invocable only (`disable-model-invocation: true`), never auto-triggered by the model.

## [1.0.0] — Initial release

### Added
- Full seven-skill set: Sandbox Setup, Prompt Improvement, Escalation, SOP Creation, Process
  Documentation, Process Exploration, Visualizer.
- Four dedicated agents: Fresh-Eyes Review, Process Explorer, Process Sparring Partner, Target
  Process Review.
- A one-file runtime re-skin seam — `## 0 — Client configuration` in `reference/house-style.md`
  — plus a full identifier-level rename checklist in the Consultant Guide.
- An end-to-end test scenario with fixtures (the Summit Gear storyline).
