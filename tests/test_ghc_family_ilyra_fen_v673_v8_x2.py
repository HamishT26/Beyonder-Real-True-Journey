from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs" / "ilyra-fen" / "v673-v8"
X1 = BASE / "x1"
X2 = BASE / "x2"
VALIDATION = BASE / "validation"
SOURCE = "c1818f0c09737c69a1870ef6bf8ed7fc339cb727"
X1_COMMIT = "b567a67858066e6c23f3abb82828f5185d7ab65e"
ALLOWED = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()


def test_strict_x1_gate_and_absence() -> None:
    gate = load(X2 / "lifecycle" / "x1-gate.json")
    assert gate["state"] == "VALID_STRICT_X1_GATE"
    assert gate["source"] == SOURCE
    assert gate["x1_commit"] == X1_COMMIT
    assert gate["x1_parent"] == SOURCE
    assert gate["x2_paths_in_x1"] == 0
    assert gate["merge_count"] == 0
    assert gate["four_way_equal"] is True
    assert len({gate["local"], gate["upstream"], gate["tracking"], gate["fresh_live_remote"]}) == 1


def test_proposal_outcomes_and_chain() -> None:
    ledger = load(X2 / "proposals" / "outcome-ledger.json")
    truth = load(X2 / "phase-truth.json")
    observed = Counter(row["observed_disposition"] for row in ledger["rows"])
    assert len(ledger["rows"]) == 40
    assert observed == Counter(completed=28, represented=8, open_gap=2, exact_gate=2)
    assert set(observed) == ALLOWED
    assert sum(row["completion_credit"] for row in ledger["rows"]) == 28
    assert ledger["proposal_chain"] == truth["proposal_chain"] == 6550


def test_positive_controls_and_invalid_mutations() -> None:
    controls = load(X2 / "fixtures" / "positive-control-ledger.json")
    mutations = load(X2 / "fixtures" / "invalid-mutation-ledger.json")
    assert controls["count"] == 36
    assert all(row["passed"] is True and row["external_actions"] == 0 for row in controls["rows"])
    assert mutations["count"] == 160
    assert mutations["all_rejected"] is True
    assert all(row["rejected"] is True for row in mutations["rows"])
    assert all(row["completion_credit"] == 0 for row in mutations["rows"])


def test_package_transaction_is_exact_and_isolated() -> None:
    receipt = load(X2 / "packages" / "transaction-receipt.json")
    assert receipt["environment_root"] == "D:/GHC-Archives/phase-tools/ilyra-fen-v673-v8"
    assert receipt["direct_surface_count"] == 3
    assert receipt["dependency_count"] == 0
    assert len(receipt["wheel_receipts"]) == 3
    assert all(row["official_digest_match"] is True for row in receipt["wheel_receipts"])
    assert all(row["actual_sha256"] == row["sha256"] for row in receipt["wheel_receipts"])
    assert all(receipt["smokes"]["cbor2"].values())
    assert receipt["smokes"]["jsonpointer"] == {"missing_rejected": True, "resolved": "weft"}
    assert all(receipt["smokes"]["immutables"].values())
    assert all(value is False for value in receipt["install_controls"].values())
    assert receipt["audit_claimed"] is False


def test_phase_local_skills_and_runners() -> None:
    bank = load(X2 / "tools" / "phase-local-tool-bank.json")
    assert bank["skill_count"] == 20
    assert bank["runner_count"] == 10
    assert bank["shared_prefix_mutated"] is False
    assert all(row["quick_validation"] == "passed" and row["used"] for row in bank["skills"])
    assert all(row["global_installation"] is False for row in bank["skills"])
    assert all(row["accepting_exit"] == 0 and row["rejecting_exit"] != 0 for row in bank["runners"])
    assert all(row["passed"] and row["used"] for row in bank["runners"])
    for row in bank["skills"]:
        path = ROOT / row["skill"]
        assert path.read_text(encoding="utf-8").startswith(f"---\nname: {row['name']}\n")
    for row in bank["runners"]:
        assert (ROOT / row["runner"]).is_file()


def test_owner_portfolios_and_held_gates() -> None:
    owner = load(X2 / "portfolios" / "owner-execution.json")
    gates = load(X2 / "portfolios" / "protected-gates.json")
    successor = load(X2 / "portfolios" / "successor-recommendations.json")
    assert owner["counts"] == {
        "safe_now_completed": 60,
        "candidate_completed": 30,
        "clean_fix_refine_completed": 60,
        "skills_built_tested_used": 20,
        "runners_built_tested_used": 10,
    }
    assert gates["exact_approval_count"] == 20
    assert gates["blocked_count"] == 10
    assert gates["all_unexecuted"] is True
    assert all(row["state"] == "visible_unexecuted_gate" for row in gates["rows"])
    assert successor["completion_credit"] == 0
    assert successor["state"] == "recommendation_only"
    assert len(successor["candidate_recommendations"]) == 20


def test_practice_and_authority_boundaries() -> None:
    chain = load(X2 / "practice" / "pattern-chain-register.json")
    graph = load(X2 / "practice" / "provenance-dag.json")
    authority = load(X2 / "practice" / "authority-and-remedy-matrix.json")
    trinity = load(X2 / "practice" / "trinity-mandala-boundaries.json")
    assert len(chain["segments"]) == 12
    assert chain["real_objects"] == 0
    assert chain["production_instructions"] is False
    assert graph["acyclic"] is True and graph["cycle_mutation_rejected"] is True
    assert authority["legal_authority"] is False
    assert authority["cultural_authority"] is False
    assert authority["maori_authority"] is False
    assert trinity["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_method_flow_counts_and_failure_retention() -> None:
    ledger = load(X2 / "method-flow" / "ledger.json")
    assert ledger["operational_failure_count"] == 23
    assert ledger["invalid_mutation_count"] == 160
    assert ledger["new_method_count"] == 402
    assert ledger["effective_counts"] == {
        "effective_negatives": 37799,
        "effective_methods": 24226,
        "effective_failed_witnesses": 9460,
        "effective_passing_witnesses": 11837,
        "open_gaps": 307,
        "exact_gates": 300,
    }
    assert all(row["state"] == "failed_retained_zero_credit" for row in ledger["operational_failures"])
    assert all(row["passing_bounded_witness"] is True for row in ledger["operational_failures"])


def test_four_tier_flashcards_are_projections() -> None:
    deck = load(X2 / "flashcards" / "four-tier-deck.json")
    assert deck["category_count"] >= 10
    assert len(deck["cards"]) == deck["category_count"]
    assert deck["tier_order"] == [
        "Freed ID owner",
        "Trinity Mandala pillar",
        "bounded practice",
        "task and method",
    ]
    assert deck["identity_claim"] is False
    assert all(row["sensitive_fields"] == [] for row in deck["cards"])
    assert all("file-backed phase evidence" in row["source_of_truth"] for row in deck["cards"])


def test_all_phase_json_parses_strictly() -> None:
    paths = sorted(BASE.rglob("*.json"))
    assert len(paths) >= 95
    for path in paths:
        load(path)


def test_working_owner_manifest_replays() -> None:
    manifest = load(X2 / "owner-manifest.json")
    assert manifest["self_excluded"] is True
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        assert path.stat().st_size == row["bytes"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256_working_bytes"]


def test_exact_index_manifest_replays() -> None:
    path = VALIDATION / "x2-evidence-manifest.json"
    assert path.is_file()
    manifest = load(path)
    assert manifest["source"] == SOURCE
    assert manifest["x1_commit"] == X1_COMMIT
    assert manifest["self_exclusions"] == [
        "docs/ilyra-fen/v673-v8/validation/x2-evidence-manifest.json"
    ]
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        blob = subprocess.check_output(
            ["git", "-C", str(ROOT), "cat-file", "blob", f":{row['path']}"]
        )
        blob = blob.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert len(blob) == row["bytes"], row["path"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256_normalized_lf"], row["path"]


def test_privacy_and_bounded_security_receipts() -> None:
    privacy = load(VALIDATION / "x2-staged-privacy.json")
    security = load(VALIDATION / "x2-bounded-security.json")
    assert privacy["confirmed_hits"] == []
    assert privacy["complete_privacy_assurance"] is False
    assert len(privacy["classes"]) == 5
    assert security["findings"] == []
    assert security["exhaustive_security_assurance"] is False


def test_changed_python_has_no_bounded_ast_hazard() -> None:
    paths = [
        ROOT / "scripts" / "build_ghc_family_ilyra_fen_v673_v8_x2.py",
        ROOT / "tests" / "test_ghc_family_ilyra_fen_v673_v8_x2.py",
    ]
    paths.extend(ROOT / row["runner"] for row in load(X2 / "tools" / "phase-local-tool-bank.json")["runners"])
    findings = []
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id in {"eval", "exec"}
            ):
                findings.append((path.name, node.lineno, node.func.id))
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if (
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ):
                        findings.append((path.name, node.lineno, "shell=True"))
    assert findings == []


def test_overview_route_and_terminal_boundaries() -> None:
    overview = (X2 / "integrated-overview.md").read_text(encoding="utf-8")
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", overview)
    route = load(X2 / "route" / "auren-candidate.json")
    truth = load(X2 / "phase-truth.json")
    assert 900 <= len(words) <= 6000
    assert route["target_exact_title"] == "Auren Lark"
    assert route["target_phase"] == "v674-v1"
    assert route["state"] == "PROSPECTIVE_NOT_SENT"
    assert route["precontact"] is False
    assert route["send_attempts"] == 0
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["external_actions"] == 0
    assert truth["complete_repository_suite"] is False
    assert truth["independent_reproduction"] is False


def test_materialized_owner_scope_below_rotation_guard() -> None:
    review = load(VALIDATION / "x2-staged-review.json")
    assert review["owner_path_count"] < 2000
    assert review["materialized_files"] < review["materialized_file_ceiling"]
    assert review["source_or_sibling_mutations"] == 0
    assert review["deletions"] == 0
