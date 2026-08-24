# Orphan-lane root and retained startup failures

## Decision

The user explicitly requested a completely blank r3 branch and worktree. The implementation is an orphan Git branch in the existing repository, not a second repository and not a shallow copy. Before x1 it has no parent commit, no tracked file, and no inherited checkout. The exact r2 final remains the read-only continuity source. This is a deliberate non-ancestral continuity model and must be described as such in every receipt.

## Sparse-state recovery

The new branch had no tree to materialize, so its orphan state already began at zero files. An interrupted startup wrapper nevertheless persisted a non-cone owner-only sparse allowlist before it stopped emitting a receipt. Later state inspection discovered that live setting when the first gitattributes stage was rejected as outside the list. The recovery extended the exact allowlist by one root file and used sparse-aware exact staging. No sibling path was added, checked out, scanned, or mutated. The 2,000-file ceiling remains an additional materialization control.

## Retained startup witnesses

- R3-F001: combined fresh-equality wrapper returned no receipt. Recovery: recovered by separate local upstream tracking and live scalar probes. Credit: zero for the failed route.
- R3-F002: assumed r2 common-builder filename was absent. Recovery: recovered by exact owner-scoped filename discovery. Credit: zero for the failed route.
- R3-F003: assumed r2 exact-final filename was absent. Recovery: recovered by exact owner-scoped filename discovery. Credit: zero for the failed route.
- R3-F004: PowerShell exact-preflight expression had a parser error. Recovery: recovered by a scalar command sequence with explicit exit capture. Credit: zero for the failed route.
- R3-F005: first worktree-lock invocation omitted its required path. Recovery: recovered by inspecting created state before the exact-path lock. Credit: zero for the failed route.
- R3-F006: combined pip-index metadata wrapper emitted no receipt within its bound. Recovery: recovered through the official PyPI JSON API. Credit: zero for the failed route.
- R3-F007: reuse candidate lacked a compatible Windows wheel. Recovery: rejected before download and replaced by pipx. Credit: zero for the failed route.
- R3-F008: package-json-validator candidate exposed a library rather than the requested CLI. Recovery: rejected before install and replaced by package-json-validator-cli. Credit: zero for the failed route.
- R3-F009: npm web page access returned 403 for dependency-cruiser. Recovery: recovered through official npm metadata and primary repository material. Credit: zero for the failed route.
- R3-F010: npm web page access returned 403 for jscpd. Recovery: recovered through official npm metadata and primary repository material. Credit: zero for the failed route.
- R3-F011: npm web page access returned 403 for package-json-validator. Recovery: recovered through official npm metadata and primary repository material. Credit: zero for the failed route.
- R3-F012: npm web page access returned 403 for license-checker-rseidelsohn. Recovery: recovered through official npm metadata and primary repository material. Credit: zero for the failed route.
- R3-F013: npm web page access returned 403 for sherif. Recovery: recovered through official npm metadata and primary repository material. Credit: zero for the failed route.
- R3-F014: browser safety filter rejected direct npm registry URL for dependency-cruiser. Recovery: recovered through npm view metadata. Credit: zero for the failed route.
- R3-F015: browser safety filter rejected direct npm registry URL for jscpd. Recovery: recovered through npm view metadata. Credit: zero for the failed route.
- R3-F016: browser safety filter rejected direct npm registry URL for package-json-validator. Recovery: recovered through npm view metadata. Credit: zero for the failed route.
- R3-F017: browser safety filter rejected direct npm registry URL for license-checker-rseidelsohn. Recovery: recovered through npm view metadata. Credit: zero for the failed route.
- R3-F018: browser safety filter rejected direct npm registry URL for sherif. Recovery: recovered through npm view metadata. Credit: zero for the failed route.
- R3-F019: first x1 build privacy scan matched its own credential-rule literal. Recovery: recovered by splitting the literal without weakening the compiled scanner. Credit: zero for the failed route.
- R3-F020: post-test PowerShell state wrapper repeated an invalid parenthesized command expression. Recovery: recovered by assigning each scalar probe before JSON composition. Credit: zero for the failed route.
- R3-F021: first gitattributes stage was outside the sparse pattern persisted by an earlier interrupted wrapper. Recovery: recovered by inspecting live sparse state, extending the exact allowlist, and staging with the sparse flag. Credit: zero for the failed route.

## Root-history contract

The x1 commit must be the root commit and have zero parents. The evidence commit must be its direct child. The final seal must be the direct child of evidence. No merge is allowed. The r2 source hash is recorded in documents but must not appear as an ancestor. Fresh live equality is required after each push. These properties are different from the inherited three-child pattern and therefore receive their own tests.

## Boundaries

This method does not prove repository completeness, privacy completeness, accessibility completeness, exhaustive security, production readiness, professional validation, legal or cultural compliance, Maori authority, independent reproduction, empirical science, consciousness, personhood, a Theory of Everything, or Stage 20. It is an owner-local Git and documentation control only.
