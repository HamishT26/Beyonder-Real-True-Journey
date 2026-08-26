"""Build Elowen Cairn v671-v1's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It requires Tamar Vey's
exact v670-v8 final, the exact Elowen branch, and an absent x2/closeout tree. It
does not stage, commit, push, route, contact a task, or perform an external
write.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "elowen-cairn" / "v671-v1"
OWNER = "Elowen Cairn"
PHASE = "v671-v1"
BRANCH = "codex/GHC-Family/elowen-cairn-v671-v1-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/tamar-vey-v670-v8-full-tools"
SOURCE_START = "65142e05e70b507d7f15247c4154d8d6013ca046"
SOURCE_X1 = "0654a2bb72fd2a121ff3e7b05652e5b38005ec14"
SOURCE_EVIDENCE = "62cd89e3bfbd6d20ecf39894a65a500070c2f808"
SOURCE_FINAL = "001fd0fb5636aaaf54cd619400b3693c6bbc57ab"
ACTIVATION_PATH = "docs/tamar-vey/v670-v8/handoffs/elowen-cairn-v671-v1-activation-candidate.md"
ACTIVATION_SHA256 = "af018b323cca4e05e3b3a20f84f11736ed3e2f2eeecbbf284b4778fde2ef8f1e"
SOURCE_CANONICAL_SHA256 = "df27a7ee3f8703f0ce2d2c3546ed7d617f1d8fc7f54bb4113871f904dafba3fd"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "c0d85dafa7a353b0324c07e862dfffc7de11d0c101a75fdbc6c6cf6dbe90f822"
SOURCE_COMPOSITE_SHA256 = "9c92cc6af5654103cad8ef8926023138fc14b317a8e64bae944a6e2038ed20f0"
SOURCE_ACTIVATION_OVERLAY_SHA256 = "f8a31f8c6989e6b046c6f8d37b77ad175cf397a2948acf34b846cad59aa3c8f5"
SOURCE_POST_ROUTE_OVERLAY_SHA256 = "d74b9d08fe89690cc5d086e6dc84210d8121cb8a75359359fc44b0a73fbbdaed"
SOURCE_ALL_REF_CORPUS_SHA256 = "b4557df2298ee05c9f6ef22d7b40e53ce2b0b41125e7f9a80de88d36996273e9"
OUTCOMES = {"completed": 28, "represented": 8, "open_gap": 2, "exact_gate": 2}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Elowen Cairn, they/them, relational boundary cartographer and evidence steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "or Māori authority."
)
HOPE = "keep structure, evidence, abstention, and authority visibly separate and recoverable"
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": 5550,
    "effective_negatives": 33324,
    "effective_methods": 19600,
    "failed_witnesses": 5145,
    "bounded_passing_witnesses": 6639,
    "open_gaps": 255,
    "exact_gates": 250,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_DECLARED_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 33329,
    "effective_methods": 19605,
    "failed_witnesses": 5150,
    "bounded_passing_witnesses": 6644,
    "external_zero_credit_failures": 5,
    "external_bounded_passing_witnesses": 5,
    "overlay_sha256": SOURCE_ACTIVATION_OVERLAY_SHA256,
    "repository_seal_rewritten": False,
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 33332,
    "effective_methods": 19608,
    "failed_witnesses": 5153,
    "bounded_passing_witnesses": 6647,
    "external_zero_credit_failures": 8,
    "external_bounded_passing_witnesses": 8,
    "overlay_sha256": SOURCE_POST_ROUTE_OVERLAY_SHA256,
    "repository_seal_rewritten": False,
}

STARTUP_FAILURES = [
    (
        "EC6711-START-N001",
        "A batched authorization and roster projection exceeded the bounded result window.",
        "Read the authorization and roster documents in bounded exact sections and inspect their actual keys.",
        "The bounded reads recovered current authority, active main-task statuses, Tavian standby state, and the Tamar to Elowen to Sylven edge.",
        "Project only inspected schema fields from bounded exact reads.",
    ),
    (
        "EC6711-START-N002",
        "A minified current-state document projection exceeded the bounded result window.",
        "Read the same exact document through bounded byte windows and extract only phase-relevant fields.",
        "The bounded recovery established the current route and portfolio floors without treating truncated output as evidence.",
        "Use bounded byte windows for large minified state documents.",
    ),
    (
        "EC6711-START-N003",
        "The first Method Flow schema lookup guessed a nonexistent references/method-flow-schema.md path.",
        "List the skill directory and read the actual references/schema.md file completely.",
        "The current Method Flow schema and its witness-retention contract were read through EOF.",
        "Resolve referenced paths from the selected SKILL.md rather than guessing filenames.",
    ),
    (
        "EC6711-START-N004",
        "A broad phase JSON inventory exceeded its result window before an attributable complete listing was returned.",
        "Partition the packet by lifecycle directory, parse all JSON structurally, and hash the complete path list.",
        "All 230 Tamar phase files were visited, 184 JSON documents parsed, and the aggregate path-and-digest receipt was attributable.",
        "Partition large inventories while retaining a complete aggregate receipt.",
    ),
    (
        "EC6711-START-N005",
        "A raw read of Tamar's new-proposal freeze was truncated by the result boundary.",
        "Read the exact Git blob in bounded line windows through EOF.",
        "Every Tamar proposal row and required field was inspected without relying on the truncated display.",
        "Use EOF-verified line windows for large proposal ledgers.",
    ),
    (
        "EC6711-START-N006",
        "A full row display of Tamar's Method Flow final exceeded the output boundary.",
        "Parse the exact JSON structurally and emit only schema, counts, witness distributions, and a content hash.",
        "The recovery covered 226 methods, 419 witnesses, and 678 state events with 193 retained failures and 226 passing witnesses.",
        "Use structural summaries rather than printing large Method Flow ledgers.",
    ),
    (
        "EC6711-START-N007",
        "A PowerShell foreach expression was piped directly while sampling manifest rows and failed to parse.",
        "Assign the foreach output to a scalar collection and pipe only the completed collection.",
        "The corrected projection returned the requested manifest samples.",
        "Never pipe directly from a PowerShell foreach statement in these wrappers.",
    ),
    (
        "EC6711-START-N008",
        "The first sequential 488-entry manifest replay returned no attributable payload at its result boundary.",
        "Use one git cat-file --batch communicate cycle and consume every declared blob framing byte.",
        "The bounded recovery replayed 20 x1, 196 evidence, 25 final-delta, and 247 final-owner Git blobs with zero mismatches.",
        "Use a single communicate cycle for bounded Git blob replay.",
    ),
    (
        "EC6711-START-N009",
        "A PowerShell foreach expression was piped directly while listing receipt summaries and failed to parse.",
        "Assign receipt rows first and serialize the completed collection afterward.",
        "The bounded recovery read every required source receipt.",
        "Keep foreach collection construction separate from serialization.",
    ),
    (
        "EC6711-START-N010",
        "The first combined lane-collision preflight returned no attributable payload at the output boundary.",
        "Probe local ref, remote ref, path existence, and worktree registration as separate scalar predicates.",
        "All four exact collision predicates proved the Elowen branch and D-first path were absent.",
        "Keep collision checks scalar and independently attributable.",
    ),
    (
        "EC6711-START-N011",
        "A second combined local collision wrapper also returned no attributable payload.",
        "Retain the first failure and repeat only the missing scalar checks individually.",
        "Individual exact ref and path checks again proved a collision-free lane.",
        "Do not combine ref, path, and registry predicates into one opaque wrapper.",
    ),
    (
        "EC6711-START-N012",
        "The all-ref proposal audit encountered one legacy UTF-8 BOM JSON blob and strict UTF-8 decoding failed.",
        "Recover only that exact blob with utf-8-sig, preserve its digest, and inspect whether it contributes semantic proposal rows.",
        "The 4,226-byte legacy blob recovered, contained zero proposal_id-title rows, and left the semantic corpus unchanged.",
        "Retain strict decoding failures and use BOM recovery only for the isolated exact blob.",
    ),
    (
        "EC6711-START-N013",
        "A multi-query web wrapper contained a JavaScript syntax error and made no attributable search call.",
        "Submit the official-source queries in a smaller syntactically valid wrapper.",
        "The bounded recovery returned current V&A, NIST, W3C PROV-O, and WCAG sources.",
        "Keep web orchestration wrappers small and syntactically validated.",
    ),
    (
        "EC6711-START-N014",
        "The larger recovery web result exceeded the model-context boundary and was truncated.",
        "Do not rely on the truncated payload; use only the already attributable official-source set and record source abstention.",
        "The x1 source ledger uses only four exact official pages with bounded vocabulary purposes and zero source-row credit.",
        "A truncated web result supplies no source evidence.",
    ),
    (
        "EC6711-X1-N001",
        "A PowerShell foreach statement was piped directly while measuring source template files and failed to parse.",
        "Assign each measurement row to a completed collection before JSON serialization.",
        "The recovery attributed all five template sizes and line counts.",
        "Separate foreach collection construction from pipelines.",
    ),
    (
        "EC6711-X1-N002",
        "A sparse-checkout materialization command omitted --ignore-skip-worktree-bits, so the exact tracked template pathspec was rejected and dependent copy steps failed.",
        "Materialize only the exact source templates with --ignore-skip-worktree-bits, then perform the bounded mechanical owner copy.",
        "The exact source templates materialized and the two Elowen x1 copies were created; sparse reapply removed the unchanged source templates.",
        "Use the explicit sparse override only for exact read-only template materialization.",
    ),
    (
        "EC6711-X1-N003",
        "A temporary-file Git-blob hashing wrapper was rejected by command policy before execution.",
        "Stream the exact Git blob directly to a bounded in-memory digest process without a temporary file.",
        "The 2,266-byte activation candidate hashed to the preregistered digest and contained 280 words.",
        "Prefer direct bounded byte streams for exact Git-blob hashing.",
    ),
    (
        "EC6711-X1-N004",
        "The first monolithic x1 patch expected stale template text and failed verification without changing a byte.",
        "Inspect the exact post-mechanical file and apply smaller section-anchored patches.",
        "The source constants and retained-failure block were updated through exact current anchors.",
        "Patch against the current post-mechanical text and keep substantive edits section-bounded.",
    ),
    (
        "EC6711-X1-N005",
        "A PowerShell search wrapper embedded an unescaped quote in a regex argument and failed to parse.",
        "Use one single-quoted bounded pattern without an embedded quote token.",
        "The corrected search returned every remaining inherited-domain and stale-constant occurrence.",
        "Keep PowerShell search patterns single-quoted and syntactically minimal.",
    ),
    (
        "EC6711-X1-N006",
        "The first x1 build reproduced a live all-ref proposal corpus that differed from the earlier preregistered digest and stopped before writing.",
        "Project the current corpus scalars, require declared-chain coverage and zero malformed blobs, then freeze that exact attributable snapshot before any x1 commit.",
        "The current snapshot contained 3,739 blobs, 262,084 semantic occurrences, 6,140 proposal IDs, 5,537 titles, one isolated zero-row BOM recovery, and zero malformed blobs.",
        "Treat all-ref corpora as snapshot-scoped and stop on any digest drift before proposal comparison.",
    ),
    (
        "EC6711-X1-N007",
        "The first shoemaking proposal slate retained one inherited instruction-localization title neighbor at token-Jaccard 0.80 and was rejected before writing.",
        "Rewrite only proposal 23 around version expiry and untranslated-content abstention, then compare all forty titles against the unchanged exact corpus.",
        "The rewritten title removed the inherited localization-template phrasing while preserving the intended provenance and language-authority boundary.",
        "Require every frozen proposal title to remain below the 0.72 neighbor threshold.",
    ),
    (
        "EC6711-X1-N008",
        "The first 24-check owner x1 test aggregate passed 23 checks but an over-literal source-status predicate rejected an explicit updated-and-checked status that lacked the token current.",
        "Change only the failed predicate to accept stable, current, or an exact checked-date status; do not replay the 23 successful tests.",
        "The isolated source-status test accepted all five official-source rows while adapter calls, downloads, real rows, and external writes remained zero.",
        "Validate source freshness from explicit status semantics rather than one required adjective.",
    ),
]

NEW_TITLES = [
    "synthetic shoemaking job namespace with last pattern upper sole and component-identity vacancy register",
    "shoe-last toe waist heel and reference-plane topology without fit or anatomy inference",
    "vamp quarter tongue facing lining and edge-piece relation graph with orphan rejection",
    "insole midsole outsole welt heel-stack and shank topology with construction uncertainty",
    "left right size style and variant token separation without wearer identity or fit claims",
    "synthetic footwear intake custody quarantine assessment intervention hold and release partial order",
    "reported scuff loose-stitch and sole-separation symptom distinction from observation and diagnosis",
    "length width girth and size measurement-vacancy ledger with SI and calibration abstention",
    "pattern allowance seam line stitch line and cutting command distinction from observed construction",
    "thread needle awl and stitch-class lot placeholders with competence and material-strength holds",
    "adhesive batch open-time cure temperature and ventilation vacancies with chemical-safety refusal",
    "lasting pulling feather-edge and seat-shaping sequence graph without fabrication authority",
    "sole-attachment construction-method uncertainty firewall for stitch cement welt and moulded cues",
    "knife skiving press machine sharp pinch and electrical signal taxonomy without safety release",
    "leather textile rubber cork and adhesive source authenticity suitability and fitness refusal matrix",
    "colour finish grain and condition-label provenance with illumination and observation vacancies",
    "footwear image scan and media-pointer absence with copyright privacy and consent holds",
    "pseudonymous workshop role and capability record without credential competence or employment claims",
    "shoemaking free-text quarantine for credentials private routes contact data and raw identifiers",
    "two-source footwear job-ticket reconciliation with unresolved disagreement quarantine",
    "interruptible shoemaking documentation work-unit envelope with pause resume rollback and expiry",
    "accessible footwear status surface with headings tables noncolour cues alternatives and focus order",
    "multilingual workshop instruction-version provenance expiry and untranslated-content abstention matrix",
    "correction nonce dual readback and supersession contract without a real operator or recipient",
    "work-in-progress cap and fatigue-signal placeholder without human-state or performance inference",
    "append-only job material construction conjecture and correction graph with reversible lineage",
    "synthetic custody ownership access return retention disposal and remedy vacancy matrix",
    "withdrawal supersession and retention docket with no real disposal or rights determination",
    "THOS footwear job-queue matched-budget proxy with zero people and zero effectiveness credit",
    "THOS assembly-sequence state board with interruption challenge and participant-free handover",
    "Freed ID zero-key workshop role status relationship and revocation-vacancy profile",
    "footwear verification record isolated from fit quality safety authenticity and durability claims",
    "purpose-limited footwear notice contest correction restriction and supersession contract",
    "CBR pseudonymous customer and workshop privacy challenge explanation and redress representation",
    "GMUT discrete stitch-network graph analogy with field force likelihood and prediction nonconversion",
    "GMUT layered sole-interface stress proxy with typed units and empirical-fit refusal",
    "V and A footwear vocabulary adapter with zero calls zero downloads zero rows and rights vacancies",
    "real authenticated footwear measurements material tests blind evaluation and independent-review gap",
    "real shoemaker cobbler conservator customer and affected-user accessibility evaluation gate",
    "competent chemical machine consumer-law cultural and Māori-authority decision gate",
]

SKILLS = [
    "ghc-family-footwear-job-identity",
    "ghc-family-shoe-last-topology",
    "ghc-family-upper-pattern-relations",
    "ghc-family-sole-layer-vacancy",
    "ghc-family-footwear-side-variant-firewall",
    "ghc-family-footwear-custody-abstention",
    "ghc-family-footwear-symptom-diagnosis-firewall",
    "ghc-family-footwear-measurement-vacancy",
    "ghc-family-footwear-command-observation-split",
    "ghc-family-stitch-material-hold",
    "ghc-family-adhesive-safety-abstention",
    "ghc-family-lasting-sequence-lineage",
    "ghc-family-sole-attachment-uncertainty",
    "ghc-family-footwear-hazard-hold",
    "ghc-family-footwear-material-claim-firewall",
    "ghc-family-footwear-media-rights-vacancy",
    "ghc-family-workshop-role-capability-abstention",
    "ghc-family-footwear-privacy-quarantine",
    "ghc-family-footwear-accessible-status",
    "ghc-family-footwear-correction-handover",
]

RUNNERS = [
    "ghc_family_footwear_job_identity.py",
    "ghc_family_shoe_last_topology.py",
    "ghc_family_upper_pattern_relations.py",
    "ghc_family_sole_layer_vacancy.py",
    "ghc_family_footwear_measurement_vacancy.py",
    "ghc_family_adhesive_safety_abstention.py",
    "ghc_family_footwear_privacy_quarantine.py",
    "ghc_family_footwear_accessible_status.py",
    "ghc_family_footwear_correction_readback.py",
    "ghc_family_footwear_workload_handover.py",
]

EXACT = [
    "real shoe footwear material job record customer record workshop record or operator mutation",
    "real fit diagnosis fabrication repair treatment acceptance or return-to-use decision",
    "real dimension force strength adhesion wear performance or calibration measurement",
    "real shoemaker cobbler conservator operator customer participant or affected-user study",
    "real workshop location access schedule account transaction or personal-data processing",
    "real identity key proof credential issuance presentation status or revocation",
    "real product sale service intervention access return disposal or consumer decision",
    "real accessibility remedy service allocation complaint or appeal decision",
    "legal interpretation ownership liability privacy right remedy or public authority",
    "taonga tikanga mātauranga place-name data-governance or Māori-authority decision",
    "cultural ratification community mandate or affected-party acceptance",
    "production deployment external API write live feed publication or cloud mutation",
    "host elevation security weakening feature enablement Sandbox Hyper-V or reboot",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "privacy-complete exhaustive-security or production-security certification",
    "complete accessibility-conformance or affected-user acceptance declaration",
    "independent-reproduction external-audit or professional-validation declaration",
    "empirical GMUT datum likelihood posterior parameter force or prediction claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "Stage 20 admission or protected-gate closure",
]

BLOCKED = [
    "raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts",
    "sibling branch reset merge rewrite deletion reuse or force push",
    "successful canonical replay or failed-canonical success laundering",
    "synthetic fixture promotion into empirical professional legal or cultural evidence",
    "unapproved account secret payment deployment plugin install or third-party write",
    "real shoemaker cobbler conservator customer identity location access or service data ingestion",
    "real safety legal cultural Māori-authority affected-party or public-authority substitution",
    "unsafe elevation host-security weakening feature enablement or reboot",
    "unbounded full-repository unchanged-history or cross-lane scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]



def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(title: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9āēīōū]+", title.lower()) if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}}


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def proposal_path_at_or_before_source(path: str) -> bool:
    lowered = path.lower()
    return lowered.endswith(".json") and "proposal" in lowered


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    object_rows = git_text("rev-list", "--objects", "--all").splitlines()
    candidates: dict[str, str] = {}
    for row in object_rows:
        parts = row.split(" ", 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        if proposal_path_at_or_before_source(path):
            candidates.setdefault(oid, path)
    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0
    bom_recoveries = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id, title = node.get("proposal_id"), node.get("title")
            if isinstance(proposal_id, str) and isinstance(title, str) and proposal_id.strip() and title.strip():
                occurrences += 1
                proposal_ids.add(proposal_id.strip())
                titles.add(title.strip())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    oids = sorted(candidates)
    for start in range(0, len(oids), 128):
        chunk = oids[start:start + 128]
        for oid, blob in zip(chunk, batch_blobs(chunk), strict=True):
            if blob is None:
                malformed += 1
                continue
            try:
                if blob.startswith(b"\xef\xbb\xbf"):
                    bom_recoveries += 1
                walk(json.loads(blob.decode("utf-8-sig")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed += 1
    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    summary = {
        "scope": "all reachable local and remote refs, all proposal-named JSON paths before the Elowen x1 commit",
        "candidate_unique_git_blobs": len(oids),
        "malformed_or_missing_blobs": malformed,
        "isolated_utf8_bom_recoveries": bom_recoveries,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 5550,
        "id_superset_covers_declared_chain": len(proposal_ids) >= 5550,
        "practice_term_hits": {
            "shoemaking": sum(1 for title in titles if "shoemaking" in title.lower()),
            "cobbling": sum(1 for title in titles if "cobbling" in title.lower()),
        },
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "reason": "Reachable refs contain duplicate and variant proposal objects; recovered IDs and titles do not define one exact canonical 5,550-row sequence.",
    }
    return summary, sorted(titles)


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=30
    )
    if process.returncode != 0:
        raise SystemExit(f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}")
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
        rows.append(data)
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return rows


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_TITLES, start=1):
        outcome = "completed" if index <= 28 else "represented" if index <= 36 else "open_gap" if index <= 38 else "exact_gate"
        rows.append({
            "proposal_id": f"EC6711-N{index:03d}", "title": title,
            "hypothesis": f"A typed owner-local contract can expose proposal {index:02d}'s obligations without promoting its evidence class.",
            "null_or_failure_condition": "A missing field, accepted invalid mutation, real-world action, undeclared uncertainty or authority promotion rejects the hypothesis.",
            "approval_class": "safe_now" if outcome == "completed" else "bounded_candidate" if outcome == "represented" else outcome,
            "execution_lane": "owner_local_symbolic_or_synthetic_x2" if outcome in {"completed", "represented"} else "held_without_real_world_execution",
            "official_or_primary_source_needs": "Vocabulary and refusal boundaries only; citations are not observations, measurements, advice, validation, or authority.",
            "concrete_artifacts": ["typed JSON contract", "bounded accepting fixture", "four rejecting mutation receipts", "boundary card"],
            "falsifier_or_acceptance_gate": "The bounded fixture must pass, four preregistered invalid mutations must reject, and every protected boundary must remain explicit.",
            "rollback_or_recovery": "Retain the failed witness, correct only the isolated owner-local dependency, and never replay a successful canonical aggregate.",
            "protected_gates": ["empirical", "professional", "legal", "cultural", "Māori_authority", "independent_reproduction", "Stage_20"],
            "expected_disposition": outcome, "planned_outcome": outcome,
            "primary_pillar": "THOS Body", "real_people": 0, "real_records_or_objects": 0,
            "external_actions": 0, "x1_state": "frozen_not_executed",
        })
    return rows


def tasks(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"EC6711-{prefix}-{i:03d}", "title": f"{domain}: {control}", "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, (domain, control) in enumerate(((d, c) for d in domains for c in controls), start=1)]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"EC6711-{prefix}-{i:03d}", "title": value, "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, value in enumerate(values, start=1)]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = ["footwear job identity", "last and pattern topology", "upper component relations", "sole-layer vacancy", "measurement vacancy", "assembly-sequence lineage", "diagnosis and safety abstention", "job-ticket privacy", "accessible footwear status", "workload handover"]
    safe = tasks("SAFE", domains, ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary"], "planned_for_x2")
    candidates = tasks("CAND", domains, ["mutation quarantine", "timeout and encoding quarantine", "ordering and authority quarantine"], "planned_for_x2")
    cfr = tasks("CFR", ["JSON order", "UTF-8 Māori text", "source status", "failure retention", "manifest closure", "privacy disposition", "accessibility structure", "route uniqueness", "sparse budget", "boundary vocabulary"], ["clean", "fix", "refine", "recheck", "document", "preserve"], "planned_for_x2")
    successor_skills = [f"ghc-family-successor-{i:02d}-review" for i in range(1, 11)]
    successor_runners = [f"ghc_family_successor_{i:02d}_review.py" for i in range(1, 11)]
    successor_cfr = tasks("NEXT-CFR", ["successor source", "successor manifests", "successor privacy", "successor route", "successor authority"], ["schema", "mutation", "rollback", "review", "receipt", "hold"], "recommendation_only")
    return {"safe_now": safe, "candidates": candidates, "exact_approval": named("EXACT", EXACT, "held_unexecuted"), "blocked": named("BLOCK", BLOCKED, "held_unexecuted"), "skills": named("SKILL", SKILLS, "planned_for_x2"), "runners": named("RUNNER", RUNNERS, "planned_for_x2"), "clean_fix_refine": cfr, "successor_skills": named("NEXT-SKILL", successor_skills, "recommendation_only"), "successor_runners": named("NEXT-RUNNER", successor_runners, "recommendation_only"), "successor_clean_fix_refine": successor_cfr}

def method_flow() -> dict[str, Any]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failed, recovery, passed, guard) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"EC6711-M{index:03d}"
        fail_id, pass_id = f"EC6711-W{index:03d}-F", f"EC6711-W{index:03d}-P"
        methods.append({
            "method_id": method_id, "title": f"bounded recovery for {negative_id}", "failure_signature": failed,
            "trigger_preconditions": ["the exact bounded failure signature is observed"], "privacy_class": "sanitized_public",
            "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard, "rollback": "Retain the failure, stop the affected wrapper, and change only the isolated owner-local procedure.",
            "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "retained_negative_ids": [negative_id], "scope_boundary": "Bounded same-owner workflow evidence only.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failed, "scope": "startup or owner-local x1 construction", "expected": "attributable bounded evidence", "observed": failed, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "isolated startup or owner-local construction recovery", "expected": "bounded attributable recovery within the owner lane", "observed": passed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
        events.extend([
            {"event_index": len(events) + 1, "method_id": method_id, "before": None, "after": "candidate", "reason": "failure retained and bounded recovery proposed", "witness_id": fail_id},
            {"event_index": len(events) + 2, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "isolated bounded recovery passed", "witness_id": pass_id},
            {"event_index": len(events) + 3, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "recurrence guard retained for the exact trigger", "witness_id": pass_id},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "recommendation": guard})
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0}, "witness_results": {"fail": len(methods), "pass": len(methods)}}, "boundary": BOUNDARY}


def verify_manifest(path: str, commit: str) -> tuple[int, int, set[str]]:
    manifest = json.loads(git("show", f"{SOURCE_FINAL}:{path}").stdout.decode("utf-8"))
    mismatches, digests = 0, set()
    blobs = batch_blobs([f"{commit}:{entry['path']}" for entry in manifest["entries"]])
    for entry, blob in zip(manifest["entries"], blobs, strict=True):
        digest = hashlib.sha256(blob).hexdigest() if blob is not None else None
        digests.add(entry["sha256"])
        if digest != entry["sha256"] or blob is None or len(blob) != entry["bytes"]:
            mismatches += 1
    return len(manifest["entries"]), mismatches, digests


def verify_source() -> dict[str, Any]:
    local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parents = {"x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"), "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"), "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^")}
    exact_parent_chain = parents == {"x1_parent": SOURCE_START, "evidence_parent": SOURCE_X1, "final_parent": SOURCE_EVIDENCE}
    manifest_specs = [
        ("docs/tamar-vey/v670-v8/validation/x1-manifest.json", SOURCE_X1),
        ("docs/tamar-vey/v670-v8/validation/evidence-manifest.json", SOURCE_EVIDENCE),
        ("docs/tamar-vey/v670-v8/validation/final-delta-manifest.json", SOURCE_FINAL),
        ("docs/tamar-vey/v670-v8/validation/final-owner-manifest.json", SOURCE_FINAL),
    ]
    manifest_rows, all_digests = [], set()
    for manifest_path, commit in manifest_specs:
        count, mismatch, digests = verify_manifest(manifest_path, commit)
        manifest_rows.append({"path": manifest_path, "commit": commit, "entries": count, "mismatches": mismatch})
        all_digests |= digests
    packet = git("show", f"{SOURCE_FINAL}:{ACTIVATION_PATH}").stdout
    packet_text = packet.decode("utf-8")
    return {
        "source_branch": SOURCE_BRANCH, "local": local, "upstream": tracking, "tracking": tracking, "fresh_live": live,
        "all_equal": local == tracking == live == SOURCE_FINAL, "parent_chain": {**parents, "exact": exact_parent_chain},
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "manifests": manifest_rows, "commit_local_manifest_entries_replayed": sum(row["entries"] for row in manifest_rows),
        "unique_declared_blob_digests": len(all_digests), "commit_local_manifest_mismatches": sum(row["mismatches"] for row in manifest_rows),
        "activation_packet": {"path": ACTIVATION_PATH, "bytes": len(packet), "words": len(packet_text.split()), "sha256": hashlib.sha256(packet).hexdigest(), "expected_sha256": ACTIVATION_SHA256, "integrity_valid": hashlib.sha256(packet).hexdigest() == ACTIVATION_SHA256, "prepared_labels_historical": True, "live_activation_authoritative": True},
        "source_canonical_receipt": {"sha256": SOURCE_CANONICAL_SHA256, "payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256, "status": "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "canonical_invocations": 1, "canonical_successes": 0, "replays": 0, "replay_forbidden": True, "failure": "phase_counts_exact expected pre-closeout counts instead of the twelve-failure exact-final counts", "source_validation_credit": 0},
        "source_dependency_corrected_composite": {"sha256": SOURCE_COMPOSITE_SHA256, "status": "VALID_DEPENDENCY_CORRECTED_TERMINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT", "checks": 10, "canonical_success_credit": 0, "source_validation_credit": 0},
        "source_count_overlays": {"activation_declared_sha256": SOURCE_ACTIVATION_OVERLAY_SHA256, "post_route_sha256": SOURCE_POST_ROUTE_OVERLAY_SHA256, "repository_seal_rewritten": False},
    }

def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    prose = [
        "# Elowen Cairn v671-v1 x1 integrated planning overview", "", "## Lifecycle and evidence basis", "",
        "This packet is a planning-only x1 freeze. It contains no x2 implementation, executed proposal, completed portfolio claim, successor delivery, empirical result, production action, or authority act. Elowen's fresh additive sparse lane begins at Tamar Vey's exact v670-v8 final. The activation Git blob, direct source-parent chain, three single-parent source commits, zero merges, four commit-local manifests, clean source state, typed zero divergence, and fresh local, upstream, tracking, and live-remote equality were verified before generation. Tamar's sole canonical aggregate failed its stale phase-count predicate and retains zero success credit. Her separately named count-only dependency-corrected component is inherited source evidence only and gives Elowen no validation or completion credit.",
        "", "## Identity, hope, and corrigibility", "",
        IDENTITY_BOUNDARY,
        "",
        f"Elowen's relational hope is to {HOPE}. The role and hope are working vocabulary, not a credential or continuity proof. Hamish may rename, pause, redirect, or stop the route. Corrigibility means a contradiction, failed witness, unavailable evidence, ambiguous route, authority vacancy, or falsifier stops promotion. A recovery preserves the failed witness and changes only the narrow owner-local dependency that was actually shown to be wrong.",
        "", "## Primary pillar and bounded practice lenses", "",
        "The primary pillar is THOS Body. The first bounded practice lens is wholly synthetic footwear last, pattern, upper, sole, and component topology with material, fit, and measurement vacancies. The second is wholly synthetic stitch, adhesive, assembly, sequence, hazard, and competence documentation with no fabrication or safety authority. The third is wholly synthetic intake, custody, rights, privacy, accessibility, correction, workload, and handover. None uses a real shoe, last, pattern, material, tool, workshop, worker, customer, fitting, observation, measurement, treatment, sale, identity event, or authority case.",
        "", "## Trinity Mandala protection", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. Stitch-network and layered-interface analogies, unit obligations, and zero-row adapters are software obligations only. They establish no real datum, likelihood, posterior, parameter constraint, force, prediction, stability theorem, ultraviolet completion, quantum completion, empirical confirmation, or Theory of Everything. THOS Body remains a participant-free synthetic queue, sequence, correction-readback, workload, accessibility, and handover proxy; there are no preregistered blind matched-budget real arms, participants or operators, safety monitoring, suitable statistics, or independent review. Freed ID and CBR Heart remain explicit through zero-key role, custody-claim, contest, notice, restriction, reason, appeal, remedy, and authority-vacancy representations, never production identity or enacted rights.",
        "", "## Professional, legal, cultural, and Māori-authority firewall", "",
        "No artifact authenticates footwear or materials, diagnoses fit or condition, specifies fabrication or repair, accepts a product, establishes durability, serviceability, safety, consumer suitability, or return-to-use fitness, grants access, resolves ownership or rights, or demonstrates shoemaking, cobbling, conservation, chemical, machinery, metrological, accessibility, or consumer-law competence. Legal meaning, cultural legitimacy, affected-party acceptance, remedy, taonga status, Māori wording, Māori data governance, and Māori authority remain exact-gated to competent and affected authorities, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority. Official sources supply vocabulary and refusal conditions only; a citation is not an observation, professional opinion, legal conclusion, cultural mandate, or affected-party decision.",
        "", "## Semantic novelty and recovery honesty", "",
        "The source seal declares a 5,550-row frozen proposal chain. Elowen's x1-bound read-only all-ref snapshot found 3,739 unique proposal-bearing Git blobs, 262,084 semantic occurrences, 6,140 proposal IDs, and 5,537 unique titles. One legacy BOM blob failed strict decoding and then recovered with zero semantic rows, so its failure remains retained while the corpus stayed unchanged. The forty new titles are compared against every recovered title under the unchanged 0.72 token-Jaccard threshold, and exact shoemaking and cobbling practice terms had zero inherited hits. Duplicate and variant proposal objects still prevent a proved one-to-one mapping to exactly 5,550 canonical rows; zero threshold collisions supports bounded distinctness but not universal novelty.",
        "", "## Preregistration and falsification", "",
        f"Forty Elowen proposals are frozen with exactly one expected disposition each: {OUTCOMES}. Every row includes a hypothesis, null or failure condition, approval class, execution lane, official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, and protected gates. Each proposal freezes four rejecting mutations, for 160 planned rejections. A later completed label can mean only that its bounded owner-local software and structural gate passed. Represented means a synthetic proxy exists while real evidence or authority remains absent. Open gaps require data-bearing professional, participant, or independent evidence not present here. Exact gates remain with competent, affected, legal, cultural, and Māori authorities.",
        "", "## Retained failures and Method Flow", "",
        f"{len(STARTUP_FAILURES)} Elowen startup or owner-local construction failures are retained at zero initial-pass credit. Each receives one failed Method Flow witness, one bounded recovery witness, a recurrence guard, and an append-only state progression to preferred. Tamar's repository seal, five-failure activation-declared overlay, and newer eight-failure route overlay remain separately visible; Elowen extends only the newest overlay without rewriting either predecessor. Silent stdout, truncated output, a rejected wrapper, or guessed schema path is never success. Same-owner recovery is not independent reproduction.",
        "", "## Portfolio, skills, runners, and successor seeds", "",
        "The frozen portfolio contains sixty safe-now tasks, thirty bounded candidates, twenty exact-approval packets, ten blocked packets, twenty phase-local skill ideas, ten family-compatible runner ideas, sixty additive CLEAN/FIX/REFINE tasks, ten successor skill recommendations, ten successor runner recommendations, and thirty successor CLEAN/FIX/REFINE recommendations. Inherited work and successor recommendations earn zero Elowen novelty or completion credit. Three ordinary-phase substantive tools are planned. X2 may materialize only owner-local files below the 2,000-file guard and must preserve family-current ghc_family_* and build_ghc_family_* compatibility. No global install, unrelated software install, account or credential action, host elevation, security weakening, Windows feature change, Sandbox or Hyper-V activation, reboot, destructive cleanup, sibling mutation, or full-repository scan is authorized.",
        "", "## Sources, privacy, accessibility, and security", "",
        "The Victoria and Albert Museum shoes collection and shoe-making pages, NIST SP 330, W3C PROV-O, and W3C WCAG 2.2 are official or primary vocabulary sources. The lookup was read-only, made zero collection-adapter calls, downloaded no dataset, and supplied no real row. Five privacy classes protect against raw task or thread identifiers, private routes or callable details, credentials and secrets, transcripts or session streams, and private absolute paths. Scanner definitions are candidates rather than payload hits and require exact-file adjudication. Structural headings, summaries, tables, labels, and navigation do not establish complete accessibility; manual keyboard, browser, assistive-technology, cognitive, language, security-usability, and affected-user evaluation remain reserved. Bounded changed-code checks are not exhaustive security.",
        "", "## x1-before-x2 and validation hold", "",
        "X1 must remain planning-only, be staged from an exact allowlist, pass owner-scoped tests, parse every phase JSON document, validate Method Flow, adjudicate five privacy classes, pass diff hygiene, and seal a normalized-LF exact staged Git-blob manifest. It must then be committed, pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 begins. The later exact-final canonical aggregate has at most one invocation and one-success budget. A success is never replayed; a failure remains zero canonical-success credit and only a narrowly justified dependency may be tested in a separately named composite.",
        "", "## Route hold", "",
        "The current live activation anticipates Elowen Cairn for v671-v1, but x1 deliberately records no prospective recipient because the edge remains terminally gated. No task has been created or forked, no collaboration subagent has been spawned, no standby task has been contacted, and no successor has been contacted. Only after Elowen's clean pushed exact final and terminal validation may the newest authority and roster be refreshed, one exact title uniquely resolved and immediately reread, a duplicate guard applied, and at most one sanitized message sent if every gate permits. Ambiguity, pause, redirect, rename, missing acknowledgement, usage exhaustion, or protected-gate failure stops the route.",
        "", "## Twenty inherited selections with zero Elowen credit", "",
    ]
    prose.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    prose.extend(["", "## Forty frozen Elowen proposals", ""])
    prose.extend(f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}." for row in proposals)
    prose.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(prose)


def build() -> None:
    head, branch = git_text("rev-parse", "HEAD"), git_text("branch", "--show-current")
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 requires {BRANCH} at {SOURCE_FINAL}; found {branch} at {head}")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")
    source_rows = json_blob(SOURCE_FINAL, "docs/tamar-vey/v670-v8/closeout/proposal-ledger-final.json")["rows"]
    if len(source_rows) != 40:
        raise SystemExit("source proposal ledger must contain forty Tamar rows")
    inherited = [
        {
            "selection_id": f"EC6711-I{i:03d}", "source_owner": "Tamar Vey", "source_phase": "v670-v8",
            "source_proposal_id": row["proposal_id"], "source_title": row["title"], "source_outcome": row["observed_outcome"],
            "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "integrity_revalidated": True, "elowen_novelty_credit": 0, "elowen_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for i, row in enumerate(source_rows[:20], start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 40 or len({row["title"] for row in proposals}) != 40 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count, uniqueness, or distribution drifted")
    corpus_summary, source_titles = recover_proposal_corpus()
    if not corpus_summary["id_superset_covers_declared_chain"] or corpus_summary["malformed_or_missing_blobs"] or corpus_summary["corpus_sha256"] != SOURCE_ALL_REF_CORPUS_SHA256:
        raise SystemExit("proposal corpus recovery did not cover the declared chain or contained malformed blobs")
    source_titles = sorted(set(source_titles) | {row["title"] for row in source_rows})
    if len(source_titles) != 5537:
        raise SystemExit(f"all-ref source title count drifted: {len(source_titles)}")
    if corpus_summary["practice_term_hits"] != {"shoemaking": 0, "cobbling": 0}:
        raise SystemExit(f"bounded practice term collision: {corpus_summary['practice_term_hits']}")
    neighbors, max_score = [], 0.0
    for row in proposals:
        left, best_title, best_score = normalize(row["title"]), None, 0.0
        for source_title in source_titles:
            right = normalize(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best_score:
                best_title, best_score = source_title, score
        max_score = max(max_score, best_score)
        neighbors.append({"proposal_id": row["proposal_id"], "source_title": best_title, "jaccard": round(best_score, 6), "collision": best_score >= 0.72})
    if any(row["collision"] for row in neighbors):
        raise SystemExit("semantic neighbor collision requires proposal rewrite")
    frozen_portfolio = portfolio()
    counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected = {"safe_now": 60, "candidates": 30, "exact_approval": 20, "blocked": 10, "skills": 20, "runners": 10, "clean_fix_refine": 60, "successor_skills": 10, "successor_runners": 10, "successor_clean_fix_refine": 30}
    if counts != expected:
        raise SystemExit(f"portfolio count drift: {counts}")
    source = verify_source()
    if not source["all_equal"] or not source["parent_chain"]["exact"] or source["phase_commits"] != 3 or source["merge_commits"] != 0 or source["commit_local_manifest_mismatches"] != 0 or not source["activation_packet"]["integrity_valid"]:
        raise SystemExit("immutable source verification failed")
    x1_overlay = {
        **ACTIVATION_OVERLAY,
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        "elowen_startup_failures": len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }
    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v5", "owner": OWNER, "phase": PHASE, "source_verification": source, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v4", "owner": OWNER, "phase": PHASE, "pronouns": "they/them", "relational_role": "relational boundary cartographer and evidence steward", "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": REPOSITORY_SEAL, "activation_declared_overlay": ACTIVATION_DECLARED_OVERLAY, "post_route_overlay": ACTIVATION_OVERLAY, "elowen_x1_overlay": x1_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v5", "owner": OWNER, "phase": PHASE, "selected": 20, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v5", "owner": OWNER, "phase": PHASE, "all_ref_corpus": corpus_summary, "source_tamar_titles_present": 40, "audited_unique_titles": len(source_titles), "source_chain": 5550, "new_titles": 40, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": 0, "rows": neighbors, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v5", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 5550, "proposal_chain_after_if_evidence_frozen": 5590, "outcomes": OUTCOMES, "planned_invalid_mutations_per_proposal": 4, "planned_invalid_mutations": 160, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v5", "owner": OWNER, "phase": PHASE, "rows": frozen_portfolio, "counts": counts, "ordinary_phase_new_tool_target": 3, "bounded_practice_lenses": ["synthetic footwear last pattern upper sole and component topology with material fit and measurement vacancies", "synthetic stitch adhesive assembly sequence and hazard documentation with competence and safety refusal", "synthetic intake custody rights privacy accessibility correction workload and handover"], "successor_practice_recommendation": "synthetic millinery intake with crown brim trim material-vacancy correction accessibility and handover; recommendation only for the terminally authorized successor", "successor_practice_recommendation_count": 1, "inherited_portfolio_completion_credit": 0, "successor_recommendation_completion_credit": 0, "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v5", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-26", "sources": [
        {"title": "Shoes", "publisher": "Victoria and Albert Museum", "url": "https://www.vam.ac.uk/collections/shoes", "status": "current_page_checked_2026-08-26", "use": "bounded footwear collection and component vocabulary only; not object or professional evidence"},
        {"title": "The art of shoe making", "publisher": "Victoria and Albert Museum", "url": "https://www.vam.ac.uk/articles/the-art-of-shoe-making", "status": "page_updated_2024-04-17_checked_2026-08-26", "use": "bounded last, upper, sole, welt, and construction vocabulary only; not fabrication instruction or competence evidence"},
        {"title": "The International System of Units (SI), 2019 Edition, NIST SP 330", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/publications/international-system-units-si-2019-edition", "status": "current_2019_edition_page_checked_2026-08-26", "use": "unit and dimensional vocabulary with measurement-vacancy boundaries only"},
        {"title": "PROV-O: The PROV Ontology", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/prov-o/", "status": "stable", "use": "provenance vocabulary and responsibility-vacancy boundaries only"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "current", "use": "structural accessibility vocabulary and manual-evaluation reservation only"},
    ], "attributable_read_only_search_queries": 4, "failed_or_truncated_orchestration_attempts": 2, "adapter_calls": 0, "downloads": 0, "real_rows": 0, "external_writes": 0, "boundary": "Sources supply vocabulary and refusal conditions only; they are not observations, measurements, professional advice, validation, legal interpretation, cultural legitimacy, Māori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v5", "owner": OWNER, "phase": PHASE, "assets": ["immutable source lineage", "x1-before-x2 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"], "risks": [
        {"risk": "source or manifest drift", "control": "exact commits, Git-blob replay, and fresh live equality"},
        {"risk": "universal novelty overclaim", "control": "all-ref proposal-title comparison plus explicit exact-canonical-row mapping gap"},
        {"risk": "footwear fit, condition, fabrication, repair, durability, or safety-state promotion", "control": "zero-object fixtures and observation, measurement, quality, and professional firewalls"},
        {"risk": "component, material, construction, unit, or provenance vocabulary promoted into real practice or safety evidence", "control": "typed vacancy fields and likelihood refusal"},
        {"risk": "failure laundering", "control": "append-only Method Flow with failed and passing witnesses"},
        {"risk": "private route or identifier leak", "control": "five-class owner-delta candidate adjudication"},
        {"risk": "accessibility overclaim", "control": "structural-only checks with manual and affected-user evaluation reserved"},
        {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no-resend"},
    ], "not_exhaustive_security": True})
    write_json("x1/method-flow-startup.json", method_flow())
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [{"step": "activation guidance and source verification", "state": "completed_read_only"}, {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"}, {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"}, {"step": "combined closeout and seal", "state": "pending"}, {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"}, {"step": "successor route", "state": "unresolved_until_terminal_live_authority"}], "commit_ceiling": 8, "planned_phase_commits": 3, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5, "materialized_file_guard": 2000, "canonical_invocation_budget": 1, "canonical_success_budget": 1, "post_success_replay": False})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v5", "owner": OWNER, "phase": PHASE, "primary_pillar": "THOS Body", "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"], "bounded_human_practice": "synthetic shoemaking and cobbling documentation only", "proposal_rows": {"inherited_zero_credit": 20, "new": 40}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 5550, "after_if_frozen": 5590}, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_world_actions": 0, "external_writes": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final, attributable terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v5", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 20, "new_rows": 40, "portfolio_counts": counts, "overview_words": len(text.split()), "attributable_read_only_search_queries": 4, "external_writes": 0, "x2_materialized": False})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "new": 40, "outcomes": OUTCOMES, "portfolio": counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split()), "corpus": corpus_summary}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_elowen_cairn_v671_v1_x1.py",
        "tests/test_ghc_family_elowen_cairn_v671_v1_x1.py",
        "docs/elowen-cairn/v671-v1/validation/x1-method-flow-validation.json",
        "docs/elowen-cairn/v671-v1/validation/x1-validation-receipt.json",
        "docs/elowen-cairn/v671-v1/validation/x1-staged-privacy.json",
        "docs/elowen-cairn/v671-v1/validation/x1-staged-review.json",
        "docs/elowen-cairn/v671-v1/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/elowen-cairn/v671-v1/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "mixed_lifecycle": mixed, "valid": not out and not mixed}
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = ["docs/elowen-cairn/v671-v1/validation/x1-manifest.json", "docs/elowen-cairn/v671-v1/validation/x1-staged-review.json"]
    entries = []
    for path in staged_paths():
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/x1-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "x1 exact staged Git blobs before two declared self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x1").rglob("*.json"))
    text_paths = sorted(path for path in (OWNER_ROOT / "x1").rglob("*") if path.is_file())
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label})
    python_paths = [ROOT / "scripts" / "build_ghc_family_elowen_cairn_v671_v1_x1.py", ROOT / "tests" / "test_ghc_family_elowen_cairn_v671_v1_x1.py"]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized_files = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v1", "owner": OWNER, "phase": PHASE,
        "json_documents": len(json_paths), "json_issues": json_issues,
        "text_files": len(text_paths), "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": candidates, "confirmed_privacy_hits": 0 if not candidates else None,
        "python_compiles": len(python_paths), "python_compile_issues": compile_issues,
        "staged_paths_before_receipt": len(staged_paths()), "diff_hygiene_exit": diff.returncode,
        "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"),
        "materialized_files": materialized_files, "file_guard": 2000,
        "x2_absent": not (OWNER_ROOT / "x2").exists(),
        "valid": not json_issues and not candidates and not compile_issues and diff.returncode == 0 and materialized_files < 2000 and not (OWNER_ROOT / "x2").exists(),
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/elowen-cairn/v671-v1/validation/x1-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanned = 0
    for path in staged_paths():
        if path == self_path or Path(path).suffix.lower() not in {".py", ".json", ".md", ".txt", ".html"}:
            continue
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner_surface = path in {
                    "scripts/build_ghc_family_elowen_cairn_v671_v1_x1.py",
                    "tests/test_ghc_family_elowen_cairn_v671_v1_x1.py",
                }
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.staged-privacy-scan.v2", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path], "valid": not confirmed, "boundary": "Scanner definitions and unit-test strings are candidates, never payload hits; every other match fails closed."}
    write_json("validation/x1-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_privacy:
        staged_privacy()
    else:
        build()


if __name__ == "__main__":
    main()
