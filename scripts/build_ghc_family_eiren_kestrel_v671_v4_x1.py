"""Build the planning-only Eiren Kestrel v671-v4 x1 packet.

This builder is intentionally limited to the current owner delta.  It does not
execute x2 proposals, replay Caelen's successful canonical aggregate, mutate a
sibling lane, contact a successor, or claim independent reproduction.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "eiren-kestrel" / "v671-v4"
OWNER = "Eiren Kestrel"
PHASE = "v671-v4"
BRANCH = "codex/GHC-Family/eiren-kestrel-v671-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v671-v3-full-tools"
SOURCE_START = "33b7c2d6b9f79f931ff98c478f136dab823c4d69"
SOURCE_X1 = "2551c126776ea0538354a32b90414f31f5cec4b3"
SOURCE_EVIDENCE = "46c41e84871edd72544ddad16f038902ec2386f5"
SOURCE_FINAL = "37ac80c499d43a90c874876402b262a220a252a1"
ACTIVATION_PATH = (
    "docs/caelen-morrow/v671-v3/handoffs/"
    "eiren-kestrel-v671-v4-activation-candidate.md"
)
ACTIVATION_SHA256 = (
    "bcbf2d7f4d9adc70bf8e64c75766947a54bafd4c293f0a641f9c46149f7aa909"
)
SOURCE_CANONICAL_SHA256 = (
    "1f0ac9dac336d699e7853b043b3c91aa49a9acadac8f99bc3dbabdbe76d093dd"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "270fad0c203fcf651d4d9ab95916e0bb41733faf0c77d469cc6888826aedf967"
)
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}

IDENTITY_BOUNDARY = (
    "Eiren Kestrel, they/them, seed-lineage cartographer and consent-vacancy "
    "steward, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "professional, operational, legal, cultural, affected-party, or Maori "
    "authority."
)
HOPE = (
    "keep every synthetic accession traceable, challengeable, reversible, and "
    "visibly short of real-world custodianship or authority"
)
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or "
    "composite evidence is not empirical confirmation, participant evidence, "
    "professional or scientific authority, production readiness, legal or "
    "cultural ratification, Maori authority, affected-party approval, complete "
    "privacy or accessibility assurance, exhaustive security, independent "
    "reproduction, AGI or ASI evidence, consciousness or personhood evidence, "
    "Theory-of-Everything proof, proof or canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "effective_negatives": 33905,
    "effective_methods": 20222,
    "failed_witnesses": 5726,
    "bounded_passing_witnesses": 7333,
    "open_gaps": 261,
    "exact_gates": 256,
    "proposal_chain": 5670,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "external_zero_credit_failures": 0,
    "external_bounded_recoveries": 0,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    {
        "signature": "reference-inventory-direct-foreach-to-pipe-parser-fault",
        "observation": "A read-only PowerShell reference projection placed a foreach statement directly before a pipe and stopped with an empty-pipe parser error.",
        "recovery": "Retain the parser fault, materialize the projection into an array, and pipe only the completed collection.",
    },
    {
        "signature": "phase-script-inventory-filter-matched-the-versioned-root-and-overproduced",
        "observation": "The first bounded script inventory searched the whole source worktree for the phase token, which also matched the worktree root and returned a needlessly oversized presentation.",
        "recovery": "Retain the overbroad projection and restrict the next inventory to the exact scripts and tests directories plus owner-specific filenames.",
    },
    {
        "signature": "source-receipt-lookup-assumed-a-nested-owner-phase-layout",
        "observation": "The first receipt lookup used a plausible nested owner and phase directory that did not exist.",
        "recovery": "Retain the absent-path probe and inventory only the exact receipts root before selecting the observed owner-phase directory.",
    },
    {
        "signature": "broad-archive-digest-search-exceeded-the-bounded-window",
        "observation": "A read-only digest search across the complete D-drive archive exceeded its bounded presentation window before locating the source receipt.",
        "recovery": "Interrupt the broad search once, retain it at zero credit, enumerate top-level receipt directories, and hash only the exact observed source receipt.",
    },
    {
        "signature": "sparse-worktree-command-outlived-its-initial-presentation-window",
        "observation": "The sparse no-checkout worktree command yielded a live session after its initial thirty-second window while Git was still completing the exact checkout.",
        "recovery": "Do not replay the worktree add; resume the same session and verify exact head, branch, sparse patterns, clean state, and zero materialized source files.",
    },
    {
        "signature": "source-canonical-receipt-was-an-atomic-wrapper-not-a-flat-payload",
        "observation": "The first x1 build stopped before artifact creation because the source verifier projected result, replay, invocation, and payload-digest fields from the outer atomic receipt instead of its payload object.",
        "recovery": "Retain the stopped build at zero credit, inspect only exact receipt keys and types, unwrap payload for validation fields, preserve the outer-byte digest, and rerun the never-completed x1 build.",
    },
    {
        "signature": "first-collision-free-title-slate-remained-structurally-derivative-on-manual-neighbor-review",
        "observation": "The first complete semantic audit stayed below the 0.72 token threshold, but manual review found twelve generic lineage, interruption, status, correction, workload, THOS, Freed-ID, and GMUT structures too close in meaning to inherited neighbors for a responsible novelty freeze.",
        "recovery": "Retain the first slate at zero novelty credit, replace only the twelve structurally derivative concepts with different falsifiable structures, and rerun the complete forty-title audit before staging.",
    },
    {
        "signature": "manual-corpus-projection-assumed-a-titles-key-in-the-summary-object",
        "observation": "A read-only post-audit review assigned the corpus summary to the title-list variable and raised KeyError when it projected a nonexistent titles key after the underlying audit had returned.",
        "recovery": "Retain the projection fault, inspect the exact function return shape, and use the committed nearest-neighbour rows without replaying the already-successful corpus audit.",
    },
]

NEW_TITLES = [
    "accession namespace conflict certificate combining prefix grammar checksum class local-global scope and non-identity disclaimer",
    "depositor source and acquisition-claim lattice with consent ownership and custodianship vacancies",
    "aliquot conservation algebra reconciling packet partitions through quantity intervals provenance cuts and noncommutative recombination refusal",
    "packet container closure label seal shelf and location relation board without storage-suitability inference",
    "taxonomic assertion ledger separating supplied name accepted name identifier confidence and competent-review vacancy",
    "Darwin Core material-entity material-sample occurrence and identification mapping with ambiguity quarantine",
    "bitemporal accession passport retaining superseded provenance date place and source assertions",
    "count mass moisture viability germination and purity vacancy ledger with units and calibration abstention",
    "storage zone cabinet shelf tray packet and duplicate-location topology without environmental assurance",
    "donation deposit exchange loan distribution and return-event distinction from ownership or benefit-sharing decision",
    "regeneration bottleneck storyboard with population-size isolation pollination and diversity-loss vacancies but no genetic verdict",
    "germination protocol placeholder with replicate count substrate duration temperature and observation vacancies",
    "quarantine pest pathogen weed phytosanitary and biosafety signal taxonomy without diagnosis or release",
    "orthodox intermediate recalcitrant and unknown storage-behaviour assertion firewall without species conclusion",
    "drying temperature humidity moisture and storage-envelope declaration with zero sensor rows",
    "viability-monitoring event structure separating protocol schedule result interpretation and action authority",
    "characterization evaluation observation measurement and breeding-value claim separation matrix",
    "label-transcription uncertainty capsule separating visible tokens inferred tokens withheld imagery and rights-review vacancies",
    "surrogate depositor curator technician taxonomist grower and recipient capability-vacancy profile",
    "sensitive taxon location traditional-knowledge and community-source disclosure budget with purpose-bound refusal",
    "accession-entry resumption cone with predecessor watermark field commit fence abandoned-draft quarantine and no executable content",
    "structural landmark crosswalk for accession lot packet assertion and hold regions with linear-print fallback and evaluation reservation",
    "language-scope matrix for vernacular scientific and supplied names with translation and naming-authority vacancies",
    "triangular contradiction card linking source assertion challenger claim and neutral hold without winner truth or authority inference",
    "three-bin unresolved-work saturation gauge using fixed counters escalation boundary and next-session acceptance without fatigue inference",
    "append-only accession lot sample event assertion and correction graph with reversible provenance",
    "claim-edge matrix for custody ownership authorship source community rights access benefit sharing and contest",
    "seed-depletion account with expected quantity interval non-negativity invariant discrepancy quarantine and irreversible-act gate",
    "THOS provenance-repair microcycle proxy binding error class minimal patch rollback receipt and zero-participant effectiveness",
    "THOS accession dependency DAG separating custodial taxonomic biosafety disclosure and accessibility blocks without priority evidence",
    "Freed ID zero-key purpose-bounded capability envelope with subjectless claim slots minimization state and lifecycle abstention",
    "Darwin Core seed-record profile isolated from taxonomic correctness material authenticity and conservation claims",
    "CBR notice contest correction and remedy transition table for synthetic seed records with no enacted right",
    "CBR pseudonymous depositor curator recipient and community-source privacy and redress representation",
    "GMUT latent-dormancy order-parameter chart with symmetry unit covariance and zero-fit obligations",
    "GMUT symbolic storage-microenvironment compartment graph with coupling placeholders and biological-prediction refusal",
    "FAO genebank and Darwin Core zero-row vocabulary adapter with zero calls downloads samples and rights decisions",
    "real authenticated seed plant accession measurement germination and independent-review evidence gap",
    "real depositor curator grower community seed guardian and affected-user evaluation gate",
    "competent biosafety phytosanitary conservation ownership benefit-sharing legal cultural and Maori-authority gate",
]

SKILLS = [
    "ghc-family-seed-accession-identity",
    "ghc-family-seed-lot-lineage",
    "ghc-family-seed-packet-topology",
    "ghc-family-seed-taxonomy-vacancy",
    "ghc-family-seed-measurement-vacancy",
    "ghc-family-seed-event-claim-split",
    "ghc-family-seed-biosafety-abstention",
    "ghc-family-seed-sensitive-data-quarantine",
    "ghc-family-seed-accessible-status",
    "ghc-family-seed-correction-handover",
    "ghc-family-seed-rights-vacancy",
    "ghc-family-seed-language-authority-hold",
    "ghc-family-seed-role-capability-abstention",
    "ghc-family-seed-viability-nonclaim",
    "ghc-family-seed-workload-envelope",
    "ghc-family-seed-source-adapter-hold",
    "ghc-family-seed-gmut-nonconversion",
    "ghc-family-seed-thos-proxy-boundary",
    "ghc-family-seed-cbr-remedy-vacancy",
    "ghc-family-seed-stage20-nonadmission",
]

RUNNERS = [
    "ghc_family_seed_accession_identity.py",
    "ghc_family_seed_lot_lineage.py",
    "ghc_family_seed_packet_topology.py",
    "ghc_family_seed_taxonomy_vacancy.py",
    "ghc_family_seed_measurement_vacancy.py",
    "ghc_family_seed_biosafety_abstention.py",
    "ghc_family_seed_sensitive_data_quarantine.py",
    "ghc_family_seed_correction_handover.py",
    "ghc_family_seed_rights_vacancy.py",
    "ghc_family_seed_accessible_status.py",
]

EXACT = [
    "real seed plant accession packet sample collection location donor record or custodian mutation",
    "real germination viability purity health diagnosis conservation propagation distribution or disposal decision",
    "real count mass moisture temperature humidity viability purity or calibration measurement",
    "real depositor curator technician taxonomist grower recipient participant or affected-user study",
    "real sensitive taxon location traditional-knowledge access account transaction or personal-data processing",
    "real identity key proof credential issuance presentation status or revocation",
    "real seed exchange sale distribution return benefit-sharing service or recipient decision",
    "real accessibility remedy service allocation complaint appeal or acceptance decision",
    "legal interpretation ownership access benefit sharing liability privacy right remedy or public authority",
    "taonga tikanga matauranga seed knowledge place-name data-governance or Maori-authority decision",
    "cultural ratification community mandate or affected-party acceptance",
    "production deployment external API write live feed publication or cloud mutation",
    "host elevation security weakening feature enablement Sandbox Hyper-V or reboot",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "privacy-complete exhaustive-security or production-security certification",
    "complete accessibility-conformance or affected-user acceptance declaration",
    "independent-reproduction external-audit or professional-validation declaration",
    "empirical GMUT datum likelihood posterior parameter force biological-law or prediction claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "Stage 20 admission or protected-gate closure",
]

BLOCKED = [
    "raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts",
    "sibling branch reset merge rewrite deletion reuse or force push",
    "successful canonical replay or failed-canonical success laundering",
    "synthetic fixture promotion into empirical professional legal cultural or conservation evidence",
    "unapproved account secret payment deployment plugin install or third-party write",
    "real depositor custodian grower recipient identity location accession or service data ingestion",
    "real biosafety phytosanitary legal cultural Maori-authority affected-party or public-authority substitution",
    "unsafe elevation host-security weakening feature enablement or reboot",
    "unbounded full-repository unchanged-history or cross-lane validation scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=False, timeout=180
    )
    if check and result.returncode != 0:
        raise SystemExit(
            f"git {' '.join(args)} failed: "
            f"{result.stderr.decode('utf-8', errors='replace')}"
        )
    return result


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalized_tokens(title: str) -> set[str]:
    stop = {"and", "the", "with", "for", "from", "without", "into"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title.lower())
        if len(token) > 2 and token not in stop
    }


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=180
    )
    if process.returncode != 0:
        raise SystemExit(
            "git cat-file --batch failed: "
            + stderr.decode("utf-8", errors="replace")
        )
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        rows.append(stream.read(size))
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return rows


def accessible_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    rows = git_text("rev-list", "--objects", "--all").splitlines()
    candidates: dict[str, str] = {}
    for row in rows:
        parts = row.split(" ", 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        lowered = path.lower()
        if lowered.endswith(".json") and "proposal" in lowered:
            candidates.setdefault(oid, path)

    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0
    bom_recoveries = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id = node.get("proposal_id")
            title = node.get("title")
            if (
                isinstance(proposal_id, str)
                and isinstance(title, str)
                and proposal_id.strip()
                and title.strip()
            ):
                occurrences += 1
                proposal_ids.add(proposal_id.strip())
                titles.add(title.strip())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    oids = sorted(candidates)
    for start in range(0, len(oids), 128):
        chunk = oids[start : start + 128]
        for blob in batch_blobs(chunk):
            if blob is None:
                malformed += 1
                continue
            try:
                if blob.startswith(b"\xef\xbb\xbf"):
                    bom_recoveries += 1
                walk(json.loads(blob.decode("utf-8-sig")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed += 1

    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    summary = {
        "scope": (
            "proposal-named JSON blobs reachable through local and remote refs "
            "only; no sibling worktree access and no general repository, "
            "unchanged-history, security, privacy, or test scan"
        ),
        "candidate_unique_git_blobs": len(oids),
        "malformed_or_missing_blobs": malformed,
        "isolated_utf8_bom_recoveries": bom_recoveries,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": sha256(canonical),
        "declared_source_chain": 5670,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "practice_term_hits": {
            term: sum(1 for title in titles if term in title.lower())
            for term in ("seed library", "accession", "germination")
        },
        "reason": (
            "Accessible proposal objects contain duplicate, summary, and "
            "variant rows and do not prove one canonical row-to-title mapping "
            "for the declared 5,630-row chain."
        ),
    }
    return summary, sorted(titles)


def source_verification(receipt_path: Path) -> dict[str, Any]:
    current_head = git_text("rev-parse", "HEAD")
    current_branch = git_text("symbolic-ref", "--short", "HEAD")
    local_source = git_text("rev-parse", SOURCE_FINAL)
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_line = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}")
    fresh_live = live_line.split("\t", 1)[0] if live_line else ""
    parent_rows = {
        "x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"),
        "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"),
        "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^"),
    }
    phase_commits = int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}"))
    merge_commits = int(
        git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")
    )
    activation = git("show", f"{SOURCE_FINAL}:{ACTIVATION_PATH}").stdout
    receipt_bytes = receipt_path.read_bytes()
    receipt_wrapper = json.loads(receipt_bytes.decode("utf-8"))
    receipt = receipt_wrapper.get("payload", receipt_wrapper)

    manifest_paths = [
        "docs/caelen-morrow/v671-v3/validation/x1-manifest.json",
        "docs/caelen-morrow/v671-v3/validation/evidence-manifest.json",
        "docs/caelen-morrow/v671-v3/validation/final-owner-manifest.json",
        "docs/caelen-morrow/v671-v3/validation/final-delta-manifest.json",
    ]
    manifest_metadata = []
    for path in manifest_paths:
        payload = json.loads(
            git("show", f"{SOURCE_FINAL}:{path}").stdout.decode("utf-8")
        )
        manifest_metadata.append(
            {
                "path": path,
                "entry_count": payload["entry_count"],
                "observed_rows": len(payload["entries"]),
                "hash_domain": payload["hash_domain"],
                "replayed": False,
            }
        )

    checks = {
        "current_branch": current_branch == BRANCH,
        "current_head_is_source_final": current_head == SOURCE_FINAL,
        "source_ref_exact": local_source == SOURCE_FINAL,
        "source_tracking_exact": tracking == SOURCE_FINAL,
        "source_fresh_live_exact": fresh_live == SOURCE_FINAL,
        "direct_parent_chain": parent_rows
        == {
            "x1_parent": SOURCE_START,
            "evidence_parent": SOURCE_X1,
            "final_parent": SOURCE_EVIDENCE,
        },
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merge_commits == 0,
        "activation_integrity": sha256(activation) == ACTIVATION_SHA256,
        "receipt_integrity": sha256(receipt_bytes) == SOURCE_CANONICAL_SHA256,
        "receipt_payload_integrity": (
            receipt_wrapper.get("payload_sha256")
            == SOURCE_CANONICAL_PAYLOAD_SHA256
        ),
        "source_canonical_success_not_replayed": (
            receipt.get("result") == "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
            and receipt.get("invocation_count") == 1
            and receipt.get("replayed") is False
        ),
        "manifest_metadata_exact": all(
            row["entry_count"] == row["observed_rows"] for row in manifest_metadata
        ),
    }
    if not all(checks.values()):
        raise SystemExit(
            "source verification failed: "
            + json.dumps({k: v for k, v in checks.items() if not v}, sort_keys=True)
        )
    return {
        "source_branch": SOURCE_BRANCH,
        "source_final": SOURCE_FINAL,
        "current_eiren_branch": current_branch,
        "current_head": current_head,
        "tracking": tracking,
        "fresh_live": fresh_live,
        "parent_chain": parent_rows,
        "phase_commits": phase_commits,
        "merge_commits": merge_commits,
        "activation_packet": {
            "path": ACTIVATION_PATH,
            "bytes": len(activation),
            "words": len(activation.decode("utf-8").split()),
            "sha256": sha256(activation),
            "historical_prepared_not_sent_preserved": True,
        },
        "canonical_receipt": {
            "sha256": sha256(receipt_bytes),
            "payload_sha256": receipt_wrapper["payload_sha256"],
            "result": receipt["result"],
            "invocation_count": receipt["invocation_count"],
            "replayed": receipt["replayed"],
            "source_validation_credit": 0,
        },
        "manifest_metadata": manifest_metadata,
        "source_manifests_replayed": 0,
        "source_canonical_replayed": False,
        "pre_mutation_read_gate": {
            "clean": True,
            "divergence": [0, 0],
            "four_way_equal": True,
            "evidence_basis": "attributable read-only terminal probes before owned worktree creation",
        },
        "checks": checks,
    }


def proposal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    gates = [
        "empirical",
        "participant",
        "professional",
        "production",
        "legal",
        "cultural",
        "Maori_authority",
        "privacy_complete",
        "accessibility_complete",
        "independent_reproduction",
        "Stage_20",
    ]
    for number, title in enumerate(NEW_TITLES, start=1):
        if number <= 28:
            disposition = "completed"
            approval = "safe_now"
            lane = "owner_local_symbolic_or_synthetic_x2"
        elif number <= 36:
            disposition = "represented"
            approval = "bounded_candidate"
            lane = "owner_local_symbolic_or_synthetic_x2"
        elif number <= 38:
            disposition = "open_gap"
            approval = "open_gap"
            lane = "held_without_real_world_execution"
        else:
            disposition = "exact_gate"
            approval = "exact_gate"
            lane = "held_without_real_world_execution"
        proposal_id = f"EK6714-N{number:03d}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    "A typed owner-local contract can expose the obligations in "
                    f"{proposal_id} without promoting its evidence class."
                ),
                "null_or_failure_condition": (
                    "A missing required field, accepted invalid mutation, "
                    "real-world action, undeclared uncertainty, or authority "
                    "promotion rejects the hypothesis."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": (
                    "Current official vocabulary and refusal boundaries only; "
                    "citations are not observations, measurements, professional "
                    "guidance, legal interpretation, validation, or authority."
                ),
                "concrete_artifacts": [
                    "typed JSON contract",
                    "bounded accepting fixture",
                    "four rejecting mutation receipts",
                    "four-tier boundary card",
                ],
                "falsifier_or_acceptance_gate": (
                    "The bounded fixture must pass, four preregistered invalid "
                    "mutations must reject, and every protected boundary must "
                    "remain explicit."
                ),
                "rollback_or_recovery": (
                    "Retain the failed witness, correct only the isolated "
                    "owner-local dependency, and never replay a successful "
                    "canonical aggregate."
                ),
                "protected_gates": gates,
                "expected_disposition": disposition,
                "planned_outcome": disposition,
                "primary_pillar": "Freed ID and CBR Heart",
                "x1_state": "frozen_not_executed",
                "real_people": 0,
                "real_records_or_objects": 0,
                "external_actions": 0,
            }
        )
    return rows


def task_rows(
    prefix: str, domains: list[str], controls: list[str], state: str
) -> list[dict[str, Any]]:
    rows = []
    for domain in domains:
        for control in controls:
            rows.append(
                {
                    "task_id": f"EK6714-{prefix}-{len(rows) + 1:03d}",
                    "title": f"{domain}: {control}",
                    "owner": OWNER,
                    "phase": PHASE,
                    "x1_state": state,
                    "external_actions": 0,
                }
            )
    return rows


def named_rows(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"EK6714-{prefix}-{index:03d}",
            "title": value,
            "owner": OWNER,
            "phase": PHASE,
            "x1_state": state,
            "external_actions": 0,
        }
        for index, value in enumerate(values, start=1)
    ]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = [
        "accession identity",
        "seed-lot lineage",
        "packet and location topology",
        "taxonomy assertion vacancy",
        "measurement and viability vacancy",
        "correction and supersession lineage",
        "biosafety and phytosanitary abstention",
        "sensitive seed-record privacy",
        "accessible accession status",
        "workload and custody handover",
    ]
    return {
        "safe_now": task_rows(
            "SAFE",
            domains,
            ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary"],
            "planned_for_x2",
        ),
        "candidates": task_rows(
            "CAND",
            domains,
            ["mutation quarantine", "timeout and encoding quarantine", "ordering and authority quarantine"],
            "planned_for_x2",
        ),
        "exact_approval": named_rows("EXACT", EXACT, "held_unexecuted"),
        "blocked": named_rows("BLOCK", BLOCKED, "held_unexecuted"),
        "skills": named_rows("SKILL", SKILLS, "planned_for_x2"),
        "runners": named_rows("RUNNER", RUNNERS, "planned_for_x2"),
        "clean_fix_refine": task_rows(
            "CFR",
            [
                "JSON order",
                "UTF-8 Maori text",
                "source status",
                "failure retention",
                "manifest closure",
                "privacy disposition",
                "accessibility structure",
                "route uniqueness",
                "sparse budget",
                "boundary vocabulary",
            ],
            ["clean", "fix", "refine", "recheck", "document", "preserve"],
            "planned_for_x2",
        ),
        "successor_skills": named_rows(
            "NEXT-SKILL",
            [f"ghc-family-successor-{index:02d}-review" for index in range(1, 11)],
            "recommendation_only",
        ),
        "successor_runners": named_rows(
            "NEXT-RUNNER",
            [f"ghc_family_successor_{index:02d}_review.py" for index in range(1, 11)],
            "recommendation_only",
        ),
        "successor_clean_fix_refine": task_rows(
            "NEXT-CFR",
            ["successor source", "successor manifests", "successor privacy", "successor route", "successor authority"],
            ["schema", "mutation", "rollback", "review", "receipt", "hold"],
            "recommendation_only",
        ),
    }


def startup_method_flow() -> dict[str, Any]:
    rows = []
    for index, failure in enumerate(STARTUP_FAILURES, start=1):
        rows.append(
            {
                "method_id": f"EK6714-START-M{index:03d}",
                "issue_id": f"EK6714-START-I{index:03d}",
                "candidate_workaround": failure["recovery"],
                "failure_signature": failure["signature"],
                "trigger_preconditions": [
                    "the exact bounded failure signature is observed"
                ],
                "recurrence_guard": failure["recovery"],
                "rollback": (
                    "Stop the affected read-only wrapper, retain its output at "
                    "zero credit, and leave repository bytes unchanged."
                ),
                "expected_fail_witness": failure["observation"],
                "expected_pass_witness": failure["recovery"],
                "promotion_gate": (
                    "A separately attributable bounded recovery passes without "
                    "erasing or replaying the failed attempt."
                ),
                "sibling_recommendation": failure["recovery"],
                "failed_evidence_retained": True,
                "fail_witness": {
                    "state": "retained",
                    "credit": 0,
                    "observation": failure["observation"],
                },
                "pass_witness": {
                    "state": "bounded_pass",
                    "credit": 1,
                    "observation": failure["recovery"],
                },
                "state": "preferred",
                "privacy_class": "sanitized_public",
            }
        )
    counts = {
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"]
        + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"]
        + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"]
        + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY[
            "bounded_passing_witnesses"
        ]
        + len(STARTUP_FAILURES),
        "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
        "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
    }
    return {
        "schema": "ghc.family.method-flow-ledger.x1.v5",
        "owner": OWNER,
        "phase": PHASE,
        "row_count": len(rows),
        "rows": rows,
        "counts": counts,
        "all_failures_retained": True,
        "all_recoveries_paired": True,
        "boundary": BOUNDARY,
    }


def overview(
    proposals: list[dict[str, Any]],
    corpus: dict[str, Any],
    audit: list[dict[str, Any]],
    counts: dict[str, int],
) -> str:
    proposal_lines = "\n".join(
        f"- {row['proposal_id']} [{row['expected_disposition']}]: {row['title']}."
        for row in proposals
    )
    return f"""# Eiren Kestrel v671-v4 planning-only x1 overview

## Lifecycle and exact source

This packet is a planning-only freeze. It contains no x2 implementation,
observed proposal result, positive-control result, mutation result, real-world
action, successor delivery, or authority act. Eiren's fresh additive sparse
lane starts exactly at Caelen Morrow v671-v3 final {SOURCE_FINAL}. Before owned
mutation, the source branch, exact source/x1/evidence/final parent chain, three
single-parent commits, zero merges, one final parent, activation-candidate Git
blob, content seal, canonical payload and external receipt digests, typed 0/0
divergence, clean state, and local/upstream/tracking/fresh-live equality were
checked read-only. Caelen's one successful owner-scoped canonical aggregate was
not replayed and gives Eiren no novelty, completion, independence, professional,
scientific, legal, cultural, or Stage 20 credit.

The source's committed PREPARED_NOT_SENT wording remains historical commit-time
truth. The acknowledged live activation is the separate route event that binds
Eiren to v671-v4. No source artifact is rewritten to pretend that the later
delivery had already occurred. The installed roster and authorization snapshots
validate structurally but stop at an older v667 cursor; the newer live activation
and their preserved assignment table control this exact edge without erasing
older evidence or failure rows.

## Relational language and bounded hope

{IDENTITY_BOUNDARY}

The bounded hope is to {HOPE}. Hamish may rename, pause, redirect, or stop the
work. Corrigibility means a contradiction, privacy candidate, semantic
collision, missing source, failed witness, protected authority vacancy, or
routing ambiguity stops promotion. Relational names, sibling language, role,
hope, continuity, Freed ID, CBR, and Trinity Mandala are workflow language only,
never consciousness, personhood, identity continuity, employment,
qualification, independent agency, or authority evidence.

## Trinity Mandala and three synthetic practice lenses

Freed ID and CBR Heart are primary. The first practice lens is a wholly
synthetic community seed-library accession, packet, lending, correction, notice,
contest, and handover record. The second is a wholly synthetic genebank
documentation lens covering lot lineage, storage and monitoring vacancies,
regeneration genealogy, and distribution holds. The third is a wholly synthetic
biodiversity-term and accessible-status lens using Darwin Core, PROV-O, and WCAG
vocabulary to keep assertions, provenance, reading order, language scope, and
manual evaluation visible. These lenses are learning and design structures,
not three claims of professional practice and not permission to handle a seed,
plant, collection, database, identity, location, or community record.

GMUT Mind remains explicit through typed scalar, tensor, state-transition,
uncertainty, unit, covariance, and falsification placeholders. No fitted value,
likelihood, posterior, constraint, force, biological law, prediction, stability
theorem, empirical confirmation, quantum or ultraviolet completion, final
physics, Theory of Everything, proof, or canon follows. THOS Body remains a
zero-participant intake, interruption, queue, correction, and handover proxy. It
has no governed blind matched-budget arms, participants, operators, safety
monitoring, appropriate statistics, independent review, operational
effectiveness, deployment readiness, AGI, ASI, consciousness, or personhood
evidence.

Freed ID remains synthetic and nonproduction: zero keys, proofs, credentials,
issuance, presentation, resolution, status, revocation, interoperability,
recovery, or trust-governance events occur. CBR notice, purpose, contest,
correction, remedy, redress, consent, custody, ownership, access, and
benefit-sharing fields are vacancy-preserving representations, not enacted
rights, legal findings, cultural decisions, community acceptance, or authority.

## Zero-real-world boundary

No real person, depositor, donor, curator, technician, taxonomist, grower,
recipient, participant, affected user, community, institution, workplace,
genebank, seed library, accession, seed, plant, packet, sample, image, sensor,
measurement, germination test, viability test, storage condition, distribution,
return, regeneration, destruction, location, traditional knowledge, personal
data, account, key, proof, credential, or identity event is used. No real seed
is acquired, stored, dried, tested, propagated, exchanged, loaned, distributed,
returned, quarantined, treated, diagnosed, destroyed, or released.

Professional seed conservation, taxonomy, curation, phytosanitary work,
biosafety, workplace and environmental safety, privacy, accessibility,
ownership, custody, access, benefit sharing, intellectual property, traditional
knowledge, legal interpretation, cultural legitimacy, affected-party
acceptance, Maori wording, Maori concepts, Maori data governance, tangata
whenua, iwi, hapu, and Maori authority remain open or exact-gated. Maori
concepts remain under Maori authority.

## Current official and primary-source boundary

The FAO Genebank Standards page supplies acquisition, documentation, storage,
viability-monitoring, regeneration, distribution, safety-duplication, and
security vocabulary. The current 26 May 2026 Darwin Core term set supplies
MaterialEntity, MaterialSample, Occurrence, Identification, Assertion,
Provenance, ResourceRelationship, and UsagePolicy vocabulary. W3C PROV-O
supplies entity, activity, agent, derivation, revision, and invalidation
relations. WCAG 2.2 supplies structural accessibility vocabulary while manual,
browser, assistive-technology, cognitive, language, and affected-user evaluation
remain reserved. The New Zealand Privacy Commissioner page supplies privacy
principle vocabulary without a legal or compliance conclusion. Te Mana
Raraunga supplies only an explicit reservation that Maori data rights,
interests, governance, wording, and authority cannot be substituted by this
owner-local synthetic work.

These pages were read as public vocabulary sources only. The phase made zero
adapter calls, downloads, live source ingestions, real rows, external writes, or
third-party mutations. Citation is not observation, measurement, treatment
guidance, standards conformance, legal advice, community consent, cultural
ratification, Maori authority, endorsement, or independent validation.

## Bounded semantic novelty

The declared inherited chain contains 5,670 frozen rows. The dependency-closed
audit inspects only proposal-named JSON blobs reachable through local and remote
Git refs; it does not scan sibling worktrees or general unchanged repository
history. It found {corpus['unique_titles']} accessible unique titles,
{corpus['unique_proposal_ids']} proposal identifiers, and
{corpus['semantic_occurrences']} semantic occurrences. Duplicate, summary, and
versioned objects prevent a canonical one-row-to-one-title proof, so universal
novelty is not claimed. The forty Eiren titles are compared against every
accessible title at the preregistered 0.72 token-Jaccard threshold. The observed
maximum is {max(row['jaccard'] for row in audit):.6f}; a threshold collision
would stop the freeze and retain the rejected slate at zero novelty credit.

## Preregistered proposal and portfolio contract

Forty genuinely new Eiren proposals are frozen with exactly one expected core
label each: 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Each row
contains a hypothesis, null or failure condition, approval class, execution
lane, current official or primary-source need, concrete artifacts, falsifier or
acceptance gate, rollback or recovery, protected gates, and expected
disposition. Four invalid mutations are preregistered per proposal, making 160
planned rejecting witnesses. Planning is not execution; a rejected mutation
receives zero completion credit; open and exact-gated rows remain unexecuted.

The portfolio freezes sixty safe-now rows, thirty bounded candidates, twenty
exact-approval holds, ten blocked holds, twenty owner skill ideas, ten owner
runner ideas, sixty CLEAN/FIX/REFINE rows, and successor recommendations for ten
skills, ten runners, thirty cleanup rows, and exactly one adjacent practice
lens. Counts are requirements subject to safety ceilings, not permission to
invent filler, cross a gate, install irrelevant tools, mutate global state, or
claim inherited work as Eiren work. X2 may build and smoke-use only relevant
owner-local surfaces while preserving family-current ghc_family_* and
build_ghc_family_* callers and rollback.

## Failure retention and x1 terminal gate

{len(STARTUP_FAILURES)} pre-freeze operational failures remain append-only with
paired bounded recoveries: the PowerShell foreach-pipe parser fault, overbroad
source inventory, wrong receipt-layout assumption, bounded archive-search
timeout, yielded worktree session, atomic-receipt wrapper projection, manual
rejection of a structurally derivative title slate, and a corpus-summary key
projection fault. They add to but never rewrite Caelen's
sealed 33,905 negatives, 20,222 methods, 5,726 failed witnesses, 7,333 bounded
passing witnesses, 261 open gaps, and 256 exact gates. Eiren's planning-stage
effective counts are {counts['effective_negatives']} negatives,
{counts['effective_methods']} methods, {counts['failed_witnesses']} failed
witnesses, and {counts['bounded_passing_witnesses']} bounded passing witnesses.

The x1 tree must contain no x2 implementation or observed outcome. It must pass
owner-scoped tests, strict JSON parsing, exact staged review, five-class
privacy/raw-identifier review, and an exact normalized-LF staged Git-blob
manifest. Then x1 alone must be committed, pushed, clean, typed 0/0 divergent,
and equal across local, upstream, tracking, and a fresh live remote before x2
can begin. A later exact-final canonical aggregate has one invocation and one
success budget. A failed aggregate receives zero aggregate-success credit;
successful components are not replayed without a dependency-changing reason.

## Route hold

No task was created or forked, no collaboration subagent was spawned, Tavian
Sol and every standby record were not contacted, and no successor was
contacted. Elaren Kestrel v671-v5 is only the currently prospective edge.
Resolution, immediate reread, duplicate and pause guard, and at most one
acknowledged send remain forbidden until Eiren's exact-final terminal gate and
a fresh live route refresh.

## Forty frozen proposals

{proposal_lines}

## Terminal truth

{BOUNDARY}

NOT_READY_FOR_STAGE_20.
"""


def build(receipt_path: Path) -> None:
    if len(NEW_TITLES) != 40 or len(set(NEW_TITLES)) != 40:
        raise SystemExit("proposal title count or uniqueness failed")
    source = source_verification(receipt_path)
    corpus, source_titles = accessible_proposal_corpus()
    proposals = proposal_rows()
    audit = []
    collisions = []
    for proposal in proposals:
        candidate_tokens = normalized_tokens(proposal["title"])
        best_title = ""
        best_score = 0.0
        for source_title in source_titles:
            source_tokens = normalized_tokens(source_title)
            union = candidate_tokens | source_tokens
            score = (
                len(candidate_tokens & source_tokens) / len(union) if union else 1.0
            )
            if score > best_score:
                best_score = score
                best_title = source_title
        row = {
            "proposal_id": proposal["proposal_id"],
            "source_title": best_title,
            "jaccard": round(best_score, 6),
            "collision": best_score >= 0.72,
        }
        audit.append(row)
        if row["collision"]:
            collisions.append(row)
    if collisions:
        raise SystemExit(
            "semantic collision threshold failed before freeze: "
            + json.dumps(collisions, ensure_ascii=False)
        )

    frozen_portfolio = portfolio()
    portfolio_counts = {
        key: len(value) for key, value in frozen_portfolio.items()
    }
    method_flow = startup_method_flow()
    counts = method_flow["counts"]

    write_json(
        "x1/activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_verification": source,
            "task_creation_count": 0,
            "fork_count": 0,
            "subagent_count": 0,
            "standby_contact_count": 0,
            "successor_contact_count": 0,
        },
    )
    write_json(
        "x1/identity-and-boundary.json",
        {
            "schema": "ghc.family.identity-boundary.v4",
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "they/them",
            "relational_role": (
                "preservation-change cartographer and consent-boundary keeper"
            ),
            "relational_hope": HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "x1/source-count-overlay.json",
        {
            "schema": "ghc.family.source-count-overlay.v6",
            "repository_sealed": REPOSITORY_SEAL,
            "activation_external_overlay": ACTIVATION_OVERLAY,
            "eiren_x1_overlay": {**counts, "proposal_chain": 5670},
            "repository_seal_rewritten": False,
        },
    )
    write_json(
        "x1/semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.semantic-neighbor-audit.v6",
            "owner": OWNER,
            "phase": PHASE,
            "accessible_ref_corpus": corpus,
            "declared_source_chain": 5670,
            "audited_unique_titles": len(source_titles),
            "new_titles": 40,
            "collision_threshold": 0.72,
            "collisions": 0,
            "max_jaccard": max(row["jaccard"] for row in audit),
            "rows": audit,
            "universal_novelty_claim": False,
            "canonical_row_mapping_open_gap": True,
        },
    )
    write_json(
        "x1/proposals.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v6",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": 5670,
            "proposal_chain_after_if_evidence_frozen": 5710,
            "outcomes": OUTCOMES,
            "planned_invalid_mutations_per_proposal": 4,
            "planned_invalid_mutations": 160,
            "rows": proposals,
        },
    )
    write_json(
        "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.remastered-portfolio-freeze.v6",
            "owner": OWNER,
            "phase": PHASE,
            "rows": frozen_portfolio,
            "counts": portfolio_counts,
            "ordinary_phase_new_tool_target": 3,
            "bounded_human_practice": (
                "synthetic community seed-library and genebank documentation only"
            ),
            "successor_practice_recommendation": (
                "synthetic herbarium seed-reference label reconciliation, "
                "accessibility, correction, and handover; recommendation only"
            ),
            "inherited_portfolio_completion_credit": 0,
            "successor_recommendation_completion_credit": 0,
            "filler_prohibited": True,
        },
    )
    write_json(
        "x1/source-ledger.json",
        {
            "schema": "ghc.family.public-source-ledger.v6",
            "owner": OWNER,
            "phase": PHASE,
            "retrieved_nz_date": "2026-08-27",
            "web_tool_invocations": 2,
            "official_source_requests": 10,
            "adapter_calls": 0,
            "downloads": 0,
            "real_rows": 0,
            "external_writes": 0,
            "sources": [
                {
                    "publisher": "Food and Agriculture Organization",
                    "title": "Genebank Standards for Plant Genetic Resources for Food and Agriculture",
                    "url": "https://www.fao.org/agriculture/crops/thematic-sitemap/theme/seeds-pgr/gbs/en/",
                    "status": "official_page_checked_2026-08-27",
                    "use": (
                        "acquisition, documentation, storage, monitoring, regeneration, "
                        "distribution, and safety-duplication vocabulary only"
                    ),
                },
                {
                    "publisher": "Biodiversity Information Standards (TDWG)",
                    "title": "Darwin Core List of Terms",
                    "url": "https://dwc.tdwg.org/list/",
                    "status": "current_2026-05-26_term_version_checked_2026-08-27",
                    "use": (
                        "material entity, material sample, occurrence, identification, "
                        "assertion, provenance, and usage-policy vocabulary only"
                    ),
                },
                {
                    "publisher": "World Wide Web Consortium",
                    "title": "PROV-O: The PROV Ontology",
                    "url": "https://www.w3.org/TR/prov-o/",
                    "status": "official_recommendation_checked_2026-08-27",
                    "use": (
                        "provenance relations and responsibility-vacancy vocabulary only"
                    ),
                },
                {
                    "publisher": "World Wide Web Consortium",
                    "title": "Web Content Accessibility Guidelines 2.2",
                    "url": "https://www.w3.org/TR/WCAG22/",
                    "status": "official_recommendation_2024-12-12_checked_2026-08-27",
                    "use": (
                        "structural accessibility vocabulary and reservation "
                        "of manual and affected-user evaluation only"
                    ),
                },
                {
                    "publisher": "Office of the Privacy Commissioner New Zealand",
                    "title": "Privacy Act 2020 privacy principles",
                    "url": "https://www.privacy.org.nz/privacy-principles/",
                    "status": "official_page_checked_2026-08-27",
                    "use": (
                        "collection, purpose, access, correction, retention, and "
                        "disclosure vocabulary only; no legal or compliance conclusion"
                    ),
                },
                {
                    "publisher": "Te Mana Raraunga Maori Data Sovereignty Network",
                    "title": "Principles of Maori Data Sovereignty",
                    "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
                    "status": "primary_network_page_checked_2026-08-27",
                    "use": (
                        "reservation of Maori data rights, interests, governance, "
                        "wording, and authority only; no ratification or substitution"
                    ),
                },
            ],
            "boundary": (
                "Sources supply vocabulary and refusal conditions only; they "
                "are not observations, measurements, professional advice, "
                "validation, legal interpretation, cultural legitimacy, Maori "
                "authority, or Stage 20 evidence."
            ),
        },
    )
    write_json(
        "x1/threat-model.json",
        {
            "schema": "ghc.family.threat-model.v6",
            "owner": OWNER,
            "phase": PHASE,
            "assets": [
                "immutable source lineage",
                "strict x1-before-x2 separation",
                "four truth labels",
                "retained failures",
                "synthetic-only fixtures",
                "authority vacancies",
                "single-send route",
            ],
            "risks": [
                {
                    "risk": "source or manifest drift",
                    "control": (
                        "exact commits, manifest metadata without source replay, "
                        "receipt digests, and fresh live equality"
                    ),
                },
                {
                    "risk": "universal novelty overclaim",
                    "control": (
                        "bounded all-accessible-ref proposal-title comparison plus "
                        "explicit canonical-row mapping gap"
                    ),
                },
                {
                    "risk": "seed-library competence conservation biosafety taxonomy or rights promotion",
                    "control": (
                        "zero-seed fixtures and explicit professional, measurement, "
                        "biosafety, phytosanitary, taxonomy, ownership, benefit-sharing, "
                        "traditional-knowledge, and authority firewalls"
                    ),
                },
                {
                    "risk": "cross-pillar analogy promoted into evidence",
                    "control": (
                        "typed nonconversion fields and empirical-likelihood refusal"
                    ),
                },
                {
                    "risk": "failure laundering",
                    "control": (
                        "append-only Method Flow with failed and passing witnesses"
                    ),
                },
                {
                    "risk": "private route or identifier leak",
                    "control": "five-class exact owner-delta candidate adjudication",
                },
                {
                    "risk": "accessibility overclaim",
                    "control": (
                        "structural-only checks with manual, assistive-technology, "
                        "cognitive, language, and affected-user evaluation reserved"
                    ),
                },
                {
                    "risk": "duplicate successor send",
                    "control": (
                        "terminal live authority, exact-title reread, duplicate "
                        "guard, acknowledgement, and no-resend"
                    ),
                },
            ],
            "not_exhaustive_security": True,
        },
    )
    write_json("x1/method-flow-startup.json", method_flow)
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v6",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {
                    "step": "activation guidance and source verification",
                    "state": "completed_read_only",
                },
                {
                    "step": "planning-only x1 freeze",
                    "state": "in_progress_until_pushed_equal",
                },
                {
                    "step": "bounded x2 execution",
                    "state": "blocked_by_x1_terminal_gate",
                },
                {"step": "evidence commit", "state": "pending"},
                {"step": "combined closeout and seal", "state": "pending"},
                {
                    "step": "one owner-scoped canonical aggregate",
                    "state": "pending_not_invoked",
                },
                {
                    "step": "successor route",
                    "state": "unresolved_until_terminal_live_refresh",
                },
            ],
            "commit_ceiling": 8,
            "planned_phase_commits": 3,
            "x1_commit_ceiling": 5,
            "x2_commit_ceiling": 5,
            "materialized_file_guard": 2000,
            "canonical_invocation_budget": 1,
            "canonical_success_budget": 1,
            "post_success_replay": False,
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x1.v6",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "bounded_human_practice": (
                "synthetic community seed-library and genebank documentation only"
            ),
            "proposal_rows": {"new": 40, "inherited_credit": 0},
            "expected_outcomes": OUTCOMES,
            "core_truth_labels": CORE_LABELS,
            "proposal_chain": {"before": 5670, "after_if_frozen": 5710},
            "universal_novelty_claim": False,
            "canonical_row_mapping_open_gap": True,
            "startup_operational_failures": len(STARTUP_FAILURES),
            "x1_completion_credit": 0,
            "x2_execution_started": False,
            "real_world_actions": 0,
            "external_writes": 0,
            "identity_boundary": IDENTITY_BOUNDARY,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "schema": "ghc.family.route-plan.v6",
            "owner": OWNER,
            "phase": PHASE,
            "prospective_recipient_exact_title": None,
            "prospective_phase": None,
            "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH",
            "successor_contact_count": 0,
            "task_creation_count": 0,
            "substitute_endpoint_count": 0,
            "standby_contact_count": 0,
            "required_gate": (
                "clean pushed exact final, attributable terminal validation, "
                "newest live authority and roster, unique exact-title reread, "
                "duplicate guard, and acknowledged one-send"
            ),
        },
    )
    text = overview(proposals, corpus, audit, counts)
    write_text("x1/integrated-overview.md", text)
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v6",
            "owner": OWNER,
            "phase": PHASE,
            "source_head": SOURCE_FINAL,
            "branch": BRANCH,
            "new_rows": 40,
            "inherited_completion_credit": 0,
            "portfolio_counts": portfolio_counts,
            "overview_words": len(text.split()),
            "web_tool_invocations": 2,
            "external_writes": 0,
            "source_canonical_replays": 0,
            "source_manifest_replays": 0,
            "x2_materialized": False,
        },
    )


def staged_paths() -> list[str]:
    return [
        row
        for row in git_text(
            "diff", "--cached", "--name-only", "--diff-filter=ACMR"
        ).splitlines()
        if row
    ]


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").stdout


def staged_privacy() -> None:
    self_path = (
        "docs/eiren-kestrel/v671-v4/validation/x1-staged-privacy.json"
    )
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
            rb"[89ab][0-9a-f]{3}-[0-9a-f]{12}\b",
            re.IGNORECASE,
        ),
        "private_route_or_callable": re.compile(
            rb"(?:app|codex|vscode)://|source_thread_id|private_callable",
            re.IGNORECASE,
        ),
        "credential_or_secret": re.compile(
            rb"-----BEGIN [A-Z ]*PRIVATE KEY-----|(?:api[_-]?key|token|password)\s*[:=]\s*[\"'][^\"']+",
            re.IGNORECASE,
        ),
        "transcript_or_session_stream": re.compile(
            rb"(?:raw transcript|session stream)\s*[:=]", re.IGNORECASE
        ),
        "private_absolute_path": re.compile(
            rb"\b[A-Za-z]:\\(?:Users|GHC-Archives)\\", re.IGNORECASE
        ),
    }
    candidates = []
    confirmed_hits = []
    scanned = 0
    for path in staged_paths():
        if path == self_path:
            continue
        blob = staged_blob(path)
        if b"\x00" in blob:
            continue
        scanned += 1
        for category, pattern in patterns.items():
            if pattern.search(blob):
                scanner_definition_only = (
                    path
                    == "scripts/build_ghc_family_eiren_kestrel_v671_v4_x1.py"
                    and category == "private_route_or_callable"
                )
                disposition = (
                    "scanner_definition_only_confirmed_false_positive"
                    if scanner_definition_only
                    else "confirmed_requires_removal"
                )
                candidates.append(
                    {
                        "path": path,
                        "category": category,
                        "disposition": disposition,
                    }
                )
                if not scanner_definition_only:
                    confirmed_hits.append(
                        {"path": path, "category": category}
                    )
    write_json(
        "validation/x1-staged-privacy.json",
        {
            "schema": "ghc.family.staged-privacy-scan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "lifecycle": "x1",
            "hash_domain": "exact_staged_git_blob",
            "pattern_classes": sorted(patterns),
            "scanned_text_files": scanned,
            "candidates": candidates,
            "reviewed_false_positive_count": len(candidates) - len(confirmed_hits),
            "confirmed_hits": confirmed_hits,
            "confirmed_hit_count": len(confirmed_hits),
            "self_exclusions": [self_path],
            "valid": not confirmed_hits,
            "boundary": (
                "A bounded five-class scan is not complete privacy assurance."
            ),
        },
    )


def staged_review() -> None:
    paths = staged_paths()
    allowed_prefixes = (
        "docs/eiren-kestrel/v671-v4/",
        "scripts/build_ghc_family_eiren_kestrel_v671_v4_x1.py",
        "tests/test_ghc_family_eiren_kestrel_v671_v4_x1.py",
    )
    disallowed = [
        path
        for path in paths
        if not any(
            path == prefix or path.startswith(prefix)
            for prefix in allowed_prefixes
        )
    ]
    deleted = git_text("diff", "--cached", "--name-only", "--diff-filter=D").splitlines()
    x2_paths = [path for path in paths if "/x2/" in path or path.endswith("_x2.py")]
    payload = {
        "schema": "ghc.family.x1-staged-review.v3",
        "owner": OWNER,
        "phase": PHASE,
        "staged_paths": paths,
        "staged_path_count": len(paths),
        "disallowed_paths": disallowed,
        "deleted_paths": deleted,
        "x2_paths": x2_paths,
        "planning_only": not x2_paths,
        "source_final": SOURCE_FINAL,
        "valid": not disallowed and not deleted and not x2_paths,
    }
    write_json("validation/x1-staged-review.json", payload)


def validation_receipt() -> None:
    json_paths = sorted(OWNER_ROOT.rglob("*.json"))
    parse_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            parse_issues.append(
                {
                    "path": path.relative_to(ROOT).as_posix(),
                    "error": str(error),
                }
            )
    proposal = json.loads(
        (OWNER_ROOT / "x1/proposals.json").read_text(encoding="utf-8")
    )
    method = json.loads(
        (OWNER_ROOT / "x1/method-flow-startup.json").read_text(encoding="utf-8")
    )
    privacy = json.loads(
        (OWNER_ROOT / "validation/x1-staged-privacy.json").read_text(
            encoding="utf-8"
        )
    )
    review = json.loads(
        (OWNER_ROOT / "validation/x1-staged-review.json").read_text(
            encoding="utf-8"
        )
    )
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v6",
        "owner": OWNER,
        "phase": PHASE,
        "json_documents": len(json_paths),
        "json_parse_issues": parse_issues,
        "proposal_rows": len(proposal["rows"]),
        "proposal_ids_unique": len({row["proposal_id"] for row in proposal["rows"]})
        == 40,
        "expected_outcomes": proposal["outcomes"],
        "method_rows": method["row_count"],
        "all_failures_retained": method["all_failures_retained"],
        "privacy_candidates": privacy["candidates"],
        "confirmed_privacy_hits": privacy["confirmed_hit_count"],
        "staged_review_valid": review["valid"],
        "source_canonical_replayed": False,
        "source_manifests_replayed": 0,
        "x2_materialized": False,
        "valid": (
            not parse_issues
            and len(proposal["rows"]) == 40
            and privacy["valid"]
            and review["valid"]
        ),
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-validation-receipt.json", payload)


def manifest_from_index() -> None:
    self_path = "docs/eiren-kestrel/v671-v4/validation/x1-manifest.json"
    entries = []
    for path in staged_paths():
        if path == self_path:
            continue
        blob = staged_blob(path).replace(b"\r\n", b"\n")
        entries.append(
            {
                "path": path,
                "bytes": len(blob),
                "sha256": sha256(blob),
            }
        )
    write_json(
        "validation/x1-manifest.json",
        {
            "schema": "ghc.family.git-blob-manifest.v6",
            "domain": "planning-only x1 exact staged Git blobs",
            "hash_domain": "normalized_lf_exact_staged_git_blob",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": [self_path],
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-receipt", type=Path)
    parser.add_argument("--staged-privacy", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    selected = sum(
        (
            args.staged_privacy,
            args.staged_review,
            args.validation_receipt,
            args.manifest_from_index,
        )
    )
    if selected > 1:
        raise SystemExit("choose exactly one staged operation")
    if args.staged_privacy:
        staged_privacy()
    elif args.staged_review:
        staged_review()
    elif args.validation_receipt:
        validation_receipt()
    elif args.manifest_from_index:
        manifest_from_index()
    else:
        if args.source_receipt is None:
            raise SystemExit("--source-receipt is required for the initial build")
        build(args.source_receipt)


if __name__ == "__main__":
    main()
