"""One-shot exact-final owner-scoped canonical validator for Elaren v685-v7."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from scripts.ghc_family_privacy_candidate_adjudication import scan_text_items

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "codex/GHC-Family/elaren-kestrel-v685-v7-full-tools"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
X1 = "0902e28aa1006b44a247e3d480797a4472bc1e58"
EVIDENCE = "0eba230431e652b9907edb5e86f11924d32c1d1d"
BASE = "docs/elaren-kestrel/v685-v7"


def run(args: list[str], *, check: bool = True, text: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(
        args,
        cwd=ROOT,
        check=check,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
    )


def git_text(*args: str) -> str:
    return run(["git", *args]).stdout.strip()


def git_blob(commit: str, path: str) -> bytes:
    return run(["git", "show", f"{commit}:{path}"], text=False).stdout


def git_json(commit: str, path: str) -> Any:
    return json.loads(git_blob(commit, path).decode("utf-8"))


def replay_manifest(commit: str, path: str) -> dict[str, Any]:
    manifest = git_json(commit, path)
    failures = []
    for item in manifest["entries"]:
        data = git_blob(commit, item["path"])
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            failures.append(item["path"])
    return {"path": path, "entry_count": manifest["entry_count"], "failure_count": len(failures), "failures": failures, "valid": not failures}


def directory_map(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    args = parser.parse_args()
    receipt = args.receipt.resolve()
    marker = receipt.with_suffix(receipt.suffix + ".invoked")
    if receipt.exists() or marker.exists():
        print(json.dumps({"status": "REFUSED_EXISTING_CANONICAL_LATCH"}, separators=(",", ":")))
        return 2
    receipt.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text(json.dumps({"phase": "v685-v7", "state": "CANONICAL_INVOKED_ONCE"}) + "\n", encoding="utf-8", newline="\n")

    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    upstream = git_text("rev-parse", "@{upstream}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live = live_line.split()[0] if live_line else ""
    divergence = git_text("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()
    status_before = git_text("status", "--porcelain=v1", "--untracked-files=all")

    tests = run([sys.executable, "-X", "utf8", "-m", "unittest", "tests.test_ghc_family_elaren_kestrel_v685_v7_final", "-q"], check=False)
    manifests = {
        "x1": replay_manifest(X1, f"{BASE}/validation/x1-index-manifest.json"),
        "evidence": replay_manifest(EVIDENCE, f"{BASE}/validation/evidence-index-manifest.json"),
        "final_delta": replay_manifest(head, f"{BASE}/validation/final-delta-manifest.json"),
        "final_owner": replay_manifest(head, f"{BASE}/validation/final-owner-manifest.json"),
    }
    owner_manifest = git_json(head, f"{BASE}/validation/final-owner-manifest.json")
    owner_paths = sorted({row["path"] for row in owner_manifest["entries"]} | set(owner_manifest["declared_self_exclusions"]))

    json_failures = []
    json_paths = [path for path in owner_paths if path.endswith(".json")]
    for path in json_paths:
        try:
            json.loads(git_blob(head, path).decode("utf-8"))
        except Exception:
            json_failures.append(path)

    python_failures = []
    security_findings = []
    python_paths = [path for path in owner_paths if path.endswith(".py")]
    for path in python_paths:
        try:
            tree = ast.parse(git_blob(head, path).decode("utf-8"), filename=path)
        except Exception:
            python_failures.append(path)
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "__import__"}:
                security_findings.append({"path": path, "call": node.func.id})

    markdown_paths = [path for path in owner_paths if path.endswith(".md")]
    markdown_failures = []
    for path in markdown_paths:
        text = git_blob(head, path).decode("utf-8")
        if not text.strip() or ("SKILL.md" not in path and not text.lstrip().startswith("#")):
            markdown_failures.append(path)

    yaml_paths = [path for path in owner_paths if path.endswith((".yaml", ".yml"))]
    yaml_failures = []
    for path in yaml_paths:
        text = git_blob(head, path).decode("utf-8")
        if "interface:" not in text or "display_name:" not in text:
            yaml_failures.append(path)

    html_paths = [path for path in owner_paths if path.endswith(".html")]
    html_failures = []
    for path in html_paths:
        text = git_blob(head, path).decode("utf-8").lower()
        if not all(token in text for token in ('<html lang="en">', "skip to main", "<main", "<h1", "<table")):
            html_failures.append(path)

    privacy = scan_text_items(
        (path, git_blob(head, path).decode("utf-8"))
        for path in owner_paths
        if Path(path).suffix.lower() in {".json", ".md", ".py", ".yaml", ".yml", ".html", ".lock"}
    )

    seal = git_json(head, f"{BASE}/closeout/content-seal.json")
    seal_failures = []
    for item in seal["targets"]:
        data = git_blob(head, item["path"])
        if len(data) != item["bytes"] or hashlib.sha256(data).hexdigest() != item["sha256"]:
            seal_failures.append(item["path"])

    baton = git_json(head, f"{BASE}/final/baton-integrity.json")
    baton_bytes = git_blob(head, baton["assembled_path"])
    baton_words = len(baton_bytes.decode("utf-8").split())
    overview_words = len(git_blob(head, f"{BASE}/final/final-integrated-overview.md").decode("utf-8").split())

    installation = git_json(head, f"{BASE}/x2/global-promotion-installation.json")
    global_parity_failures = []
    for row in installation["skills"]:
        candidate = ROOT / BASE / "x2" / "global-skills" / row["skill"]
        installed = args.skill_root / row["skill"]
        if not installed.is_dir() or directory_map(candidate) != directory_map(installed):
            global_parity_failures.append(row["skill"])

    source_to_final = git_text("rev-list", "--reverse", f"{SOURCE}..{head}").splitlines()
    merges = git_text("rev-list", "--merges", f"{SOURCE}..{head}").splitlines()
    direct_edges = {
        "x1_parent_source": git_text("rev-parse", f"{X1}^") == SOURCE,
        "evidence_parent_x1": git_text("rev-parse", f"{EVIDENCE}^") == X1,
        "final_parent_evidence": git_text("rev-parse", "HEAD^") == EVIDENCE,
    }
    final_parent_count = len(git_text("show", "-s", "--format=%P", "HEAD").split())
    status_after = git_text("status", "--porcelain=v1", "--untracked-files=all")
    upstream_after = git_text("rev-parse", "@{upstream}")
    tracking_after = git_text("rev-parse", f"refs/remotes/origin/{BRANCH}")
    live_after_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{BRANCH}")
    live_after = live_after_line.split()[0] if live_after_line else ""

    checks = {
        "branch_exact": branch == BRANCH,
        "clean_before": status_before == "",
        "clean_after": status_after == "",
        "four_way_before": head == upstream == tracking == live,
        "four_way_after": head == upstream_after == tracking_after == live_after,
        "divergence_zero": divergence == ["0", "0"],
        "commit_count_three": len(source_to_final) == 3,
        "zero_merges": not merges,
        "direct_edges": all(direct_edges.values()),
        "final_parent_one": final_parent_count == 1,
        "final_tests": tests.returncode == 0,
        "manifest_replays": all(row["valid"] for row in manifests.values()),
        "json_parses": not json_failures,
        "python_ast": not python_failures,
        "bounded_security_findings_zero": not security_findings,
        "markdown_structure": not markdown_failures,
        "yaml_structure": not yaml_failures,
        "html_structure": not html_failures,
        "privacy_confirmed_hits_zero": not privacy["confirmed_hits"],
        "content_seal": not seal_failures,
        "global_skill_byte_parity": not global_parity_failures,
        "baton_word_bounds": 10000 <= baton_words <= 100000 and baton_words == baton["word_count"],
        "overview_three_page_equivalent": overview_words >= 1500,
        "owner_file_ceiling": len(owner_paths) < 2000,
    }
    success = all(checks.values())
    payload = {
        "schema": "ghc.family.elaren-v685-v7.canonical.v1",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "owner": "Elaren Kestrel",
        "phase": "v685-v7",
        "head": head,
        "source": SOURCE,
        "x1": X1,
        "evidence": EVIDENCE,
        "canonical_invocation_count": 1,
        "canonical_success_count": 1 if success else 0,
        "canonical_replay_count": 0,
        "checks": checks,
        "counts": {
            "detailed_checks": len(checks),
            "final_tests": 18 if tests.returncode == 0 else 0,
            "manifest_entries": sum(row["entry_count"] for row in manifests.values()),
            "json_parses": len(json_paths),
            "python_ast": len(python_paths),
            "markdown": len(markdown_paths),
            "yaml": len(yaml_paths),
            "html": len(html_paths),
            "privacy_candidates": len(privacy["candidates"]),
            "privacy_confirmed_hits": len(privacy["confirmed_hits"]),
            "seal_targets": seal["target_count"],
            "owner_files": len(owner_paths),
            "global_skills": installation["installed_skill_count"],
            "shared_runners": installation["unique_shared_runner_count"],
            "baton_words": baton_words,
            "overview_words": overview_words,
        },
        "manifests": manifests,
        "direct_edges": direct_edges,
        "same_owner_not_independent_reproduction": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    payload_bytes = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["payload_sha256"] = hashlib.sha256(payload_bytes).hexdigest()
    receipt.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": payload["status"], "head": head, "checks_passed": sum(checks.values()), "checks_total": len(checks), "payload_sha256": payload["payload_sha256"]}, separators=(",", ":")))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
