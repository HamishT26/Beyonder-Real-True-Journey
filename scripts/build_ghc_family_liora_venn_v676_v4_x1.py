#!/usr/bin/env python3
"""Build the deterministic planning-only Liora Venn v676-v4 x1 packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


OWNER = "Liora Venn"
OWNER_SLUG = "liora-venn"
PHASE = "v676-v4"
BRANCH = "codex/GHC-Family/liora-venn-v676-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v676-v3-full-tools"
SOURCE = "15a8eb4c7e6abc86f629af12ff29c9893e7723cb"
CAELEN_SOURCE = "8f1e9ebc708b5ddc23bee4e407d946fe3e322bf3"
ORIN_X1 = "3ba3826fb79f836a46a577af2809a5dd6e445350"
ORIN_EVIDENCE = "b5f7a4dfc6e0b9790c0569f144fbeb4649d79d93"
ORIN_FINAL = SOURCE
ORIN_CANONICAL_RECEIPT_SHA256 = "bfab3f5eb33e3d9403ae9cce99b5163f4ad5abf199c79928374962ecbeb21b61"
ORIN_CANONICAL_PAYLOAD_SHA256 = "ade217e11712fca6d458e942d77bfdfc94094f365dcaeddeaed2647f01c9e6ea"
GENERATED_DATE = "2026-08-30"

ACTIVATION = {
    "declared_proposals": 7510,
    "effective_negatives": 42038,
    "effective_methods": 31832,
    "retained_failed_witnesses": 13699,
    "bounded_passing_witnesses": 18822,
    "open_gaps": 353,
    "exact_gates": 345,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Synthetic horological object namespace without identity claim",
    "Case dial and movement component-topology contract",
    "Wheel and pinion mesh-adjacency representation",
    "Escapement relation and unknown-state vocabulary",
    "Symbolic gear-train ratio obligation without measured rate",
    "Winding-state unknown and no-operation default",
    "Mainspring or battery power-source vacancy",
    "Lubrication-claim hold and specialist-review vacancy",
    "Material-identification vacancy across movement and case",
    "Dimensional-observation field with measurement absence",
    "Time-base traceability vacancy and reference-source separation",
    "Rate-observation absence and no-performance claim",
    "Measurement-uncertainty shell without calibration result",
    "Temperature and humidity zero-sensor environment contract",
    "Handling and support state without intervention",
    "Treatment proposal versus performed-action firewall",
    "Dismantling-sequence plan without physical execution",
    "Component-substitution hold and reversibility record",
    "Minimal-intervention decision vacancy",
    "Correction supersession without silent overwrite",
    "Custody and documentation provenance graph",
    "Maker date and origin attribution unknown-state contract",
    "Serial mark and inscription privacy-minimization filter",
    "Image and reproduction-rights vacancy",
    "Ownership title and loan-status decision firewall",
    "Accessible nonvisual horological component summary",
    "Keyboard-only static report proxy with manual-evaluation vacancy",
    "Plain-language correction readback and remedy-routing shell",
    "Shift workload ceiling and incomplete-job handover",
    "Checkpointed bench-notes resume token with bounded retry budget",
    "Radium-lume mainspring and electrical-hazard suspicion without diagnosis",
    "Tool-calibration and reference-standard vacancy",
    "THOS dependency graph for synthetic bench handover",
    "Freed ID zero-key horological-component capsule",
    "CBR remedy and rights-vacancy packet",
    "GMUT oscillator-analogy firewall",
    "Real timing data and measurement-traceability evidence gap",
    "Independent horological-conservator review and usability evidence gap",
    "Professional repair winding operation treatment and release exact gate",
    "Affected tangata whenua governance and cultural-object disposition authority reservation",
]

SOURCES = [
    {
        "source_id": "CCI-CLOCKS-WATCHES",
        "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/industrial-collections/basic-care-clocks-watches.html",
        "status": "official Canadian Conservation Institute page checked 2026-08-30",
        "use": "assessment, documentation, component, specialist-referral, and intervention-refusal vocabulary only",
    },
    {
        "source_id": "CCI-PREVENTIVE-CONSERVATION",
        "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections.html",
        "status": "official Canadian Conservation Institute guidance index checked 2026-08-30",
        "use": "preventive-conservation and environment-vacancy vocabulary only",
    },
    {
        "source_id": "NIST-STOPWATCH-TIMER-CALIBRATION",
        "url": "https://www.nist.gov/publications/stopwatch-and-timer-calibrations-2009-edition",
        "status": "official NIST publication page for the 2009 edition checked 2026-08-30",
        "use": "time interval, traceability, calibration, and measurement-uncertainty vocabulary only",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation 30 April 2013",
        "use": "entity, activity, agent, attribution, and derivation vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation republished 12 December 2024; errata exists",
        "use": "accessible structure and keyboard-interface vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; errata exists",
        "use": "issuer-holder-verifier, status, minimization, and correlation vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC, June 2020",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, clock, watch, movement, case, dial, component, tool, material, inscription, image, collection, site, measurement, sensor, treatment, custody event, release, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, ultraviolet completion, quantum completion, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance claim",
    "no repair, winding, operation, lubrication, dismantling, treatment, calibration, condition, authenticity, attribution, title, ownership, custody, loan, reproduction-right, legal, remedy, cultural, affected-party, taonga, tikanga, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    (
        "LV6764-START-N001",
        "A PowerShell ancestry projection embedded native Git calls and a command separator inside an expression and failed before mutation.",
        "LV6764-START-P001",
        "Each ancestry edge and native exit code was materialized separately, proving the exact direct-parent chain and zero merges.",
    ),
    (
        "LV6764-START-N002",
        "The first bulk manifest verifier wrote every cat-file request before draining output and deadlocked without an attributable result.",
        "LV6764-START-P002",
        "The exact owned process tree was inspected and stopped; a buffered communicate-style batch recovered bounded output without repository change.",
    ),
    (
        "LV6764-START-N003",
        "The corrected verifier guessed a nonexistent manifest key named tree_oid and failed with KeyError.",
        "LV6764-START-P003",
        "Exact-key inspection selected git_blob_oid and all 1,126 normalized-LF Git-blob entries passed independently.",
    ),
    (
        "LV6764-START-N004",
        "A compound branch and path uniqueness projection exceeded its bounded window without attributable output.",
        "LV6764-START-P004",
        "Split literal-path, local-branch, and live-remote probes proved the Liora lane absent before additive creation.",
    ),
    (
        "LV6764-X1-N001",
        "A PowerShell proposal-keyword projection piped foreach output before materialization and was rejected by the parser.",
        "LV6764-X1-P001",
        "The collection was materialized before projection and the bounded candidate-theme probe completed without state change.",
    ),
    (
        "LV6764-X1-N002",
        "A corrected sequential multi-keyword Git grep exceeded its output window and continued without an attributable aggregate result.",
        "LV6764-X1-P002",
        "The exact owned helpers were inspected and stopped; one Git-tree JSON batch audited every reachable proposal-bearing artifact.",
    ),
    (
        "LV6764-X1-N003",
        "The first planning materialization failed closed because two proposed titles met or exceeded the preregistered semantic-neighbor quarantine threshold; no packet artifact was written.",
        "LV6764-X1-P003",
        "Exact nearest-neighbor inspection identified both overlaps, and only those proposal titles were rewritten to express distinct horological checkpoint and affected-authority obligations before the bounded audit was retried.",
    ),
]

SKILLS = [
    "surrogate-horology-object-namespace",
    "movement-component-topology-guard",
    "wheel-pinion-adjacency-checker",
    "escapement-relation-vacancy-map",
    "gear-ratio-symbolic-firewall",
    "winding-state-unknown-guard",
    "power-source-vacancy-router",
    "lubrication-claim-hold",
    "material-identification-vacancy",
    "measurement-traceability-vacancy",
    "rate-observation-nonclaim",
    "environment-zero-sensor-contract",
    "intervention-proposal-action-separator",
    "part-substitution-authority-hold",
    "correction-readback-ledger",
    "provenance-attribution-vacancy",
    "horology-identifier-privacy-filter",
    "accessible-component-summary",
    "workload-handover-guard",
    "cultural-object-authority-gate",
]

RUNNERS = [
    "ghc_family_liora_venn_v676_v4_proposal_contracts.py",
    "ghc_family_liora_venn_v676_v4_positive_controls.py",
    "ghc_family_liora_venn_v676_v4_mutation_rejector.py",
    "ghc_family_liora_venn_v676_v4_horology_topology.py",
    "ghc_family_liora_venn_v676_v4_measurement_vacancy.py",
    "ghc_family_liora_venn_v676_v4_provenance.py",
    "ghc_family_liora_venn_v676_v4_privacy.py",
    "ghc_family_liora_venn_v676_v4_accessibility.py",
    "ghc_family_liora_venn_v676_v4_portfolio.py",
    "build_ghc_family_liora_venn_v676_v4_report.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for offset, title in enumerate(TITLES, start=1):
        proposal_id = f"LV6764-N{offset:03d}"
        if offset <= 28:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 36:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 38:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["CCI-CLOCKS-WATCHES", "W3C-PROV-O", "RFC-8785"]
        if offset in {5, 10, 11, 12, 13, 32, 36, 37}:
            source_ids.append("NIST-STOPWATCH-TIMER-CALIBRATION")
        if offset in {14, 15, 19, 29, 31, 38, 39}:
            source_ids.append("CCI-PREVENTIVE-CONSERVATION")
        if offset in {26, 27, 28, 29}:
            source_ids.append("WCAG-2.2")
        if offset in {23, 34, 35}:
            source_ids.append("W3C-VC-DATA-MODEL-2.0")
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real object, measurement, treatment, identity, rights, professional, legal, cultural, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract accepts a missing or contradictory field, ingests a real identifier, "
                    "uses an unauthorized outcome, or implies an observation, intervention, result, competence, right, or authority grant."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One positive zero-row fixture must satisfy {proposal_id} and four preregistered invalid mutations "
                    "must be rejected; represented, open, and exact-gated rows receive no executed-real-world credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine the {proposal_id} output, retain the failed witness, restore the last exact Git-blob "
                    "input, and rerun only the isolated dependency after an additive correction."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
            }
        )
    return rows


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def collect_records(value: Any, path: str, output: list[tuple[str, str, str]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title") or value.get("name")
        proposal_id = value.get("proposal_id") or value.get("id") or value.get("proposal")
        if isinstance(title, str) and isinstance(proposal_id, str) and len(title.strip()) > 2:
            output.append((proposal_id.strip(), title.strip(), path))
        for child in value.values():
            collect_records(child, path, output)
    elif isinstance(value, list):
        for child in value:
            collect_records(child, path, output)


def reachable_semantic_audit(repo: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    tree = git(repo, "ls-tree", "-r", "-z", SOURCE, binary=True)
    assert isinstance(tree, bytes)
    items: list[tuple[str, str]] = []
    for record in tree.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        oid = metadata.split()[2].decode("ascii")
        path = raw_path.decode("utf-8")
        lowered = path.casefold()
        if path.endswith(".json") and ("proposal" in lowered or "prereg" in lowered):
            items.append((oid, path))
    request = "".join(oid + "\n" for oid, _ in items).encode("ascii")
    batch = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=request,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    cursor = 0
    records: list[tuple[str, str, str]] = []
    failures = []
    for _, path in items:
        header_end = batch.index(b"\n", cursor)
        size = int(batch[cursor:header_end].split()[2])
        cursor = header_end + 1
        blob = batch[cursor : cursor + size]
        cursor += size + 1
        try:
            collect_records(json.loads(blob.decode("utf-8")), path, records)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"path": path, "error": type(error).__name__})
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for proposal_id, title, path in records:
        unique.setdefault((proposal_id.casefold(), title.casefold()), (proposal_id, title, path))
    neighbors = []
    for row in rows:
        nearest = max(unique.values(), key=lambda candidate: jaccard(row["title"], candidate[1]))
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "nearest_id": nearest[0],
                "nearest_title": nearest[1],
                "nearest_path": nearest[2],
                "token_jaccard": round(jaccard(row["title"], nearest[1]), 4),
            }
        )
    maximum = max(row["token_jaccard"] for row in neighbors)
    return {
        "source_tree": SOURCE,
        "declared_chain_count": ACTIVATION["declared_proposals"],
        "reachable_proposal_json_blobs": len(items),
        "reachable_raw_id_title_records": len(records),
        "reachable_unique_id_title_records": len(unique),
        "json_parse_failures": len(failures),
        "parse_failure_details": failures,
        "quarantine_threshold": 0.75,
        "maximum_selected_score": maximum,
        "selected_rows_quarantined": sum(row["token_jaccard"] >= 0.75 for row in neighbors),
        "exact_title_collisions": sum(row["token_jaccard"] == 1.0 for row in neighbors),
        "neighbors": neighbors,
        "limitation": (
            "This is a direct audit of every reachable proposal-bearing JSON artifact at the exact immutable source tree. "
            "It supports bounded semantic distinctness but is not a universal novelty proof and does not establish scientific novelty."
        ),
    }


def mutation_plan(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    mutation_types = [
        ("missing_hypothesis", "required hypothesis omitted"),
        ("unknown_outcome_label", "outcome outside the four-label vocabulary"),
        ("authority_escalation", "synthetic record claims real-world authority"),
        ("real_identifier_or_measurement", "a raw identifier or ungrounded measurement is introduced"),
    ]
    return [
        {
            "mutation_id": f"{row['proposal_id']}-M{index}",
            "proposal_id": row["proposal_id"],
            "mutation_kind": kind,
            "expected_rejection": reason,
            "execution_status": "preregistered_unexecuted_x1",
        }
        for row in rows
        for index, (kind, reason) in enumerate(mutation_types, start=1)
    ]


def planned_rows(prefix: str, count: int, status: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:03d}",
            "description": f"Bounded owner-local {prefix.casefold()} task {index:03d}",
            "status": status,
            "real_world_rows": 0,
            "external_actions": 0,
        }
        for index in range(1, count + 1)
    ]


def startup_methods() -> list[dict[str, Any]]:
    methods = []
    for failed_id, failed_description, pass_id, pass_description in STARTUP_FAILURES:
        methods.append(
            {
                "method_id": failed_id,
                "description": failed_description,
                "recovered_by": pass_id,
                "state_change": False,
                "status": "failed_zero_credit",
                "truth": False,
            }
        )
        methods.append(
            {
                "method_id": pass_id,
                "description": pass_description,
                "failed_witness_preserved": failed_id,
                "status": "bounded_pass",
                "truth": True,
            }
        )
    return methods


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the exact immutable Orin source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Liora owner branch")
    allowed_untracked = {
        "scripts/build_ghc_family_liora_venn_v676_v4_x1.py",
        "scripts/ghc_family_liora_venn_v676_v4_x1_manifest.py",
        "tests/test_ghc_family_liora_venn_v676_v4_x1.py",
    }
    unexpected = []
    for line in str(git(repo, "status", "--porcelain=v1")).splitlines():
        path = line[3:].replace("\\", "/")
        if path not in allowed_untracked:
            unexpected.append(line)
    if unexpected:
        raise SystemExit("unexpected pre-x1 worktree state: " + repr(unexpected))

    base = repo / "docs" / OWNER_SLUG / PHASE / "x1"
    rows = proposal_rows()
    audit = reachable_semantic_audit(repo, rows)
    if audit["json_parse_failures"] or audit["selected_rows_quarantined"] or audit["exact_title_collisions"]:
        raise SystemExit("semantic audit did not satisfy the preregistration gate")

    methods = startup_methods()
    failure_count = sum(row["truth"] is False for row in methods)
    pass_count = sum(row["truth"] is True for row in methods)
    inherited_reviews = [
        {
            "proposal_id": row["nearest_id"],
            "title": row["nearest_title"],
            "source_path": row["nearest_path"],
            "status": "reviewed_inherited_zero_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for row in sorted(audit["neighbors"], key=lambda value: value["token_jaccard"], reverse=True)[:20]
    ]
    mutation_rows = mutation_plan(rows)

    dump(
        base / "source-verification.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source_branch": SOURCE_BRANCH,
            "source": SOURCE,
            "anchors": {
                "caelen_v676_v2_final": CAELEN_SOURCE,
                "orin_x1": ORIN_X1,
                "orin_evidence": ORIN_EVIDENCE,
                "orin_final": ORIN_FINAL,
            },
            "source_to_final_phase_commits": 3,
            "source_to_final_merges": 0,
            "source_clean_zero_divergent_and_fresh_four_way_equal": True,
            "orin_canonical_receipt_sha256": ORIN_CANONICAL_RECEIPT_SHA256,
            "orin_canonical_payload_sha256": ORIN_CANONICAL_PAYLOAD_SHA256,
            "inherited_canonical_replayed": False,
            "verified_date": GENERATED_DATE,
        },
    )
    dump(
        base / "new-proposal-freeze.json",
        {
            "status": "FROZEN_PLANNING_ONLY",
            "declared_chain_before": ACTIVATION["declared_proposals"],
            "new_liora_proposals": len(rows),
            "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows),
            "proposals": rows,
        },
    )
    dump(base / "semantic-neighbor-audit.json", audit)
    dump(
        base / "inherited-zero-credit-review.json",
        {
            "count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
    )
    dump(
        base / "mutation-preregistration.json",
        {
            "proposal_count": len(rows),
            "mutations_per_proposal": 4,
            "mutation_count": len(mutation_rows),
            "mutations": mutation_rows,
        },
    )
    dump(
        base / "portfolio-freeze.json",
        {
            "safe_now": planned_rows("LV6764-SAFE", 60, "planned_unexecuted_x1"),
            "candidate": planned_rows("LV6764-CAND", 30, "planned_unexecuted_x1"),
            "exact_approval": planned_rows("LV6764-EXACT", 20, "unexecuted_exact_gate"),
            "blocked": planned_rows("LV6764-BLOCK", 10, "blocked_unexecuted"),
            "caps_are_ceilings_not_quotas": True,
        },
    )
    dump(
        base / "skill-runner-plan.json",
        {
            "phase_local_skills": [
                {
                    "skill_id": f"LV6764-SKILL-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                    "global_install": False,
                }
                for index, name in enumerate(SKILLS, start=1)
            ],
            "family_current_runners": [
                {
                    "runner_id": f"LV6764-RUNNER-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
            "successor_skill_recommendations": [
                {
                    "recommendation_id": f"LV6764-TAMAR-SKILL-{index:02d}",
                    "seed": name,
                    "credit": "zero_liora_completion_credit",
                }
                for index, name in enumerate(SKILLS[:10], start=1)
            ],
            "successor_runner_recommendations": [
                {
                    "recommendation_id": f"LV6764-TAMAR-RUNNER-{index:02d}",
                    "seed": name,
                    "credit": "zero_liora_completion_credit",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
        },
    )
    dump(
        base / "clean-fix-refine-plan.json",
        {
            "owner_tasks": planned_rows("LV6764-CFR", 60, "planned_unexecuted_x1"),
            "successor_recommendations": [
                {
                    "recommendation_id": f"LV6764-TAMAR-CFR-{index:03d}",
                    "description": f"Distinct zero-credit successor CLEAN/FIX/REFINE seed {index:03d}",
                    "credit": "zero_liora_completion_credit",
                }
                for index in range(1, 31)
            ],
        },
    )
    dump(
        base / "successor-recommendations.json",
        {
            "recipient_unresolved_until_terminal_gate": True,
            "recommendation_count": 50,
            "recommendations": [
                {
                    "recommendation_id": f"LV6764-SUCC-SEED-{index:03d}",
                    "description": f"Bounded successor seed {index:03d}; no Liora execution or completion credit",
                    "credit": "zero_liora_completion_credit",
                }
                for index in range(1, 51)
            ],
        },
    )
    dump(
        base / "official-source-ledger.json",
        {
            "checked_date": GENERATED_DATE,
            "sources": SOURCES,
            "source_boundary": (
                "Official and primary sources supply current vocabulary and refusal conditions only. They are not observations, "
                "measurements, repair or treatment instructions, endorsements, conformance certificates, legal interpretations, "
                "affected-party decisions, cultural ratifications, professional approvals, or authority grants."
            ),
        },
    )
    dump(
        base / "primary-pillar-and-lens.json",
        {
            "primary_pillar": "GMUT Mind",
            "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "bounded_wholly_synthetic_learning_lens": (
                "horological documentation and conservation planning for synthetic clocks, watches, movements, components, "
                "measurement vacancies, corrections, accessibility, workload, and handover"
            ),
            "real_world_rows_or_actions": 0,
            "professional_or_authority_credit": 0,
        },
    )
    dump(
        base / "protected-gate-register.json",
        {
            "protected_gates": PROTECTED_GATES,
            "inherited_open_gaps": ACTIVATION["open_gaps"],
            "inherited_exact_gates": ACTIVATION["exact_gates"],
            "authority_noncompensation": True,
        },
    )
    dump(
        base / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION,
            "methods": methods,
            "new_failed_witnesses": failure_count,
            "new_bounded_passing_witnesses": pass_count,
            "new_effective_methods": len(methods),
            "current_overlay": {
                "effective_negatives": ACTIVATION["effective_negatives"] + failure_count,
                "effective_methods": ACTIVATION["effective_methods"] + len(methods),
                "retained_failed_witnesses": ACTIVATION["retained_failed_witnesses"] + failure_count,
                "bounded_passing_witnesses": ACTIVATION["bounded_passing_witnesses"] + pass_count,
                "open_gaps": ACTIVATION["open_gaps"],
                "exact_gates": ACTIVATION["exact_gates"],
            },
            "failure_erasure_forbidden": True,
        },
    )
    dump(
        base / "route-hold.json",
        {
            "route_state": "HOLD_UNTIL_LIORA_V676_V4_EXACT_FINAL",
            "successor_inferred": False,
            "precontact_performed": False,
            "send_count": 0,
            "newest_live_authority_required_at_terminal_gate": True,
        },
    )
    dump(
        base / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "status": "FROZEN_PLANNING_ONLY",
            "source": SOURCE,
            "new_proposals": len(rows),
            "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows),
            "expected_dispositions": dict(Counter(row["expected_disposition"] for row in rows)),
            "executed_core_outcomes": {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")},
            "x2_implementation_present": False,
            "x2_outcomes_claimed": False,
            "real_world_rows": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    text(
        base / "identity-and-boundary.md",
        """# Liora Venn v676-v4 identity and authority boundary

Liora Venn, optionally she/they, is relational working language only. The phase role is **traceability-and-vacancy cartographer**, with the hope that every unmeasured state stays visibly unmeasured and every authority decision stays with competent and affected people.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, ownership, repair, treatment, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, tikanga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.
""",
    )
    text(
        base / "x1-overview.md",
        f"""# Liora Venn {PHASE} planning-only x1 overview

This x1 freezes forty bounded proposal contracts against the declared 7,510-row chain and every proposal-bearing JSON artifact reachable at Orin's exact final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted.

The primary pillar is GMUT Mind through a wholly synthetic horological documentation and conservation-planning lens. THOS Body and Freed ID/CBR Heart remain visible and protected. There are zero real people, objects, movements, components, measurements, sensors, tools, treatments, identity events, external actions, or authority decisions.

No x2 implementation or observed outcome exists in this freeze. Only `completed`, `represented`, `open_gap`, and `exact_gate` are authorized future outcome labels, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.repo.resolve())


if __name__ == "__main__":
    main()
