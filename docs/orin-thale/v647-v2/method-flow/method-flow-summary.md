# GHC Family Method Flow State

- Phase: v647-gmut-thos-v2-x1-x2
- Owner: Orin Thale
- Methods: 21
- Passing witnesses: 21
- Failed witnesses retained: 21

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

### V6472-M10 — Keep bounded ripgrep patterns in one argument

- Trigger: A PowerShell command searches several exact evidence-builder markers.
- Method: Use one quoted pattern argument or separate literal searches, then inspect exact line markers before patching.
- Recurrence guard: Keep every ripgrep pattern in one explicitly quoted argument and never append alternation fragments as paths.
- Rollback: Discard the failed read-only lookup; no edit or nested mutation occurred.
- Witnesses: V6472-M10-WFAIL, V6472-M10-WPASS, V6472-M10-WFAIL, V6472-M10-WPASS

### V6472-M11 — Use encoding-stable patch anchors

- Trigger: A generated Python source contains UTF-8 authority terms displayed through a legacy console encoding.
- Method: Use encoding-stable ASCII anchors or replace an exact in-memory block extracted from the UTF-8 file, then apply one owner-scoped patch.
- Recurrence guard: Do not use console-rendered mojibake as patch context; anchor on stable schema or key lines.
- Rollback: No rollback is needed because apply_patch rejected the edit atomically.
- Witnesses: V6472-M11-WFAIL, V6472-M11-WPASS, V6472-M11-WFAIL, V6472-M11-WPASS

### V6472-M12 — Transform unstable UTF-8 source from exact bytes

- Trigger: An uncommitted owner-generated source file cannot be patched reliably through console-rendered Unicode context.
- Method: Read the uncommitted owner script as base64, decode exact UTF-8 bytes in memory, transform stable keys and whole blocks, then replace the file through apply_patch delete and add operations.
- Recurrence guard: For an uncommitted owner file with unstable console rendering, transform exact base64-decoded UTF-8 bytes rather than console text.
- Rollback: No rollback is needed because the failed apply_patch was atomic; retain the current file until the exact-byte replacement is ready.
- Witnesses: V6472-M12-WFAIL, V6472-M12-WPASS, V6472-M12-WFAIL, V6472-M12-WPASS

### V6472-M13 — Use an isolate-local base64 decoder

- Trigger: Exact UTF-8 bytes arrive as base64 in an orchestration isolate without browser decoding globals.
- Method: Decode base64 with a small local alphabet-and-bit accumulator, then run the already bounded UTF-8 decoder and apply_patch replacement.
- Recurrence guard: Do not assume browser base64 globals exist in the orchestration isolate.
- Rollback: Discard the failed in-memory operation; no decoder completed and no file edit ran.
- Witnesses: V6472-M13-WFAIL, V6472-M13-WPASS, V6472-M13-WFAIL, V6472-M13-WPASS

### V6472-M14 — Configure the shell text channel explicitly as UTF-8

- Trigger: An owner source file with Unicode must cross the shell-to-orchestration text boundary.
- Method: Set PowerShell and console output encoding explicitly to UTF-8, read the source with -Encoding UTF8, and use the returned exact text for bounded apply_patch generation.
- Recurrence guard: Prefer an explicitly UTF-8 configured shell text channel over ad hoc base64 decoding in the isolate.
- Rollback: Discard the failed in-memory decode; no file edit ran.
- Witnesses: V6472-M14-WFAIL, V6472-M14-WPASS, V6472-M14-WFAIL, V6472-M14-WPASS

### V6472-M15 — Verify block markers before whole-block transforms

- Trigger: A long generated overview must be replaced in an uncommitted owner builder.
- Method: Inspect exact overview start and following write markers with separate literal searches, then replace between verified indices and retain the completeness guard.
- Recurrence guard: Derive block boundaries from exact verified marker indices instead of a speculative multiline regex.
- Rollback: No rollback is needed because the completeness guard stopped before apply_patch.
- Witnesses: V6472-M15-WFAIL, V6472-M15-WPASS, V6472-M15-WFAIL, V6472-M15-WPASS

### V6472-M16 — Reject truncated whole-file source transport

- Trigger: A tool result may abbreviate a long whole-file source payload.
- Method: Use bounded line windows and stable surrounding keys to reconstruct only the two truncated regions, then compile and scan before execution.
- Recurrence guard: Never use a potentially truncated whole-file tool result as source bytes; prefer bounded windows or existing repository files.
- Rollback: Do not execute the corrupt builder; reconstruct only the damaged owner lines and recompile.
- Witnesses: V6472-M16-WFAIL, V6472-M16-WPASS, V6472-M16-WFAIL, V6472-M16-WPASS

### V6472-M17 — Bind tests to declared contract and mutation roles

- Trigger: A proposal uses a zero-row receipt as its mutation artifact.
- Method: Read positive_fixture from the declared contract path and mutation rows from the declared mutation path in SURFACES.
- Recurrence guard: Resolve contract and mutation roles through the runtime surface map before asserting fields.
- Rollback: Keep the failed test output, change only the source artifact selected by the assertion, and rerun the current-phase tests.
- Witnesses: V6472-M17-WFAIL, V6472-M17-WPASS, V6472-M17-WFAIL, V6472-M17-WPASS

### V6472-M18 — Quarantine compact-token stale filenames additively

- Trigger: A compatibility adapter generates compact phase tokens inside filenames.
- Method: Retain the immutable evidence paths, add correctly labelled v6472 witness copies with identical bounded content, and publish a stale-label quarantine receipt.
- Recurrence guard: Scan both hyphenated, underscored, and compact phase tokens before staging generated witness paths.
- Rollback: Do not rewrite or delete the evidence commit; add corrected paths and quarantine the stale compatibility paths.
- Witnesses: V6472-M18-WFAIL, V6472-M18-WPASS, V6472-M18-WFAIL, V6472-M18-WPASS

### V6472-M19 — Budget inherited-checkout Git status probes explicitly

- Trigger: A bounded read-only status probe targets the inherited full checkout.
- Method: Keep the Git and file probe unchanged but give the known large inherited checkout a measured sixty-second wrapper budget.
- Recurrence guard: Use a sixty-second wrapper budget for bounded Git status probes over the inherited full checkout and retain any timeout before retry.
- Rollback: No repository rollback is required because the failed probe was read-only; stop rather than broadening scope if the bounded retry also times out.
- Witnesses: V6472-M19-WFAIL, V6472-M19-WPASS, V6472-M19-WFAIL, V6472-M19-WPASS

### V6472-M20 — Compile validation scripts before closeout use

- Trigger: A newly generated or patched validation script is about to be used for lifecycle credit.
- Method: Patch only the mismatched subprocess argument-list delimiter, then require both scripts to compile before any closeout build.
- Recurrence guard: Compile every newly landed validation script before it can generate or validate a closeout artifact.
- Rollback: Revert only the uncommitted audit-script edit if the narrow correction fails compilation; do not alter evidence history.
- Witnesses: V6472-M20-WFAIL, V6472-M20-WPASS, V6472-M20-WFAIL, V6472-M20-WPASS

### V6472-M21 — Resolve staged-review receipt paths before containment checks

- Trigger: The staged reviewer writes receipt, manifest, and privacy outputs beneath the repository root.
- Method: Resolve every staged-review output to an absolute path beneath the verified repository root before invoking the containment guard.
- Recurrence guard: Pass resolved absolute in-repository output paths to the v647-v2 staged reviewer; never weaken or remove its containment check.
- Rollback: No content review or repository mutation was credited by the failed invocation; retain the staged index and stop if resolved paths fail containment.
- Witnesses: V6472-M21-WFAIL, V6472-M21-WPASS, V6472-M21-WFAIL, V6472-M21-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
