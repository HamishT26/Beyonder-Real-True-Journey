#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Eiren Kestrel v660-v2."""

from __future__ import annotations

from ghc_family_v660_v2_data import *  # noqa: F401,F403
import ghc_family_v660_v2_data as x1


X1_FREEZE = "ba1589880e23fe0c5c615c4cd1e7d5f47c5fe96b"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6602-X2-N001",
        "signature": "combined-post-x1-push-four-way-equality-wrapper-returned-no-attributable-output",
        "recovery": "Retain the empty wrapper at zero credit and prove upstream, tracking, fresh-live remote, divergence, and cleanliness with separate scalar reads before beginning x2.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N002",
        "signature": "x2-template-inspection-guessed-a-nonexistent-v660-v1-surface-runtime-filename",
        "recovery": "Retain the missing-path failure at zero credit, inspect the immutable builder import and bounded script inventory, and use the exact ghc_family_v660_v1_runtime.py template.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N003",
        "signature": "combined-x2-status-and-template-field-inspection-returned-no-attributable-output",
        "recovery": "Retain the empty combined inspection at zero credit and inspect repository status, exact template paths, and source fields in separate bounded reads.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N004",
        "signature": "scalar-porcelain-status-with-branch-header-returned-no-attributable-output",
        "recovery": "Retain the empty status read at zero credit and use independent scalar HEAD, path, index, untracked, and diff probes rather than interpreting silence as cleanliness.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N005",
        "signature": "first-substantive-builder-patch-used-powershell-mojibake-display-text-and-failed-context-verification",
        "recovery": "Retain the rejected patch at zero credit, reread the exact file as UTF-8, and apply only a patch whose context matches the verified Unicode text.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N006",
        "signature": "first-x2-reflection-remaster-used-one-comma-joined-focus-and-scoped-zero-surfaces",
        "recovery": "Retain the zero-scope reflection packet at zero credit and rerun only the reflection dependency with separate repeatable --focus arguments for v660_v2 and stained-glass surfaces.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N007",
        "signature": "quote-heavy-combined-method-flow-example-search-was-misparsed-as-an-invalid-regex",
        "recovery": "Retain the regex parse failure at zero credit and use separate fixed-string searches for reflection and candidate-state examples.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N008",
        "signature": "targeted-tooling-assertion-guessed-scoped-surface-count-instead-of-the-declared-scoped-count-key",
        "recovery": "Retain the KeyError at zero credit, inspect the exact reflection inventory keys, and rerun only the tooling predicates with scoped_count.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N009",
        "signature": "first-x2-allowlist-classifier-required-stained-glass-in-runner-names-and-false-flagged-the-declared-gmut-pane-came-runner",
        "recovery": "Retain the false-positive allowlist result at zero credit and derive the exact ten runner paths from the immutable x1 SELF_RUNNER_SPECS list.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N010",
        "signature": "follow-up-combined-nonphase-status-projection-returned-no-attributable-output",
        "recovery": "Retain the empty projection at zero credit and compare status paths directly against phase-root, base-code, and frozen runner-spec allowlists.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6602-X2-N011",
        "signature": "exact-frozen-runner-aware-status-allowlist-wrapper-returned-no-attributable-output",
        "recovery": "Retain the empty wrapper at zero credit and stage only the explicit phase root, four x2 base-code files, and ten exact runner names from the already verified frozen specification.",
        "recovery_passed": True,
    },
]
