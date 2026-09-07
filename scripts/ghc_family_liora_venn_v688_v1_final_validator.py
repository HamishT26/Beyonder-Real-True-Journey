"""Prepare, stage-check, and exclusively validate Liora v688-v1 exact final."""
from __future__ import annotations

import argparse
import ast
import datetime
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "docs/liora-venn/v688-v1/"
SOURCE = "17fee348a09ec1cb480f7326bce70cd75413dad3"
X1 = "421abce86426674b67e0cbd5ce63ad463421fc9f"
EVIDENCE = "ffa072b57d0d3f58358f15b8fceae4440303503e"
BRANCH = "codex/GHC-Family/liora-venn-v688-v1-full-tools"
EXPECTED_COUNTS = {"proposals": 15630, "negatives": 82599, "methods": 93292, "failed_witnesses": 53447, "passing_witnesses": 83009, "open_gaps": 748, "exact_gates": 747}
EXPECTED_OUTCOMES = {"completed": 160, "represented": 14, "open_gap": 8, "exact_gate": 18}
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_liora_venn_v688_v1_x2_audit import privacy, security, strict


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def formatted(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n").encode("utf-8")


def read(path):
    return strict((ROOT / path).read_text(encoding="utf-8"))


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(formatted(value))


def normalized(path):
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def allowed(path):
    return (
        path.startswith(BASE)
        or path.startswith("scripts/build_ghc_family_liora_venn_v688_v1_")
        or path.startswith("scripts/ghc_family_liora_venn_v688_v1_")
        or path.startswith("scripts/ghc_family_caption_")
        or path.startswith("tests/test_ghc_family_liora_venn_v688_v1_")
    )


def exists_at(commit, path):
    return subprocess.run(["git", "-C", str(ROOT), "cat-file", "-e", commit + ":" + path], capture_output=True).returncode == 0


def current_paths():
    paths = []
    source_paths = set(git("ls-tree", "-r", "--name-only", SOURCE).splitlines())
    for dirname in [BASE, "scripts", "tests"]:
        directory = ROOT / dirname
        if directory.exists():
            for path in directory.rglob("*"):
                if path.is_file():
                    name = path.relative_to(ROOT).as_posix()
                    if allowed(name) and name not in source_paths:
                        paths.append(name)
    return sorted(set(paths))


def blobs(anchor, paths):
    result = {}
    process = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for path in paths:
            process.stdin.write((anchor + ":" + path + "\n").encode("utf-8")); process.stdin.flush()
            header = process.stdout.readline().decode("utf-8").strip().split()
            assert len(header) == 3 and header[1] == "blob", (path, header)
            raw = process.stdout.read(int(header[2])); assert process.stdout.read(1) == b"\n"
            result[path] = raw
    finally:
        process.stdin.close(); process.wait(timeout=10)
    return result


def scan(items):
    json_count = python_count = document_count = 0
    largest = 0
    for path, raw in items.items():
        text = raw.decode("utf-8")
        words = len(text.split()); largest = max(largest, words); assert words <= 100000, path
        if path.endswith(".json"):
            strict(text); json_count += 1
        if path.endswith(".py"):
            ast.parse(text, filename=path); python_count += 1
        if path.endswith((".md", ".html", ".txt")):
            document_count += 1
        if path.endswith(".html"):
            assert "<html" in text and "<main" in text
    privacy_report = privacy(items); assert privacy_report["confirmed_hits"] == 0, privacy_report
    security_report = security({path: raw for path, raw in items.items() if path.endswith(".py")}); assert security_report["finding_count"] == 0, security_report
    return {"strict_json": json_count, "python_ast": python_count, "documents": document_count, "largest_document_words": largest, "privacy": privacy_report, "security": security_report}


def prepare():
    assert git("rev-parse", "HEAD") == EVIDENCE
    changed_prior = git("diff", "--name-only", EVIDENCE)
    assert not changed_prior, changed_prior
    truth = read(BASE + "final/phase-truth.json")
    assert truth["state"] == "FINAL_PREPARED_FOR_ONE_EXTERNAL_CANONICAL" and truth["canonical_invocations"] == 0
    index = read(BASE + "final/baton-index.json")
    baton = (ROOT / index["path"]).read_bytes()
    assert hashlib.sha256(baton).hexdigest() == index["sha256"] and len(baton) == index["bytes"]
    assert len(baton.decode("utf-8").split()) == index["words"] and 10000 <= index["words"] <= 100000
    assert baton.decode("utf-8").count("## Module ") == 13 and baton.decode("utf-8").rstrip().endswith(index["eof"])
    assert (ROOT / BASE / "final/integrated-overview.html").read_text(encoding="utf-8").count('<section class="page">') == 3
    validation = BASE + "validation/"
    delta_manifest = validation + "final-delta-manifest.json"
    owner_manifest = validation + "final-owner-manifest.json"
    exclusions = [delta_manifest, owner_manifest]
    for name in ["final-checks.json", "final-privacy.json", "final-security.json", "final-json.json", "final-staged-review.json"]:
        write(validation + name, {"state": "pending"})
    paths = sorted(set(current_paths()) | set(exclusions))
    prior = set(git("diff", "--name-only", SOURCE, EVIDENCE).splitlines())
    assert len(prior) == 335, len(prior)
    new_paths = sorted(set(paths) - prior)
    assert len(paths) < 2000 and all(allowed(path) for path in paths)
    assert all(not exists_at(EVIDENCE, path) for path in new_paths)
    write(validation + "final-staged-review.json", {"schema": "ghc.family.staged-allowlist.v1", "source": SOURCE, "parent": EVIDENCE, "allowed_paths": new_paths, "allowed_change_kind": "A", "path_count": len(new_paths), "owner_path_count": len(paths), "deletions": 0})
    write(validation + "final-checks.json", {"schema": "ghc.family.final-preparation.v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "prior_paths_unchanged": 335, "final_baton_words": index["words"], "final_baton_modules": 13, "final_overview_pages": 3, "canonical_invocations": 0, "same_owner_only": True, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    scan_exclusions = set(exclusions + [validation + "final-privacy.json", validation + "final-security.json"])
    items = {path: normalized(ROOT / path) for path in paths if path not in scan_exclusions}
    checks = scan(items)
    checks["privacy"]["declared_self_exclusions"] = sorted(scan_exclusions)
    write(validation + "final-privacy.json", checks["privacy"])
    write(validation + "final-security.json", {"schema": "ghc.family.final-bounded-security.v1", "findings": checks["security"]["findings"], "python_ast": checks["python_ast"], "scope": "Every Python path in the Liora source-to-final owner delta; no sibling or unchanged-history execution.", "exhaustive_security": False})
    write(validation + "final-json.json", {"schema": "ghc.family.final-strict-json.v1", "strict_json_before_two_manifest_writes": checks["strict_json"], "duplicate_keys_rejected": True, "nonfinite_constants_rejected": True, "maximum_document_words": checks["largest_document_words"], "documents": checks["documents"]})

    def manifest(selected):
        entries = []
        for path in selected:
            if path not in exclusions:
                raw = normalized(ROOT / path)
                entries.append({"path": path, "bytes_normalized_lf": len(raw), "sha256_normalized_lf": hashlib.sha256(raw).hexdigest()})
        return {"schema": "ghc.family.normalized-lf-manifest.v1", "byte_domain": "normalized_lf_git_blob", "anchor": "PENDING_FINAL_COMMIT", "source": SOURCE, "entry_count": len(entries), "entries": entries, "declared_self_exclusions": exclusions}

    write(delta_manifest, manifest(new_paths))
    whole = manifest(paths); whole["owner_path_count"] = len(paths); write(owner_manifest, whole)
    print(json.dumps({"state": "FINAL_PREPARATION_PASS", "new_files": len(new_paths), "owner_files": len(paths), "final_delta_bindings": len(new_paths) - 2, "owner_bindings": len(paths) - 2, "baton_words": index["words"], "strict_json": checks["strict_json"], "python_ast": checks["python_ast"], "documents": checks["documents"], "confirmed_privacy_hits": 0, "bounded_security_findings": 0, "canonical_invocations": 0}, sort_keys=True))


def staged():
    review = read(BASE + "validation/final-staged-review.json")
    manifest = read(BASE + "validation/final-delta-manifest.json")
    staged_paths = git("diff", "--cached", "--name-only").splitlines()
    assert staged_paths == review["allowed_paths"], (staged_paths, review["allowed_paths"])
    statuses = git("diff", "--cached", "--name-status").splitlines()
    assert len(statuses) == len(staged_paths) and all(line.startswith("A\t") for line in statuses), statuses
    assert not git("diff", "--name-only")
    raw_index = git("diff", "--cached", "--raw", "--no-abbrev").splitlines()
    object_ids = {}
    for line in raw_index:
        metadata, path = line.split("\t", 1); object_ids[path] = metadata.split()[3]
    process = subprocess.Popen(["git", "-C", str(ROOT), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        for entry in manifest["entries"]:
            process.stdin.write((object_ids[entry["path"]] + "\n").encode("ascii")); process.stdin.flush()
            header = process.stdout.readline().decode("ascii").strip().split(); assert len(header) == 3 and header[1] == "blob"
            raw = process.stdout.read(int(header[2])); assert process.stdout.read(1) == b"\n"
            assert len(raw) == entry["bytes_normalized_lf"] and hashlib.sha256(raw).hexdigest() == entry["sha256_normalized_lf"], entry["path"]
    finally:
        process.stdin.close(); process.wait(timeout=10)
    assert manifest["entry_count"] + len(manifest["declared_self_exclusions"]) == len(staged_paths)
    print(json.dumps({"state": "FINAL_EXACT_STAGED_PASS", "staged_paths": len(staged_paths), "manifest_entries": manifest["entry_count"], "self_exclusions": len(manifest["declared_self_exclusions"]), "git_blob_mismatches": 0, "unstaged_paths": 0}, sort_keys=True))


def verify_manifest(anchor, path, before):
    manifest = strict(blobs(anchor, [path])[path].decode("utf-8"))
    listed = [entry["path"] for entry in manifest["entries"]]
    exclusions = manifest["declared_self_exclusions"]
    delta = set(git("diff", "--name-only", before, anchor).splitlines())
    assert len(listed) == len(set(listed)) == manifest["entry_count"]
    assert len(exclusions) == len(set(exclusions)) and not set(listed) & set(exclusions)
    assert set(listed) | set(exclusions) == delta, (path, len(delta), len(listed), exclusions)
    values = blobs(anchor, listed)
    for entry in manifest["entries"]:
        raw = values[entry["path"]].replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        assert len(raw) == entry["bytes_normalized_lf"] and hashlib.sha256(raw).hexdigest() == entry["sha256_normalized_lf"], entry["path"]
    return {"manifest": path, "anchor": anchor, "entries": len(listed), "exclusions": exclusions, "mismatches": []}


def canonical(args, head):
    checks = []
    assert git("branch", "--show-current") == BRANCH; checks.append("owner_branch")
    chain = [line.split() for line in git("rev-list", "--parents", "--reverse", SOURCE + ".." + head).splitlines()]
    assert chain == [[X1, SOURCE], [EVIDENCE, X1], [head, EVIDENCE]], chain; checks.append("three_direct_single_parent_commits")
    assert not git("rev-list", "--merges", SOURCE + ".." + head); checks.append("zero_merges")
    assert git("rev-list", "--parents", "-1", head).split() == [head, EVIDENCE]; checks.append("one_final_parent")
    assert not git("status", "--porcelain=v1", "--untracked-files=all"); checks.append("clean_before")
    delta = [line.split("\t", 1) for line in git("diff", "--name-status", SOURCE, head).splitlines()]
    assert all(kind == "A" and allowed(path) for kind, path in delta); paths = [path for _kind, path in delta]
    assert len(paths) == len(set(paths)) and len(paths) < 2000; checks.append("every_delta_path_allowed_addition")
    items = blobs(head, paths)
    policy = strict(items[BASE + "final/canonical-policy.json"].decode("utf-8"))
    assert policy["source"] == SOURCE and policy["x1"] == X1 and policy["evidence"] == EVIDENCE and policy["expected_tests"] == 28; checks.append("frozen_canonical_policy")
    manifest_specs = [(X1, BASE + "validation/x1-manifest.json", SOURCE), (EVIDENCE, BASE + "x2/validation/evidence-manifest.json", X1), (head, BASE + "validation/final-delta-manifest.json", EVIDENCE), (head, BASE + "validation/final-owner-manifest.json", SOURCE)]
    manifests = [verify_manifest(*spec) for spec in manifest_specs]; checks.append("four_lifecycle_manifests_and_exclusions")
    for anchor, before in [(X1, SOURCE), (EVIDENCE, X1)]:
        prior = git("diff", "--name-only", before, anchor).splitlines(); old = blobs(anchor, prior)
        assert all(items[path] == old[path] for path in prior)
    checks.append("immutable_x1_and_evidence")
    scanned = scan(items); checks.extend(["strict_json", "all_document_caps", "five_class_privacy_adjudication", "bounded_changed_code_security"])
    module_path = ROOT / policy["test_module"]
    spec = importlib.util.spec_from_file_location("liora_exact_final_caption_tests", module_path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module); count = suite.countTestCases(); assert count == 28
    stream = io.StringIO(); result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite); assert result.wasSuccessful(), stream.getvalue(); checks.append("twenty_eight_owner_tests")
    index = strict(items[BASE + "final/baton-index.json"].decode("utf-8")); baton = items[index["path"]]
    assert len(baton) == index["bytes"] and hashlib.sha256(baton).hexdigest() == index["sha256"] and len(baton.decode("utf-8").split()) == index["words"]
    assert 10000 <= index["words"] <= 100000 and baton.decode("utf-8").count("## Module ") == 13 and baton.decode("utf-8").rstrip().endswith(index["eof"]); checks.append("baton_digest_words_modules_eof")
    assert items[BASE + "final/integrated-overview.html"].decode("utf-8").count('<section class="page">') == 3; checks.append("three_final_overview_pages")
    seal = strict(items[BASE + "final/content-seal.json"].decode("utf-8")); assert seal["target_count"] == len(seal["targets"]) == 12
    for row in seal["targets"]:
        raw = items[row["path"]]; assert len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"]
    checks.append("twelve_content_seal_targets")
    promotion = strict(items[BASE + "x2/promotion-receipt.json"].decode("utf-8")); assert len(promotion["members"]) == 56
    for row in promotion["members"]:
        source = items[row["source"]]
        destination = args.skill_root / row["name"] / row["relative"] if row["kind"] == "skill" else args.runner_root / row["relative"]
        assert source == destination.read_bytes() and hashlib.sha256(source).hexdigest() == row["sha256"]
    for name in {row["name"] for row in promotion["members"] if row["kind"] == "skill"}:
        expected = {row["relative"] for row in promotion["members"] if row["kind"] == "skill" and row["name"] == name}
        actual = {path.relative_to(args.skill_root / name).as_posix() for path in (args.skill_root / name).rglob("*") if path.is_file()}
        assert actual == expected
    assert {path.name for path in args.runner_root.iterdir() if path.is_file()} == {row["relative"] for row in promotion["members"] if row["kind"] == "runner"}; checks.append("fifty_six_global_parity_files")
    environment_code = 'import importlib.metadata as m,json;print(json.dumps({d.metadata["Name"]:d.version for d in m.distributions()},sort_keys=True))'
    observed = json.loads(subprocess.check_output([str(args.environment_python), "-X", "utf8", "-c", environment_code], text=True, encoding="utf-8"))
    expected = strict(items[BASE + "x2/environment-receipt.json"].decode("utf-8"))["all_packages"]
    normalize = lambda values: {key.lower().replace("_", "-"): value for key, value in values.items()}
    assert normalize(observed) == normalize(expected) and len(observed) == 3; checks.append("three_pinned_environment_distributions")
    final = strict(items[BASE + "final/phase-truth.json"].decode("utf-8")); assert final["outcomes"] == EXPECTED_OUTCOMES and final["effective_counts"] == EXPECTED_COUNTS and final["terminal_verdict"] == "NOT_READY_FOR_STAGE_20"; checks.append("outcome_count_and_authority_boundaries")
    method = strict(items[BASE + "final/method-flow-ledger.json"].decode("utf-8")); assert method["counts"]["methods"] == 57 and method["counts"]["witness_results"] == {"fail": 297, "pass": 515}; checks.append("complete_method_flow_counts")
    upstream = git("rev-parse", "@{upstream}"); tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH); live = git("ls-remote", "--heads", "origin", "refs/heads/" + BRANCH).split()[0]; divergence = [int(value) for value in git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    assert head == upstream == tracking == live and divergence == [0, 0]; checks.extend(["fresh_four_way_equality", "typed_zero_divergence"])
    assert not git("status", "--porcelain=v1", "--untracked-files=all"); checks.append("clean_after")
    return {"status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "owner": "Liora Venn", "phase": "v688-v1", "source": SOURCE, "x1": X1, "evidence": EVIDENCE, "exact_final": head, "branch": BRANCH, "canonical_invocation_count": 1, "canonical_success_count": 1, "canonical_replay_count": 0, "checks": checks, "detailed_checks": len(checks), "selected_tests": count, "excluded_tests": [], "owner_files": len(paths), "manifest_bindings": sum(row["entries"] for row in manifests), "manifest_exclusions": sum(len(row["exclusions"]) for row in manifests), "manifests": manifests, "strict_json_documents": scanned["strict_json"], "python_ast_checks": scanned["python_ast"], "document_checks": scanned["documents"], "largest_document_words": scanned["largest_document_words"], "privacy_candidates": len(scanned["privacy"]["candidates"]), "confirmed_privacy_hits": 0, "bounded_security_findings": 0, "global_parity_files": 56, "environment_distributions": 3, "baton": index, "outcomes": final["outcomes"], "effective_counts": final["effective_counts"], "test_log_sha256": hashlib.sha256(stream.getvalue().encode("utf-8")).hexdigest(), "remote": {"local": head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "divergence": divergence, "clean": True}, "phase_commits": 3, "merge_commits": 0, "final_parent": EVIDENCE, "same_owner_only": True, "full_repository_suite": False, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"}


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--prepare", action="store_true")
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--canonical", action="store_true")
    parser.add_argument("--receipt-root", type=Path)
    parser.add_argument("--skill-root", type=Path)
    parser.add_argument("--runner-root", type=Path)
    parser.add_argument("--environment-python", type=Path)
    args = parser.parse_args()
    if args.prepare:
        prepare(); return
    if args.staged:
        staged(); return
    assert all([args.receipt_root, args.skill_root, args.runner_root, args.environment_python])
    receipt_root = args.receipt_root.resolve()
    assert receipt_root.drive.upper() == "D:" and not receipt_root.is_relative_to(ROOT)
    receipt_root.mkdir(parents=True, exist_ok=True)
    head = git("rev-parse", "HEAD")
    marker = receipt_root / "liora-v688-v1.canonical-invocation.json"
    receipt = receipt_root / ("liora-v688-v1-" + head + ".json")
    assert not marker.exists() and not receipt.exists(), "Canonical invocation already exists; replay refused"
    descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(formatted({"state": "CANONICAL_INVOKED_ONCE", "owner": "Liora Venn", "phase": "v688-v1", "exact_final": head, "started_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}))
    try:
        payload = canonical(args, head)
        wrapped = {"payload": payload, "payload_sha256": hashlib.sha256(formatted(payload)).hexdigest()}
        with receipt.open("xb") as handle:
            handle.write(formatted(wrapped))
        print(json.dumps({"status": payload["status"], "exact_final": head, "selected_tests": payload["selected_tests"], "detailed_checks": payload["detailed_checks"], "owner_files": payload["owner_files"], "manifest_bindings": payload["manifest_bindings"], "manifest_exclusions": payload["manifest_exclusions"], "strict_json_documents": payload["strict_json_documents"], "python_ast_checks": payload["python_ast_checks"], "document_checks": payload["document_checks"], "confirmed_privacy_hits": 0, "bounded_security_findings": 0, "payload_sha256": wrapped["payload_sha256"], "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(), "receipt": receipt.name}, sort_keys=True))
    except Exception as error:
        failed = receipt_root / ("liora-v688-v1-" + head + ".failed.json")
        with failed.open("xb") as handle:
            handle.write(formatted({"status": "FAILED_ZERO_CANONICAL_SUCCESS_CREDIT", "exact_final": head, "error_type": type(error).__name__, "error": str(error)}))
        raise


if __name__ == "__main__":
    main()
