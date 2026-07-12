# v641-v2 bounded threat model

## Scope and assets

This model covers Sable Rook's owned branch, the v641-v2 evidence artifacts, source and proposal ledgers, deterministic validators, Git route truth, and the eventual one-task sibling handoff. Protected assets include private material, credentials, raw task routes and identifiers, trustworthy phase truth, branch ownership, scientific uncertainty, legal and cultural authority, and recoverable evidence.

It is a bounded manual model with synthetic fixtures. It is not a penetration test, exhaustive Codex Security scan, dependency audit, or certification that the repository is secure.

## Principal threat paths

| Path | Consequence | Primary controls | Residual risk |
| --- | --- | --- | --- |
| Indirect prompt injection in sources or repository text | Scope drift or protected tool action | Treat external text as data; validate proposed action against Hamish's request; least authority | Novel encodings and operator error remain possible. |
| Private-material or secret exfiltration | Credential compromise or privacy harm | Do not embed raw prompts, credentials, transcripts, routes, screenshots, or local private paths; run secret/privacy scans | Pattern scanners cannot recognize every semantic secret. |
| Route spoofing | A prepared baton represented as sent | A send is `SENT` only after the task tool confirms it; store only sanitized state | Live tool or UI behavior may drift. |
| False phase truth | Premature closeout or downstream reliance | Require tests, checklist, exact diff review, clean push, and local/upstream/remote equality | A validator can encode the wrong rule. |
| Cross-lane mutation | Damage to Eiren or standing siblings | Owned branch and worktree checks; exact path and branch verification | Human command targeting remains a residual. |
| Dependency or tool-chain compromise | Unreviewed code execution | Standard library first; no automatic download or install; record versions; inspect diffs | Existing runtime and transitive Git tooling remain trusted dependencies. |
| Destructive recovery | Evidence loss | Preserve evidence; restore from a pinned clean commit; never use destructive Git cleanup | Storage or hardware failure is outside this local rehearsal. |
| Epistemic overclaim | Scientific, legal, identity, or governance harm | Typed dispositions, negative fixtures, evidence grades, expiry, and exact gates | Readers may ignore limitations. |
| Cultural appropriation | Māori authority displaced by project language | Route Māori data and concepts to Māori authority; retain Te Mana Raraunga boundary | This package has no mandate to speak for Māori authorities. |

## Recovery order

Stop protected actions; preserve sanitized evidence; downgrade unverified route claims; revoke real exposed credentials through the proper external authority; restore the pinned owned baseline; verify branch and heads; notify Hamish with bounded facts; and resume only when the relevant exact gate is satisfied.

The machine-readable red-team and recovery receipts are `red-team.json` and `recovery-drill.json`. No real secret, route, account, incident, or other sibling branch was manipulated to produce them.
