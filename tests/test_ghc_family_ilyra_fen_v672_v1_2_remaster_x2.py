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
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v672-v1-2-remaster"
X1 = PHASE_ROOT / "x1"
X2 = PHASE_ROOT / "x2"
SOURCE = "f67221fbee56905a770c64533771dd9471fb2fba"
X1_COMMIT = "da48a47bd21a8e3053094d39691eb72ef1429abd"
ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> Any:
    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=reject_duplicates)


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(ROOT), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def test_strict_x1_before_x2_gate() -> None:
    gate = load(X2 / "lifecycle" / "x1-gate.json")
    assert git("rev-parse", "HEAD") == X1_COMMIT
    assert git("rev-parse", "HEAD^") == SOURCE
    assert gate["state"] == "VALID_STRICT_X1_GATE"
    assert gate["four_way_equal"] is True
    assert len({gate["local"], gate["upstream"], gate["tracking"], gate["fresh_live_remote"]}) == 1


def test_x1_remains_planning_only() -> None:
    truth = load(X1 / "phase-truth.json")
    assert truth["state"] == "X1_PLANNING_ONLY"
    assert truth["x2_executed"] is False
    assert truth["packages_installed"] == 0
    assert truth["global_skills_installed"] == 0


def test_exact_proposal_outcomes_and_chain() -> None:
    truth = load(X2 / "phase-truth.json")
    ledger = load(X2 / "proposals" / "outcome-ledger.json")
    rows = ledger["rows"]
    observed = Counter(row["observed_disposition"] for row in rows)
    assert len(rows) == 40
    assert observed == Counter(completed=28, represented=8, open_gap=2, exact_gate=2)
    assert set(observed) == ALLOWED_OUTCOMES
    assert truth["proposal_chain"] == 5950
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert sum(row["completion_credit"] for row in rows) == 28


def test_positive_and_rejecting_fixture_counts() -> None:
    controls = load(X2 / "fixtures" / "positive-control-ledger.json")
    mutations = load(X2 / "fixtures" / "invalid-mutation-ledger.json")
    assert controls["count"] == 36
    assert all(row["passed"] is True and row["external_actions"] == 0 for row in controls["rows"])
    assert mutations["count"] == 160
    assert mutations["all_rejected"] is True
    assert all(row["rejected"] is True for row in mutations["rows"])
    assert all(row["completion_credit"] == 0 for row in mutations["rows"])


def test_package_transaction_is_exact_and_d_first() -> None:
    receipt = load(X2 / "packages" / "transaction-receipt.json")
    assert receipt["environment_root"].startswith("D:/GHC-Archives/global-tools/")
    assert receipt["direct_surface_count"] == 13
    assert receipt["python_direct_count"] == 8
    assert receipt["node_direct_count"] == 5
    assert receipt["python_transitive_count"] == 2
    assert len(receipt["wheel_receipts"]) == 8
    assert len(receipt["node_receipts"]) == 5
    assert all(row["matched"] is True for row in receipt["wheel_receipts"])
    assert all(row["matched"] is True for row in receipt["node_receipts"])
    assert receipt["install_controls"]["system_python_mutated"] is False
    assert receipt["install_controls"]["npm_global_prefix_mutated"] is False
    assert receipt["install_controls"]["profile_or_path_mutated"] is False


def test_audit_failure_is_not_promoted() -> None:
    audits = load(X2 / "packages" / "transaction-receipt.json")["audits"]
    assert audits["initial_python"]["state"] == "FAILED_RETAINED_ZERO_CREDIT"
    corrected = audits["dependency_corrected_python"]
    assert corrected["state"] == "VALID_DEPENDENCY_CORRECTED_PYTHON_AUDIT"
    assert corrected["not_original_audit_success"] is True
    assert corrected["vulnerabilities"] == 0
    assert corrected["invoked_once"] is True
    assert audits["node"]["vulnerabilities"] == 0
    assert audits["node"]["invoked_once"] is True


def test_local_skill_and_runner_bank() -> None:
    bank = load(X2 / "tools" / "local-tool-bank-receipt.json")
    assert bank["skill_count"] == 20
    assert bank["runner_count"] == 10
    assert all(row["quick_validate_exit"] == 0 and row["passed"] for row in bank["skills"])
    assert all(row["accepting_exit"] == 0 for row in bank["runners"])
    assert all(row["rejecting_exit"] != 0 and row["passed"] for row in bank["runners"])
    for row in bank["skills"]:
        path = ROOT / row["skill"]
        text = path.read_text(encoding="utf-8")
        name = path.parent.name
        assert text.startswith(f"---\nname: {name}\n")
        assert "description:" in text.split("---", 2)[1]
    for row in bank["runners"]:
        assert (ROOT / row["runner"]).is_file()


def test_global_skill_promotion_and_composite() -> None:
    receipt = load(X2 / "tools" / "global-skill-promotion-receipt.json")
    assert receipt["promoted_count"] == 5
    assert receipt["composite_count"] == 1
    assert receipt["all_validated"] is True
    assert all(row["skill_byte_parity"] and row["runner_byte_parity"] for row in receipt["rows"])
    assert all(row["quick_validate_exit"] == 0 for row in receipt["rows"])
    assert all(row["collision_before_promotion"] is False for row in receipt["rows"])
    assert receipt["composite"]["name"] == "ghc-family-d-first-structured-evidence-toolchain"
    assert receipt["composite"]["destructive_history_merge"] is False


def test_owner_and_successor_portfolios() -> None:
    owner = load(X2 / "portfolios" / "owner-execution.json")
    successor = load(X2 / "portfolios" / "successor-recommendations.json")
    gates = load(X2 / "portfolios" / "protected-gates.json")
    assert owner["counts"] == {
        "safe_now_owner_completed": 60,
        "candidate_owner_completed": 50,
        "clean_fix_refine_owner_completed": 60,
        "skills_owner_completed": 20,
        "runners_owner_completed": 10,
        "exact_approval_unexecuted": 20,
        "blocked_unexecuted": 10,
    }
    assert successor["counts"] == {
        "candidate_recommendations": 20,
        "skill_recommendations": 10,
        "runner_recommendations": 10,
        "clean_fix_refine_recommendations": 30,
    }
    assert successor["practice_recommendation"] == "synthetic public-interest incident documentation analyst"
    assert all(row["completion_credit"] == 0 for row in successor["rows"])
    assert len(gates["rows"]) == 30
    assert all(row["x2_state"] == "visible_unexecuted_gate" for row in gates["rows"])


def test_four_tier_flashcards() -> None:
    deck = load(X2 / "flashcards" / "four-tier-deck.json")
    assert deck["category_count"] >= 10
    assert len(deck["cards"]) == deck["category_count"]
    assert deck["tier_order"] == ["Freed ID owner", "Trinity Mandala pillar", "bounded practice", "task and method"]
    assert all(row["source_of_truth"] == "file-backed phase evidence, never flashcard text alone" for row in deck["cards"])
    assert all(row["sensitive_fields"] == [] for row in deck["cards"])
    assert deck["identity_claim"] is False


def test_method_flow_counts_and_failure_retention() -> None:
    ledger = load(X2 / "method-flow" / "ledger.json")
    counts = ledger["effective_counts"]
    assert ledger["operational_failure_count"] == 29
    assert ledger["invalid_mutation_count"] == 160
    assert ledger["new_method_count"] == 274
    assert counts == {
        "effective_negatives": 35196,
        "effective_methods": 21827,
        "effective_failed_witnesses": 7017,
        "effective_passing_witnesses": 9118,
        "open_gaps": 276,
        "exact_gates": 270,
    }
    assert all(row["state"] == "failed_retained_zero_credit" for row in ledger["operational_failures"])
    assert all(row["passing_bounded_witness"] is True for row in ledger["operational_failures"])


def test_all_phase_json_is_strictly_parseable() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) >= 90
    for path in paths:
        load(path)


def test_owner_manifest_replays_working_bytes() -> None:
    manifest = load(X2 / "owner-manifest.json")
    assert manifest["self_excluded"] is True
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        path = ROOT / row["path"]
        assert path.is_file(), row["path"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"], row["path"]
        assert path.stat().st_size == row["bytes"]


def test_bounded_privacy_scan_has_no_confirmed_candidate() -> None:
    patterns = {
        "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        "openai_token": re.compile(r"(?<![A-Za-z0-9])sk-[A-Za-z0-9_-]{20,}"),
        "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
        "aws_access_key": re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
        "consumer_email": re.compile(r"\b[A-Za-z0-9._%+-]+@(gmail|outlook|hotmail|yahoo)\.[A-Za-z]{2,}\b", re.IGNORECASE),
    }
    candidates: list[tuple[str, str]] = []
    for path in sorted(PHASE_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append((path.relative_to(ROOT).as_posix(), label))
    assert candidates == []


def test_changed_python_has_no_bounded_ast_finding() -> None:
    findings: list[tuple[str, int, str]] = []
    paths = [ROOT / row["runner"] for row in load(X2 / "tools" / "local-tool-bank-receipt.json")["runners"]]
    paths.extend(
        [
            ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_contract_guard.py",
            ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_structured_data_guard.py",
            ROOT / "scripts" / "ghc_family_ilyra_v672_v1_2_toolchain_guard.py",
            ROOT / "scripts" / "build_ghc_family_ilyra_fen_v672_v1_2_remaster_x2.py",
        ]
    )
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                findings.append((path.name, node.lineno, node.func.id))
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                        findings.append((path.name, node.lineno, "shell=True"))
    assert findings == []


def test_overview_and_route_boundaries() -> None:
    overview = (X2 / "integrated-overview.md").read_text(encoding="utf-8")
    words = re.findall(r"\b\w+(?:[-']\w+)*\b", overview)
    route = load(X2 / "route" / "auren-candidate.json")
    truth = load(X2 / "phase-truth.json")
    assert 900 <= len(words) <= 6000
    assert route["target_exact_title"] == "Auren Lark"
    assert route["target_phase"] == "v672-v2"
    assert route["state"] == "PROSPECTIVE_NOT_SENT"
    assert route["precontact"] is False
    assert truth["original_canonical_replayed"] is False
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["external_actions"] == 0


def test_materialized_owner_scope_below_rotation_guard() -> None:
    paths = [path for path in ROOT.rglob("*") if path.is_file()]
    assert len(paths) < 2000
