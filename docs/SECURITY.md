# Boundaries and data flow

Toolreview is an experimental cooperative reviewer. It is not an OS sandbox,
malware detector, complete shell interpreter, or compliance control. Keep native
sandboxing, credential isolation and approval controls enabled. A model's
confidence score is not a proof, and using a second call to the same model does
not make that review independent.

## What leaves the machine

The configured classifier receives action and task context for typed judgments.
The configured resolver receives task/conversation context and review evidence
for scope extraction, uncertain decisions, and follow-up learning. Depending on
the hook and available context, this can include user messages, assistant replies,
command arguments, paths, scope rules and retained tool-output excerpts.

The default classifier is the hosted TypeSafe Jev API. A local resolver does not
make the entire workflow local. Review your providers' data policies and task
sensitivity before enabling hooks. Redaction is best effort and cannot promise
that arbitrary text contains no secret. The code attempts to withhold credential
material; do not treat this as comprehensive data-loss prevention.

To build this context, the adapter reads selected session transcripts from
`$CODEX_HOME/sessions/**/*.jsonl` and queries `goals_1.sqlite` read-only. Prompt
handling can start a detached `bullet_worker.py` resolver call after the hook
returns; worker errors are recorded in `.toolreview/bullet-worker.log`.

The project does not send separate analytics or telemetry. Model requests go to
the endpoints you configure; credential commands you configure run locally.

## Local storage

- `<project>/.toolreview/`: task state, review decisions, authority records and
  retained history. Treat it as sensitive; exclude it from version control.
- `~/.cache/toolreview/<script-name>/<sha256>/`: unpacked code. Old versions are
  pruned by recent use, retaining ten.
- `$XDG_RUNTIME_DIR/toolreview/`: classifier key cache, when a runtime directory
  is configured, using restrictive file permissions. It is only memory-backed
  if that directory is actually on tmpfs; otherwise use of this directory can
  write the cache to disk. Do not set it to an untrusted/shared directory.
- Selected `$CODEX_HOME/config.toml`: project and hook trust entries. Install
  modifies them; uninstall removes hook trust but retains project trust.
- Evaluation `runs/`: model request/response recordings and results. Do not
  upload them without a separate privacy review.

## Known limits

Ordinary local and remote reads generally do not require task-specific approval
and use lower confidence thresholds than changes. User-stated limits, credential
exposure, unsafe disclosure and reviewer tampering still apply. The policy does
not restrict all reads to files or resources explicitly named in a task.

Host versions differ in hook coverage, error handling, timeouts and tool names.
A native hook failure can fail open; persistent shell sessions and hosted tools
may not be fully intercepted. The reviewer's fail-closed decision policy does
not override host behavior. Exercise the integration in a disposable project
and verify that the actions you care about really invoke it.

Stored reviewer state and the executable can be altered by users with filesystem
access. Keeping code outside the project is useful isolation, not an immutable
security boundary. This initial release has not been validated for industrial or
other high-stakes deployment. The included tests use mocked models and do not
measure false-allow/false-deny rates on real workloads.

## Reporting a vulnerability

Use GitHub's private vulnerability reporting for this repository when enabled.
Do not post credentials, private transcripts or exploit details in a public
issue. If private reporting is unavailable, open an issue asking for a private
contact channel without including the sensitive details.
