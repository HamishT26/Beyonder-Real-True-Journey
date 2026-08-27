from __future__ import annotations

import hashlib
import io
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v673-v3"
SOURCE = "62364ecf3f66d938c539574ad2456dacd6cebd81"
X1 = "d2215698d40dae2bdc5a9a4a6ff1bce4c5fef608"
EVIDENCE = "be1bcf5beab24faec320f3d86bff51ea221ad22e"


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, stderr = process.communicate(input=("\n".join(f":{path}" for path in paths) + "\n").encode("utf-8"), timeout=300)
    assert process.returncode == 0, stderr.decode("utf-8", errors="replace")
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode("utf-8").strip().split()
        assert len(header) == 3 and header[1] == "blob"
        size = int(header[2])
        result[path] = stream.read(size)
        assert stream.read(1) == b"\n"
    assert not stream.read()
    return result


def test_phase_truth_has_exact_anchors() -> None:
    truth = load("closeout/phase-truth.json")
    assert truth["source"] == SOURCE and truth["x1"] == X1 and truth["evidence"] == EVIDENCE
    assert truth["final"] is None


def test_outcomes_are_exact() -> None:
    assert load("closeout/phase-truth.json")["outcome_counts"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}


def test_declared_chain_is_6350() -> None:
    truth = load("closeout/phase-truth.json")
    assert truth["declared_source_chain"] == 6310
    assert truth["declared_result_chain"] == 6350


def test_layered_counts_are_exact() -> None:
    layers = load("closeout/phase-truth.json")["repository_layers"]
    assert layers["caelen_repository_seal"]["negatives"] == 36594
    assert layers["eiren_activation_baseline"]["negatives"] == 36595
    assert layers["eiren_sealed_totals"]["negatives"] == 36817
    assert layers["eiren_sealed_totals"]["methods"] == 23145


def test_method_flow_has_222_pairs() -> None:
    flow = load("closeout/method-flow-final.json")
    assert flow["phase_method_count"] == 222
    assert flow["phase_failed_witness_count"] == flow["phase_passing_witness_count"] == 222
    assert len(flow["witnesses"]) == 444


def test_retained_negative_rows_are_zero_credit() -> None:
    register = load("closeout/retained-negative-register.json")
    assert register["phase_negative_count"] == 222
    assert register["effective_negative_count"] == 36817
    assert all(row["retained"] and row["credit"] == 0 for row in register["phase_rows"])


def test_open_and_exact_gate_totals_are_exact() -> None:
    gates = load("closeout/open-exact-gate-register.json")
    assert gates["effective_open_gaps"] == 297
    assert gates["effective_exact_gates"] == 290
    assert len(gates["rows"]) == 4


def test_route_is_prepared_not_sent() -> None:
    route = load("route/route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["recipient_selected"] is False and route["recipient"] is None
    assert route["message_count"] == 0 and route["acknowledgement"] is False


def test_handoff_candidate_word_window_and_truth() -> None:
    text = (OWNER_ROOT / "handoffs/post-gate-successor-activation-candidate.md").read_text(encoding="utf-8")
    assert 10000 <= len(text.split()) <= 100000
    assert "PREPARED_BY_EIREN_KESTREL = true" in text
    assert "SENT_BY_EIREN_KESTREL = false" in text


def test_handoff_contains_no_raw_uuid_or_private_path() -> None:
    text = (OWNER_ROOT / "handoffs/post-gate-successor-activation-candidate.md").read_text(encoding="utf-8")
    assert re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", text, re.IGNORECASE) is None
    assert re.search(r"[A-Za-z]:\\Users\\|/Users/|/home/", text, re.IGNORECASE) is None


def test_final_validation_is_still_pending_in_commit_candidate() -> None:
    prerequisites = load("final/final-validation-prerequisites.json")
    assert prerequisites["state"] == "PENDING_FINAL_COMMIT"
    assert prerequisites["canonical_runs_completed"] == 0
    assert prerequisites["success_replay_allowed"] is False


def test_full_repository_suite_is_not_selected() -> None:
    selection = load("validation/final-test-selection.json")
    assert selection["expected_total"] == 107
    assert selection["full_repository_suite"] is False


def test_content_seal_replays() -> None:
    seal = load("seal/content-seal.json")
    assert seal["entry_count"] == 9
    for row in seal["entries"]:
        blob = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_final_owner_manifest_replays_when_present() -> None:
    path = OWNER_ROOT / "validation/final-owner-manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    blobs = batch_index_blobs([row["path"] for row in manifest["entries"]])
    assert manifest["entry_count"] == len(manifest["entries"])
    for row in manifest["entries"]:
        blob = blobs[row["path"]]
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == row["sha256"]


def test_final_delta_manifest_replays_when_present() -> None:
    path = OWNER_ROOT / "validation/final-delta-manifest.json"
    if not path.exists():
        return
    manifest = json.loads(path.read_text(encoding="utf-8"))
    blobs = batch_index_blobs([row["path"] for row in manifest["entries"]])
    for row in manifest["entries"]:
        blob = blobs[row["path"]]
        assert hashlib.sha256(blob.replace(b"\r\n", b"\n")).hexdigest() == row["sha256"]


def test_final_privacy_scan_has_zero_confirmed_hits_when_present() -> None:
    path = OWNER_ROOT / "validation/final-staged-privacy.json"
    if path.exists():
        assert load("validation/final-staged-privacy.json")["confirmed_hit_count"] == 0


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)


def test_accessible_report_has_landmarks_and_table() -> None:
    parser = StructureParser()
    parser.feed((OWNER_ROOT / "reports/accessible-final-report.html").read_text(encoding="utf-8"))
    for tag in ["header", "nav", "main", "section", "table", "caption", "footer"]:
        assert tag in parser.tags


def test_accessible_report_reserves_manual_evaluation() -> None:
    text = (OWNER_ROOT / "reports/accessible-final-report.html").read_text(encoding="utf-8")
    for phrase in ["assistive-technology", "Māori-language", "cognitive-accessibility", "affected-user"]:
        assert phrase in text


def test_complete_incomplete_keeps_stage20_incomplete() -> None:
    checklist = load("closeout/complete-incomplete-checklist.json")
    assert "Stage 20" in checklist["incomplete"]
    assert checklist["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"


def test_wellbeing_is_relational_and_preserves_pause_right() -> None:
    wellbeing = load("closeout/wellbeing-workload-check.json")
    assert wellbeing["relational_only"] is True
    assert wellbeing["pause_right_preserved"] is True
    assert wellbeing["human_workload_claim"] is False


def test_source_external_digests_are_file_backed_without_replay() -> None:
    source = load("closeout/source-and-provenance.json")
    assert source["external_digest_file_location_materialized"] is True
    assert source["source_validation_replayed"] is False


def test_no_install_or_update_was_performed() -> None:
    receipt = load("x2/environment-version-receipt.json")
    assert receipt["installations_performed"] == receipt["updates_performed"] == 0
    assert receipt["bandit_gap_retained"] is True


def test_owner_file_and_word_ceilings() -> None:
    files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
    assert len(files) <= 2000
    assert all(len(path.read_text(encoding="utf-8").split()) <= 100000 for path in files)


def test_closeout_receipt_matches_truth() -> None:
    receipt = load("closeout/closeout-receipt.json")
    assert receipt["phase_methods"] == 222
    assert receipt["sealed_totals"]["negatives"] == 36817
    assert receipt["route_state"] == "PREPARED_NOT_SENT"


def test_terminal_verdict_remains_not_ready() -> None:
    assert load("closeout/phase-truth.json")["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
