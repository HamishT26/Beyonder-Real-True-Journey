from __future__ import annotations

import ast
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ghc_family_caelen_ash_v668_v6_archive as archive
import ghc_family_caelen_ash_v668_v6_controls as controls
from build_ghc_family_caelen_ash_v668_v6_x2 import X1_HEAD, control_fixtures, x1_portfolio, x1_proposals


PHASE_ROOT = ROOT / "docs" / "caelen-ash" / "v668-v6"


def load(relative: str):
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def mutation_rows() -> list[dict]:
    rows = []
    for path in sorted((PHASE_ROOT / "x2" / "mutations").glob("results-*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8"))["results"])
    return rows


def test_x2_starts_from_exact_corrected_x1() -> None:
    assert subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip() == X1_HEAD
    assert subprocess.run(["git", "rev-parse", "HEAD^"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip() == "5bced658a5b3f5bd7c4d88d47057d795abe57f42"
    assert archive.SOURCE_FINAL == "5bced658a5b3f5bd7c4d88d47057d795abe57f42"


def test_x1_git_blob_replay_is_exact() -> None:
    replay = load("x2/evidence/x1-blob-replay.json")
    assert replay["x1_head"] == X1_HEAD
    assert replay["entry_count"] == 47
    assert replay["self_exclusion_count"] == 1
    assert replay["mismatch_count"] == 0
    assert replay["mismatches"] == []


def test_x1_worktree_surface_is_unchanged() -> None:
    paths = ["docs/caelen-ash/v668-v6/x1", "scripts/ghc_family_caelen_ash_v668_v6_archive.py", "scripts/build_ghc_family_caelen_ash_v668_v6_x1.py", "tests/test_ghc_family_caelen_ash_v668_v6_x1.py"]
    completed = subprocess.run(["git", "diff", "--quiet", X1_HEAD, "--", *paths], cwd=ROOT)
    assert completed.returncode == 0


def test_forty_proposal_artifacts_and_cards() -> None:
    proposal_files = [path for path in (PHASE_ROOT / "x2" / "proposals").glob("ca6686-n*.json")]
    card_files = list((PHASE_ROOT / "x2" / "cards").glob("ca6686-n*.json"))
    assert len(proposal_files) == 40
    assert len(card_files) == 40
    assert len(x1_proposals()) == 40


def test_outcome_vocabulary_and_counts_are_exact() -> None:
    index = load("x2/proposals/outcome-index.json")
    truth = load("x2/phase-truth.json")
    expected = {"completed": 28, "exact_gate": 2, "open_gap": 2, "represented": 8}
    assert index["outcome_counts"] == expected
    assert truth["outcome_counts"] == expected
    assert index["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]


def test_all_160_preregistered_mutations_are_rejected() -> None:
    rows = mutation_rows()
    assert len(rows) == 160
    assert len({row["mutation_id"] for row in rows}) == 160
    assert {row["state"] for row in rows} == {"rejected"}
    assert {row["failure_credit"] for row in rows} == {0}
    assert {row["production_or_truth_credit"] for row in rows} == {0}


def test_mutation_method_flow_is_complete_and_sharded() -> None:
    paths = sorted((PHASE_ROOT / "method-flow").glob("x2-mutation-shard-*.json"))
    assert len(paths) == 16
    methods = witnesses = fails = passes = 0
    for path in paths:
        ledger = json.loads(path.read_text(encoding="utf-8"))
        assert ledger["schema"] == "ghc.family.method-flow-state.v1"
        methods += len(ledger["methods"])
        witnesses += len(ledger["witnesses"])
        fails += sum(row["result"] == "fail" for row in ledger["witnesses"])
        passes += sum(row["result"] == "pass" for row in ledger["witnesses"])
        assert all(row["recommendation_state"] == "preferred" for row in ledger["methods"])
    assert (methods, witnesses, fails, passes) == (160, 320, 160, 160)


def test_overlay_arithmetic_is_additive() -> None:
    summary = load("method-flow/x2-summary.json")
    x1 = summary["x1_overlay"]
    x2 = summary["x2_overlay"]
    for key in ("effective_negatives", "methods", "failed_witnesses", "passing_witnesses"):
        assert x2[key] == x1[key] + 164
    assert x2["open_gaps"] == x1["open_gaps"] + 2
    assert x2["exact_gates"] == x1["exact_gates"] + 2
    assert summary["all_failures_retained"] is True
    assert summary["x2_operational_failures_before_evidence_commit"] == 4


def test_all_ten_controls_accept_and_reject() -> None:
    fixtures = control_fixtures()
    assert set(fixtures) == set(controls.CONTROL_NAMES)
    for name, (positive, negative) in fixtures.items():
        assert controls.evaluate_control(name, positive)["accepted"] is True
        try:
            controls.evaluate_control(name, negative)
        except controls.RejectedFixture:
            pass
        else:
            raise AssertionError(f"negative accepted by {name}")


def test_ten_runners_have_accept_and_reject_receipts() -> None:
    index = load("x2/runners/index.json")
    assert index["count"] == 10
    assert index["accepting_invocations"] == 10
    assert index["rejecting_invocations"] == 10
    receipts = sorted((PHASE_ROOT / "x2" / "runners" / "receipts").glob("*.json"))
    assert len(receipts) == 10
    for path in receipts:
        row = json.loads(path.read_text(encoding="utf-8"))
        assert row["accept_returncode"] == 0
        assert row["reject_returncode"] == 2
        assert row["accept_payload"]["accepted"] is True
        assert row["reject_payload"]["accepted"] is False
        assert row["independent_reproduction"] is False


def test_runner_names_and_sources_are_family_current() -> None:
    index = load("x2/runners/index.json")
    assert all(name.startswith("ghc_family_") for name in index["runners"])
    for name in index["runners"]:
        path = ROOT / "scripts" / f"{name}.py"
        assert path.is_file()
        source = path.read_text(encoding="utf-8")
        assert "runner_main" in source
        assert "subprocess" not in source


def test_twenty_phase_local_skills_are_smoke_used_not_global() -> None:
    index = load("x2/skills/index.json")
    assert index["count"] == 20
    assert index["global_installs"] == 0
    for name in index["skills"]:
        root = PHASE_ROOT / "x2" / "skills" / name
        assert (root / "SKILL.md").is_file()
        receipt = json.loads((root / "smoke-receipt.json").read_text(encoding="utf-8"))
        assert receipt["initialized"] and receipt["validated"] and receipt["smoke_used"]
        assert receipt["global_install"] is False
        assert receipt["negative_result"]["rejected"] is True


def test_thirty_candidate_prototypes_completed_boundedly() -> None:
    paths = sorted((PHASE_ROOT / "x2" / "candidates").glob("*.json"))
    assert len(paths) == 30
    for path in paths:
        row = json.loads(path.read_text(encoding="utf-8"))
        assert row["state"] == "completed_bounded_prototype"
        assert row["external_rows"] == 0
        assert row["authority_decisions"] == 0


def test_safe_and_clean_fix_refine_portfolios_complete_additively() -> None:
    safe = []
    for path in sorted((PHASE_ROOT / "x2" / "portfolio").glob("safe-now-*.json")):
        safe.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    cfr = []
    for path in sorted((PHASE_ROOT / "x2" / "portfolio").glob("clean-fix-refine-*.json")):
        cfr.extend(json.loads(path.read_text(encoding="utf-8"))["rows"])
    assert len(safe) == 60 and all(row["state"] == "completed" for row in safe)
    assert len(cfr) == 60 and all(row["state"] == "completed_additive_review" for row in cfr)
    assert all(not row["destructive_cleanup"] and not row["history_rewrite"] and not row["sibling_mutation"] for row in cfr)


def test_exact_and_blocked_packets_remain_unexecuted() -> None:
    index = load("x2/portfolio/owner-execution-index.json")
    assert index["exact_approval"] == {"executed": 0, "planned": 20, "state": "exact_gate"}
    assert index["blocked"] == {"executed": 0, "planned": 10, "state": "open_gap_or_exact_gate"}
    assert len(x1_portfolio("exact_approval")) == 20
    assert len(x1_portfolio("blocked")) == 10


def test_gmut_board_has_zero_empirical_credit() -> None:
    board = load("x2/evidence/gmut-obligation-board.json")
    assert board["all_structurally_present"] is True
    assert board["real_observations"] == board["likelihoods"] == board["posteriors"] == board["constraints"] == 0
    assert board["theory_of_everything"] is False


def test_thos_freed_id_cbr_and_thermo_boundaries() -> None:
    thos = load("x2/evidence/thos-handover-proxy.json")
    freed = load("x2/evidence/freed-id-custody-graph.json")
    cbr = load("x2/evidence/cbr-authority-vacancy-matrix.json")
    thermo = load("x2/evidence/thermo-nonconversion-classifier.json")
    assert thos["real_people"] == thos["real_incidents"] == thos["matched_budget_arms"] == 0
    assert thos["effectiveness_estimate"] is None
    assert freed["real_identities"] == freed["real_keys"] == 0 and freed["production"] is False
    assert cbr["software_decisions"] == 0 and cbr["outcome"] == "exact_gate"
    assert {"consciousness", "personhood", "justice", "agency"} <= set(thermo["rejected_conversions"])


def test_source_use_has_zero_download_and_empirical_rows() -> None:
    receipt = load("x2/evidence/source-use-receipt.json")
    assert receipt["downloads"] == receipt["external_rows"] == receipt["real_stations"] == receipt["real_instruments"] == receipt["real_observations"] == receipt["real_calibration_or_maintenance_records"] == receipt["real_operators_or_shifts"] == receipt["real_forecasts_or_warnings"] == receipt["measurements"] == 0
    assert receipt["citations_are_observations"] is False
    assert receipt["professional_or_conformance_credit"] == 0


def test_accessible_static_report_structure_and_reservations() -> None:
    text = (PHASE_ROOT / "x2" / "reports" / "accessible-static-report.html").read_text(encoding="utf-8")
    assert "<caption>" in text
    assert 'scope="col"' in text and 'scope="row"' in text
    assert "focus-visible" in text and "@media print" in text
    assert "assistive technology" in text and "affected-user evaluation remain open" in text
    assert text.count("<tr>") == 41


def test_evidence_overview_is_substantive_and_bounded() -> None:
    path = PHASE_ROOT / "x2" / "reports" / "evidence-overview.md"
    text = path.read_text(encoding="utf-8")
    assert archive.word_count(path) >= 850
    assert "NOT_READY_FOR_STAGE_20" in text
    assert "zero real stations" in text.casefold()
    assert "not complete accessibility conformance" in text


def test_evidence_manifest_matches_git_blob_domain() -> None:
    manifest = load("x2/evidence/evidence-content-manifest.json")
    paths = [ROOT / row["path"] for row in manifest["entries"]]
    replay = {row["path"]: row for row in archive.manifest_rows(paths)}
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        assert replay[row["path"]]["git_blob_oid"] == row["git_blob_oid"]
        assert replay[row["path"]]["sha256"] == row["sha256"]
        assert replay[row["path"]]["bytes"] == row["bytes"]
    assert len(manifest["self_exclusions"]) == 1


def test_all_phase_json_parses() -> None:
    paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(paths) > 200
    for path in paths:
        json.loads(path.read_text(encoding="utf-8"))


def test_every_phase_document_is_within_word_cap() -> None:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt", ".html"}]
    oversized = {path.relative_to(PHASE_ROOT).as_posix(): archive.word_count(path) for path in paths if archive.word_count(path) > 6000}
    assert oversized == {}


def test_changed_python_has_no_dynamic_execution_or_shell_true() -> None:
    paths = [
        ROOT / "scripts" / "ghc_family_caelen_ash_v668_v6_controls.py",
        ROOT / "scripts" / "build_ghc_family_caelen_ash_v668_v6_x2.py",
        ROOT / "tests" / "test_ghc_family_caelen_ash_v668_v6_x2.py",
    ] + [ROOT / "scripts" / f"{name}.py" for name in archive.RUNNER_NAMES]
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                assert node.func.id not in {"eval", "exec", "compile"}
            if isinstance(node, ast.Call):
                assert not any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords)


def test_five_class_confirmed_payload_patterns_are_absent() -> None:
    adjudication = load("x2/evidence/privacy-adjudication.json")
    assert adjudication["candidate_count"] == 2
    assert adjudication["confirmed_hit_count"] == 0
    assert {row["disposition"] for row in adjudication["candidates"]} == {"scanner_definition_only"}
    patterns = [
        re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
        re.compile(r"source_thread_id\s*[:=]", re.I),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        re.compile(r"\b[A-Z]:\\Users\\[^\s\"']+", re.I),
        re.compile(r"<codex_delegation>|session_meta\.payload\.id|response_item", re.I),
        re.compile(r"\b(?:ssn|medical record number|patient identifier|participant identifier)\s*[:=]\s*\S+", re.I),
    ]
    for path in [p for p in PHASE_ROOT.rglob("*") if p.is_file() and p.suffix.lower() in {".json", ".md", ".txt", ".html"}]:
        text = path.read_text(encoding="utf-8")
        assert not any(pattern.search(text) for pattern in patterns), path


def test_no_final_or_successor_contact_during_x2() -> None:
    truth = load("x2/phase-truth.json")
    successor = load("x2/successor-recommendations.json")
    assert truth["successor_contacted"] is False
    assert successor["contacted"] is False
    assert successor["recipient"] == "unresolved_until_terminal_gate"
    assert successor["completion_credit"] == 0
    assert successor["execution_count"] == 0
    assert len(successor["candidates"]) == 15
    assert len(successor["skills"]) == 10
    assert len(successor["runners"]) == 10
    assert len(successor["clean_fix_refine"]) == 30
    assert not (PHASE_ROOT / "final").exists()
    assert not (PHASE_ROOT / "closeout").exists()
    assert not (PHASE_ROOT / "seal").exists()


def test_materialized_file_count_remains_below_ceiling() -> None:
    files = [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts]
    assert len(files) < 2000
