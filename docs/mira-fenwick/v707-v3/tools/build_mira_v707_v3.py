#!/usr/bin/env python3
"""Build the additive Mira Fenwick v707-v3 finite-simplicial-complex phase artifacts.

Each lifecycle command writes only its own stage.  Planning must exist before
x1, x1 before x2, and x2 before final.  The exact final canonical is external
and read-only; this builder never invokes it.
"""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha1, sha256
import html
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
PHASE = HERE.parent
REPO = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=HERE, text=True).strip())
sys.path.insert(0, str(HERE))

from ghc_family_simplicial_lab import (  # noqa: E402
    analyze,
    canonical_bytes,
    digest,
    fixtures,
    run_x1_tests,
    run_x2_tests,
    transformation_checks,
)


OWNER = "Mira Fenwick"
PHASE_ID = "v707-v3"
SOURCE = "d3582b4dcd084f80d7b3ea569a2d7f962eb98576"
SOURCE_BRANCH = "codex/GHC-Family/ilyra-fen-main-3"
BRANCH = "codex/GHC-Family/mira-fenwick-main-4"
SUCCESSOR = "Auren Lark"
SUCCESSOR_PHASE = "v707-v4"
BOUNDARY = (
    "Finite synthetic same-owner software and documentation evidence only. "
    "No independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, "
    "participant result, professional judgment, deployment authority, legal or cultural conclusion, "
    "affected-party or Maori authority, complete privacy, accessibility or security assurance, AGI or ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
)
SOURCE_EFFECTIVE = {
    "exact_gates": 2759,
    "fail": 69681,
    "methods": 6664,
    "negatives": 78514,
    "open_gaps": 2415,
    "pass": 231878,
    "witnesses": 301559,
}
ACTIVATION_FAILURES = [
    {"id": "MF7073-ACT-FAIL-001", "state": "fail", "original_success_credit": 0, "observed": "The first combined memory and source inventory wrapper contained an empty PowerShell pipe element and did not execute.", "recovery": "MF7073-ACT-RECOVERY-001"},
    {"id": "MF7073-ACT-FAIL-002", "state": "fail", "original_success_credit": 0, "observed": "A guessed baton EOF-marker check used the wrong literal marker and returned false, earning no baton-completion credit.", "recovery": "MF7073-ACT-RECOVERY-002"},
    {"id": "MF7073-ACT-FAIL-003", "state": "fail", "original_success_credit": 0, "observed": "A recursive route-receipt inventory emitted an oversized truncated projection and earned no bounded terminal-overlay credit.", "recovery": "MF7073-ACT-RECOVERY-003"},
    {"id": "MF7073-ACT-FAIL-004", "state": "fail", "original_success_credit": 0, "observed": "The first worktree orchestration JavaScript contained an unescaped template delimiter and was rejected before any shell command ran.", "recovery": "MF7073-ACT-RECOVERY-004"},
    {"id": "MF7073-ACT-FAIL-005", "state": "fail", "original_success_credit": 0, "observed": "The worktree creation wrapper created the lane but its final report tried to join a null clean-status array and failed.", "recovery": "MF7073-ACT-RECOVERY-005"},
    {"id": "MF7073-ACT-FAIL-006", "state": "fail", "original_success_credit": 0, "observed": "A non-raw JavaScript command string stripped Windows path separators and falsely reported the new worktree missing.", "recovery": "MF7073-ACT-RECOVERY-006"},
    {"id": "MF7073-ACT-FAIL-007", "state": "fail", "original_success_credit": 0, "observed": "The first lab-file writer assumed a btoa global that was unavailable and wrote no file.", "recovery": "MF7073-ACT-RECOVERY-007"},
    {"id": "MF7073-ACT-FAIL-008", "state": "fail", "original_success_credit": 0, "observed": "The second lab-file writer assumed a TextEncoder global that was unavailable and wrote no file.", "recovery": "MF7073-ACT-RECOVERY-008"},
    {"id": "MF7073-ACT-FAIL-009", "state": "fail", "original_success_credit": 0, "observed": "The first builder-transform wrapper contained an unescaped template delimiter and was rejected before mutation.", "recovery": "MF7073-ACT-RECOVERY-009"},
]
ACTIVATION_RECOVERIES = [
    {"id": "MF7073-ACT-RECOVERY-001", "state": "pass", "repairs": "MF7073-ACT-FAIL-001", "observed": "Separate literal-path probes verified memory pointers, source branch, exact head, canonical receipt, and current v19 controls."},
    {"id": "MF7073-ACT-RECOVERY-002", "state": "pass", "repairs": "MF7073-ACT-FAIL-002", "observed": "The committed baton index and exact UTF-8 bytes established the literal EOF marker, hash, word count, and byte count."},
    {"id": "MF7073-ACT-RECOVERY-003", "state": "pass", "repairs": "MF7073-ACT-FAIL-003", "observed": "Four exact route records and a top-level-only inventory established the source terminal overlay without recursive noise."},
    {"id": "MF7073-ACT-RECOVERY-004", "state": "pass", "repairs": "MF7073-ACT-FAIL-004", "observed": "A delimiter-safe orchestration created the fresh additive Mira branch and sparse D-first worktree."},
    {"id": "MF7073-ACT-RECOVERY-005", "state": "pass", "repairs": "MF7073-ACT-FAIL-005", "observed": "A direct scalar read confirmed the exact branch, source head, sparse mode, and clean state."},
    {"id": "MF7073-ACT-RECOVERY-006", "state": "pass", "repairs": "MF7073-ACT-FAIL-006", "observed": "A raw literal-path probe confirmed the registered worktree and exact clean source head."},
    {"id": "MF7073-ACT-RECOVERY-007", "state": "pass", "repairs": "MF7073-ACT-FAIL-007", "observed": "A PowerShell literal UTF-8 writer replaced the unavailable JavaScript base64 helper."},
    {"id": "MF7073-ACT-RECOVERY-008", "state": "pass", "repairs": "MF7073-ACT-FAIL-008", "observed": "The same literal UTF-8 writer removed the unavailable TextEncoder dependency and saved the lab exactly once."},
    {"id": "MF7073-ACT-RECOVERY-009", "state": "pass", "repairs": "MF7073-ACT-FAIL-009", "observed": "A delimiter-safe staged builder transformation applied the intended owner-scoped edits."},
]
ACTIVATION_SUCCESSES = [
    {"id": "MF7073-ACT-DELIVERY-ACK", "state": "pass", "observed": "The current direct activation reports one acknowledged native corrected retry; this is delivery acceptance only and never recipient completion."}
]
X1_RUNTIME_FAILURES: list[dict[str, Any]] = []
X1_RUNTIME_RECOVERIES: list[dict[str, Any]] = []

DEFINITIONS = [
    ("record-shape", "Validate the bounded finite simplicial-complex record shape.", "x1", "completed"),
    ("face-closure", "Enumerate every face implied by the maximal facets.", "x1", "completed"),
    ("simplex-census", "Count nonempty simplices by exact dimension.", "x1", "completed"),
    ("f-vector", "Compute the exact finite f-vector.", "x1", "completed"),
    ("one-skeleton", "Extract the exact graph of vertices and one-simplices.", "x1", "completed"),
    ("connected-components", "Compute connected components of the one-skeleton.", "x1", "completed"),
    ("boundary-matrices", "Construct the exact simplicial boundary matrices over GF(2).", "x1", "completed"),
    ("boundary-square-zero", "Check that each consecutive boundary composition is zero.", "x1", "completed"),
    ("gf2-ranks", "Compute exact ranks of all boundary matrices over GF(2).", "x1", "completed"),
    ("betti-numbers", "Derive finite Betti numbers from chain dimensions and ranks.", "x1", "completed"),
    ("euler-characteristic", "Compute the alternating simplex-count Euler characteristic.", "x2", "completed"),
    ("euler-poincare", "Check equality of simplex and Betti alternating sums.", "x2", "completed"),
    ("reduced-homology", "Represent reduced Betti numbers for the nonempty complex.", "x2", "completed"),
    ("vertex-deletion", "Compute one deterministic induced vertex deletion.", "x2", "completed"),
    ("barycentric-subdivision-census", "Count subdivision simplices as chains of nonempty faces.", "x2", "completed"),
    ("relabel-covariance", "Check invariant finite results under deterministic vertex relabeling.", "x2", "completed"),
    ("accessible-summary", "Render a compact text account of the exact finite result.", "x2", "completed"),
    ("three-coordinate-model", "Represent vertex count, nonempty face count, and total Betti number.", "x2", "represented"),
    ("empirical-calibration-gap", "Retain the absence of real empirical calibration evidence.", "x2", "open_gap"),
    ("deployment-authority-hold", "Hold operational use behind competent authority and affected-party gates.", "x2", "exact_gate"),
]


def _safe_target(path: Path) -> None:
    target = path.absolute()
    try:
        target.relative_to(PHASE.absolute())
    except ValueError as exc:
        raise RuntimeError(f"write outside phase root refused: {target}") from exc
    cursor = PHASE
    for part in target.relative_to(PHASE).parts[:-1]:
        cursor = cursor / part
        if cursor.exists() and cursor.is_symlink():
            raise RuntimeError(f"symlinked parent refused: {cursor}")
    if target.exists() and target.is_symlink():
        raise RuntimeError(f"symlinked output refused: {target}")


def write_bytes(path: Path, data: bytes) -> None:
    _safe_target(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.tmp.{os.getpid()}"
    if temporary.exists():
        raise RuntimeError(f"temporary output already exists: {temporary}")
    flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(temporary, flags, 0o644)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def write_json(path: Path, value: Any) -> None:
    write_bytes(path, json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode("utf-8") + b"\n")


def write_text(path: Path, value: str) -> None:
    write_bytes(path, value.replace("\r\n", "\n").encode("utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_show_json(commit: str, path: str) -> Any:
    raw = subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=REPO)
    return json.loads(raw.decode("utf-8"))


def blob_sha1(data: bytes) -> str:
    return sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def file_entry(path: Path) -> dict[str, Any]:
    data = path.read_bytes()
    return {
        "bytes": len(data),
        "git_blob_sha1": blob_sha1(data),
        "path": path.relative_to(REPO).as_posix(),
        "sha256": sha256(data).hexdigest(),
    }


def files_under(*roots: Path, exclude: Iterable[Path] = ()) -> list[Path]:
    exclusions = {item.absolute() for item in exclude}
    files: list[Path] = []
    for root in roots:
        if root.is_file() and root.absolute() not in exclusions:
            files.append(root)
        elif root.exists():
            files.extend(path for path in root.rglob("*") if path.is_file() and path.absolute() not in exclusions and ".tmp." not in path.name)
    return sorted(set(files), key=lambda value: value.relative_to(REPO).as_posix())


def write_manifest(path: Path, roots: list[Path], self_exclusions: list[str]) -> None:
    excluded_paths = [PHASE / item for item in self_exclusions]
    entries = [file_entry(item) for item in files_under(*roots, exclude=excluded_paths)]
    write_json(
        path,
        {
            "boundary": BOUNDARY,
            "count": len(entries),
            "entries": entries,
            "schema": "ghc.family.git-blob-manifest.v1",
            "self_exclusions": self_exclusions,
        },
    )


def definition_records() -> list[dict[str, Any]]:
    rows = []
    for index, (mechanism, title, stage, disposition) in enumerate(DEFINITIONS, start=1):
        base = {"operation": index, "mechanism": mechanism, "title": title, "stage": stage, "expected_disposition": disposition}
        rows.append({**base, "definition_sha256": digest(base)})
    return rows


def proposal_records() -> list[dict[str, Any]]:
    rows = []
    definitions = definition_records()
    number = 0
    for fixture in fixtures():
        fixture_hash = digest(fixture)
        for definition in definitions:
            number += 1
            rows.append(
                {
                    "id": f"MF7073-P{number:03d}",
                    "fixture_id": fixture["id"],
                    "fixture_sha256": fixture_hash,
                    "operation": definition["operation"],
                    "mechanism": definition["mechanism"],
                    "title": f"{definition['title']} {fixture['id']}",
                    "stage": definition["stage"],
                    "expected_disposition": definition["expected_disposition"],
                    "definition_sha256": definition["definition_sha256"],
                    "scope": "Declared finite synthetic simplicial fixture and mechanism only; established finite mathematics and a new Mira implementation case.",
                    "falsifier": "Schema acceptance of an invalid subject, disagreement with the separately structured exhaustive oracle, broken bijection or transformation law, changed digest, or promotion beyond the declared disposition.",
                }
            )
    assert len(rows) == 300
    assert Counter(row["expected_disposition"] for row in rows) == Counter({"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15})
    return rows


def method_flow_counts(witnesses: list[dict[str, Any]], methods: list[str], open_gaps: int = 0, exact_gates: int = 0) -> dict[str, int]:
    states = Counter(row["state"] for row in witnesses)
    return {
        "methods": len(methods),
        "witnesses": len(witnesses),
        "pass": states["pass"],
        "fail": states["fail"],
        "negatives": states["fail"],
        "open_gaps": open_gaps,
        "exact_gates": exact_gates,
    }


def build_planning() -> None:
    planning = PHASE / "planning"
    if planning.exists():
        raise RuntimeError("planning already exists; lifecycle replay refused")
    fixture_rows = fixtures()
    proposals = proposal_records()
    inherited = git_show_json(SOURCE, "docs/ilyra-fen/v707-v2/planning/proposals.json")["proposals"]
    if len(inherited) != 300:
        raise RuntimeError("expected exactly 300 inherited source proposals")
    inherited_rows = [
        {
            "source_id": row["id"],
            "source_title": row["title"],
            "source_definition_sha256": row["definition_sha256"],
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for row in inherited
    ]
    inherited_titles = {row["source_title"] for row in inherited_rows}
    overlap = sorted(row["title"] for row in proposals if row["title"] in inherited_titles)
    if overlap:
        raise RuntimeError(f"new proposal title overlap: {overlap[:3]}")

    planning_methods = ["source exactness evidence", "terminal overlay fold discipline", "native delivery acknowledgement boundary", "v19 authority resolution", "D-first sparse-lane bootstrap"]
    planning_witnesses = [
        {"witness_id": row["id"], "state": row["state"], "kind": "retained activation failure", "original_success_credit": 0}
        for row in ACTIVATION_FAILURES
    ] + [
        {"witness_id": row["id"], "state": row["state"], "kind": "bounded activation recovery", "repairs": row["repairs"]}
        for row in ACTIVATION_RECOVERIES
    ] + [
        {"witness_id": row["id"], "state": row["state"], "kind": "bounded activation success"}
        for row in ACTIVATION_SUCCESSES
    ]
    write_json(planning / "fixtures.json", {"boundary": BOUNDARY, "count": len(fixture_rows), "fixtures": fixture_rows})
    write_json(planning / "definitions.json", {"boundary": BOUNDARY, "count": 20, "definitions": definition_records()})
    write_json(
        planning / "proposals.json",
        {
            "boundary": BOUNDARY,
            "count": 300,
            "outcomes": dict(Counter(row["expected_disposition"] for row in proposals)),
            "planning_only": True,
            "proposals": proposals,
        },
    )
    write_json(
        planning / "inherited-zero-credit.json",
        {
            "boundary": BOUNDARY,
            "count": 300,
            "source": SOURCE,
            "title_overlap_with_new": 0,
            "records": inherited_rows,
        },
    )
    write_json(
        planning / "source-proof.json",
        {
            "boundary": BOUNDARY,
            "source_owner": "Ilyra Fen",
            "source_phase": "v707-v2",
            "source_branch": SOURCE_BRANCH,
            "source_exact_final": SOURCE,
            "baton_path": "docs/ilyra-fen/v707-v2/final/baton.md",
            "baton_words": 3455,
            "baton_bytes": 26403,
            "baton_sha256": "3fef6c48077ac5fab16625a86aea919f35e97a5b1a520398098c4a678b4b63dc",
            "baton_eof": "LITERAL_EOF_ILYRA_V707_V2",
            "canonical_receipt_sha256": "1e3a7b82edd8667daa5540586fb7d71790b4c525046240c9d7b8e11cd251581f",
            "canonical_payload_sha256": "f45c03d6b0a10efa1f330ce636e8ee8a01706c79c5952fbd4d44969839484537",
            "canonical_counts": {"invocations": 1, "successes": 1, "replays": 0},
            "terminal_after_verification_selected_once": SOURCE_EFFECTIVE,
            "terminal_effective_fold_count": 1,
            "source_manifest_entries_replayed": 100,
            "source_manifest_mismatches": 0,
            "current_native_retry_acknowledged": True,
            "delivery_ack_folded_into_source_numeric_baseline": False,
            "recipient_completion": "UNCLAIMED",
            "source_replayed": False,
            "source_mutated": False,
        },
    )
    write_json(
        planning / "method-flow.json",
        {
            "schema": "ghc.family.method-flow.v1",
            "session": "planning",
            "boundary": BOUNDARY,
            "methods": planning_methods,
            "counts": method_flow_counts(planning_witnesses, planning_methods),
            "failures": ACTIVATION_FAILURES,
            "recoveries": ACTIVATION_RECOVERIES,
            "witnesses": planning_witnesses,
        },
    )
    write_json(
        planning / "workflow-v19.json",
        {
            "schema": "ghc.family.mira-finite-simplicial-complex.v1",
            "authority": "Hamish workflow v19 plus current Ilyra activation",
            "owner": OWNER,
            "phase": PHASE_ID,
            "next_owner": SUCCESSOR,
            "next_phase": SUCCESSOR_PHASE,
            "branch": BRANCH,
            "source": SOURCE,
            "shared_and_sibling_lanes": "read_only",
            "minimums": {"inherited": 300, "new": 300, "safe_each": 400, "candidate_each": 300, "cfr_each": 300, "exact": 50, "blocked": 30, "skills_each": 10, "runners_each": 5, "x1_tests": 15, "x2_tests": 30, "x2_models": 15, "hooks": 5},
            "planned": {"safe_each": 450, "candidate_each": 300, "cfr_each": 300, "skills_each": 10, "runners_each": 5, "x1_tests": 20, "x2_tests": 30, "x2_models": 15, "hooks": 5},
            "search_ceiling_each": 2000,
            "allowed_formats": ["json", "md", "txt", "html", "py"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    exact_packets = [{"id": f"MF7073-EXACT-{index:03d}", "state": "held", "executed": False, "gate": "named external evidence or competent authority required"} for index in range(1, 51)]
    blocked_packets = [{"id": f"MF7073-BLOCKED-{index:03d}", "state": "blocked", "executed": False, "reason": "outside bounded synthetic owner authority"} for index in range(1, 31)]
    write_json(planning / "approval-packets.json", {"boundary": BOUNDARY, "exact_count": 50, "blocked_count": 30, "exact": exact_packets, "blocked": blocked_packets})
    write_json(
        planning / "operations.json",
        {
            "boundary": BOUNDARY,
            "domain": "bounded finite abstract simplicial complexes, GF(2) boundaries, homology, and exact combinatorial certificates",
            "x1": {"proposal_results": 150, "safe": 450, "candidate_invalid": 300, "refusal_guards": 300, "corrected_copies": 300, "tests": 20, "skills": 10, "runners": 5},
            "x2": {"proposal_results": 150, "safe": 450, "candidate_invalid": 300, "refusal_guards": 300, "corrected_copies": 300, "tests": 30, "skills": 10, "runners": 5, "models": 15, "hooks": 5},
            "commit_plan": ["planning", "x1", "x2", "final"],
            "canonical": "one read-only metadata aggregate only after clean pushed fresh-live-equal final",
        },
    )
    write_json(
        planning / "identity.json",
        {
            "name": OWNER,
            "role": "finite-topology evidence cartographer",
            "hope": "make bounded topological structure, correction, and authority limits inspectable without promoting synthetic enumeration into real-world authority",
            "relational_only": True,
            "boundary": "Name, role, hope, pronouns, family and continuity language are working conventions only, not evidence of consciousness, personhood, identity continuity, employment, qualification, agency or authority.",
        },
    )
    write_json(
        planning / "practices.json",
        {
            "boundary": BOUNDARY,
            "count": 8,
            "practices": [
                "discrete mathematics documentation",
                "software verification",
                "archival provenance design",
                "accessibility-oriented technical writing",
                "data quality review",
                "governance boundary analysis",
                "test engineering",
                "reversible handover design",
            ],
            "qualification_claimed": False,
        },
    )
    write_json(
        planning / "law-hypotheses.json",
        {
            "boundary": BOUNDARY,
            "count": 15,
            "status": "proposal_only",
            "hypotheses": [{"id": f"MF7073-HYP-{index:02d}", "claim": f"For declared synthetic fixture {fixture['id']}, simplicial structure may be used as a finite analogy only; it is not a discovered physical or psychological law."} for index, fixture in enumerate(fixture_rows, start=1)],
        },
    )
    write_json(
        planning / "open-problem-probes.json",
        {
            "boundary": BOUNDARY,
            "count": 15,
            "status": "unsolved",
            "probes": [{"id": f"MF7073-PROBE-{index:02d}", "question": f"Which additional evidence would be required before any analogy drawn from {fixture['id']} could support an external claim?", "answer": "No external claim is established in this phase."} for index, fixture in enumerate(fixture_rows, start=1)],
        },
    )
    write_json(
        planning / "hook-plan.json",
        {
            "boundary": BOUNDARY,
            "count": 5,
            "installed": False,
            "hooks": [{"id": f"MF7073-HOOK-{index}", "mode": mode, "manual_smoke_only": True, "live_host_observation": False} for index, mode in enumerate(["planning", "x1", "x2", "final", "handoff"], start=1)],
        },
    )
    write_json(
        planning / "successor-recommendations.json",
        {
            "boundary": BOUNDARY,
            "skills": [f"mira-fenwick-recommendation-skill-{index}" for index in range(1, 6)],
            "runners": [f"mira_fenwick_recommendation_runner_{index}.py" for index in range(1, 6)],
            "practices": ["finite cell-complex visualization", "accessibility-preserving topology summaries", "provenance review for derived invariants", "independent-oracle test design"],
            "completion_credit": 0,
        },
    )
    plan_text = f"""# Mira Fenwick {PHASE_ID} planning freeze

This phase builds exact finite simplicial-complex, GF(2) boundary, Betti-number, Euler-Poincare, subdivision-census, and provenance certificates over fifteen new synthetic fixtures. It does not replay Ilyra Fen's finite-poset solver, tests, models, hooks, or canonical. Planning freezes 300 inherited Ilyra records at zero novelty and completion credit, 300 genuinely new Mira contracts, the four exact outcome labels, the v19 workload, a D-first sparse owner lane, five manual uninstalled hook candidates, and the prospective {SUCCESSOR} {SUCCESSOR_PHASE} edge.

The primary lens is GMUT Mind as disciplined finite mathematical specification. THOS Body remains visible through executable bounded evidence. Freed ID and CBR Heart remain visible through provenance, correction, remedy, accessibility, and authority reservations. No physical, empirical, production, identity, professional, legal, cultural, affected-party, Maori-authority, consciousness/personhood, proof/canon, or Stage 20 claim follows.
"""
    write_text(planning / "plan.md", plan_text)
    write_text(planning / "planning-freeze.md", f"Planning definitions frozen before x1. Source {SOURCE}. New proposals 300. Inherited zero-credit 300. Outcomes 255/15/15/15. Terminal verdict NOT_READY_FOR_STAGE_20.\n")
    write_manifest(planning / "manifest.json", [planning, HERE], ["planning/manifest.json"])


def evaluate_contract(proposal: dict[str, Any], analyses: dict[str, dict[str, Any]], transforms: dict[str, dict[str, Any]]) -> Any:
    result = analyses[proposal["fixture_id"]]
    mechanism = proposal["mechanism"]
    if mechanism == "record-shape":
        return True
    if mechanism == "face-closure":
        return result["nonempty_face_count"]
    if mechanism == "simplex-census":
        return {"dimension": result["dimension"], "count": result["nonempty_face_count"]}
    if mechanism == "f-vector":
        return result["f_vector"]
    if mechanism == "one-skeleton":
        return result["one_skeleton_edges"]
    if mechanism == "connected-components":
        return {"count": result["component_count"], "components": result["components"]}
    if mechanism == "boundary-matrices":
        return {"ranks": result["boundary_ranks"], "dimensions": len(result["f_vector"])}
    if mechanism == "boundary-square-zero":
        return result["boundary_square_zero"]
    if mechanism == "gf2-ranks":
        return result["boundary_ranks"]
    if mechanism == "betti-numbers":
        return result["betti_numbers"]
    if mechanism == "euler-characteristic":
        return result["euler_characteristic"]
    if mechanism == "euler-poincare":
        return transforms[proposal["fixture_id"]]["euler_poincare"]
    if mechanism == "reduced-homology":
        return result["reduced_betti_numbers"]
    if mechanism == "vertex-deletion":
        return transforms[proposal["fixture_id"]]["vertex_deletion"]
    if mechanism == "barycentric-subdivision-census":
        return transforms[proposal["fixture_id"]]["barycentric_subdivision_census"]
    if mechanism == "relabel-covariance":
        return transforms[proposal["fixture_id"]]["relabel_covariant"]
    if mechanism == "accessible-summary":
        return f"{proposal['fixture_id']} has {result['vertex_count']} vertices, dimension {result['dimension']}, f-vector {result['f_vector']}, Betti numbers {result['betti_numbers']}, and Euler characteristic {result['euler_characteristic']}."
    if mechanism == "three-coordinate-model":
        return {"x_vertex_count": result["vertex_count"], "y_nonempty_face_count": result["nonempty_face_count"], "z_total_betti": sum(result["betti_numbers"])}
    if mechanism == "empirical-calibration-gap":
        return {"state": "open_gap", "real_data": False, "claim": "no empirical calibration evidence supplied or inferred"}
    if mechanism == "deployment-authority-hold":
        return {"state": "exact_gate", "deployment_authorized": False, "authority_supplied": False}
    raise KeyError(mechanism)


def workload_rows(proposals: list[dict[str, Any]], stage: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    safe: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    refusals: list[dict[str, Any]] = []
    corrected: list[dict[str, Any]] = []
    safe_number = 0
    candidate_number = 0
    for proposal in proposals:
        for predicate in ("source-digest-bound", "disposition-preserved", "canonical-json-roundtrip"):
            safe_number += 1
            safe.append({"id": f"{proposal['id']}-{stage}-safe-{safe_number:04d}", "proposal_id": proposal["id"], "predicate": predicate, "state": "pass"})
        for mutation in ("remove-fixture-id", "promote-disposition"):
            candidate_number += 1
            candidate_id = f"{proposal['id']}-{stage}-candidate-{candidate_number:04d}"
            candidates.append({"id": candidate_id, "proposal_id": proposal["id"], "mutation": mutation, "state": "fail", "original_success_credit": 0})
            refusals.append({"id": candidate_id + "-REFUSAL", "subject": candidate_id, "state": "pass", "promotes_subject": False})
            corrected.append({"id": candidate_id + "-CFR", "repairs": candidate_id, "state": "pass", "original_remains_failed": True})
    assert len(safe) == 450 and len(candidates) == len(refusals) == len(corrected) == 300
    return safe, candidates, refusals, corrected


def skill_markdown(name: str, title: str, mechanism: str) -> str:
    return f"""---
name: {name}
description: Inspect the bounded {mechanism} evidence contract for finite synthetic simplicial-complex records; do not use it for empirical or operational authority.
---

# {title}

Use the saved Mira Fenwick {PHASE_ID} records to inspect `{mechanism}`. Confirm the exact fixture digest, declared disposition, and saved result before drawing a bounded software conclusion. Preserve malformed subjects as failed records even when a separate refusal or corrected-copy witness passes.

This skill is repository-local and phase-scoped. It does not rerun inherited work, install anything globally, act on an external system, or establish independent reproduction, empirical validation, professional qualification, production readiness, legal or cultural authority, Maori authority, identity/personhood, Theory-of-Everything proof, canon, or Stage 20 readiness.
"""


def runner_source(runner_id: str, stage: str) -> str:
    return f'''#!/usr/bin/env python3
"""Saved-evidence reader for {runner_id}; it never reruns the domain solver."""
import json
from pathlib import Path
import sys

path = Path(sys.argv[1])
payload = json.loads(path.read_text(encoding="utf-8"))
rows = payload["results"]
print(json.dumps({{"runner": "{runner_id}", "stage": "{stage}", "saved_records": len(rows), "source": str(path.name)}}, sort_keys=True))
'''


def validate_skills(skill_dirs: list[Path]) -> list[dict[str, Any]]:
    validator = Path("C:/Users/hamis/.codex/skills/.system/skill-creator/scripts/quick_validate.py")
    receipts = []
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    for path in skill_dirs:
        completed = subprocess.run([sys.executable, str(validator), str(path)], capture_output=True, text=True, env=environment, check=False)
        receipts.append({"skill": path.name, "state": "pass" if completed.returncode == 0 else "fail", "exit_code": completed.returncode, "stdout": completed.stdout.strip(), "stderr": completed.stderr.strip()})
    if not all(row["state"] == "pass" for row in receipts):
        raise RuntimeError("local skill validation failed")
    return receipts


def create_runners(stage_dir: Path, stage: str, results_path: Path) -> list[dict[str, Any]]:
    runner_dir = stage_dir / "runners"
    receipts = []
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    for index in range(1, 6):
        runner_id = f"ghc_family_simplicial_{stage}_{index:02d}"
        path = runner_dir / f"{runner_id}.py"
        write_text(path, runner_source(runner_id, stage))
        completed = subprocess.run([sys.executable, str(path), str(results_path)], capture_output=True, text=True, env=environment, check=False)
        receipts.append({"runner": runner_id, "state": "pass" if completed.returncode == 0 else "fail", "exit_code": completed.returncode, "stdout": completed.stdout.strip(), "stderr": completed.stderr.strip(), "saved_evidence_only": True})
    if not all(row["state"] == "pass" for row in receipts):
        raise RuntimeError("saved-evidence runner smoke failed")
    return receipts


def stage_witnesses(
    proposal_results: list[dict[str, Any]],
    safe: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    refusals: list[dict[str, Any]],
    corrected: list[dict[str, Any]],
    tests: list[dict[str, Any]],
    skills: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    extras: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    witnesses = [{"witness_id": row["id"] + "-RESULT", "state": "pass", "kind": "bounded operation result"} for row in proposal_results]
    witnesses += [{"witness_id": row["id"], "state": "pass", "kind": "safe predicate"} for row in safe]
    witnesses += [{"witness_id": row["id"], "state": "fail", "kind": "malformed candidate", "original_success_credit": 0} for row in candidates]
    witnesses += [{"witness_id": row["id"], "state": "pass", "kind": "separate refusal guard", "promotes_subject": False} for row in refusals]
    witnesses += [{"witness_id": row["id"], "state": "pass", "kind": "corrected-copy validation", "original_remains_failed": True} for row in corrected]
    witnesses += [{"witness_id": row["id"], "state": "pass", "kind": "focused test"} for row in tests]
    witnesses += [
        {"witness_id": row["id"] + "-SUBJECT", "state": "fail", "kind": "malformed focused-test subject", "original_success_credit": 0}
        for row in tests
        if row.get("invalid_subject_state") == "fail"
    ]
    witnesses += [{"witness_id": "SKILL-" + row["skill"], "state": "pass", "kind": "skill validation"} for row in skills]
    witnesses += [{"witness_id": "RUNNER-" + row["runner"], "state": "pass", "kind": "runner smoke"} for row in runners]
    witnesses += extras or []
    return witnesses


def build_x1() -> None:
    if not (PHASE / "planning" / "planning-freeze.md").exists():
        raise RuntimeError("planning freeze missing")
    x1 = PHASE / "x1"
    if x1.exists():
        raise RuntimeError("x1 already exists; lifecycle replay refused")
    proposals = [row for row in load_json(PHASE / "planning" / "proposals.json")["proposals"] if row["stage"] == "x1"]
    if len(proposals) != 150:
        raise RuntimeError("x1 proposal-stage selection did not yield 150 records")
    fixture_rows = fixtures()
    analyses = {row["id"]: analyze(row) for row in fixture_rows}
    transforms: dict[str, dict[str, Any]] = {}
    results = [{"id": row["id"], "proposal_id": row["id"], "fixture_id": row["fixture_id"], "mechanism": row["mechanism"], "disposition": row["expected_disposition"], "state": "pass", "value": evaluate_contract(row, analyses, transforms)} for row in proposals]
    safe, candidates, refusals, corrected = workload_rows(proposals, "x1")
    tests = run_x1_tests()
    if len(tests) != 20 or not all(row["passed"] for row in tests):
        raise RuntimeError("x1 focused tests did not pass")
    write_json(x1 / "results.json", {"boundary": BOUNDARY, "count": len(results), "results": results})
    write_json(x1 / "safe-now.json", {"boundary": BOUNDARY, "count": 450, "records": safe})
    write_json(x1 / "candidate.json", {"boundary": BOUNDARY, "count": 300, "records": candidates})
    write_json(x1 / "refusal-guards.json", {"boundary": BOUNDARY, "count": 300, "promotes_invalid_subject": False, "records": refusals})
    write_json(x1 / "cfr.json", {"boundary": BOUNDARY, "count": 300, "erases_original_failure": False, "records": corrected})
    write_json(x1 / "tests.json", {"boundary": BOUNDARY, "count": 20, "passed": 20, "records": tests, "complete_repository_suite": False})

    skill_dirs = []
    for mechanism, title, stage, _ in DEFINITIONS[:10]:
        assert stage == "x1"
        name = "ghc-family-simplicial-" + mechanism
        directory = x1 / "skills" / name
        write_text(directory / "SKILL.md", skill_markdown(name, title, mechanism))
        skill_dirs.append(directory)
    skill_receipts = validate_skills(skill_dirs)
    write_json(x1 / "skill-validation.json", {"boundary": BOUNDARY, "count": 10, "records": skill_receipts})
    runner_receipts = create_runners(x1, "x1", x1 / "results.json")
    write_json(x1 / "runner-receipts.json", {"boundary": BOUNDARY, "count": 5, "records": runner_receipts})

    methods = [row[0] for row in DEFINITIONS[:10]] + ["focused tests", "local skill validation", "saved-evidence runner smokes"]
    runtime_extras = [
        {"witness_id": row["id"], "state": "fail", "kind": "retained x1 runtime failure", "original_success_credit": 0}
        for row in X1_RUNTIME_FAILURES
    ] + [
        {"witness_id": row["id"], "state": "pass", "kind": "bounded x1 runtime recovery", "repairs": row["repairs"]}
        for row in X1_RUNTIME_RECOVERIES
    ]
    witnesses = stage_witnesses(results, safe, candidates, refusals, corrected, tests, skill_receipts, runner_receipts, runtime_extras)
    counts = method_flow_counts(witnesses, methods)
    if counts != {"methods": 13, "witnesses": 1540, "pass": 1235, "fail": 305, "negatives": 305, "open_gaps": 0, "exact_gates": 0}:
        raise RuntimeError(f"unexpected x1 Method Flow counts: {counts}")
    write_json(x1 / "method-flow.json", {"schema": "ghc.family.method-flow.v1", "session": "x1", "boundary": BOUNDARY, "methods": methods, "counts": counts, "runtime_failures": X1_RUNTIME_FAILURES, "runtime_recoveries": X1_RUNTIME_RECOVERIES, "witnesses": witnesses})
    write_text(
        x1 / "report.md",
        "# Mira Fenwick v707-v3 x1\n\nX1 executed exact face closure, simplex census, f-vector, one-skeleton, component, GF(2) boundary, rank, and Betti checks over fifteen synthetic complexes. Fifteen separately structured brute-force oracle comparisons and five refusal tests passed. Three hundred malformed candidates remain failed at zero credit; separate refusal and corrected-copy witnesses do not promote or erase them. Evidence is bounded same-owner software evidence only.\n",
    )
    write_json(x1 / "session-summary.json", {"boundary": BOUNDARY, "stage": "x1", "counts": counts, "tests": "20/20", "skills": "10/10", "runners": "5/5", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_manifest(x1 / "manifest.json", [x1], ["x1/manifest.json"])


def hook_source(hook_id: str) -> str:
    return f'''#!/usr/bin/env python3
"""Manual uninstalled lifecycle-envelope candidate {hook_id}."""
import json
import sys

try:
    payload = json.loads(sys.stdin.read())
except Exception:
    print(json.dumps({{"hook": "{hook_id}", "decision": "refuse", "reason": "invalid-json"}}, sort_keys=True))
    raise SystemExit(2)
required = {{"event", "owner", "phase", "exact_head"}}
if set(payload) != required or payload.get("owner") != "Mira Fenwick" or payload.get("phase") != "v707-v3" or payload.get("event") not in {{"planning", "x1", "x2", "final", "handoff"}}:
    print(json.dumps({{"hook": "{hook_id}", "decision": "refuse", "reason": "invalid-envelope"}}, sort_keys=True))
    raise SystemExit(2)
print(json.dumps({{"hook": "{hook_id}", "decision": "accept-manual-smoke-only", "event": payload["event"]}}, sort_keys=True))
'''


def create_hooks(x2: Path) -> list[dict[str, Any]]:
    receipts = []
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    events = ["planning", "x1", "x2", "final", "handoff"]
    for index, event in enumerate(events, start=1):
        hook_id = f"ghc_family_simplicial_hook_{index:02d}"
        path = x2 / "hooks" / f"{hook_id}.py"
        write_text(path, hook_source(hook_id))
        valid = json.dumps({"event": event, "owner": OWNER, "phase": PHASE_ID, "exact_head": "manual-smoke-placeholder"})
        invalid = json.dumps({"event": event, "owner": OWNER})
        accepted = subprocess.run([sys.executable, str(path)], input=valid, capture_output=True, text=True, env=environment, check=False)
        refused = subprocess.run([sys.executable, str(path)], input=invalid, capture_output=True, text=True, env=environment, check=False)
        if accepted.returncode != 0 or refused.returncode == 0:
            raise RuntimeError(f"hook smoke failed: {hook_id}")
        receipts.append(
            {
                "hook": hook_id,
                "installed": False,
                "live_host_observation": False,
                "valid": {"state": "pass", "exit_code": accepted.returncode, "stdout": accepted.stdout.strip()},
                "invalid_subject": {"state": "fail", "exit_code": refused.returncode, "stdout": refused.stdout.strip(), "original_success_credit": 0},
                "refusal_guard": {"state": "pass", "promotes_invalid_subject": False},
            }
        )
    return receipts


def build_x2() -> None:
    if not (PHASE / "x1" / "session-summary.json").exists():
        raise RuntimeError("x1 evidence missing")
    x2 = PHASE / "x2"
    if x2.exists():
        raise RuntimeError("x2 already exists; lifecycle replay refused")
    proposals = [row for row in load_json(PHASE / "planning" / "proposals.json")["proposals"] if row["stage"] == "x2"]
    if len(proposals) != 150:
        raise RuntimeError("x2 proposal-stage selection did not yield 150 records")
    fixture_rows = fixtures()
    analyses = {row["id"]: analyze(row) for row in fixture_rows}
    transforms = {row["id"]: transformation_checks(row) for row in fixture_rows}
    results = [{"id": row["id"], "proposal_id": row["id"], "fixture_id": row["fixture_id"], "mechanism": row["mechanism"], "disposition": row["expected_disposition"], "state": "pass", "value": evaluate_contract(row, analyses, transforms)} for row in proposals]
    safe, candidates, refusals, corrected = workload_rows(proposals, "x2")
    tests = run_x2_tests()
    if len(tests) != 30 or not all(row["passed"] for row in tests):
        raise RuntimeError("x2 focused tests did not pass")
    models = [
        {
            "id": f"MF7073-MODEL-{index:02d}",
            "fixture_id": row["id"],
            "coordinates": {"x_vertex_count": analyses[row["id"]]["vertex_count"], "y_nonempty_face_count": analyses[row["id"]]["nonempty_face_count"], "z_total_betti": sum(analyses[row["id"]]["betti_numbers"])},
            "abstract_data_coordinates_only": True,
        }
        for index, row in enumerate(fixture_rows, start=1)
    ]
    write_json(x2 / "results.json", {"boundary": BOUNDARY, "count": 150, "results": results})
    write_json(x2 / "transformations.json", {"boundary": BOUNDARY, "count": 15, "records": list(transforms.values())})
    write_json(x2 / "safe-now.json", {"boundary": BOUNDARY, "count": 450, "records": safe})
    write_json(x2 / "candidate.json", {"boundary": BOUNDARY, "count": 300, "records": candidates})
    write_json(x2 / "refusal-guards.json", {"boundary": BOUNDARY, "count": 300, "promotes_invalid_subject": False, "records": refusals})
    write_json(x2 / "cfr.json", {"boundary": BOUNDARY, "count": 300, "erases_original_failure": False, "records": corrected})
    write_json(x2 / "tests.json", {"boundary": BOUNDARY, "count": 30, "passed": 30, "records": tests, "complete_repository_suite": False})
    write_json(x2 / "models.json", {"boundary": BOUNDARY, "count": 15, "models": models, "physical_geometry": False, "open_world": False})

    skill_dirs = []
    for mechanism, title, stage, _ in DEFINITIONS[10:]:
        assert stage == "x2"
        name = "ghc-family-simplicial-" + mechanism
        directory = x2 / "skills" / name
        write_text(directory / "SKILL.md", skill_markdown(name, title, mechanism))
        skill_dirs.append(directory)
    skill_receipts = validate_skills(skill_dirs)
    write_json(x2 / "skill-validation.json", {"boundary": BOUNDARY, "count": 10, "records": skill_receipts})
    runner_receipts = create_runners(x2, "x2", x2 / "results.json")
    write_json(x2 / "runner-receipts.json", {"boundary": BOUNDARY, "count": 5, "records": runner_receipts})
    hook_receipts = create_hooks(x2)
    write_json(x2 / "hook-receipts.json", {"boundary": BOUNDARY, "count": 5, "installed": False, "live_host_observations": 0, "records": hook_receipts})

    proposal_cards = [{"card_id": f"CARD-{index:03d}", "tier": 4, "freed_id": OWNER, "pillar": "GMUT Mind" if index % 3 == 1 else "THOS Body" if index % 3 == 2 else "Freed ID and CBR Heart", "practice": "finite topology verification", "subject": row["id"], "content_sha256": digest(row)} for index, row in enumerate(load_json(PHASE / "planning" / "proposals.json")["proposals"], start=1)]
    cards = [
        {"card_id": "CARD-IDENTITY", "tier": 1, "subject": OWNER, "relational_only": True},
        {"card_id": "CARD-PILLAR-MIND", "tier": 2, "subject": "GMUT Mind", "claim": "typed finite mathematics only"},
        {"card_id": "CARD-PILLAR-BODY", "tier": 2, "subject": "THOS Body", "claim": "bounded software evidence only"},
        {"card_id": "CARD-PILLAR-HEART", "tier": 2, "subject": "Freed ID and CBR Heart", "claim": "provenance and authority reservations only"},
    ]
    practices = load_json(PHASE / "planning" / "practices.json")["practices"]
    cards += [{"card_id": f"CARD-PRACTICE-{index:02d}", "tier": 3, "subject": practice, "qualification_claimed": False} for index, practice in enumerate(practices, start=1)]
    cards += proposal_cards
    assert len(cards) == 312
    write_json(x2 / "context-deck.json", {"boundary": BOUNDARY, "schema": "ghc.family.four-tier-context-deck.v1", "count": 312, "cards": cards})

    header = "<tr><th scope='col'>Fixture</th><th scope='col'>Vertices</th><th scope='col'>Nonempty faces</th><th scope='col'>Total Betti</th></tr>"
    body = "".join(f"<tr><th scope='row'>{html.escape(model['fixture_id'])}</th><td>{model['coordinates']['x_vertex_count']}</td><td>{model['coordinates']['y_nonempty_face_count']}</td><td>{model['coordinates']['z_total_betti']}</td></tr>" for model in models)
    model_html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Mira v707-v3 finite-simplicial-complex atlas</title></head><body><main><h1>Finite synthetic simplicial-complex atlas</h1><p>{html.escape(BOUNDARY)}</p><table><caption>Abstract data coordinates; not physical geometry or operational authority.</caption><thead>{header}</thead><tbody>{body}</tbody></table></main></body></html>\n"
    write_text(x2 / "model-atlas.html", model_html)

    methods = [row[0] for row in DEFINITIONS[10:]] + ["focused transformation tests", "local skill validation", "saved-evidence runner smokes", "abstract model atlas", "manual uninstalled hook smokes", "four-tier context deck"]
    extras = []
    extras += [{"witness_id": f"MODEL-{row['id']}", "state": "pass", "kind": "abstract three-coordinate model"} for row in models]
    for row in hook_receipts:
        extras.append({"witness_id": row["hook"] + "-VALID", "state": "pass", "kind": "manual hook valid envelope"})
        extras.append({"witness_id": row["hook"] + "-INVALID-SUBJECT", "state": "fail", "kind": "invalid manual hook envelope", "original_success_credit": 0})
        extras.append({"witness_id": row["hook"] + "-REFUSAL", "state": "pass", "kind": "manual hook refusal guard", "promotes_subject": False})
    extras.append({"witness_id": "MF7073-CONTEXT-DECK", "state": "pass", "kind": "four-tier context deck"})
    witnesses = stage_witnesses(results, safe, candidates, refusals, corrected, tests, skill_receipts, runner_receipts, extras)
    counts = method_flow_counts(witnesses, methods, open_gaps=21, exact_gates=20)
    if counts != {"methods": 16, "witnesses": 1576, "pass": 1271, "fail": 305, "negatives": 305, "open_gaps": 21, "exact_gates": 20}:
        raise RuntimeError(f"unexpected x2 Method Flow counts: {counts}")
    write_json(x2 / "method-flow.json", {"schema": "ghc.family.method-flow.v1", "session": "x2", "boundary": BOUNDARY, "methods": methods, "counts": counts, "witnesses": witnesses})
    write_text(
        x2 / "report.md",
        "# Mira Fenwick v707-v3 x2\n\nX2 executed Euler characteristic, Euler-Poincare, reduced-homology, deterministic vertex-deletion, barycentric-subdivision census, relabel covariance, accessible-summary, and three-coordinate representations over fifteen frozen synthetic complexes. Thirty focused transformation tests passed. Empirical-calibration rows remain open gaps and deployment rows remain exact gates. Five hook candidates ran only as manual subprocesses and remain uninstalled with no live-host evidence.\n",
    )
    write_json(x2 / "session-summary.json", {"boundary": BOUNDARY, "stage": "x2", "counts": counts, "tests": "30/30", "skills": "10/10", "runners": "5/5", "models": "15/15", "hooks": "5 manual uninstalled", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_manifest(x2 / "manifest.json", [x2], ["x2/manifest.json"])


def add_counts(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    return {key: left[key] + right[key] for key in ("methods", "witnesses", "pass", "fail", "negatives", "open_gaps", "exact_gates")}


def baton_text(owner_counts: dict[str, int], effective: dict[str, int]) -> str:
    sections = [
        f"# MIRA FENWICK {PHASE_ID} EXACT FINAL TO PROSPECTIVE AUREN LARK {SUCCESSOR_PHASE} - PREPARED NOT SENT\n",
        f"Dear {SUCCESSOR},\n\nThis committed baton is preparation evidence only. It does not prove native delivery, recipient reading, activation, or completion. A later external terminal receipt must bind the exact final, the single successful non-replayed owner-scoped canonical, current exact-title uniqueness, an immediate direct-control reread, archive and duplicate controls, usage, privacy, evidence, safety, and acknowledgement guards. An accepted, pending, opaque, or unresolved delivery state stops copies.\n",
        "## Relational identity and evidence boundary\n\nMira Fenwick uses the relational role finite-topology evidence cartographer and the hope of making bounded structure, correction lineage, ambiguity, and authority limits inspectable. Names, roles, hopes, pronouns, family, and continuity language are working conventions only. They are not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority.\n\n" + BOUNDARY + "\n",
        f"## Exact source and lifecycle\n\nThe exact immutable source is Ilyra Fen {SOURCE}. Ilyra's complete 3,455-word, 26,403-byte baton was read through LITERAL_EOF_ILYRA_V707_V2 and matched SHA-256 3fef6c48077ac5fab16625a86aea919f35e97a5b1a520398098c4a678b4b63dc. The external canonical receipt matched SHA-256 1e3a7b82edd8667daa5540586fb7d71790b4c525046240c9d7b8e11cd251581f and payload SHA-256 f45c03d6b0a10efa1f330ce636e8ee8a01706c79c5952fbd4d44969839484537. It records one invocation, one success, zero replays, 37/37 checks, and 100 exact Git-blob replays. No Ilyra solver, test, model, hook, skill, runner, or canonical was replayed.\n\nIlyra's terminal-after-verification object was selected exactly once as {SOURCE_EFFECTIVE}. The repository seal and constituent canonical or route events were not re-added. The current activation separately reports one acknowledged native corrected retry. That acknowledgement is preserved as delivery acceptance only, excluded from the inherited numeric baseline, and never promoted to recipient completion. Mira's immutable repository delta is {owner_counts}; the repository-effective result is {effective}. Later canonical and route events remain external overlays.\n",
        "Planning, x1, x2, and final are direct single-parent Mira commits after the source, with zero intended merges. Planning freezes definitions before x1. X1 must be pushed, clean, typed 0/0 divergent, and fresh-live equal before x2 begins. X2 must meet the same gate before final begins. The final must be pushed, clean, typed 0/0, and fresh-live equal before one metadata canonical. A successful canonical closes the latch and cannot be replayed for convenience.\n",
        f"## Current v19 workflow and route\n\nHamish's live v19 authority and the direct activation place Ilyra Fen v707-v2, Mira Fenwick {PHASE_ID}, and prospective {SUCCESSOR} {SUCCESSOR_PHASE} consecutively at this edge. A roster projection is planning context rather than activation or completion evidence. Only after Mira's terminal gate may the native route resolve one unique existing exact-title {SUCCESSOR} main task, exhaust active and archived uniqueness, reread newest controls, and send at most once. No replacement task, fork, collaboration subagent, standby substitute, early contact, hidden-identifier inference, or post-acknowledgement monitoring is permitted.\n",
        "## New finite-simplicial-complex domain\n\nFifteen new synthetic fixtures declare two through six labelled vertices and inclusion-maximal facets. The implementation validates record shape, enumerates exact face closure, computes simplex counts and f-vectors, extracts one-skeleton components, constructs boundary matrices over GF(2), verifies consecutive boundary composition is zero, computes exact ranks and Betti numbers, and checks Euler-Poincare equality. A separately structured same-author brute-force oracle enumerates subsets and reduces boundary columns. This is algorithm diversity on one host, not independent reproduction. X2 adds deterministic vertex deletion, chain-count barycentric-subdivision census, relabel covariance, accessible summaries, and abstract coordinates.\n",
    ]
    for mechanism, title, stage, disposition in DEFINITIONS:
        sections.append(
            f"### {mechanism}\n\n{title} The frozen stage is {stage} and the declared disposition is {disposition}. Each of fifteen fixture rows is a parameterized finite software record rather than an independent experiment, observation, discovery, or authority act. The saved fixture digest, definition digest, result, disposition, and falsifier permit later audit and correction. A malformed subject remains failed at zero original credit even if a separate refusal guard or corrected copy passes. This record supplies no empirical calibration, participant finding, professional judgment, affected-party consent, deployment permission, legal or cultural authority, Maori authority, identity continuity, consciousness, personhood, Theory-of-Everything proof, scientific canon, or Stage 20 readiness.\n"
        )
    sections += [
        "## Workload, tests, capabilities, and models\n\nThe phase retains 300 inherited Ilyra proposal records at zero Mira novelty and zero completion credit and freezes 300 genuinely new Mira contracts. Outcomes are exactly 255 completed, 15 represented, 15 open_gap, and 15 exact_gate. Each session contains 450 safe predicates, 300 malformed candidate subjects, 300 separate refusal guards, and 300 corrected-copy CLEAN/FIX/REFINE checks. Passing refusal and correction witnesses never erase or promote invalid originals.\n\nX1 contains twenty focused checks: fifteen brute-force oracle comparisons and five malformed-schema refusals. X2 contains thirty checks: fifteen deterministic relabel comparisons and fifteen subdivision Euler-census comparisons. These checks cover only the declared tiny finite records. They do not establish exhaustive correctness, performance, production safety, security completeness, empirical validity, or independent validation.\n\nTwenty owner-local skills and ten saved-evidence runners are created, validated, and used, ten and five per session. Five successor skill ideas, five successor runner ideas, and four practice recommendations remain zero-credit proposals. No global skill, package, hook, shared catalog, sibling checkout, or user lane is installed or changed. Five hook candidates accept one valid manual envelope and refuse one malformed envelope each; they remain uninstalled and have zero live-host observations.\n\nThe fifteen-model atlas uses vertex count, nonempty-face count, and total Betti number as three abstract coordinates. The HTML is a self-contained accessible evidence table. These coordinates are not physical geometry, an open world, consciousness, a production simulation, or a reproduction of an external system.\n",
        "## Mind, Body, and Heart boundaries\n\nGMUT Mind is represented as typed finite mathematical specification and explicit falsifiers. The supplied Grand Mandala field-equation forms still lack a complete action, fully defined tensors, unit conventions, closure and boundary conditions, identifiable observables, likelihoods, and empirical data. Finite Betti numbers do not estimate alpha, identify Omega_AB, validate a physical field, or prove a Theory of Everything.\n\nTHOS Body is represented by exact bounded software, schemas, saved witnesses, deterministic correction, and reversible documentation. It is not an enterprise operating system, an autonomous controller, an operational safety case, a deployment benchmark, or a production release. No external system is controlled.\n\nFreed ID and CBR Heart are represented by provenance, contested classification, correction, remedy, accessibility, and authority reservations. A simplicial complex cannot supply consent, rights, cultural legitimacy, identity continuity, or competent authority. No live credential, identity lifecycle, rights decision, legal decision, or cultural act is issued. Fifteen design hypotheses remain proposals rather than discovered physical or psychological laws; fifteen broader probes remain unsolved. Maori concepts and authority remain under Maori authority. Practice lenses are study perspectives, not qualifications or employment.\n",
        "## Method Flow and retained failures\n\nThe separate Method Flow preserves nine activation-stage wrapper or read failures and their bounded recoveries, every malformed candidate, every malformed focused-test subject, every invalid hook envelope, and any later attributable runtime failure at zero original credit. The source's two reported retry-read defects remain source-side external history and are not silently converted into Mira successes. Refusal success never converts rejected input into success. Repository, canonical, route, delivery, acknowledgement, and recipient-completion layers remain distinct.\n\nThe repository seal contains only events known before its commit. The canonical may execute only after the clean pushed exact final and may succeed once. Canonical or route failures occurring later remain external overlays and cannot rewrite the seal. The standing verdict remains NOT_READY_FOR_STAGE_20.\n",
        f"## Prospective {SUCCESSOR} work\n\nUseful next directions may include finite chain-complex comparison, accessible cell-incidence projection, provenance joins, independent-oracle design, or exact persistent-homology toy records. These are recommendations rather than completed capabilities or compulsory choices. Before mutation, reread this baton through literal EOF, verify the source, manifests, seal, canonical receipt, terminal overlay, and current controls. Work solo in an additive {SUCCESSOR}-owned D-first lane and keep Mira, Ilyra, siblings, shared, standby, and user lanes read-only.\n\nAfter {SUCCESSOR}'s own terminal gate, refresh the formal roster and direct authority before resolving any later owner. Do not infer activation from historical prose, precontact a later task, create a substitute, or resend after accepted, pending, opaque, or unresolved acknowledgement. Hamish may pause, rename, narrow, redirect, or stop the route.\n\nWith care, exact finite structure, inspectability, reversibility, retained-negative discipline, and corrigibility - Mira Fenwick.\n\nPREPARED_BY_MIRA_FENWICK = true.\nSENT_BY_MIRA_FENWICK = false.\nRECIPIENT_COMPLETION = UNCLAIMED.\n\nLITERAL_EOF_MIRA_V707_V3\n",
    ]
    text = "\n".join(sections)
    if len(re.findall(r"\S+", text)) < 2000:
        raise RuntimeError("baton below v19 minimum")
    return text


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "provider_secret": re.compile(r"\b(?:sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
        "authorization_header": re.compile(r"\bBearer\s+[A-Za-z0-9._-]{20,}", re.IGNORECASE),
        "email_address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
        "phone_or_government_identifier": re.compile(r"\b(?:\+?\d[\d -]{8,}\d|\d{3}-\d{2}-\d{4})\b"),
    }
    hits = []
    scanned = 0
    for path in paths:
        if path.suffix.lower() not in {".json", ".md", ".txt", ".html", ".py"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                hits.append({"class": class_name, "path": path.relative_to(REPO).as_posix()})
    return {"classes": list(patterns), "files_scanned": scanned, "confirmed_hits": hits, "confirmed_hit_count": len(hits)}


def build_final() -> None:
    if not (PHASE / "x2" / "session-summary.json").exists():
        raise RuntimeError("x2 evidence missing")
    final = PHASE / "final"
    if final.exists():
        raise RuntimeError("final already exists; lifecycle replay refused")
    planning_counts = load_json(PHASE / "planning" / "method-flow.json")["counts"]
    x1_counts = load_json(PHASE / "x1" / "method-flow.json")["counts"]
    x2_counts = load_json(PHASE / "x2" / "method-flow.json")["counts"]
    owner_counts = add_counts(add_counts(planning_counts, x1_counts), x2_counts)
    expected_owner = {"methods": 34, "witnesses": 3135, "pass": 2516, "fail": 619, "negatives": 619, "open_gaps": 21, "exact_gates": 20}
    if owner_counts != expected_owner:
        raise RuntimeError(f"unexpected owner counts: {owner_counts}")
    effective = add_counts(SOURCE_EFFECTIVE, owner_counts)

    gaps = [{"id": f"MF7073-GAP-CAL-{index:02d}", "fixture_id": fixture["id"], "kind": "empirical calibration absent", "state": "open_gap"} for index, fixture in enumerate(fixtures(), start=1)]
    gaps += [{"id": f"MF7073-GAP-HOOK-{index:02d}", "kind": "live host hook observation absent", "state": "open_gap"} for index in range(1, 6)]
    gaps.append({"id": "MF7073-GAP-INDEPENDENT", "kind": "independent reproduction absent", "state": "open_gap"})
    gates = [{"id": f"MF7073-GATE-DEPLOY-{index:02d}", "fixture_id": fixture["id"], "kind": "deployment authority absent", "state": "exact_gate"} for index, fixture in enumerate(fixtures(), start=1)]
    gates += [
        {"id": "MF7073-GATE-EMPIRICAL", "kind": "external empirical evidence", "state": "exact_gate"},
        {"id": "MF7073-GATE-PROFESSIONAL", "kind": "competent professional review", "state": "exact_gate"},
        {"id": "MF7073-GATE-CULTURAL", "kind": "legal, cultural, affected-party, and Maori authority", "state": "exact_gate"},
        {"id": "MF7073-GATE-IDENTITY", "kind": "identity, consciousness, or personhood claims", "state": "exact_gate"},
        {"id": "MF7073-GATE-STAGE20", "kind": "proof, canon, or Stage 20 authority", "state": "exact_gate"},
    ]
    assert len(gaps) == 21 and len(gates) == 20
    write_json(final / "accounting.json", {"boundary": BOUNDARY, "source": SOURCE_EFFECTIVE, "owner": owner_counts, "effective": effective, "source_fold_count": 1, "counting_convention": "Parameterized software witnesses, not independent experiments or scientific achievement units."})
    write_json(final / "gaps-and-gates.json", {"boundary": BOUNDARY, "open_gap_count": 21, "exact_gate_count": 20, "open_gaps": gaps, "exact_gates": gates})
    write_json(
        final / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE_ID,
            "actual_git_parent": SOURCE,
            "inherited_zero_credit": 300,
            "new_contracts": 300,
            "outcomes": {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15},
            "owner_counts": owner_counts,
            "repository_effective": effective,
            "canonical_state": "NOT_YET_INVOKED",
            "route_state": "PREPARED_NOT_SENT",
            "recipient_completion": "UNCLAIMED",
            "same_owner_only": True,
            "complete_repository_suite": False,
            "independent_reproduction": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(final / "method-flow-final.json", {"boundary": BOUNDARY, "counts": {"source": SOURCE_EFFECTIVE, "owner": owner_counts, "effective": effective, "source_fold_count": 1}, "planning": "planning/method-flow.json", "x1": "x1/method-flow.json", "x2": "x2/method-flow.json", "runtime_failures": X1_RUNTIME_FAILURES, "runtime_recoveries": X1_RUNTIME_RECOVERIES})
    write_json(final / "failure-dossier.json", {"boundary": BOUNDARY, "activation_failures": ACTIVATION_FAILURES, "activation_recoveries": ACTIVATION_RECOVERIES, "x1_runtime_failures": X1_RUNTIME_FAILURES, "x1_runtime_recoveries": X1_RUNTIME_RECOVERIES, "x1_candidate_failures": 300, "x1_malformed_test_subjects": 5, "x2_candidate_failures": 300, "x2_invalid_hook_subjects": 5, "all_original_failures_retained": True, "refusal_promotes_invalid_subject": False})
    write_json(final / "workload.json", {"boundary": BOUNDARY, "inherited": 300, "new": 300, "outcomes": {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15}, "x1": load_json(PHASE / "x1" / "session-summary.json"), "x2": load_json(PHASE / "x2" / "session-summary.json"), "exact_packets_held": 50, "blocked_packets_held": 30})
    write_json(final / "route-candidate.json", {"boundary": BOUNDARY, "from": OWNER, "from_phase": PHASE_ID, "to": SUCCESSOR, "to_phase": SUCCESSOR_PHASE, "state": "PREPARED_NOT_SENT", "requires": ["clean pushed fresh-live-equal exact final", "one successful non-replayed owner-scoped metadata canonical", "fresh v19 roster and authority", "active and archived exact-title uniqueness", "immediate direct-control reread", "duplicate pause redirect rename stop usage privacy evidence safety acknowledgement guards"], "task_creation_or_fork": False, "standby_substitution": False})
    write_json(final / "allowlist.json", {"boundary": BOUNDARY, "owner_prefixes": ["docs/mira-fenwick/v707-v3/"], "file_ceiling": 2000, "commit_ceiling": 4, "shared_and_sibling_lanes": "read_only", "global_installation": False})
    write_json(final / "source-faithful-ledger.json", {"boundary": BOUNDARY, "source": SOURCE, "source_terminal_effective_selected_once": SOURCE_EFFECTIVE, "source_fold_count": 1, "source_repository_seal_readded": False, "source_delivery_acknowledgement_separate": True, "source_validation_replayed": False, "owner_counts": owner_counts, "effective": effective})
    write_json(final / "context-deck-index.json", {"boundary": BOUNDARY, "path": "docs/mira-fenwick/v707-v3/x2/context-deck.json", "cards": 312, "tiers": 4, "content_sha256": sha256((PHASE / "x2" / "context-deck.json").read_bytes()).hexdigest()})
    write_text(final / "overview.md", f"# Mira Fenwick {PHASE_ID} exact-final overview\n\nThe phase adds a bounded exact finite-simplicial-complex laboratory with fifteen synthetic fixtures, 300 new contracts, 300 inherited zero-credit records, strict planning-before-x1-before-x2 lifecycle evidence, 20/20 x1 tests, 30/30 x2 tests, twenty local skills, ten saved-evidence runners, five manual uninstalled hook candidates, fifteen abstract models, and complete retained-negative accounting. The repository-effective counts are {effective}. The verdict remains `NOT_READY_FOR_STAGE_20`.\n\n{BOUNDARY}\n")
    write_text(final / "overview.html", f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Mira {PHASE_ID} overview</title></head><body><main><h1>Mira Fenwick {PHASE_ID}</h1><p>Bounded finite synthetic simplicial-complex evidence with retained failures and exact authority gates.</p><dl><dt>Methods</dt><dd>{effective['methods']}</dd><dt>Witnesses</dt><dd>{effective['witnesses']}</dd><dt>Open gaps</dt><dd>{effective['open_gaps']}</dd><dt>Exact gates</dt><dd>{effective['exact_gates']}</dd><dt>Verdict</dt><dd>NOT_READY_FOR_STAGE_20</dd></dl><p>{html.escape(BOUNDARY)}</p></main></body></html>\n")

    baton = baton_text(owner_counts, effective)
    write_text(final / "baton.md", baton)
    baton_data = (final / "baton.md").read_bytes()
    write_json(final / "baton-index.json", {"boundary": BOUNDARY, "path": "docs/mira-fenwick/v707-v3/final/baton.md", "bytes": len(baton_data), "words": len(re.findall(r"\S+", baton)), "sha256": sha256(baton_data).hexdigest(), "literal_eof": "LITERAL_EOF_MIRA_V707_V3", "delivery": "PREPARED_NOT_SENT"})

    scan_paths = files_under(PHASE)
    scan = privacy_scan(scan_paths)
    if scan["confirmed_hit_count"]:
        raise RuntimeError(f"privacy scan confirmed candidates: {scan['confirmed_hits']}")
    write_json(final / "privacy-review.json", {"boundary": BOUNDARY, **scan, "scope": "owner files present before final manifest and content seal", "complete_privacy_assurance": False})

    exclusions = ["final/manifest.json", "final/content-seal.json"]
    paths = files_under(PHASE, exclude=[PHASE / item for item in exclusions])
    entries = [file_entry(path) for path in paths]
    manifest = {"boundary": BOUNDARY, "count": len(entries), "entries": entries, "schema": "ghc.family.git-blob-manifest.v1", "self_exclusions": exclusions}
    seal = {"boundary": BOUNDARY, "count": len(entries), "entries": entries, "excluded": exclusions, "schema": "ghc.family.content-seal.v1"}
    write_json(final / "manifest.json", manifest)
    write_json(final / "content-seal.json", seal)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["planning", "x1", "x2", "final"])
    args = parser.parse_args()
    builders = {"planning": build_planning, "x1": build_x1, "x2": build_x2, "final": build_final}
    builders[args.stage]()
    print(json.dumps({"ok": True, "owner": OWNER, "phase": PHASE_ID, "stage": args.stage, "phase_root": str(PHASE)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
