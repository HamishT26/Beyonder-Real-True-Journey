"""One-shot exact-final canonical validation for the Neris v686-v1 owner delta."""
from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import unittest
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
SOURCE = "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2"
X1 = "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323"
EVIDENCE = "71f45ab2a9bb4ff239f09c79af5b94bc889b5127"
BRANCH = "codex/GHC-Family/neris-solane-v686-v1-full-tools"


def git(*args: str, input_bytes: bytes | None = None) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], input=input_bytes)


def canonical(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def blob_batch(refs: list[str]) -> list[bytes]:
    if not refs:
        return []
    raw = git("cat-file", "--batch", input_bytes=("\n".join(refs) + "\n").encode("utf-8"))
    values = []
    position = 0
    for ref in refs:
        end = raw.index(b"\n", position)
        header = raw[position:end].split()
        if len(header) != 3:
            raise ValueError("Missing declared blob: " + ref)
        size = int(header[2])
        values.append(raw[end + 1 : end + 1 + size])
        position = end + size + 2
    return values


def replay_manifest(path: str, revision: str | None = None) -> dict:
    manifest = json.loads((ROOT / path).read_text(encoding="utf-8"))
    entries = manifest["entries"]
    paths = [row["path"] for row in entries]
    if len(paths) != len(set(paths)):
        return {"valid": False, "entries": len(entries), "failures": ["duplicate_paths"]}
    if revision:
        blobs = blob_batch([revision + ":" + path for path in paths])
    else:
        blobs = []
        for path in paths:
            data = (ROOT / path).read_bytes()
            blobs.append(data if Path(path).suffix.lower() == ".pdf" else data.replace(b"\r\n", b"\n"))
    failures = [row["path"] for row, blob in zip(entries, blobs) if len(blob) != row["bytes"] or sha_bytes(blob) != row["sha256"]]
    return {"valid": not failures, "entries": len(entries), "failures": failures}


class StructuralHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = Counter()
        self.lang = False
        self.headers = True

    def handle_starttag(self, tag, attrs):
        self.tags[tag] += 1
        values = dict(attrs)
        if tag == "html":
            self.lang = bool(values.get("lang"))
        if tag == "th" and values.get("scope") not in ("row", "col"):
            self.headers = False


def owner_paths_from_manifest() -> list[Path]:
    manifest = read("validation/final-owner-manifest.json")
    return [ROOT / row["path"] for row in manifest["entries"]] + [ROOT / path for path in manifest["self_exclusions"]]


def tree_checks(paths: list[Path] | None = None) -> dict:
    paths = paths or owner_paths_from_manifest()
    counts = Counter()
    structure_failures = []
    privacy_candidates = []
    security_findings = []
    patterns = {
        "local_path": r"(?i)\b[CD]:[\\/](?:Users|GHC-Archives)[\\/]",
        "private_uuid": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
        "private_key": r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
        "credential": r"\bsk-[A-Za-z0-9]{20,}\b",
        "callable_route": r'(?i)"(?:thread_id|threadId|session_id|providerTabId)"\s*:\s*"[^"\n]+"',
    }
    for path in paths:
        if not path.is_file():
            structure_failures.append([path.relative_to(ROOT).as_posix(), "missing"])
            continue
        counts["owner_files"] += 1
        relative = path.relative_to(ROOT).as_posix()
        if path.suffix.lower() == ".pdf":
            counts["pdf"] += 1
            continue
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            structure_failures.append([relative, "utf8", str(exc)])
            continue
        for category, pattern in patterns.items():
            for match in re.finditer(pattern, text):
                privacy_candidates.append({"path": relative, "class": category, "offset": match.start(), "length": len(match.group())})
        try:
            if path.suffix == ".json":
                json.loads(text)
                counts["json"] += 1
            elif path.suffix == ".py":
                tree = ast.parse(text)
                counts["python_ast"] += 1
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                        security_findings.append([relative, node.lineno, node.func.id])
            elif path.suffix in (".yaml", ".yml"):
                if not isinstance(yaml.safe_load(text), dict):
                    raise ValueError("YAML mapping required")
                counts["yaml"] += 1
            elif path.suffix == ".md":
                body = text
                if text.startswith("---\n"):
                    end = text.find("\n---\n", 4)
                    if end < 0:
                        raise ValueError("Unclosed YAML frontmatter")
                    frontmatter = yaml.safe_load(text[4:end])
                    if not isinstance(frontmatter, dict) or not frontmatter.get("name") or not frontmatter.get("description"):
                        raise ValueError("Missing skill frontmatter identity")
                    body = text[end + 5 :]
                if not re.search(r"(?m)^#{1,6} ", body):
                    raise ValueError("Missing Markdown heading")
                counts["markdown"] += 1
            elif path.suffix == ".html":
                parser = StructuralHTML()
                parser.feed(text)
                if not (parser.lang and parser.tags["main"] and parser.tags["h1"] and parser.tags["table"] and parser.tags["caption"] and parser.headers):
                    raise ValueError("HTML structural relation")
                counts["html"] += 1
        except Exception as exc:
            structure_failures.append([relative, type(exc).__name__, str(exc)])
    return {
        "counts": dict(counts),
        "structure_failures": structure_failures,
        "structure_valid": not structure_failures,
        "privacy_classes": list(patterns),
        "privacy_candidates": privacy_candidates,
        "privacy_confirmed_hits": len(privacy_candidates),
        "security_findings": security_findings,
        "bounded_security_findings": len(security_findings),
    }


def deck_check() -> dict:
    cards = [json.loads(path.read_text(encoding="utf-8")) for path in sorted((BASE / "x2/flashcards/cards").glob("*.json"))]
    by_id = {card["card_id"]: card for card in cards}
    failures = []
    for item in cards:
        payload = {key: value for key, value in item.items() if key != "card_id"}
        if "ghc-card-" + sha_bytes(canonical(payload))[:24] != item["card_id"]:
            failures.append([item["card_id"], "digest"])
        parents = item["parent_ids"]
        if item["tier"] == 1:
            if parents:
                failures.append([item["card_id"], "root_parent"])
        elif len(parents) != 1 or parents[0] not in by_id or by_id[parents[0]]["tier"] != item["tier"] - 1:
            failures.append([item["card_id"], "tier_parent"])
        if item["outcome"] not in ("completed", "represented", "open_gap", "exact_gate"):
            failures.append([item["card_id"], "outcome"])
    return {"valid": not failures and len(by_id) == len(cards) == 208, "cards": len(cards), "failures": failures}


def method_check() -> dict:
    ledger = read("x2/method-flow.json")
    methods = ledger["methods"]
    witnesses = ledger["witnesses"]
    by_witness = {row["witness_id"]: row for row in witnesses}
    fail_negatives = {negative for row in witnesses if row["result"] == "fail" for negative in row["retained_negative_ids"]}
    failures = []
    for method in methods:
        if not method["retained_negative_ids"] or not set(method["retained_negative_ids"]) <= fail_negatives:
            failures.append([method["method_id"], "negative_links"])
        if not all(witness in by_witness for witness in method["validation_witness_ids"]):
            failures.append([method["method_id"], "witness_links"])
        elif not any(by_witness[witness]["result"] == "pass" for witness in method["validation_witness_ids"]):
            failures.append([method["method_id"], "unvalidated"])
    actual = {
        "methods": len(methods),
        "failed_witnesses": sum(row["result"] == "fail" for row in witnesses),
        "bounded_passing_witnesses": sum(row["result"] == "pass" for row in witnesses),
        "retained_negatives": len(fail_negatives),
    }
    return {"valid": not failures and actual == ledger["counts"], "counts": actual, "failures": failures}


def equality() -> dict:
    head = git("rev-parse", "HEAD").decode().strip()
    upstream = git("rev-parse", "@{upstream}").decode().strip()
    tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH).decode().strip()
    live = git("ls-remote", "--exit-code", "origin", "refs/heads/" + BRANCH).decode().split()[0]
    return {
        "head": head,
        "upstream": upstream,
        "tracking": tracking,
        "live": live,
        "four_way_equal": len({head, upstream, tracking, live}) == 1,
        "clean": not git("status", "--porcelain").strip(),
        "divergence": git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").decode().strip(),
        "branch": git("branch", "--show-current").decode().strip(),
    }


def run_tests() -> dict:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    for module_name in ["tests.test_ghc_family_neris_solane_v686_v1_x2", "tests.test_ghc_family_neris_solane_v686_v1_final"]:
        module = __import__(module_name, fromlist=["*"])
        suite.addTests(loader.loadTestsFromModule(module))
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=1).run(suite)
    return {
        "passed": result.wasSuccessful(),
        "tests_run": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "output": stream.getvalue(),
    }


def global_parity(global_root: Path) -> dict:
    receipt = read("x2/global-promotion-installation.json")
    failures = []
    file_count = 0
    for skill in receipt["skills"]:
        folder = global_root / skill["name"]
        actual = sorted(path.relative_to(folder).as_posix() for path in folder.rglob("*") if path.is_file()) if folder.is_dir() else []
        expected = sorted(row["path"] for row in skill["files"])
        if actual != expected:
            failures.append([skill["name"], "file_set"])
        for row in skill["files"]:
            file_count += 1
            path = folder / row["path"]
            if not path.is_file() or sha_bytes(path.read_bytes()) != row["sha256"] or path.stat().st_size != row["bytes"]:
                failures.append([skill["name"], row["path"]])
    return {"valid": not failures and len(receipt["skills"]) == 10, "skills": len(receipt["skills"]), "files": file_count, "failures": failures}


def put_exclusive(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", required=True)
    parser.add_argument("--receipt", required=True, type=Path)
    parser.add_argument("--global-root", required=True, type=Path)
    args = parser.parse_args()
    receipt = args.receipt.resolve()
    marker = Path(str(receipt) + ".invoked")
    if receipt.is_relative_to(ROOT.resolve()):
        raise ValueError("Canonical receipt must be outside the sealed repository")
    if receipt.exists() or marker.exists():
        raise FileExistsError("Canonical invocation or receipt already exists; replay refused")
    if git("rev-parse", "HEAD").decode().strip() != args.final:
        raise ValueError("Exact final argument must match HEAD before invocation")
    put_exclusive(marker, {"owner": "Neris Solane", "phase": "v686-v1", "head": args.final, "invocations": 1, "replay_permitted": False})
    result = {
        "schema": "ghc.family.neris.exact-final-canonical.v1",
        "owner": "Neris Solane",
        "phase": "v686-v1",
        "head": args.final,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "canonical_invocation_count": 1,
        "canonical_success_count": 0,
        "canonical_replay_count": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "complete_repository_suite": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
    }
    try:
        policy = read("final/validation-policy.json")
        before = equality()
        scope_rows = git("diff", "--name-status", SOURCE, args.final).decode().splitlines()
        changes = [row.split("\t", 1) for row in scope_rows]
        names = sorted(row[1] for row in changes)
        checks = {
            "exact_final": before["head"] == args.final,
            "exact_branch": before["branch"] == BRANCH,
            "clean_before": before["clean"],
            "four_way_before": before["four_way_equal"],
            "zero_divergence_before": before["divergence"] == "0\t0",
            "only_owner_additions": all(row[0] == "A" for row in changes),
            "owner_file_ceiling": len(names) < 2000,
            "three_commits": git("rev-list", "--count", SOURCE + ".." + args.final).decode().strip() == "3",
            "zero_merges": git("rev-list", "--merges", SOURCE + ".." + args.final).strip() == b"",
            "source_x1_edge": git("rev-parse", X1 + "^").decode().strip() == SOURCE,
            "x1_evidence_edge": git("rev-parse", EVIDENCE + "^").decode().strip() == X1,
            "evidence_final_edge": git("rev-list", "--parents", "-n", "1", args.final).decode().split() == [args.final, EVIDENCE],
        }
        manifest_specs = [
            ("x1", "docs/neris-solane/v686-v1/validation/x1-manifest.json", X1),
            ("evidence", "docs/neris-solane/v686-v1/validation/evidence-manifest.json", EVIDENCE),
            ("cards", "docs/neris-solane/v686-v1/x2/flashcards/card-manifest.json", EVIDENCE),
            ("final_delta", "docs/neris-solane/v686-v1/validation/final-manifest.json", args.final),
            ("owner", "docs/neris-solane/v686-v1/validation/final-owner-manifest.json", args.final),
        ]
        manifests = {label: replay_manifest(path, revision) for label, path, revision in manifest_specs}
        checks["manifest_replay"] = all(row["valid"] for row in manifests.values())
        owner_manifest = read("validation/final-owner-manifest.json")
        checks["manifest_scope_complete"] = set(names) == set(row["path"] for row in owner_manifest["entries"]) | set(owner_manifest["self_exclusions"])
        final_names = git("diff", "--name-only", EVIDENCE, args.final).decode().splitlines()
        final_manifest = read("validation/final-manifest.json")
        checks["final_delta_scope_complete"] = set(final_names) == set(row["path"] for row in final_manifest["entries"]) | set(final_manifest["self_exclusions"])
        tree = tree_checks()
        checks.update(
            json_markdown_yaml_python_html_structure=tree["structure_valid"],
            privacy_hits_zero=tree["privacy_confirmed_hits"] == 0,
            bounded_security_findings_zero=tree["bounded_security_findings"] == 0,
        )
        deck = deck_check()
        method = method_check()
        checks["card_graph_and_addresses"] = deck["valid"]
        checks["method_flow_links_and_counts"] = method["valid"]
        seal = read("final/content-seal.json")
        seal_blobs = blob_batch([args.final + ":" + row["path"] for row in seal["targets"]])
        checks["ten_content_seal_targets"] = len(seal_blobs) == 10 and all(len(blob) == row["bytes"] and sha_bytes(blob) == row["sha256"] for row, blob in zip(seal["targets"], seal_blobs))
        parity = global_parity(args.global_root)
        checks["ten_global_skills_byte_parity"] = parity["valid"] and parity["skills"] == 10
        checks["five_unique_runners"] = read("x2/global-promotion-installation.json")["unique_shared_report_runners"] == 5
        baton = read("final/baton-integrity.json")
        checks["baton_word_and_section_bounds"] = 10000 <= baton["words"] <= 100000 and baton["sections"] == 13
        pdf = read("final/overview-pdf-validation.json")
        visual = read("final/overview-visual-review.json")
        checks["overview_at_least_three_pages"] = pdf["pages"] >= 3 and pdf["pdf_text_extraction_pass"] and visual["all_pages_reviewed"] and visual["layout_issues"] == []
        tests = run_tests()
        checks["selected_owner_tests"] = tests["passed"] and tests["tests_run"] == 38
        packages = read("x2/toolchain/installation-receipt.json")
        smokes = read("x2/toolchain/package-smokes.json")
        checks["three_exact_package_additions"] = packages["direct_additions"] == 3 and len(packages["installed_distributions"]) == 3 and smokes["positive_passed"] == 3 and smokes["adverse_rejected"] == 3
        catalogue = read("tooling/catalogue-validation.json")
        collisions = read("tooling/collision-adjudication.json")
        checks["toolbox_and_collision_adjudication"] = catalogue["valid"] and len(collisions["rows"]) == 13 and not collisions["silent_winner"]
        after = equality()
        checks.update(
            clean_after=after["clean"],
            four_way_after=after["four_way_equal"],
            zero_divergence_after=after["divergence"] == "0\t0",
            head_unchanged=after["head"] == args.final,
        )
        result.update(
            checks=checks,
            counts={
                **tree["counts"],
                "detailed_checks": len(checks),
                "passed_checks": sum(checks.values()),
                "tests": tests["tests_run"],
                "manifest_entries": sum(row["entries"] for row in manifests.values()),
                "global_files": parity["files"],
                "cards": deck["cards"],
                "baton_words": baton["words"],
                "overview_words": baton["overview_words"],
                "overview_pages": pdf["pages"],
                "privacy_confirmed_hits": tree["privacy_confirmed_hits"],
                "bounded_security_findings": tree["bounded_security_findings"],
            },
            manifests=manifests,
            tests=tests,
            tree=tree,
            before=before,
            after=after,
            global_parity=parity,
            scope={
                "changed_file_allowlist": names,
                "test_modules": policy["test_modules"],
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "repository_suite": False,
            },
        )
        if all(checks.values()):
            result["status"] = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
            result["canonical_success_count"] = 1
    except Exception as exc:
        result.update(failure_type=type(exc).__name__, failure=str(exc), canonical_success_count=0)
    result["payload_sha256"] = sha_bytes(canonical(result))
    put_exclusive(receipt, result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "head": result["head"],
                "counts": result.get("counts", {}),
                "failed_checks": [name for name, passed in result.get("checks", {}).items() if not passed],
                "failure": result.get("failure"),
                "canonical_invocation_count": 1,
                "canonical_success_count": result["canonical_success_count"],
                "canonical_replay_count": 0,
            },
            sort_keys=True,
        )
    )
    return 0 if result["canonical_success_count"] == 1 else 1


if __name__ == "__main__":
    raise SystemExit(main())
