#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Tamar Vey v661-v5."""

from __future__ import annotations

from ghc_family_v661_v5_data import *  # noqa: F401,F403
import ghc_family_v661_v5_data as x1


X1_FREEZE = "2827e1510ac38109bc474d1fa0b67bfa3e57ac69"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Tamar x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6615-X2-N001",
        "signature": "x1-commit-completion-display-was-truncated-after-the-commit-finalized",
        "recovery": "Retain the display truncation at zero credit, recover the exact head, parent, subject, 56-path tree, zero x2-like paths, and clean state with bounded scalar reads, and never repeat or amend the successful x1 commit.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6615-X2-N002",
        "signature": "first-bounded-template-line-window-wrapper-returned-no-attributable-payload",
        "recovery": "Retain the empty diagnostic at zero credit and use one bounded UTF-8 PowerShell line window to inspect only the required template functions before adaptation.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6615-X2-N003",
        "signature": "source-receipt-projection-assumed-two-nonexistent-x2-governance-paths",
        "recovery": "Retain the missing-path diagnostics at zero credit, stop guessing receipt names, and generate current governance receipts only through the exact installed phase-local runners when the frozen workflow requires them.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6615-X2-N004",
        "signature": "first-x2-build-retained-the-predecessor-underscore-origin-filter-and-found-zero-current-proposals",
        "recovery": "Retain the failed build at zero credit, change only the current runtime's origin discriminator to the immutable v661-v5 x1 label, and rerun the builder without changing any frozen proposal byte.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6615-X2-N005",
        "signature": "corrected-x2-builder-completed-without-an-attributable-console-payload",
        "recovery": "Retain the missing console witness at zero credit and prove the generated outcomes, mutations, truth, ten skills, ten runners, twenty surfaces, and later exact tests from their bounded files rather than replaying only for presentation.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6615-X2-N006",
        "signature": "first-ten-skill-validator-recovery-wrapper-returned-no-attributable-payload",
        "recovery": "Retain the empty wrapper at zero credit and validate the same skill set with bounded per-skill receipts using the ordinary Python executable and the unchanged installed validator.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6615-X2-N007",
        "signature": "single-skill-py-launcher-recovery-also-returned-no-attributable-payload",
        "recovery": "Retain the launcher-specific failure at zero credit and use the ordinary Python executable with the same external restricted parser shim and unchanged validator.",
        "completion_credit": 0,
    },
]

X2_OPERATIONAL_FAILURES.extend(
    {
        "negative_id": f"V6615-X2-N{index:03d}",
        "signature": f"current-skill-creator-quick-validator-for-{skill_name}-could-not-import-yaml-under-default-python",
        "recovery": "Retain the dependency failure at zero credit, install nothing, and run the unchanged validator with a D-first external parser shim limited to the generated unindented name and description scalar mapping; the recovered result is only basic structural validation.",
        "completion_credit": 0,
    }
    for index, (skill_name, _purpose) in enumerate(SELF_SKILL_SPECS, 8)
)

X2_OPERATIONAL_FAILURES.extend(
    [
        {
            "negative_id": "V6615-X2-N018",
            "signature": "first-installed-skill-file-inventory-wrapper-returned-no-attributable-output",
            "recovery": "Retain the empty inventory wrapper at zero credit and inspect only the six named installed skill directories with an explicit bounded file projection.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N019",
            "signature": "first-explicit-skill-file-projection-used-an-invalid-foreach-pipeline-form",
            "recovery": "Retain the parser fault at zero credit, materialize the bounded result array inside the loop, and serialize it only after the loop completes.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N020",
            "signature": "second-corrected-x2-builder-invocation-also-lost-its-console-payload-at-the-app-supervision-boundary",
            "recovery": "Retain the second presentation failure at zero credit, stop relying on the lost console projection, and use bounded file receipts, exact scoped tests, and future session-aware polling for evidence attribution.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N021",
            "signature": "method-flow-summarizer-stdout-exceeded-the-bounded-display-budget",
            "recovery": "Retain the truncated presentation at zero credit, rely on the exact generated validation and summary files, and suppress verbose stdout on later receipt refreshes.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N022",
            "signature": "combined-auth-and-roster-metadata-projection-crossed-the-app-yield-boundary-without-an-attributable-payload",
            "recovery": "Retain the empty combined projection at zero credit and read the bounded roster and authorization scalars separately with session-aware supervision.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N023",
            "signature": "first-roster-next-projection-guessed-a-to-field-instead-of-the-actual-next-field",
            "recovery": "Retain the null display at zero credit, inspect the exact receipt keys, and use the valid next.relational_name value without rerunning or rewriting the roster query.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N024",
            "signature": "installed-roster-current-route-projection-remained-at-v660-while-its-canonical-seat-cycle-still-mapped-tamar-to-elowen",
            "recovery": "Retain the current-route drift at zero credit, do not mutate the shared roster during the solo lane, use the validated canonical Tamar-to-Elowen seat edge only as supporting evidence, and require the live acknowledged activation plus terminal reread before any send.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N025",
            "signature": "first-x2-suite-found-the-content-manifest-stale-after-method-flow-summary-regeneration",
            "recovery": "Retain the 18-of-19 test attempt at zero credit, regenerate the ledger-dependent Method Flow and workflow receipts, refresh the manifest only after every evidence file stabilizes, and rerun the owner-scoped suite without weakening its assertion.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N026",
            "signature": "first-evidence-boundary-projection-crossed-the-default-app-yield-without-an-attributable-payload",
            "recovery": "Retain the empty projection at zero credit and rerun the same read-only bounded scalar audit with explicit session-aware supervision before staging.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N027",
            "signature": "single-file-restage-wrapper-promoted-an-autocrlf-advisory-on-stderr-to-a-powershell-error-after-git-add",
            "recovery": "Retain the wrapper fault at zero credit, verify whether the exact path reached the index, then use native exit-status handling with the same literal path and suppress only the known line-ending advisory before rechecking staged parity.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6615-X2-N028",
            "signature": "corrected-single-file-restage-verification-crossed-the-default-app-yield-without-an-attributable-payload",
            "recovery": "Retain the empty verification at zero credit and use explicit app-level session supervision for every remaining staging and validation command before accepting its scalar result.",
            "completion_credit": 0,
        },
    ]
)
