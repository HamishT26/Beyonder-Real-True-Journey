# GHC Family Method Flow State

- Phase: v648-gmut-thos-v7-x1-x2
- Owner: Tamar Vey
- Methods: 13
- Passing witnesses: 30
- Failed witnesses retained: 28

## Preferred methods

### V6487-M01 — Normalize an exact no-match search without inventing continuity

- Trigger: A bounded registry search returns zero matching rows.
- Method: Treat a no-match registry search as an explicit zero-row result and use the live committed baton plus exact Git evidence as current authority.
- Recurrence guard: Normalize the documented no-match exit separately from execution errors and never infer continuity from silence.
- Rollback: Give the no-match no continuity credit and retain it as an operational negative.
- Witnesses: V6487-M01-WFAIL, V6487-M01-WPASS

### V6487-M02 — Materialize PowerShell loop results before piping

- Trigger: A bounded PowerShell receipt wrapper needs loop output in a pipeline.
- Method: Materialize PowerShell loop output into an array before piping it to JSON conversion.
- Recurrence guard: Use an explicit array assignment around foreach results before a pipeline.
- Rollback: Credit no output from the parser-failed attempt and preserve it as a negative.
- Witnesses: V6487-M02-WFAIL, V6487-M02-WFAIL-X1-02, V6487-M02-WPASS, V6487-M02-WPASS-X1-02, V6487-M02-WFAIL-X2-01, V6487-M02-WPASS-X2-01

### V6487-M03 — Use type-aware bounded receipt summaries

- Trigger: Heterogeneous JSON receipts require a read-only summary.
- Method: Inspect receipt types and keys before indexing optional manifest entries, then emit compact type-specific summaries.
- Recurrence guard: Branch on schema or keys before indexing optional arrays and bound output by receipt type.
- Rollback: Discard unsupported fields from the broad summary and retain the wrapper fault.
- Witnesses: V6487-M03-WFAIL, V6487-M03-WPASS, V6487-M03-WFAIL-X1-02, V6487-M03-WFAIL-X1-03, V6487-M03-WPASS-X1-02, V6487-M03-WPASS-X1-03, V6487-M03-WFAIL-X2-01, V6487-M03-WPASS-X2-01, V6487-M03-WFAIL-X2-02, V6487-M03-WPASS-X2-02, V6487-M03-WFAIL-X2-03, V6487-M03-WPASS-X2-03

### V6487-M04 — Separate Git blob identity from checkout-byte counts

- Trigger: A manifest declares different hash and checkout-byte domains.
- Method: Verify commit-local Git blob identity separately from the declared working-tree checkout-byte domain.
- Recurrence guard: Read manifest domain metadata before comparing hashes or byte counts.
- Rollback: Withdraw the false mismatch classification and retain the domain error.
- Witnesses: V6487-M04-WFAIL, V6487-M04-WPASS, V6487-M04-WFAIL-X2-01, V6487-M04-WPASS-X2-01

### V6487-M05 — Verify checkout bytes only in an exact checked-out domain

- Trigger: Checkout-byte parity is needed without creating a replay lane.
- Method: Use the exact checked-out final worktree for checkout-byte verification and immutable commit objects for historical blob verification.
- Recurrence guard: Do not treat cat-file filters output as a historical checkout-byte reconstruction contract.
- Rollback: Give the failed reconstruction no proof credit and do not create a temporary replay lane.
- Witnesses: V6487-M05-WFAIL, V6487-M05-WPASS

### V6487-M06 — Prove fast-forward state with a compact postflight

- Trigger: A successful additive fast-forward emits an unbounded inherited diffstat.
- Method: Use a compact post-fast-forward probe for branch, head, clean status, ancestry, tracking, divergence, and live remote equality.
- Recurrence guard: Treat verbose fast-forward output as lifecycle noise and prove state with a separate compact exact probe.
- Rollback: Give the truncated summary no proof credit; do not repeat the fast-forward.
- Witnesses: V6487-M06-WFAIL, V6487-M06-WPASS, V6487-M06-WFAIL-X1-02, V6487-M06-WPASS-X1-02

### V6487-M07 — Use explicit UTF-8 for proposal audit output

- Trigger: Repository proposal titles may contain non-ASCII text.
- Method: Configure the child process stdout stream explicitly as UTF-8 before emitting proposal titles.
- Recurrence guard: Set explicit UTF-8 for machine-readable child-process output containing repository text.
- Rollback: Credit no complete novelty scan from the interrupted output and retain the encoding fault.
- Witnesses: V6487-M07-WFAIL, V6487-M07-WPASS, V6487-M07-WFAIL-X2-01, V6487-M07-WPASS-X2-01

### V6487-M08 — Replace collided proposal seeds after full-chain neighbour review

- Trigger: A candidate proposal batch has been compared with all 620 frozen titles.
- Method: Reject collided seeds, inspect their exact semantic neighbours, and replace them with mechanisms and practice domains absent from the 620-title chain.
- Recurrence guard: Treat every plausible title as a hypothesis until both lexical and substantive neighbour audits pass against all frozen proposals.
- Rollback: Discard all collided seed titles, retain the audit receipt, and award no novelty credit.
- Witnesses: V6487-M08-WFAIL, V6487-M08-WPASS

### V6487-M09 — Quarantine protected-gate vocabulary without weakening privacy scanning

- Trigger: A five-class scan finds a credential term inside an explicit unexecuted approval boundary.
- Method: Quarantine the exact approval register as protected-gate vocabulary while preserving the candidate and the unchanged five-class scanner.
- Recurrence guard: Distinguish protected-gate vocabulary from credential assignment or secret material without weakening the pattern set.
- Rollback: Keep x1 uncommitted, retain the candidate, and make no zero-hit claim until a bounded passing scan exists.
- Witnesses: V6487-M09-WFAIL, V6487-M09-WPASS, V6487-M09-WPASS-X1-02, V6487-M09-WFAIL-X2-01, V6487-M09-WPASS-X2-01

### V6487-M10 — Order privacy promotion behind complete-surface generation

- Trigger: A privacy pass would add new Method Flow evidence files to the surface it claims to cover.
- Method: Promote privacy recovery only after a complete generated-surface preview and require a final scan covering the new promotion evidence.
- Recurrence guard: Never promote before the full generated surface exists and a post-promotion final scan can cover the evidence files.
- Rollback: Demote the method, keep x1 uncommitted, and retain both the premature pass and later failed scan.
- Witnesses: V6487-M10-WFAIL, V6487-M10-WPASS, V6487-M10-WPASS-X1-02

### V6487-M11 — Verify function scope after context-based patching

- Trigger: A multi-function source file receives a context-based patch near repeated call shapes.
- Method: Move the receipt write into the manifest function and inspect enclosing function boundaries plus AST before execution.
- Recurrence guard: After context-based patches, inspect enclosing function boundaries rather than relying on syntax alone.
- Rollback: Do not execute the misplaced source; retain the defect and correct it additively before retry.
- Witnesses: V6487-M11-WFAIL, V6487-M11-WPASS, V6487-M11-WFAIL-X2-01, V6487-M11-WPASS-X2-01, V6487-M11-WFAIL-X2-02, V6487-M11-WPASS-X2-02

### V6487-M12 — Correct narrowed Method Flow scope additively

- Trigger: A later bounded witness exposes that an earlier preferred method covered a narrower surface.
- Method: Preserve immutable preferred history and add a stricter method whose promotion gate covers the newly exposed scope.
- Recurrence guard: Treat promotion as monotonic and use additive corrective methods rather than attempted demotion.
- Rollback: Credit no state change from the refused command and keep terminal evidence gated.
- Witnesses: V6487-M12-WFAIL, V6487-M12-WPASS, V6487-M12-WFAIL-X2-01, V6487-M12-WPASS-X2-01, V6487-M12-WFAIL-X2-02, V6487-M12-WPASS-X2-02

### V6487-M13 — Break scanner-output recursion with post-promotion coverage

- Trigger: A scanner receipt is itself included in the surface and Method Flow evidence is generated from its result.
- Method: Classify the preview as scanner output, run a complete pre-promotion scan, add recovery evidence, and run a second post-promotion scan before freeze.
- Recurrence guard: Quarantine scanner-output receipts explicitly and never describe a later scan as passed before it executes.
- Rollback: Keep x1 uncommitted, retain the recursive candidates and premature witness, and require a post-promotion scan.
- Witnesses: V6487-M13-WFAIL, V6487-M13-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
