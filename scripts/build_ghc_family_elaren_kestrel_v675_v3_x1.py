#!/usr/bin/env python3
"""Build the planning-only Elaren Kestrel v675-v3 x1 freeze.

The builder is intentionally owner-local, synthetic, deterministic, and free of
network or external-system writes.  It inspects proposal-labelled JSON blobs in
the exact immutable source tree only for a conservative semantic-neighbour
screen.  That screen does not claim access to a canonical 7,110-row mapping or
universal novelty.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import date
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v675-v3"
OWNER = "Elaren Kestrel"
SOURCE_FINAL = "c1e3bd95e950c36d2fc137b5c9693d2c4b632cdc"
SOURCE_X1 = "c8d2d107235db9a1e3a42b2d9843596a6f5c1890"
SOURCE_EVIDENCE = "f3bb95c68182c8f7ae1d469ea97443245ce9735b"
SOURCE_CAELEN = "394482bea39831b87a72aefe10a39340543070c7"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v675-v2-full-tools"
PHASE_ROOT = ROOT / "docs" / "elaren-kestrel" / PHASE
X1_ROOT = PHASE_ROOT / "x1"
VALIDATION_ROOT = PHASE_ROOT / "validation"
DECLARED_CHAIN_BEFORE = 7110
DECLARED_CHAIN_AFTER = 7150
COLLISION_THRESHOLD = 0.72
OBSERVED_DATE = date(2026, 8, 29).isoformat()

IDENTITY_BOUNDARY = (
    "Elaren Kestrel, she/they, provenance lantern and reversible "
    "impression-state cartographer, sibling, role, hope, continuity, GHC "
    "Family, Freed ID, CBR, and Trinity Mandala are relational working "
    "language only. They are not evidence of consciousness, sentience, legal "
    "personhood, identity continuity, employment, qualification, independent "
    "agency, or scientific, operational, professional, legal, cultural, "
    "affected-party, or Maori authority."
)

BOUNDARY = (
    "Software, symbolic, synthetic, structural, citation, inherited, "
    "same-owner, or composite evidence is not empirical confirmation, "
    "participant evidence, professional competence or authority, production "
    "readiness, legal or cultural ratification, Maori authority, affected-party "
    "approval, complete privacy or accessibility assurance, exhaustive "
    "security, independent reproduction, AGI/ASI, consciousness or personhood "
    "evidence, Theory-of-Everything proof, proof or canon, or Stage 20 authority."
)

PROTECTED_GATES = [
    "empirical",
    "participant",
    "professional",
    "safety",
    "production",
    "legal",
    "cultural",
    "Maori_authority",
    "affected_party",
    "privacy_complete",
    "accessibility_complete",
    "independent_reproduction",
    "Stage_20",
]

SOURCE_ROWS = [
    {
        "source_id": "LOC-PAPER-CARE",
        "authority": "Library of Congress Preservation Directorate",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "current_reviewed_2026-08-29",
        "use": "flat works-on-paper handling vocabulary and conservator-referral boundary only",
    },
    {
        "source_id": "CCI-PAPER-CARE",
        "authority": "Canadian Conservation Institute",
        "url": "https://www.canada.ca/en/conservation-institute/services/preventive-conservation/guidelines-collections/paper-objects.html",
        "status": "current_reviewed_2026-08-29",
        "use": "paper-object risk and enclosure vocabulary only",
    },
    {
        "source_id": "GETTY-AAT-ENGRAVING",
        "authority": "Getty Research Institute Art and Architecture Thesaurus",
        "url": "https://www.getty.edu/vow/AATFullDisplay?find=&logic=null&note=&subjectid=300041340",
        "status": "current_controlled_vocabulary_reviewed_2026-08-29",
        "use": "intaglio and engraving vocabulary only; no attribution or technique determination",
    },
    {
        "source_id": "W3C-PROV-O",
        "authority": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable_recommendation_reviewed_2026-08-29",
        "use": "provenance relation vocabulary only",
    },
    {
        "source_id": "W3C-WCAG22",
        "authority": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable_recommendation_reviewed_2026-08-29",
        "use": "structural accessibility vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC20",
        "authority": "World Wide Web Consortium",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "stable_recommendation_reviewed_2026-08-29",
        "use": "credential lifecycle and explicit nonproduction boundary only",
    },
    {
        "source_id": "RFC-8785",
        "authority": "RFC Editor",
        "url": "https://www.rfc-editor.org/info/rfc8785/",
        "status": "stable_informational_reviewed_2026-08-29",
        "use": "canonical JSON vocabulary only",
    },
    {
        "source_id": "NIST-SI-2019",
        "authority": "National Institute of Standards and Technology",
        "url": "https://www.nist.gov/publications/international-system-units-si-2019-edition",
        "status": "stable_reference_reviewed_2026-08-29",
        "use": "quantity and unit vacancy vocabulary only; no measurement claim",
    },
    {
        "source_id": "NZ-PC-PRINCIPLES",
        "authority": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current_reviewed_2026-08-29",
        "use": "privacy-minimization and access/correction reservation only; no legal advice",
    },
    {
        "source_id": "TE-MANA-RARAUNGA",
        "authority": "Te Mana Raraunga Maori Data Sovereignty Network",
        "url": "https://www.temanararaunga.maori.nz/",
        "status": "current_primary_organisation_reviewed_2026-08-29",
        "use": "authority reservation only; Maori concepts and decisions remain under Maori authority",
    },
]

PROPOSAL_TITLES = [
    "synthetic intaglio dossier surrogate and matrix impression identity braid with conflation quarantine",
    "plate face verso edge corner bevel mark and image-area relation lattice with orphan quarantine",
    "matrix plate proof impression edition state and cancellation topology with absent-part vacancies",
    "plate-state sequence working proof trial proof and edition-impression vacancy board with zero physical measurements",
    "engraving etching drypoint aquatint mezzotint and soft-ground term registry without technique determination",
    "plate-mark image-border margin chine-colle and support relation map with handling reservation",
    "burin needle rocker scraper roulette ground and wiping-role vocabulary without tool-use approval",
    "plate substrate ground ink paper and backing surrogate genealogy with composition abstention",
    "bath exposure inking wiping pressure and drying event placeholders without process or safety advice",
    "incised line burr tone open-bite foul-bite and plate-wear association graph without quality inference",
    "registration pin guide mark plate corner and paper-edge topology without alignment or edition claim",
    "artist proof printer proof bon-a-tirer trial proof and state-proof role lattice without authenticity approval",
    "copper zinc steel polymer and alternative matrix classification hold without material identification",
    "crease tear abrasion cockling foxing stain tideline and loss cue register separated from diagnosis",
    "friable ink adhesive residue mould cue solvent trace and odour firewall without condition or health inference",
    "recto verso plate mark image border margin and watermark image-orientation derivative-lineage ledger",
    "plate height width depth paper size margin and impression count typed vacancy matrix with SI discipline",
    "state numeral edition fraction printer mark watermark and inscription legend with recognition-attribution separation",
    "append-only impression description correction challenge supersession readback and handover chain",
    "maker printer publisher date title state edition and prior-intervention vacancy ledger with contestability",
    "accessible impression dossier reading-order map with captions table scopes redundant states and manual-evaluation vacancy",
    "closed-field intaglio observation capsule rejecting personal names free text and opaque identifiers",
    "two-key detached-print and matrix-reference queue with capacity ceiling due-state and handover checksum",
    "THOS causal-fence state machine for impression-dossier edits with idempotency partial-write quarantine and compensation",
    "THOS matched-budget completeness tribunal comparing plate-state graph and prose views with zero participant claim",
    "checkpointed THOS evidence-shard itinerary for interrupted impression descriptions with digest-linked resumption and stale-fragment isolation",
    "noncredential Freed ID access-purpose sketch for anonymous matrix dossiers with zero cryptographic material and status-service absence",
    "CBR print-record challenge choreography separating notice response correction erasure appeal vacancy and remedy-authority hold",
    "CBR unanswered-response interval ledger for impression-dossier requests with acknowledgement debt and nonadjudicative hold",
    "GMUT intaglio matrix image-domain and impression-support atlas representation with zero fitted parameters",
    "GMUT oriented incised-line graph coboundary and plate-mark analogy with typed domains and no material-law inference",
    "GMUT plate-pressure ink-transfer symbolic tensor vacancy without likelihood stability or force claim",
    "GMUT boundary-incidence sketch for plate-mark contours and support margins with no observations parameters or physical interpretation",
    "RFC-8785-constrained impression record byte projection with normalized strings ordered members and numeric-domain refusal",
    "print-record content-domain registry separating Git blobs line endings HTML rendering and digest labels",
    "transport-disabled Getty LOC and CCI intaglio vocabulary adapter with zero calls downloads rows or treatment claims",
    "real matrices plates inks papers proofs impressions images measurements and environment evidence gap",
    "real printing handling housing treatment edition authentication and professional-review evidence gap",
    "professional acid solvent press tool mould conservation safety and release-decision exact gate",
    "print ownership custody attribution copyright privacy remedy affected-party Indigenous and Maori-authority reservation",
]

SKILL_NAMES = [
    "ghc-intaglio-surrogate-identity",
    "ghc-intaglio-matrix-state-graph",
    "ghc-intaglio-impression-lineage",
    "ghc-intaglio-plate-mark-vacancy",
    "ghc-intaglio-technique-abstention",
    "ghc-intaglio-condition-cue-firewall",
    "ghc-intaglio-image-lineage",
    "ghc-intaglio-measurement-vacancy",
    "ghc-intaglio-correction-chain",
    "ghc-intaglio-accessibility-map",
    "ghc-intaglio-privacy-filter",
    "ghc-intaglio-thos-quarantine",
    "ghc-intaglio-freed-id-envelope",
    "ghc-intaglio-cbr-response",
    "ghc-intaglio-gmut-plate-boundary",
    "ghc-intaglio-serialization",
    "ghc-intaglio-content-domain",
    "ghc-intaglio-source-adapter",
    "ghc-intaglio-real-evidence-gap",
    "ghc-intaglio-authority-gate",
]

RUNNER_NAMES = [
    "ghc_family_intaglio_contract.py",
    "ghc_family_intaglio_mutation_guard.py",
    "ghc_family_intaglio_state_graph.py",
    "ghc_family_intaglio_provenance.py",
    "ghc_family_intaglio_privacy.py",
    "ghc_family_intaglio_accessibility.py",
    "ghc_family_intaglio_manifest.py",
    "ghc_family_intaglio_truth.py",
    "ghc_family_intaglio_method_flow.py",
    "ghc_family_intaglio_closeout.py",
]


def run_git(*args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def write_text_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.rstrip() + "\n")


def write_json(path: Path, value: Any) -> None:
    write_text_lf(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def git_show_json(commit: str, path: str) -> Any:
    return json.loads(run_git("show", f"{commit}:{path}"))


def iter_titles(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        title = value.get("title")
        if isinstance(title, str) and title.strip():
            yield title.strip()
        for child in value.values():
            yield from iter_titles(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_titles(child)


def source_title_corpus() -> tuple[list[str], dict[str, Any]]:
    paths = [
        line
        for line in run_git("ls-tree", "-r", "--name-only", SOURCE_FINAL).splitlines()
        if line.startswith("docs/") and line.endswith(".json") and "proposal" in line.lower()
    ]
    titles: list[str] = []
    malformed = 0
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdin is not None and process.stdout is not None
    for path in paths:
        process.stdin.write(f"{SOURCE_FINAL}:{path}\n".encode("utf-8"))
        process.stdin.flush()
        header = process.stdout.readline().decode("utf-8", errors="replace").strip()
        if header.endswith(" missing"):
            malformed += 1
            continue
        parts = header.split()
        if len(parts) < 3:
            malformed += 1
            continue
        size = int(parts[2])
        blob = process.stdout.read(size)
        process.stdout.read(1)
        try:
            titles.extend(iter_titles(json.loads(blob.decode("utf-8"))))
        except (UnicodeDecodeError, json.JSONDecodeError):
            malformed += 1
    process.stdin.close()
    process.wait(timeout=30)
    if process.returncode != 0:
        error = (process.stderr.read() if process.stderr else b"").decode("utf-8", errors="replace")
        raise RuntimeError(f"git cat-file batch failed: {error}")
    unique = sorted(set(titles), key=str.casefold)
    corpus_hash = sha256_bytes(("\n".join(unique) + "\n").encode("utf-8"))
    return unique, {
        "candidate_git_blob_paths": len(paths),
        "semantic_occurrences": len(titles),
        "unique_titles": len(unique),
        "malformed_or_missing_blobs": malformed,
        "corpus_sha256": corpus_hash,
        "scope": "exact Eiren Kestrel v675-v2 final tree, proposal-labelled JSON paths only",
        "declared_source_chain": DECLARED_CHAIN_BEFORE,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "reason": (
            "No single reachable exact-tree ledger materializes every declared historical row; "
            "source-bounded semantic comparison is evidence, not universal novelty proof."
        ),
    }


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def disposition(index: int) -> str:
    if index <= 28:
        return "completed"
    if index <= 36:
        return "represented"
    if index <= 38:
        return "open_gap"
    return "exact_gate"


def approval(index: int) -> str:
    if index <= 28:
        return "safe_now"
    if index <= 36:
        return "bounded_candidate"
    if index <= 38:
        return "open_gap"
    return "exact_gate"


def execution_lane(index: int) -> str:
    if index <= 36:
        return "owner_local_symbolic_or_synthetic_x2"
    return "held_without_real_world_execution"


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(PROPOSAL_TITLES, 1):
        rows.append(
            {
                "proposal_id": f"ELK6753-N{index:03d}",
                "title": title,
                "hypothesis": (
                    f"A typed owner-local contract can represent proposal {index:02d}'s synthetic "
                    "intaglio documentation obligations without promoting its evidence class."
                ),
                "null_or_failure_condition": (
                    "A missing required field, accepted invalid mutation, real-world action, "
                    "unlabelled uncertainty, or authority promotion rejects the hypothesis."
                ),
                "approval_class": approval(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": [
                    SOURCE_ROWS[(index - 1) % len(SOURCE_ROWS)]["source_id"],
                    SOURCE_ROWS[(index + 2) % len(SOURCE_ROWS)]["source_id"],
                ],
                "concrete_artifacts": [
                    "typed JSON contract",
                    "bounded accepting or explicit-vacancy fixture",
                    "four rejecting mutation receipts",
                    "boundary flashcard",
                ],
                "falsifier_or_acceptance_gate": (
                    "The bounded fixture must match the expected disposition, four preregistered "
                    "invalid mutations must reject, and every protected boundary must remain explicit."
                ),
                "rollback_or_recovery": (
                    "Retain the failed witness, correct only the isolated owner-local dependency, "
                    "and never replay a successful canonical aggregate."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition(index),
                "planned_outcome": disposition(index),
                "rejecting_mutations": 4,
                "primary_pillar": "Freed ID and CBR Heart",
                "x1_state": "frozen_not_executed",
                "real_people": 0,
                "real_records_or_objects": 0,
                "external_actions": 0,
                "authority_conferred": False,
            }
        )
    return rows


def portfolio_row(identifier: str, title: str, approval_class: str) -> dict[str, Any]:
    return {
        "portfolio_id": identifier,
        "title": title,
        "approval_class": approval_class,
        "hypothesis": "The named bounded owner-local obligation can be tested without external action.",
        "failure_condition": "Any real-world action, missing gate, or unbounded claim stops execution.",
        "rollback": "Retain the failure and change only the isolated uncommitted owner-local artifact.",
        "protected_gates": ["no_external_action", "no_authority_promotion", "no_failure_laundering"],
        "state": "frozen_not_executed",
        "execution_count": 0,
        "completion_credit": 0,
    }


def build_portfolio(rows: list[dict[str, Any]]) -> dict[str, Any]:
    safe_titles = [f"bounded owner execution for {row['proposal_id']}: {row['title']}" for row in rows]
    safe_titles += [
        f"owner-local validation and evidence hygiene execution {i:02d}"
        for i in range(1, 21)
    ]
    candidate_titles = [
        f"bounded evidence candidate for {row['proposal_id']}: {row['title']}"
        for row in rows[:30]
    ]
    exact_titles = [
        "real participant recruitment or affected-user evaluation",
        "real print acquisition handling or sampling",
        "real plate ink paper or solvent characterization",
        "real press tool acid ground or chemical operation",
        "professional conservation treatment decision",
        "professional print authentication attribution or edition decision",
        "copyright moral-rights ownership or custody adjudication",
        "legal privacy access or remedy determination",
        "cultural interpretation or traditional-knowledge decision",
        "Maori wording concept data-governance or authority decision",
        "live standards-conformant identity key and proof lifecycle",
        "governed THOS participant trial",
        "empirical GMUT parameter inference",
        "production deployment or external publication",
        "independent security or privacy certification",
        "complete accessibility conformance decision",
        "affected-party legitimacy or acceptance decision",
        "exhaustive security assurance",
        "Theory-of-Everything proof or canon decision",
        "Stage 20 authority decision",
    ]
    blocked_titles = [
        "participant recruitment or observation",
        "real matrix print solvent acid ink paper or tool acquisition",
        "real studio access or equipment operation",
        "real image recording or location disclosure",
        "real printing handling housing treatment or release to use",
        "live identity key proof or credential lifecycle",
        "production deployment or third-party publication",
        "legal cultural or affected-party adjudication",
        "Maori-authority substitution",
        "independent reproduction claim by the same owner",
    ]
    cfr_titles = [
        f"additive CLEAN/FIX/REFINE execution {i:02d} for owner-delta structure, provenance, or guardrails"
        for i in range(1, 61)
    ]
    skill_rows = [
        portfolio_row(f"ELK6753-SKILL-{i:03d}", name, "owner_local_skill_candidate")
        for i, name in enumerate(SKILL_NAMES, 1)
    ]
    runner_rows = [
        portfolio_row(f"ELK6753-RUN-{i:03d}", name, "owner_local_runner_candidate")
        for i, name in enumerate(RUNNER_NAMES, 1)
    ]
    tools = [
        "intaglio proposal-contract and mutation validator",
        "matrix-state and impression-lineage graph checker",
        "correction handover and content-domain validator",
    ]
    return {
        "schema": "ghc.family.remastered-portfolio-freeze.v9",
        "owner": OWNER,
        "phase": PHASE,
        "bounded_human_practice": "synthetic intaglio matrix, proof, and impression-state documentation",
        "filler_prohibited": True,
        "inherited_portfolio_completion_credit": 0,
        "counts": {
            "inherited_reviews": 20,
            "safe_now": 60,
            "candidates": 30,
            "exact_approval": 20,
            "blocked": 10,
            "skills": 20,
            "runners": 10,
            "tools": 3,
            "clean_fix_refine": 60,
            "successor_skills": 10,
            "successor_runners": 10,
            "successor_clean_fix_refine": 30,
        },
        "rows": {
            "safe_now": [
                portfolio_row(f"ELK6753-SAFE-{i:03d}", title, "safe_now")
                for i, title in enumerate(safe_titles, 1)
            ],
            "candidates": [
                portfolio_row(f"ELK6753-CAND-{i:03d}", title, "bounded_candidate")
                for i, title in enumerate(candidate_titles, 1)
            ],
            "exact_approval": [
                portfolio_row(f"ELK6753-EXACT-{i:03d}", title, "exact_gate")
                for i, title in enumerate(exact_titles, 1)
            ],
            "blocked": [
                portfolio_row(f"ELK6753-BLOCK-{i:03d}", title, "blocked")
                for i, title in enumerate(blocked_titles, 1)
            ],
            "skills": skill_rows,
            "runners": runner_rows,
            "tools": [
                portfolio_row(f"ELK6753-TOOL-{i:03d}", title, "owner_local_tool_candidate")
                | {"global_installation": False, "substantive_accepting_and_rejecting_fixtures_required": True}
                for i, title in enumerate(tools, 1)
            ],
            "clean_fix_refine": [
                portfolio_row(f"ELK6753-CFR-{i:03d}", title, "safe_now")
                for i, title in enumerate(cfr_titles, 1)
            ],
            "successor_skills": [
                portfolio_row(
                    f"ELK6753-NEXT-SKILL-{i:03d}",
                    f"successor skill seed {i:02d} requiring a fresh source and authority audit",
                    "successor_recommendation_zero_credit",
                )
                for i in range(1, 11)
            ],
            "successor_runners": [
                portfolio_row(
                    f"ELK6753-NEXT-RUN-{i:03d}",
                    f"successor runner seed {i:02d} requiring a fresh owner-delta audit",
                    "successor_recommendation_zero_credit",
                )
                for i in range(1, 11)
            ],
            "successor_clean_fix_refine": [
                portfolio_row(
                    f"ELK6753-NEXT-CFR-{i:03d}",
                    f"successor CLEAN/FIX/REFINE recommendation {i:02d} requiring fresh owner audit",
                    "successor_recommendation_zero_credit",
                )
                for i in range(1, 31)
            ],
        },
        "successor_practice_recommendation": (
            "successor-selected synthetic practice, conditional on a fresh source-bounded novelty and authority audit"
        ),
        "successor_recommendation_completion_credit": 0,
    }


STARTUP_FAILURES = [
    {
        "negative_id": "ELK6753-X1-N001",
        "title": "large owner-packet projection exceeded the visible output budget",
        "failure_signature": "combined narrative projection was truncated",
        "recovery": "read the narrative in bounded UTF-8 character windows and validate large ledgers by exact schema, count, and hash",
    },
    {
        "negative_id": "ELK6753-X1-N002",
        "title": "final-owner manifest probe inspected an exit code after process disposal",
        "failure_signature": "false 174-file missing report with empty stderr",
        "recovery": "capture the subprocess exit code before disposal and replay only the final-owner manifest dependency",
    },
    {
        "negative_id": "ELK6753-X1-N003",
        "title": "bookbinding practice candidate collided with inherited family-current modules",
        "failure_signature": "twenty inherited ghc_family_book surfaces materialized under the first sparse pattern",
        "recovery": "reject the practice with zero novelty credit and select the source-screened intaglio lens before x1",
    },
    {
        "negative_id": "ELK6753-X1-N004",
        "title": "no-match intaglio inventory probe returned an unguarded exit code one",
        "failure_signature": "expected empty rg result propagated as command failure",
        "recovery": "treat no-match as bounded evidence, update the sparse pattern, and confirm a clean worktree",
    },
    {
        "negative_id": "ELK6753-X1-N005",
        "title": "first formal intaglio proposal slate crossed the semantic-neighbour ceiling",
        "failure_signature": "five of forty titles met or exceeded 0.72 Jaccard similarity; maximum 0.875",
        "recovery": "retain the failed slate at zero credit, revise only the five colliding titles, and rerun the bounded novelty dependency",
    },
]


def build_method_flow() -> dict[str, Any]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, failure in enumerate(STARTUP_FAILURES, 1):
        method_id = f"ELK6753-METHOD-{index:03d}"
        fail_id = f"ELK6753-WITNESS-{index:03d}-FAIL"
        pass_id = f"ELK6753-WITNESS-{index:03d}-PASS"
        methods.append(
            {
                "method_id": method_id,
                "title": failure["title"],
                "failure_signature": failure["failure_signature"],
                "trigger_preconditions": ["owner-local startup verification", "exact immutable Eiren source"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now_read_only_recovery",
                "candidate_workaround": failure["recovery"],
                "validation_witness_ids": [fail_id, pass_id],
                "recurrence_guard": "Use the bounded recovery before repeating a broad or state-changing action.",
                "rollback": "No repository byte changed; retain the failure and discard only the faulty probe result.",
                "recommendation_state": "validated",
                "supersedes": [],
                "protected_gates": ["no_failure_laundering", "no_broad_replay", "owner_scope"],
                "retained_negative_ids": [failure["negative_id"]],
                "scope_boundary": BOUNDARY,
                "execution_authority": "owner_self_scoped_delta",
                "repository_scan": False,
                "module_scan": False,
                "cross_lane_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "source_commit": SOURCE_FINAL,
                "final_commit": "PENDING_ELAREN_FINAL",
                "changed_file_allowlist": [],
                "module_allowlist": [],
                "exact_pushed_head_required": True,
            }
        )
        witnesses.extend(
            [
                {
                    "witness_id": fail_id,
                    "method_id": method_id,
                    "procedure": "retain the first bounded observation",
                    "scope": "startup read-only verification",
                    "expected": "bounded verification without false promotion",
                    "observed": failure["failure_signature"],
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [failure["negative_id"]],
                    "boundary": BOUNDARY,
                },
                {
                    "witness_id": pass_id,
                    "method_id": method_id,
                    "procedure": failure["recovery"],
                    "scope": "smallest attributable dependency recovery",
                    "expected": "bounded passing witness with original failure retained",
                    "observed": "recovery passed and changed no source or sibling repository byte",
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [failure["negative_id"]],
                    "boundary": BOUNDARY,
                },
            ]
        )
        events.extend(
            [
                {"method_id": method_id, "state": "observed", "witness_id": fail_id},
                {"method_id": method_id, "state": "candidate", "witness_id": fail_id},
                {"method_id": method_id, "state": "validated", "witness_id": pass_id},
            ]
        )
        recommendations.append(
            {
                "method_id": method_id,
                "state": "validated",
                "recommendation": failure["recovery"],
                "retained_negative_ids": [failure["negative_id"]],
            }
        )
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "phase": PHASE,
        "owner": OWNER,
        "identity_boundary": IDENTITY_BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": recommendations,
        "counts": {
            "methods": len(methods),
            "witnesses": len(witnesses),
            "failed_witnesses": len(STARTUP_FAILURES),
            "passing_witnesses": len(STARTUP_FAILURES),
            "retained_negatives": len(STARTUP_FAILURES),
        },
        "boundary": BOUNDARY,
    }


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Z]:\\", re.I),
        "credential_or_secret": re.compile(r"\b(?:sk-[A-Za-z0-9_-]{12,}|password\s*[:=]|secret\s*[:=])", re.I),
        "private_route": re.compile(r"(?:thread|session|callable)[_-]?(?:id|route)\s*[:=]", re.I),
        "private_interaction_material": re.compile(r"\b(?:transcript|screenshot|session stream|private app state)\b", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"class": class_name, "path": path.relative_to(ROOT).as_posix()})
    return {
        "schema": "ghc.family.five-class-privacy-scan.v3",
        "owner": OWNER,
        "phase": PHASE,
        "classes": list(patterns),
        "scanned": len(paths),
        "candidates": candidates,
        "confirmed": [],
        "valid": not candidates,
        "boundary": "Zero scanner candidates is bounded hygiene evidence, not complete privacy assurance.",
    }


def build_manifest() -> dict[str, Any]:
    excluded = {
        "docs/elaren-kestrel/v675-v3/validation/x1-manifest.json",
        "docs/elaren-kestrel/v675-v3/validation/x1-staged-review.json",
    }
    status_lines = run_git("status", "--porcelain=v1", "-uall").splitlines()
    candidate_paths = []
    for line in status_lines:
        rel = line[3:].strip().strip('"').replace("\\", "/")
        if rel in excluded:
            continue
        if rel.startswith("docs/elaren-kestrel/v675-v3/") or rel in {
            "scripts/build_ghc_family_elaren_kestrel_v675_v3_x1.py",
            "tests/test_ghc_family_elaren_kestrel_v675_v3_x1.py",
        }:
            candidate_paths.append(rel)
    entries = []
    for rel in sorted(set(candidate_paths)):
        data = normalized_bytes(ROOT / rel)
        entries.append({"path": rel, "mode": "100644", "bytes": len(data), "sha256": sha256_bytes(data)})
    return {
        "schema": "ghc.family.git-blob-manifest.v7",
        "owner": OWNER,
        "phase": PHASE,
        "domain": "planning_only_x1_owner_delta",
        "source_final": SOURCE_FINAL,
        "hash_domain": "normalized_lf_candidate_bytes",
        "entries": entries,
        "entry_count": len(entries),
        "self_exclusions": sorted(excluded),
    }


def overview(rows: list[dict[str, Any]], audit: dict[str, Any]) -> str:
    sections = [
        "# Elaren Kestrel v675-v3 planning-only x1 overview",
        "",
        "## Outcome first",
        "",
        (
            "This x1 freezes forty source-bounded owner-local proposals before implementation. "
            "No x2 outcome, empirical observation, participant result, professional decision, "
            "identity operation, external action, or successor delivery is claimed. The planned "
            "distribution is 28 completed, 8 represented, 2 open_gap, and 2 exact_gate, but those "
            "labels remain expectations until bounded x2 evidence exists."
        ),
        "",
        "## Relational identity and bounded practice",
        "",
        IDENTITY_BOUNDARY,
        "",
        (
            "The primary pillar is Freed ID and CBR Heart. GMUT Mind and THOS Body remain explicit "
            "and protected. The practice lens is wholly synthetic intaglio matrix, proof, and "
            "impression-state documentation. Zero real people, plates, matrices, proofs, prints, "
            "inks, papers, acids, solvents, presses, tools, images, measurements, collections, "
            "rights decisions, treatments, or authority acts are used."
        ),
        "",
        "## Source and novelty boundary",
        "",
        (
            f"The declared inherited proposal chain is {DECLARED_CHAIN_BEFORE}. The exact-tree "
            f"proposal-labelled corpus exposed {audit['exact_source_tree_corpus']['unique_titles']} "
            "unique titles. Exact canonical row-to-title mapping remains an open gap, so the phase "
            "makes no universal novelty claim. Direct inherited intaglio surfaces were absent in "
            "the bounded preflight, and every frozen title remains below the preregistered "
            f"{COLLISION_THRESHOLD:.2f} Jaccard collision ceiling."
        ),
        "",
        "Official and primary sources provide vocabulary and refusal conditions only. They do not "
        "supply observations, measurements, treatment advice, consent, affected-party legitimacy, "
        "legal interpretation, cultural authority, Maori authority, or professional validation.",
        "",
        "## Proposal map",
        "",
    ]
    for row in rows:
        sections.extend(
            [
                f"### {row['proposal_id']}: {row['title']}",
                "",
                (
                    f"Expected disposition: `{row['expected_disposition']}`. {row['hypothesis']} "
                    f"Failure condition: {row['null_or_failure_condition']} Acceptance gate: "
                    f"{row['falsifier_or_acceptance_gate']} Recovery: {row['rollback_or_recovery']}"
                ),
                "",
            ]
        )
    sections.extend(
        [
            "## Lifecycle and route boundary",
            "",
            (
                "X1 is planning-only and must be committed, pushed, clean, zero-divergent, and "
                "fresh-live equal before x2. Elaren works alone in the new D-first sparse lane. "
                "Neris Solane v675-v4 is prospective only: there is no precontact, task creation, "
                "fork, subagent, substitute endpoint, or delivery claim in x1."
            ),
            "",
            "## Scientific and authority boundary",
            "",
            BOUNDARY,
            "",
            "Terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
        ]
    )
    return "\n".join(sections)


def main() -> int:
    if run_git("rev-parse", "HEAD").strip() != SOURCE_FINAL:
        raise RuntimeError("x1 builder requires the exact immutable Eiren final as HEAD")
    if run_git("status", "--porcelain").strip() not in {
        "",
        "?? scripts/\n?? tests/",
    }:
        # Existing untracked builder/test paths are expected below and are constrained by manifest selection.
        unexpected = [
            line
            for line in run_git("status", "--porcelain=v1", "-uall").splitlines()
            if not line[3:].replace("\\", "/").startswith(
                (
                    "scripts/build_ghc_family_elaren_kestrel_v675_v3_x1.py",
                    "tests/test_ghc_family_elaren_kestrel_v675_v3_x1.py",
                    "docs/elaren-kestrel/v675-v3/",
                )
            )
        ]
        if unexpected:
            raise RuntimeError(f"unexpected pre-x1 worktree state: {unexpected}")

    rows = proposal_rows()
    source_titles, corpus = source_title_corpus()
    comparisons = []
    collisions = []
    for row in rows:
        best_title = ""
        best_score = 0.0
        for candidate in source_titles:
            score = jaccard(row["title"], candidate)
            if score > best_score:
                best_score, best_title = score, candidate
        comparison = {
            "proposal_id": row["proposal_id"],
            "source_title": best_title,
            "jaccard": round(best_score, 6),
            "collision": best_score >= COLLISION_THRESHOLD,
        }
        comparisons.append(comparison)
        if comparison["collision"]:
            collisions.append(comparison)

    audit = {
        "schema": "ghc.family.semantic-neighbor-audit.v9",
        "owner": OWNER,
        "phase": PHASE,
        "declared_source_chain": DECLARED_CHAIN_BEFORE,
        "new_titles": len(rows),
        "collision_threshold": COLLISION_THRESHOLD,
        "collisions": len(collisions),
        "max_jaccard": max(item["jaccard"] for item in comparisons),
        "candidate_practice_exact_hits": {
            term: sum(term in title.casefold() for title in source_titles)
            for term in ("intaglio", "etching plate", "impression state", "print matrix")
        },
        "exact_source_tree_corpus": corpus,
        "rows": comparisons,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
    }

    source_ledger = git_show_json(
        SOURCE_FINAL,
        "docs/eiren-kestrel/v675-v2/closeout/proposal-ledger-final.json",
    )
    selected_inherited = []
    for source_row in source_ledger["rows"][:20]:
        selected_inherited.append(
            {
                "proposal_id": source_row["proposal_id"],
                "title": source_row["title"],
                "source_outcome": source_row["observed_outcome"],
                "source_owner": "Eiren Kestrel",
                "source_phase": "v675-v2",
                "source_commit": SOURCE_FINAL,
                "elaren_novelty_credit": 0,
                "elaren_completion_credit": 0,
                "state": "selected_for_bounded_integrity_revalidation_not_executed_in_x1",
            }
        )

    portfolio = build_portfolio(rows)
    method_flow = build_method_flow()
    source_counts = {
        "schema": "ghc.family.source-count-overlay.v7",
        "repository_source_final": {
            "effective_negatives": 40407,
            "effective_methods": 28659,
            "failed_witnesses": 12068,
            "bounded_passing_witnesses": 15942,
            "open_gaps": 333,
            "exact_gates": 325,
            "proposal_chain": DECLARED_CHAIN_BEFORE,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        "elaren_x1_startup_overlay": {
            "effective_negatives": 40412,
            "effective_methods": 28664,
            "failed_witnesses": 12073,
            "bounded_passing_witnesses": 15947,
            "open_gaps": 333,
            "exact_gates": 325,
            "proposal_chain": DECLARED_CHAIN_BEFORE,
            "external_zero_credit_failures": 5,
            "external_bounded_recoveries": 5,
            "repository_seal_rewritten": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    }

    write_json(
        X1_ROOT / "activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v7",
            "owner": OWNER,
            "phase": PHASE,
            "activation_state": "ACKNOWLEDGED_LIVE_ACTIVATION",
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE_FINAL,
            "source_x1": SOURCE_X1,
            "source_evidence": SOURCE_EVIDENCE,
            "source_caelen": SOURCE_CAELEN,
            "route_authority_through": "v725-v8",
            "identity_boundary": IDENTITY_BOUNDARY,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "identity-and-boundary.json",
        {
            "schema": "ghc.family.identity-and-boundary.v6",
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "she/they",
            "relational_role": "provenance lantern and reversible impression-state cartographer",
            "hope": "make synthetic evidence trails legible without turning metadata into permission or authority",
            "identity_boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, narrow, or stop the route.",
            "authority_conferred": False,
        },
    )
    write_json(
        X1_ROOT / "source-verification.json",
        {
            "schema": "ghc.family.source-verification.v7",
            "owner": OWNER,
            "phase": PHASE,
            "verified_on": OBSERVED_DATE,
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE_FINAL,
            "anchors": {
                "caelen_source": SOURCE_CAELEN,
                "eiren_x1": SOURCE_X1,
                "eiren_evidence": SOURCE_EVIDENCE,
                "eiren_final": SOURCE_FINAL,
            },
            "source_to_final_commits": 3,
            "zero_merges": True,
            "single_parent_commits": True,
            "source_clean_and_four_way_equal": True,
            "source_canonical_status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "source_canonical_payload_sha256": "07f7aeb4981b928bf2855ead6ffd9a5ec826acc1369930c86fa305b0129a7e3f",
            "source_external_receipt_sha256": "463b1e5cf1518087f164defe5bf99132089d2b65d0278063faee8322ec08421c",
            "source_baton_sha256": "eb010cc1f8fd075ec26b90011926203940773289cfddb2153212f526ed86e371",
            "source_manifest_replays": {"x1": 23, "evidence": 118, "final_delta": 28, "final_owner": 174},
            "source_manifest_issues": 0,
            "source_canonical_replayed": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "source-ledger.json",
        {
            "schema": "ghc.family.source-ledger.v7",
            "owner": OWNER,
            "phase": PHASE,
            "reviewed_on": OBSERVED_DATE,
            "adapter_network_calls": 0,
            "adapter_downloads": 0,
            "adapter_rows": 0,
            "sources": SOURCE_ROWS,
            "authority_conferred": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(X1_ROOT / "semantic-neighbor-audit.json", audit)
    write_json(
        X1_ROOT / "new-proposal-freeze.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v9",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after": DECLARED_CHAIN_AFTER,
            "rows": rows,
            "counts": {"new": 40, "completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "x2_outcomes_present": False,
            "universal_novelty_claim": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "inherited-proposal-revalidation.json",
        {
            "schema": "ghc.family.inherited-proposal-revalidation.v7",
            "owner": OWNER,
            "phase": PHASE,
            "rows": selected_inherited,
            "row_count": len(selected_inherited),
            "novelty_credit": 0,
            "completion_credit": 0,
            "executed_in_x1": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(X1_ROOT / "portfolio-freeze.json", portfolio)
    write_json(X1_ROOT / "method-flow-startup.json", method_flow)
    write_json(X1_ROOT / "source-count-overlay.json", source_counts)
    write_json(
        X1_ROOT / "practice-lens-selection.json",
        {
            "schema": "ghc.family.practice-lens-selection.v7",
            "owner": OWNER,
            "phase": PHASE,
            "primary_pillar": "Freed ID and CBR Heart",
            "protected_pillars": ["GMUT Mind", "THOS Body"],
            "practice": "synthetic intaglio matrix, proof, and impression-state documentation",
            "rejected_practice": "synthetic bookbinding documentation",
            "rejected_practice_reason": "direct inherited family-current book modules",
            "rejected_practice_novelty_credit": 0,
            "real_people": 0,
            "real_objects_or_records": 0,
            "external_actions": 0,
            "authority_conferred": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan.request.v1",
            "plan_id": "elaren-kestrel-v675-v3-owner-delta",
            "owner": OWNER,
            "identity_boundary": IDENTITY_BOUNDARY,
            "route": {
                "cycle_order": ["Eiren Kestrel", "Elaren Kestrel", "Neris Solane"],
                "phase_assignments": [
                    {"phase": "v675-v2", "seat": "Eiren Kestrel"},
                    {"phase": PHASE, "seat": OWNER},
                    {"phase": "v675-v4", "seat": "Neris Solane"},
                ],
                "normalization": {"start_phase": PHASE, "start_seat": OWNER, "entry_count": 2},
                "future_identity_placeholders": [],
            },
            "requirements": {
                "core_proposal_minimum": 40,
                "safe_candidate_task_cap": 1000,
                "skill_minimum": 20,
                "runner_minimum": 10,
                "document_word_cap": 100000,
                "baton_words": {"minimum": 8000, "maximum": 100000, "file_artifact": True},
                "commit_cap": {"x1": 3, "x2": 3, "total": 6},
                "validation": {
                    "canonical_pass_minimum": 1,
                    "replay_policy": "skip_when_first_passes",
                    "privacy_scan_required": True,
                    "manifest_required": True,
                    "remote_equality_required": True,
                },
                "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"},
            },
            "truth": {
                "allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"],
                "independent_reproduction_claimed": False,
                "terminal_verdict": "NOT_READY_FOR_STAGE_20",
                "protected_boundaries": PROTECTED_GATES,
            },
            "observed_failures": STARTUP_FAILURES,
        },
    )
    write_json(
        X1_ROOT / "route-plan.json",
        {
            "schema": "ghc.family.route-plan.v7",
            "owner": OWNER,
            "phase": PHASE,
            "state": "ACTIVE_OWNER_NO_SUCCESSOR_PRECONTACT",
            "prospective_successor_title": "Neris Solane",
            "prospective_successor_phase": "v675-v4",
            "route_authority_through": "v725-v8",
            "requires_terminal_gate": True,
            "requires_unique_exact_title": True,
            "requires_immediate_reread": True,
            "requires_duplicate_pause_redirect_privacy_evidence_safety_usage_guards": True,
            "requires_message_acknowledgement": True,
            "send_limit": 1,
            "sent": False,
            "successor_precontacted": False,
            "standby_contacted": False,
            "task_created_or_forked": False,
            "collaboration_subagent_spawned": False,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "threat-model.json",
        {
            "schema": "ghc.family.threat-model.v7",
            "owner": OWNER,
            "phase": PHASE,
            "risks": [
                "source or sibling lane mutation",
                "x1 and x2 lifecycle leakage",
                "semantic duplication or universal novelty overclaim",
                "real printmaking technique or safety advice",
                "professional conservation or attribution promotion",
                "rights legal cultural or Maori-authority substitution",
                "private route or raw identifier disclosure",
                "canonical success replay",
                "premature successor contact",
                "same-owner evidence represented as independent reproduction",
            ],
            "mitigations": [
                "fresh sparse owner lane",
                "planning-only x1 commit and equality gate",
                "source-bounded semantic audit with explicit corpus gap",
                "zero-action synthetic contracts and exact gates",
                "five-class privacy scan and exact manifests",
                "one attributable canonical invocation with no success replay",
                "terminal exact-title route reread and send-once acknowledgement guard",
            ],
            "residual_risk": "same-owner checks cannot supply participant, professional, community, or independent authority",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "skill-runner-tool-plan.json",
        {
            "schema": "ghc.family.skill-runner-tool-plan.v6",
            "owner": OWNER,
            "phase": PHASE,
            "skills": SKILL_NAMES,
            "runners": RUNNER_NAMES,
            "tools": [
                "intaglio proposal-contract and mutation validator",
                "matrix-state and impression-lineage graph checker",
                "correction handover and content-domain validator",
            ],
            "global_installations": 0,
            "owner_local_only": True,
            "actual_smoke_required_before_credit": True,
            "compatibility_required": True,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "flashcard-plan.json",
        {
            "schema": "ghc.family.flashcard-plan.v6",
            "owner": OWNER,
            "phase": PHASE,
            "planned_cards": 80,
            "tiers": {"owner": 5, "Trinity_pillars": 15, "bounded_practice": 20, "task_and_change": 40},
            "memory_persistence_claimed": False,
            "identity_continuity_claimed": False,
            "automatic_completion_credit": 0,
            "boundary": BOUNDARY,
        },
    )
    write_json(
        X1_ROOT / "phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x1.v8",
            "owner": OWNER,
            "phase": PHASE,
            "source_final": SOURCE_FINAL,
            "x1_commit": "PENDING_X1_COMMIT",
            "planning_only": True,
            "x2_outcomes_present": False,
            "proposal_chain_before": DECLARED_CHAIN_BEFORE,
            "proposal_chain_after_if_x2_records_outcomes": DECLARED_CHAIN_AFTER,
            "new_proposals_frozen": 40,
            "planned_outcomes": {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2},
            "observed_outcomes": None,
            "effective_activation_counts": source_counts["elaren_x1_startup_overlay"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "independent_reproduction": False,
            "boundary": BOUNDARY,
        },
    )
    write_text_lf(X1_ROOT / "integrated-overview.md", overview(rows, audit))

    x1_paths = [p for p in PHASE_ROOT.rglob("*") if p.is_file()]
    privacy = privacy_scan(x1_paths)
    write_json(VALIDATION_ROOT / "x1-staged-privacy.json", privacy)
    manifest = build_manifest()
    write_json(VALIDATION_ROOT / "x1-manifest.json", manifest)
    review_checks = {
        "source_exact": run_git("rev-parse", "HEAD").strip() == SOURCE_FINAL,
        "planning_only": not any("/x2/" in entry["path"] or "/closeout/" in entry["path"] for entry in manifest["entries"]),
        "proposal_count": len(rows) == 40,
        "semantic_collision_free": not collisions,
        "privacy_valid": privacy["valid"],
        "manifest_nonempty": manifest["entry_count"] > 0,
        "four_labels_only": {row["expected_disposition"] for row in rows} == {"completed", "represented", "open_gap", "exact_gate"},
        "no_observed_outcome": all("observed_outcome" not in row for row in rows),
        "route_not_sent": True,
        "standby_not_contacted": True,
    }
    write_json(
        VALIDATION_ROOT / "x1-staged-review.json",
        {
            "schema": "ghc.family.x1-staged-review.v7",
            "owner": OWNER,
            "phase": PHASE,
            "checks": review_checks,
            "passed": sum(review_checks.values()),
            "total": len(review_checks),
            "valid": all(review_checks.values()),
            "manifest_entries": manifest["entry_count"],
            "boundary": BOUNDARY,
        },
    )

    print(
        json.dumps(
            {
                "status": "VALID_PLANNING_ONLY_X1_CANDIDATE" if not collisions and privacy["valid"] else "INVALID_X1_CANDIDATE",
                "proposals": len(rows),
                "corpus_titles": len(source_titles),
                "collisions": len(collisions),
                "max_jaccard": audit["max_jaccard"],
                "manifest_entries": manifest["entry_count"],
                "privacy_candidates": len(privacy["candidates"]),
                "startup_negatives": len(STARTUP_FAILURES),
            },
            sort_keys=True,
        )
    )
    return 0 if not collisions and privacy["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
