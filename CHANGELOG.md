# Changelog — Cowork: Team-AI (plugin)

All notable changes to the plugin as a whole. Per-skill history lives in the consultant's own
version control, if any.

> **Versioning:** the plugin carries no explicit `version` field in `plugin.json` or
> `marketplace.json`. Claude Code falls back to the git commit SHA (or a fixed reference for a
> non-git distribution), so there is no manual bump. The version headings below are human
> release notes / milestones, not the installed version string.

## [1.2.2] — Prompt audit: intent-based descriptions, positive agent contracts

- Seven skill `description:` fields rewritten from quoted trigger-phrase lists to intent categories
  (escalation, process-documentation, process-exploration, prompt-improvement, sandbox-setup,
  sop-creation, visualizer). Unmeasured against a trigger eval; restore single phrases if a skill
  stops firing on one people use.
- All four agents close with a positive return contract instead of a "do not greet / ask / modify" list.
- Audit report: vault `⚙️ System/Claude/Reviews/Prompt Audit 2026-09-02.md`.

## [1.2.1] — Escalation: capability routes, script split out, autonomous tests

### Changed
- `escalation` (660 → 493 words): host differences are now two capability checks the skill
  confirms from evidence before offering anything — *session export* (attach it when the host
  has one; the handoff file is always the record) and *script by path* (else pipe the script via
  stdin; else the pre-encoded static link). No host is named as lacking anything, so a host that
  gains export is used without a skill edit. The mailto encoder lives in
  `skills/escalation/scripts/mailto_link.py` (address, subject, body → URL); the email body is
  `assets/email-body.md`, rendered in the person's language. Claude proposes the one-line
  problem; the 60-char subject cap and the hardcoded `03_Output/` path are gone.
- Description trimmed to triggers only.

### Added
- `test/claude-code/run.sh` + `grade.py`: headless Claude Code suite — English two-turn run
  (`$` encoding, `/export` route, cold-read grade by a fresh model), German run (umlaut
  encoding, language mirroring), Bash-disallowed German run (no-code rung: static link or a hand-encoded link whose umlaut survives).
- `test/cowork/RUN-IN-COWORK.md`: two paste-prompts; Claude self-audits into a report file,
  including whether an export command was offered with quoted evidence.
- `test/ESCALATION-TEST.md`: manual checklist (8 cases).
- `test/check-mailto.sh`: encoder round-trip (umlauts, newlines, `$`) + static-link-matches-§0.
- `test/check-references.sh` also checks `scripts/` and `assets/` mentions resolve.

## [1.2.0] — New skill: eli5

### Added
- `eli5`: explain any topic like I'm 5 — a dead-simple HTML picture explainer with big visuals
  and few words (`/eli5 <topic>`). Bundled here because Enterprise-managed Cowork can't install
  the community plugin directly. Sourced verbatim from `anthropics/claude-plugins-community`,
  author Thariq Shihipar, MIT license.

## [1.1.3] — Pruning pass: shorter skills, language mirroring everywhere

### Changed
- `sandbox-setup` (664 → 336 words) and `escalation` (909 → 693 words): pruned to operational
  content — duplications with house-style removed, scripted verbatim quote blocks replaced with
  content specs so replies are generated in the person's language instead of pasted in English.
- `reference/house-style.md` §1: language mirroring is now the primary rule and explicitly
  covers skill execution — a person writing German gets German questions, confirmations,
  warnings, and file contents; `client_language` is only the fallback until the person's
  language is clear. Escalation's mailto body is translated before encoding.

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
