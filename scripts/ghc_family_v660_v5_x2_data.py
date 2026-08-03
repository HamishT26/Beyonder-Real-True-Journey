#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Vesper Arlen v660-v5."""

from __future__ import annotations

from ghc_family_v660_v5_data import *  # noqa: F401,F403
import ghc_family_v660_v5_data as x1


X1_FREEZE = "38ed87786c89c77b9b78b5ad520828ba8a02982e"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6605-X2-N001",
        "signature": "mechanical-x2-scaffold-retained-source-phase-anchors-owner-credit-labels-ice-core-vocabulary-and-four-prefilled-operational-failures",
        "recovery": "Retain the scaffold audit at zero credit, bind the exact Vesper x1 SHA, clear every inherited failure prefill, rewrite current-owner and meteorite contracts, delay final-only scaffold files until after the immutable evidence commit, and compile-review every generated x2 runtime, builder, and test before execution.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N002",
        "signature": "first-owner-x2-suite-passed-eighteen-of-nineteen-and-found-the-family-current-method-workflow-reflection-and-meta-tool-receipt-group-unmaterialized",
        "recovery": "Retain the 18-pass and one missing-path error at zero credit, invoke only the declared family-current Method Flow, workflow refinement, reflection-remaster, and Meta Tool Box builders, refresh the x2 packet, and rerun the isolated owner suite.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N003",
        "signature": "source-derived-x2-test-hardcoded-a-nine-scoped-four-issue-reflection-cardinality-that-the-current-skill-did-not-produce",
        "recovery": "Retain the stale cardinality assumption at zero credit and assert current structural inventory and issue invariants without copying another owner's incidental totals.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N004",
        "signature": "source-derived-x2-test-hardcoded-forty-five-meta-tool-collisions-while-the-new-meteorite-names-produced-nine",
        "recovery": "Retain the stale collision total at zero credit and require twenty valid cards, a nonnegative reported finding count, and no automatic selection instead of manufacturing source-domain collisions.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N005",
        "signature": "first-evidence-staging-wrapper-truncated-its-large-line-ending-advisory-stream-after-requesting-all-one-hundred-eighty-intended-paths",
        "recovery": "Retain the truncated display at zero credit, refresh only affected negative and manifest artifacts, restage the exact allowlist with advisory output suppressed, and derive credit solely from the exact Git index.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N006",
        "signature": "post-staging-refresh-derived-changed-paths-only-from-unstaged-and-untracked-state-and-collapsed-the-evidence-allowlist-from-one-hundred-eighty-to-nine",
        "recovery": "Retain the collapsed candidate at zero credit, restore only the Git index to the unstaged working state, rebuild from the complete owner delta, and require the recovered 180-path allowlist and 176-entry manifest before restaging.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N007",
        "signature": "exact-index-restore-wrapper-output-exceeded-context-before-attributable-completion-state",
        "recovery": "Retain the truncated restore wrapper at zero credit, inspect the Git index through a bounded scalar count, accept recovery only after the index proves empty, and rebuild the candidate from the still-present working-tree delta.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N008",
        "signature": "bounded-candidate-count-probe-imported-the-x2-module-without-placing-the-repository-scripts-directory-on-python-path",
        "recovery": "Retain the ModuleNotFoundError at zero credit, avoid importing phase code for receipt counting, inspect the generated JSON artifacts directly, and reserve module imports for invocations with an explicit scripts path.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6605-X2-N009",
        "signature": "exact-staged-metric-probe-guessed-a-nonexistent-x2-stale-label-review-filename-after-successfully-parsing-the-staged-json-blobs",
        "recovery": "Retain the FileNotFoundError and the incomplete probe at zero credit, resolve validation receipt names from the exact generated directory listing, and keep staged JSON parsing separate from optional receipt inspection.",
        "recovery_passed": True,
    },
]
