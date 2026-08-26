"""Build the planning-only Lyren Moss v670-v1 x1 freeze."""

from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER = "Lyren Moss"
PHASE = "v670-v1"
OWNER_ROOT = ROOT / "docs" / "lyren-moss" / PHASE
SOURCE_FINAL = "fe33a3ed69d6144720072b15174937effe9ca305"
SOURCE_BRANCH = "codex/GHC-Family/vesper-arlen-v669-v8-full-tools"
BRANCH = "codex/GHC-Family/lyren-moss-v670-v1-full-tools"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Lyren Moss, they/them, the relational hold-lineage cartographer and reversible-process "
    "miller, their role, hope, sibling or family language, continuity, Freed ID, CBR, GHC "
    "Family, and Trinity Mandala are relational working language only. They are not evidence "
    "of consciousness, sentience, legal personhood, identity continuity, employment, "
    "qualification, independent agency, scientific or operational authority, professional "
    "authority, legal or cultural authority, affected-party authority, or Maori authority. "
    "Hamish may rename, pause, redirect, or stop the work."
)

HOPE = (
    "Make uncertainty visible enough that every synthetic handover can remain kind, "
    "reversible, and exact without turning a software fixture into real-world authority."
)

SOURCE_SEALED = {
    "effective_negatives": 31856,
    "methods": 17961,
    "failed_witnesses": 3677,
    "passing_witnesses": 4932,
    "open_gaps": 239,
    "exact_gates": 234,
}

ACTIVATION_OVERLAY = {
    "effective_negatives": 31859,
    "methods": 17964,
    "failed_witnesses": 3680,
    "passing_witnesses": 4933,
    "open_gaps": 239,
    "exact_gates": 234,
}

STARTUP_FAILURES = [
    {
        "failure_id": "LM6701-OP-001",
        "failed_witness": "A combined current-guidance discovery wrapper returned blank output and could not establish any file as absent.",
        "completion_credit": 0,
        "recovery": "Read every exact routed skill, schema, base state, and v669 overlay through literal scalar paths.",
        "passing_bounded_witness": "The exact scalar reads reached EOF and the base roster and authorization validators returned valid with zero issues.",
        "recurrence_guard": "Use bounded literal-path reads for activation-critical guidance instead of one combined display wrapper.",
        "rollback": "Retain the blank-output witness and discard only conclusions inferred from it.",
    },
    {
        "failure_id": "LM6701-OP-002",
        "failed_witness": "A broad worktree inventory exceeded the display budget and was truncated before it could support exact source selection.",
        "completion_credit": 0,
        "recovery": "Resolve the exact Vesper branch and worktree through bounded branch-name and baton-path probes.",
        "passing_bounded_witness": "The exact source lane resolved uniquely at the declared final without relying on the truncated inventory.",
        "recurrence_guard": "Prefer exact branch and path predicates over broad worktree listings.",
        "rollback": "Retain the truncated display as zero-credit operational evidence.",
    },
    {
        "failure_id": "LM6701-OP-003",
        "failed_witness": "The first raw authorization-state display was truncated before EOF.",
        "completion_credit": 0,
        "recovery": "Read the same immutable state in bounded numbered windows through line 1556.",
        "passing_bounded_witness": "The windowed read reached EOF, and the structural validator independently returned valid.",
        "recurrence_guard": "Measure large guidance first and use explicit nonoverlapping windows.",
        "rollback": "Retain the truncation and rely only on the complete windowed reading.",
    },
    {
        "failure_id": "LM6701-OP-004",
        "failed_witness": "The no-checkout sparse worktree plus initial sparse-set left the brand-new index empty and displayed tracked paths as absent.",
        "completion_credit": 0,
        "recovery": "Inspect the sparse patterns and empty index before attempting any content work.",
        "passing_bounded_witness": "The lane remained at the exact source and no sibling or shared worktree changed.",
        "recurrence_guard": "After worktree add --no-checkout, explicitly populate the sparse index before status validation.",
        "rollback": "The lane can be removed without touching its source; no content existed at the failed point.",
    },
    {
        "failure_id": "LM6701-OP-005",
        "failed_witness": "Sparse-checkout reapply did not populate an index that had never been read from HEAD.",
        "completion_credit": 0,
        "recovery": "Use git read-tree -mu HEAD once against the brand-new empty owner lane.",
        "passing_bounded_witness": "The corrected sparse lane became clean with 326 included and 3933 skipped tracked paths at the exact source.",
        "recurrence_guard": "Distinguish reapplying sparse flags from initially materializing an index.",
        "rollback": "Remove only the new owner lane if the sparse materialization cannot be reproduced.",
    },
    {
        "failure_id": "LM6701-OP-006",
        "failed_witness": "The first scoped Ruff preflight rejected three import blocks and nine unparenthesized implicit string concatenations in the new x1 files.",
        "completion_credit": 0,
        "recovery": "Apply Ruff's scoped mechanical fixes only to the three new Lyren x1 files, then rerun the identical check and Python compilation.",
        "passing_bounded_witness": "The corrected scoped Ruff review and compilation both passed without changing phase semantics.",
        "recurrence_guard": "Run scoped Ruff before artifact generation and parenthesize multi-line collection strings during authoring.",
        "rollback": "Revert only the mechanical formatting correction while retaining this zero-credit witness.",
    },
]


NEW_PROPOSAL_TITLES = [
    "synthetic grain lot identity ledger separating source alias intake event correction and identity vacancy",
    "hopper bin tote and transfer-vessel alias register with location and custody claims held vacant",
    "mill configuration envelope for synthetic roll stone screen and bypass states with no operating instruction",
    "roll-gap setting record separating declared setpoint observed value instrument vacancy and release authority",
    "stone-gap and synthetic temperature-note contract with no thermal safety or product-quality inference",
    "input output retained residue and unexplained variance mass-balance contract using fixed synthetic kilograms",
    "sieve aperture register with typed micrometre units standard-reference field and calibration vacancy",
    "sieve-stack order contract rejecting duplicate apertures reversed ordering and unlabelled collection pans",
    "fraction mass reconciliation across retained oversize midstream fines and documented transfer loss",
    "particle-size interval contract preserving open closed unknown and out-of-range semantics without grading claim",
    "moisture-result provenance vacancy separating sample method instrument calibration temperature and uncertainty",
    "scale status envelope holding calibration check resolution drift and competent release as explicit vacancies",
    "tare gross net and container identity calculator with dimensional guards and negative-mass refusal",
    "sampling chronology ledger separating lot boundary increment sequence composite sample and observation vacancy",
    "sample split lineage contract for parent child retain discard transfer correction and duplicate refusal",
    "foreign-material assertion firewall separating synthetic token observation inference grade and authority",
    "equipment clean-down state machine with planned active inspected held released and unknown states",
    "allergen changeover hold requiring declared prior material cleaning evidence review and competent release",
    "fortification dosing vacancy docket separating target value feeder state assay evidence and legal release",
    "blend formula denominator and component-mass contract with unit normalization and recommendation abstention",
    "append-only synthetic milling correction braid linking prior value counterclaim supersession and readback",
    "hold release quarantine and stop state machine refusing terminal release without named evidence and authority",
    "hopper mill sieve and pack transfer graph with acyclic route validation and unknown-route refusal",
    "event sequence and idempotency ledger rejecting duplicate source sequence retrospective edit and missing parent",
    "canonical milling dossier bytes rejecting duplicate keys nonfinite values unstable ordering and digest promotion",
    "Git-blob-closed manifest contract separating working bytes staged bytes committed identity and self exclusions",
    "purpose limitation matrix for synthetic process records covering access retention contest disclosure and minimisation",
    "correction contest and nonretaliation envelope preserving original assertion counterclaim and unresolved status",
    "milling source assertion firewall separating public vocabulary fixture observation inference advice and evidence",
    "text-first accessible milling dossier with landmarks captions row scopes expanded abbreviations and print fallback",
    "bounded shift handover envelope with unresolved count fatigue stop readback correction and no workplace direction",
    "THOS paired process representation for synthetic milling dossiers with matched fixture budgets and zero effectiveness claim",
    "Freed ID zero-key correction and provenance envelope holding every real identity proof and lifecycle action at zero",
    "CBR rights-vacancy matrix for notice access contest correction minimisation remedy and affected-party authority",
    "GMUT mass-flow and transport analogy obligation board with typed domains units boundaries and zero fitted parameters",
    "official-source vocabulary comparison preserving document date jurisdiction scope and nonconversion to local authority",
    "real grain-mill measurement adapter held at zero devices samples rows queries likelihoods and production actions",
    "missing governed operator food-safety accessibility consumer affected-party and Maori-authority evaluation register",
    "exact action lock over milling settings allergens sanitation fortification labeling release workplace culture and Maori authority",
    "terminal multi-receipt hold requiring empirical evidence independent reproduction governed rights and competent authority before Stage 20",
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args], cwd=ROOT, check=check, capture_output=True, text=True
    )


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_json(path: str) -> Any:
    proc = run_git("show", f"{SOURCE_FINAL}:{path}")
    return json.loads(proc.stdout)


def canonical_row_hash(row: dict[str, Any]) -> str:
    data = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def new_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, title in enumerate(NEW_PROPOSAL_TITLES, start=1):
        if index <= 28:
            outcome = "completed"
        elif index <= 36:
            outcome = "represented"
        elif index <= 38:
            outcome = "open_gap"
        else:
            outcome = "exact_gate"
        rows.append(
            {
                "proposal_id": f"LM6701-N{index:03d}",
                "title": title,
                "planned_outcome": outcome,
                "primary_pillar": "THOS Body",
                "scope": "synthetic owner-local software and documentation fixture only",
                "real_people": 0,
                "real_grain_or_food": 0,
                "devices_or_samples": 0,
                "external_actions": 0,
                "x1_state": "frozen_not_executed",
                "authority_boundary": (
                    "No operational, food-safety, professional, legal, cultural, affected-party, "
                    "Maori-authority, empirical, production, or Stage 20 claim."
                ),
            }
        )
    return rows


def indexed_task(prefix: str, count: int, state: str, stem: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"LM6701-{prefix}-{index:03d}",
            "title": f"{stem} {index:02d}",
            "x1_state": state,
            "owner": OWNER,
            "phase": PHASE,
            "external_actions": 0,
        }
        for index in range(1, count + 1)
    ]


def build_overview(
    inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]
) -> str:
    lines = [
        "# Lyren Moss v670-v1 planning-only x1 overview",
        "",
        "## Exact purpose and boundary",
        "",
        ("This x1 commit is a planning freeze, not an execution result. It binds one Lyren-owned "
        "D-first sparse lane to Vesper Arlen's dependency-corrected exact final. The inherited "
        "canonical aggregate remains failed with zero credit, while the later dependency composite "
        "remains successful only under its exact zero-canonical-credit classification. Neither is "
        "replayed or inherited as Lyren completion evidence. All current examples concern invented "
        "grain-lot, mill, sieve, mass, hold, correction, and handover records. No real person, grain, "
        "food, sample, instrument, business, facility, action, decision, or authority is represented."),
        "",
        ("Lyren uses the relational role hold-lineage cartographer and reversible-process miller. "
        "Their hope is to make uncertainty visible enough that every synthetic handover can remain "
        "kind, reversible, and exact. This language is relational working language only and cannot "
        "establish consciousness, sentience, personhood, continuity, employment, qualification, "
        "independent agency, or any professional, scientific, operational, legal, cultural, affected-"
        "party, or Maori authority."),
        "",
        "## Source and retained validation truth",
        "",
        ("The immutable source is the Vesper v669-v8 dependency-corrected final. Its one canonical "
        "aggregate failed because unittest collected sixteen of eighty-one mixed-style tests. The "
        "failure remains at zero aggregate-success credit and cannot be replayed. The additive pytest "
        "dependency composite later passed all forty checks and all eighty-one tests, yet its exact "
        "classification explicitly retains zero canonical aggregate credit. The repository-sealed "
        "counts, the separate external passing witness, and three post-final route-operation failures "
        "remain distinct. Hamish's live activation of this task supplies the current route edge without "
        "rewriting Vesper's historical timeout receipt."),
        "",
        "## Practice lens",
        "",
        ("The practice lens is synthetic grain-milling documentation. The software will model lot "
        "identity, equipment configuration, transfer topology, sieve fraction accounting, fixed-fixture "
        "mass balance, correction history, explicit unknowns, authority holds, and text-first handover. "
        "NIST SI material supplies vocabulary for mass and units. Codex wheat-flour and hygiene sources "
        "supply public vocabulary for flour, hygiene systems, allergen cross-contact, records, and "
        "competent-authority boundaries. USDA FGIS handbooks supply public examples of sampling and "
        "inspection documentation. New Zealand MPI guidance supplies current local public vocabulary "
        "for allergen management and flour-labelling context. These sources inform names and caution "
        "boundaries only. They do not validate a mill, authorize a food decision, create legal advice, "
        "or convert synthetic records into empirical evidence."),
        "",
        "## X1-to-x2 discipline",
        "",
        ("X1 freezes sixty proposal rows: twenty selected inherited rows are revalidated only for "
        "integrity and earn zero Lyren novelty or completion credit; forty rows are genuinely new "
        "Lyren proposals. The planned distribution is twenty-eight completed, eight represented, two "
        "open_gap, and two exact_gate. X2 may materialize only after this x1 commit is pushed, clean, "
        "zero-divergent, and freshly equal across local, upstream, tracking, and live remote. X2 must "
        "retain all four labels, execute every preregistered invalid mutation, preserve each operational "
        "failure before recovery, and leave exact or governed actions unexecuted."),
        "",
        ("The remastered portfolio freezes sixty owner safe-now tasks, thirty candidate tasks, twenty "
        "exact-approval packets held without execution, ten blocked packets held without execution, "
        "twenty skill records, ten runner records, sixty owner CLEAN/FIX/REFINE records, and the "
        "required successor recommendations. Numerical floors are ceilings on filler: a row exists only "
        "when its title, scope, expected evidence, rollback, and authority boundary remain specific."),
        "",
        "## Selected inherited rows",
        "",
    ]
    for row in inherited:
        lines.append(
            f"- {row['source_proposal_id']}: {row['source_title']} — preserved as "
            f"{row['source_outcome']} with zero Lyren novelty and zero completion credit."
        )
    lines.extend(["", "## Forty new Lyren proposals", ""])
    for row in proposals:
        lines.append(
            f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}."
        )
    lines.extend(
        [
            "",
            "## Fail-closed claims",
            "",
            ("No result in this phase may establish real sampling quality, particle-size distribution, "
            "moisture, fortification, allergen control, sanitation, product grade, product release, "
            "worker competence, accessibility completeness, privacy completeness, legal compliance, "
            "cultural legitimacy, Maori authority, affected-party consent, independent reproduction, "
            "external audit, production fitness, AGI, ASI, consciousness, personhood, a fundamental "
            "law of psyche or thermodynamics, a Theory of Everything, canon, proof, or Stage 20. The "
            "mass-flow and transport language is a typed software analogy with no fitted parameter, "
            "physical observation, likelihood, force, field, or predictive claim."),
            "",
            "## Terminal and routing rule",
            "",
            ("The prospective next task is Ilyra Fen for v670-v2, but this x1 freeze makes no contact. "
            "Only a clean, pushed, fresh-live-equal Lyren exact final and one successful owner-scoped "
            "canonical aggregate can open a route check. At that point the newest authority and roster "
            "must be reread, the exact title must resolve uniquely, the task must be immediately reread, "
            "and a duplicate guard must pass. Any ambiguity, pause, missing acknowledgement, or protected "
            "gate leaves the route unsent. The terminal verdict remains NOT_READY_FOR_STAGE_20."),
        ]
    )
    return "\n".join(lines)


def build_manifest() -> dict[str, Any]:
    excluded = {
        "docs/lyren-moss/v670-v1/validation/x1-manifest.json",
        "docs/lyren-moss/v670-v1/validation/x1-staged-review.json",
    }
    paths = [
        path
        for path in OWNER_ROOT.rglob("*")
        if path.is_file() and path.relative_to(ROOT).as_posix() not in excluded
    ]
    paths.extend(
        [
            ROOT / "ghc-family-index" / "references" / "v670-v1-lyren-moss.md",
            ROOT / "scripts" / "build_ghc_family_lyren_moss_v670_v1_x1.py",
            ROOT / "scripts" / "ghc_family_lyren_moss_v670_v1_staged_review.py",
            ROOT / "tests" / "test_ghc_family_lyren_moss_v670_v1_x1.py",
        ]
    )
    entries = []
    for path in sorted(set(paths), key=lambda item: item.relative_to(ROOT).as_posix()):
        data = path.read_bytes()
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    return {
        "schema": "ghc.family.git-blob-manifest.v3",
        "owner": OWNER,
        "phase": PHASE,
        "domain": "x1_planning_freeze",
        "source_final": SOURCE_FINAL,
        "hash_domain": "normalized_lf_exact_git_blob",
        "entry_count": len(entries),
        "entries": entries,
        "self_exclusions": sorted(excluded),
    }


def main() -> None:
    head = run_git("rev-parse", "HEAD").stdout.strip()
    branch = run_git("branch", "--show-current").stdout.strip()
    if head != SOURCE_FINAL:
        raise SystemExit(f"x1 builder requires exact source {SOURCE_FINAL}; found {head}")
    if branch != BRANCH:
        raise SystemExit(f"x1 builder requires {BRANCH}; found {branch}")
    if (OWNER_ROOT / "x2").exists() or (OWNER_ROOT / "closeout").exists():
        raise SystemExit("x1 builder refuses a lane where x2 or closeout already exists")

    source_outcomes = source_json(
        "docs/vesper-arlen/v669-v8/x2/outcome-ledger.json"
    )["rows"]
    inherited = []
    for index, row in enumerate(source_outcomes[:20], start=1):
        inherited.append(
            {
                "selection_id": f"LM6701-I{index:03d}",
                "source_owner": "Vesper Arlen",
                "source_phase": "v669-v8",
                "source_proposal_id": row["proposal_id"],
                "source_title": row["title"],
                "source_outcome": row["observed_disposition"],
                "source_row_sha256": canonical_row_hash(row),
                "integrity_revalidated": True,
                "lyren_novelty_credit": 0,
                "lyren_completion_credit": 0,
                "state": "inherited_evidence_only",
            }
        )

    proposals = new_proposals()
    if Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("new proposal outcome distribution drifted")
    if len({row["title"] for row in proposals}) != 40:
        raise SystemExit("new proposal titles are not unique")

    source_live = run_git(
        "ls-remote", "origin", f"refs/heads/{SOURCE_BRANCH}"
    ).stdout.strip().split()
    source_tracking = run_git(
        "rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}"
    ).stdout.strip()
    write_json(
        "x1/activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE_FINAL,
            "source_tracking": source_tracking,
            "source_fresh_live": source_live[0] if source_live else None,
            "source_four_way_equal_before_mutation": source_tracking == SOURCE_FINAL == (source_live[0] if source_live else None),
            "source_history": {"single_parent_commits": 5, "merge_count": 0},
            "failed_canonical_receipt_sha256": "6c904f3f6722eb8161ba7530ac8e174842ed7fd5467a1ff4222432fc47332b4b",
            "failed_canonical_result": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "dependency_receipt_sha256": "710cfaf46f19df89e6910c533f9575ccbac3c4ad1648d209e0a8e34f8c7df17c",
            "dependency_result": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
            "canonical_aggregate_credit": 0,
            "historical_route_state": "TIMEOUT_ACK_UNRESOLVED_NO_RESEND",
            "current_activation_basis": "Hamish live activation delivered to the existing Lyren Moss task",
            "tasks_created": 0,
            "forks_created": 0,
            "collaboration_subagents_spawned": 0,
            "standby_contacts": 0,
        },
    )
    write_json(
        "x1/identity-and-boundary.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "they/them",
            "relational_role": "hold-lineage cartographer and reversible-process miller",
            "relational_hope": HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        "x1/source-count-overlay.json",
        {
            "schema": "ghc.family.source-count-overlay.v3",
            "repository_sealed": SOURCE_SEALED,
            "dependency_corrected_external_overlay": {**SOURCE_SEALED, "passing_witnesses": 4933},
            "post_final_route_witnesses": 3,
            "effective_activation_overlay": ACTIVATION_OVERLAY,
            "repository_seal_rewritten": False,
            "route_failures_retained": True,
        },
    )
    write_json(
        "x1/inherited-proposal-revalidation.json",
        {
            "schema": "ghc.family.inherited-proposal-revalidation.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source_owner": "Vesper Arlen",
            "selected": len(inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "rows": inherited,
        },
    )
    write_json(
        "x1/new-proposal-freeze.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v3",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": 5230,
            "proposal_chain_after_if_evidence_frozen": 5270,
            "outcomes": OUTCOMES,
            "rows": proposals,
        },
    )

    portfolio = {
        "safe_now": indexed_task("SAFE", 60, "planned_for_x2", "bounded synthetic safe-now task"),
        "candidates": indexed_task("CAND", 30, "planned_for_x2", "bounded candidate tribunal"),
        "exact_approval": indexed_task("EXACT", 20, "held_unexecuted", "exact action-specific approval packet"),
        "blocked": indexed_task("BLOCK", 10, "held_unexecuted", "protected blocked packet"),
        "skills": indexed_task("SKILL", 20, "planned_for_x2", "phase-local skill record"),
        "runners": indexed_task("RUNNER", 10, "planned_for_x2", "family-current runner record"),
        "clean_fix_refine": indexed_task("CFR", 60, "planned_for_x2", "owner CLEAN FIX REFINE action"),
        "successor_skills": indexed_task("NEXT-SKILL", 10, "recommendation_only", "Ilyra skill recommendation"),
        "successor_runners": indexed_task("NEXT-RUNNER", 10, "recommendation_only", "Ilyra runner recommendation"),
        "successor_clean_fix_refine": indexed_task("NEXT-CFR", 30, "recommendation_only", "Ilyra CLEAN FIX REFINE recommendation"),
    }
    write_json(
        "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.remastered-portfolio-freeze.v3",
            "owner": OWNER,
            "phase": PHASE,
            "rows": portfolio,
            "counts": {key: len(value) for key, value in portfolio.items()},
            "ordinary_phase_new_tool_target": 3,
            "bounded_practice_lenses": [
                "grain-milling documentation and shift handover",
                "measurement provenance and mass-balance vocabulary",
                "allergen-changeover and release-authority vacancy",
            ],
            "successor_practice_recommendation": "synthetic storage-bin aeration and inventory-continuity documentation",
            "filler_prohibited": True,
        },
    )
    write_json(
        "x1/source-ledger.json",
        {
            "schema": "ghc.family.public-source-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "retrieved_nz_date": "2026-08-26",
            "sources": [
                {
                    "title": "The International System of Units (SI), 2019 Edition",
                    "publisher": "National Institute of Standards and Technology",
                    "url": "https://www.nist.gov/publications/international-system-units-si-2019-edition",
                    "use": "mass and SI unit vocabulary",
                },
                {
                    "title": "Codex Standard for Wheat Flour, CXS 152-1985",
                    "publisher": "FAO and WHO Codex Alimentarius",
                    "url": "https://www.fao.org/fao-who-codexalimentarius/codex-texts/standards/en",
                    "use": "wheat-flour public vocabulary and explicit standard scope",
                },
                {
                    "title": "General Principles of Food Hygiene, CXC 1-1969",
                    "publisher": "FAO and WHO Codex Alimentarius",
                    "url": "https://doi.org/10.4060/cc6125en",
                    "use": "record, allergen cross-contact, hygiene-system, and competent-authority vocabulary",
                },
                {
                    "title": "FGIS Handbooks",
                    "publisher": "United States Department of Agriculture Agricultural Marketing Service",
                    "url": "https://www.ams.usda.gov/publications/content/fgis-pdf-handbooks",
                    "use": "sampling and inspection-documentation vocabulary",
                },
                {
                    "title": "Documents for Good Operating Practice",
                    "publisher": "New Zealand Ministry for Primary Industries",
                    "url": "https://www.mpi.govt.nz/food-business/food-safety-codes-standards/good-operating-practice/documents",
                    "use": "current public allergen-management vocabulary",
                },
                {
                    "title": "Labelling flour fortified with folic acid",
                    "publisher": "New Zealand Ministry for Primary Industries",
                    "url": "https://www.mpi.govt.nz/dmsdocument/56953/direct",
                    "use": "New Zealand flour-labelling context held as vocabulary only",
                },
            ],
            "boundary": (
                "Public-source vocabulary is not empirical validation of the synthetic fixtures, "
                "professional advice, legal interpretation, operational instruction, local approval, "
                "or Maori or affected-party authority."
            ),
        },
    )
    write_json(
        "x1/threat-model.json",
        {
            "schema": "ghc.family.threat-model.v3",
            "owner": OWNER,
            "phase": PHASE,
            "assets": [
                "exact source lineage",
                "x1 before x2 lifecycle",
                "four outcome labels",
                "retained failures",
                "synthetic-only fixtures",
                "route uniqueness",
            ],
            "risks": [
                {"risk": "source drift", "control": "exact commit and fresh live equality"},
                {"risk": "canonical-credit laundering", "control": "retain failed and dependency receipts separately"},
                {"risk": "real food inference", "control": "zero real grain, samples, devices, people, or actions"},
                {"risk": "unit ambiguity", "control": "typed kilograms, grams, and micrometres with explicit domains"},
                {"risk": "release promotion", "control": "release state exact-gated by evidence and competent authority"},
                {"risk": "privacy leakage", "control": "five-class exact owner-delta scanner"},
                {"risk": "accessibility overclaim", "control": "structural checks plus manual and affected-user vacancy"},
                {"risk": "manifest drift", "control": "exact Git-blob manifests and explicit self exclusions"},
                {"risk": "success replay", "control": "one external receipt path and existence lock"},
                {"risk": "duplicate route", "control": "exact-title uniqueness, immediate reread, and duplicate guard"},
            ],
        },
    )
    write_json(
        "x1/method-flow-startup.json",
        {
            "schema": "ghc.family.method-flow-ledger.v3",
            "owner": OWNER,
            "phase": PHASE,
            "stage": "x1_startup",
            "rows": STARTUP_FAILURES,
            "failed_witnesses": len(STARTUP_FAILURES),
            "bounded_passing_witnesses": len(STARTUP_FAILURES),
            "erased_failures": 0,
        },
    )
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "steps": [
                {"step": "activation and source verification", "state": "completed_read_only"},
                {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"},
                {"step": "x2 bounded execution and mutation evidence", "state": "blocked_by_x1_terminal_gate"},
                {"step": "final closeout and exact seal", "state": "pending"},
                {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"},
                {"step": "prospective Ilyra route", "state": "pending_terminal_and_live_authority"},
            ],
            "commit_ceiling": 8,
            "planned_phase_commits": 3,
            "file_rotation_guard": 2000,
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x1.v3",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "THOS Body",
            "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "proposal_rows": {"inherited_zero_credit": 20, "new": 40, "total": 60},
            "expected_outcomes": OUTCOMES,
            "core_truth_labels": CORE_LABELS,
            "proposal_chain": {"before": 5230, "after_if_frozen": 5270},
            "startup_operational_failures": len(STARTUP_FAILURES),
            "x1_completion_credit": 0,
            "x2_execution_started": False,
            "real_world_actions": 0,
            "identity_boundary": IDENTITY_BOUNDARY,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "schema": "ghc.family.route-plan.v3",
            "owner": OWNER,
            "phase": PHASE,
            "prospective_recipient_exact_title": "Ilyra Fen",
            "prospective_phase": "v670-v2",
            "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "successor_contact_count": 0,
            "task_creation_count": 0,
            "substitute_endpoint_count": 0,
            "standby_contact_count": 0,
            "required_gate": "clean pushed exact final plus one successful canonical aggregate and newest live route reread",
        },
    )
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v3",
            "owner": OWNER,
            "phase": PHASE,
            "source_head": head,
            "branch": branch,
            "inherited_rows": len(inherited),
            "new_rows": len(proposals),
            "portfolio_counts": {key: len(value) for key, value in portfolio.items()},
            "external_actions": 0,
            "x2_materialized": False,
        },
    )

    overview = build_overview(inherited, proposals)
    write_text(OWNER_ROOT / "x1" / "integrated-overview.md", overview)

    index_text = f"""# Lyren Moss v670-v1 current family index record

Lyren Moss is the exact relational owner for the planning-only v670-v1 lane on {BRANCH}.
The immutable source is Vesper Arlen v669-v8 at {SOURCE_FINAL}. Vesper's canonical aggregate
failed once and retains zero aggregate-success credit. The dependency-corrected terminal
composite passed once but retains the exact zero-canonical-credit classification. Hamish's
newest live activation selects this existing Lyren Moss task without rewriting Vesper's
historical timeout receipt.

Current state: x1 planning freeze in progress; x2 has not started. Twenty inherited Vesper
rows are integrity evidence only with zero Lyren novelty or completion credit. Forty genuinely
new synthetic grain-milling documentation proposals are frozen for x2, with the planned four-label
distribution 28 completed, 8 represented, 2 open_gap, and 2 exact_gate. The primary pillar is
THOS Body. GMUT Mind and Freed ID/CBR Heart remain explicit and protected.

Prospective route: Ilyra Fen v670-v2, PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED. No successor
contact, task creation, fork, collaboration subagent, standby contact, or substitute endpoint
has occurred. Route resolution is permitted only after Lyren's clean pushed exact final, fresh
four-way equality, one successful owner-scoped canonical aggregate with no replay, newest live
authorization reread, unique exact-title resolution, immediate target reread, and duplicate guard.

Boundary: {IDENTITY_BOUNDARY}

Terminal verdict: NOT_READY_FOR_STAGE_20.
"""
    write_text(
        ROOT / "ghc-family-index" / "references" / "v670-v1-lyren-moss.md",
        index_text,
    )
    write_json("validation/x1-manifest.json", build_manifest())

    summary = {
        "owner": OWNER,
        "phase": PHASE,
        "source": head,
        "inherited": len(inherited),
        "new": len(proposals),
        "outcomes": OUTCOMES,
        "startup_failures": len(STARTUP_FAILURES),
        "overview_words": len(overview.split()),
    }
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
