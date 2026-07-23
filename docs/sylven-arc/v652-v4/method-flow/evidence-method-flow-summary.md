# GHC Family Method Flow State

- Phase: v652-v4
- Owner: Sylven Arc
- Methods: 15
- Passing witnesses: 15
- Failed witnesses retained: 15

## Preferred methods

### V6524-METHOD-01 — Bounded recovery for baton_display_truncation

- Trigger: baton_display_truncation
- Method: Read the immutable file in fixed line slices from a materialized line array.
- Recurrence guard: Use bounded fixed slices for long authoritative files.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-01-F, V6524-WITNESS-01-P

### V6524-METHOD-02 — Bounded recovery for baton_chunk_still_too_large

- Trigger: baton_chunk_still_too_large
- Method: Reduce slices to fifty lines and continue monotonically through EOF.
- Recurrence guard: Lower chunk size immediately when a bounded display still truncates.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-02-F, V6524-WITNESS-02-P

### V6524-METHOD-03 — Bounded recovery for combined_read_only_probe_timeout

- Trigger: combined_read_only_probe_timeout
- Method: Split exact Git scalars, cleanliness, storage, and manifest probes.
- Recurrence guard: Do not aggregate unrelated large-tree probes under one deadline.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-03-F, V6524-WITNESS-03-P

### V6524-METHOD-04 — Bounded recovery for fast_forward_verbose_output

- Trigger: fast_forward_verbose_output
- Method: Do not repeat the mutation; verify exact head, branch, clean state, ancestry, and remote equality with scalar reads.
- Recurrence guard: Treat progress suppression as advisory and rely on scalar postconditions.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-04-F, V6524-WITNESS-04-P

### V6524-METHOD-05 — Bounded recovery for broad_inventory_timeout

- Trigger: broad_inventory_timeout
- Method: Use exact Git-tree phase-root enumeration and bounded source probes.
- Recurrence guard: Prefer exact phase-root enumeration over broad parallel scans.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-05-F, V6524-WITNESS-05-P

### V6524-METHOD-06 — Bounded recovery for parallel_line_count_timeout

- Trigger: parallel_line_count_timeout
- Method: Use one repository-local enumeration process.
- Recurrence guard: Keep small filesystem metadata reads in one local process.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-06-F, V6524-WITNESS-06-P

### V6524-METHOD-07 — Bounded recovery for source_search_output_truncation

- Trigger: source_search_output_truncation
- Method: Search and open the exact OASIS OpenDocument 1.4 package target only.
- Recurrence guard: Use one exact standards target for final source verification.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-07-F, V6524-WITNESS-07-P

### V6524-METHOD-08 — Bounded recovery for doi_redirect_open_refusal

- Trigger: doi_redirect_open_refusal
- Method: Use an exact bibliographic search and authoritative metadata result without bypassing the wrapper.
- Recurrence guard: Use exact bibliographic discovery when direct DOI redirects are unavailable.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-08-F, V6524-WITNESS-08-P

### V6524-METHOD-09 — Bounded recovery for inherited_identifier_uniqueness_assumption

- Trigger: inherited_identifier_uniqueness_assumption
- Method: Preserve every inherited row unchanged, record the historical duplicates, and require only that all thirty v652-v4 identifiers are unique and absent from the inherited identifier set.
- Recurrence guard: Treat immutable predecessor rows as authoritative evidence and scope new-identifier uniqueness to the additive phase.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-09-F, V6524-WITNESS-09-P

### V6524-METHOD-10 — Bounded recovery for method_flow_count_key_assumption

- Trigger: method_flow_count_key_assumption
- Method: Read the Method Flow schema's nested witness_results fail and pass counters without changing the ledger.
- Recurrence guard: Bind tests to the current Method Flow count schema instead of inferred aliases.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-10-F, V6524-WITNESS-10-P

### V6524-METHOD-11 — Bounded recovery for ordinary_document_cap_domain_assumption

- Trigger: ordinary_document_cap_domain_assumption
- Method: Apply the cap to ordinary narrative Markdown, HTML, and text documents while recording machine-ledger counts separately.
- Recurrence guard: Declare ordinary narrative and machine-ledger cap domains explicitly.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-11-F, V6524-WITNESS-11-P

### V6524-METHOD-12 — Bounded recovery for powershell_hash_literal_command_expression

- Trigger: powershell_hash_literal_command_expression
- Method: Compute Git head, status count, and diff exit as separate scalar variables before constructing the summary object.
- Recurrence guard: Keep command execution outside PowerShell hash-literal value expressions.
- Rollback: Stop, retain the failed witness, and leave external, sibling, participant, production, professional, legal, cultural, and authority state unchanged.
- Witnesses: V6524-WITNESS-12-F, V6524-WITNESS-12-P

### V6524-METHOD-13 — Bounded recovery for skill_validator_help_assumption

- Trigger: skill_validator_help_assumption
- Method: Invoke quick_validate.py with each concrete phase-local skill directory after deterministic initialization and customization.
- Recurrence guard: Treat quick_validate.py as a positional path validator rather than an argparse help surface.
- Rollback: Stop, retain the failed probe, and leave global skills, sibling state, external systems, and authority state unchanged.
- Witnesses: V6524-WITNESS-13-F, V6524-WITNESS-13-P

### V6524-METHOD-14 — Bounded recovery for dual_import_context_assumption

- Trigger: dual_import_context_assumption
- Method: Support both direct runner execution and package-based unittest import with a narrow phase-data import fallback.
- Recurrence guard: Exercise family-current modules both as direct scripts and package imports.
- Rollback: Stop, retain the failed probe, and leave global skills, sibling state, external systems, and authority state unchanged.
- Witnesses: V6524-WITNESS-14-F, V6524-WITNESS-14-P

### V6524-METHOD-15 — Bounded recovery for family_current_runner_allowlist_assumption

- Trigger: family_current_runner_allowlist_assumption
- Method: Allow exactly the ten runner filenames frozen in x1 plus the explicit v652-v4 builder, core, validator, and test paths, without broadening the scripts directory.
- Recurrence guard: Derive staged script allowlists from the frozen runner ledger rather than requiring phase tokens in family-current compatibility names.
- Rollback: Stop, retain the failed probe, and leave global skills, sibling state, external systems, and authority state unchanged.
- Witnesses: V6524-WITNESS-15-F, V6524-WITNESS-15-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
