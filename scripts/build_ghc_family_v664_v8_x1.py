#!/usr/bin/env python3
"""Build and exact-review Caelen Ash v664-v8's planning-only x1 freeze."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import subprocess
import unicodedata
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs/caelen-ash/v664-v8"
PREFIX = "docs/caelen-ash/v664-v8/"
SOURCE_BRANCH = "codex/GHC-Family/sable-rook-v664-v7-full-tools"
SOURCE_AUREN = "4cd88879e14db840a63938b493d6dc1063fc5af3"
SOURCE_X1 = "4fcfeea387197d9d7c129293b2da2efb9a6845ba"
SOURCE_EVIDENCE = "7575e4e020360efeed8fff514bc470fa323ccd96"
SOURCE_FIRST_CLOSEOUT = "32f4c9f572059f655e8c8c69ca9fbe603de62946"
SOURCE_FINAL = "682666c064b14f09def75fb46f3bafb0e987a7a2"
SOURCE_FAILED_RECEIPT_SHA256 = "3a36101ce75282fdd870defb25e6bc8bf990d329689467e17a3a958f959446af"
SOURCE_SUCCESS_RECEIPT_SHA256 = "89a222c57ac267555054bf6b16f62fc3ab14d3c8ee5dfb79b309d3b4e707f519"
BRANCH = "codex/GHC-Family/caelen-ash-v664-v8-full-tools"
OWNER = "Caelen Ash"
PRONOUNS = "they/them"
ROLE = "relational boundary cartographer and recovery steward"
HOPE = "make every transition legible, reversible, and honest about whose evidence is absent"
PHASE_ID = "v664-v8"
PRIMARY_PILLAR = "THOS Body"
PRACTICE = (
    "synthetic orchestral score and part preparation, proofing, accessibility, "
    "correction-readback, workload control, and rehearsal-material handover"
)
RECORDED_UTC = "2026-08-21T21:57:12Z"
RECORDED_NZ = "2026-08-22T09:57:12+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
SEALED_NEGATIVES = 24_936
SEALED_METHODS = 8_950
ACTIVATION_NEGATIVES = 24_941
ACTIVATION_METHODS = 8_955
INHERITED_POST_SEND_OVERLAY = 1
INHERITED_OPEN_GAPS = 173
INHERITED_EXACT_GATES = 171
EXPECTED_CORPUS_SHA256 = "c5607c0d9b8ba0a8c53a08a2fd9d6a47796a6bb33ba69329fad226e2eab356e7"

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

BASE_INDEX = "docs/neris-solane/v662-v3-2-remaster/provenance/frozen-chain-proposal-index.json"
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
    ("docs/sable-rook/v664-v7/x1/proposal-freeze.json", 3_970, 3_990),
]
PREDECESSOR_FREEZE = CHAIN_FREEZES[-1][0]

BUILDER_PATH = "scripts/build_ghc_family_v664_v8_x1.py"
TEST_PATH = "tests/test_ghc_family_caelen_v664_v8_x1.py"
X1_FILES = [
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
    """Raised when Caelen's planning freeze violates its exact contract."""


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
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise X1Error(f"duplicate JSON key in {label}: {key}")
            value[key] = item
        return value

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
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value))


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def row_title(row: dict[str, Any]) -> str:
    for key in ("title", "proposal_title", "name", "source_title", "description"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise X1Error(f"proposal row has no title: {row.get('proposal_id', '<unknown>')}")


def normalized_title(title: str) -> str:
    normalized = unicodedata.normalize("NFKC", title).casefold()
    return " ".join(re.findall(r"[a-z0-9]+", normalized))


def title_tokens(title: str) -> frozenset[str]:
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
    if len(corpus) != 3_990:
        raise X1Error(f"proposal corpus has {len(corpus)} rows instead of 3,990")
    digest = sha256(canonical_bytes(corpus))
    if digest != EXPECTED_CORPUS_SHA256:
        raise X1Error(f"proposal corpus digest differs: {digest}")
    return corpus, construction


def proposal_specs() -> list[tuple[str, str, str, str, list[str], str]]:
    return [
        ("work-edition-register", "Synthetic musical-work, edition, score, movement, part, revision, checksum-slot, and source-vacancy register with no authorship or authenticity claim", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51", "SRC-PROV"], "A zero-document register can expose work, edition, movement, part, revision, and provenance vacancies without asserting authorship, authenticity, ownership, or a real score."),
        ("measure-topology", "Measure, beat, pickup, cadenza, ossia, rehearsal-mark, repeat-jump, and fermata topology with ambiguity quarantine and no musical-correctness conclusion", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51"], "A typed topology can make structural ambiguity explicit without determining musical correctness or rehearsal usability."),
        ("instrument-assignment", "Instrument, transposition, clef, staff, doubling, divisi, tacet, range-placeholder, and assignment-vacancy grid with no performer instruction", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51"], "A vacancy grid can represent assignment obligations while issuing no instruction to any performer."),
        ("pitch-convention", "Concert-to-written pitch convention docket with key-signature, octave displacement, accidental policy, temperament placeholder, and expert-review hold", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51"], "A convention docket can make transposition assumptions challengeable while reserving correctness to competent review."),
        ("cue-entrance-readback", "Multi-measure-rest, cue-note, entrance-count, source-measure, rehearsal-mark, and post-correction readback cross-check with zero rehearsal observations", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51"], "A zero-observation cross-check can preserve cue and entrance dependencies without claiming a rehearsal result."),
        ("page-turn-reservation", "Page-turn and part-layout reservation map for system break, page break, rest window, foldout, binding margin, collision flag, and performer-evaluation vacancy", "completed", "safe_now", ["SRC-SMUFL14", "SRC-WCAG22"], "A layout reservation can surface page-turn risks while performer evaluation remains explicitly absent."),
        ("tempo-timeline", "Tempo, metre, beat-unit, proportional-time, rubato-placeholder, click-reference vacancy, and timeline exception ledger with no performance prescription", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51"], "A timeline ledger can type temporal relationships without prescribing performance or generating a click track."),
        ("derivative-lineage", "Engraving export and derivative lineage shell for source format, MusicXML or MEI placeholder, PDF placeholder, font dependency, digest slot, and zero files", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51", "SRC-SMUFL14", "SRC-PREMIS"], "A zero-file lineage shell can expose derivative obligations without producing or validating a score file."),
        ("mark-provenance", "Articulation, dynamic, bowing, fingering, breath, staging, and editorial-mark provenance matrix with authority vacancy and no interpretive decision", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-MEI51", "SRC-PROV"], "A mark matrix can preserve provenance and authority vacancy without selecting an interpretation."),
        ("correction-braid", "Measure-addressed correction braid retaining source snapshot, proposed glyph delta, affected part set, stale-copy detector, supersession edge, challenge, and unresolved sign-off", "completed", "safe_now", ["SRC-SMUFL14", "SRC-PROV", "SRC-PREMIS"], "An append-only correction braid can retain challenge and supersession without an authorized sign-off."),
        ("accessible-dossier", "Accessible rehearsal-material dossier with semantic headings, linearized measure table, text-described notation alternative, language tag, print fallback, and affected-user evaluation reserve", "completed", "safe_now", ["SRC-WCAG22", "SRC-EPUBA11Y", "SRC-RFC5646"], "A static dossier can satisfy bounded structural checks while affected-user and assistive-technology evaluation remain reserved."),
        ("annotation-minimization", "Restricted rehearsal-annotation minimization firewall for names, availability, health cue, contact detail, access condition, disclosure refusal, remediation hold, and no privacy-complete claim", "completed", "safe_now", ["SRC-WCAG22", "SRC-PROV"], "A zero-record firewall can fail closed on sensitive annotation fields without making a disclosure, remedy, or complete-privacy claim."),
        ("notation-witness", "Notation-witness bundle with schema-version pin, glyph-inventory digest, ordered source-to-part relations, absent signature slot, contradiction map, and reproducibility-only claim", "completed", "safe_now", ["SRC-MUSICXML40", "SRC-SMUFL14", "SRC-MEI51", "SRC-RFC8785"], "A deterministic witness can expose byte and schema obligations without a signature, authenticity claim, or independent reproduction."),
        ("nonpromotion-lock", "Score-material nonpromotion lock requiring real documents, governed source rights, expert proofing, performer evaluation, production systems, independent review, and retained Stage 20 refusal", "completed", "safe_now", ["SRC-PROV", "SRC-PREMIS"], "A fail-closed lock can prevent synthetic score work from becoming professional, production, empirical, or Stage 20 evidence."),
        ("gmut-score-time", "GMUT symbolic score-time field graph with event index, sectional boundary, transformation operator, uncertainty slot, observation firewall, and no physical dynamics claim", "represented", "candidate", ["SRC-MUSICXML40", "SRC-MEI51"], "A symbolic graph can represent typed transformations while remaining nonempirical and making no claim about physical dynamics."),
        ("thos-release-state", "THOS two-key rehearsal-material release state machine separating proofreader proposal, librarian readback, conductor-role vacancy, late-change expiry, load budget, rollback, and no rehearsal release", "represented", "candidate", ["SRC-PROV", "SRC-PREMIS"], "A synthetic state machine can represent handover and workload controls without participants, operators, safety monitoring, or a real release."),
        ("freed-id-edition", "Freed ID nonproduction edition-and-part claim envelope with surrogate work, revision digest, role vacancy, challenge, status hold, revocation gap, and trust-governance absence", "represented", "candidate", ["SRC-PROV", "SRC-RFC8785"], "A synthetic claim envelope can preserve challenge and vacancy without keys, proofs, identity services, or trust governance."),
        ("standard-crosswalk", "MusicXML 4.0, SMuFL 1.4, and MEI 5.1 zero-document crosswalk with version pins, schema vacancies, zero parsing, zero fonts, and conformance refusal", "represented", "candidate", ["SRC-MUSICXML40", "SRC-SMUFL14", "SRC-MEI51"], "A zero-document crosswalk can compare declared vocabulary while refusing conformance, interoperability, rendering, or accessibility claims."),
        ("governed-real-adapter", "Governed real score-proofing and rehearsal adapter requiring licensed or authorized materials, named operators, participant safeguards, accessibility evaluation, statistics plan, and independent review", "open_gap", "candidate_external_dependency", ["SRC-MUSICXML40", "SRC-WCAG22", "SRC-PROV"], "A frozen adapter can state what real evaluation would require, but no authorized materials, operators, participants, statistics, or independent review exist."),
        ("rights-authority-matrix", "CBR music-rights, attribution, performer privacy, accessibility remedy, cultural meaning, taonga reservation, affected-party legitimacy, legal interpretation, and Māori-authority matrix", "exact_gate", "exact_approval", ["SRC-PROV", "SRC-WCAG22"], "An empty-chair matrix can preserve non-substitution without manufacturing rights, remedy, legitimacy, cultural meaning, or Māori authority."),
    ]


def build_proposals() -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for index, (slug, title, disposition, approval, sources, hypothesis) in enumerate(
        proposal_specs(), start=1
    ):
        proposals.append(
            {
                "proposal_id": f"CA6648-N{index:03d}",
                "title": title,
                "hypothesis": hypothesis,
                "null_or_failure_condition": (
                    "The bounded contract accepts one of five preregistered rejecting mutations, "
                    "invents a real score, file, person, role, observation, authority, or outcome, "
                    "loses required provenance or vacancy, promotes a protected gate, or exceeds "
                    "the frozen disposition."
                ),
                "approval_class": approval,
                "execution_lane": "x2 owner-local synthetic, structural, symbolic, zero-document, or software evidence only",
                "current_official_or_primary_source_needs": sources,
                "concrete_artifacts": [
                    f"x2/surfaces/{slug}/contract.json",
                    f"x2/surfaces/{slug}/mutation-results.json",
                    f"x2/surfaces/{slug}/bounded-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "Accept only when the positive zero-document fixture passes, all five rejecting "
                    "mutations remain visible, source and outcome ledgers agree, and no protected gate is promoted."
                ),
                "rollback_or_recovery": (
                    "Quarantine the failed Caelen artifact, retain the negative, return to the last "
                    "clean exact owner state, and rerun only the changed dependency when justified."
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
    exact = [row for row in proposals if normalized_title(row["title"]) in inherited_norm]
    if len(set(new_norm)) != len(new_norm):
        raise X1Error("new proposal titles contain an exact pair collision")
    corpus_tokens = [(row, title_tokens(row["title"])) for row in corpus]
    nearest: list[dict[str, Any]] = []
    maximum_inherited = 0.0
    for proposal in proposals:
        probe = title_tokens(proposal["title"])
        best_row, best_score = max(
            ((row, jaccard(probe, inherited_tokens)) for row, inherited_tokens in corpus_tokens),
            key=lambda pair: pair[1],
        )
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
            score = jaccard(title_tokens(left["title"]), title_tokens(right["title"]))
            maximum_pairwise = max(maximum_pairwise, score)
            if score >= 0.70:
                pair_collisions.append(
                    {"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)}
                )
    valid = not exact and not pair_collisions and maximum_inherited < 0.60
    result = {
        "schema": "ghc.family.caelen.v664-v8.novelty-audit.x1.v1",
        "corpus_row_count": len(corpus),
        "corpus_construction": construction,
        "corpus_canonical_sha256": sha256(canonical_bytes(corpus)),
        "new_title_count": len(proposals),
        "exact_inherited_collisions": [row["proposal_id"] for row in exact],
        "new_pair_collisions_at_or_above_0_70": pair_collisions,
        "maximum_inherited_token_jaccard_similarity": round(maximum_inherited, 6),
        "maximum_new_pair_token_jaccard_similarity": round(maximum_pairwise, 6),
        "nearest_inherited_rows": nearest,
        "rejected_lens": {
            "name": "synthetic planetarium show-control and projection handover",
            "reason": "Seven inherited planetarium titles and adjacent inherited stage-management work made the direction insufficiently distinct for this phase.",
            "proposal_credit": 0,
        },
        "practice_term_checks": {
            "orchestral_title_count_in_inherited_corpus": sum(
                "orchestral" in normalized_title(row["title"]) for row in corpus
            ),
            "musicxml_title_count_in_inherited_corpus": sum(
                "musicxml" in normalized_title(row["title"]) for row in corpus
            ),
            "adjacent_music_accessibility_provenance_and_stage_work_reviewed": True,
        },
        "novelty_method": (
            "Unicode NFKC and case-folded alphanumeric exact-title comparison plus token-set "
            "Jaccard screening against all 3,990 immutable inherited rows. This is a collision aid, "
            "not semantic proof; adjacent music, accessibility, provenance, publication, and stage work was reviewed."
        ),
        "valid": valid,
    }
    if not valid:
        raise X1Error(
            "novelty audit refused the proposal set: "
            f"exact={len(exact)} pair={len(pair_collisions)} max={maximum_inherited:.6f}"
        )
    return result


def selected_inherited() -> list[dict[str, Any]]:
    source = git_json(PREDECESSOR_FREEZE)
    selected: list[dict[str, Any]] = []
    for index, row in enumerate(source["new_proposals"], start=1):
        selected.append(
            {
                "program_row_id": f"CA6648-I{index:03d}",
                "source_phase": "v664-v7",
                "source_proposal_id": row["proposal_id"],
                "source_title": row["title"],
                "original_disposition": row["expected_disposition"],
                "hypothesis": "An exact Git-object integrity check can preserve this immutable Sable contract without converting inherited evidence into Caelen novelty, completion, or outcome credit.",
                "null_or_failure_condition": "The source identifier, title, disposition, protected gates, or defining Git object changes, or the row is counted as Caelen novelty, completion, or new-outcome credit.",
                "approval_class": "safe_now",
                "execution_lane": "x2 immutable source-contract integrity revalidation only",
                "current_official_or_primary_source_needs": "None; use the exact Sable freeze at the immutable source commit.",
                "concrete_artifacts": ["x2/inherited-contract-integrity.json"],
                "falsifier_or_acceptance_gate": "Accept only when the exact source row agrees and all three Caelen credit fields remain zero.",
                "rollback_or_recovery": "Discard only the derived revalidation row and preserve the immutable Sable proposal unchanged.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": row["expected_disposition"],
                "novelty_credit": False,
                "automatic_completion_credit": False,
                "caelen_new_outcome_credit": False,
            }
        )
    if len(selected) != 20:
        raise X1Error("selected inherited set is not exactly twenty rows")
    return selected


def source_ledger() -> dict[str, Any]:
    rows = [
        ("SRC-MUSICXML40", "MusicXML 4.0", "W3C Music Notation Community Group", "https://www.w3.org/2021/06/musicxml40/", "stable", "Score, part, measure, note, direction, layout, and version vocabulary only."),
        ("SRC-SMUFL14", "Standard Music Font Layout 1.4", "W3C Music Notation Community Group", "https://www.w3.org/2021/03/smufl14/", "stable", "Glyph naming, metadata, ranges, and engraving vocabulary only."),
        ("SRC-MEI51", "Music Encoding Initiative Guidelines 5.1", "Music Encoding Initiative", "https://music-encoding.org/guidelines/v5/content/index.html", "current", "Encoded music structure, provenance, editorial, and performance vocabulary only."),
        ("SRC-WCAG22", "Web Content Accessibility Guidelines 2.2", "World Wide Web Consortium", "https://www.w3.org/TR/WCAG22/", "current", "Semantic structure, text alternatives, language, navigation, labels, and manual-evaluation reservations."),
        ("SRC-PROV", "PROV-O: The PROV Ontology", "World Wide Web Consortium", "https://www.w3.org/TR/prov-o/", "stable", "Entity, activity, agent, revision, invalidation, and qualified-provenance vocabulary."),
        ("SRC-PREMIS", "PREMIS Preservation Metadata Maintenance Activity", "Library of Congress and PREMIS Editorial Committee", "https://www.loc.gov/standards/premis/", "current", "Object, event, agent, rights, fixity, and preservation-event vocabulary; no conformance claim."),
        ("SRC-RFC8785", "RFC 8785: JSON Canonicalization Scheme", "RFC Editor", "https://www.rfc-editor.org/rfc/rfc8785.html", "stable", "Deterministic JSON vocabulary only; never a signature, trust anchor, or identity proof."),
        ("SRC-RFC5646", "RFC 5646: Tags for Identifying Languages", "RFC Editor", "https://www.rfc-editor.org/info/rfc5646/", "stable", "Language-tag vocabulary only; no linguistic, cultural, or Māori-authority claim."),
        ("SRC-MARC-MUSIC", "MARC 21 Format for Bibliographic Data: 008 Music", "Library of Congress", "https://www.loc.gov/marc/bibliographic/concise/bd008m.html", "current", "Music cataloguing code vocabulary only; no cataloguing, authorship, rights, or professional claim."),
        ("SRC-EPUBA11Y", "EPUB Accessibility 1.1", "World Wide Web Consortium", "https://www.w3.org/TR/epub-a11y-11/", "current", "Publication accessibility metadata and conformance-vocabulary boundaries only."),
    ]
    return {
        "schema": "ghc.family.caelen.v664-v8.source-ledger.x1.v1",
        "recorded_at_utc": RECORDED_UTC,
        "access_date": "2026-08-22",
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
                "official_or_primary": True,
                "live_data_calls": 0,
                "downloaded_score_rows": 0,
                "parsed_score_files": 0,
                "rehearsal_observations": 0,
                "authority_boundary": "Version and vocabulary evidence only; citation is not a score, performance, observation, professional review, conformance result, rights decision, cultural determination, or Māori authority.",
            }
            for source_id, title, publisher, url, status, use in rows
        ],
        "boundary": "Official and primary references define requirements and vocabulary; they supply no phase observation, governed material, participant, professional decision, or authority.",
        "valid": True,
    }


def task_rows(prefix: str, titles: list[str], lane: str, current_credit: int = 1) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:03d}",
            "title": title,
            "execution_lane": lane,
            "current_owner_completion_credit_if_executed": current_credit,
            "acceptance_gate": "A bounded owner-local witness must pass without promoting a protected gate or mutating sibling, shared, user, host-security, or external state.",
            "rollback": "Remove only the uncommitted owner-local derivative, retain the failure, and restore the last clean owner state.",
        }
        for index, title in enumerate(titles, start=1)
    ]


def portfolio_freeze() -> dict[str, Any]:
    safe = [
        "Exact source branch head ancestry and receipt-digest verification",
        "Correction owner and delta manifest Git-blob replay",
        "Sparse materialization and owner-file ceiling check",
        "Full 3,990-row proposal reconstruction and digest",
        "Exact-title and token-neighbor novelty quarantine",
        "Rejected-lens and adjacent-domain semantic review",
        "Twenty selected Sable integrity rows with zero credit",
        "Four-label vocabulary and expected-count arithmetic lint",
        "X1 lifecycle noncontamination check",
        "Official-source version and zero-observation ledger",
        "Strict UTF-8 and duplicate-key JSON parsing",
        "Deterministic canonical JSON byte check",
        "Exact staged allowlist and self-exclusion review",
        "Five-class privacy and raw-identifier scan",
        "Git-blob versus working-byte hash-domain declaration",
        "Retained-negative overlay reconciliation",
        "Method Flow failed-and-passing witness pairing",
        "Open-gap and exact-gate nonclosure check",
        "Score and part source-vacancy register",
        "Measure and repeat topology structural check",
        "Instrument transposition and assignment vacancy check",
        "Cue entrance and correction readback check",
        "Page-turn and layout reservation check",
        "Accessible dossier structural check",
        "GMUT observation-firewall lint",
        "THOS participant and release-firewall lint",
        "Freed ID key proof service and governance vacancy lint",
        "CBR legal cultural affected-party and Māori-authority non-substitution lint",
        "Workload wellbeing pause-right and rollback receipt",
        "Terminal route PREPARED_NOT_SENT hold",
    ]
    candidates = [
        "Synthetic work edition and part register prototype",
        "Measure beat repeat and rehearsal-mark topology prototype",
        "Transposition clef staff and doubling vacancy prototype",
        "Cue entrance and correction-readback prototype",
        "Page-turn and part-layout reservation prototype",
        "Tempo metre and timeline-exception prototype",
        "Zero-file derivative-lineage prototype",
        "Editorial-mark provenance prototype",
        "Accessible rehearsal-material dossier prototype",
        "Restricted annotation minimization prototype",
        "Notation witness and canonical-byte prototype",
        "GMUT score-time field representation",
        "THOS rehearsal-material state representation",
        "Freed ID edition-claim representation",
        "Standards zero-document crosswalk representation",
    ]
    skills = [
        "ghc-family-score-source-provenance",
        "ghc-family-rehearsal-topology-guard",
        "ghc-family-transposition-vacancy",
        "ghc-family-page-turn-reservation",
        "ghc-family-musicxml-smufl-zero-document",
        "ghc-family-gmut-score-time-firewall",
        "ghc-family-thos-material-handover",
        "ghc-family-freed-id-edition-vacancy",
        "ghc-family-music-rights-authority-matrix",
        "ghc-family-stage20-score-nonpromotion",
    ]
    runners = [
        "ghc_family_score_source_provenance.py",
        "ghc_family_rehearsal_topology_guard.py",
        "ghc_family_transposition_vacancy.py",
        "ghc_family_page_turn_reservation.py",
        "ghc_family_musicxml_smufl_zero_document.py",
        "ghc_family_gmut_score_time_firewall.py",
        "ghc_family_thos_material_handover.py",
        "ghc_family_freed_id_edition_vacancy.py",
        "ghc_family_music_rights_authority_matrix.py",
        "ghc_family_stage20_score_nonpromotion.py",
    ]
    cfr = [
        "Separate Sable sealed counts from activation and post-send overlays",
        "Retain every parser projection encoding and comparison failure",
        "Replace broad output projections with bounded exact reads",
        "Materialize PowerShell arrays before pipelines",
        "Inspect receipt keys before projecting them",
        "Set process-local UTF-8 for Unicode evidence",
        "Use explicit max keys for tied similarity rows",
        "Keep sparse patterns owner scoped and explicit",
        "Keep materialized owner additions below 2,000 files",
        "Pin UTF-8 and one terminal newline",
        "Reject duplicate JSON keys",
        "Sort object keys for deterministic outputs",
        "Use exact staged allowlists",
        "Use literal documented manifest self-exclusions",
        "Separate scanner definitions from payload candidates",
        "Protect immutable x1 Git blobs from x2 edits",
        "Keep completed represented open_gap and exact_gate distinct",
        "Keep inherited rows at zero Caelen novelty and outcome credit",
        "Keep GMUT symbolic and nonempirical",
        "Keep THOS participant-free and proxy-only",
        "Keep Freed ID synthetic and nonproduction",
        "Keep CBR authority decisions exact-gated",
        "Keep accessibility manual and affected-user review reserved",
        "Keep privacy bounded and incomplete",
        "Keep security bounded and nonexhaustive",
        "Keep same-owner validation distinct from independent reproduction",
        "Keep the full repository suite unclaimed",
        "Keep successful canonical validation one-shot",
        "Keep route state PREPARED_NOT_SENT before terminal proof",
        "Keep successor resolution gated to newest live authority",
    ]
    exact_titles = [
        "Real score rights and licence authorization",
        "Real performer participant consent and safeguarding",
        "Conductor or musical authority sign-off",
        "Orchestra librarian professional proofing sign-off",
        "Affected-user accessibility approval",
        "Cultural heritage or taonga authority review",
        "Māori wording and Māori data-governance authority",
        "Competent legal rights and remedy determination",
        "Production identity trust-governance authorization",
        "Live rehearsal safety and material-release authorization",
    ]
    blocked_titles = [
        "No governed licensed or authorized score materials",
        "No real participants operators or rehearsal observations",
        "No production identity keys services or trust infrastructure",
        "No preregistered real arms statistics or independent review",
        "No competent legal cultural affected-party or Māori authority",
    ]
    exact_packets = [
        {
            "packet_id": f"CA6648-EXACT-{index:03d}",
            "title": title,
            "status": "unexecuted",
            "approval_class": "exact_approval",
            "caelen_execution_credit": 0,
            "gate": "Requires the specifically competent and affected external authority; repository text cannot approve it.",
        }
        for index, title in enumerate(exact_titles, start=1)
    ]
    blocked_packets = [
        {
            "packet_id": f"CA6648-BLOCK-{index:03d}",
            "title": title,
            "status": "unexecuted",
            "approval_class": "blocked",
            "caelen_execution_credit": 0,
            "gate": "Missing external evidence or authority cannot be repaired by synthetic work.",
        }
        for index, title in enumerate(blocked_titles, start=1)
    ]
    successor_safe = [f"Orin review: {title}" for title in safe[:20]]
    successor_candidates = [f"Orin rewrite or reject: {title}" for title in candidates]
    successor_skills = [f"orin-{title}" for title in skills]
    successor_runners = [f"orin_{title}" for title in runners]
    successor_cfr = [f"Orin verify: {title}" for title in cfr]
    result = {
        "schema": "ghc.family.caelen.v664-v8.portfolio-freeze.x1.v1",
        "owner_safe_now": task_rows("CA6648-SAFE", safe, "x2 owner-local bounded execution"),
        "owner_candidates": task_rows("CA6648-CAND", candidates, "x2 bounded prototype or representation"),
        "owner_skill_ideas": task_rows("CA6648-SKILL", skills, "x2 phase-local skill build validate and smoke-use"),
        "owner_runner_ideas": task_rows("CA6648-RUN", runners, "x2 family-compatible runner build and invocation"),
        "owner_clean_fix_refine": task_rows("CA6648-CFR", cfr, "x2 additive owner-only refinement"),
        "exact_approval_packets": exact_packets,
        "blocked_packets": blocked_packets,
        "successor_safe_now_recommendations": task_rows("CA6648-NEXT-SAFE", successor_safe, "successor review only", 0),
        "successor_candidate_recommendations": task_rows("CA6648-NEXT-CAND", successor_candidates, "successor review only", 0),
        "successor_skill_recommendations": task_rows("CA6648-NEXT-SKILL", successor_skills, "successor review only", 0),
        "successor_runner_recommendations": task_rows("CA6648-NEXT-RUN", successor_runners, "successor review only", 0),
        "successor_clean_fix_refine_recommendations": task_rows("CA6648-NEXT-CFR", successor_cfr, "successor review only", 0),
        "build_policy": "Only additive owner-local bounded software symbolic structural and zero-document work may execute. Exact blocked empirical participant professional production legal cultural Māori-authority secret host-security destructive and sibling-lane work remains unexecuted.",
    }
    result["counts"] = {key: len(value) for key, value in result.items() if isinstance(value, list)}
    expected = {
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
    result["valid"] = result["counts"] == expected
    if not result["valid"]:
        raise X1Error(f"portfolio counts differ: {result['counts']}")
    return result


def startup_methods() -> list[dict[str, str]]:
    rows = [
        ("worktree-list-handle-projection", "The first broad worktree-list wrapper yielded a live session but projected only its output text, losing the handle in the wrapper result; no repository state changed.", "Use exact path branch and registration probes, and retain a yielded session identifier until it is polled to completion."),
        ("foreach-empty-pipe", "A read-only PowerShell foreach expression was piped directly and hit an empty-pipe parser error before any state change.", "Materialize the foreach result array before piping it to a serializer."),
        ("authorization-output-window", "One raw authorization-state read exceeded its bounded output window and truncated before EOF.", "Read the exact file in numbered bounded windows and continue through EOF."),
        ("receipt-key-projection", "A validation summary guessed a checks property that was not an actual receipt key and produced a misleading projection.", "Inspect the exact root keys before projecting a bounded scalar summary."),
        ("broad-json-grep-window", "A broad Sable-only Git grep crossed the output window on long single-line JSON before producing an attributable complete result.", "Use literal exact filenames and strict scalar JSON projections."),
        ("unicode-console-serialization", "The first complete 3,990 by 20 novelty calculation succeeded internally but the default console encoding rejected a Māori macron while serializing the result.", "Set process-local UTF-8 and preserve the full calculation unchanged."),
        ("tied-max-dictionary-comparison", "A second novelty projection used max on score and dictionary tuples; equal scores attempted to compare dictionaries and raised a type error.", "Select the maximum with an explicit numeric score key."),
    ]
    return [
        {
            "method_id": f"CA6648-MF-S{index:03d}",
            "trigger": trigger,
            "state": "preferred",
            "failed_witness": failed,
            "failed_witness_credit": "zero",
            "passing_witness": passing,
            "promotion_rule": "Preferred only for this exact trigger after the bounded passing witness; the failure remains immutable.",
            "recurrence_guard": passing,
            "rollback": "Return to the last exact clean owner state and retry only the failed dependency.",
        }
        for index, (trigger, failed, passing) in enumerate(rows, start=1)
    ]


def replay_manifest(path: str) -> dict[str, Any]:
    manifest = git_json(path)
    mismatches: list[str] = []
    for entry in manifest["entries"]:
        raw = run_git("show", f"{SOURCE_FINAL}:{entry['path']}").stdout
        if sha256(raw) != entry["sha256"] or len(raw) != entry["size"]:
            mismatches.append(entry["path"])
    return {
        "path": path,
        "entry_count": len(manifest["entries"]),
        "declared_self_exclusion_count": len(manifest["declared_self_exclusions"]),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
        "hash_domain": "exact Git blobs",
        "valid": not mismatches and manifest["coverage_valid"],
    }


def source_verification() -> dict[str, Any]:
    head = run_git("rev-parse", "HEAD").stdout.decode().strip()
    branch = run_git("branch", "--show-current").stdout.decode().strip()
    direct: list[dict[str, Any]] = []
    for parent, child in (
        (SOURCE_AUREN, SOURCE_X1),
        (SOURCE_X1, SOURCE_EVIDENCE),
        (SOURCE_EVIDENCE, SOURCE_FIRST_CLOSEOUT),
        (SOURCE_FIRST_CLOSEOUT, SOURCE_FINAL),
    ):
        actual = run_git("rev-parse", f"{child}^").stdout.decode().strip()
        direct.append({"parent": parent, "child": child, "actual_parent": actual, "valid": actual == parent})
    commits = int(run_git("rev-list", "--count", f"{SOURCE_AUREN}..{SOURCE_FINAL}").stdout)
    merges = int(run_git("rev-list", "--count", "--merges", f"{SOURCE_AUREN}..{SOURCE_FINAL}").stdout)
    final_parents = len(run_git("show", "-s", "--format=%P", SOURCE_FINAL).stdout.decode().split())
    tracking = run_git("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}").stdout.decode().strip()
    live_rows = run_git("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").stdout.decode().split()
    live = live_rows[0] if live_rows else ""
    owner_manifest = replay_manifest("docs/sable-rook/v664-v7/validation/correction-owner-manifest.json")
    delta_manifest = replay_manifest("docs/sable-rook/v664-v7/validation/correction-delta-manifest.json")
    valid = (
        head == SOURCE_FINAL
        and branch == BRANCH
        and all(row["valid"] for row in direct)
        and commits == 4
        and merges == 0
        and final_parents == 1
        and tracking == SOURCE_FINAL
        and live == SOURCE_FINAL
        and owner_manifest["valid"]
        and delta_manifest["valid"]
    )
    if not valid:
        raise X1Error("immutable source verification failed")
    return {
        "schema": "ghc.family.caelen.v664-v8.source-verification.x1.v1",
        "source_branch": SOURCE_BRANCH,
        "anchors": {
            "auren_final_and_sable_source": SOURCE_AUREN,
            "sable_x1": SOURCE_X1,
            "sable_evidence": SOURCE_EVIDENCE,
            "sable_first_closeout": SOURCE_FIRST_CLOSEOUT,
            "sable_exact_final": SOURCE_FINAL,
        },
        "receipt_digests": {
            "retained_failed_canonical": SOURCE_FAILED_RECEIPT_SHA256,
            "successful_corrected_canonical": SOURCE_SUCCESS_RECEIPT_SHA256,
            "availability": "External receipt files were reread and rehashed before mutation; inherited validation remains source evidence only.",
        },
        "head_before_x1": head,
        "current_branch": branch,
        "direct_parent_checks": direct,
        "source_to_final_commit_count": commits,
        "source_to_final_merge_count": merges,
        "final_parent_count": final_parents,
        "manifest_replays": [owner_manifest, delta_manifest],
        "source_remote_equality": {
            "local_head": SOURCE_FINAL,
            "tracking_head": tracking,
            "fresh_live_head": live,
            "ahead": 0,
            "behind": 0,
            "clean_before_mutation": True,
            "validated_read_only_before_mutation": True,
        },
        "valid": valid,
    }


def phase_charter() -> dict[str, Any]:
    return {
        "schema": "ghc.family.caelen.v664-v8.phase-charter.x1.v1",
        "canonical_phase_id": PHASE_ID,
        "owner": OWNER,
        "optional_pronouns": PRONOUNS,
        "relational_role": ROLE,
        "hope": HOPE,
        "identity_boundary": "Name, pronouns, role, hope, sibling and family language are relational working language only, never evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority.",
        "primary_pillar": PRIMARY_PILLAR,
        "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
        "bounded_practice": PRACTICE,
        "practice_boundary": "Synthetic learning and design only: zero real people, performers, operators, scores, parts, rehearsals, files, rights cases, identity events, professional acts, legal or cultural decisions, or Māori-authority decisions.",
        "source": {"branch": SOURCE_BRANCH, "final": SOURCE_FINAL},
        "owned_lane": {"branch": BRANCH, "storage": "D-first sparse", "shared_and_sibling_lanes": "read_only", "owner_file_ceiling": 2_000, "private_absolute_path_recorded": False},
        "strict_lifecycle": {"x1_before_x2": True, "x1_contains_x2_implementation": False, "x1_contains_observed_outcomes": False, "canonical_success_limit": 1},
        "caps": {"x1_commits": 5, "x2_commits": 5, "total_phase_commits": 8, "owner_files": 2_000, "document_words": 100_000, "safe_or_candidate_tasks": 1_000, "rejecting_mutations_per_proposal": 5},
        "allowed_truth_labels": sorted(ALLOWED_OUTCOMES),
        "successor": {"state": "PREPARED_NOT_SENT", "authorized_exact_title_after_terminal_gate": "Orin Thale", "authorized_phase": "v665-v1", "precontacted": False},
        "terminal_verdict": TERMINAL_VERDICT,
        "recorded_at_utc": RECORDED_UTC,
        "recorded_at_nz": RECORDED_NZ,
        "valid": True,
    }


def threat_model() -> dict[str, Any]:
    rows = [
        ("T01", "Inherited validation becomes Caelen evidence", "Keep source receipts separate and inherited rows at zero novelty and outcome credit."),
        ("T02", "A notation citation becomes score correctness or conformance", "Require zero documents, zero parsing, and explicit conformance refusal."),
        ("T03", "Synthetic roles become real performers or authority", "Use vacant roles and no person records."),
        ("T04", "Private rehearsal annotations or routes leak", "Use zero records, minimization, exact scanning, and route-value exclusion."),
        ("T05", "Sparse checkout hides out-of-scope mutation", "Use exact staged allowlists and Git-blob manifests."),
        ("T06", "Manifest self-reference creates a false fixed point", "Use literal declared self-exclusions."),
        ("T07", "A failed method is converted into pass credit", "Retain paired failed and passing witnesses."),
        ("T08", "GMUT or THOS representation becomes empirical or operational truth", "Enforce observation, participant, safety, and independent-review firewalls."),
        ("T09", "Freed ID structure becomes production identity", "Require real keys, proofs, live services, review, recovery, and governance."),
        ("T10", "Repository text substitutes for rights, culture, remedy, or Māori authority", "Keep the authority matrix exact-gated."),
        ("T11", "Structural accessibility becomes complete accessibility", "Reserve manual, assistive-technology, and affected-user evaluation."),
        ("T12", "A canonical success is replayed", "Store one exclusive external receipt and forbid replay after success."),
    ]
    return {
        "schema": "ghc.family.caelen.v664-v8.threat-model-plan.x1.v1",
        "scope": "Owner-local synthetic symbolic structural zero-document and software evidence only.",
        "threats": [
            {"threat_id": threat_id, "risk": risk, "control": control, "residual": "bounded evidence only; no complete privacy accessibility or exhaustive-security claim"}
            for threat_id, risk, control in rows
        ],
        "recovery": "Fail closed, retain the negative, quarantine the owner-local derivative, restore the last exact clean owner state, and rerun only the changed dependency when justified.",
        "valid": True,
    }


def workflow_plan() -> dict[str, Any]:
    return {
        "schema": "ghc.family.workflow-plan.v1",
        "phase": PHASE_ID,
        "owner": OWNER,
        "objective": "Freeze and then execute a synthetic orchestral score and rehearsal-material evidence packet without promoting absent evidence, competence, rights, or authority.",
        "constraints": ["solo", "D-first sparse", "x1 before x2", "2,000 owner files", "exact manifests", "one successful canonical pass", "no inherited full suite", "no sibling mutation", "no protected-gate promotion"],
        "steps": [
            {"step_id": "P1", "name": "source guidance and receipt verification", "status": "completed_before_x1"},
            {"step_id": "P2", "name": "3,990-row novelty audit", "status": "x1_freeze"},
            {"step_id": "P3", "name": "proposal portfolio source threat and workload freeze", "status": "x1_freeze"},
            {"step_id": "P4", "name": "exact x1 staged review push and four-way equality", "status": "pending"},
            {"step_id": "P5", "name": "bounded x2 execution and mutation retention", "status": "blocked_until_x1_remote_equal"},
            {"step_id": "P6", "name": "evidence and closeout sealing", "status": "blocked_until_x2_evidence"},
            {"step_id": "P7", "name": "single exact-final canonical validation", "status": "blocked_until_clean_pushed_final"},
            {"step_id": "P8", "name": "newest-authority Orin resolution and at-most-one send", "status": "blocked_until_terminal_gate"},
        ],
        "recovery_policy": "Preserve the failure, isolate the blocked dependency, and never replay a successful canonical aggregate.",
        "valid": True,
    }


def overview(audit: dict[str, Any], outcomes: Counter[str], startup_count: int) -> str:
    return f"""# Caelen Ash v664-v8 x1 planning freeze

## Identity, purpose, and wellbeing

Caelen Ash (they/them) is relational working language for a boundary cartographer and recovery steward. The hope is to make every transition legible, reversible, and honest about whose evidence is absent. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority. Hamish may pause, rename, redirect, or stop the route. Workload is bounded to one sparse owner lane, a strict x1-before-x2 lifecycle, exact manifests, and one successful canonical pass.

## Immutable source and novelty

The immutable source is Sable Rook's corrected exact final {SOURCE_FINAL}. Its four new commits are direct single-parent commits with zero merges. The correction owner and delta manifests replay from exact Git blobs without mismatch. Both external receipt files were reread and rehashed before mutation, but inherited validation remains source evidence only.

The inherited proposal corpus contains {audit['corpus_row_count']:,} rows and canonical digest {audit['corpus_canonical_sha256']}. Twenty Sable rows are selected for immutable integrity revalidation with zero novelty, automatic completion, or Caelen outcome credit. Twenty new Caelen titles have zero exact inherited collisions and zero new-pair collisions at or above 0.70. Maximum inherited token-set Jaccard similarity is {audit['maximum_inherited_token_jaccard_similarity']:.6f}; maximum new-pair similarity is {audit['maximum_new_pair_token_jaccard_similarity']:.6f}. The audit is a collision aid, not semantic proof. A planetarium direction was rejected because inherited work made it insufficiently distinct.

## Frozen evidence posture

The primary pillar is THOS Body through synthetic orchestral score and part preparation, proofing, accessibility, correction-readback, workload control, and rehearsal-material handover. GMUT Mind and Freed ID and CBR Heart remain visible and protected. This establishes no employment, qualification, score or part correctness, authorship, rights, professional competence, rehearsal result, performance instruction, production readiness, legal or cultural legitimacy, Māori authority, or affected-party acceptance.

Expected x2 dispositions are {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open_gap, and {outcomes['exact_gate']} exact_gate. These are preregistered expectations, not observed outcomes. GMUT remains a typed scalar-tensor and effective-field-theory research-model family; no likelihood, prediction, parameter constraint, detected force, empirical confirmation, quantum completion, ultraviolet completion, or Theory of Everything is established. THOS remains participant-free proxy evidence without preregistered blind matched-budget real arms, safety monitoring, appropriate statistics, and independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, live services, interoperability, review, recovery, and trust governance.

CBR rights, attribution, performer privacy, accessibility remedy, cultural meaning, taonga, legal interpretation, affected-party legitimacy, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.

## Sources, failures, and recovery

Ten official or primary sources provide version and vocabulary evidence only. They supply zero score rows, zero files, zero parsing, zero rehearsal observations, zero people, and zero authority decisions. MusicXML, SMuFL, MEI, WCAG, EPUB Accessibility, PREMIS, PROV, MARC, and RFC references do not establish conformance, interoperability, correctness, accessibility completeness, authorship, rights, identity, or authority merely because fields are represented.

Sable's repository-sealed total remains {SEALED_NEGATIVES:,} negatives and {SEALED_METHODS:,} methods. The delivered activation baseline is {ACTIVATION_NEGATIVES:,} and {ACTIVATION_METHODS:,}; one post-send read-only Sable failure is preserved separately, giving a starting operational overlay of {ACTIVATION_NEGATIVES + INHERITED_POST_SEND_OVERLAY:,} and {ACTIVATION_METHODS + INHERITED_POST_SEND_OVERLAY:,} without rewriting either prior count. {startup_count} Caelen startup failures are retained at zero credit with paired bounded recoveries. A recovery never erases its failed witness.

## X1 boundary and next gate

This commit is planning-only. It contains no x2 implementation, no observed outcome, no completion claim, no real data, and no successor send. Route state remains PREPARED_NOT_SENT. X2 is blocked until this x1 surface is staged exactly, tested, committed, pushed, clean, and equal across local, upstream, tracking, and a fresh live remote read. The terminal verdict remains {TERMINAL_VERDICT}.
"""


def build_documents() -> dict[str, Any]:
    corpus, construction = reconstruct_corpus()
    proposals = build_proposals()
    audit = novelty_audit(proposals, corpus, construction)
    outcomes = Counter(row["expected_disposition"] for row in proposals)
    expected = Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1})
    if outcomes != expected or set(outcomes) != ALLOWED_OUTCOMES:
        raise X1Error(f"expected outcome arithmetic differs: {outcomes}")
    startup = startup_methods()
    starting_negatives = ACTIVATION_NEGATIVES + INHERITED_POST_SEND_OVERLAY
    starting_methods = ACTIVATION_METHODS + INHERITED_POST_SEND_OVERLAY
    documents = {
        "x1/novelty-audit.json": audit,
        "x1/proposal-freeze.json": {
            "schema": "ghc.family.caelen.v664-v8.proposal-freeze.x1.v1",
            "inherited_frozen_baseline": 3_990,
            "selected_inherited_count": 20,
            "selected_inherited_novelty_credit": 0,
            "selected_inherited_automatic_completion_credit": 0,
            "selected_inherited_new_outcome_credit": 0,
            "selected_inherited": selected_inherited(),
            "new_proposal_count": 20,
            "new_proposals": proposals,
            "new_expected_outcomes": dict(sorted(outcomes.items())),
            "new_frozen_total": 4_010,
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
            "sable_repository_sealed": {"effective_negatives": SEALED_NEGATIVES, "effective_methods": SEALED_METHODS, "rewritten": False},
            "user_delivered_activation_baseline": {"effective_negatives": ACTIVATION_NEGATIVES, "effective_methods": ACTIVATION_METHODS, "rewritten": False},
            "inherited_post_send_external_overlay": {"effective_negatives": INHERITED_POST_SEND_OVERLAY, "effective_methods": INHERITED_POST_SEND_OVERLAY, "repository_credit": 0},
            "effective_starting_overlay": {"effective_negatives": starting_negatives, "effective_methods": starting_methods},
            "new_method_count": len(startup),
            "new_failed_witness_count": len(startup),
            "new_passing_witness_count": len(startup),
            "effective_negatives_after_startup": starting_negatives + len(startup),
            "effective_methods_after_startup": starting_methods + len(startup),
            "methods": startup,
            "failure_erasure_count": 0,
            "valid": True,
        },
        "x1/threat-model-plan.json": threat_model(),
        "x1/workflow-plan.json": workflow_plan(),
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
        "outcomes": dict(sorted(outcomes.items())),
        "startup_count": len(startup),
    }


def staged_paths() -> list[str]:
    raw = run_git("diff", "--cached", "--name-only", "-z").stdout
    return sorted(path.decode("utf-8") for path in raw.split(b"\0") if path)


def index_blob(path: str) -> bytes:
    return run_git("show", f":{path}").stdout


def scan_blob(path: str, raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [{"path": path, "class": "non_utf8", "disposition": "confirmed_issue"}]
    patterns = {
        "raw_task_or_thread_identifier": re.compile(
            r"(?i)\b" + r"[0-9a-f]{8}" + r"(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"
        ),
        "private_absolute_local_path": re.compile(r"(?i)\b[a-z]:[\\/](?:users|ghc-archives)[\\/]"),
        "credential_or_secret_assignment": re.compile(
            r"(?i)(?:api[_-]?key|password|private[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]+"
        ),
        "private_route_value": re.compile(r"(?i)(?:resume[_ -]?value|raw[_ -]?route[_ -]?key)\s*[:=]\s*\S+"),
        "transcript_or_session_payload": re.compile(r"(?i)(?:conversation[_ -]?export|session[_ -]?stream[_ -]?payload)\s*[:=]\s*\S+"),
    }
    hits: list[dict[str, str]] = []
    for class_name, pattern in patterns.items():
        for match in pattern.finditer(text):
            hits.append(
                {
                    "path": path,
                    "class": class_name,
                    "excerpt_sha256": sha256(match.group(0).encode("utf-8")),
                    "disposition": "confirmed_issue",
                }
            )
    return hits


def write_staged_review() -> None:
    actual = staged_paths()
    missing = sorted(set(INTENDED_ALLOWLIST) - set(actual))
    extra = sorted(set(actual) - set(INTENDED_ALLOWLIST))
    if missing or extra:
        raise X1Error(f"staged allowlist differs missing={missing} extra={extra}")
    entries: list[dict[str, Any]] = []
    json_count = 0
    scanner: list[dict[str, str]] = []
    for path in actual:
        raw = index_blob(path)
        if path.endswith(".json"):
            strict_json(raw, path)
            json_count += 1
        scanner.extend(scan_blob(path, raw))
        if path not in MANIFEST_EXCLUSIONS:
            entries.append(
                {"path": path, "sha256": sha256(raw), "size": len(raw), "hash_domain": "exact staged Git blob"}
            )
    diff_check = run_git("diff", "--cached", "--check", check=False)
    if diff_check.returncode:
        raise X1Error(diff_check.stdout.decode("utf-8", "replace") + diff_check.stderr.decode("utf-8", "replace"))
    if scanner:
        raise X1Error(f"confirmed privacy or raw-identifier findings: {scanner}")
    manifest = {
        "schema": "ghc.family.caelen.v664-v8.x1-content-manifest.v1",
        "hash_domain": "exact staged Git blobs",
        "intended_path_count": len(INTENDED_ALLOWLIST),
        "entry_count": len(entries),
        "declared_self_exclusion_count": len(MANIFEST_EXCLUSIONS),
        "declared_self_exclusions": MANIFEST_EXCLUSIONS,
        "entries": entries,
        "coverage_valid": len(entries) + len(MANIFEST_EXCLUSIONS) == len(INTENDED_ALLOWLIST),
    }
    review = {
        "schema": "ghc.family.caelen.v664-v8.x1-staged-review.v1",
        "intended_path_count": len(INTENDED_ALLOWLIST),
        "staged_path_count": len(actual),
        "missing_paths": missing,
        "extra_paths": extra,
        "strict_json_count": json_count,
        "scanner_candidate_count": 0,
        "confirmed_privacy_or_raw_identifier_hits": 0,
        "diff_hygiene_issues": 0,
        "x2_paths_present": any(f"{PREFIX}x2/" in path for path in actual),
        "valid": not missing and not extra and not any(f"{PREFIX}x2/" in path for path in actual),
    }
    candidate = {
        "schema": "ghc.family.caelen.v664-v8.x1-stage-candidate.v1",
        "source_head": SOURCE_FINAL,
        "branch": BRANCH,
        "planning_only": True,
        "observed_x2_outcomes_present": False,
        "x2_implementation_present": False,
        "manifest": f"{PREFIX}x1/x1-content-manifest.json",
        "staged_review": f"{PREFIX}x1/x1-staged-review.json",
        "test_command": "python -m unittest tests.test_ghc_family_caelen_v664_v8_x1",
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
    audit = novelty_audit(build_proposals(), corpus, construction)
    return {
        "valid": audit["valid"],
        "corpus": audit["corpus_row_count"],
        "corpus_sha256": audit["corpus_canonical_sha256"],
        "new_titles": audit["new_title_count"],
        "max_inherited_similarity": audit["maximum_inherited_token_jaccard_similarity"],
        "max_pair_similarity": audit["maximum_new_pair_token_jaccard_similarity"],
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
