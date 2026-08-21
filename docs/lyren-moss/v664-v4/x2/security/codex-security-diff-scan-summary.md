# Lyren Moss v664-v4 bounded security-diff summary

## Result

The solo bounded diff review completed against the immutable pre-fix x2 working-tree snapshot rooted at `a11d57463d86a37876a06e5ea3cc04ac37cd7e99`. It reviewed all three changed executable Python sources and retained one high-confidence, medium-severity grouped finding: the pre-fix output writers could follow or race filesystem links at predictable artifact leaves and redirect a write outside the declared Lyren phase.

An isolated Windows temporary-directory proof established the direct flashcard path without mutating repository or external user data. A dangling output-leaf symlink was followed and thirteen bytes were created at the proof's outside target. The evidence builder separately contained a check-then-write race established by source trace. Fixed owner-local names, same-user access, non-elevated execution, and the absence of a remote service constrain likelihood and impact; they do not erase the finding.

## Additive remediation

The owner delta changed after the immutable scan snapshot to reject symlink leaves, use exclusive no-follow creation where supported, and write repeatable artifacts through an exclusively created same-directory temporary file followed by atomic replacement. The isolated regression `FlashcardRemasterTests.test_dangling_output_symlink_is_rejected_without_escape` passed and confirmed that the outside target remained absent.

The completed report intentionally retains the pre-fix finding. The additive remediation does not rewrite the snapshot, erase `LM6644-X2-NEG104`, or claim exhaustive filesystem security. Parent-directory reparse-point behavior and every possible Windows race remain outside this bounded proof.

## Coverage and boundaries

The evidence builder and family flashcard runner were reported through the grouped finding. The fixed-registry archival-audio engine produced no reportable source finding under checks for schema smuggling, dynamic execution, subprocesses, network access, filesystem writes, and false evidence promotion. Generated evidence artifacts, tests, and unchanged repository files were not executable production-source review surfaces.

This is same-owner structural validation. It is not a penetration test, an external audit, exhaustive-security assurance, privacy completeness, accessibility completeness, professional preservation authority, independent reproduction, or Stage 20 evidence. No successor was contacted during this scan.

The exact external report and canonical JSON remain outside the repository; their sanitized SHA-256 values, sizes, measured token usage, and the retained finding summary are recorded in `codex-security-diff-scan-receipt.json` without a private scan identifier or temporary path.
