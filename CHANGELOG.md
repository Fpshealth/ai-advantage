# Changelog — Cowork: Team-AI (plugin)

All notable changes to the plugin as a whole. Per-skill history lives in the consultant's own
version control, if any.

> **Versioning:** the plugin carries no explicit `version` field in `plugin.json` or
> `marketplace.json`. Claude Code falls back to the git commit SHA (or a fixed reference for a
> non-git distribution), so there is no manual bump. The version headings below are human
> release notes / milestones, not the installed version string.

## [1.0.0] — Initial release

### Added
- Full seven-skill set: Sandbox Setup, Prompt Improvement, Escalation, SOP Creation, Process
  Documentation, Process Exploration, Visualizer.
- Four dedicated agents: Fresh-Eyes Review, Process Explorer, Process Sparring Partner, Target
  Process Review.
- A one-file runtime re-skin seam — `## 0 — Client configuration` in `reference/house-style.md`
  — plus a full identifier-level rename checklist in the Consultant Guide.
- An end-to-end test scenario with fixtures (the Summit Gear storyline).
