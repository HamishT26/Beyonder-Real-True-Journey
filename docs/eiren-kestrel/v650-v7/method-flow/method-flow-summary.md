# GHC Family Method Flow State

- Phase: v650-v7
- Owner: Eiren Kestrel
- Methods: 28
- Passing witnesses: 28
- Failed witnesses retained: 29

## Preferred methods

### V6507-M01 — Materialize PowerShell foreach results before downstream conversion

- Trigger: A PowerShell statement-level foreach block is followed by a pipeline in the same expression.
- Method: Accumulate each term result in an explicit array and pipe that completed array to JSON conversion after the loop.
- Recurrence guard: When a PowerShell foreach statement produces structured rows, assign those rows to an array before applying a downstream pipeline.
- Rollback: Give the rejected wrapper zero novelty-audit credit and leave the repository source state unchanged.
- Witnesses: V6507-M01-WFAIL, V6507-M01-WPASS, V6507-M01-WFAIL2

### V6507-M02 — Inspect installed CLI subcommand help before constructing validation calls

- Trigger: A phase invokes a local skill runner whose current argument schema has not been read in the same phase.
- Method: Read the exact installed subcommand help first, then invoke only its declared arguments and inspect the generated receipt.
- Recurrence guard: Treat remembered CLI options as unverified until the current installed --help output confirms them.
- Rollback: Give the rejected validation call zero credit and retain its failure before constructing a corrected call.
- Witnesses: V6507-M02-WFAIL, V6507-M02-WPASS

### V6507-M03 — Resolve historical artifact paths before direct reads

- Trigger: A predecessor phase may use a different directory or filename layout for a requested artifact.
- Method: Use a bounded filename or content search first, then read only an exact resolved path or the current skill schema.
- Recurrence guard: Never infer phase-local artifact paths from a neighboring phase without an existence or indexed-search witness.
- Rollback: Give the failed read zero inspection credit and leave the repository unchanged.
- Witnesses: V6507-M03-WFAIL, V6507-M03-WPASS

### V6507-M04 — Split authoritative schema reads from bounded recent-artifact searches

- Trigger: A discovery wrapper combines a repository-wide content search with an authoritative schema read.
- Method: Read the exact current schema directly, then search only the relevant recent phase roots with a separate bound.
- Recurrence guard: Do not attach a broad historical corpus search to an authoritative small-file read.
- Rollback: Give the timed-out wrapper zero evidence credit and leave repository state unchanged.
- Witnesses: V6507-M04-WFAIL, V6507-M04-WPASS

### V6507-M05 — Inspect exact line context before count-sensitive source patches

- Trigger: A patch targets long generated-style list lines whose wrapping may differ from the proposed context.
- Method: Read the exact target lines first and apply a smaller uniquely anchored replacement.
- Recurrence guard: Do not patch long list literals from remembered wrapping; anchor against the current file text.
- Rollback: Treat the rejected patch as zero change and preserve the pre-patch file unchanged.
- Witnesses: V6507-M05-WFAIL, V6507-M05-WPASS

### V6507-M06 — Run exact portfolio counts after every list adjustment

- Trigger: A count-sensitive portfolio list is edited by removing or restoring entries.
- Method: Restore one explicitly scoped refinement entry and rerun all five portfolio counts before generation.
- Recurrence guard: Use executable cardinality checks after list edits rather than mental subtraction.
- Rollback: Do not freeze or credit the mismatched portfolio; keep the preflight result as a failed witness.
- Witnesses: V6507-M06-WFAIL, V6507-M06-WPASS

### V6507-M07 — Regenerate count mirrors from the complete retained-negative source

- Trigger: New Method Flow failures were recorded after the phase-data negative list was first authored.
- Method: Append every later operational negative plus this failed test to the source list, regenerate the packet, and rerun the isolated x1 tests.
- Recurrence guard: Derive lifecycle count mirrors from the final pre-freeze Method Flow failure set, not an earlier hand-maintained snapshot.
- Rollback: Give the failed x1 test run zero pass credit and freeze no commit until the isolated scope passes.
- Witnesses: V6507-M07-WFAIL, V6507-M07-WPASS

### V6507-M08 — Assert generated workflow fields at their exact schema path

- Trigger: A test consumes generated workflow-refinement output whose nested shape has not been inspected.
- Method: Inspect the generated output keys and assert the confirmation flag at its exact nested path.
- Recurrence guard: Inspect generated JSON shape before asserting field placement, even when the field appears in runner console output.
- Rollback: Give the failed isolated test run zero successful-pass credit and change only the incorrect assertion.
- Witnesses: V6507-M08-WFAIL, V6507-M08-WPASS

### V6507-M09 — Compare manifests within their declared Git-blob hash domain

- Trigger: A manifest declares path-filtered Git blobs while Windows checkout bytes may use a different line-ending domain.
- Method: Inspect object-id, exact Git-blob bytes, and checkout bytes separately; validate each field only in its declared domain.
- Recurrence guard: Never compare a Git-blob SHA-256 field directly to unnormalized checkout bytes on Windows.
- Rollback: Give the failed aggregate zero pre-commit review credit and retain its mismatches before a corrected domain-aware review.
- Witnesses: V6507-M09-WFAIL, V6507-M09-WPASS

### V6507-M10 — Decode staged Git text explicitly as UTF-8 on Windows

- Trigger: An inline verifier reads staged UTF-8 JSON through subprocess text mode on a legacy Windows console codec.
- Method: Read git show output as bytes and decode every staged text blob explicitly with UTF-8.
- Recurrence guard: Never rely on the process default text codec for staged repository artifacts containing Maori or other Unicode text.
- Rollback: Give the failed aggregate zero staged-review credit and preserve the exact staged content unchanged until the corrected read.
- Witnesses: V6507-M10-WFAIL, V6507-M10-WPASS

### V6507-M11 — Invoke quick_validate only with an initialized skill directory

- Trigger: The skill validator is a path-only utility and does not declare a help-mode contract.
- Method: Initialize a phase-local skill first, then pass its exact directory to quick_validate.
- Recurrence guard: Do not assume every local script supports argparse help; inspect its usage or invoke it only with its documented positional path.
- Rollback: Give the failed help probe zero skill-validation credit and leave every global skill untouched.
- Witnesses: V6507-M11-WFAIL, V6507-M11-WPASS

### V6507-M12 — Split repository inspection into bounded constant-time probes

- Trigger: A compound inspection combines recursive Git status, file reads, and metadata collection under one short timeout.
- Method: Run file existence and size, syntax compilation, and Git state as separate bounded probes; credit only completed probes.
- Recurrence guard: Keep potentially recursive Git inspection separate from constant-time filesystem and syntax checks, and never treat a timed-out wrapper as a partial pass.
- Rollback: Give the compound command zero inspection credit and leave repository content unchanged until bounded probes complete.
- Witnesses: V6507-M12-WFAIL, V6507-M12-WPASS

### V6507-M13 — Parse Git porcelain without trimming its status columns

- Trigger: A helper feeds porcelain-v1 output through a generic stdout function that strips leading whitespace.
- Method: Read NUL-delimited porcelain bytes directly and remove exactly the three-byte status prefix from each complete record.
- Recurrence guard: Never pass column-sensitive or NUL-delimited Git output through a text helper that applies strip.
- Rollback: Stop before x2 execution, give the failed preflight zero evidence credit, and preserve every existing path unchanged.
- Witnesses: V6507-M13-WFAIL, V6507-M13-WPASS

### V6507-M14 — Add the scripts directory before importing a standalone sibling-import module

- Trigger: An inline validation probe imports a standalone script whose imports resolve relative to the scripts directory when executed directly.
- Method: Prepend the repository scripts directory to sys.path for the bounded inline probe, then import the standalone module.
- Recurrence guard: Match an inline probe's import search path to the script's supported direct-execution context.
- Rollback: Give the failed probe zero parser-validation credit and leave source and repository state unchanged.
- Witnesses: V6507-M14-WFAIL, V6507-M14-WPASS

### V6507-M15 — Preflight skill interface length before official initialization

- Trigger: A generated skill slug can produce a short_description shorter than the creator's 25-character lower bound.
- Method: Construct 25-64 character interface descriptions before initialization and use the official YAML generator only to finish an initializer-created partial directory.
- Recurrence guard: Assert every generated short_description is between 25 and 64 characters before calling init_skill.py.
- Rollback: Give the failed initializer zero skill credit, retain the partial phase-local directory as the recovery target, and do not install anything globally.
- Witnesses: V6507-M15-WFAIL, V6507-M15-WPASS

### V6507-M16 — Permit only preregistered partial x2 artifacts during bounded retry

- Trigger: A stopped x2 builder has already written owner-scoped phase runners before a later skill-initialization failure.
- Method: Allow the exact phase-root, ghc_family_v650_v7 script namespace, evidence builder, and x2 test path while rejecting every other path.
- Recurrence guard: Design retry preflights around the declared partial-write surface, never a clean-start-only path set and never an unrestricted repository prefix.
- Rollback: Give the rejected retry zero execution credit and preserve the already written owner-scoped runner files for bounded inspection.
- Witnesses: V6507-M16-WFAIL, V6507-M16-WPASS

### V6507-M17 — Project descendant-incompatible historical lifecycle assertions before aggregate recovery

- Trigger: A repository-wide descendant run fails historical tests that bind mutable HEAD or a superseded pre-correction owner manifest.
- Method: Isolate the exact failures, verify that each is a historical lifecycle projection rather than a current functional regression, then add only those exact IDs to the inherited exclusion set.
- Recurrence guard: Keep historical phase tests immutable but project mutable-head and superseded-manifest assertions explicitly in descendant full-suite plans.
- Rollback: Give the failed aggregate zero pass credit, retain its six assertion failures, and prohibit post-success replay.
- Witnesses: V6507-M17-WFAIL, V6507-M17-WPASS

### V6507-M18 — Replace broad source-corpus searches with exact failing-test reads

- Trigger: A broad recursive search across several large phase trees is used to locate already identified failure anchors.
- Method: Read the five exact failing test files and rerun only the one module whose failure name was truncated in the aggregate receipt.
- Recurrence guard: Once a failed module is known, use exact files and exact test IDs rather than a multi-tree recursive search.
- Rollback: Give the timed-out search zero classification credit and preserve the clean evidence head.
- Witnesses: V6507-M18-WFAIL, V6507-M18-WPASS

### V6507-M19 — Avoid all-ref path history scans during exact-anchor triage

- Trigger: A path-limited Git history query adds --all across the large shared repository during failure triage.
- Method: Use exact known commits and bounded rev-list or rev-parse queries on the current ancestry instead of scanning every ref.
- Recurrence guard: Do not combine --all with large path histories when the failing tests already provide exact source, evidence, or final anchors.
- Rollback: Give both timed-out history queries zero anchor credit and keep the evidence commit unchanged.
- Witnesses: V6507-M19-WFAIL, V6507-M19-WPASS

### V6507-M20 — Read the exact phase-data constant before final packet generation

- Trigger: The first closeout build referenced a remembered PRACTICE_LENS attribute that the current phase-data module does not export.
- Method: Inspect exported phase-data names and use the exact BOUNDED_PRACTICE constant before retrying the deterministic builder.
- Recurrence guard: Inspect exported phase-data names and use the exact BOUNDED_PRACTICE constant before retrying the deterministic builder.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M20-WFAIL, V6507-M20-WPASS

### V6507-M21 — Use direct literal-file context when a targeted text search stalls

- Trigger: A single-file rg lookup unexpectedly timed out while an attributable traceback already identified the symbol family.
- Method: Patch from the exact traceback context and use direct literal-file inspection only for a bounded confirmation.
- Recurrence guard: Patch from the exact traceback context and use direct literal-file inspection only for a bounded confirmation.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M21-WFAIL, V6507-M21-WPASS

### V6507-M22 — Split closeout source patches when one generated line mismatches

- Trigger: A combined multi-hunk closeout patch was rejected because one generated validator line did not match the proposed whitespace.
- Method: Apply small exact-context patches and verify each applied change before continuing.
- Recurrence guard: Apply small exact-context patches and verify each applied change before continuing.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M22-WFAIL, V6507-M22-WPASS

### V6507-M23 — Quarantine exact inherited privacy-scanner receipts during owner rescans

- Trigger: The final owner scan treated two inherited privacy-receipt files as payload because its scanner-definition allowlist omitted them.
- Method: Add only the exact x1 and evidence privacy-receipt paths to the scanner-definition quarantine and rerun the deterministic manifest step.
- Recurrence guard: Add only the exact x1 and evidence privacy-receipt paths to the scanner-definition quarantine and rerun the deterministic manifest step.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M23-WFAIL, V6507-M23-WPASS

### V6507-M24 — Use nonconflicting delimiters in generated Python string fixtures

- Trigger: The first closeout test source used single-quoted HTML tokens inside a single-quoted generated tuple and failed Python parsing.
- Method: Generate the token tuple with double-quoted Python strings while retaining single quotes only inside the HTML fragments.
- Recurrence guard: Generate the token tuple with double-quoted Python strings while retaining single quotes only inside the HTML fragments.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M24-WFAIL, V6507-M24-WPASS

### V6507-M25 — Use one communicate transaction for Git batch-object verification

- Trigger: The first exact Git-index verifier closed a buffered batch input before consuming the child output and timed out without a result.
- Method: Supply all object identifiers through subprocess communicate semantics, consume the complete bounded batch once, and parse its framed blobs in memory.
- Recurrence guard: Supply all object identifiers through subprocess communicate semantics, consume the complete bounded batch once, and parse its framed blobs in memory.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M25-WFAIL, V6507-M25-WPASS

### V6507-M26 — Supply both immutable suite receipts to the closeout builder

- Trigger: A closeout rebuild was invoked without its required failed-suite and recovery-suite receipt arguments and stopped at argument parsing.
- Method: Treat both external receipt paths as mandatory inputs and invoke the deterministic builder only after checking that each receipt exists.
- Recurrence guard: Treat both external receipt paths as mandatory inputs and invoke the deterministic builder only after checking that each receipt exists.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M26-WFAIL, V6507-M26-WPASS

### V6507-M27 — Derive terminal Method Flow assertions from the extended ledger

- Trigger: After M25 and M26 were recorded, the closeout builder still asserted the earlier 24-method ledger size and stopped before final packet credit.
- Method: Update the deterministic closeout and its generated tests to the exact extended ledger counts before rebuilding from the unchanged evidence head.
- Recurrence guard: Update the deterministic closeout and its generated tests to the exact extended ledger counts before rebuilding from the unchanged evidence head.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M27-WFAIL, V6507-M27-WPASS

### V6507-M28 — Keep generated preferred-state counts synchronized with Method Flow growth

- Trigger: The regenerated closeout test updated method and witness counts but retained the earlier preferred-state expectation of 24.
- Method: Update method, failed-witness, passing-witness, and preferred-state counts together whenever a retained Method Flow entry is added.
- Recurrence guard: Update method, failed-witness, passing-witness, and preferred-state counts together whenever a retained Method Flow entry is added.
- Rollback: Give the failed attempt zero credit, retain it, and preserve the owner lane until the bounded recovery passes.
- Witnesses: V6507-M28-WFAIL, V6507-M28-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
