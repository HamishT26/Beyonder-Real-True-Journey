from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elaren-kestrel" / "v675-v3"
SOURCE_FINAL = "c1e3bd95e950c36d2fc137b5c9693d2c4b632cdc"
X1_COMMIT = "5775287f4ffdcf7cb169bbcf59cbd013c04a779f"
EVIDENCE_COMMIT = "dbc5699676042ba961b2dae870227f91163c5490"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
COUNTS = {
    "negatives": 40580,
    "methods": 28832,
    "failed_witnesses": 12241,
    "passing_witnesses": 16171,
    "open_gaps": 335,
    "exact_gates": 327,
    "proposal_chain": 7150,
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
        assert staged_blob("docs/elaren-kestrel/v675-v3/final/phase-truth.json")
    else:
        assert git("rev-parse", f"{head}^").decode().strip() == EVIDENCE_COMMIT
        assert int(git("rev-list", "--count", f"{SOURCE_FINAL}..{head}").decode()) == 3
        assert int(git("rev-list", "--merges", "--count", f"{SOURCE_FINAL}..{head}").decode()) == 0


def test_exact_final_truth_and_counts():
    truth = load("docs/elaren-kestrel/v675-v3/final/phase-truth.json")
    assert truth["outcomes"] == OUTCOMES
    assert truth["effective_counts"] == COUNTS
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["real_people"] == truth["real_objects"] == truth["external_actions"] == 0
    assert truth["authority_conferred"] is False


def test_retained_layers_and_no_erasure():
    retained = load("docs/elaren-kestrel/v675-v3/final/retained-negative-register.json")
    assert retained["effective_counts"] == COUNTS
    assert sum(row["negatives"] for row in retained["elaren_layers"]) == 173
    assert retained["failures_erased"] == retained["gates_erased"] == 0
    method = load("docs/elaren-kestrel/v675-v3/final/method-flow-final.json")
    assert method["failures_rewritten"] == 0
    assert method["successful_aggregate_replayed"] is False


def test_gate_register_preserves_authority():
    gates = load("docs/elaren-kestrel/v675-v3/final/open-exact-gate-register.json")
    assert gates["effective_open_gaps"] == 335
    assert gates["effective_exact_gates"] == 327
    assert len(gates["new_open_gaps"]) == 2
    assert len(gates["new_exact_gates"]) == 2
    assert gates["Maori_concepts_under_Maori_authority"] is True
    assert gates["authority_conferred"] is False


def test_content_seal_replays_exact_staged_blobs():
    seal = load("docs/elaren-kestrel/v675-v3/closeout/content-seal.json")
    assert seal["entry_count"] == 9
    for entry in seal["entries"]:
        blob = staged_blob(entry["path"])
        assert len(blob) == entry["bytes"]
        assert hashlib.sha256(blob).hexdigest() == entry["sha256"]


def test_final_manifests_replay_exact_index():
    for relative in [
        "docs/elaren-kestrel/v675-v3/validation/final-delta-manifest.json",
        "docs/elaren-kestrel/v675-v3/validation/final-owner-manifest.json",
    ]:
        manifest = load(relative)
        assert manifest["entry_count"] == len(manifest["entries"])
        assert len({entry["path"] for entry in manifest["entries"]}) == manifest["entry_count"]
        for entry in manifest["entries"]:
            blob = staged_blob(entry["path"])
            assert len(blob) == entry["bytes"]
            assert hashlib.sha256(blob).hexdigest() == entry["sha256"]


def test_final_staged_review_and_privacy():
    review = load("docs/elaren-kestrel/v675-v3/validation/final-staged-review.json")
    privacy = load("docs/elaren-kestrel/v675-v3/validation/final-staged-privacy.json")
    assert review["passed"] is True
    assert all(value is True for value in review["checks"].values())
    assert privacy["confirmed_hit_count"] == 0
    assert privacy["privacy_complete_claim"] is False


def test_route_remains_prepared_not_sent():
    route = load("docs/elaren-kestrel/v675-v3/final/route-state.json")
    assert route["prospective_successor_exact_title"] == "Neris Solane"
    assert route["prospective_successor_phase"] == "v675-v4"
    assert route["prepared"] is True
    assert route["sent"] is route["delivery_acknowledged"] is route["precontacted"] is False
    baton = (OWNER_ROOT / "handoffs" / "neris-solane-v675-v4-activation-candidate.md").read_text(encoding="utf-8")
    assert "PREPARED_NOT_SENT" in baton
    assert "SENT_BY_ELAREN_KESTREL = false" in baton
    assert "DELIVERY_ACKNOWLEDGED = false" in baton


def test_baton_integrity_matches_closeout():
    closeout = load("docs/elaren-kestrel/v675-v3/closeout/closeout-receipt.json")
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
    baton = (OWNER_ROOT / "handoffs" / "neris-solane-v675-v4-activation-candidate.md").read_text(encoding="utf-8")
    assert not re.search(r"(?i)[a-z]:\\users\\", baton)
    assert not re.search(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", baton)


def test_checklists_wellbeing_and_validation_plan():
    checklist = load("docs/elaren-kestrel/v675-v3/final/complete-incomplete-checklist.json")
    wellbeing = load("docs/elaren-kestrel/v675-v3/final/wellbeing-check.json")
    plan = load("docs/elaren-kestrel/v675-v3/final/validation-plan.json")
    assert checklist["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert wellbeing["working_language_only"] and wellbeing["corrigibility_preserved"]
    assert wellbeing["successor_precontacted"] is False
    assert plan["canonical_invocation_cap"] == 1
    assert plan["success_replay_allowed"] is False
    assert plan["full_repository_suite_planned"] is False


def test_owner_file_cap():
    manifest = load("docs/elaren-kestrel/v675-v3/validation/final-owner-manifest.json")
    assert manifest["entry_count"] < 2000


def test_exact_four_core_outcome_labels():
    labels = {
        row["core_outcome"]
        for row in load("docs/elaren-kestrel/v675-v3/x2/proposal-outcomes.json")["rows"]
    }
    assert labels == set(OUTCOMES)
