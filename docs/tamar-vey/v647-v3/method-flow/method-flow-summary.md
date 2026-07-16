# GHC Family Method Flow State

- Phase: v647-gmut-thos-v3-x1-x2
- Owner: Tamar Vey
- Methods: 16
- Passing witnesses: 17
- Failed witnesses retained: 17

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
- Witnesses: V6473-M07-WFAIL, V6473-M07-WPASS, V6473-M07-WFAIL-X2, V6473-M07-WPASS-X2

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

### V6473-M10 — Keep orchestration template delimiters out of generated artifact bodies

- Trigger: A JavaScript orchestration template contains generated Markdown or Python source.
- Method: Split large generated artifacts into quote-safe apply_patch surfaces and keep JavaScript template literals free of unescaped Markdown backticks.
- Recurrence guard: Scan cross-language template bodies for the outer delimiter before executing any nested edit call.
- Rollback: Discard the parser-rejected orchestration cell; it ran no nested tool and changed no file.
- Witnesses: V6473-M10-WFAIL, V6473-M10-WPASS

### V6473-M11 — Separate Python skill prompt construction from JavaScript interpolation syntax

- Trigger: Generated Python source must contain a dollar-prefixed skill name inside a JavaScript template.
- Method: Construct dollar-prefixed skill prompts with Python string concatenation so JavaScript sees no dollar-brace interpolation syntax.
- Recurrence guard: Avoid dollar-brace sequences inside JavaScript template literals unless JavaScript interpolation is intended.
- Rollback: Discard the ReferenceError result; it ran no patch and changed no file.
- Witnesses: V6473-M11-WFAIL, V6473-M11-WPASS

### V6473-M12 — Preflight owner-scoped deliverable directories before bounded copies

- Trigger: A generated artifact must be copied into a new phase deliverables directory.
- Method: Create the exact owner-scoped destination directory before copying a generated deliverable.
- Recurrence guard: Preflight the destination parent and create only the declared owner-scoped directory.
- Rollback: No partial destination existed; retain the source and retry only after the bounded parent exists.
- Witnesses: V6473-M12-WFAIL, V6473-M12-WPASS

### V6473-M13 — Normalize same-owner labels without weakening reproduction boundaries

- Trigger: A validator compares exact reproduction-boundary vocabulary.
- Method: Normalize the bounded evidence label to the canonical lowercase same-owner spelling and rerun the exact current-phase tests.
- Recurrence guard: Use the canonical same-owner label consistently across overview, receipts, report, and validators.
- Rollback: Retain the failed test output and change only the label casing; do not weaken the assertion.
- Witnesses: V6473-M13-WFAIL, V6473-M13-WPASS

### V6473-M14 — Replace timed-out parallel verification with explicit serial witnesses

- Trigger: A verification wrapper times out without returning child results.
- Method: Replay each verification as a short single-command witness and accept only its explicit exit status.
- Recurrence guard: Use short serial verification commands when wrapper output or startup latency can consume the orchestration deadline.
- Rollback: Retain the timeout and award no credit to its unobserved children.
- Witnesses: V6473-M14-WFAIL, V6473-M14-WPASS

### V6473-M15 — Discover exact staged-reviewer paths before invocation

- Trigger: A phase contains more than one staged-review or x1-review helper.
- Method: Discover the exact frozen reviewer path with a bounded filename query before invoking help.
- Recurrence guard: Use exact repository discovery for phase-local reviewer names instead of inferring a suffix.
- Rollback: Retain the failed read-only probe; it changed no file, index entry, ref, or worktree.
- Witnesses: V6473-M15-WFAIL, V6473-M15-WPASS

### V6473-M16 — Preflight lifecycle HEAD before phase-bound evidence generation

- Trigger: A phase builder is intentionally bound to one frozen lifecycle anchor.
- Method: Preflight HEAD and use the evidence builder only while it equals the frozen x1 anchor; after evidence commit, update closeout receipts additively without rerunning generation.
- Recurrence guard: Compare HEAD with the frozen x1 anchor before every evidence-builder invocation.
- Rollback: Retain the refused invocation; the guard wrote no derived evidence and no history changed.
- Witnesses: V6473-M16-WFAIL, V6473-M16-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
