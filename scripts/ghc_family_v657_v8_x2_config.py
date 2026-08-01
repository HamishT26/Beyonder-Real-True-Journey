#!/usr/bin/env python3
"""Immutable x2 lifecycle configuration for Tamar Vey v657-v8."""

from __future__ import annotations


SOURCE_COMMIT = "664460f294989f14c8ebcb1c157bdf67f9bf1052"
FIRST_X1_COMMIT = "a48c87af28aa55a8bb6aea056e4652906cdb575f"
X1_COMMIT = "a48c87af28aa55a8bb6aea056e4652906cdb575f"
PHASE_ROOT = "docs/tamar-vey/v657-v8"
SOURCE_SEALED_EFFECTIVE_NEGATIVES = 16313
SOURCE_EFFECTIVE_NEGATIVES = 16314
X1_OPERATIONAL_NEGATIVES = 21
SOURCE_OPEN_GAPS = 111
SOURCE_EXACT_GATES = 110
SOURCE_METHODS = 2588
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
        "negative_id": "V6578-X2-N01",
        "slug": "overbroad-predecessor-runtime-read-truncated-context",
        "failure_signature": (
            "An initial attempt to render the predecessor runtime and builder too broadly "
            "exceeded the useful model-context envelope and was truncated before it could "
            "support a safe domain adaptation."
        ),
        "candidate_workaround": (
            "Inspect declarations and bounded function windows, then copy only the reusable "
            "engine and replace phase-local domain surfaces explicitly."
        ),
        "recurrence_guard": (
            "Use declaration searches and bounded line windows for inherited lifecycle tools; "
            "never render an entire large builder merely to locate its active functions."
        ),
        "fail_procedure": "Request an overbroad combined runtime and builder rendering.",
        "fail_observed": (
            "The response was truncated and earned zero evidence credit; no repository byte "
            "or external state changed."
        ),
        "pass_procedure": (
            "Read the runtime and active builder regions in bounded windows and verify the "
            "selected reusable functions before any substantive edit."
        ),
        "pass_observed": (
            "The contract, mutation, skill, runner, evidence, Method Flow, and truth-building "
            "functions were identified without replaying Liora's aggregate."
        ),
        "scope_boundary": (
            "Owner-local read and recovery only; no scientific, production, route, authority, "
            "or independent-reproduction credit."
        ),
    },
    {
        "negative_id": "V6578-X2-N02",
        "slug": "combined-skill-domain-patch-assumed-mechanical-owner-token",
        "failure_signature": (
            "The first combined skill-domain patch assumed that the predecessor's short "
            "owner label had been changed by the earlier full-name replacement, so its exact "
            "context was absent and the patch was atomically rejected."
        ),
        "candidate_workaround": (
            "Reread the bounded skill-template region and patch the exact current short owner "
            "label together with the audiovisual domain text."
        ),
        "recurrence_guard": (
            "After a mechanical migration, inspect every substantive template region before "
            "constructing a combined semantic patch."
        ),
        "fail_procedure": "Patch a presumed Tamar short label without rereading the migrated template.",
        "fail_observed": "Apply-patch rejected the edit atomically; no repository byte changed and no credit was assigned.",
        "pass_procedure": "Read the exact template window and patch its current Liora short label explicitly.",
        "pass_observed": "The audiovisual skill and runner wording was installed against exact current context.",
        "scope_boundary": "Owner-local source-edit recovery only; no scientific, route, or authority credit.",
    },
    {
        "negative_id": "V6578-X2-N03",
        "slug": "console-mojibake-used-as-unicode-patch-context",
        "failure_signature": (
            "A second combined patch used a console-rendered mojibake spelling as context even "
            "though the UTF-8 source contained the correct Māori code point."
        ),
        "candidate_workaround": (
            "Use the correct Unicode source spelling in apply-patch and treat console mojibake "
            "as a display fault until exact bytes prove otherwise."
        ),
        "recurrence_guard": "Never infer a UTF-8 repository defect from legacy console rendering alone.",
        "fail_procedure": "Use shell-rendered mojibake as an exact source anchor.",
        "fail_observed": "Apply-patch found no matching line and changed nothing; zero credit was assigned.",
        "pass_procedure": "Patch the exact UTF-8 line containing U+0101 and re-read the resulting template.",
        "pass_observed": "The domain edit succeeded while preserving correct Māori spelling.",
        "scope_boundary": "Owner-local encoding diagnosis only; no cultural, authority, or completion credit.",
    },
    {
        "negative_id": "V6578-X2-N04",
        "slug": "package-style-phase-data-import-missed-scripts-path",
        "failure_signature": (
            "A scalar proposal-count probe imported the phase-data module through the scripts "
            "package while that module intentionally uses a sibling file-context import."
        ),
        "candidate_workaround": (
            "Invoke the phase script in its declared file context or add the repository scripts "
            "directory to sys.path explicitly for a read-only scalar probe."
        ),
        "recurrence_guard": (
            "Respect the import context declared by phase-local executable modules; do not "
            "assume package and script invocation are interchangeable."
        ),
        "fail_procedure": "Import scripts.ghc_family_v657_v8_phase_data from the repository root.",
        "fail_observed": "Python raised ModuleNotFoundError for the sibling catalogue; compilation itself had passed.",
        "pass_procedure": "Insert the exact scripts directory in sys.path and import the module by its executable name.",
        "pass_observed": "The bounded probe reports thirty proposals and the frozen 23/5/1/1 distribution.",
        "scope_boundary": "Owner-local import-context recovery only; no proposal or scientific credit.",
    },
    {
        "negative_id": "V6578-X2-N05",
        "slug": "obsolete-prose-limit-applied-to-frozen-machine-ledger",
        "failure_signature": (
            "The first detailed evidence validation applied a 6,000-word prose ceiling to the "
            "compact 2,650-row machine ledger and failed one of 327 checks at 38,748 words."
        ),
        "candidate_workaround": (
            "Honor the frozen phase-wide 100,000-word document ceiling recorded by x1 while "
            "keeping the human-facing integrated overview intentionally concise."
        ),
        "recurrence_guard": (
            "Read the phase's committed cap receipt before inheriting a historical prose-only "
            "threshold into machine-generated ledgers."
        ),
        "fail_procedure": "Validate every phase document against an assumed 6,000-word ceiling.",
        "fail_observed": "326 detailed checks passed and document_word_cap failed; the attempt received zero aggregate credit.",
        "pass_procedure": "Validate against the committed x1 limit_words value of 100000 and report the observed maximum.",
        "pass_observed": "The 38,748-word frozen proposal index remains within its declared phase ceiling.",
        "scope_boundary": "Document-policy recovery only; no scientific, production, route, or authority credit.",
    },
    {
        "negative_id": "V6578-X2-N06",
        "slug": "guessed-cap-path-and-windows-rg-wildcards",
        "failure_signature": (
            "A read-only cap lookup guessed a nonexistent path and passed PowerShell wildcard "
            "tokens directly to rg, which rejected the Windows path syntax."
        ),
        "candidate_workaround": "Enumerate exact phase paths with rg --files, then read the literal cap receipt.",
        "recurrence_guard": "Discover exact files before probing them and avoid shell-specific wildcard assumptions in rg path arguments.",
        "fail_procedure": "Probe guessed cap filenames and wildcard paths in one rg invocation.",
        "fail_observed": "The command returned path and filename syntax errors and earned zero read credit.",
        "pass_procedure": "Filter rg --files output for cap and validation names, then use Get-Content -LiteralPath.",
        "pass_observed": "The committed x1 receipt was read and confirmed limit_words 100000 with maximum_words 38748.",
        "scope_boundary": "Read-only path-discovery recovery only; no repository or completion credit.",
    },
]
