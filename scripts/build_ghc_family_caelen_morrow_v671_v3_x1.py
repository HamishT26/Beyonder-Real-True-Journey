"""Build the planning-only Caelen Morrow v671-v3 x1 packet.

This builder is intentionally limited to the current owner delta.  It does not
execute x2 proposals, replay Sylven's successful canonical aggregate, mutate a
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
OWNER_ROOT = ROOT / "docs" / "caelen-morrow" / "v671-v3"
OWNER = "Caelen Morrow"
PHASE = "v671-v3"
BRANCH = "codex/GHC-Family/caelen-morrow-v671-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v671-v2-full-tools"
SOURCE_START = "ebbd2ea41873c12287d94b0ec2b64dc22a87c07d"
SOURCE_X1 = "26c88fefc685b48965a1418d07204cc91f6580a0"
SOURCE_EVIDENCE = "140714b7a4e25814de333752a8627055384195ab"
SOURCE_FINAL = "33b7c2d6b9f79f931ff98c478f136dab823c4d69"
ACTIVATION_PATH = (
    "docs/sylven-arc/v671-v2/handoffs/"
    "caelen-morrow-v671-v3-activation-candidate.md"
)
ACTIVATION_SHA256 = (
    "a4a1c5812fc9e421e2a7d0e8c5aeb90eaab9421a9220a30650016f84046fe2dc"
)
SOURCE_CANONICAL_SHA256 = (
    "e04b9d221dfbf26c593d0aa662d4e82d51838e6caccef3ccb3dca5f977f8fa2d"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "1da9b7c6e3d2826173560d28c411d8b51f56aeb5bf32624511d1047aff94a807"
)
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}

IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, preservation-change cartographer and "
    "consent-boundary keeper, is relational working language only. It is not "
    "evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "professional, operational, legal, cultural, affected-party, or Maori "
    "authority."
)
HOPE = (
    "make every synthetic transition auditable, reversible, and unmistakably "
    "short of real-world authority"
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
    "effective_negatives": 33707,
    "effective_methods": 20024,
    "failed_witnesses": 5528,
    "bounded_passing_witnesses": 7099,
    "open_gaps": 259,
    "exact_gates": 254,
    "proposal_chain": 5630,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 33711,
    "effective_methods": 20028,
    "failed_witnesses": 5532,
    "bounded_passing_witnesses": 7103,
    "external_zero_credit_failures": 4,
    "external_bounded_recoveries": 4,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    {
        "signature": "reference-inventory-foreach-piped-without-materialized-collection",
        "observation": "A read-only PowerShell inventory wrapper ended in an empty-pipe parser error before emitting rows.",
        "recovery": "Materialize the projection into an array and pipe only the completed array.",
    },
    {
        "signature": "script-inventory-repeated-unmaterialized-foreach-pipeline",
        "observation": "A second read-only inventory reused the same invalid foreach-to-pipe shape and was rejected.",
        "recovery": "Apply the already identified materialized-array recurrence guard before sorting.",
    },
    {
        "signature": "source-ancestry-probe-mistyped-one-character-of-source-sha",
        "observation": "Git rejected an ambiguous inherited source revision because one character was omitted.",
        "recovery": "Rerun only ancestry and commit-count scalars with the exact committed source SHA.",
    },
    {
        "signature": "source-packet-inventory-guessed-nonexistent-source-verification-file",
        "observation": "The guessed x1 source-verification filename was absent; the data lived in activation-intake.json.",
        "recovery": "Enumerate the exact x1 directory and read only observed filenames.",
    },
    {
        "signature": "sparse-worktree-wrapper-window-elapsed-during-active-checkout",
        "observation": "The worktree command returned only a preparing line while Git continued under its index lock.",
        "recovery": "Do not replay; inspect processes and the registered worktree, wait for completion, then verify exact head, sparse patterns, clean state, and file count.",
    },
    {
        "signature": "parallel-proposal-display-exceeded-combined-result-budget",
        "observation": "A multi-window read returned a truncated combined presentation.",
        "recovery": "Read the two missing numbered windows separately through EOF.",
    },
    {
        "signature": "raw-portfolio-display-truncated-before-all-repetitive-rows",
        "observation": "The raw portfolio display exceeded its result budget.",
        "recovery": "Parse the exact JSON and emit every row as a compact semantic projection.",
    },
    {
        "signature": "combined-x1-packet-display-truncated-before-several-small-files",
        "observation": "A combined packet read omitted middle files from the presentation window.",
        "recovery": "Reread each omitted exact file separately and retain the truncated attempt.",
    },
    {
        "signature": "first-letterpress-title-slate-crossed-semantic-collision-threshold",
        "observation": "Nine of forty draft titles scored at or above the preregistered 0.72 token-Jaccard threshold against accessible source-tree titles, so the slate received zero novelty credit and was not frozen.",
        "recovery": "Retain the rejected neighbor rows, rewrite only the nine colliding concepts around different structures, and rerun the complete forty-title comparison before freeze.",
    },
    {
        "signature": "exact-source-tree-semantic-corpus-undercovered-declared-accessible-history",
        "observation": "The first collision-free rerun inspected 1,439 exact-source-tree titles, materially fewer than the 5,577-title accessible all-ref corpus declared by the inherited activation, so it earned zero freeze credit.",
        "recovery": "Expand only the proposal-title audit to unique proposal-named JSON blobs reachable through local and remote refs, retain the canonical-row mapping gap, and rerun before freeze.",
    },
    {
        "signature": "multi-hunk-semantic-scope-patch-missed-renamed-callsite",
        "observation": "A verification-first multi-hunk patch expected a callsite spelling that no longer matched the current file and was rejected without changing bytes.",
        "recovery": "Inspect the exact function and callsite, then apply narrow context-matched patches only.",
    },
    {
        "signature": "expanded-semantic-audit-retained-stale-source-tree-output-key",
        "observation": "The first successful all-ref build still serialized its corpus beneath the pre-expansion source_tree_corpus key, making the otherwise correct scope needlessly ambiguous.",
        "recovery": "Rename only the generated field to accessible_ref_corpus and regenerate the uncommitted planning packet before freeze.",
    },
    {
        "signature": "first-x1-five-class-scan-stopped-on-scanner-definition-token",
        "observation": "The first exact staged five-class scan found one private-route-class candidate in its own scanner definition and correctly remained invalid pending exact review.",
        "recovery": "Retain the candidate and failed scan, then allowlist only the exact builder path and exact scanner-definition class after confirming that no route value or callable identifier is present.",
    },
]

NEW_TITLES = [
    "synthetic letterpress job namespace with forme chase type case proof edition and component-identity vacancy register",
    "letterpress forme chase bed bearer and reference-plane topology without lockup pressure or press-readiness inference",
    "type-case compartment sort quoin furniture and spacing-material relation graph with orphan rejection",
    "page folio signature sheet side and imposition-position topology with pagination uncertainty",
    "roman italic small-cap ligature ornament and sort-variant token separation without type-authenticity claims",
    "surrogate edition dependency lattice encoding parentless leaf bundles quarantined custody assertions and irreversible-release prohibition",
    "reported slur setoff show-through picking and misregister cue separation from observation diagnosis and treatment",
    "measure leading point pica millimetre sheet-caliper and impression-depth vacancy ledger with SI and calibration abstention",
    "copy manuscript galley proof revise and press-command distinction from observed printed output",
    "composing stick galley bodkin brayer roller and tympan lot placeholders with competence and performance holds",
    "ink pigment vehicle reducer cleaner and wash batch drying ventilation and incompatibility vacancies with chemical-safety refusal",
    "composition lockup makeready proofing printing drying and distribution sequence graph without production authority",
    "paper stock grain direction deckle watermark sizing and coating uncertainty firewall without material-authenticity claims",
    "platen cylinder gripper feed flywheel sharp pinch crush electrical and fire signal taxonomy without workplace safety release",
    "metal wood polymer paper ink solvent and adhesive source authenticity suitability and fitness refusal matrix",
    "ink hue density gloss coverage edge and condition-label provenance with illumination and observation vacancies",
    "printed-sheet image scan and media-pointer absence with copyright trademark privacy and consent holds",
    "surrogate printer compositor press-operator binder and editor capability-vacancy profile separating attribution competence employment and authority",
    "token-shape classifier for print prose fields with redact isolate review discard and preserve decisions and no payload retention",
    "two-source print job docket reconciliation with unresolved copy colour edition date and custody disagreement quarantine",
    "interrupt ledger using monotone work-unit ordinals lease expiry restart checksum and executable-command exclusion for print documentation",
    "dual-channel print-status dossier with error-first index non-colour state vocabulary reading-order checksum and reserved human usability review",
    "language-scope matrix for copy variants recording source-script tag translation vacancy review-owner absence and publication hold",
    "proof-correction handshake with challenge token field-level readback immutable predecessor digest supersession edge and reprint abstention",
    "proof-batch attention budget ledger with queue-width stop threshold transfer checksum and no human fatigue or performance inference",
    "append-only copy material imposition impression conjecture and correction graph with reversible letterpress lineage",
    "claim-edge matrix for edition attribution reproduction custody exhibition withdrawal contest and unresolved decision ownership",
    "withdrawal cancellation supersession pulping and retention docket with no real destruction reprinting or rights determination",
    "THOS letterpress documentation queue proxy with zero people zero press actions and zero effectiveness credit",
    "THOS proof-cycle state board with interruption challenge correction readback and participant-free handover",
    "Freed ID zero-key proof-correction subject envelope binding role claims to challengeable states without issuance resolution status or revocation event",
    "printed-edition verification record isolated from authenticity legibility quality safety condition and durability claims",
    "CBR reason-and-remedy transition table for synthetic print notices with purpose expiry data-category vacancy contest state response debt and no enacted right",
    "CBR pseudonymous printer editor custodian reader and client privacy challenge remedy and redress representation",
    "GMUT ink-transfer scalar tensor surrogate with typed units contact-state vacancies and empirical-fit refusal",
    "GMUT forme-pressure contact-network proxy with likelihood force prediction stability and material-law nonconversion",
    "Library of Congress paper-deterioration vocabulary adapter with zero calls zero downloads zero object rows and rights vacancies",
    "real authenticated print dimensions paper ink measurements blind quality evaluation and independent-review gap",
    "real printer conservator owner reader and affected-user accessibility evaluation gate",
    "competent machine chemical fire workplace heritage copyright legal cultural and Maori-authority decision gate",
]

SKILLS = [
    "ghc-family-letterpress-job-identity",
    "ghc-family-letterpress-forme-topology",
    "ghc-family-typecase-relation-guard",
    "ghc-family-imposition-position-graph",
    "ghc-family-letterpress-measurement-vacancy",
    "ghc-family-letterpress-command-observation-split",
    "ghc-family-letterpress-material-hold",
    "ghc-family-letterpress-hazard-abstention",
    "ghc-family-letterpress-privacy-quarantine",
    "ghc-family-letterpress-accessible-handover",
    "ghc-family-letterpress-correction-lineage",
    "ghc-family-letterpress-rights-vacancy",
    "ghc-family-letterpress-language-authority-hold",
    "ghc-family-letterpress-role-capability-abstention",
    "ghc-family-letterpress-proof-state",
    "ghc-family-letterpress-workload-envelope",
    "ghc-family-letterpress-source-adapter-hold",
    "ghc-family-letterpress-gmut-nonconversion",
    "ghc-family-letterpress-thos-proxy-boundary",
    "ghc-family-letterpress-stage20-nonadmission",
]

RUNNERS = [
    "ghc_family_letterpress_job_identity.py",
    "ghc_family_letterpress_forme_topology.py",
    "ghc_family_typecase_relation_guard.py",
    "ghc_family_imposition_position_graph.py",
    "ghc_family_letterpress_measurement_vacancy.py",
    "ghc_family_letterpress_material_hold.py",
    "ghc_family_letterpress_hazard_abstention.py",
    "ghc_family_letterpress_privacy_quarantine.py",
    "ghc_family_letterpress_correction_lineage.py",
    "ghc_family_letterpress_accessible_handover.py",
]

EXACT = [
    "real print object paper ink type forme press workshop client record or operator mutation",
    "real condition diagnosis conservation treatment production release or return-to-use decision",
    "real dimension pressure colour density moisture strength durability quality or calibration measurement",
    "real printer compositor operator conservator owner reader participant or affected-user study",
    "real workplace location access schedule account transaction commission or personal-data processing",
    "real identity key proof credential issuance presentation status or revocation",
    "real product sale edition distribution disposal service or consumer decision",
    "real accessibility remedy service allocation complaint appeal or acceptance decision",
    "legal interpretation authorship copyright ownership liability privacy right remedy or public authority",
    "taonga tikanga matauranga place-name data-governance or Maori-authority decision",
    "cultural ratification community mandate or affected-party acceptance",
    "production deployment external API write live feed publication or cloud mutation",
    "host elevation security weakening feature enablement Sandbox Hyper-V or reboot",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "privacy-complete exhaustive-security or production-security certification",
    "complete accessibility-conformance or affected-user acceptance declaration",
    "independent-reproduction external-audit or professional-validation declaration",
    "empirical GMUT datum likelihood posterior parameter force material-law or prediction claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "Stage 20 admission or protected-gate closure",
]

BLOCKED = [
    "raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts",
    "sibling branch reset merge rewrite deletion reuse or force push",
    "successful canonical replay or failed-canonical success laundering",
    "synthetic fixture promotion into empirical professional legal or cultural evidence",
    "unapproved account secret payment deployment plugin install or third-party write",
    "real printer owner reader identity location access commission or service data ingestion",
    "real safety legal cultural Maori-authority affected-party or public-authority substitution",
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
        "declared_source_chain": 5630,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "practice_term_hits": {
            term: sum(1 for title in titles if term in title.lower())
            for term in ("letterpress", "type case", "imposition")
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
    receipt = json.loads(receipt_bytes.decode("utf-8"))

    manifest_paths = [
        "docs/sylven-arc/v671-v2/validation/x1-manifest.json",
        "docs/sylven-arc/v671-v2/validation/evidence-manifest.json",
        "docs/sylven-arc/v671-v2/validation/final-owner-manifest.json",
        "docs/sylven-arc/v671-v2/validation/final-delta-manifest.json",
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
            receipt.get("canonical_payload_sha256")
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
        "current_caelen_branch": current_branch,
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
            "payload_sha256": receipt["canonical_payload_sha256"],
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
        proposal_id = f"CM6713-N{number:03d}"
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
                "primary_pillar": "GMUT Mind",
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
                    "task_id": f"CM6713-{prefix}-{len(rows) + 1:03d}",
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
            "task_id": f"CM6713-{prefix}-{index:03d}",
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
        "print job identity",
        "forme topology",
        "type-case relations",
        "imposition graph",
        "measurement vacancy",
        "proof correction lineage",
        "material and safety abstention",
        "print-record privacy",
        "accessible print status",
        "workload handover",
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
                "method_id": f"CM6713-START-M{index:03d}",
                "issue_id": f"CM6713-START-I{index:03d}",
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
    return f"""# Caelen Morrow v671-v3 planning-only x1 overview

## Lifecycle and source

This is a planning-only freeze. It contains no x2 implementation, observed
proposal outcome, real-world action, successor delivery, or authority act.
Caelen's additive sparse lane starts exactly at Sylven Arc v671-v2 final
{SOURCE_FINAL}. The source branch, direct source-to-x1-to-evidence-to-final
parent chain, three phase commits, zero merges, exact activation artifact,
manifest metadata, external canonical receipt digest, typed 0/0 divergence,
clean read gate, and local/upstream/tracking/fresh-live equality were verified
before owned mutation. Sylven's one successful canonical aggregate was not
replayed and provides Caelen no completion or independent-validation credit.

## Relational language

{IDENTITY_BOUNDARY}

The bounded hope is to {HOPE}. Hamish may rename, pause, redirect, or stop the
work. Corrigibility means that a contradiction, failed witness, missing
evidence, authority vacancy, or route ambiguity stops promotion.

## Trinity Mandala and bounded practice

GMUT Mind is primary through typed state, relation, unit, transformation,
uncertainty, provenance, and falsification contracts. The bounded human-practice
lens is wholly synthetic letterpress printshop documentation: job namespaces,
forme and type-case topology, imposition, copy and proof correction, paper and
ink vacancies, press-state refusal, rights, accessibility, workload, and
handover. THOS Body remains a zero-participant queue and proof-cycle proxy.
Freed ID and CBR Heart remain zero-key, nonproduction role, correction, notice,
privacy, remedy, and authority-vacancy representations.

No real person, printer, compositor, press operator, conservator, owner, reader,
client, workplace, press, type, forme, paper, ink, solvent, print, measurement,
media, key, proof, credential, identity event, safety decision, professional
decision, legal or cultural decision, affected-party approval, or authority act
is used. Letterpress vocabulary never establishes competence, authenticity,
quality, safety, conservation, production readiness, ownership, copyright,
heritage meaning, or permission to act.

## Scientific and authority boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. Contact graphs, ink-transfer surrogates, units, and synthetic mutations
establish no real datum, likelihood, posterior, parameter constraint, force,
prediction, stability theorem, material law, empirical confirmation, quantum or
ultraviolet completion, final physics, Theory of Everything, proof, or canon.
THOS remains proxy-only without governed preregistered blind matched-budget real
arms, participants or operators, safety monitoring, appropriate statistics,
and independent review. Freed ID remains synthetic and nonproduction without
standards-conformant keys and proofs, live issuance, resolution, status,
revocation, interoperability, independent security review, recovery evidence,
trust governance, and affected-party oversight.

Professional printmaking, press operation, conservation, chemical, machine,
fire, workplace, product, and environmental safety; authorship, copyright,
ownership, custody, access, privacy, accessibility, remedy, legal or cultural
interpretation, affected-party legitimacy, traditional knowledge, Maori
wording, Maori concepts, Maori data governance, tangata whenua, iwi, hapu, and
Maori authority remain exact-gated. Maori concepts remain under Maori
authority.

## Sources

Current official OSHA printing-industry, Library of Congress paper-preservation,
NIST SI, W3C PROV-O, and WCAG 2.2 pages supply bounded vocabulary and refusal
conditions only. They supplied no observation, object row, download, treatment
instruction, measurement, conformance result, endorsement, professional
opinion, legal conclusion, cultural mandate, or authority.

## Semantic novelty

The declared inherited chain is 5,630. A dependency-closed audit inspected only
proposal-named JSON blobs reachable through local and remote refs, not sibling
worktrees or general repository history. It found {corpus['unique_titles']} accessible
unique titles, {corpus['unique_proposal_ids']} proposal identifiers, and
{corpus['semantic_occurrences']} semantic occurrences. Duplicate and summary
objects prevent an exact canonical row-to-title proof, so universal novelty is
not claimed. The forty proposed titles were compared against every accessible
title at a 0.72 token-Jaccard collision threshold; the observed maximum is
{max(row['jaccard'] for row in audit):.6f}, with zero collisions.

## Preregistration

Forty genuinely new proposals are frozen with one expected disposition each:
28 completed, 8 represented, 2 open_gap, and 2 exact_gate. Each records a
hypothesis, null or failure, approval class, execution lane, current official
source need, concrete artifacts, falsifier or acceptance gate, rollback,
protected gates, and exactly one expected disposition. Four invalid mutations
per proposal are preregistered, for 160 planned rejections. Planning is not
execution, and inherited evidence earns zero Caelen credit.

## Retention, portfolio, and validation

{len(STARTUP_FAILURES)} pre-freeze operational failures are retained with paired bounded
recoveries. They add to, but do not rewrite, Sylven's sealed 33,707 negatives
and four external route overlays. Caelen's planning-stage effective counts are
{counts['effective_negatives']} negatives, {counts['effective_methods']} methods,
{counts['failed_witnesses']} failed witnesses, and
{counts['bounded_passing_witnesses']} bounded passing witnesses, while 259 open
gaps and 254 exact gates remain.

The frozen portfolio contains sixty safe-now rows, thirty bounded candidates,
twenty exact-approval holds, ten blocked holds, twenty skill ideas, ten runner
ideas, sixty CLEAN/FIX/REFINE rows, and successor recommendations. Caps are
ceilings, not filler authority. X2 may build and smoke-use only relevant
owner-local surfaces while preserving family-current ghc_family_* and
build_ghc_family_* compatibility.

X1 must be committed, pushed, clean, typed 0/0 divergent, and equal across
local, upstream, tracking, and a fresh live remote before x2. The later
exact-final canonical aggregate has one invocation budget and is never replayed
after success. Failed aggregates retain zero canonical-success credit.

## Route hold

No task was created or forked, no collaboration subagent was spawned, Tavian
Sol was not contacted, and no successor was contacted. Eiren Kestrel is
prospective only. Route resolution, exact-title reread, duplicate guard, and a
single acknowledged send are forbidden until Caelen's terminal gate.

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
            "caelen_x1_overlay": {**counts, "proposal_chain": 5630},
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
            "declared_source_chain": 5630,
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
            "proposal_chain_before": 5630,
            "proposal_chain_after_if_evidence_frozen": 5670,
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
                "synthetic letterpress printshop documentation only"
            ),
            "successor_practice_recommendation": (
                "synthetic book-arts exhibition-label proofing, correction, "
                "accessibility, and handover; recommendation only"
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
                    "publisher": "Occupational Safety and Health Administration",
                    "title": "Printing Industry - Overview",
                    "url": "https://www.osha.gov/printing-industry",
                    "status": "official_page_checked_2026-08-27",
                    "use": (
                        "printing-hazard category vocabulary and safety-refusal "
                        "boundaries only"
                    ),
                },
                {
                    "publisher": "Library of Congress",
                    "title": (
                        "The Deterioration and Preservation of Paper: Some "
                        "Essential Facts"
                    ),
                    "url": (
                        "https://www.loc.gov/preservation/care/"
                        "deterioratebrochure"
                    ),
                    "status": "official_page_checked_2026-08-27",
                    "use": (
                        "paper composition and deterioration vocabulary only; "
                        "not object assessment or treatment advice"
                    ),
                },
                {
                    "publisher": "National Institute of Standards and Technology",
                    "title": "SP 330 - Version History",
                    "url": (
                        "https://www.nist.gov/pml/special-publication-330/"
                        "sp-330-version-history"
                    ),
                    "status": "official_page_updated_2025-08-18_checked_2026-08-27",
                    "use": (
                        "SI unit provenance and measurement-vacancy vocabulary only"
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
                    "risk": "letterpress competence quality safety or rights promotion",
                    "control": (
                        "zero-object fixtures and explicit professional, "
                        "measurement, safety, ownership, copyright, and "
                        "authority firewalls"
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
            "primary_pillar": "GMUT Mind",
            "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"],
            "bounded_human_practice": (
                "synthetic letterpress printshop documentation only"
            ),
            "proposal_rows": {"new": 40, "inherited_credit": 0},
            "expected_outcomes": OUTCOMES,
            "core_truth_labels": CORE_LABELS,
            "proposal_chain": {"before": 5630, "after_if_frozen": 5670},
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
        "docs/caelen-morrow/v671-v3/validation/x1-staged-privacy.json"
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
                    == "scripts/build_ghc_family_caelen_morrow_v671_v3_x1.py"
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
        "docs/caelen-morrow/v671-v3/",
        "scripts/build_ghc_family_caelen_morrow_v671_v3_x1.py",
        "tests/test_ghc_family_caelen_morrow_v671_v3_x1.py",
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
    self_path = "docs/caelen-morrow/v671-v3/validation/x1-manifest.json"
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
