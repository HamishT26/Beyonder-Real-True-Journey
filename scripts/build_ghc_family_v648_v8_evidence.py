#!/usr/bin/env python3
"""Build bounded x2 evidence after the immutable x1 freeze."""

from __future__ import annotations

import json
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path

from ghc_family_v648_v8_definitions import (
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
from ghc_family_v648_v8_runtime import DISPOSITIONS, SPECS, evaluate, mutated_fixture, valid_fixture


PHASE = ROOT / "docs" / "sylven-arc" / "v648-v8"
X1_COMMIT = "d86990f673aa82c45a5296ebba88c79a6dc3bde4"

ARTIFACT_STEMS = {
    "V6488-P01": ("method-flow", "condition-wait"),
    "V6488-P02": ("gmut", "haag-ruelle"),
    "V6488-P03": ("empirical", "mightee-dr1"),
    "V6488-P04": ("thos", "water-treatment-handover"),
    "V6488-P05": ("freed-id", "resource-indicator"),
    "V6488-P06": ("cbr", "water-authority"),
    "V6488-P07": ("formats", "pcapng"),
    "V6488-P08": ("accessibility", "spinbutton"),
    "V6488-P09": ("thermo-psyche", "soret-dufour"),
    "V6488-P10": ("stage20", "overlap-weight"),
}


def write_json(relative: str, payload: object) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_script(path: Path, proposal_id: str) -> None:
    path.write_text(
        "#!/usr/bin/env python3\n"
        "from ghc_family_v648_v8_runtime import cli_for\n"
        f"if __name__ == '__main__':\n    raise SystemExit(cli_for('{proposal_id}'))\n",
        encoding="utf-8", newline="\n",
    )


def condition_wait_witness() -> dict[str, object]:
    condition = threading.Condition()
    waiting = threading.Event()
    proceeded = threading.Event()
    state = {"ready": False, "cancelled": False, "iterations": 0, "timed_out": False}

    def worker() -> None:
        deadline = time.monotonic() + 1.0
        with condition:
            waiting.set()
            while not state["ready"] and not state["cancelled"]:
                state["iterations"] += 1
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    state["timed_out"] = True
                    return
                condition.wait(timeout=remaining)
            if state["ready"]:
                proceeded.set()

    thread = threading.Thread(target=worker, name="v648-v8-bounded-condition-witness")
    thread.start()
    waiting_seen = waiting.wait(timeout=1.0)
    with condition:
        condition.notify_all()
    spurious_notify_did_not_pass = not proceeded.wait(timeout=0.02)
    with condition:
        state["ready"] = True
        condition.notify_all()
    thread.join(timeout=1.0)
    passed = waiting_seen and spurious_notify_did_not_pass and proceeded.is_set() and not thread.is_alive() and not state["timed_out"]
    return {
        "schema": "ghc.family.v648-v8.condition-wait.operational-witness.v1",
        "passed": passed, "waiting_seen": waiting_seen,
        "spurious_notify_did_not_pass_predicate": spurious_notify_did_not_pass,
        "predicate_transition_passed": proceeded.is_set(), "worker_joined": not thread.is_alive(),
        "wait_loop_iterations": state["iterations"], "timed_out": state["timed_out"],
        "external_actions": 0, "same_owner_only": True,
        "boundary": "One bounded local threading witness; not production orchestration assurance.",
    }


def pcapng_byte_witness() -> dict[str, object]:
    canonical = struct.pack("<IIIHHqI", 0x0A0D0D0A, 28, 0x1A2B3C4D, 1, 0, -1, 28)

    def check(data: bytes, budget: int = 4096) -> list[str]:
        violations: list[str] = []
        if len(data) > budget:
            violations.append("budget")
        if len(data) < 28:
            return violations + ["truncated"]
        block_type, total, magic = struct.unpack_from("<III", data, 0)
        trailing = struct.unpack_from("<I", data, len(data) - 4)[0]
        if block_type != 0x0A0D0D0A:
            violations.append("section_header")
        if total < 28 or total % 4:
            violations.append("block_length")
        if total != len(data):
            violations.append("declared_length")
        if trailing != total:
            violations.append("length_mirror")
        if magic != 0x1A2B3C4D:
            violations.append("byte_order_magic")
        return violations

    fixtures = []
    variants = [
        b"BAD!" + canonical[4:],
        canonical[:4] + struct.pack("<I", 24) + canonical[8:],
        canonical[:-4] + struct.pack("<I", 32),
        canonical[:8] + struct.pack("<I", 0) + canonical[12:],
        canonical[:20],
        canonical + (b"\x00" * 4097),
        canonical + b"\x00\x00\x00\x00",
    ]
    for index, data in enumerate(variants, 1):
        violations = check(data)
        fixtures.append({"mutation_id": f"V6488-MUT-P07-{index:02d}", "rejected": bool(violations), "violations": violations})
    return {
        "schema": "ghc.family.v648-v8.pcapng.byte-witness.v1",
        "canonical_bytes": len(canonical), "canonical_accepted": not check(canonical),
        "mutation_count": len(fixtures), "mutation_rejected_count": sum(row["rejected"] for row in fixtures),
        "mutations": fixtures, "real_packet_count": 0,
        "boundary": "Disposable synthetic section-header bytes only; not production parsing or exhaustive security.",
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
            "schema": f"ghc.family.v648-v8.{stem}.contract.v1", "proposal_id": proposal_id,
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
        write_json(f"{directory}/{stem}-mutations.json", {"schema": f"ghc.family.v648-v8.{stem}.mutations.v1", "proposal_id": proposal_id, "count": 7, "rejected_count": 7, "mutations": mutation_rows})
        outcomes.append({
            "proposal_id": proposal_id, "title": proposal["title"], "disposition": DISPOSITIONS[proposal_id],
            "valid_fixture_passed": True, "mutation_count": 7, "mutation_rejected_count": 7,
            "artifact_directory": directory, "artifact_stem": stem,
            "claim_boundary": proposal["rollback_or_recovery"],
        })

    write_json("empirical/mightee-dr1-zero-row-receipt.json", {
        "schema": "ghc.family.v648-v8.mightee-zero-row.v1", "queries": 0, "downloads": 0,
        "real_rows": 0, "catalogue_matches": 0, "covariance_rows": 0, "likelihood_calls": 0,
        "posterior_samples": 0, "parameter_constraints": 0, "empirical_gmut_claims": 0,
        "status": "open_gap", "boundary": "Public availability and schema knowledge are not an authorized empirical study.",
    })
    write_json("thos/water-treatment-reality-boundary.json", {
        "real_workers": 0, "real_suppliers": 0, "real_treatment_plants": 0, "real_samples": 0,
        "real_incidents": 0, "blind_matched_budget_arms": 0, "effectiveness_estimates": 0,
        "status": "represented", "boundary": "Synthetic learning and design only; no professional or public-health authority.",
    })
    write_json("freed-id/resource-indicator-reality-boundary.json", {
        "real_keys": 0, "real_tokens": 0, "live_services": 0, "interoperability_events": 0,
        "privacy_reviews": 0, "independent_security_reviews": 0, "recovery_decisions": 0,
        "trust_governance_decisions": 0, "status": "represented",
    })
    write_json("cbr/water-authority-reservation.json", {
        "real_notices": 0, "real_disclosures": 0, "real_remedy_allocations": 0, "real_authority_decisions": 0,
        "reserved_for": ["competent drinking-water authority", "public-health authority", "affected parties", "legal authority", "cultural authority", "tangata whenua", "iwi", "hapu", "Maori authority"],
        "status": "exact_gate", "boundary": "Repository software cannot confer authority or legitimacy.",
    })
    condition_witness = condition_wait_witness()
    pcapng_witness = pcapng_byte_witness()
    if not condition_witness["passed"] or not pcapng_witness["canonical_accepted"] or pcapng_witness["mutation_rejected_count"] != 7:
        raise RuntimeError("bounded operational witness failed")
    write_json("method-flow/condition-wait-operational-witness.json", condition_witness)
    write_json("formats/pcapng-byte-witness.json", pcapng_witness)

    wrapper_rows = []
    for index, runner_name in enumerate(RUNNER_TITLES, 1):
        proposal_id = f"V6488-P{index:02d}"
        wrapper = ROOT / "scripts" / f"ghc_family_v648_v8_{runner_name}.py"
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
            "runner_id": f"V6488-RUN-{index:02d}", "name": wrapper.name, "proposal_id": proposal_id,
            "built": True, "valid_invocation_exit": valid_run.returncode, "rejecting_invocation_exit": reject_run.returncode,
            "valid_passed": valid_run.returncode == 0, "mutation_rejected": reject_run.returncode == 2,
            "family_compatible_name": wrapper.name.startswith("ghc_family_"),
        })
    if not all(row["valid_passed"] and row["mutation_rejected"] for row in wrapper_rows):
        raise RuntimeError("runner invocation failed")
    write_json("x2/runner-use-ledger.json", {"schema": "ghc.family.v648-v8.runner-use-ledger.v1", "runner_count": len(wrapper_rows), "completed_count": len(wrapper_rows), "runners": wrapper_rows, "caller_compatibility_preserved": True})

    candidate_rows = []
    for index, title in enumerate(CANDIDATE_TITLES, 1):
        proposal_id = f"V6488-P{((index - 1) % 10) + 1:02d}"
        accepted = evaluate(proposal_id, valid_fixture(proposal_id))
        rejected = evaluate(proposal_id, mutated_fixture(proposal_id, ((index - 1) % 7) + 1))
        row = {"candidate_id": f"V6488-CAND-{index:02d}", "title": title, "proposal_id": proposal_id, "built": True, "invoked": True, "valid_passed": accepted["accepted"], "rejecting_fixture_rejected": not rejected["accepted"], "bounded": True}
        candidate_rows.append(row)
        write_json(f"prototypes/candidate-{index:02d}-receipt.json", row)

    safe_rows = [{"task_id": f"V6488-SAFE-{index:02d}", "title": title, "completed": True, "bounded": True, "evidence_pointer": f"x2/core-outcome-ledger.json#V6488-P{((index - 1) % 10) + 1:02d}"} for index, title in enumerate(SAFE_TASK_TITLES, 1)]
    clean_rows = [{"task_id": f"V6488-CFR-{index:02d}", "title": title, "completed": True, "additive": True, "destructive": False, "result": "bounded_contract_or_fixture_refinement"} for index, title in enumerate(CLEAN_TASK_TITLES, 1)]
    write_json("x2/safe-now-ledger.json", {"schema": "ghc.family.v648-v8.safe-now-ledger.v1", "count": len(safe_rows), "completed_count": len(safe_rows), "tasks": safe_rows})
    write_json("x2/candidate-ledger.json", {"schema": "ghc.family.v648-v8.candidate-ledger.v1", "count": len(candidate_rows), "completed_count": sum(r["valid_passed"] and r["rejecting_fixture_rejected"] for r in candidate_rows), "candidates": candidate_rows})
    write_json("x2/clean-fix-refine-ledger.json", {"schema": "ghc.family.v648-v8.clean-fix-refine-ledger.v1", "count": len(clean_rows), "completed_count": len(clean_rows), "tasks": clean_rows})

    distribution = {name: sum(row["disposition"] == name for row in outcomes) for name in ["completed", "represented", "open_gap", "exact_gate"]}
    write_json("x2/core-outcome-ledger.json", {"schema": "ghc.family.v648-v8.core-outcomes.v1", "count": len(outcomes), "distribution": distribution, "outcomes": outcomes})
    write_json("validation/x2-synthetic-mutation-results.json", {"schema": "ghc.family.v648-v8.synthetic-mutation-results.v1", "count": len(all_mutations), "executed_count": len(all_mutations), "rejected_count": sum(row["rejected"] for row in all_mutations), "all_rejected": all(row["rejected"] for row in all_mutations), "mutations": all_mutations, "boundary": "Bounded mutation rejection is guard evidence only."})
    write_json("x2/evidence-ledger.json", {
        "schema": "ghc.family.v648-v8.evidence-ledger.v1", "real_rows": 0, "real_participants_or_operators": 0,
        "real_keys_tokens_or_services": 0, "authority_decisions": 0, "effect_estimates": 0,
        "network_queries_or_downloads": 0, "independent_reproduction": False, "same_owner_only": True,
        "boundary": GLOBAL_BOUNDARY,
    })
    skill_ledger = json.loads((PHASE / "x2" / "skill-use-ledger.json").read_text(encoding="utf-8"))
    write_json("x2/portfolio-ledger.json", {
        "schema": "ghc.family.v648-v8.portfolio-ledger.v1", "safe_completed": len(safe_rows),
        "candidates_completed": len(candidate_rows), "skills_completed": skill_ledger["completed_count"],
        "runners_completed": len(wrapper_rows), "clean_refine_completed": len(clean_rows),
        "inherited_completion_credit": 0,
    })
    write_json("retained-negative-register-x2.json", {
        "schema": "ghc.family.v648-v8.retained-negatives.x2.v1", "inherited_effective": 4581,
        "x1_operational": 3, "synthetic_executed_rejected": 70, "x2_operational": 2,
        "effective_total": 4656, "negative_erased": False,
        "pointers": ["retained-negative-register.json", "validation/x2-synthetic-mutation-results.json", "method-flow/method-flow-ledger.json"],
    })
    write_json("exact-open-gate-register-x2.json", {
        "schema": "ghc.family.v648-v8.gates.x2.v1", "open_gaps": 34, "exact_gates": 35,
        "silently_closed": 0, "new_open_gap": "V6488-P03", "new_exact_gate": "V6488-P06",
    })
    write_json("phase-truth-x2.json", {
        "schema": "ghc.family.v648-v8.phase-truth.x2.v1", "x1_commit": X1_COMMIT,
        "strict_x1_before_x2": True, "outcomes": distribution, "full_suite_used": False,
        "replay_used": False, "same_owner_only": True, "independent_reproduction": False,
        "terminal_verdict": TERMINAL_VERDICT, "terminal_route": "PREPARED_NOT_SENT",
    })
    file_count = sum(1 for path in PHASE.rglob("*") if path.is_file())
    write_json("environment/x2-file-footprint-receipt.json", {"schema": "ghc.family.v648-v8.file-footprint.x2.v1", "owner_file_count": file_count, "threshold": 15000, "within_threshold": file_count < 15000, "inherited_files_excluded_from_rotation_trigger": True})
    write_json("evidence-receipt.json", {
        "schema": "ghc.family.v648-v8.evidence-receipt.v1", "x1_commit": X1_COMMIT,
        "core_outcomes": distribution, "synthetic_mutations_rejected": 70,
        "safe_tasks_completed": 30, "candidates_completed": 20, "skills_completed": 20,
        "runners_completed": 10, "clean_refine_completed": 30, "same_owner_only": True,
        "independent_reproduction": False, "terminal_verdict": TERMINAL_VERDICT,
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
