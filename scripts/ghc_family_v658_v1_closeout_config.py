#!/usr/bin/env python3
"""Immutable closeout configuration for Elowen Cairn v658-v1."""

from __future__ import annotations


SOURCE_COMMIT = "15857de0afd21f7432196bf71b2f53ab2f5504c9"
FIRST_X1_COMMIT = "6f42b9dc6fca6ffed17438030ce8c36bc2535846"
X1_COMMIT = FIRST_X1_COMMIT
EVIDENCE_COMMIT = "dc89caf2989c9be4d62a64c59756fc167bf5c52a"
PHASE_ROOT = "docs/elowen-cairn/v658-v1"
BRANCH = "codex/GHC-Family/elowen-cairn-v658-v1-full-tools"
EVIDENCE_EFFECTIVE_NEGATIVES = 16655
EVIDENCE_EFFECTIVE_METHODS = 2929
OPEN_GAPS = 113
EXACT_GATES = 112


CLOSEOUT_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6581-CLOSEOUT-N01",
        "slug": "short-commit-prefix-expanded-by-assumption",
        "failure_signature": (
            "The first closeout configuration expanded the displayed short evidence prefix "
            "into an invented full hash before the exact commit object was reread."
        ),
        "candidate_workaround": (
            "Read the immutable evidence head with git rev-parse and bind the configuration "
            "only to that exact forty-character object name."
        ),
        "recurrence_guard": (
            "Never infer or synthesize the undisplayed suffix of a commit identifier; resolve "
            "every lifecycle anchor directly from Git before execution."
        ),
        "fail_procedure": "Populate an immutable lifecycle constant by guessing beyond a short commit prefix.",
        "fail_observed": "The owner-local uncommitted configuration briefly contained the wrong hash and was never executed.",
        "pass_procedure": "Run git rev-parse HEAD and patch the exact observed evidence commit into the configuration.",
        "pass_observed": "The closeout configuration now names the exact immutable evidence commit.",
        "scope_boundary": "Owner-local pre-execution anchor recovery only; no evidence, route, or completion credit.",
    },
    {
        "negative_id": "V6581-CLOSEOUT-N02",
        "slug": "powershell-double-quoted-rg-pattern-reinterpreted",
        "failure_signature": (
            "A combined rg stale-token probe placed escaped double quotes inside a "
            "PowerShell double-quoted argument; PowerShell ended the argument early and "
            "attempted to load part of the pattern as a module."
        ),
        "candidate_workaround": (
            "Pass the regular expression as one PowerShell single-quoted literal and keep "
            "path arguments outside that literal."
        ),
        "recurrence_guard": (
            "For PowerShell rg probes containing quote characters, use a single-quoted "
            "pattern or a literal pattern file rather than backslash-escaping double quotes."
        ),
        "fail_procedure": "Embed backslash-escaped quote fragments in a PowerShell double-quoted rg pattern.",
        "fail_observed": "PowerShell rejected the read-only probe before rg ran; no file was changed.",
        "pass_procedure": "Repeat the stale-token audit with a single-quoted literal pattern.",
        "pass_observed": "The bounded literal-pattern probe completed and returned only genuine matches.",
        "scope_boundary": "Owner-local read-only shell quoting recovery only; no artifact or completion credit.",
    },
]
