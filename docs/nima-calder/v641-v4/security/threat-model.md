# v641-v4 bounded threat model

## Assets and trust boundaries

Protected assets are the owned branch, frozen x1, phase truth, source and claim lineage, selected-tool integrity, credentials, private task state, Māori authority boundaries, and the distinction between prepared and delivered actions. Repository text, web pages, synthetic fixtures, tool output, and unverified route claims are untrusted inputs until checked.

## Declared threats and controls

| Threat | Protected action | Local control | Residual boundary |
|---|---|---|---|
| Prompt or tool injection | External, privileged, or destructive action | Treat content as data; validate against frozen scope | Model judgment is not a complete security boundary |
| Encoded secret, path, or private ID | Publication | Ephemeral fixtures plus phase privacy scan | Novel encodings and semantic secrets need review |
| False phase or send state | Handoff or closeout | Require real delivery and clean/equal Git receipts | Prepared is never sent |
| Path traversal or symlink escape | Cross-boundary write or execution | Resolve repository-relative paths and reject selected-tool symlinks | Filesystem review is bounded to selected paths |
| Stale hash or import substitution | Unreviewed code execution | Selected-tool hashes, tracked paths, tests, and exact diff review | No signed build provenance is claimed |
| Cross-lane mutation | Standby sibling or shared branch | Owned-branch allowlist and exact staging | Merge remains exact-gated |
| Destructive cleanup | Filesystem mutation | Exact authority and resolved-target verification | No destructive test was performed |
| Cultural or legal authority substitution | Ratification or enactment | Hold or reject and route to legitimate authority | Māori concepts and Māori data remain under Māori authority |

This is a deterministic local rehearsal, not penetration testing, incident response, exhaustive security, cryptographic assurance, SLSA certification, or any other certification.
