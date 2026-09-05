"""Validate only Vesper Arlen's exact v686-v3 source-to-head delta."""

from __future__ import annotations

import argparse
import ast
import collections
import hashlib
import importlib
import io
import json
import re
import subprocess
import sys
import unittest
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = "docs/vesper-arlen/v686-v3/"
SOURCE = "910fc54d8b79b23b1053af7e1b3e10697f529eda"
BRANCH = "codex/GHC-Family/vesper-arlen-v686-v3-full-tools"
SCRIPTS = [
    "scripts/ghc_family_config_toml.py",
    "scripts/ghc_family_config_layers.py",
    "scripts/ghc_family_config_transaction.py",
    "scripts/ghc_family_config_assurance.py",
    "scripts/ghc_family_config_obligations.py",
]
TEST = "tests/test_ghc_family_vesper_v686_v3.py"


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args])


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def snapshot(head: str) -> dict[str, bytes]:
    args = ["diff", "--raw", "--no-abbrev", "--no-renames", SOURCE]
    if head == "INDEX":
        args.insert(1, "--cached")
    else:
        args.append(head)
    entries = []
    for line in git(*args).decode().splitlines():
        metadata, path = line.split("\t", 1)
        parts = metadata.split()
        entries.append((path, parts[3], parts[4]))
    allowed = lambda path: path.startswith(BASE) or path in SCRIPTS + [TEST]
    assert entries and all(status == "A" and allowed(path) for path, _oid, status in entries), "owner allowlist or additive state"
    request = "".join(oid + "\n" for _path, oid, _status in entries).encode()
    process = subprocess.run(["git", "-C", str(ROOT), "cat-file", "--batch"], input=request, capture_output=True, check=True)
    data = process.stdout
    position = 0
    blobs: dict[str, bytes] = {}
    for path, oid, _status in entries:
        end = data.index(b"\n", position)
        header = data[position:end].split()
        size = int(header[2])
        assert header[0].decode() == oid and header[1] == b"blob"
        blobs[path] = data[end + 1 : end + 1 + size]
        position = end + size + 2
    assert position == len(data)
    return blobs


def load(blobs: dict[str, bytes], relative: str) -> object:
    return json.loads(blobs[BASE + relative])


def manifest(blobs: dict[str, bytes], relative: str, expected: set[str] | None = None) -> int:
    record = load(blobs, relative)
    rows = record.get("entries", record.get("targets"))
    assert isinstance(rows, list)
    paths = [row["path"] for row in rows]
    assert len(paths) == len(set(paths))
    for row in rows:
        data = blobs[row["path"]]
        assert len(data) == row["bytes"] and sha(data) == row["sha256"], row["path"]
    if expected is not None:
        assert set(paths) == expected, "manifest coverage mismatch"
    return len(rows)


def equality(head: str) -> dict:
    assert git("branch", "--show-current").decode().strip() == BRANCH
    values = [git("rev-parse", ref).decode().strip() for ref in ["HEAD", "@{upstream}", "refs/remotes/origin/" + BRANCH]]
    live = git("ls-remote", "--heads", "origin", "refs/heads/" + BRANCH).decode().split()
    assert len(live) == 2
    values.append(live[0])
    divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    clean = not git("status", "--porcelain=v1")
    assert values == [head] * 4 and divergence == [0, 0] and clean
    return {"local_upstream_tracking_fresh_live": values, "divergence": divergence, "clean": clean}


def validate(args) -> dict:
    checks = []
    counts: dict[str, int] = {}

    def check(name: str, function):
        value = function()
        assert value is not False, name
        checks.append({"check": name, "pass": True})
        return value

    blobs = snapshot(args.head)
    check("additive_exact_owner_allowlist", lambda: len(blobs) < 2000)
    counts["owner_files"] = len(blobs)
    check(
        "worktree_equals_selected_git_blobs",
        lambda: all((ROOT / path).read_bytes().replace(b"\r\n", b"\n") == data for path, data in blobs.items() if not path.endswith(".pdf"))
        and all((ROOT / path).read_bytes() == data for path, data in blobs.items() if path.endswith(".pdf")),
    )
    parsed = {path: json.loads(data) for path, data in blobs.items() if path.endswith(".json")}
    counts["json"] = len(parsed)
    check("all_owner_json_parses", lambda: True)
    python_paths = [path for path in blobs if path.endswith(".py")]
    for path in python_paths:
        ast.parse(blobs[path].decode("utf-8"), filename=path)
    counts["python_ast"] = len(python_paths)
    check("all_owner_python_ast_parses", lambda: True)
    counts["markdown"] = sum(path.endswith(".md") for path in blobs)
    check("markdown_utf8_nonempty", lambda: all(data.decode("utf-8").strip() and "\ufffd" not in data.decode("utf-8") for path, data in blobs.items() if path.endswith(".md")))

    x1 = load(blobs, "validation/x1-equality.json")["x1"]
    check("x1_direct_source_parent", lambda: git("rev-parse", x1 + "^").decode().strip() == SOURCE)
    check("immutable_x1", lambda: not git("diff", "--name-only", x1, *([] if args.head == "INDEX" else [args.head]), "--", BASE + "x1"))
    x1_equality = load(blobs, "validation/x1-equality.json")
    check("x1_preimplementation_equality", lambda: x1_equality["clean_before_x2"] and x1_equality["divergence"] == [0, 0] and x1_equality["local_upstream_tracking_fresh_live"] == [x1] * 4)
    manifest_count = check("x1_manifest_replay", lambda: manifest(blobs, "validation/x1-manifest.json"))
    deck_paths = {path for path in blobs if path.startswith(BASE + "x2/flashcards/")}
    manifest_count += check("card_manifest_exact_coverage", lambda: manifest(blobs, "x2/flashcards/card-manifest.json", deck_paths - {BASE + "x2/flashcards/card-manifest.json"}))
    if args.phase == "final":
        check("direct_source_x1_evidence_final_lifecycle", lambda: git("rev-list", "--count", SOURCE + ".." + args.head).strip() == b"3" and git("rev-list", "--count", "--merges", SOURCE + ".." + args.head).strip() == b"0" and git("rev-parse", args.head + "^").decode().strip() == args.evidence and git("rev-parse", args.evidence + "^").decode().strip() == x1)
        evidence_blobs = snapshot(args.evidence)
        evidence_paths = set(evidence_blobs)
        evidence_manifest = "validation/evidence-manifest-corrected.json" if BASE + "validation/evidence-manifest-corrected.json" in blobs else "validation/evidence-manifest.json"
        manifest_count += check("evidence_manifest_immutable_replay", lambda: manifest(blobs, evidence_manifest, evidence_paths - {BASE + evidence_manifest}))
        check("immutable_evidence_files", lambda: all(blobs[path] == data for path, data in evidence_blobs.items()))
        manifest_count += check("final_content_seal_replay", lambda: manifest(blobs, "final/content-seal.json", set(blobs) - {BASE + "final/content-seal.json", BASE + "validation/final-manifest.json"}))
        manifest_count += check("final_manifest_complete_replay", lambda: manifest(blobs, "validation/final-manifest.json", set(blobs) - {BASE + "validation/final-manifest.json"}))
    elif BASE + "validation/evidence-manifest-corrected.json" in blobs or BASE + "validation/evidence-manifest.json" in blobs:
        evidence_manifest = "validation/evidence-manifest-corrected.json" if BASE + "validation/evidence-manifest-corrected.json" in blobs else "validation/evidence-manifest.json"
        manifest_count += check("evidence_manifest_exact_coverage", lambda: manifest(blobs, evidence_manifest, set(blobs) - {BASE + evidence_manifest}))
    counts["manifest_entries"] = manifest_count

    rows = load(blobs, "x1/new-proposals.json")["proposals"]
    results = load(blobs, "x2/contract-results.json")["results"]
    negatives = load(blobs, "x2/registered-mutations.json")["negatives"]
    portfolio = load(blobs, "x2/portfolio-results.json")
    check("proposal_counts_and_four_outcomes", lambda: len(rows) == 200 and len({row["proposal_id"] for row in rows}) == 200 and collections.Counter(row["expected_execution_disposition"] for row in rows) == {"completed": 170, "represented": 10, "open_gap": 10, "exact_gate": 10})
    inherited = load(blobs, "x1/inherited-selection.json")["selections"]
    check("inherited_zero_credit_selection", lambda: len(inherited) == 200 and all(item["execution_credit"] == item["novelty_credit"] == 0 for item in inherited))
    novelty = load(blobs, "x1/novelty-audit.json")
    check("bounded_novelty_scope", lambda: novelty["comparisons"] == 40000 and novelty["quarantined"] == 0 and novelty["max_title_jaccard"] < novelty["threshold"] and not novelty["universal_novelty_claimed"])
    check("frozen_definition_hashes", lambda: all(sha(compact({key: value for key, value in row.items() if key != "definition_sha256"})) == row["definition_sha256"] for row in rows))
    sys.path.insert(0, str(ROOT / "scripts"))
    import ghc_family_config_toml as common

    module_names = {"toml": "config_toml", "layers": "config_layers", "transaction": "config_transaction", "assurance": "config_assurance", "obligations": "config_obligations"}
    compute = {key: importlib.import_module("ghc_family_" + name).evaluate for key, name in module_names.items()}
    row_map = {row["proposal_id"]: row for row in rows}
    check("positive_report_recomputation", lambda: len(results) == 200 and all(common.canonical(compute[row_map[result["proposal_id"]]["runner"]](row_map[result["proposal_id"]]["operation"], row_map[result["proposal_id"]]["input"])) == common.canonical(result["result"]) == common.canonical(row_map[result["proposal_id"]]["expected_result"]) and result["input_nonmutation"] for result in results))
    check("all_registered_mutations_rejected", lambda: len(negatives) == 1000 and len({item["negative_id"] for item in negatives}) == 1000 and all(item["success_credit"] == 0 and item["rejected"] and not common.verify_envelope(row_map[item["proposal_id"]], item["retained_record"], compute[row_map[item["proposal_id"]]["runner"]])["accepted"] for item in negatives))
    check("portfolio_counts_and_unexecuted_gates", lambda: [len(portfolio[key]) for key in ["safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets"]] == [300, 250, 300, 50, 30] and all(not task["executed"] for key in ["exact_packets", "blocked_packets"] for task in portfolio[key]))
    check("safe_and_candidate_evidence", lambda: all(task["passed"] and task["disposition"] == "completed" for key in ["safe_now", "candidates"] for task in portfolio[key]))
    check("all_correction_failures_and_recoveries", lambda: all(not common.verify_envelope(row_map[task["proposal_id"]], task["retained_before"], compute[row_map[task["proposal_id"]]["runner"]])["accepted"] and common.verify_envelope(row_map[task["proposal_id"]], task["corrected_after"], compute[row_map[task["proposal_id"]]["runner"]])["accepted"] and task["success_credit_for_initial"] == 0 for task in portfolio["clean_fix_refine"]))

    ledger = load(blobs, "x2/method-flow.json")
    summary = load(blobs, "x2/evidence-summary.json")
    baseline = load(blobs, "x1/activation-source.json")["effective_activation_baseline"]
    check("method_flow_counts_and_non_erasure", lambda: len(ledger["methods"]) == 1333 and len(ledger["witnesses"]) == 2666 and len({method["method_id"] for method in ledger["methods"]}) == 1333 and collections.Counter(witness["result"] for witness in ledger["witnesses"]) == {"pass": 1333, "fail": 1333})
    check("effective_count_arithmetic", lambda: all(summary["repository_seal"][key] == baseline[key] + (10 if key in ("open_gaps", "exact_gates") else 1333) for key in baseline))
    check("operational_failure_count", lambda: len(load(blobs, "x2/all-operational-events.json")["events"]) == 15)

    cards = [value for path, value in parsed.items() if path.startswith(BASE + "x2/flashcards/cards/")]
    by_id = {card["card_id"]: card for card in cards}
    check("four_tier_card_graph", lambda: len(cards) == 211 and len(by_id) == 211 and all((card["tier"] == 1 and not card["parent_ids"]) or (len(card["parent_ids"]) == 1 and card["parent_ids"][0] in by_id and by_id[card["parent_ids"][0]]["tier"] == card["tier"] - 1) for card in cards))
    counts["cards"] = len(cards)

    class Page(HTMLParser):
        def __init__(self):
            super().__init__()
            self.tags = collections.Counter()
            self.scope = collections.Counter()
            self.ids = []

        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            self.tags[tag] += 1
            if tag == "th":
                self.scope[values.get("scope")] += 1
            if "id" in values:
                self.ids.append(values["id"])

    page = Page()
    page.feed(blobs[BASE + "x2/flashcards/accessible-report.html"].decode("utf-8"))
    check("accessible_html_structure", lambda: page.tags["main"] == 1 and page.tags["caption"] == 1 and page.scope["col"] == 4 and page.scope["row"] == 200 and len(page.ids) == len(set(page.ids)))
    review = load(blobs, "x2/overview-visual-review.json")
    pdf = blobs[BASE + "x2/integrated-overview.pdf"]
    check("four_page_pdf_review_binding", lambda: review["all_pages_passed"] and review["pages_reviewed"] == [1, 2, 3, 4] and review["pdf_sha256"] == sha(pdf))
    from pypdf import PdfReader

    document = PdfReader(io.BytesIO(pdf))
    texts = [page.extract_text() for page in document.pages]
    check("pdf_text_and_glyph_structure", lambda: len(texts) == 4 and "Māori" in texts[-1] and "NOT_READY_FOR_STAGE_20" in texts[0] and all("■" not in text for text in texts))
    counts["pdf_pages"] = 4
    baton_path = "final/future-seat-04-v686-v4-baton.md" if args.phase == "final" else "x2/future-seat-04-v686-v4-activation-candidate.md"
    baton = blobs[BASE + baton_path].decode("utf-8")
    counts["baton_words"] = len(baton.split())
    check("modular_baton_profile", lambda: 10000 <= len(baton.split()) <= 100000 and len(re.findall(r"(?m)^# \d\d ", baton)) == 13 and "future seat 04" in baton and "v686-v4" in baton)

    installation = load(blobs, "x2/toolchain/installation-receipt.json")
    smokes = load(blobs, "x2/toolchain/package-smokes.json")
    audit = load(blobs, "x2/toolchain/advisory-audit.json")
    check("three_isolated_packages_and_smokes", lambda: installation["direct_distribution_count"] == 3 and installation["hash_required"] and installation["offline_install"] and smokes["pass"] and len(smokes["checks"]) == 9 and audit["findings"] == 0 and len(audit["response"]["results"]) == 3)
    if args.tool_python:
        inventory = json.loads(subprocess.check_output([args.tool_python, "-c", "import importlib.metadata as m,json;print(json.dumps(sorted((d.metadata['Name'],d.version) for d in m.distributions() if d.metadata['Name'].lower() in {'tomlkit','immutables','configupdater'})))"]))
        check("current_isolated_distribution_inventory", lambda: inventory == installation["packages"])

    promotion = load(blobs, "tooling/global-promotion-corrected.json")
    parity = []
    for entry in promotion["entries"]:
        local = blobs[BASE + "skills/" + entry["skill"] + "/" + entry["path"]]
        global_bytes = (Path.home() / ".codex/skills" / entry["skill"] / entry["path"]).read_bytes()
        parity.append(local == global_bytes and sha(local) == entry["sha256"])
    check("ten_global_skill_byte_parity", lambda: len(parity) == 80 and all(parity) and promotion["skills"] == 10)
    for skill in load(blobs, "x1/skill-runner-plan.json")["skills"]:
        markdown = blobs[BASE + "skills/" + skill["name"] + "/SKILL.md"].decode("utf-8")
        yaml = blobs[BASE + "skills/" + skill["name"] + "/agents/openai.yaml"].decode("utf-8")
        assert markdown.startswith("---\nname: " + skill["name"] + "\n") and "references/contracts.json" in markdown
        assert "$" + skill["name"] in yaml and "allow_implicit_invocation: true" in yaml
    check("skill_frontmatter_and_contract_routing", lambda: True)
    catalogue_validation = load(blobs, "tooling/catalogue-v3-validate.json")
    runner_query = load(blobs, "tooling/runner-query-v3.json")
    collisions = load(blobs, "tooling/catalogue-v3-collisions.json")
    check("exact_tool_catalogue_and_policy", lambda: catalogue_validation["valid"] and runner_query["result_count"] == 5 and collisions["finding_count"] == 0 and all(load(blobs, "tooling/promotion-checks/" + skill["name"] + ".json")["state"] == "ready" for skill in load(blobs, "x1/skill-runner-plan.json")["skills"]))

    privacy = []
    patterns = {
        "private_absolute_path": r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]",
        "private_identifier": r"\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b",
        "credential": r"(?:gh" + "p_|gl" + "pat-|sk-" + r"proj-)[A-Za-z0-9_\-]{16,}",
        "private_payload_field": r'"(?:raw_' + "transcript|private_" + "route|thread_" + 'id|session_' + r'id)"\s*:',
        "private_key": r"BEGIN [A-Z ]*" + "PRIVATE KEY",
    }
    scanner_definition_paths = {BASE + "validation/validate_owner.py"}
    candidates = []
    for path, data in blobs.items():
        if path.endswith(".pdf"):
            continue
        content = data.decode("utf-8")
        for kind, pattern in patterns.items():
            for match in re.finditer(pattern, content):
                candidate = {"path": path, "class": kind, "offset": match.start(), "scanner_definition": path in scanner_definition_paths}
                candidates.append(candidate)
                if not candidate["scanner_definition"]:
                    privacy.append(candidate)
    check("bounded_five_class_privacy", lambda: not privacy)
    counts["privacy_candidates"] = len(candidates)
    counts["privacy_confirmed_hits"] = len(privacy)

    security = []
    for path in python_paths:
        tree = ast.parse(blobs[path].decode("utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                security.append({"path": path, "kind": node.func.id})
            if isinstance(node, ast.keyword) and node.arg == "shell" and isinstance(node.value, ast.Constant) and node.value.value is True:
                security.append({"path": path, "kind": "shell_true"})
    check("bounded_code_execution_security_scan", lambda: not security)
    counts["bounded_security_findings"] = len(security)

    sys.path.insert(0, str(ROOT / "tests"))
    module = importlib.import_module(Path(TEST).stem)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)

    def flatten(test_suite):
        for item in test_suite:
            if isinstance(item, unittest.TestSuite):
                yield from flatten(item)
            else:
                yield item.id()

    identifiers = list(flatten(suite))
    check("exact_selected_test_collection", lambda: len(identifiers) == len(set(identifiers)) == 45)
    if args.phase == "final":
        definition = load(blobs, "final/test-definition-manifest.json")
        check("test_definition_manifest_binding", lambda: definition["identifiers"] == identifiers and definition["definition_sha256"] == sha(blobs[TEST]))
    output = io.StringIO()
    run = unittest.TextTestRunner(stream=output, verbosity=1).run(suite)
    check("selected_owner_tests", lambda: run.wasSuccessful() and run.testsRun == 45)
    counts["selected_tests"] = run.testsRun
    counts["detailed_checks"] = len(checks)
    counts["passed_checks"] = len(checks)
    return {"checks": checks, "counts": counts, "tests": {"identifiers": identifiers, "definition_sha256": sha(blobs[TEST]), "tests_run": run.testsRun, "failures": len(run.failures), "errors": len(run.errors), "complete_repository_suite": False}, "same_owner_only": True, "independent_reproduction": False, "complete_repository_suite": False}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--head", required=True)
    parser.add_argument("--phase", choices=["evidence", "final"], required=True)
    parser.add_argument("--evidence")
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--canonical", action="store_true")
    parser.add_argument("--tool-python")
    args = parser.parse_args()
    assert not args.receipt.exists(), "Receipt already exists; no replay."
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    before = None
    if args.canonical:
        assert args.phase == "final" and args.head != "INDEX" and args.evidence
        before = equality(args.head)
        marker = args.receipt.with_suffix(args.receipt.suffix + ".invoked")
        with marker.open("x", encoding="utf-8") as handle:
            json.dump({"head": args.head, "owner": "Vesper Arlen", "invocations": 1}, handle)
    payload = {"schema": "ghc.family.vesper.owner-validation.v686.v3", "source": SOURCE, "head": args.head, "evidence": args.evidence, "owner": "Vesper Arlen", "phase": "v686-v3", "observed_at": datetime.now(timezone.utc).isoformat(), "canonical_invocation_count": 1 if args.canonical else 0, "canonical_success_count": 0, "canonical_replay_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    try:
        payload.update(validate(args))
        if args.canonical:
            payload["before"] = before
            payload["after"] = equality(args.head)
        payload["status"] = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if args.canonical else "PASS_OWNER_COMPONENT_PREFLIGHT"
        payload["canonical_success_count"] = 1 if args.canonical else 0
    except Exception as exc:
        payload.update(status="FAILED_RETAINED_ZERO_CREDIT", failure_type=type(exc).__name__, failure=str(exc)[:500], canonical_success_count=0)
    payload["payload_sha256"] = sha(compact(payload))
    with args.receipt.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n")
    print(json.dumps({"status": payload["status"], "counts": payload.get("counts"), "failure": payload.get("failure")}))
    return 1 if payload["status"] == "FAILED_RETAINED_ZERO_CREDIT" else 0


if __name__ == "__main__":
    raise SystemExit(main())
