#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Liora Venn v661-v4."""

from __future__ import annotations

from ghc_family_v661_v4_data import *  # noqa: F401,F403
import ghc_family_v661_v4_data as x1


X1_FREEZE = "177e00fee935b76290bbd8c4cea9edba13681800"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Liora x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6614-X2-N001",
        "signature": "combined-x1-commit-and-conditional-push-supervision-returned-no-exit-after-the-commit-finalized",
        "recovery": "Retain the supervision-output fault at zero credit, inspect the exact head, parent, subject, status, and live Git processes before issuing a separate bounded push; never repeat the successful x1 commit.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6614-X2-N002",
        "signature": "first-x1-four-way-equality-wrapper-compared-tab-formatted-divergence-to-a-space-formatted-literal",
        "recovery": "Retain the false wrapper exit at zero credit and split the divergence output on whitespace before requiring two numeric zeros alongside identical local, upstream, tracking, and fresh-live hashes and zero status rows.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6614-X2-N003",
        "signature": "first-x2-anchor-projection-guessed-a-nonexistent-source-phase-data-attribute",
        "recovery": "Retain the AttributeError at zero credit and inspect only declared module attributes, while using the builder's explicit immutable Orin source-phase path for selected-row replay.",
        "completion_credit": 0,
    },
]

X2_OPERATIONAL_FAILURES.extend(
    {
        "negative_id": f"V6614-X2-N{index:03d}",
        "signature": f"skill-creator-quick-validator-for-{skill_name}-could-not-import-yaml-under-the-default-python",
        "recovery": "Retain the dependency failure at zero credit, install nothing, and rerun the unchanged validator with a D-first bounded two-scalar frontmatter parser shim only after documenting its restricted YAML surface.",
        "completion_credit": 0,
    }
    for index, (skill_name, _purpose) in enumerate(SELF_SKILL_SPECS, 4)
)

X2_OPERATIONAL_FAILURES.extend(
    [
        {
            "negative_id": "V6614-X2-N014",
            "signature": "bundled-codex-primary-runtime-python-also-lacked-the-yaml-module",
            "recovery": "Retain the dependency probe at zero credit and do not modify the bundled runtime; use the same bounded external parser-shim recovery for the validator only.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6614-X2-N015",
            "signature": "windows-store-python-3-13-also-lacked-the-yaml-module",
            "recovery": "Retain the dependency probe at zero credit, install nothing, and stop probing system interpreters before using the bounded external parser-shim recovery.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6614-X2-N016",
            "signature": "post-x1-template-recreation-materialized-three-untracked-closeout-seeds-before-the-immutable-evidence-boundary",
            "recovery": "Retain the lifecycle fault at zero credit, remove only Liora's reproducible untracked closeout builder, final validator, and closeout test, exclude them from evidence staging, and recreate them from Orin's immutable source only after evidence is pushed clean and fresh-remote equal.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6614-X2-N017",
            "signature": "first-x2-content-manifest-reconciliation-probe-used-a-colon-adjacent-interpolated-powershell-variable-and-failed-to-parse",
            "recovery": "Retain the parser failure at zero credit; use the format operator for bounded diagnostic strings, then verify all manifest hashes, byte counts, coverage, protected x1 paths, and diff hygiene without changing the evidence set.",
            "completion_credit": 0,
        },
        {
            "negative_id": "V6614-X2-N018",
            "signature": "first-post-n017-x2-suite-run-found-the-derived-method-flow-validation-receipt-stale-at-sixty-three-methods",
            "recovery": "Retain the bounded suite failure at zero credit, keep the dynamic test unchanged, and rerun the installed Method Flow validator and summarizer against the regenerated append-only x2 ledger before repeating the scoped suite.",
            "completion_credit": 0,
        },
    ]
)
