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
OWNER_ROOT = ROOT / "docs" / "elaren-kestrel" / "v673-v4"
SOURCE = "ab37cd3be0fcfb4ae913c48779851340aa2c1e0c"
X1 = "67c6baceb91e76a80f62ea39cf3724c4ec0b991a"
EVIDENCE = "a16b97e83258547cc0a39f3b92f3d78517e9e29c"


def load(relative: str) -> Any:
    return json.loads((OWNER_ROOT / relative).read_text(encoding="utf-8"))


def batch_index_blobs(paths: list[str]) -> dict[str, bytes]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(f":{path}" for path in paths) + "\n").encode(), timeout=300
    )
    assert process.returncode == 0, stderr.decode("utf-8", errors="replace")
    stream = io.BytesIO(output)
    result: dict[str, bytes] = {}
    for path in paths:
        header = stream.readline().decode().strip().split()
        assert len(header) == 3 and header[1] == "blob"
        size = int(header[2])
        result[path] = stream.read(size)
        assert stream.read(1) == b"\n"
    assert not stream.read()
    return result


def test_exact_anchors_outcomes_and_chain() -> None:
    truth = load("closeout/phase-truth.json")
    assert (truth["source"], truth["x1"], truth["evidence"], truth["final"]) == (
        SOURCE,
        X1,
        EVIDENCE,
        None,
    )
    assert truth["outcome_counts"] == {
        "completed": 28,
        "represented": 8,
        "open_gap": 2,
        "exact_gate": 2,
    }
    assert (truth["declared_source_chain"], truth["declared_result_chain"]) == (6350, 6390)


def test_layered_counts_are_exact() -> None:
    layers = load("closeout/phase-truth.json")["repository_layers"]
    assert layers["eiren_repository_seal"]["negatives"] == 36817
    assert layers["elaren_activation_baseline"]["negatives"] == 36821
    assert layers["elaren_sealed_totals"] == {
        "negatives": 37035,
        "methods": 23363,
        "failed_witnesses": 8696,
        "passing_witnesses": 10926,
        "open_gaps": 299,
        "exact_gates": 292,
    }


def test_method_flow_has_214_retained_pairs() -> None:
    flow = load("closeout/method-flow-final.json")
    assert flow["phase_method_count"] == 214
    assert flow["phase_failed_witness_count"] == flow["phase_passing_witness_count"] == 214
    assert len(flow["methods"]) == 214 and len(flow["witnesses"]) == 428
    assert all(row["retained"] and row["credit"] == 0 for row in flow["witnesses"])


def test_retained_negative_register_is_zero_credit() -> None:
    register = load("closeout/retained-negative-register.json")
    assert register["phase_negative_count"] == 214
    assert register["effective_negative_count"] == 37035
    assert all(row["retained"] and row["credit"] == 0 for row in register["phase_rows"])


def test_open_and_exact_gate_totals_are_exact() -> None:
    gates = load("closeout/open-exact-gate-register.json")
    assert gates["effective_open_gaps"] == 299
    assert gates["effective_exact_gates"] == 292
    assert len(gates["rows"]) == 4


def test_route_is_neris_prepared_not_sent() -> None:
    route = load("route/route-state.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["recipient_selected"] is True
    assert route["prospective_recipient"] == "Neris Solane"
    assert route["message_count"] == 0 and route["acknowledgement"] is False


def test_handoff_candidate_word_window_and_truth() -> None:
    text = (OWNER_ROOT / "handoffs/neris-solane-v673-v5-activation-candidate.md").read_text(encoding="utf-8")
    assert 10000 <= len(text.split()) <= 100000
    assert "PREPARED_BY_ELAREN_KESTREL = true" in text
    assert "SENT_BY_ELAREN_KESTREL = false" in text
    assert "DELIVERY_ACKNOWLEDGED = false" in text


def test_handoff_contains_no_raw_uuid_or_private_path() -> None:
    text = (OWNER_ROOT / "handoffs/neris-solane-v673-v5-activation-candidate.md").read_text(encoding="utf-8")
    assert re.search(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", text, re.IGNORECASE) is None
    assert re.search(r"[A-Za-z]:\\Users\\|/Users/|/home/", text, re.IGNORECASE) is None


def test_final_prerequisites_and_selection_are_bounded() -> None:
    prerequisites = load("final/final-validation-prerequisites.json")
    selection = load("validation/final-test-selection.json")
    assert prerequisites["state"] == "PENDING_FINAL_COMMIT"
    assert prerequisites["canonical_runs_completed"] == 0
    assert prerequisites["success_replay_allowed"] is False
    assert selection["expected_total"] == 107 and selection["full_repository_suite"] is False


def test_content_seal_replays() -> None:
    seal = load("seal/content-seal.json")
    assert seal["entry_count"] == 9
    for row in seal["entries"]:
        blob = (ROOT / row["path"]).read_bytes().replace(b"\r\n", b"\n")
        assert len(blob) == row["bytes"]
        assert hashlib.sha256(blob).hexdigest() == row["sha256"]


def test_final_manifests_replay_when_present() -> None:
    for name in ["final-owner-manifest.json", "final-delta-manifest.json"]:
        path = OWNER_ROOT / "validation" / name
        if not path.exists():
            continue
        manifest = json.loads(path.read_text(encoding="utf-8"))
        blobs = batch_index_blobs([row["path"] for row in manifest["entries"]])
        assert manifest["entry_count"] == len(manifest["entries"])
        for row in manifest["entries"]:
            normalized = blobs[row["path"]].replace(b"\r\n", b"\n")
            assert len(normalized) == row["bytes"]
            assert hashlib.sha256(normalized).hexdigest() == row["sha256"]


def test_final_privacy_scan_has_zero_confirmed_hits() -> None:
    path = OWNER_ROOT / "validation/final-staged-privacy.json"
    if path.exists():
        scan = load("validation/final-staged-privacy.json")
        assert scan["class_count"] == 5 and scan["confirmed_hit_count"] == 0


class StructureParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(tag)


def test_accessible_report_has_structure_and_reserved_evaluation() -> None:
    text = (OWNER_ROOT / "reports/accessible-final-report.html").read_text(encoding="utf-8")
    parser = StructureParser()
    parser.feed(text)
    for tag in ["header", "nav", "main", "section", "table", "caption", "footer"]:
        assert tag in parser.tags
    for phrase in ["assistive-technology", "Māori-language", "cognitive-accessibility", "affected-user"]:
        assert phrase in text


def test_checklist_and_wellbeing_preserve_boundaries() -> None:
    checklist = load("closeout/complete-incomplete-checklist.json")
    wellbeing = load("closeout/wellbeing-workload-check.json")
    assert "Stage 20" in checklist["incomplete"]
    assert checklist["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert wellbeing["relational_only"] is True and wellbeing["human_workload_claim"] is False
    assert wellbeing["pause_right_preserved"] is True


def test_sources_and_environment_are_read_only() -> None:
    source = load("closeout/source-and-provenance.json")
    environment = load("closeout/environment-version-receipt.json")
    assert source["source_validation_replayed"] is False
    assert len(source["source_external_digests"]) == 2
    assert environment["versions_verified_only"] is True
    assert environment["updates_or_installs"] == 0


def test_proposal_source_ledger_preserves_bounded_novelty() -> None:
    ledger = load("closeout/proposal-source-ledger.json")
    assert ledger["proposal_chain"] == {"source": 6350, "result": 6390}
    assert ledger["universal_novelty_claim"] is False
    assert ledger["source_authority_conferred"] is False


def test_owner_file_word_and_overview_floors() -> None:
    files = [path for path in OWNER_ROOT.rglob("*") if path.is_file()]
    assert len(files) <= 2000
    assert all(len(path.read_text(encoding="utf-8").split()) <= 100000 for path in files)
    overview = (OWNER_ROOT / "reports/final-integrated-overview.md").read_text(encoding="utf-8")
    assert len(overview.split()) >= 1200


def test_closeout_receipt_and_terminal_verdict() -> None:
    receipt = load("closeout/closeout-receipt.json")
    truth = load("closeout/phase-truth.json")
    assert receipt["phase_methods"] == 214
    assert receipt["sealed_totals"]["negatives"] == 37035
    assert receipt["route_state"] == "PREPARED_NOT_SENT"
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
