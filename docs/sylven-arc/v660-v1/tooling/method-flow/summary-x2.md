# GHC Family Method Flow State

- Phase: v660-v1
- Owner: Sylven Arc
- Methods: 44
- Passing witnesses: 44
- Failed witnesses retained: 124

## Preferred methods

### V6601-X1-METHOD-001 — Bounded recovery for startup-assumed-method-flow-schema-filename-instead-of-skill-declared-schema-path

- Trigger: startup-assumed-method-flow-schema-filename-instead-of-skill-declared-schema-path
- Method: Retain the FileNotFoundException and read the exact skill-declared references/schema.md through EOF.
- Recurrence guard: Retain the FileNotFoundException and read the exact skill-declared references/schema.md through EOF.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-001-F, V6601-X1-METHOD-001-P

### V6601-X1-METHOD-002 — Bounded recovery for source-manifest-inspection-piped-directly-from-a-powershell-foreach-block

- Trigger: source-manifest-inspection-piped-directly-from-a-powershell-foreach-block
- Method: Retain the empty-pipe parser rejection and materialize foreach output before ConvertTo-Json.
- Recurrence guard: Retain the empty-pipe parser rejection and materialize foreach output before ConvertTo-Json.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-002-F, V6601-X1-METHOD-002-P

### V6601-X1-METHOD-003 — Bounded recovery for overbroad-source-script-inventory-exceeded-output-budget

- Trigger: overbroad-source-script-inventory-exceeded-output-budget
- Method: Retain the truncated inventory and enumerate exact v659_v8 basenames with bounded filters.
- Recurrence guard: Retain the truncated inventory and enumerate exact v659_v8 basenames with bounded filters.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-003-F, V6601-X1-METHOD-003-P

### V6601-X1-METHOD-004 — Bounded recovery for recurrence-guard-was-not-applied-before-a-second-direct-foreach-pipeline

- Trigger: recurrence-guard-was-not-applied-before-a-second-direct-foreach-pipeline
- Method: Retain the repeated parser fault separately and use a mandatory materialized-row template for later projections.
- Recurrence guard: Retain the repeated parser fault separately and use a mandatory materialized-row template for later projections.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-004-F, V6601-X1-METHOD-004-P

### V6601-X1-METHOD-005 — Bounded recovery for first-manifest-coverage-probe-used-the-wrong-final-delta-base-and-phase-only-owner-scope

- Trigger: first-manifest-coverage-probe-used-the-wrong-final-delta-base-and-phase-only-owner-scope
- Method: Retain the false coverage result and replay hashes once, then compare correction delta and declared owner scope separately.
- Recurrence guard: Retain the false coverage result and replay hashes once, then compare correction delta and declared owner scope separately.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-005-F, V6601-X1-METHOD-005-P

### V6601-X1-METHOD-006 — Bounded recovery for corrected-python-manifest-coverage-wrapper-returned-no-attributable-output

- Trigger: corrected-python-manifest-coverage-wrapper-returned-no-attributable-output
- Method: Retain the empty wrapper and recover only the two unresolved coverage predicates with bounded PowerShell.
- Recurrence guard: Retain the empty wrapper and recover only the two unresolved coverage predicates with bounded PowerShell.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-006-F, V6601-X1-METHOD-006-P

### V6601-X1-METHOD-007 — Bounded recovery for source-final-owner-manifest-selector-omitted-the-phase-specific-novelty-probe

- Trigger: source-final-owner-manifest-selector-omitted-the-phase-specific-novelty-probe
- Method: Preserve Elowen's immutable manifest scope omission; verify the x1 manifest hash and identical x1/final Git blob without rewriting source.
- Recurrence guard: Preserve Elowen's immutable manifest scope omission; verify the x1 manifest hash and identical x1/final Git blob without rewriting source.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-007-F, V6601-X1-METHOD-007-P

### V6601-X1-METHOD-008 — Bounded recovery for combined-lane-collision-remote-and-free-space-wrapper-returned-no-evidence

- Trigger: combined-lane-collision-remote-and-free-space-wrapper-returned-no-evidence
- Method: Retain the empty wrapper and run local branch, remote branch, path, registry, and drive-space probes separately.
- Recurrence guard: Retain the empty wrapper and run local branch, remote branch, path, registry, and drive-space probes separately.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-008-F, V6601-X1-METHOD-008-P

### V6601-X1-METHOD-009 — Bounded recovery for worktree-add-tool-returned-before-the-large-internal-checkout-finished

- Trigger: worktree-add-tool-returned-before-the-large-internal-checkout-finished
- Method: Preserve the initializing lock, wait for the original Git process to exit, and do not unlock or mutate the partial checkout.
- Recurrence guard: Preserve the initializing lock, wait for the original Git process to exit, and do not unlock or mutate the partial checkout.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-009-F, V6601-X1-METHOD-009-P

### V6601-X1-METHOD-010 — Bounded recovery for premature-full-status-during-initializing-produced-a-multimegabyte-truncated-deletion-view

- Trigger: premature-full-status-during-initializing-produced-a-multimegabyte-truncated-deletion-view
- Method: Retain the truncated status, wait for checkout completion, then use scalar head, branch, diff, and untracked probes.
- Recurrence guard: Retain the truncated status, wait for checkout completion, then use scalar head, branch, diff, and untracked probes.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-010-F, V6601-X1-METHOD-010-P

### V6601-X1-METHOD-011 — Bounded recovery for recursive-worktree-file-count-monitor-returned-no-attributable-output

- Trigger: recursive-worktree-file-count-monitor-returned-no-attributable-output
- Method: Retain the empty monitor and poll only the exact Git process and registry lock state.
- Recurrence guard: Retain the empty monitor and poll only the exact Git process and registry lock state.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-011-F, V6601-X1-METHOD-011-P

### V6601-X1-METHOD-012 — Bounded recovery for combined-post-materialization-head-branch-and-status-wrapper-returned-no-evidence

- Trigger: combined-post-materialization-head-branch-and-status-wrapper-returned-no-evidence
- Method: Retain the empty wrapper and use separate scalar head and branch checks.
- Recurrence guard: Retain the empty wrapper and use separate scalar head and branch checks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-012-F, V6601-X1-METHOD-012-P

### V6601-X1-METHOD-013 — Bounded recovery for combined-staged-and-unstaged-diff-wrapper-returned-no-evidence

- Trigger: combined-staged-and-unstaged-diff-wrapper-returned-no-evidence
- Method: Retain the empty wrapper and run each quiet diff with its own explicit exit receipt.
- Recurrence guard: Retain the empty wrapper and run each quiet diff with its own explicit exit receipt.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-013-F, V6601-X1-METHOD-013-P

### V6601-X1-METHOD-014 — Bounded recovery for source-preregistration-inspection-guessed-a-nonexistent-proposals-json-path

- Trigger: source-preregistration-inspection-guessed-a-nonexistent-proposals-json-path
- Method: Retain the FileNotFoundException, enumerate the exact directory, and use proposal-ledger.json.
- Recurrence guard: Retain the FileNotFoundException, enumerate the exact directory, and use proposal-ledger.json.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-014-F, V6601-X1-METHOD-014-P

### V6601-X1-METHOD-015 — Bounded recovery for raw-text-search-over-a-minified-frozen-chain-index-overflowed-the-output-budget

- Trigger: raw-text-search-over-a-minified-frozen-chain-index-overflowed-the-output-budget
- Method: Retain the truncated one-line output and parse the index structurally before emitting matched IDs and titles.
- Recurrence guard: Retain the truncated one-line output and parse the index structurally before emitting matched IDs and titles.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-015-F, V6601-X1-METHOD-015-P

### V6601-X1-METHOD-016 — Bounded recovery for first-twenty-title-novelty-screen-rejected-one-generic-authority-perimeter-draft

- Trigger: first-twenty-title-novelty-screen-rejected-one-generic-authority-perimeter-draft
- Method: Retain the rejected draft at zero credit, replace noun substitution with an empty-chair authority circuit, and rerun the same twenty-title screen.
- Recurrence guard: Retain the rejected draft at zero credit, replace noun substitution with an empty-chair authority circuit, and rerun the same twenty-title screen.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-016-F, V6601-X1-METHOD-016-P

### V6601-X1-METHOD-017 — Bounded recovery for quote-heavy-stale-template-rg-expression-was-misparsed-by-powershell-before-python-compilation-ran

- Trigger: quote-heavy-stale-template-rg-expression-was-misparsed-by-powershell-before-python-compilation-ran
- Method: Retain the PowerShell command-construction fault, split the stale-label scan from compilation, and use a single-quoted bounded search expression.
- Recurrence guard: Retain the PowerShell command-construction fault, split the stale-label scan from compilation, and use a single-quoted bounded search expression.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-017-F, V6601-X1-METHOD-017-P

### V6601-X1-METHOD-018 — Bounded recovery for first-workflow-plan-audit-mixed-one-active-assignment-with-the-terminally-gated-successor-assignment

- Trigger: first-workflow-plan-audit-mixed-one-active-assignment-with-the-terminally-gated-successor-assignment
- Method: Retain the needs-refinement packet at zero credit, keep Eiren in the bounded live override and terminal-successor fields, and rerun only the workflow dependency with the one-entry active assignment list.
- Recurrence guard: Retain the needs-refinement packet at zero credit, keep Eiren in the bounded live override and terminal-successor fields, and rerun only the workflow dependency with the one-entry active assignment list.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-018-F, V6601-X1-METHOD-018-P

### V6601-X1-METHOD-019 — Bounded recovery for repository-local-reflection-remaster-name-resolved-to-a-phase-tribunal-wrapper-instead-of-the-required-global-audit-runner

- Trigger: repository-local-reflection-remaster-name-resolved-to-a-phase-tribunal-wrapper-instead-of-the-required-global-audit-runner
- Method: Retain the wrong-runner output at zero credit and invoke the skill-bundled reflection audit by its exact absolute executable path with a bounded focus list.
- Recurrence guard: Retain the wrong-runner output at zero credit and invoke the skill-bundled reflection audit by its exact absolute executable path with a bounded focus list.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-019-F, V6601-X1-METHOD-019-P

### V6601-X1-METHOD-020 — Bounded recovery for first-x1-test-aggregate-treated-session-stream-prohibition-vocabulary-as-confirmed-private-material

- Trigger: first-x1-test-aggregate-treated-session-stream-prohibition-vocabulary-as-confirmed-private-material
- Method: Retain the 21-of-22 aggregate at zero aggregate credit, adjudicate only the exact blocked-packet and source-definition occurrences as protected-boundary vocabulary, and rerun the failed privacy dependency plus Method Flow count checks.
- Recurrence guard: Retain the 21-of-22 aggregate at zero aggregate credit, adjudicate only the exact blocked-packet and source-definition occurrences as protected-boundary vocabulary, and rerun the failed privacy dependency plus Method Flow count checks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-020-F, V6601-X1-METHOD-020-P

### V6601-X1-METHOD-021 — Bounded recovery for post-staged-review-combined-cleanliness-count-wrapper-returned-no-attributable-output

- Trigger: post-staged-review-combined-cleanliness-count-wrapper-returned-no-attributable-output
- Method: Retain the silent wrapper and the earlier passed staged receipt, then probe unstaged diff, untracked count, staged count, and head in separate scalar commands before committing.
- Recurrence guard: Retain the silent wrapper and the earlier passed staged receipt, then probe unstaged diff, untracked count, staged count, and head in separate scalar commands before committing.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6601-X1-METHOD-021-F, V6601-X1-METHOD-021-P

### V6601-X2-METHOD-001 — Bounded contract and mutation tribunal for marionette-intake-custody-passport

- Trigger: V6601-P001
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-001-F01, V6601-X2-METHOD-001-F02, V6601-X2-METHOD-001-F03, V6601-X2-METHOD-001-F04, V6601-X2-METHOD-001-F05, V6601-X2-METHOD-001-P

### V6601-X2-METHOD-002 — Bounded contract and mutation tribunal for marionette-suspension-graph

- Trigger: V6601-P002
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-002-F01, V6601-X2-METHOD-002-F02, V6601-X2-METHOD-002-F03, V6601-X2-METHOD-002-F04, V6601-X2-METHOD-002-F05, V6601-X2-METHOD-002-P

### V6601-X2-METHOD-003 — Bounded contract and mutation tribunal for puppet-articulation-map

- Trigger: V6601-P003
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-003-F01, V6601-X2-METHOD-003-F02, V6601-X2-METHOD-003-F03, V6601-X2-METHOD-003-F04, V6601-X2-METHOD-003-F05, V6601-X2-METHOD-003-P

### V6601-X2-METHOD-004 — Bounded contract and mutation tribunal for stage-frame-blocking-graph

- Trigger: V6601-P004
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-004-F01, V6601-X2-METHOD-004-F02, V6601-X2-METHOD-004-F03, V6601-X2-METHOD-004-F04, V6601-X2-METHOD-004-F05, V6601-X2-METHOD-004-P

### V6601-X2-METHOD-005 — Bounded contract and mutation tribunal for marionette-quantity-envelope

- Trigger: V6601-P005
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-005-F01, V6601-X2-METHOD-005-F02, V6601-X2-METHOD-005-F03, V6601-X2-METHOD-005-F04, V6601-X2-METHOD-005-F05, V6601-X2-METHOD-005-P

### V6601-X2-METHOD-006 — Bounded contract and mutation tribunal for puppet-association-lineage

- Trigger: V6601-P006
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-006-F01, V6601-X2-METHOD-006-F02, V6601-X2-METHOD-006-F03, V6601-X2-METHOD-006-F04, V6601-X2-METHOD-006-F05, V6601-X2-METHOD-006-P

### V6601-X2-METHOD-007 — Bounded contract and mutation tribunal for marionette-cue-stack-machine

- Trigger: V6601-P007
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-007-F01, V6601-X2-METHOD-007-F02, V6601-X2-METHOD-007-F03, V6601-X2-METHOD-007-F04, V6601-X2-METHOD-007-F05, V6601-X2-METHOD-007-P

### V6601-X2-METHOD-008 — Bounded contract and mutation tribunal for puppet-sweep-quarantine

- Trigger: V6601-P008
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-008-F01, V6601-X2-METHOD-008-F02, V6601-X2-METHOD-008-F03, V6601-X2-METHOD-008-F04, V6601-X2-METHOD-008-F05, V6601-X2-METHOD-008-P

### V6601-X2-METHOD-009 — Bounded contract and mutation tribunal for marionette-repair-lineage

- Trigger: V6601-P009
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-009-F01, V6601-X2-METHOD-009-F02, V6601-X2-METHOD-009-F03, V6601-X2-METHOD-009-F04, V6601-X2-METHOD-009-F05, V6601-X2-METHOD-009-P

### V6601-X2-METHOD-010 — Bounded contract and mutation tribunal for puppet-bitemporal-assertions

- Trigger: V6601-P010
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-010-F01, V6601-X2-METHOD-010-F02, V6601-X2-METHOD-010-F03, V6601-X2-METHOD-010-F04, V6601-X2-METHOD-010-F05, V6601-X2-METHOD-010-P

### V6601-X2-METHOD-011 — Bounded contract and mutation tribunal for puppet-timed-text-companion

- Trigger: V6601-P011
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-011-F01, V6601-X2-METHOD-011-F02, V6601-X2-METHOD-011-F03, V6601-X2-METHOD-011-F04, V6601-X2-METHOD-011-F05, V6601-X2-METHOD-011-P

### V6601-X2-METHOD-012 — Bounded contract and mutation tribunal for marionette-parallel-language-labels

- Trigger: V6601-P012
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-012-F01, V6601-X2-METHOD-012-F02, V6601-X2-METHOD-012-F03, V6601-X2-METHOD-012-F04, V6601-X2-METHOD-012-F05, V6601-X2-METHOD-012-P

### V6601-X2-METHOD-013 — Bounded contract and mutation tribunal for puppet-package-scitt-profile

- Trigger: V6601-P013
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-013-F01, V6601-X2-METHOD-013-F02, V6601-X2-METHOD-013-F03, V6601-X2-METHOD-013-F04, V6601-X2-METHOD-013-F05, V6601-X2-METHOD-013-P

### V6601-X2-METHOD-014 — Bounded contract and mutation tribunal for gmut-constrained-marionette-board

- Trigger: V6601-P014
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-014-F01, V6601-X2-METHOD-014-F02, V6601-X2-METHOD-014-F03, V6601-X2-METHOD-014-F04, V6601-X2-METHOD-014-F05, V6601-X2-METHOD-014-P

### V6601-X2-METHOD-015 — Bounded contract and mutation tribunal for gmut-marionette-mode-proxy

- Trigger: V6601-P015
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-015-F01, V6601-X2-METHOD-015-F02, V6601-X2-METHOD-015-F03, V6601-X2-METHOD-015-F04, V6601-X2-METHOD-015-F05, V6601-X2-METHOD-015-P

### V6601-X2-METHOD-016 — Bounded contract and mutation tribunal for thos-cue-map-trial-proxy

- Trigger: V6601-P016
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-016-F01, V6601-X2-METHOD-016-F02, V6601-X2-METHOD-016-F03, V6601-X2-METHOD-016-F04, V6601-X2-METHOD-016-F05, V6601-X2-METHOD-016-P

### V6601-X2-METHOD-017 — Bounded contract and mutation tribunal for thos-cue-debt-handover-proxy

- Trigger: V6601-P017
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-017-F01, V6601-X2-METHOD-017-F02, V6601-X2-METHOD-017-F03, V6601-X2-METHOD-017-F04, V6601-X2-METHOD-017-F05, V6601-X2-METHOD-017-P

### V6601-X2-METHOD-018 — Bounded contract and mutation tribunal for puppet-accessibility-evaluation-proxy

- Trigger: V6601-P018
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-018-F01, V6601-X2-METHOD-018-F02, V6601-X2-METHOD-018-F03, V6601-X2-METHOD-018-F04, V6601-X2-METHOD-018-F05, V6601-X2-METHOD-018-P

### V6601-X2-METHOD-019 — Bounded contract and mutation tribunal for real-marionette-evidence-gap

- Trigger: V6601-P019
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-019-F01, V6601-X2-METHOD-019-F02, V6601-X2-METHOD-019-F03, V6601-X2-METHOD-019-F04, V6601-X2-METHOD-019-F05, V6601-X2-METHOD-019-P

### V6601-X2-METHOD-020 — Bounded contract and mutation tribunal for marionette-empty-chair-authority

- Trigger: V6601-P020
- Method: Validate one synthetic fixture and reject all five declared mutations.
- Recurrence guard: Run only the exact frozen surface and retain every rejecting witness.
- Rollback: Stop, retain the witness, and leave real, sibling, external, and authority state unchanged.
- Witnesses: V6601-X2-METHOD-020-F01, V6601-X2-METHOD-020-F02, V6601-X2-METHOD-020-F03, V6601-X2-METHOD-020-F04, V6601-X2-METHOD-020-F05, V6601-X2-METHOD-020-P

### V6601-X2-METHOD-021 — Bounded recovery for first-x2-test-aggregate-found-the-overview-at-779-words-below-the-900-word-three-page-equivalent-floor

- Trigger: first-x2-test-aggregate-found-the-overview-at-779-words-below-the-900-word-three-page-equivalent-floor
- Method: Retain the 16-of-17 aggregate at zero aggregate credit, expand only the overview with evidence-semantics and falsifier detail, and rerun the document dependency plus affected truth and manifest checks.
- Recurrence guard: Retain the 16-of-17 aggregate at zero aggregate credit, expand only the overview with evidence-semantics and falsifier detail, and rerun the document dependency plus affected truth and manifest checks.
- Rollback: Stop, retain the failed aggregate at zero credit, and leave already successful components unchanged.
- Witnesses: V6601-X2-METHOD-021-F, V6601-X2-METHOD-021-P

### V6601-X2-METHOD-022 — Bounded recovery for meta-tool-box-validation-used-the-undeclared-receipt-flag-and-exited-before-validation

- Trigger: meta-tool-box-validation-used-the-undeclared-receipt-flag-and-exited-before-validation
- Method: Retain the argparse rejection at zero credit, inspect the exact subcommand help, and rerun only validation with the declared --output flag; require a valid bounded receipt before catalogue use.
- Recurrence guard: Retain the argparse rejection at zero credit, inspect the exact subcommand help, and rerun only validation with the declared --output flag; require a valid bounded receipt before catalogue use.
- Rollback: Stop, retain the failed aggregate at zero credit, and leave already successful components unchanged.
- Witnesses: V6601-X2-METHOD-022-F, V6601-X2-METHOD-022-P

### V6601-X2-METHOD-023 — Bounded recovery for isolated-x2-recovery-found-two-tests-hard-coded-the-prior-operational-failure-total

- Trigger: isolated-x2-recovery-found-two-tests-hard-coded-the-prior-operational-failure-total
- Method: Retain the two failed assertions at zero credit, derive operational, Method Flow, witness, and cumulative totals from the immutable failure lists, then rerun only the two affected tests and their manifest dependencies.
- Recurrence guard: Retain the two failed assertions at zero credit, derive operational, Method Flow, witness, and cumulative totals from the immutable failure lists, then rerun only the two affected tests and their manifest dependencies.
- Rollback: Stop, retain the failed aggregate at zero credit, and leave already successful components unchanged.
- Witnesses: V6601-X2-METHOD-023-F, V6601-X2-METHOD-023-P

## Retained boundary

Same-owner workflow and mutation evidence only; no independent reproduction or protected-gate closure.
