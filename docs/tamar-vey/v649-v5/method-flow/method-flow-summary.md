# GHC Family Method Flow State

- Phase: v649-gmut-thos-v5-x1-x2
- Owner: Tamar Vey
- Methods: 7
- Passing witnesses: 7
- Failed witnesses retained: 7

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

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
