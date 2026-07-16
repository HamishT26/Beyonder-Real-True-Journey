# GHC Family Method Flow State

- Phase: v646-gmut-thos-v1-x1-x2
- Owner: Eiren Kestrel
- Methods: 5
- Passing witnesses: 5
- Failed witnesses retained: 5

## Preferred methods

### V6461-M01 — Split a timed-out parallel startup and source-introspection probe

- Trigger: shared-drive repository; multiple evidence-producing children; fail-fast wrapper returned a partial result
- Method: Split shared-drive startup probes by evidence surface and give every child an independent deadline and credit decision.
- Recurrence guard: A timed-out orchestration wrapper supplies no evidence for children whose complete result was not returned.
- Rollback: Give the partial wrapper zero startup credit and make no phase mutation until every required split probe passes.
- Witnesses: V6461-W01-F, V6461-W01-P

### V6461-M02 — Clear read-only Git fixture objects before bounded teardown

- Trigger: owner-local disposable fixture; resolved fixture inside declared scratch root; Git object carried a read-only attribute
- Method: Verify the resolved fixture remains inside the declared scratch root, clear only disposable file read-only bits through the deletion callback, and retry the same scoped teardown once.
- Recurrence guard: Never apply the writable-bit recovery to a canonical, sibling, unverified, or out-of-root path.
- Rollback: Retain the failed teardown, stop before any broader cleanup, and require an exact root-containment check.
- Witnesses: V6461-W02-F, V6461-W02-P

### V6461-M03 — Run skill quick validation under explicit UTF-8 on Windows

- Trigger: UTF-8 skill content; validator used locale-dependent default decoding; Windows CP1252 process environment
- Method: Preserve the skill content and rerun the unchanged skill-creator validator with Python UTF-8 mode explicitly enabled.
- Recurrence guard: Treat locale-dependent decoding failures as validation failures; never remove culturally correct text merely to obtain a pass.
- Rollback: Retain all twenty failed validator witnesses and give no skill validation credit until the explicit UTF-8 rerun passes.
- Witnesses: V6461-W03-F, V6461-W03-P

### V6461-M04 — Bind x1 absence assertions to the immutable x1 commit

- Trigger: x1 tests reused after x2 build; live worktree contains legitimate x2 artifacts; exact x1 commit remains available
- Method: Keep the x1 proposal and portfolio checks live, but evaluate no-x2 artifact assertions against the exact immutable x1 commit tree.
- Recurrence guard: Lifecycle-specific absence tests must name the immutable commit or stage they are proving instead of assuming the current worktree is still at that stage.
- Rollback: Give the failed combined run zero suite credit, retain both assertion failures, and rerun only after the snapshot-bound test passes.
- Witnesses: V6461-W04-F, V6461-W04-P

### V6461-M05 — Refresh logical manifest after lifecycle receipt mutation

- Trigger: phase lifecycle documents changed after evidence freeze; logical manifest covers one or more changed documents; exact evidence commit remains ancestral
- Method: After any lifecycle document changes, refresh the logical manifest before rerunning phase-local tests and validators, then verify the exact changed-file hashes rather than weakening manifest parity.
- Recurrence guard: Treat lifecycle receipt generation as a manifest-affecting mutation and refresh the manifest before any closeout validator is credited.
- Rollback: Give the failed lifecycle run zero validation credit, retain all three stale-hash findings, and stop before the closeout commit until exact manifest parity is restored.
- Witnesses: V6461-W05-F, V6461-W05-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
