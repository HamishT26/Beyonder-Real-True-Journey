# GHC Family Method Flow State

- Phase: v661-v4
- Owner: Liora Venn
- Methods: 27
- Passing witnesses: 27
- Failed witnesses retained: 27

## Preferred methods

### V6614-X1-METHOD-001 — Bounded recovery for login-profile-read-only-wrappers-returned-no-attributable-output

- Trigger: login-profile-read-only-wrappers-returned-no-attributable-output
- Method: Retain the empty wrappers and use no-profile scalar commands with explicit exit and payload checks.
- Recurrence guard: Retain the empty wrappers and use no-profile scalar commands with explicit exit and payload checks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-001-F, V6614-X1-METHOD-001-P

### V6614-X1-METHOD-002 — Bounded recovery for broad-external-receipt-digest-content-scan-exceeded-bounded-supervision

- Trigger: broad-external-receipt-digest-content-scan-exceeded-bounded-supervision
- Method: Retain the bounded timeout, stop only the exact search helpers, and resolve the exact receipt path from the read-only source task before hashing it.
- Recurrence guard: Retain the bounded timeout, stop only the exact search helpers, and resolve the exact receipt path from the read-only source task before hashing it.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-002-F, V6614-X1-METHOD-002-P

### V6614-X1-METHOD-003 — Bounded recovery for first-selected-revalidation-invariant-projection-guessed-numeric-mutation-fields

- Trigger: first-selected-revalidation-invariant-projection-guessed-numeric-mutation-fields
- Method: Retain the false assumption and inspect the exact JSON keys and Boolean zero-credit semantics before evaluating the invariant.
- Recurrence guard: Retain the false assumption and inspect the exact JSON keys and Boolean zero-credit semantics before evaluating the invariant.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-003-F, V6614-X1-METHOD-003-P

### V6614-X1-METHOD-004 — Bounded recovery for powershell-selected-revalidation-detail-projection-used-an-empty-foreach-pipe

- Trigger: powershell-selected-revalidation-detail-projection-used-an-empty-foreach-pipe
- Method: Retain the parser rejection and materialize the result array before JSON conversion.
- Recurrence guard: Retain the parser rejection and materialize the result array before JSON conversion.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-004-F, V6614-X1-METHOD-004-P

### V6614-X1-METHOD-005 — Bounded recovery for powershell-manifest-detail-projection-used-an-empty-foreach-pipe

- Trigger: powershell-manifest-detail-projection-used-an-empty-foreach-pipe
- Method: Retain the parser rejection and collect manifest projections in an explicit array before conversion.
- Recurrence guard: Retain the parser rejection and collect manifest projections in an explicit array before conversion.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-005-F, V6614-X1-METHOD-005-P

### V6614-X1-METHOD-006 — Bounded recovery for per-entry-python-manifest-replay-completed-without-attributable-output

- Trigger: per-entry-python-manifest-replay-completed-without-attributable-output
- Method: Retain the silent replay at zero credit and use one communicate-style cat-file batch with an attributable structured summary.
- Recurrence guard: Retain the silent replay at zero credit and use one communicate-style cat-file batch with an attributable structured summary.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-006-F, V6614-X1-METHOD-006-P

### V6614-X1-METHOD-007 — Bounded recovery for first-batch-manifest-inline-python-f-string-lost-literal-quotes

- Trigger: first-batch-manifest-inline-python-f-string-lost-literal-quotes
- Method: Retain the syntax error and use quote-simple concatenation in the bounded batch transport.
- Recurrence guard: Retain the syntax error and use quote-simple concatenation in the bounded batch transport.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-007-F, V6614-X1-METHOD-007-P

### V6614-X1-METHOD-008 — Bounded recovery for guessed-phase-lifecycle-filename-was-absent

- Trigger: guessed-phase-lifecycle-filename-was-absent
- Method: Retain the missing-path assumption and list the exact bounded lifecycle directory before reading its actual anchor contract.
- Recurrence guard: Retain the missing-path assumption and list the exact bounded lifecycle directory before reading its actual anchor contract.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-008-F, V6614-X1-METHOD-008-P

### V6614-X1-METHOD-009 — Bounded recovery for powershell-command-discovery-projection-used-an-empty-foreach-pipe

- Trigger: powershell-command-discovery-projection-used-an-empty-foreach-pipe
- Method: Retain the parser rejection and materialize command-discovery rows before projection.
- Recurrence guard: Retain the parser rejection and materialize command-discovery rows before projection.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-009-F, V6614-X1-METHOD-009-P

### V6614-X1-METHOD-010 — Bounded recovery for workflow-summary-probe-guessed-two-absent-method-flow-filenames

- Trigger: workflow-summary-probe-guessed-two-absent-method-flow-filenames
- Method: Retain the guessed names and enumerate the exact method-flow directory before reading both state files.
- Recurrence guard: Retain the guessed names and enumerate the exact method-flow directory before reading both state files.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-010-F, V6614-X1-METHOD-010-P

### V6614-X1-METHOD-011 — Bounded recovery for source-task-reread-request-exceeded-the-live-per-item-output-limit

- Trigger: source-task-reread-request-exceeded-the-live-per-item-output-limit
- Method: Retain the rejected read-only request and retry once at the documented maximum without messaging the source task.
- Recurrence guard: Retain the rejected read-only request and retry once at the documented maximum without messaging the source task.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-011-F, V6614-X1-METHOD-011-P

### V6614-X1-METHOD-012 — Bounded recovery for eight-turn-source-task-projection-exceeded-the-output-budget

- Trigger: eight-turn-source-task-projection-exceeded-the-output-budget
- Method: Retain the truncated projection and request only the two newest turns before locally selecting agent messages.
- Recurrence guard: Retain the truncated projection and request only the two newest turns before locally selecting agent messages.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-012-F, V6614-X1-METHOD-012-P

### V6614-X1-METHOD-013 — Bounded recovery for combined-candidate-domain-powershell-projection-returned-no-attributable-output

- Trigger: combined-candidate-domain-powershell-projection-returned-no-attributable-output
- Method: Retain the silent projection and use a bounded UTF-8 Python JSON parser over the exact 3350-row chain.
- Recurrence guard: Retain the silent projection and use a bounded UTF-8 Python JSON parser over the exact 3350-row chain.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-013-F, V6614-X1-METHOD-013-P

### V6614-X1-METHOD-014 — Bounded recovery for temporary-file-digest-wrapper-was-rejected-before-execution

- Trigger: temporary-file-digest-wrapper-was-rejected-before-execution
- Method: Retain the policy rejection and compute the exact immutable blob digest in memory without a temporary file.
- Recurrence guard: Retain the policy rejection and compute the exact immutable blob digest in memory without a temporary file.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-014-F, V6614-X1-METHOD-014-P

### V6614-X1-METHOD-015 — Bounded recovery for python-unicode-repr-projection-hit-the-default-cp1252-encoder

- Trigger: python-unicode-repr-projection-hit-the-default-cp1252-encoder
- Method: Retain the encoding failure and pin PYTHONIOENCODING to UTF-8 before Unicode-emitting diagnostics.
- Recurrence guard: Retain the encoding failure and pin PYTHONIOENCODING to UTF-8 before Unicode-emitting diagnostics.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-015-F, V6614-X1-METHOD-015-P

### V6614-X1-METHOD-016 — Bounded recovery for first-data-patch-assumed-a-shifted-bare-current-owner-label

- Trigger: first-data-patch-assumed-a-shifted-bare-current-owner-label
- Method: Retain the rejected patch and reread the exact current lines before applying smaller verified hunks.
- Recurrence guard: Retain the rejected patch and reread the exact current lines before applying smaller verified hunks.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-016-F, V6614-X1-METHOD-016-P

### V6614-X1-METHOD-017 — Bounded recovery for first-category-patch-assumed-shifted-bare-source-labels

- Trigger: first-category-patch-assumed-shifted-bare-source-labels
- Method: Retain the rejected patch and patch exact bare labels only after a UTF-8 numbered reread.
- Recurrence guard: Retain the rejected patch and patch exact bare labels only after a UTF-8 numbered reread.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-017-F, V6614-X1-METHOD-017-P

### V6614-X1-METHOD-018 — Bounded recovery for first-stale-label-ripgrep-orchestration-script-had-an-extra-closing-parenthesis

- Trigger: first-stale-label-ripgrep-orchestration-script-had-an-extra-closing-parenthesis
- Method: Retain the JavaScript syntax rejection and rerun the same bounded read-only search with a syntactically checked wrapper.
- Recurrence guard: Retain the JavaScript syntax rejection and rerun the same bounded read-only search with a syntactically checked wrapper.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-018-F, V6614-X1-METHOD-018-P

### V6614-X1-METHOD-019 — Bounded recovery for first-novelty-probe-invocation-omitted-the-required-index-and-standard-input-title-array

- Trigger: first-novelty-probe-invocation-omitted-the-required-index-and-standard-input-title-array
- Method: Retain the argparse rejection and invoke the read-only probe with the immutable 3,350-row index plus the exact twenty preregistered titles on standard input.
- Recurrence guard: Retain the argparse rejection and invoke the read-only probe with the immutable 3,350-row index plus the exact twenty preregistered titles on standard input.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-019-F, V6614-X1-METHOD-019-P

### V6614-X1-METHOD-020 — Bounded recovery for first-x1-build-hit-a-sparse-checkout-missing-inherited-v659-v8-data-module

- Trigger: first-x1-build-hit-a-sparse-checkout-missing-inherited-v659-v8-data-module
- Method: Retain the import failure and add only the immutable tracked v659-v7/v659-v8 data dependency patterns to this owner worktree's sparse materialization before rebuilding.
- Recurrence guard: Retain the import failure and add only the immutable tracked v659-v7/v659-v8 data dependency patterns to this owner worktree's sparse materialization before rebuilding.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-020-F, V6614-X1-METHOD-020-P

### V6614-X1-METHOD-021 — Bounded recovery for first-sparse-checkout-add-used-an-unsupported-no-cone-option-on-the-add-subcommand

- Trigger: first-sparse-checkout-add-used-an-unsupported-no-cone-option-on-the-add-subcommand
- Method: Retain the usage rejection and add the two bounded patterns under the worktree's already-active non-cone mode without repeating that option.
- Recurrence guard: Retain the usage rejection and add the two bounded patterns under the worktree's already-active non-cone mode without repeating that option.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-021-F, V6614-X1-METHOD-021-P

### V6614-X1-METHOD-022 — Bounded recovery for first-materialized-novelty-gate-rejected-at-least-one-new-title-above-the-bounded-overlap-threshold

- Trigger: first-materialized-novelty-gate-rejected-at-least-one-new-title-above-the-bounded-overlap-threshold
- Method: Retain the rejected x1 build, inspect the exact prior and peer collision scores, and rename only colliding proposals without changing their preregistered mechanisms or expected truth labels.
- Recurrence guard: Retain the rejected x1 build, inspect the exact prior and peer collision scores, and rename only colliding proposals without changing their preregistered mechanisms or expected truth labels.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-022-F, V6614-X1-METHOD-022-P

### V6614-X1-METHOD-023 — Bounded recovery for first-corrected-novelty-pipeline-lost-python-string-quotes-and-fed-empty-input-to-the-probe

- Trigger: first-corrected-novelty-pipeline-lost-python-string-quotes-and-fed-empty-input-to-the-probe
- Method: Retain both attributable pipeline errors as one failed invocation and use a PowerShell-safe double-quoted Python program with single-quoted literals before rerunning the read-only probe.
- Recurrence guard: Retain both attributable pipeline errors as one failed invocation and use a PowerShell-safe double-quoted Python program with single-quoted literals before rerunning the read-only probe.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-023-F, V6614-X1-METHOD-023-P

### V6614-X1-METHOD-024 — Bounded recovery for mechanical-template-copy-materialized-untracked-x2-and-closeout-seeds-before-the-immutable-x1-boundary

- Trigger: mechanical-template-copy-materialized-untracked-x2-and-closeout-seeds-before-the-immutable-x1-boundary
- Method: Retain the premature-materialization fault, remove only Liora's seven reproducible untracked x2/closeout seeds, prove no x2 surface remains, and recreate them from Orin's immutable source only after x1 is pushed clean and fresh-remote equal.
- Recurrence guard: Retain the premature-materialization fault, remove only Liora's seven reproducible untracked x2/closeout seeds, prove no x2 surface remains, and recreate them from Orin's immutable source only after x1 is pushed clean and fresh-remote equal.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-024-F, V6614-X1-METHOD-024-P

### V6614-X1-METHOD-025 — Bounded recovery for first-combined-current-label-scan-used-an-unterminated-powershell-quoted-pattern

- Trigger: first-combined-current-label-scan-used-an-unterminated-powershell-quoted-pattern
- Method: Retain the parser failure and perform the bounded stale-current-label review with a UTF-8 Python literal list instead of a shell-quoted alternation.
- Recurrence guard: Retain the parser failure and perform the bounded stale-current-label review with a UTF-8 Python literal list instead of a shell-quoted alternation.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-025-F, V6614-X1-METHOD-025-P

### V6614-X1-METHOD-026 — Bounded recovery for first-combined-domain-scan-passed-windows-wildcards-as-literal-ripgrep-paths

- Trigger: first-combined-domain-scan-passed-windows-wildcards-as-literal-ripgrep-paths
- Method: Retain the two invalid-path diagnostics and use explicit directories plus include globs, while adjudicating inherited selected-row and novelty-neighbour matches separately.
- Recurrence guard: Retain the two invalid-path diagnostics and use explicit directories plus include globs, while adjudicating inherited selected-row and novelty-neighbour matches separately.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-026-F, V6614-X1-METHOD-026-P

### V6614-X1-METHOD-027 — Bounded recovery for first-python-current-label-scan-lost-an-apostrophe-bearing-literal-through-the-shell

- Trigger: first-python-current-label-scan-lost-an-apostrophe-bearing-literal-through-the-shell
- Method: Retain the syntax failure and use a PowerShell SimpleMatch array containing only quote-safe stale-current phrases over the five exact x1 code paths.
- Recurrence guard: Retain the syntax failure and use a PowerShell SimpleMatch array containing only quote-safe stale-current phrases over the five exact x1 code paths.
- Rollback: Stop, retain the failure at zero credit, and leave sibling, remote, external, and authority state unchanged.
- Witnesses: V6614-X1-METHOD-027-F, V6614-X1-METHOD-027-P

## Retained boundary

Same-owner workflow evidence only; no independent reproduction or protected-gate closure.
