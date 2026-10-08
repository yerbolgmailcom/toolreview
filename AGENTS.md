# toolreview public repository

The executable is a self-contained shell script with 25 verbatim embedded assets.
Use tools/assets.py split/join to edit; never duplicate runtime code in projects.
Run ./toolreview test and syntax-check only the shell section before exit.
Use the pinned Nix flake for additional development tools.

Keep fixtures synthetic and offline unit tests free of provider calls. Never add
personal configuration, transcripts, raw evaluation runs or credentials. Live
model evaluations are distinct from unit tests and require an intended provider
configuration. Test installation in disposable profiles/projects. Switching the
maintainer's installed executable requires an explicit migration request (the
owner authorized the initial single-source/private-overlay migration).

Keep code changes on feature branches and commit coherent work promptly. Do not
leave completed changes uncommitted; report remaining work explicitly. Inspect
and test a public release before pushing; no private development history belongs
in this repository. Keep security limitations and data-flow documentation aligned
with actual behavior. CLAUDE.md is a symlink to this canonical instruction file.

Maintainer instruction for this release: obtain explicit OK before any push, public
repository creation, or GitHub release. Local preparation and commits are authorized.

The public repository is the only maintained executable source. Keep personal
settings, prompts, private evaluations and historical development outside it.
Command aliases select config/state/cache by invocation name, not by the resolved
source filename. Run tools/test_aliases.py when changing launcher behavior. Do not
create a private runtime fork or copy code into the personal overlay.
