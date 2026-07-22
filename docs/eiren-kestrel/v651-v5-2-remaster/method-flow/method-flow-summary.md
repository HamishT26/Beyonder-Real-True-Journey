# GHC Family Method Flow State

- Phase: v651-v5-2-remaster
- Owner: Eiren Kestrel
- Methods: 18
- Passing witnesses: 19
- Failed witnesses retained: 24

## Preferred methods

### V6515R-M01 — Bound inherited-checkout verification

- Trigger: A newly materialized inherited worktree requires source, branch, and clean-diff verification.
- Method: Verify branch and head directly, then use bounded staged and unstaged index-diff checks without repeating the full status scan.
- Recurrence guard: Avoid full status enumeration as the first check on a newly materialized 46000-plus-file checkout.
- Rollback: Retain the timeout at zero credit and stop if branch, head, or either diff domain is not attributable.
- Witnesses: V6515R-M01-WFAIL, V6515R-M01-WPASS

### V6515R-M02 — Quote Git revision peel expressions in PowerShell

- Trigger: PowerShell passes a Git revision containing caret and brace syntax.
- Method: Wrap the complete revision peel expression in single quotes before passing it to git rev-parse.
- Recurrence guard: Quote every revision expression containing caret, braces, colon, or shell-significant punctuation.
- Rollback: Retain the fatal probe and use the already attributable plain head only if the peeled form cannot be verified.
- Witnesses: V6515R-M02-WFAIL, V6515R-M02-WPASS, V6515R-M02-WFAIL-TERMINAL, V6515R-M02-WPASS-TERMINAL

### V6515R-M03 — Derive proposal outcome totals from frozen specifications

- Trigger: A proposal table and declared aggregate are authored separately.
- Method: Count expected dispositions directly from the frozen proposal table and fail before writing if the declared aggregate differs.
- Recurrence guard: Never change proposal evidence labels to satisfy a preferred distribution; derive the distribution from proposal truth.
- Rollback: Retain the failed generator attempt and write no packet until the aggregate matches the frozen table.
- Witnesses: V6515R-M03-WFAIL, V6515R-M03-WPASS

### V6515R-M04 — Separate live policy overrides from legacy workflow-runner route validation

- Trigger: A newer live request expands policy caps beyond the installed workflow runner's encoded values.
- Method: Preserve the authoritative live request and failed audit, then validate only immediate route structure through a marked compatibility projection that carries the live overrides explicitly.
- Recurrence guard: Never present a compatibility projection as validation of the newer policy values.
- Rollback: Retain the failed audit and stop route execution if the immediate ownership projection also fails.
- Witnesses: V6515R-M04-WFAIL, V6515R-M04-WPASS

### V6515R-M05 — Respect Method Flow witness auto-promotion

- Trigger: The Method Flow runner records a passing witness for a candidate method.
- Method: Read the state returned by the witness command and transition directly from validated to preferred only once.
- Recurrence guard: Do not hard-code a second validated transition after a passing witness.
- Rollback: Retain the rejected transition and resume from the ledger's actual valid state without rebuilding the ledger.
- Witnesses: V6515R-M05-WFAIL, V6515R-M05-WPASS, V6515R-M05-WFAIL-REPEAT-01, V6515R-M05-WFAIL-REPEAT-02, V6515R-M05-WFAIL-REPEAT-03

### V6515R-M06 — Declare UTF-8 for Windows skill validation

- Trigger: A Python validator reads UTF-8 GHC skill text on Windows.
- Method: Set PYTHONUTF8=1 for the skill validator on Windows before reading UTF-8 skill documents.
- Recurrence guard: Declare UTF-8 for Python subprocesses that read skill packages on Windows; do not strip or transliterate valid text to satisfy a legacy codec.
- Rollback: Retain the failed validation at zero credit and stop if explicit UTF-8 still cannot read the package.
- Witnesses: V6515R-M06-WFAIL, V6515R-M06-WPASS

### V6515R-M07 — Keep a uniform explicit Boundaries section in every skill

- Trigger: Generated and hand-authored skills share one structural contract.
- Method: Give every skill package an explicit Boundaries heading even when equivalent constraints already appear under a specialized heading.
- Recurrence guard: Validate shared structural headings across both generated and hand-authored packages before the aggregate.
- Rollback: Retain the failed aggregate and remove only the additive heading if it introduces a contradiction.
- Witnesses: V6515R-M07-WFAIL, V6515R-M07-WPASS

### V6515R-M08 — Bind closeout builders to the current Method Flow summary schema

- Trigger: A closeout builder reads a generated Method Flow summary.
- Method: Inspect the current Method Flow summary keys and consume preferred_methods with its published field names.
- Recurrence guard: Inspect generated JSON keys and one representative row before binding a closeout builder to the summary schema.
- Rollback: Retain the failed builder attempt at zero credit and remove any partial closeout output before retrying; no partial files were written in this instance.
- Witnesses: V6515R-M08-WFAIL, V6515R-M08-WPASS

### V6515R-M09 — Repeat Reflection-Remaster focus arguments

- Trigger: The reflection runner accepts --focus with argparse append semantics.
- Method: Pass each reflection focus term with its own --focus argument because the runner uses an append action.
- Recurrence guard: Inspect argparse action and confirm scoped_count is nonzero before crediting a focused reflection run.
- Rollback: Retain the zero-scoped output at zero credit and overwrite only the additive reflection output with a correctly focused run.
- Witnesses: V6515R-M09-WFAIL, V6515R-M09-WPASS

### V6515R-M10 — Use literal-path Select-String for quote-sensitive PowerShell probes

- Trigger: A short PowerShell source probe contains nested quote characters.
- Method: Use Select-String with literal paths and separately quoted patterns when inspecting PowerShell source text.
- Recurrence guard: Prefer literal-path PowerShell cmdlets for short source probes containing nested quote syntax.
- Rollback: Retain the parser error at zero credit and issue no mutation before a quote-safe read succeeds.
- Witnesses: V6515R-M10-WFAIL, V6515R-M10-WPASS

### V6515R-M11 — Preserve Windows paths through raw wrapper literals

- Trigger: A JavaScript wrapper sends a Windows path containing backslashes to PowerShell or the shell workdir field.
- Method: Use raw JavaScript template literals or explicitly doubled backslashes for every Windows command and workdir path passed through an orchestration wrapper.
- Recurrence guard: Construct Windows command and workdir strings with String.raw before dispatch and verify the resolved D-first directory read-only.
- Rollback: Retain each wrapper rejection at zero credit and leave the staged index untouched until a raw-path probe succeeds.
- Witnesses: V6515R-M11-WFAIL-01, V6515R-M11-WFAIL-02, V6515R-M11-WPASS

### V6515R-M12 — Bind Git probes to the resolved owned worktree

- Trigger: A Git command depends on repository discovery and the current wrapper directory may be outside the repository.
- Method: Run repository-scoped Git probes from the resolved owned worktree, not from the configuration directory.
- Recurrence guard: Resolve the owned worktree first, then bind every repository-scoped Git probe to that workdir.
- Rollback: Retain the failed read at zero credit and perform no mutation before a worktree-bound Git probe passes.
- Witnesses: V6515R-M12-WFAIL, V6515R-M12-WPASS

### V6515R-M13 — Discover the Method Flow command surface before invocation

- Trigger: A caller has not verified the current Method Flow runner subcommand names.
- Method: Read the runner's top-level help first and invoke only its accepted record, witness, set-state, validate, and summarize surfaces.
- Recurrence guard: Capture the accepted command list from top-level help before requesting subcommand help.
- Rollback: Retain each parser refusal at zero credit and do not edit the ledger directly.
- Witnesses: V6515R-M13-WFAIL-01, V6515R-M13-WFAIL-02, V6515R-M13-WPASS

### V6515R-M14 — Use ripgrep glob filters for Windows filename selection

- Trigger: A Windows ripgrep scan must select filename families across fixed repository directories.
- Method: Pass fixed directories to ripgrep and express filename selection with one or more -g filters on Windows.
- Recurrence guard: Use positional directory roots plus ripgrep glob filters instead of wildcard positional paths.
- Rollback: Retain the refused scan at zero credit and do not infer absence until the corrected directory-scoped scan passes.
- Witnesses: V6515R-M14-WFAIL, V6515R-M14-WPASS

### V6515R-M15 — Honor staged-manifest self-exclusion before generation

- Trigger: A staged-review generator declares its own output receipts as index self-exclusions.
- Method: Before generating self-excluding staged manifests, remove only the declared receipt paths from the index and assert their staged intersection is empty.
- Recurrence guard: Stage intended inputs, unstage only declared self-excluding outputs, assert zero staged intersections, then generate and restage the receipts.
- Rollback: Retain the refused generator at zero credit and leave working-tree receipt content available until the exact index contract is restored.
- Witnesses: V6515R-M15-WFAIL, V6515R-M15-WPASS

### V6515R-M16 — Resolve final-review documents from declared path constants

- Trigger: A final-review script adds a new repository-relative artifact read.
- Method: Resolve phase artifacts as REPO / PHASE_ROOT / relative_path inside the final-review script.
- Recurrence guard: Reuse only path constants declared by the script and exercise new path expressions in an isolated read before the generator.
- Rollback: Retain the NameError at zero credit and do not stage any incomplete receipt output.
- Witnesses: V6515R-M16-WFAIL, V6515R-M16-WPASS

### V6515R-M17 — Avoid quote-dense inline Python for Windows path witnesses

- Trigger: A read-only Windows witness would require nested path strings inside an inline Python argument.
- Method: Use LiteralPath PowerShell reads for simple Windows word-count witnesses instead of quote-dense inline Python.
- Recurrence guard: Prefer a checked-in script or LiteralPath cmdlets whenever an inline program contains nested path-string quoting.
- Rollback: Retain the inline-program failure at zero credit and do not infer file readability from the failed expression.
- Witnesses: V6515R-M17-WFAIL, V6515R-M17-WPASS

### V6515R-M18 — Bind correction review to exact attributable parent heads

- Trigger: An additive terminal correction follows a clean pushed closeout commit.
- Method: Permit staged-review generation only at the exact evidence head or the exact known closeout correction parent, and reject every other head.
- Recurrence guard: Bind correction-capable lifecycle tools to an explicit finite set of attributable parent heads rather than relaxing exact-head checks generally.
- Rollback: Retain the refused correction review at zero credit and stop if the current head is neither the evidence head nor the known closeout parent.
- Witnesses: V6515R-M18-WFAIL, V6515R-M18-WPASS

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
