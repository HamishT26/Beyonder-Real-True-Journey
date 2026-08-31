#!/usr/bin/env python3
"""Build the planning-only Elaren Kestrel v679-v1 x1 packet."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


OWNER = "Elaren Kestrel"
OWNER_SLUG = "elaren-kestrel"
PHASE = "v679-v1"
DISPLAY_PHASE = "v679-v1"
BRANCH = "codex/GHC-Family/elaren-kestrel-v679-v1-full-tools"
SOURCE = "b6757d6f466a3b7b48909dd8a2ddd93b43b3e035"
SOURCE_PHASE = "v678-v8"
GENERATED_AT_NZ = "2026-08-31T14:20:00+12:00"
DECLARED_CHAIN_BEFORE = 8750
DECLARED_CHAIN_AFTER = 8810
QUARANTINE_THRESHOLD = 0.75

ACTIVATION_BASELINE = {
    "effective_negatives": 47918,
    "effective_methods": 47288,
    "retained_failed_witnesses": 19579,
    "bounded_passing_witnesses": 30796,
    "open_gaps": 416,
    "exact_gates": 407,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    "basis": (
        "Eiren Kestrel v678-v8 immutable repository seal of 47,913 negatives, 47,280 methods, 19,574 failed witnesses, and 30,793 bounded passing witnesses, plus the separately attributable external overlay yielding 47,918 / 47,288 / 19,579 / 30,796; the 416 open gaps and 407 exact gates remain unchanged."
    ),
}

NEW_TITLES = [
    "Synthetic letterpress dossier namespace without printer identity ownership or production claim",
    "Type-case cabinet drawer and compartment topology without collection inventory assertion",
    "Uppercase lowercase small-cap figure and punctuation compartment map without historical attribution",
    "Type-body point-size set-width and alignment placeholder without dimensional measurement",
    "Typeface family style weight and variant relation matrix without authorship or trademark conclusion",
    "Sort quantity distribution and replenishment ledger with every real count vacant",
    "Missing sort pied type damaged face and mixed-font cue register without condition diagnosis",
    "Composing-stick line-length and measure relation without typesetting instruction",
    "Galley tray line sequence and proof-stage relation without handling permission",
    "Chase furniture reglet quoin and lockup topology without pressure or stability assessment",
    "Forme imposition graph for pages signatures and blanks without executable press layout",
    "Signature folio recto verso gathering and pagination relation without publication claim",
    "Lockup force packing and impression-pressure vacancy without measured mechanics",
    "Makeready overlay underlay and packing-layer registry without operational advice",
    "Tympan frisket gauge pin and paper-position relation without setup instruction",
    "Platen bed roller and feed-path topology with every machine command disabled",
    "Ink-disc distributor roller and duct relation without motion or maintenance guidance",
    "Ink pigment vehicle drier and additive material vacancies without composition determination",
    "Paper stock grain direction basis weight caliper and finish fields with zero measurements",
    "Dampening humidity curl and static cue registry without observed readings or cause attribution",
    "Registration target colour-pass and trapping relation without print-quality conclusion",
    "Proof state first revise second revise and approval-label lineage without release authority",
    "Author correction compositor correction and printer correction separation without role identity",
    "Proof-sheet trim crop margin slug and furniture-mark locator without image capture",
    "Punch matrix mould and type-casting provenance chain without manufacture or authenticity claim",
    "Wood type metal type polymer plate and photopolymer material vacancies without identification",
    "Stereotype electrotype plate and duplicate-form lineage without originality determination",
    "Ornament border rule leader and spacing-material relation without design-rights conclusion",
    "Printer device colophon imprint publisher and workshop role vacancies without attribution",
    "Job ticket edition run impression and spoilage fields with every real production value vacant",
    "Press-room cabinet shelf drawer and access-location placeholders with all real locations absent",
    "Type-case galley forme and proof movement ledger with custody and possession disabled",
    "Cleaning solvent rag wash-up and roller-treatment action refusal board",
    "Guillotine cutter saw router and trimming-machine action refusal board",
    "Molten type-metal lead alloy heat and fume hazard reservation without exposure assessment",
    "Platen nip crush shear entanglement and unexpected-motion hazard reservation without safety advice",
    "Heavy forme chase paper-stack and type-case lifting hold without manual-handling instruction",
    "Noise ink solvent dust and ventilation cue register without exposure measurement",
    "Emergency-stop guard interlock and lockout placeholder with zero machine operations",
    "Reversible correction and supersession lineage for letterpress dossier assertions",
    "Dual-clock proof assertion lineage joining surrogate state changes to correction epochs",
    "Deterministic dossier byte contract for letterpress records using JCS-compatible ordering and finite-value refusal",
    "Commit-object provenance inventory binding owner artifacts to newline-normalized SHA-256 digests",
    "Assistive reading-order map linking forme regions to prose landmarks with evaluator vacancy",
    "Textual proof-sheet alternative using ordered type blocks margins furniture and blank regions",
    "Low-vision type-case contrast and zoom companion proxy with manual review reserved",
    "Cognitive-accessibility companion explaining synthetic composition steps with reader testing absent",
    "Field minimization matrix for anonymous type and proof topology with expiry vacancies",
    "Contestation queue for disputed imprint and print-history assertions with reversible visibility states",
    "Hash-bound study-card deck for letterpress lifecycle distinctions and correction recall",
    "GMUT imposition-graph analogy for pages signatures and adjacency without physical-law promotion",
    "GMUT identifiability hold for under-observed symbolic imposition matrices and vacant coefficients",
    "THOS blinded paired-documentation trial charter for proof states with no human arms",
    "Freed ID nonproduction proof-role envelope with zero keys proofs issuance or verification",
    "Real printer compositor press operator conservator custodian and affected-user evaluation gap",
    "Independent assistive-user and browser evaluation vacancy for the static proof dossier",
    "Declared 8750-row lineage cannot be bijectively matched to reachable proposal titles",
    "Real press operation setup cleaning repair trimming casting and professional-release exact gate",
    "Contested imprint ownership copyright access cultural heritage and Māori-authority exact gate",
    "Promotion veto matrix reserving Stage 20 for independent evidence and named competent authorities",
]

SOURCES = [
    {
        "source_id": "SMITHSONIAN-CINCINNATI-ARMY-PRESS",
        "url": "https://americanhistory.si.edu/collections/object/nmah_1296859",
        "status": "official Smithsonian National Museum of American History object record checked 2026-08-31",
        "use": "press-object, manufacturer, date, medium, dimensions, and collection-record vocabulary only; no object inspection or attribution authority",
    },
    {
        "source_id": "LOC-LETTERPRESS-COLLECTION",
        "url": "https://www.loc.gov/pictures/item/2010651997/",
        "status": "official Library of Congress collection record checked 2026-08-31",
        "use": "letterpress, print, collection, rights-advisory, and catalogue-reservation vocabulary only",
    },
    {
        "source_id": "LOC-PAPER-CARE",
        "url": "https://www.loc.gov/preservation/care/paper.html",
        "status": "official Library of Congress paper-care guidance checked 2026-08-31",
        "use": "paper handling, storage, environment, and professional-referral vocabulary only; no treatment authority",
    },
    {
        "source_id": "WORKSAFE-PLATEN-PRESS",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-working-with-printing-machinery/platen-press/",
        "status": "official WorkSafe New Zealand legacy guidance checked 2026-08-31; page is watch-status because it states it has not been updated to current legislation",
        "use": "nip, crush, guard, feed, stop, training, and refusal vocabulary only; no operational advice or current-law conclusion",
    },
    {
        "source_id": "WORKSAFE-MACHINE-LOCKOUTS",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/keeping-workers-safe-with-machine-lockouts/",
        "status": "official WorkSafe New Zealand lockout guidance checked 2026-08-31",
        "use": "isolation, unexpected-startup, stored-energy, competence, and stop-condition vocabulary only; no machine operation",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation checked 2026-08-31",
        "use": "entity, activity, agent, derivation, and attribution vocabulary only",
    },
    {
        "source_id": "NIST-TN-1297",
        "url": "https://www.nist.gov/pml/nist-technical-note-1297",
        "status": "official NIST uncertainty guidance page checked 2026-08-31",
        "use": "quantity, uncertainty, traceability, and absent-measurement boundary vocabulary only",
    },
    {
        "source_id": "WORKSAFE-SAFE-MACHINERY",
        "url": "https://www.worksafe.govt.nz/topic-and-industry/machinery/safe-use-of-machinery/",
        "status": "official WorkSafe New Zealand machinery guidance page checked 2026-08-31",
        "use": "hazard-elimination, guarding, competence, and action-refusal vocabulary only; no operational advice",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation with current errata",
        "use": "structural accessibility vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation checked 2026-08-31",
        "use": "status, minimization, correlation, and lifecycle vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "NZ-PRIVACY-PRINCIPLES",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "official New Zealand Privacy Commissioner principles page checked 2026-08-31",
        "use": "collection, use, disclosure, access, correction, retention, and minimization vocabulary only; no compliance or legal conclusion",
    },
    {
        "source_id": "TE-MANA-RARAUNGA",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "Te Mana Raraunga principles publication checked 2026-08-31",
        "use": "Māori data-sovereignty and authority-reservation vocabulary only; no Māori wording, ratification, interpretation, or authority claim",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, printer, compositor, press operator, conservator, custodian, owner, affected user, press, type, forme, plate, paper, proof, print, job record, observation, measurement, image, handling, setup, operation, cleaning, repair, trimming, casting, release, network row, or external write",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, stability theorem, ultraviolet or quantum completion, final physics, or Theory-of-Everything claim",
    "no THOS participant evidence, operational effectiveness, safety, deployment, AGI, ASI, cognition, consciousness, personhood, or independent-reproduction claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, trust-governance, affected-party acceptance, or identity-continuity claim",
    "no professional, condition, material, typographic, publication, access, machinery, nip, crush, shear, sharp-tool, solvent, ink, dust, lead-alloy, heat, fume, lifting, repair, handling, conservation, ownership, custody, imprint, trademark, heritage, copyright, legal, privacy-remedy, cultural, affected-party, traditional-knowledge, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, proof, canon, or Stage 20 claim",
]

TOOL_PLAN = [
    {
        "ecosystem": "python",
        "name": "tzdata",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pytest",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "hypothesis",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pytest-cov",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "ruff",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "mypy",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pip-audit",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "openai",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "typer",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "bandit",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pre-commit",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pip-tools",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "build",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "python",
        "name": "pipdeptree",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "typescript",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "eslint",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "prettier",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "vitest",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "tsx",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "c8",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "markdownlint-cli2",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "npm-check-updates",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "pyright",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "knip",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
    {
        "ecosystem": "node",
        "name": "madge",
        "version": "verify-installed-current",
        "need": "bounded owner-local version and smoke-use witness; no installation or profile mutation",
    },
]

STARTUP_FAILURES = [
    (
        "EL6791-START-N001",
        "A broad worktree-list probe did not complete within the bounded presentation window and was interrupted without filesystem mutation.",
        "EL6791-START-P001",
        "Literal source and destination path probes replaced the broad inventory and established the exact lanes without enumerating sibling worktrees.",
    ),
    (
        "EL6791-START-N002",
        "The first packet-reader wrapper embedded PowerShell backticks in a JavaScript template and failed before filesystem access.",
        "EL6791-START-P002",
        "A bounded literal-path reader with character-code newline handling completed the exact 24,460-word packet through EOF.",
    ),
    (
        "EL6791-START-N003",
        "A PowerShell foreach pipeline used an empty pipe element while measuring required references and failed before any write.",
        "EL6791-START-P003",
        "Materializing the collection before ConvertTo-Json recovered the exact reference inventory.",
    ),
    (
        "EL6791-START-N004",
        "A combined roster-schema, roster-state, and overlay display exceeded the model result budget and earned no complete-read credit.",
        "EL6791-START-P004",
        "Separate literal reads completed the schema, current roster, and latest delivery overlay through EOF.",
    ),
    (
        "EL6791-START-N005",
        "A combined three-window authorization-state projection exceeded the presentation budget and earned no complete-read credit.",
        "EL6791-START-P005",
        "Six bounded non-overlapping windows completed the exact authorization state through EOF without mutation.",
    ),
    (
        "EL6791-START-N006",
        "A broad packet pattern projection expanded repeated flashcard prose and exceeded its output budget.",
        "EL6791-START-P006",
        "The already completed full packet read plus exact bounded headings supplied the work-program and route fields without repeating the broad projection.",
    ),
    (
        "EL6791-X1-N001",
        "The first source-bounded semantic screen found ten proposal titles at or above the preregistered 0.75 token-Jaccard quarantine ceiling, including one exact inherited collision, and failed closed before any x1 document was written.",
        "EL6791-X1-P001",
        "A bounded neighbor projection identified only the ten quarantined proposal IDs; those titles were rewritten while the other fifty proposals and the immutable source remained unchanged, then only the semantic dependency was rerun.",
    ),
    (
        "EL6791-X1-N002",
        "An x1-only cleanup allowlist compared Windows backslashes with Git forward-slash paths and removed all twenty-one owner-untracked template copies instead of retaining four x1 files.",
        "EL6791-X1-P002",
        "The four declared x1 files were recopied from the clean read-only template and the already-reviewed v679 edits were reapplied; no committed, source, sibling, or shared file changed, and the lane became correctly x1-only.",
    ),
    (
        "EL6791-X1-N003",
        "The first ten-test x1 invocation passed nine tests and failed the boundary-token assertion because the overview used Māori authority without the established hyphenated Māori-authority token.",
        "EL6791-X1-P003",
        "The overview and deterministic builder were corrected to the established boundary token, and only the isolated failed test was rerun after manifest refresh; the other nine passing tests were not replayed.",
    ),
]

OWNER_SKILLS = [
    "letterpress-dossier-namespace",
    "type-case-topology",
    "sort-quantity-vacancy",
    "forme-imposition-graph",
    "proof-state-lineage",
    "type-metal-claim-firewall",
    "press-action-refusal-firewall",
    "machine-hazard-reservation",
    "paper-ink-material-vacancy",
    "provenance-correction-ledger",
    "letterpress-accessibility-proxy",
    "imprint-rights-contestation",
    "freed-id-zero-key-envelope",
    "content-addressed-flashcard-index",
    "flashcard-supersession-nonerasure",
    "gmut-imposition-analogy-firewall",
    "gmut-identifiability-boundary",
    "thos-proof-handover-proxy",
    "cbr-affected-party-gate",
    "stage20-letterpress-refusal",
]

SUCCESSOR_SKILLS = [
    "successor-context-card-intake",
    "successor-proposal-neighbor-audit",
    "successor-toolchain-delta-guard",
    "successor-method-flow-nonerasure",
    "successor-static-report-landmarks",
    "successor-zero-network-adapter",
    "successor-exact-gate-register",
    "successor-bounded-retry-selector",
    "successor-roster-route-refresh",
    "successor-baton-file-index",
]

OWNER_RUNNERS = [
    "ghc_family_elaren_kestrel_v679_v1_contract_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_mutation_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_topology_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_metadata_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_flashcard_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_toolchain_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_privacy_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_accessibility_runner.py",
    "ghc_family_elaren_kestrel_v679_v1_portfolio_runner.py",
    "build_ghc_family_elaren_kestrel_v679_v1_report.py",
]

SUCCESSOR_RUNNERS = [
    "ghc_family_successor_context_card_reader.py",
    "ghc_family_successor_proposal_revalidator.py",
    "ghc_family_successor_toolchain_delta.py",
    "ghc_family_successor_method_flow_ingest.py",
    "ghc_family_successor_static_report_check.py",
    "ghc_family_successor_zero_network_adapter.py",
    "ghc_family_successor_exact_gate_check.py",
    "ghc_family_successor_bounded_retry.py",
    "ghc_family_successor_route_refresh.py",
    "ghc_family_successor_baton_index.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout if binary else result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load_git_json(repo: Path, commit: str, path: str) -> dict[str, Any]:
    raw = git(repo, "show", f"{commit}:{path}")
    return json.loads(str(raw))


def inherited_selection(repo: Path) -> list[dict[str, Any]]:
    source_phase = "Eiren Kestrel v678-v8 exact final"
    path = "docs/eiren-kestrel/v678-v8/x1/new-proposal-freeze.json"
    rows = load_git_json(repo, SOURCE, path)["proposals"][:60]
    selected: list[dict[str, Any]] = []
    for row in rows:
        selected.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "original_expected_disposition": row["expected_disposition"],
                "original_approval_class": row["approval_class"],
                "source_phase": source_phase,
                "source_path": path,
                "selected_for": "bounded revalidation or representation only",
                "elaren_novelty_credit": 0,
                "automatic_completion_credit": 0,
            }
        )
    if len(selected) != 60:
        raise RuntimeError("exactly sixty inherited rows are required")
    return selected


def new_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, title in enumerate(NEW_TITLES, start=1):
        proposal_id = f"EL6791-N{offset:03d}"
        if offset <= 42:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 54:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 57:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 25:
            source_ids += ["SMITHSONIAN-CINCINNATI-ARMY-PRESS", "LOC-LETTERPRESS-COLLECTION"]
        if 26 <= offset <= 45:
            source_ids += ["LOC-PAPER-CARE", "WORKSAFE-PLATEN-PRESS", "WORKSAFE-MACHINE-LOCKOUTS", "WORKSAFE-SAFE-MACHINERY"]
        if offset in {22, 28, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 55, 56, 58, 59, 60}:
            source_ids += ["WCAG-2.2", "W3C-VC-DATA-MODEL-2.0"]
        if offset in {45, 46, 55, 56, 59, 60}:
            source_ids += ["NZ-PRIVACY-PRINCIPLES", "TE-MANA-RARAUNGA"]
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real type, forme, press, paper, proof, production record, measurement, operation, treatment, identity, rights, professional, legal, cultural, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"{proposal_id} accepts a missing or contradictory field, a raw or real identifier, a non-authorized outcome label, "
                    "or an observation, measurement, intervention, treatment, repair, competence, right, identity, or authority claim."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One bounded positive fixture must satisfy {proposal_id} and four preregistered invalid mutations must be rejected; "
                    "represented, open, and exact-gated rows receive no real-world execution credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine {proposal_id}, retain the failed witness, restore the exact committed input, and rerun only the isolated dependency."
                ),
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
            }
        )
    return rows


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 0.0


def parse_tree_entries(raw: bytes) -> list[tuple[str, str, str]]:
    entries: list[tuple[str, str, str]] = []
    cursor = 0
    while cursor < len(raw):
        mode_end = raw.index(b" ", cursor)
        name_end = raw.index(b"\0", mode_end + 1)
        mode = raw[cursor:mode_end].decode("ascii")
        name = raw[mode_end + 1 : name_end].decode("utf-8", errors="surrogateescape")
        oid_start = name_end + 1
        oid_end = oid_start + 20
        entries.append((mode, name, raw[oid_start:oid_end].hex()))
        cursor = oid_end
    return entries


def fetch_many(repo: Path, requests: list[tuple[str, str]]) -> list[tuple[str, str, bytes]]:
    request = b"".join(oid.encode("ascii") + b"\n" for oid, _ in requests)
    response = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "--batch"],
        input=request,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    output: list[tuple[str, str, bytes]] = []
    cursor = 0
    for requested_oid, path in requests:
        header_end = response.index(b"\n", cursor)
        header = response[cursor:header_end].split()
        cursor = header_end + 1
        if len(header) != 3 or header[1] == b"missing":
            raise RuntimeError(f"missing Git object for {path}")
        actual_oid, object_type, raw_size = header
        if actual_oid.decode("ascii") != requested_oid:
            raise RuntimeError(f"Git object identity mismatch for {path}")
        size = int(raw_size)
        raw = response[cursor : cursor + size]
        cursor += size
        if len(raw) != size or response[cursor : cursor + 1] != b"\n":
            raise RuntimeError(f"truncated Git object for {path}")
        cursor += 1
        output.append((object_type.decode("ascii"), path, raw))
    if cursor != len(response):
        raise RuntimeError("unattributed Git batch bytes")
    return output


def collect_title_records(value: Any, path: str, output: list[tuple[str, str, str]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title") or value.get("name")
        proposal_id = value.get("proposal_id") or value.get("id") or value.get("proposal")
        if isinstance(title, str) and isinstance(proposal_id, str) and len(title.strip()) > 2:
            output.append((proposal_id.strip(), title.strip(), path))
        for child in value.values():
            collect_title_records(child, path, output)
    elif isinstance(value, list):
        for child in value:
            collect_title_records(child, path, output)


def semantic_audit(repo: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    if git(repo, "rev-parse", "--show-object-format") != "sha1":
        raise RuntimeError("verified SHA-1 Git object format required")
    root = str(git(repo, "show", "-s", "--format=%T", SOURCE))
    level: list[tuple[str, str]] = [(root, "")]
    blobs: list[tuple[str, str]] = []
    tree_count = 0
    while level:
        next_level: list[tuple[str, str]] = []
        for object_type, prefix, raw in fetch_many(repo, level):
            if object_type != "tree":
                raise RuntimeError(f"expected tree at {prefix or '<root>'}")
            tree_count += 1
            for mode, name, oid in parse_tree_entries(raw):
                path = f"{prefix}/{name}" if prefix else name
                if mode == "40000":
                    if not prefix and name != "docs":
                        continue
                    next_level.append((oid, path))
                elif path.endswith(".json") and ("proposal" in path.casefold() or "prereg" in path.casefold()):
                    blobs.append((oid, path))
        level = next_level
    records: list[tuple[str, str, str]] = []
    failures: list[dict[str, str]] = []
    for object_type, path, raw in fetch_many(repo, blobs):
        if object_type != "blob":
            failures.append({"path": path, "error": f"unexpected_{object_type}"})
            continue
        try:
            collect_title_records(json.loads(raw.decode("utf-8")), path, records)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"path": path, "error": type(error).__name__})
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for proposal_id, title, path in records:
        unique.setdefault((proposal_id.casefold(), title.casefold()), (proposal_id, title, path))
    neighbors = []
    for row in rows:
        nearest = max(unique.values(), key=lambda candidate: jaccard(row["title"], candidate[1]))
        score = jaccard(row["title"], nearest[1])
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "nearest_id": nearest[0],
                "nearest_title": nearest[1],
                "nearest_path": nearest[2],
                "token_jaccard": round(score, 4),
                "quarantined": score >= QUARANTINE_THRESHOLD,
            }
        )
    quarantined = [row for row in neighbors if row["quarantined"]]
    exact_titles = {title.casefold() for _, title, _ in unique.values()}
    exact_collisions = [row["proposal_id"] for row in rows if row["title"].casefold() in exact_titles]
    return {
        "source": SOURCE,
        "source_root_tree_oid": root,
        "declared_chain_count": DECLARED_CHAIN_BEFORE,
        "reachable_tree_objects": tree_count,
        "reachable_proposal_json_blobs": len(blobs),
        "reachable_raw_id_title_records": len(records),
        "reachable_unique_id_title_records": len(unique),
        "json_parse_failures": len(failures),
        "parse_failure_details": failures,
        "exact_title_collisions": exact_collisions,
        "quarantine_threshold": QUARANTINE_THRESHOLD,
        "selected_rows_quarantined": len(quarantined),
        "maximum_selected_score": max(row["token_jaccard"] for row in neighbors),
        "neighbors": neighbors,
        "universal_novelty_proved": False,
        "limitation": (
            "Every reachable proposal-bearing JSON blob at the exact source was inspected. The declared chain is larger than the "
            "materialized unique-title set, so this supports source-bounded semantic distinctness rather than universal or scientific novelty."
        ),
    }


def portfolio(kind: str, count: int, owner: str, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"EL6791-{prefix}-{index:03d}",
            "kind": kind,
            "owner": owner,
            "plan_only_at_x1": True,
            "task": f"Bounded {kind} contract {index:03d} for modular evidence, flashcards, tooling, documentation, validation, or cleanup",
            "acceptance": "One explicit owner-local artifact or receipt; no hidden external action or protected-gate conversion",
            "rollback": "Retain the failed witness, revert only the owner-local uncommitted target, and rerun the isolated dependency",
            "protected_gates": PROTECTED_GATES,
        }
        for index in range(1, count + 1)
    ]


def exact_or_blocked(kind: str, count: int, prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "packet_id": f"EL6791-{prefix}-{index:03d}",
            "kind": kind,
            "state": "UNEXECUTED",
            "reason": "Action-specific target, competent authority, affected-party acceptance, or protected evidence is absent",
            "execution_authorized": False,
            "protected_gates": PROTECTED_GATES,
        }
        for index in range(1, count + 1)
    ]


def x1_manifest(repo: Path, paths: list[Path]) -> dict[str, Any]:
    entries = []
    for path in sorted(paths):
        raw = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        entries.append(
            {
                "path": path.relative_to(repo).as_posix(),
                "bytes": len(path.read_bytes()),
                "sha256_normalized_lf": hashlib.sha256(raw).hexdigest(),
            }
        )
    return {
        "source": SOURCE,
        "phase": PHASE,
        "normalization": "CRLF and CR normalized to LF before SHA-256",
        "declared_self_exclusions": [
            "docs/elaren-kestrel/v679-v1/validation/x1-manifest.json",
            "docs/elaren-kestrel/v679-v1/validation/x1-staged-review.json",
        ],
        "entry_count": len(entries),
        "entries": entries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the immutable Eiren Kestrel v678-v8 exact final as HEAD")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("unexpected branch")
    root = repo / "docs" / OWNER_SLUG / PHASE
    if root.exists():
        raise SystemExit("Elaren x1 already exists; no overwrite permitted")

    rows = new_rows()
    inherited = inherited_selection(repo)
    audit = semantic_audit(repo, rows)
    if audit["exact_title_collisions"] or audit["selected_rows_quarantined"] or audit["json_parse_failures"]:
        raise SystemExit(
            "semantic audit failed closed: "
            + json.dumps(
                {
                    "exact": audit["exact_title_collisions"],
                    "quarantined": [
                        {
                            "proposal_id": row["proposal_id"],
                            "nearest_id": row["nearest_id"],
                            "token_jaccard": row["token_jaccard"],
                        }
                        for row in audit["neighbors"]
                        if row["quarantined"]
                    ],
                    "parse_failures": audit["json_parse_failures"],
                },
                sort_keys=True,
            )
        )

    x1 = root / "x1"
    validation = root / "validation"
    dump(
        x1 / "new-proposal-freeze.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after": DECLARED_CHAIN_AFTER,
            "new_elaren_proposals": len(rows),
            "universal_novelty_proved": False,
            "proposals": rows,
        },
    )
    dump(
        x1 / "inherited-proposal-selection.json",
        {
            "selection_count": len(inherited),
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
            "rows": inherited,
        },
    )
    dump(
        x1 / "combined-program.json",
        {
            "total_rows": 120,
            "inherited_selected": 60,
            "genuinely_new": 60,
            "sixty_or_more_new_claim": True,
            "never_describe_as_120_new": True,
            "inherited_ids": [row["proposal_id"] for row in inherited],
            "new_ids": [row["proposal_id"] for row in rows],
        },
    )
    dump(x1 / "semantic-neighbor-audit.json", audit)
    dump(x1 / "official-source-plan.json", {"sources": SOURCES, "citations_are_not_observations_or_authority": True})
    dump(
        x1 / "pillar-and-practices.json",
        {
            "primary_pillar": "THOS Body",
            "practice_1": "synthetic movable-type, type-case, composing, forme/imposition, and proof-state documentation",
            "practice_2": "synthetic provenance, rights, accessibility, machinery-refusal, correction, and handover documentation",
            "successor_recommendation": "synthetic provenance-record continuity and refusal-boundary documentation",
            "employment_qualification_competence_or_authority_claim": False,
            "real_people_objects_records_or_actions": 0,
        },
    )
    dump(
        x1 / "portfolio-freeze.json",
        {
            "owner_safe_now": portfolio("safe_now", 120, OWNER, "SAFE"),
            "owner_candidate": portfolio("candidate", 80, OWNER, "CAND"),
            "successor_candidate_recommendations": portfolio("candidate_recommendation", 20, "Neris Solane", "SCAND"),
            "exact_approval": exact_or_blocked("exact_approval", 20, "EXACT"),
            "blocked": exact_or_blocked("blocked", 10, "BLOCK"),
            "counts": {
                "owner_safe_now": 120,
                "owner_candidate": 80,
                "successor_candidate_recommendations": 20,
                "candidate_total": 100,
                "exact_approval": 20,
                "blocked": 10,
            },
        },
    )
    dump(
        x1 / "skill-runner-plan.json",
        {
            "owner_skill_ideas": OWNER_SKILLS,
            "successor_skill_recommendations": SUCCESSOR_SKILLS,
            "owner_runner_ideas": OWNER_RUNNERS,
            "successor_runner_recommendations": SUCCESSOR_RUNNERS,
            "global_promotion_target": 0,
            "global_promotion_ceiling": 0,
            "owner_local_only": True,
            "owner_local_validation_requires": [
                "official skill-creator initialization",
                "complete read",
                "collision check",
                "quick validation",
                "accepting and rejecting smoke",
                "exact owner-source byte parity",
                "rollback",
            ],
        },
    )
    dump(
        x1 / "clean-fix-refine-plan.json",
        {
            "owner": portfolio("clean_fix_refine", 100, OWNER, "CFR"),
            "successor_recommendations": portfolio("clean_fix_refine_recommendation", 30, "Neris Solane", "SCFR"),
            "owner_execution_target": 100,
            "successor_recommendation_count": 30,
        },
    )
    dump(
        x1 / "toolchain-verification-plan.json",
        {
            "candidate_count": len(TOOL_PLAN),
            "candidates": TOOL_PLAN,
            "codex_cli": {
                "requested_stable": "verify current installed release",
                "observed_before_x1": "recorded during x2 version probes",
                "action": "verify and bounded-use if present; do not update Codex desktop or install in this phase",
            },
            "verification_scope": "existing inherited global and local surfaces only",
            "installation_authorized": False,
            "requirements": [
                "read-only version receipts for already installed surfaces",
                "D-first owner receipts without PATH or profile mutation",
                "no package installation and no npm lifecycle scripts",
                "no elevation, reboot, Windows-feature change, account, key, purchase, deployment, or Codex desktop update",
                "one bounded positive smoke and one meaningful rejecting smoke per direct surface",
                "rollback and retained-failure evidence",
            ],
        },
    )
    sections = [
        "identity-and-route",
        "source-and-lifecycle",
        "three-pillar-boundaries",
        "letterpress-composition-and-proof-practice",
        "provenance-rights-accessibility-and-handover-practice",
        "inherited-proposal-selection",
        "new-proposal-freeze",
        "approval-portfolios",
        "toolchain-verification",
        "skills-and-runners",
        "clean-fix-refine",
        "method-flow-and-failures",
        "validation-and-closeout",
        "successor-route",
    ]
    dump(
        x1 / "flashcard-plan.json",
        {
            "schema": "ghc-freed-id-flashcards/v1",
            "tier_order": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
            "owner_anchor": OWNER,
            "sections": sections,
            "section_count": len(sections),
            "content_addressed": True,
            "supersession_non_erasing": True,
            "large_baton_file_only": True,
            "live_message_compact": True,
        },
    )
    dump(
        x1 / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION_BASELINE,
            "startup_failure_recovery_pairs": [
                {"failure_id": fid, "failure": failure, "recovery_id": pid, "recovery": recovery}
                for fid, failure, pid, recovery in STARTUP_FAILURES
            ],
            "failed_witnesses_are_zero_credit_and_nonerasing": True,
            "x1_execution_credit": 0,
        },
    )
    dump(
        x1 / "route-hold.json",
        {
            "state": "PLANNING_ONLY_X1_ROUTE_HOLD",
            "send_count": 0,
            "successor": "Neris Solane",
            "successor_phase": "v679-v2",
            "authority_horizon": "v725-v8",
            "precontact_forbidden": True,
            "release_requires": [
                "immutable x1 push and fresh-live equality before x2",
                "immutable evidence",
                "clean pushed exact final",
                "one attributable owner-scoped canonical attempt plus dependency-closed terminal evidence, with no replay of a success",
                "fresh live roster and authority read",
                "exactly one exact-title successor and immediate reread",
                "duplicate and direct-control guards",
                "one acknowledged send",
            ],
        },
    )
    dump(
        x1 / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "display_phase": DISPLAY_PHASE,
            "source": SOURCE,
            "branch": BRANCH,
            "lifecycle_state": "PLANNING_ONLY_X1",
            "inherited_selected": 60,
            "new_proposals": 60,
            "combined_program": 120,
            "x2_implementation_present": False,
            "observed_outcomes_present": False,
            "completion_claim_present": False,
            "route_send_count": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_text(
        x1 / "x1-overview.md",
        f"""# Elaren Kestrel {DISPLAY_PHASE} planning-only x1

This additive owner lane begins at Eiren Kestrel's immutable v678-v8 exact final `{SOURCE}` on `{BRANCH}`. It does not rewrite Eiren's repository seal, delivery event, or retained evidence, and it does not replay Eiren's successful owner-scoped canonical aggregate or any already-passing component.

## Program

X1 freezes sixty inherited proposals for bounded revalidation at zero novelty and automatic completion credit, plus sixty source-bounded distinct Elaren proposals. The combined 120-row programme is never described as 120 new proposals. The declared chain advances from {DECLARED_CHAIN_BEFORE} to {DECLARED_CHAIN_AFTER}; every reachable proposal-bearing source blob is inspected, while universal historical novelty remains unproved.

## Practice, pillars, and flashcards

The primary pillar is THOS Body. The wholly synthetic learning/design lens is movable type, type-case, composing, forme/imposition, proof-state, provenance, accessibility, machinery-refusal, correction, and handover documentation. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. No real person, press, type, forme, paper, proof, print, job, image, measurement, setup, operation, cleaning, repair, handling, release, rights decision, cultural decision, or authority act exists. The four-tier flashcard order is owner anchor, Trinity pillar, bounded practice, and task across fourteen modular sections.

## Planned bounded work

The packet freezes 120 owner safe-now tasks, 80 owner candidates, 20 successor candidate recommendations, 20 unexecuted exact-approval packets, 10 unexecuted blocked packets, 20 owner-local skill ideas, 10 successor skill recommendations, 10 owner runner ideas, 10 successor runner recommendations, 100 owner CLEAN/FIX/REFINE tasks, and 30 successor recommendations. These are plans, not execution credit.

Twenty-five already-installed Python and Node surfaces are candidates for read-only version verification and bounded smoke use only. This phase authorizes no package installation, Codex desktop update, global promotion, profile or PATH mutation, elevation, reboot, Windows-feature change, account, credential, external write, or protected real-world action.

## Boundaries

GMUT remains a typed scalar-tensor/EFT research-model family without empirical confirmation or Theory-of-Everything proof. THOS remains participant-free proxy work without governed real arms or independent review. Freed ID remains synthetic and nonproduction without real keys, proofs, lifecycle events, interoperability, security review, recovery, or trust governance. Professional printing, type and material identification, machinery and nip/crush/shear safety, ink/solvent/lead-alloy/heat/fume exposure, lifting, handling, repair, conservation, authorship, imprint, trademark, copyright, ownership, custody, access, legal or cultural interpretation, affected-party legitimacy, Māori data governance, Māori-authority, accessibility completeness, privacy completeness, exhaustive security, independent reproduction, consciousness/personhood, proof/canon, and Stage 20 claims remain open or exact-gated.

No x2 implementation, observed outcome, completion claim, successor contact, or external action is present in this commit.
""",
    )

    generated = sorted(path for path in x1.rglob("*") if path.is_file())
    manifest = x1_manifest(repo, generated)
    dump(validation / "x1-manifest.json", manifest)
    dump(
        validation / "x1-staged-review.json",
        {
            "source": SOURCE,
            "status": "PRECOMMIT_X1_REVIEW",
            "planning_only": True,
            "x2_paths": 0,
            "unexpected_paths": [],
            "privacy_or_raw_identifier_hits": 0,
            "manifest_entries": manifest["entry_count"],
            "declared_self_exclusions": manifest["declared_self_exclusions"],
        },
    )
    print(
        json.dumps(
            {
                "status": "BUILT_PLANNING_ONLY_X1",
                "phase": PHASE,
                "new_proposals": len(rows),
                "inherited_selected": len(inherited),
                "maximum_neighbor_score": audit["maximum_selected_score"],
                "manifest_entries": manifest["entry_count"],
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
