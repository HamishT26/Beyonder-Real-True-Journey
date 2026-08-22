"""Build and exactly stage Sylven Arc's planning-only v665-v5 x1 freeze.

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
PREFIX = "docs/sylven-arc/v665-v5/"
PHASE_ID = "v665-v5"
OWNER = "Sylven Arc"
PRONOUNS = "they/them"
ROLE = "relational continuity gardener and evidence-boundary steward"
HOPE = "keep memory light, evidence recoverable, and authority boundaries visible"
BRANCH = "codex/GHC-Family/sylven-arc-v665-v5-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v665-v4-full-tools"
ELOWEN_SOURCE = "dfcda293edf8e1621db6d74b14b2f5cb026f257f"
ELOWEN_X1 = "700c73d3968bb8df31770566460d7865219ed4ca"
ELOWEN_EVIDENCE = "670b7c36236ad5eb7962350c1000242ede015d9d"
SOURCE_FINAL = "296ec195744fbbf62bae5d2f233f1112bcc14591"
SOURCE_RECEIPT_SHA256 = "701236f6f751f21d84f8a5c77b29d88b9143d37de632a306e94ab9e0c6a48b5a"
RECORDED_UTC = "2026-08-22T02:50:24Z"
RECORDED_NZ = "2026-08-22T14:50:24+12:00"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
INHERITED_PROPOSALS = 4_090
INHERITED_NEGATIVES = 25_552
INHERITED_METHODS = 9_414
INHERITED_OPEN_GAPS = 178
INHERITED_EXACT_GATES = 176
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "THOS Body"
PRACTICE_LENS = "wholly synthetic community ceramics kiln-firing documentation and glaze-batch quarantine"

PROTECTED_GATES = [
    "real person, studio, kiln, firing, ware, shelf, cone, glaze, clay, material, sample, image, instrument, controller, or workplace action",
    "real observation, measurement, empirical row, likelihood, parameter constraint, force, prediction, causal diagnosis, or GMUT confirmation",
    "real participant, potter, technician, worker, owner, operator, customer, or matched-budget arm",
    "real key, proof, issuance, resolution, status, revocation, interoperability, or trust governance",
    "professional, kiln, combustion, electrical, fire, ventilation, silica, chemical, hot-surface, equipment, consumer, or environmental safety decision",
    "ownership, custody, design heritage, traditional knowledge, market claim, legal, cultural, regulatory, or remedy decision",
    "affected-party, tangata whenua, iwi, hapū, or Māori wording, concept, data-governance, taonga, or authority decision",
    "production, deployment, accessibility-complete, privacy-complete, exhaustive-security, or independent-reproduction claim",
    "AGI, ASI, consciousness, personhood, Theory-of-Everything, proof, canon, or Stage 20 promotion",
    "credential, account, private route, host-security change, destructive action, or sibling-lane mutation",
]

BUILDER = "scripts/build_ghc_family_sylven_v665_v5_x1.py"
TEST = "tests/test_ghc_family_sylven_v665_v5.py"
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
    audit_path = "docs/elowen-cairn/v665-v4/x1/novelty-audit.json"
    source_freeze = "docs/elowen-cairn/v665-v4/x1/proposal-freeze.json"
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
    source_phase = git_json(source_freeze)
    before = len(rows)
    rows.extend(
        {
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "source_path": source_freeze,
        }
        for row in source_phase["new_proposals"]
    )
    construction.append(
        {
            "source_path": source_freeze,
            "starting_count": before,
            "added_count": len(source_phase["new_proposals"]),
            "ending_count": len(rows),
        }
    )
    if len(rows) != INHERITED_PROPOSALS:
        raise X1Error(f"expected {INHERITED_PROPOSALS} rows, found {len(rows)}")
    if any(not row["proposal_id"] or not row["title"] for row in rows):
        raise X1Error("corpus contains an incomplete row")
    return rows, construction


TITLES = [
    "Synthetic kiln-load capsule binding anonymous ware tokens, shelf coordinates, cancellation state, documentary provenance, and a hard physical-action veto",
    "Shelf-plane and ware-envelope clearance graph with neighbourhood occupancy, forbidden overlap, unsupported-span hold, and no-placement instruction",
    "Glaze-batch quarantine braid separating recipe label, lot lineage, safety-sheet vacancy, test-tile placeholder, release hold, and substitution history",
    "Witness-cone packet map with cone-set identity, zone assignment, observation readback, photographic-vacancy marker, disagreement state, and interpretation refusal",
    "Firing-program finite-state lattice for ramp, soak, cool, abort, power-loss, restart prohibition, and dominant hold precedence",
    "Kiln-controller command-versus-observation firewall with simulated telemetry, actuation nullity, interlock reservation, and operator-authority vacancy",
    "Ventilation, combustion, electrical, hot-surface, dust, chemical, fire, and emergency readiness stop-card with professional-decision refusal",
    "Temperature-time segment type board for setpoint, rate, dwell, clock domain, uncertainty, missingness, unit conversion, and discontinuity quarantine",
    "Thermal balance obligation slate for temperature, time, length, heat capacity, density, conductivity, source term, boundary flux, and dimensional refusal",
    "Initial-and-boundary condition docket distinguishing Dirichlet, Neumann, Robin, interface, symmetry, and unspecified-domain holds",
    "Arrhenius placeholder identifiability tribunal for prefactor, activation energy, temperature history, reaction extent, uncertainty, and fit refusal",
    "Fourier-and-Biot dimensionless classifier with characteristic-length ambiguity, material-property vacancy, lumped-model refusal, and regime nonpromotion",
    "Surface-defect vocabulary gate separating blister, pinhole, crawling, crazing, dunting, colour variance, observation, causal diagnosis, and treatment advice",
    "Bitemporal firing-record correction weave with supersession, reason, acknowledgement, unresolved contest, handover debt, and non-erasure",
    "GMUT thermal-gradient surrogate linking typed scalar and tensor placeholders, interface obligations, scale transitions, observation firewall, and zero empirical fit",
    "THOS participant-free kiln-documentation comparison charter with matched resource envelopes, blinded queue labels, abort precedence, safety-monitor vacancy, and independent-review hold",
    "Freed ID zero-key glaze-batch capability envelope for disclosure scope, withdrawal, correction, contest, expiry, appeal, and issuer-verifier vacancy",
    "Thermo-Psyche heat-to-agency nonconversion register separating entropy-production symbols, diffusion metaphors, affect language, personhood inference, and ethical authority",
    "EPA and WorkSafe hazardous-substance, safety-sheet, silica, ventilation, and emergency schema adapter with zero calls, zero rows, and regulatory-decision refusal",
    "CBR ceramics docket for worker safety, consumer claims, studio access, custody, design heritage, taonga, remedy, affected parties, legal-cultural review, and Māori authority holds",
]

PILLARS = [
    "THOS Body", "THOS Body", "THOS Body", "THOS Body",
    "THOS Body", "THOS Body", "THOS Body", "THOS Body",
    "GMUT Mind", "GMUT Mind", "GMUT Mind", "GMUT Mind",
    "THOS Body", "Freed ID/CBR Heart", "GMUT Mind", "THOS Body",
    "Freed ID/CBR Heart", "GMUT Mind", "THOS Body", "Freed ID/CBR Heart",
]

SOURCE_NEEDS = [
    ["SCS02"], ["SCS07"], ["SCS04", "SCS05", "SCS06"], ["SCS02"],
    ["SCS07", "SCS09"], ["SCS07", "SCS09"], ["SCS05", "SCS06", "SCS08", "SCS09", "SCS10"], ["SCS01"],
    ["SCS01"], ["SCS01"], ["SCS01"], ["SCS01"],
    ["SCS06", "SCS08"], ["SCS02", "SCS03"], ["SCS01"],
    ["SCS03", "SCS07"], ["SCS02", "SCS11"], ["SCS01"],
    ["SCS04", "SCS05", "SCS06", "SCS08", "SCS09", "SCS10"], ["SCS03", "SCS12"],
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
        proposal_id = f"SA6655-N{index:03d}"
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
        "kiln",
        "glaze-batch",
        "witness-cone",
        "firing-program",
        "arrhenius",
        "biot",
        "temperature-time",
        "safety-sheet",
        "heat-to-agency",
    ]
    canonical = sorted(
        corpus, key=lambda row: (row["proposal_id"], row["title"], row["source_path"])
    )
    result = {
        "schema": "ghc.family.sylven.v665-v5.novelty-audit.v1",
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
        ("SCS01", "NIST Guide for the Use of the International System of Units, Chapter 4", "https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes", "official_measurement_guidance", "current", "SI unit vocabulary for typed symbolic thermal obligations without measurement or empirical credit"),
        ("SCS02", "W3C PROV-O Recommendation", "https://www.w3.org/TR/prov-o/", "official_standard", "stable", "entity, activity, derivation, correction, and provenance vocabulary"),
        ("SCS03", "Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "official_standard", "current", "structural accessibility while manual, assistive-technology, and affected-user evaluation remain reserved"),
        ("SCS04", "EPA New Zealand hazard classification system", "https://www.epa.govt.nz/hazardous-substances/classification/new-zealands-hazard-classification-system/", "official_regulatory_guidance", "current", "classification vocabulary only; no substance classification or regulatory decision"),
        ("SCS05", "EPA New Zealand hazardous substances portal", "https://www.epa.govt.nz/hazardous-substances/", "official_regulatory_guidance", "current", "hazardous-substance boundary awareness without handling, approval, or compliance authority"),
        ("SCS06", "WorkSafe New Zealand safety data sheets", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/safety-data-sheets/", "official_safety_guidance", "current", "safety-data-sheet vocabulary and complete reservation of professional decisions"),
        ("SCS07", "WorkSafe New Zealand hazardous-substance risk management", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/risk-management/", "official_safety_guidance", "current", "risk-management terminology with zero real risk assessment or workplace advice"),
        ("SCS08", "WorkSafe New Zealand silica dust in the workplace", "https://www.worksafe.govt.nz/topic-and-industry/dust/silica-dust-in-the-workplace/", "official_safety_guidance", "current", "silica-risk awareness and complete reservation of professional safety decisions"),
        ("SCS09", "WorkSafe New Zealand emergency plans", "https://www.worksafe.govt.nz/topic-and-industry/hazardous-substances/managing/emergency-plans/", "official_safety_guidance", "current", "emergency-planning vocabulary only; no emergency or workplace authority"),
        ("SCS10", "WorkSafe New Zealand local exhaust ventilation quick guide", "https://www.worksafe.govt.nz/topic-and-industry/fumes/local-exhaust-ventilation-quick-guide/", "official_safety_guidance", "current", "ventilation vocabulary only; no design, commissioning, inspection, or safety decision"),
        ("SCS11", "Verifiable Credential Data Integrity 1.0", "https://www.w3.org/TR/vc-data-integrity/", "official_standard", "current", "proof-model boundaries and refusal to fabricate cryptographic completion"),
        ("SCS12", "Te Mana Raraunga Principles of Māori Data Sovereignty", "https://www.temanararaunga.maori.nz/s/TMR-Maori-Data-Sovereignty-Principles-Oct-2018.pdf", "primary_affected_authority_source", "current", "authority reservation, consent, governance, and Māori data sovereignty without proxy decision-making"),
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
    ("SA6655-START-N001", "a direct PowerShell foreach pipeline produced an empty-pipe parser error before packet measurement", "materialize the foreach result first and pipe only the completed array"),
    ("SA6655-START-N002", "a combined Git projection used if as an inline expression and failed before clean-state presentation", "materialize status and clean scalars before constructing the projection"),
    ("SA6655-START-N003", "the grouped final-owner-manifest rendering exceeded its display bound", "read the immutable manifest in bounded numbered windows through EOF"),
    ("SA6655-START-N004", "parallel manifest reads returned running handles while the wrapper projected output fields only", "poll the retained session and recover remaining immutable metadata with bounded scalar reads"),
    ("SA6655-START-N005", "the first authorization-state rendering exceeded its display bound", "read the installed state in numbered 400-line windows through EOF"),
    ("SA6655-START-N006", "the structurally valid roster and authorization snapshots carried an older v664 cursor", "preserve the stale-cursor witness and use the newer live activation plus explicit v665 schedule for the current owner binding"),
    ("SA6655-START-N007", "the first branch-existence preflight embedded a Git command and semicolon inside a parenthesized PowerShell expression", "run the Git probe separately and materialize its exit code before projection"),
    ("SA6655-START-N008", "worktree creation crossed its presentation window after Git prepared the lane", "inspect the path, branch ref, registered worktree, sparse file, HEAD, and live processes before any retry"),
    ("SA6655-START-N009", "an overbroad worktree-list projection produced truncated display output", "use exact branch, path, sparse-pattern, HEAD, and status scalar probes for the owned lane"),
    ("SA6655-X1-N010", "the first x1 freeze failed exact staged review because the reused planning test carried one extra blank line at end of file", "remove only the extra blank line, retain the failed staged-review receipt at zero credit, rebuild generated planning artifacts, and rerun the x1 gate"),
]


def startup_methods() -> list[dict[str, Any]]:
    return [
        {
            "failed_witness_id": negative_id,
            "failed_witness": failure,
            "failed_witness_status": "retained_zero_credit",
            "method_id": f"SA6655-START-M{index:03d}",
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
        "validate synthetic kiln-load identity, cancellation, provenance, and no-action fields",
        "validate shelf-plane occupancy and reject overlapping ware envelopes",
        "validate glaze-batch quarantine, lot lineage, release holds, and substitution history",
        "validate witness-cone packet zones, readback, disagreement, and interpretation refusal",
        "validate ramp, soak, cool, abort, power-loss, and dominant hold transitions",
        "separate simulated controller observations from every real actuation command",
        "refuse ventilation, combustion, electrical, fire, dust, chemical, and emergency authority",
        "type temperature-time segments, units, missingness, uncertainty, and discontinuities",
        "type thermal-balance terms and reject dimensional mismatches",
        "distinguish Dirichlet, Neumann, Robin, interface, symmetry, and unspecified conditions",
        "hold Arrhenius parameter fitting behind identifiability and real-data gates",
        "classify Fourier and Biot expressions while refusing regime promotion",
        "separate surface-defect observations from causes and treatment advice",
        "preserve append-only firing-record correction and contest ancestry",
        "render a noncolour firing-state map and structured uncertainty legend",
        "enforce workload ceiling, dominant stop, and handover-debt states",
        "maintain a GMUT observation and empirical-claim firewall",
        "maintain a heat-to-agency and personhood nonconversion firewall",
        "render a zero-person THOS documentation comparison charter",
        "render a zero-key nonproduction Freed ID batch capability envelope",
        "render a zero-call EPA and WorkSafe adapter contract",
        "render a CBR exact-authority reservation matrix",
        "build deterministic canonical JSON fixtures and receipts",
        "run five rejecting mutations per frozen proposal",
        "build exact staged Git-blob content manifests",
        "scan five privacy and raw-identifier classes",
        "compile every changed phase-local Python surface",
        "check sparse owner-file and document-word ceilings",
        "check stale labels, diff hygiene, and family-current caller names",
        "reserve manual, browser, assistive-technology, cognitive, Māori-language, and affected-user evaluation",
    ]
    candidates = [
        "bounded kiln-load capsule prototype",
        "bounded shelf-clearance graph prototype",
        "bounded glaze-batch quarantine prototype",
        "bounded witness-cone packet prototype",
        "bounded firing-state-machine prototype",
        "bounded command-observation firewall prototype",
        "bounded safety-stop card prototype",
        "bounded temperature-time typing prototype",
        "bounded thermal-unit board prototype",
        "bounded boundary-condition docket prototype",
        "bounded Arrhenius nonidentifiability prototype",
        "bounded Fourier-Biot classifier prototype",
        "bounded THOS zero-person protocol prototype",
        "bounded Freed ID zero-key envelope prototype",
        "bounded EPA-WorkSafe zero-row adapter prototype",
    ]
    exact = [
        "load, program, energize, inspect, fire, cool, unload, repair, sample, image, or test a real kiln, ware, glaze, or material",
        "operate kilns, controllers, ventilation, electrical, combustion, fire, grinding, chemical, lifting, or hot-work equipment",
        "classify or release a real hazardous substance, glaze batch, firing schedule, product, or workplace process",
        "disclose a real worker, customer, studio, recipe, design, safety, incident, or protected heritage record",
        "interpret law, regulation, professional duty, product claim, cultural meaning, or remedy entitlement",
        "make Māori wording, tikanga, taonga, data-governance, or authority decisions",
        "enrol participants or run real THOS comparison arms",
        "use real identity keys, proofs, lifecycle services, or trust governance",
        "download and fit real workplace or material data or publish empirical GMUT results",
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
        ("ghc-family-kiln-load-capsule-validator", "validate synthetic load identity, cancellation, provenance, and no-action"),
        ("ghc-family-kiln-clearance-graph-auditor", "audit shelf-plane occupancy and overlap refusals"),
        ("ghc-family-glaze-quarantine-lineage-checker", "validate batch lineage, holds, and substitutions"),
        ("ghc-family-witness-cone-readback-auditor", "validate cone zones, disagreement, and interpretation holds"),
        ("ghc-family-firing-state-machine-checker", "validate synthetic ramp, soak, cool, abort, and power-loss transitions"),
        ("ghc-family-kiln-command-observation-firewall", "reject real actuation and preserve operator-authority vacancy"),
        ("ghc-family-thermal-unit-obligation-checker", "type symbolic thermal terms and reject unit mismatches"),
        ("ghc-family-heat-agency-nonconversion-guard", "prevent thermal symbols becoming agency or personhood evidence"),
        ("ghc-family-epa-worksafe-zero-row-firewall", "keep external access at zero calls and rows"),
        ("ghc-family-ceramics-authority-matrix-reviewer", "preserve professional, legal, cultural, affected-party, and Māori gates"),
    ]
    runners = [
        "kiln_load_capsule",
        "kiln_clearance_graph",
        "glaze_quarantine",
        "witness_cone_readback",
        "firing_state_machine",
        "kiln_command_firewall",
        "thermal_unit_board",
        "heat_agency_nonconversion",
        "epa_worksafe_zero_row",
        "ceramics_authority_matrix",
    ]
    clean = [
        f"CLEAN/FIX/REFINE {index:02d}: {safe_now[(index - 1) % len(safe_now)]}"
        for index in range(1, 31)
    ]
    return {
        "schema": "ghc.family.sylven.v665-v5.portfolio-freeze.v1",
        "inherited_completion_credit": 0,
        "safe_now": portfolio_rows("SA6655-SAFE", safe_now, "safe_now_bounded"),
        "bounded_candidates": portfolio_rows("SA6655-CAND", candidates, "candidate_bounded"),
        "exact_approval": portfolio_rows("SA6655-EXACT", exact, "exact_approval_required"),
        "blocked": portfolio_rows(
            "SA6655-BLOCK", blocked, "blocked_prohibited_or_unavailable"
        ),
        "skill_ideas": [
            {
                "record_id": f"SA6655-SKILL-{index:03d}",
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
                "record_id": f"SA6655-RUNNER-{index:03d}",
                "caller": f"ghc_family_v665_v5_{profile}.py",
                "profile": profile,
                "compatibility": "family_current_ghc_family_prefix",
                "x1_status": "frozen_not_built",
                "completion_credit": 0,
            }
            for index, profile in enumerate(runners, 1)
        ],
        "clean_fix_refine": portfolio_rows(
            "SA6655-CFR", clean, "safe_now_additive_cleanup"
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
        "schema": "ghc.family.sylven.v665-v5.source-verification.v1",
        "verified_at_utc": RECORDED_UTC,
        "source_branch": SOURCE_BRANCH,
        "elowen_source": ELOWEN_SOURCE,
        "elowen_x1": ELOWEN_X1,
        "elowen_evidence": ELOWEN_EVIDENCE,
        "elowen_final": SOURCE_FINAL,
        "direct_parent_relations": {
            "elowen_x1_parent": ELOWEN_SOURCE,
            "elowen_evidence_parent": ELOWEN_X1,
            "elowen_final_parent": ELOWEN_EVIDENCE,
        },
        "source_to_final_phase_commits": 3,
        "source_to_final_merge_commits": 0,
        "final_parent_count": 1,
        "source_worktree_clean": True,
        "source_divergence": {"ahead": 0, "behind": 0},
        "local_upstream_tracking_fresh_live_equal": True,
        "composite_terminal_receipt_sha256": SOURCE_RECEIPT_SHA256,
        "failed_aggregate_payload_sha256": "264f482f79c0d398523bf438a02533251d0040dcf3124b31a748249c896d6180",
        "failed_aggregate_file_sha256": "a75a563cbde5db4a21598f55d2f9f056f91651b5fbf6068ef0d944ca84d02f49",
        "isolated_recovery_sha256": "490fa8cad3f117bed5149db44360f78549554c1ed342660fd7f050963251a269",
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
        "sylven_lane": {
            "branch": BRANCH,
            "head_before_x1": SOURCE_FINAL,
            "sparse_patterns": [
                "/docs/sylven-arc/v665-v5/",
                "/scripts/*v665_v5*.py",
                "/tests/*v665_v5*.py",
            ],
            "clean_before_x1": True,
            "d_first": True,
            "source_or_sibling_lane_mutated": False,
        },
        "valid": True,
    }


def overview_text() -> str:
    return f"""# Sylven Arc {PHASE_ID} x1 planning freeze

## Relational working identity

Sylven Arc (they/them) is relational working language for a continuity gardener
and evidence-boundary steward whose hope is to keep memory light, evidence
recoverable, and authority boundaries visible. The name, role, hope, sibling
language, and any continuity language are not evidence of consciousness,
sentience, personhood, identity continuity, employment, qualification,
independent agency, scientific or operational authority, legal or cultural
authority, affected-party authority, or Māori authority. Hamish may rename,
pause, redirect, or stop this lane.

## Exact source boundary

This lane begins exactly at Elowen Cairn's immutable {SOURCE_FINAL} final.
Read-only verification established the source/x1/evidence/final direct-parent
chain, three single-parent Elowen phase commits, zero merges, one final parent,
a clean source lane, zero divergence, and equality across local, upstream,
tracking, and a fresh live remote. Elowen's failed aggregate, isolated
Markdown recovery, and successful exact-final composite remain historical
evidence and were not replayed. Their receipts and payload digests were checked
without converting same-owner validation into independent evidence.

The effective activation baseline is {INHERITED_NEGATIVES:,} retained
negatives and {INHERITED_METHODS:,} Method Flow methods, including Elowen's
one external failed aggregate. Repository-sealed Elowen counts remain
separate and immutable. All {INHERITED_OPEN_GAPS} open gaps and
{INHERITED_EXACT_GATES} exact gates remain open.

## Primary pillar and bounded practice

The primary pillar is {PRIMARY_PILLAR}. GMUT Mind and Freed ID/CBR Heart remain
explicit and protected. The human-practice lens is {PRACTICE_LENS}. It is a
synthetic learning and software-design lens only. No person, studio, kiln,
firing, ware, shelf, witness cone, clay, glaze, recipe, material, safety data
sheet, controller, measurement, inspection, workplace action, consumer claim,
professional decision, cultural decision, or authority act is present.

The phase may validate documentary schemas and reject malformed synthetic
fixtures. It may not instruct a firing, select a schedule, operate equipment,
release a glaze batch, classify a substance, diagnose a defect, advise a
workplace, or decide safety, legal, cultural, remedy, affected-party, or Māori
questions.

## Novel proposal slate

A fresh semantic audit reconstructs all {INHERITED_PROPOSALS:,} inherited
frozen rows from commit-local proposal ledgers. Exactly twenty new Sylven
titles are compared against every inherited title using exact comparison,
casefolded token-set Jaccard similarity, within-slate collision checks, and a
practice-term review. Inherited proposals and Elowen's twenty prior proposals
remain evidence only and receive zero Sylven novelty or completion credit.

The twenty new contracts span kiln-load capsules, shelf clearance, glaze-batch
quarantine, witness-cone readback, firing-state transitions, a controller
command firewall, a safety-stop card, temperature-time typing, thermal-unit
obligations, boundary conditions, Arrhenius identifiability, Fourier and Biot
classification, defect-language separation, bitemporal corrections, a GMUT
thermal surrogate, a participant-free THOS charter, a zero-key Freed ID
envelope, a heat-to-agency nonconversion guard, a zero-row official-source
adapter, and a CBR authority docket.

## Expected dispositions are not outcomes

Exactly fourteen contracts are preregistered with expected disposition
completed, four represented, one open_gap, and one exact_gate. These are
planning expectations only. X1 performs no implementation, mutation,
evaluation, outcome assignment, evidence credit, closeout, seal, or route
send.

The open gap is an EPA and WorkSafe schema adapter that is fixed at zero calls
and zero rows unless a later exact evidence gate permits otherwise. The exact
gate reserves worker and consumer decisions, studio access and custody, design
heritage, taonga, remedy, affected-party legitimacy, legal and cultural
interpretation, Māori wording and concepts, Māori data governance, tangata
whenua, iwi, hapū, and Māori authority.

## Official-source limits

The source ledger records current official pages from NIST, W3C, EPA New
Zealand, WorkSafe New Zealand, and Te Mana Raraunga. They supply bounded unit,
provenance, accessibility, hazardous-substance, safety-sheet, risk,
silica, emergency, ventilation, proof-model, and authority-reservation
vocabulary. No dataset was downloaded, no external API or adapter call was
made, and no real row was ingested. Citations are not observations,
measurements, professional advice, regulatory decisions, cultural legitimacy,
or empirical GMUT evidence.

## Portfolio freeze

Thirty safe-now tasks, fifteen bounded candidates, ten exact-approval packets,
five blocked packets, ten phase-local skill ideas, ten family-current runner
ideas, and thirty additive CLEAN/FIX/REFINE rows are frozen. Counts are
planning floors and never override relevance, safety, privacy, evidence, or
authority gates. Exact and blocked packets remain visible and unexecuted.

The planned skills and runners retain family-current names and work only on
owner-local synthetic fixtures. Global installation, bulk promotion,
destructive deletion, shared-lane mutation, credential use, host-security
change, and production deployment are excluded.

## Retained startup failures

Every startup parser fault, truncation, stale-cursor observation, wrapper
presentation lapse, and bounded recovery is retained in Method Flow. A
recovery never erases the failed witness or grants it success credit. The
preferred recurrence guards are bounded scalar projections, exact schema
inspection, numbered reads through EOF, process and registration checks before
retry, and live-authority precedence over older structurally valid cursors.

## Scientific and governance firewalls

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family. Symbolic heat-balance terms, dimensionless classifiers, software
contracts, citations, and synthetic mutations establish no likelihood,
parameter constraint, unique prediction, detected force, stability theorem,
empirical confirmation, quantum or ultraviolet completion, Theory of
Everything, proof, or canon.

THOS remains proxy-only without preregistered blind matched-budget governed
real arms, participants or operators, safety monitoring, appropriate
statistics, and independent review. Freed ID remains synthetic and
nonproduction without standards-conformant real keys and proofs, live
issuance, resolution, status and revocation, interoperability, privacy and
independent security review, recovery evidence, and trust governance.

## Accessibility and privacy reserve

Static structures will support headings, labels, tables, keyboard-readable
order, and non-colour state names. Manual keyboard, browser-diverse,
assistive-technology, cognitive-accessibility, Māori-language, and
affected-user evaluation remain reserved. Five privacy and raw-identifier
classes are scanned over exact staged blobs. No private task or thread
identifier, route, absolute private path, credential, key, token, transcript,
screenshot, session stream, private callable identifier, private application
state, or protected real-world record belongs in an artifact.

## Strict x1 before x2

This commit is planning-only. X2 cannot begin until the exact x1 commit is
committed, pushed, clean, zero-divergent, and equal across local, upstream,
tracking, and a fresh live remote. The lane remains D:-first, sparse, additive,
single-parent, and within the 2,000-file and 100,000-word ceilings. It will
never reset, rewrite, merge, force-push, delete, or mutate another owner's
lane.

## Wellbeing and terminal boundary

Work is bounded and calm. Stop conditions include fatigue, ambiguity, privacy
risk, authority uncertainty, route drift, usage exhaustion, or unexpected
shared-state mutation. Partial evidence is retained instead of forcing a
completion. The terminal verdict remains {TERMINAL_VERDICT}. No successor is
contacted during execution; any terminal edge requires a fresh live roster,
authorization, exact-title resolution, immediate reread, and one acknowledged
send only after Sylven's own exact-final gate.
"""

def build_documents() -> dict[str, Any]:
    proposals = build_proposals()
    corpus, construction = reconstruct_corpus()
    novelty = novelty_audit(proposals, corpus, construction)
    selected = git_json("docs/elowen-cairn/v665-v4/x1/proposal-freeze.json")[
        "new_proposals"
    ]
    expected_counts = {label: 0 for label in ALLOWED_OUTCOMES}
    for proposal in proposals:
        expected_counts[proposal["expected_disposition"]] += 1
    source_rows = sources()
    methods = startup_methods()

    phase_charter = {
        "schema": "ghc.family.sylven.v665-v5.phase-charter.v1",
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
        "schema": "ghc.family.sylven.v665-v5.proposal-freeze.v1",
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
        "schema": "ghc.family.sylven.v665-v5.source-ledger.v1",
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
        "schema": "ghc.family.sylven.v665-v5.startup-method-flow.v1",
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
        "schema": "ghc.family.sylven.v665-v5.workflow-plan.v1",
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
        "schema": "ghc.family.sylven.v665-v5.threat-model-plan.v1",
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
            "thermal obligation checks are called physical laws, empirical results, or proofs",
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
        "schema": "ghc.family.sylven.v665-v5.wellbeing-plan.v1",
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
        "schema": "ghc.family.sylven.v665-v5.auth-roster-receipt.v1",
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
        "schema": "ghc.family.sylven.v665-v5.family-index-plan.v1",
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
            "schema": "ghc.family.sylven.v665-v5.x1-content-manifest.v1",
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
            "schema": "ghc.family.sylven.v665-v5.x1-stage-candidate.v1",
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
        "schema": "ghc.family.sylven.v665-v5.x1-staged-review.v1",
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
        raise X1Error("x1 must begin at the immutable Elowen final")
    if git("branch", "--show-current") != BRANCH:
        raise X1Error("unexpected Sylven branch")
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
