# v499 GMUT/THOS v35 v3 x1 to x2 Prep Design Bank

- generated_utc: `2026-06-07T06:04:10Z`
- overall_status: `PASS_X2_PREP_READY_WITH_COMPLETION_GATE_HELD`
- target_phase_slug: `v499-gmut-thos-v35-v3-x2`

## Phase Boundary

Do not start x2 closeout until all five completion receipts are ready. This prep bank is allowed during the x1 cadence window, but it is not completion proof.

## X2 Build Candidates

- Build a watcher-control fallback hardening receipt that treats control timeout as a recoverable supervisor gap.
- Build a five-lane evidence matrix that requires app completion gate, CLI notifier, CLI quality gate, marker review, and exposure guard before x2 closeout.
- Build a source-to-runner map that links OpenAI/Codex release signals to CLI/App readiness checks.
- Build a source-to-security map that links MCP and OWASP guidance to status-only receipt design.
- Build a command-surface checklist for launch, wait, gate, notify, normalize, guard, exact-stage, publish, and remote-verify.
- Build a skills-overlay draft set without mutating user skills until exact approval is active.
- Build a stale-flow taxonomy for app watcher, CLI watcher, final-marker, loader warning, plugin-sync warning, source drift, and remote verification.
- Build a THOS AI-factory analogy map from NVIDIA architecture signals to local multi-agent orchestration patterns.
- Build an x2 publication preflight that refuses broad staging and refuses completion if any raw lane output appears.
- Build a v499 v4 launch readiness card only after v499 v3 x2 is published and remote-verified.
