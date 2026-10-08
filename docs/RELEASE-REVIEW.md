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
