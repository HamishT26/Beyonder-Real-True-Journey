# GHC Family Method Flow State

- Phase: v659-v1
- Owner: Ilyra Fen
- Methods: 13
- Passing witnesses: 12
- Failed witnesses retained: 13

## Preferred methods

### V6591-X1-METHOD-001 — Bounded recovery for broad-memory-registry-search-output-truncated

- Trigger: broad-memory-registry-search-output-truncated
- Method: Use one fixed keyword at a time, cap lines, and open only the one directly referenced rollout summary.
- Recurrence guard: Use one fixed keyword at a time, cap lines, and open only the one directly referenced rollout summary.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-001-F, V6591-X1-METHOD-001-P

### V6591-X1-METHOD-003 — Bounded recovery for powershell-python-c-quote-stripping-in-manifest-replay

- Trigger: powershell-python-c-quote-stripping-in-manifest-replay
- Method: Feed the unchanged ASCII verifier through python -X utf8 stdin and retain raw Git cat-file batch framing.
- Recurrence guard: Feed the unchanged ASCII verifier through python -X utf8 stdin and retain raw Git cat-file batch framing.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-003-F, V6591-X1-METHOD-003-P

### V6591-X1-METHOD-004 — Bounded recovery for external-canonical-receipt-filename-assumption-wrong

- Trigger: external-canonical-receipt-filename-assumption-wrong
- Method: Hash the bounded receipt directory and select the artifact by the supplied SHA-256 instead of guessing its filename.
- Recurrence guard: Hash the bounded receipt directory and select the artifact by the supplied SHA-256 instead of guessing its filename.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-004-F, V6591-X1-METHOD-004-P

### V6591-X1-METHOD-005 — Bounded recovery for combined-large-worktree-postflight-wrapper-returned-no-result

- Trigger: combined-large-worktree-postflight-wrapper-returned-no-result
- Method: Inspect concrete Git processes and locks, then split registration, index, status, and tracked-count probes.
- Recurrence guard: Inspect concrete Git processes and locks, then split registration, index, status, and tracked-count probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-005-F, V6591-X1-METHOD-005-P

### V6591-X1-METHOD-006 — Bounded recovery for worktree-add-progress-stream-ended-before-index-finalization

- Trigger: worktree-add-progress-stream-ended-before-index-finalization
- Method: Do not retry; inspect path, branch, HEAD, index lock, final index, process state, tracked count, and cleanliness until the original add completes.
- Recurrence guard: Do not retry; inspect path, branch, HEAD, index lock, final index, process state, tracked count, and cleanliness until the original add completes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-006-F, V6591-X1-METHOD-006-P

### V6591-X1-METHOD-007 — Bounded recovery for first-x1-build-rejected-semantic-neighbor-title-collisions

- Trigger: first-x1-build-rejected-semantic-neighbor-title-collisions
- Method: Retain the failed freeze attempt at zero credit, rewrite the astronomy proposals around domain-specific FITS, ephemeris, instrument-configuration, time-scale, and decision-right mechanisms, and rerun the unchanged all-title novelty gate before any x1 freeze.
- Recurrence guard: Retain the failed freeze attempt at zero credit, rewrite the astronomy proposals around domain-specific FITS, ephemeris, instrument-configuration, time-scale, and decision-right mechanisms, and rerun the unchanged all-title novelty gate before any x1 freeze.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-007-F, V6591-X1-METHOD-007-P

### V6591-X1-METHOD-008 — Bounded recovery for windows-rg-literal-wildcard-path-rejected

- Trigger: windows-rg-literal-wildcard-path-rejected
- Method: Pass each scripts directory as a literal search root and express the Python filename filter with rg -g '*.py'.
- Recurrence guard: Pass each scripts directory as a literal search root and express the Python filename filter with rg -g '*.py'.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-008-F, V6591-X1-METHOD-008-P

### V6591-X1-METHOD-009 — Bounded recovery for parallel-direct-py-entrypoints-returned-incomplete-artifact-set

- Trigger: parallel-direct-py-entrypoints-returned-incomplete-artifact-set
- Method: Invoke each Python skill entrypoint explicitly with python -X utf8, keep independent output directories, and verify the exact output inventory before credit.
- Recurrence guard: Invoke each Python skill entrypoint explicitly with python -X utf8, keep independent output directories, and verify the exact output inventory before credit.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-009-F, V6591-X1-METHOD-009-P

### V6591-X1-METHOD-010 — Bounded recovery for phase-request-output-supplied-to-special-packet-validator

- Trigger: phase-request-output-supplied-to-special-packet-validator
- Method: Use the workflow refinement engine self-test plus its generic phase-request validation receipt; reserve the special packet validator for its declared raw-audit and normalized-pass bundle layout.
- Recurrence guard: Use the workflow refinement engine self-test plus its generic phase-request validation receipt; reserve the special packet validator for its declared raw-audit and normalized-pass bundle layout.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-010-F, V6591-X1-METHOD-010-P

### V6591-X1-METHOD-011 — Bounded recovery for x1-source-ledger-test-referenced-nonexistent-source-specs-constant

- Trigger: x1-source-ledger-test-referenced-nonexistent-source-specs-constant
- Method: Inspect the frozen module's exact exported names, bind the unchanged row-count assertion to OFFICIAL_SOURCES, and rerun only the scoped x1 module.
- Recurrence guard: Inspect the frozen module's exact exported names, bind the unchanged row-count assertion to OFFICIAL_SOURCES, and rerun only the scoped x1 module.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-011-F, V6591-X1-METHOD-011-P

### V6591-X1-METHOD-012 — Bounded recovery for combined-staged-git-show-per-path-verifier-returned-no-receipt-at-timeout

- Trigger: combined-staged-git-show-per-path-verifier-returned-no-receipt-at-timeout
- Method: Split diff hygiene from content replay, build one staged index object map, and drain one bounded git cat-file --batch stream for JSON, manifest, and privacy checks.
- Recurrence guard: Split diff hygiene from content replay, build one staged index object map, and drain one bounded git cat-file --batch stream for JSON, manifest, and privacy checks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-012-F, V6591-X1-METHOD-012-P

### V6591-X1-METHOD-013 — Bounded recovery for first-batch-staged-replay-found-checkout-blob-domain-drift-and-scanner-definition-candidate

- Trigger: first-batch-staged-replay-found-checkout-blob-domain-drift-and-scanner-definition-candidate
- Method: Declare LF-normalized Git-clean manifest bytes, replay staged blobs in one batch, classify scanner-rule definitions as visible candidates, and require zero confirmed payload hits.
- Recurrence guard: Declare LF-normalized Git-clean manifest bytes, replay staged blobs in one batch, classify scanner-rule definitions as visible candidates, and require zero confirmed payload hits.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6591-X1-METHOD-013-F, V6591-X1-METHOD-013-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
