# GHC Family Method Flow State

- Phase: v647-gmut-thos-v2-x1-x2
- Owner: Orin Thale
- Methods: 9
- Passing witnesses: 9
- Failed witnesses retained: 9

## Preferred methods

### V6472-M01 — Resolve a real repository root before worktree inventory

- Trigger: A task starts in a project settings directory rather than a checked-out repository.
- Method: Enumerate the bounded D-drive worktree bank first and run Git only with an explicit verified repository path.
- Recurrence guard: Never infer repository status from the process cwd; pass -C with the exact owner or source worktree.
- Rollback: Discard the failed read-only probe; no repository mutation occurred.
- Witnesses: V6472-M01-WFAIL, V6472-M01-WPASS, V6472-M01-WFAIL, V6472-M01-WPASS

### V6472-M02 — Inspect proposal-index schema before selecting rows

- Trigger: Family phases may preserve different proposal-index schemas.
- Method: Read top-level keys, select prior_proposals, then append the current source x1 proposals explicitly.
- Recurrence guard: Require the declared count and actual array count to match before semantic-neighbor analysis.
- Rollback: Discard the empty projection; no file mutation occurred.
- Witnesses: V6472-M02-WFAIL, V6472-M02-WPASS, V6472-M02-WFAIL, V6472-M02-WPASS

### V6472-M03 — Split official-source discovery by evidence surface

- Trigger: A combined source query spans unrelated scientific, standards, and practice domains.
- Method: Use bounded domain-specific official-source queries and retain zero-result or omitted surfaces.
- Recurrence guard: Require at least one directly reviewed official or primary source per material surface before freezing source IDs.
- Rollback: Retain the incomplete search as a negative and do not infer absence from it.
- Witnesses: V6472-M03-WFAIL, V6472-M03-WPASS, V6472-M03-WFAIL, V6472-M03-WPASS

### V6472-M04 — Use quiet fast-forward output and independent exact-hash proofs

- Trigger: A sequential branch advances across multiple artifact-heavy phases.
- Method: Use quiet fast-forward where supported, then prove head, upstream, tracking, live remote, clean state, commit count, and merge count separately.
- Recurrence guard: Treat verbose path output as nonauthoritative; exact Git hashes and status are the authoritative witness.
- Rollback: No rollback; the fast-forward and push were valid, and exact proofs confirmed the intended head.
- Witnesses: V6472-M04-WFAIL, V6472-M04-WPASS, V6472-M04-WFAIL, V6472-M04-WPASS

### V6472-M05 — Treat elevation-required Sandbox probes as unavailable

- Trigger: Sandbox feature state cannot be read by the ordinary process.
- Method: Record capability as unavailable to the current process and do not elevate, enable features, weaken security, or reboot.
- Recurrence guard: Never retry the feature query with elevation inside a family phase.
- Rollback: No system mutation occurred; retain the error and continue with bounded owner-local fixtures.
- Witnesses: V6472-M05-WFAIL, V6472-M05-WPASS, V6472-M05-WFAIL, V6472-M05-WPASS

### V6472-M06 — Keep JavaScript replacement strings quote-safe

- Trigger: An orchestration cell transforms prose containing possessives or quoted names.
- Method: Use double-quoted JavaScript literals or template strings for replacement text containing apostrophes.
- Recurrence guard: Parse the orchestration source before allowing any nested edit call and avoid mixed quote ownership.
- Rollback: Discard the parser-rejected cell; no nested command or file edit ran.
- Witnesses: V6472-M06-WFAIL, V6472-M06-WPASS, V6472-M06-WFAIL, V6472-M06-WPASS

### V6472-M07 — Use available UTF-8 text transport in the orchestration isolate

- Trigger: A local source file must be transformed and installed through apply_patch.
- Method: Ask the shell tool for UTF-8 text, isolate its Output section, normalize line endings, and pass the transformed content to apply_patch.
- Recurrence guard: Do not assume browser encoding globals exist in the orchestration isolate.
- Rollback: Discard the failed in-memory transform; no apply_patch call occurred.
- Witnesses: V6472-M07-WFAIL, V6472-M07-WPASS, V6472-M07-WFAIL, V6472-M07-WPASS

### V6472-M08 — Validate owner labels before sealing Method Flow

- Trigger: A phase builder is adapted from a prior owner's compatible implementation.
- Method: Scan owner, phase, route, and boundary labels before staging; fix the authoritative builder and regenerate only owner-scoped precommit artifacts.
- Recurrence guard: Require every Method Flow scope boundary to begin with Orin v647-v2 before ledger validation and x1 staging.
- Rollback: Discard the uncommitted owner-generated ledger, keep this failed witness, regenerate from the corrected builder, and rerun the family Method Flow runner.
- Witnesses: V6472-M08-WFAIL, V6472-M08-WPASS, V6472-M08-WFAIL, V6472-M08-WPASS

### V6472-M09 — Run staged diff hygiene before fixed-point manifest credit

- Trigger: New validators are created through compatibility-preserving text adaptation.
- Method: Remove only the surplus terminal blank lines, retain the failed staged receipt, restage the exact same owned surface, and rerun the reviewer.
- Recurrence guard: Require diff hygiene to pass before manifest fixed-point or x1 commit credit.
- Rollback: Keep all substantive staged content, withdraw the failed review's pass credit, and apply only the bounded whitespace correction.
- Witnesses: V6472-M09-WFAIL, V6472-M09-WPASS, V6472-M09-WFAIL, V6472-M09-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
