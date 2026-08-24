from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "ilyra-fen" / "v668-v3"
SOURCE_FINAL = "da0d852ccacbfc228f7257888691b809a280ad86"
INITIAL_X1_HEAD = "c7954ae5efdffd58ca2f53d8fe9abd7530e7a49b"
X1_HEAD = "c9cde9ebf7f39c7a3b4b4cf4775fd9426bba4e52"
EVIDENCE_HEAD = "a22360acce1a200ef852a97110cc8da12497775b"
OWNER_MANIFEST = "docs/ilyra-fen/v668-v3/validation/final-owner-manifest.json"
DELTA_MANIFEST = "docs/ilyra-fen/v668-v3/validation/final-delta-manifest.json"


def load(relative: str) -> dict:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str, check: bool = True) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=check, text=True, encoding="utf-8"
    ).stdout.strip()


def git_bytes(*args: str) -> bytes:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout


def replay_manifest(relative: str) -> int:
    manifest = load(relative.removeprefix("docs/ilyra-fen/v668-v3/"))
    for row in manifest["entries"]:
        data = git_bytes("show", f":{row['path']}")
        assert git("rev-parse", f":{row['path']}") == row["git_blob_oid"]
        assert hashlib.sha256(data).hexdigest() == row["sha256"]
        assert len(data) == row["bytes"]
    return len(manifest["entries"])


def mutation_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted((PHASE_ROOT / "x2/mutations").glob("results-*.json")):
        rows.extend(json.loads(path.read_text(encoding="utf-8"))["results"])
    return rows


def test_exact_lifecycle_anchors_and_commit_shape() -> None:
    assert git("rev-parse", f"{INITIAL_X1_HEAD}^") == SOURCE_FINAL
    assert git("rev-parse", f"{X1_HEAD}^") == INITIAL_X1_HEAD
    assert git("rev-parse", f"{EVIDENCE_HEAD}^") == X1_HEAD
    assert git("rev-list", "--count", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}") == "3"
    assert git("rev-list", "--merges", f"{SOURCE_FINAL}..{EVIDENCE_HEAD}") == ""
    head = git("rev-parse", "HEAD")
    if head != EVIDENCE_HEAD:
        assert git("rev-parse", "HEAD^") == EVIDENCE_HEAD
        assert git("rev-list", "--count", f"{SOURCE_FINAL}..HEAD") == "4"
        assert git("rev-list", "--merges", f"{SOURCE_FINAL}..HEAD") == ""
        assert len(git("rev-list", "--parents", "-n", "1", "HEAD").split()) - 1 == 1


def test_final_truth_counts_and_verdict_are_exact() -> None:
    truth = load("final/phase-truth.json")
    assert truth["allowed_outcomes"] == ["completed", "represented", "open_gap", "exact_gate"]
    assert truth["outcome_counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["frozen_proposal_chain"] == 4710
    assert truth["repository_sealed_counts"] == {
        "effective_negatives": 29399,
        "methods": 15985,
        "failed_witnesses": 1700,
        "passing_witnesses": 2533,
        "open_gaps": 213,
        "exact_gates": 208,
    }
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["canonical_validation_invoked"] is False
    assert truth["successor_contacted"] is False


def test_retained_negative_arithmetic_and_final_method_flow() -> None:
    retained = load("closeout/retained-negative-register.json")
    assert 29218 + 12 + 6 + 3 + 160 == retained["effective_negatives_before_canonical"]
    assert retained["effective_negatives_before_canonical"] == 29399
    assert retained["all_failures_retained"] is True
    assert retained["correction_erases_failure"] is False
    ledger = load("method-flow/final-operational.json")
    assert ledger["counts"] == {"methods": 3, "failed_witnesses": 3, "passing_witnesses": 3, "retained_negatives": 3}
    assert all(row["recommendation_state"] == "preferred" for row in ledger["methods"])
    assert [row["result"] for row in ledger["witnesses"]] == ["fail", "pass", "fail", "pass", "fail", "pass"]


def test_open_gaps_and_exact_gates_remain_visible() -> None:
    gaps = load("closeout/open-gap-register.json")
    gates = load("closeout/exact-gate-register.json")
    assert gaps["effective_open_gaps"] == 213 and gaps["none_silently_closed"] is True
    assert gates["effective_exact_gates"] == 208 and gates["none_silently_closed"] is True
    assert len(gaps["new_gaps"]) == 2
    assert len(gates["new_gates"]) == 2


def test_outcomes_mutations_and_portfolio_remain_exact() -> None:
    outcomes = load("x2/proposals/outcome-index.json")
    assert outcomes["outcome_counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    rows = mutation_rows()
    assert len(rows) == 160
    assert all(row["state"] == "rejected" for row in rows)
    portfolio = load("final/portfolio-receipt.json")
    assert portfolio["safe_now_completed"] == 60
    assert portfolio["candidates_completed_boundedly"] == 30
    assert portfolio["skills_built_and_smoke_used"] == 20
    assert portfolio["runners_built_and_accept_reject_used"] == 10
    assert portfolio["clean_fix_refine_completed_additively"] == 30
    assert portfolio["exact_packets_unexecuted"] == 20
    assert portfolio["blocked_packets_unexecuted"] == 10
    assert portfolio["global_installations"] == 0


def test_x1_and_x2_are_immutable_during_closeout() -> None:
    changed = git(
        "diff", "--cached", "--name-only", EVIDENCE_HEAD, "--",
        "docs/ilyra-fen/v668-v3/x1", "docs/ilyra-fen/v668-v3/x2",
        "scripts/ghc_family_ilyra_fen_v668_v3_archive.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_x1.py",
        "scripts/build_ghc_family_ilyra_fen_v668_v3_x2.py",
        "scripts/ghc_family_ilyra_fen_v668_v3_controls.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_x1.py",
        "tests/test_ghc_family_ilyra_fen_v668_v3_x2.py",
    )
    assert changed == ""


def test_final_manifests_replay_in_git_blob_domain() -> None:
    delta = load("validation/final-delta-manifest.json")
    owner = load("validation/final-owner-manifest.json")
    assert delta["entry_count"] == replay_manifest(DELTA_MANIFEST)
    assert owner["entry_count"] == replay_manifest(OWNER_MANIFEST)
    assert delta["self_exclusions"] == [DELTA_MANIFEST, OWNER_MANIFEST]
    assert owner["self_exclusions"] == [OWNER_MANIFEST]
    assert len({row["path"] for row in owner["entries"]}) == owner["entry_count"]


def test_route_is_prepared_not_sent_and_unresolved() -> None:
    route = load("route/prepared-route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["successor_exact_title"] == "UNRESOLVED_UNTIL_TERMINAL_GATE"
    assert route["successor_phase"] == "UNRESOLVED_UNTIL_TERMINAL_GATE"
    assert route["successor_contacted"] is False
    assert route["task_created"] is False
    assert route["fork_created"] is False
    assert route["subagent_spawned"] is False
    assert route["single_send_maximum"] == 1


def test_canonical_plan_is_owner_scoped_and_not_invoked() -> None:
    credit = load("validation/validation-credit.json")
    plan = load("validation/canonical-plan.json")
    assert credit["state"] == "NOT_INVOKED"
    assert credit["canonical_invocation_count"] == 0
    assert credit["canonical_success_count"] == 0
    assert credit["post_success_replay_allowed"] is False
    assert plan["full_repository_suite"] is False
    assert plan["invocation_limit"] == 1
    assert plan["success_limit"] == 1
    assert plan["post_success_replay"] is False


def test_source_environment_and_accessibility_boundaries() -> None:
    sources = load("final/source-ledger.json")
    environment = load("final/environment-receipt.json")
    accessibility = load("final/accessibility-reservation.json")
    assert sources["downloads"] == 0 and sources["empirical_rows"] == 0 and sources["measurements"] == 0
    assert sources["citations_are_evidence_of_observation"] is False
    assert environment["verified_only"] is True
    assert environment["desktop_application_updated_by_phase"] is False
    assert environment["elevation"] is False
    assert environment["host_security_changed"] is False
    assert accessibility["complete_accessibility_claim"] is False
    assert "assistive technology" in accessibility["reserved"]
    assert "affected-user evaluation" in accessibility["reserved"]


def test_privacy_candidate_disposition_is_explicit() -> None:
    disposition = load("x2/evidence/privacy-candidate-disposition.json")
    assert disposition["raw_candidates"] == 1
    assert disposition["scanner_literal_candidates"] == 1
    assert disposition["confirmed_payload_hits"] == 0
    assert disposition["dispositions"][0]["confirmed_payload"] is False


def test_integrated_overview_and_handoff_basis_are_substantive_and_bounded() -> None:
    overview = (PHASE_ROOT / "final/integrated-overview.md").read_text(encoding="utf-8")
    basis = (PHASE_ROOT / "handoffs/successor-terminal-basis.md").read_text(encoding="utf-8")
    assert len(re.findall(r"\b\w+[\w'-]*\b", overview)) >= 1300
    assert "NOT_READY_FOR_STAGE_20" in overview
    assert "zero real films" in overview.casefold()
    assert "PREPARED_NOT_SENT" in basis
    assert "UNRESOLVED" not in basis
    assert "SENT_BY_ILYRA_FEN = false" in basis
    assert "consciousness" in basis and "Maori" in basis and "independent reproduction" in basis


def test_all_owner_json_parses_and_documents_fit_word_cap() -> None:
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    assert len(json_paths) > 210
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    oversized = {}
    for path in PHASE_ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".json", ".md", ".txt", ".html"}:
            words = len(re.findall(r"\b\w+[\w'-]*\b", path.read_text(encoding="utf-8")))
            if words > 6000:
                oversized[path.relative_to(PHASE_ROOT).as_posix()] = words
    assert oversized == {}


def test_materialized_file_count_and_commit_ceiling() -> None:
    materialized = sum(1 for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts)
    assert materialized < 2000
    history = load("closeout/source-to-final-history.json")
    assert history["expected_source_to_final_commits"] == 4
    assert history["hard_commit_ceiling"] == 8
    assert history["expected_merge_count"] == 0
    assert history["final_hash_supplied_external_after_commit"] is True


def test_seal_has_no_impossible_self_hash_or_promotion() -> None:
    seal = load("seal/content-seal.json")
    receipt = load("seal/final-receipt.json")
    assert seal["self_hash_claim"] is False
    assert seal["expected_final_parent"] == EVIDENCE_HEAD
    assert receipt["state"] == "CONTENT_SEALED_PENDING_EXACT_FINAL_CANONICAL"
    assert receipt["canonical_invoked"] is False
    assert receipt["independent_reproduction"] is False
    assert receipt["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
