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
sharing project state and code-cache namespaces. The release audit also corrected
denial precedence: explicit owner rules,
quoted task limits and partial refusals outrank the ordinary-read shortcut.
Four regression tests cover the fix and the retained ordinary-read exemption.
`tools/assets.py` is the author's asset editor from
the same development tree. The additional public examples are newly written
synthetic fixtures, not evidence of measured model accuracy.

The included source is licensed under Apache License 2.0. Python, Codex, Nix,
Git, Gitleaks and hosted
model services are separate dependencies with their own licenses and terms;
this repository does not bundle their implementations or grant service access.

The release candidate uses Apache License 2.0 at the owner's direction. Earlier
local commits retain their historical MIT license, fixture host labels and
implementation comments about unpublished experiments. Those commits contain
no private development history or provider recordings; they have not been
rewritten. Current fixtures use generic identifiers and current comments do not
claim measured model accuracy from unpublished experiments.
