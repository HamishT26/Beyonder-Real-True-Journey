# GHC Family Method Flow State

- Phase: v646-gmut-thos-v8-x1-x2
- Owner: Ilyra Fen
- Methods: 13
- Passing witnesses: 12
- Failed witnesses retained: 13

## Preferred methods

### V6468-M01 — Follow the exact reference path declared by the selected skill

- Trigger: a selected skill names a required reference; a similarly named path is tempting
- Method: Read the selected SKILL.md completely and resolve its literal relative reference before opening the schema.
- Recurrence guard: Never infer a reference filename when SKILL.md declares one.
- Rollback: Give the failed read zero instruction credit and make no task mutation.
- Witnesses: V6468-M01-F, V6468-M01-P

### V6468-M02 — Collect PowerShell loop output before formatting or piping

- Trigger: a loop emits objects; the result will be formatted or piped
- Method: Assign the loop output to a variable, then pipe that variable.
- Recurrence guard: Evaluate compound PowerShell producers before formatting consumers.
- Rollback: Give the parser-failed wrapper zero diagnostic credit.
- Witnesses: V6468-M02-F, V6468-M02-P

### V6468-M04 — Use Git-index path evidence for exact skill-name collision preflight

- Trigger: candidate names map to package paths; the worktree content surface is large
- Method: Enumerate tracked Git paths once and compare candidate names against the returned path set.
- Recurrence guard: Use path evidence for package-name collisions; reserve content search for a bounded explicit file set.
- Rollback: Give the timed-out content scan zero absence credit and leave the candidate list unfrozen until the path witness passes.
- Witnesses: V6468-M04-F, V6468-M04-P

### V6468-M05 — Invoke PowerShell command shims through PowerShell

- Trigger: a command resolves to a PowerShell script shim; a Python subprocess probe needs only version text
- Method: Invoke the shim through a no-profile PowerShell command and capture only its sanitized version line.
- Recurrence guard: Resolve the command type before selecting a subprocess invocation method.
- Rollback: Give the failed builder zero packet credit and make no permission or installation change.
- Witnesses: V6468-M05-F, V6468-M05-P

### V6468-M06 — Require diff-hygiene success after staged-review fixed point

- Trigger: staged review and manifest are byte-stable; diff hygiene has not yet passed
- Method: Retain the failed staged state, normalize only the reported EOF, restage, and rerun the unchanged staged and diff gates.
- Recurrence guard: A stable manifest is necessary but never substitutes for diff hygiene.
- Rollback: Do not commit the stable but hygiene-invalid staged tree.
- Witnesses: V6468-M06-F, V6468-M06-P

### V6468-M07 — Pin UTF-8 before phase-local skill initialization

- Trigger: skill metadata may contain non-ASCII text; the inherited console codec is not guaranteed UTF-8
- Method: Set PYTHONUTF8 and PYTHONIOENCODING before process start, then initialize only missing phase-local packages.
- Recurrence guard: Pin UTF-8 before invoking skill-creator tools that may emit or persist non-ASCII text; never delete culturally correct wording to satisfy a legacy codec.
- Rollback: Give the partial initialization zero portfolio completion credit, keep it phase-local, and complete only missing files after the encoding guard is active.
- Witnesses: V6468-M07-F, V6468-M07-P

### V6468-M08 — Explicitly close SQLite handles before Windows fixture teardown

- Trigger: a disposable SQLite fixture uses multiple source or destination connections; the host enforces open-file deletion locks
- Method: Close every SQLite connection explicitly before deleting the verified disposable fixture root, then rerun the unchanged confinement tribunal.
- Recurrence guard: Do not treat sqlite3 connection context managers as handle-closure guards; explicitly close every source and destination connection before Windows fixture teardown.
- Rollback: Give the failed all-proposal run zero integrated-run credit, wait for process exit, verify the leftover root is a child of the declared disposable bank, and remove only that root.
- Witnesses: V6468-M08-F, V6468-M08-P

### V6468-M09 — Adjudicate scanner candidates and retain scoped-test diagnostics

- Trigger: a five-class scan reports a lexical candidate; a compact test receipt reports a failure without a diagnostic tail
- Method: Separate lexical scanner candidates from confirmed payload hits with exact semantic dispositions, and preserve a bounded sanitized failing-test tail before rerunning the unchanged scoped gates.
- Recurrence guard: A regex match is a candidate, not a confirmed payload; record an exact disposition and retain enough sanitized test output to diagnose every scoped failure.
- Rollback: Give the failed 25-check validation zero pass credit, preserve its receipt, and do not weaken or delete any scanner class or test.
- Witnesses: V6468-M09-F, V6468-M09-P

### V6468-M10 — Derive staged runner scope from the frozen exact allowlist

- Trigger: x1 freezes family-current runner filenames; a staged scope predicate relies on a phase-version prefix
- Method: Bind staged-script scope to the exact ten frozen runner filenames plus the version-prefixed phase scripts, rather than assuming every family-current runner carries the phase version.
- Recurrence guard: Generate the exact staged runner allowlist from the frozen x1 runner ledger; do not infer scope from a filename prefix alone.
- Rollback: Give the failed staged review zero commit credit, retain its result, and leave every staged path intact until the corrected exact predicate passes.
- Witnesses: V6468-M10-F, V6468-M10-P

### V6468-M11 — Synchronize semantic candidate disposition and persisted review status

- Trigger: the same semantic field appears in generated evidence and its source definition; a staged review writer persists richer status than its console return
- Method: Apply the existing exact semantic accessibility-field disposition to both its generated artifact and source definition, and make receipt-writing return the persisted review result rather than structural status alone.
- Recurrence guard: Adjudicate an exact semantic token consistently across generated artifacts and source definitions, and bind command success to the persisted review result.
- Rollback: Give both the misleading writer status and failed fixed-point check zero commit credit; retain all candidates and do not remove or weaken a scanner class.
- Witnesses: V6468-M11-F, V6468-M11-P

### V6468-M12 — Classify exact Method Flow scanner-incident mirrors

- Trigger: an append-only Method Flow record documents an exact scanner match; the same incident appears in the ledger mirror
- Method: Keep exact incident descriptions intact and classify only the named Method Flow incident record and its ledger mirror as retained-scanner-incident candidates while leaving unmatched paths unresolved.
- Recurrence guard: When a scanner incident must quote the matched token, disposition only the exact retained incident files and class; never introduce a broad path or content exemption.
- Rollback: Give the failed broader validation zero pass credit, preserve both incident candidates, and do not delete diagnostic text or weaken the callable-pattern scanner.
- Witnesses: V6468-M12-F, V6468-M12-P

### V6468-M13 — Preserve Git porcelain columns before path slicing

- Trigger: Git porcelain leading columns carry machine meaning; a shared command helper trims output
- Method: Read Git porcelain output without global trimming, preserve both status columns, and slice the path only after each raw line has been retained.
- Recurrence guard: Never pass machine-column output through a helper that globally strips leading whitespace; parse raw lines first.
- Rollback: Give the stopped closeout builder zero lifecycle credit, retain the already-passed safe portfolio result, and write no closeout artifact until raw parsing passes.
- Witnesses: V6468-M13-F, V6468-M13-P

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
