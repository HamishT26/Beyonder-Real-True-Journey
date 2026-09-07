"""Validate and bind Liora v688-v1 x2 evidence without touching inherited lanes."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


BASE = "docs/liora-venn/v688-v1/"
SOURCE = "17fee348a09ec1cb480f7326bce70cd75413dad3"
X1 = "421abce86426674b67e0cbd5ce63ad463421fc9f"
BRANCH = "codex/GHC-Family/liora-venn-v688-v1-full-tools"
EXPECTED_OUTCOMES = {"completed": 160, "represented": 14, "open_gap": 8, "exact_gate": 18}
EXPECTED_COUNTS = {"proposals": 15630, "negatives": 82596, "methods": 93289, "failed_witnesses": 53444, "passing_witnesses": 83006, "open_gaps": 748, "exact_gates": 747}
PATTERNS = {
    "raw_identifier": re.compile(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", re.I),
    "private_absolute_path": re.compile(r"[A-Z]:[/\\](?:Users|GHC-Archives)[/\\]", re.I),
    "private_callable_key": re.compile(r"(?:thread|task|agent|session)_id[\"\x27]?\s*[:=]", re.I),
    "credential_assignment": re.compile(r"(?:api[_-]?key|password|secret|token)[\"\x27]?\s*[:=]\s*[\"\x27]?[A-Za-z0-9_/-]{12,}", re.I),
    "private_stream": re.compile(r"(?:private_transcript|session_stream|screenshot_payload)", re.I),
}


def strict(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("DUPLICATE_JSON_KEY")
            result[key] = value
        return result

    def constant(_):
        raise ValueError("NONFINITE_JSON_CONSTANT")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")


def normalized(path):
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def allowed(path):
    return (
        path.startswith(BASE + "x2/")
        or path.startswith(BASE + "skills/")
        or path.startswith("scripts/build_ghc_family_liora_venn_v688_v1_x2")
        or path.startswith("scripts/ghc_family_liora_venn_v688_v1_")
        or path.startswith("scripts/ghc_family_caption_")
        or path.startswith("tests/test_ghc_family_liora_venn_v688_v1_")
    )


def exists_at(root, commit, path):
    return subprocess.run(["git", "-C", str(root), "cat-file", "-e", commit + ":" + path], capture_output=True).returncode == 0


def all_owner_files(root):
    paths = []
    for dirname in [BASE, "scripts", "tests"]:
        directory = root / dirname
        if directory.exists():
            for path in directory.rglob("*"):
                if path.is_file():
                    name = path.relative_to(root).as_posix()
                    if name.startswith(BASE) or allowed(name) or name.startswith("scripts/build_ghc_family_liora_venn_v688_v1_x1") or name.startswith("scripts/ghc_family_liora_venn_v688_v1_x1") or name == "scripts/ghc_family_liora_venn_v688_v1_fixtures.py":
                        paths.append(name)
    return sorted(set(paths))


def evidence_files(root):
    return [path for path in all_owner_files(root) if allowed(path) and not exists_at(root, X1, path)]


def privacy(items):
    candidates = []
    for path, raw in items.items():
        text = raw.decode("utf-8")
        definition_lines = set()
        if path.endswith(".py"):
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "PATTERNS" for target in node.targets):
                    definition_lines.update(range(node.lineno, node.end_lineno + 1))
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                candidates.append({"path": path, "line": line, "class": label, "adjudication": "scanner_definition" if line in definition_lines else "confirmed_payload"})
    return {"schema": "ghc.family.five-class-privacy.v1", "classes": list(PATTERNS), "files_scanned": len(items), "candidates": candidates, "confirmed_hits": sum(row["adjudication"] == "confirmed_payload" for row in candidates), "scope": "Bounded Liora x2 text artifacts only; not complete privacy assurance."}


def security(items):
    findings = []
    for path, raw in items.items():
        if not path.endswith(".py"):
            continue
        tree = ast.parse(raw.decode("utf-8"), filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name):
                    name = node.func.value.id + "." + node.func.attr
                if name in {"eval", "exec", "os.system"}:
                    findings.append({"path": path, "line": node.lineno, "class": "dynamic_execution"})
                if name in {"subprocess.run", "subprocess.Popen", "subprocess.call", "subprocess.check_call", "subprocess.check_output"} and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                    findings.append({"path": path, "line": node.lineno, "class": "shell_true"})
    return {"schema": "ghc.family.bounded-python-security.v1", "python_files": sum(path.endswith(".py") for path in items), "findings": findings, "finding_count": len(findings), "exhaustive_security": False}


def local_skill_check(root, plan):
    total_members = 0
    for item in plan["skills"]:
        directory = root / BASE / "skills" / item["name"]
        manifest = strict((directory / "manifest.json").read_text(encoding="utf-8"))
        actual = {path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file()}
        expected = {row["relative"] for row in manifest["members"]} | {"manifest.json"}
        if actual != expected:
            return False, total_members
        for row in manifest["members"]:
            if hashlib.sha256((directory / row["relative"]).read_bytes()).hexdigest() != row["sha256"]:
                return False, total_members
        total_members += len(actual)
    return total_members == 50, total_members


def promotion_parity(root, receipt, skill_root, runner_root):
    for row in receipt["members"]:
        source = root / row["source"]
        destination = skill_root / row["name"] / row["relative"] if row["kind"] == "skill" else runner_root / row["relative"]
        if not destination.is_file() or source.read_bytes() != destination.read_bytes() or hashlib.sha256(source.read_bytes()).hexdigest() != row["sha256"]:
            return False
    return True


def deck_check(root):
    deck = root / BASE / "x2/deck"
    index = strict((deck / "deck-index.json").read_text(encoding="utf-8"))
    cards = [strict((deck / "cards" / (identifier + ".json")).read_text(encoding="utf-8")) for identifier in index["cards"]]
    by_id = {row["card_id"]: row for row in cards}
    if len(cards) != len(by_id) or len(cards) != 208 or index["counts"] != {"owner": 1, "pillar": 3, "practice": 4, "task": 200}:
        return False
    for row in cards:
        if row["tier"] == 1 and row["parent_ids"] != []:
            return False
        if row["tier"] > 1 and (len(row["parent_ids"]) != 1 or row["parent_ids"][0] not in by_id or by_id[row["parent_ids"][0]]["tier"] != row["tier"] - 1):
            return False
    manifest = strict((deck / "card-manifest.json").read_text(encoding="utf-8"))
    if manifest["card_count"] != 208 or len(manifest["entries"]) != 214:
        return False
    return all((root / row["path"]).is_file() and (root / row["path"]).stat().st_size == row["bytes"] and hashlib.sha256((root / row["path"]).read_bytes()).hexdigest() == row["sha256"] for row in manifest["entries"])


def validate(root, skill_root, runner_root):
    get = lambda path: strict((root / BASE / path).read_text(encoding="utf-8"))
    proposals = get("x1/new-proposals.json")["proposals"]
    proposal_map = {row["proposal_id"]: row for row in proposals}
    results = get("x2/contract-results.json")
    mutations = get("x2/mutation-results.json")
    portfolio = get("x2/portfolio-results.json")
    skills = get("x2/skill-validation.json")
    runners = get("x2/runner-smokes.json")
    packages = get("x2/package-smokes.json")
    environment = get("x2/environment-receipt.json")
    promotion = get("x2/promotion-receipt.json")
    truth = get("x2/phase-truth.json")
    ledger = get("x2/method-flow/ledger.json")
    retained = get("x2/retained-negative-register.json")
    gaps = get("x2/open-gap-register.json")
    gates = get("x2/exact-gate-register.json")
    execution = get("x2/execution-summary.json")
    plan = get("x1/skill-runner-plan.json")
    route = get("x1/route-plan.json")
    local_skills, local_skill_members = local_skill_check(root, plan)
    result_rows = {row["proposal_id"]: row for row in results["rows"]}
    outcomes = Counter(row["outcome"] for row in result_rows.values())
    x1_changed = subprocess.check_output(["git", "-C", str(root), "diff", "--name-only", X1, "--", BASE + "x1", "scripts/build_ghc_family_liora_venn_v688_v1_x1.py", "scripts/ghc_family_liora_venn_v688_v1_fixtures.py", "scripts/ghc_family_liora_venn_v688_v1_x1_audit.py"], text=True).splitlines()
    dirty = [line[3:].replace("\\", "/") for line in subprocess.check_output(["git", "-C", str(root), "status", "--porcelain=v1", "--untracked-files=all"], text=True).splitlines()]
    checks = {
        "exact_x1_head": subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip() == X1,
        "exact_branch": subprocess.check_output(["git", "-C", str(root), "branch", "--show-current"], text=True).strip() == BRANCH,
        "x1_immutable": x1_changed == [],
        "owner_paths_only": all(allowed(path) for path in dirty),
        "proposal_chain": len(proposals) == 200 and get("x1/new-proposals.json")["chain_after"] == 15630,
        "results_complete": results["count"] == 200 and len(result_rows) == 200 and all(row["pass"] and row["complete_match"] and row["input_unchanged"] and canonical(row["actual_output"]) == canonical(proposal_map[row["proposal_id"]]["expected_output"]) for row in result_rows.values()),
        "outcomes": dict(outcomes) == EXPECTED_OUTCOMES and truth["outcomes"] == EXPECTED_OUTCOMES,
        "mutations": mutations["count"] == mutations["rejected"] == 250 and len(mutations["rows"]) == 250 and all(row["rejected"] and row["original_candidate_success_credit"] == 0 for row in mutations["rows"]),
        "portfolio_counts": all(len(portfolio[key]) == count for key, count in [("safe_now", 300), ("candidates", 250), ("clean_fix_refine", 300), ("exact_packets", 50), ("blocked_packets", 30)]),
        "portfolio_execution": all(row["executed"] and row["procedure_pass"] for key in ["safe_now", "candidates", "clean_fix_refine"] for row in portfolio[key]) and all(not row["executed"] for key in ["exact_packets", "blocked_packets"] for row in portfolio[key]),
        "local_skills": local_skills and local_skill_members == 50 and skills["validated_and_used"] == skills["complete_read_before_use"] == 10 and all(row["quick_validate_returncode"] == 0 and row["eof_read_before_smoke"] and row["positive_pass"] and row["adverse_rejected"] for row in skills["rows"]),
        "local_runners": runners["validated_and_used"] == 5 and runners["operation_smokes"] == 10 and all(row["positive_pass"] and row["adverse_rejected"] and len(row["positive_rows"]) == 2 for row in runners["rows"]),
        "packages": packages["distribution_count"] == 3 and len(packages["positive"]) == len(packages["adverse"]) == 3 and environment["distribution_count"] == 3 and environment["declared_dependencies"] == 0 and environment["hash_required"] and environment["wheel_only"] and environment["no_index_install"],
        "promotion_shape": promotion["skill_count"] == 10 and promotion["runner_count"] == 5 and promotion["file_count"] == len(promotion["members"]) == 56 and promotion["overwrites"] == 0 and promotion["source_global_byte_equal"],
        "promotion_parity": promotion_parity(root, promotion, skill_root, runner_root),
        "deck": deck_check(root),
        "method_flow": len(ledger["methods"]) == 35 and len(ledger["witnesses"]) == 768 and len(ledger["state_events"]) == 105 and ledger["counts"] == {"methods": 35, "witnesses": 768, "state_events": 105, "recommendations": 0, "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": 35, "superseded": 0, "validated": 0}, "witness_results": {"fail": 275, "pass": 493}},
        "retained_failures": len(retained["operational_failures"]) == 7 and retained["x2_delta"] == {"negatives": 275, "methods": 35, "failed_witnesses": 275, "passing_witnesses": 493} and retained["erased_negative_count"] == retained["failed_candidates_promoted"] == 0,
        "effective_counts": truth["effective_counts"] == EXPECTED_COUNTS and retained["effective_counts"] == EXPECTED_COUNTS,
        "gap_counts": gaps["inherited"] == 740 and gaps["phase_added"] == 8 and gaps["effective"] == 748 and gaps["closed_by_software"] == 0,
        "gate_counts": gates["inherited"] == 729 and gates["phase_added"] == 18 and gates["effective"] == 747 and gates["closed_by_software"] == 0 and gates["maori_concepts_under_maori_authority"],
        "execution": execution["frozen_contract_matches"] == 200 and execution["altered_outputs_rejected"] == 250 and execution["deck_cards"] == 208 and execution["retained_operational_failures"] == 7 and execution["real_media_rows"] == execution["external_actions"] == 0,
        "route_unsent": route["message_count"] == 0 and not route["precontacted"] and not truth["successor_contacted"] and not truth["successor_created"],
        "terminal": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20" and truth["canonical_invocations"] == truth["canonical_successes"] == 0,
        "owner_file_ceiling": len(all_owner_files(root)) < 2000,
    }
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    parser.add_argument("--runner-root", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    root = args.repo.resolve()
    checks = validate(root, args.skill_root, args.runner_root)
    assert all(checks.values()), checks
    out = root / BASE / "x2/validation"
    out.mkdir(parents=True, exist_ok=True)

    def write(name, value):
        (out / name).write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")

    if args.staged:
        review = strict(subprocess.check_output(["git", "-C", str(root), "show", ":" + BASE + "x2/validation/evidence-staged-review.json"]).decode("utf-8"))
        manifest = strict(subprocess.check_output(["git", "-C", str(root), "show", ":" + BASE + "x2/validation/evidence-manifest.json"]).decode("utf-8"))
        staged = subprocess.check_output(["git", "-C", str(root), "diff", "--cached", "--name-only"], text=True).splitlines()
        assert staged == review["allowed_paths"], (staged, review["allowed_paths"])
        statuses = subprocess.check_output(["git", "-C", str(root), "diff", "--cached", "--name-status"], text=True).splitlines()
        assert len(statuses) == len(staged) and all(line.startswith("A\t") for line in statuses), statuses
        assert subprocess.check_output(["git", "-C", str(root), "diff", "--name-only"], text=True).splitlines() == []
        raw_index = subprocess.check_output(["git", "-C", str(root), "diff", "--cached", "--raw", "--no-abbrev"], text=True).splitlines()
        object_ids = {}
        for line in raw_index:
            metadata, path = line.split("\t", 1)
            fields = metadata.split()
            object_ids[path] = fields[3]
        process = subprocess.Popen(["git", "-C", str(root), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            for entry in manifest["entries"]:
                process.stdin.write((object_ids[entry["path"]] + "\n").encode("ascii")); process.stdin.flush()
                header = process.stdout.readline().decode("ascii").strip().split()
                assert len(header) == 3 and header[1] == "blob", (entry["path"], header)
                raw = process.stdout.read(int(header[2])); assert process.stdout.read(1) == b"\n"
                assert len(raw) == entry["bytes_normalized_lf"] and hashlib.sha256(raw).hexdigest() == entry["sha256_normalized_lf"], entry["path"]
        finally:
            process.stdin.close(); process.wait(timeout=10)
        assert manifest["entry_count"] + len(manifest["declared_self_exclusions"]) == len(staged)
        print(json.dumps({"state": "X2_EXACT_STAGED_PASS", "staged_paths": len(staged), "manifest_entries": manifest["entry_count"], "self_exclusions": len(manifest["declared_self_exclusions"]), "git_blob_mismatches": 0, "unstaged_paths": 0}, sort_keys=True))
        return

    if args.write:
        test = subprocess.run([sys.executable, "-X", "utf8", "-m", "unittest", "-v", "tests.test_ghc_family_liora_venn_v688_v1_caption"], cwd=root, capture_output=True, text=True, encoding="utf-8")
        combined = test.stdout + test.stderr
        assert test.returncode == 0 and "Ran 28 tests" in combined and combined.rstrip().endswith("OK"), combined
        write("owner-test-receipt.json", {"schema": "ghc.family.owner-test-receipt.v1", "selection": ["tests.test_ghc_family_liora_venn_v688_v1_caption"], "tests": 28, "failures": 0, "errors": 0, "returncode": 0, "output_tail": [line for line in combined.splitlines() if line.startswith("Ran ") or line == "OK"], "full_repository_suite": False, "same_owner_only": True})
        write("evidence-checks.json", {"schema": "ghc.family.x2-structural-checks.v1", "checks": checks, "check_count": len(checks), "state": "PASS", "canonical_credit": 0})
        write("evidence-privacy.json", {"schema": "ghc.family.five-class-privacy.v1", "state": "pending_scan"})
        write("evidence-security.json", {"schema": "ghc.family.bounded-python-security.v1", "state": "pending_scan"})
        write("evidence-staged-review.json", {"schema": "ghc.family.staged-allowlist.v1", "state": "pending_scan"})
        manifest_path = BASE + "x2/validation/evidence-manifest.json"
        privacy_path = BASE + "x2/validation/evidence-privacy.json"
        security_path = BASE + "x2/validation/evidence-security.json"
        paths = sorted(set(evidence_files(root) + [manifest_path]))
        assert len(all_owner_files(root)) < 2000 and len(paths) < 2000
        write("evidence-staged-review.json", {"schema": "ghc.family.staged-allowlist.v1", "x1": X1, "allowed_paths": paths, "allowed_change_kind": "A", "planned_path_count": len(paths), "x1_paths_allowed": False})
        privacy_items = {path: normalized(root / path) for path in paths if path not in {manifest_path, privacy_path, security_path}}
        scan = privacy(privacy_items)
        scan["declared_self_exclusions"] = [privacy_path, security_path, manifest_path]
        assert scan["confirmed_hits"] == 0, scan
        write("evidence-privacy.json", scan)
        security_items = {path: normalized(root / path) for path in paths if path.endswith(".py")}
        security_scan = security(security_items)
        assert security_scan["finding_count"] == 0, security_scan
        write("evidence-security.json", security_scan)
        items = {path: normalized(root / path) for path in paths if path != manifest_path}
        strict_count = python_count = document_count = 0
        max_words = 0
        for path, raw in items.items():
            text = raw.decode("utf-8")
            if path.endswith(".json"):
                strict(text); strict_count += 1
            if path.endswith(".py"):
                ast.parse(text, filename=path); python_count += 1
            if path.endswith((".md", ".html", ".txt")):
                words = len(text.split()); max_words = max(max_words, words); document_count += 1; assert words <= 100000
            if path.endswith(".html"):
                assert "<html" in text and "<main" in text
        entries = [{"path": path, "bytes_normalized_lf": len(raw), "sha256_normalized_lf": hashlib.sha256(raw).hexdigest()} for path, raw in items.items()]
        write("evidence-manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "byte_domain": "normalized_lf_git_blob", "x1": X1, "anchor": "PENDING_EVIDENCE_COMMIT", "entries": entries, "entry_count": len(entries), "declared_self_exclusions": [manifest_path]})
        print(json.dumps({"state": "X2_STRUCTURAL_PASS", "checks": len(checks), "owner_tests": 28, "manifest_entries": len(entries), "self_exclusions": 1, "owner_files": len(all_owner_files(root)), "strict_json": strict_count, "python_ast": python_count, "documents": document_count, "maximum_document_words": max_words, "privacy_candidates": len(scan["candidates"]), "confirmed_privacy_hits": 0, "security_findings": 0}, sort_keys=True))
    else:
        print(json.dumps({"state": "X2_STRUCTURAL_PASS", "checks": checks}, sort_keys=True))


if __name__ == "__main__":
    main()
