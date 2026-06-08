# v502-gmut-thos-v38-v4-x1 Temp Output Hygiene Verifier Design

- generated_utc: `2026-06-08T07:17:37Z`
- overall_status: `PASS_TEMP_OUTPUT_HYGIENE_VERIFIER_DESIGN_READY`
- design_only: `True`
- full_x2_build_allowed: `False`
- blocked_until_arby_final_message: `True`

Design goal:
- Create a future verifier that checks CLI lane temp-output receipts publish only redacted names, counts, hashes, byte sizes, and status while keeping prompt bodies, raw lane text, event streams, stderr, and local temp paths unpublished.

Proposed checks:
- Receipt includes temp-output redaction boundary.
- Receipt does not publish local absolute paths.
- Receipt does not publish prompt body.
- Receipt does not publish raw final-message text.
- Receipt does not publish event JSONL content.
- Receipt does not publish stderr/stdout content.
- Receipt may publish byte counts, line counts, word counts, heading booleans, hashes, and safe bridge aliases.
- Receipt records whether original and repair processes were killed, left running, or completed.
- Receipt records next manual status check timestamp.
- Receipt records duration as non-proof.

Future CLI:
- Script candidate: `scripts/thos_cli_temp_output_hygiene_verifier.py`
- Inputs: phase slug, launcher receipt, quality gate receipt, live wait or repair receipt.
- Outputs: status-only JSON and Markdown receipts.
- Return policy: nonzero on publication-boundary open gap.

Publication boundary: status only; no raw lane text, raw logs, prompt bodies, local absolute paths, credentials, screenshots, or session streams.

Claim boundary: GMUT and canon gates remain open; duration is not completion proof.
