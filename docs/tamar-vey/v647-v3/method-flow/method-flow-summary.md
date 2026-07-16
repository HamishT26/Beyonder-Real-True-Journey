# GHC Family Method Flow State

- Phase: v647-gmut-thos-v3-x1-x2
- Owner: Tamar Vey
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6473-M01 — Use literal paths when the shell interface has no positional argument channel

- Trigger: A nested shell call needs to read an exact local instruction file.
- Method: Embed the already-known literal path in the bounded read command and avoid interpolating private data.
- Recurrence guard: Do not assume shell positional arguments exist unless the tool schema explicitly provides them.
- Rollback: Discard the failed read-only wrapper; no repository action occurred.
- Witnesses: V6473-M01-WFAIL, V6473-M01-WPASS

### V6473-M02 — Split large-checkout startup probes into lightweight bounded witnesses

- Trigger: A large inherited checkout makes status and worktree inventory slow.
- Method: Run worktree and drive inventory first, then exact branch, status, ancestry, and live-remote checks separately with a longer bound.
- Recurrence guard: Do not bundle multiple large-checkout status scans behind the shortest timeout.
- Rollback: Discard the timeout result; it made no mutation.
- Witnesses: V6473-M02-WFAIL, V6473-M02-WPASS

### V6473-M03 — Use quiet fast-forward plus exact-hash proofs for artifact-heavy ancestry

- Trigger: The sequential branch advances across several artifact-heavy phases.
- Method: Treat path output as nonauthoritative and prove head, upstream, tracking, fresh live remote, status, ancestry, commit count, and merge count separately.
- Recurrence guard: Use quiet Git output where practical and always retain independent exact-hash receipts.
- Rollback: No rollback; exact proofs confirmed the authorized fast-forward and push.
- Witnesses: V6473-M03-WFAIL, V6473-M03-WPASS

### V6473-M04 — Split official-source discovery by evidence surface

- Trigger: One search spans unrelated science, standards, accessibility, and tooling topics.
- Method: Run a bounded domain-specific official-source query and retain the incomplete search as a negative.
- Recurrence guard: Require at least one directly reviewed official or primary source for each material proposal surface.
- Rollback: Do not infer absence from the broad search and do not query or download data.
- Witnesses: V6473-M04-WFAIL, V6473-M04-WPASS

### V6473-M05 — Use single-quoted literal patterns for PowerShell stale-label scans

- Trigger: A PowerShell wrapper passes one alternation pattern containing quote-sensitive text.
- Method: Place the complete bounded ripgrep alternation in one PowerShell single-quoted literal and keep file paths as separate arguments.
- Recurrence guard: Do not mix embedded double quotes with a double-quoted native-command pattern.
- Rollback: Discard the failed read-only scan; it changed no file or ref.
- Witnesses: V6473-M05-WFAIL, V6473-M05-WPASS

### V6473-M06 — Let the Method Flow runner append witness identifiers from an empty initial list

- Trigger: A generated method record is about to be ingested by the family Method Flow runner.
- Method: Initialize validation_witness_ids as an empty list and let each witness command append its stable identifier exactly once.
- Recurrence guard: Inspect the first summary for duplicate witness IDs before x1 staging.
- Rollback: Discard only the uncommitted owner-generated derived ledger and rebuild it from corrected records; retain the first summary as a negative description.
- Witnesses: V6473-M06-WFAIL, V6473-M06-WPASS

### V6473-M07 — Use ripgrep-owned glob filters instead of PowerShell wildcard path expansion

- Trigger: A native ripgrep command needs to scan version-patterned files on Windows.
- Method: Pass stable directories as paths and use ripgrep -g filters for version-patterned filenames.
- Recurrence guard: Do not rely on PowerShell to expand native-command wildcard path arguments.
- Rollback: Discard the failed read-only scan; no file was staged or changed.
- Witnesses: V6473-M07-WFAIL, V6473-M07-WPASS

### V6473-M08 — Pass absolute receipt paths to staged reviewers that relativize against the repository root

- Trigger: The staged reviewer computes public receipt paths relative to its absolute repository root.
- Method: Resolve each owner-scoped receipt to an absolute path before invoking the reviewer while keeping the staged surface unchanged.
- Recurrence guard: Inspect reviewer path semantics before the first lifecycle invocation and use absolute receipt paths consistently.
- Rollback: Retain the same uncommitted staged set; the failed invocation emitted no receipt and changed no ref.
- Witnesses: V6473-M08-WFAIL, V6473-M08-WPASS

### V6473-M09 — Run staged diff hygiene before fixed-point manifest credit

- Trigger: Compatibility-preserving source adaptation creates new Python files.
- Method: Retain the failed staged receipt, remove only surplus terminal blank lines, restage the same owned surface, and rerun the reviewer.
- Recurrence guard: Require git diff --cached --check before fixed-point manifest or commit credit.
- Rollback: Keep all substantive staged bytes, withdraw the failed review's pass credit, and apply only bounded EOF whitespace correction.
- Witnesses: V6473-M09-WFAIL, V6473-M09-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
