#!/usr/bin/env python3
"""Immutable-x1-aware x2 truth overlay for Orin Thale v661-v3."""

from __future__ import annotations

from ghc_family_v661_v3_data import *  # noqa: F401,F403
import ghc_family_v661_v3_data as x1


X1_FREEZE = "e7529a4bc2ddb4c095fc6a1ebbd6933f8d2faa8f"
ACTIVATION_AFTER_X1_NEGATIVES = x1.ACTIVATION_NEGATIVES + len(x1.STARTUP_FAILURES)
ACTIVATION_AFTER_X1_METHODS = x1.ACTIVATION_METHODS + len(x1.STARTUP_FAILURES)

# Append only failures actually observed after the immutable Orin x1 freeze.
# Expected rejecting mutations belong to the mutation register, not here.
X2_OPERATIONAL_FAILURES: list[dict[str, object]] = [
    {
        "negative_id": "V6613-X2-N001",
        "signature": "combined-x1-commit-push-and-equality-wrapper-returned-no-attributable-payload",
        "recovery": "Retain the empty wrapper at zero credit, infer no gate from it, and prove commit identity, upstream, tracking, divergence, cleanliness, and fresh live remote equality with separate no-profile probes.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6613-X2-N002",
        "signature": "login-profile-combined-git-audit-returned-no-attributable-output",
        "recovery": "Retain the second empty wrapper at zero credit and use explicit no-profile scalar Git commands whose bounded outputs identify the exact x1 commit and four-way equality.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6613-X2-N003",
        "signature": "first-read-only-evidence-tree-template-projection-used-an-empty-foreach-pipe",
        "recovery": "Retain the PowerShell parser fault at zero credit, materialize the result array, and confirm the inherited closeout code was absent from the immutable evidence commit before preserving the same lifecycle split.",
        "completion_credit": 0,
    },
    {
        "negative_id": "V6613-X2-N004",
        "signature": "first-x2-builder-wrapper-returned-no-attributable-console-payload",
        "recovery": "Retain the silent wrapper at zero credit, do not rerun the completed builder, and validate its declared output set, process absence, exact counts, and scoped tests directly.",
        "completion_credit": 0,
    }
]

X2_OPERATIONAL_FAILURES.extend(
    {
        "negative_id": f"V6613-X2-N{index:03d}",
        "signature": f"phase-local-skill-{skill_name}-first-quick-validation-used-default-cp1252-and-rejected-utf8-boundary-text",
        "recovery": "Retain the UnicodeDecodeError at zero credit, pin PYTHONUTF8=1 for the same official quick validator, and require a bounded passing result without changing the skill package.",
        "completion_credit": 0,
    }
    for index, (skill_name, _purpose) in enumerate(SELF_SKILL_SPECS, 5)
)

X2_OPERATIONAL_FAILURES.extend(
    {
        "negative_id": f"V6613-X2-N{index:03d}",
        "signature": f"phase-local-skill-{skill_name}-utf8-quick-validation-rejected-indented-frontmatter-description-key",
        "recovery": "Retain the invalid-YAML witness at zero credit, remove only the erroneous frontmatter indentation in the generator and existing package, and rerun the same UTF-8 quick validator.",
        "completion_credit": 0,
    }
    for index, (skill_name, _purpose) in enumerate(SELF_SKILL_SPECS, 15)
)

X2_OPERATIONAL_FAILURES.append(
    {
        "negative_id": "V6613-X2-N025",
        "signature": "first-current-domain-stale-label-scan-passed-a-literal-windows-wildcard-path-to-ripgrep",
        "recovery": "Retain the invalid-path diagnostic at zero credit, enumerate exact current-owner files first, and scan the materialized literal path set while keeping inherited zero-credit source labels visible.",
        "completion_credit": 0,
    }
)

X2_OPERATIONAL_FAILURES.append(
    {
        "negative_id": "V6613-X2-N027",
        "signature": "first-179-entry-git-index-manifest-replay-returned-no-attributable-console-result",
        "recovery": "Retain the silent replay at zero credit, write the same bounded comparison to an external D-first validation receipt, and reread the receipt explicitly before awarding parity.",
        "completion_credit": 0,
    }
)

X2_OPERATIONAL_FAILURES.append(
    {
        "negative_id": "V6613-X2-N026",
        "signature": "first-x2-evidence-stage-refused-ten-owner-runner-paths-outside-the-worktree-sparse-definition",
        "recovery": "Retain the partial stage at zero credit and rerun Git add with explicit --sparse against the same literal owner allowlist without changing sparse patterns or any sibling surface.",
        "completion_credit": 0,
    }
)
