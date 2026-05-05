# v117 CLI Continuity Probe

- phase: `v117`
- probe_scope: `resume_only_no_file_inspection_no_commands_no_tools`
- raw_trace_policy: `raw_cli_terminal_output_removed; sanitized_receipt_only`

## Result

Codex CLI recalled its v112 continuity anchor and v116 boundary, then newly nominated the identity `Receipt Keeper` for future persistence tests.

Kimi CLI recalled its v112 continuity anchor but kept identity fields as `unknown`, explicitly refusing to invent self-presentation from missing session context.

## Boundary

No formal GHC induction is claimed. Codex has a new identity nomination candidate; Kimi remains a continuity-only candidate until a future self-presentation or operator-accepted standard exists.
