# Initial publication plan

Nothing in this plan authorizes publication. Obtain the owner's explicit OK for
the exact final commit, repository name, license and public Git author metadata
before creating a public repository, pushing, or creating a release.

Proposed repository: `yerbolgmailcom/toolreview`, public, MIT licensed.

1. Finish local regression tests, the Python 3.11/3.14 checks, asset round-trip,
   secret scan and review of every tracked file. Confirm executable and symlink
   modes, a clean working tree, and a clean public history. Inspect author metadata
   with `git log --format=fuller`; an email in that history will become public.
   If author metadata changes, obtain approval for the resulting commit instead.
2. After approval, create an **empty** repository: do not generate a README,
   license or gitignore on GitHub. Attach only the intended repository as remote.
3. Push only the approved commit from `release/initial-public` to `main`, using
   the explicit refspec `release/initial-public:main`. Do not use `--all`,
   `--mirror`, or a remote pointing to the private development repository.
4. Enable private vulnerability reporting before announcing the repository and
   verify the reporting route. Check GitHub Actions for the exact approved SHA.
   If CI fails, prepare fixes locally/on a feature branch and obtain approval
   before another push. Do not tag a failing or unreviewed commit.
5. Once checks pass and release approval covers the exact SHA, create the
   `v0.1.0` experimental release pointing at that commit. Include the validation
   scope and limitations from CHANGELOG.md and docs/SECURITY.md; add the actual
   hosted CI result without implying live model accuracy or complete interception.

The initial release has no fresh live-provider evaluation and no complete agent
session interception test. Publication must not describe it as a validated
security boundary. The installed private reviewer and personal website are
outside this publication operation.
