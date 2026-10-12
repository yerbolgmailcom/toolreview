# Changelog

## 0.1.0 — initial experimental release

First clean public export of the experimental tool-call reviewer.

- One executable with 25 embedded assets, including 193 offline unit tests.
- Configurable classifier, resolver and Codex profile; no personal endpoints.
- Review cascade with task limits, partial approvals, delegated scope, and audit
  records. Explicit owner rules, quoted task limits and partial refusals now
  outrank the ordinary-read shortcut; unrelated ordinary reads still require
  no task-specific scope grant. Four regression tests cover this ordering.
- Trust-helper config writes preserve permission bits and symlinks; new files
  default to mode 0600, with five regression tests.
- Invocation-name aliases share one executable with separate config/state/cache
  namespaces; independent stable/experimental worktrees share Git history, with
  one installed reviewer per project. Private settings remain external. Launcher regression tests
  verify this behavior without changing an installed profile.
- Setup guidance, data-flow and integration limitations, Apache License 2.0,
  synthetic evaluation examples, pinned Nix dev shell, and GitHub Actions tests.

### Local validation

- All 193 offline unit tests pass on Python 3.14; the embedded suite also passes
  on Python 3.11 in the pinned Nix shell.
- All 25 assets survive split/join byte-identically; shell syntax passes.
- Gitleaks scans of the candidate directory and full public Git history report
  no detected secrets; no private session exports are included.
- Installed Codex CLI 0.159.2 registers, lists and removes all five hook definitions
  in a disposable project/profile. This checks integration registration, not a
  live agent session or complete host interception coverage.
- A synthetic hook event with unavailable local providers returns a native JSON
  denial without a traceback; no proposed action is executed.
- The two synthetic evaluation cases load and construct review scopes. They have
  not been run against live providers. No fresh model-accuracy claim is made.

These are local prepublication checks. Hosted CI results belong to the exact
release commit and must pass before tagging; they are not implied by this list.
