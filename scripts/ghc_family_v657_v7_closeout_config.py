#!/usr/bin/env python3
"""Immutable closeout configuration for Liora Venn v657-v7."""

from __future__ import annotations


SOURCE_COMMIT = "b7f207d4c354dfd2671cd0562a058ac69f83fe35"
FIRST_X1_COMMIT = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
X1_COMMIT = "9219708f5a8d16f7faee010f9c7f219f804b59a2"
EVIDENCE_COMMIT = "f10ab507209ce652c645718545054ae237b87962"
PHASE_ROOT = "docs/liora-venn/v657-v7"
BRANCH = "codex/GHC-Family/liora-venn-v657-v7-full-tools"
EVIDENCE_EFFECTIVE_NEGATIVES = 16310
EVIDENCE_EFFECTIVE_METHODS = 2585
OPEN_GAPS = 111
EXACT_GATES = 110


CLOSEOUT_OPERATIONAL_NEGATIVES: list[dict[str, str]] = [
    {
        "negative_id": "V6577-CLOSEOUT-N01",
        "slug": "overbroad-closeout-builder-range-read-exceeded-output-context",
        "failure_signature": (
            "An overbroad range read of the closeout builder exceeded the useful "
            "tool and model output window, so its truncated output earned no review credit."
        ),
        "candidate_workaround": (
            "Use targeted ripgrep anchors and bounded line windows no larger than the "
            "specific function or contract under review."
        ),
        "recurrence_guard": (
            "Estimate output scope before each read and split long generated-source "
            "inspection into named, bounded sections."
        ),
        "scope_boundary": (
            "The failed read did not mutate the repository, validate closeout content, "
            "contact a route target, or earn canonical-pass credit."
        ),
        "fail_procedure": (
            "Request a broad multi-hundred-line closeout-builder range in one tool call."
        ),
        "fail_observed": (
            "The response was truncated beyond the useful inspection boundary and was "
            "therefore retained as a zero-credit failed witness."
        ),
        "pass_procedure": (
            "Locate precise anchors with ripgrep, then inspect only bounded nearby lines."
        ),
        "pass_observed": (
            "The targeted windows exposed the ancestry, baton, route, count, and lifecycle "
            "contracts without another output overflow."
        ),
    },
    {
        "negative_id": "V6577-CLOSEOUT-N02",
        "slug": "combined-stale-token-regex-used-an-invalid-powershell-escape",
        "failure_signature": (
            "A combined ripgrep expression crossed PowerShell and regex escaping domains, "
            "producing an unrecognized escape sequence before any audit result existed."
        ),
        "candidate_workaround": (
            "Run bounded fixed-string searches with explicit -F patterns, then use a small "
            "separate valid regular expression only where structural matching is required."
        ),
        "recurrence_guard": (
            "Do not combine JSON quoting, shell quoting, and regex escapes in one Windows "
            "audit expression without first proving the literal form."
        ),
        "scope_boundary": (
            "The parser fault did not inspect content, change any file, contact Tamar, or "
            "earn stale-label or canonical validation credit."
        ),
        "fail_procedure": (
            "Pass one large mixed literal-and-regex expression through PowerShell to ripgrep."
        ),
        "fail_observed": (
            "Ripgrep rejected an unrecognized escape sequence and produced no content audit."
        ),
        "pass_procedure": (
            "Use separate fixed-string searches for each stale token and inspect any hits "
            "with bounded exact context."
        ),
        "pass_observed": (
            "The replacement literal searches completed without parser ambiguity and exposed "
            "only evidence-bounded text or no stale content."
        ),
    },
    {
        "negative_id": "V6577-CLOSEOUT-N03",
        "slug": "combined-cleanliness-probe-lost-inner-session-attribution",
        "failure_signature": (
            "A combined Git status, diff, and untracked-file probe exceeded the default "
            "yield window while its caller emitted only stdout, losing the returned inner "
            "session identifier and therefore all completion credit."
        ),
        "candidate_workaround": (
            "Emit the full execution result, use a thirty-second yield, and split status, "
            "diff, and untracked-file checks into bounded calls."
        ),
        "recurrence_guard": (
            "Never discard session_id when a command can exceed the default window; inspect "
            "the structured execution result before leaving the tool isolate."
        ),
        "scope_boundary": (
            "The lost probe was read-only. A bounded audit found no index lock, the exact "
            "immutable evidence HEAD, and no remaining Git process before staging resumed."
        ),
        "fail_procedure": (
            "Run several potentially slow Git cleanliness commands together and print only "
            "the initial stdout field."
        ),
        "fail_observed": (
            "The call returned no attributable completion output and the inner session could "
            "not be resumed from the next isolate."
        ),
        "pass_procedure": (
            "Audit processes, index lock, HEAD, and Git directory separately, then rerun each "
            "cleanliness surface with its structured result and sufficient yield."
        ),
        "pass_observed": (
            "No index lock remained, the worktree stayed at the immutable evidence commit, "
            "and the bounded replacement probes retained their completion attribution."
        ),
    },
]
