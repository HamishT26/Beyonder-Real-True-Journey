#!/usr/bin/env python3
"""Build the additive dependency correction after the v679-v4 preflight failure."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from ghc_family_lyren_moss_v679_v4_core import read_json, write_json


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "lyren-moss" / "v679-v4"
FINAL = PHASE / "final"
CORRECTION = PHASE / "correction1"
VALIDATION = PHASE / "validation"
SOURCE = "e1c3ef6d2ff0bc2f1e38f5d702e008149842659f"
X1_HEAD = "1fe28fafc308298e1043a9e2afbecf59c24c9866"
EVIDENCE_HEAD = "b204dcbfbcb3d016ab18f4bebc5ef9dc56d9dee6"
INITIAL_FINAL = "20923e75fe7490f43ed585ee97dca596b9ca7adc"
BRANCH = "codex/GHC-Family/lyren-moss-v679-v4-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8").strip()


def normalized_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")).hexdigest()


def build() -> dict:
    if git("rev-parse", "HEAD") != INITIAL_FINAL:
        raise RuntimeError("correction builder must run from the retained initial final")
    original = read_json(FINAL / "terminal-truth.json")
    corrected = dict(original)
    corrected.update(
        {
            "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-terminal-overlay.v1",
            "retained_initial_final": INITIAL_FINAL,
            "correction_parent": INITIAL_FINAL,
            "exact_corrected_final_head": "RESOLVED_ONLY_AFTER_CORRECTION_COMMIT",
            "lifecycle_state": "PREPARED_FOR_DEPENDENCY_CORRECTED_FINAL_COMMIT",
            "canonical_state": "PENDING_ONE_EXACT_CORRECTED_FINAL_INVOCATION",
            "canonical_successes": 0,
            "canonical_replays": 0,
            "route_state": "PREPARED_NOT_SENT",
            "successor_send_count": 0,
        }
    )
    for key in ("operational_failures_retained", "effective_negatives", "method_flow_methods", "failed_witnesses", "bounded_passing_witnesses"):
        corrected[key] += 2
    CORRECTION.mkdir(parents=True, exist_ok=True)
    write_json(CORRECTION / "terminal-overlay.json", corrected)
    write_json(
        CORRECTION / "preflight-failure.json",
        {
            "event_id": "LM6794-OP-036",
            "classification": "FAILED_NONCANONICAL_PREFLIGHT_ZERO_CANONICAL_CREDIT",
            "retained_initial_final": INITIAL_FINAL,
            "failure": "The exact-final dependency preflight stopped before the canonical latch because the inherited x1 manifest uses sha256_normalized_lf and bytes fields while the canonical replay expected sha256 and normalized_lf_bytes.",
            "recovery": "Add a field-alias normalizer, bind it in one direct-child correction, replay the immutable original final seal at the retained initial final, and invoke the canonical validator only on the corrected exact head.",
            "canonical_invocations": 0,
            "canonical_success_credit": 0,
            "canonical_latch_created": False,
            "failure_retained": True,
            "recovery_erases_failure": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        CORRECTION / "correction-test-failure.json",
        {
            "event_id": "LM6794-OP-037",
            "classification": "FAILED_CORRECTION_SCOPED_TEST_ZERO_CANONICAL_CREDIT",
            "failure": "The first correction-only test invocation expected at least nine correction JSON files before this retained test-failure receipt existed; the exact set contained eight.",
            "recovery": "Materialize this retained failure receipt, preserve the eight previously passing tests, and rerun only the corrected correction-test dependency set.",
            "initial_result": {"passed": 8, "failed": 1, "reported_subtests_passed": 5},
            "canonical_invocations": 0,
            "canonical_success_credit": 0,
            "failure_retained": True,
            "recovery_erases_failure": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20"
        },
    )
    write_json(
        CORRECTION / "lifecycle.json",
        {
            "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-lifecycle.v1",
            "branch": BRANCH,
            "source_head": SOURCE,
            "x1_head": X1_HEAD,
            "evidence_head": EVIDENCE_HEAD,
            "retained_initial_final": INITIAL_FINAL,
            "prospective_corrected_final_parent": INITIAL_FINAL,
            "source_to_corrected_final_commit_target": 4,
            "merge_target": 0,
            "commit_ceiling": 8,
            "strict_planning_only_x1_before_x2": True,
            "initial_final_remains_ancestral_and_immutable": True,
        },
    )
    route = read_json(FINAL / "route-and-roster-overlay.json")
    route = dict(route)
    route.update(
        {
            "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-route-overlay.v1",
            "retained_initial_final": INITIAL_FINAL,
            "corrected_final_required": True,
            "route_state": "PREPARED_NOT_SENT",
            "precontact": False,
            "send_count": 0,
        }
    )
    write_json(CORRECTION / "route-overlay.json", route)

    original_baton = (FINAL / "handoffs" / "ilyra-fen-v679-v5-activation-candidate.md").read_text(encoding="utf-8")
    corrected_baton = original_baton.replace(
        "# ILYRA FEN — LYREN MOSS v679-v4 PREPARED EXACT-FINAL → SOLO v679-v5 ACTIVATION CANDIDATE",
        "# ILYRA FEN — LYREN MOSS v679-v4 DEPENDENCY-CORRECTED EXACT-FINAL → SOLO v679-v5 ACTIVATION CANDIDATE",
    )
    corrected_baton = corrected_baton.replace(
        "- Exact Lyren final: supplied only by the later live activation after the direct-child commit, push, fresh-live equality proof, and one successful exact-head canonical invocation",
        f"- Retained noncanonical initial final: `{INITIAL_FINAL}`\n- Dependency-corrected exact Lyren final: supplied only by the later live activation after the direct-child correction commit, push, fresh-live equality proof, and one successful exact-head canonical invocation",
    )
    corrected_baton = corrected_baton.replace(
        "The intended source-to-final lifecycle contains exactly three new direct single-parent Lyren commits and zero merges: x1 is the direct child of Vesper's source, evidence is the direct child of x1, and final is the direct child of evidence.",
        "The dependency-corrected source-to-final lifecycle contains exactly four new direct single-parent Lyren commits and zero merges: x1 is the direct child of Vesper's source, evidence is the direct child of x1, the retained initial final is the direct child of evidence, and the corrected final is the direct child of that retained initial final.",
    )
    corrected_baton = corrected_baton.replace("49127 effective negatives", "49129 effective negatives")
    corrected_baton = corrected_baton.replace("50441 Method Flow methods", "50443 Method Flow methods")
    corrected_baton = corrected_baton.replace("20788 retained failed witnesses", "20790 retained failed witnesses")
    corrected_baton = corrected_baton.replace("32781 bounded passing witnesses", "32783 bounded passing witnesses")
    corrected_baton = corrected_baton.replace("All 35 operational failures", "All 37 operational failures")
    correction_section = f"""

## Dependency-correction boundary

The retained initial final `{INITIAL_FINAL}` was clean, pushed, 0/0 divergent, and four-way equal, but its noncanonical dependency preflight failed before creating any canonical receipt latch. The x1 manifest used the historical fields `sha256_normalized_lf` and `bytes`; the canonical replay expected the family-current aliases `sha256` and `normalized_lf_bytes`. This schema-alias mismatch is retained as `LM6794-OP-036`, earns zero canonical-success or broader credit, and remains visible in `docs/lyren-moss/v679-v4/correction1/preflight-failure.json`.

The direct-child correction changes only the manifest field normalizer and additive correction evidence. It does not rewrite x1, x2 evidence, or the retained initial final. The original final manifest and content seal must be replayed at `{INITIAL_FINAL}`; the correction manifest and correction seal must be replayed at the later corrected exact final. One canonical invocation remains available because the failed preflight created no latch and ran no selected tests. Do not relabel the preflight as a canonical failure or success, and do not replay the canonical aggregate after its first success.

The first correction-only test invocation later found one bounded portfolio-shape dependency: the test expected at least nine correction JSON files before the retained correction-test-failure receipt itself existed. It completed eight tests and five subtests successfully, failed that one floor, and earned zero aggregate-success or canonical credit. `LM6794-OP-037` materializes the missing retained-failure record; only the corrected correction-test dependency set may be rerun before the final canonical invocation.
"""
    marker = "\n## Your solo Ilyra v679-v5 lane\n"
    corrected_baton = corrected_baton.replace(marker, correction_section + marker)
    handoff = CORRECTION / "handoffs" / "ilyra-fen-v679-v5-dependency-corrected-activation-candidate.md"
    handoff.parent.mkdir(parents=True, exist_ok=True)
    handoff.write_text(corrected_baton, encoding="utf-8", newline="\n")
    metadata = {
        "schema": "ghc-family.lyren-moss.v679-v4.dependency-corrected-activation-metadata.v1",
        "path": handoff.relative_to(ROOT).as_posix(),
        "normalized_lf_sha256": normalized_sha(corrected_baton),
        "normalized_lf_bytes": len(corrected_baton.encode("utf-8")),
        "words": len(corrected_baton.split()),
        "retained_initial_final": INITIAL_FINAL,
        "prepared_by_lyren_moss": True,
        "prepared_not_sent": True,
        "sent_by_lyren_moss": False,
        "prospective_successor_title": "Ilyra Fen",
        "prospective_successor_phase": "v679-v5",
    }
    write_json(CORRECTION / "activation-candidate-metadata.json", metadata)
    overview = f"""# Lyren Moss v679-v4 dependency correction

The retained initial final `{INITIAL_FINAL}` remains immutable and ancestral. A noncanonical preflight—not the canonical aggregate—found one schema-alias mismatch while replaying the inherited x1 normalized-LF manifest. No canonical latch was created and no selected tests ran in that failed preflight.

This direct-child correction accepts both the historical x1 fields (`sha256_normalized_lf`, `bytes`) and the family-current fields (`sha256`, `normalized_lf_bytes`). It preserves the original final manifest and content seal at the retained initial final and adds a separate corrected-final manifest and content seal. The corrected repository overlay is {corrected['effective_negatives']} effective negatives, {corrected['method_flow_methods']} Method Flow methods, {corrected['failed_witnesses']} failed witnesses, {corrected['bounded_passing_witnesses']} bounded passing witnesses, {corrected['open_gaps']} open gaps, and {corrected['exact_gates']} exact gates. Terminal verdict remains `{corrected['terminal_verdict']}`.

The successor route remains `PREPARED_NOT_SENT`. The exact corrected final must be pushed, clean, fresh-live equal, and canonically validated once before any fresh exact-title Ilyra resolution or send.
"""
    (CORRECTION / "correction-overview.md").write_text(overview, encoding="utf-8", newline="\n")
    receipt = {
        "state": "VALID_DEPENDENCY_CORRECTION_CANDIDATE",
        "retained_initial_final": INITIAL_FINAL,
        "handoff_words": metadata["words"],
        "handoff_sha256": metadata["normalized_lf_sha256"],
        "corrected_effective_negatives": corrected["effective_negatives"],
        "corrected_method_flow_methods": corrected["method_flow_methods"],
        "corrected_failed_witnesses": corrected["failed_witnesses"],
        "corrected_bounded_passing_witnesses": corrected["bounded_passing_witnesses"],
        "canonical_invocations": 0,
        "route_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json(VALIDATION / "correction1-build-receipt.json", receipt)
    return receipt


if __name__ == "__main__":
    print(json.dumps(build(), sort_keys=True))
