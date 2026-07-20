# GHC Family Method Flow State

- Phase: v650-v8
- Owner: Ilyra Fen
- Methods: 15
- Passing witnesses: 17
- Failed witnesses retained: 18

## Preferred methods

### V6508-M01 — Recover from combined broad Git preflight timeout without erasing the failed witness

- Trigger: combined broad Git preflight timeout
- Method: Split branch, live-ref, worktree, ancestry, and status checks into independently bounded probes.
- Recurrence guard: Never combine broad branch, ref, worktree, and status discovery under one short wrapper.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M01-WFAIL, V6508-M01-WPASS

### V6508-M02 — Recover from native output early-close failure without erasing the failed witness

- Trigger: native output early-close failure
- Method: Consume the complete immutable blob first and then slice the in-memory text for inspection.
- Recurrence guard: Do not pipe native Git blob output to an early-closing consumer when complete-read evidence is required.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M02-WFAIL, V6508-M02-WPASS

### V6508-M03 — Recover from short-bound Git diff timeout without erasing the failed witness

- Trigger: short-bound Git diff timeout
- Method: Use explicit tracked-status and untracked-count probes with a wider bounded wrapper.
- Recurrence guard: Use attributable status probes instead of a short silent diff wrapper on a large Windows worktree.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M03-WFAIL, V6508-M03-WPASS

### V6508-M04 — Recover from PowerShell foreach pipeline parse without erasing the failed witness

- Trigger: PowerShell foreach pipeline parse
- Method: Materialize foreach output in an explicit array before piping or serializing it.
- Recurrence guard: Never pipe directly from a statement-level foreach block in Windows PowerShell 5.1.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M04-WFAIL, V6508-M04-WPASS

### V6508-M05 — Recover from bounded search early-close failure without erasing the failed witness

- Trigger: bounded search early-close failure
- Method: Read exact files and bounded result sets without prematurely closing the producer.
- Recurrence guard: Do not grant search credit when an early consumer termination makes producer completion ambiguous.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M05-WFAIL, V6508-M05-WPASS

### V6508-M06 — Recover from owner-manifest coverage scope error without erasing the failed witness

- Trigger: owner-manifest coverage scope error
- Method: Compare the immutable source-to-final path set across documentation, scripts, and tests against the declared owner manifest and exclusions.
- Recurrence guard: Define owner coverage from the exact Git change set, never from one assumed subtree.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M06-WFAIL, V6508-M06-WPASS

### V6508-M07 — Recover from stale Method Flow subcommand names without erasing the failed witness

- Trigger: stale Method Flow subcommand names
- Method: Inspect the installed record, witness, and set-state help and use only those exact subcommands.
- Recurrence guard: Treat remembered local-runner subcommands as unverified until current --help confirms them.
- Rollback: Give the failed operation zero pass credit, preserve its negative, and leave source, sibling, external, participant, production, and authority state unchanged.
- Witnesses: V6508-M07-WFAIL, V6508-M07-WPASS

### V6508-M08 — Split broad builder patches at exact current function boundaries

- Trigger: A long patch spans multiple generated-style regions and one remembered context line is stale.
- Method: Read the exact current function boundaries and split the update into small uniquely anchored patches.
- Recurrence guard: Do not combine unrelated builder changes behind one long remembered context block.
- Rollback: Treat the rejected patch as zero change and preserve the pre-patch file unchanged.
- Witnesses: V6508-M08-WFAIL, V6508-M08-WPASS, V6508-M08-WFAIL2, V6508-M08-WPASS2

### V6508-M09 — Inspect exact UTF-8 source bytes before patching rendered separators

- Trigger: Console rendering differs from the UTF-8 code points stored in a source literal.
- Method: Patch non-Unicode fields independently, then inspect exact source bytes before replacing the two rendered separator literals.
- Recurrence guard: Do not use console-rendered mojibake as patch context for UTF-8 source.
- Rollback: Treat the rejected patch as zero change and preserve the UTF-8 source unchanged.
- Witnesses: V6508-M09-WFAIL, V6508-M09-WPASS, V6508-M09-WFAIL2, V6508-M09-WFAIL3, V6508-M09-WPASS3

### V6508-M10 — Invoke the skill validator only with an actual skill directory

- Trigger: A helper script may not implement argparse-style help and expects a positional skill path.
- Method: Use init_skill.py help for initialization syntax, inspect the validator entrypoint contract, and invoke quick_validate.py only with an actual phase-local skill directory.
- Recurrence guard: Do not assume helper scripts implement argparse-style --help; inspect their entrypoint before probing.
- Rollback: Give the rejected helper invocation zero skill-validation credit and leave phase-local skill state unchanged.
- Witnesses: V6508-M10-WFAIL, V6508-M10-WPASS

### V6508-M11 — Split Git state and source inspection into bounded probes

- Trigger: A combined Windows repository-state and source-inspection wrapper approaches its time bound.
- Method: Split repository state and exact-file code inspection into independently bounded probes and avoid coupling slow Git status to source inspection.
- Recurrence guard: Do not combine potentially slow Windows Git status with multi-file source inspection under one short wrapper.
- Rollback: Give the timed-out wrapper zero pass credit and leave repository, branch, remote, sibling, participant, production, and authority state unchanged.
- Witnesses: V6508-M11-WFAIL, V6508-M11-WPASS

### V6508-M12 — Use an evidence-sized bound for staged-manifest refresh

- Trigger: The expanded owner staged surface cannot be hashed within a generic short inspection wrapper.
- Method: Run the single attributable manifest refresh under an evidence-sized bounded wrapper, then independently parse its manifest and privacy receipts.
- Recurrence guard: Size manifest-refresh bounds to the measured owner surface rather than a generic short inspection timeout.
- Rollback: Give partial refresh output zero parity credit and preserve all previously committed x1 and sibling state unchanged.
- Witnesses: V6508-M12-WFAIL, V6508-M12-WPASS

### V6508-M13 — Bind closeout prose to the exact frozen proposal schema

- Trigger: Lifecycle prose is generated from proposal fields whose names may differ across phase schemas.
- Method: Inspect the exact frozen proposal schema and use its current falsifier_or_acceptance_gate field in both overview and baton generation.
- Recurrence guard: Read frozen proposal keys directly before reusing a field name from an earlier phase schema.
- Rollback: Give the stopped build zero closeout credit and preserve the immutable evidence commit unchanged.
- Witnesses: V6508-M13-WFAIL, V6508-M13-WPASS

### V6508-M14 — Resolve the exact source-ledger path before schema inspection

- Trigger: A generated phase ledger filename is remembered rather than read from the exact directory.
- Method: List the exact bounded source directory, select the committed source ledger by its real name, and inspect only that file.
- Recurrence guard: Resolve generated ledger filenames from the exact phase directory before opening them.
- Rollback: Give the failed read zero schema credit and leave repository state unchanged.
- Witnesses: V6508-M14-WFAIL, V6508-M14-WPASS

### V6508-M15 — Classify final privacy candidates by exact reviewed path

- Trigger: A final scan reports candidates outside its exact scanner-definition quarantine.
- Method: Read only the generated candidate rows, quarantine exact scanner-definition or retained-policy files if justified, remove any genuine payload, and rerun all five unchanged pattern classes.
- Recurrence guard: Expand privacy-definition quarantine only from exact reviewed candidate paths, never from directory-wide assumptions.
- Rollback: Give the partial packet zero final or seal credit and retain the unchanged evidence commit as the last remote-equal anchor.
- Witnesses: V6508-M15-WFAIL, V6508-M15-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
