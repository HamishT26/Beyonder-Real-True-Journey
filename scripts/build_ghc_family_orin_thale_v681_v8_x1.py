#!/usr/bin/env python3
"""Build Orin Thale v681-v8 planning-only x1 artifacts.

This builder creates only preregistration, portfolio, source, gate, privacy,
and lifecycle records.  It deliberately creates no x2 implementation or
observed proposal outcome.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "orin-thale" / "v681-v8"
X1 = PHASE / "x1"
VALIDATION = PHASE / "validation"
SOURCE = "7327e6cb3972e93a4d6a27e45ad2ba3445a4d6ce"
SOURCE_BRANCH = "codex/GHC-Family/caelen-ash-v681-v7-full-tools"
BRANCH = "codex/GHC-Family/orin-thale-v681-v8-full-tools"
DECLARED_CHAIN_BEFORE = 10130
DECLARED_CHAIN_AFTER = 10190
QUARANTINE_THRESHOLD = 0.78
BASELINE = {
    "effective_negatives": 54848,
    "effective_methods": 63660,
    "failed_witnesses": 26509,
    "bounded_passing_witnesses": 45182,
    "open_gaps": 485,
    "exact_gates": 476,
}


def run(args: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args,
        cwd=ROOT,
        input=input_bytes,
        capture_output=True,
        check=False,
    )


def git(*args: str) -> str:
    result = run(["git", *args])
    if result.returncode:
        raise RuntimeError(result.stderr.decode("utf-8", errors="replace"))
    return result.stdout.decode("utf-8").strip()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def normalized_title(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def title_tokens(value: str) -> set[str]:
    return set(normalized_title(value).split())


def jaccard(left: str, right: str) -> float:
    a, b = title_tokens(left), title_tokens(right)
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def walk_dicts(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_dicts(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_dicts(child)


def proposal_blob_records() -> tuple[list[dict[str, str]], dict[str, Any]]:
    tree = run(["git", "ls-tree", "-r", "-z", SOURCE])
    if tree.returncode:
        raise RuntimeError(tree.stderr.decode("utf-8", errors="replace"))
    selected: list[tuple[str, str]] = []
    for raw in tree.stdout.split(b"\0"):
        if not raw:
            continue
        head, raw_path = raw.split(b"\t", 1)
        parts = head.decode("ascii").split()
        path = raw_path.decode("utf-8")
        if path.endswith(".json") and "proposal" in path.lower():
            selected.append((parts[2], path))

    request = b"".join((oid + "\n").encode("ascii") for oid, _ in selected)
    batch = run(["git", "cat-file", "--batch"], input_bytes=request)
    if batch.returncode:
        raise RuntimeError(batch.stderr.decode("utf-8", errors="replace"))
    cursor = 0
    parsed_paths = 0
    failures: list[dict[str, str]] = []
    records: list[dict[str, str]] = []
    for (_, path) in selected:
        line_end = batch.stdout.index(b"\n", cursor)
        header = batch.stdout[cursor:line_end].decode("ascii")
        cursor = line_end + 1
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            failures.append({"path": path, "reason": "non_blob_or_missing"})
            continue
        size = int(parts[2])
        payload = batch.stdout[cursor : cursor + size]
        cursor += size + 1
        try:
            document = json.loads(payload.decode("utf-8"))
            parsed_paths += 1
        except Exception as exc:
            failures.append({"path": path, "reason": type(exc).__name__})
            continue
        for item in walk_dicts(document):
            title = item.get("title")
            proposal_id = item.get("proposal_id") or item.get("id")
            if isinstance(title, str) and isinstance(proposal_id, str):
                records.append(
                    {
                        "proposal_id": proposal_id,
                        "title": title,
                        "path": path,
                    }
                )
    deduped: dict[tuple[str, str], dict[str, str]] = {}
    for item in records:
        deduped[(item["proposal_id"], normalized_title(item["title"]))] = item
    return list(deduped.values()), {
        "proposal_json_paths_discovered": len(selected),
        "proposal_json_paths_parsed": parsed_paths,
        "proposal_json_parse_failures": failures,
        "reachable_id_title_records": len(deduped),
        "universal_10130_row_materialization_claimed": False,
    }


PROPOSAL_TITLES = [
    "Synthetic nautical chart product identity and correction-state separation",
    "Official chart authority label and local working-copy non-equivalence",
    "National chart number INT number and catalogue identifier role split",
    "Paper chart sheet and electronic navigational chart cell firewall",
    "New edition reprint and cumulative correction version distinction",
    "Notice-to-mariners publication edition and individual notice tuple uniqueness",
    "Notice supersession cancellation and reference-chain cycle guard",
    "Permanent temporary and preliminary notice classification state machine",
    "Correction-applied state and navigation-readiness nonpromotion",
    "Source publication time and local correction-application time separation",
    "Chart scale compilation scale and display scale nonconflation",
    "Horizontal datum label with coordinate-transform execution refused",
    "Vertical datum chart datum and tidal reference separation",
    "Latitude longitude notation and hemisphere consistency contract",
    "Unqualified coordinate pair quarantine with exact location withheld",
    "Charted-feature change and source hazard report non-equivalence",
    "Insert delete amend and substitute correction-action taxonomy",
    "Block correction patch asset digest and provenance firewall",
    "Textual correction instruction and graphical annotation purpose split",
    "Affected chart cell and geographic applicability declaration hold",
    "Missing sequential correction detection without inferred content",
    "Cumulative correction ledger monotonicity and omission marker",
    "Duplicate correction idempotency key and content-digest decision",
    "Out-of-order notice quarantine with bounded later reconciliation",
    "Correction readback using before-and-after normalized digests",
    "Superseded working-copy retention without operative-use claim",
    "Failed correction rollback preserving rejected witness and prior state",
    "Reviewer acknowledgement and hydrographic-authority acceptance separation",
    "Shift handover receipt with unresolved chart-correction exceptions",
    "Correction workload pause resume stop and ownership-transfer contract",
    "Bounded retry fixture with no notice download or external request",
    "Archive retention horizon with no deletion or legal-hold decision",
    "Source URL media type and digest metadata without payload ingestion",
    "Chart-image text-alternative placeholder with manual review vacancy",
    "Plain-language correction summary that cannot substitute for a chart",
    "Minimum-disclosure reviewer alias with real identity linkage refused",
    "Sensitive location token with exact coordinate materialization prohibited",
    "Chart licence copyright and redistribution authority vacancy",
    "Chart preview and authoritative corrected chart non-equivalence",
    "Hydrographic note report and verified danger-to-navigation non-equivalence",
    "Navigational warning and chart-correction notice nonconflation",
    "Canonical JSON receipt for a zero-row correction structure",
    "Represented GMUT datum-frame obligation board without physical inference",
    "Represented GMUT correction-uncertainty analogy without likelihood or posterior",
    "Represented GMUT chart-amendment discrepancy ledger with no dynamical observable or predictive claim",
    "Represented THOS chart-correction workflow proxy with reversible holds",
    "Represented THOS conflict queue workload stop and handover state machine",
    "Represented Freed ID pseudonymous reviewer capability without identity event",
    "Represented Freed ID correction-attestation envelope without keys or proofs",
    "Represented CBR chart-correction challenge queue with remedy authority vacant",
    "Represented CBR accessible-notice obligation with affected-user review vacant",
    "Represented IHO S-4 vocabulary crosswalk without chart conformance",
    "Represented IHO S-101 vocabulary crosswalk without ENC production",
    "Represented PROV-O lineage pattern for synthetic chart patches with conformance unassessed",
    "Open gap for real hydrographers chart compilers mariners and bridge operators",
    "Open gap for real chart editions ENC cells corrections navigation results and independent reproduction",
    "Open gap for disabled users affected communities and Māori cultural-data review",
    "Exact gate for navigation safety chart correction release and hydrographic authority",
    "Exact gate for chart rights heritage taonga Māori data governance and Māori authority",
    "Absolute refusal to elevate zero-row nautical-chart workflow artifacts into Stage 20 or any empirical deployment identity AGI ASI consciousness personhood theorem canon or final-physics claim",
]


def disposition(index: int) -> str:
    if index <= 42:
        return "completed"
    if index <= 54:
        return "represented"
    if index <= 57:
        return "open_gap"
    return "exact_gate"


def approval_class(index: int) -> str:
    if index <= 42:
        return "safe_now"
    if index <= 54:
        return "candidate_proxy_only"
    if index <= 57:
        return "external_evidence_open_gap"
    return "exact_approval"


def execution_lane(index: int) -> str:
    if index <= 42:
        return "owner_local_synthetic_zero_row"
    if index <= 54:
        return "bounded_representation_without_real_execution"
    if index <= 57:
        return "unexecuted_empirical_vacancy"
    return "unexecuted_competent_authority_gate"


def source_needs(index: int) -> list[str]:
    if index <= 20:
        return ["IHO-S4-4.10.0", "LINZ-NTM-GUIDANCE"]
    if index <= 36:
        return ["IHO-S4-4.10.0", "W3C-PROV-O", "RFC8785"]
    if index <= 42:
        return ["LINZ-NTM-GUIDANCE", "W3C-WCAG22", "RFC8785"]
    if index <= 57:
        return ["IHO-S4-4.10.0", "IHO-S101-2.0.0", "LINZ-NTM-GUIDANCE"]
    if index == 59:
        return ["TMR-MDS-PRINCIPLES", "LINZ-NTM-GUIDANCE"]
    return ["LINZ-NTM-GUIDANCE", "LINZ-CHART-DISCLAIMER"]


def proposals() -> list[dict[str, Any]]:
    rows = []
    mutation_types = [
        "missing_required_field",
        "identifier_role_swap",
        "stale_precondition_digest",
        "correction_order_inversion",
        "authority_promotion",
    ]
    for index, title in enumerate(PROPOSAL_TITLES, start=1):
        proposal_id = f"OR6818-N{index:03d}"
        expected = disposition(index)
        rows.append(
            {
                "proposal_id": proposal_id,
                "title": title,
                "hypothesis": (
                    f"A bounded synthetic validator for {title.lower()} can reject its five "
                    "preregistered counterexamples while preserving every empirical and authority boundary."
                ),
                "null_or_failure_condition": (
                    f"The {proposal_id} contract is falsified if any preregistered invalid fixture is "
                    "accepted, its bounded positive structure is rejected, or a protected gate is promoted."
                ),
                "approval_class": approval_class(index),
                "execution_lane": execution_lane(index),
                "official_or_primary_source_needs": source_needs(index),
                "concrete_artifacts": [
                    f"docs/orin-thale/v681-v8/x2/proposal-evidence.json#{proposal_id}",
                    f"docs/orin-thale/v681-v8/x2/mutations.json#{proposal_id}",
                ],
                "falsifier_or_acceptance_gate": (
                    f"Accept only if {proposal_id} has one bounded positive witness, all five invalid "
                    "mutations are rejected, and no wider claim or authority is inferred."
                ),
                "rollback_or_recovery": (
                    f"Quarantine only the {proposal_id} witness, retain the failed receipt at zero credit, "
                    "and regenerate from this immutable x1 contract."
                ),
                "protected_gates": [
                    "real participants and operators",
                    "empirical measurements and likelihoods",
                    "production chart correction or navigation use",
                    "professional hydrographic and navigation-safety authority",
                    "legal cultural affected-party and Māori authority",
                    "privacy-complete accessibility-complete and exhaustive-security claims",
                    "independent reproduction proof canon and Stage 20",
                ],
                "expected_disposition": expected,
                "preregistered_rejecting_mutations": [
                    {
                        "mutation_id": f"{proposal_id}-M{offset:02d}",
                        "mutation_type": mutation_type,
                        "expected_result": "rejected_zero_credit",
                    }
                    for offset, mutation_type in enumerate(mutation_types, start=1)
                ],
            }
        )
    return rows


OFFICIAL_SOURCES = [
    {
        "source_id": "IHO-S4-4.10.0",
        "title": "IHO S-4 Regulations for International Charts and Chart Specifications",
        "url": "https://iho.int/en/standards-and-specifications",
        "status": "official_IHO_Edition_4.10.0_March_2026_checked_2026-09-01",
        "use": "chart specification, edition, correction, and portrayal vocabulary only; no chart production or conformance claim",
    },
    {
        "source_id": "IHO-S101-2.0.0",
        "title": "IHO S-101 Electronic Navigational Chart Product Specification",
        "url": "https://registry.iho.int/productspec/view.do?category=product_ID&domainS=ALL&idx=214&product_ID=S-101&statusS=5",
        "status": "official_IHO_Edition_2.0.0_in_force_2026-01-01_checked_2026-09-01",
        "use": "ENC product, feature, catalogue, and update vocabulary only; no ENC generation, validation, or navigation use",
    },
    {
        "source_id": "IHO-S100-REGISTRY",
        "title": "IHO S-100 Geospatial Information Registry",
        "url": "https://registry.iho.int/document/list.do",
        "status": "official_registry_showing_S100_5.2.1_and_S101_2.0.0_checked_2026-09-01",
        "use": "published product-version vocabulary only; no data download, registry conformance, or operational claim",
    },
    {
        "source_id": "LINZ-NTM-GUIDANCE",
        "title": "Toitū Te Whenua About Notices to Mariners",
        "url": "https://www.linz.govt.nz/guidance/marine-information/charts/about-notices-mariners",
        "status": "official_LINZ_guidance_checked_2026-09-01",
        "use": "annual, fortnightly, correction, publication, withdrawal, and authority-boundary vocabulary only; no notice application or navigational decision",
    },
    {
        "source_id": "LINZ-NTM-INDEX",
        "title": "Toitū Te Whenua Notices to Mariners index",
        "url": "https://www.linz.govt.nz/products-services/maritime-safety/notices-mariners",
        "status": "official_LINZ_current_and_previous_editions_surface_checked_2026-09-01",
        "use": "edition, cumulative-list, temporary, preliminary, chart-catalogue, and update-frequency vocabulary only; no notice or chart downloaded",
    },
    {
        "source_id": "LINZ-CHART-DISCLAIMER",
        "title": "Toitū Te Whenua where to find charts",
        "url": "https://www.linz.govt.nz/products-services/charts/where-find-charts",
        "status": "official_LINZ_page_checked_2026-09-01",
        "use": "official-chart, preview, update, and non-navigation substitute refusal vocabulary only",
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "W3C PROV-O",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "W3C_Recommendation_stable_checked_2026-09-01",
        "use": "entity, activity, derivation, revision, attribution, and provenance vocabulary only; no conformance",
    },
    {
        "source_id": "W3C-WCAG22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "W3C_Recommendation_checked_2026-09-01",
        "use": "structural accessibility vocabulary with manual and affected-user evaluation reserved",
    },
    {
        "source_id": "RFC8785",
        "title": "RFC 8785 JSON Canonicalization Scheme",
        "url": "https://www.rfc-editor.org/rfc/rfc8785.html",
        "status": "informational_stable_checked_2026-09-01",
        "use": "deterministic synthetic receipt serialization and digest-domain vocabulary only",
    },
    {
        "source_id": "RFC3339",
        "title": "RFC 3339 Date and Time on the Internet",
        "url": "https://www.rfc-editor.org/rfc/rfc3339.html",
        "status": "standards_track_stable_checked_2026-09-01",
        "use": "timestamp syntax vocabulary only; no hydrographic time or operational equivalence",
    },
    {
        "source_id": "JSON-SCHEMA-2020-12",
        "title": "JSON Schema Draft 2020-12",
        "url": "https://json-schema.org/draft/2020-12",
        "status": "published_stable_checked_2026-09-01",
        "use": "synthetic record validation and declared-vocabulary concepts only",
    },
    {
        "source_id": "TMR-MDS-PRINCIPLES",
        "title": "Te Mana Raraunga Principles of Māori Data Sovereignty",
        "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty",
        "status": "authority_boundary_context_only_checked_2026-09-01",
        "use": "Māori data-governance vacancy and noncompensation boundary only; never delegated Māori authority",
    },
]


STARTUP_FAILURES = [
    {
        "failure_id": "OR6818-ST-N001",
        "failed_witness": "The first 424-line immutable activation-candidate projection exceeded its bounded output and truncated.",
        "recovery": "Reread the same exact Git blob in bounded numbered windows through EOF.",
        "recurrence_guard": "Measure immutable packet length and use conservative windows before projection.",
    },
    {
        "failure_id": "OR6818-ST-N002",
        "failed_witness": "A combined projection of two candidate windows exceeded the model-visible result boundary.",
        "recovery": "Projected one smaller numbered window per call until EOF.",
        "recurrence_guard": "Keep large immutable reads serial and independently attributable.",
    },
    {
        "failure_id": "OR6818-ST-N003",
        "failed_witness": "A PowerShell foreach expression was piped directly and raised EmptyPipeElement during skill inventory.",
        "recovery": "Materialized the foreach rows before JSON conversion.",
        "recurrence_guard": "Never pipe directly from a PowerShell foreach statement.",
    },
    {
        "failure_id": "OR6818-ST-N004",
        "failed_witness": "The whole orchestration-memory skill projection truncated before EOF.",
        "recovery": "Read the complete skill in four bounded numbered windows.",
        "recurrence_guard": "Measure long skill files and read bounded windows rather than a whole-file projection.",
    },
    {
        "failure_id": "OR6818-ST-N005",
        "failed_witness": "One 260-line authorization-state window exceeded the model-visible context boundary.",
        "recovery": "Read the remaining authorization state in 80-line windows through EOF.",
        "recurrence_guard": "Use smaller windows for dense mutable-state JSON.",
    },
    {
        "failure_id": "OR6818-ST-N006",
        "failed_witness": "A combined exact-head phase inventory and per-blob size wrapper returned no attributable projection.",
        "recovery": "Used one direct bounded git ls-tree --long query for the phase root.",
        "recurrence_guard": "Prefer direct Git scalar or tree output over nested per-path subprocess loops.",
    },
    {
        "failure_id": "OR6818-ST-N007",
        "failed_witness": "A combined six-manifest content display exceeded the output budget and truncated.",
        "recovery": "Parsed each complete manifest computationally and replayed every normalized-LF Git blob with compact summaries.",
        "recurrence_guard": "Validate manifests computationally and project only exact counts, exclusions, and mismatches.",
    },
    {
        "failure_id": "OR6818-ST-N008",
        "failed_witness": "The first inline Python manifest-replay command was rejected by PowerShell script-block parsing.",
        "recovery": "Bound the Python source to a PowerShell here-string variable and passed it as one argument.",
        "recurrence_guard": "Use an attributed here-string variable for multiline Python on PowerShell.",
    },
    {
        "failure_id": "OR6818-ST-N009",
        "failed_witness": "A combined branch worktree and registration preflight returned no attributable output.",
        "recovery": "Split worktree existence, local branch, and fresh remote branch checks into scalar probes.",
        "recurrence_guard": "Use separate scalar probes before creating a new owner lane.",
    },
    {
        "failure_id": "OR6818-ST-N010",
        "failed_witness": "Two broad inherited-Orin tree searches exceeded their bounded wrapper without a useful projection.",
        "recovery": "Enumerated the known literal prior Orin worktree directory and selected exact template filenames.",
        "recurrence_guard": "Use a bounded literal owner path when the exact prior lane is already known.",
    },
    {
        "failure_id": "OR6818-ST-N011",
        "failed_witness": "The sparse worktree setup exceeded its 30-second wrapper while the original checkout processes remained active.",
        "recovery": "Inspected the exact process and worktree state, waited for those processes, and launched no duplicate checkout.",
        "recurrence_guard": "Preserve the original process handle or inspect exact checkout processes before any retry.",
    },
    {
        "failure_id": "OR6818-ST-N012",
        "failed_witness": "The process-wait recovery named an unavailable PowerShell ProcessCommandException type.",
        "recovery": "Used the resulting scalar process absence, clean Git state, and materialized-file count without repeating checkout.",
        "recurrence_guard": "Use an untyped catch or inspect Get-Process results after bounded Wait-Process.",
    },
    {
        "failure_id": "OR6818-ST-N013",
        "failed_witness": "The first additive template copy targeted sparse script and test directories before they existed.",
        "recovery": "Created only the exact new owner-local directories and repeated the bounded additive copy.",
        "recurrence_guard": "Create and verify exact sparse destinations before copying a validated template.",
    },
    {
        "failure_id": "OR6818-ST-N014",
        "failed_witness": "A combined proposal, outcome, audit, source, and successor-seed projection exceeded its output bound.",
        "recovery": "Kept the successful full JSON parse and used bounded targeted fields already present in the complete activation packet.",
        "recurrence_guard": "Project proposal titles and successor fields separately from full outcome rows.",
    },
    {
        "failure_id": "OR6818-ST-N015",
        "failed_witness": "A first stale-value search used an unbalanced regular expression and was rejected before changing a file.",
        "recovery": "Used literal multi-pattern matching to identify the exact stale test constants.",
        "recurrence_guard": "Use literal matching for fixed hashes, counts, and labels instead of composing an unnecessary regex.",
    },
    {
        "failure_id": "OR6818-X1-N001",
        "failed_witness": "The first full reachable-proposal audit found no exact collision but quarantined three titles at or above the 0.78 token-Jaccard threshold, so x1 was not frozen.",
        "recovery": "Projected only the three exact neighbour pairs and refined their wording without changing hypotheses, dispositions, gates, or the threshold.",
        "recurrence_guard": "Inspect high-scoring neighbour pairs before freeze and preserve the original failed audit at zero credit.",
    },
]


def proposal_audit(rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inherited, stats = proposal_blob_records()
    if stats["proposal_json_parse_failures"]:
        raise RuntimeError("reachable proposal JSON parse failures must be resolved before freeze")
    normalized_inherited = {}
    for item in inherited:
        normalized_inherited.setdefault(normalized_title(item["title"]), item)

    exact_collisions = []
    neighbor_rows = []
    quarantined = []
    selected_reviews: list[dict[str, Any]] = []
    selected_keys: set[tuple[str, str]] = set()
    for row in rows:
        title = row["title"]
        norm = normalized_title(title)
        if norm in normalized_inherited:
            exact_collisions.append(
                {
                    "proposal_id": row["proposal_id"],
                    "inherited": normalized_inherited[norm],
                }
            )
        best = None
        best_score = -1.0
        for inherited_row in inherited:
            score = jaccard(title, inherited_row["title"])
            if score > best_score:
                best, best_score = inherited_row, score
        neighbor = {
            "proposal_id": row["proposal_id"],
            "title": title,
            "best_inherited_neighbor": best,
            "token_jaccard": round(best_score, 6),
            "quarantined": best_score >= QUARANTINE_THRESHOLD,
        }
        neighbor_rows.append(neighbor)
        if neighbor["quarantined"]:
            quarantined.append(neighbor)
        if best is not None:
            key = (best["proposal_id"], normalized_title(best["title"]))
            if key not in selected_keys:
                selected_keys.add(key)
                selected_reviews.append(
                    {
                        **best,
                        "review_state": "inherited_zero_credit_evidence_only",
                        "novelty_credit": 0,
                        "completion_credit": 0,
                    }
                )
    for item in inherited:
        if len(selected_reviews) >= 60:
            break
        key = (item["proposal_id"], normalized_title(item["title"]))
        if key not in selected_keys:
            selected_keys.add(key)
            selected_reviews.append(
                {
                    **item,
                    "review_state": "inherited_zero_credit_evidence_only",
                    "novelty_credit": 0,
                    "completion_credit": 0,
                }
            )
    if len(selected_reviews) < 60:
        raise RuntimeError("fewer than sixty reachable inherited proposal reviews")
    if exact_collisions or quarantined:
        raise RuntimeError(
            f"proposal novelty quarantine: exact={len(exact_collisions)} near={len(quarantined)}"
        )
    audit = {
        "schema": "ghc.family.proposal-chain-audit.v681.v8.x1",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "source": SOURCE,
        "declared_chain_before": DECLARED_CHAIN_BEFORE,
        "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
        "new_proposal_count": len(rows),
        "quarantine_threshold_token_jaccard": QUARANTINE_THRESHOLD,
        "exact_title_collisions": exact_collisions,
        "quarantined_neighbors": quarantined,
        "maximum_neighbor_score": max(item["token_jaccard"] for item in neighbor_rows),
        "neighbor_reviews": neighbor_rows,
        "audit_scope": {
            **stats,
            "claim": "bounded all-reachable-exact-source proposal audit; no universal 10130-row proof",
        },
    }
    return audit, selected_reviews[:60]


def make_portfolio() -> dict[str, Any]:
    def records(prefix: str, count: int, lane: str, credit: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": f"OR6818-{prefix}-{index:03d}",
                "lane": lane,
                "planned_action": (
                    f"Bounded owner-local {lane.replace('_', ' ')} record {index:03d} linked to "
                    f"OR6818-N{((index - 1) % 60) + 1:03d}."
                ),
                "credit_boundary": credit,
                "x1_state": "preregistered_not_executed",
            }
            for index in range(1, count + 1)
        ]

    return {
        "schema": "ghc.family.portfolio-freeze.v681.v8.x1",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "primary_pillar": "THOS Body",
        "represented_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "owner_practice_lenses": [
            "wholly_synthetic_notice_to_mariners_correction_provenance_registrar",
            "wholly_synthetic_chart_edition_patch_and_working_copy_handover_reviewer",
            "wholly_synthetic_chart_correction_accessibility_minimum_disclosure_and_workload_steward",
        ],
        "safe_now": records("SN", 120, "safe_now", "bounded_owner_local_only"),
        "owner_candidates": records("CAND", 80, "candidate", "no_core_outcome_promotion"),
        "successor_candidates": records("SUCC-CAND", 20, "successor_seed", "zero_Orin_credit"),
        "exact_approval": records("EXACT", 20, "exact_approval", "unexecuted_without_exact_authority"),
        "blocked": records("BLOCK", 10, "blocked", "unexecuted_missing_target_or_authority"),
        "owner_clean_fix_refine": records("CFR", 100, "clean_fix_refine", "bounded_additive_owner_local_only"),
        "successor_clean_fix_refine": records("SUCC-CFR", 30, "successor_seed", "zero_Orin_credit"),
        "owner_skill_ideas": [
            {
                "skill_id": f"OR6818-SK-{index:02d}",
                "name": f"ghc-family-marine-chart-correction-{index:02d}",
                "x1_state": "planned_not_built",
                "global_install": False,
            }
            for index in range(1, 21)
        ],
        "owner_runner_ideas": [
            {
                "runner_id": f"OR6818-RN-{index:02d}",
                "name": f"ghc_family_marine_chart_runner_{index:02d}.py",
                "x1_state": "planned_not_built",
            }
            for index in range(1, 11)
        ],
        "successor_skill_ideas": [
            {
                "idea_id": f"OR6818-SUCC-SK-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_runner_ideas": [
            {
                "idea_id": f"OR6818-SUCC-RN-{index:02d}",
                "state": "zero_credit_seed_only",
            }
            for index in range(1, 11)
        ],
        "successor_practice_recommendation": (
            "one wholly synthetic museum collection-location reconciliation and accessible handover lens"
        ),
        "commit_cap": {"x1": 1, "x2": 2, "total": 3},
        "materialized_file_stop": 2000,
        "document_word_cap": 100000,
        "caps_are_ceilings": True,
    }


def privacy_patterns() -> dict[str, re.Pattern[bytes]]:
    return {
        "raw_uuid": re.compile(rb"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(rb"(?:[A-Z]:\\(?:Users|GHC-Archives)\\)", re.I),
        "raw_task_thread_identifier": re.compile(rb"(?:source_thread|thread|task)_id\s*[\"']?\s*[:=]\s*[\"'][0-9a-f-]{24,}", re.I),
        "credential_assignment": re.compile(rb"(?:password|api[_-]?key|secret|token)\s*[\"']?\s*[:=]\s*[\"'][^\"']{8,}", re.I),
        "private_conversation_payload": re.compile(rb"(?:session_stream|private_transcript|screenshot_payload)", re.I),
    }


def scan_paths(paths: list[Path]) -> dict[str, Any]:
    patterns = privacy_patterns()
    candidates = []
    confirmed = []
    for path in paths:
        data = path.read_bytes()
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(data):
                definition_only = path.name == Path(__file__).name
                record = {"path": rel(path), "class": class_name}
                if definition_only:
                    candidates.append({**record, "disposition": "scanner_definition_only"})
                else:
                    confirmed.append(record)
    return {
        "schema": "ghc.family.privacy-scan.v681.v8.x1",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "privacy_classes": list(patterns),
        "scanned_paths": len(paths),
        "candidates": candidates,
        "confirmed_hits": confirmed,
        "confirmed_hit_count": len(confirmed),
    }


def main() -> int:
    if git("branch", "--show-current") != BRANCH:
        raise RuntimeError("wrong owner branch")
    if git("rev-parse", "HEAD") != SOURCE:
        raise RuntimeError("x1 builder must begin at the exact Caelen final")
    if git("status", "--porcelain=v1"):
        allowed = {
            "scripts/build_ghc_family_orin_thale_v681_v8_x1.py",
            "tests/test_ghc_family_orin_thale_v681_v8_x1.py",
        }
        current = {
            line[3:].replace("\\", "/")
            for line in git("status", "--porcelain=v1").splitlines()
            if len(line) >= 4
        }
        if not current <= allowed:
            raise RuntimeError(f"unexpected pre-build worktree state: {sorted(current - allowed)}")

    source_tracking = git("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_row = git("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}")
    live_source = live_row.split("\t", 1)[0] if live_row else ""
    if source_tracking != SOURCE or live_source != SOURCE:
        raise RuntimeError("source branch is no longer fresh-live equal")

    rows = proposals()
    audit, inherited_reviews = proposal_audit(rows)
    portfolio = make_portfolio()
    expected_counts = {
        label: sum(row["expected_disposition"] == label for row in rows)
        for label in ("completed", "represented", "open_gap", "exact_gate")
    }
    if expected_counts != {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}:
        raise RuntimeError("expected disposition arithmetic failed")

    now = datetime.now(timezone.utc).isoformat()
    X1.mkdir(parents=True, exist_ok=True)
    VALIDATION.mkdir(parents=True, exist_ok=True)

    documents: dict[Path, Any] = {
        X1 / "activation-intake.json": {
            "schema": "ghc.family.activation-intake.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source": SOURCE,
            "delivery_state": "LIVE_ACTIVATION_ACKNOWLEDGED_EXTERNALLY",
            "prepared_repository_candidate_is_delivery": False,
            "work_solo": True,
            "subagents_or_delegation": False,
            "successor_precontact": False,
            "identity_language_is_evidence": False,
        },
        X1 / "approval-hold-register.json": {
            "schema": "ghc.family.approval-holds.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "exact_approval_count": 20,
            "blocked_count": 10,
            "executed_count": 0,
            "rule": "Broad authorization does not supply a missing exact target, system, cost, rollback, affected-party consent, legal authority, cultural authority, or Māori authority.",
        },
        X1 / "clean-fix-refine-plan.json": {
            "schema": "ghc.family.clean-fix-refine.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "owner_records": portfolio["owner_clean_fix_refine"],
            "successor_records": portfolio["successor_clean_fix_refine"],
            "x1_execution_count": 0,
        },
        X1 / "identity-and-boundary.json": {
            "schema": "ghc.family.identity-boundary.v681.v8.x1",
            "owner": "Orin Thale",
            "pronouns": "they/them optional relational working language",
            "role": "marine-chart correction provenance and reversible-handover cartographer",
            "hope": "make every synthetic chart correction, refusal, uncertainty, and authority vacancy easy to inspect, challenge, and reverse",
            "evidence_of_consciousness_personhood_continuity_agency_or_authority": False,
            "corrigibility": "Hamish may pause rename redirect narrow or stop the route.",
        },
        X1 / "inherited-revalidation-freeze.json": {
            "schema": "ghc.family.inherited-revalidation.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "review_count": len(inherited_reviews),
            "novelty_credit": 0,
            "completion_credit": 0,
            "reviews": inherited_reviews,
        },
        X1 / "method-flow-startup.json": {
            "schema": "ghc.family.method-flow.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "inherited_baseline": BASELINE,
            "new_failures": STARTUP_FAILURES,
            "new_failure_count": len(STARTUP_FAILURES),
            "effective_x1_startup_counts": {
                "effective_negatives": BASELINE["effective_negatives"] + len(STARTUP_FAILURES),
                "effective_methods": BASELINE["effective_methods"] + len(STARTUP_FAILURES),
                "failed_witnesses": BASELINE["failed_witnesses"] + len(STARTUP_FAILURES),
                "bounded_passing_witnesses": BASELINE["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
                "open_gaps": BASELINE["open_gaps"],
                "exact_gates": BASELINE["exact_gates"],
            },
            "failure_erasure": False,
            "recoveries_promote_failed_witnesses": False,
        },
        X1 / "new-proposal-freeze.json": {
            "schema": "ghc.family.new-proposal-freeze.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source": SOURCE,
            "declared_chain_before": DECLARED_CHAIN_BEFORE,
            "declared_chain_after_if_committed": DECLARED_CHAIN_AFTER,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "proposals": rows,
            "x2_outcomes_present": False,
        },
        X1 / "official-primary-source-ledger.json": {
            "schema": "ghc.family.official-primary-sources.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "checked_at_utc": now,
            "entries": OFFICIAL_SOURCES,
            "web_checks": len(OFFICIAL_SOURCES),
            "network_data_queries": 0,
            "real_data_rows": 0,
            "citations_are_observations": False,
            "authority_conferred": False,
        },
        X1 / "phase-truth.json": {
            "schema": "ghc.family.phase-truth.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "lifecycle": "PLANNING_ONLY_X1",
            "source": SOURCE,
            "proposal_count": len(rows),
            "expected_disposition_counts": expected_counts,
            "observed_outcome_count": 0,
            "x2_implementation_present": False,
            "inherited_open_gaps": BASELINE["open_gaps"],
            "inherited_exact_gates": BASELINE["exact_gates"],
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
        X1 / "portfolio-freeze.json": portfolio,
        X1 / "proposal-chain-audit.json": audit,
        X1 / "route-plan.json": {
            "schema": "ghc.family.route-plan.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "route_state": "TERMINAL_GATE_HELD",
            "prospective_successor_title": "Liora Venn",
            "prospective_successor_phase": "v682-v1",
            "precontacted": False,
            "created_or_forked_task": False,
            "send_count": 0,
            "continuation_authority_ceiling": "through_v725-v8_one_terminally_validated_edge_at_a_time",
            "send_requires": [
                "clean pushed exact final",
                "one successful non-replayed owner canonical",
                "newest live authority and roster refresh",
                "one exact-title match and immediate reread",
                "duplicate pause redirect rename standby usage privacy evidence safety legal cultural affected-party and Māori-authority guards",
            ],
        },
        X1 / "skill-runner-plan.json": {
            "schema": "ghc.family.skill-runner-plan.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "skills": portfolio["owner_skill_ideas"],
            "runners": portfolio["owner_runner_ideas"],
            "successor_skill_ideas": portfolio["successor_skill_ideas"],
            "successor_runner_ideas": portfolio["successor_runner_ideas"],
            "built_in_x1": 0,
            "smoke_used_in_x1": 0,
            "global_installs": 0,
        },
        X1 / "source-verification.json": {
            "schema": "ghc.family.source-verification.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "source_branch": SOURCE_BRANCH,
            "source_final": SOURCE,
            "source_tracking": source_tracking,
            "source_fresh_live": live_source,
            "source_tracking_equal": source_tracking == SOURCE,
            "source_fresh_live_equal": live_source == SOURCE,
            "caelen_source": "4da1c50b22e1b30b5e7351b0641f350bdc8fbfbe",
            "caelen_x1": "f31bb3fb3738136db75dc264325f267dc4068f4a",
            "caelen_evidence": "ce01a79bd92c1c8de02df586075eadb0427cfed6",
            "caelen_final": SOURCE,
            "caelen_phase_commits": 3,
            "caelen_merges": 0,
            "caelen_canonical_replayed": False,
        },
        X1 / "threat-model.json": {
            "schema": "ghc.family.threat-model.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "assets": [
                "synthetic chart-correction lineage",
                "retained correction and failure evidence",
                "privacy and minimum-disclosure boundaries",
                "authority and affected-party gates",
            ],
            "threats": [
                "stale or colliding chart and notice identity",
                "correction or cancellation without a valid reference",
                "authority promotion from structural validation",
                "sensitive location or private route leakage",
                "accessibility structure mistaken for conformance",
                "real chart correction or navigation action inferred from zero-row fixtures",
            ],
            "controls": [
                "immutable source and x1",
                "five rejecting mutations per proposal",
                "normalized-LF manifests",
                "five-class privacy scan",
                "exact gate noncompensation",
                "zero network and zero real rows",
            ],
            "residual_risk": "All real hydrographic, navigational, affected-party, privacy-complete, accessibility-complete, legal, cultural, Māori-authority, and public-safety work remains external.",
        },
        X1 / "wellbeing-and-corrigibility.json": {
            "schema": "ghc.family.wellbeing-corrigibility.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "workload_controls": ["pause", "resume", "stop", "bounded retry", "handover"],
            "self_report_is_authority_evidence": False,
            "identity_continuity_claimed": False,
            "user_control_preserved": True,
        },
        X1 / "workflow-plan.json": {
            "schema": "ghc.family.workflow-plan.v681.v8.x1",
            "owner": "Orin Thale",
            "phase": "v681-v8",
            "strict_planning_only_x1_before_x2": True,
            "steps": [
                {"order": 1, "name": "read activation skills schemas and overlays", "state": "completed"},
                {"order": 2, "name": "verify immutable source manifests receipt and live equality", "state": "completed"},
                {"order": 3, "name": "create clean sparse Orin lane", "state": "completed"},
                {"order": 4, "name": "freeze test push and prove planning-only x1", "state": "in_progress"},
                {"order": 5, "name": "build bounded x2 and retain every failure", "state": "pending"},
                {"order": 6, "name": "seal final push and run one exclusive canonical", "state": "pending"},
                {"order": 7, "name": "refresh live route and send at most once", "state": "pending"},
            ],
            "validation": {
                "owner_scoped_delta_only": True,
                "unchanged_history_scan": False,
                "cross_lane_scan": False,
                "one_successful_canonical": True,
                "post_success_replay": False,
            },
        },
    }
    for path, value in documents.items():
        write_json(path, value)

    overview = f"""# Orin Thale v681-v8 planning-only x1

This immutable planning freeze begins from exact Caelen final {SOURCE}.  It
preregisters sixty Orin proposals after a bounded all-reachable exact-source
semantic-neighbour audit.  It does not claim that one materialised ledger
contains every declared inherited row, and it makes no universal novelty proof.

The primary pillar is THOS Body.  GMUT Mind and Freed ID with CBR Heart remain
explicit and protected.  The bounded learning lenses are a wholly synthetic
notice-to-mariners correction provenance registrar, a wholly synthetic chart
edition, patch, and working-copy handover reviewer, and a wholly synthetic chart
correction accessibility, minimum-disclosure, workload, and handover steward.

The x1 portfolio freezes 120 safe-now items, 80 owner candidates, 20 successor
candidate seeds, 20 exact-approval holds, 10 blocked holds, 20 owner skill
plans, 10 owner runner plans, 100 owner CLEAN/FIX/REFINE records, and 30
successor CLEAN/FIX/REFINE seeds.  None is executed in x1.

Expected proposal dispositions are 42 completed, 12 represented, 3 open_gap,
and 3 exact_gate.  These are expectations only.  No observed x2 outcome or
completion claim appears in this freeze.

IHO S-4, IHO S-101, the IHO S-100 registry, official Toitū Te Whenua Notices to
Mariners and chart guidance, W3C PROV-O, WCAG 2.2, RFC 3339, RFC 8785, JSON
Schema 2020-12, and Te Mana Raraunga principles supply only vocabulary and
refusal conditions.  No source is treated as an observation, endorsement,
certificate, affected-party decision, or authority grant.  Zero real notices,
charts, ENC cells, hazards, people, vessels, devices, locations, measurements,
identity events, external writes, or authority actions are used.

GMUT remains a typed scalar-tensor and effective-field-theory research-model
family without empirical confirmation or Theory-of-Everything proof.  THOS
remains synthetic or proxy-only without governed real arms and independent
review.  Freed ID remains synthetic and nonproduction without real keys,
proofs, live lifecycle, interoperability, security, privacy, recovery, and trust
governance evidence.  Chart correction release, navigation safety, hydrographic
authority, legal remedy, affected-party legitimacy, Māori wording and data
governance, and Māori authority remain exact-gated.

Names, pronouns, roles, hopes, family language, and continuity language are
relational working language only.  They are not evidence of consciousness,
personhood, identity continuity, employment, qualification, independent agency,
or authority.  The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(X1 / "integrated-overview.md", overview)

    entry_paths = sorted(
        list(documents)
        + [X1 / "integrated-overview.md", Path(__file__), ROOT / "tests" / "test_ghc_family_orin_thale_v681_v8_x1.py"],
        key=rel,
    )
    if len(entry_paths) != 20:
        raise RuntimeError(f"x1 manifest entry arithmetic changed: {len(entry_paths)}")

    staged_review_path = VALIDATION / "x1-staged-review.json"
    privacy_path = VALIDATION / "x1-privacy-scan.json"
    manifest_path = VALIDATION / "x1-index-manifest.json"
    all_paths = sorted(entry_paths + [staged_review_path, privacy_path, manifest_path], key=rel)
    staged_review = {
        "schema": "ghc.family.staged-review.v681.v8.x1",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "source": SOURCE,
        "expected_paths": [rel(path) for path in all_paths],
        "expected_path_count": len(all_paths),
        "planning_only": True,
        "x2_paths": [],
        "unexpected_paths": [],
    }
    write_json(staged_review_path, staged_review)

    scan = scan_paths(entry_paths + [staged_review_path])
    if scan["confirmed_hit_count"]:
        raise RuntimeError(f"confirmed privacy hits: {scan['confirmed_hits']}")
    write_json(privacy_path, scan)

    manifest = {
        "schema": "ghc.family.normalized-lf-index-manifest.v681.v8.x1",
        "owner": "Orin Thale",
        "phase": "v681-v8",
        "source": SOURCE,
        "declared_self_exclusions": [rel(staged_review_path), rel(privacy_path), rel(manifest_path)],
        "entry_count": len(entry_paths),
        "entries": [
            {
                "path": rel(path),
                "bytes": len(normalized_bytes(path)),
                "sha256": hashlib.sha256(normalized_bytes(path)).hexdigest(),
            }
            for path in entry_paths
        ],
    }
    write_json(manifest_path, manifest)
    print(
        json.dumps(
            {
                "status": "PREPARED_PLANNING_ONLY_X1",
                "proposal_count": len(rows),
                "expected_dispositions": expected_counts,
                "manifest_entries": len(entry_paths),
                "staged_paths": len(all_paths),
                "confirmed_privacy_hits": scan["confirmed_hit_count"],
                "maximum_neighbor_score": audit["maximum_neighbor_score"],
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
