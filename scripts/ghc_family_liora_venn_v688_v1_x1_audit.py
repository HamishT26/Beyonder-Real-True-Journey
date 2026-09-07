"""Validate and bind Liora v688-v1 planning-only x1 without executing x2."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


BASE = "docs/liora-venn/v688-v1/"
SOURCE = "17fee348a09ec1cb480f7326bce70cd75413dad3"
BRANCH = "codex/GHC-Family/liora-venn-v688-v1-full-tools"
EXPECTED_COUNTS = {
    "proposals": 15630,
    "negatives": 82321,
    "methods": 93254,
    "failed_witnesses": 53169,
    "passing_witnesses": 82513,
    "open_gaps": 740,
    "exact_gates": 729,
}
PATTERNS = {
    "raw_identifier": re.compile(r"\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b", re.I),
    "private_absolute_path": re.compile(r"[A-Z]:[/\\](?:Users|GHC-Archives)[/\\]", re.I),
    "private_callable_key": re.compile(r"(?:thread|task|agent|session)_id[\"\x27]?\s*[:=]", re.I),
    "credential_assignment": re.compile(r"(?:api[_-]?key|password|secret|token)[\"\x27]?\s*[:=]\s*[\"\x27]?[A-Za-z0-9_/-]{12,}", re.I),
    "private_stream": re.compile(r"(?:private_transcript|session_stream|screenshot_payload)", re.I),
}


def strict(raw: str):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("DUPLICATE_JSON_KEY")
            out[key] = value
        return out

    def constant(_):
        raise ValueError("NONFINITE_JSON_CONSTANT")

    return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant)


def normalized(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def allowed(path: str) -> bool:
    return (
        path.startswith(BASE)
        or path.startswith("scripts/build_ghc_family_liora_venn_v688_v1_")
        or path.startswith("scripts/ghc_family_liora_venn_v688_v1_")
        or path.startswith("tests/test_ghc_family_liora_venn_v688_v1_")
    )


def owner_files(root: Path):
    paths = []
    for dirname in [BASE, "scripts", "tests"]:
        directory = root / dirname
        if directory.exists():
            for file in directory.rglob("*"):
                if file.is_file():
                    name = file.relative_to(root).as_posix()
                    if allowed(name):
                        paths.append(name)
    return sorted(set(paths))


def privacy(items):
    candidates = []
    for path, raw in items.items():
        text = raw.decode("utf-8")
        definition_lines = set()
        if path.endswith(".py"):
            tree = ast.parse(text)
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign) and any(
                    isinstance(target, ast.Name) and target.id == "PATTERNS"
                    for target in node.targets
                ):
                    definition_lines.update(range(node.lineno, node.end_lineno + 1))
        for label, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                candidates.append(
                    {
                        "path": path,
                        "line": line,
                        "class": label,
                        "adjudication": (
                            "scanner_definition"
                            if line in definition_lines
                            else "confirmed_payload"
                        ),
                    }
                )
    return {
        "schema": "ghc.family.five-class-privacy.v1",
        "classes": list(PATTERNS),
        "files_scanned": len(items),
        "candidates": candidates,
        "confirmed_hits": sum(
            row["adjudication"] == "confirmed_payload" for row in candidates
        ),
        "scope": "Bounded owner text artifacts only; not complete privacy assurance.",
    }


def validate(root: Path):
    get = lambda name: strict((root / BASE / "x1" / name).read_text(encoding="utf-8"))
    proposals = get("new-proposals.json")
    rows = proposals["proposals"]
    inherited = get("inherited-review.json")
    novelty = get("novelty-review.json")
    portfolio = get("portfolio-plan.json")
    truth = get("phase-truth.json")
    skills = get("skill-runner-plan.json")
    wheels = get("wheel-plan.json")
    packages = get("package-plan.json")
    route = get("route-plan.json")
    methods = strict(
        (root / BASE / "x1/method-flow/ledger.json").read_text(encoding="utf-8")
    )
    outcomes = Counter(row["expected_execution_disposition"] for row in rows)
    operation_counts = Counter(row["operation"] for row in rows)
    expected_outcomes = {
        "completed": 160,
        "represented": 14,
        "open_gap": 8,
        "exact_gate": 18,
    }
    checks = {
        "source": truth["source"] == SOURCE,
        "branch": subprocess.check_output(
            ["git", "-C", str(root), "branch", "--show-current"], text=True
        ).strip()
        == BRANCH,
        "planning_only": truth["state"] == "PLANNING_ONLY_FREEZE"
        and not truth["x2_started"]
        and truth["x2_completion_credit"] == 0
        and truth["canonical_invocations"] == 0,
        "no_x2_directory": not (root / BASE / "x2").exists(),
        "proposal_count": len(rows) == 200
        and proposals["count"] == 200
        and proposals["chain_before"] == 15430
        and proposals["chain_after"] == 15630
        and truth["frozen_chain_total"] == 15630,
        "distinct_inputs": len(
            {json.dumps(row["input"], sort_keys=True) for row in rows}
        )
        == 200,
        "ten_operation_families": len(operation_counts) == 10
        and set(operation_counts.values()) == {20},
        "four_outcomes_only": dict(outcomes) == expected_outcomes
        and truth["expected_outcomes"] == expected_outcomes,
        "whole_expected_outputs": all(
            set(row["expected_output"])
            == {"accepted", "value", "error", "external_credit"}
            and type(row["expected_output"]["accepted"]) is bool
            and row["expected_output"]["external_credit"] is False
            for row in rows
        ),
        "proposal_fields": all(
            all(
                field in row
                for field in [
                    "hypothesis",
                    "null_or_failure_condition",
                    "approval_class",
                    "execution_lane",
                    "source_status",
                    "concrete_artifact",
                    "falsifier_or_acceptance_gate",
                    "rollback_or_recovery",
                    "protected_gates",
                    "expected_execution_disposition",
                ]
            )
            for row in rows
        ),
        "no_observed_outcomes": all(
            "outcome" not in row
            and "observed_output" not in row
            and row["execution_lane"] == "x2_only"
            for row in rows
        ),
        "inherited_zero_credit": len(inherited["reviews"]) == 200
        and all(
            row["new_owner_novelty_credit"] == 0
            and row["new_owner_completion_credit"] == 0
            for row in inherited["reviews"]
        ),
        "bounded_novelty": novelty["new_count"] == 200
        and novelty["inherited_review_count"] == 200
        and novelty["exact_title_collisions"] == []
        and novelty["exact_input_collisions"] == 0
        and novelty["quarantined"] is False,
        "portfolio_counts": all(
            len(portfolio[key]) == count
            for key, count in [
                ("safe_now", 300),
                ("candidates", 250),
                ("clean_fix_refine", 300),
                ("exact_packets", 50),
                ("blocked_packets", 30),
            ]
        ),
        "portfolio_unexecuted": not portfolio["execution_started"]
        and all(
            row["executed"] is False
            for key in [
                "safe_now",
                "candidates",
                "clean_fix_refine",
                "exact_packets",
                "blocked_packets",
            ]
            for row in portfolio[key]
        ),
        "skills_and_runners": len(skills["skills"]) == 10
        and len(skills["runners"]) == 5
        and skills["global_promotions"] == {
            "skills": 10,
            "runners": 5,
            "overwrite": False,
            "byte_parity_required": True,
        },
        "three_uninstalled_packages": len(packages["direct_packages"]) == 3
        and packages["installed"] is False
        and packages["network_install"] is False
        and len(wheels["wheels"]) == 3
        and wheels["installed"] is False
        and wheels["rejected_candidate"]["name"] == "srt"
        and wheels["rejected_candidate"]["success_credit"] == 0,
        "no_route_send": route["message_count"] == 0
        and route["precontacted"] is False
        and route["next_owner"] == "future-sibling-11-self-chosen"
        and route["next_phase"] == "v688-v2"
        and route["following_owner"] == "Tamar Vey"
        and route["following_phase"] == "v688-v3",
        "three_overview_pages": (
            root / BASE / "x1/integrated-overview.html"
        ).read_text(encoding="utf-8").count('<section class="page">')
        == 3,
        "retained_pre_x2_failures": len(methods["methods"]) == 19
        and len(methods["witnesses"]) == 38
        and methods["counts"]["methods"] == 19
        and methods["counts"]["witnesses"] == 38
        and methods["counts"]["witness_results"] == {"fail": 19, "pass": 19},
        "effective_counts": truth["effective_activation_counts"] == EXPECTED_COUNTS,
        "terminal_boundary": truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20",
    }
    return checks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--staged", action="store_true")
    args = parser.parse_args()
    root = args.repo.resolve()
    assert (
        subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
        == SOURCE
    )
    checks = validate(root)
    assert all(checks.values()), checks
    out = root / BASE / "validation"
    out.mkdir(parents=True, exist_ok=True)

    def write(name, value):
        (out / name).write_text(
            json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

    if args.staged:
        review = strict(
            subprocess.check_output(
                ["git", "-C", str(root), "show", ":" + BASE + "validation/x1-staged-review.json"]
            ).decode("utf-8")
        )
        manifest = strict(
            subprocess.check_output(
                ["git", "-C", str(root), "show", ":" + BASE + "validation/x1-manifest.json"]
            ).decode("utf-8")
        )
        staged = subprocess.check_output(
            ["git", "-C", str(root), "diff", "--cached", "--name-only"], text=True
        ).splitlines()
        assert staged == review["allowed_paths"], (staged, review["allowed_paths"])
        statuses = subprocess.check_output(
            ["git", "-C", str(root), "diff", "--cached", "--name-status"], text=True
        ).splitlines()
        assert len(statuses) == len(staged) and all(line.startswith("A\t") for line in statuses), statuses
        unstaged = subprocess.check_output(
            ["git", "-C", str(root), "diff", "--name-only"], text=True
        ).splitlines()
        assert unstaged == [], unstaged
        for entry in manifest["entries"]:
            raw = subprocess.check_output(
                ["git", "-C", str(root), "show", ":" + entry["path"]]
            )
            assert len(raw) == entry["bytes_normalized_lf"], entry["path"]
            assert hashlib.sha256(raw).hexdigest() == entry["sha256_normalized_lf"], entry["path"]
        assert manifest["entry_count"] + len(manifest["declared_self_exclusions"]) == len(staged)
        print(
            json.dumps(
                {
                    "state": "X1_EXACT_STAGED_PASS",
                    "staged_paths": len(staged),
                    "change_kind_A": len(statuses),
                    "manifest_entries": manifest["entry_count"],
                    "self_exclusions": len(manifest["declared_self_exclusions"]),
                    "unstaged_paths": 0,
                    "git_blob_mismatches": 0,
                },
                sort_keys=True,
            )
        )
    elif args.write:
        write(
            "x1-checks.json",
            {
                "schema": "ghc.family.x1-structural-checks.v1",
                "checks": checks,
                "execution_credit": 0,
                "state": "PASS",
            },
        )
        write("x1-privacy.json", {"schema": "ghc.family.five-class-privacy.v1", "state": "pending_scan"})
        write("x1-staged-review.json", {"schema": "ghc.family.staged-allowlist.v1", "state": "pending_scan"})
        manifest_path = BASE + "validation/x1-manifest.json"
        paths = sorted(set(owner_files(root) + [manifest_path]))
        assert len(paths) < 2000
        write(
            "x1-staged-review.json",
            {
                "schema": "ghc.family.staged-allowlist.v1",
                "source": SOURCE,
                "allowed_paths": paths,
                "allowed_change_kind": "A",
                "planned_path_count": len(paths),
                "x2_present": False,
            },
        )
        items = {path: normalized(root / path) for path in paths if path != manifest_path}
        scan = privacy(items)
        assert scan["confirmed_hits"] == 0, scan
        write("x1-privacy.json", scan)
        items = {path: normalized(root / path) for path in paths if path != manifest_path}
        strict_count = 0
        ast_count = 0
        for path, raw in items.items():
            if path.endswith(".json"):
                strict(raw.decode("utf-8"))
                strict_count += 1
            if path.endswith(".py"):
                ast.parse(raw.decode("utf-8"), filename=path)
                ast_count += 1
            if path.endswith((".md", ".html", ".txt")):
                assert len(raw.decode("utf-8").split()) <= 100000
        entries = [
            {
                "path": path,
                "bytes_normalized_lf": len(raw),
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
            for path, raw in items.items()
        ]
        write(
            "x1-manifest.json",
            {
                "schema": "ghc.family.normalized-lf-manifest.v1",
                "byte_domain": "normalized_lf_git_blob",
                "source": SOURCE,
                "anchor": "PENDING_X1_COMMIT",
                "entries": entries,
                "entry_count": len(entries),
                "declared_self_exclusions": [manifest_path],
            },
        )
        print(
            json.dumps(
                {
                    "state": "X1_STRUCTURAL_PASS",
                    "checks": len(checks),
                    "manifest_entries": len(entries),
                    "self_exclusions": 1,
                    "owner_files": len(paths),
                    "strict_json": strict_count,
                    "python_ast": ast_count,
                    "confirmed_privacy_hits": 0,
                    "retained_failures": 19,
                    "x2_execution_credit": 0,
                },
                sort_keys=True,
            )
        )
    else:
        print(json.dumps({"state": "X1_STRUCTURAL_PASS", "checks": checks}, sort_keys=True))


if __name__ == "__main__":
    main()
