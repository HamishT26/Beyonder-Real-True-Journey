# GHC Family Method Flow State

- Phase: v648-gmut-thos-v5-x1-x2
- Owner: Sable Rook
- Methods: 6
- Passing witnesses: 6
- Failed witnesses retained: 6

## Preferred methods

### V6485-M01 — Treat exact-current memory no-match as absence, not continuity

- Trigger: The live activation refers to a phase newer than the current memory registry entries.
- Method: Record the no-match, use the live activation and exact committed baton as authority, and infer nothing from registry silence.
- Recurrence guard: Never turn an absent memory hit into identity, continuity, or completion evidence.
- Rollback: Give the lookup zero continuity credit and retain the live request as the controlling authority.
- Witnesses: V6485-M01-WFAIL, V6485-M01-WPASS

### V6485-M02 — Split broad worktree startup probes into bounded native checks

- Trigger: A large Windows worktree needs anchor, diff, index, and untracked checks before mutation.
- Method: Run anchor, tracked-diff, staged-diff, and untracked probes independently with native exit-code capture.
- Recurrence guard: Do not combine status, worktree listing, ancestry, and remote proof in one short startup wrapper.
- Rollback: Retain the timeout, give it no cleanliness credit, and use only the bounded recovery results.
- Witnesses: V6485-M02-WFAIL, V6485-M02-WPASS

### V6485-M03 — Pin UTF-8 before Unicode-bearing diagnostics

- Trigger: A diagnostic may emit Māori or other non-ASCII text on Windows PowerShell.
- Method: Set console output and Python I/O encoding to UTF-8 before reading or emitting the exact text.
- Recurrence guard: Pin UTF-8 before every Unicode-emitting phase command, builder, validator, and source diagnostic.
- Rollback: Retain the mojibake witness, leave the Git blob unchanged, and rerun only the diagnostic with UTF-8 pinned.
- Witnesses: V6485-M03-WFAIL, V6485-M03-WPASS

### V6485-M04 — Use one indexed-path collision audit instead of repeated full scans

- Trigger: Many proposed family-current package names require an exact pre-build collision check.
- Method: Query Git's indexed path list once, then apply one exact-name alternation and adjudicate only returned paths.
- Recurrence guard: Do not launch one full historical content scan per proposed package name.
- Rollback: Retain the timeout, create no package from the failed scan, and use only indexed-path results.
- Witnesses: V6485-M04-WFAIL, V6485-M04-WPASS

### V6485-M05 — Keep exact-name collision checks in the indexed path domain

- Trigger: Exact family-current skill and runner names need collision evidence across a very large historical repository.
- Method: Filter the Git indexed-path list, report exact matching filenames, and inspect content only for the small returned set.
- Recurrence guard: Do not use whole-body traversal for a package-name collision question that the index can answer.
- Rollback: Retain the failed recovery, give it no novelty credit, and rely only on the indexed-path pass.
- Witnesses: V6485-M05-WFAIL, V6485-M05-WPASS

### V6485-M06 — Keep x2 scaffolding absent from the x1 worktree surface

- Trigger: A successor phase adapts a prior phase's multi-stage builder family before x1 is committed.
- Method: Keep only definitions, x1 builder, and x1 tests in the owner worktree until x1 is committed, pushed, and remote-equal.
- Recurrence guard: Do not materialize x2 runtime, evidence, closeout, or outcome tests before the x1 publication gate.
- Rollback: Remove only the exact owner-created untracked placeholders and recreate them from the frozen x1 commit after publication.
- Witnesses: V6485-M06-WFAIL, V6485-M06-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
