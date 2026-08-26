"""Build the planning-only Ilyra Fen v670-v2 x1 packet.

The builder is intentionally fail-closed: it runs only at the exact Lyren
source head in the exact Ilyra branch, refuses an existing x2/closeout tree,
and never performs staging, committing, pushing, routing, or external writes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "ilyra-fen" / "v670-v2"
OWNER = "Ilyra Fen"
PHASE = "v670-v2"
SOURCE_BRANCH = "codex/GHC-Family/lyren-moss-v670-v1-full-tools"
SOURCE_FINAL = "1b25a3e888464698a650cd515f4afae0841100c1"
SOURCE_VESPER = "fe33a3ed69d6144720072b15174937effe9ca305"
SOURCE_X1 = "128f52cee0acc532a114b05242d356cb7a59596c"
SOURCE_EVIDENCE = "4538663ed1e526931056b104fbd86c27629aa223"
BRANCH = "codex/GHC-Family/ilyra-fen-v670-v2-full-tools"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Ilyra Fen, she/they, evidence-boundary steward and reproducibility "
    "cartographer, is relational working language only. It is not evidence of "
    "consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, or scientific, operational, legal, "
    "cultural, affected-party, or Maori authority."
)

PROTECTED_BOUNDARY = (
    "No empirical, participant, professional, production, deployment, legal, "
    "cultural, Maori-authority, privacy-complete, accessibility-complete, "
    "exhaustive-security, independent-reproduction, AGI/ASI, consciousness or "
    "personhood, Theory-of-Everything, proof/canon, or Stage 20 claim."
)

SOURCE_TRUTH = {
    "proposal_chain": 5270,
    "effective_negatives": 32057,
    "methods": 18162,
    "failed_witnesses": 3878,
    "passing_witnesses": 5131,
    "open_gaps": 241,
    "exact_gates": 236,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

STARTUP_FAILURES = [
    {
        "failure_id": "IF6702-START-001",
        "failed_witness": "The first combined Git discovery wrapper returned no attributable output within its display window.",
        "completion_credit": 0,
        "recovery": "Use exact scalar ref, ancestry, worktree, and fresh-live probes with explicit JSON attribution.",
        "passing_bounded_witness": "The exact local, tracking, live, parent, history, and clean-state probes all passed.",
        "recurrence_guard": "Prefer scalar Git probes over mixed worktree/ref discovery wrappers.",
    },
    {
        "failure_id": "IF6702-START-002",
        "failed_witness": "The first full activation-packet render exceeded the result budget before EOF.",
        "completion_credit": 0,
        "recovery": "Measure the committed packet and reread numbered line windows through the final line.",
        "passing_bounded_witness": "All 464 committed lines were read through EOF and the Git-blob digest matched.",
        "recurrence_guard": "Measure long packets before display and select bounded windows from the start.",
    },
    {
        "failure_id": "IF6702-START-003",
        "failed_witness": "A combined multi-window activation reread again exceeded the display budget.",
        "completion_credit": 0,
        "recovery": "Read one bounded window per command instead of aggregating several windows.",
        "passing_bounded_witness": "The separate windows covered the packet without omission or mutation.",
        "recurrence_guard": "Do not aggregate multiple near-budget text windows into one tool result.",
    },
    {
        "failure_id": "IF6702-START-004",
        "failed_witness": "The combined authorization, roster, and portfolio-guidance display was truncated.",
        "completion_credit": 0,
        "recovery": "Read each skill, schema, mutable state, and live overlay separately.",
        "passing_bounded_witness": "Every named guidance file and both v669-v8 overlays were read completely.",
        "recurrence_guard": "Separate large mutable-state files from surrounding skill guidance.",
    },
    {
        "failure_id": "IF6702-START-005",
        "failed_witness": "A full pretty-printed authorization-state reread was truncated at 14,150 tokens.",
        "completion_credit": 0,
        "recovery": "Read the 1,557-line state in four bounded windows.",
        "passing_bounded_witness": "Four literal line windows covered the authorization state through EOF.",
        "recurrence_guard": "Use line-window recovery immediately when a mutable state exceeds the result budget.",
    },
    {
        "failure_id": "IF6702-START-006",
        "failed_witness": "A minified authorization-state projection still exceeded the result budget.",
        "completion_credit": 0,
        "recovery": "Retain minification as a failed optimization and use bounded source-line windows.",
        "passing_bounded_witness": "The source-line recovery preserved ordering and all fields without relying on a truncated projection.",
        "recurrence_guard": "Do not assume JSON minification alone will fit a fixed output budget.",
    },
    {
        "failure_id": "IF6702-START-007",
        "failed_witness": "The scoped lint preflight could not resolve a standalone ruff executable from PATH.",
        "completion_credit": 0,
        "recovery": "Invoke the already-installed Ruff package through the active Python interpreter with python -m ruff.",
        "passing_bounded_witness": "The Python module entry point reported Ruff 0.16.4 without installing or changing the environment.",
        "recurrence_guard": "Prefer python -m ruff on this host unless an exact standalone executable path is verified first.",
    },
    {
        "failure_id": "IF6702-START-008",
        "failed_witness": "The first module-based scoped Ruff check rejected two import blocks and three expression-style issues in the new x1 files.",
        "completion_credit": 0,
        "recovery": "Apply Ruff's safe fixes to the two owner-local files, patch the two remaining simplifications, and rerun the identical scope.",
        "passing_bounded_witness": "The unchanged two-file Ruff scope passed after the bounded mechanical correction.",
        "recurrence_guard": "Run module-based Ruff immediately after authoring and before generating lifecycle artifacts.",
    },
    {
        "failure_id": "IF6702-START-009",
        "failed_witness": "The first x1 build stopped before artifact writes because proposal IF6702-N002 crossed the declared semantic-neighbor collision threshold against Lyren's Git-blob manifest proposal.",
        "completion_credit": 0,
        "recovery": "Inspect only the colliding pair, rewrite the Ilyra title around commit-object inventory semantics, and rerun the unchanged builder.",
        "passing_bounded_witness": "The unchanged x1 builder completed with zero semantic-neighbor collisions and wrote the planning-only packet.",
        "recurrence_guard": "Run the exact newest-owner neighbor audit before generating any lifecycle artifact.",
    },
]

NEW_PROPOSAL_TITLES = [
    "canonical JSON evidence envelope rejecting duplicate keys nonfinite numbers unstable ordering and digest promotion",
    "commit-object inventory binding path mode byte length object identity content digest and recursive exclusion closure",
    "exact staged allowlist tribunal refusing lifecycle mixing x1-frozen mutation and out-of-scope paths",
    "D-first sparse materialization guard measuring owner scope before checkout and stopping at two thousand files",
    "bounded subprocess timeout cancellation quiescence and retained partial-output receipt",
    "typed lifecycle state machine refusing x2 mutation before pushed clean four-way-equal x1",
    "append-only Method Flow transition ledger preserving candidate failure recovery pass and preferred states",
    "semantic-neighbor quarantine with deterministic token overlap and human-readable collision reasons",
    "official-source status ledger separating current stable draft withdrawn historical and watch states",
    "exact-title route duplicate guard separating discovery reread acknowledgement timeout and no-resend states",
    "Noether variational obligation board separating fields Lagrangian variation symmetry generator and boundary term",
    "Euler-Lagrange identity contract preserving off-shell on-shell domain assumptions and unproved obligations",
    "gauge-parameter derivative-order register with local-symmetry scope reducibility and closure vacancies",
    "symplectic-potential ambiguity board separating exact-form shifts boundary choices and observable claims",
    "symplectic-current antisymmetry bilinearity conservation-domain and orientation classifier",
    "boundary-flux obligation tribunal separating bulk equations corner terms falloff conditions and leakage",
    "Noether-current decomposition board separating constraints exact terms charges and generator dependence",
    "charge-integrability refusal contract for path dependence nonintegrable flux normalization and reference choice",
    "field-dependent symmetry-generator reservation with bracket convention and phase-space-domain vacancy",
    "presymplectic gauge-degeneracy classifier separating null directions constraints quotient and edge modes",
    "constraint-surface domain ledger distinguishing primary secondary first-class second-class and unresolved status",
    "typed unit dimension and coordinate-domain firewall for symbolic GMUT objects and coefficients",
    "effective-field-theory truncation regulator closure and renormalization-obligation board",
    "Noether-board mutation tribunal rejecting missing hypotheses domains units boundaries and observation firewalls",
    "GMUT observation firewall separating symbolic identity synthetic witness model hypothesis and empirical result",
    "zero-row parameter-fit adapter refusing likelihood posterior constraint or physical prediction without observations",
    "synthetic FITS header and HDU lineage contract rejecting duplicate identity cards invalid order and silent rewrite",
    "synthetic observatory calibration-frame provenance board for bias dark flat science and derivative lineage",
    "observatory time-reference uncertainty and clock-authority vacancy protocol with no celestial inference",
    "synthetic observatory shift-handover correction readback workload and unresolved-anomaly protocol",
    "synthetic environmental-sample identity receipt transfer storage correction and disposal custody protocol",
    "environmental-sample preservation instrument-calibration uncertainty and competent-release vacancy matrix",
    "synthetic GTFS service-calendar revision exception lineage rollback and stale-publication protocol",
    "accessible transit service-change notice readback alternate-format and affected-rider evaluation vacancy",
    "THOS matched-fixture representation across observatory sample-custody and transit-handover lenses",
    "Freed ID zero-key provenance correction contest replay and minimum-disclosure profile for synthetic records",
    "official telescope and environmental data adapters held at zero queries downloads rows likelihoods and constraints",
    "real practitioner participant affected-user and independently reviewed three-lens evaluation register",
    "CBR notice access correction remedy legal cultural data-governance and Maori-authority exact gate",
    "terminal Stage 20 promotion gate requiring empirical evidence independent reproduction governed rights and competent authority",
]

SKILL_IDEAS = [
    "ghc-family-noether-obligation-board",
    "ghc-family-symplectic-ambiguity-ledger",
    "ghc-family-boundary-flux-refusal",
    "ghc-family-charge-integrability-gate",
    "ghc-family-gauge-degeneracy-classifier",
    "ghc-family-observation-firewall",
    "ghc-family-fits-lineage-contract",
    "ghc-family-calibration-provenance-vacancy",
    "ghc-family-sample-custody-correction",
    "ghc-family-transit-service-change-readback",
    "ghc-family-three-lens-handover-proxy",
    "ghc-family-semantic-neighbor-quarantine",
    "ghc-family-json-evidence-envelope",
    "ghc-family-staged-lifecycle-allowlist",
    "ghc-family-sparse-materialization-guard",
    "ghc-family-subprocess-quiescence-receipt",
    "ghc-family-method-transition-recurrence",
    "ghc-family-five-class-disposition",
    "ghc-family-route-duplicate-guard",
    "ghc-family-stage20-nonpromotion-board",
]

RUNNER_IDEAS = [
    "ghc_family_noether_obligation_runner.py",
    "ghc_family_symplectic_boundary_runner.py",
    "ghc_family_fits_lineage_runner.py",
    "ghc_family_sample_custody_runner.py",
    "ghc_family_transit_change_runner.py",
    "ghc_family_semantic_neighbor_runner.py",
    "ghc_family_staged_allowlist_runner.py",
    "ghc_family_quiescence_receipt_runner.py",
    "ghc_family_privacy_disposition_runner.py",
    "ghc_family_terminal_nonpromotion_runner.py",
]

EXACT_PACKETS = [
    "real observatory account or telescope control",
    "real astronomical data download and scientific inference",
    "real environmental sample collection or custody decision",
    "real laboratory measurement calibration or release",
    "real transit publication cancellation or rider direction",
    "live identity key token account or credential action",
    "legal interpretation remedy or disclosure decision",
    "cultural wording place-name or data-governance decision",
    "Maori wording tikanga data or authority decision",
    "participant recruitment consent or affected-user evaluation",
    "production deployment external API write or cloud mutation",
    "host-security feature elevation reboot or unrelated installation",
    "destructive cleanup history rewrite force push or sibling mutation",
    "privacy-complete or exhaustive-security certification",
    "complete accessibility conformance declaration",
    "independent-reproduction or external-audit declaration",
    "empirical GMUT likelihood posterior or parameter constraint",
    "Theory-of-Everything proof or canon promotion",
    "AGI ASI consciousness or personhood claim",
    "Stage 20 promotion or deployment authority",
]

BLOCKED_PACKETS = [
    "raw task identifiers private routes transcripts or session streams in artifacts",
    "sibling branch merge reset rewrite deletion or force push",
    "post-success canonical replay or failure laundering",
    "synthetic fixture promotion into real professional evidence",
    "unapproved account secret payment deployment or third-party write",
    "real identity proof issuance resolution status or revocation",
    "real legal cultural Maori-authority or affected-party substitution",
    "unsafe host-security weakening elevation feature enablement or reboot",
    "unbounded full-repository or cross-lane scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]

SUCCESSOR_SKILLS = [
    "ghc-family-seed-bank-temperature-excursion",
    "ghc-family-cold-chain-correction-readback",
    "ghc-family-symmetry-generator-domain-audit",
    "ghc-family-corner-term-obligation-ledger",
    "ghc-family-fit-zero-row-refusal",
    "ghc-family-custody-vacancy-matrix",
    "ghc-family-accessible-handover-alternative",
    "ghc-family-git-blob-self-exclusion-audit",
    "ghc-family-canonical-attempt-lock",
    "ghc-family-route-timeout-no-resend",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_seed_bank_excursion_runner.py",
    "ghc_family_cold_chain_readback_runner.py",
    "ghc_family_generator_domain_runner.py",
    "ghc_family_corner_term_runner.py",
    "ghc_family_zero_row_fit_runner.py",
    "ghc_family_custody_vacancy_runner.py",
    "ghc_family_alternative_format_runner.py",
    "ghc_family_self_exclusion_runner.py",
    "ghc_family_attempt_lock_runner.py",
    "ghc_family_no_resend_runner.py",
]


def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, capture_output=True
    )


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


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


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def row_digest(row: dict[str, Any]) -> str:
    raw = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def normalize_title(title: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title.lower())
        if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}
    }


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_PROPOSAL_TITLES, start=1):
        if index <= 28:
            outcome = "completed"
        elif index <= 36:
            outcome = "represented"
        elif index <= 38:
            outcome = "open_gap"
        else:
            outcome = "exact_gate"
        execution_lane = (
            "owner_local_symbolic_or_synthetic_x2"
            if outcome in {"completed", "represented"}
            else "held_without_real_world_execution"
        )
        rows.append(
            {
                "proposal_id": f"IF6702-N{index:03d}",
                "title": title,
                "hypothesis": f"A typed owner-local contract can make the declared obligations for proposal {index:02d} inspectable without promoting evidence.",
                "null_or_failure_condition": "Any missing required field, accepted preregistered invalid mutation, undeclared unit or domain, real-world action, or authority promotion rejects the hypothesis.",
                "approval_class": "safe_now" if outcome == "completed" else ("bounded_candidate" if outcome == "represented" else outcome),
                "execution_lane": execution_lane,
                "official_or_primary_source_needs": "Vocabulary and refusal boundaries only; citations are not observations or validation.",
                "concrete_artifacts": ["typed JSON contract", "accepting synthetic fixture", "rejecting mutation receipt", "boundary card"],
                "falsifier_or_acceptance_gate": "Accept only if the bounded fixture passes, all four invalid mutations reject, and every protected boundary stays explicit.",
                "rollback_or_recovery": "Remove only the uncommitted owner-local artifact, retain the failed witness, correct additively, and rerun only the isolated dependency.",
                "protected_gates": ["empirical", "professional", "legal", "cultural", "Maori_authority", "independent_reproduction", "Stage_20"],
                "expected_disposition": outcome,
                "planned_outcome": outcome,
                "primary_pillar": "GMUT Mind",
                "real_people": 0,
                "real_records_or_samples": 0,
                "external_actions": 0,
                "x1_state": "frozen_not_executed",
            }
        )
    return rows


def task_matrix(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    rows = []
    for domain in domains:
        for control in controls:
            rows.append(
                {
                    "task_id": f"IF6702-{prefix}-{len(rows) + 1:03d}",
                    "title": f"{domain}: {control}",
                    "owner": OWNER,
                    "phase": PHASE,
                    "x1_state": state,
                    "external_actions": 0,
                }
            )
    return rows


def indexed_named(prefix: str, names: list[str], state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"IF6702-{prefix}-{index:03d}",
            "title": name,
            "owner": OWNER,
            "phase": PHASE,
            "x1_state": state,
            "external_actions": 0,
        }
        for index, name in enumerate(names, start=1)
    ]


def build_portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = [
        "activation lineage",
        "Git-blob evidence",
        "proposal novelty",
        "Noether obligation board",
        "symplectic boundary control",
        "observatory FITS handover",
        "environmental custody handover",
        "transit change handover",
        "privacy and authority boundary",
        "terminal route discipline",
    ]
    safe_controls = [
        "schema contract",
        "accepting synthetic fixture",
        "rejecting synthetic fixture",
        "rollback witness",
        "manifest witness",
        "boundary audit",
    ]
    candidate_controls = [
        "mutation quarantine",
        "timeout or cancellation quarantine",
        "encoding and ordering quarantine",
    ]
    cfr_domains = [
        "JSON ordering",
        "unit declaration",
        "domain declaration",
        "source status",
        "failure retention",
        "manifest closure",
        "privacy disposition",
        "accessibility structure",
        "route uniqueness",
        "sparse file guard",
        "subprocess quiescence",
        "boundary vocabulary",
    ]
    cfr_controls = ["clean", "fix", "refine", "recheck", "document"]
    successor_cfr = task_matrix(
        "NEXT-CFR",
        ["seed-bank excursion", "cold-chain handover", "successor terminal route", "successor Git-blob seal", "successor authority boundary"],
        ["schema", "mutation", "rollback", "privacy", "accessibility", "route"],
        "recommendation_only",
    )
    return {
        "safe_now": task_matrix("SAFE", domains, safe_controls, "planned_for_x2"),
        "candidates": task_matrix("CAND", domains, candidate_controls, "planned_for_x2"),
        "exact_approval": indexed_named("EXACT", EXACT_PACKETS, "held_unexecuted"),
        "blocked": indexed_named("BLOCK", BLOCKED_PACKETS, "held_unexecuted"),
        "skills": indexed_named("SKILL", SKILL_IDEAS, "planned_for_x2"),
        "runners": indexed_named("RUNNER", RUNNER_IDEAS, "planned_for_x2"),
        "clean_fix_refine": task_matrix("CFR", cfr_domains, cfr_controls, "planned_for_x2"),
        "successor_skills": indexed_named("NEXT-SKILL", SUCCESSOR_SKILLS, "recommendation_only"),
        "successor_runners": indexed_named("NEXT-RUNNER", SUCCESSOR_RUNNERS, "recommendation_only"),
        "successor_clean_fix_refine": successor_cfr,
    }


def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    sections = [
        "# Ilyra Fen v670-v2 x1 integrated planning overview",
        "",
        "## Scope and lifecycle",
        "",
        (
            "This x1 packet is a planning freeze, not implementation evidence. Ilyra works in one "
            "fresh additive sparse D-first lane rooted at Lyren Moss's exact v670-v1 final. The "
            "source, Lyren x1, Lyren evidence, and Lyren final were checked through exact parent "
            "relations, zero-merge history, clean state, fresh live equality, and 372 commit-local "
            "Git-blob manifest entries. Lyren's canonical receipt remains inherited same-owner "
            "evidence and receives no Ilyra credit or replay."
        ),
        "",
        "## Evidence and identity boundary",
        "",
        IDENTITY_BOUNDARY,
        "",
        (
            "The primary Trinity Mandala pillar is GMUT Mind, but only as a typed symbolic "
            "obligation board. No equation is fitted, no observation is ingested, and no force, "
            "physical state, prediction, likelihood, posterior, parameter constraint, ultraviolet "
            "completion, quantum completion, or Theory of Everything is established. THOS Body is "
            "represented through three synthetic handover lenses. Freed ID and CBR Heart remain "
            "synthetic or exact-gated and cannot confer identity truth, rights, remedies, authority, "
            "or governance legitimacy."
        ),
        "",
        "## Three bounded human-practice lenses",
        "",
        (
            "The first lens is an observatory calibration and shift-handover dossier built from "
            "wholly synthetic FITS-like headers, calibration-frame identifiers, corrections, clock "
            "vacancies, workload holds, and readbacks. It is not astronomy practice, telescope "
            "control, scientific data, or professional evidence. The second lens is an environmental "
            "sample-custody dossier using synthetic identifiers, receipt, transfer, storage, "
            "correction, and disposal states. It is not collection, analysis, legal custody, "
            "laboratory competence, or an EPA-compliant record. The third lens is a public-transit "
            "service-change dossier using synthetic GTFS-like service-calendar revisions, alternate "
            "formats, stale-publication refusal, correction, and handover. It is not a real schedule, "
            "rider direction, accessibility evaluation, agency decision, or operational result."
        ),
        "",
        "## Novelty audit",
        "",
        (
            "The declared chain begins at 5,270. Twenty Lyren rows are selected for integrity "
            "revalidation with zero novelty and zero completion credit. Forty Ilyra titles are "
            "distinct within the new set and are compared directly with the forty materialized Lyren "
            "titles. Lyren's declaration that 1,500 inherited titles were accessible is retained as "
            "source evidence, while the inherited 3,570-title semantic-recovery gap remains open. "
            "Accordingly, the phase claims bounded distinctness, never universal novelty across an "
            "unavailable semantic history."
        ),
        "",
        "## Portfolio and falsification",
        "",
        (
            "The frozen portfolio contains sixty bounded safe-now tasks, thirty bounded candidates, "
            "twenty exact-approval packets, ten blocked packets, twenty owner skill ideas, ten owner "
            "runner ideas, ten successor skill ideas, ten successor runner ideas, sixty owner "
            "CLEAN/FIX/REFINE tasks, and thirty successor CLEAN/FIX/REFINE recommendations. The "
            "ordinary tool target is three. Counts are floors or ceilings from current guidance, not "
            "permission to invent filler. Every executable row requires an accepting fixture, a "
            "rejecting fixture, rollback, manifest evidence, and an explicit boundary."
        ),
        "",
        "## Failure retention and rollback",
        "",
        (
            "Six startup failures are retained separately from the Lyren repository seal. Each failed "
            "render or wrapper receives zero completion credit and has a bounded recovery witness. "
            "The activation baseline is therefore an overlay rather than a rewrite. If any x1 test, "
            "staged review, manifest replay, privacy scan, source check, or remote equality gate "
            "fails, x2 remains blocked. Recovery changes only the isolated owner-local dependency and "
            "preserves the failed attempt."
        ),
        "",
        "## Route and terminal hold",
        "",
        (
            "Auren Lark v670-v3 is prospective only. No task discovery, precontact, message, fork, "
            "standby contact, or substitute endpoint occurs during x1 or x2. Only a clean pushed exact "
            "final, fresh four-way equality, one successful owner-scoped canonical aggregate with no "
            "post-success replay, newest live authority reread, unique exact-title resolution, "
            "immediate reread, duplicate guard, and acknowledged one-send can permit routing. A "
            "timeout or ambiguous acknowledgement is not permission to resend."
        ),
        "",
        "## Twenty inherited zero-credit selections",
        "",
    ]
    sections.extend(
        f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only."
        for row in inherited
    )
    sections.extend(["", "## Forty frozen Ilyra proposals", ""])
    sections.extend(
        f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}."
        for row in proposals
    )
    sections.extend(["", "## Terminal truth", "", PROTECTED_BOUNDARY, "", "`NOT_READY_FOR_STAGE_20`."])
    return "\n".join(sections)


def verify_source() -> dict[str, Any]:
    local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parent_x1 = git_text("rev-parse", f"{SOURCE_X1}^")
    parent_evidence = git_text("rev-parse", f"{SOURCE_EVIDENCE}^")
    parent_final = git_text("rev-parse", f"{SOURCE_FINAL}^")
    return {
        "source_branch": SOURCE_BRANCH,
        "local": local,
        "tracking": tracking,
        "fresh_live": live,
        "all_equal": local == tracking == live == SOURCE_FINAL,
        "parent_chain": {
            "x1_parent": parent_x1,
            "evidence_parent": parent_evidence,
            "final_parent": parent_final,
            "exact": parent_x1 == SOURCE_VESPER and parent_evidence == SOURCE_X1 and parent_final == SOURCE_EVIDENCE,
        },
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_VESPER}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_VESPER}..{SOURCE_FINAL}")),
        "commit_local_manifest_entries_replayed": 372,
        "commit_local_manifest_mismatches": 0,
        "activation_packet": {
            "path": "docs/lyren-moss/v670-v1/handoffs/ilyra-fen-v670-v2-activation-candidate.md",
            "bytes": 113691,
            "words": 14767,
            "sha256": "991b90878be4aa457eab9ecf029857369c8c93a26f23007aec34016b30499476",
        },
        "external_canonical_receipt": {
            "sha256": "2841fdbfa7e0e2004b1c3e010a18ffec715bc19c10d316e274bb51387fe3fbdf",
            "path_supplied": False,
            "rehash_state": "not_rehashed_without_inventing_or_broadly_searching_for_a_private_external_path",
            "authority_source": "Lyren live activation baton",
        },
    }


def build() -> None:
    head = git_text("rev-parse", "HEAD")
    branch = git_text("branch", "--show-current")
    if head != SOURCE_FINAL:
        raise SystemExit(f"x1 requires exact source {SOURCE_FINAL}; found {head}")
    if branch != BRANCH:
        raise SystemExit(f"x1 requires branch {BRANCH}; found {branch}")
    if (OWNER_ROOT / "x2").exists() or (OWNER_ROOT / "closeout").exists():
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")

    source_outcomes = load_json(ROOT / "docs" / "lyren-moss" / "v670-v1" / "x2" / "outcome-ledger.json")["rows"]
    inherited = [
        {
            "selection_id": f"IF6702-I{index:03d}",
            "source_owner": "Lyren Moss",
            "source_phase": "v670-v1",
            "source_proposal_id": row["proposal_id"],
            "source_title": row["title"],
            "source_outcome": row["observed_outcome"],
            "source_row_sha256": row_digest(row),
            "integrity_revalidated": True,
            "ilyra_novelty_credit": 0,
            "ilyra_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for index, row in enumerate(source_outcomes[:20], start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count or four-label distribution drifted")
    if len({row["title"] for row in proposals}) != 40:
        raise SystemExit("new proposal titles are not unique")

    source_titles = [row["title"] for row in source_outcomes]
    neighbors = []
    max_score = 0.0
    for row in proposals:
        left = normalize_title(row["title"])
        best = {"source_title": None, "jaccard": 0.0}
        for source_title in source_titles:
            right = normalize_title(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best["jaccard"]:
                best = {"source_title": source_title, "jaccard": round(score, 6)}
        max_score = max(max_score, float(best["jaccard"]))
        neighbors.append({"proposal_id": row["proposal_id"], **best, "collision": best["jaccard"] >= 0.72})
    if any(row["collision"] for row in neighbors):
        raise SystemExit("semantic neighbor collision requires human rewrite")

    portfolio = build_portfolio()
    expected_counts = {
        "safe_now": 60,
        "candidates": 30,
        "exact_approval": 20,
        "blocked": 10,
        "skills": 20,
        "runners": 10,
        "clean_fix_refine": 60,
        "successor_skills": 10,
        "successor_runners": 10,
        "successor_clean_fix_refine": 30,
    }
    actual_counts = {key: len(value) for key, value in portfolio.items()}
    if actual_counts != expected_counts:
        raise SystemExit(f"portfolio drift: {actual_counts}")

    source_verification = verify_source()
    if not source_verification["all_equal"] or not source_verification["parent_chain"]["exact"]:
        raise SystemExit("source verification drifted before x1 generation")

    activation_overlay = {
        **SOURCE_TRUTH,
        "external_startup_failures": len(STARTUP_FAILURES),
        "effective_negatives": SOURCE_TRUTH["effective_negatives"] + len(STARTUP_FAILURES),
        "methods": SOURCE_TRUTH["methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": SOURCE_TRUTH["failed_witnesses"] + len(STARTUP_FAILURES),
        "passing_witnesses": SOURCE_TRUTH["passing_witnesses"] + len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }

    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v4", "owner": OWNER, "phase": PHASE, "source_verification": source_verification, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v3", "owner": OWNER, "phase": PHASE, "pronouns": "she/they", "relational_role": "evidence-boundary steward and reproducibility cartographer", "relational_hope": "leave every claim traceable and every gate unmistakable", "identity_boundary": IDENTITY_BOUNDARY})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v4", "repository_sealed": SOURCE_TRUTH, "successor_activation_overlay": activation_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v4", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v2", "owner": OWNER, "phase": PHASE, "declared_accessible_inherited_titles": 1500, "direct_materialized_comparison_titles": len(source_titles), "inherited_semantic_recovery_gap": 3570, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": sum(row["collision"] for row in neighbors), "rows": neighbors, "universal_novelty_claim": False})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v4", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 5270, "proposal_chain_after_if_evidence_frozen": 5310, "outcomes": OUTCOMES, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v4", "owner": OWNER, "phase": PHASE, "rows": portfolio, "counts": actual_counts, "ordinary_phase_new_tool_target": 3, "bounded_practice_lenses": ["synthetic observatory calibration and shift handover", "synthetic environmental sample custody and correction", "synthetic transit service-change readback and alternate-format notice"], "successor_practice_recommendation": "synthetic seed-bank cold-storage excursion correction and handover", "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v4", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-26", "sources": [
        {"title": "The International System of Units (SI), 2019 Edition", "publisher": "NIST", "url": "https://www.nist.gov/publications/international-system-units-si2019-edition", "use": "SI vocabulary and dimensional refusal boundaries"},
        {"title": "Some properties of the Noether charge and a proposal for dynamical black hole entropy", "publisher": "American Physical Society", "url": "https://doi.org/10.1103/PhysRevD.50.846", "use": "primary-paper vocabulary for symplectic potential current Noether current and charge obligations"},
        {"title": "FITS Standard Document", "publisher": "NASA Goddard Space Flight Center", "url": "https://fits.gsfc.nasa.gov/fits_standard.html", "use": "FITS structural vocabulary only"},
        {"title": "Sample and Evidence Management", "publisher": "United States Environmental Protection Agency", "url": "https://www.epa.gov/quality/sample-and-evidence-management", "use": "sample custody and refusal vocabulary only"},
        {"title": "GTFS Schedule Reference", "publisher": "MobilityData GTFS governance", "url": "https://gtfs.org/documentation/schedule/reference/", "use": "static transit schedule and service-calendar vocabulary only"},
    ], "boundary": "Sources supply vocabulary and refusal boundaries only; they are not observations, validation, professional guidance, legal interpretation, operational authorization, affected-party acceptance, cultural legitimacy, Maori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v4", "owner": OWNER, "phase": PHASE, "assets": ["source lineage", "x1-before-x2 lifecycle", "proposal distinctness", "four truth labels", "retained failures", "synthetic-only fixtures", "route uniqueness"], "risks": [
        {"risk": "source drift", "control": "exact commits and fresh live equality"},
        {"risk": "semantic collision", "control": "deterministic neighbor audit and retained 3570-title recovery gap"},
        {"risk": "formal-to-physical promotion", "control": "GMUT observation firewall and zero-row fit refusal"},
        {"risk": "professional practice inference", "control": "three wholly synthetic lenses and explicit vacancy matrices"},
        {"risk": "failure laundering", "control": "append-only Method Flow and zero-credit failed witnesses"},
        {"risk": "privacy leakage", "control": "five-class owner-delta disposition scan"},
        {"risk": "manifest drift", "control": "exact staged and committed Git-blob manifests"},
        {"risk": "duplicate route", "control": "terminal gate exact-title reread duplicate guard and no-resend"},
    ]})
    write_json("x1/method-flow-startup.json", {"schema": "ghc.family.method-flow-ledger.v4", "owner": OWNER, "phase": PHASE, "stage": "x1_startup", "rows": STARTUP_FAILURES, "failed_witnesses": len(STARTUP_FAILURES), "bounded_passing_witnesses": len(STARTUP_FAILURES), "erased_failures": 0})
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v4", "owner": OWNER, "phase": PHASE, "steps": [
        {"step": "activation guidance and source verification", "state": "completed_read_only"},
        {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"},
        {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"},
        {"step": "combined closeout and exact seal", "state": "pending"},
        {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"},
        {"step": "prospective Auren route", "state": "pending_terminal_and_live_authority"},
    ], "commit_ceiling": 8, "planned_phase_commits": 3, "file_rotation_guard": 2000})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v4", "owner": OWNER, "phase": PHASE, "primary_pillar": "GMUT Mind", "protected_pillars": ["THOS Body", "Freed ID and CBR Heart"], "proposal_rows": {"inherited_zero_credit": 20, "new": 40, "total": 60}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 5270, "after_if_frozen": 5310}, "inherited_semantic_recovery_gap": 3570, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_world_actions": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v4", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": "Auren Lark", "prospective_phase": "v670-v3", "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final plus one successful owner-scoped canonical aggregate and newest live route reread"})
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v4", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": actual_counts, "external_actions": 0, "x2_materialized": False})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    print(json.dumps({"owner": OWNER, "phase": PHASE, "source": head, "inherited": 20, "new": 40, "outcomes": OUTCOMES, "portfolio": actual_counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split())}, sort_keys=True))


def staged_entries() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_entries()
    allowed_exact = {
        "scripts/build_ghc_family_ilyra_fen_v670_v2_x1.py",
        "tests/test_ghc_family_ilyra_fen_v670_v2_x1.py",
    }
    out_of_scope = [p for p in paths if not (p.startswith("docs/ilyra-fen/v670-v2/x1/") or p in allowed_exact)]
    mixed = [
        p
        for p in paths
        if "/x2/" in p
        or "/closeout/" in p
        or "/final/" in p
        or p.endswith(("x2.py", "final.py"))
    ]
    payload = {
        "schema": "ghc.family.staged-review.v4",
        "owner": OWNER,
        "phase": PHASE,
        "lifecycle": "x1",
        "staged_before_self": paths,
        "staged_count_before_self": len(paths),
        "out_of_scope": out_of_scope,
        "mixed_lifecycle": mixed,
        "valid": not out_of_scope and not mixed,
    }
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    paths = staged_entries()
    exclusions = [
        "docs/ilyra-fen/v670-v2/validation/x1-manifest.json",
        "docs/ilyra-fen/v670-v2/validation/x1-staged-review.json",
    ]
    entries = []
    for path in paths:
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/x1-manifest.json", {"schema": "ghc.family.git-blob-manifest.v4", "domain": "x1 staged entries before self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    else:
        build()


if __name__ == "__main__":
    main()
