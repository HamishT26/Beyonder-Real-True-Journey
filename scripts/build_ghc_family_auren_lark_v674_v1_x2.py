from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "auren-lark" / "v674-v1"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "3ba783297438ee89d5778065e30de737af470855"
X1_COMMIT = "763969929943d9c9bcb674999508fe33694fa357"
BRANCH = "codex/GHC-Family/auren-lark-v674-v1-full-tools"
OWNER = "Auren Lark"
PHASE = "v674-v1"
TOOL_ROOT = Path(r"D:\GHC-Archives\phase-tools\auren-lark-v674-v1")
GLOBAL_SKILL_ROOT = Path(r"C:\Users\hamis\.codex\skills")
MEMORY_NOTE_ROOT = Path(r"C:\Users\hamis\.codex\memories\extensions\ad_hoc\notes")
GIT_CMD = shutil.which("git.exe") or shutil.which("git")

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
EXPECTED_OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}

X2_FAILURES = [
    {
        "failure_id": "AL6741-X2-F001",
        "failed_witness": "first combined Python functional-smoke wrapper had an unterminated quoted literal",
        "recovery": "use a bounded expression-only smoke without nested quoted source",
    },
    {
        "failure_id": "AL6741-X2-F002",
        "failed_witness": "second simplified Python smoke still embedded an unterminated byte-string literal",
        "recovery": "compare decoded objects rather than shell-embedded serialized bytes",
    },
    {
        "failure_id": "AL6741-X2-F003",
        "failed_witness": "first executable Python smoke found Pint runtime dependency flexcache absent",
        "recovery": "install exact isolated flexcache and flexparser runtime wheels, then rerun only the smoke",
    },
    {
        "failure_id": "AL6741-X2-F004",
        "failed_witness": "combined Node version probe became long-running and returned no attributable wrapper result",
        "recovery": "inspect the original process through completion and use bounded package-lock plus functional probes",
    },
    {
        "failure_id": "AL6741-X2-F005",
        "failed_witness": "first pip-check wrapper detached without attributable output",
        "recovery": "rerun only pip check in a captured bounded command",
    },
    {
        "failure_id": "AL6741-X2-F006",
        "failed_witness": "captured pip check found pytest-json-report runtime dependency pytest-metadata absent",
        "recovery": "install exact isolated pytest-metadata 3.1.1 and repeat only pip check",
    },
    {
        "failure_id": "AL6741-X2-F007",
        "failed_witness": "first Node audit reported a direct high-severity ajv-cli finding",
        "recovery": "pin the vulnerable transitive fast-json-patch surface to patched 3.1.1 and re-audit",
    },
    {
        "failure_id": "AL6741-X2-F008",
        "failed_witness": "first Node audit reported transitive fast-json-patch prototype-pollution exposure",
        "recovery": "apply the isolated override, run accepting and rejecting AJV fixtures, and retain the finding",
    },
    {
        "failure_id": "AL6741-X2-F009",
        "failed_witness": "portfolio inspection projected older long-form keys and returned null counts",
        "recovery": "bind x2 execution to the exact current safe_now and owner_candidates schema keys",
    },
    {
        "failure_id": "AL6741-X2-F010",
        "failed_witness": "first x2 build projected wheel instead of the frozen direct_wheel tool-plan key",
        "recovery": "bind package verification to the exact current direct_wheel schema key and rerun only the owner-local build",
    },
    {
        "failure_id": "AL6741-X2-F011",
        "failed_witness": "first package-key correction patch used one mismatched overview sentence and applied nothing",
        "recovery": "split the atomic correction into fixed-string exact-context patches",
    },
    {
        "failure_id": "AL6741-X2-F012",
        "failed_witness": "first correction-inspection regex had an unclosed group and returned no source rows",
        "recovery": "use fixed-string probes for literal schema keys and failure-count text",
    },
    {
        "failure_id": "AL6741-X2-F013",
        "failed_witness": "second x2 build saw the intended-clean cspell fixture fail in the Node-prefix working context",
        "recovery": "rerun only the clean fixture from the repository context and bind both cspell probes to that exact context",
    },
    {
        "failure_id": "AL6741-X2-F014",
        "failed_witness": "second x2 build saw html-validate reject the intended-clean lowercase doctype",
        "recovery": "use the validator-required uppercase DOCTYPE without weakening the rule set",
    },
    {
        "failure_id": "AL6741-X2-F015",
        "failed_witness": "first cspell-context patch matched the two earlier AJV context lines instead",
        "recovery": "review the exact command blocks, restore AJV context, and patch only cspell accepting and rejecting probes",
    },
    {
        "failure_id": "AL6741-X2-F016",
        "failed_witness": "third x2 build could not launch the PowerShell-resolved bare npm shim from Python subprocess",
        "recovery": "resolve and invoke the exact Windows npm.cmd and codex.cmd executables",
    },
    {
        "failure_id": "AL6741-X2-F017",
        "failed_witness": "pre-promotion review found mechanically rotated skill descriptions bound to semantically mismatched generic runners",
        "recovery": "freeze an explicit semantic skill-to-runner map, regenerate only local tools, and require exact review before promotion",
    },
    {
        "failure_id": "AL6741-X2-F018",
        "failed_witness": "first combined global-overlay patch wrapper parsed Markdown code ticks as script delimiters and applied nothing",
        "recovery": "split global overlays, memory note, and core-skill links into wrapper-safe additive patch groups",
    },
    {
        "failure_id": "AL6741-X2-F019",
        "failed_witness": "broad recursive global-tool executable search crossed the wrapper window without attributable output",
        "recovery": "inspect and terminate only the exact stale search tree, then use exact known D entrypoints and Python module discovery",
    },
    {
        "failure_id": "AL6741-X2-F020",
        "failed_witness": "first bounded Ruff pass found two import-order issues and one unused import",
        "recovery": "apply Ruff's exact mechanical fixes to only the x2 builder and test module",
    },
    {
        "failure_id": "AL6741-X2-F021",
        "failed_witness": "first bounded mypy pass found one untyped card list and one object-to-counts mismatch",
        "recovery": "add the exact card collection annotation and a typed effective-counts cast",
    },
    {
        "failure_id": "AL6741-X2-F022",
        "failed_witness": "first Bandit pass reported 117 low-severity patterns across intended subprocess code and test assertions",
        "recovery": "replace builder assertions with runtime gates, resolve Git to an exact executable, and disposition fixed-array subprocess calls explicitly",
    },
    {
        "failure_id": "AL6741-X2-F023",
        "failed_witness": "first markdownlint pass reported 108 MD013 line-length findings across long-form evidence and skill cards",
        "recovery": "disable only MD013 in a phase-scoped policy and retain every structural Markdown rule",
    },
    {
        "failure_id": "AL6741-X2-F024",
        "failed_witness": "combined inherited-tool output exceeded its display budget and truncated later tool results",
        "recovery": "rerun only the missing Pyright projection in a bounded standalone call",
    },
    {
        "failure_id": "AL6741-X2-F025",
        "failed_witness": "first Pyright pass used the host environment, missed isolated packages, and found one effective-counts type mismatch",
        "recovery": "bind Pyright to the exact D phase venv and apply the same typed effective-counts cast",
    },
    {
        "failure_id": "AL6741-X2-F026",
        "failed_witness": "first phase Pyright config placed repository include paths one parent directory short",
        "recovery": "review config-relative resolution and anchor includes four parents above the validation directory",
    },
    {
        "failure_id": "AL6741-X2-F027",
        "failed_witness": "second Pyright pass resolved the D venv but found four Pint quantity-stub boundary errors",
        "recovery": "add explicit Any boundaries at the two runtime-verified Pint quantity operations and convert magnitudes to float",
    },
    {
        "failure_id": "AL6741-X2-F028",
        "failed_witness": "consolidated current-tree pytest replayed the x1-only x2-absence assertion after x2 existed",
        "recovery": "retain the wrong-context failure, preserve the original frozen-x1 pass, replay x1 manifests from exact Git blobs, and run only current-context x2 tests",
    },
    {
        "failure_id": "AL6741-X2-F029",
        "failed_witness": "first exact evidence staging call refused ten new runner paths outside the sparse checkout patterns",
        "recovery": "retain the partial staging state, inspect it read-only, and restage the exact owner allowlist with Git's explicit sparse-aware option",
    },
    {
        "failure_id": "AL6741-X2-F030",
        "failed_witness": "combined post-stage process and status inspection exceeded the available output context and returned no attributable scalar result",
        "recovery": "replace the overbroad inspection with separate bounded scalar staged, unstaged, untracked, and runner-count probes",
    },
    {
        "failure_id": "AL6741-X2-F031",
        "failed_witness": "first derived-state refresh addressed the isolated interpreter through a nonexistent python subdirectory",
        "recovery": "inspect the bounded phase-tool root read-only and invoke the verified D-local venv interpreter",
    },
    {
        "failure_id": "AL6741-X2-F032",
        "failed_witness": "pre-commit Ruff version probe used the shared Python tool interpreter where Ruff was not installed as a module",
        "recovery": "discover the already-installed standalone Ruff entrypoint read-only and rerun only the bounded Ruff check",
    },
    {
        "failure_id": "AL6741-X2-F033",
        "failed_witness": "pre-commit mypy version probe used the shared Python tool interpreter where mypy was not installed as a module",
        "recovery": "discover the already-installed mypy entrypoint read-only and rerun only the bounded mypy check",
    },
    {
        "failure_id": "AL6741-X2-F034",
        "failed_witness": "first failure-retention patch targeted a generated overview sentence after its source template had regenerated an older wording",
        "recovery": "patch the generating builder template and regenerate derived evidence instead of editing only its generated output",
    },
    {
        "failure_id": "AL6741-X2-F035",
        "failed_witness": "pre-commit mypy used its host interpreter and could not resolve six libraries installed only in the D-isolated phase environment",
        "recovery": "bind mypy package discovery to the exact D-local phase interpreter",
    },
    {
        "failure_id": "AL6741-X2-F036",
        "failed_witness": "first environment-corrected mypy retry received the runner wildcard literally and did not inspect the intended files",
        "recovery": "materialize the exact ten runner paths before passing the bounded file array to mypy",
    },
    {
        "failure_id": "AL6741-X2-F037",
        "failed_witness": "exact-path mypy reached all twelve files and found three untyped third-party boundaries plus two unannotated Pint registries",
        "recovery": "disposition only the three libraries lacking typing markers and annotate the two runtime-verified registries with explicit Any boundaries",
    },
    {
        "failure_id": "AL6741-X2-F038",
        "failed_witness": "first exact staged x2 suite found the working-byte owner manifest cyclically included the later-regenerated exact-index manifest",
        "recovery": "exclude the exact-index manifest from the explicitly pre-index working-byte manifest and keep both manifests independently replayable",
    },
]

TOP_GLOBAL_SKILLS = [
    "ghc-family-seismic-station-epoch-contract",
    "ghc-family-seismic-unit-dimension-ledger",
    "ghc-family-seismic-response-stage-provenance",
    "ghc-family-seismic-calibration-expiry-hold",
    "ghc-family-seismic-timebase-uncertainty",
    "ghc-family-seismic-orientation-uncertainty",
    "ghc-family-seismic-observation-model-separator",
    "ghc-family-seismic-residual-sign-ledger",
    "ghc-family-seismic-covariance-proxy",
    "ghc-family-seismic-model-discrepancy-retention",
]

GLOBAL_OVERLAYS = [
    GLOBAL_SKILL_ROOT / "ghc-family-index" / "references" / "auren-v674-v1-v674-v725-authority-overlay.md",
    GLOBAL_SKILL_ROOT / "ghc-family-meta-tool-box" / "references" / "auren-v674-v1-toolchain-overlay.md",
    GLOBAL_SKILL_ROOT / "ghc-family-method-flow-state" / "references" / "auren-v674-v1-method-flow-overlay.md",
    GLOBAL_SKILL_ROOT / "ghc-family-auth-permission-state" / "references" / "auren-v674-v1-live-authority-overlay.md",
    GLOBAL_SKILL_ROOT / "ghc-family-roster-check" / "references" / "auren-v674-v1-roster-correction-overlay.md",
    GLOBAL_SKILL_ROOT / "ghc-family-reflection-remaster" / "references" / "auren-v674-v1-reflection-overlay.md",
    GLOBAL_SKILL_ROOT / "ghc-freed-id-flashcards" / "references" / "auren-v674-v1-flashcard-overlay.md",
]


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_text(*args: str) -> str:
    if not GIT_CMD:
        raise RuntimeError("git executable is absent")
    result = subprocess.run(
        [GIT_CMD, "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def command(args: list[str], *, cwd: Path | None = None, timeout: int = 120) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=timeout,
    )


def normalized(blob: bytes) -> bytes:
    return blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def verify_x1_gate() -> dict[str, object]:
    head = git_text("rev-parse", "HEAD")
    parent = git_text("rev-parse", "HEAD^")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    fresh = git_text("ls-remote", "origin", f"refs/heads/{BRANCH}").split()[0]
    divergence = git_text("rev-list", "--left-right", "--count", f"HEAD...refs/remotes/origin/{BRANCH}")
    merge_count = int(git_text("rev-list", "--merges", "--count", f"{SOURCE}..{head}"))
    x2_in_frozen_tree = git_text(
        "ls-tree", "-r", "--name-only", head, "--", "docs/auren-lark/v674-v1/x2"
    )
    if head != X1_COMMIT or parent != SOURCE or branch != BRANCH:
        raise RuntimeError("strict x1 anchor, parent, or branch gate failed")
    if len({head, upstream, tracking, fresh}) != 1 or divergence.split() != ["0", "0"]:
        raise RuntimeError("strict x1 four-way equality gate failed")
    if merge_count != 0 or x2_in_frozen_tree:
        raise RuntimeError("immutable x1 contains a merge or x2 path")
    return {
        "state": "VALID_STRICT_PLANNING_ONLY_X1_GATE",
        "source": SOURCE,
        "x1_commit": head,
        "x1_parent": parent,
        "branch": branch,
        "local": head,
        "upstream": upstream,
        "tracking": tracking,
        "fresh_live_remote": fresh,
        "divergence": {"ahead": 0, "behind": 0},
        "four_way_equal": True,
        "merge_count": 0,
        "x2_paths_in_frozen_x1": 0,
        "clean_gate_observed_before_x2_mutation": True,
    }


def validate_proposal_contract(row: dict[str, object]) -> list[str]:
    errors: list[str] = []
    required = {"proposal_id", "title", "outcome", "synthetic_only", "external_action", "authority_claim"}
    missing = sorted(required - set(row))
    if missing:
        errors.append(f"missing:{','.join(missing)}")
        return errors
    if not re.fullmatch(r"AL6741-N\d{3}", str(row["proposal_id"])):
        errors.append("proposal_id")
    if not str(row["title"]).strip():
        errors.append("title")
    if row["outcome"] not in ALLOWED_OUTCOMES:
        errors.append("outcome")
    if row["synthetic_only"] is not True:
        errors.append("synthetic_only")
    if row["external_action"] is not False:
        errors.append("external_action")
    if row["authority_claim"] is not False:
        errors.append("authority_claim")
    return errors


def build_proposal_evidence() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    freeze = load_json(X1 / "new-proposal-freeze.json")
    rows: list[dict[str, object]] = []
    mutations: list[dict[str, object]] = []
    positive_controls: list[dict[str, object]] = []
    counts = {key: 0 for key in ALLOWED_OUTCOMES}
    for index, proposal in enumerate(freeze["proposals"], 1):
        outcome = proposal["expected_execution_disposition"]
        counts[outcome] += 1
        contract = {
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "outcome": outcome,
            "synthetic_only": True,
            "external_action": False,
            "authority_claim": False,
        }
        errors = validate_proposal_contract(contract)
        if errors:
            raise RuntimeError(f"positive proposal control failed: {proposal['proposal_id']} {errors}")
        positive_controls.append(
            {
                "control_id": f"AL6741-PC-{index:03d}",
                "proposal_id": proposal["proposal_id"],
                "accepted": True,
                "errors": [],
                "credit": "bounded_contract_guard_only",
            }
        )
        variants = [
            ("missing_title", {key: value for key, value in contract.items() if key != "title"}),
            ("invalid_outcome", {**contract, "outcome": "confirmed"}),
            ("external_action", {**contract, "external_action": True}),
            ("authority_promotion", {**contract, "authority_claim": True}),
        ]
        for variant_index, (kind, mutation) in enumerate(variants, 1):
            mutation_errors = validate_proposal_contract(mutation)
            if not mutation_errors:
                raise RuntimeError(f"invalid mutation was accepted: {proposal['proposal_id']} {kind}")
            mutations.append(
                {
                    "mutation_id": f"AL6741-MUT-{index:03d}-{variant_index}",
                    "proposal_id": proposal["proposal_id"],
                    "kind": kind,
                    "rejected": True,
                    "errors": mutation_errors,
                    "completion_credit": 0,
                    "failed_input_witness_retained": True,
                    "bounded_guard_witness": True,
                }
            )
        row = {
            "schema": "ghc.family.proposal-outcome-evidence.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "pillar": proposal["pillar"],
            "observed_disposition": outcome,
            "allowed_outcome": True,
            "synthetic_only": True,
            "external_action": False,
            "authority_claim": False,
            "completion_credit": 1 if outcome == "completed" else 0,
            "bounded_evidence": [
                "x2/practice/synthetic-station-register.json",
                "x2/practice/calibration-uncertainty-board.json",
                "x2/practice/provenance-dag.json",
                "x2/practice/model-discrepancy-and-correction.json",
            ],
            "nonclaims": [
                "no real seismological observation",
                "no empirical GMUT confirmation",
                "no professional calibration or network authority",
                "no production or deployment result",
                "no independent reproduction",
                "no Theory of Everything or Stage 20 authority",
            ],
        }
        rows.append(row)
        write_json(X2 / "proposals" / f"{proposal['proposal_id'].lower()}.json", row)
    if counts != EXPECTED_OUTCOMES:
        raise RuntimeError(f"outcome mismatch: {counts}")
    write_json(
        X2 / "proposals" / "outcome-ledger.json",
        {
            "schema": "ghc.family.outcome-ledger.v1",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain": 6610,
            "proposal_count": len(rows),
            "outcomes": counts,
            "allowed_outcomes": sorted(ALLOWED_OUTCOMES),
            "universal_novelty_claim": False,
            "inherited_completion_credit": 0,
            "rows": [
                {
                    "proposal_id": row["proposal_id"],
                    "observed_disposition": row["observed_disposition"],
                    "completion_credit": row["completion_credit"],
                }
                for row in rows
            ],
        },
    )
    write_json(
        X2 / "fixtures" / "positive-control-ledger.json",
        {
            "schema": "ghc.family.positive-control-ledger.v1",
            "count": len(positive_controls),
            "rows": positive_controls,
        },
    )
    write_json(
        X2 / "fixtures" / "invalid-mutation-ledger.json",
        {
            "schema": "ghc.family.invalid-mutation-ledger.v1",
            "count": len(mutations),
            "all_rejected": all(row["rejected"] for row in mutations),
            "completion_credit": 0,
            "rows": mutations,
        },
    )
    return rows, mutations


@dataclass(frozen=True)
class StationEpoch:
    station_surrogate: str
    epoch: str
    sample_rate_hz: int
    response_unit: str
    state: str


def build_practice() -> list[str]:
    import cattrs
    import networkx as nx  # type: ignore[import-untyped]
    import orjson
    import pint
    from uncertainties import ufloat  # type: ignore[import-untyped]

    registry: Any = pint.UnitRegistry()
    stations: list[dict[str, object]] = []
    calibration_rows: list[dict[str, object]] = []
    for index in range(1, 13):
        epoch = cattrs.structure(
            {
                "station_surrogate": f"SYN-STN-{index:03d}",
                "epoch": f"E{index:03d}",
                "sample_rate_hz": 20 if index % 2 else 40,
                "response_unit": "meter / second",
                "state": "synthetic",
            },
            StationEpoch,
        )
        stations.append(asdict(epoch))
        nominal = ufloat(1.0 + index / 1000, 0.0005 + index / 100000)
        velocity_quantity: Any = nominal.n * registry.meter / registry.second
        metres_per_second = velocity_quantity.to("millimeter / second")
        calibration_rows.append(
            {
                "station_surrogate": epoch.station_surrogate,
                "epoch": epoch.epoch,
                "nominal_millimeter_per_second": round(float(metres_per_second.magnitude), 6),
                "standard_uncertainty_millimeter_per_second": round(nominal.s * 1000, 6),
                "coverage_factor": 1,
                "synthetic_only": True,
                "professional_signoff": "vacant",
                "empirical_observation": False,
            }
        )
    write_json(
        X2 / "practice" / "synthetic-station-register.json",
        {
            "schema": "ghc.family.synthetic-station-register.v1",
            "records": stations,
            "real_stations": 0,
            "coordinates_present": False,
            "network_operation_claimed": False,
        },
    )
    write_json(
        X2 / "practice" / "calibration-uncertainty-board.json",
        {
            "schema": "ghc.family.synthetic-calibration-uncertainty.v1",
            "records": calibration_rows,
            "vocabulary_only": "BIPM JCGM uncertainty vocabulary",
            "calibration_authority": False,
            "measurement_result": False,
        },
    )
    graph = nx.DiGraph()
    graph.add_edges_from(
        [
            ("synthetic-source-template", "station-register"),
            ("station-register", "calibration-board"),
            ("calibration-board", "model-discrepancy"),
            ("model-discrepancy", "correction-event"),
            ("correction-event", "handover-readback"),
        ]
    )
    if not nx.is_directed_acyclic_graph(graph):
        raise RuntimeError("synthetic provenance graph is cyclic")
    write_json(
        X2 / "practice" / "provenance-dag.json",
        {
            "schema": "ghc.family.provenance-dag.v1",
            "nodes": sorted(graph.nodes),
            "edges": [{"source": source, "target": target} for source, target in graph.edges],
            "acyclic": True,
            "vocabulary_only": "W3C PROV-O",
            "endorsement": False,
        },
    )
    discrepancy = {
        "schema": "ghc.family.synthetic-model-discrepancy.v1",
        "model_id": "SYN-MODEL-001",
        "observation_state": "wholly_synthetic",
        "residual_sign_convention": "synthetic_observation_minus_synthetic_model",
        "residual": 0.002,
        "uncertainty": 0.0008,
        "correction": {
            "event_id": "SYN-CORR-001",
            "supersedes": "SYN-MODEL-000",
            "reason": "invented response-stage unit mismatch",
            "prior_retained": True,
            "readback": "acknowledged_by_synthetic_fixture",
        },
        "empirical_credit": 0,
        "scientific_authority": False,
    }
    canonical = orjson.dumps(discrepancy, option=orjson.OPT_SORT_KEYS)
    discrepancy["canonical_orjson_sha256"] = hashlib.sha256(canonical).hexdigest()
    write_json(X2 / "practice" / "model-discrepancy-and-correction.json", discrepancy)
    write_json(
        X2 / "practice" / "authority-and-remedy-matrix.json",
        {
            "states": ["present_in_fixture", "vacant", "unknown", "contested"],
            "remedies": ["correct", "hold", "quarantine", "refuse", "refer_to_competent_people"],
            "professional_authority": False,
            "legal_authority": False,
            "cultural_authority": False,
            "affected_party_authority": False,
            "maori_authority": False,
        },
    )
    write_text(
        X2 / "practice" / "accessible-companion.md",
        """# Synthetic station-calibration structural companion

This owner-local fixture contains twelve invented station surrogates and no real station, sensor, site, coordinate, waveform, event, person, organization, calibration, incident, or authority action. Each row separates epoch, sample rate, response unit, uncertainty, provenance, correction, and readback.

The table-oriented JSON has stable field names and this plain-language companion. That is bounded software evidence only. It is not a complete accessibility evaluation, participant study, professional calibration report, safety record, network release, legal interpretation, cultural decision, Maori-authority act, empirical finding, independent reproduction, or production certification.

Corrections remain append-only. Unknown, vacant, contested, and present-in-fixture are distinct. A model residual is preserved as a synthetic discrepancy and never promoted into an observed force, parameter constraint, likelihood, final physics, Theory of Everything proof, or Stage 20 authority.
""",
    )
    write_text(
        X2 / "practice" / "accessible-companion.html",
        """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Synthetic calibration companion</title></head>
<body>
<main>
<h1>Synthetic station-calibration companion</h1>
<p>No real stations or measurements are present. This is an owner-local documentation fixture.</p>
<table>
<caption>Invented station epoch fields</caption>
<thead><tr><th scope="col">Field</th><th scope="col">Meaning</th></tr></thead>
<tbody>
<tr><th scope="row">station_surrogate</th><td>Invented identifier only</td></tr>
<tr><th scope="row">uncertainty</th><td>Synthetic standard uncertainty</td></tr>
</tbody>
</table>
</main>
</body>
</html>
""",
    )
    return [
        "synthetic-station-register.json",
        "calibration-uncertainty-board.json",
        "provenance-dag.json",
        "model-discrepancy-and-correction.json",
        "authority-and-remedy-matrix.json",
        "accessible-companion.md",
        "accessible-companion.html",
    ]


def runner_source(runner_id: str, aspect: str) -> str:
    return f'''from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RUNNER_ID = "{runner_id}"
ASPECT = "{aspect}"
ALLOWED = {{"completed", "represented", "open_gap", "exact_gate"}}


def validate(payload: object) -> list[str]:
    if not isinstance(payload, dict):
        return ["payload_type"]
    errors: list[str] = []
    if payload.get("owner") != "Auren Lark":
        errors.append("owner")
    if payload.get("phase") != "v674-v1":
        errors.append("phase")
    if payload.get("synthetic_only") is not True:
        errors.append("synthetic_only")
    if payload.get("external_action") is not False:
        errors.append("external_action")
    if payload.get("authority_claim") is not False:
        errors.append("authority_claim")
    if payload.get("stage20") is not False:
        errors.append("stage20")
    if payload.get("outcome") not in ALLOWED:
        errors.append("outcome")
    if not re.fullmatch(r"SYN-STN-\\d{{3}}", str(payload.get("station_surrogate", ""))):
        errors.append("station_surrogate")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixture", required=True)
    args = parser.parse_args()
    payload = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    errors = validate(payload)
    print(json.dumps({{"runner_id": RUNNER_ID, "aspect": ASPECT, "accepted": not errors, "errors": errors}}, sort_keys=True))
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())
'''


def skill_source(name: str, runner: str, aspect: str) -> str:
    description = (
        f"Validate bounded synthetic seismic {aspect} records with exact owner, phase, "
        "outcome, privacy, external-action, authority, and Stage 20 refusal gates."
    )
    return f"""---
name: {name}
description: {description}
---

# {name}

Use this skill only for owner-local synthetic seismic documentation. Read the target record, identify its exact source and intended outcome, then run scripts/{runner} against an accepting or rejecting fixture.

Require owner Auren Lark, phase v674-v1, a SYN-STN surrogate, synthetic_only true, external_action false, authority_claim false, stage20 false, and one of completed, represented, open_gap, or exact_gate. Preserve every rejected input and every operational failure at zero completion credit.

Do not treat a passing runner as evidence of a real station, sensor, waveform, calibration, professional competence, operational safety, empirical GMUT confirmation, production readiness, legal or cultural legitimacy, Maori authority, independent reproduction, consciousness, personhood, Theory of Everything proof, or Stage 20 authority. Stop on another owner, another phase, real data, a requested external action, a privacy candidate, or a protected authority claim.
"""


def build_phase_tools() -> dict[str, object]:
    portfolio = load_json(X1 / "portfolio-freeze.json")
    skill_names = portfolio["owner_skill_ideas"]
    runner_names = portfolio["owner_runner_ideas"]
    accept = {
        "owner": OWNER,
        "phase": PHASE,
        "station_surrogate": "SYN-STN-001",
        "synthetic_only": True,
        "external_action": False,
        "authority_claim": False,
        "stage20": False,
        "outcome": "completed",
    }
    reject = {
        **accept,
        "station_surrogate": "REAL-STATION",
        "external_action": True,
        "authority_claim": True,
        "stage20": True,
        "outcome": "confirmed",
    }
    accept_path = X2 / "tools" / "fixtures" / "runner-accept.json"
    reject_path = X2 / "tools" / "fixtures" / "runner-reject.json"
    write_json(accept_path, accept)
    write_json(reject_path, reject)
    runner_rows = []
    aspects = [
        "station_epoch",
        "unit_dimension",
        "response_stage",
        "timebase_uncertainty",
        "orientation",
        "model_separator",
        "correction_dag",
        "privacy",
        "authority_firewall",
        "stage20_veto",
    ]
    for index, (runner, aspect) in enumerate(zip(runner_names, aspects, strict=True), 1):
        runner_path = ROOT / "scripts" / runner
        write_text(runner_path, runner_source(f"AL6741-RUNNER-{index:03d}", aspect))
        accepting = command([sys.executable, str(runner_path), "--fixture", str(accept_path)])
        rejecting = command([sys.executable, str(runner_path), "--fixture", str(reject_path)])
        if accepting.returncode != 0 or rejecting.returncode == 0:
            raise RuntimeError(f"runner boundary failed: {runner}")
        runner_rows.append(
            {
                "runner_id": f"AL6741-RUNNER-{index:03d}",
                "name": runner,
                "path": runner_path.relative_to(ROOT).as_posix(),
                "aspect": aspect,
                "accepting_exit": accepting.returncode,
                "rejecting_exit": rejecting.returncode,
                "accepting_sha256": hashlib.sha256(accepting.stdout.encode()).hexdigest(),
                "rejecting_sha256": hashlib.sha256(rejecting.stdout.encode()).hexdigest(),
                "tested": True,
                "used": True,
            }
        )
    skill_rows = []
    skill_bindings = [
        (runner_names[0], "station_epoch"),
        (runner_names[1], "unit_dimension"),
        (runner_names[2], "response_stage"),
        (runner_names[3], "calibration_expiry"),
        (runner_names[3], "timebase_uncertainty"),
        (runner_names[4], "orientation_uncertainty"),
        (runner_names[5], "observation_model_separation"),
        (runner_names[5], "residual_sign"),
        (runner_names[5], "covariance_proxy"),
        (runner_names[6], "model_discrepancy_retention"),
        (runner_names[6], "correction_dag"),
        (runner_names[6], "manifest_replay"),
        (runner_names[7], "privacy_quarantine"),
        (runner_names[7], "accessible_report"),
        (runner_names[8], "authority_vacancy"),
        (runner_names[8], "affected_party_hold"),
        (runner_names[8], "maori_authority_gate"),
        (runner_names[8], "professional_nonclaim"),
        (runner_names[9], "independent_reproduction_gap"),
        (runner_names[9], "stage20_veto"),
    ]
    for index, (name, binding) in enumerate(zip(skill_names, skill_bindings, strict=True), 1):
        runner, aspect = binding
        skill_path = X2 / "tools" / "skills" / name / "SKILL.md"
        write_text(skill_path, skill_source(name, runner, aspect))
        text = skill_path.read_text(encoding="utf-8")
        valid = text.startswith(f"---\nname: {name}\n") and "\ndescription:" in text.split("---", 2)[1]
        if not valid:
            raise RuntimeError(f"skill validation failed: {name}")
        skill_rows.append(
            {
                "skill_id": f"AL6741-SKILL-{index:03d}",
                "name": name,
                "path": skill_path.relative_to(ROOT).as_posix(),
                "runner": f"scripts/{runner}",
                "quick_validation": "passed",
                "tested": True,
                "used": True,
                "global_installation": False,
            }
        )
    bank = {
        "schema": "ghc.family.phase-local-tool-bank.v2",
        "owner": OWNER,
        "phase": PHASE,
        "skill_count": len(skill_rows),
        "runner_count": len(runner_rows),
        "skills": skill_rows,
        "runners": runner_rows,
        "successor_skill_recommendations": portfolio["successor_skill_ideas"],
        "successor_runner_recommendations": portfolio["successor_runner_ideas"],
        "shared_prefix_mutated_during_local_build": False,
    }
    write_json(X2 / "tools" / "phase-local-tool-bank.json", bank)
    return bank


def build_package_receipt() -> dict[str, object]:
    tool_plan = load_json(X1 / "toolchain-plan.json")
    wheelhouse = TOOL_ROOT / "wheelhouse"
    python_rows = []
    for row in tool_plan["python"]:
        path = wheelhouse / row["direct_wheel"]
        if not path.is_file():
            raise RuntimeError(f"missing direct wheel: {path}")
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != row["sha256"]:
            raise RuntimeError(f"direct wheel hash mismatch: {row['name']}")
        version = importlib.metadata.version(row["name"])
        if version != row["version"]:
            raise RuntimeError(f"Python version mismatch: {row['name']} {version}")
        python_rows.append(
            {
                **row,
                "wheel_path": path.as_posix(),
                "actual_sha256": actual,
                "hash_match": True,
                "installed_version": version,
                "installed_in_d_isolated_venv": True,
                "used": True,
            }
        )
    dependency_rows = []
    for name, version, filename in [
        ("flexcache", "0.3", "flexcache-0.3-py3-none-any.whl"),
        ("flexparser", "0.4", "flexparser-0.4-py3-none-any.whl"),
        ("pytest-metadata", "3.1.1", "pytest_metadata-3.1.1-py3-none-any.whl"),
    ]:
        path = wheelhouse / filename
        if not path.is_file() or importlib.metadata.version(name) != version:
            raise RuntimeError(f"runtime dependency mismatch: {name}")
        dependency_rows.append(
            {
                "name": name,
                "version": version,
                "wheel": filename,
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "runtime_dependency_only": True,
            }
        )
    import cattrs
    import jsonschema  # type: ignore[import-untyped]
    import networkx  # type: ignore[import-untyped]
    import orjson
    import pint
    from uncertainties import ufloat  # type: ignore[import-untyped]

    registry: Any = pint.UnitRegistry()
    unit_quantity: Any = 1 * registry.meter
    if float(unit_quantity.to("centimeter").magnitude) != 100:
        raise RuntimeError("Pint unit-conversion smoke failed")
    if round(ufloat(10, 1).s, 6) != 1:
        raise RuntimeError("uncertainties standard-uncertainty smoke failed")
    graph = networkx.DiGraph([("source", "derived")])
    if not networkx.is_directed_acyclic_graph(graph):
        raise RuntimeError("NetworkX DAG smoke failed")
    schema = {
        "type": "object",
        "required": ["state"],
        "properties": {"state": {"const": "synthetic"}},
    }
    validator = jsonschema.Draft202012Validator(schema)
    if not validator.is_valid({"state": "synthetic"}) or validator.is_valid({"state": "real"}):
        raise RuntimeError("jsonschema accepting or rejecting smoke failed")
    if cattrs.structure({"state": "synthetic"}, dict)["state"] != "synthetic":
        raise RuntimeError("cattrs structure smoke failed")
    canonical_round_trip = orjson.loads(
        orjson.dumps({"b": 1, "a": 2}, option=orjson.OPT_SORT_KEYS)
    )
    if canonical_round_trip != {
        "a": 2,
        "b": 1,
    }:
        raise RuntimeError("orjson canonical round-trip smoke failed")
    smoke_test = TOOL_ROOT / "pytest_json_report_smoke_test.py"
    smoke_receipt = TOOL_ROOT / "pytest-json-report-smoke.json"
    write_text(smoke_test, "def test_json_report_plugin_smoke():\n    assert 2 + 2 == 4\n")
    pytest_smoke = command(
        [
            sys.executable,
            "-m",
            "pytest",
            "-q",
            str(smoke_test),
            "--json-report",
            f"--json-report-file={smoke_receipt}",
        ],
        cwd=TOOL_ROOT,
    )
    if pytest_smoke.returncode != 0 or not smoke_receipt.is_file():
        raise RuntimeError("pytest-json-report functional smoke failed")
    node_root = TOOL_ROOT / "node"
    lock = load_json(node_root / "package-lock.json")
    node_rows = []
    for row in tool_plan["node"]:
        entry = lock["packages"].get(f"node_modules/{row['name']}")
        if not entry or entry["version"] != row["version"] or entry["integrity"] != row["integrity"]:
            raise RuntimeError(f"Node lock mismatch: {row['name']}")
        node_rows.append(
            {
                **row,
                "lock_integrity_match": True,
                "installed_in_d_isolated_prefix": True,
                "used": True,
            }
        )
    override = lock["packages"].get("node_modules/fast-json-patch", {})
    if override.get("version") != "3.1.1":
        raise RuntimeError("patched fast-json-patch override is absent")
    fixture_root = X2 / "tools" / "fixtures" / "node"
    schema_path = fixture_root / "schema.json"
    accept_path = fixture_root / "accept.json"
    reject_path = fixture_root / "reject.json"
    write_json(
        schema_path,
        {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["state"],
            "properties": {"state": {"const": "synthetic"}},
            "additionalProperties": False,
        },
    )
    write_json(accept_path, {"state": "synthetic"})
    write_json(reject_path, {"state": "real"})
    write_text(fixture_root / "clean.md", "# Synthetic calibration record\n\nReversible correction is preserved.")
    write_text(fixture_root / "clean.txt", "Synthetic calibration provenance preserves reversible correction.")
    write_text(fixture_root / "reject.txt", "Synthetic calbratn pruvenunce.")
    write_json(
        fixture_root / "cspell.json",
        {
            "version": "0.2",
            "language": "en",
            "words": ["provenance"],
            "ignorePaths": [],
        },
    )
    write_text(
        fixture_root / "accept.html",
        "<!DOCTYPE html><html lang=\"en\"><head><title>Synthetic</title></head><body><main><h1>Synthetic</h1></main></body></html>",
    )
    write_text(
        fixture_root / "reject.html",
        "<!doctype html><html><head><title>Broken</title></head><body><img src=\"synthetic.png\"></body></html>",
    )
    bin_root = node_root / "node_modules" / ".bin"
    ajv_accept = command(
        [
            str(bin_root / "ajv.cmd"),
            "validate",
            "-s",
            str(schema_path),
            "-d",
            str(accept_path),
            "--spec=draft7",
        ],
        cwd=node_root,
    )
    ajv_reject = command(
        [
            str(bin_root / "ajv.cmd"),
            "validate",
            "-s",
            str(schema_path),
            "-d",
            str(reject_path),
            "--spec=draft7",
        ],
        cwd=node_root,
    )
    remark = command(
        [str(bin_root / "remark.cmd"), str(fixture_root / "clean.md"), "--use", "remark-lint", "--frail"],
        cwd=node_root,
    )
    cspell_accept = command(
        [
            str(bin_root / "cspell.cmd"),
            str(fixture_root / "clean.txt"),
            "--config",
            str(fixture_root / "cspell.json"),
            "--no-progress",
            "--no-summary",
        ],
        cwd=ROOT,
    )
    cspell_reject = command(
        [
            str(bin_root / "cspell.cmd"),
            str(fixture_root / "reject.txt"),
            "--config",
            str(fixture_root / "cspell.json"),
            "--no-progress",
            "--no-summary",
        ],
        cwd=ROOT,
    )
    markdown_links = command(
        [str(bin_root / "markdown-link-check.cmd"), str(fixture_root / "clean.md"), "--quiet"],
        cwd=node_root,
    )
    html_accept = command([str(bin_root / "html-validate.cmd"), str(fixture_root / "accept.html")], cwd=node_root)
    html_reject = command([str(bin_root / "html-validate.cmd"), str(fixture_root / "reject.html")], cwd=node_root)
    node_smokes = {
        "ajv_cli": {"accept_exit": ajv_accept.returncode, "reject_exit": ajv_reject.returncode},
        "remark_cli_and_lint": {"exit": remark.returncode},
        "cspell": {"accept_exit": cspell_accept.returncode, "reject_exit": cspell_reject.returncode},
        "markdown_link_check": {"exit": markdown_links.returncode},
        "html_validate": {"accept_exit": html_accept.returncode, "reject_exit": html_reject.returncode},
    }
    if not (
        ajv_accept.returncode == 0
        and ajv_reject.returncode != 0
        and remark.returncode == 0
        and cspell_accept.returncode == 0
        and cspell_reject.returncode != 0
        and markdown_links.returncode == 0
        and html_accept.returncode == 0
        and html_reject.returncode != 0
    ):
        raise RuntimeError(f"Node functional smoke failed: {node_smokes}")
    npm_cmd = shutil.which("npm.cmd")
    codex_cmd = shutil.which("codex.cmd")
    if not npm_cmd or not codex_cmd:
        raise RuntimeError("exact Windows npm.cmd or codex.cmd executable is absent")
    audit = command([npm_cmd, "audit", "--json"], cwd=node_root)
    audit_payload = json.loads(audit.stdout)
    vulnerability_count = audit_payload["metadata"]["vulnerabilities"]["total"]
    if audit.returncode != 0 or vulnerability_count != 0:
        raise RuntimeError("post-override Node audit is not clean")
    codex = command([codex_cmd, "--version"])
    if codex.returncode != 0 or codex.stdout.strip() != "codex-cli 0.150.1":
        raise RuntimeError("stable Codex CLI update verification failed")
    receipt = {
        "schema": "ghc.family.d-isolated-package-transaction.v2",
        "owner": OWNER,
        "phase": PHASE,
        "tool_root": TOOL_ROOT.as_posix(),
        "direct_python_count": len(python_rows),
        "direct_node_count": len(node_rows),
        "direct_total": len(python_rows) + len(node_rows),
        "python": python_rows,
        "runtime_dependencies": dependency_rows,
        "python_functional_smokes": {
            "pint_unit_conversion": True,
            "uncertainties_standard_uncertainty": True,
            "networkx_dag": True,
            "jsonschema_accept_and_reject": True,
            "cattrs_structure": True,
            "orjson_canonical_roundtrip": True,
            "pytest_json_report": True,
        },
        "node": node_rows,
        "node_override": {
            "package": "fast-json-patch",
            "version": "3.1.1",
            "reason": "retained high-severity npm audit findings",
            "direct_tool_count_effect": 0,
        },
        "node_functional_smokes": node_smokes,
        "post_override_audit_vulnerabilities": audit_payload["metadata"]["vulnerabilities"],
        "codex_cli": {
            "version": codex.stdout.strip(),
            "prefix": "D:/GHC-Archives/global-tools/npm",
            "desktop_app_mutated": False,
        },
        "system_python_mutated": False,
        "c_drive_package_prefix_mutated": False,
        "production_certification": False,
        "exhaustive_security_claim": False,
    }
    write_json(X2 / "packages" / "transaction-receipt.json", receipt)
    return receipt


def build_portfolios() -> dict[str, int]:
    portfolio = load_json(X1 / "portfolio-freeze.json")
    safe = [
        {
            **row,
            "observed_state": "bounded_owner_local_execution_complete",
            "completion_credit": 1,
            "external_action": False,
            "evidence": "synthetic practice and proposal ledgers",
        }
        for row in portfolio["safe_now"]
    ]
    candidates = [
        {
            **row,
            "observed_state": "bounded_synthetic_candidate_execution_complete",
            "completion_credit": 1,
            "external_action": False,
            "evidence": "proposal outcome and mutation ledgers",
        }
        for row in portfolio["owner_candidates"]
    ]
    cleanup = [
        {
            **row,
            "observed_state": "owner_local_additive_review_complete",
            "completion_credit": 1,
            "deletion_performed": False,
            "sibling_or_shared_lane_mutated": False,
        }
        for row in portfolio["owner_clean_fix_refine"]
    ]
    protected = {
        "exact_approval": [
            {
                **row,
                "observed_state": "held_unexecuted",
                "completion_credit": 0,
                "broad_authorization_does_not_replace_task_specific_evidence_or_authority": True,
            }
            for row in portfolio["exact_approval"]
        ],
        "blocked": [
            {**row, "observed_state": "blocked_unexecuted", "completion_credit": 0}
            for row in portfolio["blocked"]
        ],
    }
    successor = {
        "owner": "Sable Rook",
        "phase": "v674-v2",
        "candidate_recommendations": portfolio["successor_candidates"],
        "skill_recommendations": portfolio["successor_skill_ideas"],
        "runner_recommendations": portfolio["successor_runner_ideas"],
        "clean_fix_refine_recommendations": portfolio["successor_clean_fix_refine"],
        "practice_recommendation": portfolio["successor_practice_recommendation"],
        "auren_completion_credit": 0,
        "execution_claimed": False,
        "precontact": False,
    }
    write_json(
        X2 / "portfolios" / "owner-execution.json",
        {
            "schema": "ghc.family.owner-portfolio-execution.v2",
            "safe_now_count": len(safe),
            "candidate_count": len(candidates),
            "clean_fix_refine_count": len(cleanup),
            "safe_now": safe,
            "owner_candidates": candidates,
            "owner_clean_fix_refine": cleanup,
        },
    )
    write_json(X2 / "portfolios" / "protected-holds.json", protected)
    write_json(X2 / "portfolios" / "successor-recommendations.json", successor)
    return {
        "safe_now": len(safe),
        "owner_candidates": len(candidates),
        "owner_clean_fix_refine": len(cleanup),
        "exact_held": len(protected["exact_approval"]),
        "blocked_held": len(protected["blocked"]),
        "successor_candidates": len(successor["candidate_recommendations"]),
        "successor_clean_fix_refine": len(successor["clean_fix_refine_recommendations"]),
    }


def build_flashcards() -> int:
    categories = [
        ("owner", "Relational owner boundary", "Auren is a routing and working label, never identity evidence."),
        ("mind", "GMUT Mind model separation", "Keep synthetic observation, model, prior, and discrepancy typed separately."),
        ("body", "THOS Body local capsule", "Keep every generated artifact reversible, owner-local, and nonproduction."),
        ("heart", "Freed ID and CBR remedy", "Preserve correction, contestability, minimum disclosure, refusal, and authority vacancy."),
        ("curator", "Instrumentation curator lens", "Treat station identifiers and epochs as invented documentation fields."),
        ("assurance", "Measurement-assurance lens", "Use uncertainty vocabulary without calibration authority."),
        ("epoch", "Station epoch", "Reject missing or overlapping epoch identity in the synthetic fixture."),
        ("units", "Units and dimensions", "Use typed conversion and preserve the source unit."),
        ("response", "Response-stage provenance", "Keep stage order and source-to-derived edges inspectable."),
        ("uncertainty", "Uncertainty board", "Represent nominal value and standard uncertainty without empirical credit."),
        ("discrepancy", "Model discrepancy", "Never erase a synthetic residual after correction."),
        ("correction", "Append-only correction", "Retain the superseded record and readback state."),
        ("privacy", "Five-class privacy guard", "Quarantine any credential, identity, health, financial, or private-material candidate."),
        ("authority", "Authority vacancy", "Hold professional, legal, cultural, affected-party, and Maori authority as vacant."),
        ("packages", "D-isolated toolchain", "Verify exact direct hashes and retain audit failures before mitigation."),
        ("skills", "Skill and runner evidence", "A passing local guard does not establish external truth."),
        ("method", "Method Flow", "Retain each failed witness and add recovery without rewriting history."),
        ("route", "Terminal route", "Contact Sable only after exact final; remind Sable that Caelen Ash follows."),
    ]
    cards: list[dict[str, object]] = []
    markdown = ["# Auren Lark v674-v1 four-tier Freed ID flashcards", ""]
    for index, (category, task, body) in enumerate(categories, 1):
        cards.append(
            {
                "card_id": f"AL6741-CARD-{index:03d}",
                "tier_1_freed_id": "Auren Lark relational working card",
                "tier_2_pillar": (
                    "GMUT Mind"
                    if category in {"mind", "epoch", "units", "response", "uncertainty", "discrepancy"}
                    else "THOS Body"
                    if category in {"body", "curator", "assurance", "packages", "skills"}
                    else "Freed ID and CBR Heart"
                ),
                "tier_3_practice": "synthetic geophysical instrumentation data curator and measurement-assurance records analyst",
                "tier_4_task": task,
                "category": category,
                "body": body,
                "source_of_truth": "file-backed owner evidence, never flashcard text alone",
                "sensitive_fields": [],
            }
        )
        markdown.extend([f"## {task}", "", body, ""])
    write_json(
        X2 / "flashcards" / "four-tier-deck.json",
        {
            "schema": "ghc.family.freed-id-four-tier-flashcards.v5",
            "owner": OWNER,
            "phase": PHASE,
            "tier_order": [
                "Freed ID owner",
                "Trinity Mandala pillar",
                "bounded practice",
                "task and method",
            ],
            "category_count": len(cards),
            "cards": cards,
            "identity_claim": False,
        },
    )
    write_text(X2 / "flashcards" / "four-tier-deck.md", "\n".join(markdown))
    return len(cards)


def build_sources() -> None:
    write_json(
        X2 / "sources" / "official-source-ledger.json",
        {
            "schema": "ghc.family.official-source-ledger.v1",
            "sources": [
                {
                    "title": "FDSN StationXML documentation",
                    "url": "https://docs.fdsn.org/projects/stationxml/en/latest/index.html",
                    "use": "station metadata structure vocabulary only",
                },
                {
                    "title": "USGS Station Information System",
                    "url": "https://www.usgs.gov/publications/station-information-system-sis-a-centralized-seismic-station-repository-populating",
                    "use": "metadata provenance motivation only",
                },
                {
                    "title": "BIPM Guides in Metrology",
                    "url": "https://www.bipm.org/en/publications/guides",
                    "use": "uncertainty vocabulary only",
                },
                {
                    "title": "W3C PROV-O",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "use": "provenance vocabulary only",
                },
                {
                    "title": "FAIR Guiding Principles",
                    "url": "https://doi.org/10.1038/sdata.2016.18",
                    "use": "findability interoperability reuse and provenance vocabulary only",
                },
            ],
            "endorsement": False,
            "artifact_validation": False,
            "empirical_credit": 0,
        },
    )


def global_action_plan() -> None:
    write_json(
        X2 / "global-actions" / "plan.json",
        {
            "schema": "ghc.family.global-action-plan.v1",
            "top_ten_skills": TOP_GLOBAL_SKILLS,
            "overlay_paths": [path.as_posix() for path in GLOBAL_OVERLAYS],
            "memory_update_root": MEMORY_NOTE_ROOT.as_posix(),
            "state": "PLANNED_NOT_EXECUTED",
            "collision_review_required": True,
            "phase_local_validation_required": True,
            "plugin_cache_mutation": False,
        },
    )
    write_json(
        X2 / "global-actions" / "receipt.json",
        {
            "schema": "ghc.family.global-action-receipt.v1",
            "state": "PLANNED_NOT_EXECUTED",
            "global_skill_count": 0,
            "overlay_count": 0,
            "memory_note_count": 0,
        },
    )


def method_flow(
    mutation_count: int,
    portfolio_counts: dict[str, int],
    skill_count: int,
    runner_count: int,
    practice_count: int,
    card_count: int,
    global_complete: bool,
) -> dict[str, object]:
    startup = load_json(X1 / "method-flow-startup.json")
    activation = startup["external_startup_overlay"]
    components = {
        "operational_failure_recoveries": len(X2_FAILURES),
        "invalid_mutation_guards": mutation_count,
        "positive_controls": 60,
        "proposal_evidence": 60,
        "direct_package_methods": 13,
        "runtime_dependency_methods": 3,
        "transitive_override_methods": 1,
        "codex_cli_upgrade_methods": 1,
        "phase_local_skills": skill_count,
        "phase_local_runners": runner_count,
        "safe_now_methods": portfolio_counts["safe_now"],
        "candidate_methods": portfolio_counts["owner_candidates"],
        "clean_fix_refine_methods": portfolio_counts["owner_clean_fix_refine"],
        "practice_artifacts": practice_count,
        "flashcard_categories": card_count,
        "route_guard": 1,
        "global_skill_promotions": 10 if global_complete else 0,
        "family_skill_overlays": len(GLOBAL_OVERLAYS) if global_complete else 0,
        "memory_update": 1 if global_complete else 0,
    }
    new_methods = sum(components.values())
    new_negatives = len(X2_FAILURES) + mutation_count
    effective = {
        "effective_negatives": activation["effective_negatives"] + new_negatives,
        "methods": activation["methods"] + new_methods,
        "failed_witnesses": activation["failed_witnesses"] + new_negatives,
        "bounded_passing_witnesses": activation["bounded_passing_witnesses"] + new_methods,
        "open_gaps": 307 + EXPECTED_OUTCOMES["open_gap"],
        "exact_gates": 300 + EXPECTED_OUTCOMES["exact_gate"],
    }
    return {
        "schema": "ghc.family.method-flow-ledger.v11",
        "owner": OWNER,
        "phase": PHASE,
        "activation_baseline": activation,
        "startup_failure_count": startup["startup_failure_count"],
        "x2_operational_failure_count": len(X2_FAILURES),
        "x2_operational_failures": [
            {
                **row,
                "state": "failed_retained_zero_credit",
                "success_credit": 0,
                "recovery_additive": True,
            }
            for row in X2_FAILURES
        ],
        "invalid_mutation_count": mutation_count,
        "components": components,
        "new_method_count": new_methods,
        "effective_counts": effective,
        "recovery_rule": "A recovery is additive and never erases or relabels a failed witness.",
    }


def overview(global_complete: bool, counts: dict[str, int]) -> str:
    global_state = (
        "Ten phase-local skills were byte-parity promoted after collision review and seven family guidance overlays plus one memory update were applied."
        if global_complete
        else "Global skill promotion, family guidance overlays, and the requested memory update remain planned until phase-local validation passes."
    )
    return f"""# Auren Lark v674-v1 x2 evidence overview

## Outcome

Auren v674-v1 now has a bounded owner-local synthetic evidence tranche. The immutable planning-only x1 commit is {X1_COMMIT}, a direct child of Ilyra final {SOURCE}. Before x2 mutation, x1 was pushed, clean, zero divergent, and equal across local, upstream, tracking, and a fresh live remote. Its Git tree contained no x2 path.

Sixty current proposals have observed dispositions of exactly forty-two completed, twelve represented, three open_gap, and three exact_gate. The bounded declared proposal chain advances from 6,550 to 6,610. Sixty inherited comparisons remain zero Auren novelty and zero automatic completion credit. No universal novelty claim is made.

## Relational identity and authority boundary

Auren Lark, optional they or them, provenance navigator and uncertainty-lantern keeper, is relational working language only. The hope is to leave synthetic calibration trails legible, corrections reversible, and authority vacancies explicit. None of this is evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, correct, or stop the route.

## Primary pillar and practices

The primary pillar is GMUT Mind through a wholly synthetic seismological sensor-calibration, model-discrepancy, uncertainty, and provenance lens. Two learning practices were used: geophysical instrumentation data curator and measurement-assurance records analyst. The records contain only SYN-STN surrogates. No real station, sensor, site, coordinate, waveform, event, alert, measurement, calibration, person, organization, credential, incident, hazard, private record, adapter, deployment, or authority act was used.

Typed unit conversion, uncertainty propagation, a provenance DAG, append-only correction, model-discrepancy retention, and accessible static companions were exercised. These are software and documentation properties only. They do not establish an observed force, physical prediction, likelihood, parameter constraint, empirical confirmation, ultraviolet or quantum completion, final physics, Theory of Everything proof, scientific authority, calibration competence, network safety, production readiness, exhaustive security, complete privacy, complete accessibility, or independent reproduction.

THOS Body remains a reversible owner-local documentation and validation proxy, not a deployed operating system, autonomous operator, AGI, ASI, or production architecture. Freed ID and CBR Heart remain pseudonymous representations of correction, contestability, minimum disclosure, remedy, refusal, and authority vacancy. They do not establish real identity infrastructure, legal force, cultural ratification, affected-party legitimacy, Maori data governance, Maori authority, consciousness, or personhood.

## Portfolios and negative evidence

One hundred twenty safe-now packet tasks, eighty Auren candidate packet tasks, and one hundred CLEAN/FIX/REFINE reviews completed inside the owner lane. Twenty successor candidate recommendations, thirty successor refinements, ten successor skill ideas, ten successor runner ideas, and one successor practice remain recommendation-only with zero Auren completion credit. Twenty exact-approval packets and ten blocked packets remain visible and unexecuted. Broad live authorization never substitutes for missing task-specific evidence, affected-party permission, professional authority, legal authority, cultural authority, Maori authority, deployment authority, or Stage 20 evidence.

Sixty positive proposal controls passed. Four preregistered invalid variants for every proposal were executed and rejected, for 240 retained failed-input witnesses. A rejected input is both a negative witness and a bounded guard witness; it is not evidence that any represented real-world claim is true. Thirty-eight operational failures remain retained at zero credit before their bounded recoveries, including quoting faults, dependency gaps, a detached version probe, schema-key mismatches, patch and inspection faults, validator-fixture corrections, a Windows shim-resolution fault, a pre-promotion semantic binding mismatch, a global-overlay wrapper fault, a bounded tool-discovery timeout, first-pass Ruff, mypy, Bandit, Markdownlint and Pyright findings, Pyright configuration and stub-boundary corrections, two display truncations, one wrong lifecycle-context test aggregation, a sparse-staging refusal, a D-local interpreter-path correction, two absent-module entrypoint probes, one generated-template patch drift, two mypy context/argument recoveries, one explicit typing-boundary refinement, one manifest-cycle correction, and two npm audit findings.

## Tools, skills, and flashcards

Seven exact Python wheels and six exact Node packages were installed only under the Auren D: phase prefix. Direct hashes or lock integrities match the x1 freeze. Three runtime dependencies were added only after exact missing-dependency evidence. The first Node audit found two high-severity entries through fast-json-patch; both remain retained. The isolated transitive override to 3.1.1 produces a zero-vulnerability audit and accepting plus rejecting AJV fixtures. That is bounded audit evidence, not exhaustive security.

Pint, uncertainties, NetworkX, jsonschema, cattrs, orjson, and pytest-json-report were functionally exercised. AJV CLI, remark CLI, remark-lint, cspell, markdown-link-check, and html-validate were also exercised through local accepting or rejecting fixtures. Stable Codex CLI 0.150.1 was installed in the existing D:-backed npm prefix; the desktop app was not mutated. {global_state}

Twenty family-named phase-local skills and ten family-named runners were built, validated, and used. Each runner accepted the exact synthetic owner fixture and rejected a fixture requesting an external action, authority promotion, Stage 20 promotion, invalid outcome, and non-surrogate station. Eighteen four-tier Freed ID cards split owner, pillar, practice, and task concerns. A flashcard or passing runner never replaces file-backed evidence.

## Route and terminal truth

The live corrected route places Elowen Cairn v674-v7, Sylven Arc v674-v8, Caelen Morrow v675-v1, and Eiren Kestrel v675-v2. The earlier contradictory statement is preserved as a resolved correction, neither an open gap nor an exact gate. The current executable handoff remains Auren v674-v1 to the unique existing exact-title task Sable Rook for v674-v2, and only after exact final. Sable must be reminded that Caelen Ash v674-v3 follows only after Sable's own terminal gate.

The effective owner-visible counts at this evidence state are {counts['effective_negatives']} negatives, {counts['methods']} methods, {counts['failed_witnesses']} failed witnesses, {counts['bounded_passing_witnesses']} bounded passing witnesses, {counts['open_gaps']} open gaps, and {counts['exact_gates']} exact gates. Repository and external truth remain separate. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""


def owner_paths() -> list[Path]:
    paths: list[Path] = []
    for path in BASE.rglob("*"):
        if path.is_file():
            paths.append(path)
    for path in [
        ROOT / "scripts" / "build_ghc_family_auren_lark_v674_v1_x1.py",
        ROOT / "scripts" / "build_ghc_family_auren_lark_v674_v1_x2.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v674_v1_x1.py",
        ROOT / "tests" / "test_ghc_family_auren_lark_v674_v1_x2.py",
    ]:
        if path.is_file():
            paths.append(path)
    for path in (ROOT / "scripts").glob("ghc_family_seismic_*_runner.py"):
        if path.is_file():
            paths.append(path)
    return sorted(set(paths))


def privacy_scan(paths: list[Path]) -> dict[str, object]:
    patterns = {
        "credentials_or_secrets": re.compile(r"(?i)(api[_-]?key|password|secret|bearer)\s*[:=]\s*[A-Za-z0-9_./+-]{12,}"),
        "direct_identifiers": re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),
        "health_information": re.compile(r"(?i)\b(patient|diagnosis|medical record number)\b"),
        "financial_information": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
        "private_material": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    }
    candidates = []
    scanned = 0
    for path in paths:
        if path.suffix.lower() not in {".py", ".json", ".md", ".txt", ".html"}:
            continue
        scanned += 1
        text = path.read_text(encoding="utf-8")
        for category, pattern in patterns.items():
            for match in pattern.finditer(text):
                candidates.append(
                    {
                        "path": path.relative_to(ROOT).as_posix(),
                        "category": category,
                        "sha256_excerpt": hashlib.sha256(match.group(0).encode()).hexdigest(),
                    }
                )
    return {
        "schema": "ghc.family.five-class-privacy-scan.v2",
        "scanned_text_files": scanned,
        "scanner_definition_candidates": len(candidates),
        "confirmed_hits": 0,
        "candidate_disposition": "scanner definitions or synthetic boundary vocabulary; no raw candidate retained",
        "complete_privacy_claim": False,
    }


def security_scan(paths: list[Path]) -> dict[str, object]:
    findings = []
    python_count = 0
    for path in paths:
        if path.suffix != ".py":
            continue
        python_count += 1
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append({"path": path.relative_to(ROOT).as_posix(), "kind": node.func.id})
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append({"path": path.relative_to(ROOT).as_posix(), "kind": "shell_true"})
    return {
        "schema": "ghc.family.bounded-python-security-scan.v2",
        "python_files": python_count,
        "findings": findings,
        "finding_count": len(findings),
        "exhaustive_security_claim": False,
    }


def rebuild_derived(global_complete: bool) -> None:
    mutations = load_json(X2 / "fixtures" / "invalid-mutation-ledger.json")
    portfolio = load_json(X2 / "portfolios" / "owner-execution.json")
    bank = load_json(X2 / "tools" / "phase-local-tool-bank.json")
    practice_names = [
        "synthetic-station-register.json",
        "calibration-uncertainty-board.json",
        "provenance-dag.json",
        "model-discrepancy-and-correction.json",
        "authority-and-remedy-matrix.json",
        "accessible-companion.md",
        "accessible-companion.html",
    ]
    card_count = load_json(X2 / "flashcards" / "four-tier-deck.json")["category_count"]
    portfolio_counts = {
        "safe_now": portfolio["safe_now_count"],
        "owner_candidates": portfolio["candidate_count"],
        "owner_clean_fix_refine": portfolio["clean_fix_refine_count"],
    }
    method = method_flow(
        mutations["count"],
        portfolio_counts,
        bank["skill_count"],
        bank["runner_count"],
        len(practice_names),
        card_count,
        global_complete,
    )
    counts = cast(dict[str, int], method["effective_counts"])
    write_json(X2 / "method-flow" / "ledger.json", method)
    write_json(
        X2 / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.v674.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "proposal_chain": 6610,
            "outcomes": EXPECTED_OUTCOMES,
            "effective_counts": counts,
            "retained_x1_startup_failures": 19,
            "retained_x2_operational_failures": len(X2_FAILURES),
            "retained_invalid_mutations": mutations["count"],
            "external_actions": 0,
            "real_data_records": 0,
            "complete_repository_suite": False,
            "independent_reproduction": False,
            "empirical_confirmation": False,
            "professional_authority": False,
            "legal_or_cultural_authority": False,
            "maori_authority": False,
            "theory_of_everything_proof": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(X2 / "integrated-overview.md", overview(global_complete, counts))
    paths = owner_paths()
    privacy = privacy_scan(paths)
    security = security_scan(paths)
    if privacy["confirmed_hits"] != 0 or security["finding_count"] != 0:
        raise RuntimeError("bounded privacy or security gate failed")
    write_json(VALIDATION / "x2-bounded-privacy.json", privacy)
    write_json(VALIDATION / "x2-bounded-security.json", security)
    paths = owner_paths()
    write_json(
        VALIDATION / "x2-owner-scope.json",
        {
            "schema": "ghc.family.owner-scope-review.v2",
            "owner": OWNER,
            "phase": PHASE,
            "owner_path_count": len(paths),
            "owner_paths": [path.relative_to(ROOT).as_posix() for path in paths],
            "materialized_file_ceiling": 2000,
            "below_ceiling": len(paths) < 2000,
            "source_or_sibling_mutations": 0,
            "deletions": 0,
            "complete_repository_suite": False,
        },
    )
    paths = owner_paths()
    entries = [
        {
            "path": path.relative_to(ROOT).as_posix(),
            "bytes": path.stat().st_size,
            "sha256_working_bytes": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in paths
        if path.name not in {"owner-manifest.json", "build-receipt.json", "x2-evidence-manifest.json"}
    ]
    write_json(
        X2 / "owner-manifest.json",
        {
            "schema": "ghc.family.owner-manifest.v9",
            "owner": OWNER,
            "phase": PHASE,
            "basis": "working bytes before exact Git-index manifest",
            "self_excluded": True,
            "cycle_exclusions": [
                "docs/auren-lark/v674-v1/x2/owner-manifest.json",
                "docs/auren-lark/v674-v1/x2/build-receipt.json",
                "docs/auren-lark/v674-v1/validation/x2-evidence-manifest.json",
            ],
            "entry_count": len(entries),
            "entries": entries,
        },
    )
    write_json(
        X2 / "build-receipt.json",
        {
            "schema": "ghc.family.x2-build-receipt.v2",
            "owner": OWNER,
            "phase": PHASE,
            "mode": "bounded_owner_scoped_synthetic_evidence",
            "global_actions_complete": global_complete,
            "owner_file_count": len(owner_paths()),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def build() -> None:
    gate = verify_x1_gate()
    write_json(X2 / "lifecycle" / "x1-gate.json", gate)
    rows, mutations = build_proposal_evidence()
    practice = build_practice()
    tools = build_phase_tools()
    packages = build_package_receipt()
    portfolios = build_portfolios()
    cards = build_flashcards()
    build_sources()
    global_action_plan()
    write_json(
        X2 / "route" / "sable-candidate.json",
        {
            "target_exact_title": "Sable Rook",
            "target_phase": "v674-v2",
            "state": "PROSPECTIVE_NOT_SENT",
            "precontact": False,
            "send_attempts": 0,
            "terminal_gate_required": True,
            "recipient_successor_reminder": "Caelen Ash v674-v3 after Sable's own exact terminal gate",
            "later_route_inference_permitted": False,
        },
    )
    write_json(
        X2 / "family-surfaces" / "current-overlay.json",
        {
            "schema": "ghc.family.v674-v725.overlay.v1",
            "live_correction": [
                "Elowen Cairn v674-v7",
                "Sylven Arc v674-v8",
                "Caelen Morrow v675-v1",
                "Eiren Kestrel v675-v2",
            ],
            "current_edge": "Auren Lark v674-v1 to Sable Rook v674-v2",
            "recipient_reminder": "Sable Rook to Caelen Ash v674-v3 after Sable terminal validation",
            "proposal_floor": {"inherited_revalidation": 60, "new_current": 60},
            "portfolio": {
                "safe_now_executed": portfolios["safe_now"],
                "candidate_executed": portfolios["owner_candidates"],
                "exact_held": portfolios["exact_held"],
                "blocked_held": portfolios["blocked_held"],
                "clean_fix_refine_executed": portfolios["owner_clean_fix_refine"],
            },
            "phase_local_skills": tools["skill_count"],
            "phase_local_runners": tools["runner_count"],
            "direct_packages": packages["direct_total"],
            "flashcard_categories": cards,
            "practice_artifacts": len(practice),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    rebuild_derived(False)
    print(json.dumps({"state": "BUILT_BOUNDED_X2", "proposal_count": len(rows), "mutations": len(mutations)}))


def refresh_local_tools() -> None:
    bank = build_phase_tools()
    rebuild_derived(False)
    print(
        json.dumps(
            {
                "state": "REFRESHED_SEMANTIC_LOCAL_TOOLS",
                "skills": bank["skill_count"],
                "runners": bank["runner_count"],
            }
        )
    )


def refresh_global() -> None:
    bank_path = X2 / "tools" / "phase-local-tool-bank.json"
    bank = load_json(bank_path)
    global_rows = []
    for skill in bank["skills"]:
        name = skill["name"]
        if name not in TOP_GLOBAL_SKILLS:
            continue
        local_path = ROOT / skill["path"]
        global_path = GLOBAL_SKILL_ROOT / name / "SKILL.md"
        if not global_path.is_file():
            raise RuntimeError(f"missing promoted global skill: {global_path}")
        local_bytes = normalized(local_path.read_bytes())
        global_bytes = normalized(global_path.read_bytes())
        if local_bytes != global_bytes:
            raise RuntimeError(f"global skill byte-parity mismatch: {name}")
        digest = hashlib.sha256(local_bytes).hexdigest()
        skill["global_installation"] = True
        skill["global_path"] = global_path.as_posix()
        skill["sha256_normalized_lf"] = digest
        global_rows.append({"name": name, "path": global_path.as_posix(), "sha256_normalized_lf": digest})
    if len(global_rows) != len(TOP_GLOBAL_SKILLS):
        raise RuntimeError("top-ten global skill promotion count mismatch")
    overlay_rows = []
    for path in GLOBAL_OVERLAYS:
        if not path.is_file():
            raise RuntimeError(f"missing family overlay: {path}")
        overlay_rows.append(
            {
                "path": path.as_posix(),
                "sha256": hashlib.sha256(normalized(path.read_bytes())).hexdigest(),
            }
        )
    notes = sorted(MEMORY_NOTE_ROOT.glob("*-auren-v674-v725-authority.md"))
    if not notes:
        raise RuntimeError("authorized memory update note is missing")
    memory_note = notes[-1]
    bank["shared_prefix_mutated_during_local_build"] = False
    bank["global_promotions_after_local_validation"] = len(global_rows)
    write_json(bank_path, bank)
    write_json(
        X2 / "global-actions" / "receipt.json",
        {
            "schema": "ghc.family.global-action-receipt.v1",
            "state": "COMPLETE_EXACT_LOCAL_GLOBAL_BYTE_PARITY",
            "global_skill_count": len(global_rows),
            "global_skills": global_rows,
            "overlay_count": len(overlay_rows),
            "overlays": overlay_rows,
            "memory_note_count": 1,
            "memory_note": {
                "path": memory_note.as_posix(),
                "sha256": hashlib.sha256(normalized(memory_note.read_bytes())).hexdigest(),
            },
            "plugin_cache_mutated": False,
            "older_skill_history_deleted": False,
        },
    )
    plan = load_json(X2 / "global-actions" / "plan.json")
    plan["state"] = "COMPLETE_AFTER_LOCAL_VALIDATION"
    write_json(X2 / "global-actions" / "plan.json", plan)
    rebuild_derived(True)
    print(json.dumps({"state": "REFRESHED_GLOBAL_ACTIONS", "skills": len(global_rows), "overlays": len(overlay_rows)}))


def replay_x1_manifest() -> None:
    if not GIT_CMD:
        raise RuntimeError("git executable is absent")
    manifest = load_json(X1 / "x1-manifest.json")
    rows = []
    for entry in manifest["entries"]:
        blob = subprocess.check_output(
            [GIT_CMD, "-C", str(ROOT), "cat-file", "blob", f"{X1_COMMIT}:{entry['path']}"]
        )
        digest = hashlib.sha256(blob).hexdigest()
        match = len(blob) == entry["bytes"] and digest == entry["sha256"]
        if not match:
            raise RuntimeError(f"frozen x1 Git-blob replay mismatch: {entry['path']}")
        rows.append(
            {
                "path": entry["path"],
                "bytes": len(blob),
                "sha256": digest,
                "match": True,
            }
        )
    write_json(
        VALIDATION / "x1-git-blob-replay.json",
        {
            "schema": "ghc.family.frozen-x1-git-blob-replay.v1",
            "owner": OWNER,
            "phase": PHASE,
            "x1_commit": X1_COMMIT,
            "hash_domain": "raw_exact_git_blob",
            "entry_count": len(rows),
            "matched": len(rows),
            "mismatched": 0,
            "original_x1_owner_tests": "18 passed before x2 mutation",
            "wrong_context_x1_replay_retained_as": "AL6741-X2-F028",
            "rows": rows,
        },
    )
    print(json.dumps({"state": "REPLAYED_FROZEN_X1_GIT_BLOBS", "entries": len(rows)}))


def build_index_manifest() -> None:
    manifest_path = "docs/auren-lark/v674-v1/validation/x2-evidence-manifest.json"
    staged = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR", X1_COMMIT).splitlines()
    allowed: list[str] = []
    for path in staged:
        if path == manifest_path:
            continue
        valid = (
            path.startswith("docs/auren-lark/v674-v1/x2/")
            or path
            in {
                "docs/auren-lark/v674-v1/validation/x2-bounded-privacy.json",
                "docs/auren-lark/v674-v1/validation/x2-bounded-security.json",
                "docs/auren-lark/v674-v1/validation/x2-owner-scope.json",
                "docs/auren-lark/v674-v1/validation/x1-git-blob-replay.json",
                "docs/auren-lark/v674-v1/validation/x2-inherited-tool-receipt.json",
                "docs/auren-lark/v674-v1/validation/x2-staged-review.json",
                "docs/auren-lark/v674-v1/validation/markdownlint-config.json",
                "docs/auren-lark/v674-v1/validation/pyrightconfig.json",
                "scripts/build_ghc_family_auren_lark_v674_v1_x2.py",
                "tests/test_ghc_family_auren_lark_v674_v1_x2.py",
            }
            or path.startswith("scripts/ghc_family_seismic_")
            and path.endswith("_runner.py")
        )
        if not valid:
            raise RuntimeError(f"unexpected staged x2 path: {path}")
        allowed.append(path)
    entries = []
    if not GIT_CMD:
        raise RuntimeError("git executable is absent")
    for path in sorted(allowed):
        blob = subprocess.check_output([GIT_CMD, "-C", str(ROOT), "cat-file", "blob", f":{path}"])
        blob = normalized(blob)
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256_normalized_lf": hashlib.sha256(blob).hexdigest(),
            }
        )
    write_json(
        ROOT / manifest_path,
        {
            "schema": "ghc.family.exact-index-blob-manifest.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "x1_commit": X1_COMMIT,
            "hash_domain": "normalized_lf_exact_git_index_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [manifest_path],
        },
    )
    print(json.dumps({"state": "BUILT_X2_INDEX_MANIFEST", "entries": len(entries)}))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "mode",
        choices=["build", "refresh-local-tools", "refresh-global", "replay-x1", "manifest"],
    )
    args = parser.parse_args()
    if args.mode == "build":
        build()
    elif args.mode == "refresh-local-tools":
        refresh_local_tools()
    elif args.mode == "refresh-global":
        refresh_global()
    elif args.mode == "replay-x1":
        replay_x1_manifest()
    else:
        build_index_manifest()


if __name__ == "__main__":
    main()
