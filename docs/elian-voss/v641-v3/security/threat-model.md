# v641-v3 bounded threat model

## Assets and trust boundaries

Protected assets are the owned branch, phase truth, source provenance, credentials, private task state, Māori authority boundaries, and the distinction between prepared and delivered actions. External content, repository text, web pages, synthetic fixtures, and unverified route claims are untrusted inputs.

## Declared threats and controls

| Threat | Protected action | Local control | Residual boundary |
|---|---|---|---|
| Prompt or tool injection | External or destructive action | Treat content as data; validate against user scope | Model judgment is not a complete security boundary |
| Encoded secret or private ID | Publication | Ephemeral fixtures plus public-artifact scanner | Novel encodings and semantic secrets need review |
| False phase or send state | Handoff or closeout | Require real delivery and clean/equal Git receipts | Prepared is never sent |
| Dependency tampering | Code execution | Pinned source, review, and test before execution | No supply-chain certification is claimed |
| Cross-lane mutation | Sibling or shared branch | Owned-branch allowlist and exact staging | Merge remains exact-gated |
| Destructive cleanup | Filesystem mutation | Exact authority and resolved-target checks | No destructive test was performed |
| Cultural or legal authority substitution | Ratification or enactment | Hold/reject and route to legitimate authority | Māori concepts and data remain under Māori authority |

This is a deterministic local rehearsal, not penetration testing, incident response, exhaustive security, or certification.
