# v462A_GMUT_v6 Aster Vale CLI Advisory Report v1

Generated UTC: 2026-05-29T10:08:26Z
Generated NZ: 2026-05-29T22:08:26+12:00
Phase version: v462A_GMUT_v6
Boundary: branch-local CLI advisory only; not shared omega publication proof.

## Lane Proof

- evidence: Parent-shell checkpoint path was `D:/GHC-Archives/agent-worktrees/v461-round-robin/aster-vale-advisory`.
- evidence: Branch was `ghc/aster-vale-advisory-line` with upstream `origin/ghc/aster-vale-advisory-line`.
- evidence: Parent-shell local and upstream heads were both `7c0576c6c98529e6ec80913c9de6a757956c0a47`, drift `0 0`, with clean tracked status.
- evidence: Parent-shell Codex CLI version was verified as `codex-cli 0.135.0`.
- context: Shared omega v5 head `b7e82d0da1274b5b5579ac8eb8203ffed05bb95c` was treated as context for the requested v6 advisory.

## Fresh CLI Report Attempt

- evidence: A read-only `codex exec` advisory report was launched inside the Aster Vale lane.
- blocker: The child read-only advisory did not produce a final-message file within the bounded phase window.
- blocker: The child process was stopped after the bounded wait to prevent stale background work from overlapping the next heartbeat.
- boundary: Raw event logs were not staged, summarized as proof, or treated as completed advisory content.

## v6 Use

- advisory: v6 uses Aster Vale's parent-shell branch proof and records the child report as blocked.
- advisory: v7 may retry a narrower Aster Vale prompt if CLI report depth is still useful, but it should avoid broad repo scans that risk long-running raw output.
