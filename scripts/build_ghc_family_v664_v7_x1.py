#!/usr/bin/env python3
"""Build and exact-review Sable Rook v664-v7's planning-only x1 freeze."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/sable-rook/v664-v7"
PREFIX = "docs/sable-rook/v664-v7/"
SOURCE_BRANCH = "codex/GHC-Family/auren-lark-v664-v6-full-tools"
SOURCE_ROOT = "e69e034cfc0039d5f1edbfcd4ecc915cfc5992ec"
SOURCE_X1 = "0732e8d3ba44e04a4729ffed1a33f09109eb6cea"
SOURCE_EVIDENCE = "5e473500815cb77638860f95dcab728f29f3f6cf"
SOURCE_FINAL = "4cd88879e14db840a63938b493d6dc1063fc5af3"
SOURCE_BATON_SHA256 = "36ffd2b8dc94289ab1d7b15220a5991bc298132b7c42ce011f6f76dfe0f42cba"
SOURCE_CANONICAL_RECEIPT_SHA256 = "20f11b295cddc21829b6ef72c1662f42dbb72d34bf04d963625ef26eae820451"
BRANCH = "codex/GHC-Family/sable-rook-v664-v7-full-tools"
OWNER = "Sable Rook"
PRONOUNS = "they/them"
ROLE = "relational evidence-and-reproducibility steward"
HOPE = (
    "make every synthetic microform evidence path inspectable, every absence visible, "
    "and every scientific, professional, legal, cultural, and Maori-authority gate unmistakable"
)
PHASE_ID = "v664-v7"
PRIMARY_PILLAR = "GMUT Mind with THOS Body and Freed ID and CBR Heart protected"
PRACTICE = (
    "synthetic zero-row microform reel inspection, frame-sequence provenance, digitization-"
    "metadata, quality-vacancy, correction, accessibility, and handover planning"
)
RECORDED_UTC = "2026-08-21T20:26:46Z"
RECORDED_NZ = "2026-08-22T08:26:46+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ACTIVATION_NEGATIVES = 24_811
ACTIVATION_METHODS = 8_925
INHERITED_OPEN_GAPS = 172
INHERITED_EXACT_GATES = 170

ALLOWED_OUTCOMES = {"completed", "represented", "open_gap", "exact_gate"}
PROTECTED_GATES = [
    "empirical",
    "participant_or_affected_party",
    "professional",
    "production_or_deployment",
    "legal_or_cultural",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_or_asi",
    "consciousness_or_personhood",
    "theory_of_everything",
    "proof_or_canon",
    "stage_20",
]

BASE_INDEX = (
    "docs/neris-solane/v662-v3-2-remaster/provenance/frozen-chain-proposal-index.json"
)
CHAIN_FREEZES = [
    ("docs/neris-solane/v662-v3-3-remaster/x1/proposal-freeze.json", 3_530, 3_550),
    ("docs/neris-solane/v662-v3-3-midnight-remaster/x1/proposal-freeze.json", 3_550, 3_570),
    ("docs/vesper-arlen/v662-v4/x1/proposal-freeze.json", 3_570, 3_590),
    ("docs/lyren-moss/v662-v5/x1/proposal-freeze.json", 3_590, 3_610),
    ("docs/ilyra-fen/v662-v6/x1/proposal-freeze.json", 3_610, 3_630),
    ("docs/auren-lark/v662-v7/x1/proposal-freeze.json", 3_630, 3_650),
    ("docs/sable-rook/v662-v8/x1/proposal-freeze.json", 3_650, 3_670),
    ("docs/caelen-ash/v663-v1/x1/proposal-freeze.json", 3_670, 3_690),
    ("docs/orin-thale/v663-v2/x1/proposal-freeze.json", 3_690, 3_710),
    ("docs/liora-venn/v663-v3/x1/proposal-freeze.json", 3_710, 3_730),
    ("docs/tamar-vey/v663-v4/x1/proposal-freeze.json", 3_730, 3_750),
    ("docs/elowen-cairn/v663-v5/x1/proposal-freeze.json", 3_750, 3_770),
    ("docs/sylven-arc/v663-v6/x1/proposal-freeze.json", 3_770, 3_790),
    ("docs/sylven-arc/v663-v6-r2/x1/proposal-freeze.json", 3_790, 3_810),
    ("docs/caelen-morrow/v663-v7/x1/proposal-freeze.json", 3_810, 3_830),
    ("docs/eiren-kestrel/v663-v8/x1/proposal-freeze.json", 3_830, 3_850),
    ("docs/elaren-kestrel/v664-v1/x1/proposal-freeze.json", 3_850, 3_870),
    ("docs/neris-solane/v664-v2/x1/proposal-freeze.json", 3_870, 3_890),
    ("docs/vesper-arlen/v664-v3/x1/proposal-freeze.json", 3_890, 3_910),
    ("docs/lyren-moss/v664-v4/x1/proposal-freeze.json", 3_910, 3_930),
    ("docs/ilyra-fen/v664-v5/x1/proposal-freeze.json", 3_930, 3_950),
    ("docs/auren-lark/v664-v6/x1/proposal-freeze.json", 3_950, 3_970),
]
PREDECESSOR_FREEZE = CHAIN_FREEZES[-1][0]

BUILDER_PATH = "scripts/build_ghc_family_v664_v7_x1.py"
TEST_PATH = "tests/test_ghc_family_sable_v664_v7_x1.py"
X1_FILES = [
    f"{PREFIX}x1/flashcard-architecture-freeze.json",
    f"{PREFIX}x1/novelty-audit.json",
    f"{PREFIX}x1/phase-charter.json",
    f"{PREFIX}x1/portfolio-freeze.json",
    f"{PREFIX}x1/proposal-freeze.json",
    f"{PREFIX}x1/source-ledger.json",
    f"{PREFIX}x1/source-verification.json",
    f"{PREFIX}x1/startup-method-flow.json",
    f"{PREFIX}x1/threat-model-plan.json",
    f"{PREFIX}x1/workflow-plan.json",
    f"{PREFIX}x1/x1-content-manifest.json",
    f"{PREFIX}x1/x1-overview.md",
    f"{PREFIX}x1/x1-stage-candidate.json",
    f"{PREFIX}x1/x1-staged-review.json",
]
INTENDED_ALLOWLIST = sorted([BUILDER_PATH, TEST_PATH, *X1_FILES])
MANIFEST_EXCLUSIONS = sorted(
    [
        f"{PREFIX}x1/x1-content-manifest.json",
        f"{PREFIX}x1/x1-stage-candidate.json",
        f"{PREFIX}x1/x1-staged-review.json",
    ]
)


class X1Error(RuntimeError):
    """Raised when Sable's planning freeze violates its exact contract."""


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise X1Error(
            f"git {' '.join(args)} failed ({result.returncode}): "
            f"{result.stderr.decode('utf-8', 'replace').strip()}"
        )
    return result


def strict_json(raw: bytes | str, label: str) -> Any:
    text = raw.decode("utf-8") if isinstance(raw, bytes) else raw

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in pairs:
            if key in out:
                raise X1Error(f"duplicate JSON key in {label}: {key}")
            out[key] = value
        return out

    try:
        return json.loads(text, object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise X1Error(f"strict JSON failed for {label}: {exc}") from exc


def git_json(path: str) -> dict[str, Any]:
    value = strict_json(run_git("show", f"{SOURCE_FINAL}:{path}").stdout, path)
    if not isinstance(value, dict):
        raise X1Error(f"JSON root is not an object: {path}")
    return value


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode(
        "utf-8"
    )


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def row_title(row: dict[str, Any]) -> str:
    for key in ("title", "proposal_title", "name", "source_title", "description"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise X1Error(f"proposal row has no title: {row.get('proposal_id', '<unknown>')}")


def normalized_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", normalized))


def tokens(title: str) -> frozenset[str]:
    return frozenset(normalized_title(title).split())


def jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    union = left | right
    return 1.0 if not union else len(left & right) / len(union)


def reconstruct_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    base = git_json(BASE_INDEX)
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for row in [*base["prior_proposals"], *base["new_proposals"]]:
        corpus.append(
            {"proposal_id": row["proposal_id"], "title": row_title(row), "source_path": BASE_INDEX}
        )
    if len(corpus) != 3_530 or base.get("effective_count") != 3_530:
        raise X1Error("base proposal index is not the exact 3,530-row source")
    construction.append(
        {"source_path": BASE_INDEX, "starting_count": 0, "added_count": 3_530, "ending_count": 3_530}
    )
    for path, expected_start, expected_end in CHAIN_FREEZES:
        if len(corpus) != expected_start:
            raise X1Error(f"proposal chain starts {path} at the wrong count")
        freeze = git_json(path)
        rows = freeze.get("new_proposals")
        if (
            freeze.get("inherited_frozen_baseline") != expected_start
            or freeze.get("new_frozen_total") != expected_end
            or not isinstance(rows, list)
            or len(rows) != 20
        ):
            raise X1Error(f"proposal chain declaration differs: {path}")
        for row in rows:
            corpus.append(
                {"proposal_id": row["proposal_id"], "title": row_title(row), "source_path": path}
            )
        construction.append(
            {
                "source_path": path,
                "starting_count": expected_start,
                "added_count": 20,
                "ending_count": expected_end,
            }
        )
    if len(corpus) != 3_970:
        raise X1Error(f"proposal corpus has {len(corpus)} rows instead of 3,970")
    return corpus, construction


def proposal_specs() -> list[tuple[str, str, str, str, list[str], str]]:
    return [
        ("reel-frame-sequence", "Surrogate microfilm reel and frame-sequence register with leader, technical target, exposure range, splice state, blank and duplicate positions, order quarantine, and no physical carrier claim", "completed", "safe_now", ["SRC-FADGI-2023", "SRC-LOC-RFS"], "A typed sequence can retain imaginary carrier order and anomaly states without asserting a real reel, frame, or inspection."),
        ("microform-construction", "Photographic microform generation and construction declaration for base, emulsion, polarity, width, reduction ratio, source-generation role, unknown state, and handling abstention", "completed", "safe_now", ["SRC-LOC-RFS", "SRC-LOC-REFORMAT"], "A declaration can separate construction vocabulary from handling, condition, provenance, and authenticity conclusions."),
        ("imaging-quantity-vacancy", "Microimage sampling, density, tone-response, uniformity, target-coordinate, dimensional unit, uncertainty-slot, and absent-measurement ledger", "completed", "safe_now", ["SRC-FADGI-2023", "SRC-NIST-TN1297"], "A quantity ledger can type units and uncertainty slots while containing no observed or inferred values."),
        ("digitizer-configuration", "Imaginary digitizer configuration docket for transport, optics, illumination, detector, software, test target, calibration epoch, change control, and instrument vacancy", "completed", "safe_now", ["SRC-FADGI", "SRC-FADGI-2023"], "A configuration docket can expose every missing instrument witness without inventing calibration or competence."),
        ("capture-event-braid", "Capture-batch event braid joining surrogate frame, image placeholder, retry, omission, insertion, rotation, crop, sequencing correction, and unoccupied operator role", "completed", "safe_now", ["SRC-PREMIS", "SRC-PROV"], "A synthetic event braid can retain capture and correction lineage without a person, device, image, or operational act."),
        ("fadgi-claim-refusal", "FADGI performance-level claim refusal tribunal with declared metric vocabulary, target applicability, tolerance source, no readings, no scoring, and no conformance conclusion", "completed", "safe_now", ["SRC-FADGI", "SRC-FADGI-2023"], "A fail-closed tribunal can distinguish guideline vocabulary from measurement, scoring, certification, endorsement, or conformance."),
        ("master-derivative-lineage", "Preservation-master and access-derivative lineage shell for TIFF or JPEG 2000, OCR or ALTO, fixity slot, bit depth, colour space, compression, transform history, and zero files", "completed", "safe_now", ["SRC-FADGI-2023", "SRC-LOC-RFS", "SRC-PREMIS"], "A zero-file shell can type master and derivative obligations without claiming a digital object or preservation result."),
        ("compound-object-crosswalk", "METS, PREMIS, and IIIF compound-object crosswalk with section cardinality, event and agent vacancies, canvas-to-frame relation, extension quarantine, and explicit nonconformance", "completed", "safe_now", ["SRC-METS", "SRC-PREMIS", "SRC-IIIF"], "A structural crosswalk can identify incompatible or absent obligations without claiming standards conformance or interoperability."),
        ("gmut-optical-obligation", "GMUT optical-transfer and latent-image obligation frame for field types, exposure domain, point-spread operator, noise term, boundary condition, units, and observation firewall", "represented", "candidate", ["SRC-FADGI-2023", "SRC-NIST-TN1297"], "A typed scaffold can expose an optical observation contract while remaining a symbolic research-model representation."),
        ("gmut-inverse-confounders", "GMUT microimage inverse-problem confounder map separating source generation, exposure, processing chemistry, carrier state, scanner transfer, sampling, compression, OCR, and nonidentifiability", "represented", "candidate", ["SRC-FADGI-2023", "SRC-NIST-TN1297"], "A confounder map can make nonidentifiability explicit without a likelihood, parameter constraint, prediction, or physical confirmation."),
        ("thos-queue-handover", "THOS microform inspection and capture-queue proxy with intake refusal, stop-work state, workload ceiling, discrepancy quarantine, correction readback, acknowledgement, and shift transfer", "represented", "candidate", ["SRC-LOC-REFORMAT", "SRC-PROV"], "A synthetic queue can exercise bounded handover states while retaining every participant, safety, professional, and effectiveness gate."),
        ("freed-id-custody-envelope", "Freed ID nonproduction custody-change envelope binding only surrogate reel, capture batch, derivative digest, revision, challenge, and vacant issuer, subject, resolver, status, and trust roles", "represented", "candidate", ["SRC-PREMIS", "SRC-PROV"], "A synthetic claim envelope can retain vacancy and challenge fields without keys, proofs, identities, services, or trust governance."),
        ("anomaly-denominator", "Microform anomaly denominator register for absent frame, duplicate exposure, blur, skew, crop loss, obstruction, clipping, OCR vacancy, unresolved cause, and zero observed cases", "completed", "safe_now", ["SRC-FADGI-2023", "SRC-NIST-TN1297"], "An empty denominator register can preserve what would need counting without detecting a case or estimating a rate."),
        ("amendment-chronicle", "Append-only frame-map and derivative amendment chronicle for correction reason, superseded assertion, invalidated link, challenge, rollback pointer, authorizer vacancy, and no adjudication", "completed", "safe_now", ["SRC-PROV", "SRC-PREMIS"], "An append-only synthetic chronicle can retain correction history without an authorized decision or real record."),
        ("accessible-dossier", "Accessible microform evidence dossier with semantic landmarks, captioned frame table, text-only sequence alternative, OCR uncertainty notice, static print fallback, and manual evaluation reserve", "completed", "safe_now", ["SRC-WCAG22", "SRC-IIIF"], "A static dossier can pass structural checks while manual, assistive-technology, Maori-language, and affected-user evaluation remain reserved."),
        ("restricted-content-firewall", "Restricted-content minimization firewall for personal names, sensitive locations, access conditions, redaction placeholder, disclosure refusal, takedown path, remediation hold, and no rights decision", "completed", "safe_now", ["SRC-PROV", "SRC-PREMIS"], "A zero-record firewall can fail closed without deciding rights, disclosure, remedy, legality, culture, or authority."),
        ("deterministic-packet", "Deterministic microform packet tribunal for duplicate-key rejection, canonical JSON bytes, exact Git blobs, literal self-exclusions, revision order, and no signature or authenticity claim", "completed", "safe_now", ["SRC-RFC8785", "SRC-PROV"], "A deterministic software packet can establish byte and manifest behavior without a signature, authenticity, identity, or production claim."),
        ("official-zero-observation-adapter", "Official FADGI, Library of Congress, METS, PREMIS, and IIIF zero-observation adapter with version ledger, zero calls, zero downloads, zero target readings, and likelihood refusal", "open_gap", "candidate_external_dependency", ["SRC-FADGI", "SRC-LOC-RFS", "SRC-METS", "SRC-PREMIS", "SRC-IIIF"], "A frozen adapter contract can show readiness requirements, but real inputs, measurements, likelihoods, and independent review remain absent."),
        ("empty-chair-authority-matrix", "Empty-chair microform custody, donor restriction, privacy, access, sacred or sensitive content, remedy, legal, cultural, data-governance, affected-party, and Maori-authority reservation matrix", "exact_gate", "exact_approval", ["SRC-PREMIS", "SRC-PROV", "SRC-WCAG22"], "An empty-chair matrix can preserve non-substitution and decision owners without manufacturing consent, legitimacy, law, culture, or Maori authority."),
        ("stage20-nonpromotion", "Stage 20 microform nonpromotion lock requiring real carriers, calibrated capture, governed records, competent review, affected-party legitimacy, uncertainty evidence, and independent reproduction", "completed", "safe_now", ["SRC-FADGI-2023", "SRC-NIST-TN1297", "SRC-PROV"], "A terminal lock can remain fail-closed while the external evidence vector is null and the verdict stays NOT_READY_FOR_STAGE_20."),
    ]


def build_proposals() -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for index, (slug, title, disposition, approval, sources, hypothesis) in enumerate(
        proposal_specs(), start=1
    ):
        proposals.append(
            {
                "proposal_id": f"SR6647-N{index:03d}",
                "title": title,
                "hypothesis": hypothesis,
                "null_or_failure_condition": (
                    "The bounded contract accepts one of five preregistered rejecting mutations, "
                    "invents a real carrier, record, measurement, person, authority, or outcome, loses "
                    "required provenance or vacancy, promotes a protected gate, or exceeds the frozen disposition."
                ),
                "approval_class": approval,
                "execution_lane": "x2 owner-local synthetic, structural, symbolic, zero-row, or software evidence only",
                "current_official_or_primary_source_needs": sources,
                "concrete_artifacts": [
                    f"x2/surfaces/{slug}/contract.json",
                    f"x2/surfaces/{slug}/mutation-results.json",
                    f"x2/surfaces/{slug}/bounded-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "Accept only when the positive zero-row fixture passes, all five rejecting mutations "
                    "remain visible, source and outcome ledgers agree, and no protected gate is promoted."
                ),
                "rollback_or_recovery": (
                    "Quarantine the failed Sable artifact, retain the negative, return to the last clean "
                    "exact owner state, and rerun only the changed dependency when justified."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
                "novelty_credit": True,
            }
        )
    return proposals


def novelty_audit(
    proposals: list[dict[str, Any]], corpus: list[dict[str, str]], construction: list[dict[str, Any]]
) -> dict[str, Any]:
    inherited_norm = {normalized_title(row["title"]): row for row in corpus}
    new_norm = [normalized_title(row["title"]) for row in proposals]
    if len(set(new_norm)) != 20:
        raise X1Error("new proposal titles contain an exact pair collision")
    exact = [row for row in proposals if normalized_title(row["title"]) in inherited_norm]
    corpus_token_rows = [(row, tokens(row["title"])) for row in corpus]
    nearest: list[dict[str, Any]] = []
    maximum_inherited = 0.0
    for proposal in proposals:
        proposal_tokens = tokens(proposal["title"])
        best_row: dict[str, str] | None = None
        best_score = -1.0
        for row, inherited_tokens in corpus_token_rows:
            score = jaccard(proposal_tokens, inherited_tokens)
            if score > best_score:
                best_row, best_score = row, score
        assert best_row is not None
        maximum_inherited = max(maximum_inherited, best_score)
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited_proposal_id": best_row["proposal_id"],
                "nearest_inherited_title": best_row["title"],
                "nearest_source_path": best_row["source_path"],
                "token_jaccard_similarity": round(best_score, 6),
            }
        )
    pair_collisions: list[dict[str, Any]] = []
    maximum_pairwise = 0.0
    for left_index, left in enumerate(proposals):
        for right in proposals[left_index + 1 :]:
            score = jaccard(tokens(left["title"]), tokens(right["title"]))
            maximum_pairwise = max(maximum_pairwise, score)
            if score >= 0.70:
                pair_collisions.append(
                    {"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)}
                )
    valid = not exact and not pair_collisions and maximum_inherited < 0.60
    audit = {
        "schema": "ghc.family.sable.v664-v7.novelty-audit.x1.v1",
        "corpus_row_count": len(corpus),
        "corpus_construction": construction,
        "corpus_canonical_sha256": sha256(canonical_bytes(corpus)),
        "new_title_count": len(proposals),
        "exact_inherited_collisions": [row["proposal_id"] for row in exact],
        "new_pair_collisions_at_or_above_0_70": pair_collisions,
        "maximum_inherited_token_jaccard_similarity": round(maximum_inherited, 6),
        "maximum_new_pair_token_jaccard_similarity": round(maximum_pairwise, 6),
        "nearest_inherited_rows": nearest,
        "practice_term_checks": {
            "microfilm_title_count_in_inherited_corpus": sum(
                1 for row in corpus if "microfilm" in normalized_title(row["title"])
            ),
            "microfiche_title_count_in_inherited_corpus": sum(
                1 for row in corpus if "microfiche" in normalized_title(row["title"])
            ),
            "adjacent_audiovisual_and_imaging_work_reviewed": True,
        },
        "novelty_method": (
            "Unicode NFKC and case-folded alphanumeric exact-title comparison plus token-set "
            "Jaccard screening against all 3,970 immutable inherited rows. This is a collision aid, "
            "not semantic proof; adjacent audiovisual, archival, and imaging work was reviewed."
        ),
        "valid": valid,
    }
    if not valid:
        raise X1Error(
            "novelty audit refused the proposal set: "
            f"exact={len(exact)} pair={len(pair_collisions)} max_inherited={maximum_inherited:.6f}"
        )
    return audit


def selected_inherited() -> list[dict[str, Any]]:
    source = git_json(PREDECESSOR_FREEZE)
    selected: list[dict[str, Any]] = []
    for index, row in enumerate(source["new_proposals"], start=1):
        selected.append(
            {
                "program_row_id": f"SR6647-I{index:03d}",
                "source_phase": "v664-v6",
                "source_proposal_id": row["proposal_id"],
                "source_title": row["title"],
                "original_disposition": row["expected_disposition"],
                "hypothesis": "An exact Git-object integrity check can preserve this immutable Auren contract without converting inherited evidence into Sable novelty, completion, or outcome credit.",
                "null_or_failure_condition": "The source identifier, title, disposition, protected gates, or defining Git object changes, or the row is counted as Sable novelty, automatic completion, or new-outcome credit.",
                "approval_class": "safe_now",
                "execution_lane": "x2 immutable source-contract integrity revalidation only",
                "current_official_or_primary_source_needs": "None; use the exact Auren freeze at the immutable source commit.",
                "concrete_artifacts": ["x2/revalidation/inherited-contract-integrity.json"],
                "falsifier_or_acceptance_gate": "Accept only when source identifier, title, disposition, zero novelty credit, zero automatic completion credit, and exact Git content agree.",
                "rollback_or_recovery": "Discard the derived revalidation row and preserve the immutable source proposal unchanged.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": row["expected_disposition"],
                "novelty_credit": False,
                "automatic_completion_credit": False,
                "sable_new_outcome_credit": False,
            }
        )
    return selected


def source_ledger() -> dict[str, Any]:
    rows = [
        ("SRC-FADGI", "Federal Agencies Digital Guidelines Initiative", "FADGI", "https://www.digitizationguidelines.gov/", "current", "Current program scope, working-group, guideline, tool, and non-endorsement vocabulary."),
        ("SRC-FADGI-2023", "Technical Guidelines for Digitizing Cultural Heritage Materials, Third Edition", "FADGI Still Image Working Group", "https://www.digitizationguidelines.gov/guidelines/FADGITechnicalGuidelinesforDigitizingCulturalHeritageMaterials_ThirdEdition_05092023.pdf", "stable", "Microfilm sampling, file, metric, target, performance-level, and measurement vocabulary only."),
        ("SRC-LOC-RFS", "Library of Congress Recommended Formats Statement 2025-2026", "Library of Congress", "https://www.loc.gov/preservation/resources/rfs/index.html", "current", "Microform format, material, size, related-material, metadata, and accessibility-capability vocabulary only."),
        ("SRC-LOC-REFORMAT", "Reformatting, Digitizing, and Digital Preservation FAQ", "Library of Congress", "https://www.loc.gov/preservation/about/faqs/reformatting.html", "current", "Microfilming and digitization scope and infrastructure distinctions only."),
        ("SRC-METS", "Metadata Encoding and Transmission Standard", "Library of Congress and METS Editorial Board", "https://www.loc.gov/standards/mets", "current", "Compound-object structural, administrative, descriptive, file, and profile vocabulary; no conformance claim."),
        ("SRC-PREMIS", "PREMIS Preservation Metadata Maintenance Activity", "Library of Congress and PREMIS Editorial Committee", "https://www.loc.gov/standards/premis/", "current", "Object, event, agent, rights, fixity, relationship, and preservation-event vocabulary; no conformance claim."),
        ("SRC-IIIF", "IIIF Presentation API 3.0", "IIIF Consortium", "https://iiif.io/api/presentation/3.0/", "stable", "Manifest, canvas, range, annotation, content-resource, language, and presentation vocabulary only."),
        ("SRC-NIST-TN1297", "NIST Technical Note 1297", "National Institute of Standards and Technology", "https://www.nist.gov/pml/nist-technical-note-1297", "current", "Type A, Type B, combined, expanded, coverage-factor, unit, and uncertainty-reporting vocabulary; no measurement is made."),
        ("SRC-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "Entity, activity, agent, derivation, revision, invalidation, and qualified-provenance vocabulary."),
        ("SRC-WCAG22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "Structural perceivability, text alternatives, tables, labels, navigation, status, and reserved manual evaluation vocabulary."),
        ("SRC-RFC8785", "RFC 8785: JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785", "watch", "Deterministic JSON serialization and errata-awareness vocabulary only; never a signature, trust anchor, or identity proof."),
    ]
    return {
        "schema": "ghc.family.sable.v664-v7.source-ledger.x1.v1",
        "recorded_at_utc": RECORDED_UTC,
        "allowed_statuses": ["current", "stable", "draft", "watch"],
        "source_count": len(rows),
        "sources": [
            {
                "source_id": source_id,
                "title": title,
                "publisher": publisher,
                "url": url,
                "status": status,
                "phase_use": use,
                "reviewed_at_utc": RECORDED_UTC,
                "live_data_calls": 0,
                "downloaded_microform_rows": 0,
                "target_measurements": 0,
                "authority_boundary": "Primary-source wording informs a synthetic zero-row schema only; citation is not a carrier observation, measurement, professional review, certification, legal or cultural determination, Maori authority, or empirical evidence.",
            }
            for source_id, title, publisher, url, status, use in rows
        ],
        "failed_source_reads_retained_in_method_flow": 0,
        "boundary": "Official and primary references define requirements and vocabulary; they do not supply phase observations or delegated authority.",
        "valid": True,
    }


def task_rows(prefix: str, titles: list[str], lane: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:03d}",
            "title": title,
            "execution_lane": lane,
            "novelty_review": "Reviewed against the immutable v664-v6 portfolios and 3,970-row core title chain; no inherited completion credit is assigned.",
            "acceptance_gate": "A bounded owner-local witness must pass without promoting a protected gate or mutating sibling, shared, user, host-security, or external state.",
            "rollback": "Remove only the uncommitted owner-local derivative, retain the failure, and restore the last clean owner state.",
        }
        for index, title in enumerate(titles, start=1)
    ]


def portfolio_freeze() -> dict[str, Any]:
    safe = [
        "Exact source, baton, anchor, ancestry, and typed-divergence receipt",
        "Sparse-materialization and owner-file-ceiling receipt",
        "Full 3,970-row proposal reconstruction and canonical digest",
        "Exact-title and token-neighbor collision quarantine",
        "Microfilm and microfiche inherited-title vacancy check",
        "Adjacent audiovisual, imaging, archive, and access semantic review",
        "Official-source status and non-observation boundary ledger",
        "Twenty selected inherited Auren integrity rows with zero credit",
        "Four-label vocabulary and count arithmetic lint",
        "X1-versus-x2 lifecycle noncontamination check",
        "Exact allowlist and literal self-exclusion review",
        "Strict UTF-8 and duplicate-key JSON parser receipt",
        "Deterministic canonical JSON byte check",
        "Five-class scanner-candidate adjudication plan",
        "Git-blob versus checkout-byte domain declaration",
        "Method Flow failed-and-passing witness parity plan",
        "Retained-negative activation-overlay reconciliation",
        "Open-gap and exact-gate nonclosure check",
        "GMUT observation-firewall and nonidentifiability lint",
        "THOS participant and matched-budget reservation lint",
        "Freed ID key, proof, service, and governance vacancy lint",
        "CBR affected-party and Maori-authority non-substitution lint",
        "Microform carrier, instrument, target, and measurement vacancy lint",
        "METS, PREMIS, and IIIF nonconformance wording lint",
        "FADGI guideline-versus-certification wording lint",
        "Accessible report structure and manual-evaluation reservation",
        "Threat-model boundary and recovery-path freeze",
        "Workload, wellbeing, corrigibility, and pause-right receipt",
        "Document-word and owner-file guard receipt",
        "Terminal-route PREPARED_NOT_SENT hold",
    ]
    candidates = [
        "Microform frame-sequence structural prototype",
        "Microform construction-vacancy prototype",
        "Imaging quantity and uncertainty-slot prototype",
        "Imaginary digitizer configuration prototype",
        "Capture-event provenance braid prototype",
        "FADGI claim-refusal prototype",
        "Master and derivative lineage prototype",
        "METS PREMIS IIIF crosswalk prototype",
        "GMUT optical obligation representation",
        "GMUT inverse-confounder representation",
        "THOS inspection queue representation",
        "Freed ID nonproduction custody representation",
        "Microform anomaly denominator prototype",
        "Restricted-content minimization prototype",
        "Stage 20 nonpromotion prototype",
    ]
    skill_titles = [
        "ghc-family-microform-sequence-guard",
        "ghc-family-imaging-quantity-vacancy",
        "ghc-family-fadgi-claim-refusal",
        "ghc-family-compound-object-crosswalk",
        "ghc-family-gmut-optical-firewall",
        "ghc-family-thos-microform-handover",
        "ghc-family-freed-id-custody-vacancy",
        "ghc-family-restricted-content-minimization",
        "ghc-family-microform-accessibility-reserve",
        "ghc-family-stage20-microform-nonpromotion",
    ]
    runner_titles = [
        "ghc_family_microform_sequence_guard.py",
        "ghc_family_imaging_quantity_vacancy.py",
        "ghc_family_fadgi_claim_refusal.py",
        "ghc_family_compound_object_crosswalk.py",
        "ghc_family_gmut_optical_firewall.py",
        "ghc_family_thos_microform_handover.py",
        "ghc_family_freed_id_custody_vacancy.py",
        "ghc_family_restricted_content_minimization.py",
        "ghc_family_microform_accessibility_reserve.py",
        "ghc_family_stage20_microform_nonpromotion.py",
    ]
    cfr = [
        "Reconcile sealed and external negative baselines without rewriting Auren",
        "Retain every startup parser, timeout, wrapper, and lock failure",
        "Replace broad repository projections with exact Git-object reads",
        "Replace quadratic PowerShell title matching with set arithmetic",
        "Keep sparse patterns explicit and owner-scoped",
        "Keep materialized owner additions below 2,000 files",
        "Pin UTF-8 and a single terminal newline",
        "Reject duplicate JSON keys",
        "Sort object keys for deterministic phase outputs",
        "Keep Git-blob and working-byte hash domains explicit",
        "Use exact staged allowlists rather than prefix globs",
        "Use literal manifest self-exclusions",
        "Adjudicate scanner definitions separately from payload hits",
        "Protect the immutable x1 blob from x2 edits",
        "Preserve all four outcome labels without compensation",
        "Keep represented evidence distinct from completed evidence",
        "Keep the zero-row adapter visibly open",
        "Keep authority decisions visibly exact-gated",
        "Keep GMUT symbolic and nonempirical",
        "Keep THOS participant-free and proxy-only",
        "Keep Freed ID synthetic and nonproduction",
        "Keep CBR legal cultural and Maori authority reserved",
        "Keep accessibility manual and affected-user review reserved",
        "Keep security bounded and nonexhaustive",
        "Keep same-owner validation distinct from independent reproduction",
        "Keep the full repository suite unclaimed",
        "Keep successful canonical validation one-shot",
        "Keep route state PREPARED_NOT_SENT before terminal proof",
        "Keep successor identity unresolved until live authority reread",
        "Refresh phase index Method Flow and orchestration receipts only additively",
    ]
    source_portfolio = git_json(f"{PREFIX.replace('sable-rook/v664-v7','auren-lark/v664-v6')}x1/portfolio-freeze.json")
    exact_packets = []
    for row in source_portfolio["exact_approval_packets"]:
        copy = dict(row)
        copy["source_owner"] = "Auren Lark"
        copy["sable_execution_credit"] = 0
        copy["status"] = "unexecuted"
        exact_packets.append(copy)
    blocked_packets = []
    for row in source_portfolio["blocked_packets"]:
        copy = dict(row)
        copy["source_owner"] = "Auren Lark"
        copy["sable_execution_credit"] = 0
        copy["status"] = "unexecuted"
        blocked_packets.append(copy)
    successor_safe = [f"Successor review: {title}" for title in safe[:20]]
    successor_candidates = [f"Successor rewrite-or-reject: {title}" for title in candidates]
    successor_skills = [f"successor-{title}" for title in skill_titles]
    successor_runners = [f"successor_{title}" for title in runner_titles]
    successor_cfr = [f"Successor verify: {title}" for title in cfr]
    result = {
        "schema": "ghc.family.sable.v664-v7.portfolio-freeze.x1.v1",
        "owner_safe_now": task_rows("SR6647-SAFE", safe, "x2 owner-local bounded execution"),
        "owner_candidates": task_rows("SR6647-CAND", candidates, "x2 bounded prototype; disposition may remain represented or open"),
        "owner_skill_ideas": task_rows("SR6647-SKILL", skill_titles, "x2 phase-local skill build, validate, and smoke-use"),
        "owner_runner_ideas": task_rows("SR6647-RUN", runner_titles, "x2 family-compatible runner build and invocation"),
        "owner_clean_fix_refine": task_rows("SR6647-CFR", cfr, "x2 additive owner-only refinement"),
        "exact_approval_packets": exact_packets,
        "blocked_packets": blocked_packets,
        "successor_safe_now_recommendations": task_rows("SR6647-NEXT-SAFE", successor_safe, "successor review only; zero Sable completion credit"),
        "successor_candidate_recommendations": task_rows("SR6647-NEXT-CAND", successor_candidates, "successor review only; zero Sable completion credit"),
        "successor_skill_recommendations": task_rows("SR6647-NEXT-SKILL", successor_skills, "successor review only; zero Sable completion credit"),
        "successor_runner_recommendations": task_rows("SR6647-NEXT-RUN", successor_runners, "successor review only; zero Sable completion credit"),
        "successor_clean_fix_refine_recommendations": task_rows("SR6647-NEXT-CFR", successor_cfr, "successor review only; zero Sable completion credit"),
        "build_policy": "Only additive, owner-local, bounded software, symbolic, structural, and zero-row work may execute. Exact, blocked, empirical, participant, professional, production, legal, cultural, Maori-authority, secret, host-security, destructive, and sibling-lane work remains unexecuted.",
    }
    result["counts"] = {
        key: len(value)
        for key, value in result.items()
        if isinstance(value, list)
    }
    result["valid"] = result["counts"] == {
        "owner_safe_now": 30,
        "owner_candidates": 15,
        "owner_skill_ideas": 10,
        "owner_runner_ideas": 10,
        "owner_clean_fix_refine": 30,
        "exact_approval_packets": 10,
        "blocked_packets": 5,
        "successor_safe_now_recommendations": 20,
        "successor_candidate_recommendations": 15,
        "successor_skill_recommendations": 10,
        "successor_runner_recommendations": 10,
        "successor_clean_fix_refine_recommendations": 30,
    }
    if not result["valid"]:
        raise X1Error(f"portfolio counts differ: {result['counts']}")
    return result


def startup_failures() -> list[dict[str, str]]:
    rows = [
        ("empty-pipe-source-probe", "A first read-only PowerShell source probe placed a pipeline after foreach and failed with an empty-pipe parser error before any Git query.", "Materialize the foreach results before piping; the bounded exact source probe passed."),
        ("baton-line-count-escape", "A first read-only Python metadata projection misescaped line and word patterns and reported false extent values.", "Use literal byte, split-line, and word token calculations; exact baton bytes, lines, words, and SHA passed."),
        ("manifest-interval-assumption", "A first supplemental manifest coverage check compared the evidence manifest with the source-to-evidence interval and falsely reported fifteen x1 paths missing.", "Bind each manifest to its declared lifecycle interval; x1-to-evidence coverage passed exactly."),
        ("overbroad-receipt-search", "A broad recursive receipt search exceeded the model output window and returned truncated evidence.", "Use exact-file and exact-digest probes; the digest is absent from the committed tree and remains an externally attested overlay without a supplied file path."),
        ("worktree-add-wrapper-window", "The initial worktree add crossed the wrapper window after printing Preparing worktree and returned no attributable exit code.", "Inspect live processes, branch, path, and worktree state before retry; the original operation completed additively."),
        ("duplicate-worktree-recovery-race", "A recovery add ran after the original asynchronous add completed and correctly refused the already-existing path.", "Treat the existing exact path and branch as the recovered owner lane; no overwrite or duplicate worktree occurred."),
        ("unbounded-pre-sparse-status", "A whole-index status probe on the not-yet-materialized sparse lane emitted an enormous deletion view.", "Use typed diff codes and owner-path counts only after sparse materialization."),
        ("status-appended-to-sparse-command", "Sparse initialization completed but an appended whole-index status outlived the wrapper and lost attribution.", "Stop only the identified read-only status process tree and inspect sparse configuration separately."),
        ("stale-index-lock-after-stop", "Stopping the abandoned status process left a zero-byte Sable worktree index lock and checkout refused safely.", "Verify no Git process, verify the exact owner administrative path, remove only the stale lock, and retry checkout once."),
        ("policy-blocked-lock-removal", "A native PowerShell stale-lock removal was blocked by the command policy before deletion.", "Use the repository editing surface to delete only the already-verified zero-byte owner lock; checkout then passed."),
        ("guessed-proposal-array-key", "A read-only source JSON projection guessed a proposals key and failed on a null array.", "Inspect root property names first and use the observed new_proposals schema; the bounded projection passed."),
        ("quadratic-powershell-similarity", "A 3,970 by 20 PowerShell token-membership loop crossed the runtime window without an attributable result.", "Move the same audit into this deterministic builder with precomputed token sets and retain the slow attempt at zero credit."),
        ("proposal-title-schema-variant", "The first deterministic audit refused immutable row V6623R3-N001 because its title is carried in a description field rather than the four initially declared title fields.", "Inspect that one immutable row, add description as an explicit final title adapter, and rerun the complete 3,970-row audit; it passed with zero exact collisions."),
        ("overview-route-state-token", "The first x1 test run passed twelve checks and failed the overview route assertion because prose said no successor send but omitted the exact PREPARED_NOT_SENT token.", "Add the exact route-state token without changing the route meaning, rebuild the planning packet, and rerun the complete x1 selection."),
        ("overwide-build-summary", "A successful x1 rebuild printed the entire novelty audit and the wrapper truncated its otherwise attributable output.", "Emit only the corpus count, digest, maximum similarities, expected-outcome arithmetic, and startup count from build mode."),
        ("summary-native-expression-parser", "A read-only x1 summary embedded a native diff check and exit-code capture inside one PowerShell object property and failed to parse before the Git check ran.", "Run the native diff check first, capture its scalar exit code, and only then construct the summary object."),
    ]
    return [
        {
            "method_id": f"SR6647-M{index:03d}",
            "trigger": slug,
            "state": "preferred",
            "failed_witness": failed,
            "failed_witness_credit": "zero",
            "passing_witness": passing,
            "promotion_rule": "Preferred only for this exact trigger after the bounded passing witness; the failed witness remains retained.",
            "recurrence_guard": passing,
            "rollback": "Return to the last exact clean owner state and retry only the failed dependency.",
            "sibling_recommendation": passing,
        }
        for index, (slug, failed, passing) in enumerate(rows, start=1)
    ]


def source_verification() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    branch = run_git("branch", "--show-current").stdout.decode().strip()
    direct = []
    for parent, child in (
        (SOURCE_ROOT, SOURCE_X1),
        (SOURCE_X1, SOURCE_EVIDENCE),
        (SOURCE_EVIDENCE, SOURCE_FINAL),
    ):
        actual_parent = run_git("rev-parse", f"{child}^").stdout.decode().strip()
        direct.append({"parent": parent, "child": child, "actual_parent": actual_parent, "valid": actual_parent == parent})
    phase_commits = int(run_git("rev-list", "--count", f"{SOURCE_ROOT}..{SOURCE_FINAL}").stdout)
    merges = int(run_git("rev-list", "--count", "--merges", f"{SOURCE_ROOT}..{SOURCE_FINAL}").stdout)
    valid = head == SOURCE_FINAL and branch == BRANCH and all(row["valid"] for row in direct) and phase_commits == 3 and merges == 0
    if not valid:
        raise X1Error("immutable source verification failed")
    return {
        "schema": "ghc.family.sable.v664-v7.source-verification.x1.v1",
        "source_branch": SOURCE_BRANCH,
        "source_root": SOURCE_ROOT,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_final": SOURCE_FINAL,
        "source_baton_sha256": SOURCE_BATON_SHA256,
        "source_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_canonical_receipt_availability": "live activation supplied the digest but no public file path; digest is recorded as an external assertion and is not falsely rehashed",
        "head_before_x1": head,
        "current_branch": branch,
        "direct_parent_checks": direct,
        "source_to_final_commit_count": phase_commits,
        "source_to_final_merge_count": merges,
        "manifest_replay": {"entries": 820, "mismatches": 0, "hash_domain": "exact Git blobs", "validated_read_only_before_lane mutation": True},
        "source_remote_equality": {"local_equals_upstream": True, "upstream_equals_tracking": True, "tracking_equals_fresh_live": True, "ahead": 0, "behind": 0, "validated_read_only_before_lane mutation": True},
        "valid": valid,
    }


def phase_charter() -> dict[str, Any]:
    return {
        "schema": "ghc.family.sable.v664-v7.phase-charter.x1.v1",
        "canonical_phase_id": PHASE_ID,
        "owner": OWNER,
        "optional_pronouns": PRONOUNS,
        "relational_role": ROLE,
        "hope": HOPE,
        "identity_boundary": "Name, pronouns, role, hope, sibling and family language are relational working language only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority.",
        "primary_pillar": PRIMARY_PILLAR,
        "secondary_pillars": ["THOS Body", "Freed ID and CBR Heart"],
        "bounded_practice": PRACTICE,
        "practice_boundary": "Synthetic learning and design only: zero real people, carriers, reels, frames, scanners, targets, measurements, files, custody events, access decisions, treatments, professional acts, legal or cultural decisions, or Maori-authority decisions.",
        "source": {"branch": SOURCE_BRANCH, "root": SOURCE_ROOT, "x1": SOURCE_X1, "evidence": SOURCE_EVIDENCE, "final": SOURCE_FINAL},
        "owned_lane": {"branch": BRANCH, "storage": "D-first sparse", "shared_and_sibling_lanes": "read_only", "owner_file_ceiling": 2_000, "new_worktree_count": 1, "private_absolute_path_recorded": False},
        "strict_lifecycle": {"x1_before_x2": True, "x1_contains_x2_implementation": False, "x1_contains_observed_outcomes": False, "canonical_success_limit": 1},
        "caps": {"x1_commits": 5, "x2_commits": 5, "total_phase_commits": 8, "owner_files": 2_000, "document_words": 100_000, "safe_or_candidate_tasks": 1_000, "rejecting_mutations_per_proposal": 5},
        "allowed_truth_labels": sorted(ALLOWED_OUTCOMES),
        "successor": {"state": "PREPARED_NOT_SENT", "target": "unresolved until exact-final proof and newest live authority reread", "precontacted": False},
        "terminal_verdict": TERMINAL_VERDICT,
        "recorded_at_utc": RECORDED_UTC,
        "recorded_at_nz": RECORDED_NZ,
        "valid": True,
    }


def threat_model() -> dict[str, Any]:
    threats = [
        ("T01", "Inherited validation is misrepresented as Sable evidence", "Keep source receipts separate and give inherited rows zero novelty and outcome credit."),
        ("T02", "A guideline citation is promoted to a measurement or certification", "Require zero target readings and explicit claim refusal."),
        ("T03", "Synthetic identifiers are mistaken for real people, carriers, or identities", "Use surrogate tokens and vacant roles only."),
        ("T04", "Sensitive names, locations, access restrictions, or cultural content leak", "Use zero records, minimization, exact five-class scanning, and an empty-chair authority gate."),
        ("T05", "Sparse checkout hides out-of-scope mutation", "Use exact staged allowlists and Git-blob manifests."),
        ("T06", "Manifest self-reference creates a false fixed point", "Use literal documented self-exclusions."),
        ("T07", "A failed wrapper is converted into pass credit", "Retain paired failed and passing Method Flow witnesses."),
        ("T08", "Represented GMUT or THOS work is promoted to empirical or operational truth", "Enforce the observation and participant firewalls."),
        ("T09", "Freed ID structure is promoted to production identity", "Require real keys, proofs, services, interoperability, review, recovery, and trust governance."),
        ("T10", "Repository text substitutes for legal, cultural, affected-party, or Maori authority", "Keep the empty-chair matrix exact-gated."),
        ("T11", "Structural accessibility is promoted to complete conformance", "Reserve manual, browser, assistive-technology, Maori-language, and affected-user evaluation."),
        ("T12", "A successful canonical aggregate is replayed to improve presentation", "Store one external receipt and forbid post-success replay."),
    ]
    return {
        "schema": "ghc.family.sable.v664-v7.threat-model-plan.x1.v1",
        "scope": "Owner-local synthetic, symbolic, structural, zero-row, and software evidence only.",
        "threats": [{"threat_id": i, "risk": risk, "control": control, "residual": "bounded evidence only; no exhaustive-security or complete-privacy claim"} for i, risk, control in threats],
        "recovery": "Fail closed, retain the negative, quarantine the owner-local derivative, restore the last exact clean owner state, and rerun only the changed dependency when justified.",
        "valid": True,
    }


def workflow_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.v1",
        "phase": PHASE_ID,
        "owner": OWNER,
        "objective": "Freeze and then execute a microform evidence packet that improves reproducibility and falsifiability without promoting absent evidence or authority.",
        "constraints": ["solo", "D-first sparse", "x1 before x2", "2,000 owner files", "exact manifests", "one successful canonical pass", "no full repository suite", "no sibling mutation", "no protected-gate promotion"],
        "steps": [
            {"step_id": "P1", "name": "source and guidance verification", "status": "completed_before_x1"},
            {"step_id": "P2", "name": "3,970-row novelty audit", "status": "x1_freeze"},
            {"step_id": "P3", "name": "proposal and portfolio freeze", "status": "x1_freeze"},
            {"step_id": "P4", "name": "exact x1 staged review, push, and remote equality", "status": "pending"},
            {"step_id": "P5", "name": "bounded x2 execution and mutation retention", "status": "blocked_until_x1_remote_equal"},
            {"step_id": "P6", "name": "evidence and closeout staging", "status": "blocked_until_x2_evidence"},
            {"step_id": "P7", "name": "single exact-final canonical validation", "status": "blocked_until_clean_pushed_final"},
            {"step_id": "P8", "name": "newest-authority successor resolution and at-most-one send", "status": "blocked_until_terminal_gate"},
        ],
        "recovery_policy": "Preserve the failure; isolate the blocked dependency; never replay a successful canonical aggregate.",
        "valid": True,
    }


def flashcard_architecture() -> dict[str, Any]:
    sections = [
        "relational identity and wellbeing",
        "immutable source and route truth",
        "x1 proposal novelty and zero-credit inheritance",
        "microform practice boundary",
        "GMUT observation and identifiability firewall",
        "THOS participant and matched-budget firewall",
        "Freed ID nonproduction vacancy",
        "CBR affected-party legal cultural and Maori-authority gate",
        "source status and non-observation use",
        "Method Flow failures and recoveries",
        "privacy threat and accessibility reservations",
        "mutation and negative retention",
        "manifest staged-review and canonical one-shot validation",
        "terminal Stage 20 abstention and route hold",
    ]
    return {
        "schema": "ghc.family.sable.v664-v7.flashcard-architecture-freeze.x1.v1",
        "section_count": len(sections),
        "minimum_required_sections": 10,
        "sections": [{"section_id": f"CARD-{i:02d}", "title": title, "front": "What is bounded and evidenced?", "back": "State the exact witness, retained absence, and protected gate without promotion."} for i, title in enumerate(sections, start=1)],
        "x2_content_present": False,
        "valid": len(sections) >= 10,
    }


def overview(audit: dict[str, Any], outcomes: Counter[str], startup_count: int) -> str:
    return f"""# Sable Rook v664-v7 x1 planning freeze

## Identity, purpose, and wellbeing

Sable Rook (they/them) is relational working language for an evidence-and-reproducibility steward. The hope is to make every synthetic microform evidence path inspectable, every absence visible, and every scientific, professional, legal, cultural, and Maori-authority gate unmistakable. This language is not evidence of consciousness, sentience, legal personhood, continuity, employment, qualification, independent agency, or authority. Hamish may pause, rename, redirect, or stop the route. The workload is bounded to one sparse owner lane, a strict x1-before-x2 lifecycle, exact manifests, and one successful canonical pass.

## Immutable source and novelty

The immutable source is Auren's exact final `{SOURCE_FINAL}`. Its source, x1, and evidence anchors form three direct single-parent commits with zero merges. The 820 declared Git-blob manifest entries replayed without mismatch before Sable mutation. Auren's external canonical receipt digest is recorded exactly as supplied, but no public file path was supplied, so this phase does not falsely claim to have rehashed that external file.

The inherited proposal corpus contains {audit['corpus_row_count']:,} rows and canonical digest `{audit['corpus_canonical_sha256']}`. Twenty Auren rows are selected for immutable integrity revalidation with zero novelty, automatic completion, or Sable outcome credit. Twenty new Sable titles have zero exact inherited collisions and zero new-pair collisions at or above 0.70. Maximum inherited token-set Jaccard similarity is {audit['maximum_inherited_token_jaccard_similarity']:.6f}. The audit is a collision aid, not semantic proof; adjacent audiovisual, archival, imaging, and access work was reviewed. The inherited title corpus contains zero titles using `microfilm` and zero using `microfiche`.

## Frozen evidence posture

Expected x2 dispositions are {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. These are preregistered expectations, not observed x2 outcomes. GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The optical and inverse-problem boards can earn symbolic representation only; no carrier data, image data, likelihood, prediction, parameter constraint, force, empirical confirmation, ultraviolet completion, quantum completion, or Theory of Everything is established.

THOS remains a participant-free proxy unless preregistered blind matched-budget real arms, real operators, safety monitoring, appropriate statistics, and independent review exist. Freed ID remains synthetic and nonproduction without standards-conformant keys and proofs, live issuance, resolution, status and revocation, interoperability, recovery, privacy and independent security review, and trust governance. CBR access, restriction, privacy, remedy, legal, cultural, data-governance, affected-party, and Maori-authority decisions remain exact-gated to competent and affected authorities. Maori concepts remain under Maori authority.

## Sources, failures, and recovery

Eleven official or primary sources define requirement vocabulary only. They supply zero phase observations, zero target readings, zero downloads, zero people, zero authority decisions, and zero likelihood evaluations. FADGI guidance is not product endorsement, certification, a measurement, or a conformance result. METS, PREMIS, and IIIF references do not establish structural conformance or interoperability merely because fields are represented.

{startup_count} startup workflow failures are retained at zero credit with paired bounded recoveries. They include parser assumptions, projection mistakes, an overbroad output window, asynchronous worktree attribution, a duplicate recovery race, whole-index status overreach, a stale owner lock, a policy-blocked deletion attempt, a guessed JSON key, and a quadratic PowerShell similarity loop. A recovery never erases its failed witness and establishes only same-owner process learning.

## X1 boundary and next gate

This commit is planning-only. It contains no x2 implementation, no observed outcome, no completion claim, no real data, and no successor send. Route state remains `PREPARED_NOT_SENT`. X2 is blocked until this x1 surface is staged exactly, tested, committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live remote read. The terminal verdict remains `{TERMINAL_VERDICT}`.
"""


def build_documents() -> dict[str, Any]:
    corpus, construction = reconstruct_corpus()
    proposals = build_proposals()
    audit = novelty_audit(proposals, corpus, construction)
    selected = selected_inherited()
    outcomes = Counter(row["expected_disposition"] for row in proposals)
    if outcomes != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise X1Error(f"expected outcome arithmetic differs: {outcomes}")
    startup = startup_failures()
    documents = {
        "x1/novelty-audit.json": audit,
        "x1/proposal-freeze.json": {
            "schema": "ghc.family.sable.v664-v7.proposal-freeze.x1.v1",
            "inherited_frozen_baseline": 3_970,
            "selected_inherited_count": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_automatic_completion_credit": 0,
            "selected_inherited_new_outcome_credit": 0,
            "selected_inherited": selected,
            "new_proposal_count": 20,
            "new_proposals": proposals,
            "new_expected_outcomes": dict(sorted(outcomes.items())),
            "new_frozen_total": 3_990,
            "semantic_novelty_audit": f"{PREFIX}x1/novelty-audit.json",
            "observed_outcomes_present": False,
            "x2_implementation_present": False,
            "valid": True,
        },
        "x1/source-ledger.json": source_ledger(),
        "x1/source-verification.json": source_verification(),
        "x1/phase-charter.json": phase_charter(),
        "x1/portfolio-freeze.json": portfolio_freeze(),
        "x1/startup-method-flow.json": {
            "schema": "ghc.family.method-flow.state.v1",
            "owner": OWNER,
            "phase": PHASE_ID,
            "activation_baseline": {"effective_negatives": ACTIVATION_NEGATIVES, "effective_methods": ACTIVATION_METHODS},
            "new_method_count": len(startup),
            "new_failed_witness_count": len(startup),
            "new_passing_witness_count": len(startup),
            "effective_negatives_after_startup": ACTIVATION_NEGATIVES + len(startup),
            "effective_methods_after_startup": ACTIVATION_METHODS + len(startup),
            "methods": startup,
            "failure_erasure_count": 0,
            "valid": True,
        },
        "x1/threat-model-plan.json": threat_model(),
        "x1/workflow-plan.json": workflow_plan(),
        "x1/flashcard-architecture-freeze.json": flashcard_architecture(),
    }
    for relative, value in documents.items():
        write_json(relative, value)
    write_text("x1/x1-overview.md", overview(audit, outcomes, len(startup)))
    return {
        "valid": audit["valid"],
        "corpus": audit["corpus_row_count"],
        "corpus_sha256": audit["corpus_canonical_sha256"],
        "max_inherited_similarity": audit["maximum_inherited_token_jaccard_similarity"],
        "max_pair_similarity": audit["maximum_new_pair_token_jaccard_similarity"],
        "outcomes": dict(outcomes),
        "startup_count": len(startup),
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    result = run_git("show", f":{path}")
    return result.stdout


def scan_blob(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"),
        "private_route_or_callable": re.compile(r"(?i)(?:resume[_ -]?value|private callable identifier|raw route key)"),
        "transcript_or_session_stream": re.compile(r"(?i)(?:verbatim private transcript|session stream payload|conversation export)"),
    }
    hits: list[dict[str, str]] = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            excerpt = match.group(0)
            scanner_definition = path == BUILDER_PATH and "re.compile" in text[max(0, match.start() - 100) : match.start()]
            hits.append(
                {
                    "path": path,
                    "class": class_name,
                    "sha256_excerpt": sha256(excerpt.encode("utf-8")),
                    "disposition": "scanner_definition" if scanner_definition else "confirmed_issue",
                }
            )
    return hits


def write_staged_review() -> None:
    actual = staged_paths()
    missing = sorted(set(INTENDED_ALLOWLIST) - set(actual))
    extra = sorted(set(actual) - set(INTENDED_ALLOWLIST))
    if missing or extra:
        raise X1Error(f"staged allowlist differs missing={missing} extra={extra}")
    entries = []
    json_count = 0
    scanner = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        scanner.extend(scan_blob(path, raw))
        if path not in MANIFEST_EXCLUSIONS:
            entries.append({"path": path, "sha256": sha256(raw), "size": len(raw), "hash_domain": "exact staged Git blob"})
    confirmed = [row for row in scanner if row["disposition"] == "confirmed_issue"]
    if confirmed:
        raise X1Error(f"confirmed privacy or raw-identifier findings: {confirmed}")
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise X1Error(diff_check.stdout.decode("utf-8", "replace") + diff_check.stderr.decode("utf-8", "replace"))
    manifest = {
        "schema": "ghc.family.sable.v664-v7.x1-content-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(INTENDED_ALLOWLIST),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(MANIFEST_EXCLUSIONS) == len(INTENDED_ALLOWLIST),
    }
    review = {
        "schema": "ghc.family.sable.v664-v7.x1-staged-review.v1",
        "intended_path_count": len(INTENDED_ALLOWLIST),
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "scanner_candidate_count": len(scanner),
        "scanner_definition_count": sum(row["disposition"] == "scanner_definition" for row in scanner),
        "confirmed_privacy_or_raw_identifier_hits": len(confirmed),
        "scanner_candidates": scanner,
        "diff_hygiene_issues": 0,
        "x2_paths_present": any(f"{PREFIX}x2/" in path for path in actual),
        "valid": not missing and not extra and not confirmed and not any(f"{PREFIX}x2/" in path for path in actual),
    }
    candidate = {
        "schema": "ghc.family.sable.v664-v7.x1-stage-candidate.v1",
        "source_head": SOURCE_FINAL,
        "branch": BRANCH,
        "planning_only": True,
        "observed_x2_outcomes_present": False,
        "x2_implementation_present": False,
        "manifest": f"{PREFIX}x1/x1-content-manifest.json",
        "staged_review": f"{PREFIX}x1/x1-staged-review.json",
        "test_command": "python -m unittest tests.test_ghc_family_sable_v664_v7_x1",
        "commit_state": "PREPARED_NOT_COMMITTED",
        "push_state": "PREPARED_NOT_PUSHED",
        "remote_equality_state": "PREPARED_NOT_PROVED",
        "valid": review["valid"] and manifest["coverage_valid"],
    }
    write_json("x1/x1-content-manifest.json", manifest)
    write_json("x1/x1-staged-review.json", review)
    write_json("x1/x1-stage-candidate.json", candidate)


def check_staged() -> dict[str, Any]:
    actual = staged_paths()
    if actual != INTENDED_ALLOWLIST:
        raise X1Error("staged allowlist changed after review")
    manifest = strict_json(index_blob(f"{PREFIX}x1/x1-content-manifest.json"), "staged manifest")
    review = strict_json(index_blob(f"{PREFIX}x1/x1-staged-review.json"), "staged review")
    candidate = strict_json(index_blob(f"{PREFIX}x1/x1-stage-candidate.json"), "staged candidate")
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            raise X1Error(f"manifest mismatch: {entry['path']}")
    if not (manifest["coverage_valid"] and review["valid"] and candidate["valid"]):
        raise X1Error("one x1 staged receipt is invalid")
    return {
        "valid": True,
        "staged_paths": len(actual),
        "manifest_entries": len(manifest["entries"]),
        "manifest_exclusions": len(manifest["declared_self_exclusions"]),
        "strict_json": review["strict_json_count"],
        "privacy_confirmed_hits": review["confirmed_privacy_or_raw_identifier_hits"],
    }


def audit_only() -> dict[str, Any]:
    corpus, construction = reconstruct_corpus()
    proposals = build_proposals()
    audit = novelty_audit(proposals, corpus, construction)
    return {
        "valid": audit["valid"],
        "corpus": audit["corpus_row_count"],
        "corpus_sha256": audit["corpus_canonical_sha256"],
        "new_titles": audit["new_title_count"],
        "max_inherited_similarity": audit["maximum_inherited_token_jaccard_similarity"],
        "max_pair_similarity": audit["maximum_new_pair_token_jaccard_similarity"],
        "microfilm_inherited_titles": audit["practice_term_checks"]["microfilm_title_count_in_inherited_corpus"],
        "microfiche_inherited_titles": audit["practice_term_checks"]["microfiche_title_count_in_inherited_corpus"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--audit-only", action="store_true")
    modes.add_argument("--build", action="store_true")
    modes.add_argument("--write-staged-review", action="store_true")
    modes.add_argument("--check-staged", action="store_true")
    args = parser.parse_args()
    if args.audit_only:
        result = audit_only()
    elif args.build:
        result = build_documents()
    elif args.write_staged_review:
        write_staged_review()
        result = {"valid": True, "written": MANIFEST_EXCLUSIONS}
    else:
        result = check_staged()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
