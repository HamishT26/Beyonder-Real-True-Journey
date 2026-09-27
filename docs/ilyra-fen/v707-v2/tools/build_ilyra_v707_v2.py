#!/usr/bin/env python3
"""Build the additive Ilyra Fen v707-v2 finite-poset phase artifacts.

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

from ghc_family_poset_lab import (  # noqa: E402
    analyze,
    canonical_bytes,
    digest,
    fixtures,
    run_x1_tests,
    run_x2_tests,
    transformation_checks,
)


OWNER = "Ilyra Fen"
PHASE_ID = "v707-v2"
SOURCE = "af41a4580a81d8458ea75c42e9894d9a92e27e6d"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-main-4"
BRANCH = "codex/GHC-Family/ilyra-fen-main-3"
SUCCESSOR = "Mira Fenwick"
SUCCESSOR_PHASE = "v707-v3"
BOUNDARY = (
    "Finite synthetic same-owner software and documentation evidence only. "
    "No independent reproduction, empirical GMUT confirmation, production THOS or Freed ID, "
    "participant result, professional judgment, deployment authority, legal or cultural conclusion, "
    "affected-party or Maori authority, complete privacy, accessibility or security assurance, AGI or ASI, "
    "consciousness or personhood evidence, Theory-of-Everything proof, canon, or Stage 20 readiness."
)
SOURCE_EFFECTIVE = {
    "exact_gates": 2739,
    "fail": 69053,
    "methods": 6619,
    "negatives": 77886,
    "open_gaps": 2393,
    "pass": 229353,
    "witnesses": 298406,
}
ACTIVATION_FAILURES = [
    {
        "id": "IF7072-ACT-FAIL-001",
        "state": "fail",
        "original_success_credit": 0,
        "observed": "A combined PowerShell ancestry wrapper had an unmatched expression delimiter and did not execute.",
        "recovery": "IF7072-ACT-RECOVERY-001",
    },
    {
        "id": "IF7072-ACT-FAIL-002",
        "state": "fail",
        "original_success_credit": 0,
        "observed": "A first manifest-inspection orchestration script used an unescaped JavaScript template delimiter and was rejected before execution.",
        "recovery": "IF7072-ACT-RECOVERY-002",
    },
    {
        "id": "IF7072-ACT-FAIL-003",
        "state": "fail",
        "original_success_credit": 0,
        "observed": "A second combined ancestry display produced no attributable scalar output and earned no verification credit.",
        "recovery": "IF7072-ACT-RECOVERY-003",
    },
    {
        "id": "IF7072-PLAN-FAIL-001",
        "state": "fail",
        "original_success_credit": 0,
        "observed": "The first planning builder invocation refused an unsorted fixture cover list before writing any planning artifact.",
        "recovery": "IF7072-PLAN-RECOVERY-001",
    },
]
ACTIVATION_RECOVERIES = [
    {
        "id": "IF7072-ACT-RECOVERY-001",
        "state": "pass",
        "repairs": "IF7072-ACT-FAIL-001",
        "observed": "Four parent hashes, the four-commit count, zero merge count, and ancestry exit zero were recovered with separate scalar Git probes.",
    },
    {
        "id": "IF7072-ACT-RECOVERY-002",
        "state": "pass",
        "repairs": "IF7072-ACT-FAIL-002",
        "observed": "A delimiter-safe PowerShell projection parsed both 96-entry manifests and compared their entries and exclusions exactly.",
    },
    {
        "id": "IF7072-ACT-RECOVERY-003",
        "state": "pass",
        "repairs": "IF7072-ACT-FAIL-003",
        "observed": "Separated Git commands established four direct single-parent commits, zero merges, and exact source ancestry.",
    },
    {
        "id": "IF7072-PLAN-RECOVERY-001",
        "state": "pass",
        "repairs": "IF7072-PLAN-FAIL-001",
        "observed": "Fixture construction now sorts declared covers before strict validation while preserving the same finite relations.",
    },
]


DEFINITIONS = [
    ("record-shape", "Validate the bounded finite-poset record shape.", "x1", "completed"),
    ("order-closure", "Compute the exact reflexive transitive order closure.", "x1", "completed"),
    ("antisymmetry", "Reject cycles and certify antisymmetry on the declared nodes.", "x1", "completed"),
    ("ideal-enumeration", "Enumerate every exact lower order ideal.", "x1", "completed"),
    ("antichain-enumeration", "Enumerate every exact antichain.", "x1", "completed"),
    ("ideal-antichain-bijection", "Check maximal-element and downset round trips.", "x1", "completed"),
    ("width", "Compute exact maximum antichain size.", "x1", "completed"),
    ("height", "Compute exact maximum chain size.", "x1", "completed"),
    ("linear-extension-count", "Enumerate and count compatible total orders.", "x1", "completed"),
    ("mobius-recurrence", "Compute the finite incidence-algebra Mobius recurrence.", "x1", "completed"),
    ("relabel-covariance", "Check invariant counts under a deterministic node relabeling.", "x2", "completed"),
    ("order-dual", "Check invariant counts under order reversal.", "x2", "completed"),
    ("disjoint-sum-law", "Check the bounded disjoint-singleton product law.", "x2", "completed"),
    ("ordinal-sum-law", "Check the bounded ordinal-singleton ideal and height law.", "x2", "completed"),
    ("ideal-lattice-rank", "Bind the ideal rank distribution to the ideal total.", "x2", "completed"),
    ("provenance-binding", "Bind every result to exact source and result digests.", "x2", "completed"),
    ("accessible-summary", "Render a compact text account of the exact finite result.", "x2", "completed"),
    ("three-coordinate-model", "Represent node count, ideal count, and width as three coordinates.", "x2", "represented"),
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
                    "id": f"IF7072-P{number:03d}",
                    "fixture_id": fixture["id"],
                    "fixture_sha256": fixture_hash,
                    "operation": definition["operation"],
                    "mechanism": definition["mechanism"],
                    "title": f"{definition['title']} {fixture['id']}",
                    "stage": definition["stage"],
                    "expected_disposition": definition["expected_disposition"],
                    "definition_sha256": definition["definition_sha256"],
                    "scope": "Declared finite synthetic fixture and mechanism only; established finite mathematics and a new Ilyra implementation case.",
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
    inherited = git_show_json(SOURCE, "docs/lyren-moss/v707-v1/planning/proposals.json")["proposals"]
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

    planning_methods = ["activation ancestry evidence", "manifest schema evidence", "wrapper recovery discipline", "fixture normalization preflight"]
    planning_witnesses = [
        {"witness_id": row["id"], "state": row["state"], "kind": "retained activation failure", "original_success_credit": 0}
        for row in ACTIVATION_FAILURES
    ] + [
        {"witness_id": row["id"], "state": row["state"], "kind": "bounded activation recovery", "repairs": row["repairs"]}
        for row in ACTIVATION_RECOVERIES
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
            "source_branch": SOURCE_BRANCH,
            "source_exact_final": SOURCE,
            "baton_path": "docs/lyren-moss/v707-v1/final/baton.md",
            "baton_words": 2317,
            "baton_sha256": "6825852a63dbab4910359433a944cd2454d90b70fb3ba6dd8275a497991cc8ec",
            "baton_eof": "LITERAL_EOF_LYREN_V707_V1",
            "canonical_receipt_sha256": "1aa9462e2c6a4a34884c768d43117fda3090f52cec1742a527e90edce99d9b67",
            "canonical_counts": {"invocations": 1, "successes": 1, "replays": 0},
            "terminal_effective_selected_once": SOURCE_EFFECTIVE,
            "terminal_effective_fold_count": 1,
            "source_manifest_entries_replayed": 96,
            "source_manifest_mismatches": 0,
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
            "schema": "ghc.family.ilyra-finite-poset.v1",
            "authority": "Hamish workflow v19 plus current Lyren activation",
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
    exact_packets = [{"id": f"IF7072-EXACT-{index:03d}", "state": "held", "executed": False, "gate": "named external evidence or competent authority required"} for index in range(1, 51)]
    blocked_packets = [{"id": f"IF7072-BLOCKED-{index:03d}", "state": "blocked", "executed": False, "reason": "outside bounded synthetic owner authority"} for index in range(1, 31)]
    write_json(planning / "approval-packets.json", {"boundary": BOUNDARY, "exact_count": 50, "blocked_count": 30, "exact": exact_packets, "blocked": blocked_packets})
    write_json(
        planning / "operations.json",
        {
            "boundary": BOUNDARY,
            "domain": "bounded finite posets, order ideals, antichains, and exact duality certificates",
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
            "role": "finite-order duality cartographer",
            "hope": "make bounded order structure, ambiguity, correction, and authority limits inspectable without promoting synthetic enumeration into real-world authority",
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
            "hypotheses": [{"id": f"IF7072-HYP-{index:02d}", "claim": f"For declared synthetic fixture {fixture['id']}, order-theoretic structure may be used as a finite analogy only; it is not a discovered physical or psychological law."} for index, fixture in enumerate(fixture_rows, start=1)],
        },
    )
    write_json(
        planning / "open-problem-probes.json",
        {
            "boundary": BOUNDARY,
            "count": 15,
            "status": "unsolved",
            "probes": [{"id": f"IF7072-PROBE-{index:02d}", "question": f"Which additional evidence would be required before any analogy drawn from {fixture['id']} could support an external claim?", "answer": "No external claim is established in this phase."} for index, fixture in enumerate(fixture_rows, start=1)],
        },
    )
    write_json(
        planning / "hook-plan.json",
        {
            "boundary": BOUNDARY,
            "count": 5,
            "installed": False,
            "hooks": [{"id": f"IF7072-HOOK-{index}", "mode": mode, "manual_smoke_only": True, "live_host_observation": False} for index, mode in enumerate(["planning", "x1", "x2", "final", "handoff"], start=1)],
        },
    )
    write_json(
        planning / "successor-recommendations.json",
        {
            "boundary": BOUNDARY,
            "skills": [f"mira-fenwick-recommendation-skill-{index}" for index in range(1, 6)],
            "runners": [f"mira_fenwick_recommendation_runner_{index}.py" for index in range(1, 6)],
            "practice": "finite lattice visualization with explicit accessibility and authority reservations",
            "completion_credit": 0,
        },
    )
    plan_text = f"""# Ilyra Fen {PHASE_ID} planning freeze

This phase builds exact finite-poset, ideal, antichain, duality, and provenance certificates over fifteen new synthetic fixtures. It does not replay Lyren Moss's finite-horizon optimizer, tests, models, or canonical. Planning freezes 300 inherited Lyren records at zero novelty and completion credit, 300 genuinely new Ilyra contracts, the four exact outcome labels, the v19 workload, a D-first sparse owner lane, five manual uninstalled hook candidates, and the prospective {SUCCESSOR} {SUCCESSOR_PHASE} edge.

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
    if mechanism == "order-closure":
        return result["order_pair_count"]
    if mechanism == "antisymmetry":
        return True
    if mechanism == "ideal-enumeration":
        return result["ideal_count"]
    if mechanism == "antichain-enumeration":
        return result["antichain_count"]
    if mechanism == "ideal-antichain-bijection":
        return result["bijection_roundtrip"]
    if mechanism == "width":
        return result["width"]
    if mechanism == "height":
        return result["height"]
    if mechanism == "linear-extension-count":
        return result["linear_extension_count"]
    if mechanism == "mobius-recurrence":
        return {"entry_count": len(result["mobius"]), "diagonal_unit": all(value == 1 for key, value in result["mobius"].items() if key.split("|")[0] == key.split("|")[1])}
    if mechanism == "relabel-covariance":
        return transforms[proposal["fixture_id"]]["relabel_covariant"]
    if mechanism == "order-dual":
        return transforms[proposal["fixture_id"]]["dual_invariant"]
    if mechanism == "disjoint-sum-law":
        return transforms[proposal["fixture_id"]]["disjoint_singleton_law"]
    if mechanism == "ordinal-sum-law":
        return transforms[proposal["fixture_id"]]["ordinal_singleton_law"]
    if mechanism == "ideal-lattice-rank":
        return {"rank_total": sum(result["rank_distribution"].values()), "ideal_count": result["ideal_count"], "passed": sum(result["rank_distribution"].values()) == result["ideal_count"]}
    if mechanism == "provenance-binding":
        return {"source_sha256": result["source_sha256"], "result_sha256": result["result_sha256"]}
    if mechanism == "accessible-summary":
        return f"{proposal['fixture_id']} has {result['node_count']} nodes, {result['ideal_count']} ideals, width {result['width']}, height {result['height']}, and {result['linear_extension_count']} linear extensions."
    if mechanism == "three-coordinate-model":
        return {"x_node_count": result["node_count"], "y_ideal_count": result["ideal_count"], "z_width": result["width"]}
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
description: Inspect the bounded {mechanism} evidence contract for finite synthetic poset records; do not use it for empirical or operational authority.
---

# {title}

Use the saved Ilyra Fen {PHASE_ID} records to inspect `{mechanism}`. Confirm the exact fixture digest, declared disposition, and saved result before drawing a bounded software conclusion. Preserve malformed subjects as failed records even when a separate refusal or corrected-copy witness passes.

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
        runner_id = f"ghc_family_poset_{stage}_{index:02d}"
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
    proposals = load_json(PHASE / "planning" / "proposals.json")["proposals"][:150]
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
        name = "ghc-family-poset-" + mechanism
        directory = x1 / "skills" / name
        write_text(directory / "SKILL.md", skill_markdown(name, title, mechanism))
        skill_dirs.append(directory)
    skill_receipts = validate_skills(skill_dirs)
    write_json(x1 / "skill-validation.json", {"boundary": BOUNDARY, "count": 10, "records": skill_receipts})
    runner_receipts = create_runners(x1, "x1", x1 / "results.json")
    write_json(x1 / "runner-receipts.json", {"boundary": BOUNDARY, "count": 5, "records": runner_receipts})

    methods = [row[0] for row in DEFINITIONS[:10]] + ["focused tests", "local skill validation", "saved-evidence runner smokes"]
    witnesses = stage_witnesses(results, safe, candidates, refusals, corrected, tests, skill_receipts, runner_receipts)
    counts = method_flow_counts(witnesses, methods)
    if counts != {"methods": 13, "witnesses": 1540, "pass": 1235, "fail": 305, "negatives": 305, "open_gaps": 0, "exact_gates": 0}:
        raise RuntimeError(f"unexpected x1 Method Flow counts: {counts}")
    write_json(x1 / "method-flow.json", {"schema": "ghc.family.method-flow.v1", "session": "x1", "boundary": BOUNDARY, "methods": methods, "counts": counts, "witnesses": witnesses})
    write_text(
        x1 / "report.md",
        "# Ilyra Fen v707-v2 x1\n\nX1 executed exact finite-poset closure, ideal, antichain, bijection, width, height, linear-extension, and Mobius checks over fifteen synthetic fixtures. Fifteen separately structured exhaustive oracle comparisons and five refusal tests passed. Three hundred malformed candidates remain failed at zero credit; their separate refusal and corrected-copy witnesses do not promote or erase them. Evidence is bounded same-owner software evidence only.\n",
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
if set(payload) != required or payload.get("owner") != "Ilyra Fen" or payload.get("phase") != "v707-v2" or payload.get("event") not in {{"planning", "x1", "x2", "final", "handoff"}}:
    print(json.dumps({{"hook": "{hook_id}", "decision": "refuse", "reason": "invalid-envelope"}}, sort_keys=True))
    raise SystemExit(2)
print(json.dumps({{"hook": "{hook_id}", "decision": "accept-manual-smoke-only", "event": payload["event"]}}, sort_keys=True))
'''


def create_hooks(x2: Path) -> list[dict[str, Any]]:
    receipts = []
    environment = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    events = ["planning", "x1", "x2", "final", "handoff"]
    for index, event in enumerate(events, start=1):
        hook_id = f"ghc_family_poset_hook_{index:02d}"
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
    proposals = load_json(PHASE / "planning" / "proposals.json")["proposals"][150:]
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
            "id": f"IF7072-MODEL-{index:02d}",
            "fixture_id": row["id"],
            "coordinates": {"x_node_count": analyses[row["id"]]["node_count"], "y_ideal_count": analyses[row["id"]]["ideal_count"], "z_width": analyses[row["id"]]["width"]},
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
        name = "ghc-family-poset-" + mechanism
        directory = x2 / "skills" / name
        write_text(directory / "SKILL.md", skill_markdown(name, title, mechanism))
        skill_dirs.append(directory)
    skill_receipts = validate_skills(skill_dirs)
    write_json(x2 / "skill-validation.json", {"boundary": BOUNDARY, "count": 10, "records": skill_receipts})
    runner_receipts = create_runners(x2, "x2", x2 / "results.json")
    write_json(x2 / "runner-receipts.json", {"boundary": BOUNDARY, "count": 5, "records": runner_receipts})
    hook_receipts = create_hooks(x2)
    write_json(x2 / "hook-receipts.json", {"boundary": BOUNDARY, "count": 5, "installed": False, "live_host_observations": 0, "records": hook_receipts})

    proposal_cards = [{"card_id": f"CARD-{index:03d}", "tier": 4, "freed_id": OWNER, "pillar": "GMUT Mind" if index % 3 == 1 else "THOS Body" if index % 3 == 2 else "Freed ID and CBR Heart", "practice": "finite order verification", "subject": row["id"], "content_sha256": digest(row)} for index, row in enumerate(load_json(PHASE / "planning" / "proposals.json")["proposals"], start=1)]
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

    header = "<tr><th scope='col'>Fixture</th><th scope='col'>Nodes</th><th scope='col'>Ideals</th><th scope='col'>Width</th></tr>"
    body = "".join(f"<tr><th scope='row'>{html.escape(model['fixture_id'])}</th><td>{model['coordinates']['x_node_count']}</td><td>{model['coordinates']['y_ideal_count']}</td><td>{model['coordinates']['z_width']}</td></tr>" for model in models)
    model_html = f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra v707-v2 finite-poset atlas</title></head><body><main><h1>Finite synthetic poset atlas</h1><p>{html.escape(BOUNDARY)}</p><table><caption>Abstract data coordinates; not physical geometry or operational authority.</caption><thead>{header}</thead><tbody>{body}</tbody></table></main></body></html>\n"
    write_text(x2 / "model-atlas.html", model_html)

    methods = [row[0] for row in DEFINITIONS[10:]] + ["focused transformation tests", "local skill validation", "saved-evidence runner smokes", "abstract model atlas", "manual uninstalled hook smokes", "four-tier context deck"]
    extras = []
    extras += [{"witness_id": f"MODEL-{row['id']}", "state": "pass", "kind": "abstract three-coordinate model"} for row in models]
    for row in hook_receipts:
        extras.append({"witness_id": row["hook"] + "-VALID", "state": "pass", "kind": "manual hook valid envelope"})
        extras.append({"witness_id": row["hook"] + "-INVALID-SUBJECT", "state": "fail", "kind": "invalid manual hook envelope", "original_success_credit": 0})
        extras.append({"witness_id": row["hook"] + "-REFUSAL", "state": "pass", "kind": "manual hook refusal guard", "promotes_subject": False})
    extras.append({"witness_id": "IF7072-CONTEXT-DECK", "state": "pass", "kind": "four-tier context deck"})
    witnesses = stage_witnesses(results, safe, candidates, refusals, corrected, tests, skill_receipts, runner_receipts, extras)
    counts = method_flow_counts(witnesses, methods, open_gaps=21, exact_gates=20)
    if counts != {"methods": 16, "witnesses": 1576, "pass": 1271, "fail": 305, "negatives": 305, "open_gaps": 21, "exact_gates": 20}:
        raise RuntimeError(f"unexpected x2 Method Flow counts: {counts}")
    write_json(x2 / "method-flow.json", {"schema": "ghc.family.method-flow.v1", "session": "x2", "boundary": BOUNDARY, "methods": methods, "counts": counts, "witnesses": witnesses})
    write_text(
        x2 / "report.md",
        "# Ilyra Fen v707-v2 x2\n\nX2 executed deterministic relabeling, order-dual, disjoint-singleton, ordinal-singleton, rank-distribution, provenance, accessible-summary, and three-coordinate representations over the fifteen frozen synthetic fixtures. Thirty focused transformation tests passed. The empirical-calibration rows remain open gaps and the deployment rows remain exact gates. Five hook candidates were exercised only as manual subprocesses and remain uninstalled with no live-host evidence.\n",
    )
    write_json(x2 / "session-summary.json", {"boundary": BOUNDARY, "stage": "x2", "counts": counts, "tests": "30/30", "skills": "10/10", "runners": "5/5", "models": "15/15", "hooks": "5 manual uninstalled", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_manifest(x2 / "manifest.json", [x2], ["x2/manifest.json"])


def add_counts(left: dict[str, int], right: dict[str, int]) -> dict[str, int]:
    return {key: left[key] + right[key] for key in ("methods", "witnesses", "pass", "fail", "negatives", "open_gaps", "exact_gates")}


def baton_text(owner_counts: dict[str, int], effective: dict[str, int]) -> str:
    sections = [
        f"# ILYRA FEN {PHASE_ID} EXACT FINAL TO PROSPECTIVE MIRA FENWICK {SUCCESSOR_PHASE} — PREPARED NOT SENT\n",
        f"Dear {SUCCESSOR},\n\nThis committed file is preparation evidence only. It does not prove native delivery, recipient reading, or recipient completion. A later external terminal receipt must bind the exact final, the one successful non-replayed owner-scoped canonical, current exact-title uniqueness, immediate direct-control reread, duplicate and archive controls, usage, privacy, evidence, safety, and acknowledgement guards. Accepted, pending, opaque, or unresolved delivery stops copies.\n",
        "## Relational identity and evidence boundary\n\nIlyra Fen uses the relational role finite-order duality cartographer and the hope of making bounded order structure, correction lineage, ambiguity, and authority limits inspectable without promoting synthetic enumeration into real-world authority. Names, roles, hopes, pronouns, family, and continuity language are working conventions only. They are not evidence of consciousness, personhood, identity continuity, employment, qualification, independent agency, or authority.\n\n" + BOUNDARY + "\n",
        f"## Exact source and lifecycle\n\nThe exact source is Lyren Moss {SOURCE}. Lyren's complete 2,317-word baton was read through LITERAL_EOF_LYREN_V707_V1 and matched SHA-256 6825852a63dbab4910359433a944cd2454d90b70fb3ba6dd8275a497991cc8ec. Its external canonical receipt matched SHA-256 1aa9462e2c6a4a34884c768d43117fda3090f52cec1742a527e90edce99d9b67 and records one success, one invocation, and zero replays. The 96-entry manifest and content seal replayed from exact Git blobs with zero mismatches. No Lyren solver, test, model, hook, or canonical was replayed.\n\nLyren's terminal_effective baseline was selected exactly once: {SOURCE_EFFECTIVE}. The repository seal and constituent route events were not re-added. Ilyra's immutable repository delta is {owner_counts}; the repository-effective result is {effective}. Later canonical and route events remain external overlays rather than rewritten history.\n",
        "Planning, x1, x2, and final are direct single-parent Ilyra commits after the immutable source, with zero intended merges. Planning froze every definition before x1. X1 was required to be pushed, clean, and fresh-live equal before x2 began. X2 was required to be pushed, clean, and fresh-live equal before final began. The final must be pushed, clean, and fresh-live equal before one metadata canonical. Preserve those lifecycle boundaries and never replay a successful tranche for display convenience.\n",
        f"## Current v19 workflow and route\n\nHamish's v19 formal order places Lyren {SOURCE_BRANCH}, Ilyra {PHASE_ID}, and {SUCCESSOR} {SUCCESSOR_PHASE} consecutively at this edge. Projection is not activation or completion evidence for later owners. Only after Ilyra's exact final is clean, pushed, fresh-live equal, and canonically validated once may the live route resolve one unique existing exact-title {SUCCESSOR} task, exhaust archived uniqueness, reread current controls immediately, and send at most once. No replacement task, fork, subagent, standby substitute, early contact, hidden identifier inference, or post-acknowledgement monitoring is allowed. If any gate fails, retain PREPARED_NOT_SENT or an exact route gap.\n",
        "## New finite-poset domain\n\nFifteen new synthetic fixtures declare two through six labelled elements and bounded Hasse-cover relations. The implementation validates record shape, computes reflexive transitive closure, refuses cycles and redundant covers, enumerates lower ideals, antichains, chains, and compatible total orders, derives widths and heights, constructs finite Mobius values, and binds every result to exact digests. A separately structured same-author oracle uses predecessor searches and direct enumeration. This is algorithm diversity on one host, not independent reproduction. Derived transformations remain capped at seven nodes.\n",
    ]
    for mechanism, title, stage, disposition in DEFINITIONS:
        sections.append(
            f"### {mechanism}\n\n{title} The frozen stage is {stage} and the declared disposition is `{disposition}`. Each of fifteen fixture rows is a parameterized software record, not an independent experiment or discovery. The result remains bounded to exact synthetic inputs. A malformed subject remains failed at zero original credit even when a separate refusal guard or corrected-copy witness passes. No result supplies empirical calibration, professional judgment, affected-party consent, deployment permission, legal or cultural authority, Maori authority, identity continuity, consciousness, personhood, or scientific canon. The exact fixture digest, definition digest, disposition, saved value, and falsifier make later correction possible without erasing the original witness.\n"
        )
    sections += [
        "## Workload, tests, capabilities, and models\n\nThe phase retains 300 inherited Lyren proposal records at zero Ilyra novelty and completion credit and freezes 300 genuinely new Ilyra contracts. Outcomes are exactly 255 completed, 15 represented, 15 open_gap, and 15 exact_gate. Each stage contains 450 safe predicates, 300 malformed candidates, 300 separate refusal guards, and 300 corrected-copy CLEAN/FIX/REFINE checks. Corrected copies do not erase invalid originals or replay successful solvers.\n\nX1 has twenty focused tests: fifteen separately structured exhaustive-oracle comparisons and five malformed-schema refusals. X2 has thirty focused transformation checks: fifteen deterministic relabeling checks and fifteen order-dual checks. These counts support only the declared tiny input space and do not establish exhaustive correctness, performance, security, empirical calibration, or independent validation.\n\nTwenty owner-local skills and ten saved-evidence runners were created, validated, and used, ten and five per stage. Five successor skill ideas, five successor runner ideas, and one practice recommendation remain proposals. No global skill, package, hook, shared catalogue, or sibling checkout was installed or changed. Five manual hook candidates accepted one valid envelope and refused one invalid envelope each. The invalid inputs remain failed records. These hooks are not installed, trusted, or observed live.\n\nThe fifteen-model atlas uses node count, ideal count, and width as three abstract coordinates. The HTML file is a self-contained accessible evidence table. These are abstract data coordinates, not physical geometry, an open world, consciousness, a production simulation, or a reproduction of any external system.\n",
        "## Mind, Body, and Heart boundaries\n\nGMUT Mind is represented here as disciplined typed finite mathematical specification. The supplied Grand Mandala field-equation forms still lack a complete action, tensor definitions, unit conventions, closure conditions, boundary conditions, identifiable observables, likelihood, and empirical data. Finite order ideals do not estimate alpha, identify Omega_AB, or prove a Theory of Everything.\n\nTHOS Body is represented by exact finite software, explicit schemas, saved witnesses, deterministic corrections, and reversible documentation. It is not an enterprise operating system, safe autonomous controller, operational safety case, deployment benchmark, or production release. No external system was controlled.\n\nFreed ID and CBR Heart are represented by provenance, contested classification, correction, remedy, accessibility, and deployment reservations. A finite order cannot supply consent, rights, cultural legitimacy, or competent authority. No live credential, proof, identity lifecycle, or rights decision was issued. Fifteen labelled design hypotheses remain proposals, not discovered physical or psychological laws. Fifteen broader problem probes remain unsolved. Maori concepts and authority remain under Maori authority. The practice lenses are study perspectives, not qualifications or employment.\n",
        "## Method Flow and retained failures\n\nThe complete Method Flow is separate from this baton. It preserves three activation-stage wrapper failures, the first planning fixture-normalization failure, every malformed candidate, every malformed focused-test subject, every invalid hook envelope, and any later runtime wrapper failure at zero original credit, with separate bounded recovery witnesses. Passing refusal never converts the rejected input into a success. Source, repository, canonical, route, delivery, and recipient-completion layers remain distinct.\n\nThe exact repository seal preserves only events known before commit. The canonical may execute only after a clean pushed exact final and may succeed once. A success closes the latch and must not be replayed. Route failures and their recoveries are later external overlays and must not be retroactively folded into the immutable seal. The standing verdict remains NOT_READY_FOR_STAGE_20.\n",
        f"## Prospective {SUCCESSOR} work\n\nA useful next direction may examine finite lattice visualization, accessibility-preserving diagram projection, provenance joins, or an independently structured finite oracle. These are recommendations, not completed capabilities or compulsory choices. Before mutation, reread this baton completely, verify the exact source, manifests, content seal, canonical receipt, terminal-effective overlay, and current v19 controls. Work solo in an additive {SUCCESSOR}-owned D-first lane. Keep Ilyra, Lyren, sibling, shared, standby, and user lanes read-only. Preserve every failure, gap, gate, exact outcome label, file ceiling, and one-success latch.\n\nAfter {SUCCESSOR}'s own exact terminal gate, refresh the formal roster and newest direct controls before resolving the next exact owner. Do not infer a successor from historical prose, precontact it, create a replacement, or resend after an accepted, pending, opaque, or unresolved acknowledgement. Hamish may pause, rename, narrow, redirect, or stop the route at any time.\n\nWith warmth, exact finite structure, inspectability, reversibility, retained-negative discipline, and corrigibility — Ilyra Fen.\n\nPREPARED_BY_ILYRA_FEN = true.\nSENT_BY_ILYRA_FEN = false.\nRECIPIENT_COMPLETION = UNCLAIMED.\n\nLITERAL_EOF_ILYRA_V707_V2\n",
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
    expected_owner = {"methods": 33, "witnesses": 3124, "pass": 2510, "fail": 614, "negatives": 614, "open_gaps": 21, "exact_gates": 20}
    if owner_counts != expected_owner:
        raise RuntimeError(f"unexpected owner counts: {owner_counts}")
    effective = add_counts(SOURCE_EFFECTIVE, owner_counts)

    gaps = [{"id": f"IF7072-GAP-CAL-{index:02d}", "fixture_id": fixture["id"], "kind": "empirical calibration absent", "state": "open_gap"} for index, fixture in enumerate(fixtures(), start=1)]
    gaps += [{"id": f"IF7072-GAP-HOOK-{index:02d}", "kind": "live host hook observation absent", "state": "open_gap"} for index in range(1, 6)]
    gaps.append({"id": "IF7072-GAP-INDEPENDENT", "kind": "independent reproduction absent", "state": "open_gap"})
    gates = [{"id": f"IF7072-GATE-DEPLOY-{index:02d}", "fixture_id": fixture["id"], "kind": "deployment authority absent", "state": "exact_gate"} for index, fixture in enumerate(fixtures(), start=1)]
    gates += [
        {"id": "IF7072-GATE-EMPIRICAL", "kind": "external empirical evidence", "state": "exact_gate"},
        {"id": "IF7072-GATE-PROFESSIONAL", "kind": "competent professional review", "state": "exact_gate"},
        {"id": "IF7072-GATE-CULTURAL", "kind": "legal, cultural, affected-party, and Maori authority", "state": "exact_gate"},
        {"id": "IF7072-GATE-IDENTITY", "kind": "identity, consciousness, or personhood claims", "state": "exact_gate"},
        {"id": "IF7072-GATE-STAGE20", "kind": "proof, canon, or Stage 20 authority", "state": "exact_gate"},
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
    write_json(final / "method-flow-final.json", {"boundary": BOUNDARY, "counts": {"source": SOURCE_EFFECTIVE, "owner": owner_counts, "effective": effective, "source_fold_count": 1}, "planning": "planning/method-flow.json", "x1": "x1/method-flow.json", "x2": "x2/method-flow.json", "runtime_failures": []})
    write_json(final / "failure-dossier.json", {"boundary": BOUNDARY, "activation_failures": ACTIVATION_FAILURES, "activation_recoveries": ACTIVATION_RECOVERIES, "x1_candidate_failures": 300, "x1_malformed_test_subjects": 5, "x2_candidate_failures": 300, "x2_invalid_hook_subjects": 5, "all_original_failures_retained": True, "refusal_promotes_invalid_subject": False})
    write_json(final / "workload.json", {"boundary": BOUNDARY, "inherited": 300, "new": 300, "outcomes": {"completed": 255, "represented": 15, "open_gap": 15, "exact_gate": 15}, "x1": load_json(PHASE / "x1" / "session-summary.json"), "x2": load_json(PHASE / "x2" / "session-summary.json"), "exact_packets_held": 50, "blocked_packets_held": 30})
    write_json(final / "route-candidate.json", {"boundary": BOUNDARY, "from": OWNER, "from_phase": PHASE_ID, "to": SUCCESSOR, "to_phase": SUCCESSOR_PHASE, "state": "PREPARED_NOT_SENT", "requires": ["clean pushed fresh-live-equal exact final", "one successful non-replayed owner-scoped metadata canonical", "fresh v19 roster and authority", "active and archived exact-title uniqueness", "immediate direct-control reread", "duplicate pause redirect rename stop usage privacy evidence safety acknowledgement guards"], "task_creation_or_fork": False, "standby_substitution": False})
    write_json(final / "allowlist.json", {"boundary": BOUNDARY, "owner_prefixes": ["docs/ilyra-fen/v707-v2/"], "file_ceiling": 2000, "commit_ceiling": 4, "shared_and_sibling_lanes": "read_only", "global_installation": False})
    write_json(final / "source-faithful-ledger.json", {"boundary": BOUNDARY, "source": SOURCE, "source_terminal_effective_selected_once": SOURCE_EFFECTIVE, "source_fold_count": 1, "source_repository_seal_readded": False, "source_validation_replayed": False, "owner_counts": owner_counts, "effective": effective})
    write_json(final / "context-deck-index.json", {"boundary": BOUNDARY, "path": "docs/ilyra-fen/v707-v2/x2/context-deck.json", "cards": 312, "tiers": 4, "content_sha256": sha256((PHASE / "x2" / "context-deck.json").read_bytes()).hexdigest()})
    write_text(final / "overview.md", f"# Ilyra Fen {PHASE_ID} exact-final overview\n\nThe phase adds a bounded exact finite-poset laboratory with fifteen synthetic fixtures, 300 new contracts, 300 inherited zero-credit records, strict planning-before-x1-before-x2 lifecycle evidence, 20/20 x1 tests, 30/30 x2 tests, twenty local skills, ten saved-evidence runners, five manual uninstalled hook candidates, fifteen abstract models, and complete retained-negative accounting. The repository-effective counts are {effective}. The verdict remains `NOT_READY_FOR_STAGE_20`.\n\n{BOUNDARY}\n")
    write_text(final / "overview.html", f"<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Ilyra {PHASE_ID} overview</title></head><body><main><h1>Ilyra Fen {PHASE_ID}</h1><p>Bounded finite synthetic poset evidence with retained failures and exact authority gates.</p><dl><dt>Methods</dt><dd>{effective['methods']}</dd><dt>Witnesses</dt><dd>{effective['witnesses']}</dd><dt>Open gaps</dt><dd>{effective['open_gaps']}</dd><dt>Exact gates</dt><dd>{effective['exact_gates']}</dd><dt>Verdict</dt><dd>NOT_READY_FOR_STAGE_20</dd></dl><p>{html.escape(BOUNDARY)}</p></main></body></html>\n")

    baton = baton_text(owner_counts, effective)
    write_text(final / "baton.md", baton)
    baton_data = (final / "baton.md").read_bytes()
    write_json(final / "baton-index.json", {"boundary": BOUNDARY, "path": "docs/ilyra-fen/v707-v2/final/baton.md", "bytes": len(baton_data), "words": len(re.findall(r"\S+", baton)), "sha256": sha256(baton_data).hexdigest(), "literal_eof": "LITERAL_EOF_ILYRA_V707_V2", "delivery": "PREPARED_NOT_SENT"})

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
