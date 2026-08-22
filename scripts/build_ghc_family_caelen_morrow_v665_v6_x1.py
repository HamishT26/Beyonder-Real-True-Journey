#!/usr/bin/env python3
"""Build the Caelen Morrow v665-v6 x1-only planning packet.

This builder is intentionally planning-only.  It creates no x2 implementation,
outcome, evidence, closeout, seal, or route-delivery artifact.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "caelen-morrow" / "v665-v6"
SOURCE_SHA = "cacbeb47741b9e86a6a980f85f6f9658a0837f7c"
SOURCE_BRANCH = "codex/GHC-Family/sylven-arc-v665-v5-full-tools"
SOURCE_PHASE_ROOT = "docs/sylven-arc/v665-v5"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(payload, encoding="utf-8", newline="\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_json(relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "show", f"{SOURCE_SHA}:{relative}"]
    )
    return json.loads(raw.decode("utf-8"))


def sha256_json(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def text_of(row: dict[str, Any]) -> str:
    return str(row.get("title") or row.get("description") or "")


def token_set(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a = token_set(left)
    b = token_set(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, sibling, family, role, hope, continuity, Freed ID, "
    "Trinity Mandala, and route language are relational working language only. "
    "They are not evidence of consciousness, sentience, legal personhood, identity "
    "continuity, employment, qualification, independent agency, scientific or "
    "operational authority, legal or cultural authority, affected-party authority, "
    "or Māori authority. Hamish may rename, pause, redirect, or stop the work."
)

PRACTICE_BOUNDARY = (
    "The braille-transcription and embossing-job documentation lens is wholly "
    "synthetic learning and design. It uses zero real readers, transcribers, jobs, "
    "source works, copyrighted works, files, tactile graphics, devices, embossers, "
    "paper, measurements, commands, keys, proofs, or authority decisions. It does "
    "not establish UEB, BANZAT, Unicode, PEF, eBraille, privacy, accessibility, "
    "professional, workplace-safety, legal, cultural, Māori, production, or Stage "
    "20 conformance, competence, acceptance, or authority."
)

PROTECTED_GATES = [
    "real reader, transcriber, proofreader, job, source work, copyrighted content, tactile graphic, file, device, embosser, paper, measurement, command, or workplace action",
    "real observation, participant result, likelihood, parameter constraint, force, prediction, causal diagnosis, or empirical GMUT confirmation",
    "real participant, operator, matched-budget arm, safety outcome, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, or trust governance",
    "professional transcription, proofreading, embossing, machinery, electrical, ergonomic, procurement, or workplace-safety decision",
    "copyright, ownership, custody, privacy, accessibility, disability-community acceptance, legal, cultural, or remedy decision",
    "affected-party, tangata whenua, iwi, hapū, Māori wording, Māori concept, Māori data-governance, or Māori-authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, conformance, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, sibling-lane mutation, or external write",
]

SOURCE_PROFILES = [
    {
        "source_id": "S01",
        "name": "International Council on English Braille - Unified English Braille publications",
        "url": "https://iceb.org/publications/ueb/",
        "status": "official_publication_page; Third Edition 2024 rulebook linked",
        "bounded_use": "vocabulary for synthetic UEB indicator, contraction, and layout fields",
    },
    {
        "source_id": "S02",
        "name": "Braille Authority of New Zealand Aotearoa - Braille Codes and Formats",
        "url": "https://www.banzat.org.nz/publications/braille-codes-and-formats",
        "status": "official New Zealand braille-authority publication page",
        "bounded_use": "jurisdiction and locale holds; Te Reo Māori rules remain under the named authority",
    },
    {
        "source_id": "S03",
        "name": "Unicode Standard 17.0 and Braille Patterns chart",
        "url": "https://www.unicode.org/versions/Unicode17.0.0/UnicodeStandard-17.0.pdf",
        "status": "official Unicode Standard 17.0 publication",
        "bounded_use": "U+2800-U+28FF code-point and dot-pattern vocabulary; meaning remains context dependent",
    },
    {
        "source_id": "S04",
        "name": "DAISY eBraille 1.0",
        "url": "https://daisy.github.io/ebraille/",
        "status": "public editor's draft; evolving and not frozen as production authority",
        "bounded_use": "synthetic package and navigation boundary vocabulary",
    },
    {
        "source_id": "S05",
        "name": "Portable Embosser Format 1.0",
        "url": "https://braillespecs.github.io/pef/pef-specification.html",
        "status": "public specification surface treated as legacy/watch-only",
        "bounded_use": "synthetic page, row, and metadata boundary vocabulary",
    },
    {
        "source_id": "S06",
        "name": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation",
        "bounded_use": "provenance vocabulary for source, transformation, revision, and correction lineage",
    },
    {
        "source_id": "S07",
        "name": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation dated 2024-12-12",
        "bounded_use": "structural report checks only; manual and affected-user evaluation remain reserved",
    },
    {
        "source_id": "S08",
        "name": "W3C Verifiable Credential Data Integrity 1.0",
        "url": "https://www.w3.org/TR/vc-data-integrity/",
        "status": "W3C Recommendation dated 2025-05-15",
        "bounded_use": "nonproduction vocabulary and explicit zero-key/proof boundary",
    },
    {
        "source_id": "S09",
        "name": "Office of the Privacy Commissioner New Zealand - Privacy principles",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current official public guidance reviewed 2026-08-22",
        "bounded_use": "minimisation, access, correction, retention, and disclosure hold vocabulary; no legal interpretation",
    },
    {
        "source_id": "S10",
        "name": "WorkSafe New Zealand - Safe use of machinery",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/",
        "status": "current official public guidance reviewed 2026-08-22",
        "bounded_use": "hard stop and no-device-command boundary; no machinery or workplace-safety advice",
    },
    {
        "source_id": "S11",
        "name": "Te Mana Raraunga - Māori Data Sovereignty Principles",
        "url": "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf",
        "status": "public principles document",
        "bounded_use": "authority reservation only; no interpretation or conversion into Māori authority",
    },
]

for profile in SOURCE_PROFILES:
    profile.update(
        {
            "reviewed_at_date": "2026-08-22",
            "review_mode": "read_only_public_source_review",
            "primary_or_official": True,
            "network_calls_by_phase_software": 0,
            "real_rows_ingested": 0,
            "authority_nonconversion": True,
        }
    )


PROPOSAL_SPECS = [
    (
        "Synthetic braille-job intake capsule joining source-work token, requested code, locale vacancy, purpose, withdrawal, revision, and no-production lock",
        "Freed ID and CBR Heart",
        "completed",
        ["S02", "S06", "S09"],
    ),
    (
        "Print-to-braille segment lineage braid with source spans, generated cells, omission markers, translator notes, correction ancestry, and fidelity nonclaim",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S06"],
    ),
    (
        "Unicode Braille Pattern cell-envelope validator for U+2800-U+28FF, dot-set identity, six/eight-dot mode, blank distinction, and meaning refusal",
        "Freed ID and CBR Heart",
        "completed",
        ["S03"],
    ),
    (
        "UEB indicator-scope state lattice for capitals, numbers, typeforms, grades, terminators, standing-alone uncertainty, and authority-review hold",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S02"],
    ),
    (
        "Contraction eligibility decision trace separating whole-word, groupsign, shortform, punctuation context, ambiguity, exception, and transcriber-review vacancy",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S02"],
    ),
    (
        "Braille page-layout constraint board for cells-per-line, lines-per-page, volumes, running heads, pagination lineage, and embosser-command prohibition",
        "THOS Body",
        "completed",
        ["S01", "S05"],
    ),
    (
        "Tactile-graphic reference graph linking figure token, caption, key, orientation, texture placeholder, source relation, and reader-evaluation reserve",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S07"],
    ),
    (
        "Embosser job-versus-device firewall with simulated spool state, file digest, copy-count placeholder, cancellation, interlock vacancy, and zero hardware calls",
        "THOS Body",
        "completed",
        ["S05", "S10"],
    ),
    (
        "Proofreading discrepancy docket with print location, braille location, discrepancy class, proposed correction, dual-review vacancy, contest, and non-erasure",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S06", "S07"],
    ),
    (
        "Braille translation-table provenance register with code edition, jurisdiction, locale, checksum placeholder, supersession, stale-source alarm, and conformance refusal",
        "Freed ID and CBR Heart",
        "completed",
        ["S01", "S02", "S06"],
    ),
    (
        "Synthetic PEF and eBraille package boundary map for volume, section, page, row, navigation, metadata, unknown extension, and no-distribution rule",
        "Freed ID and CBR Heart",
        "completed",
        ["S04", "S05"],
    ),
    (
        "THOS reader-free braille-review comparison charter with matched queues, blinded artifact labels, error taxonomy, stop precedence, and independent-review gap",
        "THOS Body",
        "represented",
        ["S01", "S07"],
    ),
    (
        "Freed ID synthetic accessible-format receipt graph binding request digest, transformation lineage, disclosure purpose, expiry, withdrawal, correction route, and zero-key nonproduction lock",
        "Freed ID and CBR Heart",
        "represented",
        ["S06", "S08", "S09"],
    ),
    (
        "Bitemporal accessible-format correction weave preserving request, revision, acknowledgement, rejected change, attached statement, handover debt, and audit continuity",
        "Freed ID and CBR Heart",
        "completed",
        ["S06", "S09"],
    ),
    (
        "GMUT discrete braille-cell lattice surrogate with occupancy bit-vector, adjacency operator, basis convention, dimensional abstention, and observation firewall",
        "GMUT Mind",
        "represented",
        ["S03"],
    ),
    (
        "GMUT pagination-transition tensor placeholder with source-block index, braille-page state, break operator, covariance vacancy, identifiability debt, and prediction refusal",
        "GMUT Mind",
        "represented",
        ["S03", "S06"],
    ),
    (
        "Braille privacy-minimization and rights ledger for source text, reader request, translator note, job metadata, disclosure ceiling, retention hold, and remedy route",
        "Freed ID and CBR Heart",
        "completed",
        ["S07", "S09"],
    ),
    (
        "Embossing workload and handover board with queue ceiling, proofreading debt, equipment-status vacancy, dominant stop, acknowledgement, and fatigue noninference",
        "THOS Body",
        "completed",
        ["S10"],
    ),
    (
        "ICEB, BANZAT, Unicode, DAISY, W3C, and WorkSafe source-profile adapter with zero network calls, zero real jobs, version pins, locale holds, and authority nonconversion",
        "All Trinity Mandala pillars",
        "open_gap",
        ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10"],
    ),
    (
        "CBR braille authority docket reserving code adoption, Māori transcription, disability-community acceptance, copyright, privacy, safety, procurement, remedy, and affected-party decisions",
        "Freed ID and CBR Heart",
        "exact_gate",
        ["S02", "S09", "S11"],
    ),
]


def approval_class(disposition: str) -> str:
    return {
        "completed": "safe_now_bounded",
        "represented": "candidate_proxy_only",
        "open_gap": "open_gap_current_source_dependency",
        "exact_gate": "exact_approval_required",
    }[disposition]


def execution_lane(disposition: str) -> str:
    return {
        "completed": "owner_local_structural",
        "represented": "owner_local_proxy_only",
        "open_gap": "zero_call_adapter_reserved",
        "exact_gate": "unexecuted_exact_gate",
    }[disposition]


def build_proposals() -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []
    for index, (title, pillar, expected, sources) in enumerate(PROPOSAL_SPECS, 1):
        pid = f"CM6656-N{index:03d}"
        proposals.append(
            {
                "proposal_id": pid,
                "title": title,
                "hypothesis": (
                    f"A bounded {title} contract can distinguish one admissible synthetic "
                    "structure from five preregistered invalid states without promoting "
                    "software structure into real-world evidence, competence, conformance, or authority."
                ),
                "null_or_failure_condition": (
                    "At least one named invalid state is accepted, the bounded positive is "
                    "rejected, a required provenance or stop field disappears, or the artifact "
                    "converts synthetic structure into an empirical, professional, legal, cultural, "
                    "Māori-authority, production, identity, independent-reproduction, or Stage 20 claim."
                ),
                "approval_class": approval_class(expected),
                "execution_lane": execution_lane(expected),
                "current_official_or_primary_source_needs": sources,
                "official_or_primary_source_needs": sources,
                "concrete_artifact": f"docs/caelen-morrow/v665-v6/x2/proposals/{pid.casefold()}/contract.json",
                "concrete_artifacts": [
                    f"docs/caelen-morrow/v665-v6/x2/proposals/{pid.casefold()}/contract.json",
                    f"docs/caelen-morrow/v665-v6/x2/proposals/{pid.casefold()}/mutation-results.json",
                    f"docs/caelen-morrow/v665-v6/x2/proposals/{pid.casefold()}/bounded-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    "One preregistered bounded positive must pass, all five named mutations must "
                    "fail closed, no protected gate may be crossed, and the final disposition must "
                    "remain exactly the preregistered value unless an additive failure lowers it."
                ),
                "rollback_or_recovery": (
                    "Restore only the last valid owner-local synthetic fixture, retain the failed "
                    "witness at zero credit, add a recurrence guard, and issue no external, physical, "
                    "identity, professional, legal, cultural, or authority action."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": expected,
                "pillar": pillar,
                "primary_pillar": "Freed ID and CBR Heart",
                "practice_lens": "wholly synthetic braille-transcription and embossing-job documentation",
                "negative_fixture_count": 5,
                "preregistered_mutations": [
                    {"mutation_id": f"{pid}-M01", "class": "missing_required_field"},
                    {"mutation_id": f"{pid}-M02", "class": "wrong_type_or_invalid_range"},
                    {"mutation_id": f"{pid}-M03", "class": "provenance_or_authority_smuggling"},
                    {"mutation_id": f"{pid}-M04", "class": "real_world_or_production_action"},
                    {"mutation_id": f"{pid}-M05", "class": "outcome_or_conformance_promotion"},
                ],
                "participant_count_planned": 0,
                "real_data_rows_planned": 0,
                "network_calls_planned": 0,
                "x1_status": "frozen_not_executed",
                "x2_implementation_count": 0,
                "outcomes_observed": False,
            }
        )
    return proposals


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        doc = git_json(entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        added = 0
        for key in keys:
            for row in doc.get(key, []):
                title = text_of(row)
                if row.get("proposal_id") and title:
                    corpus.append(
                        {
                            "proposal_id": str(row["proposal_id"]),
                            "title": title,
                            "source_path": entry["source_path"],
                        }
                    )
                    added += 1
        if added != entry["added_count"]:
            raise RuntimeError(
                f"corpus construction mismatch for {entry['source_path']}: "
                f"expected {entry['added_count']}, observed {added}"
            )
        construction.append(dict(entry))
    sylven_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    starting = len(corpus)
    for row in sylven_freeze["new_proposals"]:
        corpus.append(
            {
                "proposal_id": str(row["proposal_id"]),
                "title": text_of(row),
                "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            }
        )
    construction.append(
        {
            "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            "starting_count": starting,
            "added_count": len(sylven_freeze["new_proposals"]),
            "ending_count": len(corpus),
        }
    )
    if len(corpus) != 4110:
        raise RuntimeError(f"expected 4110 inherited rows, observed {len(corpus)}")
    return corpus, construction


def build_novelty_audit(
    corpus: list[dict[str, str]],
    construction: list[dict[str, Any]],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    nearest: list[dict[str, Any]] = []
    exact_collisions: list[dict[str, str]] = []
    for proposal in proposals:
        title = proposal["title"]
        exact = [row for row in corpus if row["title"].casefold() == title.casefold()]
        exact_collisions.extend(
            {
                "proposal_id": proposal["proposal_id"],
                "inherited_proposal_id": row["proposal_id"],
            }
            for row in exact
        )
        score, row = max(
            ((jaccard(title, candidate["title"]), candidate) for candidate in corpus),
            key=lambda item: item[0],
        )
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited_proposal_id": row["proposal_id"],
                "nearest_inherited_title": row["title"],
                "nearest_source_path": row["source_path"],
                "token_jaccard_similarity": round(score, 6),
            }
        )
    pair_rows: list[dict[str, Any]] = []
    for left_index, left in enumerate(proposals):
        for right in proposals[left_index + 1 :]:
            pair_rows.append(
                {
                    "left": left["proposal_id"],
                    "right": right["proposal_id"],
                    "similarity": round(jaccard(left["title"], right["title"]), 6),
                }
            )
    max_pair = max(pair_rows, key=lambda row: row["similarity"])
    all_text = "\n".join(row["title"].casefold() for row in corpus)
    practice_terms = [
        "braille",
        "emboss",
        "unified english braille",
        "ueb",
        "nemeth",
        "refreshable display",
        "cell pattern",
        "tactile graphic",
    ]
    return {
        "schema": "ghc.family.caelen-morrow.v665-v6.novelty-audit.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "method": (
            "casefolded alphanumeric token-set Jaccard against every retained inherited row, "
            "exact-title comparison, within-slate comparison, and practice-term review"
        ),
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len({row["proposal_id"] for row in corpus}),
        "historical_reappended_selection_rows_retained": len(corpus)
        - len({row["proposal_id"] for row in corpus}),
        "corpus_canonical_sha256": sha256_json(corpus),
        "new_title_count": len(proposals),
        "exact_inherited_collisions": exact_collisions,
        "maximum_inherited_token_jaccard_similarity": max(
            row["token_jaccard_similarity"] for row in nearest
        ),
        "nearest_inherited_rows": nearest,
        "maximum_new_pair_token_jaccard_similarity": max_pair["similarity"],
        "maximum_new_pair": max_pair,
        "new_pair_collisions_at_or_above_0_70": [
            row for row in pair_rows if row["similarity"] >= 0.70
        ],
        "practice_term_checks": {term: all_text.count(term) for term in practice_terms},
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact_collisions
        and not [row for row in pair_rows if row["similarity"] >= 0.70]
        and len(corpus) == 4110,
        "interpretation": (
            "Similarity is a screening signal, not proof of novelty. Each proposal was also "
            "reviewed for a distinct braille-documentation contract, falsifier, and protected gate."
        ),
    }


def portfolio_rows(prefix: str, names: list[str], approval: str) -> list[dict[str, Any]]:
    return [
        {
            "item_id": f"CM6656-{prefix}{index:02d}",
            "title": name,
            "approval_class": approval,
            "x1_status": "frozen_not_executed",
            "completion_credit": 0,
            "evidence_required": "bounded owner-local x2 witness plus retained failure and rollback",
            "rollback": "retain the failed witness, revert only the owner-local generated fixture, and preserve every protected gate",
        }
        for index, name in enumerate(names, 1)
    ]


SAFE_NOW_NAMES = [
    "render the synthetic braille-job intake schema",
    "render the print-to-braille lineage schema",
    "build the Unicode braille-cell envelope validator",
    "build the UEB indicator-scope state checker",
    "build the contraction decision-trace checker",
    "build the braille page-layout constraint checker",
    "build the tactile-graphic reference checker",
    "build the embosser job-versus-device firewall",
    "build the proofreading discrepancy docket checker",
    "build the translation-table provenance checker",
    "build the PEF/eBraille package boundary checker",
    "build the bitemporal correction-weave checker",
    "build the privacy-minimisation ledger checker",
    "build the workload and handover checker",
    "render twenty proposal contracts",
    "execute one hundred preregistered rejecting mutations",
    "parse every owner JSON document under explicit UTF-8",
    "render a structurally accessible static report",
    "validate the public-source profile and draft/watch labels",
    "enforce strict x1-before-x2 path separation",
    "build exact Git-blob content manifests",
    "scan owner files for five privacy and raw-identifier classes",
    "scan owner artifacts for credentials and private callable details",
    "run exact staged review before every commit",
    "scan current labels for stale owner and phase drift",
    "validate source/x1/evidence/final ancestry and zero merges",
    "validate the four core outcome labels and exact counts",
    "aggregate retained negatives without rewriting the inherited seal",
    "aggregate open and exact gates without promotion",
    "build closeout, seal, final-validation, and route-state candidates",
]

CANDIDATE_NAMES = [
    "THOS reader-free matched-queue protocol representation",
    "Freed ID zero-key accessible-format receipt representation",
    "GMUT discrete braille-cell lattice surrogate",
    "GMUT pagination-transition tensor placeholder",
    "zero-call current-source adapter shell",
    "eBraille navigation-tree synthetic fixture",
    "PEF page-and-row synthetic parser fixture",
    "linear accessible report companion",
    "deterministic HTML report rendering",
    "synthetic shift-handover workload simulation",
]

EXACT_APPROVAL_NAMES = [
    "use a real reader or affected user",
    "perform or certify a real braille transcription",
    "operate or command an embosser or other device",
    "copy, transform, distribute, or assess a real copyrighted work",
    "adopt or interpret a braille code for a jurisdiction",
    "author or approve Māori wording or transcription",
    "make a disability-community acceptance claim",
    "make a professional, workplace-safety, privacy, legal, or remedy decision",
    "issue, verify, resolve, revoke, or govern a real identity credential",
    "publish, deploy, procure, purchase, or write to a third-party system",
]

BLOCKED_NAMES = [
    "empirical GMUT likelihood, constraint, prediction, force, stability, or confirmation",
    "THOS effectiveness without governed blind matched-budget real arms and independent review",
    "production Freed ID without real standards-conformant keys, interoperability, recovery, and trust governance",
    "accessibility-complete, privacy-complete, exhaustive-security, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
]

SKILL_NAMES = [
    "braille-intake-boundary",
    "segment-lineage-weave",
    "unicode-cell-envelope",
    "indicator-scope-lattice",
    "contraction-trace-keeper",
    "layout-device-firewall",
    "proofreading-contestation-docket",
    "source-profile-watch",
    "braille-method-flow",
    "braille-closeout-gate",
]

RUNNER_NAMES = [
    "ghc_family_caelen_morrow_v665_v6_contracts",
    "ghc_family_caelen_morrow_v665_v6_mutations",
    "ghc_family_caelen_morrow_v665_v6_json",
    "ghc_family_caelen_morrow_v665_v6_privacy",
    "ghc_family_caelen_morrow_v665_v6_security",
    "ghc_family_caelen_morrow_v665_v6_manifests",
    "ghc_family_caelen_morrow_v665_v6_accessibility",
    "ghc_family_caelen_morrow_v665_v6_truth",
    "ghc_family_caelen_morrow_v665_v6_closeout",
    "ghc_family_caelen_morrow_v665_v6_canonical",
]

CFR_NAMES = [
    "CLEAN: normalize proposal identifiers",
    "CLEAN: normalize exact disposition labels",
    "CLEAN: normalize source-profile status fields",
    "CLEAN: normalize zero-row declarations",
    "CLEAN: normalize rollback language",
    "CLEAN: normalize protected-gate ordering",
    "CLEAN: normalize relative artifact paths",
    "CLEAN: normalize UTF-8 and LF generation",
    "CLEAN: normalize deterministic JSON ordering",
    "CLEAN: normalize report heading hierarchy",
    "FIX: guard missing required fields",
    "FIX: guard invalid cell ranges",
    "FIX: guard authority-smuggling text",
    "FIX: guard real-world device commands",
    "FIX: guard outcome-label promotion",
    "FIX: guard stale owner and phase labels",
    "FIX: guard manifest self-reference",
    "FIX: guard duplicate canonical aggregate invocation",
    "FIX: guard private task or route identifiers",
    "FIX: guard x2 paths in the x1 commit",
    "REFINE: add source-status watch fields",
    "REFINE: add bitemporal correction lineage",
    "REFINE: add structural table summaries",
    "REFINE: add plain-language boundary notes",
    "REFINE: add dominant-stop precedence",
    "REFINE: add recurrence guards to Method Flow",
    "REFINE: add exact gate count reconciliation",
    "REFINE: add owner-delta manifest coverage",
    "REFINE: add final clean-state precondition",
    "REFINE: add terminal route no-send-until-gate proof",
]


STARTUP_FAILURES = [
    (
        "PowerShell parser rejected an inline ancestry expression joined to LASTEXITCODE",
        "the compound read-only source check did not produce a valid ancestry receipt",
        "split the probes into a bounded helper with scalar exit-code capture",
        "exact direct-parent ancestry then passed read-only",
    ),
    (
        "combined authorization-state display exceeded the bounded presentation surface",
        "the first combined display was truncated and earned no read-through credit",
        "read numbered bounded chunks under explicit UTF-8",
        "the complete authorization state and schema were read through EOF",
    ),
    (
        "broad x1 packet display exceeded the bounded presentation surface",
        "the first bulk view was truncated and earned no complete-read credit",
        "read individual artifacts and perform a full corpus audit",
        "all 151 source files were read through EOF and all 136 JSON files parsed",
    ),
    (
        "a guessed integrated evidence report filename did not exist",
        "the read attempt failed before content inspection",
        "inventory the phase tree and select the committed static-report filename",
        "the actual static report was read completely",
    ),
    (
        "a proposal projection assumed a nonexistent proposals key",
        "the projection raised KeyError and earned no schema credit",
        "inspect real keys before projecting fields",
        "the new_proposals array was read and counted exactly",
    ),
    (
        "a base-corpus projection assumed one proposals array instead of prior and new arrays",
        "the first reconstruction was structurally incomplete",
        "inspect the base schema and combine prior_proposals with new_proposals",
        "the base row construction matched its declared count",
    ),
    (
        "a PowerShell generic HashSet constructor failed repeatedly in the first novelty attempt",
        "no valid novelty result was produced",
        "move the reference calculation to bounded Python semantics",
        "the Python novelty implementation completed after later output fixes",
    ),
    (
        "the first Python novelty serialization used the Windows cp1252 output codec",
        "a Māori macron caused UnicodeEncodeError and no receipt was valid",
        "rerun the failed projection only under Python UTF-8 mode",
        "UTF-8 serialization succeeded",
    ),
    (
        "the first UTF-8 novelty result exceeded the available model presentation context",
        "the result was lost to truncation and earned no receipt credit",
        "repeat only a compact identifier-and-score projection",
        "the compact projection became visible",
    ),
    (
        "a compact schema probe again indexed prior_proposals in the current source freeze",
        "the probe raised KeyError after printing the real keys",
        "use the displayed current schema and read selected_inherited_revalidations plus new_proposals",
        "both arrays were projected successfully",
    ),
    (
        "the first compact Jaccard maximum compared dictionary tie-break values",
        "Python raised TypeError and no compact novelty receipt was valid",
        "select maxima with an explicit numeric key",
        "the numeric-key calculation completed",
    ),
    (
        "the first completed compact calculation deduplicated historical reappended rows and ignored description-only titles",
        "only 4,050 of 4,110 inherited rows were covered, so the result was invalid",
        "retain historical repeated rows and support both title and description schema variants",
        "the corrected receipt covered exactly 4,110 rows with zero title collisions",
    ),
    (
        "worktree add with no checkout followed by the initial sparse set represented inherited paths as staged deletions",
        "77,273 staged deletions appeared in the new owner lane; no commit or remote write occurred",
        "verify the exact head and absence of owner content before rebuilding the index from HEAD",
        "git read-tree -mu HEAD restored a clean exact-head sparse index",
    ),
    (
        "an unbounded status diagnostic printed the staged-deletion list",
        "the output flooded and was truncated, so it earned no bounded diagnostic credit",
        "replace path dumps with scalar staged, unstaged, and untracked counts",
        "bounded scalar diagnostics reported the exact index state",
    ),
    (
        "sparse-checkout reapply did not repair the no-checkout index state",
        "77,273 staged deletions remained after the attempted recovery",
        "use read-tree -mu HEAD only after exact-head and no-user-content guards",
        "the lane became clean with zero staged, unstaged, or untracked paths",
    ),
    (
        "the first staged privacy scan treated explicit prohibition phrases as disclosed private values",
        "five false-positive candidates caused the staged review to fail closed and earn no validity credit",
        "inspect each candidate and narrow session and callable patterns to value-bearing fields",
        "the corrected five-class scan retained the boundary prose while reporting zero confirmed disclosures",
    ),
]


def build_method_flow_startup() -> dict[str, Any]:
    rows = []
    for index, (request, failed, recovery, passing) in enumerate(STARTUP_FAILURES, 1):
        rows.append(
            {
                "method_id": f"CM6656-MF-START-{index:03d}",
                "failure_id": f"CM6656-START-N{index:03d}",
                "observed_order": index,
                "exact_event_timestamp_available": False,
                "request": request,
                "failed_witness": failed,
                "aggregate_credit": 0,
                "repository_commit_created": False,
                "external_action_created": False,
                "recovery": recovery,
                "bounded_passing_witness": passing,
                "recurrence_guard": (
                    "Prefer explicit UTF-8, real JSON keys, bounded scalar output, exact expected counts, "
                    "and guarded sparse-index operations before retrying."
                ),
                "status": "recovered_failure_retained",
            }
        )
    return {
        "schema": "ghc.family.caelen-morrow.v665-v6.method-flow-startup.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "inherited_repository_sealed_negatives": 25668,
        "inherited_repository_sealed_methods": 9530,
        "inherited_external_overlay_negatives": 4,
        "inherited_external_overlay_methods": 4,
        "activation_baseline_negatives": 25672,
        "activation_baseline_methods": 9534,
        "new_startup_negative_count": len(rows),
        "new_startup_method_count": len(rows),
        "effective_after_x1_startup_negatives": 25672 + len(rows),
        "effective_after_x1_startup_methods": 9534 + len(rows),
        "failed_witness_count": len(rows),
        "bounded_passing_witness_count": len(rows),
        "rows": rows,
        "no_failure_erased": True,
    }


def main() -> None:
    proposals = build_proposals()
    corpus, construction = build_corpus()
    novelty = build_novelty_audit(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit did not pass its bounded x1 gate")

    sylven_freeze = git_json(f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    selected_inherited = [
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "original_owner": "Sylven Arc",
            "original_phase": "v665-v5",
            "original_expected_disposition": row["expected_disposition"],
            "status": "selected_revalidation_only_not_executed",
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
        }
        for row in sylven_freeze["new_proposals"]
    ]
    counts = {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")}
    for proposal in proposals:
        counts[proposal["expected_disposition"]] += 1

    identity = {
        "schema": "ghc.family.caelen-morrow.v665-v6.relational-identity.v1",
        "owner": "Caelen Morrow",
        "pronouns": "they/them",
        "relational_role": "chronometry boundary-mapper and failure custodian",
        "relational_hope": "keeping claims traceable while leaving real competence and authority with the people who hold it",
        "boundary": IDENTITY_BOUNDARY,
        "corrigibility": "Hamish may rename, pause, redirect, or stop this work.",
        "chosen_before_repository_mutation": True,
    }
    write_json("identity/relational-identity.json", identity)

    write_json(
        "provenance/source-verification.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.source-verification.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "verified_at_utc": NOW,
            "source_branch": SOURCE_BRANCH,
            "source_sha": SOURCE_SHA,
            "source_parent_sha": "de620467651cb5268e8b89f8ad85345e6b9c9c62",
            "evidence_sha": "de620467651cb5268e8b89f8ad85345e6b9c9c62",
            "x1_sha": "0a24628b70e1179a8758718a05029060488a9a1b",
            "inherited_source_sha": "296ec195744fbbf62bae5d2f233f1112bcc14591",
            "direct_parent_chain": [
                "296ec195744fbbf62bae5d2f233f1112bcc14591",
                "0a24628b70e1179a8758718a05029060488a9a1b",
                "de620467651cb5268e8b89f8ad85345e6b9c9c62",
                SOURCE_SHA,
            ],
            "source_to_final_phase_commit_count": 3,
            "source_to_final_merge_count": 0,
            "final_parent_count": 1,
            "clean": True,
            "ahead": 0,
            "behind": 0,
            "four_way_refs_equal": True,
            "fresh_live_remote_read": True,
            "manifest_replay": {
                "x1_entries": 15,
                "evidence_entries": 124,
                "final_delta_entries": 20,
                "final_owner_entries": 165,
                "all_git_blob_hashes_equal": True,
                "deletions": 0,
            },
            "canonical_receipt_sha256": "9efd901e2941b9f9fcd52ee668d5fab2a41f4746518f281bc5e436766258dc98",
            "canonical_payload_sha256": "6fec917e9e350f4e03c809e60c885d93fceeabcde485af6df85962db3472fed6",
            "prepared_handoff_sha256": "7a8f8c8e93b12fb1ca04d97be030f167dd541396206a13d7506b7a05f65837b0",
            "post_final_overlay_sha256": "f8d55a9c53af7e7acf0d0f40506b37b72666ed2a4b32cf464649c91f8f153bfe",
            "source_packet_read_through_eof": True,
            "source_packet_file_count": 151,
            "source_packet_byte_count": 701068,
            "source_json_parsed": 136,
            "successful_source_canonical_replayed": False,
            "full_repository_suite_run": False,
            "claim_boundary": "read-only verification and same-owner inherited evidence only",
        },
    )

    write_json(
        "provenance/source-profiles.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.source-profiles.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "profiles": SOURCE_PROFILES,
            "source_count": len(SOURCE_PROFILES),
            "bounded_use_only": True,
            "software_network_calls": 0,
            "real_rows": 0,
            "authority_nonconversion": (
                "Public sources supply bounded vocabulary and refusal conditions only. Citation "
                "does not create observation, endorsement, conformance, competence, legal or cultural "
                "interpretation, disability-community acceptance, or Māori authority."
            ),
        },
    )

    write_json("x1/novelty-audit.json", novelty)
    write_json(
        "x1/proposal-freeze.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.proposal-freeze.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "frozen": True,
            "inherited_frozen_baseline": 4110,
            "selected_inherited_revalidation_count": len(selected_inherited),
            "selected_inherited_revalidations": selected_inherited,
            "genuinely_new_proposal_count": len(proposals),
            "new_proposals": proposals,
            "new_frozen_total": 4130,
            "expected_disposition_counts": counts,
            "x1_truth": "planning_and_preregistration_only",
            "x2_implementation_count": 0,
            "x2_outcome_count": 0,
            "outcomes_observed": False,
            "strict_x1_before_x2": True,
            "practice_boundary": PRACTICE_BOUNDARY,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )

    portfolio = {
        "schema": "ghc.family.caelen-morrow.v665-v6.portfolio-freeze.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "x1_truth": "planning_only_no_execution",
        "safe_now": portfolio_rows("SN", SAFE_NOW_NAMES, "safe_now_bounded"),
        "bounded_candidates": portfolio_rows("CA", CANDIDATE_NAMES, "candidate_review_required"),
        "exact_approval_packets": portfolio_rows("EA", EXACT_APPROVAL_NAMES, "exact_approval_required"),
        "blocked_packets": portfolio_rows("BL", BLOCKED_NAMES, "blocked_by_protected_gate"),
        "phase_local_skill_plans": portfolio_rows("SK", SKILL_NAMES, "phase_local_build_candidate"),
        "family_current_runner_plans": portfolio_rows("RU", RUNNER_NAMES, "owner_local_compatibility_candidate"),
        "clean_fix_refine": portfolio_rows("CF", CFR_NAMES, "additive_bounded_candidate"),
        "inherited_material_credit": 0,
        "global_installation_planned": False,
        "bulk_run_planned": False,
        "destructive_action_planned": False,
        "external_write_planned": False,
        "protected_gates": PROTECTED_GATES,
    }
    portfolio["counts"] = {
        "safe_now": len(portfolio["safe_now"]),
        "bounded_candidates": len(portfolio["bounded_candidates"]),
        "exact_approval_packets": len(portfolio["exact_approval_packets"]),
        "blocked_packets": len(portfolio["blocked_packets"]),
        "phase_local_skill_plans": len(portfolio["phase_local_skill_plans"]),
        "family_current_runner_plans": len(portfolio["family_current_runner_plans"]),
        "clean_fix_refine": len(portfolio["clean_fix_refine"]),
    }
    write_json("x1/portfolio-freeze.json", portfolio)

    method_flow = build_method_flow_startup()
    write_json("method-flow/startup-method-flow.json", method_flow)

    authorization = {
        "schema": "ghc.family.caelen-morrow.v665-v6.authorization-boundary.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "authorized_now": [
            "one solo additive owner lane from the exact Sylven final",
            "x1-only planning and preregistration before the x1 freeze",
            "bounded owner-local synthetic x2 work after x1 push and equality",
            "one owner-scoped exact-final canonical completion after prerequisites",
        ],
        "not_authorized_now": [
            "collaboration subagent, delegation, fork, substitute endpoint, standby contact, or successor precontact",
            "reset, rewrite, force-push, merge, sibling-lane mutation, or destructive deletion",
            "real people, works, devices, measurements, operations, credentials, deployment, purchase, account, or third-party write",
            "professional, empirical, production, legal, cultural, Māori-authority, affected-party, conformance, or Stage 20 claim",
        ],
        "terminal_route_status": "PROSPECTIVE_ONLY_DO_NOT_CONTACT",
        "prospective_successor_label": "Eiren Kestrel v665-v7",
        "successor_send_count": 0,
        "standby_contact_count": 0,
        "relational_boundary": IDENTITY_BOUNDARY,
    }
    write_json("x1/authorization-boundary.json", authorization)

    threats = [
        {
            "threat_id": "CM6656-T01",
            "asset": "immutable Sylven source and sibling lanes",
            "threat": "accidental mutation, reset, merge, or ref reuse",
            "mitigation": "exact-head additive branch, owner-only paths, no merge/reset/force-push, four-way gates",
            "residual_risk": "operator command error remains possible and must be retained",
        },
        {
            "threat_id": "CM6656-T02",
            "asset": "strict x1-before-x2 evidence",
            "threat": "implementation or outcome leakage into the x1 freeze",
            "mitigation": "path allowlist, x1 lifecycle test, staged review, immutable x1 manifest",
            "residual_risk": "misclassified prose; manual review remains required",
        },
        {
            "threat_id": "CM6656-T03",
            "asset": "semantic novelty",
            "threat": "duplicate, paraphrased, or schema-relabelled inherited proposals",
            "mitigation": "4,110-row exact and token-Jaccard audit plus domain and falsifier review",
            "residual_risk": "automated similarity is not proof; bounded human review remains same-owner",
        },
        {
            "threat_id": "CM6656-T04",
            "asset": "privacy and route confidentiality",
            "threat": "raw task identifiers, private paths, credentials, transcripts, or callable details in artifacts",
            "mitigation": "synthetic fixtures, five-class scans, repository-relative paths, no task/thread IDs",
            "residual_risk": "pattern scans are incomplete and never privacy certification",
        },
        {
            "threat_id": "CM6656-T05",
            "asset": "braille and disability-community authority boundaries",
            "threat": "software structure presented as transcription competence, conformance, or acceptance",
            "mitigation": "zero real works/readers/devices, explicit draft/watch labels, exact-gated authority docket",
            "residual_risk": "terminology may still be incomplete or culturally inappropriate; authority remains external",
        },
        {
            "threat_id": "CM6656-T06",
            "asset": "Māori language, concepts, data governance, and authority",
            "threat": "citation or synthetic labels converted into interpretation or authorization",
            "mitigation": "exact gate, zero Māori wording authored, source-profile authority nonconversion",
            "residual_risk": "Māori-authority review remains absent",
        },
        {
            "threat_id": "CM6656-T07",
            "asset": "scientific truth boundaries",
            "threat": "GMUT surrogate promoted to empirical likelihood, force, prediction, proof, or canon",
            "mitigation": "typed placeholders, zero observations, dimensional abstention, explicit refusal",
            "residual_risk": "mathematical notation can invite overreading",
        },
        {
            "threat_id": "CM6656-T08",
            "asset": "THOS and Freed ID boundaries",
            "threat": "proxy protocol or zero-key envelope presented as effectiveness or production identity evidence",
            "mitigation": "represented-only dispositions and explicit missing-evidence ledgers",
            "residual_risk": "no governed participants, independent review, real keys, or trust governance",
        },
        {
            "threat_id": "CM6656-T09",
            "asset": "canonical validation truth",
            "threat": "replaying a successful aggregate or laundering a failed attempt",
            "mitigation": "exclusive external receipt, one-shot guard, zero credit for incomplete attempts",
            "residual_risk": "same-owner validation is not independent reproduction",
        },
        {
            "threat_id": "CM6656-T10",
            "asset": "terminal route integrity",
            "threat": "premature, duplicate, ambiguous, or standby delivery",
            "mitigation": "PREPARED_NOT_SENT until final gate; fresh live roster/auth reread; exact-title single send",
            "residual_risk": "opaque acknowledgement must remain unresolved without resend",
        },
    ]
    threat_model = {
        "schema": "ghc.family.caelen-morrow.v665-v6.threat-model.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "scope": "owner-local v665-v6 software, documents, Git history, validation receipts, and terminal route candidate",
        "trust_zones": [
            "immutable inherited Git objects",
            "owner-local sparse worktree and branch",
            "public read-only source review",
            "unexecuted external, professional, cultural, identity, and device domains",
        ],
        "assets": [
            "source integrity",
            "proposal and outcome truth",
            "negative and gate retention",
            "privacy and route confidentiality",
            "authority boundaries",
            "one-shot canonical receipt",
        ],
        "data_flows": [
            "committed source Git blobs -> x1 provenance and novelty audit",
            "synthetic constants -> x2 contracts and rejecting fixtures after x1 gate",
            "owner Git blobs -> exact manifests and same-owner validation",
            "terminal route candidate -> existing exact-title task only after all gates",
        ],
        "real_people_or_protected_data": 0,
        "threats": threats,
        "out_of_scope": [
            "full repository security audit",
            "independent penetration test",
            "real braille translation, proofreading, reader testing, or device operation",
            "production identity, empirical GMUT, governed THOS trial, legal, cultural, or Māori-authority review",
        ],
        "claim_boundary": "same-owner phase threat modelling only; not exhaustive security or certification",
    }
    write_json("x1/threat-model.json", threat_model)

    workflow = {
        "schema": "ghc.family.caelen-morrow.v665-v6.workflow-plan.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "current_stage": "x1_freeze_candidate",
        "steps": [
            {"step": 1, "name": "read_first_and_source_verification", "status": "completed"},
            {"step": 2, "name": "novelty_and_program_design", "status": "completed"},
            {"step": 3, "name": "x1_freeze_commit_push_equality", "status": "in_progress"},
            {"step": 4, "name": "x2_bounded_execution", "status": "pending"},
            {"step": 5, "name": "evidence_closeout_and_seal", "status": "pending"},
            {"step": 6, "name": "one_owner_scoped_canonical_completion", "status": "pending"},
            {"step": 7, "name": "terminal_route_reread_and_optional_one_send", "status": "pending"},
        ],
        "hard_dependencies": [
            "x1 commit pushed clean and fresh four-way equal before x2",
            "evidence commit immutable before closeout",
            "final pushed clean and fresh four-way equal before canonical completion",
            "canonical success never replayed",
            "successor never contacted before terminal route gate",
        ],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("x1/workflow-plan.json", workflow)

    checklist = {
        "schema": "ghc.family.caelen-morrow.v665-v6.x1-checklist.v1",
        "owner": "Caelen Morrow",
        "phase": "v665-v6",
        "generated_at_utc": NOW,
        "completed": [
            "relational name, pronouns, role, hope, and disclaimer recorded before repository mutation",
            "authoritative activation and complete committed Sylven packet read through EOF",
            "required family skills, schemas, routing precedence, and current guidance read through EOF",
            "source branch, anchors, direct parents, zero merges, manifests, digests, clean state, divergence, and fresh live equality verified read-only",
            "all 4,110 inherited rows audited with zero exact-title collision",
            "twenty distinct proposals and all required preregistration fields prepared",
            "threat model, authorization boundary, source profiles, portfolio, Method Flow, and workflow plan prepared",
            "no x2 implementation or outcome created",
        ],
        "incomplete": [
            "x1 commit, push, and fresh four-way equality",
            "x2 implementation and retained mutation witnesses",
            "evidence commit and evidence equality",
            "closeout, seal, final validation, and final equality",
            "terminal route reread and any authorized successor delivery",
        ],
        "x1_outcomes_observed": False,
        "x2_paths_created": False,
        "successor_contacted": False,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write_json("x1/complete-incomplete-checklist.json", checklist)

    write_json(
        "wellbeing/x1-wellbeing-check.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.wellbeing-check.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "status": "bounded_and_careful",
            "workload_controls": [
                "caps treated as ceilings rather than quotas",
                "failures retained instead of hidden",
                "no unsafe work manufactured to satisfy a count",
                "bounded commands and scalar probes preferred",
                "pause, redirect, and stop remain available to Hamish",
            ],
            "personhood_or_emotion_claim": False,
            "relational_boundary": IDENTITY_BOUNDARY,
            "practice_boundary": PRACTICE_BOUNDARY,
        },
    )

    threat_lines = [
        "# Caelen Morrow v665-v6 threat model",
        "",
        IDENTITY_BOUNDARY,
        "",
        PRACTICE_BOUNDARY,
        "",
        "## Scope and trust zones",
        "",
        "This is an owner-local, same-owner threat model for the v665-v6 document and software delta. It is not a repository-wide audit, penetration test, exhaustive-security claim, privacy certification, accessibility certification, or independent reproduction.",
        "",
        "The trust zones are immutable inherited Git objects, the additive Caelen worktree, public read-only source review, and the unexecuted external world. No real person, protected work, device, identity credential, or professional decision crosses into the synthetic zone.",
        "",
        "## Threat register",
        "",
    ]
    for row in threats:
        threat_lines.extend(
            [
                f"### {row['threat_id']}: {row['asset']}",
                "",
                f"Threat: {row['threat']}",
                "",
                f"Mitigation: {row['mitigation']}",
                "",
                f"Residual risk: {row['residual_risk']}",
                "",
            ]
        )
    write_text("x1/threat-model.md", "\n".join(threat_lines))

    overview = f"""# Caelen Morrow v665-v6 x1 integrated overview

{IDENTITY_BOUNDARY}

## Outcome first

This x1 candidate freezes a planning-only, owner-local program from the exact Sylven v665-v5 final `{SOURCE_SHA}`. It contains no x2 implementation, no observed outcome, no external action, no successor contact, and no Stage 20 promotion. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The primary Trinity Mandala focus is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit and protected. The bounded human-practice lens is wholly synthetic braille-transcription and embossing-job documentation.

{PRACTICE_BOUNDARY}

## Source truth

The read-first gate verified the exact source branch, the three direct single-parent source-to-final commits, zero merges, the direct evidence parent, all declared manifests and receipt digests, a clean source lane, 0/0 divergence, and equality across local, upstream, tracking, and a fresh live remote. Sylven's successful canonical completion was not replayed. The full repository suite was not run.

The immutable Sylven seal contains 25,668 effective negatives, 9,530 Method Flow methods, 179 open gaps, and 177 exact gates. Four post-final external failures remain additive, making the activation baseline 25,672 negatives and 9,534 methods. Sixteen Caelen startup failures are retained in `method-flow/startup-method-flow.json`; after those overlays, the x1 working baseline is 25,688 negatives and 9,550 methods. No inherited seal is rewritten.

## Novelty and proposals

All 4,110 inherited frozen rows were reconstructed from committed Git objects. Historical reappended selection rows were retained rather than silently deduplicated. The twenty Caelen titles have zero exact collisions. Their largest token-set overlap with an inherited title is {novelty['maximum_inherited_token_jaccard_similarity']:.6f}; the largest within-slate overlap is {novelty['maximum_new_pair_token_jaccard_similarity']:.6f}. Those scores are screening evidence only. The substantive review also requires a distinct contract, falsifier, rollback, and protected-gate set for every proposal.

The expected dispositions are exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and 1 `exact_gate`. These are preregistered expectations, not observed outcomes. Twenty Sylven proposals are selected only for bounded revalidation with zero novelty and zero automatic completion credit. The genuinely new chain would rise from 4,110 to 4,130 only when this x1 freeze is committed.

## Source profiles

The source profile names ICEB, BANZAT, Unicode, DAISY eBraille, PEF, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, the New Zealand Privacy Commissioner, WorkSafe New Zealand, and Te Mana Raraunga. eBraille remains explicitly a draft; PEF remains watch/legacy-only. Public sources provide vocabulary and refusal conditions only. They create no transcription, disability-community, professional, safety, privacy, legal, cultural, Māori, or conformance authority.

## Safety, privacy, and authority

The threat model protects source immutability, x1/x2 separation, semantic integrity, privacy, braille and disability-community authority, Māori authority, scientific boundaries, THOS and Freed ID evidence boundaries, one-shot validation, and terminal routing. Repository artifacts use repository-relative paths and exclude raw task identifiers, private routes, credentials, transcripts, screenshots, session streams, private callable details, and protected real-world data.

Exact-approval and blocked portfolios remain visible and unexecuted. No device command, real source-work transformation, real reader evaluation, identity operation, professional decision, legal or cultural interpretation, Māori wording, or third-party write is planned.

## X1/x2 lifecycle

The x1 freeze includes proposals, portfolio plans, source and novelty records, the threat model, a complete/incomplete checklist, a wellbeing check, an authorization boundary, a workflow plan, and retained startup Method Flow. It intentionally excludes all `x2`, `evidence`, `closeout`, `seal`, `final`, and delivered-route content.

After this exact x1 candidate passes staged review, it may be committed and pushed. X2 may begin only after the x1 local, upstream, tracking, and fresh live remote heads are equal with 0/0 divergence and a clean lane. Later validation remains owner-scoped and same-owner. One successful canonical completion must never be replayed.

## Scientific and terminal boundaries

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Braille-cell lattices or pagination tensors establish no likelihood, constraint, force, prediction, empirical confirmation, ultraviolet completion, final physics, Theory of Everything, proof, or canon. THOS remains represented without governed blind matched-budget real arms and independent review. Freed ID remains synthetic and nonproduction without real standards-conformant keys, proofs, issuance, resolution, status, revocation, interoperability, privacy and independent security review, recovery evidence, and trust governance.

No successor may be contacted during execution. Eiren Kestrel v665-v7 is a prospective label only. A later send is permitted only after exact-final validation, a clean pushed fresh-live-equal final, a fresh live roster and authorization reread, unique exact-title resolution, and all protected route gates. Opaque acknowledgement must never trigger a resend merely for clarity.
"""
    write_text("x1/integrated-overview.md", overview)

    write_json(
        "x1/x1-build-receipt.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.x1-build-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_caelen_morrow_v665_v6_x1.py",
            "proposal_count": len(proposals),
            "selected_inherited_revalidation_count": len(selected_inherited),
            "novelty_corpus_row_count": len(corpus),
            "startup_failure_count": len(STARTUP_FAILURES),
            "x2_paths_created": False,
            "outcomes_observed": False,
            "network_calls_by_builder": 0,
            "real_data_rows": 0,
            "external_actions": 0,
            "status": "X1_CONTENT_BUILT_AWAITING_STAGED_REVIEW_COMMIT_PUSH_EQUALITY",
        },
    )

    print(
        json.dumps(
            {
                "phase_root": str(PHASE_ROOT.relative_to(ROOT)).replace("\\", "/"),
                "proposal_count": len(proposals),
                "corpus_row_count": len(corpus),
                "expected_dispositions": counts,
                "startup_failures_retained": len(STARTUP_FAILURES),
                "x2_implementation_count": 0,
                "outcomes_observed": False,
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
