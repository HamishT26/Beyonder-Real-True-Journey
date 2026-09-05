"""One owner-scoped canonical invocation; write only external receipts."""
import argparse
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys

SOURCE = "74dd8f72cfc9d06d8c6c7370131a5baa61a66397"
X1 = "e3f97e0764cbbf0f5aa7d3a9f2ecf42bfb142b64"
EVIDENCE = "0c975a4f95b3011121ebdc25e3a7c695fd3292b8"
BRANCH = "codex/GHC-Family/rowan-ash-v685-v6-full-tools"
BASE = "docs/rowan-ash/v685-v6/"
EXTRA = {"scripts/ghc_family_evidence_capsule.py", "tests/test_ghc_family_evidence_capsule.py"}
PRIVATE = {
    "private_local_path": re.compile(r"(?i)[A-Z]:[\\/](?:Users|GHC-Archives)[\\/]"),
    "private_uri": re.compile(r"(?i)(?:app|codex|chatgpt|session)://"),
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
    "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret)\s*[:=]\s*['\"][A-Za-z0-9_-]{16,}"),
    "delegation_markup": re.compile(r"<(?:source_thread_id|codex_delegation|thread_id)>"),
}


def encode(value):
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False,
                       allow_nan=False) + "\n").encode("utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--expected-final", required=True)
    ap.add_argument("--receipt", required=True)
    args = ap.parse_args()
    repo = Path(args.repo).resolve()
    receipt_path = Path(args.receipt)
    reservation_path = Path(str(receipt_path) + ".invocation.json")
    if receipt_path.exists() or reservation_path.exists():
        raise SystemExit("Canonical already invoked; no replay is permitted.")
    binding = dict(owner="Rowan Ash", phase="v685-v6", source=SOURCE, x1=X1,
                   evidence=EVIDENCE, final=args.expected_final, branch=BRANCH)
    with reservation_path.open("xb") as stream:
        stream.write(encode(dict(schema="ghc.family.rowan-ash.canonical-reservation.v1",
                                 binding=binding, canonical_invocation_count=1,
                                 canonical_success_count=0, replay_prohibited=True)))
    checks, details = {}, {}
    manifest_entries = 0

    def check(name, value):
        checks[name] = bool(value)

    def git(*argv):
        run = subprocess.run(["git", "-C", str(repo), *argv], capture_output=True)
        if run.returncode:
            raise RuntimeError("git_read_failed")
        return run.stdout

    def changed(a, b):
        raw = git("diff", "--name-only", "-z", a, b)
        return raw.decode("utf-8").rstrip("\0").split("\0") if raw else []

    try:
        spec = importlib.util.spec_from_file_location("capsule", repo / "scripts/ghc_family_evidence_capsule.py")
        c = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(c)
        head = git("rev-parse", "HEAD").decode().strip()
        check("expected_final", head == args.expected_final and bool(re.fullmatch("[0-9a-f]{40}", head)))
        check("owned_branch", git("symbolic-ref", "--short", "HEAD").decode().strip() == BRANCH)
        expected_parents = {X1: SOURCE, EVIDENCE: X1, head: EVIDENCE}
        chain = git("rev-list", "--parents", SOURCE + ".." + head).decode().splitlines()
        check("three_direct_single_parent_commits",
              len(chain) == 3 and all(line.split() == [line.split()[0], expected_parents.get(line.split()[0])]
                                      for line in chain))
        delta = changed(SOURCE, head)
        x1_paths = changed(SOURCE, X1)
        evidence_paths = changed(X1, EVIDENCE)
        final_paths = changed(EVIDENCE, head)
        check("exact_owner_delta", bool(delta) and all(p.startswith(BASE) or p in EXTRA for p in delta))
        status = git("diff", "--name-status", "-z", SOURCE, head).decode().rstrip("\0").split("\0")
        check("additive_only", all(status[i] == "A" for i in range(0, len(status), 2)))
        check("file_ceiling", len(delta) < 2000)
        check("planning_only_x1", len(x1_paths) == 38 and all(
            p.startswith(BASE + "x1/") or p in {BASE + "validation/x1-manifest.json", BASE + "validation/x1-precommit.json"}
            for p in x1_paths))
        check("x1_remains_immutable", not changed(X1, head) or not (set(changed(X1, head)) & set(x1_paths)))
        check("x2_remains_immutable", not (set(final_paths) & set(evidence_paths)))

        def blobs(revision, paths):
            result, modes = {}, {}
            for i in range(0, len(paths), 64):
                chunk, chunk_modes = c.git_payloads(repo, revision, paths[i:i + 64])
                result.update(chunk)
                modes.update(chunk_modes)
                c.need(sum(map(len, result.values())) <= 64 * 1024 * 1024, "canonical_payload_budget")
            return result, modes

        data, modes = blobs(head, delta)
        x1_data, _ = blobs(X1, x1_paths)
        evidence_data, _ = blobs(EVIDENCE, evidence_paths)
        read = lambda p: c.strict_json(data[BASE + p])

        def manifest(path, view, expected, allowed_exclusions):
            nonlocal manifest_entries
            m = c.strict_json(data[path])
            entries = m.get("entries", [])
            excluded = set(m.get("declared_self_exclusions", []))
            paths = [e["path"] for e in entries]
            valid = (m.get("byte_domain") == "raw_git_blob_v1"
                     and m.get("entry_count") == len(entries)
                     and len(paths) == len(set(paths))
                     and paths == sorted(paths)
                     and excluded == set(allowed_exclusions)
                     and set(paths) == set(expected) - excluded)
            for entry in entries:
                b = view.get(entry["path"])
                valid = valid and b is not None
                if b is not None:
                    valid = valid and (entry.get("byte_domain", m["byte_domain"]) == "raw_git_blob_v1"
                                       and type(entry.get("bytes")) is int
                                       and entry["bytes"] == len(b)
                                       and entry.get("sha256") == hashlib.sha256(b).hexdigest())
                    if "mode" in entry:
                        valid = valid and entry["mode"] == modes[entry["path"]]
            manifest_entries += len(entries)
            return valid

        x1_ex = [BASE + "validation/x1-manifest.json", BASE + "validation/x1-precommit.json"]
        ev_ex = [BASE + "validation/evidence-manifest.json", BASE + "validation/evidence-precommit.json"]
        final_ex = [BASE + "validation/final-delta-manifest.json",
                    BASE + "validation/final-owner-manifest.json",
                    BASE + "validation/final-precommit.json"]
        check("x1_manifest", manifest(x1_ex[0], x1_data, x1_paths, x1_ex))
        check("evidence_manifest", manifest(ev_ex[0], evidence_data, evidence_paths, ev_ex))
        card_paths = [p for p in evidence_paths if p.startswith(BASE + "x2/flashcards/")]
        card_manifest = BASE + "x2/flashcards/card-manifest.json"
        check("card_manifest", manifest(card_manifest, evidence_data, card_paths, [card_manifest]))
        check("final_delta_manifest", manifest(final_ex[0], data, final_paths, final_ex))
        check("final_owner_manifest", manifest(final_ex[1], data, delta, final_ex))
        seal_paths = [BASE + "final/" + p for p in
                      ("phase-truth.json", "completion-checklist.json", "overview.md", "terminal-route.json")]
        check("content_seal", manifest(BASE + "seal/content-seal.json", data, seal_paths, []))

        parsed = {}
        privacy_hits, python_count, security_hits = [], 0, []
        for path, raw in data.items():
            text = raw.decode("utf-8")
            if path.endswith(".json"):
                parsed[path] = c.strict_json(text)
            for name, pattern in PRIVATE.items():
                if pattern.search(text):
                    privacy_hits.append(dict(path=path, pattern_class=name))
            if path.endswith(".py"):
                tree = ast.parse(text, filename=path)
                python_count += 1
                for node in ast.walk(tree):
                    if not isinstance(node, ast.Call):
                        continue
                    if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "breakpoint"}:
                        security_hits.append(dict(path=path, class_name="dynamic_execution"))
                    if any(k.arg == "shell" and isinstance(k.value, ast.Constant) and k.value.value is True
                           for k in node.keywords):
                        security_hits.append(dict(path=path, class_name="shell_true"))
        check("all_json_parses", bool(parsed))
        check("all_changed_python_parses", python_count == 13)
        check("five_class_privacy", not privacy_hits)
        check("bounded_security_review", not security_hits and read("final/validation-contract.json")["manual_code_review_completed"])
        check("diff_whitespace", not git("diff", "--check", SOURCE, head))

        baseline, focused = read("x2/behavioral-tests.json"), read("x2/focused-recovery.json")
        check("attributable_behavioral_composite", baseline["valid"] and baseline["tests_run"] == 60
              and len(set(baseline["successful_proposals"])) == 60 and baseline["rejecting_fixture_count"] == 103
              and focused["valid"] and focused["tests_run"] == 2 and focused["rejecting_fixture_count"] == 9)
        definitions = read("x2/definition-bindings.json")
        check("retained_and_current_definition_hashes",
              all(hashlib.sha256(data[definitions["retained_definition_paths"][p]]).hexdigest() == digest
                  for p, digest in definitions["baseline"].items())
              and all(hashlib.sha256(data[p]).hexdigest() == digest for p, digest in definitions["current"].items()))
        runner, skills = read("x2/runner-validation.json"), read("x2/skill-validation.json")
        check("ten_runner_interfaces", runner["valid"] and runner["runner_count"] == 10
              and all(r["valid"] for r in runner["rows"]))
        check("twenty_local_skills", skills["valid"] and skills["skill_count"] == 20
              and all(r["valid"] and r["read_through_eof"] for r in skills["rows"]))
        deck = read("x2/flashcards/deck-index.json")
        check("four_tier_deck", c.validate_deck(deck)["card_count"] == 67)
        check("report_representation_only", c.validate_report(data[BASE + "x2/accessible-report.html"].decode())["manual_evaluation_complete"] is False)
        rows = read("x2/proposal-evidence.json")["rows"]
        check("four_outcomes_preserved", len(rows) == 60 and
              {s: sum(r["outcome"] == s for r in rows) for s in c.OUTCOMES} ==
              {"completed": 48, "represented": 6, "open_gap": 3, "exact_gate": 3}
              and all(c.validate_credit(r)["valid"] for r in rows))
        inherited = read("x2/inherited-revalidation.json")
        check("inherited_zero_credit", inherited["count"] == 60 and
              all(r["novelty_credit"] == r["current_completion_credit"] == 0 for r in inherited["rows"]))
        startup = read("x1/startup.json")
        check("source_canonical_failure_retained", startup["source"] == SOURCE
              and startup["source_canonical"] == {"invocations": 1, "checks": 24, "passed": 23,
                 "success_credit": 0, "replays": 0, "failed_dependency": "content_seal_pass"})
        flow = read("x2/method-flow.json")
        negatives = read("x2/retained-negatives.json")
        counts = read("final/phase-truth.json")["effective_record_counts"]
        actual_counts = dict(effective_negatives=62965 + len(negatives["rows"]),
                             effective_methods=79730 + len(flow["methods"]),
                             failed_witnesses=34026 + sum(w["result"] == "fail" for w in flow["witnesses"]),
                             bounded_passing_witnesses=61314 + sum(w["result"] == "pass" for w in flow["witnesses"]),
                             open_gaps=564, exact_gates=551)
        check("retained_record_arithmetic", counts == actual_counts and
              len(negatives["rows"]) == 190 and read("x2/method-flow-validation.json")["valid"])
        complete = read("final/completion-checklist.json")
        check("complete_incomplete_boundary", complete["all_frozen_safe_and_representation_conditions_resolved"]
              and complete["real_actions_behind_gates_executed"] == 0)
        route = read("final/terminal-route.json")
        check("terminal_route_held", route["outbound_send_count"] == 0
              and route["remaster_started"] is False and route["new_tasks_created"] == 0
              and route["state"] == "HELD_FOR_FRESH_DIRECT_TERMINAL_CONTROL")
        check("clean_state", not git("status", "--porcelain=v1", "--untracked-files=all"))
        upstream = git("rev-parse", "@{upstream}").decode().strip()
        tracking = git("rev-parse", "refs/remotes/origin/" + BRANCH).decode().strip()
        live = git("ls-remote", "origin", "refs/heads/" + BRANCH).decode().splitlines()
        live_head = live[0].split()[0] if len(live) == 1 else None
        check("fresh_four_way_equality", head == upstream == tracking == live_head)
        divergence = git("rev-list", "--left-right", "--count", "HEAD...@{upstream}").decode().split()
        check("zero_divergence", divergence == ["0", "0"])
        materialized = sum(p.is_file() and p.name != ".git" for p in repo.rglob("*"))
        check("materialized_file_ceiling", materialized < 2000)
        details.update(owner_file_count=len(delta), materialized_file_count=materialized,
                       json_parse_count=len(parsed), python_file_count=python_count,
                       manifest_entry_total=manifest_entries, privacy_hits=privacy_hits,
                       bounded_security_findings=security_hits, fresh_live=live_head,
                       record_counts=counts)
    except Exception as exc:
        checks["canonical_execution_completed"] = False
        details["execution_error_class"] = type(exc).__name__
    valid = bool(checks) and all(checks.values())
    result = dict(schema="ghc.family.rowan-ash.exact-final-canonical.v1", **binding,
                  status="VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL" if valid else "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                  valid=valid, canonical_invocation_count=1, canonical_success_count=int(valid),
                  canonical_replay_count=0, checks=checks, check_count=len(checks),
                  pass_count=sum(checks.values()), failed_checks=[k for k,v in checks.items() if not v],
                  details=details, inherited_canonical_success_credit=0,
                  full_repository_suite=False, independent_reproduction=False,
                  terminal_verdict="NOT_READY_FOR_STAGE_20")
    with receipt_path.open("xb") as stream:
        stream.write(encode(result))
    sys.stdout.buffer.write(encode(dict(status=result["status"], check_count=len(checks),
                                        pass_count=result["pass_count"], failed_checks=result["failed_checks"],
                                        owner_file_count=details.get("owner_file_count"))))
    return 0 if valid else 2


if __name__ == "__main__":
    raise SystemExit(main())
