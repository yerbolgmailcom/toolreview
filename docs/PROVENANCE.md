# Source provenance

Toolreview was developed by Yerbol Akhmetbekov, with assistance from AI coding
agents. This repository starts with a clean public export. It does not include
the private development Git history, personal prompts, machine configuration,
provider-call recordings, or evaluations derived from private sessions.

The exported executable derives from the author's reviewer snapshot
`15b93d9` (promoted October 7, 2026), whose original executable SHA-256 is
`e50a59699eb7ea1c656f4560ecf1114d750c607654b7a0c3056c68c30cc8eafb`.
The implementation began in the author's earlier `hv-reviewer` work and was
consolidated into this self-contained script. Historical `toolreview:` comments
mark changes made during that development; they are not third-party copyrights.

Public-export changes include generic comments, help paths and synthetic test
identifiers, plus a legacy test fixture's endpoint/model. Pre-release review also
fixed the trust helper's config writes to preserve file modes and symlinks, and
added five offline regression tests. The launcher also selects its instance by
invocation name so multiple command aliases can share one executable without
sharing config/state/cache namespaces. The runtime review-decision logic is
unchanged. `tools/assets.py` is the author's asset editor from
the same development tree. The additional public examples are newly written
synthetic fixtures, not evidence of measured model accuracy.

The included source is MIT licensed. Python, Codex, Nix, Git, Gitleaks and hosted
model services are separate dependencies with their own licenses and terms;
this repository does not bundle their implementations or grant service access.
