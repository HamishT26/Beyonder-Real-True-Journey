# GHC Family Method Flow State

- Phase: v648-gmut-thos-v6-x1-x2
- Owner: Orin Thale
- Methods: 13
- Passing witnesses: 13
- Failed witnesses retained: 13

## Preferred methods

### V6486-M01 — Recover comparison_literal_fault without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes comparison_literal_fault.
- Method: Parse the two divergence values as integers and require both to equal zero.
- Recurrence guard: Never compare native tab output to an escaped single-quoted literal; parse fields.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M01-WFAIL, V6486-M01-WPASS

### V6486-M02 — Recover hash_domain_assumption without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes hash_domain_assumption.
- Method: Verify Git blob identity in the blob domain and treat checkout bytes as a separately labelled working-tree domain.
- Recurrence guard: Do not mix filtered checkout byte counts with raw Git object byte sizes.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M02-WFAIL, V6486-M02-WPASS

### V6486-M03 — Recover unbounded_status_output without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes unbounded_status_output.
- Method: Run compact exact head, branch, clean, divergence, tracking, and live-remote probes after the successful fast-forward and push.
- Recurrence guard: Suppress or separate inherited change summaries; validate state with compact exact probes.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M03-WFAIL, V6486-M03-WPASS

### V6486-M04 — Recover memory_registry_no_match without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes memory_registry_no_match.
- Method: Retain the no-match and use the live activation, committed baton, and exact Git evidence as current authority.
- Recurrence guard: Treat exact-current memory absence as absence, not proof or contradiction.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M04-WFAIL, V6486-M04-WPASS

### V6486-M05 — Recover parallel_read_timeout without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes parallel_read_timeout.
- Method: Use bounded no-profile probes with a longer allowance and smaller output surfaces.
- Recurrence guard: Do not bind multiple PowerShell startup-heavy reads to a ten-second aggregate timeout.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M05-WFAIL, V6486-M05-WPASS

### V6486-M06 — Recover semantic_seed_collision without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes semantic_seed_collision.
- Method: Retain the collisions, inspect exact semantic neighbors, and replace them with different mechanisms and domains.
- Recurrence guard: Treat plausible novelty as a hypothesis until both lexical and substantive neighbor audits pass.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M06-WFAIL, V6486-M06-WPASS

### V6486-M07 — Recover broad_regex_false_neighbor without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes broad_regex_false_neighbor.
- Method: Reject the collided seeds and use exact-token and proposal-title-domain searches before manual semantic review.
- Recurrence guard: Use word-bounded exact identifiers and frozen proposal titles, not broad substrings, for novelty evidence.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M07-WFAIL, V6486-M07-WPASS

### V6486-M08 — Recover truncated_scaffold_copy without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes truncated_scaffold_copy.
- Method: Replace only the owner-created untracked scaffold with a compact x1-specific builder and preflight it from the local file.
- Recurrence guard: Never use display-truncated command output as source-file content; build compact successors or read bounded complete sections.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M08-WFAIL, V6486-M08-WPASS

### V6486-M09 — Recover threshold_proposal_collision without erasing its failed witness

- Trigger: A bounded v648-v6 workflow exposes threshold_proposal_collision.
- Method: Retain the refusal and narrow the title to theatre cancellation, cultural-content stewardship, performer-audience confidentiality, ticket redress, consent provenance, taonga reservation, and decision rights without weakening its gates.
- Recurrence guard: Do not rely on a generic authority-matrix title; expose the phase-specific mechanism while preserving the full gate body.
- Rollback: Give the failed attempt no proof credit, retain it, and rely only on a bounded passing witness.
- Witnesses: V6486-M09-WFAIL, V6486-M09-WPASS

### V6486-M10 — Recover mechanical owner-origin drift without erasing its failed witness

- Trigger: A mechanically adapted successor test retains a predecessor owner token.
- Method: Correct only the owner-origin assertion to orin_v648_v6_new and rerun the bounded x1 suite.
- Recurrence guard: Audit owner, slug, branch, and origin tokens independently after mechanical phase-number replacement.
- Rollback: Give the failing suite no pass credit, retain the mismatch, and keep the generated packet unchanged.
- Witnesses: V6486-M10-WFAIL, V6486-M10-WPASS

### V6486-M11 — Refresh lifecycle receipts before rerunning an aggregate

- Trigger: A correction mutates tests or Method Flow after an earlier manifest was generated.
- Method: Withhold aggregate credit, complete the pending fail/pass Method Flow lifecycle, validate and summarize it, then regenerate the manifest before retry.
- Recurrence guard: After any Method Flow or covered-file mutation, refresh lifecycle receipts and the exact manifest before a broad validation attempt.
- Rollback: Retain the premature aggregate as a failure and do not treat its passing subtests as an aggregate pass.
- Witnesses: V6486-M11-WFAIL, V6486-M11-WPASS

### V6486-M12 — Move quote-bearing staged review out of inline PowerShell

- Trigger: Exact staged review combines Python regex syntax with Windows PowerShell string parsing.
- Method: Use a dedicated UTF-8 Python runner with explicit staged-blob, manifest, JSON, diff-hygiene, and scanner-definition domains.
- Recurrence guard: Do not embed quote-bearing privacy regexes inside a PowerShell inline Python string.
- Rollback: Retain the parser fault, confirm the index is unchanged, and stage only after the dedicated runner and manifest are current.
- Witnesses: V6486-M12-WFAIL, V6486-M12-WPASS

### V6486-M13 — Require diff hygiene before staged-review credit

- Trigger: A newly added x1 runner is staged for exact review.
- Method: Trim only the extra trailing blank line, preserve one final newline, regenerate covered hashes, and restage the exact surface.
- Recurrence guard: Run diff hygiene on every new runner before awarding staged-review credit.
- Rollback: Retain the failed review and do not award path, JSON, privacy, or staged aggregate credit from the attempt.
- Witnesses: V6486-M13-WFAIL, V6486-M13-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
