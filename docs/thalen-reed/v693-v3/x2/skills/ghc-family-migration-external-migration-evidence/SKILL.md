---
name: ghc-family-migration-external-migration-evidence
description: Expose missing external migration evidence without promoting local assertions. Use for bounded synthetic configuration review with explicit inputs and retained refusals.
---

# Expose missing external migration evidence without promoting local assertions.

Use this skill when a reviewer needs the exact external_migration_evidence contract. Read the operation guide in references/contract.md before execution.

1. Keep the original record and the full request envelope. Supply exactly op, record and args.
2. Use operation external_migration_evidence with the literal argument shape shown in the guide. No external changes are performed.
3. Run the adjacent owner TXT runner ghc_family_config_migration_x2_5.txt with a UTF-8 request on stdin. Its fixed source binding must match before compilation.
4. Compare the complete response, including disposition, error, external_credit and all value fields. Preserve malformed subjects separately from a passing refusal check.
5. Preserve the original input and every failed attempt. A corrected request is a separate witness and does not erase failure.

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
