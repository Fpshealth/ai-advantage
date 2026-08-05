# Changelog — Cowork: Team-AI (plugin)

All notable changes to the plugin as a whole. Per-skill history lives in the consultant's own
version control, if any.

> **Versioning:** the plugin carries no explicit `version` field in `plugin.json` or
> `marketplace.json`. Claude Code falls back to the git commit SHA (or a fixed reference for a
> non-git distribution), so there is no manual bump. The version headings below are human
> release notes / milestones, not the installed version string.

## [1.1.2] — Streamline: no OneDrive caveats, handoff file is the whole escalation record

### Changed
- `sandbox-setup`: removed the "Always keep on this device" OneDrive tip — OneDrive guidance is
  now simply "anywhere is fine"; sync conflicts get handled if and when one actually occurs.
- `escalation`: removed the Settings → Privacy → Export data fallback entirely — on Enterprise
  plans only the org's Primary Owner can run data exports (support article 9450526), so members
  cannot use that path at all. The Claude-written handoff file is now the complete escalation
  record, extended with a "Tools & actions" section (skills invoked, code run, files
  read/written, searches) so the consultant gets a full debugging trace.

## [1.1.1] — Field fixes: sandbox setup, OneDrive guidance, export guidance, self-contained references

### Fixed
- `sandbox-setup`: restored `reference/sandbox-claude-template.md` inside the skill folder —
  the CLAUDE.md template the skill writes was lost in the port from the Bobshop plugin, so
  setup could not complete.
- `sandbox-setup`: `AI_SANDBOX` inside OneDrive is explicitly fine again — the port had
  introduced a "no cloud-sync folders" rule that broke the proven Bobshop workflow. The only
  remaining OneDrive note is a practical one: mark the folder "Always keep on this device" so
  on-demand placeholder files don't confuse the sandbox (anthropics/claude-code#62140).
- `escalation`: rewritten for current Cowork, which has no per-session `/export` (that's a
  Claude Code feature). Claude now writes a compact `03_Output/escalation-handoff.md` from full
  session context (goal, attempts, exact blocker verbatim, files) and the person emails that;
  the account-wide Settings → Privacy → Export data route (email link, whole account) is
  documented as an on-request fallback only. Mailto bodies and static link re-encoded.
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
