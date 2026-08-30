from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "sylven-arc" / "v676-v7"
FINAL = BASE / "final"
SOURCE = "b8e8b258876b5af3b3e3247f42ac58dde9a7e6a4"
X1 = "b9861f8aaed6f98606e5370ad0f11918865b3433"
EVIDENCE = "dee3fe5b0909b14ca3b807d702e36f6ced478ff0"
BRANCH = "codex/GHC-Family/sylven-arc-v676-v7-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(["git", "-C", str(REPO), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def test_final_phase_truth_is_exact_and_nonpromotional() -> None:
    truth = load(FINAL / "phase-truth.json")
    assert truth["owner"] == "Sylven Arc"
    assert truth["phase"] == "v676-v7"
    assert truth["source"] == SOURCE and truth["x1"] == X1 and truth["evidence"] == EVIDENCE
    assert truth["declared_proposal_chain_before"] == 7630
    assert truth["declared_proposal_chain_after"] == 7670
    assert truth["new_sylven_proposals"] == 40
    assert truth["outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["canonical_state"] == "PENDING_EXACT_PUSHED_FINAL"
    assert truth["real_world_rows"] == truth["observed_measurements"] == truth["external_actions"] == 0


def test_final_method_flow_preserves_all_failures_and_recoveries() -> None:
    flow = load(FINAL / "method-flow-ledger.json")
    assert flow["phase_ledger_counts"] == {"methods": 674, "failed": 217, "passing": 457}
    assert flow["current_overlay"] == {
        "effective_negatives": 42883,
        "effective_methods": 34482,
        "retained_failed_witnesses": 14544,
        "bounded_passing_witnesses": 20627,
        "open_gaps": 361,
        "exact_gates": 353,
    }
    methods = flow["methods"]
    ids = {row["method_id"] for row in methods}
    failed = [row for row in methods if row["truth"] is False]
    passing = [row for row in methods if row["truth"] is True]
    assert len(methods) == len(ids) == 674
    assert len(failed) == 217 and len(passing) == 457
    assert all(row["status"] in {"failed_zero_credit", "rejected_negative_zero_credit"} for row in failed)
    assert all(row["recovered_by"] in ids for row in failed)
    assert flow["failure_erasure_forbidden"] is True


def test_retained_negative_register_has_zero_conversion() -> None:
    register = load(FINAL / "retained-negative-register.json")
    assert register["activation_baseline"] == 42666
    assert register["phase_failed_witnesses"] == 217
    assert register["current_effective_negatives"] == 42883
    assert register["converted_to_pass"] == 0
    assert len(register["failed_witnesses"]) == 217


def test_outcomes_and_rejecting_mutations_are_exact() -> None:
    outcome = load(BASE / "x2" / "proposal-outcomes.json")
    assert len(outcome["outcomes"]) == 40
    assert set(row["outcome"] for row in outcome["outcomes"]) == LABELS
    assert Counter(row["outcome"] for row in outcome["outcomes"]) == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    mutation = load(BASE / "x2" / "mutation-summary.json")
    assert mutation == {"preregistered": 160, "executed": 160, "rejected": 160, "failed_witnesses_retained": 160}


def test_skill_runner_and_portfolio_truth_is_bounded() -> None:
    truth = load(FINAL / "skill-runner-truth.json")
    assert truth["global_install_count"] == 0
    assert truth["skills"]["count"] == 20 and truth["skills"]["global_installs"] == 0
    assert truth["runners"]["count"] == 10
    assert all(row["positive"] and row["invalid_rejected"] for row in truth["runners"]["runners"])
    portfolio = load(FINAL / "portfolio-truth.json")
    assert portfolio["exact_or_blocked_executed"] == 0
    assert portfolio["execution"]["safe_now_completed"] == 60
    assert portfolio["execution"]["candidate_completed_without_core_promotion"] == 30
    assert portfolio["execution"]["clean_fix_refine_completed"] == 60
    assert portfolio["execution"]["exact_approval_unexecuted"] == 20
    assert portfolio["execution"]["blocked_unexecuted"] == 10


def test_gap_and_gate_registers_are_exact() -> None:
    gaps = load(FINAL / "open-gap-register.json")
    gates = load(FINAL / "exact-gate-register.json")
    assert gaps["inherited"] == 359 and gaps["new"] == 2 and gaps["current"] == 361
    assert gates["inherited"] == 351 and gates["new"] == 2 and gates["current"] == 353
    assert gates["exact_approval_packets_unexecuted"] == 20
    assert gates["blocked_packets_unexecuted"] == 10


def test_source_and_proposal_ledger_retains_bounded_novelty() -> None:
    ledger = load(FINAL / "source-and-proposal-ledger.json")
    assert ledger["source"] == SOURCE and ledger["x1"] == X1 and ledger["evidence"] == EVIDENCE
    assert ledger["declared_chain_before"] == 7630 and ledger["declared_chain_after"] == 7670
    assert ledger["proposal_count"] == 40
    assert ledger["universal_novelty_proved"] is False
    assert ledger["semantic_audit"]["exact_title_collisions"] == 0
    assert ledger["semantic_audit"]["selected_rows_quarantined"] == 0


def test_complete_incomplete_and_wellbeing_boundaries_are_visible() -> None:
    checklist = load(FINAL / "complete-incomplete-checklist.json")
    assert len(checklist["complete"]) >= 6 and len(checklist["incomplete"]) >= 6
    assert any("Māori-authority" in row for row in checklist["incomplete"])
    wellbeing = load(FINAL / "wellbeing-workload-check.json")
    assert wellbeing["relational_language_only"] is True
    assert wellbeing["workload"] == "bounded"
    assert wellbeing["owner_added_files_before_final"] < wellbeing["owner_file_stop"] == 2000
    assert wellbeing["document_word_stop"] == 100000 and wellbeing["phase_commit_stop"] == 8


def test_scientific_identity_and_authority_boundaries_hold() -> None:
    boundary = load(FINAL / "scientific-authority-boundaries.json")
    assert "research-model family only" in boundary["gmut"]
    assert "zero-person proxy" in boundary["thos"]
    assert "zero real keys" in boundary["freed_id"]
    assert "exact-gated" in boundary["cbr"]
    assert boundary["theory_of_everything_proved"] is False
    assert boundary["agi_or_asi_evidence"] is False
    assert boundary["consciousness_or_personhood_evidence"] is False
    assert boundary["stage20_ready"] is False


def test_privacy_and_accessibility_reservations_hold() -> None:
    boundary = load(FINAL / "privacy-accessibility-boundaries.json")
    for field in ("raw_task_identifiers", "private_routes", "credentials_or_tokens", "transcripts_or_screenshots", "real_people_or_records"):
        assert boundary[field] == 0
    for field in ("accessibility_complete", "manual_assistive_technology_review", "cognitive_review", "affected_user_review", "maori_language_review"):
        assert boundary[field] is False


def test_static_report_is_structurally_accessible_but_not_conformance_claim() -> None:
    value = (BASE / "closeout" / "static-report.html").read_text(encoding="utf-8")
    for token in ("<!doctype html>", "<html lang=\"en\">", "<meta charset=\"utf-8\">", "<main>", "<h1>", "<h2>"):
        assert token in value
    assert "Accessibility remains incomplete" not in value
    assert "remain open" in value
    assert "NOT_READY_FOR_STAGE_20" in value


def test_route_is_prepared_not_sent_and_has_no_selected_successor() -> None:
    route = load(BASE / "orchestration" / "route-state-prepared.json")
    assert route["status"] == "PREPARED_NOT_SENT"
    assert route["successor_selected"] is route["successor_contacted"] is route["standby_contacted"] is False
    candidate = (BASE / "handoffs" / "next-owner-activation-candidate.md").read_text(encoding="utf-8")
    assert "PREPARED_NOT_SENT" in candidate
    assert "selects no recipient" in candidate


def test_content_seal_replays_current_precommit_files() -> None:
    seal = load(BASE / "seal" / "content-seal.json")
    assert seal["source"] == SOURCE and seal["x1"] == X1 and seal["evidence"] == EVIDENCE
    assert seal["entry_count"] == len(seal["entries"]) >= 20
    for row in seal["entries"]:
        raw = (REPO / row["path"]).read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert hashlib.sha256(raw).hexdigest() == row["sha256_normalized_lf"]


def test_final_manifests_replay_exact_git_blobs() -> None:
    for name in ("final-delta-manifest.json", "final-owner-manifest.json"):
        manifest = load(BASE / "validation" / name)
        assert manifest["entry_count"] == len(manifest["entries"])
        for row in manifest["entries"]:
            raw = git("cat-file", "-p", row["git_blob_oid"], binary=True)
            normalized = raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
            assert hashlib.sha256(normalized).hexdigest() == row["sha256_normalized_lf"]
    review = load(BASE / "validation" / "final-staged-review.json")
    assert review["unexpected_paths"] == []
    assert review["confirmed_privacy_or_raw_identifier_hits"] == 0
    assert review["status"] == "VALID_EXACT_FINAL_STAGED_REVIEW"


def test_x1_and_evidence_lifecycle_boundaries_hold_in_exact_commits() -> None:
    x1_paths = [path for path in git("ls-tree", "-r", "--name-only", X1, "--", "docs/sylven-arc/v676-v7", "scripts", "tests").splitlines() if path.startswith("docs/sylven-arc/v676-v7/") or "sylven_arc_v676_v7" in path]
    evidence_paths = [path for path in git("ls-tree", "-r", "--name-only", EVIDENCE, "--", "docs/sylven-arc/v676-v7", "scripts", "tests").splitlines() if path.startswith("docs/sylven-arc/v676-v7/") or "sylven_arc_v676_v7" in path]
    assert not any("/x2/" in path or "/final/" in path or "/closeout/" in path or "/handoffs/" in path for path in x1_paths)
    assert not any("/final/" in path or "/closeout/" in path or "/handoffs/" in path or "_final.py" in path for path in evidence_paths)
    assert git("rev-parse", f"{X1}^") == SOURCE
    assert git("rev-parse", f"{EVIDENCE}^") == X1


def test_current_or_precommit_topology_is_direct_single_parent_and_zero_merge() -> None:
    assert git("branch", "--show-current") == BRANCH
    head = git("rev-parse", "HEAD")
    if head == EVIDENCE:
        assert git("diff", "--cached", "--name-only")
    else:
        assert git("rev-parse", "HEAD^") == EVIDENCE
        assert git("rev-list", "--count", f"{SOURCE}..HEAD") == "3"
        assert git("rev-list", "--merges", "--count", f"{SOURCE}..HEAD") == "0"
        assert len(git("rev-list", "--parents", "-n", "1", "HEAD").split()) == 2


def test_all_phase_json_parses_and_documents_stay_below_caps() -> None:
    json_paths = list(BASE.rglob("*.json"))
    assert len(json_paths) >= 500
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    docs = [path for path in BASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html"}]
    assert len(docs) >= 24
    assert max(len(path.read_text(encoding="utf-8").split()) for path in docs) <= 100_000


def test_owner_documents_contain_no_confirmed_private_payload() -> None:
    patterns = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
        re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    ]
    for path in BASE.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".html", ".txt", ".yaml", ".yml"}:
            continue
        value = path.read_text(encoding="utf-8")
        assert not any(pattern.search(value) for pattern in patterns), path.relative_to(REPO)
