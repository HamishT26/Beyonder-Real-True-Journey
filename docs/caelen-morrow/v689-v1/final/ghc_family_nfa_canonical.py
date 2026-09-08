"""One-shot exact-final owner-scoped canonical validator for Caelen Morrow v689-v1."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

SOURCE = "9968e60dab5393ed2629ed978c8d1128bb63a0b9"
X1 = "3635cfeeb48b27540452eabf104a5ad3f491b82c"
X2 = "a53b2ffc7020ad8d485878392793de7bd2722a7c"
REL = "docs/caelen-morrow/v689-v1"
BRANCH = "codex/GHC-Family/caelen-morrow-v689-v1-full-tools"
SOURCE_RECEIPT_SHA256 = "ca184b1bc09adc84f9c82fc545d34dd19ba8d1ac64a217b5f30a82436b21b5c1"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict(data: bytes):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("duplicate JSON key")
            result[key] = value
        return result

    return json.loads(data, object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(payload, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


class Seal:
    def __init__(self, args):
        self.args = args
        self.repo = args.repo.resolve()
        self.checks: dict[str, bool] = {}
        self.manifests: list[dict] = []

    def git(self, *args: str, input_bytes: bytes | None = None) -> bytes:
        return subprocess.check_output(["git", "-C", str(self.repo), *args], input=input_bytes, timeout=180)

    def check(self, name: str, value) -> None:
        self.checks[name] = bool(value)
        if not value:
            raise ValueError(name)

    def batch(self, revision: str, paths: list[str]) -> dict[str, bytes]:
        data = self.git("cat-file", "--batch", input_bytes="".join(f"{revision}:{path}\n" for path in paths).encode("utf-8"))
        result = {}
        position = 0
        for path in paths:
            end = data.index(b"\n", position)
            header = data[position:end].split()
            if len(header) != 3 or header[1] != b"blob":
                raise ValueError("missing or nonblob owner dependency")
            size = int(header[2])
            result[path] = data[end + 1 : end + 1 + size]
            position = end + size + 2
        self.check("complete_batch_framing_" + str(len(self.checks)), position == len(data))
        return result

    def equality(self):
        local = self.git("rev-parse", "HEAD").decode().strip()
        upstream = self.git("rev-parse", "@{upstream}").decode().strip()
        tracking = self.git("rev-parse", "refs/remotes/origin/" + BRANCH).decode().strip()
        lines = self.git("ls-remote", "origin", "refs/heads/" + BRANCH).decode().splitlines()
        live = lines[0].split()[0] if len(lines) == 1 else None
        divergence = [int(value) for value in self.git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").decode().split()]
        clean = not self.git("status", "--porcelain=v1", "--untracked-files=all").strip()
        return {
            "local": local,
            "upstream": upstream,
            "tracking": tracking,
            "fresh_live": live,
            "divergence": divergence,
            "clean": clean,
            "all_equal": local == upstream == tracking == live == self.args.head,
        }

    def manifest(self, revision: str, path: str) -> list[str]:
        manifest = strict(self.git("show", f"{revision}:{path}"))
        paths = [row["path"] for row in manifest["entries"]]
        label = path.split("/")[-2]
        self.check("unique_manifest_paths_" + label, len(paths) == len(set(paths)))
        blobs = self.batch(revision, paths)
        self.check("manifest_fixity_" + label, all(len(blobs[row["path"]]) == row["bytes"] and sha(blobs[row["path"]]) == row["sha256"] for row in manifest["entries"]))
        self.manifests.append({"path": path, "revision": revision, "entries": len(paths), "valid": True})
        return sorted(set(paths + manifest["self_exclusions"]))

    def static(self):
        self.check("branch_exact", self.git("branch", "--show-current").decode().strip() == BRANCH)
        before = self.equality()
        self.check("fresh_four_way_equal", before["all_equal"])
        self.check("clean", before["clean"])
        self.check("zero_divergence", before["divergence"] == [0, 0])
        self.check("exact_direct_parent_chain", self.git("show", "-s", "--format=%P", X1).decode().strip() == SOURCE and self.git("show", "-s", "--format=%P", X2).decode().strip() == X1 and self.git("show", "-s", "--format=%P", self.args.head).decode().strip() == X2)
        self.check("three_phase_commits", self.git("rev-list", "--count", SOURCE + ".." + self.args.head).decode().strip() == "3")
        self.check("zero_merges", self.git("rev-list", "--count", "--merges", SOURCE + ".." + self.args.head).decode().strip() == "0")
        changes = [line.split("\t") for line in self.git("diff", "--name-status", SOURCE, self.args.head).decode().splitlines()]
        paths = [row[1] for row in changes]
        self.check("additive_owner_scope", all(row[0] == "A" and row[1].startswith(REL + "/") and ".." not in PurePosixPath(row[1]).parts for row in changes))
        self.check("owner_file_ceiling", 0 < len(paths) <= 2000)
        blobs = self.batch(self.args.head, paths)
        parsed = 0
        python_files = 0
        privacy = []
        security = []
        patterns = [
            ("private_absolute_path", re.compile(r"(?i)\b(?:C|D)" + r":[\\/]")),
            ("raw_uuid", re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I)),
            ("credential_or_token", re.compile("(?i)(?:sk-" + r"[A-Za-z0-9]{20,}|(?:api[_-]?key|access[_-]?token|password|secret)\s*[:=]\s*[\"'][^\"']+[\"'])")),
            ("private_key", re.compile("BEGIN " + r"(?:RSA |EC )?PRIVATE KEY")),
            ("private_route_markup", re.compile("(?i)<" + r"(?:codex_delegation|source_thread_id)>|(?:app|plugin)" + r"://")),
        ]
        maximum = {"path": None, "words": 0}
        for path, data in blobs.items():
            text = data.decode("utf-8")
            words = len(text.split())
            if words > maximum["words"]:
                maximum = {"path": path, "words": words}
            if path.endswith(".json"):
                strict(data)
                parsed += 1
            if path.endswith(".py"):
                tree = ast.parse(text)
                python_files += 1
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                        security.append({"path": path, "kind": node.func.id})
                    if isinstance(node, ast.Call) and any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                        security.append({"path": path, "kind": "shell_true"})
            for label, pattern in patterns:
                for match in pattern.finditer(text):
                    privacy.append({"path": path, "class": label, "line": text.count("\n", 0, match.start()) + 1})
        self.check("document_ceiling", maximum["words"] <= 100000)
        self.check("five_class_privacy_raw_identifier_scan", not privacy)
        self.check("bounded_ast_security", not security)
        scopes = {
            "x1": self.manifest(X1, REL + "/x1/manifest.json"),
            "x2": self.manifest(X2, REL + "/x2/manifest.json"),
            "final": self.manifest(self.args.head, REL + "/final/manifest.json"),
        }
        owner = strict(blobs[REL + "/final/owner-manifest.json"])
        self.check("owner_manifest_complete", set(paths) == {row["path"] for row in owner["entries"]} | set(owner["self_exclusions"]))
        self.check("owner_manifest_fixity", all(len(blobs[row["path"]]) == row["bytes"] and sha(blobs[row["path"]]) == row["sha256"] for row in owner["entries"]))
        seal = strict(blobs[REL + "/final/content-seal.json"])
        self.check("content_seal_owner_manifest", seal["owner_manifest_sha256"] == sha(blobs[REL + "/final/owner-manifest.json"]))
        self.check("content_seal_stage_manifests", seal["stage_manifest_sha256"] == {stage: sha(blobs[REL + f"/{stage}/manifest.json"]) for stage in ["x1", "x2", "final"]})
        self.check("stage_scope_complete", set(scopes["x1"]) | set(scopes["x2"]) | set(scopes["final"]) == set(paths))

        def read(name: str):
            return strict(blobs[REL + "/" + name])

        truth = read("final/phase-truth.json")
        self.check("outcomes", truth["outcomes"] == {"completed": 170, "represented": 17, "open_gap": 3, "exact_gate": 10})
        self.check("effective_counts", truth["effective_counts"] == {"proposals": 17230, "negatives": 86292, "methods": 94237, "failed_witnesses": 57265, "passing_witnesses": 86430, "open_gaps": 771, "exact_gates": 805})
        self.check("phase_method_counts", truth["phase_methods"] == 57 and truth["phase_witnesses"] == 604 and truth["phase_unique_negatives"] == 482 and truth["effective_phase_methods"] == 61 and truth["effective_phase_failed_witnesses"] == 486 and truth["effective_phase_passing_witnesses"] == 126)
        self.check("not_ready_for_stage20", truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20")
        route = read("final/terminal-route.json")
        self.check("prepared_not_sent", route["state"] == "PREPARED_NOT_SENT" and route["send_count"] == 0 and route["creation_count"] == 0 and truth["successor_contacts"] == 0)
        self.check("portfolio_complete", read("x2/portfolio-results.json")["predicate_passes"] == 850 and all(row["predicate_pass"] is True for row in read("x2/portfolio-results.json")["records"] if row["action_executed"]))
        self.check("exact_and_blocked_unexecuted", all(not row["action_executed"] for row in read("x2/portfolio-results.json")["records"] if row["group"] in {"exact_packets", "blocked_packets"}))
        self.check("contracts_complete", read("x2/contract-summary.json") == {"contracts": 200, "passed": 200, "failed": 0, "failure_ids": []})
        method_validation = read("x2/method-flow-validation.json")
        self.check("method_validation", method_validation["valid"] and method_validation["method_count"] == 57 and method_validation["witness_count"] == 604)
        self.check("retained_negatives", read("final/retained-negative-register.json")["phase_negative_count"] == 486 and read("final/retained-negative-register.json")["erased_negative_count"] == 0)
        self.check("gates_retained", read("final/open-exact-gate-register.json")["effective_open_gaps"] == 771 and read("final/open-exact-gate-register.json")["effective_exact_gates"] == 805)
        deck = read("x2/deck/card-manifest.json")
        self.check("deck_manifest_fixity", all(len(blobs[row["path"]]) == row["bytes"] and sha(blobs[row["path"]]) == row["sha256"] for row in deck["entries"]))
        self.check("deck_card_count", read("x2/deck/deck-index.json")["card_count"] == 265)
        transaction = read("x2/package-transaction.json")
        self.check("package_artifacts", all((self.args.package_bank / "artifacts" / row["filename"]).stat().st_size == row["bytes"] and sha((self.args.package_bank / "artifacts" / row["filename"]).read_bytes()) == row["sha256"] for row in transaction["verified_artifacts"]))
        package_smokes = read("x2/package-smoke-summary.json")
        self.check("package_smokes", package_smokes["comparison_count"] == package_smokes["comparison_passes"] == 420 and package_smokes["adverse_count"] == package_smokes["adverse_rejections"] == 3)
        self.check("advisory_snapshot", len(transaction["osv_results"]["results"]) == 8 and transaction["listed_vulnerability_count"] == 0 and not transaction["exhaustive_security"])
        promotion = read("x2/tool-promotion.json")
        self.check("tool_smokes", len(promotion["smokes"]) == 190 and all(row["predicate_pass"] for row in promotion["smokes"]))
        for row in promotion["parity"]:
            if row["tool"].startswith("ghc-family-"):
                target = self.args.skill_root / row["tool"] / row["relative_path"]
                source = REL + "/x2/skills/" + row["tool"] + "/" + row["relative_path"]
            elif row["tool"] == "shared_core":
                target = self.args.runner_root / row["relative_path"]
                source = REL + "/x2/code/ghc_family_nfa_core.py"
            else:
                target = self.args.runner_root / row["relative_path"]
                source = REL + "/x2/code/" + row["relative_path"]
            target_bytes = target.read_bytes()
            self.check("promotion_raw_and_git_parity_" + str(len(self.checks)), len(target_bytes) == row["bytes"] and sha(target_bytes) == row["sha256"] and target_bytes.replace(b"\r\n", b"\n") == blobs[source])
        self.check("source_receipt_fixity", sha(self.args.source_receipt.read_bytes()) == SOURCE_RECEIPT_SHA256)
        baton = blobs[REL + "/handoffs/future-self-chosen-sibling-15-v689-v2-activation-baton.md"].decode("utf-8")
        self.check("baton_budget_and_eof", 10000 <= len(baton.split()) <= 100000 and len(re.findall(r"^## Module ", baton, re.M)) == 13 and baton.rstrip().endswith("EOF CAELEN MORROW v689-v1 BATON."))
        self.check("baton_hash", read("final/baton-index.json")["sha256"] == sha(baton.encode("utf-8")))
        policy = read("final/canonical-policy.json")
        self.check("canonical_policy", policy["source"] == SOURCE and policy["x1"] == X1 and policy["x2"] == X2 and len(policy["test_modules"]) == 4 and policy["expected_total_tests"] == sum(row["expected_tests"] for row in policy["test_modules"]) == 52)
        self.check("full_repository_suite_not_run", policy["full_repository_suite"] is False)
        return {
            "before": before,
            "paths": paths,
            "blobs": blobs,
            "scopes": scopes,
            "policy": policy,
            "scan": {"strict_json": parsed, "python_ast": python_files, "maximum_document": maximum, "confirmed_privacy_hits": len(privacy), "privacy_classes": [label for label, _ in patterns], "bounded_security_findings": security},
        }

    def run_tests(self, static, output: Path):
        results = []
        definitions = {"x1": X1, "x2": X2, "final": self.args.head}
        materialized: dict[str, int] = {}
        for row in static["policy"]["test_modules"]:
            stage = row["stage"]
            root = output / "definitions" / stage
            if stage not in materialized:
                if stage == "x1":
                    paths = static["scopes"]["x1"]
                elif stage == "x2":
                    paths = sorted(set(static["scopes"]["x1"] + static["scopes"]["x2"]))
                else:
                    paths = static["paths"]
                blobs = self.batch(definitions[stage], paths)
                root.mkdir(parents=True, exist_ok=False)
                for path, data in blobs.items():
                    target = root / path
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with target.open("xb") as handle:
                        handle.write(data)
                materialized[stage] = len(paths)
            env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
            completed = subprocess.run([sys.executable, "-X", "utf8", str(root / row["path"])], cwd=root, env=env, capture_output=True, text=True, timeout=120)
            output_name = row["label"] + "-tests"
            (output / (output_name + ".stdout.txt")).write_text(completed.stdout, encoding="utf-8", newline="\n")
            (output / (output_name + ".stderr.txt")).write_text(completed.stderr, encoding="utf-8", newline="\n")
            match = re.search(r"Ran (\d+) tests?", completed.stdout + completed.stderr)
            count = int(match.group(1)) if match else 0
            results.append({"stage": stage, "module": row["path"], "definition": definitions[stage], "definition_sha256": sha((root / row["path"]).read_bytes()), "materialized_files": materialized[stage], "tests": count, "expected_tests": row["expected_tests"], "returncode": completed.returncode, "passed": completed.returncode == 0 and count == row["expected_tests"]})
        self.checks["all_lifecycle_tests"] = len(results) == len(static["policy"]["test_modules"]) and all(row["passed"] for row in results)
        return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ["repo", "package-bank", "source-receipt", "skill-root", "runner-root", "receipt-root"]:
        parser.add_argument("--" + name, type=Path, required=True)
    parser.add_argument("--head", required=True)
    parser.add_argument("--mode", choices=["preflight", "canonical"], required=True)
    args = parser.parse_args()
    if not re.fullmatch(r"[a-f0-9]{40}", args.head):
        raise ValueError("exact full head required")
    output = args.receipt_root / ("canonical-" + args.head[:12])
    marker = output / "invocation.json"
    receipt = output / "exact-final-owner-scoped-canonical.json"
    if marker.exists() or receipt.exists():
        raise ValueError("canonical replay refused")
    if args.mode == "preflight":
        seal = Seal(args)
        static = seal.static()
        write(output / "preflight.json", {"schema": "ghc.family.nfa.canonical-preflight.v1", "head": args.head, "checks": seal.checks, "valid": all(seal.checks.values()), "owner_files": len(static["paths"]), "test_modules_planned": static["policy"]["test_modules"], "canonical_invocations": 0})
        print(json.dumps({"mode": "preflight", "valid": True, "checks": len(seal.checks), "owner_files": len(static["paths"])}))
        return 0
    preflight = strict((output / "preflight.json").read_bytes())
    if preflight["head"] != args.head or not preflight["valid"]:
        raise ValueError("exact valid preflight required")
    write(marker, {"head": args.head, "invocation_count": 1, "success_count": 0, "replay_count": 0})
    seal = Seal(args)
    tests = []
    error = None
    before = None
    after = None
    scan = None
    try:
        static = seal.static()
        before = static["before"]
        scan = static["scan"]
        tests = seal.run_tests(static, output)
        seal.check("all_lifecycle_tests", all(row["passed"] for row in tests) and sum(row["tests"] for row in tests) == 52)
        after = seal.equality()
        seal.check("fresh_four_way_equal_after", after["all_equal"])
        seal.check("clean_after", after["clean"])
        success = all(seal.checks.values())
    except Exception as exception:
        success = False
        error = type(exception).__name__ + ": " + str(exception)
    payload = {
        "schema": "ghc.family.nfa.exact-final-owner-scoped-canonical.v1",
        "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if success else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL_RETAINED_ZERO_CREDIT",
        "head": args.head,
        "source": SOURCE,
        "x1": X1,
        "x2": X2,
        "branch": BRANCH,
        "invocation_count": 1,
        "success_count": 1 if success else 0,
        "replay_count": 0,
        "checks": seal.checks,
        "check_count": len(seal.checks),
        "tests": tests,
        "total_tests": sum(row.get("tests", 0) for row in tests),
        "expected_tests": 52,
        "manifests": seal.manifests,
        "scan": scan,
        "before": before,
        "after": after,
        "error": error,
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
        "exhaustive_security": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write(receipt, payload)
    marker.write_text(json.dumps({"head": args.head, "invocation_count": 1, "success_count": 1 if success else 0, "replay_count": 0}, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"status": payload["status"], "checks": len(seal.checks), "tests": payload["total_tests"], "receipt": receipt.name}))
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
