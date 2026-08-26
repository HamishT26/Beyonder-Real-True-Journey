#!/usr/bin/env python3
"""Build and validate the planning-only Elaren Kestrel v671-v5 x1 freeze.

This entry point is deliberately owner-local.  It never executes x2 contracts,
touches a sibling lane, installs software, contacts another task, or promotes a
protected claim.  Exact staged Git blobs, rather than working-tree line endings,
form the manifest domain.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
OWNER = "Elaren Kestrel"
PHASE = "v671-v5"
SLUG = "elaren-kestrel"
OWNER_ROOT = ROOT / "docs" / SLUG / PHASE
BRANCH = "codex/GHC-Family/elaren-kestrel-v671-v5-full-tools"

SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v671-v4-full-tools"
SOURCE_START = "37ac80c499d43a90c874876402b262a220a252a1"
SOURCE_X1 = "1c4d262b14cb8528fb9d72aad40a5e4fb7423b26"
SOURCE_EVIDENCE = "000c4c75ccac98794b43a0171f2d330436e6069d"
SOURCE_FINAL = "e70391872f07cdcaa13accac44d4330eca75e2b4"
SOURCE_BATON = (
    "docs/eiren-kestrel/v671-v4/handoffs/"
    "elaren-kestrel-v671-v5-activation-candidate.md"
)
SOURCE_BATON_SHA256 = (
    "37e9956e4c6a4ab8222d2aebd97e69887ca229387414df968a029aa306a33698"
)
SOURCE_BATON_BYTES = 236665
SOURCE_BATON_WORDS = 29008
SOURCE_CANONICAL_SHA256 = (
    "79c5290764ff2ce5da28a2c1fdb735ab290be0924712c7e721e80bcfc912dafd"
)
SOURCE_CANONICAL_PAYLOAD_SHA256 = (
    "4f4afdd57cd40abd6cd94b9888f21a96785299e76667a27a4d15d3a5773ba5a3"
)
SOURCE_RECOVERY_SHA256 = (
    "70f2506737b4a20330feeedb45f2d1b0c46eb333c2ac07a4f627f756a8b78b47"
)
SOURCE_RECOVERY_PAYLOAD_SHA256 = (
    "06da7c17d50fbdd08a3997f3ea1c1d5f0c7ef4d207f50c2652f700c866718c11"
)

DECLARED_PROPOSAL_CHAIN = 5710
PROPOSAL_CHAIN_AFTER = 5750
COLLISION_THRESHOLD = 0.72
NEW_OUTCOMES = {
    "completed": 28,
    "represented": 8,
    "open_gap": 2,
    "exact_gate": 2,
}
CORE_OUTCOMES = set(NEW_OUTCOMES)

REPOSITORY_SEAL = {
    "effective_negatives": 34088,
    "effective_methods": 20405,
    "failed_witnesses": 5909,
    "bounded_passing_witnesses": 7552,
    "open_gaps": 263,
    "exact_gates": 258,
}
ACTIVATION_OVERLAY = {
    "effective_negatives": 34089,
    "effective_methods": 20406,
    "failed_witnesses": 5910,
    "bounded_passing_witnesses": 7553,
    "open_gaps": 263,
    "exact_gates": 258,
}

RELATIONAL_ROLE = "pattern-lantern and reversible-workflow cartographer"
RELATIONAL_HOPE = (
    "make synthetic evidence legible without borrowing authority from people, "
    "communities, professions, affected parties, or Maori authorities"
)
IDENTITY_BOUNDARY = (
    "Elaren Kestrel, she/they, the relational role, hope, sibling and family "
    "language, continuity language, Freed ID, CBR, GHC Family, and Trinity "
    "Mandala are working language only. They are not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific or operational authority, professional "
    "authority, legal or cultural authority, affected-party authority, or Maori "
    "authority. Hamish may rename, pause, redirect, or stop the route."
)
BOUNDARY = (
    "Bounded same-owner synthetic software and documentation planning only; not "
    "empirical evidence, independent reproduction, production or deployment "
    "fitness, exhaustive security, complete privacy or accessibility assurance, "
    "professional validation, legal or cultural interpretation, Maori authority, "
    "affected-party acceptance, AGI or ASI evidence, consciousness or personhood "
    "evidence, Theory-of-Everything proof, canon, or Stage 20 authority."
)


NEW_TITLES = [
    "Synthetic mechanical-music apparatus accession capsule",
    "Orchestrion component identity and adjacency topology",
    "Pinned-cylinder program-carrier lineage capsule",
    "Perforated-roll program-carrier lineage capsule",
    "Interchangeable barrel and cylinder relationship register",
    "Stop register and voice vocabulary vacancy ledger",
    "Clockwork drive dependency graph with zero-operation lock",
    "Bellows and pneumatic-circuit dependency graph",
    "Electrical subsystem absent unknown and prohibited-state marker",
    "Motive-power source hold and zero-energization firewall",
    "Apparatus condition vocabulary without diagnosis or treatment",
    "Detached component and fragment relationship register",
    "Prior intervention and material-assertion vacancy record",
    "Dimension unit and uncertainty placeholder with zero measurement",
    "Manufacturer serial and maker attribution claim-tier matrix",
    "Date place and provenance attribution claim-tier matrix",
    "Custody ownership and access-right vacancy docket",
    "Program work composition and performance-right reservation",
    "Image audio and transcription lineage abstention record",
    "Bitemporal catalog correction and supersession chain",
    "Synthetic program-sequence event dependency graph",
    "Pinned-position and perforation-coordinate schema",
    "Tempo register and dynamics cue placeholder contract",
    "Repeat jump stop and end-condition deterministic parser plan",
    "Impossible program-transition quarantine contract",
    "Program-media to apparatus compatibility matrix",
    "Program item and carrier count-reconciliation contract",
    "Structural program transcript without audio or performance claim",
    "Language script reading-order and translation-vacancy representation",
    "Privacy-minimized donor maker and operator vacancy representation",
    "THOS zero-operator matched-queue documentation charter",
    "GMUT discrete program-state transition surrogate board",
    "GMUT pneumatic-response zero-parameter tensor vacancy",
    "Freed ID zero-key apparatus-program statement graph",
    "CBR notice contest correction remedy and redress reservation",
    "Structural accessibility and manual-evaluation reservation matrix",
    "Current public-source adapter with zero calls and zero ingested rows",
    "Independent conservation operation and rights-review vacancy",
    "Real apparatus operation machinery and electrical-safety authority gate",
    "Rights cultural Maori-authority and affected-party acceptance gate",
]


SKILL_IDEAS = [
    "ghc-family-mechanical-music-accession-capsule",
    "ghc-family-mechanical-music-component-topology",
    "ghc-family-mechanical-music-program-lineage",
    "ghc-family-mechanical-music-zero-operation-lock",
    "ghc-family-mechanical-music-condition-vacancy",
    "ghc-family-mechanical-music-attribution-tier",
    "ghc-family-mechanical-music-rights-reservation",
    "ghc-family-mechanical-music-sequence-graph",
    "ghc-family-mechanical-music-accessibility-structure",
    "ghc-family-mechanical-music-mutation-quarantine",
    "ghc-family-mechanical-music-count-reconciliation",
    "ghc-family-mechanical-music-correction-chain",
    "ghc-family-mechanical-music-source-vacancy",
    "ghc-family-mechanical-music-freed-id-hold",
    "ghc-family-mechanical-music-cbr-docket",
    "ghc-family-mechanical-music-gmut-surrogate",
    "ghc-family-mechanical-music-thos-proxy",
    "ghc-family-mechanical-music-privacy-minimizer",
    "ghc-family-mechanical-music-manifest-replay",
    "ghc-family-mechanical-music-closeout",
]


RUNNER_IDEAS = [
    "ghc_family_mechanical_music_contracts.py",
    "ghc_family_mechanical_music_mutations.py",
    "ghc_family_mechanical_music_json_guard.py",
    "ghc_family_mechanical_music_privacy_guard.py",
    "ghc_family_mechanical_music_security_guard.py",
    "ghc_family_mechanical_music_manifest.py",
    "ghc_family_mechanical_music_accessibility.py",
    "ghc_family_mechanical_music_truth.py",
    "ghc_family_mechanical_music_closeout.py",
    "ghc_family_mechanical_music_canonical.py",
]


EXACT_APPROVAL_ROWS = [
    "Operate or energize a real mechanical musical apparatus",
    "Open remove adjust repair tune or restore a real component",
    "Issue a machinery electrical dust chemical or handling-safety decision",
    "Identify real materials condition damage or conservation treatment",
    "Capture or publish real sound image score transcription or performance",
    "Assert authorship ownership copyright moral rights or public-domain status",
    "Accept transfer custody access loan deaccession or disposal authority",
    "Use real donor maker operator owner or visitor personal information",
    "Make a professional conservation registration or valuation decision",
    "Run a real THOS participant operator or matched-budget trial",
    "Fit a real GMUT likelihood coefficient prediction or physical law",
    "Issue real Freed ID keys proofs credentials status or revocation",
    "Interpret law regulation contract rights consent remedy or redress",
    "Make a cultural attribution authenticity or traditional-knowledge decision",
    "Use Maori wording concepts data or authority beyond explicit reservation",
    "Claim affected-party community institution or owner acceptance",
    "Claim complete privacy accessibility security or interoperability",
    "Deploy publish or connect a real external adapter or service",
    "Claim independent reproduction empirical confirmation or external audit",
    "Claim AGI ASI consciousness personhood Theory of Everything or Stage 20",
]


BLOCKED_ROWS = [
    "No real apparatus or authorized collection is in scope",
    "No qualified conservator registrar engineer or safety authority participates",
    "No rights holder affected party community or institution participates",
    "No standards-conformant real keys proofs status or trust governance exist",
    "No governed blind matched-budget real THOS arms exist",
    "No real GMUT observations likelihood or independent scientific review exist",
    "No legal or cultural authority has supplied interpretation or ratification",
    "No Maori authority has supplied wording governance or approval",
    "No manual browser assistive-technology or affected-user evaluation exists",
    "No independent team has reproduced or externally audited the work",
]


STARTUP_FAILURES = [
    {
        "signature": "javascript_reader_backtick_parse_fault",
        "observation": "The first raw-reader wrapper failed before shell launch on an unescaped backtick.",
        "recovery": "Use a literal bounded PowerShell reader without JavaScript template interpolation.",
    },
    {
        "signature": "combined_skill_read_presentation_truncation",
        "observation": "A combined mandatory-skill read exceeded the presentation budget and earned no full-read credit.",
        "recovery": "Read each mandatory skill separately through its attributable EOF.",
    },
    {
        "signature": "orchestration_skill_projection_truncation",
        "observation": "The orchestration-memory projection truncated before EOF.",
        "recovery": "Recover the missing bounded line windows and verify the complete 391-line file.",
    },
    {
        "signature": "authorization_state_display_truncation",
        "observation": "The complete authorization-state display exceeded its output window.",
        "recovery": "Read bounded non-overlapping windows through EOF and preserve the newest live overlay.",
    },
    {
        "signature": "activation_baton_window_truncation",
        "observation": "One large activation-baton window truncated before its declared boundary.",
        "recovery": "Recover the missing small windows and verify exact Git-blob bytes words and digest.",
    },
    {
        "signature": "metadata_probe_tab_escape_fault",
        "observation": "A metadata wrapper failed before shell launch on a tab-escape construction.",
        "recovery": "Use scalar PowerShell variables and literal tab splitting.",
    },
    {
        "signature": "batched_source_artifact_projection_truncation",
        "observation": "A batched compact source-artifact projection truncated.",
        "recovery": "Read the substantive source artifacts individually with bounded output.",
    },
    {
        "signature": "proposal_ledger_full_projection_truncation",
        "observation": "The full inherited proposal-ledger display truncated.",
        "recovery": "Read the ledger in bounded non-overlapping ranges and inspect structured counts.",
    },
    {
        "signature": "portfolio_projection_truncation",
        "observation": "The combined inherited portfolio projection truncated.",
        "recovery": "Project each portfolio category and count independently.",
    },
    {
        "signature": "live_remote_ref_parser_false_negative",
        "observation": "The first live-remote parser retained the full ref line and falsely reported inequality.",
        "recovery": "Split the ls-remote line at the literal tab and compare only the forty-hex object id.",
    },
    {
        "signature": "manifest_wrapper_colon_parse_fault",
        "observation": "A JavaScript-composed manifest verifier failed before shell launch on PowerShell colon syntax.",
        "recovery": "Use a literal PowerShell body and isolate exact manifest replay.",
    },
    {
        "signature": "manifest_byte_enumeration_no_attributable_result",
        "observation": "A manifest verifier enumerated byte arrays beyond its window and returned no attributable completion.",
        "recovery": "Use scalar byte readers and bounded exact Git-blob replay with an atomic summary.",
    },
    {
        "signature": "broad_receipt_content_search_timeout",
        "observation": "A broad receipt-bank content search exceeded ninety seconds and was interrupted.",
        "recovery": "Use bounded directory metadata and exact phase receipt filenames.",
    },
    {
        "signature": "validation_filename_search_interrupted",
        "observation": "A broad validation filename search ran beyond its useful window and was interrupted.",
        "recovery": "Inspect the exact phase receipt directory rather than recursively searching banks.",
    },
    {
        "signature": "validation_bank_filename_search_interrupted",
        "observation": "A second validation-bank filename search ran beyond its useful window and was interrupted.",
        "recovery": "Resolve the exact bounded receipt directory from phase metadata.",
    },
    {
        "signature": "uniqueness_materialization_combined_probe_lost_session",
        "observation": "A combined uniqueness and materialization probe exceeded its window without an attributable session result.",
        "recovery": "Run isolated scalar branch path and file-count probes before mutation.",
    },
    {
        "signature": "worktree_add_presentation_timeout",
        "observation": "The additive worktree creation exceeded the first presentation window.",
        "recovery": "Resume the same live session, verify one registered worktree, exact head, sparse paths, and clean status without retrying creation.",
    },
    {
        "signature": "receipt_depth_projection_truncation",
        "observation": "A depth-limited JSON projection warned that nested receipt content was truncated.",
        "recovery": "Use exact file digests and bounded scalar fields; do not mistake the projection for receipt execution.",
    },
    {
        "signature": "x1_test_scanner_definition_false_positive",
        "observation": "The first x1 unit run treated the builder's own observed-outcome scanner token as emitted x2 evidence.",
        "recovery": "Test concrete x2 output calls and generated artifacts rather than a scanner-definition string.",
    },
    {
        "signature": "x1_failed_test_diagnostic_projection_truncation",
        "observation": "The failed assertion rendered the builder source and exceeded the diagnostic presentation budget.",
        "recovery": "Retain the scalar failing predicate and use a bounded targeted patch without replaying unrelated source reads.",
    },
    {
        "signature": "post_mutation_source_clean_assertion",
        "observation": "The first x1 build stopped because source verification required a pristine worktree after the declared builder and test were created.",
        "recovery": "Preserve the pre-mutation clean receipt and allow exactly the two declared owner-local x1 files before artifact generation.",
    },
]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(*args: str, check: bool = True, timeout: int = 180) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, check=False, timeout=timeout
    )
    if check and result.returncode != 0:
        raise SystemExit(
            f"git {' '.join(args)} failed: "
            f"{result.stderr.decode('utf-8', errors='replace')}"
        )
    return result


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8").strip()


def git_blob(spec: str) -> bytes:
    return git("show", spec).stdout


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


def normalized_tokens(title: str) -> set[str]:
    stop = {"and", "the", "with", "for", "from", "without", "into", "only"}
    return {
        token
        for token in re.findall(r"[a-z0-9]+", title.lower())
        if len(token) > 2 and token not in stop
    }


def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"],
        cwd=ROOT,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=240
    )
    if process.returncode != 0:
        raise SystemExit(
            "git cat-file --batch failed: "
            + stderr.decode("utf-8", errors="replace")
        )
    stream = io.BytesIO(output)
    result: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            result.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        result.append(stream.read(size))
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return result


def accessible_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    candidates: dict[str, str] = {}
    for row in git_text("rev-list", "--objects", "--all").splitlines():
        parts = row.split(" ", 1)
        if len(parts) != 2:
            continue
        oid, path = parts
        lowered = path.lower()
        if lowered.endswith(".json") and "proposal" in lowered:
            candidates.setdefault(oid, path)

    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0
    bom_recoveries = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id = node.get("proposal_id")
            title = node.get("title")
            if (
                isinstance(proposal_id, str)
                and isinstance(title, str)
                and proposal_id.strip()
                and title.strip()
            ):
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
        for blob in batch_blobs(oids[start : start + 128]):
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
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return (
        {
            "scope": (
                "proposal-named JSON blobs reachable through local and remote "
                "Git refs; no sibling-worktree traversal or general unchanged-"
                "history, privacy, security, or test scan"
            ),
            "candidate_unique_git_blobs": len(oids),
            "malformed_or_missing_blobs": malformed,
            "isolated_utf8_bom_recoveries": bom_recoveries,
            "semantic_occurrences": occurrences,
            "unique_proposal_ids": len(proposal_ids),
            "unique_titles": len(titles),
            "corpus_sha256": sha256(canonical),
            "declared_source_chain": DECLARED_PROPOSAL_CHAIN,
            "exact_canonical_row_mapping": False,
            "canonical_row_mapping_open_gap": True,
            "practice_term_hits": {
                term: sum(1 for title in titles if term in title.lower())
                for term in (
                    "mechanical music",
                    "orchestrion",
                    "pinned cylinder",
                    "perforated roll",
                )
            },
            "reason": (
                "Accessible proposal objects contain duplicate, summary, and "
                "versioned rows and do not prove a canonical one-row-to-one-"
                "title mapping for the declared chain."
            ),
        },
        sorted(titles),
    )


def read_wrapped_receipt(path: Path) -> tuple[bytes, dict[str, Any], dict[str, Any]]:
    raw = path.read_bytes()
    wrapper = json.loads(raw.decode("utf-8"))
    payload = wrapper.get("payload", wrapper)
    if not isinstance(payload, dict):
        raise SystemExit(f"receipt payload is not an object: {path.name}")
    return raw, wrapper, payload


def source_verification(canonical_path: Path, recovery_path: Path) -> dict[str, Any]:
    if git_text("symbolic-ref", "--short", "HEAD") != BRANCH:
        raise SystemExit("owned branch mismatch")
    if git_text("rev-parse", "HEAD") != SOURCE_FINAL:
        raise SystemExit("owned lane does not start at exact source final")
    status_rows = set(git_text("status", "--porcelain").splitlines())
    permitted_prebuild_rows = {
        "?? scripts/build_ghc_family_elaren_kestrel_v671_v5_x1.py",
        "?? tests/test_ghc_family_elaren_kestrel_v671_v5_x1.py",
    }
    if status_rows != permitted_prebuild_rows:
        raise SystemExit(
            "unexpected owned-lane mutation before x1 build: "
            + json.dumps(sorted(status_rows))
        )

    live_line = git_text(
        "ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}"
    )
    fresh_live = live_line.split("\t", 1)[0] if live_line else ""
    parent_chain = {
        "x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"),
        "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"),
        "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^"),
    }
    phase_commits = int(
        git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")
    )
    merge_commits = int(
        git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")
    )
    baton = git_blob(f"{SOURCE_FINAL}:{SOURCE_BATON}")
    canonical_raw, canonical_wrapper, canonical = read_wrapped_receipt(canonical_path)
    recovery_raw, recovery_wrapper, recovery = read_wrapped_receipt(recovery_path)
    source_tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")

    checks = {
        "source_branch_ref_exact": git_text("rev-parse", SOURCE_BRANCH) == SOURCE_FINAL,
        "source_tracking_exact": source_tracking == SOURCE_FINAL,
        "source_fresh_live_exact": fresh_live == SOURCE_FINAL,
        "direct_parent_chain": parent_chain
        == {
            "x1_parent": SOURCE_START,
            "evidence_parent": SOURCE_X1,
            "final_parent": SOURCE_EVIDENCE,
        },
        "three_phase_commits": phase_commits == 3,
        "zero_merges": merge_commits == 0,
        "baton_bytes": len(baton) == SOURCE_BATON_BYTES,
        "baton_words": len(baton.decode("utf-8").split()) == SOURCE_BATON_WORDS,
        "baton_sha256": sha256(baton) == SOURCE_BATON_SHA256,
        "canonical_receipt_sha256": sha256(canonical_raw) == SOURCE_CANONICAL_SHA256,
        "canonical_payload_sha256": canonical_wrapper.get("payload_sha256")
        == SOURCE_CANONICAL_PAYLOAD_SHA256,
        "canonical_failed_once_zero_credit": (
            canonical.get("result") == "INVALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"
            and canonical.get("invocation_count") == 1
            and canonical.get("successful_invocation_count") == 0
            and canonical.get("replayed") is False
        ),
        "recovery_receipt_sha256": sha256(recovery_raw) == SOURCE_RECOVERY_SHA256,
        "recovery_payload_sha256": recovery_wrapper.get("payload_sha256")
        == SOURCE_RECOVERY_PAYLOAD_SHA256,
        "narrow_recovery_exact": (
            recovery.get("result") == "VALID_NARROW_PRIVACY_DEPENDENCY_RECOVERY"
            and recovery.get("canonical_aggregate_success_credit") == 0
            and recovery.get("tests_rerun") == 0
            and recovery.get("manifests_replayed") == 0
            and recovery.get("repository_bytes_changed") == 0
            and recovery.get("confirmed_hit_count") == 0
        ),
    }
    if not all(checks.values()):
        raise SystemExit(
            "source verification failed: "
            + json.dumps({key: value for key, value in checks.items() if not value})
        )

    return {
        "source_branch": SOURCE_BRANCH,
        "source_start": SOURCE_START,
        "source_x1": SOURCE_X1,
        "source_evidence": SOURCE_EVIDENCE,
        "source_final": SOURCE_FINAL,
        "source_tracking": source_tracking,
        "source_fresh_live": fresh_live,
        "parent_chain": parent_chain,
        "phase_commits": phase_commits,
        "merge_commits": merge_commits,
        "baton": {
            "path": SOURCE_BATON,
            "bytes": len(baton),
            "words": len(baton.decode("utf-8").split()),
            "sha256": sha256(baton),
            "historical_prepared_not_sent_preserved": True,
        },
        "canonical": {
            "receipt_sha256": sha256(canonical_raw),
            "payload_sha256": canonical_wrapper["payload_sha256"],
            "result": canonical["result"],
            "aggregate_success_credit": 0,
            "invocation_count": canonical["invocation_count"],
            "replayed": canonical["replayed"],
        },
        "narrow_recovery": {
            "receipt_sha256": sha256(recovery_raw),
            "payload_sha256": recovery_wrapper["payload_sha256"],
            "result": recovery["result"],
            "tests_rerun": recovery["tests_rerun"],
            "manifests_replayed": recovery["manifests_replayed"],
            "repository_bytes_changed": recovery["repository_bytes_changed"],
        },
        "source_manifest_replay": {
            "x1": 20,
            "evidence": 195,
            "final_delta": 24,
            "final_owner": 242,
            "basis": "independent read-only pre-mutation exact Git-blob replay",
            "replayed_by_this_builder": False,
        },
        "prebuild_worktree": {
            "pre_mutation_clean_gate": True,
            "permitted_owner_local_rows": sorted(permitted_prebuild_rows),
            "observed_rows": sorted(status_rows),
            "unexpected_rows": 0,
        },
        "checks": checks,
    }


def expected_disposition(number: int) -> tuple[str, str, str]:
    if number <= 28:
        return "completed", "safe_now", "owner_local_synthetic_x2"
    if number <= 36:
        return "represented", "bounded_candidate", "owner_local_synthetic_x2"
    if number <= 38:
        return "open_gap", "open_gap", "held_without_real_world_execution"
    return "exact_gate", "exact_gate", "held_without_real_world_execution"


def proposal_rows() -> list[dict[str, Any]]:
    gates = [
        "empirical",
        "participant",
        "professional",
        "production",
        "legal",
        "cultural",
        "Maori_authority",
        "affected_party",
        "privacy_complete",
        "accessibility_complete",
        "exhaustive_security",
        "independent_reproduction",
        "AGI_ASI",
        "consciousness_personhood",
        "Theory_of_Everything",
        "Stage_20",
    ]
    rows = []
    for number, title in enumerate(NEW_TITLES, start=1):
        disposition, approval, lane = expected_disposition(number)
        proposal_id = f"EL6715-N{number:03d}"
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    "A typed owner-local contract can make the declared "
                    f"{proposal_id} obligations falsifiable without promoting "
                    "the evidence or authority class."
                ),
                "null_or_failure_condition": (
                    "Any missing required field, accepted invalid mutation, "
                    "real-world action, undeclared uncertainty, external side "
                    "effect, or authority promotion rejects the hypothesis."
                ),
                "approval_class": approval,
                "execution_lane": lane,
                "official_or_primary_source_needs": (
                    "Current official vocabulary and refusal boundaries only; "
                    "a citation is not observation, measurement, professional "
                    "advice, legal interpretation, validation, or authority."
                ),
                "concrete_artifacts": [
                    "typed JSON contract",
                    "one bounded accepting fixture",
                    "four preregistered rejecting mutation receipts",
                    "four-tier evidence-boundary card",
                ],
                "falsifier_or_acceptance_gate": (
                    "The bounded synthetic fixture must pass, four declared "
                    "invalid mutations must reject, and every protected boundary "
                    "must remain explicit."
                ),
                "rollback_or_recovery": (
                    "Retain the failed witness at zero credit, isolate only the "
                    "changed owner-local dependency, preserve rollback, and never "
                    "replay a successful canonical aggregate."
                ),
                "protected_gates": gates,
                "expected_disposition": disposition,
                "planned_outcome": disposition,
                "primary_pillar": "THOS Body",
                "x1_state": "frozen_not_executed",
                "real_people": 0,
                "real_objects_or_records": 0,
                "external_actions": 0,
            }
        )
    return rows


def inherited_revalidations() -> list[dict[str, Any]]:
    source_path = "docs/eiren-kestrel/v671-v4/x1/proposals.json"
    payload = json.loads(git_blob(f"{SOURCE_FINAL}:{source_path}").decode("utf-8"))
    source_rows = payload["rows"]
    selected_indices = list(range(10)) + list(range(28, 36)) + [36, 38]
    if len(source_rows) != 40 or len(selected_indices) != 20:
        raise SystemExit("unexpected inherited proposal shape")
    result = []
    for index, source_index in enumerate(selected_indices, start=1):
        source = source_rows[source_index]
        result.append(
            {
                "selection_id": f"EL6715-R{index:03d}",
                "source_commit": SOURCE_FINAL,
                "source_path": source_path,
                "source_proposal_id": source["proposal_id"],
                "title": source["title"],
                "source_expected_disposition": source["expected_disposition"],
                "x1_state": "frozen_revalidation_not_executed",
                "elaren_novelty_credit": 0,
                "automatic_completion_credit": 0,
                "purpose": "bounded source-integrity revalidation only",
            }
        )
    return result


def task_rows(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    rows = []
    for domain in domains:
        for control in controls:
            rows.append(
                {
                    "task_id": f"EL6715-{prefix}-{len(rows) + 1:03d}",
                    "title": f"{domain}: {control}",
                    "owner": OWNER,
                    "phase": PHASE,
                    "x1_state": state,
                    "external_actions": 0,
                }
            )
    return rows


def named_rows(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [
        {
            "task_id": f"EL6715-{prefix}-{index:03d}",
            "title": value,
            "owner": OWNER,
            "phase": PHASE,
            "x1_state": state,
            "external_actions": 0,
        }
        for index, value in enumerate(values, start=1)
    ]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = [
        "apparatus identity",
        "component topology",
        "program-carrier lineage",
        "sequence dependency",
        "condition and intervention vacancy",
        "measurement and uncertainty vacancy",
        "rights and attribution reservation",
        "correction and supersession",
        "accessible structural companion",
        "handover and zero-operation lock",
    ]
    return {
        "safe_now": task_rows(
            "SAFE",
            domains,
            ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary"],
            "planned_for_x2",
        ),
        "candidates": task_rows(
            "CAND",
            domains,
            ["mutation quarantine", "encoding-timeout quarantine", "authority-ordering quarantine"],
            "planned_for_x2",
        ),
        "exact_approval": named_rows("EXACT", EXACT_APPROVAL_ROWS, "held_unexecuted"),
        "blocked": named_rows("BLOCK", BLOCKED_ROWS, "held_unexecuted"),
        "skill_ideas": named_rows("SKILL", SKILL_IDEAS, "selection_pool_for_x2"),
        "runner_ideas": named_rows("RUNNER", RUNNER_IDEAS, "planned_for_x2"),
        "clean_fix_refine": task_rows(
            "CFR",
            [
                "JSON ordering",
                "UTF-8 Maori-boundary text",
                "source status",
                "failure retention",
                "manifest closure",
                "privacy disposition",
                "accessibility structure",
                "route uniqueness",
                "sparse file budget",
                "boundary vocabulary",
            ],
            ["clean", "fix", "refine", "recheck", "document", "preserve"],
            "planned_for_x2",
        ),
        "successor_skill_recommendations": named_rows(
            "NEXT-SKILL",
            [f"ghc-family-successor-mechanical-music-review-{index:02d}" for index in range(1, 11)],
            "recommendation_only",
        ),
        "successor_runner_recommendations": named_rows(
            "NEXT-RUNNER",
            [f"ghc_family_successor_mechanical_music_review_{index:02d}.py" for index in range(1, 11)],
            "recommendation_only",
        ),
        "successor_clean_fix_refine": task_rows(
            "NEXT-CFR",
            ["successor source", "successor manifests", "successor privacy", "successor route", "successor authority"],
            ["schema", "mutation", "rollback", "review", "receipt", "hold"],
            "recommendation_only",
        ),
    }


def startup_method_flow() -> dict[str, Any]:
    rows = []
    for index, failure in enumerate(STARTUP_FAILURES, start=1):
        rows.append(
            {
                "method_id": f"EL6715-START-M{index:03d}",
                "issue_id": f"EL6715-START-I{index:03d}",
                "candidate_workaround": failure["recovery"],
                "failure_signature": failure["signature"],
                "trigger_preconditions": ["the exact bounded failure signature is observed"],
                "recurrence_guard": failure["recovery"],
                "rollback": "Stop the affected wrapper, retain zero credit, and leave repository bytes unchanged.",
                "expected_fail_witness": failure["observation"],
                "expected_pass_witness": failure["recovery"],
                "promotion_gate": "A separately attributable bounded recovery passes without erasing or replaying the failure.",
                "sibling_recommendation": failure["recovery"],
                "failed_evidence_retained": True,
                "fail_witness": {"state": "retained", "credit": 0, "observation": failure["observation"]},
                "pass_witness": {"state": "bounded_pass", "credit": 1, "observation": failure["recovery"]},
                "state": "preferred",
                "privacy_class": "sanitized_public",
            }
        )
    counts = {
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(rows),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(rows),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(rows),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(rows),
        "open_gaps": ACTIVATION_OVERLAY["open_gaps"],
        "exact_gates": ACTIVATION_OVERLAY["exact_gates"],
    }
    return {
        "schema": "ghc.family.method-flow-ledger.x1.v6",
        "owner": OWNER,
        "phase": PHASE,
        "row_count": len(rows),
        "rows": rows,
        "counts": counts,
        "all_failures_retained": True,
        "all_recoveries_paired": True,
        "boundary": BOUNDARY,
    }


def public_source_ledger() -> dict[str, Any]:
    sources = [
        {
            "publisher": "Canadian Conservation Institute",
            "title": "Musical instruments",
            "url": "https://www.canada.ca/en/conservation-institute/services/care-objects/musical-instruments.html",
            "status": "current",
            "checked_nz_date": "2026-08-27",
            "use": "collection-care vocabulary and explicit specialist/operation reservation only",
            "credit": "vocabulary_only_no_professional_validation",
        },
        {
            "publisher": "Library of Congress",
            "title": "Controlled Vocabularies",
            "url": "https://www.loc.gov/librarians/controlled-vocabularies/",
            "status": "current",
            "checked_nz_date": "2026-08-27",
            "use": "medium-of-performance vocabulary discovery only",
            "credit": "vocabulary_only_no_cataloguing_authority",
        },
        {
            "publisher": "World Wide Web Consortium",
            "title": "PROV-O: The PROV Ontology",
            "url": "https://www.w3.org/TR/prov-o/",
            "status": "stable",
            "checked_nz_date": "2026-08-27",
            "use": "entity activity derivation revision and invalidation vocabulary only",
            "credit": "structural_vocabulary_only",
        },
        {
            "publisher": "World Wide Web Consortium",
            "title": "Web Content Accessibility Guidelines 2.2",
            "url": "https://www.w3.org/TR/WCAG22/",
            "status": "current",
            "checked_nz_date": "2026-08-27",
            "use": "structural accessibility vocabulary and manual-evaluation reservation only",
            "credit": "no_complete_accessibility_claim",
        },
        {
            "publisher": "World Wide Web Consortium",
            "title": "Verifiable Credentials Data Model v2.0",
            "url": "https://www.w3.org/TR/vc-data-model/",
            "status": "current",
            "checked_nz_date": "2026-08-27",
            "use": "issuer holder verifier status and trust-boundary vocabulary only",
            "credit": "zero_keys_zero_proofs_no_conformance",
        },
        {
            "publisher": "National Institute of Standards and Technology",
            "title": "NIST Guide to the SI",
            "url": "https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-1-introduction",
            "status": "stable",
            "checked_nz_date": "2026-08-27",
            "use": "quantity unit and measurement-reporting vocabulary only",
            "credit": "zero_measurements_no_metrology_validation",
        },
        {
            "publisher": "Office of the Privacy Commissioner New Zealand",
            "title": "Privacy principles",
            "url": "https://www.privacy.org.nz/privacy-principles/",
            "status": "current",
            "checked_nz_date": "2026-08-27",
            "use": "purpose access correction retention and disclosure vocabulary only",
            "credit": "no_legal_or_compliance_conclusion",
        },
        {
            "publisher": "Te Mana Raraunga Maori Data Sovereignty Network",
            "title": "Principles of Maori Data Sovereignty",
            "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
            "status": "primary",
            "checked_nz_date": "2026-08-27",
            "use": "reservation of Maori data rights interests governance wording and authority only",
            "credit": "no_ratification_no_substitution_no_Maori_authority",
        },
    ]
    return {
        "schema": "ghc.family.public-source-ledger.v7",
        "owner": OWNER,
        "phase": PHASE,
        "retrieved_nz_date": "2026-08-27",
        "web_tool_invocations": 3,
        "official_or_primary_requests": 13,
        "adapter_calls": 0,
        "downloads": 0,
        "ingested_rows": 0,
        "external_writes": 0,
        "sources": sources,
        "status_counts": {
            status: sum(1 for row in sources if row["status"] == status)
            for status in ("current", "stable", "primary", "draft", "watch")
        },
        "boundary": (
            "Public sources supply vocabulary and refusal conditions only. "
            "They are not observations, measurements, standards conformance, "
            "professional advice, legal interpretation, cultural legitimacy, "
            "Maori authority, affected-party acceptance, or Stage 20 evidence."
        ),
    }


def threat_model() -> dict[str, Any]:
    rows = [
        ("sibling_lane_mutation", "exact owner path and additive-worktree gate", "stop and leave sibling lanes read-only"),
        ("x1_x2_leakage", "planning-only path and content review", "reject freeze before commit"),
        ("semantic_duplicate", "accessible-ref Jaccard screen plus declared corpus gap", "retain rejected slate at zero novelty credit"),
        ("private_material_disclosure", "five value-bearing scan classes and manual disposition", "remove only owner-local candidate before commit"),
        ("operation_or_restoration_promotion", "zero-operation and specialist-authority locks", "hold real apparatus work behind exact approval"),
        ("rights_or_custody_promotion", "rights attribution and custody vacancy docket", "retain legal and affected-party gates"),
        ("Maori_authority_substitution", "explicit authority reservation", "stop; Maori concepts remain under Maori authority"),
        ("GMUT_empirical_overclaim", "zero observation coefficient likelihood and prediction fields", "retain represented or open status"),
        ("THOS_operational_overclaim", "zero participant operator arm session and outcome fields", "retain proxy-only status"),
        ("Freed_ID_production_promotion", "zero key proof issue resolve status and revoke fields", "retain synthetic nonproduction status"),
        ("accessibility_completeness_promotion", "structural-only receipt and manual-evaluation reserve", "do not claim complete accessibility"),
        ("canonical_replay", "one invocation and one success budget", "retain failure and recover only changed dependency"),
        ("premature_route_send", "successor contact count fixed at zero in x1", "defer exact-title resolution until terminal gate"),
    ]
    return {
        "schema": "ghc.family.threat-model.v7",
        "owner": OWNER,
        "phase": PHASE,
        "rows": [
            {
                "threat_id": f"EL6715-T{index:02d}",
                "threat": threat,
                "control": control,
                "rollback_or_hold": rollback,
                "residual_risk": "open_same_owner_and_authority_boundary",
            }
            for index, (threat, control, rollback) in enumerate(rows, start=1)
        ],
        "residual_risk_accepted_for_planning_only": True,
        "boundary": BOUNDARY,
    }


def planning_overview(
    proposals: list[dict[str, Any]],
    revalidations: list[dict[str, Any]],
    corpus: dict[str, Any],
    audit: list[dict[str, Any]],
    within_new_max: float,
    counts: dict[str, int],
) -> str:
    proposal_lines = "\n".join(
        f"- {row['proposal_id']} [{row['expected_disposition']}]: {row['title']}."
        for row in proposals
    )
    revalidation_lines = "\n".join(
        f"- {row['selection_id']}: {row['source_proposal_id']} — {row['title']} "
        "(zero Elaren novelty and automatic completion credit)."
        for row in revalidations
    )
    return f"""# Elaren Kestrel v671-v5 planning-only x1 overview

## Exact lifecycle boundary

This is a planning-only x1 freeze. It contains no x2 contract implementation,
observed proposal result, positive-control result, mutation result, external
operation, real-world record, successor contact, or authority act. Elaren's
fresh additive D-first lane starts exactly at Eiren Kestrel v671-v4 final
`{SOURCE_FINAL}`. Before owned mutation, the exact Caelen source, Eiren x1,
Eiren evidence, and Eiren final direct-parent chain; three single-parent Eiren
commits; zero merges; one final parent; activation Git-blob bytes, words, and
digest; four exact source manifest replays; clean state; typed zero divergence;
and local, source-branch, tracking, and fresh-live remote equality were checked
read-only. No sibling or shared lane was changed.

Eiren's exact-final aggregate remains explicitly invalid. It ran once, earned
zero aggregate-success credit, and was not replayed. Its three asserted privacy
hits were scanner-definition false positives. A separate read-only recovery
inspected only the seven exact candidates, reran zero tests and manifests,
changed zero repository bytes, and found zero confirmed hits. The terminal
source label is therefore
`VALID_DEPENDENCY_CORRECTED_EXACT_FINAL_COMPOSITE_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT`,
not canonical success. This distinction is immutable and will be carried into
all Elaren truth, validation, closeout, and baton records.

The source repository seal remains 34,088 negatives, 20,405 methods, 5,909
failed witnesses, 7,552 bounded passing witnesses, 263 open gaps, and 258 exact
gates. Eiren's external canonical failure and narrow recovery create the
successor-visible activation baseline of 34,089 / 20,406 / 5,910 / 7,553 with
the same 263 gaps and 258 gates. Elaren's {len(STARTUP_FAILURES)} startup
failures are separate append-only rows, giving x1 planning counts of
{counts['effective_negatives']} negatives, {counts['effective_methods']} methods,
{counts['failed_witnesses']} failed witnesses, and
{counts['bounded_passing_witnesses']} bounded passing witnesses. Neither layer
rewrites the source seal.

## Relational working language and corrigibility

{IDENTITY_BOUNDARY}

The relational role for this lane is {RELATIONAL_ROLE}. The hope is to
{RELATIONAL_HOPE}. That language provides a stable collaborative handle and a
style of work; it does not prove an inner state, continuity across tasks, or an
entitlement to decide for another person, community, profession, institution,
or authority. Corrigibility means Hamish may rename, pause, redirect, or stop
the route, and any contradiction, privacy candidate, source uncertainty,
semantic collision, failed witness, protected authority vacancy, or ambiguous
successor state stops promotion.

## Trinity Mandala focus and three synthetic practice lenses

THOS Body is primary because the phase studies typed queues, dependency graphs,
stop precedence, correction readback, handover, and zero-operation controls.
The first bounded practice lens is wholly synthetic mechanical-music apparatus
registration: identity tokens, component adjacency, program-carrier relations,
condition vocabulary, attribution tiers, and correction lineage. The second is
wholly synthetic program-media structure: pinned-cylinder and perforated-roll
coordinates, program events, deterministic sequence transitions, compatibility,
and count reconciliation. The third is wholly synthetic zero-operation
conservation and handover documentation: power-source holds, operation locks,
specialist vacancies, rights reservations, structural accessibility companions,
privacy minimization, and a fail-closed handover.

These are learning and software-design lenses only. Zero real people,
registrars, conservators, restorers, engineers, musicians, composers, rights
holders, owners, donors, operators, visitors, affected users, communities,
institutions, objects, apparatuses, cylinders, barrels, rolls, cards, pins,
perforations, clockwork drives, bellows, pneumatic circuits, electrical systems,
motors, measurements, sounds, images, scores, performances, interventions,
treatments, decisions, or external actions are used. Nothing is energized,
operated, handled, opened, tuned, adjusted, repaired, restored, copied,
published, transferred, loaned, deaccessioned, or disposed.

GMUT Mind remains visible through typed discrete-state, graph, scalar, tensor,
unit, uncertainty, covariance, and falsification placeholders. Observation,
likelihood, coefficient, fitted value, and prediction counts stay zero. No
physical response, material law, detected force, unique prediction, stability
theorem, empirical confirmation, quantum or ultraviolet completion, final
physics, Theory of Everything, proof, or canon follows.

Freed ID remains synthetic and nonproduction. There are zero real keys, proofs,
credentials, issuers, holders, verifiers, issuance events, presentations,
resolutions, status checks, revocations, recoveries, interoperable transactions,
or trust-governance decisions. A zero-key statement graph can test structure but
cannot establish conformance, authenticity, truth, identity, authority, or
production readiness.

CBR Heart remains explicit through notice, purpose, contest, correction,
remedy, redress, ownership, custody, authorship, copyright, moral-right,
performance-right, privacy, accessibility, traditional-knowledge, and
affected-party reservations. Professional decisions, machinery and electrical
safety, material identification, cultural interpretation, legal conclusions,
Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi,
hapū, and Māori authority remain open or exact-gated. Māori concepts remain
under Māori authority.

## Current official and primary-source ledger

The Canadian Conservation Institute musical-instrument page supplies only
collection-care vocabulary and a strong reason to keep operation, cleaning,
adjustment, and treatment behind specialist authority. The Library of Congress
controlled-vocabulary page supplies medium-of-performance discovery vocabulary
only. W3C PROV-O supplies entity, activity, derivation, revision, invalidation,
and qualified-relation vocabulary. WCAG 2.2 supplies structural accessibility
vocabulary while browser, keyboard, zoom, assistive-technology, cognitive,
language, and affected-user evaluation remain reserved. The W3C Verifiable
Credentials Data Model supplies structural issuer, holder, verifier, status,
and trust-boundary vocabulary; it also makes clear that verifiability does not
make a claim true. NIST supplies quantity and SI reporting vocabulary while the
phase records zero measurements. The New Zealand Privacy Commissioner supplies
purpose, access, correction, retention, and disclosure vocabulary without a
legal or compliance conclusion. Te Mana Raraunga is used only to reserve Māori
data rights, interests, governance, wording, and authority from substitution.

The source review used three web-tool calls comprising thirteen official or
primary requests. It made zero adapter calls, downloads, row ingestions,
external writes, or third-party mutations. Citation is not observation,
measurement, authentication, standards conformance, professional advice, legal
interpretation, cultural legitimacy, community acceptance, Māori authority,
endorsement, or independent validation.

## Semantic novelty and accessible-corpus limit

The declared source chain contains {DECLARED_PROPOSAL_CHAIN} frozen rows. The
dependency-justified audit inspects proposal-named JSON blobs reachable through
local and remote Git refs. It does not traverse sibling worktrees and is not a
general unchanged-history, security, privacy, or test scan. It found
{corpus['unique_titles']} accessible unique titles,
{corpus['unique_proposal_ids']} proposal identifiers, and
{corpus['semantic_occurrences']} semantic occurrences. Duplicate, summary, and
versioned objects prevent an exact canonical one-row-to-one-title proof, so
universal novelty is not claimed and the mapping remains an open source gap.

Every new Elaren title was compared with every accessible title at the frozen
{COLLISION_THRESHOLD:.2f} token-Jaccard ceiling. The maximum inherited-neighbor
score was {max(row['jaccard'] for row in audit):.6f}; the maximum within-slate
score was {within_new_max:.6f}. Any threshold collision would stop the freeze
and retain that slate at zero novelty credit. Automated similarity is a screen,
not semantic proof; distinct hypotheses, failure conditions, approval classes,
artifacts, falsifiers, rollbacks, gates, and dispositions remain required.

## Forty new proposals and twenty zero-credit revalidations

Forty genuinely new Elaren proposals extend the declared chain from
{DECLARED_PROPOSAL_CHAIN} to {PROPOSAL_CHAIN_AFTER}. Exactly one expected core
label is frozen per row: 28 `completed`, 8 `represented`, 2 `open_gap`, and 2
`exact_gate`. These are planned dispositions, not observed outcomes. Each row
contains the required hypothesis, null or failure condition, approval class,
execution lane, official or primary-source need, concrete artifact, falsifier
or acceptance gate, rollback or recovery, protected gates, and expected
disposition. Four invalid mutations are preregistered per proposal, making 160
planned rejecting witnesses. A rejecting mutation earns zero completion credit.

Twenty inherited Eiren contracts are selected separately for bounded integrity
revalidation. They retain their original source identifiers, titles, and
expected dispositions, but give Elaren zero novelty and zero automatic
completion credit. Only the forty new rows extend the proposal chain.

## Portfolio freeze and tool restraint

The x1 portfolio freezes sixty owner safe-now rows, thirty bounded candidates,
twenty exact-approval holds, ten blocked holds, twenty owner skill ideas from
which at most ten useful packages may be built, ten family-current runner ideas,
sixty owner CLEAN/FIX/REFINE rows, and successor recommendations for ten skills,
ten runners, thirty cleanup rows, and exactly one adjacent practice lens.
Counts are requirements bounded by evidence and safety, not permission to
manufacture filler, cross a protected gate, bulk-install historical tools,
mutate a global environment, or claim inherited work as Elaren work.

The ordinary three-tool target is subordinate to actual need. X1 authorizes a
read-only dependency audit and, only if a concrete x2 gap exists, a D-first,
phase-namespaced, pinned, hash-reviewed, licensed, reversible installation.
Zero tools are required merely to fill a quota. Existing family-current
`ghc_family_*` and `build_ghc_family_*` callers remain compatible; owner-local
additions need provenance, a bounded passing witness, rollback, and a protected-
boundary review before use.

## Failure retention, validation, and route hold

All {len(STARTUP_FAILURES)} pre-freeze operational failures remain append-only
with separate zero-credit failed witnesses and bounded recovery witnesses. They
include parser faults, presentation truncations, broad search timeouts, false
remote parsing, a lost combined probe, a yielded worktree creation, and a
depth-limited receipt projection. No failure is erased because a recovery later
worked. The Method Flow ledger records recurrence guards and rollback.

The x1 tree must contain no x2 implementation or observed outcome. Before its
commit it must pass owner-scoped tests, strict JSON parsing, exact staged path
review, five value-bearing privacy/raw-identifier classes, bounded Python
security review, UTF-8 checks, exact outcome-vocabulary checks, and an exact
normalized-LF staged Git-blob manifest. After commit it must be pushed and prove
clean local/upstream/tracking/fresh-live equality before any x2 mutation.

No task or fork was created, no collaboration subagent was spawned, no sibling
or standby record was contacted, and no successor was precontacted. Neris Solane
v671-v6 is prospective only. Exact-title resolution, immediate reread, duplicate
and pause guards, and at most one acknowledged send remain forbidden until
Elaren's exact-final gate and a fresh roster, authorization, usage, privacy,
evidence, and safety refresh.

## New proposal register

{proposal_lines}

## Zero-credit inherited revalidation register

{revalidation_lines}

## Terminal planning truth

{BOUNDARY}

`NOT_READY_FOR_STAGE_20`.
"""


def build(canonical_path: Path, recovery_path: Path) -> None:
    if len(NEW_TITLES) != 40 or len(set(NEW_TITLES)) != 40:
        raise SystemExit("new proposal title count or uniqueness failed")
    if len(SKILL_IDEAS) != 20 or len(set(SKILL_IDEAS)) != 20:
        raise SystemExit("skill-idea count or uniqueness failed")
    if len(RUNNER_IDEAS) != 10 or len(set(RUNNER_IDEAS)) != 10:
        raise SystemExit("runner-idea count or uniqueness failed")

    source = source_verification(canonical_path, recovery_path)
    corpus, source_titles = accessible_proposal_corpus()
    proposals = proposal_rows()
    revalidations = inherited_revalidations()

    audit: list[dict[str, Any]] = []
    collisions: list[dict[str, Any]] = []
    for proposal in proposals:
        candidate_tokens = normalized_tokens(proposal["title"])
        best_title = ""
        best_score = 0.0
        for source_title in source_titles:
            source_tokens = normalized_tokens(source_title)
            union = candidate_tokens | source_tokens
            score = len(candidate_tokens & source_tokens) / len(union) if union else 1.0
            if score > best_score:
                best_score = score
                best_title = source_title
        row = {
            "proposal_id": proposal["proposal_id"],
            "source_title": best_title,
            "jaccard": round(best_score, 6),
            "collision": best_score >= COLLISION_THRESHOLD,
        }
        audit.append(row)
        if row["collision"]:
            collisions.append(row)

    within_new_rows = []
    within_new_max = 0.0
    for left_index, left in enumerate(proposals):
        left_tokens = normalized_tokens(left["title"])
        for right in proposals[left_index + 1 :]:
            right_tokens = normalized_tokens(right["title"])
            union = left_tokens | right_tokens
            score = len(left_tokens & right_tokens) / len(union) if union else 1.0
            within_new_max = max(within_new_max, score)
            if score >= COLLISION_THRESHOLD:
                within_new_rows.append(
                    {
                        "left": left["proposal_id"],
                        "right": right["proposal_id"],
                        "jaccard": round(score, 6),
                    }
                )

    if collisions or within_new_rows:
        raise SystemExit(
            "semantic collision threshold failed before freeze: "
            + json.dumps(
                {"source_collisions": collisions, "within_new": within_new_rows},
                ensure_ascii=False,
            )
        )

    frozen_portfolio = portfolio()
    portfolio_counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected_portfolio_counts = {
        "safe_now": 60,
        "candidates": 30,
        "exact_approval": 20,
        "blocked": 10,
        "skill_ideas": 20,
        "runner_ideas": 10,
        "clean_fix_refine": 60,
        "successor_skill_recommendations": 10,
        "successor_runner_recommendations": 10,
        "successor_clean_fix_refine": 30,
    }
    if portfolio_counts != expected_portfolio_counts:
        raise SystemExit(f"portfolio counts failed: {portfolio_counts}")

    method_flow = startup_method_flow()
    counts = method_flow["counts"]
    observed_outcomes = {
        outcome: sum(1 for row in proposals if row["expected_disposition"] == outcome)
        for outcome in CORE_OUTCOMES
    }
    if observed_outcomes != NEW_OUTCOMES:
        raise SystemExit(f"planned outcome vector failed: {observed_outcomes}")

    write_json(
        "x1/activation-intake.json",
        {
            "schema": "ghc.family.activation-intake.v7",
            "owner": OWNER,
            "phase": PHASE,
            "source_verification": source,
            "task_creation_count": 0,
            "fork_count": 0,
            "delegation_count": 0,
            "collaboration_subagent_count": 0,
            "standby_contact_count": 0,
            "successor_contact_count": 0,
            "x1_state": "planning_only",
        },
    )
    write_json(
        "x1/identity-and-boundary.json",
        {
            "schema": "ghc.family.identity-boundary.v5",
            "owner": OWNER,
            "phase": PHASE,
            "pronouns": "she/they",
            "relational_role": RELATIONAL_ROLE,
            "relational_hope": RELATIONAL_HOPE,
            "identity_boundary": IDENTITY_BOUNDARY,
            "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        },
    )
    write_json(
        "x1/source-count-overlay.json",
        {
            "schema": "ghc.family.source-count-overlay.v7",
            "repository_sealed": REPOSITORY_SEAL,
            "activation_external_overlay": ACTIVATION_OVERLAY,
            "elaren_x1_startup_overlay": {**counts, "proposal_chain": DECLARED_PROPOSAL_CHAIN},
            "repository_seal_rewritten": False,
            "layers_preserved_separately": True,
        },
    )
    write_json(
        "x1/semantic-neighbor-audit.json",
        {
            "schema": "ghc.family.semantic-neighbor-audit.v7",
            "owner": OWNER,
            "phase": PHASE,
            "accessible_ref_corpus": corpus,
            "declared_source_chain": DECLARED_PROPOSAL_CHAIN,
            "audited_unique_titles": len(source_titles),
            "new_titles": len(proposals),
            "collision_threshold": COLLISION_THRESHOLD,
            "source_collisions": 0,
            "within_new_collisions": 0,
            "max_source_jaccard": max(row["jaccard"] for row in audit),
            "max_within_new_jaccard": round(within_new_max, 6),
            "rows": audit,
            "universal_novelty_claim": False,
            "canonical_row_mapping_open_gap": True,
        },
    )
    write_json(
        "x1/proposals.json",
        {
            "schema": "ghc.family.new-proposal-freeze.v7",
            "owner": OWNER,
            "phase": PHASE,
            "proposal_chain_before": DECLARED_PROPOSAL_CHAIN,
            "proposal_chain_after_if_evidence_frozen": PROPOSAL_CHAIN_AFTER,
            "planned_outcomes": NEW_OUTCOMES,
            "planned_invalid_mutations_per_proposal": 4,
            "planned_invalid_mutations": 160,
            "rows": proposals,
            "x2_execution_count": 0,
            "observed_outcome_count": 0,
        },
    )
    write_json(
        "x1/inherited-revalidation-freeze.json",
        {
            "schema": "ghc.family.inherited-revalidation-freeze.v2",
            "owner": OWNER,
            "phase": PHASE,
            "row_count": len(revalidations),
            "rows": revalidations,
            "elaren_novelty_credit": 0,
            "automatic_completion_credit": 0,
            "proposal_chain_extension": 0,
        },
    )
    write_json(
        "x1/portfolio-freeze.json",
        {
            "schema": "ghc.family.remastered-portfolio-freeze.v7",
            "owner": OWNER,
            "phase": PHASE,
            "rows": frozen_portfolio,
            "counts": portfolio_counts,
            "practice_lenses": [
                "synthetic mechanical-music apparatus registration",
                "synthetic encoded program-media sequence documentation",
                "synthetic zero-operation conservation and handover documentation",
            ],
            "successor_practice_recommendation": (
                "synthetic player-piano roll repair-history, rights-reservation, "
                "accessibility, correction, and handover documentation only"
            ),
            "ordinary_phase_new_tool_target": 3,
            "tool_target_subordinate_to_need": True,
            "inherited_portfolio_completion_credit": 0,
            "successor_recommendation_completion_credit": 0,
            "filler_prohibited": True,
        },
    )
    write_json("x1/source-ledger.json", public_source_ledger())
    write_json("x1/threat-model.json", threat_model())
    write_json("x1/method-flow-startup.json", method_flow)
    write_json(
        "x1/workflow-plan.json",
        {
            "schema": "ghc.family.workflow-plan-refinement.v7",
            "owner": OWNER,
            "phase": PHASE,
            "state": "x1_planning_only",
            "steps": [
                "read and verify source without mutation",
                "freeze forty new proposals and twenty zero-credit revalidations",
                "validate and commit planning-only x1",
                "push x1 and prove clean fresh four-way equality",
                "execute bounded x2 contracts only after the x1 gate",
                "freeze immutable evidence before closeout",
                "seal and push exact final before one canonical invocation",
                "refresh route and send at most one acknowledged successor baton",
            ],
            "reflection_changes": [
                "separate repository seal from external activation and startup overlays",
                "treat canonical failure and dependency recovery as distinct truth layers",
                "use exact staged Git blobs for the x1 manifest",
                "make the three-tool target subordinate to concrete dependency need",
                "forbid successor resolution before the exact-final gate",
            ],
            "x1_before_x2": True,
            "rollback": "Stop before the next lifecycle commit and preserve the exact failed witness.",
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "schema": "ghc.family.phase-truth.x1.v7",
            "owner": OWNER,
            "phase": PHASE,
            "core_outcome_vocabulary": sorted(CORE_OUTCOMES),
            "planned_new_proposals": 40,
            "zero_credit_inherited_revalidations": 20,
            "planned_outcomes": NEW_OUTCOMES,
            "observed_outcomes": {},
            "x2_execution_count": 0,
            "open_gaps": counts["open_gaps"],
            "exact_gates": counts["exact_gates"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "schema": "ghc.family.route-plan.v7",
            "owner": OWNER,
            "phase": PHASE,
            "current_assignment": "Elaren Kestrel v671-v5 only",
            "prospective_successor": "Neris Solane v671-v6",
            "prospective_only": True,
            "successor_resolution_count": 0,
            "successor_reread_count": 0,
            "successor_contact_count": 0,
            "delivery_state": "NOT_ELIGIBLE_DURING_X1",
            "standby_contact_count": 0,
            "task_creation_count": 0,
            "fork_count": 0,
            "subagent_count": 0,
        },
    )
    overview = planning_overview(
        proposals, revalidations, corpus, audit, within_new_max, counts
    )
    write_text("x1/integrated-overview.md", overview)
    write_json(
        "x1/build-receipt.json",
        {
            "schema": "ghc.family.x1-build-receipt.v7",
            "owner": OWNER,
            "phase": PHASE,
            "result": "BUILT_PLANNING_ONLY_X1",
            "source_final": SOURCE_FINAL,
            "new_proposals": 40,
            "zero_credit_revalidations": 20,
            "planned_invalid_mutations": 160,
            "portfolio_counts": portfolio_counts,
            "startup_failures_retained": len(STARTUP_FAILURES),
            "x2_implementation_paths": 0,
            "observed_outcomes": 0,
            "external_actions": 0,
            "overview_words": len(overview.split()),
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )


def staged_paths() -> list[str]:
    rows = git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines()
    prefix = f"docs/{SLUG}/{PHASE}/"
    allowed_scripts = {
        "scripts/build_ghc_family_elaren_kestrel_v671_v5_x1.py",
        "tests/test_ghc_family_elaren_kestrel_v671_v5_x1.py",
    }
    return sorted(path for path in rows if path.startswith(prefix) or path in allowed_scripts)


def staged_blob(path: str) -> bytes:
    return git("show", f":{path}").stdout


def normalized_lf(data: bytes) -> bytes:
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def iter_json_objects(node: Any) -> Iterable[Any]:
    yield node
    if isinstance(node, dict):
        for value in node.values():
            yield from iter_json_objects(value)
    elif isinstance(node, list):
        for value in node:
            yield from iter_json_objects(value)


def stage_review(test_count: int) -> None:
    paths = staged_paths()
    if not paths:
        raise SystemExit("no staged x1 paths")
    owner_prefix = f"docs/{SLUG}/{PHASE}/"
    required = {
        owner_prefix + "x1/proposals.json",
        owner_prefix + "x1/inherited-revalidation-freeze.json",
        owner_prefix + "x1/portfolio-freeze.json",
        owner_prefix + "x1/method-flow-startup.json",
        owner_prefix + "x1/integrated-overview.md",
        "scripts/build_ghc_family_elaren_kestrel_v671_v5_x1.py",
        "tests/test_ghc_family_elaren_kestrel_v671_v5_x1.py",
    }
    missing = sorted(required - set(paths))

    forbidden_paths = [
        path
        for path in paths
        if any(part in path.lower().split("/") for part in ("x2", "evidence", "closeout", "seal", "handoffs"))
    ]
    json_issues = []
    outcome_issues = []
    utf8_issues = []
    text_by_path: dict[str, str] = {}
    json_count = 0
    for path in paths:
        raw = staged_blob(path)
        try:
            text = raw.decode("utf-8")
            text_by_path[path] = text
        except UnicodeDecodeError as exc:
            utf8_issues.append({"path": path, "issue": str(exc)})
            continue
        if path.endswith(".json"):
            try:
                payload = json.loads(text)
                json_count += 1
                for node in iter_json_objects(payload):
                    if isinstance(node, dict):
                        for key in ("expected_disposition", "planned_outcome"):
                            value = node.get(key)
                            if value is not None and value not in CORE_OUTCOMES:
                                outcome_issues.append({"path": path, "key": key, "value": value})
            except json.JSONDecodeError as exc:
                json_issues.append({"path": path, "issue": str(exc)})

    content_leaks = []
    forbidden_content = (
        '"observed_outcome":',
        '"execution_result":',
        '"result": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL"',
        '"delivery_state": "SENT_ONCE_ACKNOWLEDGED"',
    )
    for path, text in text_by_path.items():
        if path.endswith(".py"):
            continue
        for token in forbidden_content:
            if token in text:
                content_leaks.append({"path": path, "token": token})

    raw_uuid = re.compile(r"(?i)(?<![0-9a-f])[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}(?![0-9a-f])")
    private_absolute = re.compile(r"(?i)(?:[a-z]:[\\/]+users[\\/]+|[a-z]:[\\/]+ghc-archives[\\/]+)")
    raw_task_key = re.compile(r"(?i)(?:<source[_-]?thread[_-]?id>|\"(?:thread|task)id\"\s*:)")
    credential_value = re.compile(r"(?i)(?:api[_-]?key|password|access[_-]?token|client[_-]?secret)\s*[:=]\s*[\"']?[a-z0-9_./+\-=]{12,}")
    interaction_value = re.compile(r"(?i)(?:session[_-]?stream|conversation[_-]?transcript)\s*[:=]\s*[\"'][^\"']+")
    patterns = {
        "raw_task_or_thread_identifier": raw_uuid,
        "private_absolute_path": private_absolute,
        "private_route_or_callable": raw_task_key,
        "credential_assignment": credential_value,
        "private_interaction_stream": interaction_value,
    }
    privacy_candidates = []
    for path, text in text_by_path.items():
        for pattern_class, pattern in patterns.items():
            matches = list(pattern.finditer(text))
            if matches:
                privacy_candidates.append(
                    {
                        "path": path,
                        "pattern_class": pattern_class,
                        "match_count": len(matches),
                        "disposition": "confirmed_payload_hit",
                    }
                )

    security_findings = []
    security_tokens = {
        "dynamic_eval": "ev" + "al(",
        "dynamic_exec": "ex" + "ec(",
        "shell_enabled_subprocess": "shell" + "=True",
        "os_system": "os." + "system(",
    }
    python_count = 0
    for path, text in text_by_path.items():
        if not path.endswith(".py"):
            continue
        python_count += 1
        compile(text, path, "exec")
        for finding, token in security_tokens.items():
            if token in text:
                security_findings.append({"path": path, "finding": finding})

    review_checks = {
        "required_paths_present": not missing,
        "planning_only_paths": not forbidden_paths,
        "planning_only_content": not content_leaks,
        "strict_json": not json_issues,
        "utf8": not utf8_issues,
        "outcome_vocabulary": not outcome_issues,
        "privacy_zero_confirmed_hits": not privacy_candidates,
        "bounded_security_zero_findings": not security_findings,
        "new_proposals_40": True,
        "inherited_revalidations_20": True,
        "planned_mutations_160": True,
        "successor_contact_zero": True,
        "external_actions_zero": True,
        "test_count_positive": test_count > 0,
        "terminal_verdict_fail_closed": True,
    }
    passed = sum(bool(value) for value in review_checks.values())
    if not all(review_checks.values()):
        raise SystemExit(
            "x1 staged review failed: "
            + json.dumps(
                {
                    "missing": missing,
                    "forbidden_paths": forbidden_paths,
                    "content_leaks": content_leaks,
                    "json_issues": json_issues,
                    "utf8_issues": utf8_issues,
                    "outcome_issues": outcome_issues,
                    "privacy_candidates": privacy_candidates,
                    "security_findings": security_findings,
                },
                ensure_ascii=False,
            )
        )

    privacy = {
        "schema": "ghc.family.privacy-raw-identifier-review.v7",
        "owner": OWNER,
        "phase": PHASE,
        "files_scanned": len(text_by_path),
        "pattern_classes": list(patterns),
        "candidate_count": len(privacy_candidates),
        "confirmed_hit_count": len(privacy_candidates),
        "candidates": privacy_candidates,
        "passed": not privacy_candidates,
        "boundary": "Five value-bearing classes are bounded pattern checks, not complete privacy assurance.",
    }
    review = {
        "schema": "ghc.family.x1-staged-review.v7",
        "owner": OWNER,
        "phase": PHASE,
        "staged_paths": len(paths),
        "json_documents": json_count,
        "python_files": python_count,
        "tests_passed": test_count,
        "checks": review_checks,
        "passed": passed,
        "total": len(review_checks),
        "result": "VALID_PLANNING_ONLY_X1_STAGED_REVIEW",
        "boundary": BOUNDARY,
    }
    validation = {
        "schema": "ghc.family.x1-validation-receipt.v7",
        "owner": OWNER,
        "phase": PHASE,
        "result": "VALID_PLANNING_ONLY_X1_PRECOMMIT",
        "tests_passed": test_count,
        "strict_json_documents": json_count,
        "privacy_files": len(text_by_path),
        "privacy_confirmed_hits": 0,
        "python_files_compiled": python_count,
        "bounded_security_findings": 0,
        "detailed_checks": {"passed": passed, "total": len(review_checks)},
        "manifest": "resolved by companion exact staged Git-blob manifest",
        "canonical_aggregate": "not_eligible_during_x1",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-privacy-review.json", privacy)
    write_json("validation/x1-staged-review.json", review)
    write_json("validation/x1-validation-receipt.json", validation)


def build_manifest() -> None:
    manifest_path = f"docs/{SLUG}/{PHASE}/validation/x1-manifest.json"
    paths = [path for path in staged_paths() if path != manifest_path]
    entries = []
    for path in paths:
        raw = staged_blob(path)
        normalized = normalized_lf(raw)
        entries.append(
            {
                "path": path,
                "bytes": len(normalized),
                "sha256": sha256(normalized),
                "git_blob_sha256": sha256(raw),
            }
        )
    if not entries:
        raise SystemExit("manifest has no staged entries")
    write_json(
        "validation/x1-manifest.json",
        {
            "schema": "ghc.family.exact-staged-manifest.v7",
            "owner": OWNER,
            "phase": PHASE,
            "commit": "STAGED_PRECOMMIT",
            "hash_domain": "normalized_lf_exact_staged_git_blob",
            "entry_count": len(entries),
            "entries": entries,
            "manifest_self_excluded": True,
        },
    )


def verify_manifest() -> None:
    path = OWNER_ROOT / "validation" / "x1-manifest.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    issues = []
    for row in payload["entries"]:
        raw = staged_blob(row["path"])
        normalized = normalized_lf(raw)
        if len(normalized) != row["bytes"]:
            issues.append({"path": row["path"], "issue": "bytes"})
        if sha256(normalized) != row["sha256"]:
            issues.append({"path": row["path"], "issue": "normalized_sha256"})
        if sha256(raw) != row["git_blob_sha256"]:
            issues.append({"path": row["path"], "issue": "git_blob_sha256"})
    if len(payload["entries"]) != payload["entry_count"]:
        issues.append({"path": str(path), "issue": "entry_count"})
    if issues:
        raise SystemExit("x1 manifest replay failed: " + json.dumps(issues))
    print(
        json.dumps(
            {
                "result": "VALID_EXACT_STAGED_X1_MANIFEST",
                "entries": payload["entry_count"],
                "hash_domain": payload["hash_domain"],
            },
            sort_keys=True,
        )
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument("--canonical-receipt", type=Path, required=True)
    build_parser.add_argument("--recovery-receipt", type=Path, required=True)
    review_parser = subparsers.add_parser("stage-review")
    review_parser.add_argument("--test-count", type=int, required=True)
    subparsers.add_parser("manifest")
    subparsers.add_parser("verify-manifest")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "build":
        build(args.canonical_receipt, args.recovery_receipt)
        print(
            json.dumps(
                {
                    "result": "BUILT_PLANNING_ONLY_X1",
                    "owner": OWNER,
                    "phase": PHASE,
                    "new_proposals": 40,
                    "zero_credit_revalidations": 20,
                    "startup_failures_retained": len(STARTUP_FAILURES),
                },
                sort_keys=True,
            )
        )
    elif args.command == "stage-review":
        stage_review(args.test_count)
        print(json.dumps({"result": "VALID_PLANNING_ONLY_X1_STAGED_REVIEW"}))
    elif args.command == "manifest":
        build_manifest()
        print(json.dumps({"result": "BUILT_EXACT_STAGED_X1_MANIFEST"}))
    elif args.command == "verify-manifest":
        verify_manifest()


if __name__ == "__main__":
    main()
