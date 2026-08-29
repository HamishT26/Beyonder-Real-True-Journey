from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
BASE = REPO / "docs" / "elowen-cairn" / "v676-v6"
SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
X1 = "0943c5da5d4c1aced1ed9a29aca2d18de1c16b26"
EVIDENCE = "c32fde8ba3aa9518e65f212b8a87d1a108dbc69a"
BRANCH = "codex/GHC-Family/elowen-cairn-v676-v6-full-tools"
LABELS = {"completed", "represented", "open_gap", "exact_gate"}
OWNER_PREFIX = "docs/elowen-cairn/v676-v6/"
FINAL_SELF = {
    OWNER_PREFIX + "validation/final-delta-manifest.json",
    OWNER_PREFIX + "validation/final-owner-manifest.json",
    OWNER_PREFIX + "validation/final-staged-review.json",
}


def load(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def git(*args: str, binary: bool = False):
    result = subprocess.run(["git", "-C", str(REPO), *args], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def allowed(path: str) -> bool:
    return (
        path.startswith(OWNER_PREFIX)
        or re.fullmatch(r"scripts/(?:build_ghc_family|ghc_family|validate_ghc_family)_elowen_cairn_v676_v6_.*\.py", path) is not None
        or re.fullmatch(r"tests/test_ghc_family_elowen_cairn_v676_v6_.*\.py", path) is not None
    )


def final_ref_and_paths() -> tuple[str, set[str], set[str]]:
    head = git("rev-parse", "HEAD")
    if head == EVIDENCE:
        staged = {path for path in git("diff", "--cached", "--name-only", "--diff-filter=ACMR", EVIDENCE, "--").splitlines() if path}
        committed = {path for path in git("diff", "--name-only", "--diff-filter=ACMR", SOURCE, EVIDENCE, "--").splitlines() if path and allowed(path)}
        return ":", staged, committed | staged
    delta = {path for path in git("diff", "--name-only", "--diff-filter=ACMR", EVIDENCE, head, "--").splitlines() if path}
    owner = {path for path in git("diff", "--name-only", "--diff-filter=ACMR", SOURCE, head, "--").splitlines() if path and allowed(path)}
    return head, delta, owner


def object_map(ref: str) -> dict[str, str]:
    result: dict[str, str] = {}
    if ref == ":":
        for line in git("ls-files", "-s").splitlines():
            left, path = line.split("\t", 1)
            mode, oid, stage = left.split()
            if stage == "0":
                result[path] = oid
    else:
        for line in git("ls-tree", "-r", ref).splitlines():
            left, path = line.split("\t", 1)
            mode, kind, oid = left.split()
            if kind == "blob":
                result[path] = oid
    return result


def batch_blobs(oids: set[str]) -> dict[str, bytes]:
    proc = subprocess.Popen(
        ["git", "-C", str(REPO), "cat-file", "--batch"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert proc.stdin and proc.stdout
    result: dict[str, bytes] = {}
    for oid in sorted(oids):
        proc.stdin.write((oid + "\n").encode("ascii"))
        proc.stdin.flush()
        header = proc.stdout.readline().split()
        assert len(header) >= 3 and header[1] == b"blob"
        raw = proc.stdout.read(int(header[2]))
        proc.stdout.read(1)
        result[oid] = raw
    proc.stdin.close()
    stderr = proc.stderr.read().decode("utf-8", "replace") if proc.stderr else ""
    assert proc.wait() == 0, stderr
    return result


def normalized(raw: bytes) -> bytes:
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def test_final_truth_and_outcomes_are_exact_and_bounded() -> None:
    truth = load("final/phase-truth.json")
    assert truth["source"] == SOURCE and truth["x1"] == X1 and truth["evidence"] == EVIDENCE
    assert truth["declared_proposal_chain"] == 7630
    assert truth["core_outcomes"] == {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
    assert set(truth["core_outcomes"]) == LABELS
    assert truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"
    assert truth["real_world_rows"] == truth["participants"] == truth["external_actions"] == 0
    assert truth["production_identity_events"] == truth["authority_actions"] == 0
    assert truth["full_repository_suite_run"] is False
    assert truth["independent_reproduction_claimed"] is False


def test_final_method_flow_retains_every_false_witness_and_recovery() -> None:
    ledger = load("final/method-flow-ledger.json")
    methods = ledger["methods"]
    failed = [row for row in methods if row["truth"] is False]
    passed = [row for row in methods if row["truth"] is True]
    assert ledger["phase_ledger_counts"] == {"methods": 654, "failed": 207, "passing": 447}
    assert (len(methods), len(failed), len(passed)) == (654, 207, 447)
    ids = {row["method_id"] for row in methods}
    assert len(ids) == len(methods)
    assert all(row.get("recovered_by") in ids for row in failed)
    assert ledger["post_evidence_failed_witnesses"] == 26
    assert ledger["post_evidence_bounded_recoveries"] == 26
    for number in range(1, 17):
        assert f"EC6766-CLOSE-N{number:03d}" in ids
        assert f"EC6766-CLOSE-P{number:03d}" in ids
    assert ledger["current_overlay"] == {
        "effective_negatives": 42648,
        "effective_methods": 33772,
        "retained_failed_witnesses": 14309,
        "bounded_passing_witnesses": 20152,
        "open_gaps": 359,
        "exact_gates": 351,
    }
    negatives = load("final/retained-negative-register.json")
    assert negatives["phase_failed_witness_count"] == 207
    assert negatives["failed_witnesses_converted_to_pass"] == 0


def test_gap_gate_and_portfolio_boundaries_remain_exact() -> None:
    gaps = load("final/open-gap-register.json")
    gates = load("final/exact-gate-register.json")
    portfolio = load("final/portfolio-truth.json")
    assert gaps["current"] == 359 and gaps["new"] == 2
    assert gates["current"] == 351 and gates["new"] == 2
    assert gates["exact_approval_packets_unexecuted"] == 20
    assert gates["blocked_packets_unexecuted"] == 10
    assert portfolio["safe_now_completed"] == 60
    assert portfolio["candidate_completed_without_core_promotion"] == 30
    assert portfolio["clean_fix_refine_completed"] == 60
    assert portfolio["core_outcome_counts_unchanged_by_portfolio_status"] is True


def test_source_proposal_ledger_has_forty_rows_and_exact_labels() -> None:
    ledger = load("final/source-and-proposal-ledger.json")
    assert ledger["declared_chain_before"] == 7590 and ledger["declared_chain_after"] == 7630
    assert len(ledger["proposals"]) == 40 and len(ledger["outcomes"]) == 40
    assert Counter(row["outcome"] for row in ledger["outcomes"]) == Counter({"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2})
    assert ledger["universal_novelty_proof_claimed"] is False


def test_final_delta_and_owner_manifests_have_exact_set_and_blob_parity() -> None:
    ref, delta_paths, owner_paths = final_ref_and_paths()
    assert all(allowed(path) for path in delta_paths | owner_paths)
    manifests = []
    for relative, expected in (
        ("validation/final-delta-manifest.json", delta_paths),
        ("validation/final-owner-manifest.json", owner_paths),
    ):
        manifest = load(relative)
        entries = manifest["entries"]
        exclusions = {row["path"] for row in manifest["declared_exclusions"]}
        assert exclusions == FINAL_SELF
        assert manifest["entry_count"] == len(entries)
        assert {row["path"] for row in entries} | exclusions == expected
        assert not ({row["path"] for row in entries} & exclusions)
        manifests.append(entries)
    objects = object_map(ref)
    rows = [row for entries in manifests for row in entries]
    raw_by_oid = batch_blobs({row["git_blob_oid"] for row in rows})
    for row in rows:
        assert objects[row["path"]] == row["git_blob_oid"]
        raw = raw_by_oid[row["git_blob_oid"]]
        assert hashlib.sha256(normalized(raw)).hexdigest() == row["sha256_normalized_lf"]


def test_final_staged_review_and_content_seal_are_exact() -> None:
    review = load("validation/final-staged-review.json")
    assert review["status"] == "VALID_PRECOMMIT_FINAL_STAGED_REVIEW"
    assert review["unexpected_paths"] == []
    assert review["confirmed_five_class_privacy_or_raw_identifier_hits"] == 0
    assert review["exact_staged_review"] is True
    seal = load("closeout/content-seal.json")
    assert len(seal["entries"]) == 8
    for row in seal["entries"]:
        path = REPO / row["path"]
        assert hashlib.sha256(normalized(path.read_bytes())).hexdigest() == row["sha256_normalized_lf"]


def test_terminal_route_is_prepared_not_sent_and_single_edge_gated() -> None:
    route = load("orchestration/terminal-route-hold.json")
    assert route["state"] == "PREPARED_NOT_SENT"
    assert route["provisional_exact_title"] == "Sylven Arc"
    assert route["provisional_phase"] == "v676-v7"
    assert route["continuation_authority_terminal_label"] == "v725-v8"
    assert route["precontact_performed"] is False and route["send_count"] == 0
    baton = (BASE / "handoffs" / "sylven-arc-v676-v7-activation-candidate.md").read_text(encoding="utf-8")
    assert "PREPARED NOT SENT" in baton
    assert "SENT_BY_ELOWEN_CAIRN = false" in baton
    assert "Elowen Cairn" in baton and "v676-v6" in baton and "Sylven Arc" in baton and "v676-v7" in baton
    assert "one terminally validated and acknowledged edge at a time" in baton


def test_lifecycle_is_direct_single_parent_and_merge_free() -> None:
    assert git("rev-parse", X1 + "^") == SOURCE
    assert git("rev-parse", EVIDENCE + "^") == X1
    head = git("rev-parse", "HEAD")
    assert git("branch", "--show-current") == BRANCH
    if head != EVIDENCE:
        assert git("rev-parse", head + "^") == EVIDENCE
        assert int(git("rev-list", "--count", SOURCE + ".." + head)) == 3
        assert git("rev-list", "--merges", SOURCE + ".." + head) == ""
        assert len(git("show", "-s", "--format=%P", head).split()) == 1


def test_all_phase_json_parses_documents_and_owner_files_remain_below_caps() -> None:
    json_paths = list(BASE.rglob("*.json"))
    assert len(json_paths) >= 510
    for path in json_paths:
        json.loads(path.read_text(encoding="utf-8"))
    documents = [path for path in BASE.rglob("*") if path.is_file() and path.suffix.lower() in {".md", ".html"}]
    assert len(documents) >= 25
    assert max(len(path.read_text(encoding="utf-8").split()) for path in documents) <= 100_000
    owner_files = [path for path in BASE.rglob("*") if path.is_file()]
    owner_files += list((REPO / "scripts").glob("*elowen_cairn_v676_v6*.py"))
    owner_files += list((REPO / "tests").glob("test_ghc_family_elowen_cairn_v676_v6*.py"))
    assert len(owner_files) < 2000


def test_no_private_path_raw_route_secret_assignment_or_uuid_payload_exists() -> None:
    patterns = [
        re.compile(r"(?i)[A-Z]:[\\/]+Users[\\/]+"),
        re.compile(r"(?i)(source_thread_id|thread_id|clientThreadId)"),
        re.compile(r"(?i)(api[_-]?key|private[_-]?key|password|bearer)\s*[:=]"),
        re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        re.compile(r"(?i)(session[_ -]?stream|terminal transcript|screenshot payload)"),
    ]
    for path in BASE.rglob("*"):
        if not path.is_file():
            continue
        if path.name.endswith("-staged-review.json") or path.name.endswith("privacy-adjudication.json"):
            continue
        value = path.read_text(encoding="utf-8")
        for pattern in patterns:
            assert pattern.search(value) is None, f"{pattern.pattern} in {path.relative_to(REPO)}"


def test_unknown_outcome_labels_are_absent_and_diff_is_hygienic() -> None:
    values = []
    for path in BASE.rglob("*.json"):
        stack = [json.loads(path.read_text(encoding="utf-8"))]
        while stack:
            node = stack.pop()
            if isinstance(node, dict):
                for key in ("outcome", "expected_disposition"):
                    if key in node and isinstance(node[key], str):
                        values.append(node[key])
                stack.extend(node.values())
            elif isinstance(node, list):
                stack.extend(node)
    assert set(values) <= LABELS
    head = git("rev-parse", "HEAD")
    args = ["diff", "--check"] if head == EVIDENCE else ["diff", "--check", EVIDENCE + ".." + head]
    subprocess.run(["git", "-C", str(REPO), *args], check=True)
