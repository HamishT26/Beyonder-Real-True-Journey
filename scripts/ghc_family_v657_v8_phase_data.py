#!/usr/bin/env python3
"""Phase constants for Tamar Vey's v657-v8 x1/x2 bundle."""

from __future__ import annotations

from ghc_family_v657_v8_phase_catalogue import (
    CANDIDATE_TASKS,
    CLEAN_TASKS,
    OFFICIAL_SOURCES,
    PROPOSALS,
    PROTECTED_GATES,
    RUNNER_SPECS,
    SAFE_TASKS,
    SKILL_SPECS,
    X1_OPERATIONAL_NEGATIVES,
)


PHASE = "v657-v8"
PHASE_CODE = "V6578"
OWNER = "Tamar Vey"
PRONOUNS = "she/they"
ROLE = "relational evidence-and-recovery steward"
HOPE = (
    "keep every claim, handoff, and failure inspectable, corrigible, and safely "
    "retractable without converting synthetic structure into authority"
)
BRANCH = "codex/GHC-Family/tamar-vey-v657-v8-full-tools"
PHASE_ROOT = "docs/tamar-vey/v657-v8"

SOURCE_OWNER = "Liora Venn"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v657-v7-full-tools"
SOURCE_X1 = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
SOURCE_EVIDENCE = "f10ab507209ce652c645718545054ae237b87962"
SOURCE_CLOSEOUT = "664460f294989f14c8ebcb1c157bdf67f9bf1052"
SOURCE_FINAL = "664460f294989f14c8ebcb1c157bdf67f9bf1052"
SOURCE_ORIGINAL_FINAL = SOURCE_FINAL
SOURCE_CANONICAL_RECEIPT_SHA256 = (
    "f54671b32980fd48e829ae7b81fafdea8c7f9ddd4048d1e6d766824c960cdec2"
)
SOURCE_BATON_SHA256 = (
    "a41c7bc02fbc934c4ea0dd7c61f747d58aa99ff2604299b0d452be069e80083b"
)
SOURCE_BATON_CHECKOUT_SHA256 = (
    "c3e3f40be2844740a2c2b805d3e73264e271f6e13452f9409859cab91a50a1ec"
)

PRIOR_FROZEN = 2620
SOURCE_CLOSEOUT_EFFECTIVE_NEGATIVES = 16313
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16313
SOURCE_EFFECTIVE_NEGATIVES = 16314
SOURCE_POSTFINAL_ROUTE_NEGATIVE = {
    "slug": "V6577-POST-N01",
    "count": 1,
    "credit": 0,
    "repository_retained": False,
    "signatures": ["overbroad-recursive-tamar-history-render-truncated"],
    "recovery": (
        "A bounded five-turn user/final extraction recovered the exact route evidence. "
        "The failure changed no repository or task state and remains external to "
        "Liora's sealed 16,313 count."
    ),
}
SOURCE_OPEN_GAPS = 111
SOURCE_EXACT_GATES = 110
SOURCE_METHODS = 2588
SOURCE_FAILED_WITNESSES = 2588
SOURCE_PASSING_WITNESSES = 2588

PRIMARY_FOCUS = (
    "Freed ID and CBR Heart through typed audiovisual custody, preservation provenance, "
    "rights-expression refusal, synthetic credential lifecycle, privacy, correction, "
    "accessibility, affected-party legitimacy, and Māori-authority reservation, with "
    "GMUT Mind and THOS Body explicit and protected"
)
BOUNDED_PRACTICE = (
    "audiovisual-preservation transfer and magnetic-tape digitization quality-control, "
    "carrier and package custody, signal-chain configuration, synthetic signal envelopes, "
    "metadata, fixity, derivative separation, correction, accessibility, workload, readback, "
    "and shift handover used only as a synthetic software, formal, structural, and learning "
    "lens; no real person, recording, carrier, playback machine, converter, archive, signal, "
    "measurement, transfer, preservation action, rights decision, professional competence, "
    "employment, legal interpretation, cultural ratification, Māori authority, affected-party "
    "approval, or real-world outcome"
)

CODEX_CLI_VERSION = "codex-cli 0.146.0"
CODEX_DESKTOP_VERSION = "26.727.6591.0"
CHATGPT_DESKTOP_VERSION = "1.2026.190.0"
GIT_VERSION = "git version 2.55.0.windows.2"
PYTHON_VERSION = "Python 3.12.10"
NODE_VERSION = "v24.18.0"

EXPECTED_DISTRIBUTION = {
    "completed": 23,
    "represented": 5,
    "open_gap": 1,
    "exact_gate": 1,
}
ALLOWED_OUTCOMES = set(EXPECTED_DISTRIBUTION)
