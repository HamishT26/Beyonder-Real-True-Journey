# GHC Family Method Flow State

- Phase: v649-gmut-thos-v5-x1-x2
- Owner: Tamar Vey
- Methods: 13
- Passing witnesses: 13
- Failed witnesses retained: 14

## Preferred methods

### V6495-M01 — Recover combined_receipt_listing_timeout while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes combined_receipt_listing_timeout.
- Method: Split exact receipt reads and manifest checks into bounded queries.
- Recurrence guard: Query exact receipts and immutable manifests separately.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M01-WFAIL, V6495-M01-WPASS

### V6495-M02 — Recover parallel_wrapper_aggregation_failure while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes parallel_wrapper_aggregation_failure.
- Method: Use all-settled aggregation and normalize expected empty-search exits.
- Recurrence guard: Use all-settled orchestration for independent read-only probes.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M02-WFAIL, V6495-M02-WPASS

### V6495-M03 — Recover broad_title_extraction_timeout while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes broad_title_extraction_timeout.
- Method: Parse the frozen JSON once and print only the requested proposal family.
- Recurrence guard: Prefer structured JSON projection over broad text pipelines.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M03-WFAIL, V6495-M03-WPASS

### V6495-M04 — Recover multi_term_query_timeout while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes multi_term_query_timeout.
- Method: Treat partial output as no credit and use narrower structured searches.
- Recurrence guard: Limit each semantic probe by family and mechanism.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M04-WFAIL, V6495-M04-WPASS

### V6495-M05 — Recover memory_registry_no_current_match while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes memory_registry_no_current_match.
- Method: Retain the no-match and use the committed baton plus exact live Git proof.
- Recurrence guard: Treat absent current memory as absence, never as proof.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M05-WFAIL, V6495-M05-WPASS

### V6495-M06 — Recover semantic_seed_collisions while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes semantic_seed_collisions.
- Method: Withdraw every collision and replace mechanisms without lowering the novelty threshold.
- Recurrence guard: A new domain label does not establish a new mechanism.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M06-WFAIL, V6495-M06-WPASS

### V6495-M07 — Recover similarity_tuple_comparison_fault while retaining the failed witness

- Trigger: A bounded v649-v5 workflow exposes similarity_tuple_comparison_fault.
- Method: Supply an explicit numeric key for maximum-score selection.
- Recurrence guard: Always key aggregate selection on the numeric score when payloads are non-orderable.
- Rollback: Give the failed attempt no credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6495-M07-WFAIL, V6495-M07-WPASS

### V6495-M08 — Recover skill smoke predicate mismatch while retaining the failed aggregate

- Trigger: A generated skill aggregate separates body and interface evidence.
- Method: Inspect exact generated files and require complementary SKILL.md boundary text plus the protected-gate phrase in openai.yaml.
- Recurrence guard: Bind smoke predicates to exact fields in the artifact where each field is generated.
- Rollback: Give the failed aggregate no credit, inspect exact artifacts, and rerun only after correcting the predicate.
- Witnesses: V6495-M08-WFAIL, V6495-M08-WPASS

### V6495-M09 — Classify exact closeout scanner definitions without hiding payload hits

- Trigger: A phase-owned executable defines the same privacy patterns used by the staged scanner.
- Method: Inspect the exact hit paths, confirm they are regex definitions in the bounded scanner, and add only that exact runner to scanner-definition quarantine.
- Recurrence guard: Register every scanner implementation path explicitly before scanning executable source and never quarantine content-bearing artifacts.
- Rollback: Keep the evidence build failed, retain all candidate rows, and never broaden quarantine beyond exact scanner source paths.
- Witnesses: V6495-M09-WFAIL, V6495-M09-WPASS

### V6495-M10 — Use commit-local blobs for phase-freeze tests

- Trigger: A bounded successor validation crosses an immutable lifecycle or process boundary.
- Method: Bind x1 JSON reads to immutable x1 commit blobs while leaving the current document-cap scan explicit.
- Recurrence guard: Phase-freeze tests must read commit-local blobs after a phase advances.
- Rollback: Give the failed aggregate zero credit, preserve its witness, and change only the demonstrated bounded fault.
- Witnesses: V6495-M10-WFAIL, V6495-M10-WPASS

### V6495-M11 — Track validator process and receipt independently of the app handle

- Trigger: A bounded successor validation crosses an immutable lifecycle or process boundary.
- Method: Launch the bounded validator as a tracked hidden process with external output capture and monitor both process state and the receipt path.
- Recurrence guard: A lost app handle never implies completion; require an attributable receipt or retain and terminate the confirmed orphan.
- Rollback: Give the failed aggregate zero credit, preserve its witness, and change only the demonstrated bounded fault.
- Witnesses: V6495-M11-WFAIL, V6495-M11-WPASS

### V6495-M12 — Project inherited lifecycle assertions from committed state records

- Trigger: A bounded successor validation crosses an immutable lifecycle or process boundary.
- Method: Project only those pre-pass values from Orin's committed single-pass plan and evidence ledger without excluding either test.
- Recurrence guard: Successor checks of lifecycle assertions must bind each assertion to its committed pre-pass or post-pass evidence state.
- Rollback: Give the failed aggregate zero credit, preserve its witness, and change only the demonstrated bounded fault.
- Witnesses: V6495-M12-WFAIL, V6495-M12-WPASS

### V6495-M13 — Count detailed checks structurally before freezing the contract

- Trigger: A bounded successor validation crosses an immutable lifecycle or process boundary.
- Method: Enumerate the detailed-check list structurally and correct the contract and result count to the observed 33 without removing a check. Restore the unmodified 33-check list, fold the plan-count guard into an existing plan check, and change only the expected and reported total.
- Recurrence guard: Count validator list elements structurally before freezing declared detailed-check totals. Inspect exact list cardinality after a proposed correction and before consuming another aggregate attempt.
- Rollback: Give the failed aggregate zero credit, preserve its witness, and change only the demonstrated bounded fault.
- Witnesses: V6495-M13-WFAIL-1, V6495-M13-WFAIL-2, V6495-M13-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
