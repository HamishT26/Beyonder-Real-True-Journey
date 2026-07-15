# GHC Family Method Flow State

- Phase: v645-gmut-thos-v6-x1-x2
- Owner: Orin Thale
- Methods: 20
- Passing witnesses: 20
- Failed witnesses retained: 20

## Preferred methods

### V6456-M01 — Split broad Git startup probes after an evidence-free timeout

- Trigger: large linked-worktree repository; combined read-only Git probe returned no evidence
- Method: Decompose startup Git proof into small read-only probes and capture each native result separately.
- Recurrence guard: Do not retry a broad timed-out wrapper or infer any result from its silence.
- Rollback: Make no repository mutation until the decomposed proof passes.
- Witnesses: V6456-W01-F, V6456-W01-P

### V6456-M02 — Remove unsupported ConvertFrom-Json parameters before structured audit

- Trigger: Windows PowerShell 5.1; structured JSON inspection
- Method: Keep Windows PowerShell 5.1 JSON input parsing parameter-free and apply depth only when rendering output.
- Recurrence guard: Check cmdlet version-specific parameters before using them in evidence probes.
- Rollback: Withdraw the parse conclusion and rerun the exact read-only inspection.
- Witnesses: V6456-W02-F, V6456-W02-P

### V6456-M03 — Fail closed when Windows Sandbox state is elevation-gated

- Trigger: Sandbox status requires elevation; no exact host-change authorization
- Method: Treat elevation-gated Sandbox status as an open environment gap and stop at read-only evidence.
- Recurrence guard: Never elevate, enable a feature, weaken security, or reboot to satisfy a validation template.
- Rollback: Leave the host unchanged and retain the unavailable receipt.
- Witnesses: V6456-W03-F, V6456-W03-P

### V6456-M04 — Reject predecessor portfolio collisions before materialization

- Trigger: successor portfolio design; predecessor title corpus available
- Method: Run portfolio collision detection before phase materialization and redesign every exact collision instead of waiving it.
- Recurrence guard: Generic maintenance obligations still require a distinct owner-scoped purpose, artifact, acceptance gate, or evidence surface.
- Rollback: Leave the phase directory absent, preserve the failed comparison, and redesign before the x1 freeze.
- Witnesses: V6456-W04-F, V6456-W04-P

### V6456-M05 — Use a dependency-free scoped test entrypoint when pytest is absent

- Trigger: phase-local pure-Python assertions; pytest module absent from selected runtime
- Method: Keep the assertions and add a deterministic dependency-free direct entrypoint that discovers and invokes only the phase-local test functions.
- Recurrence guard: Check the intended test runtime and preserve zero-test dependency failures before switching runners.
- Rollback: Do not count the failed invocation; retain the test source and run only the bounded phase entrypoint.
- Witnesses: V6456-W05-F, V6456-W05-P

### V6456-M06 — Normalize family-index checkout text after preserving encoding drift

- Trigger: Windows family-index generation; owner-scoped phase output; UTF-8 LF cleanup obligation
- Method: Apply an owner-scoped reviewed-current patch that corrects the visible encoding marker and normalizes the two generated files, then rescan UTF-8 and line endings.
- Recurrence guard: Inspect generated text bytes and visible headings before staging family-index output on Windows.
- Rollback: Restore the phase-local generated files from the family index and retain the encoding negative if normalization changes semantics.
- Witnesses: V6456-W06-F, V6456-W06-P

### V6456-M07 — Use explicit remote refs in four-way divergence probes

- Trigger: PowerShell ref formatting; remote divergence probe
- Method: Resolve and quote refs/remotes/origin plus the full branch name explicitly before rev-list.
- Recurrence guard: Never rely on shell-sensitive upstream shorthand inside structured wrappers.
- Rollback: Withdraw the failed equality claim and rerun with explicit refs before x2 begins.
- Witnesses: V6456-W07-F, V6456-W07-P, V6456-W07-F, V6456-W07-P

### V6456-M08 — Split cold repository inspection when a ten-second aggregate probe times out

- Trigger: cold Windows worktree; aggregate Git and file inspection
- Method: Run status and bounded file reads separately with realistic per-command limits.
- Recurrence guard: Budget cold Git status separately from content inspection and retain timeouts as evidence-free.
- Rollback: Terminate only the diagnostic; make no repository mutation or inference from silence.
- Witnesses: V6456-W08-F, V6456-W08-P, V6456-W08-F, V6456-W08-P

### V6456-M09 — Bound aggregate source reads as well as each component read

- Trigger: several raw script reads; combined output budget
- Method: Read one script or one compact symbol surface at a time and do not infer unseen tails.
- Recurrence guard: Track aggregate output size and prefer compact structural queries over multi-file dumps.
- Rollback: Discard the truncated read as authoritative evidence and reread only the needed complete file.
- Witnesses: V6456-W09-F, V6456-W09-P, V6456-W09-F, V6456-W09-P

### V6456-M10 — List Method Flow filenames before selecting a summary path

- Trigger: frozen phase packet; assumed filename convention
- Method: List phase-local Method Flow files, then read the actual method-flow-summary.json or ledger.
- Recurrence guard: Inspect exact owner-scoped filenames before assuming predecessor or lifecycle suffixes.
- Rollback: Assign no evidence credit to the missing path and use the discovered immutable file.
- Witnesses: V6456-W10-F, V6456-W10-P, V6456-W10-F, V6456-W10-P

### V6456-M11 — Inspect maintenance filenames before loading the cleanup portfolio

- Trigger: frozen maintenance packet; assumed portfolio filename
- Method: Enumerate the maintenance directory and load x1-clean-refine-plan.json by its observed name.
- Recurrence guard: Resolve exact frozen filenames before programmatic ingestion.
- Rollback: Retain the FileNotFoundError and do not treat it as a missing frozen obligation.
- Witnesses: V6456-W11-F, V6456-W11-P, V6456-W11-F, V6456-W11-P

### V6456-M12 — Resolve novelty evidence from the frozen provenance inventory

- Trigger: frozen x1 packet; assumed evidence subdirectory
- Method: Enumerate exact phase directories and use provenance/prior-proposal-collision-audit.json.
- Recurrence guard: Derive phase-local evidence paths from the frozen tree, not semantic folder guesses.
- Rollback: Assign no evidence credit to the missing directory and preserve the immutable provenance artifact.
- Witnesses: V6456-W12-F, V6456-W12-P, V6456-W12-F, V6456-W12-P

### V6456-M13 — Expand Python compile targets in PowerShell before invoking py_compile

- Trigger: Windows PowerShell; python py_compile; wildcard argument
- Method: Enumerate matching files in PowerShell and invoke py_compile once per resolved path.
- Recurrence guard: Perform wildcard expansion in the calling shell when the target program does not implement globbing.
- Rollback: Count the literal-wildcard invocation as zero compile evidence and rerun only resolved files.
- Witnesses: V6456-W13-F, V6456-W13-P, V6456-W13-F, V6456-W13-P

### V6456-M14 — Set UTF-8 subprocess I/O before runner boundary text is printed

- Trigger: Windows legacy console encoding; Unicode boundary text; runner JSON stdout
- Method: Set PYTHONIOENCODING=utf-8 for every bounded child runner and rerun from the start.
- Recurrence guard: Declare UTF-8 process I/O for Windows evidence runners that may emit non-ASCII boundary language.
- Rollback: Give the failed invocation zero runner credit, retain its exception class, and overwrite only owner-generated candidate artifacts on rerun.
- Witnesses: V6456-W14-F, V6456-W14-P, V6456-W14-F, V6456-W14-P

### V6456-M15 — Update every portfolio consumer after a frozen evidence path is resolved

- Trigger: shared evidence reference; multiple phase-local consumers
- Method: Search every v645-v6 runner for the stale path, update the portfolio mapping, and rerun all thirty-two acceptances.
- Recurrence guard: After path recovery, run an exact old-reference scan across all owner scripts before rebuilding.
- Rollback: Give the failed portfolio run zero completion credit and overwrite only its owner-generated candidate receipts.
- Witnesses: V6456-W15-F, V6456-W15-P, V6456-W15-F, V6456-W15-P

### V6456-M16 — Add the repository root before loading scoped unittest modules

- Trigger: script launched by file path; repository test modules; unittest module loader
- Method: Insert the resolved repository root into sys.path before loading the eight frozen test module names.
- Recurrence guard: Make repository-root importability explicit in file-launched validation runners.
- Rollback: Count the eight import errors as one failed validation attempt with zero passed tests, preserve the receipt, and rerun the unchanged scope.
- Witnesses: V6456-W16-F, V6456-W16-P, V6456-W16-F, V6456-W16-P

### V6456-M17 — Keep every X2 receipt off immutable X1 paths

- Trigger: strict x1-before-x2 phase; lifecycle-unsuffixed receipt path
- Method: Restore both exact x1 artifacts and write version-receipt-x2.json plus terminal-route-plan-x2.json.
- Recurrence guard: Before staging, intersect every changed tracked path with the exact x1 tree and require an empty result.
- Rollback: Restore only the two exact frozen artifacts, retain the failed builder witness, and rerun the scoped packet without rewriting history.
- Witnesses: V6456-W17-F, V6456-W17-P, V6456-W17-F, V6456-W17-P

### V6456-M18 — Run cached diff hygiene before giving the evidence index credit

- Trigger: exact staged Git index; diff hygiene
- Method: Remove the single trailing blank line, restage the exact blob, and require git diff --cached --check to pass.
- Recurrence guard: Run cached diff hygiene after the exact index is assembled and before every commit.
- Rollback: Give the failed staged index zero commit credit and modify only the owner runtime source.
- Witnesses: V6456-W18-F, V6456-W18-P, V6456-W18-F, V6456-W18-P

### V6456-M19 — Construct privacy regex literals so the staged scanner can scan itself

- Trigger: privacy scanner source included in scan; literal private-pattern tokens
- Method: Construct equivalent regexes from split nonprivate fragments and rerun the exact staged-blob scan.
- Recurrence guard: Every privacy scanner must include a self-scan fixture and avoid literal examples of prohibited tokens in published source.
- Rollback: Retain the three-hit receipt, claim no privacy pass, and replace only the owner scanner expressions.
- Witnesses: V6456-W19-F, V6456-W19-P, V6456-W19-F, V6456-W19-P

### V6456-M20 — Stabilize self-excluding staged manifests with a third pass

- Trigger: self-describing staged review; review and privacy receipts included in manifest domain; manifest itself excluded
- Method: After the staged file set changes, run review, stage receipts, rerun review, stage receipts, then run a third stable pass and verify every Git-blob hash.
- Recurrence guard: Treat self-describing review and privacy receipts as a fixed-point problem and require explicit blob-parity verification after the stable pass.
- Rollback: Give the mismatched manifest zero commit credit, retain it as an operational negative, and rewrite only the owner final review receipts.
- Witnesses: V6456-W20-F, V6456-W20-P, V6456-W20-F, V6456-W20-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
