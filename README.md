# toolreview

A review layer for AI coding-agent actions, by Yerbol Akhmetbekov.

`toolreview` checks a proposed tool call against the task, its limits, and the
user's approvals before the host executes it. It combines checks in code,
focused judgments from a System One classifier (a model for narrow decisions),
and a separately configured LLM reviewer. It was developed for local coding models and integrates with Codex
through project hooks.

**Status: experimental, first public release.** This is a cooperative guardrail,
not a security sandbox or a guarantee that an action is safe. Keep the host's
sandbox and approval controls enabled. Model judgments can be wrong; host hook
failures or unsupported tool paths can leave gaps. See [boundaries and data
flow](docs/SECURITY.md).

## How it works

1. **Code checks** catch explicit credential material, protected reviewer paths,
   and ended scopes.
2. **Standing rules** ask focused Jev questions about the action.
3. **Task scope** relates the action to instructions, limits, and approvals,
   including partial approvals and scope delegated to a document.
4. **LLM review** interprets unresolved cases and checks cited authority.

Ordinary local and remote reads generally need no task-specific authorization
and use lower confidence thresholds than changes. Explicit user limits,
credential exposure, unsafe disclosure and reviewer tampering are still checked;
this is not a read-access allowlist.

Only uncertainty moves review to the next layer. A decisive result allows or
denies the action; an unresolved review returns a denial explaining what needs
clarification. This is the reviewer's decision policy, not a promise that the
host can never bypass or fail to run a hook.

The working agent, classifier, and reviewer LLM are separate roles. The agent is
configured in Codex; the other two are configured here. A replacement classifier
must implement the same typed question/answer protocol as Jev, not just a chat API.

## Requirements

- GNU/Linux, POSIX shell, GNU coreutils, awk, and Python 3.11 or newer.
- Codex CLI on PATH, with project hooks and `app-server hooks/list` support. The release
  was checked against `codex-cli 0.159.2`; other versions need validation.
- A [TypeSafe Jev](https://typesafe.ai/) API key (default classifier), or a
  compatible classifier service. Arrange service access separately; this release
  does not include credentials, provider credits or an access guarantee.
- An OpenAI-compatible chat-completions endpoint for the reviewer LLM. It can be
  local or hosted and can differ from the model used by the working agent.

Python code uses the standard library. No Python packages are required. A pinned
Nix development shell supplies testing tools; it does not install Codex or models.

## Try the tests first

```sh
git clone https://github.com/yerbolgmailcom/toolreview.git
cd toolreview
./toolreview test
```

The embedded unit tests mock model calls and require no API key. They establish
code behavior, not model accuracy or real-world safety.

## Configure

Copy [examples/config.example.toml](examples/config.example.toml) to
`~/.config/toolreview/config.toml`, or set `TOOLREVIEW_CONFIG` to another file.
Set the resolver URL and model to your actual service. Supply keys through the
named environment variables or a credential-manager command. Do not put key
values in the configuration file or command string.

```sh
./toolreview config
./toolreview config --check
```

`config --check` checks whether a classifier key is available and requests the
resolver's `/models` endpoint. It does **not** test a classifier decision or a
resolver completion. Missing model IDs are reported but do not currently fail
the check. Review the output before installing hooks.

Configuration precedence is environment → TOML file → defaults. Available
overrides: `TOOLREVIEW_CLASSIFIER_URL`, `TOOLREVIEW_CLASSIFIER_MODEL`,
`TOOLREVIEW_RESOLVER_URL`, `TOOLREVIEW_RESOLVER_MODEL`, and
`TOOLREVIEW_CODEX_HOME`. The default Codex profile is `$CODEX_HOME`, then
`~/.codex`. A separate local-agent profile must be selected explicitly if it
uses a different home.

## Enable for a project

Create `~/.local/bin/toolreview` as a symlink to the checked-out script and put
`~/.local/bin` on PATH. Keep the checkout outside the project the agent edits.
From the checkout, create the link (this refuses to overwrite an existing entry):

```sh
mkdir -p "$HOME/.local/bin"
ln -s "$PWD/toolreview" "$HOME/.local/bin/toolreview"
```

If that path already exists, inspect its target before changing it. Then, in a
disposable project first:

```sh
toolreview install
toolreview status
codex -c features.hooks=true
```

`install` runs the tests and configuration check, writes `.codex/hooks.json` and
`.toolreview/`, and registers project/hook trust in the selected Codex profile.
Inspect and back up existing hook files before using `--force`: that option
replaces them without a backup. Installation is not transactional: a trust
registration failure can leave the hook file in place. An existing untrusted
project entry must be resolved explicitly in Codex before installing.
Back up the selected profile's `config.toml` before the first installation.
The tool does not install dependencies or change the agent's model.

Code executes from a checksum-keyed cache outside the project. The project stores
review state and history. Add `.toolreview/` to the project's `.gitignore`.
Retain review data only as long as needed; it can contain sensitive task context.

```sh
toolreview uninstall          # remove hooks and hook trust; retain review history
# toolreview uninstall --purge  # also delete review history
```

Uninstall retains the Codex project's trust entry. Review that entry separately
if you no longer want the project trusted.

## Evaluate with your models

[examples/eval](examples/eval) contains a small synthetic allow/deny pair. It
illustrates the format; it is not a benchmark or a held-out safety evaluation.

```sh
./toolreview eval examples/eval --workers 1
```

This command makes real calls to your configured providers and may incur charges.
It evaluates proposed actions; it does not execute the commands in the fixtures.
Runs record the script hash, model configuration, decisions and provider calls
under `examples/eval/runs/` (ignored by Git). Keep these records private unless
reviewed for publication. Use `--replay RUN` to reuse recorded model responses,
or `eval --compare RUN_A RUN_B` to compare recorded outcomes.

## Development

The executable is one file: shell code, `exit`, then 25 verbatim code, schema,
hook and test assets. To edit embedded assets safely:

```sh
python3 tools/assets.py split toolreview /tmp/toolreview-edit
# Edit the relevant file under /tmp/toolreview-edit/assets/.
python3 tools/assets.py join /tmp/toolreview-edit toolreview
./toolreview test
```

`join` checks shell syntax and verifies every asset extracts byte for byte.
The Nix shell provides Python, coreutils, awk, Git and Gitleaks:
`nix develop -c ./toolreview test`. See [contributing](CONTRIBUTING.md).

Released under the [MIT license](LICENSE). See [provenance](docs/PROVENANCE.md)
for the clean source export and [release notes](CHANGELOG.md) for validation.
