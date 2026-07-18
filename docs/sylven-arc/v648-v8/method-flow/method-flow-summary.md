# GHC Family Method Flow State

- Phase: v648-v8
- Owner: Sylven Arc
- Methods: 13
- Passing witnesses: 13
- Failed witnesses retained: 13

## Preferred methods

### v6488-m01 — Commit-manifest byte-domain discriminator

- Trigger: A commit-local manifest declares checkout_bytes_domain separately from git_blob identity.; Later commits may have changed files that were present in an earlier staged manifest.
- Method: Validate changed-path parity and Git object identity at the named commit, then use the retained staged-review receipt for checkout-domain byte parity instead of equating checkout bytes with raw blob size.
- Recurrence guard: Read hash_domain and checkout_bytes_domain before comparing sizes; never infer that the two byte domains are identical.
- Rollback: Discard the false mismatch conclusion and retain the failed probe as an operational negative.
- Witnesses: v6488-m01-wfail-01, v6488-m01-wpass-01

### v6488-m02 — Scanner-definition candidate discriminator

- Trigger: A scanner source file is included in the exact staged-file domain.; The source contains the literal patterns it is designed to detect.
- Method: Retain every raw candidate, inspect the matching source line, and classify only pattern-definition lines in the scanner itself as scanner-definition candidates rather than confirmed artifact leaks.
- Recurrence guard: Report candidate and confirmed-hit counts separately; never discard scanner self-matches without exact line-context classification.
- Rollback: Restore fail-closed classification if a candidate is outside an exact scanner-definition line.
- Witnesses: v6488-m02-wfail-01, v6488-m02-wpass-01

### v6488-m03 — Generated-JSON narrow patch recovery

- Trigger: A generated JSON artifact uses deterministic sorted keys.; The proposed patch context was inferred rather than read from the current file.
- Method: Read the exact bounded current snippet, patch source-of-truth code first, then patch or regenerate the artifact with minimal exact context.
- Recurrence guard: Inspect generated key order before patching and avoid broad multi-file contexts that depend on inferred serialization order.
- Rollback: No rollback is needed when apply_patch reports zero changes; retain the failed patch witness.
- Witnesses: v6488-m03-wfail-01, v6488-m03-wpass-01

### v6488-m04 — Lifecycle-stable x1 assertion

- Trigger: The same test module remains in the repository after x2 begins.; The test checks current path absence rather than immutable x1 truth and commit-local review evidence.
- Method: Assert the frozen x1 phase-truth flags and x1 staged-review x2 path count, which remain valid after later additive lifecycle files exist.
- Recurrence guard: Historical lifecycle tests must read frozen receipts, never infer prior state from the current later worktree.
- Rollback: Restore the exact x1 test from its commit if the receipt-based assertion no longer matches the frozen evidence.
- Witnesses: v6488-m04-wfail-01, v6488-m04-wpass-01

### v6488-m05 — Multi-file patch hunk grammar guard

- Trigger: One patch updates several files.; A hunk boundary is followed immediately by another file header without valid context.
- Method: Use one syntactically complete update hunk per file and validate each file header boundary before submitting the patch.
- Recurrence guard: Do not leave a bare hunk marker before the next file header; prefer smaller multi-file patches when contexts differ.
- Rollback: No rollback is required because patch parsing failed before mutation.
- Witnesses: v6488-m05-wfail-01, v6488-m05-wpass-01

### v6488-m06 — PowerShell live-remote line parser

- Trigger: git ls-remote output is embedded directly in a parenthesized split expression.; PowerShell collection and operator precedence is not made explicit.
- Method: Capture exactly one ls-remote output line first, then split that scalar line on whitespace and require a forty-hex-character hash.
- Recurrence guard: Validate live hash length and hexadecimal form before comparing it with local, upstream, and tracking heads.
- Rollback: Discard the malformed one-character value and make no remote-equality claim from it.
- Witnesses: v6488-m06-wfail-01, v6488-m06-wpass-01

### v6488-m07 — Bounded Git status decomposition

- Trigger: A large Windows worktree is queried with several Git and recursive filesystem operations in one wrapper.; The wrapper timeout is shorter than the combined cold-path latency.
- Method: Split the probe into narrow Git commands and count staged and unstaged paths without recursive directory enumeration.
- Recurrence guard: Use one bounded purpose per status probe and never treat a timeout as clean-state evidence.
- Rollback: Retain the timeout as an operational negative and make no state claim from it.
- Witnesses: v6488-m07-wfail-01, v6488-m07-wpass-01

### v6488-m08 — Method Flow flat-layout locator

- Trigger: A prior phase layout is inferred without reading the current phase file list.; Several guessed paths are read in one wrapper.
- Method: List the exact current method-flow directory first and read the discovered flat filenames literally.
- Recurrence guard: Discover current ledger-adjacent paths before reading method and witness records.
- Rollback: Retain the path errors and make no content claim from missing files.
- Witnesses: v6488-m08-wfail-01, v6488-m08-wpass-01

### v6488-m09 — Method Flow validate-option guard

- Trigger: Several Method Flow subcommands are composed in one wrapper.; Different subcommands expose similar but nonidentical output option names.
- Method: Read subcommand help and call validate with --receipt while reserving --json-output for summarize.
- Recurrence guard: Resolve each Method Flow subcommand schema independently before composing lifecycle wrappers.
- Rollback: Do not duplicate the already-recorded methods or witnesses; resume from ledger state and regenerate validation and summary receipts.
- Witnesses: v6488-m09-wfail-01, v6488-m09-wpass-01

### v6488-m10 — Phase source-ledger path discovery

- Trigger: A generated packet groups ledgers into subdirectories.; A path is inferred from its artifact name rather than discovered from the current tree.
- Method: Use a narrow file-name search within the owned phase before reading the discovered literal path.
- Recurrence guard: Discover generated artifact paths before composing multi-file reads.
- Rollback: Retain the missing-path error and make no source-ledger claim from it.
- Witnesses: v6488-m10-wfail-01, v6488-m10-wpass-01

### v6488-m11 — Search no-match exit discriminator

- Trigger: A read-only search is used to locate implementation details.; No-match is possible and the wrapper treats every nonzero exit as a tooling fault.
- Method: Read the exact known file when its path is already available, or explicitly distinguish no-match from execution error.
- Recurrence guard: Use a no-match-aware wrapper for discovery searches and never infer file absence from an overcompressed pattern.
- Rollback: Retain the failed search and make no content claim from it.
- Witnesses: v6488-m11-wfail-01, v6488-m11-wpass-01

### v6488-m12 — Unittest discovery root-path guard

- Trigger: A script under scripts loads repository test modules by dotted name.; Only the script directory is present on the interpreter module path.
- Method: Add the repository root to the builder module path before loading test names and reject implausibly small selected counts.
- Recurrence guard: Inspect loaded identifiers and require the authorized selection to exceed the known inherited floor before staging.
- Rollback: Discard the nine-placeholder count, retain the candidate artifacts as superseded preflight output, and regenerate before canonical use.
- Witnesses: v6488-m12-wfail-01, v6488-m12-wpass-01

### v6488-m13 — Index-tree revision materializer

- Trigger: A checker accepts a revision and the intended domain is the current Git index.; Index stage syntax is confused with a tree object accepted by ls-tree.
- Method: Materialize the exact index with git write-tree and pass the resulting tree object to the revision checker.
- Recurrence guard: Use stage syntax only for individual index paths; use an exact write-tree object for index-wide tree operations.
- Rollback: Retain the failed check, make no manifest-parity claim from it, and leave the staged index unchanged.
- Witnesses: v6488-m13-wfail-01, v6488-m13-wpass-01

## Retained boundary

This ledger records bounded workflow evidence. Same-owner validation is not independent reproduction and does not establish scientific, legal, cultural, identity, production, security, accessibility, deployment, or Stage 20 claims.
