from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "neris-solane" / "v675-v4"
SOURCE_FINAL = "78f2d675771a9f37340d51c5e66c4a83a85fe6c0"
X1_COMMIT = "5bd78357eab01cf9a09f01648356411feedb2180"
EVIDENCE_COMMIT = "596c8d5cc2cd5f3408f5320b5fa8e15bfdfc0400"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
COUNTS = {
    "negatives": 40760,
    "methods": 29012,
    "failed_witnesses": 12421,
    "passing_witnesses": 16407,
    "open_gaps": 337,
    "exact_gates": 329,
    "proposal_chain": 7190,
}


def load(relative: str):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def git(*args: str) -> bytes:
    result = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=False)
    assert result.returncode == 0, result.stderr.decode("utf-8", errors="replace")
    return result.stdout


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_lifecycle_ancestry_precommit_or_exact_final():
    head = git("rev-parse", "HEAD").decode().strip()
    assert git("rev-parse", f"{X1_COMMIT}^").decode().strip() == SOURCE_FINAL
    assert git("rev-parse", f"{EVIDENCE_COMMIT}^").decode().strip() == X1_COMMIT
    if head == EVIDENCE_COMMIT:
        assert staged_blob("docs/neris-solane/v675-v4/final/phase-truth.json")
    else:
        assert git("rev-parse", f"{head}^").decode().strip() == EVIDENCE_COMMIT
        assert int(git("rev-list", "--count", f"{SOURCE_FINAL}..{head}").decode()) == 3
        assert int(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}").decode()) == 0


def test_exact_final_truth_and_counts():
    truth = load("docs/neris-solane/v675-v4/final/phase-truth.json")
    assert truth["outcomes"] == OUTCOMES
    assert truth["effective_counts"] == COUNTS
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["real_people"] == truth["real_objects"] == truth["external_actions"] == 0
    assert truth["authority_conferred"] is False


def test_retained_layers_and_no_erasure():
    retained = load("docs/neris-solane/v675-v4/final/retained-negative-register.json")
    assert retained["effective_counts"] == COUNTS
    assert sum(row["negatives"] for row in retained["additive_layers"]) == 180
    assert retained["failures_erased"] == retained["gates_erased"] == 0
    method = load("docs/neris-solane/v675-v4/final/method-flow-final.json")
    assert method["failures_rewritten"] == 0
    assert method["successful_aggregate_replayed"] is False


def test_gate_register_preserves_authority():
    gates = load("docs/neris-solane/v675-v4/final/open-exact-gate-register.json")
    assert gates["effective_open_gaps"] == 337
    assert gates["effective_exact_gates"] == 329
    assert len(gates["new_open_gaps"]) == 2
    assert len(gates["new_exact_gates"]) == 2
    assert gates["Maori_concepts_under_Maori_authority"] is True
    assert gates["authority_conferred"] is False


def test_content_seal_replays_exact_staged_blobs():
    seal = load("docs/neris-solane/v675-v4/closeout/content-seal.json")
    assert seal["entry_count"] == 9
    for entry in seal["entries"]:
        blob = staged_blob(entry["path"])
        assert len(blob) == entry["bytes"]
        assert hashlib.sha256(blob).hexdigest() == entry["sha256"]


def test_final_manifests_replay_exact_index():
    for relative in [
        "docs/neris-solane/v675-v4/validation/final-delta-manifest.json",
        "docs/neris-solane/v675-v4/validation/final-owner-manifest.json",
    ]:
        manifest = load(relative)
        assert manifest["entry_count"] == len(manifest["entries"])
        assert len({entry["path"] for entry in manifest["entries"]}) == manifest["entry_count"]
        for entry in manifest["entries"]:
            blob = staged_blob(entry["path"])
            assert len(blob) == entry["bytes"]
            assert hashlib.sha256(blob).hexdigest() == entry["sha256"]


def test_final_staged_review_and_privacy():
    review = load("docs/neris-solane/v675-v4/validation/final-staged-review.json")
    privacy = load("docs/neris-solane/v675-v4/validation/final-staged-privacy.json")
    assert review["passed"] is True
    assert all(value is True for value in review["checks"].values())
    assert privacy["confirmed_hit_count"] == 0
    assert privacy["privacy_complete_claim"] is False


def test_route_remains_prepared_not_sent():
    route = load("docs/neris-solane/v675-v4/final/route-state.json")
    assert route["prospective_successor_exact_title"] == "Vesper Arlen"
    assert route["prospective_successor_phase"] == "v675-v5"
    assert route["prepared"] is True
    assert route["sent"] is route["delivery_acknowledged"] is route["precontacted"] is False
    baton = (OWNER_ROOT / "handoffs" / "vesper-arlen-v675-v5-activation-candidate.md").read_text(encoding="utf-8")
    assert "PREPARED_NOT_SENT" in baton
    assert "SENT_BY_NERIS_SOLANE = false" in baton
    assert "DELIVERY_ACKNOWLEDGED = false" in baton


def test_baton_integrity_matches_closeout():
    closeout = load("docs/neris-solane/v675-v4/closeout/closeout-receipt.json")
    blob = staged_blob(closeout["baton_path"])
    assert len(blob) == closeout["baton_bytes"]
    assert len(blob.decode("utf-8").split()) == closeout["baton_words"]
    assert hashlib.sha256(blob).hexdigest() == closeout["baton_sha256"]
    assert closeout["baton_state"] == "PREPARED_NOT_SENT"


def test_final_static_report_structure():
    html = (OWNER_ROOT / "final" / "accessible-report.html").read_text(encoding="utf-8")
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


def test_no_private_absolute_path_or_raw_uuid_in_baton():
    baton = (OWNER_ROOT / "handoffs" / "vesper-arlen-v675-v5-activation-candidate.md").read_text(encoding="utf-8")
    assert not re.search(r"(?i)[a-z]:\\users\\", baton)
    assert not re.search(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", baton)


def test_checklists_wellbeing_and_validation_plan():
    checklist = load("docs/neris-solane/v675-v4/final/complete-incomplete-checklist.json")
    wellbeing = load("docs/neris-solane/v675-v4/final/wellbeing-check.json")
    plan = load("docs/neris-solane/v675-v4/final/validation-plan.json")
    assert checklist["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert wellbeing["working_language_only"] and wellbeing["corrigibility_preserved"]
    assert wellbeing["successor_precontacted"] is False
    assert plan["canonical_invocation_cap"] == 1
    assert plan["success_replay_allowed"] is False
    assert plan["full_repository_suite_planned"] is False


def test_owner_file_cap():
    manifest = load("docs/neris-solane/v675-v4/validation/final-owner-manifest.json")
    assert manifest["entry_count"] < 2000


def test_exact_four_core_outcome_labels():
    labels = {
        row["core_outcome"]
        for row in load("docs/neris-solane/v675-v4/x2/proposal-outcomes.json")["rows"]
    }
    assert labels == set(OUTCOMES)
