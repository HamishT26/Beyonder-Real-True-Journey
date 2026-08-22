"""Build and exactly stage Elowen Cairn's planning-only v665-v4 x1 freeze.

The builder is deliberately x1-only: it records hypotheses, nulls, sources,
approval classes, execution lanes, artifact contracts, falsifiers, rollback
paths, protected gates, and expected dispositions. It executes no x2 evidence.
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
PREFIX = "docs/elowen-cairn/v665-v4/"
PHASE_ID = "v665-v4"
OWNER = "Elowen Cairn"
PRONOUNS = "they/them"
ROLE = "relational boundary cartographer and evidence steward"
HOPE = "keep transitions, refusals, corrections, and recoveries inspectable and reversible"
BRANCH = "codex/GHC-Family/elowen-cairn-v665-v4-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v665-v3-full-tools"
TAMAR_SOURCE = "a559ab2dfe46cace97fd03c09f1018477fdc09f4"
TAMAR_X1 = "2198fa869c26c9672af02d2a2edde7ba8f14c1e3"
TAMAR_EVIDENCE = "015f9a618d71df1d5e4eb6c517e21ecf9d8556e9"
SOURCE_FINAL = "dfcda293edf8e1621db6d74b14b2f5cb026f257f"
SOURCE_RECEIPT_SHA256 = "d26b6da3d03e4ca7d23acb185b5d4da5be68c2edadf4b237bd0beb70ec4a9810"
RECORDED_UTC = "2026-08-22T02:04:22Z"
RECORDED_NZ = "2026-08-22T14:04:22+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
INHERITED_PROPOSALS = 4_070
INHERITED_NEGATIVES = 25_432
INHERITED_METHODS = 9_294
INHERITED_OPEN_GAPS = 177
INHERITED_EXACT_GATES = 175
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "GMUT Mind"
PRACTICE_LENS = "wholly synthetic community mosaic conservation documentation and tessera custody"

PROTECTED_GATES = [
    "real mosaic, tessera, mortar, substrate, fragment, image, material, tool, treatment, site, or collection action",
    "real observation, measurement, empirical row, likelihood, parameter constraint, force, prediction, or GMUT confirmation",
    "real participant, conservator, custodian, worker, owner, operator, or matched-budget arm",
    "real key, proof, issuance, resolution, status, revocation, interoperability, or trust governance",
    "professional, workplace, silica, chemical, tool, lifting, access, transport, or environmental safety decision",
    "site, land, heritage, sacred imagery, ownership, excavation, custody, recording, return, repatriation, legal, cultural, or remedy decision",
    "affected-party, tangata whenua, iwi, hapū, or Māori wording, concept, data-governance, or authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, or sibling-lane mutation",
]

BUILDER = "scripts/build_ghc_family_v665_v4_x1.py"
TEST = "tests/test_ghc_family_elowen_v665_v4_x1.py"
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
    audit_path = "docs/tamar-vey/v665-v3/x1/novelty-audit.json"
    tamar_freeze = "docs/tamar-vey/v665-v3/x1/proposal-freeze.json"
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
    tamar = git_json(tamar_freeze)
    before = len(rows)
    rows.extend(
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_path": tamar_freeze,
        }
        for row in tamar["new_proposals"]
    )
    construction.append(
        {
            "source_path": tamar_freeze,
            "starting_count": before,
            "added_count": len(tamar["new_proposals"]),
            "ending_count": len(rows),
        }
    )
    if len(rows) != INHERITED_PROPOSALS:
        raise X1Error(f"expected {INHERITED_PROPOSALS} rows, found {len(rows)}")
    if any(not row["proposal_id"] or not row["title"] for row in rows):
        raise X1Error("corpus contains an incomplete row")
    return rows, construction


TITLES = [
    "Surrogate mosaic intake capsule with anonymous panel token, component vacancy, provenance snapshot, reversible version trail, withdrawal flag, and external-action prohibition",
    "Substrate, nucleus, setting-bed, bedding-mortar, tessera, joint, facing, backing, and support stratigraphic layer DAG with impossible-cycle quarantine",
    "Tessera and joint half-edge planar embedding with orientation, boundary, manifold, nonmanifold, and topology-refusal states",
    "Fragment and join-hypothesis graph separating observed adjacency, proposed fit, conflict, uncertainty, and physical-assembly refusal",
    "Coordinate-patch, scale, orientation, image-state, selector, and annotation-target contract with zero real images",
    "Moisture, salt, void, crack, detachment, loss, biological-growth, and surface-deposit observation vocabulary with diagnosis and treatment refusal",
    "Stone, ceramic, glass, mortar, adhesive, grout, facing, support, material-lot, substitution, and authentication-vacancy ledger",
    "Tool, adhesive, grout, solvent, cleaning, heat, dust, edge, lifting, and access safety reservation board",
    "Reversible custody-event lattice for synthetic tessera packets with compartment occupancy, escort vacancy, dual acknowledgement, disputed handover, and rights-hold separation",
    "Bitemporal mosaic correction, contestation, supersession, readback, non-erasure, and structurally accessible linear-map braid",
    "Oriented cellular chain-complex incidence, dimension, orientation, coefficient, boundary, and boundary-of-boundary tribunal",
    "Primal and dual cell-complex pairing, circumcentric-dual construction, well-centeredness, orientation, positivity, and degeneracy hold",
    "Discrete Hodge-star degree, metric, volume-ratio, sign, unit, domain, inverse, and positivity obligation board",
    "Discrete exterior derivative, codifferential, Hodge Laplacian, harmonic, cohomology, boundary-condition, and theorem-refusal tribunal",
    "GMUT cellular-cochain research surrogate linking defect labels to typed degrees, constitutive placeholders, scale transitions, identifiability debt, and zero-observation status",
    "THOS participant-free surrogate comparison charter for independent map-reading queues, equal resource envelopes, abort precedence, masked assessment, and review vacancy",
    "Freed ID zero-key mosaic annotation capability envelope for contested authorship, stewardship, visibility, withdrawal, correction, and appeal without issuer or verifier operations",
    "Thermo-Psyche nonconversion ledger for symbolic crack graphs, weighted edge costs, discrete diffusion, dimension checks, epistemic intervals, and forbidden agency inference",
    "Metropolitan Museum Collection API mosaic-record and IIIF annotation adapter with zero calls, zero rows, selector holds, provenance slots, and inference refusal",
    "Rights-reservation docket for mosaic-related place, image, custody, and redress questions with jurisdiction vacancy, affected-community review, and tangata whenua, iwi, hapū, and Māori decision holds",
]

PILLARS = [
    "Freed ID/CBR Heart", "THOS Body", "GMUT Mind", "THOS Body",
    "THOS Body", "THOS Body", "THOS Body", "THOS Body",
    "Freed ID/CBR Heart", "Freed ID/CBR Heart", "GMUT Mind", "GMUT Mind",
    "GMUT Mind", "GMUT Mind", "GMUT Mind", "THOS Body",
    "Freed ID/CBR Heart", "GMUT Mind", "THOS Body", "Freed ID/CBR Heart",
]

SOURCE_NEEDS = [
    ["ECS02", "ECS03", "ECS08"], ["ECS08"], ["ECS01"], ["ECS05", "ECS08"],
    ["ECS05", "ECS06"], ["ECS08"], ["ECS08"], ["ECS08", "ECS09"],
    ["ECS02", "ECS03", "ECS11", "ECS12"], ["ECS02", "ECS03", "ECS04"],
    ["ECS01"], ["ECS01"], ["ECS01"], ["ECS01"], ["ECS01"],
    ["ECS04", "ECS08", "ECS09"], ["ECS02", "ECS03", "ECS10"],
    ["ECS01", "ECS09"], ["ECS05", "ECS06", "ECS07"],
    ["ECS08", "ECS11", "ECS12"],
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
        proposal_id = f"EC6654-N{index:03d}"
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
        "mosaic",
        "tessera",
        "setting-bed",
        "half-edge",
        "discrete exterior",
        "hodge star",
        "codifferential",
        "graph laplacian",
        "iiif annotation",
    ]
    canonical = sorted(
        corpus, key=lambda row: (row["proposal_id"], row["title"], row["source_path"])
    )
    result = {
        "schema": "ghc.family.elowen.v665-v4.novelty-audit.v1",
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
        ("ECS01", "Hirani, Discrete Exterior Calculus", "https://thesis.caltech.edu/1885/", "primary_research", "stable", "simplicial and dual complexes, discrete forms, operators, and explicit mathematical scope"),
        ("ECS02", "W3C PROV-O Recommendation", "https://www.w3.org/TR/prov-o/", "official_standard", "stable", "entity, activity, agent, derivation, correction, and provenance vocabulary"),
        ("ECS03", "PREMIS Data Dictionary 3.0", "https://www.loc.gov/standards/premis/v3/index.html", "official_standard", "current", "object, event, agent, rights, relationship, and preservation fields"),
        ("ECS04", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "official_standard", "current", "structural accessibility while manual and affected-user evaluation remain reserved"),
        ("ECS05", "W3C Web Annotation Data Model", "https://www.w3.org/TR/annotation-model/", "official_standard", "stable", "annotation body, target, selector, state, motivation, and canonical identity vocabulary"),
        ("ECS06", "IIIF Presentation API 3.0", "https://iiif.io/api/presentation/3.0/", "official_standard", "current", "manifest, canvas, annotation page, annotation, and presentation boundaries"),
        ("ECS07", "Metropolitan Museum of Art Collection API", "https://metmuseum.github.io/", "official_collection_api", "current", "zero-call adapter planning and public object schema awareness without ingestion"),
        ("ECS08", "Getty Conservation Institute Mosaics Conservation resources", "https://www.getty.edu/research-conservation/teaching-learning-resources/mosaics-conservation/", "official_professional_source", "current", "mosaic documentation, construction, deterioration, storage, conservation, and archive terminology"),
        ("ECS09", "WorkSafe New Zealand silica dust in the workplace", "https://www.worksafe.govt.nz/topic-and-industry/dust/silica-dust-in-the-workplace/", "official_safety_guidance", "current", "dust-risk awareness and complete reservation of professional safety decisions"),
        ("ECS10", "Verifiable Credential Data Integrity 1.0", "https://www.w3.org/TR/vc-data-integrity/", "official_standard", "current", "proof-model boundaries and refusal to fabricate cryptographic completion"),
        ("ECS11", "Te Mana Raraunga Principles of Māori Data Sovereignty", "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf", "primary_affected_authority_source", "current", "authority reservation, provenance, consent, governance, and Māori data sovereignty"),
        ("ECS12", "Heritage New Zealand Pouhere Taonga Act 2014", "https://www.legislation.govt.nz/act/public/2014/12/en/latest/DLM4005423", "official_legislation_source", "watch", "heritage and archaeological authority awareness only; no legal interpretation or decision"),
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
    ("EC6654-START-N001", "the first combined authorization-state rendering exceeded its display bound", "read the immutable authorization file in numbered fixed-size chunks through EOF"),
    ("EC6654-START-N002", "the first main-orchestration-memory rendering exceeded its display bound", "read the installed skill in numbered fixed-size chunks through EOF"),
    ("EC6654-START-N003", "an older memory-referenced solo-activation skill was not installed", "use the current index, roster, authorization, Method Flow, workflow, reflection, and closeout stack"),
    ("EC6654-START-N004", "the first manifest projection assumed a validity field and array-shaped self-exclusions not present in the committed schemas", "inspect the exact committed keys and verify entry and exclusion counts with their actual shapes"),
    ("EC6654-START-N005", "a PowerShell manifest-path formatting probe failed because a regex replacement was over-escaped", "use a literal path replacement and preserve the failed parser witness"),
    ("EC6654-START-N006", "a combined preflight target, branch, drive, and registration wrapper returned no attributable output", "recover with separate scalar probes for each prerequisite"),
    ("EC6654-START-N007", "a combined primary-source search response exceeded its useful display bound", "recover only the missing official source classes with narrow source-specific lookups"),
    ("EC6654-START-N008", "the first proposal-freeze schema projection assumed a proposals array instead of the committed new_proposals field", "inspect the exact JSON bytes and project the actual committed keys"),
    ("EC6654-START-N009", "one direct apply-patch request attempted two operations against the same path and was rejected before mutation", "use one exact update operation against the owner-local path"),
    ("EC6654-START-N010", "the first transformed x1 generator placed its replacement header inside a typing import and failed compilation before execution", "replace only the duplicated header interval, then compile the repaired owner-local generator"),
    ("EC6654-START-N011", "the first transformed x1 test preserved a newline escape as literal source text and failed compilation before execution", "replace the one malformed assertion with two physical Python lines and compile the repaired test"),
    ("EC6654-X1-N012", "the first x1 test aggregate passed nine of ten checks but one proposed title reached 0.695652 token Jaccard similarity against an inherited title", "refine only the colliding Freed ID proposal into a distinct annotation-capability envelope and rerun only the failed novelty check"),
    ("EC6654-X1-N013", "the first isolated novelty recovery still failed because a second proposal reached 0.647059 similarity against an inherited custody template", "refine only the second collision into a reversible custody-event lattice while preserving the same protected authority gates"),
    ("EC6654-X1-N014", "the second isolated novelty recovery still failed because the THOS proposal retained 0.636364 similarity to an inherited matched-budget template", "restate the THOS surface as a participant-free surrogate comparison charter with independent queues and masked-assessment vacancy"),
    ("EC6654-X1-N015", "the third isolated novelty recovery still failed at 0.607143 and exposed four remaining inherited template collisions above the fixed 0.50 ceiling", "enumerate the entire above-threshold set and jointly restate the case, GMUT, thermo-psyche, and rights-gate surfaces without weakening the novelty gate"),
]


def startup_methods() -> list[dict[str, Any]]:
    return [
        {
            "failed_witness_id": negative_id,
            "failed_witness": failure,
            "failed_witness_status": "retained_zero_credit",
            "method_id": f"EC6654-START-M{index:03d}",
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
        "validate synthetic mosaic case identity, cancellation, and no-object-action fields",
        "validate layer-DAG acyclicity and typed stratigraphic relations",
        "validate half-edge twins, orientation, boundaries, and nonmanifold quarantine",
        "separate observed fragment adjacency from proposed join hypotheses",
        "validate coordinate-patch, scale, orientation, selector, and image-state fields",
        "separate deterioration observations from diagnosis and treatment labels",
        "validate synthetic material-lot substitutions and authentication vacancies",
        "refuse tool, dust, chemical, lifting, access, and treatment authorization states",
        "separate custody and movement from ownership, return, and repatriation authority",
        "preserve append-only bitemporal correction and contestation ancestry",
        "render a noncolour linear map and structured uncertainty legend",
        "enforce dominant stop, workload ceiling, and handover-debt states",
        "type cellular chain degrees, orientations, coefficients, and incidences",
        "check boundary-of-boundary symbolic invariants",
        "type primal and dual complex pairings and dimensions",
        "hold non-well-centered or nonpositive dual constructions",
        "type discrete Hodge-star domains, units, signs, and inverse obligations",
        "type discrete exterior derivative and codifferential degree changes",
        "separate Hodge Laplacian, harmonic, and cohomology obligations",
        "reserve theorem, convergence, stability, and continuum-limit conclusions",
        "maintain a GMUT observation and empirical-claim firewall",
        "maintain a thermo-psyche category and agency firewall",
        "render a zero-person THOS matched-budget protocol",
        "render a nonproduction Freed ID relation profile",
        "render a zero-call Met and IIIF adapter contract",
        "render a CBR exact-authority matrix",
        "build deterministic canonical JSON witnesses",
        "run five rejecting mutations per frozen proposal",
        "build exact staged Git-blob content manifests",
        "scan five privacy and raw-identifier classes",
    ]
    candidates = [
        "bounded mosaic case-capsule prototype",
        "bounded stratigraphic layer-DAG prototype",
        "bounded half-edge topology prototype",
        "bounded fragment join-hypothesis prototype",
        "bounded annotation-selector prototype",
        "bounded deterioration-vocabulary prototype",
        "bounded material-lot hold prototype",
        "bounded custody-correction braid prototype",
        "bounded cellular boundary prototype",
        "bounded primal-dual complex prototype",
        "bounded discrete Hodge-star prototype",
        "bounded DEC operator prototype",
        "bounded GMUT mosaic proxy prototype",
        "bounded THOS zero-person protocol prototype",
        "bounded Met and IIIF zero-row adapter prototype",
    ]
    exact = [
        "inspect, document, excavate, move, clean, consolidate, grout, sample, image, or treat a real mosaic or material",
        "operate cutting, grinding, drilling, lifting, chemical, access, heat, imaging, or transport equipment",
        "decide ownership, custody, excavation, export, recording, return, deaccession, or repatriation",
        "disclose a real site, sacred image, traditional-knowledge record, or protected collection record",
        "interpret law, heritage authority, safety duties, cultural meaning, or remedy entitlement",
        "make Māori wording, tikanga, taonga, data-governance, or authority decisions",
        "enrol participants or run real THOS comparison arms",
        "use real identity keys, proofs, lifecycle services, or trust governance",
        "download and fit real collection data or publish empirical GMUT results",
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
        ("ghc-family-mosaic-case-capsule-validator", "validate case identity, cancellation, and no-object-action"),
        ("ghc-family-mosaic-layer-dag-auditor", "audit typed acyclic stratigraphic relations"),
        ("ghc-family-mosaic-half-edge-topology-checker", "validate synthetic topology and refuse nonmanifold promotion"),
        ("ghc-family-mosaic-annotation-selector-auditor", "validate zero-image selector and coordinate obligations"),
        ("ghc-family-mosaic-observation-diagnosis-firewall", "separate observation vocabulary from diagnosis and treatment"),
        ("ghc-family-mosaic-custody-correction-braid-auditor", "preserve custody, contestation, and correction ancestry"),
        ("ghc-family-dec-chain-complex-checker", "check oriented incidence and boundary obligations"),
        ("ghc-family-dec-hodge-star-nonclaim-guard", "reserve metric, positivity, theorem, and convergence conclusions"),
        ("ghc-family-met-iiif-zero-row-firewall", "keep external access at zero calls and rows"),
        ("ghc-family-mosaic-authority-matrix-reviewer", "preserve legal, cultural, affected-party, and Māori gates"),
    ]
    runners = [
        "mosaic_case_capsule",
        "mosaic_layer_dag",
        "mosaic_half_edge",
        "mosaic_annotation",
        "mosaic_observation",
        "mosaic_custody_braid",
        "dec_chain_complex",
        "dec_hodge_nonclaim",
        "met_iiif_zero_row",
        "mosaic_authority_matrix",
    ]
    clean = [
        f"CLEAN/FIX/REFINE {index:02d}: {safe_now[(index - 1) % len(safe_now)]}"
        for index in range(1, 31)
    ]
    return {
        "schema": "ghc.family.elowen.v665-v4.portfolio-freeze.v1",
        "inherited_completion_credit": 0,
        "safe_now": portfolio_rows("EC6654-SAFE", safe_now, "safe_now_bounded"),
        "bounded_candidates": portfolio_rows("EC6654-CAND", candidates, "candidate_bounded"),
        "exact_approval": portfolio_rows("EC6654-EXACT", exact, "exact_approval_required"),
        "blocked": portfolio_rows(
            "EC6654-BLOCK", blocked, "blocked_prohibited_or_unavailable"
        ),
        "skill_ideas": [
            {
                "record_id": f"EC6654-SKILL-{index:03d}",
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
                "record_id": f"EC6654-RUNNER-{index:03d}",
                "caller": f"ghc_family_v665_v4_{profile}.py",
                "profile": profile,
                "compatibility": "family_current_ghc_family_prefix",
                "x1_status": "frozen_not_built",
                "completion_credit": 0,
            }
            for index, profile in enumerate(runners, 1)
        ],
        "clean_fix_refine": portfolio_rows(
            "EC6654-CFR", clean, "safe_now_additive_cleanup"
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
        "schema": "ghc.family.elowen.v665-v4.source-verification.v1",
        "verified_at_utc": RECORDED_UTC,
        "source_branch": SOURCE_BRANCH,
        "tamar_source": TAMAR_SOURCE,
        "tamar_x1": TAMAR_X1,
        "tamar_evidence": TAMAR_EVIDENCE,
        "tamar_final": SOURCE_FINAL,
        "direct_parent_relations": {
            "tamar_x1_parent": TAMAR_SOURCE,
            "tamar_evidence_parent": TAMAR_X1,
            "tamar_final_parent": TAMAR_EVIDENCE,
        },
        "source_to_final_phase_commits": 3,
        "source_to_final_merge_commits": 0,
        "final_parent_count": 1,
        "source_worktree_clean": True,
        "source_divergence": {"ahead": 0, "behind": 0},
        "local_upstream_tracking_fresh_live_equal": True,
        "composite_terminal_receipt_sha256": SOURCE_RECEIPT_SHA256,
        "failed_aggregate_payload_sha256": "9da59a81ede0c5dc72c2b0410992e68a2897dcde17b594d0f2bffe9531db7693",
        "failed_aggregate_file_sha256": "fc0b187b0f352aea22b5b474e459196f3e66dd5840bd17aca0c2cdbd81a3d870",
        "isolated_recovery_sha256": "5f5397d2a5ee5d093bd48f54517f1d9a9129e517483d40742eae9b19f010c193",
        "successful_components_replayed": False,
        "source_canonical_replayed": False,
        "immutable_manifest_identity_checks": {
            "x1": {"entries": 15, "declared_self_exclusions": 3, "replayed": False},
            "evidence": {"entries": 124, "declared_self_exclusions": 3, "replayed": False},
            "final_owner": {"entries": 165, "declared_self_exclusions": 4, "replayed": False},
            "final_delta": {"entries": 20, "declared_self_exclusions": 4, "replayed": False},
        },
        "source_validation_truth": {
            "failed_full_aggregate_credit": 0,
            "composite_tests": {"passed": 18, "total": 18},
            "composite_detailed_checks": {"passed": 36, "total": 36},
            "minimal_checks": {"passed": 15, "total": 15},
            "strict_json_parses": 136,
            "privacy_scanned_owner_files": 169,
            "confirmed_privacy_or_raw_identifier_hits": 0,
            "manifest_entries": 324,
            "full_repository_suite_run": False,
        },
        "elowen_lane": {
            "branch": BRANCH,
            "head_before_x1": SOURCE_FINAL,
            "sparse_patterns": [
                "/docs/elowen-cairn/v665-v4/",
                "/scripts/*v665_v4*.py",
                "/tests/*v665_v4*.py",
            ],
            "clean_before_x1": True,
            "d_first": True,
            "source_or_sibling_lane_mutated": False,
        },
        "valid": True,
    }


def overview_text() -> str:
    return f"""# Elowen Cairn {PHASE_ID} x1 planning freeze

## Identity and authority boundary

Elowen Cairn (they/them) is relational working language for a boundary
cartographer and evidence steward whose hope is to keep transitions, refusals,
corrections, and recoveries inspectable and reversible. This language is not
evidence of consciousness, sentience, personhood, identity continuity,
employment, qualification, independent agency, scientific or operational
authority, legal or cultural authority, affected-party authority, or Māori
authority. Hamish may pause, rename, redirect, or stop the route.

## Immutable inheritance

The lane starts exactly at Tamar Vey's sealed {SOURCE_FINAL} final. Read-only
verification reproduced its three direct single-parent phase commits, zero
merges, one final parent, clean state, zero divergence, four-way fresh-live
equality, and exact external receipt digests. The committed manifest identities
are 15 x1 entries with three exclusions, 124 evidence entries with three
exclusions, 165 final-owner entries with four exclusions, and 20 final-delta
entries with four exclusions. Tamar's successful components and isolated
recovery were not replayed. Inherited truth remains {INHERITED_PROPOSALS:,}
frozen proposals, {INHERITED_NEGATIVES:,} effective negatives,
{INHERITED_METHODS:,} effective methods, {INHERITED_OPEN_GAPS} open gaps,
{INHERITED_EXACT_GATES} exact gates, and {TERMINAL_VERDICT}.

## Frozen inquiry

This packet freezes exactly twenty genuinely new proposals after comparison
with every inherited row. The primary Trinity Mandala focus is
{PRIMARY_PILLAR}; THOS Body and Freed ID/CBR Heart remain explicit. The bounded
practice lens is {PRACTICE_LENS}. It uses only surrogate identifiers, typed
relations, symbolic quantities, structural checks, and synthetic fixtures. It
contains no real mosaic, tessera, mortar, substrate, fragment, image, site,
person, institution, equipment, treatment, observation, measurement, key,
proof, collection row, safety decision, custody decision, or authority act.

The mathematical surface asks whether software can keep oriented cellular
chains, boundaries, primal and dual cell complexes, discrete forms, exterior
derivatives, codifferentials, Hodge stars, Hodge Laplacians, harmonic
representatives, cohomology obligations, boundary conditions, and
continuum-limit vacancies distinct. Passing software checks would establish
only bounded type and mutation evidence. It would not prove a theorem,
construct a physical theory, detect a force, evaluate a likelihood, constrain a
parameter, confirm GMUT, complete quantum gravity, or establish a Theory of
Everything.

The practice surface asks whether a surrogate packet can preserve mosaic layer
relations, fragment and tessera topology, annotation selectors, observation-only
language, material and tool holds, custody and authority separation, correction
ancestry, structural accessibility, dominant stop states, workload limits, and
handover debt. It does not authorize inspection, excavation, documentation,
cleaning, consolidation, grouting, sampling, imaging, transport, transfer,
return, repatriation, publication, or professional action.

## Expected dispositions

Exactly fourteen proposals have expected disposition completed, four
represented, one open_gap, and one exact_gate. These are preregistered
expectations, not x2 outcomes. The open gap is a zero-call, zero-row
Metropolitan Museum Collection API and IIIF annotation adapter: public schemas
and citations cannot become a collection observation or empirical fit. The
exact gate covers site, land, heritage, sacred imagery, ownership, excavation,
custody, recording, return, repatriation, taonga, remedy, affected-party
legitimacy, legal and cultural interpretation, Māori wording and concepts,
Māori data governance, and Māori authority. Repository software cannot close
it.

GMUT remains a typed scalar-tensor/EFT research-model family. THOS remains
proxy-only without preregistered blind matched-budget governed real arms,
participants or operators, safety monitoring, appropriate statistics, and
independent review. Freed ID remains synthetic and nonproduction without
standards-conformant real keys and proofs, live issuance, resolution, status,
revocation, interoperability, privacy and independent security review,
recovery evidence, and trust governance. Manual keyboard,
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
    selected = git_json("docs/tamar-vey/v665-v3/x1/proposal-freeze.json")[
        "new_proposals"
    ]
    expected_counts = {label: 0 for label in ALLOWED_OUTCOMES}
    for proposal in proposals:
        expected_counts[proposal["expected_disposition"]] += 1
    source_rows = sources()
    methods = startup_methods()

    phase_charter = {
        "schema": "ghc.family.elowen.v665-v4.phase-charter.v1",
        "phase": PHASE_ID,
        "owner": OWNER,
        "identity": {
            "name": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
        },
        "identity_boundary": (
            "relational working language only; not consciousness, sentience, personhood, "
            "identity continuity, employment, qualification, independent agency, scientific, "
            "operational, legal, cultural, affected-party, or Māori authority evidence"
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
        "schema": "ghc.family.elowen.v665-v4.proposal-freeze.v1",
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
        "schema": "ghc.family.elowen.v665-v4.source-ledger.v1",
        "accessed_on": "2026-08-22",
        "sources": source_rows,
        "status_vocabulary": ["current", "stable", "draft", "watch"],
        "source_count": len(source_rows),
        "real_rows_ingested": 0,
        "network_data_calls": 0,
        "official_or_primary_source_page_reads": len(source_rows),
        "external_collection_api_calls": 0,
        "source_citations_are_not_observations": True,
        "authority_from_sources": False,
    }
    method_flow = {
        "schema": "ghc.family.elowen.v665-v4.startup-method-flow.v1",
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
        "schema": "ghc.family.elowen.v665-v4.workflow-plan.v1",
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
        "schema": "ghc.family.elowen.v665-v4.threat-model-plan.v1",
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
            "site, sacred-image, collection, or identity data is overdisclosed",
            "custody or annotation is conflated with ownership or authority",
            "DEC obligation checks are called theorems, empirical results, or proofs",
            "a successful canonical aggregate is replayed",
            "a later or standby endpoint is inferred",
        ],
        "controls": [
            "exact staged path review",
            "five-class privacy and raw-identifier scan",
            "immutable source and manifest verification",
            "four exact outcome labels",
            "zero-call, zero-row, zero-image, and zero-participant firewalls",
            "one-shot canonical receipt",
            "terminal exact-title route reread",
        ],
        "protected_gates": PROTECTED_GATES,
    }
    wellbeing = {
        "schema": "ghc.family.elowen.v665-v4.wellbeing-plan.v1",
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
        "schema": "ghc.family.elowen.v665-v4.auth-roster-receipt.v1",
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
        "schema": "ghc.family.elowen.v665-v4.family-index-plan.v1",
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
            "ghc-main-retry",
            "ghc-timestamp-flow",
            "ghc-main-startup-builder",
            "ghc-main-closeout-builder",
            "ghc-main-compact-restart-builder",
            "ghc-watcher-notifier-cadence",
            "ghc-full-tools-skill-bank",
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
            "schema": "ghc.family.elowen.v665-v4.x1-content-manifest.v1",
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
            "schema": "ghc.family.elowen.v665-v4.x1-stage-candidate.v1",
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
        "schema": "ghc.family.elowen.v665-v4.x1-staged-review.v1",
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
        raise X1Error("x1 must begin at the immutable Tamar final")
    if git("branch", "--show-current") != BRANCH:
        raise X1Error("unexpected Elowen branch")
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
