"""Invoke one exact-final Neris v689-v6 canonical without replaying passed components."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess  # nosec B404 - fixed git executable and literal owner-generated arguments only
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath

SOURCE = "ffdff93a34f607f5d4a7c497f0056afcc82cdbf2"
PLANNING = "a30a336b8dd0442a8ca7fef00772161d10392151"
X1 = "8e0d069dcb41d4dcd66342655949c90b0e21e9f9"
X2 = "2e565f3a81c6bd389d342a34ac6284b411adca9c"
BRANCH = "codex/GHC-Family/neris-solane-main"
PREFIX = "docs/neris-solane/v689-v6/"
SCRIPT_NAMES = {
    "ghc_family_mesh_x1.py", "ghc_family_mesh_x2.py", "ghc_family_mesh_cli.py",
    "ghc_family_grid_geometry.py", "ghc_family_interpolation_forward_difference.py",
    "ghc_family_backward_central_difference.py", "ghc_family_curvature_quadrature.py",
    "ghc_family_grid_error_refinement_order.py", "ghc_family_poisson_solution_residual.py",
    "ghc_family_flux_richardson.py", "ghc_family_adaptive_cfl.py", "ghc_family_heat_energy.py",
    "ghc_family_mesh_provenance_claim.py",
}
TEST_NAMES = {"test_ghc_family_mesh_x1.py", "test_ghc_family_mesh_x2.py"}
OUTCOMES = {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5}


def require(condition: bool, code: str) -> None:
    if not condition:
        raise ValueError(code)


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def unique_pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, "E_DUPLICATE_JSON_KEY")
        result[key] = value
    return result


def strict_json(raw: bytes):
    return json.loads(raw, object_pairs_hook=unique_pairs, parse_constant=lambda _: (_ for _ in ()).throw(ValueError("E_NONFINITE_JSON")))


def git(repo: Path, *args: str) -> bytes:
    executable = shutil.which("git")
    require(executable is not None, "E_GIT_UNAVAILABLE")
    result = subprocess.run([executable, "-C", str(repo), *args], capture_output=True, timeout=180, check=False)  # nosec B603
    require(result.returncode == 0, "E_GIT_" + args[0])
    return result.stdout


def check_paths(paths: list[str]) -> int:
    require(paths and len(paths) == len(set(paths)), "E_PATH_SET")
    for value in paths:
        path = PurePosixPath(value)
        require(not path.is_absolute() and ".." not in path.parts and "\\" not in value, "E_PATH_ESCAPE")
        allowed = value.startswith(PREFIX)
        allowed |= len(path.parts) == 2 and path.parts[0] == "scripts" and path.name in SCRIPT_NAMES
        allowed |= len(path.parts) == 2 and path.parts[0] == "tests" and path.name in TEST_NAMES
        require(allowed and "__pycache__" not in path.parts and path.suffix != ".pyc", "E_OWNER_SCOPE")
    return len(paths)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--expected-final", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    final = args.expected_final
    require(re.fullmatch(r"[0-9a-f]{40}", final) is not None, "E_FINAL_HASH")
    bank = repo.parents[1] / "phase-banks" / "neris-solane-v689-v6" / "canonical"
    require(args.output.resolve() == (bank / "exact-final.json").resolve(), "E_CANONICAL_OUTPUT_SCOPE")
    bank.mkdir(parents=True, exist_ok=True)
    started = datetime.now(UTC).isoformat()
    latch = {"owner": "Neris Solane", "phase": "v689-v6", "expected_final": final, "started_at_utc": started, "invocations": 1, "replay_permitted": False}
    with (bank / "invocation-latch.json").open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(latch, stream, indent=2)
        stream.write("\n")
    checks = []
    raw_cache: dict[str, bytes] = {}

    def record(name: str, details: object) -> None:
        checks.append({"name": name, "passed": True, "details": details})
        print(json.dumps({"check": name, "passed": True}), flush=True)

    def raw(relative: str) -> bytes:
        if relative not in raw_cache:
            path = (repo / relative).resolve()
            require(path.is_relative_to(repo), "E_PATH_ESCAPE")
            raw_cache[relative] = path.read_bytes()
        return raw_cache[relative]

    def read(relative: str):
        return strict_json(raw(relative))

    try:
        head = git(repo, "rev-parse", "HEAD").decode().strip()
        upstream = git(repo, "rev-parse", "@{u}").decode().strip()
        tracking = git(repo, "rev-parse", "refs/remotes/origin/" + BRANCH).decode().strip()
        branch = git(repo, "branch", "--show-current").decode().strip()
        live_rows = git(repo, "ls-remote", "origin", "refs/heads/" + BRANCH).decode().splitlines()
        require(len(live_rows) == 1, "E_LIVE_REFERENCE")
        live = live_rows[0].split()[0]
        divergence = list(map(int, git(repo, "rev-list", "--left-right", "--count", "HEAD...@{u}").decode().split()))
        require(head == upstream == tracking == live == final and branch == BRANCH, "E_FINAL_EQUALITY")
        require(divergence == [0, 0] and not git(repo, "status", "--porcelain=v1").strip(), "E_CLEAN_STATE")
        record("exact_final_git_state", {"head": head, "upstream": upstream, "tracking": tracking, "fresh_live": live, "divergence": divergence, "clean": True})

        ancestry = [line.split() for line in git(repo, "rev-list", "--parents", SOURCE + ".." + final).decode().splitlines()]
        require(ancestry == [[final, X2], [X2, X1], [X1, PLANNING], [PLANNING, SOURCE]], "E_OWNER_ANCESTRY")
        record("direct_owner_lifecycle", {"owner_commits": 4, "merges": 0, "source": SOURCE})

        delta = git(repo, "diff", "--name-status", SOURCE, final).decode().splitlines()
        require(all(line.startswith("A\t") for line in delta), "E_NONADDITIVE_DELTA")
        paths = [line.split("\t", 1)[1] for line in delta]
        record("owner_delta_scope", {"paths": check_paths(paths), "all_additive": True, "sibling_mutations": 0})
        tracked = len(git(repo, "ls-files", "-z").split(b"\0")) - 1
        materialized = 0
        for folder, directories, files in os.walk(repo):
            directories[:] = [name for name in directories if name != ".git"]
            materialized += len(files)
        require(tracked < 2000 and materialized < 2000, "E_FILE_CAPACITY")
        record("owner_file_capacity", {"tracked": tracked, "materialized": materialized, "ceiling": 2000, "sparse_before_checkout": True})

        seal_path = PREFIX + "final/content-seal.json"
        seal = read(seal_path)
        require(set(paths) == set(seal["entries"]) | {seal_path}, "E_SEAL_SCOPE")
        tree = {}
        for entry in git(repo, "ls-tree", "-r", "-z", final).split(b"\0"):
            if entry:
                metadata, name = entry.split(b"\t", 1)
                tree[name.decode()] = metadata.decode().split()[2]
        for path, item in seal["entries"].items():
            value = raw(path)
            require(len(value) == item["bytes"] and sha(value) == item["sha256"], "E_FILE_FIXITY")
            # Git object identity is SHA-1 by repository format; this is not a security digest.
            oid = hashlib.sha1(("blob " + str(len(value)) + "\0").encode() + value, usedforsecurity=False).hexdigest()
            require(tree.get(path) == oid == item["git_blob_sha1"], "E_GIT_BYTE_DOMAIN")
        record("exact_owner_content_seal", {"entries": len(seal["entries"]), "self_exclusion": seal_path, "checkout_git_blob_parity": True})

        definitions = read(PREFIX + "plan/new-proposals.json")["proposals"]
        inherited = read(PREFIX + "plan/inherited-selections.json")["selections"]
        require(len(definitions) == len({item["proposal_id"] for item in definitions}) == 200, "E_PROPOSAL_COUNT")
        require(len({digest(item["request"]) for item in definitions}) == 200, "E_REQUEST_UNIQUENESS")
        require(all(digest(item["expected"]) == item["expected_sha256"] and item["outcomes_observed"] is False for item in definitions), "E_FROZEN_ORACLES")
        require(len(inherited) == 200 and all(item["new_execution_credit"] == item["new_novelty_credit"] == 0 for item in inherited), "E_INHERITED_CREDIT")
        record("frozen_proposal_definitions", {"new": 200, "inherited": 200, "universal_novelty_claimed": False})
        by_id = {item["proposal_id"]: item for item in definitions}

        admitted = []
        for session, filename in (("x1", "results-effective.json"), ("x2", "results.json")):
            result = read(PREFIX + session + "/" + filename)
            require(len(result["safe"]) == len(result["candidate"]) == 100, "E_PORTFOLIO_COUNT")
            for row in result["safe"]:
                proposal = by_id[row["proposal_id"]]
                require(row["passed"] is True and row["input_unchanged"] is True, "E_SAFE_PASS")
                require(row["request_sha256"] == digest(proposal["request"]), "E_REQUEST_BINDING")
                require(row["expected_sha256"] == proposal["expected_sha256"] == digest(proposal["expected"]), "E_ORACLE_BINDING")
                require(digest(row["observed"]) == proposal["expected_sha256"] and row["outcome"] == proposal["expected_disposition"], "E_OBSERVED_BINDING")
                admitted.append(row)
            for row in result["candidate"]:
                proposal = by_id[row["proposal_id"]]
                require(row["passed"] is True and row["input_unchanged"] is True and row["subject_success_credit"] == 0, "E_CANDIDATE_CREDIT")
                require(digest(row["observed"]) == digest(proposal["candidate_expected"]) and row["request_sha256"] == digest(proposal["candidate_request"]), "E_CANDIDATE_BINDING")
        original = read(PREFIX + "x1/results.json")
        recovery = read(PREFIX + "x1/portfolio-recovery.json")
        require(original["safe_passed"] == 90 and recovery["reexecuted_safe_cases"] == recovery["recovered_passed"] == 10 and recovery["replayed_passing_safe_cases"] == 0, "E_X1_RECOVERY")
        require(Counter(row["outcome"] for row in admitted) == Counter(OUTCOMES), "E_CORE_OUTCOMES")
        record("portfolio_receipt_bindings", {"safe": 200, "candidate_refusal_predicates": 200, "candidate_subject_successes": 0, "outcomes": OUTCOMES, "passing_cases_replayed_in_recovery": 0})

        selected = {item["selection_id"]: item for item in inherited}
        for session in ("x1", "x2"):
            projection = read(PREFIX + session + "/source-projections.json")["projections"]
            cleanup = read(PREFIX + session + "/cleanup-receipt.json")
            require(len(projection) == len(cleanup["rows"]) == cleanup["passed"] == 100, "E_CLEANUP_COUNT")
            for row in projection:
                require(digest(dict(zip(row["keys"], row["values"]))) == selected[row["selection_id"]]["source_record_sha256"], "E_PROJECTION_BINDING")
            require(all(row["passed"] is True and row["source_execution_credit"] == 0 and row["host_cleanup_claimed"] is False for row in cleanup["rows"]), "E_CLEANUP_CREDIT")
        record("source_record_projection_bindings", {"refinements": 200, "source_execution_credit": 0, "host_cleanup_claimed": False})

        test_counts = {}
        for session, expected in (("x1", 20), ("x2", 21)):
            receipt = read(PREFIX + session + "/test-receipt.json")
            require(receipt["returncode"] == 0 and receipt["test_count"] == expected, "E_TEST_RECEIPT")
            test_counts[session] = expected
        record("invariant_test_receipt_bindings", {**test_counts, "tests_reexecuted_by_canonical": 0, "independent_reproduction": False})

        for session in ("x1", "x2"):
            validations = read(PREFIX + session + "/skill-validation.json")["skills"]
            smokes = read(PREFIX + session + "/runner-smokes.json")["smokes"]
            require(len(validations) == 10 and all(item["passed"] and item["example_safe_passed"] for item in validations), "E_SKILL_VALIDATION")
            require(len(smokes) == 20 and all(item["passed"] for item in smokes), "E_RUNNER_SMOKES")
        catalogue = read(PREFIX + "final/meta-tool-catalogue.json")["cards"]
        require(len(catalogue) == 33 and sum(item["kind"] == "skill" for item in catalogue) == 20, "E_CATALOGUE")
        require(all(sha(raw(item["source_path"])) == item["sha256"] for item in catalogue), "E_CATALOGUE_FIXITY")
        record("skills_runners_and_catalogue", {"skills": 20, "paired_runners": 10, "shared_modules": 3, "runner_smokes": 40, "global_promotions": 0})

        package_plan = read(PREFIX + "plan/package-plan.json")
        installation = read(PREFIX + "x1/package-install-receipt.json")
        smokes = read(PREFIX + "x1/package-smoke-receipt.json")
        comparisons = read(PREFIX + "x2/package-comparisons.json")
        require(len(package_plan["closure"]) == installation["closure_distributions"] == 11 and package_plan["direct_additions"] == installation["direct_additions"] == 3, "E_PACKAGE_COUNTS")
        require(len(smokes["positive"]) == len(smokes["adverse"]) == 3 and all(item.get("passed", item.get("rejected")) for item in smokes["positive"] + smokes["adverse"]), "E_PACKAGE_SMOKES")
        require(comparisons["total_comparisons"] == 30 and all(comparisons[name]["passed"] == 10 for name in ("findiff", "numdifftools", "meshio")), "E_PACKAGE_COMPARISONS")
        require(package_plan["known_advisories_at_review"] == installation["known_advisories_at_plan_review"] == 0, "E_PACKAGE_ADVISORY_REVIEW")
        record("package_receipt_bindings", {"direct_additions": 3, "closure_distributions": 11, "positive_smokes": 3, "adverse_smokes": 3, "comparisons": 30, "known_advisories_at_review": 0})

        interpretation = read(PREFIX + "x2/interpretation-study.json")
        require(len(interpretation["observations"]) == 5 and interpretation["observations"][0]["observed"]["energy_after"] == "10", "E_INTERPRETATION")
        require("No new fundamental law validated" in interpretation["candidate_thermo_psyche_law_status"], "E_LAW_BOUNDARY")
        record("interpretation_and_claim_boundaries", {"cases": 5, "new_fundamental_law_validated": False, "physical_measurements": 0})

        ledger = read(PREFIX + "final/method-flow-final.json")
        methods = {item["method_id"]: item for item in ledger["methods"]}
        witnesses = {item["witness_id"]: item for item in ledger["witnesses"]}
        require(len(methods) == len(ledger["methods"]) and len(witnesses) == len(ledger["witnesses"]), "E_LEDGER_UNIQUENESS")
        require(all(item["method_id"] in methods and item["same_owner_only"] is True and item["independent_reproduction"] is False for item in witnesses.values()), "E_WITNESS_SCOPE")
        require(ledger["counts"]["methods"] == len(methods) and ledger["counts"]["witnesses"] == len(witnesses), "E_LEDGER_COUNT")
        require(ledger["counts"]["failed_witnesses"] == sum(item["result"] == "fail" for item in witnesses.values()) and ledger["counts"]["passing_witnesses"] == sum(item["result"] == "pass" for item in witnesses.values()), "E_WITNESS_COUNT")
        render_recovery = read(PREFIX + "final/closeout-render-recovery.json")
        require(len(render_recovery["retained_failures"]) == 2 and render_recovery["text_or_deck_artifacts_replayed"] is False, "E_RENDER_RECOVERY")
        record("method_flow_bindings", {**ledger["counts"], "render_recovery_failures": 2})

        deck_index = read(PREFIX + "deck/deck-index.json")
        cards = [read(PREFIX + "deck/cards/" + identifier + ".json") for identifier in deck_index["card_ids"]]
        by_card = {item["card_id"]: item for item in cards}
        require(len(cards) == len(by_card) == 288 and Counter(item["tier"] for item in cards) == {1: 1, 2: 3, 3: 4, 4: 280}, "E_CARD_COUNT")
        for card in cards:
            value = dict(card)
            identifier = value.pop("card_id")
            require(identifier == "ghc-card-" + digest(value)[:24] and card["outcome"] in OUTCOMES, "E_CARD_DIGEST")
            if card["tier"] == 1:
                require(card["parent_ids"] == [], "E_ROOT_PARENT")
            else:
                require(len(card["parent_ids"]) == 1 and card["parent_ids"][0] in by_card and by_card[card["parent_ids"][0]]["tier"] == card["tier"] - 1, "E_CARD_PARENT")
        record("four_tier_deck", {"cards": 288, "roots": 1, "cycles": 0})
        deck_manifest = read(PREFIX + "deck/card-manifest.json")
        for name, item in deck_manifest["entries"].items():
            value = raw(PREFIX + "deck/" + name)
            require(sha(value) == item["sha256"] and len(value) == item["bytes"], "E_DECK_MANIFEST")
        record("deck_manifest", {"entries": len(deck_manifest["entries"]), "stable_cards": 8, "volatile_cards": 280})

        baton = raw(PREFIX + "final/hand-off-baton.md")
        index = read(PREFIX + "final/baton-module-index.json")
        require(10_000 <= len(baton.decode().split()) <= 100_000 and len(index["modules"]) == 13, "E_BATON_SIZE")
        require(sha(baton) == index["baton_sha256"] and baton.decode().rstrip().endswith("EOF NERIS SOLANE v689-v6 BATON."), "E_BATON_BINDING")
        require(all(sha(raw(item["path"])) == item["sha256"] for item in index["modules"]), "E_MODULE_FIXITY")
        record("modular_handoff", {"words": len(baton.decode().split()), "modules": 13, "eof_present": True})
        qa = read(PREFIX + "final/overview-qa.json")
        require(qa["pages"] == 3 and qa["visual_inspection"] == "passed_all_three_rendered_pages" and all(length > 300 for length in qa["page_text_lengths"]), "E_OVERVIEW_REVIEW")
        require(sha(raw(PREFIX + "final/overview.pdf")) == qa["pdf_sha256"], "E_PDF_BINDING")
        record("rendered_overview", {"pages": 3, "visual_inspection": qa["visual_inspection"], "manual_accessibility_reserved": True})

        exact = read(PREFIX + "final/exact-packet-state.json")
        blocked = read(PREFIX + "plan/blocked-packets.json")["packets"]
        route = read(PREFIX + "final/terminal-route-candidate.json")
        require(len(exact["packets"]) == 50 and exact["completed_at_repository_seal"] == 45 and exact["remaining"] == 5, "E_EXACT_PACKET_STATE")
        require(len(blocked) == 30 and all(item["executed"] is False for item in blocked), "E_BLOCKED_EXECUTION")
        require(route["state"] == "PREPARED_NOT_SENT" and route["successor_exact_title"] == "Vesper Arlen" and route["successor_phase"] == "v689-v7" and route["native_messages_sent"] == 0, "E_ROUTE_CANDIDATE")
        record("approval_and_route_state", {"exact_packets": 50, "precommit_completed": 45, "blocked_unexecuted": 30, "route": "PREPARED_NOT_SENT"})

        for session in ("plan", "x1", "x2"):
            manifest = read(PREFIX + session + "/manifest.json")
            for name, expected in manifest["entries"].items():
                path = PREFIX + name if not name.startswith(("scripts/", "tests/")) else name
                require(sha(raw(path)) == expected, "E_FROZEN_SESSION_BYTES")
        record("frozen_lifecycle_manifests", {"planning": PLANNING, "x1": X1, "x2": X2, "source_replays": 0})

        patterns = {
            "private_task_identifier": r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            "private_user_path": r"C:[/\\]Users[/\\]",
            "private_protocol": r"(?:codex|app|plugin)://",
            "credential_assignment": r"(?i)(?:api_key|access_token|password)\s*[:=]\s*[\"'][^\"']{12,}[\"']",
        }
        candidates = []
        for path in paths:
            if Path(path).suffix.lower() in {".pdf", ".png"}:
                continue
            text = raw(path).decode("utf-8")
            for name, pattern in patterns.items():
                if re.search(pattern, text):
                    candidates.append({"path": path, "class": name})
        require(not candidates, "E_PRIVACY_CANDIDATE")
        record("scoped_privacy", {"new_owner_files": len(paths), "pattern_classes": list(patterns), "candidates": [], "complete_privacy_claimed": False})

        for session, modules in (("x1", 7), ("x2", 6)):
            security = read(PREFIX + session + "/security-review.json")
            recovery = security.get("recovery", security)
            require(recovery["bounded_findings"] == 0 and security["complete_security_claimed"] is False, "E_SECURITY_REVIEW")
            require(security["source_or_sibling_files_scanned"] == 0 if "source_or_sibling_files_scanned" in security else recovery["source_or_sibling_files_scanned"] == 0, "E_SECURITY_SCOPE")
        record("bounded_security_reviews", {"owner_modules": 13, "bounded_findings": 0, "exhaustive_security_claimed": False})

        truth = read(PREFIX + "final/phase-truth.json")
        source = read(PREFIX + "final/source-and-lifecycle.json")
        require(truth["outcomes"] == OUTCOMES and truth["independent_reproduction"] is False and truth["real_measurements"] == 0 and truth["terminal_verdict"] == "NOT_READY_FOR_STAGE_20", "E_CLAIM_BOUNDARY")
        require(source["source_canonical_status"] == "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" and source["source_canonical_replays"] == 0 and source["source_execution_credit"] == 0, "E_SOURCE_CREDIT")
        record("scientific_and_source_boundaries", {"source_execution_credit": 0, "empirical_measurements": 0, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
        require(git(repo, "rev-parse", "HEAD").decode().strip() == final and not git(repo, "status", "--porcelain=v1").strip(), "E_POST_VALIDATION_STATE")
        record("post_validation_readback", {"head_unchanged": True, "clean": True, "source_canonical_replays": 0})
        status = "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        error = None
    except Exception as exception:  # noqa: BLE001 - every canonical failure must still emit one immutable receipt
        status = "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
        error = {"type": type(exception).__name__, "message": str(exception)}
        checks.append({"name": "stopped_component", "passed": False, "details": error})

    receipt = {"schema": "ghc.family.exact-final-owner-canonical.v1", "owner": "Neris Solane", "phase": "v689-v6", "final_commit": final, "source": SOURCE, "planning": PLANNING, "x1": X1, "x2": X2, "status": status, "canonical_invocations": 1, "canonical_successes": int(error is None), "canonical_replays": 0, "source_canonical_replays": 0, "checks": checks, "checks_passed": sum(item["passed"] for item in checks), "check_count": len(checks), "error": error, "started_at_utc": started, "finished_at_utc": datetime.now(UTC).isoformat(), "entrypoint_sha256": sha(Path(__file__).read_bytes()), "terminal_verdict": "NOT_READY_FOR_STAGE_20", "independent_reproduction": False, "full_repository_suite_run": False}
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(receipt, stream, indent=2, sort_keys=True)
        stream.write("\n")
    print(json.dumps({"status": status, "checks_passed": receipt["checks_passed"], "check_count": receipt["check_count"], "receipt": str(args.output)}), flush=True)
    return 0 if error is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
