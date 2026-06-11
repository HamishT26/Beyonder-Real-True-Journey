# v507 GMUT/THOS v43 v6 x1 Arby Repair1 Halted No-Tools Blocker

- overall_status: `OPEN_GAP_REPAIR_HALTED_NO_TOOLS_CONTRACT`
- lane: `Arby`
- repair attempt: `repair1`
- blocker class: CLI read-only advisory route does not hard-disable shell/tool inspection.
- observed status: no final repair message was ready; the process was stopped because the repair lane began read-only shell inspection despite the no-tools advisory prompt.
- CLI help check: `codex exec --help` exposes read-only/workspace-write/danger-full-access sandbox modes, but no obvious hard no-tools/no-shell switch.
- boundary: no raw lane text, raw transport, raw shell commands, screenshots, credentials, local absolute paths, GMUT validation, or canon-promotion claim is published.

## Safe Next Options

1. Design a no-tools advisory wrapper that can enforce output-only behavior before relaunching Arby repairs.
2. Accept Arby's first pass only as structurally complete but depth-gated open, not as a full x1 closeout.
3. Keep v507 v6 x1 open until a safe elaboration repair or exact approval changes the lane contract.
4. Do not advance to v507 v6 x2 while this lane-quality blocker remains open.
