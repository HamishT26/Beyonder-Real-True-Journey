from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "neris-solane" / "v675-v4"
SOURCE_FINAL = "78f2d675771a9f37340d51c5e66c4a83a85fe6c0"
X1_COMMIT = "5bd78357eab01cf9a09f01648356411feedb2180"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout


def import_path(path: Path):
    name = "test_" + hashlib.sha256(str(path).encode("utf-8")).hexdigest()[:12]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_exact_source_and_immutable_x1():
    assert git("rev-parse", f"{X1_COMMIT}^").decode().strip() == SOURCE_FINAL
    x1_paths = git("ls-tree", "-r", "--name-only", X1_COMMIT, "--", "docs/neris-solane/v675-v4/x1").decode().splitlines()
    assert len(x1_paths) >= 18
    for path in x1_paths:
        committed = git("show", f"{X1_COMMIT}:{path}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        current = (ROOT / path).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert current == committed
    assert not git("diff", "--name-only", X1_COMMIT, "--", "docs/neris-solane/v675-v4/x1").strip()


def test_proposal_outcomes_and_execution_boundary():
    payload = load("docs/neris-solane/v675-v4/x2/proposal-outcomes.json")
    rows = payload["rows"]
    assert len(rows) == 40
    assert Counter(row["core_outcome"] for row in rows) == Counter(OUTCOMES)
    assert payload["declared_chain_before"] == 7150
    assert payload["declared_chain_after"] == 7190
    assert payload["universal_novelty_claim"] is False
    for row in rows:
        assert row["planned_outcome"] == row["core_outcome"]
        assert row["synthetic_only"] is True
        assert row["real_people"] == row["real_objects"] == row["external_actions"] == 0
        assert row["authority_conferred"] is False
        if row["core_outcome"] in {"open_gap", "exact_gate"}:
            assert row["executed"] is False


def test_contract_files_match_outcome_rows():
    payload = load("docs/neris-solane/v675-v4/x2/proposal-outcomes.json")
    contract = import_path(ROOT / "scripts" / "ghc_family_spectrograph_contract.py")
    for row in payload["rows"]:
        separate = load(f"docs/neris-solane/v675-v4/x2/proposal-contracts/{row['proposal_id']}.json")
        assert separate == row
        assert contract.validate_record(row)["passed"] is True


def test_positive_controls_and_mutations():
    positives = load("docs/neris-solane/v675-v4/x2/positive-controls.json")
    mutations = load("docs/neris-solane/v675-v4/x2/rejecting-mutations.json")
    assert positives["count"] == 36
    assert all(row["passed"] and not row["authority_conferred"] for row in positives["rows"])
    assert mutations["count"] == 160
    assert all(row["rejected"] and row["failure_retained"] and row["completion_credit"] == 0 for row in mutations["rows"])
    assert Counter(row["failure_class"] for row in mutations["rows"]) == Counter(
        {
            "missing_proposal_id": 40,
            "real_person_injection": 40,
            "authority_promotion": 40,
            "unknown_outcome": 40,
        }
    )


def test_inherited_revalidation_zero_credit():
    payload = load("docs/neris-solane/v675-v4/x2/inherited-revalidation.json")
    assert payload["count"] == 20
    assert all(row["novelty_credit"] == row["completion_credit"] == 0 for row in payload["rows"])
    assert all(row["bounded_integrity_check"] == "passed" for row in payload["rows"])


def test_portfolio_counts_and_gated_work():
    payload = load("docs/neris-solane/v675-v4/x2/portfolio-outcomes.json")
    counts = Counter(row["class"] for row in payload["rows"])
    assert counts["safe_now"] == 60
    assert counts["candidate"] == 30
    assert counts["exact_approval"] == 20
    assert counts["blocked"] == 10
    assert counts["skill"] == 20
    assert counts["runner"] == 10
    assert counts["tool"] == 3
    assert counts["clean_fix_refine"] == 60
    assert all(
        row["observed_state"] == "retained_unexecuted"
        for row in payload["rows"]
        if row["class"] in {"exact_approval", "blocked"}
    )


def test_three_tools_and_ten_runner_smokes():
    runners = load("docs/neris-solane/v675-v4/x2/runner-validation.json")
    tools = load("docs/neris-solane/v675-v4/x2/tool-validation.json")
    assert runners["count"] == 10
    assert all(row["passed"] and row["actual_smoke_used"] for row in runners["rows"])
    assert tools["count"] == 3
    assert all(row["passed"] and row["actual_smoke_used"] for row in tools["rows"])


def test_twenty_skill_packages_and_usage():
    usage = load("docs/neris-solane/v675-v4/x2/skill-usage.json")
    assert usage["count"] == 20
    assert all(row["structural_check_passed"] and row["actual_owner_local_use"] for row in usage["rows"])
    assert all(row["skill_creator_quick_validation"] == "passed_once_before_evidence_seal" for row in usage["rows"])
    assert all(row["skill_creator_quick_validation_invocations"] == 1 for row in usage["rows"])
    assert all(row["globally_installed"] is False for row in usage["rows"])
    validator = load("docs/neris-solane/v675-v4/x2/skill-creator-validation.json")
    assert validator["invocations"] == validator["passed"] == 20
    assert validator["failed"] == validator["globally_installed"] == 0
    for row in usage["rows"]:
        path = OWNER_ROOT / "x2" / "skills" / row["skill"] / "SKILL.md"
        assert path.is_file()


def test_eighty_flashcards_and_graph():
    payload = load("docs/neris-solane/v675-v4/x2/freed-id-flashcard-deck.json")
    assert payload["card_count"] == 80
    assert len(payload["cards"]) == 80
    assert len(payload["graph"]["nodes"]) == 80
    assert len(payload["graph"]["edges"]) == 79
    assert len({row["card_id"] for row in payload["cards"]}) == 80
    assert payload["tier_counts"] == {
        "Trinity_pillars": 15,
        "bounded_practice": 20,
        "owner": 5,
        "task_and_change": 40,
    }


def test_state_graph_and_handover_tools():
    graph = load("docs/neris-solane/v675-v4/x2/spectral-record-state-graph.json")
    assert graph["validation"]["passed"] is True
    handover = import_path(ROOT / "scripts" / "ghc_family_spectrograph_handover.py")
    result = handover.validate_handover(
        {
            "synthetic_only": True,
            "events": [
                {"sequence": 1, "operation": "append"},
                {"sequence": 2, "operation": "supersede"},
            ],
            "challenge_open": True,
            "remedy_authority_present": False,
        }
    )
    assert result["passed"] is True


def test_method_flow_retains_all_failures():
    payload = load("docs/neris-solane/v675-v4/x2/method-flow.json")
    assert payload["counts"] == {
        "methods": 176,
        "failure_witnesses": 176,
        "passing_witnesses": 176,
        "state_events": 528,
    }
    assert payload["failures_rewritten"] == 0
    assert all(row["retained"] and row["completion_credit"] == 0 for row in payload["failure_witnesses"])


def test_source_count_overlay_layers_are_separate():
    payload = load("docs/neris-solane/v675-v4/x2/source-count-overlay.json")
    assert payload["immutable_elaren_repository_seal"] == {
        "negatives": 40580,
        "methods": 28832,
        "failed_witnesses": 12241,
        "passing_witnesses": 16171,
        "open_gaps": 335,
        "exact_gates": 327,
        "proposal_chain": 7150,
    }
    assert payload["effective_evidence_state"] == {
        "negatives": 40760,
        "methods": 29012,
        "failed_witnesses": 12421,
        "passing_witnesses": 16407,
        "open_gaps": 337,
        "exact_gates": 329,
        "proposal_chain": 7190,
    }
    assert payload["no_failure_or_gate_erased"] is True


def test_source_adapter_is_zero_row_and_transport_disabled():
    payload = load("docs/neris-solane/v675-v4/x2/source-adapter.json")
    assert payload["transport"] == "disabled"
    assert payload["network_calls"] == payload["downloads"] == payload["ingested_rows"] == 0
    assert payload["authority_conferred"] is False


def test_environment_checks_are_read_only():
    payload = load("docs/neris-solane/v675-v4/x2/environment-versions.json")
    assert len(payload["checks"]) == 4
    assert payload["updates_performed"] == 0
    assert payload["elevation"] is False
    assert payload["host_security_changed"] is False
    assert payload["windows_features_changed"] is False
    assert payload["rebooted"] is False


def test_static_report_accessibility_structure_and_no_network():
    html = (OWNER_ROOT / "x2" / "accessible-report.html").read_text(encoding="utf-8")
    required = [
        '<html lang="en">',
        'href="#main"',
        "<header>",
        "<nav aria-label=",
        '<main id="main">',
        "<h1>",
        "<caption>",
        'scope="col"',
        "prefers-reduced-motion",
    ]
    assert all(token in html for token in required)
    assert "<script" not in html.lower()
    assert "http://" not in html.lower() and "https://" not in html.lower()


def test_phase_truth_and_wellbeing_boundaries():
    truth = load("docs/neris-solane/v675-v4/x2/phase-truth.json")
    wellbeing = load("docs/neris-solane/v675-v4/x2/wellbeing-check.json")
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["real_people"] == truth["real_objects"] == truth["external_actions"] == 0
    assert truth["authority_conferred"] is False
    assert wellbeing["working_language_only"] is True
    assert wellbeing["successor_precontacted"] is False


def test_exact_staged_manifest_privacy_and_review():
    manifest = load("docs/neris-solane/v675-v4/validation/evidence-manifest.json")
    privacy = load("docs/neris-solane/v675-v4/validation/evidence-staged-privacy.json")
    review = load("docs/neris-solane/v675-v4/validation/evidence-staged-review.json")
    assert manifest["entry_count"] == len(manifest["entries"])
    assert manifest["content_domain"] == "normalized_lf_exact_staged_git_blob"
    assert len({row["path"] for row in manifest["entries"]}) == manifest["entry_count"]
    for row in manifest["entries"]:
        blob = git("show", f":{row['path']}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]
    assert privacy["confirmed_hit_count"] == 0
    assert review["passed"] is True
    assert all(value is True for value in review["checks"].values())


def test_only_four_core_outcome_labels():
    labels: set[str] = set()
    for path in (OWNER_ROOT / "x2").rglob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        stack = [payload]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                for key, item in value.items():
                    if key in {"core_outcome", "planned_outcome", "expected_outcome"} and isinstance(item, str):
                        labels.add(item)
                    stack.append(item)
            elif isinstance(value, list):
                stack.extend(value)
    assert labels == {"completed", "represented", "open_gap", "exact_gate"}
