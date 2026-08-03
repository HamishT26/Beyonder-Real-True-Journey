#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Elaren Kestrel v660-v3."""

from __future__ import annotations

from ghc_family_v660_v3_data import *  # noqa: F401,F403
import ghc_family_v660_v3_data as x1


X1_FREEZE = "759c285c49ed95175437f0dd08aff403cfb38618"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Only failures observed after the x1 freeze belong here. Expected rejecting
# mutations are recorded in the mutation register and Method Flow witnesses,
# not prefilled as tooling faults.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6603-X2-N001",
        "signature": "first-post-x1-fresh-fetch-wrapper-used-an-undelimited-powershell-branch-variable-in-a-refspec",
        "recovery": "Retain the invalid refspec at zero credit, delimit the branch variable explicitly, and rerun only the fresh-fetch and four-way-equality dependency before x2 mutation.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N002",
        "signature": "advanced-tree-test-run-applied-an-x1-only-absence-assertion-to-the-x2-working-tree",
        "recovery": "Retain the failed advanced-tree assertion at zero credit, keep the frozen x1 test byte-stable, verify the absence contract directly from the immutable x1 Git tree, and exclude only that lifecycle-only assertion from advanced-tree test loading.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N003",
        "signature": "first-x2-privacy-pass-classified-prohibition-and-scanner-definition-language-as-private-payload",
        "recovery": "Retain the two false-positive file findings at zero credit, adjudicate only the exact scanner and closeout-validator definition files as definition vocabulary, and rerun the same five concrete payload classes without weakening payload detection.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N004",
        "signature": "first-x2-test-enrichment-patch-used-a-nonmatching-context-line-and-was-rejected-atomically",
        "recovery": "Retain the rejected patch at zero credit, reread the bounded test window, and apply the same additive immutable-x1 recovery assertion against exact surrounding lines.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N005",
        "signature": "first-advanced-tree-x1-selection-command-lost-python-string-quoting-under-powershell-and-raised-nameerror-before-test-loading",
        "recovery": "Retain the pre-load quoting failure at zero credit, enumerate the frozen x1 test methods mechanically, and invoke every advanced-tree-safe method by exact unittest name while the lifecycle-only absence contract remains bound to the immutable x1 tree.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N006",
        "signature": "first-x2-workflow-validation-targeted-the-normalized-x1-subdirectory-without-the-required-raw-audit-domain",
        "recovery": "Retain the missing-input validation failure at zero credit, build one new x2-scoped workflow packet from the frozen sanitized request, and validate that complete packet without changing the x1 workflow artifacts.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N007",
        "signature": "first-x2-meta-tool-box-build-resolved-a-relative-phase-root-against-the-skill-directory-and-produced-a-zero-card-catalogue",
        "recovery": "Retain the zero-card catalogue at zero credit, rebuild the x2 catalogue with the absolute phase root while requiring repository-relative card paths, then validate and collision-review the corrected catalogue.",
        "recovery_passed": True,
    },
    {
        "negative_id": "V6603-X2-N008",
        "signature": "second-x2-workflow-validator-expected-a-composite-raw-and-normalized-packet-layout-not-emitted-by-the-current-one-pass-refinement-runner",
        "recovery": "Retain the incompatible-layout validation attempt at zero credit, use the refinement runner's own valid 20-of-20 policy receipt for the exact sanitized request, and do not fabricate absent composite audit domains or claim the separate validator passed.",
        "recovery_passed": True,
    },
]
