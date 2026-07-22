# GHC Family Method Flow State

- Phase: v651-v5-2-remaster
- Owner: Eiren Kestrel
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

## Preferred methods

### V6515R-M01 — Bound inherited-checkout verification

- Trigger: A newly materialized inherited worktree requires source, branch, and clean-diff verification.
- Method: Verify branch and head directly, then use bounded staged and unstaged index-diff checks without repeating the full status scan.
- Recurrence guard: Avoid full status enumeration as the first check on a newly materialized 46000-plus-file checkout.
- Rollback: Retain the timeout at zero credit and stop if branch, head, or either diff domain is not attributable.
- Witnesses: V6515R-M01-WFAIL, V6515R-M01-WPASS

### V6515R-M02 — Quote Git revision peel expressions in PowerShell

- Trigger: PowerShell passes a Git revision containing caret and brace syntax.
- Method: Wrap the complete revision peel expression in single quotes before passing it to git rev-parse.
- Recurrence guard: Quote every revision expression containing caret, braces, colon, or shell-significant punctuation.
- Rollback: Retain the fatal probe and use the already attributable plain head only if the peeled form cannot be verified.
- Witnesses: V6515R-M02-WFAIL, V6515R-M02-WPASS

### V6515R-M03 — Derive proposal outcome totals from frozen specifications

- Trigger: A proposal table and declared aggregate are authored separately.
- Method: Count expected dispositions directly from the frozen proposal table and fail before writing if the declared aggregate differs.
- Recurrence guard: Never change proposal evidence labels to satisfy a preferred distribution; derive the distribution from proposal truth.
- Rollback: Retain the failed generator attempt and write no packet until the aggregate matches the frozen table.
- Witnesses: V6515R-M03-WFAIL, V6515R-M03-WPASS

### V6515R-M04 — Separate live policy overrides from legacy workflow-runner route validation

- Trigger: A newer live request expands policy caps beyond the installed workflow runner's encoded values.
- Method: Preserve the authoritative live request and failed audit, then validate only immediate route structure through a marked compatibility projection that carries the live overrides explicitly.
- Recurrence guard: Never present a compatibility projection as validation of the newer policy values.
- Rollback: Retain the failed audit and stop route execution if the immediate ownership projection also fails.
- Witnesses: V6515R-M04-WFAIL, V6515R-M04-WPASS

### V6515R-M05 — Respect Method Flow witness auto-promotion

- Trigger: The Method Flow runner records a passing witness for a candidate method.
- Method: Read the state returned by the witness command and transition directly from validated to preferred only once.
- Recurrence guard: Do not hard-code a second validated transition after a passing witness.
- Rollback: Retain the rejected transition and resume from the ledger's actual valid state without rebuilding the ledger.
- Witnesses: V6515R-M05-WFAIL, V6515R-M05-WPASS

### V6515R-M06 — Declare UTF-8 for Windows skill validation

- Trigger: A Python validator reads UTF-8 GHC skill text on Windows.
- Method: Set PYTHONUTF8=1 for the skill validator on Windows before reading UTF-8 skill documents.
- Recurrence guard: Declare UTF-8 for Python subprocesses that read skill packages on Windows; do not strip or transliterate valid text to satisfy a legacy codec.
- Rollback: Retain the failed validation at zero credit and stop if explicit UTF-8 still cannot read the package.
- Witnesses: V6515R-M06-WFAIL, V6515R-M06-WPASS

### V6515R-M07 — Keep a uniform explicit Boundaries section in every skill

- Trigger: Generated and hand-authored skills share one structural contract.
- Method: Give every skill package an explicit Boundaries heading even when equivalent constraints already appear under a specialized heading.
- Recurrence guard: Validate shared structural headings across both generated and hand-authored packages before the aggregate.
- Rollback: Retain the failed aggregate and remove only the additive heading if it introduces a contradiction.
- Witnesses: V6515R-M07-WFAIL, V6515R-M07-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
