# Prepublication review and resolution

Review date: October 8, 2026. Independent reviewer: Claude Code with
`claude-opus-5-5`, confirmed by the completed session's model metadata. The review
covered the clean public candidate, not the private development repository.
Codex assessed the findings and made the changes below. No publication or push
has been performed as part of this review.

## Accepted and addressed

- **Config permissions and symlinks:** the trust helper could replace a private
  config with a less restrictive file and replace managed symlinks. Writes now
  resolve the target, preserve its permission bits, default new files to 0600,
  use a unique temporary file and clean it up on failure. Five regression tests
  cover permissions, new files, symlinks, invalid TOML and failed replacement.
- **Read policy:** README and security guidance now disclose that ordinary reads
  generally require no task-specific authorization and have lower confidence
  thresholds. Explicit restrictions and sensitive-action checks still apply.
- **Data flow:** documented reads of session transcripts and the goals database,
  detached resolver work, and its error log.
- **Public fixtures and setup:** replaced remaining personal fixture identifiers,
  clarified Codex wording, explained the classifier dependency, supplied a
  non-overwriting symlink command and documented partial-install behavior.
- **Publishing plan:** records the exact-commit approval gate, empty repository
  creation, explicit branch refspec, public author metadata review, private
  vulnerability reporting, CI before tagging and unchanged private installation.
  Changelog validation wording no longer depends on an unreleased status.
- **Untested-module syntax:** CI now compiles every embedded Python module on each
  supported test version, in addition to unit tests and asset round-trip checks.

## Validation after corrections

- 189 offline unit tests pass on Python 3.14; the full embedded suite also passes
  on Python 3.11 in the pinned Nix development shell.
- All 25 assets round-trip byte-identically; shell syntax and Python compilation
  pass. Executable and CLAUDE.md symlink modes are correct; no empty tracked files.
- Codex CLI 0.159.2 registers, lists and removes all five hooks in a disposable
  project/profile with the corrected trust helper.
- A synthetic PreToolUse event through the executable with unavailable local
  providers returns the native JSON permission decision `deny`, without a
  traceback. No proposed tool action executes.
- Gitleaks reports no detected secrets in the release directory. Targeted checks
  confirm the reviewed personal fixture strings have been replaced.

## Limits and decisions

Opus performed a read-only review: its Read tool was denied, but it inspected
files through Grep. It did not run tests or perform a full policy audit. Its
report is advisory, not a security certification. Codex ran the checks above.
One detail in its suggested smoke test was corrected: this handled provider
failure produces a JSON denial with process exit 0, not an exit-2 failure.

Existing installation limits are documented, rather than expanded into an
installer rewrite: registration is not transactional; pre-existing untrusted
project entries need explicit resolution; --force does not back up foreign hooks;
uninstall retains project trust. Read-only or otherwise managed config targets
may reject writes; there is no attempt to bypass their management system.

Compatibility names in runtime security checks remain to preserve behavior.
No classifier/policy rewrite, new live-provider evaluation or complete agent-turn
interception test was added. Hosted CI and its Ubuntu awk implementation still
need their first run after the approved push. Action-version modernization can
follow evidence from that run. No full-system security guarantee is claimed.

## Follow-up: private configuration overlay

The owner subsequently requested one maintained public implementation with private
settings kept externally. The launcher now uses the invocation name for instance
selection. Two additional offline launcher tests verify that symlink aliases share
a source hash while keeping config/state/cache separate, that both aliases can
share one private config symlink, and that environment configuration overrides it.
These tests and the 189 embedded tests pass on Python 3.11 and 3.14. Assets still
round-trip byte-identically. Review-decision policy remains unchanged.

The owner clarified that stable and experimental must also have independent code
versions. The maintained installation therefore uses separate stable/experimental
Git worktrees and command targets, sharing one repository history. A shared
executable target is supported by the launcher but is not the owner's desired
stable/experimental deployment. Personal configuration remains external.

## Apache candidate audit — October 11, 2026

The owner selected Apache License 2.0. LICENSE uses the Apache Software
Foundation's canonical text; the executable SPDX header and current release
documentation agree. Earlier local commits retain their historical MIT license
and author metadata; no Git history was rewritten.

An independent read-only Codex review (gpt-6.1-sol) covered tracked public files,
all embedded assets, and the three preceding commits. It found a deterministic
denial-precedence bug: the ordinary-read shortcut returned before checking
explicit owner rules and quoted task limits. The release candidate now checks
those denials and explicit partial refusals before the shortcut. Four end-to-end
regressions cover the three denials and preserve ordinary unrelated reads without
a task-specific scope grant. The reviewer independently inspected this correction.

Current synthetic fixtures use generic host/skill labels. Unpublished numerical
model-evaluation claims were removed from implementation comments; this does not
change prompts or confidence thresholds. Historical commits retain earlier
labels/comments. The shared endpoint-keyed classifier credential-command cache
is documented as a limitation, with environment keys as the identity-specific
alternative. No broader credential-cache redesign was included.

Checks performed on the candidate:

- All 193 embedded unit tests and all three launcher/alias tests pass on Python
  3.14.7 and Python 3.11.16 (the pinned development shell).
- All 25 embedded assets extract and round-trip byte-identically. Shell syntax
  and compilation of every embedded Python module pass.
- Codex CLI 0.159.2 registers, trusts and lists all five hooks, then removes their
  definitions/trust in a disposable project/profile. Project trust and review
  history remain, matching the documentation. A local fake model-list server
  supplies setup validation; no real provider calls or installed-profile changes.
- Gitleaks reports no detected secrets in candidate files or reachable public Git
  history. File modes, symlinks and the publication tree are checked separately.

No live-provider evaluation, complete agent-session interception test, or hosted
CI run was performed. The review cannot independently prove original source
ownership. Stable remains unchanged pending explicit promotion/publication
approval; the candidate is on `release/apache-2.0`.
