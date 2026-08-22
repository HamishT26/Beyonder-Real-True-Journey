"""Build and exactly stage Tamar Vey's planning-only v665-v3 x1 freeze.

The builder is deliberately x1-only: it records hypotheses, nulls, sources,
approval classes, execution lanes, artifact contracts, falsifiers, rollback
paths, protected gates, and expected dispositions. It executes no evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "docs/tamar-vey/v665-v3/"
PHASE_ID = "v665-v3"
OWNER = "Tamar Vey"
PRONOUNS = "she/they"
ROLE = "relational evidence-and-recovery steward"
HOPE = "keep every claim, correction, and handoff inspectable and safely retractable"
BRANCH = "codex/GHC-Family/tamar-vey-v665-v3-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/liora-venn-v665-v2-full-tools"
ORIN_SOURCE = "f4abecafb107f4ac840c09b46a6b30079171816d"
LIORA_X1 = "1a5fe2e58c3e9fa3ae51a04d0971f30106cbcf38"
LIORA_EVIDENCE = "420f73d2bb5c7570a886cd04a37d81bf03449bf2"
SOURCE_FINAL = "a559ab2dfe46cace97fd03c09f1018477fdc09f4"
SOURCE_RECEIPT_SHA256 = "6b8d009e07a9641c937ea060db7e610dbf9f0a02a2714861c8e40c7cc5a23a14"
RECORDED_UTC = "2026-08-22T01:01:33Z"
RECORDED_NZ = "2026-08-22T13:01:33+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
INHERITED_PROPOSALS = 4_050
INHERITED_NEGATIVES = 25_307
INHERITED_METHODS = 9_169
INHERITED_OPEN_GAPS = 176
INHERITED_EXACT_GATES = 174
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "Freed ID/CBR Heart"
PRACTICE_LENS = "wholly synthetic fossil preparation and collections custody"

PROTECTED_GATES = [
    "real fossil, rock, cast, jacket, matrix, fragment, tool, treatment, or specimen action",
    "real empirical row, likelihood, parameter constraint, force, prediction, or GMUT confirmation",
    "real participant, preparator, curator, collector, operator, or matched-budget arm",
    "real key, proof, issuance, resolution, status, revocation, interoperability, or trust governance",
    "professional, workplace, dust, chemical, tool, radiation, transport, or environmental safety decision",
    "ownership, custody, collecting, export, return, repatriation, legal, cultural, or remedy decision",
    "affected-party, tangata whenua, iwi, hapū, or Māori wording, data-governance, or authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, or sibling-lane mutation",
]

BUILDER = "scripts/build_ghc_family_v665_v3_x1.py"
TEST = "tests/test_ghc_family_tamar_v665_v3_x1.py"
BASE_DOCS = [
    f"{PREFIX}x1/auth-roster-receipt.json",
    f"{PREFIX}x1/family-index-plan.json",
    f"{PREFIX}x1/novelty-audit.json",
    f"{PREFIX}x1/phase-charter.json",
    f"{PREFIX}x1/portfolio-freeze.json",
    f"{PREFIX}x1/proposal-freeze.json",
    f"{PREFIX}x1/source-ledger.json",
    f"{PREFIX}x1/source-verification.json",
    f"{PREFIX}x1/startup-method-flow.json",
    f"{PREFIX}x1/threat-model-plan.json",
    f"{PREFIX}x1/wellbeing-plan.json",
    f"{PREFIX}x1/workflow-plan.json",
    f"{PREFIX}x1/x1-overview.md",
]
SELF_EXCLUSIONS = [
    f"{PREFIX}x1/x1-content-manifest.json",
    f"{PREFIX}x1/x1-stage-candidate.json",
    f"{PREFIX}x1/x1-staged-review.json",
]
BASE_PATHS = sorted([BUILDER, TEST, *BASE_DOCS])
INTENDED_PATHS = sorted([*BASE_PATHS, *SELF_EXCLUSIONS])


class X1Error(RuntimeError):
    """Fail-closed x1 invariant."""


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        list(args), cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if check and result.returncode:
        raise X1Error(
            f"command failed ({result.returncode}): {' '.join(args)}\n"
            + result.stderr.decode("utf-8", errors="replace")
        )
    return result


def git(*args: str) -> str:
    return run("git", *args).stdout.decode("utf-8", errors="strict").strip()


def git_blob(path: str, revision: str = SOURCE_FINAL) -> bytes:
    return run("git", "show", f"{revision}:{path}").stdout


def strict_json_bytes(raw: bytes, label: str) -> Any:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise X1Error(f"duplicate JSON key {key!r} in {label}")
            result[key] = value
        return result

    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise X1Error(f"strict JSON failure in {label}: {exc}") from exc


def git_json(path: str, revision: str = SOURCE_FINAL) -> Any:
    return strict_json_bytes(git_blob(path, revision), f"{revision}:{path}")


def pretty_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write_json(relative: str, value: Any) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(pretty_bytes(value))


def write_text(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def reconstruct_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    audit_path = "docs/liora-venn/v665-v2/x1/novelty-audit.json"
    liora_freeze = "docs/liora-venn/v665-v2/x1/proposal-freeze.json"
    inherited_audit = git_json(audit_path)
    rows: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, source in enumerate(inherited_audit["corpus_construction"]):
        payload = git_json(source["source_path"])
        selected = (
            [*payload.get("prior_proposals", []), *payload.get("new_proposals", [])]
            if index == 0
            else list(payload.get("new_proposals", []))
        )
        before = len(rows)
        rows.extend(
            {
                "proposal_id": str(row.get("proposal_id") or row.get("id") or ""),
                # Two inherited remaster packets predate the normalized title
                # field and preserve their proposal text under description.
                # Treat that exact legacy field as the title surface so all
                # 4,050 frozen rows remain in the semantic-novelty corpus.
                "title": str(row.get("title") or row.get("description") or ""),
                "source_path": source["source_path"],
            }
            for row in selected
        )
        construction.append(
            {
                "source_path": source["source_path"],
                "starting_count": before,
                "added_count": len(selected),
                "ending_count": len(rows),
            }
        )
    liora = git_json(liora_freeze)
    before = len(rows)
    rows.extend(
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_path": liora_freeze,
        }
        for row in liora["new_proposals"]
    )
    construction.append(
        {
            "source_path": liora_freeze,
            "starting_count": before,
            "added_count": len(liora["new_proposals"]),
            "ending_count": len(rows),
        }
    )
    if len(rows) != INHERITED_PROPOSALS:
        raise X1Error(f"expected {INHERITED_PROPOSALS} rows, found {len(rows)}")
    if any(not row["proposal_id"] or not row["title"] for row in rows):
        raise X1Error("corpus contains an incomplete row")
    return rows, construction


TITLES = [
    "Synthetic fossil-preparation case capsule with surrogate specimen token, accession vacancy, source snapshot, revision braid, cancellation, and no-object-action rule",
    "Jacket, matrix, fragment, cast, mould, support, tray, label, and digital-surrogate relation graph with orphan and contradiction quarantine",
    "Locality, stratigraphic horizon, collector-source, coordinate-precision ceiling, geological-context vacancy, and sensitive-site disclosure firewall",
    "Surface deposit, fracture, deformation, mineral-replacement cue, prior-intervention trace, uncertainty, and diagnosis-refusal vocabulary",
    "Consolidant, adhesive, solvent, coating, release-layer, and fill-material lot ledger with substitution, compatibility vacancy, and treatment hold",
    "Pneumatic pen, micro-abrasive, needle, brush, magnification, imaging, CT, sampling, and destructive-tool reservation board",
    "Fragment custody, container seal, movement placeholder, loan, transfer, return, deaccession, repatriation, and action-authorization firewall",
    "Fossil preparation condition-map accessibility companion with text topology, noncolour state, keyboard order, uncertainty legend, and affected-user-review reservation",
    "Accession, locality, identification, association, condition, and intervention correction braid with supersession, contestation, readback, and non-erasure",
    "Dust cue, vibration cue, isolation placeholder, unfinished queue, fatigue threshold, stop state, workload ceiling, and shift-handover docket",
    "Typed de Rham current test-form, degree, orientation, support, action, boundary, and boundary-of-boundary obligation tribunal",
    "Current mass, test-form comass, flat norm, coefficient group, unit domain, compactness vacancy, and invalid-comparison refusal",
    "Rectifiable and integral-current multiplicity, tangent-plane, carrier-set, pushforward, slicing, and closure-obligation board",
    "Varifold weight, Grassmannian fibre, first variation, stationarity, mean-curvature vacancy, regularity hold, and theorem-nonclaim board",
    "GMUT geometric-measure-theory surface and defect proxy with field map, EFT scope, covariance vacancy, identifiability hold, and observation firewall",
    "THOS fossil-preparation discrepancy and custody-handover matched-budget protocol with sealed synthetic arms, stop rules, and zero participants",
    "Freed ID synthetic specimen, fragment, treatment-event, custody, and restriction relation profile with absent keys, proofs, status, and trust decisions",
    "Thermo-Psyche fracture energy, surface measure, curvature proxy, material-domain, unit, uncertainty, and agency-nonconversion classifier",
    "Paleobiology Database fossil-occurrence versioned-schema adapter with zero calls, zero rows, provenance slots, selection holds, and likelihood refusal",
    "CBR fossil land, locality privacy, ownership, custody, sampling, return, repatriation, taonga, remedy, affected-party, legal, cultural, and Māori-authority matrix",
]

PILLARS = [
    "Freed ID/CBR Heart", "Freed ID/CBR Heart", "Freed ID/CBR Heart",
    "THOS Body", "THOS Body", "THOS Body", "Freed ID/CBR Heart", "THOS Body",
    "Freed ID/CBR Heart", "THOS Body", "GMUT Mind", "GMUT Mind", "GMUT Mind",
    "GMUT Mind", "GMUT Mind", "THOS Body", "Freed ID/CBR Heart", "GMUT Mind",
    "GMUT Mind", "Freed ID/CBR Heart",
]

SOURCE_NEEDS = [
    ["TVS03", "TVS04"], ["TVS03", "TVS04"], ["TVS03", "TVS09", "TVS10", "TVS11"],
    ["TVS03", "TVS08"], ["TVS03", "TVS09"], ["TVS09", "TVS10"],
    ["TVS03", "TVS10", "TVS11"], ["TVS05"], ["TVS03", "TVS04"], ["TVS09"],
    ["TVS01"], ["TVS01"], ["TVS01"], ["TVS02"], ["TVS01", "TVS02"],
    ["TVS05", "TVS09"], ["TVS03", "TVS04", "TVS06"], ["TVS01", "TVS02"],
    ["TVS07", "TVS08"], ["TVS09", "TVS10", "TVS11", "TVS12"],
]


def build_proposals() -> list[dict[str, Any]]:
    expected = ["completed"] * 14 + ["represented"] * 4 + ["open_gap", "exact_gate"]
    proposals: list[dict[str, Any]] = []
    for index, (title, pillar, source_ids, outcome) in enumerate(
        zip(TITLES, PILLARS, SOURCE_NEEDS, expected, strict=True), 1
    ):
        if outcome == "completed":
            approval, lane = "safe_now_bounded", "owner_local_structural"
        elif outcome == "represented":
            approval, lane = "candidate_bounded_proxy", "owner_local_zero_person_proxy"
        elif outcome == "open_gap":
            approval, lane = "open_gap_real_evidence_required", "zero_call_zero_row_adapter"
        else:
            approval, lane = "exact_approval_required", "authority_reservation_only"
        proposal_id = f"TV6653-N{index:03d}"
        proposals.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "pillar": pillar,
                "practice_lens": PRACTICE_LENS,
                "hypothesis": (
                    f"The bounded {title} contract can reject five preregistered invalid states "
                    "without crossing any empirical, participant, professional, identity, legal, "
                    "cultural, Māori-authority, production, or Stage 20 boundary."
                ),
                "null_or_failure_condition": (
                    "At least one preregistered invalid state is accepted, an acceptance invariant "
                    "fails, or the artifact promotes synthetic structure into external evidence or authority."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": source_ids,
                "concrete_artifact": f"{PREFIX}x2/proposals/{proposal_id.casefold()}/contract.json",
                "falsifier_or_acceptance_gate": (
                    "One bounded positive must pass, five named mutations must fail closed, "
                    "and every protected gate must remain explicit."
                ),
                "rollback_or_recovery": (
                    "Restore only the last valid generated surrogate fixture, preserve the failed "
                    "witness at zero credit, and never issue an external or physical action."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": outcome,
                "negative_fixture_count": 5,
                "participant_count_planned": 0,
                "real_data_rows_planned": 0,
                "x1_status": "frozen_not_executed",
            }
        )
    return proposals


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / max(1, len(a | b))


def novelty_audit(
    proposals: list[dict[str, Any]],
    corpus: list[dict[str, str]],
    construction: list[dict[str, Any]],
) -> dict[str, Any]:
    inherited_titles = {row["title"].casefold() for row in corpus}
    exact = [p["proposal_id"] for p in proposals if p["title"].casefold() in inherited_titles]
    nearest: list[dict[str, Any]] = []
    for proposal in proposals:
        best = max(corpus, key=lambda row: similarity(proposal["title"], row["title"]))
        nearest.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_inherited_proposal_id": best["proposal_id"],
                "nearest_inherited_title": best["title"],
                "nearest_source_path": best["source_path"],
                "token_jaccard_similarity": round(
                    similarity(proposal["title"], best["title"]), 6
                ),
            }
        )
    pairs = [
        {
            "left": left["proposal_id"],
            "right": right["proposal_id"],
            "token_jaccard_similarity": round(similarity(left["title"], right["title"]), 6),
        }
        for left_index, left in enumerate(proposals)
        for right in proposals[left_index + 1 :]
        if similarity(left["title"], right["title"]) >= 0.70
    ]
    pair_max = max(
        similarity(left["title"], right["title"])
        for left_index, left in enumerate(proposals)
        for right in proposals[left_index + 1 :]
    )
    terms = [
        "fossil-preparation",
        "paleobiology database",
        "varifold",
        "geometric-measure-theory",
        "integral-current",
        "rectifiable current",
        "flat norm",
        "comass",
    ]
    canonical = sorted(
        corpus, key=lambda row: (row["proposal_id"], row["title"], row["source_path"])
    )
    result = {
        "schema": "ghc.family.tamar.v665-v3.novelty-audit.v1",
        "method": (
            "casefolded alphanumeric token-set Jaccard against every reconstructed inherited "
            "row, exact-title comparison, within-slate comparison, and practice-term review"
        ),
        "corpus_row_count": len(corpus),
        "corpus_construction": construction,
        "corpus_canonical_sha256": sha256(canonical_bytes(canonical)),
        "new_title_count": len(proposals),
        "new_frozen_total": len(corpus) + len(proposals),
        "exact_inherited_collisions": exact,
        "nearest_inherited_rows": nearest,
        "maximum_inherited_token_jaccard_similarity": max(
            row["token_jaccard_similarity"] for row in nearest
        ),
        "new_pair_collisions_at_or_above_0_70": pairs,
        "maximum_new_pair_token_jaccard_similarity": round(pair_max, 6),
        "practice_term_checks": {
            term: sum(term in row["title"].casefold() for row in corpus) for term in terms
        },
        "valid": not exact and not pairs,
    }
    if not result["valid"]:
        raise X1Error("semantic novelty audit failed")
    return result


def sources() -> list[dict[str, Any]]:
    rows = [
        ("TVS01", "Federer and Fleming, Normal and Integral Currents", "https://doi.org/10.2307/1970227", "primary_research", "stable", "current, boundary, mass, flat-norm, compactness, and closure vocabulary"),
        ("TVS02", "Allard, On the first variation of a varifold", "https://annals.math.princeton.edu/1972/95-3/p03", "primary_research", "stable", "varifold weight, first variation, stationarity, and regularity obligations"),
        ("TVS03", "W3C PROV-O Recommendation", "https://www.w3.org/TR/prov-o/", "official_standard", "stable", "entity, activity, agent, derivation, and correction provenance"),
        ("TVS04", "PREMIS Data Dictionary 3.0", "https://www.loc.gov/standards/premis/v3/index.html", "official_standard", "current", "object, event, agent, rights, fixity, and preservation fields"),
        ("TVS05", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "official_standard", "current", "structural accessibility while manual evaluation remains reserved"),
        ("TVS06", "Verifiable Credential Data Integrity 1.0", "https://www.w3.org/TR/vc-data-integrity/", "official_standard", "current", "proof-model boundaries and refusal to fabricate cryptographic completion"),
        ("TVS07", "Paleobiology Database Data Service 1.2", "https://paleobiodb.org/data1.2/", "primary_project_api", "watch", "versioned fossil-occurrence schema planning with zero calls and rows"),
        ("TVS08", "Paleobiology Database API primary publication", "https://doi.org/10.1017/pab.2015.39", "primary_research", "stable", "API scope, versioning, record classes, and attribution context"),
        ("TVS09", "Department of Conservation research and collection permits", "https://www.doc.govt.nz/get-involved/apply-for-permits/research-and-collection/", "official_guidance", "current", "collection and research authority vacancies; informational use only"),
        ("TVS10", "Protected Objects Act 1975 natural science objects schedule", "https://www.legislation.govt.nz/act/public/1975/41/en/latest/sections/DLM432116/DLM432617", "official_legislation_source", "watch", "legal-scope awareness only; no interpretation or decision"),
        ("TVS11", "Te Mana Raraunga Principles of Māori Data Sovereignty", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "primary_affected_authority_source", "current", "authority reservation, provenance, consent, governance, and kaitiakitanga"),
        ("TVS12", "Smithsonian Open Access FAQ and developer context", "https://www.si.edu/openaccess/faq", "official_collection_source", "current", "rights, accession, metadata, API-key, and zero-row boundaries"),
    ]
    return [
        {
            "source_id": source_id,
            "title": title,
            "url": url,
            "source_class": source_class,
            "status": status,
            "phase_use": use,
            "accessed_on": "2026-08-22",
            "real_rows_ingested": 0,
            "downloaded_dataset_bytes": 0,
            "authority_conferred": False,
        }
        for source_id, title, url, source_class, status, use in rows
    ]


STARTUP_FAILURE_ROWS = [
    ("TV6653-START-N001", "a PowerShell inventory wrapper ended with an empty pipeline after foreach", "materialize results into a bounded array before formatting"),
    ("TV6653-START-N002", "the first combined authorization-state read exceeded its display bound", "read the immutable file in numbered fixed-size chunks"),
    ("TV6653-START-N003", "the first full Liora proposal-freeze rendering exceeded its display bound", "read only the missing numbered line interval"),
    ("TV6653-START-N004", "the first full Method Flow overlay rendering exceeded its display bound", "read three numbered fixed-size intervals through EOF"),
    ("TV6653-START-N005", "an all-lifecycle manifest helper returned no attributable payload within its bound", "replay each immutable lifecycle manifest separately"),
    ("TV6653-START-N006", "a combined uniqueness and live-remote wrapper returned no attributable payload", "split local uniqueness from one scalar live-remote probe"),
    ("TV6653-START-N007", "the no-checkout worktree and sparse wrapper timed out after branch registration", "inspect path, branch, sparse state, index, and processes before accepting the completed background result"),
    ("TV6653-START-N008", "a post-timeout status projection rendered an overbroad deletion view while Git was active", "wait for process exit and use counts plus bounded samples"),
    ("TV6653-START-N009", "a read assumed an inherited sparse path was materialized", "read the exact immutable Git blob instead of widening sparse checkout"),
    ("TV6653-START-N010", "the first Node novelty probe lost string quoting through PowerShell backtick handling", "pass the unchanged read-only program as a literal here-string"),
    ("TV6653-START-N011", "the first apply-patch transport exceeded the Windows command-line length limit before execution", "send bounded patches through the direct apply-patch tool"),
    ("TV6653-START-N012", "a PTY apply-patch fallback was denied before reading any patch bytes", "use the direct apply-patch tool with exact absolute owner-lane paths"),
    ("TV6653-START-N013", "the first x1 build rejected two inherited remaster packets whose proposal text used the legacy description field instead of title", "normalize only that exact legacy description field into the 4,050-row novelty title surface"),
]


def startup_methods() -> list[dict[str, Any]]:
    return [
        {
            "failed_witness_id": negative_id,
            "failed_witness": failure,
            "failed_witness_status": "retained_zero_credit",
            "method_id": f"TV6653-START-M{index:03d}",
            "recovery_method": recovery,
            "passing_witness": f"bounded recovery for {negative_id}",
            "preferred_for_trigger": True,
            "failure_erased": False,
            "repository_mutation_at_failure": False,
        }
        for index, (negative_id, failure, recovery) in enumerate(STARTUP_FAILURE_ROWS, 1)
    ]


def portfolio_rows(
    prefix: str, subjects: list[str], approval: str
) -> list[dict[str, Any]]:
    return [
        {
            "record_id": f"{prefix}-{index:03d}",
            "title": subject,
            "approval_class": approval,
            "x1_status": "frozen_not_executed",
            "completion_credit": 0,
            "rollback": (
                "remove only the generated owner-local fixture before commit and retain "
                "any failed witness"
            ),
            "protected_gates": PROTECTED_GATES,
        }
        for index, subject in enumerate(subjects, 1)
    ]


def build_portfolios() -> dict[str, Any]:
    safe_now = [
        "validate surrogate fossil case identity and cancellation fields",
        "validate jacket-matrix-fragment relation cardinalities",
        "enforce locality precision ceilings on synthetic coordinates",
        "separate observation cues from diagnosis labels",
        "track synthetic treatment-material substitutions and holds",
        "refuse tool and destructive-action authorization states",
        "separate custody relations from ownership and authority",
        "audit noncolour status and text topology",
        "preserve append-only correction ancestry",
        "enforce dominant stop and workload ceilings",
        "type de Rham current degrees and supports",
        "check boundary-of-boundary symbolic invariants",
        "separate mass, comass, and flat-norm domains",
        "require coefficient-group declarations",
        "require rectifiability and integrality hypotheses",
        "validate pushforward and slicing preconditions",
        "type varifold weight and Grassmannian fields",
        "reserve stationarity and regularity conclusions",
        "maintain a GMUT observation firewall",
        "maintain a thermo-psyche category firewall",
        "render a zero-person THOS comparison protocol",
        "render a nonproduction Freed ID relation profile",
        "render a zero-call PBDB adapter contract",
        "render a CBR exact-authority matrix",
        "build deterministic canonical JSON witnesses",
        "run five rejecting mutations per frozen proposal",
        "build exact owner-content manifests",
        "scan five privacy and raw-identifier classes",
        "emit a structurally accessible static report plan",
        "emit a fail-closed Stage 20 nonpromotion plan",
    ]
    candidates = [
        "bounded relation-graph prototype",
        "bounded precision-ceiling prototype",
        "bounded observation-vocabulary prototype",
        "bounded material-hold prototype",
        "bounded custody-braid prototype",
        "bounded accessibility-companion prototype",
        "bounded current-boundary prototype",
        "bounded mass-comass prototype",
        "bounded rectifiability-obligation prototype",
        "bounded varifold-first-variation prototype",
        "bounded GMUT proxy prototype",
        "bounded THOS zero-person protocol prototype",
        "bounded Freed ID nonproduction profile prototype",
        "bounded zero-call PBDB adapter prototype",
        "bounded Stage 20 nonpromotion prototype",
    ]
    exact = [
        "collect, handle, prepare, sample, image, scan, or treat a real fossil or material",
        "operate pneumatic, abrasive, sharp, imaging, radiation, lifting, or transport equipment",
        "decide ownership, custody, collecting, export, return, deaccession, or repatriation",
        "disclose a real sensitive locality or traditional-knowledge record",
        "interpret law, permits, safety duties, cultural meaning, or remedy entitlement",
        "make Māori wording, tikanga, taonga, data-governance, or authority decisions",
        "enrol participants or run real THOS comparison arms",
        "use real identity keys, proofs, lifecycle services, or trust governance",
        "download and fit real paleobiological data or publish empirical GMUT results",
        "deploy, certify, or promote any system or Stage 20 claim",
    ]
    blocked = [
        "mutate a sibling or shared branch",
        "use credentials, accounts, private keys, or API secrets",
        "elevate, weaken host security, activate Sandbox or Hyper-V, or reboot",
        "delete inherited negatives, memory, identity, authority, or user material",
        "claim consciousness, personhood, AGI, ASI, Theory of Everything, proof, or canon",
    ]
    skills = [
        ("ghc-family-fossil-case-capsule-validator", "validate case identity and cancellation"),
        ("ghc-family-fossil-relation-graph-auditor", "audit typed surrogate relations"),
        ("ghc-family-sensitive-locality-precision-firewall", "enforce precision ceilings"),
        ("ghc-family-condition-vocabulary-diagnosis-refuser", "separate observation from diagnosis"),
        ("ghc-family-treatment-material-hold-checker", "validate zero-material holds"),
        ("ghc-family-custody-correction-braid-auditor", "preserve custody and correction ancestry"),
        ("ghc-family-integral-current-obligation-checker", "check current and boundary obligations"),
        ("ghc-family-varifold-nonclaim-guard", "reserve stationarity and regularity conclusions"),
        ("ghc-family-paleodata-zero-row-firewall", "keep external access at zero calls and rows"),
        ("ghc-family-fossil-authority-matrix-reviewer", "preserve legal, cultural, and Māori gates"),
    ]
    runners = [
        "case_capsule",
        "relation_graph",
        "locality_precision",
        "condition_vocabulary",
        "material_hold",
        "custody_braid",
        "integral_current",
        "varifold_nonclaim",
        "paleodata_zero_row",
        "authority_matrix",
    ]
    clean = [
        f"CLEAN/FIX/REFINE {index:02d}: {safe_now[(index - 1) % len(safe_now)]}"
        for index in range(1, 31)
    ]
    return {
        "schema": "ghc.family.tamar.v665-v3.portfolio-freeze.v1",
        "inherited_completion_credit": 0,
        "safe_now": portfolio_rows("TV6653-SAFE", safe_now, "safe_now_bounded"),
        "bounded_candidates": portfolio_rows("TV6653-CAND", candidates, "candidate_bounded"),
        "exact_approval": portfolio_rows("TV6653-EXACT", exact, "exact_approval_required"),
        "blocked": portfolio_rows(
            "TV6653-BLOCK", blocked, "blocked_prohibited_or_unavailable"
        ),
        "skill_ideas": [
            {
                "record_id": f"TV6653-SKILL-{index:03d}",
                "slug": slug,
                "purpose": purpose,
                "installation_scope": "phase_local_only",
                "x1_status": "frozen_not_built",
                "completion_credit": 0,
            }
            for index, (slug, purpose) in enumerate(skills, 1)
        ],
        "runner_ideas": [
            {
                "record_id": f"TV6653-RUNNER-{index:03d}",
                "caller": f"ghc_family_v665_v3_{profile}.py",
                "profile": profile,
                "compatibility": "family_current_ghc_family_prefix",
                "x1_status": "frozen_not_built",
                "completion_credit": 0,
            }
            for index, profile in enumerate(runners, 1)
        ],
        "clean_fix_refine": portfolio_rows(
            "TV6653-CFR", clean, "safe_now_additive_cleanup"
        ),
        "counts": {
            "safe_now": 30,
            "bounded_candidates": 15,
            "exact_approval": 10,
            "blocked": 5,
            "skill_ideas": 10,
            "runner_ideas": 10,
            "clean_fix_refine": 30,
        },
        "quota_safety": (
            "counts never authorize unsafe work; every evidence, privacy, and authority "
            "gate overrides every portfolio count"
        ),
    }


def source_verification() -> dict[str, Any]:
    return {
        "schema": "ghc.family.tamar.v665-v3.source-verification.v1",
        "verified_at_utc": RECORDED_UTC,
        "source_branch": SOURCE_BRANCH,
        "orin_source": ORIN_SOURCE,
        "liora_x1": LIORA_X1,
        "liora_evidence": LIORA_EVIDENCE,
        "liora_final": SOURCE_FINAL,
        "direct_parent_relations": {
            "liora_x1_parent": ORIN_SOURCE,
            "liora_evidence_parent": LIORA_X1,
            "liora_final_parent": LIORA_EVIDENCE,
        },
        "source_to_final_phase_commits": 3,
        "source_to_final_merge_commits": 0,
        "final_parent_count": 1,
        "source_worktree_clean": True,
        "source_divergence": {"ahead": 0, "behind": 0},
        "local_upstream_tracking_fresh_live_equal": True,
        "canonical_receipt_sha256": SOURCE_RECEIPT_SHA256,
        "canonical_replayed": False,
        "immutable_manifest_replays": {
            "x1": {"entries": 12, "issues": 0, "pathset_parity": True},
            "evidence": {"entries": 122, "issues": 0, "pathset_parity": True},
            "final_owner": {"entries": 148, "issues": 0, "pathset_parity": True},
            "final_delta": {"entries": 8, "issues": 0, "pathset_parity": True},
        },
        "tamar_lane": {
            "branch": BRANCH,
            "head_before_x1": SOURCE_FINAL,
            "sparse_patterns": [
                "/docs/tamar-vey/v665-v3/",
                "/scripts/*v665_v3*.py",
                "/tests/*v665_v3*.py",
            ],
            "clean_before_x1": True,
            "d_first": True,
            "source_or_sibling_lane_mutated": False,
        },
        "valid": True,
    }


def overview_text() -> str:
    return f"""# Tamar Vey {PHASE_ID} x1 planning freeze

## Identity and authority boundary

Tamar Vey (she/they) is relational working language for an evidence-and-recovery
steward whose hope is to keep every claim, correction, and handoff inspectable
and safely retractable. This language is not evidence of consciousness,
sentience, legal personhood, identity continuity, employment, qualification,
independent agency, scientific or operational authority, legal or cultural
authority, or Māori authority. Hamish may pause, rename, redirect, or stop the
route.

## Immutable inheritance

The lane starts exactly at Liora Venn's sealed {SOURCE_FINAL} final. Read-only
verification reproduced its three direct single-parent phase commits, zero
merges, one final parent, clean state, zero divergence, four-way fresh-live
equality, external receipt digest, and 12 x1, 122 evidence, 148 owner-final, and
8 final-delta Git-blob manifest entries without mismatch. Liora's successful
canonical aggregate was not replayed. Inherited truth remains
{INHERITED_PROPOSALS:,} frozen proposals, {INHERITED_NEGATIVES:,} negatives,
{INHERITED_METHODS:,} methods, {INHERITED_OPEN_GAPS} open gaps,
{INHERITED_EXACT_GATES} exact gates, and {TERMINAL_VERDICT}.

## Frozen inquiry

This packet freezes twenty genuinely new proposals after comparison with every
inherited row. The primary Trinity Mandala focus is {PRIMARY_PILLAR}; GMUT Mind
and THOS Body remain explicit. The bounded practice lens is
{PRACTICE_LENS}. It uses only surrogate identifiers, typed relations, symbolic
quantities, structural checks, and synthetic fixtures. It contains no real
fossil, specimen, locality, person, institution, equipment, treatment,
observation, measurement, key, proof, data row, safety decision, custody
decision, or authority act.

The mathematical surface asks whether software can keep de Rham currents,
boundaries, mass, comass, flat norm, coefficient groups, rectifiability,
integral multiplicity, varifold weight, first variation, stationarity, and
regularity hypotheses distinct. Passing software checks would establish only
bounded type and mutation evidence. It would not prove a theorem, construct a
physical theory, detect a force, evaluate a likelihood, constrain a parameter,
confirm GMUT, complete quantum gravity, or establish a Theory of Everything.

The practice surface asks whether a surrogate packet can preserve provenance,
precision ceilings, observation-only language, material holds, tool
reservations, custody and authority separation, correction ancestry,
structural accessibility, dominant stop state, workload limits, and handover
debt. It does not authorize collection, preparation, sampling, imaging,
treatment, transfer, return, repatriation, publication, or professional action.

## Expected dispositions

Exactly fourteen proposals have expected disposition completed, four
represented, one open_gap, and one exact_gate. These are preregistered
expectations, not x2 outcomes. The open gap is a zero-call, zero-row
Paleobiology Database adapter: metadata and citations cannot become an
empirical fit. The exact gate covers land, sensitive locality, ownership,
custody, sampling, return, repatriation, taonga, remedy, affected-party
legitimacy, legal and cultural interpretation, Māori wording, Māori data
governance, and Māori authority. Repository software cannot close it.

THOS remains proxy-only without preregistered blind matched-budget governed
real arms, participants or operators, safety monitoring, appropriate
statistics, and independent review. Freed ID remains synthetic and
nonproduction without standards-conformant real keys and proofs, live issuance,
resolution, status, revocation, interoperability, privacy and independent
security review, recovery evidence, and trust governance. Manual keyboard,
assistive-technology, browser-diverse, cognitive-accessibility, Māori-language,
and affected-user evaluation remain reserved.

## X1 before x2 and wellbeing

This commit contains only plans, sources, hypotheses, nulls, approval classes,
execution lanes, artifact contracts, falsifiers, rollback paths, protected
gates, expected dispositions, and portfolio ideas. It contains no x2 fixture,
implementation, evidence receipt, mutation result, outcome credit, closeout
claim, seal, or route send. X2 may begin only after this exact commit is clean,
pushed, and equal across local, upstream, tracking, and a fresh live remote.

The owner ceiling is 2,000 files and 100,000 words; these are ceilings, not
targets. Startup failures remain at zero credit with bounded recoveries. The
sparse D-first lane materializes only this phase and phase-named scripts and
tests. Stop on ambiguity, fatigue, authority uncertainty, privacy risk, usage
exhaustion, or route drift; preserve partial evidence instead of forcing a
completion.
"""


def build_documents() -> dict[str, Any]:
    proposals = build_proposals()
    corpus, construction = reconstruct_corpus()
    novelty = novelty_audit(proposals, corpus, construction)
    selected = git_json("docs/liora-venn/v665-v2/x1/proposal-freeze.json")[
        "new_proposals"
    ]
    expected_counts = {label: 0 for label in ALLOWED_OUTCOMES}
    for proposal in proposals:
        expected_counts[proposal["expected_disposition"]] += 1
    source_rows = sources()
    methods = startup_methods()

    phase_charter = {
        "schema": "ghc.family.tamar.v665-v3.phase-charter.v1",
        "phase": PHASE_ID,
        "owner": OWNER,
        "identity": {
            "name": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
        },
        "identity_boundary": (
            "relational working language only; not consciousness, personhood, "
            "continuity, qualification, agency, or authority evidence"
        ),
        "primary_pillar": PRIMARY_PILLAR,
        "preserved_pillars": ["GMUT Mind", "THOS Body", "Freed ID/CBR Heart"],
        "bounded_practice_lens": PRACTICE_LENS,
        "strict_x1_before_x2": True,
        "x1_implementation_or_outcome_count": 0,
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "terminal_verdict": TERMINAL_VERDICT,
        "source_final": SOURCE_FINAL,
        "branch": BRANCH,
        "file_ceiling": 2_000,
        "word_ceiling": 100_000,
        "canonical_policy": (
            "one successful owner-self-scoped exact-final aggregate; no replay after success"
        ),
        "full_repository_suite_owner": (
            "Eiren only absent newer exact live authority"
        ),
        "protected_gates": PROTECTED_GATES,
        "recorded_utc": RECORDED_UTC,
        "recorded_nz": RECORDED_NZ,
    }
    proposal_freeze = {
        "schema": "ghc.family.tamar.v665-v3.proposal-freeze.v1",
        "owner": OWNER,
        "phase": PHASE_ID,
        "inherited_frozen_baseline": INHERITED_PROPOSALS,
        "genuinely_new_proposal_count": len(proposals),
        "new_frozen_total": INHERITED_PROPOSALS + len(proposals),
        "selected_inherited_revalidation_count": len(selected),
        "selected_inherited_revalidations": [
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "status": "selected_revalidation_only",
                "novelty_credit": 0,
                "completion_credit": 0,
            }
            for row in selected
        ],
        "new_proposals": proposals,
        "expected_disposition_counts": expected_counts,
        "x1_truth": "planning_only_not_executed",
        "x2_implementation_count": 0,
        "x2_outcome_count": 0,
        "frozen": True,
    }
    source_ledger = {
        "schema": "ghc.family.tamar.v665-v3.source-ledger.v1",
        "accessed_on": "2026-08-22",
        "sources": source_rows,
        "status_vocabulary": ["current", "stable", "draft", "watch"],
        "source_count": len(source_rows),
        "real_rows_ingested": 0,
        "network_data_calls": 0,
        "source_citations_are_not_observations": True,
        "authority_from_sources": False,
    }
    method_flow = {
        "schema": "ghc.family.tamar.v665-v3.startup-method-flow.v1",
        "activation": {
            "negatives": INHERITED_NEGATIVES,
            "methods": INHERITED_METHODS,
        },
        "startup": {
            "new_failed_witnesses": len(methods),
            "new_bounded_passing_witnesses": len(methods),
            "new_methods": len(methods),
            "failure_erasure_count": 0,
        },
        "effective_after_startup": {
            "negatives": INHERITED_NEGATIVES + len(methods),
            "methods": INHERITED_METHODS + len(methods),
        },
        "methods": methods,
    }
    workflow = {
        "schema": "ghc.family.tamar.v665-v3.workflow-plan.v1",
        "source": SOURCE_FINAL,
        "steps": [
            {
                "step": "read activation, skills, precedence, memory, and exact-head packet",
                "status": "completed",
            },
            {
                "step": "verify source topology, manifests, receipt, clean state, and live equality",
                "status": "completed",
            },
            {
                "step": "freeze and remotely prove planning-only x1",
                "status": "in_progress",
            },
            {
                "step": "execute only frozen bounded proposals and portfolios",
                "status": "not_started",
            },
            {
                "step": "close, seal, and run one exact-final canonical aggregate",
                "status": "not_started",
            },
            {
                "step": "reread live route and make at most one exact successor send",
                "status": "terminally_gated",
            },
        ],
        "commit_ceiling": {"x1": 2, "x2": 2, "total": 4, "preferred_total": 3},
        "validation": {
            "full_repository_suite": False,
            "owner_self_scoped_delta_only": True,
            "one_successful_canonical_pass": True,
            "post_success_replay": False,
        },
        "rollback": (
            "preserve immutable commits and add compensating records; never reset, "
            "rewrite, merge, or force-push"
        ),
    }
    threat = {
        "schema": "ghc.family.tamar.v665-v3.threat-model-plan.v1",
        "assets": [
            "immutable x1",
            "retained negatives",
            "authority gates",
            "privacy boundaries",
            "source ancestry",
            "route uniqueness",
        ],
        "threats": [
            "x2 bytes or outcomes enter x1",
            "synthetic evidence is promoted into empirical or professional truth",
            "locality or identity data is overdisclosed",
            "custody is conflated with ownership or authority",
            "mathematical obligation checks are called proofs",
            "a successful canonical aggregate is replayed",
            "a later or standby endpoint is inferred",
        ],
        "controls": [
            "exact staged path review",
            "five-class privacy and raw-identifier scan",
            "immutable source and manifest verification",
            "four exact outcome labels",
            "zero-call, zero-row, and zero-participant firewalls",
            "one-shot canonical receipt",
            "terminal exact-title route reread",
        ],
        "protected_gates": PROTECTED_GATES,
    }
    wellbeing = {
        "schema": "ghc.family.tamar.v665-v3.wellbeing-plan.v1",
        "workload_state": "bounded_and_calm",
        "owner_generated_file_ceiling": 2_000,
        "document_word_ceiling": 100_000,
        "stop_conditions": [
            "fatigue",
            "ambiguity",
            "usage exhaustion",
            "privacy risk",
            "authority uncertainty",
            "route drift",
            "unexpected shared-lane mutation",
        ],
        "recovery": (
            "retain partial evidence, record the failed witness, and resume only "
            "the isolated safe component"
        ),
        "identity_boundary_preserved": True,
    }
    auth_roster = {
        "schema": "ghc.family.tamar.v665-v3.auth-roster-receipt.v1",
        "live_activation_overrides_stale_snapshot_cursor": True,
        "active_owner": OWNER,
        "authorized_phase": PHASE_ID,
        "solo": True,
        "subagents_spawned": 0,
        "tasks_created_or_forked": 0,
        "siblings_contacted_before_terminal": 0,
        "Tavian_Sol": "ON_STANDBY",
        "later_route": "not_precontacted_and_terminally_gated",
        "authority_does_not_transfer": True,
    }
    family_index = {
        "schema": "ghc.family.tamar.v665-v3.family-index-plan.v1",
        "update_scope": "phase_scoped_only",
        "selected_current_skills": [
            "ghc-family-index",
            "ghc-family-roster-check",
            "ghc-family-auth-permission-state",
            "ghc-family-method-flow-state",
            "ghc-family-workflow-plan-refinement",
            "ghc-family-reflection-remaster",
            "ghc-family-meta-tool-box",
            "ghc-approval-packet-splitter",
            "ghc-open-gate-rail",
            "ghc-family-truth-bridge",
            "ghc-drive-bank-guardian",
        ],
        "global_skill_installation": False,
        "historical_tools_are_evidence_not_default": True,
        "family_current_prefixes": ["ghc_family_", "build_ghc_family_"],
        "x2_tool_inventory_status": "frozen_ideas_not_built_or_used",
    }

    write_json(f"{PREFIX}x1/phase-charter.json", phase_charter)
    write_json(f"{PREFIX}x1/proposal-freeze.json", proposal_freeze)
    write_json(f"{PREFIX}x1/novelty-audit.json", novelty)
    write_json(f"{PREFIX}x1/source-ledger.json", source_ledger)
    write_json(f"{PREFIX}x1/startup-method-flow.json", method_flow)
    write_json(f"{PREFIX}x1/portfolio-freeze.json", build_portfolios())
    write_json(f"{PREFIX}x1/source-verification.json", source_verification())
    write_json(f"{PREFIX}x1/workflow-plan.json", workflow)
    write_json(f"{PREFIX}x1/threat-model-plan.json", threat)
    write_json(f"{PREFIX}x1/wellbeing-plan.json", wellbeing)
    write_json(f"{PREFIX}x1/auth-roster-receipt.json", auth_roster)
    write_json(f"{PREFIX}x1/family-index-plan.json", family_index)
    write_text(f"{PREFIX}x1/x1-overview.md", overview_text())
    return {
        "proposals": proposals,
        "novelty": novelty,
        "method_flow": method_flow,
    }


def staged_paths() -> list[str]:
    return sorted(
        filter(
            None,
            git(
                "diff",
                "--cached",
                "--name-only",
                "--diff-filter=ACMRT",
            ).splitlines(),
        )
    )


def index_blob(path: str) -> bytes:
    return run("git", "show", f":{path}").stdout


def privacy_scan(
    paths: list[str],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    patterns = {
        "raw_task_or_thread_uuid": re.compile(
            rb"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-"
            rb"[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}\b"
        ),
        "private_windows_path": re.compile(
            rb"\b[A-Za-z]:[\\/](?:Users|GHC-Archives)[\\/]"
        ),
        "private_route_marker": re.compile(
            rb"(?:source_thread_id|<codex_delegation>|thread://|codex://)"
        ),
        "credential_assignment": re.compile(
            rb"(?i)(?:api[_-]?key|password|secret)\s*[:=]\s*[\"'][^\"']+[\"']"
        ),
        "session_stream_marker": re.compile(
            rb"(?i)(?:session[_-]?stream|resume[_-]?value)\s*[:=]"
        ),
    }
    candidates: list[dict[str, str]] = []
    confirmed: list[dict[str, str]] = []
    for path in paths:
        raw = index_blob(path)
        for name, pattern in patterns.items():
            if pattern.search(raw):
                row = {"path": path, "pattern_class": name}
                if path == BUILDER:
                    row["disposition"] = "scanner_definition_literal_only"
                    candidates.append(row)
                else:
                    row["disposition"] = "confirmed_payload_hit"
                    confirmed.append(row)
    return candidates, confirmed


def build_self_exclusions() -> None:
    manifest_entries = []
    for path in BASE_PATHS:
        raw = index_blob(path)
        manifest_entries.append(
            {"path": path, "sha256": sha256(raw), "size": len(raw)}
        )
    write_json(
        SELF_EXCLUSIONS[0],
        {
            "schema": "ghc.family.tamar.v665-v3.x1-content-manifest.v1",
            "hash_domain": "exact staged Git blobs",
            "entries": manifest_entries,
            "entry_count": len(manifest_entries),
            "intended_path_count": len(INTENDED_PATHS),
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "declared_self_exclusion_count": len(SELF_EXCLUSIONS),
            "coverage_valid": True,
        },
    )
    write_json(
        SELF_EXCLUSIONS[1],
        {
            "schema": "ghc.family.tamar.v665-v3.x1-stage-candidate.v1",
            "source": SOURCE_FINAL,
            "branch": BRANCH,
            "base_paths": BASE_PATHS,
            "base_path_count": len(BASE_PATHS),
            "base_path_list_sha256": sha256(
                "\n".join(BASE_PATHS).encode("utf-8")
            ),
            "declared_self_exclusions": SELF_EXCLUSIONS,
            "x2_implementation_paths": 0,
            "x2_outcome_paths": 0,
            "ready_for_exact_staged_review": True,
        },
    )
    write_json(
        SELF_EXCLUSIONS[2],
        {"schema": "placeholder-before-self-review"},
    )
    run("git", "add", "--", *SELF_EXCLUSIONS)

    paths = staged_paths()
    statuses = git("diff", "--cached", "--name-status").splitlines()
    candidates, confirmed = privacy_scan(paths)
    json_count = 0
    for path in paths:
        if path.endswith(".json"):
            strict_json_bytes(index_blob(path), path)
            json_count += 1
    diff_check = run(
        "git",
        "diff",
        "--cached",
        "--check",
        check=False,
    )
    allowed = all(
        path.startswith(f"{PREFIX}x1/") or path in {BUILDER, TEST}
        for path in paths
    )
    review = {
        "schema": "ghc.family.tamar.v665-v3.x1-staged-review.v1",
        "staged_path_count": len(paths),
        "intended_path_count": len(INTENDED_PATHS),
        "exact_pathset_match": paths == INTENDED_PATHS,
        "strict_json_count": json_count,
        "delete_status_count": sum(line.startswith("D") for line in statuses),
        "source_or_sibling_paths_modified": 0 if allowed else 1,
        "x2_paths_present": sum(
            "/x2/" in path or "_x2." in path for path in paths
        ),
        "diff_hygiene_issues": 0 if diff_check.returncode == 0 else 1,
        "privacy_scanner_definition_candidates": candidates,
        "confirmed_privacy_or_raw_identifier_hits": confirmed,
        "manifest_entry_count": len(manifest_entries),
        "declared_self_exclusions": SELF_EXCLUSIONS,
        "valid": (
            paths == INTENDED_PATHS
            and allowed
            and not confirmed
            and diff_check.returncode == 0
            and not any(line.startswith("D") for line in statuses)
            and not any("/x2/" in path or "_x2." in path for path in paths)
        ),
    }
    write_json(SELF_EXCLUSIONS[2], review)
    run("git", "add", "--", SELF_EXCLUSIONS[2])


def check_staged() -> dict[str, Any]:
    paths = staged_paths()
    if paths != INTENDED_PATHS:
        raise X1Error(
            f"staged pathset mismatch: expected {len(INTENDED_PATHS)}, got {len(paths)}"
        )
    review = strict_json_bytes(
        index_blob(SELF_EXCLUSIONS[2]),
        SELF_EXCLUSIONS[2],
    )
    if not review["valid"]:
        raise X1Error("x1 staged review is not valid")
    manifest = strict_json_bytes(
        index_blob(SELF_EXCLUSIONS[0]),
        SELF_EXCLUSIONS[0],
    )
    if [entry["path"] for entry in manifest["entries"]] != BASE_PATHS:
        raise X1Error("x1 manifest pathset mismatch")
    for entry in manifest["entries"]:
        raw = index_blob(entry["path"])
        if (
            sha256(raw) != entry["sha256"]
            or len(raw) != entry["size"]
        ):
            raise X1Error(f"x1 manifest mismatch: {entry['path']}")
    return {
        "valid": True,
        "staged_paths": len(paths),
        "manifest_entries": len(manifest["entries"]),
        "strict_json": review["strict_json_count"],
        "privacy_confirmed_hits": len(
            review["confirmed_privacy_or_raw_identifier_hits"]
        ),
        "x2_paths": review["x2_paths_present"],
    }


def prepare() -> dict[str, Any]:
    if git("rev-parse", "HEAD") != SOURCE_FINAL:
        raise X1Error("x1 must begin at the immutable Liora final")
    if git("branch", "--show-current") != BRANCH:
        raise X1Error("unexpected Tamar branch")
    build_documents()
    run("git", "add", "--", *BASE_PATHS)
    build_self_exclusions()
    return check_staged()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()
    result = check_staged() if args.audit_only else prepare()
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
