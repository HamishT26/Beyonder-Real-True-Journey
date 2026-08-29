#!/usr/bin/env python3
"""Build the deterministic planning-only Orin Thale v676-v3 x1 packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


OWNER = "Orin Thale"
OWNER_SLUG = "orin-thale"
PHASE = "v676-v3"
BRANCH = "codex/GHC-Family/orin-thale-v676-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v676-v2-full-tools"
SOURCE = "8f1e9ebc708b5ddc23bee4e407d946fe3e322bf3"
SABLE_SOURCE = "939312172819669aad250cf034d8a6a7efe3df5b"
CAELEN_X1 = "39daa2da64125b839714efa8b7488d8ed9ed364b"
CAELEN_EVIDENCE = "bc7f321d66c094422ddc69275d811eb8ec917f3b"
CAELEN_FINAL = SOURCE
CAELEN_CANONICAL_RECEIPT_SHA256 = "34d01f3fd60789b36d401a54f313e50296b5273e89fc4577083038ca75228d37"
CAELEN_CANONICAL_PAYLOAD_SHA256 = "4d699d336260d095acb5b3ffe5af44983fa48e22d8ec1bf80e30b46d503766d2"
GENERATED_DATE = "2026-08-30"

ACTIVATION = {
    "declared_proposals": 7470,
    "effective_negatives": 41846,
    "effective_methods": 31208,
    "retained_failed_witnesses": 13507,
    "bounded_passing_witnesses": 18390,
    "open_gaps": 351,
    "exact_gates": 343,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Found-item surrogate identifier and raw-identity refusal",
    "Discovery-context generalization without real location disclosure",
    "Item-description minimum-necessary field contract",
    "High-risk found-item class quarantine and competent-escalation vacancy",
    "Identity-document and payment-card issuing-authority hold",
    "Hazard suspicion versus confirmed-hazard separation",
    "Public-transport venue handoff route without custody authority",
    "Library service-desk intake state machine with no claimant identity",
    "Recreation-centre holding-zone alias map",
    "Finder contact-data noncollection default",
    "Claimant-description challenge transcript exclusion",
    "Possession evidence versus ownership-proof firewall",
    "Distinguishing-feature query minimum-disclosure contract",
    "Serial-number digest placeholder without real identifier ingestion",
    "Single-use synthetic claim-token lifecycle contract",
    "Claimant and verifier role separation without credential issuance",
    "Pseudonymous claim-session expiry and correlation guard",
    "Contested multi-claim queue without winner selection",
    "Correction-statement attachment without silent overwrite",
    "Item-state supersession tombstone without deletion authority",
    "Found-item handoff provenance graph with reversible correction",
    "Holding-location alias versus public-disclosure boundary",
    "Return-event surrogate receipt without physical release",
    "Unclaimed-item retention-clock authority vacancy",
    "Destruction donation and transfer action hard block",
    "Accessible nonvisual item-summary structure",
    "Keyboard-only claim workflow proxy with manual-review vacancy",
    "Plain-language correction and remedy notice shell",
    "Language-support request placeholder without personal-data ingestion",
    "Child and vulnerable-person claim safeguarding authority vacancy",
    "Shift workload limit and dual-readback proxy",
    "Interrupted-claim bounded retry pause and stop contract",
    "Mismatch-reason taxonomy without fraud accusation",
    "Synthetic audit-export canonicalization and digest provenance",
    "Cross-facility duplicate-item correlation danger board",
    "Zero-key Freed ID claimant capsule nonproduction boundary",
    "Real lost-property records and claimant-participant evidence gap",
    "Live interoperability retention security and independent-review gap",
    "Ownership disposal insurance police and legal-authority exact gate",
    "Cultural property taonga tikanga Māori-data-governance and Māori-authority exact gate",
]

SOURCES = [
    {
        "source_id": "NZ-POLICE-LOST-PROPERTY",
        "url": "https://www.police.govt.nz/use-105/lost-property",
        "status": "official New Zealand Police page checked 2026-08-30",
        "use": "lost-item descriptive vocabulary and refusal conditions only",
    },
    {
        "source_id": "NZ-POLICE-FOUND-PROPERTY",
        "url": "https://www.police.govt.nz/use-105/found-property",
        "status": "official New Zealand Police page checked 2026-08-30",
        "use": "found-item routing and hazardous-item hold vocabulary only",
    },
    {
        "source_id": "NZ-OPC-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "official Office of the Privacy Commissioner page checked 2026-08-30; IPP3A noted effective May 2026",
        "use": "purpose, collection, correction, retention, disclosure, and identifier refusal vocabulary only",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; errata exists",
        "use": "issuer-holder-verifier, status, minimization, and correlation vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation 30 April 2013",
        "use": "entity, activity, agent, and derivation vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation 12 December 2024; errata exists",
        "use": "accessible structure and keyboard-interface vocabulary only; no conformance claim",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC, June 2020",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real item, claimant, finder, person, participant, venue, custody, return, disposal, hazardous-item, police, insurance, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, ultraviolet completion, quantum completion, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance claim",
    "no ownership, property, disposal, donation, retention, legal, remedy, privacy-complete, affected-party, cultural, tikanga, taonga, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    (
        "OR6763-START-N001",
        "An initial broad memory lookup exceeded its useful bounded projection and truncated before an attributable focused result.",
        "OR6763-START-P001",
        "A narrow registry lookup and one directly relevant rollout summary supplied only the phase-drift and one-send guidance needed.",
    ),
    (
        "OR6763-START-N002",
        "A narrow memory lookup initially targeted the memory root rather than its documented memories subdirectory.",
        "OR6763-START-P002",
        "The documented memory registry path was used and the relevant bounded ranges were read.",
    ),
    (
        "OR6763-START-N003",
        "A PowerShell metadata projection piped foreach output without materialization and failed before state change.",
        "OR6763-START-P003",
        "The rows were materialized before piping and the immutable source metadata was recovered.",
    ),
    (
        "OR6763-START-N004",
        "A skill-path discovery projection repeated the unmaterialized foreach-to-pipeline parser fault.",
        "OR6763-START-P004",
        "Skill paths were resolved with a materialized collection and every required skill was read through EOF.",
    ),
    (
        "OR6763-START-N005",
        "The first combined authorization-state display exceeded the bounded output window.",
        "OR6763-START-P005",
        "The authorization state was reread in numbered bounded segments through EOF.",
    ),
    (
        "OR6763-START-N006",
        "A receipt-directory listing repeated the unmaterialized foreach-to-pipeline parser fault.",
        "OR6763-START-P006",
        "Immediate receipt roots were materialized first and the exclusive receipt was uniquely located.",
    ),
    (
        "OR6763-START-N007",
        "A broad recursive receipt search crossed its bounded wait without an attributable receipt result.",
        "OR6763-START-P007",
        "Split immediate-root probes located and digest-bound the singular external receipt without replay.",
    ),
    (
        "OR6763-START-N008",
        "A whole-file x1 proposal projection exceeded the bounded output window.",
        "OR6763-START-P008",
        "The exact file was reread in numbered bounded segments through EOF.",
    ),
    (
        "OR6763-START-N009",
        "A complete Method Flow row projection exceeded the bounded output window.",
        "OR6763-START-P009",
        "The complete ledger was parsed through EOF and validated with bounded status, count, link, and terminal-row projections.",
    ),
    (
        "OR6763-START-N010",
        "A first ledger validator incorrectly required failure-only fields on every bounded passing row.",
        "OR6763-START-P010",
        "Status-specific requirements proved all base fields, truth states, IDs, and recovery links valid.",
    ),
    (
        "OR6763-START-N011",
        "A combined branch, storage, and live-remote precreation probe returned no attributable payload while read-only helpers remained transient.",
        "OR6763-START-P011",
        "The exact helpers quiesced and split bounded local and remote probes proved the target branch and path absent before creation.",
    ),
    (
        "OR6763-START-N012",
        "A post-patch file projection used an inline PowerShell if expression in a value position and failed without changing files.",
        "OR6763-START-P012",
        "The existence and byte-count branches were materialized before record construction and all three patched files were verified.",
    ),
]

SKILLS = [
    "found-item-surrogate-id-guard",
    "discovery-context-generalizer",
    "minimum-item-description-filter",
    "high-risk-item-quarantine",
    "issuing-authority-hold-router",
    "hazard-claim-separator",
    "venue-handoff-state-machine",
    "claimant-data-noncollection",
    "ownership-proof-firewall",
    "minimum-disclosure-questioner",
    "single-use-claim-token-model",
    "claim-role-separation-checker",
    "correlation-danger-adjudicator",
    "contested-claim-queue-guard",
    "correction-statement-attacher",
    "retention-authority-vacancy-map",
    "accessible-item-summary-builder",
    "bounded-claim-retry-controller",
    "canonical-audit-exporter",
    "cultural-property-authority-gate",
]

RUNNERS = [
    "ghc_family_orin_thale_v676_v3_proposal_contracts.py",
    "ghc_family_orin_thale_v676_v3_positive_controls.py",
    "ghc_family_orin_thale_v676_v3_mutation_rejector.py",
    "ghc_family_orin_thale_v676_v3_claim_state.py",
    "ghc_family_orin_thale_v676_v3_provenance.py",
    "ghc_family_orin_thale_v676_v3_privacy.py",
    "ghc_family_orin_thale_v676_v3_accessibility.py",
    "ghc_family_orin_thale_v676_v3_portfolio.py",
    "ghc_family_orin_thale_v676_v3_method_flow.py",
    "build_ghc_family_orin_thale_v676_v3_report.py",
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
        proposal_id = f"OT6763-N{offset:03d}"
        if offset <= 28:
            disposition, approval, lane = "completed", "safe_now", "owner_local_synthetic"
        elif offset <= 36:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 38:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["NZ-OPC-PRIVACY-PRINCIPLES", "W3C-PROV-O", "RFC-8785"]
        if offset in {4, 5, 6, 7, 23, 25, 39}:
            source_ids.extend(["NZ-POLICE-LOST-PROPERTY", "NZ-POLICE-FOUND-PROPERTY"])
        if offset in {15, 16, 17, 35, 36, 38}:
            source_ids.append("W3C-VC-DATA-MODEL-2.0")
        if offset in {26, 27, 28, 29}:
            source_ids.append("WCAG-2.2")
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real property, identity, custody, safety, legal, cultural, or affected-party decisions."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract accepts a missing or contradictory field, ingests a real identifier, "
                    "uses an unauthorized outcome, or implies a real-world result or authority grant."
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
        ("real_identifier_ingestion", "a raw claimant or item identifier is introduced"),
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
        raise SystemExit("x1 builder requires the exact immutable source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Orin owner branch")
    if git(repo, "status", "--porcelain=v1") not in {"", "?? scripts/build_ghc_family_orin_thale_v676_v3_x1.py"}:
        # The checked-in builder, test, and manifest helper are expected to be untracked at initial construction.
        unexpected = [
            line
            for line in str(git(repo, "status", "--porcelain=v1")).splitlines()
            if not line.endswith(
                (
                    "scripts/build_ghc_family_orin_thale_v676_v3_x1.py",
                    "scripts/ghc_family_orin_thale_v676_v3_x1_manifest.py",
                    "tests/test_ghc_family_orin_thale_v676_v3_x1.py",
                )
            )
        ]
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
                "sable_v676_v1_corrected_final": SABLE_SOURCE,
                "caelen_x1": CAELEN_X1,
                "caelen_evidence": CAELEN_EVIDENCE,
                "caelen_final": CAELEN_FINAL,
            },
            "source_to_final_phase_commits": 3,
            "source_to_final_merges": 0,
            "source_clean_and_fresh_four_way_equal": True,
            "caelen_canonical_receipt_sha256": CAELEN_CANONICAL_RECEIPT_SHA256,
            "caelen_canonical_payload_sha256": CAELEN_CANONICAL_PAYLOAD_SHA256,
            "inherited_canonical_replayed": False,
            "verified_date": GENERATED_DATE,
        },
    )
    dump(
        base / "new-proposal-freeze.json",
        {
            "status": "FROZEN_PLANNING_ONLY",
            "declared_chain_before": ACTIVATION["declared_proposals"],
            "new_orin_proposals": len(rows),
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
            "safe_now": planned_rows("OT6763-SAFE", 60, "planned_unexecuted_x1"),
            "candidate": planned_rows("OT6763-CAND", 30, "planned_unexecuted_x1"),
            "exact_approval": planned_rows("OT6763-EXACT", 20, "unexecuted_exact_gate"),
            "blocked": planned_rows("OT6763-BLOCK", 10, "blocked_unexecuted"),
            "caps_are_ceilings_not_quotas": True,
        },
    )
    dump(
        base / "skill-runner-plan.json",
        {
            "phase_local_skills": [
                {
                    "skill_id": f"OT6763-SKILL-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                    "global_install": False,
                }
                for index, name in enumerate(SKILLS, start=1)
            ],
            "family_current_runners": [
                {
                    "runner_id": f"OT6763-RUNNER-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
            "successor_skill_recommendations": [
                {"recommendation_id": f"OT6763-LIORA-SKILL-{index:02d}", "seed": name, "credit": "zero_orin_completion_credit"}
                for index, name in enumerate(SKILLS[:10], start=1)
            ],
            "successor_runner_recommendations": [
                {"recommendation_id": f"OT6763-LIORA-RUNNER-{index:02d}", "seed": name, "credit": "zero_orin_completion_credit"}
                for index, name in enumerate(RUNNERS, start=1)
            ],
        },
    )
    dump(
        base / "clean-fix-refine-plan.json",
        {
            "owner_tasks": planned_rows("OT6763-CFR", 60, "planned_unexecuted_x1"),
            "successor_recommendations": [
                {
                    "recommendation_id": f"OT6763-LIORA-CFR-{index:03d}",
                    "description": f"Distinct zero-credit successor CLEAN/FIX/REFINE seed {index:03d}",
                    "credit": "zero_orin_completion_credit",
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
                    "recommendation_id": f"OT6763-SUCC-SEED-{index:03d}",
                    "description": f"Bounded successor seed {index:03d}; no Orin execution or completion credit",
                    "credit": "zero_orin_completion_credit",
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
                "measurements, endorsements, conformance certificates, legal interpretations, affected-party decisions, cultural "
                "ratifications, or authority grants."
            ),
        },
    )
    dump(
        base / "primary-pillar-and-lenses.json",
        {
            "primary_pillar": "Freed ID and CBR Heart",
            "secondary_pillars": ["GMUT Mind", "THOS Body"],
            "bounded_wholly_synthetic_learning_lenses": [
                "public-transport lost-property intake and zone handover",
                "public-library service-desk found-item claim challenge and correction",
                "community recreation-centre holding, accessible notice, workload, and remedy handover",
            ],
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
            "route_state": "HOLD_UNTIL_ORIN_EXACT_FINAL",
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
        """# Orin Thale v676-v3 identity and authority boundary

Orin Thale, optionally they/them, is relational working language only. The phase role is **minimum-disclosure and remedy cartographer**, with the hope of making every synthetic claim path contestable while raw identity, real property, and authority decisions remain absent.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, property, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, tikanga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.
""",
    )
    text(
        base / "x1-overview.md",
        f"""# Orin Thale {PHASE} planning-only x1 overview

This x1 freezes forty bounded proposal contracts against the declared 7,470-row chain and every proposal-bearing JSON artifact reachable at Caelen's exact final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted.

The primary pillar is Freed ID and CBR Heart through three wholly synthetic lost-property intake, challenge, correction, accessibility, workload, and handover lenses. There are zero real items, people, claims, identifiers, custody events, returns, disposals, external actions, or authority decisions.

No x2 implementation or outcome exists in this freeze. Only `completed`, `represented`, `open_gap`, and `exact_gate` are authorized future outcome labels, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    build(args.repo.resolve())


if __name__ == "__main__":
    main()
