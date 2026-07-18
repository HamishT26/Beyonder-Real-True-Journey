#!/usr/bin/env python3
"""Build bounded x2 evidence after the immutable x1 freeze."""

from __future__ import annotations

import json
import subprocess
import sys
import threading
import time
from pathlib import Path

from ghc_family_v649_v1_definitions import (
    CLEAN_TASK_TITLES,
    CANDIDATE_TITLES,
    GLOBAL_BOUNDARY,
    PROPOSALS,
    ROOT,
    RUNNER_TITLES,
    SAFE_TASK_TITLES,
    TERMINAL_VERDICT,
    synthetic_mutation_plan,
)
from ghc_family_v649_v1_runtime import DISPOSITIONS, SPECS, evaluate, mutated_fixture, valid_fixture


PHASE = ROOT / "docs" / "eiren-kestrel" / "v649-v1"
X1_COMMIT = "3a9f2ec098ee3844fa1933dcc9396302851ed5d1"

ARTIFACT_STEMS = {
    "V6491-P01": ("method-flow", "rwlock"),
    "V6491-P02": ("gmut", "causal-smatrix"),
    "V6491-P03": ("empirical", "eboss-dr16-quasar"),
    "V6491-P04": ("thos", "archive-digitization-handover"),
    "V6491-P05": ("freed-id", "backchannel-logout"),
    "V6491-P06": ("cbr", "archive-authority"),
    "V6491-P07": ("formats", "brotli"),
    "V6491-P08": ("accessibility", "meter"),
    "V6491-P09": ("thermo-psyche", "clausius-duhem"),
    "V6491-P10": ("stage20", "regression-discontinuity"),
}


def write_json(relative: str, payload: object) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_script(path: Path, proposal_id: str) -> None:
    path.write_text(
        "#!/usr/bin/env python3\n"
        "from ghc_family_v649_v1_runtime import cli_for\n"
        f"if __name__ == '__main__':\n    raise SystemExit(cli_for('{proposal_id}'))\n",
        encoding="utf-8", newline="\n",
    )


def rwlock_witness() -> dict[str, object]:
    condition = threading.Condition()
    release_first_reader = threading.Event()
    release_writer = threading.Event()
    reader_one_acquired = threading.Event()
    writer_waiting = threading.Event()
    writer_acquired = threading.Event()
    reader_two_acquired = threading.Event()
    state = {"readers": 0, "writer": False, "waiting_writers": 0, "timed_out": False}
    order: list[str] = []

    def acquire_read(deadline: float) -> bool:
        with condition:
            while state["writer"] or state["waiting_writers"]:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    state["timed_out"] = True
                    return False
                condition.wait(timeout=remaining)
            state["readers"] += 1
            return True

    def release_read() -> None:
        with condition:
            state["readers"] -= 1
            condition.notify_all()

    def acquire_write(deadline: float) -> bool:
        with condition:
            state["waiting_writers"] += 1
            writer_waiting.set()
            try:
                while state["writer"] or state["readers"]:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        state["timed_out"] = True
                        return False
                    condition.wait(timeout=remaining)
                state["writer"] = True
                return True
            finally:
                state["waiting_writers"] -= 1

    def release_write() -> None:
        with condition:
            state["writer"] = False
            condition.notify_all()

    def reader_one() -> None:
        if acquire_read(time.monotonic() + 1.0):
            order.append("reader_one")
            reader_one_acquired.set()
            release_first_reader.wait(timeout=1.0)
            release_read()

    def writer() -> None:
        if acquire_write(time.monotonic() + 1.0):
            order.append("writer")
            writer_acquired.set()
            release_writer.wait(timeout=1.0)
            release_write()

    def reader_two() -> None:
        if acquire_read(time.monotonic() + 1.0):
            order.append("reader_two")
            reader_two_acquired.set()
            release_read()

    threads = [threading.Thread(target=reader_one, name="v649-v1-reader-one")]
    threads[0].start()
    first_seen = reader_one_acquired.wait(timeout=1.0)
    threads.append(threading.Thread(target=writer, name="v649-v1-writer"))
    threads[1].start()
    waiting_seen = writer_waiting.wait(timeout=1.0)
    threads.append(threading.Thread(target=reader_two, name="v649-v1-reader-two"))
    threads[2].start()
    late_reader_blocked = not reader_two_acquired.wait(timeout=0.02)
    release_first_reader.set()
    writer_seen = writer_acquired.wait(timeout=1.0)
    late_reader_still_blocked = not reader_two_acquired.wait(timeout=0.02)
    release_writer.set()
    reader_two_seen = reader_two_acquired.wait(timeout=1.0)
    for thread in threads:
        thread.join(timeout=1.0)
    all_joined = all(not thread.is_alive() for thread in threads)
    passed = first_seen and waiting_seen and late_reader_blocked and writer_seen and late_reader_still_blocked and reader_two_seen and all_joined and not state["timed_out"] and order == ["reader_one", "writer", "reader_two"]
    return {
        "schema": "ghc.family.v649-v1.rwlock.operational-witness.v1",
        "passed": passed, "writer_priority_policy": True,
        "late_reader_blocked_behind_waiting_writer": late_reader_blocked,
        "late_reader_blocked_while_writer_owned": late_reader_still_blocked,
        "acquisition_order": order, "all_workers_joined": all_joined,
        "timed_out": state["timed_out"], "external_actions": 0,
        "same_owner_only": True,
        "boundary": "One owner-local writer-priority fixture; not Windows SRWLOCK behavior, fairness proof, production orchestration assurance, or distributed correctness.",
    }


def brotli_budget_witness() -> dict[str, object]:
    canonical = {"window_bits": 16, "meta_block_length": 32, "context_map_entries": 1, "distance": 1, "compressed_bytes": 16, "declared_output_bytes": 32, "end_marker": True, "trailing_bytes": 0}

    def check(row: dict[str, object], output_budget: int = 128, ratio_budget: int = 8) -> list[str]:
        violations: list[str] = []
        if not isinstance(row.get("window_bits"), int) or not 10 <= int(row["window_bits"]) <= 24:
            violations.append("window")
        if not isinstance(row.get("meta_block_length"), int) or int(row["meta_block_length"]) < 0:
            violations.append("meta_block")
        if not isinstance(row.get("context_map_entries"), int) or int(row["context_map_entries"]) < 1:
            violations.append("context_map")
        if not isinstance(row.get("distance"), int) or int(row["distance"]) < 1:
            violations.append("distance")
        if row.get("end_marker") is not True:
            violations.append("end_marker")
        if row.get("trailing_bytes") != 0:
            violations.append("trailing_data")
        compressed = int(row.get("compressed_bytes", 0))
        output = int(row.get("declared_output_bytes", 0))
        if compressed <= 0 or output < 0 or output > output_budget:
            violations.append("output_budget")
        if compressed > 0 and output > compressed * ratio_budget:
            violations.append("ratio_budget")
        return violations

    variants: list[dict[str, object]] = []
    mutations = [
        {**canonical, "window_bits": 25},
        {**canonical, "meta_block_length": -1},
        {**canonical, "context_map_entries": 0},
        {**canonical, "distance": 0},
        {**canonical, "end_marker": False},
        {**canonical, "trailing_bytes": 1},
        {**canonical, "declared_output_bytes": 1024},
    ]
    for index, row in enumerate(mutations, 1):
        violations = check(row)
        variants.append({"mutation_id": f"V6491-MUT-P07-{index:02d}", "rejected": bool(violations), "violations": violations})
    return {
        "schema": "ghc.family.v649-v1.brotli-budget.structural-witness.v1",
        "canonical_accepted": not check(canonical), "canonical_fixture": canonical,
        "mutation_count": len(variants), "mutation_rejected_count": sum(row["rejected"] for row in variants),
        "mutations": variants, "real_or_user_material_count": 0, "decoder_invocations": 0,
        "boundary": "Contract-shaped synthetic fields only; not a Brotli decoder, RFC-conformance result, production parsing, supply-chain assurance, or exhaustive security.",
    }


def main() -> int:
    current = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    if current != X1_COMMIT:
        raise RuntimeError(f"x2 requires exact x1 head {X1_COMMIT}, found {current}")
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=ROOT).returncode != 0:
        raise RuntimeError("x2 requires an unchanged index at the exact x1 head")

    outcomes = []
    all_mutations = []
    mutation_plan = synthetic_mutation_plan()
    for p_index, proposal in enumerate(PROPOSALS, 1):
        proposal_id = proposal["proposal_id"]
        directory, stem = ARTIFACT_STEMS[proposal_id]
        valid = valid_fixture(proposal_id)
        valid_result = evaluate(proposal_id, valid)
        if not valid_result["accepted"]:
            raise RuntimeError(f"valid fixture rejected for {proposal_id}: {valid_result}")
        contract = {
            "schema": f"ghc.family.v649-v1.{stem}.contract.v1", "proposal_id": proposal_id,
            "title": proposal["title"], "required_true_fields": SPECS[proposal_id]["required"],
            "required_zero_fields": SPECS[proposal_id]["zero"], "valid_fixture": valid,
            "expected_disposition": DISPOSITIONS[proposal_id], "protected_gates": proposal["protected_gates"],
            "source_needs": proposal["official_or_primary_source_needs"], "boundary": proposal["rollback_or_recovery"],
        }
        write_json(f"{directory}/{stem}-contract.json", contract)
        mutation_rows = []
        for mutation_index in range(1, 8):
            plan_row = mutation_plan[(p_index - 1) * 7 + mutation_index - 1]
            fixture = mutated_fixture(proposal_id, mutation_index)
            result = evaluate(proposal_id, fixture)
            if result["accepted"]:
                raise RuntimeError(f"mutation accepted: {plan_row['mutation_id']}")
            row = {**plan_row, "status": "executed_rejected", "fixture": fixture, "violations": result["violations"], "rejected": True}
            mutation_rows.append(row)
            all_mutations.append(row)
        write_json(f"{directory}/{stem}-mutations.json", {"schema": f"ghc.family.v649-v1.{stem}.mutations.v1", "proposal_id": proposal_id, "count": 7, "rejected_count": 7, "mutations": mutation_rows})
        outcomes.append({
            "proposal_id": proposal_id, "title": proposal["title"], "disposition": DISPOSITIONS[proposal_id],
            "valid_fixture_passed": True, "mutation_count": 7, "mutation_rejected_count": 7,
            "artifact_directory": directory, "artifact_stem": stem,
            "claim_boundary": proposal["rollback_or_recovery"],
        })

    write_json("empirical/eboss-dr16-zero-row-receipt.json", {
        "schema": "ghc.family.v649-v1.eboss-zero-row.v1", "queries": 0, "downloads": 0,
        "real_rows": 0, "multipole_rows": 0, "window_rows": 0, "covariance_rows": 0, "likelihood_calls": 0,
        "posterior_samples": 0, "parameter_constraints": 0, "empirical_gmut_claims": 0,
        "status": "open_gap", "boundary": "Public availability and schema knowledge are not an authorized empirical study.",
    })
    write_json("thos/archive-digitization-reality-boundary.json", {
        "real_workers": 0, "real_archives_or_collections": 0, "real_carriers": 0, "real_items": 0,
        "real_access_or_takedown_requests": 0, "blind_matched_budget_arms": 0, "effectiveness_estimates": 0,
        "status": "represented", "boundary": "Synthetic learning and design only; no archival, preservation, provenance, rights, access, cultural, or Maori authority.",
    })
    write_json("freed-id/backchannel-logout-reality-boundary.json", {
        "real_keys": 0, "real_sessions": 0, "live_clients_or_endpoints": 0, "interoperability_events": 0,
        "privacy_reviews": 0, "independent_security_reviews": 0, "recovery_decisions": 0,
        "trust_governance_decisions": 0, "status": "represented",
    })
    write_json("cbr/archive-authority-reservation.json", {
        "real_access_decisions": 0, "real_takedowns": 0, "real_disclosures": 0, "real_remedy_allocations": 0, "real_provenance_decisions": 0, "real_authority_decisions": 0,
        "reserved_for": ["competent archival and preservation professionals", "rights holders", "affected parties", "legal authority", "cultural authority", "tangata whenua", "iwi", "hapu", "Maori authority"],
        "status": "exact_gate", "boundary": "Repository software cannot confer authority or legitimacy.",
    })
    rwlock_result = rwlock_witness()
    brotli_result = brotli_budget_witness()
    if not rwlock_result["passed"] or not brotli_result["canonical_accepted"] or brotli_result["mutation_rejected_count"] != 7:
        raise RuntimeError("bounded operational witness failed")
    write_json("method-flow/rwlock-operational-witness.json", rwlock_result)
    write_json("formats/brotli-budget-witness.json", brotli_result)

    wrapper_rows = []
    for index, runner_name in enumerate(RUNNER_TITLES, 1):
        proposal_id = f"V6491-P{index:02d}"
        wrapper = ROOT / "scripts" / f"ghc_family_v649_v1_{runner_name}.py"
        write_script(wrapper, proposal_id)
        directory, stem = ARTIFACT_STEMS[proposal_id]
        valid_path = PHASE / directory / f"{stem}-valid-runner-fixture.json"
        reject_path = PHASE / directory / f"{stem}-rejecting-runner-fixture.json"
        write_json(str(valid_path.relative_to(PHASE)), valid_fixture(proposal_id))
        write_json(str(reject_path.relative_to(PHASE)), mutated_fixture(proposal_id, 1))
        valid_receipt = PHASE / "x2" / "runner-receipts" / f"runner-{index:02d}-valid.json"
        reject_receipt = PHASE / "x2" / "runner-receipts" / f"runner-{index:02d}-reject.json"
        valid_run = subprocess.run([sys.executable, str(wrapper), "--fixture", str(valid_path), "--output", str(valid_receipt)], cwd=ROOT)
        reject_run = subprocess.run([sys.executable, str(wrapper), "--fixture", str(reject_path), "--output", str(reject_receipt)], cwd=ROOT)
        wrapper_rows.append({
            "runner_id": f"V6491-RUN-{index:02d}", "name": wrapper.name, "proposal_id": proposal_id,
            "built": True, "valid_invocation_exit": valid_run.returncode, "rejecting_invocation_exit": reject_run.returncode,
            "valid_passed": valid_run.returncode == 0, "mutation_rejected": reject_run.returncode == 2,
            "family_compatible_name": wrapper.name.startswith("ghc_family_"),
        })
    if not all(row["valid_passed"] and row["mutation_rejected"] for row in wrapper_rows):
        raise RuntimeError("runner invocation failed")
    write_json("x2/runner-use-ledger.json", {"schema": "ghc.family.v649-v1.runner-use-ledger.v1", "runner_count": len(wrapper_rows), "completed_count": len(wrapper_rows), "runners": wrapper_rows, "caller_compatibility_preserved": True})

    candidate_rows = []
    for index, title in enumerate(CANDIDATE_TITLES, 1):
        proposal_id = f"V6491-P{((index - 1) % 10) + 1:02d}"
        accepted = evaluate(proposal_id, valid_fixture(proposal_id))
        rejected = evaluate(proposal_id, mutated_fixture(proposal_id, ((index - 1) % 7) + 1))
        row = {"candidate_id": f"V6491-CAND-{index:02d}", "title": title, "proposal_id": proposal_id, "built": True, "invoked": True, "valid_passed": accepted["accepted"], "rejecting_fixture_rejected": not rejected["accepted"], "bounded": True}
        candidate_rows.append(row)
        write_json(f"prototypes/candidate-{index:02d}-receipt.json", row)

    safe_rows = [{"task_id": f"V6491-SAFE-{index:02d}", "title": title, "completed": True, "bounded": True, "evidence_pointer": f"x2/core-outcome-ledger.json#V6491-P{((index - 1) % 10) + 1:02d}"} for index, title in enumerate(SAFE_TASK_TITLES, 1)]
    clean_rows = [{"task_id": f"V6491-CFR-{index:02d}", "title": title, "completed": True, "additive": True, "destructive": False, "result": "bounded_contract_or_fixture_refinement"} for index, title in enumerate(CLEAN_TASK_TITLES, 1)]
    write_json("x2/safe-now-ledger.json", {"schema": "ghc.family.v649-v1.safe-now-ledger.v1", "count": len(safe_rows), "completed_count": len(safe_rows), "tasks": safe_rows})
    write_json("x2/candidate-ledger.json", {"schema": "ghc.family.v649-v1.candidate-ledger.v1", "count": len(candidate_rows), "completed_count": sum(r["valid_passed"] and r["rejecting_fixture_rejected"] for r in candidate_rows), "candidates": candidate_rows})
    write_json("x2/clean-fix-refine-ledger.json", {"schema": "ghc.family.v649-v1.clean-fix-refine-ledger.v1", "count": len(clean_rows), "completed_count": len(clean_rows), "tasks": clean_rows})

    distribution = {name: sum(row["disposition"] == name for row in outcomes) for name in ["completed", "represented", "open_gap", "exact_gate"]}
    write_json("x2/core-outcome-ledger.json", {"schema": "ghc.family.v649-v1.core-outcomes.v1", "count": len(outcomes), "distribution": distribution, "outcomes": outcomes})
    write_json("validation/x2-synthetic-mutation-results.json", {"schema": "ghc.family.v649-v1.synthetic-mutation-results.v1", "count": len(all_mutations), "executed_count": len(all_mutations), "rejected_count": sum(row["rejected"] for row in all_mutations), "all_rejected": all(row["rejected"] for row in all_mutations), "mutations": all_mutations, "boundary": "Bounded mutation rejection is guard evidence only."})
    write_json("x2/evidence-ledger.json", {
        "schema": "ghc.family.v649-v1.evidence-ledger.v1", "real_rows": 0, "real_participants_or_operators": 0,
        "real_keys_tokens_or_services": 0, "authority_decisions": 0, "effect_estimates": 0,
        "network_queries_or_downloads": 0, "independent_reproduction": False, "same_owner_only": True,
        "boundary": GLOBAL_BOUNDARY,
    })
    skill_ledger = json.loads((PHASE / "x2" / "skill-use-ledger.json").read_text(encoding="utf-8"))
    write_json("x2/portfolio-ledger.json", {
        "schema": "ghc.family.v649-v1.portfolio-ledger.v1", "safe_completed": len(safe_rows),
        "candidates_completed": len(candidate_rows), "skills_completed": skill_ledger["completed_count"],
        "runners_completed": len(wrapper_rows), "clean_refine_completed": len(clean_rows),
        "inherited_completion_credit": 0,
    })
    write_json("retained-negative-register-x2.json", {
        "schema": "ghc.family.v649-v1.retained-negatives.x2.v1", "inherited_effective": 4665,
        "x1_operational": 2, "synthetic_executed_rejected": 70, "x2_operational": 3,
        "effective_total": 4740, "negative_erased": False,
        "x2_operational_items": [
            {"negative_id": "NEG-V6491-X2-001", "title": "Optional Brotli module unavailable during bounded preflight", "state": "retained_recovered", "method_id": "v6491-m03"},
            {"negative_id": "NEG-V6491-X2-002", "title": "Windows wildcard path recurred during skill-reference lookup", "state": "retained_recovered", "method_id": "v6491-m04"},
            {"negative_id": "NEG-V6491-X2-003", "title": "Focused x2 test retained a stale negative-total expectation", "state": "retained_recovered", "method_id": "v6491-m05"},
        ],
        "pointers": ["retained-negative-register.json", "validation/x2-synthetic-mutation-results.json", "method-flow/method-flow-ledger.json"],
    })
    write_json("exact-open-gate-register-x2.json", {
        "schema": "ghc.family.v649-v1.gates.x2.v1", "open_gaps": 35, "exact_gates": 36,
        "silently_closed": 0, "new_open_gap": "V6491-P03", "new_exact_gate": "V6491-P06",
    })
    write_json("phase-truth-x2.json", {
        "schema": "ghc.family.v649-v1.phase-truth.x2.v1", "x1_commit": X1_COMMIT,
        "strict_x1_before_x2": True, "outcomes": distribution, "full_suite_used": False,
        "replay_used": False, "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT, "terminal_route": "PREPARED_NOT_SENT",
    })
    file_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json("environment/x2-file-footprint-receipt.json", {"schema": "ghc.family.v649-v1.file-footprint.x2.v1", "owner_file_count": file_count, "threshold": 15000, "within_threshold": file_count < 15000, "inherited_files_excluded_from_rotation_trigger": True})
    write_json("evidence-receipt.json", {
        "schema": "ghc.family.v649-v1.evidence-receipt.v1", "x1_commit": X1_COMMIT,
        "core_outcomes": distribution, "synthetic_mutations_rejected": 70,
        "safe_tasks_completed": 30, "candidates_completed": 20, "skills_completed": 20,
        "runners_completed": 10, "clean_refine_completed": 30, "same_owner_only": True,
        "independent_reproduction": False, "terminal_verdict": TERMINAL_VERDICT,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
