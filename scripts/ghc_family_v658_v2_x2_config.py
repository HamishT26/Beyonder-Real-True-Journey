#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Sylven Arc v658-v2."""

from __future__ import annotations


SOURCE_COMMIT = "9009c83b898fe11c63a95e4e1153ad388f328d3f"
FIRST_X1_COMMIT = "2254b08806b48bd302a04b6cdba7908ad39514d5"
X1_COMMIT = FIRST_X1_COMMIT
PHASE_ROOT = "docs/sylven-arc/v658-v2"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16657
SOURCE_EFFECTIVE_NEGATIVES = 16658
X1_OPERATIONAL_NEGATIVES = 20
SOURCE_OPEN_GAPS = 113
SOURCE_EXACT_GATES = 112
SOURCE_METHODS = 2931
X1_METHODS = 21
MUTATIONS_PER_PROPOSAL = 5
EXPECTED_PROPOSALS = 30
EXPECTED_MUTATIONS = EXPECTED_PROPOSALS * MUTATIONS_PER_PROPOSAL
EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}


X2_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6582-X2-N01",
        "slug": "windows-rg-shell-glob-path-rejection",
        "failure_signature": "A read-only rg hygiene probe passed a wildcard inside a Windows path argument; rg rejected the invalid path before reading files.",
        "candidate_workaround": "Pass literal directories and use rg's explicit -g file-selection filter.",
        "recurrence_guard": "On Windows, keep search roots literal and express filename wildcards with the search tool's own glob option.",
        "fail_procedure": "Invoke rg with scripts/*v658_v2*.py as a path argument.",
        "fail_observed": "The filename or volume-label syntax was rejected; no repository or external state changed.",
        "pass_procedure": "Invoke rg on literal scripts and tests roots with -g *v658_v2*.py.",
        "pass_observed": "The bounded stale-token search completed with attributable output.",
        "scope_boundary": "Owner-local read-only hygiene recovery only; no completion, scientific, professional, route, or authority credit.",
    },
    {
        "negative_id": "V6582-X2-N02",
        "slug": "skill-quick-validate-default-cp1252-decode",
        "failure_signature": "The first x2 build initialized the first phase-local skill, but quick_validate.py used the Windows CP1252 default to read UTF-8 Māori text and raised UnicodeDecodeError before skill-validation credit.",
        "candidate_workaround": "Run the unchanged current validator in explicit Python UTF-8 mode and preserve the initialized owner-local directory.",
        "recurrence_guard": "Set PYTHONUTF8=1 and PYTHONIOENCODING=utf-8 for skill-creator initialization and validation subprocesses on Windows.",
        "fail_procedure": "Validate the UTF-8 skill under the inherited Windows default codec.",
        "fail_observed": "The validator stopped on a multibyte Māori character; the x2 build earned zero aggregate credit and no external state changed.",
        "pass_procedure": "Invoke quick_validate.py only for the affected skill with explicit Python UTF-8 mode.",
        "pass_observed": "The unchanged skill passed the current quick validator under explicit UTF-8.",
        "scope_boundary": "Owner-local encoding recovery and skill-schema validation only; no cultural, completion, scientific, route, or authority credit.",
    },
]
