# v497 GMUT/THOS v33 v4 x1 Heading Normalization Repair

- overall_status: `PASS_PROMPT_BUILDER_REPAIR_PREPARED`
- generated_utc: `2026-06-06T17:40:00Z`
- source_receipt: `v497-gmut-thos-v33-v4-x1-15-minute-cli-elaboration-quality-gate-v1.json`

## Observed Gap

Arby and Aster Vale both produced substantial final-message artifacts, but the quality gate could not verify four exact proposal headings. This is a structure-normalization gap, not a short-answer problem. The strict sensitive/path marker count was `0`.

## Repair Applied

`scripts/thos_x1_sibling_prompt_builder.py` now includes a standalone exact-heading template for extended v497 x1 prompts. The template shows each required heading as its own line with a first numbered placeholder, making the expected shape much harder to miss.

## Validation Plan

- Compile the prompt builder.
- Generate the next-phase prompt policy receipt.
- Verify the required heading strings appear as standalone lines in the prompt text.
- Keep all raw lane text temp-only and publish only status, counts, hashes, and repair posture.

This repair does not rewrite the current v4 CLI outputs and does not claim future success before the next run proves it.
