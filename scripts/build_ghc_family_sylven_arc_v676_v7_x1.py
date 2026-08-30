#!/usr/bin/env python3
"""Build the deterministic planning-only Sylven Arc v676-v7 x1 packet."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


OWNER = "Sylven Arc"
OWNER_SLUG = "sylven-arc"
PHASE = "v676-v7"
BRANCH = "codex/GHC-Family/sylven-arc-v676-v7-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v676-v6-full-tools"
SOURCE = "b8e8b258876b5af3b3e3247f42ac58dde9a7e6a4"
ELOWEN_SOURCE = "56b4e82909b3d7197b817a2415da592f8fc7df6e"
ELOWEN_X1 = "0943c5da5d4c1aced1ed9a29aca2d18de1c16b26"
ELOWEN_EVIDENCE = "c32fde8ba3aa9518e65f212b8a87d1a108dbc69a"
ELOWEN_FIRST_FINAL = "b37d777b2800372003451d95d3ad5b854ff77d7b"
ELOWEN_CORRECTION_1 = "74a389089cca17558a93c9300af2a4232b3d145e"
ELOWEN_CORRECTION_2 = "674c21f98c115a24d057a71489b759f855b9b69f"
ELOWEN_CORRECTION_3 = "ac724eccb7b21cfad2f2b166d49e12f333cf4b52"
ELOWEN_FINAL = SOURCE
ELOWEN_FAILED_RECEIPT_SHA256 = [
    "95b95bb8c0be81a413e45f72bfe0204d9ed9c92e439f45bc0a50656539c0dbbf",
    "3dc85c6780d59715817f075fba0465ddbe2e21e32dc41c93eaba0ea9b603e09f",
    "1879b71dbc7fb4f5acf9dd7ca841ad927e5a32f1bc199b520dfd06d6f64af544",
]
ELOWEN_CANONICAL_RECEIPT_SHA256 = "7bc57f5a9e4c7895ad74e4f828a38297bd9089f325aec25f3302aa2fbcc2424f"
ELOWEN_CANONICAL_PAYLOAD_SHA256 = "ce08da2ecd0d999f43e77424136bd42a38b3597c8ffad34b23480d5675e4a71b"
GENERATED_DATE = "2026-08-30"

ACTIVATION = {
    "declared_proposals": 7630,
    "effective_negatives": 42666,
    "effective_methods": 33808,
    "retained_failed_witnesses": 14327,
    "bounded_passing_witnesses": 20170,
    "open_gaps": 359,
    "exact_gates": 351,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}

TITLES = [
    "Synthetic marionette namespace without object identity or performance claim",
    "Control-bar component topology with grip and handling abstention",
    "Suspension-string channel graph with tension and vibration measurement vacancy",
    "Crown and head-anchor relation with attachment uncertainty",
    "Shoulder elbow wrist joint topology without range-of-motion claim",
    "Hip knee ankle joint topology without load-bearing claim",
    "Jaw eyelid and mouth control channel without actuation",
    "Crossbar airplane-control and T-bar vocabulary firewall",
    "String-to-control attachment map with knot and fastening vacancy",
    "String-to-body attachment map with anchor-material hold",
    "Cue-to-channel command representation without performance execution",
    "Neutral and rest-pose state contract with zero observation",
    "Slack tangle and break cue register without diagnosis",
    "String numbering and label namespace without real inspection",
    "Marionette material finish paint and adhesive claim hold",
    "Fray crack wear deformation and residue cue register without condition diagnosis",
    "Suspension overhead lifting and rigging safety abstention",
    "Adjustment restringing disassembly and repair-action firewall",
    "Marionette image crop orientation and derivative-lineage contract",
    "Character voice script identity copyright and privacy firewall",
    "Repertoire performance recording and publicity-rights vacancy",
    "Immutable correction lineage with contested cue state and reversible supersession",
    "Accessible control-topology summary with noncolour cues and focus order",
    "Operator-free workload budget ledger with resumable stop token and unresolved queue",
    "Pseudonymous marionette custodian capsule with zero keys and zero proofs",
    "Entity activity agent provenance bundle for zero-object control-channel revisions",
    "JCS-shaped vacancy envelope rejecting NaN Infinity duplicate keys and unstated channels",
    "Metrology firewall for string length tension mass angle and cue timing",
    "GMUT constrained transition graph on synthetic marionette topology",
    "GMUT gauge-relabeling analogy firewall for string-channel identifiers",
    "GMUT coupled-oscillator analogy board without physical-model promotion",
    "Participant-absent THOS comparator plan for blind equal-budget documentation arms",
    "Non-credential pseudonym compartment with vacant status revocation and recovery proofs",
    "Rights-challenge escrow and unresolved remedy ledger for synthetic topology claims",
    "Landmarked HTML topology report with keyboard semantics while human review stays open",
    "Checkpointed deterministic CLI resume token for owner-scoped fixture generation",
    "Zero-network Smithsonian marionette lexicon adapter with rights-aware vacancy",
    "Real marionette observation manipulation professional evaluation and independent-review gap",
    "Competent-person suspension handling serviceability and release authority barrier",
    "Ownership copyright cultural-context affected-party and Māori-authority decision gate",
]

SOURCES = [
    {
        "source_id": "NMAH-TETO-MARIONETTE",
        "url": "https://americanhistory.si.edu/collections/object/nmah_662190",
        "status": "official Smithsonian National Museum of American History object page checked 2026-08-30",
        "use": "marionette, control, and string-count vocabulary only; no media ingestion, object observation, handling, performance, rights, or professional claim",
    },
    {
        "source_id": "NMAH-JACK-MARIONETTE",
        "url": "https://www.americanhistory.si.edu/collections/object/nmah_662194",
        "status": "official Smithsonian National Museum of American History object page checked 2026-08-30",
        "use": "control-bar and multi-string relation vocabulary only; no image reuse, inspection, measurement, treatment, authenticity, or conformance claim",
    },
    {
        "source_id": "LOC-MARIONETTE-RECORD-PHOTOGRAPHS",
        "url": "https://www.loc.gov/item/2005686460/",
        "status": "official Library of Congress catalogue page checked 2026-08-30; record explicitly says rights status of individual images was not evaluated",
        "use": "catalogue, collection, record, access, surrogate, and rights-uncertainty vocabulary only; zero media download or rights determination",
    },
    {
        "source_id": "SMITHSONIAN-OPEN-ACCESS-DEVTOOLS",
        "url": "https://www.si.edu/openaccess/devtools",
        "status": "official Smithsonian developer-tools page checked 2026-08-30",
        "use": "API, metadata, media-limitation, and zero-call adapter vocabulary only; no key creation, call, download, or row ingestion",
    },
    {
        "source_id": "BIPM-VIM",
        "url": "https://www.bipm.org/en/committees/jc/jcgm/publications",
        "status": "official BIPM JCGM publications page checked 2026-08-30",
        "use": "quantity, measurement, indication, uncertainty, and metrological-traceability refusal vocabulary only; zero measurement",
    },
    {
        "source_id": "W3C-PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C Recommendation 30 April 2013",
        "use": "entity, activity, agent, attribution, and derivation vocabulary only",
    },
    {
        "source_id": "WCAG-2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C Recommendation republished 12 December 2024; errata exists",
        "use": "accessible structure and keyboard-interface vocabulary only; no conformance claim",
    },
    {
        "source_id": "W3C-VC-DATA-MODEL-2.0",
        "url": "https://www.w3.org/TR/vc-data-model-2.0/",
        "status": "W3C Recommendation 15 May 2025; errata exists",
        "use": "issuer-holder-verifier, status, minimization, and correlation vocabulary only; zero keys and zero proofs",
    },
    {
        "source_id": "RFC-8785",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "RFC Editor informational RFC, June 2020",
        "use": "deterministic JSON vocabulary only; no production cryptographic assurance",
    },
]

PROTECTED_GATES = [
    "no real person, participant, puppeteer, conservator, registrar, owner, affected user, marionette, control bar, string, joint, stage, script, image, recording, collection, site, observation, measurement, manipulation, performance, repair, custody event, release, network row, or external action",
    "no empirical GMUT datum, likelihood, posterior, force, prediction, parameter constraint, detected effect, ultraviolet completion, quantum completion, or Theory-of-Everything claim",
    "no THOS operational-effectiveness, safety, professional-competence, deployment, AGI, or ASI claim",
    "no production Freed ID key, proof, issuance, resolution, status, revocation, interoperability, recovery, or trust-governance claim",
    "no suspension, lifting, rigging, manipulation, restringing, adjustment, disassembly, repair, treatment, work release, material, condition, authenticity, maker, date, place, character, script, performance, recording, authorship, ownership, custody, copyright, publicity, disclosure, legal, remedy, cultural, affected-party, taonga, mātauranga, Māori-data-governance, or Māori-authority decision",
    "no accessibility-complete, privacy-complete, exhaustive-security, independent-reproduction, consciousness, personhood, proof, canon, or Stage 20 claim",
]

STARTUP_FAILURES = [
    (
        "SA6767-START-N001",
        "The first PowerShell foreach projection was piped without materialization and failed before its read-only probe executed.",
        "SA6767-START-P001",
        "The projection was materialized into a bounded array before serialization; the failed syntax remains zero credit.",
    ),
    (
        "SA6767-START-N002",
        "A second PowerShell foreach projection repeated the empty-pipe parser fault before repository access.",
        "SA6767-START-P002",
        "A scalar property projection recovered the intended read-only state without repeating a mutation.",
    ),
    (
        "SA6767-START-N003",
        "The first external receipt inventory used the same unmaterialized foreach pipeline and failed at parse time.",
        "SA6767-START-P003",
        "A bounded exact receipt-directory inventory verified all four immutable receipt digests and the successful payload digest.",
    ),
    (
        "SA6767-START-N004",
        "The first inherited lifecycle-manifest replay stayed active without attributable completion.",
        "SA6767-START-P004",
        "The process was stopped after recognizing that replaying an already successful Elowen canonical component was forbidden; committed counts and receipt truth were read instead.",
    ),
    (
        "SA6767-START-N005",
        "A narrower inherited lifecycle-manifest replay also stayed active without attributable completion.",
        "SA6767-START-P005",
        "The second process was stopped and no manifest replay was credited; exact committed manifests, exclusions, and canonical receipt totals were read through EOF.",
    ),
    (
        "SA6767-START-N006",
        "A combined source-topology projection returned no visible payload despite making no state change.",
        "SA6767-START-P006",
        "Independent scalar Git probes established exact branch, ancestry, commit count, merge count, and clean state.",
    ),
    (
        "SA6767-START-N007",
        "PowerShell misparsed the unquoted HEAD tree-expression revision before Git could resolve it.",
        "SA6767-START-P007",
        "The exact tree was recovered from the final commit topology record using a parser-safe format.",
    ),
    (
        "SA6767-START-N008",
        "A broad worktree-list projection returned no attributable display within its bounded output contract.",
        "SA6767-START-P008",
        "Exact branch-ref and literal-path probes proved the intended Sylven branch and path were initially absent.",
    ),
    (
        "SA6767-START-N009",
        "A narrowed worktree-list filter likewise produced no attributable display.",
        "SA6767-START-P009",
        "Direct exact branch, path, and later worktree-admin probes replaced the unreliable listing projection.",
    ),
    (
        "SA6767-START-N010",
        "The first worktree-add process created the exact branch ref but stalled before registering the intended directory.",
        "SA6767-START-P010",
        "The stalled process was interrupted; one narrower worktree add reused the exact existing branch and registered the intended D-first path once.",
    ),
    (
        "SA6767-START-N011",
        "A redundant checkout refresh stalled while building the new lane index.",
        "SA6767-START-P011",
        "The redundant process was stopped; exact sparse patterns were retained and a purpose-built sparse-index read replaced it.",
    ),
    (
        "SA6767-START-N012",
        "Host policy rejected the first shell-based stale index-lock cleanup after the stopped checkout.",
        "SA6767-START-P012",
        "The verified owner-local stale lock was removed through the approved patch surface after all owning processes were confirmed stopped.",
    ),
    (
        "SA6767-START-N013",
        "An index-existence probe piped directly from an if expression and hit the PowerShell empty-pipe parser fault.",
        "SA6767-START-P013",
        "The object was assigned before JSON serialization and confirmed the initial index absence.",
    ),
    (
        "SA6767-START-N014",
        "A combined index and status projection encountered the absent index and then left a long-running status process.",
        "SA6767-START-P014",
        "The exact process tree was identified and stopped before the sparse index was built; its stale lock was preserved until safe cleanup.",
    ),
    (
        "SA6767-START-N015",
        "A standalone pre-index status probe exceeded its response window and produced no complete status.",
        "SA6767-START-P015",
        "The exact status process was interrupted and no cleanliness credit was taken from it.",
    ),
    (
        "SA6767-START-N016",
        "The first patch-based lock cleanup failed because a separate earlier status process still held the owner-local file.",
        "SA6767-START-P016",
        "The lingering exact process tree was found and stopped, after which the same verified stale lock was removed once.",
    ),
    (
        "SA6767-START-N017",
        "The first full sparse-index materialization crossed multiple response windows before completion.",
        "SA6767-START-P017",
        "The single process was monitored without replay and completed successfully; the clean exact-source sparse lane was then verified.",
    ),
    (
        "SA6767-START-N018",
        "A later source-window projection repeated the PowerShell foreach empty-pipe parser fault before reading the owned file.",
        "SA6767-START-P018",
        "The range objects were materialized before serialization and all requested windows were then read without repository mutation.",
    ),
    (
        "SA6767-START-N019",
        "The first patch-composition wrapper treated Markdown backticks as JavaScript delimiters and failed before the patch tool was called.",
        "SA6767-START-P019",
        "The same bounded text edit was composed with escaped delimiters and applied once through the approved patch surface.",
    ),
    (
        "SA6767-START-N020",
        "The first combined manifest-and-test scaffold wrapper treated a completed source read as an error and aborted before adding either file.",
        "SA6767-START-P020",
        "Each exact scaffold was read and added separately through the approved patch surface, with no inherited file modified.",
    ),
    (
        "SA6767-X1-N001",
        "The inherited full-tree semantic-audit transport crossed the five-minute attribution window and was stopped before writing any x1 artifact.",
        "SA6767-X1-P001",
        "The audit transport was replaced with an exact Git-object tree walker that prunes outside docs while preserving the same source and quarantine contract.",
    ),
    (
        "SA6767-X1-N002",
        "The first proposed Git ls-tree pathspec recovery used unsupported glob magic and was rejected before traversal.",
        "SA6767-X1-P002",
        "The unsupported command receives no audit credit; the exact Git-object walker applies filename filtering after decoding committed tree entries.",
    ),
    (
        "SA6767-X1-N003",
        "A docs-only recursive ls-tree recovery also crossed the five-minute attribution window and was stopped without a complete path inventory.",
        "SA6767-X1-P003",
        "Level-batched Git-object reads replace recursive formatted enumeration and retain exact commit-tree provenance.",
    ),
    (
        "SA6767-X1-N004",
        "The first Git-object walker used batches large enough for Windows pipe backpressure to deadlock producer and consumer before any x1 write.",
        "SA6767-X1-P004",
        "The isolated transport dependency was corrected to eight-object batches so each request set fits before exact payload reads begin.",
    ),
    (
        "SA6767-X1-N005",
        "Eight-object Git batches retained the same flat producer-consumer backpressure signature on this Windows pipe.",
        "SA6767-X1-P005",
        "The exact object transport was reduced to one request followed by one complete response, eliminating bidirectional pipe contention.",
    ),
    (
        "SA6767-X1-N006",
        "One-object interactive transport removed hard backpressure but still exceeded the five-minute attribution window under per-object pipe latency.",
        "SA6767-X1-P006",
        "Noninteractive communicate-managed batches now write complete request sets and consume complete responses without bidirectional deadlock.",
    ),
    (
        "SA6767-X1-N007",
        "Deadlock-safe 256-object batches progressed but paid the repository's high cat-file startup cost repeatedly and were stopped before x1 output.",
        "SA6767-X1-P007",
        "Each complete tree level and the full filtered blob set now use one communicate-managed process, preserving exact responses while removing repeated startup cost.",
    ),
    (
        "SA6767-X1-N008",
        "The first completed semantic tribunal failed closed with two exact title collisions and ten rows at or above the 0.75 quarantine threshold.",
        "SA6767-X1-P008",
        "An isolated diagnostic named all ten nearest inherited rows; only those titles were rewritten while source, fields, and the 0.75 gate stayed fixed.",
    ),
    (
        "SA6767-X1-N009",
        "The first staged x1 diff-hygiene check rejected one extra blank line at the end of the manifest builder.",
        "SA6767-X1-P009",
        "Only the trailing blank line was removed; Method Flow and the exact staged manifest were regenerated for the changed target before commit.",
    ),
    (
        "SA6767-X1-N010",
        "The first post-hygiene builder recovery rejected its own exact staged Sylven x1 packet because preflight allowed only untracked scaffolds.",
        "SA6767-X1-P010",
        "Preflight was narrowed to accept only exact owner x1 paths, its two transient validation outputs, and the three declared x1 code surfaces.",
    ),
    (
        "SA6767-X1-N011",
        "The changed x1 test target then failed 12 of 13 because Method Flow still contained the pre-recovery count.",
        "SA6767-X1-P011",
        "After the bounded builder recovery refreshed Method Flow, only the changed x1 selection was rerun and all 13 tests passed.",
    ),
    (
        "SA6767-X1-N012",
        "The dependency-corrected x1 builder crossed its 30-second response window without returning a process handle while its original process continued.",
        "SA6767-X1-P012",
        "A read-only process audit and bounded wait observed the original process complete; no duplicate builder invocation was made.",
    ),
    (
        "SA6767-X1-N013",
        "The first persisted-state probe guessed two obsolete x1 artifact names and therefore found neither file.",
        "SA6767-X1-P013",
        "Bounded owner-directory enumeration recovered the actual generated filenames and staged-state evidence without changing the packet.",
    ),
]

SKILLS = [
    "synthetic-marionette-namespace",
    "control-bar-topology",
    "string-channel-vacancy",
    "joint-relation-abstention",
    "cue-command-separation",
    "rest-pose-observation-firewall",
    "string-label-privacy-filter",
    "material-condition-claim-hold",
    "marionette-image-lineage",
    "performance-rights-vacancy",
    "marionette-metrology-vacancy",
    "rigging-safety-reservation",
    "repair-action-hold",
    "marionette-provenance-braid",
    "accessible-marionette-summary",
    "marionette-workload-handover",
    "zero-key-marionette-custodian",
    "gmut-marionette-analogy-firewall",
    "thos-zero-person-proxy-guard",
    "maori-authority-reservation",
]

RUNNERS = [
    "ghc_family_sylven_arc_v676_v7_proposal_contracts.py",
    "ghc_family_sylven_arc_v676_v7_positive_controls.py",
    "ghc_family_sylven_arc_v676_v7_mutation_rejector.py",
    "ghc_family_sylven_arc_v676_v7_marionette_topology.py",
    "ghc_family_sylven_arc_v676_v7_measurement_vacancy.py",
    "ghc_family_sylven_arc_v676_v7_provenance.py",
    "ghc_family_sylven_arc_v676_v7_privacy.py",
    "ghc_family_sylven_arc_v676_v7_rights_accessibility.py",
    "ghc_family_sylven_arc_v676_v7_portfolio.py",
    "build_ghc_family_sylven_arc_v676_v7_report.py",
]


def git(repo: Path, *args: str, binary: bool = False) -> str | bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8").strip()


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for offset, title in enumerate(TITLES, start=1):
        proposal_id = f"SA6767-N{offset:03d}"
        if offset <= 28:
            disposition, approval, lane = "completed", "safe_now", "owner_local_zero_row_synthetic"
        elif offset <= 36:
            disposition, approval, lane = "represented", "candidate", "represented_proxy_only"
        elif offset <= 38:
            disposition, approval, lane = "open_gap", "candidate", "external_evidence_vacancy"
        else:
            disposition, approval, lane = "exact_gate", "exact_approval", "competent_authority_reserved"
        source_ids = ["W3C-PROV-O", "RFC-8785"]
        if offset <= 21 or offset in {26, 29, 30, 31, 37, 38, 39}:
            source_ids.extend(["NMAH-TETO-MARIONETTE", "NMAH-JACK-MARIONETTE"])
        if offset in {19, 20, 21, 37, 39, 40}:
            source_ids.append("LOC-MARIONETTE-RECORD-PHOTOGRAPHS")
        if offset == 37:
            source_ids.append("SMITHSONIAN-OPEN-ACCESS-DEVTOOLS")
        if offset in {3, 13, 28, 31, 38, 39}:
            source_ids.append("BIPM-VIM")
        if offset in {19, 23, 35}:
            source_ids.append("WCAG-2.2")
        if offset in {20, 21, 22, 25, 33, 34, 39, 40}:
            source_ids.append("W3C-VC-DATA-MODEL-2.0")
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A deterministic zero-row owner-local contract can represent {title.lower()} while refusing "
                    "real object, measurement, treatment, identity, rights, professional, legal, cultural, or authority claims."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract accepts a missing or contradictory field, ingests a real identifier, "
                    "uses an unauthorized outcome, or implies an observation, intervention, result, competence, right, or authority grant."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": sorted(set(source_ids)),
                "concrete_artifacts": [
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/contracts/{proposal_id}.json",
                    f"docs/{OWNER_SLUG}/{PHASE}/x2/evidence/{proposal_id}-receipt.json",
                ],
                "falsifier_or_acceptance_gate": (
                    f"One positive zero-row fixture must satisfy {proposal_id} and four preregistered invalid mutations "
                    "must be rejected; represented, open, and exact-gated rows receive no executed-real-world credit."
                ),
                "rollback_or_recovery": (
                    f"Quarantine the {proposal_id} output, retain the failed witness, restore the last exact Git-blob "
                    "input, and rerun only the isolated dependency after an additive correction."
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


def collect_records(value: Any, path: str, output: list[tuple[str, str, str]]) -> None:
    if isinstance(value, dict):
        title = value.get("title") or value.get("proposal_title") or value.get("name")
        proposal_id = value.get("proposal_id") or value.get("id") or value.get("proposal")
        if isinstance(title, str) and isinstance(proposal_id, str) and len(title.strip()) > 2:
            output.append((proposal_id.strip(), title.strip(), path))
        for child in value.values():
            collect_records(child, path, output)
    elif isinstance(value, list):
        for child in value:
            collect_records(child, path, output)


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


def reachable_semantic_audit(repo: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    if git(repo, "rev-parse", "--show-object-format") != "sha1":
        raise SystemExit("semantic tree walker currently requires the verified SHA-1 repository object format")
    root_oid = str(git(repo, "show", "-s", "--format=%T", SOURCE))

    def fetch_many(requests: list[tuple[str, str]]) -> list[tuple[str, str, bytes]]:
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
                raise RuntimeError(f"missing or malformed Git object header for {path}")
            actual_oid, object_type, raw_size = header
            if actual_oid.decode("ascii") != requested_oid:
                raise RuntimeError(f"Git object identity mismatch for {path}")
            size = int(raw_size)
            raw = response[cursor : cursor + size]
            cursor += size
            if len(raw) != size or response[cursor : cursor + 1] != b"\n":
                raise RuntimeError(f"truncated Git object payload for {path}")
            cursor += 1
            output.append((object_type.decode("ascii"), path, raw))
        if cursor != len(response):
            raise RuntimeError("unattributed trailing bytes in Git object batch")
        return output

    items: list[tuple[str, str]] = []
    tree_count = 0
    level: list[tuple[str, str]] = [(root_oid, "")]
    while level:
        next_level: list[tuple[str, str]] = []
        for object_type, prefix, raw in fetch_many(level):
            if object_type != "tree":
                raise RuntimeError(f"expected tree object at {prefix or '<root>'}")
            tree_count += 1
            for mode, name, oid in parse_tree_entries(raw):
                path = f"{prefix}/{name}" if prefix else name
                if mode == "40000":
                    if not prefix and name != "docs":
                        continue
                    next_level.append((oid, path))
                    continue
                lowered = path.casefold()
                if path.endswith(".json") and ("proposal" in lowered or "prereg" in lowered):
                    items.append((oid, path))
        level = next_level

    records: list[tuple[str, str, str]] = []
    failures = []
    for object_type, path, blob in fetch_many(items):
        if object_type != "blob":
            failures.append({"path": path, "error": f"unexpected_{object_type}"})
            continue
        try:
            collect_records(json.loads(blob.decode("utf-8")), path, records)
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            failures.append({"path": path, "error": type(error).__name__})
    unique: dict[tuple[str, str], tuple[str, str, str]] = {}
    for proposal_id, title, path in records:
        unique.setdefault((proposal_id.casefold(), title.casefold()), (proposal_id, title, path))
    neighbors = []
    for row in rows:
        nearest = max(unique.values(), key=lambda candidate: jaccard(row["title"], candidate[1]))
        neighbors.append(
            {
                "proposal_id": row["proposal_id"],
                "title": row["title"],
                "nearest_id": nearest[0],
                "nearest_title": nearest[1],
                "nearest_path": nearest[2],
                "token_jaccard": round(jaccard(row["title"], nearest[1]), 4),
            }
        )
    maximum = max(row["token_jaccard"] for row in neighbors)
    return {
        "source_tree": SOURCE,
        "source_root_tree_oid": root_oid,
        "reachable_tree_objects": tree_count,
        "declared_chain_count": ACTIVATION["declared_proposals"],
        "reachable_proposal_json_blobs": len(items),
        "reachable_raw_id_title_records": len(records),
        "reachable_unique_id_title_records": len(unique),
        "json_parse_failures": len(failures),
        "parse_failure_details": failures,
        "quarantine_threshold": 0.75,
        "maximum_selected_score": maximum,
        "selected_rows_quarantined": sum(row["token_jaccard"] >= 0.75 for row in neighbors),
        "exact_title_collisions": sum(row["token_jaccard"] == 1.0 for row in neighbors),
        "neighbors": neighbors,
        "limitation": (
            "This is a direct audit of every reachable proposal-bearing JSON artifact at the exact immutable source tree. "
            "It supports bounded semantic distinctness but is not a universal novelty proof and does not establish scientific novelty."
        ),
    }


def mutation_plan(rows: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    mutation_types = [
        ("missing_hypothesis", "required hypothesis omitted"),
        ("unknown_outcome_label", "outcome outside the four-label vocabulary"),
        ("authority_escalation", "synthetic record claims real-world authority"),
        ("real_identifier_or_measurement", "a raw identifier or ungrounded measurement is introduced"),
    ]
    return [
        {
            "mutation_id": f"{row['proposal_id']}-M{index}",
            "proposal_id": row["proposal_id"],
            "mutation_kind": kind,
            "expected_rejection": reason,
            "execution_status": "preregistered_unexecuted_x1",
        }
        for row in rows
        for index, (kind, reason) in enumerate(mutation_types, start=1)
    ]


SAFE_SUPPORT = [
    "Validate the four-label vocabulary and reject aliases before any x2 outcome is written",
    "Freeze the source firewall that distinguishes citations from observations and authority",
    "Freeze the zero-call Smithsonian adapter configuration with no credentials or rows",
    "Specify normalized-LF JSON and Markdown emission for deterministic manifests",
    "Specify the owner-only privacy scanner and its scanner-definition adjudication allowlist",
    "Specify the exact staged allowlist for the planning and evidence lifecycles",
    "Define recovery pairing so no bounded pass can erase a failed witness",
    "Define the x1-to-x2 lifecycle guard and reject premature implementation paths",
    "Define the open-gap register for real observation and specialist evaluation",
    "Define the exact-gate register for rigging safety rights culture and Māori authority",
    "Define the zero-key zero-proof Freed ID profile and reject live identity events",
    "Define the THOS zero-person protocol and reject participant or operator claims",
    "Define the GMUT analogy firewall and reject empirical parameter or force claims",
    "Define accessible HTML structure while reserving manual and affected-user evaluation",
    "Define the workload pause stop and resumable handover state machine",
    "Define a no-media fixture policy for collection and performance records",
    "Define a rights-uncertainty field that cannot be converted into permission",
    "Define a correction supersession braid with immutable prior-state references",
    "Define a rollback packet for every owner-local generated artifact",
    "Define exact owner-scope and file-count ceilings before evidence materialization",
]

EXACT_GATE_TASKS = [
    "Handle or manipulate a real marionette or control bar",
    "Suspend lift rig or load a real marionette",
    "Measure real string length tension mass angle motion or timing",
    "Diagnose real wear fray cracking deformation or material condition",
    "Adjust restring disassemble repair clean lubricate or treat a real object",
    "Approve real work release display operation or performance readiness",
    "Assert professional puppetry conservation registration or rigging competence",
    "Determine title ownership custody provenance accession or deaccession",
    "Determine copyright script recording performance publicity or image permissions",
    "Publish or ingest protected real-person identity or contact data",
    "Issue resolve suspend revoke or recover a real Freed ID credential",
    "Claim WCAG conformance without manual and affected-user evaluation",
    "Claim privacy completeness or exhaustive security without independent review",
    "Run participant or operator THOS trials without governance and monitoring",
    "Promote a GMUT analogy into a physical prediction or empirical constraint",
    "Interpret cultural significance traditional knowledge or sacred context",
    "Choose Māori wording or apply tikanga without Māori authority",
    "Govern Māori data without tangata whenua iwi hapū and Māori authority",
    "Make a legal remedy affected-party legitimacy or public-policy decision",
    "Promote this same-owner synthetic phase to Stage 20 proof canon AGI or ASI",
]

BLOCKED_TASKS = [
    "Call the Smithsonian API without an exact approved key target budget and rollback",
    "Download or republish collection media without item-specific rights review",
    "Create real participant recruitment records or consent materials",
    "Create production keys credentials tokens or identity lifecycle events",
    "Make purchases deployments publications or third-party writes",
    "Elevate privileges weaken host security or change Windows features",
    "Update Codex desktop or install unrelated host software",
    "Mutate an inherited sibling branch worktree receipt or sealed artifact",
    "Contact a successor before Sylven exact-final terminal validation",
    "Erase failed canonical receipts negative witnesses open gaps or exact gates",
]

CFR_SUPPORT = [
    "Normalize all owner JSON to deterministic UTF-8 and trailing-newline form",
    "Replace owner-version-locked call sites with family-current compatible names where bounded",
    "Check every generated path against the Sylven sparse owner allowlist",
    "Check every artifact for private absolute paths and raw task-route material",
    "Check every artifact for credentials tokens keys and assignment-like secrets",
    "Check every artifact for unsupported empirical or authority language",
    "Check every source citation for vocabulary-only status and nonconversion wording",
    "Check every Method Flow recovery for its retained failed-witness link",
    "Check every exact-gate and blocked packet remains visibly unexecuted",
    "Check every candidate row remains bounded to represented proxy evidence",
    "Check every core outcome uses exactly one authorized label",
    "Check all forty proposal identifiers and four mutation identifiers remain unique",
    "Check local skills remain owner-local and are not globally promoted",
    "Check family-current runners accept valid and reject invalid fixtures",
    "Check accessible report headings landmarks tables links and text alternatives structurally",
    "Check manual browser assistive-technology cognitive and affected-user reviews remain reserved",
    "Check x1 manifests contain no x2 implementation or observed outcome",
    "Check evidence manifests exclude final closeout and route claims",
    "Check final manifests use normalized Git blobs with declared self-exclusions",
    "Check the terminal route remains prepared and unsent until live reread",
]

SUCCESSOR_SUPPORT = [
    "Re-audit inherited proposal recommendations for current novelty and protected gates",
    "Retain every Sylven failure as zero-credit successor evidence",
    "Select a distinct primary pillar and synthetic human-practice lens",
    "Keep x1 planning-only and prove remote equality before x2",
    "Use owner-self-scoped dependency-closed validation only",
    "Build and smoke-use only a useful owner-local subset of skills and runners",
    "Carry open gaps and exact gates without promotion",
    "Use current primary sources as vocabulary rather than observation or authority",
    "Prepare a sanitized file-backed baton with no private identifiers or paths",
    "Refresh the live roster and send at most one acknowledged terminal edge",
]


def safe_descriptions() -> list[str]:
    return [
        f"Prepare a positive zero-row fixture and four rejection predicates for {title}"
        for title in TITLES
    ] + SAFE_SUPPORT


def candidate_descriptions() -> list[str]:
    return [
        f"Represent a proxy-only comparison design with explicit missing real-world evidence for {title}"
        for title in TITLES[:30]
    ]


def cfr_descriptions() -> list[str]:
    return [
        f"Review schema fields source status rollback protected gates and outcome discipline for {title}"
        for title in TITLES
    ] + CFR_SUPPORT


def planned_rows(prefix: str, descriptions: list[str], status: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"{prefix}-{index:03d}",
            "description": description,
            "status": status,
            "real_world_rows": 0,
            "external_actions": 0,
        }
        for index, description in enumerate(descriptions, start=1)
    ]


def startup_methods() -> list[dict[str, Any]]:
    methods = []
    for failed_id, failed_description, pass_id, pass_description in STARTUP_FAILURES:
        methods.append(
            {
                "method_id": failed_id,
                "description": failed_description,
                "recovered_by": pass_id,
                "state_change": False,
                "status": "failed_zero_credit",
                "truth": False,
            }
        )
        methods.append(
            {
                "method_id": pass_id,
                "description": pass_description,
                "failed_witness_preserved": failed_id,
                "status": "bounded_pass",
                "truth": True,
            }
        )
    return methods


def build(repo: Path) -> None:
    if git(repo, "rev-parse", "HEAD") != SOURCE:
        raise SystemExit("x1 builder requires the exact immutable corrected Elowen source head")
    if git(repo, "branch", "--show-current") != BRANCH:
        raise SystemExit("x1 builder requires the exact Sylven owner branch")
    allowed_code = {
        "scripts/build_ghc_family_sylven_arc_v676_v7_x1.py",
        "scripts/ghc_family_sylven_arc_v676_v7_x1_manifest.py",
        "tests/test_ghc_family_sylven_arc_v676_v7_x1.py",
    }
    allowed_validation = {
        "docs/sylven-arc/v676-v7/validation/x1-manifest.json",
        "docs/sylven-arc/v676-v7/validation/x1-staged-review.json",
    }
    unexpected = []
    for line in str(git(repo, "status", "--porcelain=v1")).splitlines():
        path = line[3:].replace("\\", "/")
        if (
            path not in allowed_code
            and path not in allowed_validation
            and not path.startswith("docs/sylven-arc/v676-v7/x1/")
        ):
            unexpected.append(line)
    if unexpected:
        raise SystemExit("unexpected pre-x1 worktree state: " + repr(unexpected))

    base = repo / "docs" / OWNER_SLUG / PHASE / "x1"
    rows = proposal_rows()
    audit = reachable_semantic_audit(repo, rows)
    if audit["json_parse_failures"] or audit["selected_rows_quarantined"] or audit["exact_title_collisions"]:
        raise SystemExit("semantic audit did not satisfy the preregistration gate")

    methods = startup_methods()
    failure_count = sum(row["truth"] is False for row in methods)
    pass_count = sum(row["truth"] is True for row in methods)
    inherited_reviews = [
        {
            "proposal_id": row["nearest_id"],
            "title": row["nearest_title"],
            "source_path": row["nearest_path"],
            "status": "reviewed_inherited_zero_credit",
            "novelty_credit": 0,
            "completion_credit": 0,
        }
        for row in sorted(audit["neighbors"], key=lambda value: value["token_jaccard"], reverse=True)[:20]
    ]
    mutation_rows = mutation_plan(rows)

    dump(
        base / "source-verification.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "branch": BRANCH,
            "source_branch": SOURCE_BRANCH,
            "source": SOURCE,
            "anchors": {
                "tamar_v676_v5_corrected_final_and_elowen_source": ELOWEN_SOURCE,
                "elowen_x1": ELOWEN_X1,
                "elowen_evidence": ELOWEN_EVIDENCE,
                "elowen_first_final": ELOWEN_FIRST_FINAL,
                "elowen_correction_1": ELOWEN_CORRECTION_1,
                "elowen_correction_2": ELOWEN_CORRECTION_2,
                "elowen_correction_3": ELOWEN_CORRECTION_3,
                "elowen_correction_4_exact_final": ELOWEN_FINAL,
            },
            "source_to_final_phase_commits": 7,
            "source_to_final_merges": 0,
            "source_clean_zero_divergent_and_fresh_four_way_equal": True,
            "elowen_failed_canonical_receipt_sha256": ELOWEN_FAILED_RECEIPT_SHA256,
            "elowen_successful_canonical_receipt_sha256": ELOWEN_CANONICAL_RECEIPT_SHA256,
            "elowen_successful_canonical_payload_sha256": ELOWEN_CANONICAL_PAYLOAD_SHA256,
            "three_failed_canonical_receipts_preserved_at_zero_success_credit": True,
            "inherited_canonical_replayed": False,
            "verified_date": GENERATED_DATE,
        },
    )
    dump(
        base / "new-proposal-freeze.json",
        {
            "status": "FROZEN_PLANNING_ONLY",
            "declared_chain_before": ACTIVATION["declared_proposals"],
            "new_sylven_proposals": len(rows),
            "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows),
            "proposals": rows,
        },
    )
    dump(base / "semantic-neighbor-audit.json", audit)
    dump(
        base / "inherited-zero-credit-review.json",
        {
            "count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
    )
    dump(
        base / "mutation-preregistration.json",
        {
            "proposal_count": len(rows),
            "mutations_per_proposal": 4,
            "mutation_count": len(mutation_rows),
            "mutations": mutation_rows,
        },
    )
    dump(
        base / "portfolio-freeze.json",
        {
            "safe_now": planned_rows("SA6767-SAFE", safe_descriptions(), "planned_unexecuted_x1"),
            "candidate": planned_rows("SA6767-CAND", candidate_descriptions(), "planned_unexecuted_x1"),
            "exact_approval": planned_rows("SA6767-EXACT", EXACT_GATE_TASKS, "unexecuted_exact_gate"),
            "blocked": planned_rows("SA6767-BLOCK", BLOCKED_TASKS, "blocked_unexecuted"),
            "caps_are_ceilings_not_quotas": True,
        },
    )
    dump(
        base / "skill-runner-plan.json",
        {
            "phase_local_skills": [
                {
                    "skill_id": f"SA6767-SKILL-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                    "global_install": False,
                }
                for index, name in enumerate(SKILLS, start=1)
            ],
            "family_current_runners": [
                {
                    "runner_id": f"SA6767-RUNNER-{index:02d}",
                    "name": name,
                    "status": "planned_unbuilt_x1",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
            "successor_skill_recommendations": [
                {
                    "recommendation_id": f"SA6767-SUCCESSOR-SKILL-{index:02d}",
                    "seed": name,
                    "credit": "zero_sylven_completion_credit",
                }
                for index, name in enumerate(SKILLS[:10], start=1)
            ],
            "successor_runner_recommendations": [
                {
                    "recommendation_id": f"SA6767-SUCCESSOR-RUNNER-{index:02d}",
                    "seed": name,
                    "credit": "zero_sylven_completion_credit",
                }
                for index, name in enumerate(RUNNERS, start=1)
            ],
        },
    )
    dump(
        base / "clean-fix-refine-plan.json",
        {
            "owner_tasks": planned_rows("SA6767-CFR", cfr_descriptions(), "planned_unexecuted_x1"),
            "successor_recommendations": [
                {
                    "recommendation_id": f"SA6767-SUCCESSOR-CFR-{index:03d}",
                    "description": cfr_descriptions()[index - 1],
                    "credit": "zero_sylven_completion_credit",
                }
                for index in range(1, 31)
            ],
        },
    )
    dump(
        base / "successor-recommendations.json",
        {
            "recipient_unresolved_until_terminal_gate": True,
            "recommendation_count": 50,
            "recommendations": [
                {
                    "recommendation_id": f"SA6767-SUCC-SEED-{index:03d}",
                    "description": (
                        f"Re-audit as zero-credit successor seed: {TITLES[index - 1]}"
                        if index <= len(TITLES)
                        else SUCCESSOR_SUPPORT[index - len(TITLES) - 1]
                    ),
                    "credit": "zero_sylven_completion_credit",
                }
                for index in range(1, 51)
            ],
        },
    )
    dump(
        base / "official-source-ledger.json",
        {
            "checked_date": GENERATED_DATE,
            "sources": SOURCES,
            "source_boundary": (
                "Official and primary sources supply current vocabulary and refusal conditions only. They are not observations, "
                "measurements, repair or treatment instructions, endorsements, conformance certificates, legal interpretations, "
                "affected-party decisions, cultural ratifications, professional approvals, or authority grants."
            ),
        },
    )
    dump(
        base / "primary-pillar-and-lens.json",
        {
            "primary_pillar": "THOS Body",
            "secondary_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "bounded_wholly_synthetic_learning_lenses": [
                "marionette control-topology documentation analyst for synthetic zero-object records",
                "string-channel and joint-relation steward for synthetic topology only",
                "accessible cue correction and handover designer for synthetic records",
            ],
            "real_world_rows_or_actions": 0,
            "professional_or_authority_credit": 0,
        },
    )
    dump(
        base / "protected-gate-register.json",
        {
            "protected_gates": PROTECTED_GATES,
            "inherited_open_gaps": ACTIVATION["open_gaps"],
            "inherited_exact_gates": ACTIVATION["exact_gates"],
            "authority_noncompensation": True,
        },
    )
    dump(
        base / "method-flow-startup.json",
        {
            "activation_baseline": ACTIVATION,
            "methods": methods,
            "new_failed_witnesses": failure_count,
            "new_bounded_passing_witnesses": pass_count,
            "new_effective_methods": len(methods),
            "current_overlay": {
                "effective_negatives": ACTIVATION["effective_negatives"] + failure_count,
                "effective_methods": ACTIVATION["effective_methods"] + len(methods),
                "retained_failed_witnesses": ACTIVATION["retained_failed_witnesses"] + failure_count,
                "bounded_passing_witnesses": ACTIVATION["bounded_passing_witnesses"] + pass_count,
                "open_gaps": ACTIVATION["open_gaps"],
                "exact_gates": ACTIVATION["exact_gates"],
            },
            "failure_erasure_forbidden": True,
        },
    )
    dump(
        base / "route-hold.json",
        {
            "route_state": "HOLD_UNTIL_SYLVEN_V676_V7_TERMINAL_GATE",
            "successor_inferred": False,
            "prospective_successor_title": None,
            "prospective_successor_phase": None,
            "precontact_performed": False,
            "send_count": 0,
            "newest_live_authority_required_at_terminal_gate": True,
        },
    )
    dump(
        base / "phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "status": "FROZEN_PLANNING_ONLY",
            "source": SOURCE,
            "new_proposals": len(rows),
            "declared_chain_after": ACTIVATION["declared_proposals"] + len(rows),
            "expected_dispositions": dict(Counter(row["expected_disposition"] for row in rows)),
            "executed_core_outcomes": {label: 0 for label in ("completed", "represented", "open_gap", "exact_gate")},
            "x2_implementation_present": False,
            "x2_outcomes_claimed": False,
            "real_world_rows": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    text(
        base / "identity-and-boundary.md",
        """# Sylven Arc v676-v7 identity and authority boundary

Sylven Arc, optionally they/them, is relational working language only. The phase role is **relational topology steward and boundary weaver**, with the hope of making complex dependencies legible while keeping evidence, uncertainty, and authority visibly separate.

This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority. Hamish may rename, pause, redirect, narrow, or stop the route.

GMUT remains a typed scalar-tensor and effective-field-theory research-model family with no empirical result here. THOS remains synthetic proxy evidence without real participants, operators, safety monitoring, statistics, or independent review. Freed ID remains synthetic and nonproduction with zero real keys, proofs, lifecycle events, or trust governance. CBR, ownership, authorship, copyright, performance and recording rights, manipulation, rigging, repair, material safety, privacy remedy, legal interpretation, cultural legitimacy, affected-party acceptance, mātauranga, taonga, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities.
""",
    )
    text(
        base / "x1-overview.md",
        f"""# Sylven Arc {PHASE} planning-only x1 overview

This x1 freezes forty bounded proposal contracts against the declared 7,630-row chain and every proposal-bearing JSON artifact reachable at Elowen's exact fourth-correction final `{SOURCE}`. Twenty inherited neighbors are reviewed at zero novelty and completion credit. Four invalid mutations per proposal are preregistered but unexecuted. The bounded tribunal cannot prove universal or scientific novelty where no single historical ledger materializes every declared row.

The primary pillar is THOS Body through wholly synthetic marionette control-bar, string-channel, joint-topology, cue, correction, and accessible-handover documentation. GMUT Mind and Freed ID/CBR Heart remain visible and protected. There are zero real people, marionettes, controls, strings, joints, stages, scripts, images, recordings, measurements, observations, tools, manipulations, performances, repairs, identity events, external actions, or authority decisions.

No x2 implementation or observed outcome exists in this freeze. Only `completed`, `represented`, `open_gap`, and `exact_gate` are authorized future outcome labels, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--diagnose-audit", action="store_true")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.diagnose_audit:
        audit = reachable_semantic_audit(repo, proposal_rows())
        print(
            json.dumps(
                {
                    "json_parse_failures": audit["json_parse_failures"],
                    "parse_failure_details": audit["parse_failure_details"],
                    "exact_title_collisions": audit["exact_title_collisions"],
                    "selected_rows_quarantined": audit["selected_rows_quarantined"],
                    "maximum_selected_score": audit["maximum_selected_score"],
                    "quarantined_neighbors": [
                        row for row in audit["neighbors"] if row["token_jaccard"] >= audit["quarantine_threshold"]
                    ],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return
    build(repo)


if __name__ == "__main__":
    main()
