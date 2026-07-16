# GHC Family Method Flow State

- Phase: v646-gmut-thos-v3-x1-x2
- Owner: Sable Rook
- Methods: 9
- Passing witnesses: 11
- Failed witnesses retained: 13

## Preferred methods

### V6463-M01 — Bounded direct-path shell-startup probe

- Trigger: known owner paths are available; a broad D-drive listing would add no evidence; ordinary user privileges only
- Method: Use direct known-path probes with login-profile startup disabled and a measured sixty-second upper bound.
- Recurrence guard: Avoid broad archive-root enumeration; use known paths, disable login startup, and keep the command bound at or below sixty seconds.
- Rollback: Stop the probe without mutation and retain unavailable state if the widened bounded envelope also fails.
- Witnesses: V6463-M01-F1, V6463-M01-F2, V6463-M01-P

### V6463-M02 — Array-before-pipeline PowerShell sequencing

- Trigger: PowerShell foreach output must feed a later pipeline; the operation is read-only
- Method: Materialize foreach output as an array and pipe only the completed array.
- Recurrence guard: Wrap foreach output in an array before formatting or filtering it.
- Rollback: Stop before any command executes and rerun only the read-only query with array materialization.
- Witnesses: V6463-M02-F, V6463-M02-P

### V6463-M03 — Windows ripgrep glob-filter guard

- Trigger: versioned files must be searched on Windows; literal wildcard paths are unsupported
- Method: Pass concrete directories to ripgrep and constrain filenames with -g filters.
- Recurrence guard: Use rg -g for wildcard selection on Windows rather than wildcard path arguments.
- Rollback: Treat the failed search as no result and rerun against real directories with filters.
- Witnesses: V6463-M03-F, V6463-M03-P, V6463-M03-F2, V6463-M03-P2

### V6463-M04 — Two-layer proposal and support collision quarantine

- Trigger: core and expanded portfolios are both frozen; predecessor artifacts are immutable
- Method: Retain the collision receipt, rewrite only exact title collisions, and rerun the full support-title comparison.
- Recurrence guard: Require both core-proposal and support-portfolio collision counts to be zero before x1 review.
- Rollback: Reject the candidate build, preserve the failed collision list, and edit only Sable-owned definitions.
- Witnesses: V6463-M04-F, V6463-M04-P

### V6463-M05 — Split non-login inspection envelope

- Trigger: the requested inspection spans multiple output classes; known owner paths are available; ordinary user privileges only
- Method: Disable login startup, split status and pattern inspection into bounded commands, and keep each query on known owner paths.
- Recurrence guard: Use non-login shell startup and separate status, file inventory, and targeted content searches so each bounded command has one purpose.
- Rollback: Stop the read-only probe without mutation and retain unavailable state if the split command still exceeds the widened envelope.
- Witnesses: V6463-M05-F1, V6463-M05-F2, V6463-M05-P

### V6463-M06 — Exact test-identifier source lookup

- Trigger: an existing selection names exact public test identifiers; source location must be reverified; no broader exclusion is authorized
- Method: Use the exact test identifiers already declared by the successor selection instead of a speculative semantic pattern.
- Recurrence guard: When a test-selection artifact already names exclusions, search those exact public test identifiers before inventing semantic synonyms.
- Rollback: Treat a zero-row speculative search as no discovery evidence and leave the selection unchanged until exact identifiers resolve.
- Witnesses: V6463-M06-F, V6463-M06-P, V6463-M06-F2, V6463-M06-P2

### V6463-M07 — Explicit negative-zero canonicalization guard

- Trigger: canonical JSON bytes participate in a manifest or digest; the host serializer is not itself proof of RFC 8785 behavior; synthetic mutation evidence is in scope
- Method: Reject negative zero explicitly before canonical-byte comparison, then require the valid fixed point and every mutation to produce the intended acceptance state.
- Recurrence guard: Do not infer RFC 8785 numeric normalization from the host JSON serializer; test negative zero and other forbidden numeric forms explicitly.
- Rollback: Keep the skill portfolio invalid and preserve the failed smoke receipt if the explicit numeric guard does not reject the mutation.
- Witnesses: V6463-M07-F, V6463-M07-P

### V6463-M08 — Frozen negative-ledger schema binding

- Trigger: a successor reconciles an immutable predecessor ledger; field names differ across lifecycle summaries; append-only negative accounting is required
- Method: Bind the external-negative reconciler to the frozen x1 ledger's new_x1_operational field and separately verify the retained-register arithmetic.
- Recurrence guard: Inspect the immutable source schema before binding count assertions; do not infer field names from a successor summary.
- Rollback: Keep aggregate runner credit at zero and retain the stopped receipt if the isolated reconciler still fails.
- Witnesses: V6463-M08-F, V6463-M08-P

### V6463-M09 — Immutable companion-drift quarantine

- Trigger: a predecessor manifest is immutable; exact Git-blob replay reveals a bounded companion mismatch; history rewrite is prohibited
- Method: Verify every immutable x1 Git blob, quarantine only the two known post-manifest review companions, and deny exact fixed-point credit to the x1 manifest while requiring exact parity for v646-v3 evidence and final manifests.
- Recurrence guard: Treat review or manifest companions written after a hash capture as quarantined drift, never as exact parity; require successor manifests to hash exact staged Git-index blobs after the path set stabilizes.
- Rollback: Stop the aggregate and deny x1 fixed-point credit if any mismatch falls outside the two named immutable companion rows.
- Witnesses: V6463-M09-F, V6463-M09-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
