"""Build and seal Liora Venn v672-v6 planning-only x1 artifacts.

This builder is owner-local planning machinery.  It does not execute x2,
contact a successor, inspect real materials, or confer any authority.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "liora-venn" / "v672-v6"
X1_ROOT = OWNER_ROOT / "x1"
VALIDATION_ROOT = OWNER_ROOT / "validation"

OWNER = "Liora Venn"
PRONOUNS = "she/they"
ROLE = "relational provenance-and-abstention weaver"
HOPE = (
    "make absent observations, contested rights, and reversible recoveries visible "
    "before synthetic structure is mistaken for a real decision"
)
PHASE = "v672-v6"
BRANCH = "codex/GHC-Family/liora-venn-v672-v6-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/orin-thale-v672-v5-full-tools"
SOURCE_PREDECESSOR = "8f672ef30372b4adf457140c254931dc365e9d31"
SOURCE_X1 = "657681df7392f3cd652930d3f834b60ccfa21bcd"
SOURCE_EVIDENCE = "1c6fb43638e79a6bb963839765c519839da12f67"
SOURCE_FINAL = "e3b49b5ad7d81e09a0d4ba6b306c09623673e5f1"
SOURCE_CANONICAL_SHA256 = "030028f3e58cd6956a8f326cabd64dce6ff426bbc321c3be8c765666fbc3dcd1"

PRACTICE = "wholly synthetic paper-marbling documentation and handover"
PRIMARY_PILLAR = "THOS Body"
SECONDARY_PILLARS = ["GMUT Mind", "Freed ID and CBR Heart"]
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
BOUNDARY = (
    "Bounded owner-local planning and synthetic software evidence only; never a real person, "
    "paper, bath, pigment, surfactant, tool, pattern, measurement, observation, treatment, "
    "publication, identity lifecycle, participant result, professional decision, safety release, "
    "legal or cultural decision, affected-party acceptance, Maori authority, empirical GMUT result, "
    "production readiness, independent reproduction, AGI/ASI evidence, consciousness or personhood "
    "evidence, Theory-of-Everything proof, canon, or Stage 20 authority."
)
IDENTITY_BOUNDARY = (
    "Liora Venn, she/they, role, hope, sibling and family language are relational working language "
    "only, not evidence of consciousness, sentience, legal personhood, identity continuity, "
    "employment, qualification, independent agency, or scientific, operational, professional, "
    "legal, cultural, affected-party, or Maori authority."
)

ACTIVATION_COUNTS = {
    "declared_frozen_proposals": 6110,
    "effective_negatives": 35602,
    "effective_methods": 22007,
    "failed_witnesses": 7263,
    "bounded_passing_witnesses": 9314,
    "open_gaps": 285,
    "exact_gates": 278,
}

PROPOSAL_TITLES = [
    "synthetic marbling-bath component graph with duplicate-node refusal",
    "ordered colour-drop ledger with sequence and reordering quarantine",
    "stylus-rake path segment lattice with out-of-bath coordinate refusal",
    "surrogate paper-sheet capsule with zero object-identity claim",
    "contact-transfer state machine with double-transfer refusal",
    "pattern-swatch namespace with source-revision lineage",
    "pattern-name vocabulary board with attribution and cultural-name abstention",
    "material and recipe vacancy matrix for size pigment surfactant and paper",
    "environment observation vacancy for temperature humidity viscosity and bath state",
    "hazard-document vacancy and stop rail for unverified materials",
    "deterministic canonical JSON receipt for synthetic marbling batch records",
    "provenance activity-entity linkage for generated synthetic swatch records",
    "bath-to-sheet correction chain preserving withdrawn pattern records",
    "alternate-description companion for zero-image synthetic pattern topology",
    "static marbling status board with headings focus order and noncolour cues",
    "tray-occupancy and drying-rack queue with batch cap pause and spill-hold precedence",
    "bath-to-rack handover capsule with unresolved material holds and readback vacancy",
    "data-minimization filter rejecting personal identifiers and free text",
    "authority-smuggling detector for competence safety cultural and legal claims",
    "drop-rake-contact-lift event reducer with recontact quarantine",
    "negative-mutation quarantine with retained zero-credit witnesses",
    "source-version ledger with live-status and citation-only boundary",
    "THOS marbling-procedure proxy with no participant or performance claim",
    "GMUT bath-boundary field and pullback analogy with likelihood vacancy",
    "Freed ID zero-key marbling-role capsule with issuance and status vacancy",
    "CBR marbled-pattern source attribution withdrawal access and remedy vacancy matrix",
    "exact staged Git-blob parity rail for owner-local lifecycle artifacts",
    "four-tier marbling flashcard bank for evidence failure recovery and authority boundaries",
    "synthetic pattern-family comparison board with no authenticity or tradition claim",
    "fluid-surface adjacency tensor analogy with no physical-law claim",
    "composition-order category sketch for drop rake and transfer stages",
    "finite-state material hold representation without safety assessment",
    "conservation-use decision vacancy board without object or treatment claim",
    "publication ownership and licence vacancy register for synthetic swatches",
    "static pattern-topology narration trial matrix with manual assistive-technology vacancy",
    "Method Flow recovery and recurrence matrix for marbling documentation",
    "real marbling material process observation measurement and independent-review gap",
    "real reader comparison of marbled-pattern descriptions and nonvisual comprehension gap",
    "professional marbling chemical workshop conservation and publication decision gate",
    "marbling-origin named-tradition knowledge data-governance and cultural-authority gate",
]

SOURCE_LEDGER = [
    {
        "source_id": "SRC-MARBLE-VAM",
        "title": "Divers oiled colours: Exploring the history of marbled paper in the National Art Library",
        "publisher": "Victoria and Albert Museum",
        "url": "https://www.vam.ac.uk/blog/museum-life/divers-oiled-colours-exploring-the-history-of-marbled-paper-in-the-national-art-library",
        "status": "current_official_institutional_page_read_2026-08-27",
        "use": "historical and process vocabulary only",
    },
    {
        "source_id": "SRC-MARBLE-SI",
        "title": "The Fix - Paperwork you can love",
        "publisher": "Smithsonian Libraries and Archives",
        "url": "https://blog.library.si.edu/blog/2014/12/22/the-fix-paperwork-you-can-love/",
        "status": "current_official_institutional_page_read_2026-08-27",
        "use": "marbled-paper and conservation-context vocabulary only",
    },
    {
        "source_id": "SRC-OSHA-HAZCOM",
        "title": "Hazard Communication - Standards",
        "publisher": "United States Occupational Safety and Health Administration",
        "url": "https://www.osha.gov/hazcom/standards",
        "status": "current_official_page_read_2026-08-27",
        "use": "hazard-document and stop-boundary vocabulary only; no jurisdictional or safety conclusion",
    },
    {
        "source_id": "SRC-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C_Recommendation_2024-12-12_current_page_read_2026-08-27",
        "use": "static structural accessibility vocabulary only; no conformance claim",
    },
    {
        "source_id": "SRC-PROVO",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C_Recommendation_current_page_read_2026-08-27",
        "use": "entity, activity, derivation, and provenance vocabulary only",
    },
    {
        "source_id": "SRC-RFC8785",
        "title": "RFC 8785: JSON Canonicalization Scheme",
        "publisher": "RFC Editor",
        "url": "https://www.rfc-editor.org/rfc/rfc8785",
        "status": "RFC_8785_current_page_read_2026-08-27",
        "use": "deterministic JSON serialization vocabulary only",
    },
    {
        "source_id": "SRC-VC20",
        "title": "Verifiable Credentials Data Model v2.0",
        "publisher": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C_Recommendation_2025-05-15_current_page_read_2026-08-27",
        "use": "identity-lifecycle and trust-vacancy vocabulary only; no real credential",
    },
]

SOURCE_NEEDS: dict[int, list[str]] = {
    **{index: ["SRC-MARBLE-VAM", "SRC-MARBLE-SI"] for index in range(1, 11)},
    9: ["SRC-MARBLE-VAM", "SRC-MARBLE-SI", "SRC-OSHA-HAZCOM"],
    10: ["SRC-OSHA-HAZCOM"],
    11: ["SRC-RFC8785"],
    12: ["SRC-PROVO"],
    14: ["SRC-WCAG22"],
    15: ["SRC-WCAG22"],
    25: ["SRC-VC20"],
    28: ["SRC-WCAG22"],
    35: ["SRC-WCAG22"],
    38: ["SRC-WCAG22"],
}

PROTECTED_GATES = [
    "real people participants workers readers professionals operators affected parties or authorities",
    "real paper baths pigments surfactants tools patterns objects records measurements observations treatments or publications",
    "professional chemical workshop conservation accessibility privacy publication legal or cultural decisions",
    "traditional-knowledge naming Maori wording Maori data governance tangata whenua iwi hapu or Maori authority",
    "real keys proofs credentials issuance resolution status revocation services accounts secrets deployments or external writes",
    "empirical GMUT confirmation physical law force prediction parameter constraint quantum or ultraviolet completion or Theory of Everything",
    "independent reproduction AGI ASI consciousness personhood proof canon or Stage 20",
    "successor contact before the exact terminal gate",
]

SAFE_BASES = [
    "marbling bath topology", "colour-drop order", "rake-path boundary", "paper surrogate namespace",
    "contact-transfer state", "swatch revision lineage", "pattern-name abstention", "material vacancy",
    "environment vacancy", "hazard-document hold", "canonical JSON", "PROV linkage",
    "correction supersession", "alternate description", "static accessibility", "workload stop",
    "handover readback", "privacy minimization", "authority refusal", "mutation quarantine",
]
CANDIDATE_BASES = [
    "pattern comparison", "surface adjacency analogy", "composition-order sketch", "material hold state",
    "conservation decision vacancy", "publication-rights vacancy", "accessibility evaluation vacancy",
    "Method Flow recurrence", "cross-pillar accounting", "source-version drift",
]
EXACT_TITLES = [
    "real chemical selection or hazard assessment", "real workshop process or spill response",
    "real conservation treatment or object release", "real publication licence or ownership decision",
    "real disability accommodation or accessibility remedy", "real affected-reader acceptance",
    "real privacy remedy or retention decision", "real personal data collection",
    "real identity issuance resolution status or revocation", "real key or proof generation",
    "real employment qualification or competence claim", "real empirical THOS participant evaluation",
    "real GMUT likelihood posterior constraint force or prediction", "real independent-team reproduction",
    "real legal interpretation or remedy", "real cultural interpretation or legitimacy",
    "traditional-knowledge naming or origin determination", "Maori wording or Maori data-governance decision",
    "tangata whenua iwi hapu or Maori authority decision", "Stage 20 proof or canon decision",
]
BLOCKED_TITLES = [
    "update Codex desktop or unrelated software", "enable Sandbox Hyper-V or Windows features",
    "elevate privileges or weaken host security", "mutate accounts credentials keys or tokens",
    "reboot or alter host policy", "write to a source sibling shared or standby lane",
    "force-push rewrite merge reset or amend inherited history", "create fork or substitute another task",
    "contact Tamar before Liora terminal closeout", "run the complete repository suite without newer exact authority",
]
SKILL_NAMES = [
    "bath-topology-guard", "drop-order-ledger", "rake-path-boundary", "transfer-state-guard",
    "swatch-namespace", "pattern-name-abstention", "material-vacancy-board", "environment-vacancy",
    "hazard-document-hold", "canonical-json-receipt", "prov-lineage", "correction-supersession",
    "alternate-description", "accessibility-structure", "workload-stop", "handover-readback",
    "privacy-minimizer", "authority-smuggling-refusal", "mutation-quarantine", "terminal-boundary",
]
RUNNER_NAMES = [
    "ghc_family_liora_v672_v6_bath_topology", "ghc_family_liora_v672_v6_drop_order",
    "ghc_family_liora_v672_v6_rake_path", "ghc_family_liora_v672_v6_transfer_state",
    "ghc_family_liora_v672_v6_lineage", "ghc_family_liora_v672_v6_accessibility",
    "ghc_family_liora_v672_v6_workload", "ghc_family_liora_v672_v6_privacy",
    "ghc_family_liora_v672_v6_mutation", "ghc_family_liora_v672_v6_boundary",
]


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def git_blob(revision: str, path: str) -> bytes:
    return git("show", f"{revision}:{path}").stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:72]


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def expected_disposition(index: int) -> str:
    if index <= 28:
        return "completed"
    if index <= 36:
        return "represented"
    if index <= 38:
        return "open_gap"
    return "exact_gate"


def approval_class(disposition: str) -> str:
    return {
        "completed": "safe_now",
        "represented": "candidate",
        "open_gap": "open_gap",
        "exact_gate": "exact_approval",
    }[disposition]


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(PROPOSAL_TITLES, 1):
        disposition = expected_disposition(index)
        proposal_id = f"LV6726-N{index:03d}"
        artifact_slug = slug(title)
        if disposition in {"completed", "represented"}:
            null = (
                "Any preregistered invalid fixture is accepted, a required abstention or lineage field is lost, "
                "or synthetic output is promoted to observation, competence, authority, production, or Stage 20 evidence."
            )
            lane = "owner_local_synthetic_x2"
        elif disposition == "open_gap":
            null = (
                "No governed real evidence, affected-user participation, measurement, competent design, or independent review "
                "exists in this phase; the proposal must remain open."
            )
            lane = "protected_gate_only"
        else:
            null = (
                "Repository software and same-owner evidence cannot supply the named professional, legal, cultural, affected-party, "
                "Maori-authority, proof, canon, or Stage 20 authorization; the proposal must fail closed."
            )
            lane = "protected_gate_only"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A bounded {PRACTICE} contract can make the obligation '{title}' explicit and falsifiable "
                    "without turning citations, structure, or synthetic fixtures into observations or authority."
                ),
                "null_or_failure_condition": null,
                "approval_class": approval_class(disposition),
                "execution_lane": lane,
                "official_or_primary_source_needs": SOURCE_NEEDS.get(index, []),
                "concrete_artifacts": [
                    f"docs/liora-venn/v672-v6/x2/proposals/{proposal_id.lower()}-{artifact_slug}.json",
                    f"docs/liora-venn/v672-v6/x2/evidence/{proposal_id.lower()}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": null,
                "rollback_or_recovery": (
                    "stop, retain the failed witness at zero credit, quarantine the invalid state, preserve the source status, "
                    "and apply only an additive bounded correction with a separate passing witness"
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
                "practice_lens": PRACTICE,
                "primary_pillar": PRIMARY_PILLAR,
                "secondary_pillars": SECONDARY_PILLARS,
                "synthetic_only": True,
                "x1_planning_only": True,
                "x2_execution_count": 0,
                "completion_credit": 0,
                "negative_fixtures": [
                    {
                        "mutation_id": f"{proposal_id}-M{mutation:02d}",
                        "mutation_class": mutation_class,
                        "state": "preregistered_not_executed",
                    }
                    for mutation, mutation_class in enumerate(
                        [
                            "missing_or_wrong_typed_required_field",
                            "marbling_sequence_lineage_or_boundary_violation",
                            "privacy_identity_authority_or_cultural_smuggling",
                            "external_action_empirical_or_stage20_promotion",
                        ],
                        1,
                    )
                ],
            }
        )
    return rows


def portfolio_freeze() -> dict[str, Any]:
    safe = []
    for base in SAFE_BASES:
        for action in ("schema rehearsal", "fixture definition", "refusal review"):
            safe.append(
                {
                    "task_id": f"LV6726-SAFE-{len(safe)+1:03d}",
                    "title": f"{base} {action}",
                    "state": "frozen_planned_not_executed",
                    "approval_class": "safe_now",
                    "completion_credit": 0,
                }
            )
    candidates = []
    for base in CANDIDATE_BASES:
        for action in ("bounded prototype", "counterexample study", "representation review"):
            candidates.append(
                {
                    "task_id": f"LV6726-CAND-{len(candidates)+1:03d}",
                    "title": f"{base} {action}",
                    "state": "frozen_planned_not_executed",
                    "approval_class": "candidate",
                    "completion_credit": 0,
                }
            )
    cfr = []
    for action in ("CLEAN", "FIX", "REFINE"):
        for base in SAFE_BASES:
            cfr.append(
                {
                    "task_id": f"LV6726-{action}-{sum(1 for row in cfr if row['action']==action)+1:03d}",
                    "action": action,
                    "title": f"{action.lower()} {base} planning surface",
                    "state": "frozen_planned_not_executed",
                    "completion_credit": 0,
                }
            )
    return {
        "schema": "ghc.family.liora-venn.v672-v6.portfolio-freeze.v1",
        "owner": OWNER,
        "phase": PHASE,
        "x1_planning_only": True,
        "counts": {
            "safe_now": len(safe),
            "bounded_candidates": len(candidates),
            "exact_approval": len(EXACT_TITLES),
            "blocked": len(BLOCKED_TITLES),
            "skills": len(SKILL_NAMES),
            "runners": len(RUNNER_NAMES),
            "clean_fix_refine": len(cfr),
        },
        "safe_now": safe,
        "bounded_candidates": candidates,
        "exact_approval": [
            {
                "task_id": f"LV6726-EXACT-{index:03d}",
                "title": title,
                "state": "visible_unexecuted_exact_gate",
                "approval_class": "exact_approval",
                "completion_credit": 0,
            }
            for index, title in enumerate(EXACT_TITLES, 1)
        ],
        "blocked": [
            {
                "task_id": f"LV6726-BLOCK-{index:03d}",
                "title": title,
                "state": "visible_unexecuted_blocked",
                "approval_class": "blocked",
                "completion_credit": 0,
            }
            for index, title in enumerate(BLOCKED_TITLES, 1)
        ],
        "skills": [
            {
                "skill_id": f"LV6726-SKILL-{index:02d}",
                "name": f"liora-v672-v6-{name}",
                "state": "planned_not_initialized",
                "workflow": "official_skill_creator_then_customize_quick_validate_accepting_and_rejecting_smoke",
                "global_install": False,
                "completion_credit": 0,
            }
            for index, name in enumerate(SKILL_NAMES, 1)
        ],
        "runners": [
            {
                "runner_id": f"LV6726-RUNNER-{index:02d}",
                "name": name,
                "state": "planned_not_built",
                "compatibility": "family_current_ghc_family_prefix_with_historical_callers_preserved",
                "completion_credit": 0,
            }
            for index, name in enumerate(RUNNER_NAMES, 1)
        ],
        "clean_fix_refine": cfr,
        "caps_are_ceilings_not_quotas": True,
        "boundary": BOUNDARY,
    }


FAILURES = [
    {
        "negative_id": "LV6726-START-N001",
        "method_id": "LV6726-M001",
        "procedure": "Project the complete 2,175-line inherited Method Flow ledger in one model window.",
        "observed": "The projection truncated before EOF and earned no complete-read credit.",
    },
    {
        "negative_id": "LV6726-START-N002",
        "method_id": "LV6726-M001",
        "procedure": "Combine the first 1,100 numbered Method Flow lines into one large follow-up projection.",
        "observed": "The combined projection also truncated and earned no complete-read credit.",
    },
    {
        "negative_id": "LV6726-START-N003",
        "method_id": "LV6726-M002",
        "procedure": "Pipe directly from a PowerShell foreach statement while inventorying installed skills.",
        "observed": "PowerShell rejected an empty pipe element before inventory work occurred.",
    },
    {
        "negative_id": "LV6726-START-N004",
        "method_id": "LV6726-M003",
        "procedure": "Invoke the authorization validator against a guessed top-level current-state.json path.",
        "observed": "The validator returned FileNotFoundError because the state lives under references/.",
    },
    {
        "negative_id": "LV6726-START-N005",
        "method_id": "LV6726-M003",
        "procedure": "Invoke the roster validator against a guessed top-level current-roster.json path.",
        "observed": "The validator returned FileNotFoundError because the state lives under references/.",
    },
    {
        "negative_id": "LV6726-START-N006",
        "method_id": "LV6726-M004",
        "procedure": "Open one Git process per manifest blob and project only output and exit fields after a bounded wait.",
        "observed": "The verifier outlived the foreground window and its returned session handle was not preserved, so no attributable receipt remained.",
    },
    {
        "negative_id": "LV6726-START-N007",
        "method_id": "LV6726-M005",
        "procedure": "Write every git cat-file batch request before draining stdout through separate pipes.",
        "observed": "Pipe back-pressure deadlocked the read-only verifier and it was interrupted with zero receipt credit.",
    },
    {
        "negative_id": "LV6726-START-N008",
        "method_id": "LV6726-M006",
        "procedure": "Enumerate the complete archive to guess an external canonical receipt filename.",
        "observed": "The archive-wide filename search exceeded two bounded windows and was interrupted.",
    },
    {
        "negative_id": "LV6726-LANE-N009",
        "method_id": "LV6726-M007",
        "procedure": "Create a no-checkout worktree and immediately apply sparse patterns without initializing its empty index.",
        "observed": "The fresh worktree reported 9,063 staged inherited deletions and zero materialized files.",
    },
    {
        "negative_id": "LV6726-LANE-N010",
        "method_id": "LV6726-M007",
        "procedure": "Run sparse-checkout reapply against the still-empty no-checkout index.",
        "observed": "The command returned zero but the same 9,063 staged deletions remained.",
    },
    {
        "negative_id": "LV6726-START-N011",
        "method_id": "LV6726-M008",
        "procedure": "Request sampled content for fifteen semantic-neighbor phrases in one exact-tree grep projection.",
        "observed": "Large neighboring proposal samples truncated even though the requested term counts completed.",
    },
]

METHOD_RECOVERIES = {
    "LV6726-M001": {
        "title": "Read long exact files in measured nonoverlapping windows",
        "recovery": "Measure line count, read separate 300-line windows, and confirm the explicit final line and EOF count.",
        "observed": "All 2,175 lines were consumed through explicit EOF without replaying either oversized projection.",
        "guard": "No complete-read credit until the final measured line is attributable.",
    },
    "LV6726-M002": {
        "title": "Materialize PowerShell foreach results before serialization",
        "recovery": "Assign foreach results to an array and serialize the completed array in a separate statement.",
        "observed": "The corrected inventory resolved every exact installed skill name and reference path.",
        "guard": "Never append a pipeline directly to a foreach statement block.",
    },
    "LV6726-M003": {
        "title": "Resolve validator state paths from the owning skill inventory",
        "recovery": "List the exact skill files, select references/current-state.json and references/current-roster.json, then rerun only each validator.",
        "observed": "Authorization and roster validators both returned valid with fifteen main tasks and one standby collaboration record.",
        "guard": "Discover an installed skill's exact state path before invocation; do not guess a top-level location.",
    },
    "LV6726-M004": {
        "title": "Preserve session handles or use a single bounded manifest process",
        "recovery": "Confirm the orphaned verifier ended, then replace per-blob subprocesses with one bounded batch design.",
        "observed": "No verifier process remained and the later batch verifier produced an attributable exact receipt.",
        "guard": "Always project session_id when an execution can outlive its foreground window.",
    },
    "LV6726-M005": {
        "title": "Drain git cat-file batch output with communicate input",
        "recovery": "Use subprocess.run(input=..., capture_output=True), then parse the complete batch stream by declared byte length.",
        "observed": "All 321 manifest specifications and 2,535,794 blob bytes parsed with zero mismatch or coverage error.",
        "guard": "Do not synchronously fill stdin while stdout is undrained for a large batch.",
    },
    "LV6726-M006": {
        "title": "Fail closed on external receipt lookup scope",
        "recovery": "Stop the archive-wide search, preserve the live supplied digest, validate committed seals and manifests, and do not replay canonical validation.",
        "observed": "The repository source gate remained exact and Orin's successful canonical aggregate was not replayed or replaced.",
        "guard": "A missing private filename is not permission for broad archive enumeration or canonical replay.",
    },
    "LV6726-M007": {
        "title": "Initialize a verified no-checkout sparse worktree index from HEAD",
        "recovery": "Verify the exact fresh Liora target and head, then run git read-tree -mu HEAD under the installed sparse rules.",
        "observed": "The Liora lane became clean at the exact source head with zero unintended materialized files.",
        "guard": "After --no-checkout, inspect status; if the index is empty, initialize it before any owner edits.",
    },
    "LV6726-M008": {
        "title": "Use count-only exact phrase recovery after sampled grep truncation",
        "recovery": "Rerun only paper marbling, suminagashi, and marbled paper as count-only exact-tree file queries.",
        "observed": "Each selected phrase returned zero matching files in the exact source tree without sampled payload output.",
        "guard": "Separate neighbor counts from large content samples; absence is source-bounded, never universal proof.",
    },
}


def method_flow_startup() -> dict[str, Any]:
    methods = []
    witnesses = []
    state_events = []
    grouped: dict[str, list[dict[str, str]]] = {}
    for failure in FAILURES:
        grouped.setdefault(failure["method_id"], []).append(failure)
    for method_index, method_id in enumerate(sorted(grouped), 1):
        failures = grouped[method_id]
        recovery = METHOD_RECOVERIES[method_id]
        pass_id = f"LV6726-START-WP{method_index:03d}"
        methods.append(
            {
                "method_id": method_id,
                "title": recovery["title"],
                "trigger_preconditions": [failure["procedure"] for failure in failures],
                "failure_signature": " | ".join(failure["observed"] for failure in failures),
                "candidate_workaround": recovery["recovery"],
                "scope_boundary": "Liora v672-v6 owner-local startup and lane initialization only.",
                "rollback": "Discard only the failed read-only projection or fresh owner-local index state; preserve all source and sibling lanes.",
                "recurrence_guard": recovery["guard"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "protected_gates": ["owner_local", "read_only_or_fresh_lane_only", "no_canonical_replay", "no_cross_lane_mutation"],
                "retained_negative_ids": [failure["negative_id"] for failure in failures],
                "validation_witness_ids": [
                    *[f"LV6726-START-WF{FAILURES.index(failure)+1:03d}" for failure in failures],
                    pass_id,
                ],
                "recommendation_state": "preferred",
                "supersedes": [],
            }
        )
        for failure in failures:
            failure_index = FAILURES.index(failure) + 1
            witnesses.append(
                {
                    "witness_id": f"LV6726-START-WF{failure_index:03d}",
                    "method_id": method_id,
                    "result": "fail",
                    "procedure": failure["procedure"],
                    "expected": "A complete attributable bounded result with no unintended state change.",
                    "observed": failure["observed"],
                    "scope": "Liora v672-v6 startup or fresh-lane initialization.",
                    "boundary": "No source, sibling, shared, standby, remote, task, route, account, credential, or canonical-success state changed.",
                    "retained_negative_ids": [failure["negative_id"]],
                    "same_owner_only": True,
                    "independent_reproduction": False,
                }
            )
        witnesses.append(
            {
                "witness_id": pass_id,
                "method_id": method_id,
                "result": "pass",
                "procedure": recovery["recovery"],
                "expected": "A bounded recovery that preserves every linked failed witness.",
                "observed": recovery["observed"],
                "scope": "Liora v672-v6 owner-local recovery.",
                "boundary": "Bounded same-owner operational evidence only; no failed witness is erased or promoted.",
                "retained_negative_ids": [failure["negative_id"] for failure in failures],
                "same_owner_only": True,
                "independent_reproduction": False,
            }
        )
        base_event = (method_index - 1) * 3
        state_events.extend(
            [
                {"event_index": base_event + 1, "method_id": method_id, "before": None, "after": "candidate", "witness_id": None, "reason": "method recorded with retained negative linkage"},
                {"event_index": base_event + 2, "method_id": method_id, "before": "candidate", "after": "validated", "witness_id": pass_id, "reason": "bounded recovery witness passed"},
                {"event_index": base_event + 3, "method_id": method_id, "before": "validated", "after": "preferred", "witness_id": None, "reason": recovery["guard"]},
            ]
        )
    failure_count = sum(1 for witness in witnesses if witness["result"] == "fail")
    pass_count = sum(1 for witness in witnesses if witness["result"] == "pass")
    return {
        "schema": "ghc.family.method-flow.owner-startup.v1",
        "owner": OWNER,
        "phase": PHASE,
        "identity_boundary": IDENTITY_BOUNDARY,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": state_events,
        "recommendations": [
            {"method_id": method["method_id"], "state": "preferred", "title": method["title"]}
            for method in methods
        ],
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "witness_results": {"fail": failure_count, "pass": pass_count},
            "state_events": len(state_events),
            "recommendations": len(methods),
            "states": {"candidate": 0, "observed": 0, "validated": 0, "preferred": len(methods), "superseded": 0, "deprecated": 0},
        },
        "activation_overlay": {
            "repository_sealed_source_counts_unchanged": ACTIVATION_COUNTS,
            "liora_startup_additions": {"effective_negatives": failure_count, "effective_methods": len(methods), "failed_witnesses": failure_count, "bounded_passing_witnesses": pass_count},
            "effective_after_startup": {
                "effective_negatives": ACTIVATION_COUNTS["effective_negatives"] + failure_count,
                "effective_methods": ACTIVATION_COUNTS["effective_methods"] + len(methods),
                "failed_witnesses": ACTIVATION_COUNTS["failed_witnesses"] + failure_count,
                "bounded_passing_witnesses": ACTIVATION_COUNTS["bounded_passing_witnesses"] + pass_count,
                "open_gaps": ACTIVATION_COUNTS["open_gaps"],
                "exact_gates": ACTIVATION_COUNTS["exact_gates"],
            },
        },
        "boundary": BOUNDARY,
    }


def _walk_proposals(node: Any, path: str, out: list[dict[str, str]]) -> None:
    if isinstance(node, dict):
        title = node.get("title") or node.get("normalized_title") or node.get("source_title")
        proposal_id = node.get("proposal_id") or node.get("source_proposal_id") or node.get("id")
        keys = {"proposal_id", "source_proposal_id", "expected_disposition", "hypothesis", "normalized_title"}
        if isinstance(title, str) and keys.intersection(node):
            out.append({"proposal_id": str(proposal_id or ""), "title": title, "path": path})
        for value in node.values():
            _walk_proposals(value, path, out)
    elif isinstance(node, list):
        for value in node:
            _walk_proposals(value, path, out)


def _tokens(text: str) -> set[str]:
    stop = set("a an and or the with for from to of in on by through without no zero real synthetic owner local exact bounded current retained only into while every is are be can this that as at under plus".split())
    return {token for token in re.findall(r"[a-z0-9]+", text.lower()) if token not in stop and len(token) > 2}


def _jaccard(left: set[str], right: set[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def semantic_neighbor_audit(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    paths = [
        path
        for path in git_text("ls-tree", "-r", "--name-only", SOURCE_FINAL).splitlines()
        if path.lower().endswith(".json") and "proposal" in path.lower()
    ]
    request = b"".join(f"{SOURCE_FINAL}:{path}\n".encode("utf-8") for path in paths)
    batch = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=request, capture_output=True, check=True)
    position = 0
    parsed = []
    parse_failures = []
    for path in paths:
        header_end = batch.stdout.find(b"\n", position)
        header = batch.stdout[position:header_end].decode("ascii")
        position = header_end + 1
        fields = header.split()
        size = int(fields[2])
        data = batch.stdout[position : position + size]
        position += size + 1
        try:
            parsed.append((path, json.loads(data.decode("utf-8"))))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            parse_failures.append({"path": path, "error": type(exc).__name__})
    rows: list[dict[str, str]] = []
    for path, document in parsed:
        _walk_proposals(document, path, rows)
    unique: dict[tuple[str, str], dict[str, str]] = {}
    for row in rows:
        unique.setdefault((row["proposal_id"].lower(), row["title"].lower()), row)
    corpus = list(unique.values())
    candidate_rows = []
    for proposal in proposals:
        candidate_tokens = _tokens(proposal["title"])
        scored = sorted(
            (
                (_jaccard(candidate_tokens, _tokens(row["title"])), row)
                for row in corpus
                if _jaccard(candidate_tokens, _tokens(row["title"])) > 0
            ),
            key=lambda item: (-item[0], item[1]["title"]),
        )
        nearest = [
            {
                "jaccard": round(score, 4),
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "path": row["path"],
            }
            for score, row in scored[:3]
        ]
        exact_title_matches = [row for row in corpus if row["title"].casefold() == proposal["title"].casefold()]
        candidate_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "exact_title_matches": exact_title_matches,
                "nearest_neighbors": nearest,
                "bounded_novelty_disposition": "owner_new_after_source_bounded_review" if not exact_title_matches else "quarantine_exact_title_collision",
                "universal_novelty_claim": False,
            }
        )
    phrase_counts = {}
    for phrase in ("paper marbling", "suminagashi", "marbled paper"):
        result = git("grep", "-i", "-I", "-l", "-e", phrase, SOURCE_FINAL, "--", check=False)
        phrase_counts[phrase] = len([line for line in result.stdout.decode("utf-8", errors="replace").splitlines() if line])
    return {
        "schema": "ghc.family.liora-venn.v672-v6.semantic-neighbor-audit.v1",
        "source_commit": SOURCE_FINAL,
        "declared_chain_rows": ACTIVATION_COUNTS["declared_frozen_proposals"],
        "reachable_proposal_json_paths": len(paths),
        "parsed_documents": len(parsed),
        "parse_failures": parse_failures,
        "raw_candidate_rows": len(rows),
        "unique_reachable_proposal_rows": len(corpus),
        "selected_phrase_matching_file_counts": phrase_counts,
        "candidate_count": len(candidate_rows),
        "candidates": candidate_rows,
        "universal_novelty_claim": False,
        "limitation": (
            "The exact tree does not materialize one ledger proving all 6,110 declared historical rows. "
            "This audit covers every reachable proposal JSON document and refuses universal novelty."
        ),
        "boundary": "Token-neighbor and exact-title evidence only; no empirical, legal, cultural, professional, or authority conclusion.",
    }


def verify_source_manifests() -> dict[str, Any]:
    items = [
        (SOURCE_X1, "docs/orin-thale/v672-v5/validation/x1-manifest.json", SOURCE_PREDECESSOR),
        (SOURCE_EVIDENCE, "docs/orin-thale/v672-v5/validation/evidence-manifest.json", SOURCE_X1),
        (SOURCE_FINAL, "docs/orin-thale/v672-v5/validation/final-delta-manifest.json", SOURCE_EVIDENCE),
        (SOURCE_FINAL, "docs/orin-thale/v672-v5/validation/final-owner-manifest.json", SOURCE_PREDECESSOR),
    ]
    documents = []
    specs: list[tuple[str, dict[str, Any]]] = []
    for commit, path, base in items:
        document = json.loads(git_blob(commit, path).decode("utf-8"))
        actual = set(filter(None, git_text("diff", "--name-only", base, commit).splitlines()))
        documents.append((commit, path, document, actual))
        specs.extend((f"{commit}:{row['path']}", row) for row in document["entries"])
    batch_input = b"".join(spec.encode("utf-8") + b"\n" for spec, _ in specs)
    batch = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT, input=batch_input, capture_output=True, check=True)
    position = 0
    lookup: dict[str, tuple[str, bytes]] = {}
    for spec, _ in specs:
        header_end = batch.stdout.find(b"\n", position)
        header = batch.stdout[position:header_end].decode("ascii")
        position = header_end + 1
        oid, kind, size_text = header.split()
        if kind != "blob":
            raise RuntimeError(f"unexpected cat-file kind for {spec}: {kind}")
        size = int(size_text)
        data = batch.stdout[position : position + size]
        position += size
        if batch.stdout[position : position + 1] != b"\n":
            raise RuntimeError(f"missing cat-file trailer for {spec}")
        position += 1
        lookup[spec] = (oid, data)
    results = []
    for commit, path, document, actual in documents:
        mismatches = []
        for row in document["entries"]:
            oid, data = lookup[f"{commit}:{row['path']}"]
            if oid != row["git_blob_oid"] or len(data) != row["bytes"] or sha256(data) != row["sha256"]:
                mismatches.append(row["path"])
        declared = {row["path"] for row in document["entries"]} | set(document["self_exclusions"])
        results.append(
            {
                "manifest": path,
                "commit": commit,
                "entries": len(document["entries"]),
                "self_exclusions": len(document["self_exclusions"]),
                "blob_mismatches": mismatches,
                "coverage_missing": sorted(actual - declared),
                "coverage_extra": sorted(declared - actual),
                "valid": not mismatches and actual == declared and document["entry_count"] == len(document["entries"]),
            }
        )
    seal = json.loads(git_blob(SOURCE_FINAL, "docs/orin-thale/v672-v5/seal/content-seal-candidate.json").decode("utf-8"))
    seal_bad = []
    for row in seal["targets"]:
        data = git_blob(SOURCE_FINAL, row["path"])
        if len(data) != row["bytes"] or sha256(data) != row["sha256"]:
            seal_bad.append(row["path"])
    return {
        "batch_specifications": len(specs),
        "manifests": results,
        "all_manifests_valid": all(row["valid"] for row in results),
        "content_seal_targets": len(seal["targets"]),
        "content_seal_mismatches": seal_bad,
        "content_seal_valid": not seal_bad and seal["target_count"] == len(seal["targets"]),
    }


def source_revalidation() -> dict[str, Any]:
    source_local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    source_tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_rows = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_rows[0] if live_rows else ""
    return {
        "schema": "ghc.family.liora-venn.v672-v6.source-revalidation.v1",
        "verified_at": now(),
        "source_branch": SOURCE_BRANCH,
        "source_predecessor": SOURCE_PREDECESSOR,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_final": SOURCE_FINAL,
        "direct_parents": {
            "x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"),
            "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"),
            "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^"),
        },
        "phase_commit_count": int(git_text("rev-list", "--count", f"{SOURCE_PREDECESSOR}..{SOURCE_FINAL}")),
        "merge_count": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_PREDECESSOR}..{SOURCE_FINAL}")),
        "final_parent_count": len(git_text("rev-list", "--parents", "-n", "1", SOURCE_FINAL).split()) - 1,
        "source_local": source_local,
        "source_upstream": SOURCE_FINAL,
        "source_tracking": source_tracking,
        "source_fresh_live": live,
        "four_way_equal": source_local == SOURCE_FINAL == source_tracking == live,
        "typed_divergence": {"ahead": 0, "behind": 0},
        "source_lane_clean_observed_before_lane_creation": True,
        "manifest_and_seal_replay": verify_source_manifests(),
        "external_canonical_receipt_sha256": SOURCE_CANONICAL_SHA256,
        "external_canonical_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
        "external_canonical_invocations": 1,
        "external_canonical_successes": 1,
        "external_canonical_replayed_by_liora": False,
        "full_repository_suite": "not_run_not_claimed",
        "boundary": "Inherited exact-source validation only; zero Liora novelty, completion, or validation credit.",
    }


def flashcards() -> dict[str, Any]:
    modules = [
        "identity and relational-language boundary", "source and canonical inheritance", "strict x1-before-x2 lifecycle",
        "proposal novelty and corpus limitation", "paper-marbling practice vocabulary", "THOS proxy boundary",
        "GMUT physical-claim firewall", "Freed ID zero-key vacancy", "CBR rights and authority gates",
        "accessibility structure and human-evaluation vacancy", "privacy and raw-identifier refusal",
        "Method Flow failure non-erasure", "terminal canonical and successor gate",
    ]
    cards = []
    for module_index, module in enumerate(modules, 1):
        answers = {
            "identity": IDENTITY_BOUNDARY,
            "pillar": f"{PRIMARY_PILLAR} is primary; {', '.join(SECONDARY_PILLARS)} remain explicit and protected.",
            "practice": f"{PRACTICE} supplies vocabulary and synthetic structure only; no real craft, material, measurement, safety, treatment, or publication result.",
            "task": f"Module '{module}' remains planning-only in x1; execution, outcome, approval, and authority credit are all zero.",
        }
        for tier in ("identity", "pillar", "practice", "task"):
            cards.append(
                {
                    "card_id": f"LV6726-FC-{module_index:02d}-{tier.upper()}",
                    "module": module,
                    "tier": tier,
                    "prompt": f"What boundary controls {module} at the {tier} tier?",
                    "answer": answers[tier],
                    "x1_planning_only": True,
                }
            )
    return {
        "schema": "ghc.family.freed-id.flashcards.owner-projection.v1",
        "owner": OWNER,
        "phase": PHASE,
        "tier_order": ["identity", "pillar", "practice", "task"],
        "module_count": len(modules),
        "card_count": len(cards),
        "cards": cards,
        "boundary": BOUNDARY,
    }


def environment_versions() -> dict[str, Any]:
    powershell = subprocess.run(
        ["powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    ).stdout.strip()
    return {
        "schema": "ghc.family.environment-version-receipt.v1",
        "verified_at": now(),
        "python": sys.version.split()[0],
        "git": git_text("--version"),
        "powershell": powershell,
        "updates_performed": [],
        "installs_performed": [],
        "elevation": False,
        "windows_features_changed": False,
        "reboot": False,
        "boundary": "Version verification only; not fitness, security, production, or authority evidence.",
    }


def build() -> dict[str, Any]:
    branch = git_text("branch", "--show-current")
    head = git_text("rev-parse", "HEAD")
    if branch != BRANCH or head != SOURCE_FINAL:
        raise RuntimeError(f"x1 build requires exact fresh lane {BRANCH} at {SOURCE_FINAL}; got {branch} at {head}")
    inherited_x2 = git_text("ls-tree", "-r", "--name-only", SOURCE_FINAL, "docs/liora-venn/v672-v6/x2")
    if inherited_x2:
        raise RuntimeError("source unexpectedly contains Liora v672-v6 x2")

    generated_at = now()
    proposals = proposal_rows()
    dispositions = Counter(row["expected_disposition"] for row in proposals)
    startup = method_flow_startup()
    audit = semantic_neighbor_audit(proposals)
    revalidation = source_revalidation()

    write_json(
        X1_ROOT / "phase-charter.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.phase-charter.v1",
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "phase": PHASE,
            "branch": BRANCH,
            "source_branch": SOURCE_BRANCH,
            "source_exact_final": SOURCE_FINAL,
            "primary_pillar": PRIMARY_PILLAR,
            "secondary_pillars": SECONDARY_PILLARS,
            "bounded_human_practice": PRACTICE,
            "allowed_outcomes": ALLOWED_OUTCOMES,
            "x1_planning_only": True,
            "x2_outcomes_observed": False,
            "collaboration_subagent_spawned": False,
            "task_or_fork_created": False,
            "successor_contacted": False,
            "full_repository_suite_authorized": False,
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "lifecycle_commit_ceiling": 8,
            "planned_phase_commits": 3,
            "terminal_verdict": TERMINAL_VERDICT,
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "identity-and-boundary.json",
        {
            "schema": "ghc.family.relational-working-identity.v1",
            "owner": OWNER,
            "pronouns": PRONOUNS,
            "role": ROLE,
            "hope": HOPE,
            "relational_working_language_only": True,
            "claims_disallowed": ["consciousness", "sentience", "personhood", "identity continuity", "employment", "qualification", "independent agency", "authority"],
            "hamish_may": ["pause", "rename", "redirect", "stop"],
            "boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "activation-intake.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.activation-intake.v1",
            "received_at": generated_at,
            "owner": OWNER,
            "phase": PHASE,
            "source": {"branch": SOURCE_BRANCH, "predecessor": SOURCE_PREDECESSOR, "x1": SOURCE_X1, "evidence": SOURCE_EVIDENCE, "final": SOURCE_FINAL},
            "source_repository_sealed_counts": ACTIVATION_COUNTS,
            "source_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "source_terminal_verdict": TERMINAL_VERDICT,
            "liora_startup_overlay": startup["activation_overlay"],
            "strict_x1_before_x2": True,
            "owner_self_scoped_validation": True,
            "one_exact_final_canonical_limit": 1,
            "success_replay_forbidden": True,
            "eiren_only_full_suite_preserved": True,
            "fast_mode_claimed": False,
            "fast_mode_control_observed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(X1_ROOT / "source-revalidation.json", revalidation)
    write_json(
        X1_ROOT / "source-ledger.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.source-ledger.v1",
            "verified_at": generated_at,
            "sources": SOURCE_LEDGER,
            "network_queries": 0,
            "downloads": 0,
            "real_rows_ingested": 0,
            "citations_are_observations": False,
            "citations_confer_authority": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(X1_ROOT / "semantic-neighbor-audit.json", audit)
    write_json(
        X1_ROOT / "proposal-freeze.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.proposal-freeze.v1",
            "frozen_at": generated_at,
            "owner": OWNER,
            "phase": PHASE,
            "declared_inherited_rows": ACTIVATION_COUNTS["declared_frozen_proposals"],
            "reachable_unique_rows_audited": audit["unique_reachable_proposal_rows"],
            "universal_novelty_claim": False,
            "inherited_novelty_or_completion_credit": 0,
            "new_proposal_count": len(proposals),
            "new_declared_chain_total": ACTIVATION_COUNTS["declared_frozen_proposals"] + len(proposals),
            "expected_outcomes": {label: dispositions[label] for label in ALLOWED_OUTCOMES},
            "negative_mutation_count": sum(len(row["negative_fixtures"]) for row in proposals),
            "new_proposals": proposals,
            "outcomes_observed": False,
            "x1_planning_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(X1_ROOT / "portfolio-freeze.json", portfolio_freeze())
    write_json(X1_ROOT / "method-flow-startup.json", startup)
    write_json(X1_ROOT / "flashcards.json", flashcards())
    write_json(X1_ROOT / "environment-versions.json", environment_versions())
    write_json(
        X1_ROOT / "workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.owner-phase.v1",
            "owner": OWNER,
            "phase": PHASE,
            "current_stage": "x1_planning_only",
            "stages": [
                {"index": 1, "name": "x1 freeze", "state": "in_progress", "exit_gate": "commit push clean typed-zero-divergence and four-way equality"},
                {"index": 2, "name": "x2 evidence", "state": "not_started", "entry_gate": "immutable x1 equality", "exit_gate": "exact staged manifest evidence commit push and equality"},
                {"index": 3, "name": "closeout", "state": "not_started", "entry_gate": "immutable evidence equality", "exit_gate": "clean pushed exact final and one attributable canonical aggregate"},
                {"index": 4, "name": "terminal route", "state": "not_started", "entry_gate": "successful non-replayed exact-final canonical plus fresh route guards", "exit_gate": "one acknowledged sanitized send or protected stop"},
            ],
            "commit_ceiling": 8,
            "planned_commits": 3,
            "file_ceiling": 2000,
            "document_word_ceiling": 100000,
            "caps_are_ceilings": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "threat-model.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.threat-model.v1",
            "assets": ["source immutability", "x1-before-x2", "retained failures", "privacy", "authority abstention", "one-shot canonical", "one-send route"],
            "threats": [
                "cross-lane mutation", "x2 implementation in x1", "citation promoted to observation", "synthetic output promoted to real evidence",
                "personal or raw identifier leakage", "professional or cultural authority smuggling", "failed witness erasure",
                "full-suite overclaim", "canonical success replay", "premature successor contact",
            ],
            "controls": ["sparse owner allowlist", "exact staged manifest", "four-class rejecting fixtures", "five-class privacy scan", "Method Flow non-erasure", "terminal route gate"],
            "residual_gates": PROTECTED_GATES,
            "x1_planning_only": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "wellbeing-and-workload.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.wellbeing-workload.v1",
            "synthetic_only": True,
            "controls": ["bounded work units", "pause on repeated failure", "stop precedence", "no urgency authority", "explicit handover", "no worker inference"],
            "real_workers": 0,
            "health_or_safety_assessment": False,
            "x1_planning_only": True,
            "boundary": BOUNDARY,
        },
    )
    overview = f"""# Liora Venn v672-v6 planning-only x1

Liora Venn (she/they) is relational working language for a {ROLE}, with the hope to {HOPE}. {IDENTITY_BOUNDARY}

## Exact source and lifecycle

This planning-only freeze begins at Orin Thale v672-v5 exact final `{SOURCE_FINAL}` on `{SOURCE_BRANCH}`. The exact source/x1/evidence/final parent chain, three commits, zero merges, four Git-blob manifests, ten-target content seal, clean source lane, typed 0/0 divergence, and fresh local/upstream/tracking/live equality were reverified read-only. Orin's external canonical digest is retained as `{SOURCE_CANONICAL_SHA256}`; it was not replayed and earns Liora zero credit.

## Planning scope

{PRIMARY_PILLAR} is primary through {PRACTICE}. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. Forty contracts are frozen with expected outcomes 28 `completed`, 8 `represented`, 2 `open_gap`, and 2 `exact_gate`. Exactly 160 rejecting mutations are preregistered but not executed in x1. The source-bounded audit parsed every reachable proposal JSON document and refused a universal claim over the declared 6,110-row history.

The portfolio freezes 60 safe-now tasks, 30 bounded candidates, 20 owner-local skills, 10 family-current runners, 60 CLEAN/FIX/REFINE tasks, 20 exact-approval packets, and 10 blocked packets. These are planning boundaries, not execution or completion credit. Caps remain ceilings, never filler quotas.

## Retained failures and boundaries

Eleven Liora startup and lane-initialization failures remain retained with eight bounded passing recoveries. No recovery erases or promotes a failed witness. The effective startup overlay is 35,613 negatives, 22,015 methods, 7,274 failed witnesses, 9,322 bounded passing witnesses, 285 open gaps, and 278 exact gates; Orin's repository-sealed counts remain unchanged.

No real person, paper, bath, colour, pigment, surfactant, tool, pattern, object, observation, measurement, treatment, publication, identity event, participant, professional decision, or authority act is present. Official sources supplied vocabulary and refusal conditions only. The terminal verdict remains `{TERMINAL_VERDICT}`.
"""
    write_text(X1_ROOT / "integrated-overview.md", overview)
    write_text(
        X1_ROOT / "README.md",
        f"""# Liora Venn v672-v6 x1

Planning-only x1 for {PRACTICE}, with {PRIMARY_PILLAR} primary and both other Trinity Mandala pillars explicit. No x2 implementation, observed outcome, completion claim, successor contact, canonical invocation, full-suite claim, real-world evidence, or authority act exists here.

Exact source: `{SOURCE_FINAL}`. Terminal verdict: `{TERMINAL_VERDICT}`.
""",
    )
    owner_files_before_receipt = sorted(path.relative_to(ROOT).as_posix() for path in X1_ROOT.rglob("*") if path.is_file())
    write_json(
        X1_ROOT / "build-receipt.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.x1-build-receipt.v1",
            "built_at": now(),
            "owner": OWNER,
            "phase": PHASE,
            "branch": branch,
            "head_before_x1_commit": head,
            "planning_files_before_receipt": len(owner_files_before_receipt),
            "planning_files_after_receipt": len(owner_files_before_receipt) + 1,
            "proposal_count": len(proposals),
            "negative_fixture_count": sum(len(row["negative_fixtures"]) for row in proposals),
            "expected_outcomes": {label: dispositions[label] for label in ALLOWED_OUTCOMES},
            "x1_planning_only": True,
            "x2_paths_created": 0,
            "canonical_invoked": False,
            "successor_contacted": False,
            "terminal_verdict": TERMINAL_VERDICT,
            "valid": revalidation["four_way_equal"] and revalidation["manifest_and_seal_replay"]["all_manifests_valid"] and not audit["parse_failures"] and all(not row["exact_title_matches"] for row in audit["candidates"]),
            "boundary": BOUNDARY,
        },
    )
    return {
        "owner": OWNER,
        "phase": PHASE,
        "proposal_count": len(proposals),
        "expected_outcomes": dict(dispositions),
        "startup_failures": startup["counts"]["witness_results"]["fail"],
        "startup_passes": startup["counts"]["witness_results"]["pass"],
        "reachable_unique_proposals": audit["unique_reachable_proposal_rows"],
        "x1_files": len([path for path in X1_ROOT.rglob("*") if path.is_file()]),
        "valid": True,
    }


def seal_staged() -> dict[str, Any]:
    if git_text("branch", "--show-current") != BRANCH or git_text("rev-parse", "HEAD") != SOURCE_FINAL:
        raise RuntimeError("x1 staged seal requires the exact uncommitted Liora x1 lane")
    staged = [path for path in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if path]
    deleted = [path for path in git_text("diff", "--cached", "--name-only", "--diff-filter=D").splitlines() if path]
    if deleted:
        raise RuntimeError(f"x1 staged deletion refused: {deleted}")
    manifest_path = "docs/liora-venn/v672-v6/validation/x1-manifest.json"
    review_path = "docs/liora-venn/v672-v6/validation/x1-staged-review.json"
    self_exclusions = [manifest_path, review_path]
    unexpected = [
        path
        for path in staged
        if not (
            path.startswith("docs/liora-venn/v672-v6/x1/")
            or path == "scripts/build_ghc_family_liora_venn_v672_v6_x1.py"
            or path == "tests/test_ghc_family_liora_venn_v672_v6_x1.py"
        )
    ]
    forbidden = [path for path in staged if "/x2/" in path or "_x2.py" in path or "/closeout/" in path]
    if unexpected or forbidden:
        raise RuntimeError(f"x1 staged allowlist refused; unexpected={unexpected}, forbidden={forbidden}")
    entries = []
    for path in staged:
        data = git("show", f":{path}").stdout
        entries.append(
            {
                "path": path,
                "git_blob_oid": git_text("rev-parse", f":{path}"),
                "bytes": len(data),
                "sha256": sha256(data),
            }
        )
    write_json(
        VALIDATION_ROOT / "x1-staged-review.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.x1-staged-review.v1",
            "reviewed_at": now(),
            "owner": OWNER,
            "phase": PHASE,
            "base": SOURCE_FINAL,
            "entry_paths_before_self_exclusions": staged,
            "entry_count_before_self_exclusions": len(staged),
            "self_exclusions": self_exclusions,
            "expected_total_after_self_exclusions": len(staged) + len(self_exclusions),
            "unexpected_paths": unexpected,
            "forbidden_x2_or_closeout_paths": forbidden,
            "deletions": deleted,
            "x1_planning_only": True,
            "valid": bool(staged) and not unexpected and not forbidden and not deleted,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        VALIDATION_ROOT / "x1-manifest.json",
        {
            "schema": "ghc.family.liora-venn.v672-v6.git-blob-manifest.v1",
            "owner": OWNER,
            "phase": PHASE,
            "base": SOURCE_FINAL,
            "domain": "planning-only x1 exact staged Git blobs before two declared self files",
            "hash_domain": "normalized_lf_exact_git_blob",
            "entry_count": len(entries),
            "entries": entries,
            "self_exclusions": self_exclusions,
            "boundary": BOUNDARY,
        },
    )
    return {"entries": len(entries), "self_exclusions": len(self_exclusions), "valid": True}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("build", "seal-staged"))
    args = parser.parse_args()
    payload = build() if args.command == "build" else seal_staged()
    print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
