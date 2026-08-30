# Sylven Arc v678-v6 correction2 static-audit correction

Correction1 `79c42c6158c9799344e16a9ed5fc49092422b698` remains immutable. A non-canonical static audit replayed the evidence, first-final, and correction1 manifests successfully and confirmed all file and word caps. It then failed closed for two independent reasons: the validator had not yet listed the x1 and correction1 manifest scripts as scanner-definition sources, and the flashcard builder used `__import__("collections")` solely to access `Counter`.

No canonical aggregate, receipt, or latch was invoked or created. Correction2 adds exact-file scanner adjudication for the manifest implementations and replaces dynamic import with `from collections import Counter`. Payload matches remain failures, and `eval`, `exec`, and `__import__` remain forbidden call sites in owner code. The validator now binds correction1 to its immutable tree and gives correction2 its own delta, corrected-owner, and content-seal layer.

A later read-only ripgrep inspection expression was rejected as an unclosed group before inspecting any file. The bounded recovery supplied each search pattern separately and succeeded without changing repository content. Both the failed method and its recovery remain explicit in Method Flow.

The first correction2 manifest build also failed closed because its seal expected `canonical-preflight-state.json` while the builder emitted `precanonical-state.json`. The producer now emits the exact seal-target name, and only that failed manifest-build dependency is rerun.

The next isolated manifest build failed closed on a second filename mismatch: the seal targeted a nonexistent receipt-contract document rather than the generated `static-audit-correction.md`. The seal now binds the actual static-audit evidence file.

The first correction2 test aggregate then completed 6/8. Its two stale assertions expected the earlier counts and the superseded `precanonical-state.json` filename. The aggregate remains zero-credit; only those two failed methods are rerun after the exact expectations are corrected.

The first correction2 INDEX verifier then crossed its display window while still running, and its stdout-only wrapper discarded the live session handle. The process was allowed to finish, but no status was inferred. A corrected wrapper retains session metadata and captures one complete rerun against the changed final staged target.

A subsequent regeneration attempt failed closed because the earlier correction delta remained staged. Only the Sylven-owned correction2 paths were unstaged, preserving every worktree byte. The count-only test run immediately after the rejected builder also failed against the correctly unchanged generated file; after regeneration, only that failed assertion is rerun.

The corrected final must be the direct child of correction1. Source to corrected final must contain exactly five direct single-parent Sylven commits and zero merges. The route remains `PREPARED_NOT_SENT`; scientific, empirical, participant, professional, legal, cultural, affected-party, Māori-authority, privacy-complete, accessibility-complete, independent-reproduction, consciousness, personhood, Theory-of-Everything, proof, canon, and Stage 20 gates remain unchanged.
