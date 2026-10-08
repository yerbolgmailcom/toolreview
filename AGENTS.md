# toolreview public repository

The executable is a self-contained shell script with 25 verbatim embedded assets.
Use tools/assets.py split/join to edit; never duplicate runtime code in projects.
Run ./toolreview test and syntax-check only the shell section before exit.
Use the pinned Nix flake for additional development tools.

Keep fixtures synthetic and offline unit tests free of provider calls. Never add
personal configuration, transcripts, raw evaluation runs or credentials. Live
model evaluations are distinct from unit tests and require an intended provider
configuration. Do not install this release into the maintainer's working profile
while testing; use a disposable profile/project.

Keep code changes on feature branches and commit coherent work promptly. Do not
leave completed changes uncommitted; report remaining work explicitly. Inspect
and test a public release before pushing; no private development history belongs
in this repository. Keep security limitations and data-flow documentation aligned
with actual behavior. CLAUDE.md is a symlink to this canonical instruction file.

Maintainer instruction for this release: obtain explicit OK before any push, public
repository creation, or GitHub release. Local preparation and commits are authorized.
