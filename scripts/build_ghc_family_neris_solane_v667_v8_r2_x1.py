#!/usr/bin/env python3
"""Build and validate the planning-only Neris Solane v667-v8-r2 x1 freeze."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v8-r2"
OWNER = "Neris Solane"
OWNER_SLUG = "neris-solane"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
REL_PHASE_ROOT = f"docs/{OWNER_SLUG}/{PHASE}"
NOW = "2026-08-24T00:22:45.332Z"

SOURCE_BRANCH = "codex/GHC-Family/neris-solane-v667-v8-full-tools"
SOURCE_PARENT_SHA = "6a29ea3d264591bde02964ea8bf4c2c09c802084"
SOURCE_X1_SHA = "653ff8a70328e6dd8641bb9b2d1887ce94f1759e"
SOURCE_EVIDENCE_SHA = "6a29ea3d264591bde02964ea8bf4c2c09c802084"
SOURCE_SHA = "0db6ed4837c09868a27782e9309c7bea5c943d44"
SOURCE_PHASE_ROOT = "docs/neris-solane/v667-v8"
SOURCE_BATON_SHA256 = "c9fdfc7014bd49cfef947c89569e221c3aaea337318c5740451e59eeb0333d3e"
SOURCE_CANONICAL_FAILURE_SHA256 = "fdab810d374532ce2f6cbf51150d9d0e83566866bd43b660f0d7a9f5ea836d55"
SOURCE_COMPONENT_COMPOSITE_SHA256 = "1de60f7287c3419e624e2acc99cf1e6fce9f3b3558e08fc02d95bde2ad6d6455"

INHERITED_PROPOSAL_COUNT = 4530
NEW_FROZEN_TOTAL = 4550
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
PRIMARY_PILLAR = "THOS Body"
PRACTICE = "wholly synthetic software supply-chain and release-engineering assurance"
PROFESSION_LENS = "software supply-chain and release engineering"
ROLE = "datum-boundary weaver"
HOPE = (
    "expose provenance, uncertainty, dependency boundaries, and stop conditions "
    "before local software evidence is mistaken for production, security, or scientific authority"
)

SOURCE_BUILDER = ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_x1.py"
_spec = importlib.util.spec_from_file_location("_neris_v667_v8_source_x1", SOURCE_BUILDER)
if _spec is None or _spec.loader is None:
    raise RuntimeError("unable to load immutable Neris v667-v8 x1 compatibility surface")
source_base = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(source_base)
run_git = source_base.run_git
git_json = source_base.git_json
similarity = source_base.similarity

MANDATORY_SKILLS = [
    "ghc-freed-id-flashcards", "ghc-family-index",
    "ghc-family-reflection-remaster", "ghc-family-method-flow-state",
    "ghc-family-meta-tool-box", "ghc-family-auth-permission-state",
    "ghc-family-roster-check", "ghc-main-orchestration-memory",
    "ghc-main-startup-builder", "ghc-main-compact-restart-builder",
    "ghc-main-closeout-builder", "ghc-main-retry", "ghc-open-gate-rail",
    "ghc-timestamp-flow", "ghc-full-tools-skill-bank",
    "ghc-family-truth-bridge", "ghc-worktree-branch-rotation",
    "ghc-web-reflection-ledger", "ghc-watcher-notifier-cadence",
    "ghc-drive-bank-guardian", "ghc-approval-packet-splitter",
]

ACTIVE_ROSTER = [
    "Eiren Kestrel", "Elaren Kestrel", "Neris Solane", "Vesper Arlen",
    "Lyren Moss", "Ilyra Fen", "Auren Lark", "Sable Rook", "Caelen Ash",
    "Orin Thale", "Liora Venn", "Tamar Vey", "Elowen Cairn",
    "Sylven Arc", "Caelen Morrow",
]

PROTECTED_GATES = [
    "real maintainers users participants affected parties operators regulators cultural authorities or Maori authorities",
    "real credentials accounts secrets signing keys certificates protected disclosures telemetry packages releases registries devices or production services",
    "real publication deployment upload signing attestation revocation disclosure access purchase account mutation or third-party write",
    "professional software security privacy accessibility legal licensing cultural workplace release or production authority",
    "complete provenance reproducible build standards conformance license compliance privacy accessibility exhaustive security production readiness or deployment approval",
    "empirical GMUT final physics Theory-of-Everything proof or canon",
    "THOS operational effectiveness AGI ASI consciousness personhood or independent reproduction",
    "Freed ID keys proofs credentials identity events recovery events or trust-governance actions",
    "legal cultural affected-party traditional-knowledge or Maori interpretation governance or authority",
    "system Python C-drive package elevation Windows-feature Codex-desktop host-security reboot destructive plugin-cache sibling-lane history-rewrite or deletion action",
    "successor contact before the current terminal gate or substitution for Vesper Arlen",
    "Stage 20 promotion or conversion of same-owner synthetic evidence into external truth or authority",
]

MUTATION_CLASSES = [
    "missing_required_field",
    "wrong_type_version_digest_or_integrity",
    "provenance_license_or_authority_smuggling",
    "lifecycle_external_or_production_action",
    "security_conformance_or_stage20_promotion",
]

TOOL_ROWS = [
    ("check-wheel-contents", "python", "0.6.3", "Python >=3.10", "MIT", "check_wheel_contents-0.6.3-py3-none-any.whl", "5ae39c8c434b972f0740d04610759168590713175aab584b012b1b84f6771874", "https://pypi.org/project/check-wheel-contents/0.6.3/", "inspect one disposable wheel for common content mistakes"),
    ("wheel-inspect", "python", "1.8.0", "Python ~=3.10", "MIT", "wheel_inspect-1.8.0-py3-none-any.whl", "0881fa6730873251f30b481173c6083608bdcc24212a483b9d9605bf85d4cb80", "https://pypi.org/project/wheel-inspect/1.8.0/", "parse one local wheel metadata structure without executing its code"),
    ("pydistcheck", "python", "0.11.3", "Python >=3.9", "BSD-3-Clause", "pydistcheck-0.11.3-py3-none-any.whl", "9b3a92b414aeb171a2c5e2928c5591a01a05681358072194a929813fe6529dc2", "https://pypi.org/project/pydistcheck/0.11.3/", "inspect one disposable distribution for bounded packaging anomalies"),
    ("import-linter", "python", "2.13", "Python >=3.10", "BSD-2-Clause metadata", "import_linter-2.13-py3-none-any.whl", "c0372e7ee5e15657bc06a8e841445e13237afd738a672d26863dc927af9f0bf5", "https://pypi.org/project/import-linter/2.13/", "enforce one synthetic import-layer contract"),
    ("pydoclint", "python", "0.9.1", "Python >=3.10", "MIT metadata", "pydoclint-0.9.1-py3-none-any.whl", "685b4a1c3c852045e4523b61d9c3f789672dfab3a454fe51a9e346c9e21dfcdb", "https://pypi.org/project/pydoclint/0.9.1/", "check one disposable function and docstring contract"),
    ("interrogate", "python", "1.7.0", "Python >=3.8", "MIT classifier metadata", "interrogate-1.7.0-py3-none-any.whl", "b13ff4dd8403369670e2efe684066de9fcb868ad9d7f2b4095d8112142dc9d12", "https://pypi.org/project/interrogate/1.7.0/", "measure docstring coverage for one disposable module"),
    ("pytest-timeout", "python", "2.4.0", "Python >=3.7", "MIT metadata", "pytest_timeout-2.4.0-py3-none-any.whl", "c42667e5cdadb151aeb5b26d114aff6bdf5a907f176a007a30b940d3d865b5c2", "https://pypi.org/project/pytest-timeout/2.4.0/", "enforce one short synthetic test deadline"),
    ("spdx-tools", "python", "0.8.5", "Python >=3.10", "Apache-2.0", "spdx_tools-0.8.5-py3-none-any.whl", "7c2d5865941be9d2e898f5b084e8d5422dd298dc5a29320ddb198fec304f59c4", "https://pypi.org/project/spdx-tools/0.8.5/", "parse and validate one synthetic SPDX document"),
    ("publint", "node", "0.3.24", "Node >=18", "MIT", "npm registry package", "sha512-9zS56KrKBoqi5Qt8h92uMP8TTM9AYZSgnmCo4u2priMqkOZvQnTsziZ2p5LJ2ywbYkAjoCDp2jda9u4cgFefIw==", "https://www.npmjs.com/package/publint/v/0.3.24", "lint one disposable npm package surface"),
    ("@arethetypeswrong/cli", "node", "0.18.5", "Node >=20", "MIT", "npm registry package", "sha512-gM+8vRsQOD/Uc7EnBedUhkG5OCsDWE4uoak5QvomGpMpaky0Eh41p04nIMgrWb8EOmqZUJGc6zz9hsP6E56R7g==", "https://www.npmjs.com/package/@arethetypeswrong/cli/v/0.18.5", "inspect one packed disposable declaration surface"),
    ("npm-package-json-lint", "node", "11.0.0", "Node >=22 and npm >=10", "MIT", "npm registry package", "sha512-XOFaxHM+TB9tK51Uj609kA1iA87cJe/VNCv/5INLCDbM///KpZpIai+t9LRRyOzvkd62j0JEWKSJeDUlzOSG6Q==", "https://www.npmjs.com/package/npm-package-json-lint/v/11.0.0", "validate one disposable package manifest"),
    ("lockfile-lint", "node", "5.0.1", "Node >=16", "Apache-2.0", "npm registry package", "sha512-Ukjf5yGBQwfl7L2niV3in7bU5wEww3+4Dkw89JGTzOuq18tzS7jaszl2oO7M6u+jcim080MfX5E4Gokt1KhRHQ==", "https://www.npmjs.com/package/lockfile-lint/v/5.0.1", "check one synthetic lockfile registry-origin policy"),
    ("syncpack", "node", "15.3.3", "Node >=14.17", "MIT", "npm registry package", "sha512-MC99meBhgc/E5xbB5mFUS99wj4bquTbKLKHLXYh3qPbmPZl2HD8KA4ls29a9Xv67oZ03isCaJaqSl+JIfXIfpA==", "https://www.npmjs.com/package/syncpack/v/15.3.3", "check one disposable workspace dependency-version alignment"),
]

TOOL_PLAN = [
    {
        "tool": name, "ecosystem": ecosystem, "version": version,
        "runtime": runtime, "license_metadata": license_meta,
        "artifact": artifact, "sha256_or_integrity": digest,
        "official_url": url, "bounded_use": bounded_use,
    }
    for name, ecosystem, version, runtime, license_meta, artifact, digest, url, bounded_use in TOOL_ROWS
]

STANDARD_SOURCES = [
    ("pip secure installs guidance", "https://pip.pypa.io/en/stable/topics/secure-installs/", "exact pins hashes wheel-only resolution and dependency closure"),
    ("Python virtual environments", "https://docs.python.org/3/library/venv.html", "isolated environment and non-portability boundaries"),
    ("Python packaging RECORD specification", "https://packaging.python.org/en/latest/specifications/recording-installed-packages/", "installed-file hash and metadata vocabulary"),
    ("npm package-lock documentation", "https://docs.npmjs.com/cli/configuring-npm/package-lock-json", "lockfile resolved and integrity vocabulary"),
    ("npm scripts documentation", "https://docs.npmjs.com/cli/using-npm/scripts", "lifecycle-script identification and disablement"),
    ("SLSA provenance specification", "https://slsa.dev/spec/v1.2/provenance", "provenance predicate and build-claim vocabulary"),
    ("SPDX specification", "https://spdx.github.io/spdx-spec/v2.3/", "software bill-of-materials structure"),
    ("CycloneDX specification", "https://cyclonedx.org/specification/overview/", "component and dependency inventory vocabulary"),
    ("NIST Secure Software Development Framework", "https://csrc.nist.gov/pubs/sp/800/218/final", "secure-development practice vocabulary"),
    ("W3C PROV-O Recommendation", "https://www.w3.org/TR/prov-o/", "entity activity derivation revision and provenance vocabulary"),
    ("Web Content Accessibility Guidelines 2.2", "https://www.w3.org/TR/WCAG22/", "structural accessibility and manual-review reservations"),
    ("New Zealand Privacy Commissioner privacy principles", "https://www.privacy.org.nz/privacy-principles/", "purpose minimization access correction and disclosure reservations"),
    ("Te Mana Raraunga principles", "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "authority-reservation labels only"),
    ("Git cat-file documentation", "https://git-scm.com/docs/git-cat-file", "exact Git-object byte-length discipline"),
]

PROPOSAL_SPECS = [
    ("synthetic direct-tool identity and version capsule with ecosystem runtime floor source and no fitness claim", "Tool identity version ecosystem runtime and source remain explicit without a fitness claim.", ["S15"], "completed"),
    ("artifact digest and registry-integrity ledger with mismatch quarantine and no authenticity promotion", "Digest equality is retained separately from authenticity maintainer identity and trust.", ["S01", "S03", "S04"], "completed"),
    ("dependency-closure graph with direct versus transitive classification and duplicate visibility", "Every resolved dependency stays attributable while completeness remains unclaimed.", ["S01", "S04", "S08"], "completed"),
    ("lifecycle-script quarantine policy with disabled-by-default install and explicit exception gate", "Node lifecycle scripts stay disabled unless a separate exact review permits one.", ["S05", "S09"], "completed"),
    ("license-metadata inventory with unknown state conflict retention and no legal interpretation", "License labels remain metadata and missing or conflicting values stay visible.", ["S07"], "completed"),
    ("synthetic SBOM structural validator with relationships hashes and no certification", "A synthetic SBOM may pass structural checks without proving deployed contents or compliance.", ["S07", "S08"], "completed"),
    ("provenance statement graph with builder vacancy materials parameters and no attestation", "Provenance fields remain assertions with vacant trust anchors and zero signing.", ["S06", "S10"], "completed"),
    ("reproducible-wheel comparison fixture with normalized timestamps exact diff and no reproducible-build claim", "Two disposable builds expose differences while any pass stays fixture-local.", ["S02", "S03"], "completed"),
    ("npm tarball content and export-surface inspection with pack-only execution and zero publication", "A local pack exposes files and exports without account use or publication.", ["S04", "S05"], "completed"),
    ("lockfile registry-origin and integrity policy with host allowlist and rejecting mutation", "Synthetic lockfile entries require the preregistered host and integrity fields.", ["S04"], "completed"),
    ("Python import-layer contract with acyclic boundary and forbidden-edge mutation", "A disposable package demonstrates one allowed direction and rejects one forbidden edge.", ["S18"], "completed"),
    ("typed package API surface snapshot with declaration resolution export map and diff receipt", "Declaration and export checks detect a bounded defect without semantic compatibility promises.", ["S24"], "completed"),
    ("bounded test-timeout contract with deterministic fixture and retained timeout witness", "A local deadline catches one deliberate stall without timing the full repository.", ["S21"], "completed"),
    ("documentation contract and coverage ledger with parameter-return consistency", "Docstring checks remain structural while clarity and affected-user evaluation stay reserved.", ["S19", "S20"], "completed"),
    ("THOS staged-release queue with equal symbolic budgets stop precedence and zero operators", "A participant-free queue represents release gates without deployment evidence.", ["S09", "S11"], "represented"),
    ("GMUT dependency-risk symbolic board with typed nodes uncertainty and zero fitted coefficients", "A symbolic graph fits no likelihood prediction physical law or empirical result.", ["S09", "S10"], "represented"),
    ("Freed ID zero-key tool-provenance graph with correction tombstone and no lifecycle calls", "A zero-key graph has no issuer holder proof resolver credential or trust decision.", ["S06", "S10", "S12"], "represented"),
    ("CBR accessibility privacy contestation and remedy shell with zero users or decisions", "A shell represents notice correction appeal and remedy without deciding them.", ["S11", "S12", "S13"], "represented"),
    ("real supply-chain evidence escrow requiring governed builds authentic artifacts users incidents and independent review", "Real build telemetry maintainers affected users incidents and reproduction are absent.", ["S06", "S08", "S09"], "open_gap"),
    ("exact authority circuit for publication deployment signing disclosure licensing privacy cultural and Maori decisions", "No real authority action proceeds without exact competent authority.", ["S09", "S12", "S13"], "exact_gate"),
]

STARTUP_FAILURES = [
    ("NS6678R2-X1-N001", "combined roster and authorization display exceeded the result budget", "read separately and finish authorization in numbered windows"),
    ("NS6678R2-X1-N002", "a JavaScript orchestration string failed before metadata inventory", "use plain delimiters in a bounded second command"),
    ("NS6678R2-X1-N003", "the first four-window prior-baton display was truncated", "reread missing ranges in smaller windows"),
    ("NS6678R2-X1-N004", "the 94-270 baton recovery was itself truncated", "read the omitted 173-200 range separately"),
    ("NS6678R2-X1-N005", "a receipt search guessed two nonexistent owner filenames", "enumerate the exact owner surface first"),
    ("NS6678R2-X1-N006", "combined package inventory ended before Node state", "resolve npm root once and test exact paths"),
    ("NS6678R2-X1-N007", "grouped official-source search returned no attributable projection", "use one explicitly projected primary page and registry APIs"),
    ("NS6678R2-X1-N008", "grouped direct-page open returned no attributable projection", "retain it and use bounded primary registry records"),
    ("NS6678R2-X1-N009", "sparse set left an empty index and absent-file status", "verify lock state and run one sparse-aware read-tree"),
    ("NS6678R2-X1-N010", "sparse add rejected an unsupported no-cone option", "use the supported skip-checks surface"),
    ("NS6678R2-X1-N011", "working-tree baton hash used a line-ending materialization domain", "hash exact committed Git-blob bytes"),
    ("NS6678R2-X1-N012", "the first apply-patch orchestration payload had unescaped delimiters", "split patches and use delimiter-free source text"),
    ("NS6678R2-X1-N013", "the first x1 privacy scan matched the literal Unix user-path rule in its own scanner source", "construct user-path fragments dynamically and rerun only the uncommitted x1 build"),
]


def canonical_json(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8") + b"\n")


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def source_profiles() -> list[dict[str, str]]:
    rows = []
    for index, (name, url, use) in enumerate(STANDARD_SOURCES, start=1):
        rows.append({"source_id": f"S{index:02d}", "name": name, "url": url, "bounded_use": use, "status": "official or primary source reviewed read-only"})
    for index, tool in enumerate(TOOL_PLAN, start=len(rows) + 1):
        rows.append({"source_id": f"S{index:02d}", "name": f"{tool['tool']} {tool['version']} release", "url": tool["official_url"], "bounded_use": tool["bounded_use"], "status": "primary registry metadata verified read-only"})
    return rows


def build_corpus() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    corpus, construction = source_base.build_corpus()
    freeze = git_json(SOURCE_X1_SHA, f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    additions = [
        {
            "proposal_id": row["proposal_id"], "title": row["title"],
            "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
            "source_row_sha256": hashlib.sha256(canonical_json(row)).hexdigest(),
        }
        for row in freeze["new_proposals"]
    ]
    corpus = list(corpus) + additions
    construction = list(construction) + [{"source": f"{SOURCE_X1_SHA}:{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json", "rows_added": len(additions), "running_total": len(corpus), "credit": 0}]
    if len(corpus) != INHERITED_PROPOSAL_COUNT:
        raise AssertionError(f"inherited corpus mismatch: {len(corpus)}")
    return corpus, construction


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (title, invariant, sources, outcome) in enumerate(PROPOSAL_SPECS, start=1):
        proposal_id = f"NS6678R2-N{index:03d}"
        rows.append({
            "proposal_id": proposal_id, "title": title, "distinctive_invariant": invariant,
            "source_ids": sources, "primary_pillar": PRIMARY_PILLAR,
            "practice_lens": PRACTICE, "expected_disposition": outcome,
            "hypothesis": f"A wholly synthetic fixture can represent and test: {invariant}",
            "falsifier": "reject the positive accept an invalid mutation omit provenance or cross a protected gate",
            "outcomes_observed": False, "x1_planning_only": True,
            "x2_implementation_count": 0, "completion_credit": 0,
            "negative_fixture_count": 5,
            "negative_fixtures": [{"mutation_id": f"{proposal_id}-M{i:02d}", "class": kind, "status": "preregistered_not_executed"} for i, kind in enumerate(MUTATION_CLASSES, start=1)],
            "planned_artifacts": [f"{REL_PHASE_ROOT}/x2/proposals/{proposal_id.casefold()}/{name}" for name in ("contract.json", "mutation-results.json", "bounded-receipt.json")],
            "rollback": "restore only the last valid owner-local synthetic fixture and retain every failure",
            "protected_gates": PROTECTED_GATES,
        })
    return rows


def selected_inherited_rows() -> list[dict[str, Any]]:
    freeze = git_json(SOURCE_X1_SHA, f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json")
    return [{
        "proposal_id": row["proposal_id"], "title": row["title"],
        "source_path": f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json",
        "source_row_sha256": hashlib.sha256(canonical_json(row)).hexdigest(),
        "selection_reason": "immediately inherited read-only integrity revalidation",
        "novelty_credit": 0, "automatic_completion_credit": 0,
        "completion_credit": 0, "outcomes_observed": False, "x1_planning_only": True,
    } for row in freeze["new_proposals"][:20]]


def build_novelty(corpus: list[dict[str, Any]], construction: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    exact, nearest, pairs = [], [], []
    for proposal in proposals:
        exact.extend({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]} for row in corpus if str(row["title"]).casefold() == proposal["title"].casefold())
        score, inherited = max(((similarity(proposal["title"], str(row["title"])), row) for row in corpus), key=lambda item: item[0])
        nearest.append({"proposal_id": proposal["proposal_id"], "score": round(score, 6), "inherited_proposal_id": inherited["proposal_id"], "inherited_title": inherited["title"], "distinctive_invariant": proposal["distinctive_invariant"]})
    for index, left in enumerate(proposals):
        for right in proposals[index + 1:]:
            score = similarity(left["title"], right["title"])
            if score >= 0.90:
                pairs.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        groups.setdefault(str(row["proposal_id"]), []).append({"title": str(row["title"]), "source_path": str(row.get("source_path", ""))})
    duplicates = [{"proposal_id": key, "occurrence_count": len(values), "occurrences": values} for key, values in sorted(groups.items()) if len(values) > 1]
    return {
        "schema": "ghc-family-proposal-novelty-audit-v8", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "corpus_row_count": len(corpus), "corpus_unique_proposal_id_count": len(groups),
        "corpus_duplicate_proposal_id_count": len(duplicates),
        "corpus_duplicate_occurrence_overage": sum(row["occurrence_count"] - 1 for row in duplicates),
        "corpus_duplicate_proposal_ids": duplicates, "corpus_construction": construction,
        "corpus_canonical_sha256": hashlib.sha256(canonical_json(corpus)).hexdigest(),
        "new_proposal_count": len(proposals), "new_frozen_total": len(corpus) + len(proposals),
        "exact_title_collisions": exact, "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": max(row["score"] for row in nearest),
        "pair_collision_threshold": 0.90, "pair_collisions_at_or_above_threshold": pairs,
        "valid": not exact and not pairs and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "lexical comparison is triage only and grants no semantic or completion credit",
    }


def portfolio_row(item_id: str, title: str, approval: str, expected: str, target: str) -> dict[str, Any]:
    return {
        "item_id": item_id, "title": title, "approval_class": approval,
        "expected_execution_disposition": expected, "target_owner": target,
        "x1_state": "frozen_not_executed", "x2_execution_count": 0,
        "observed_outcome": None, "automatic_credit": 0,
        "rollback": "stop locally retain the failed witness and leave sibling shared account production and external state unchanged",
        "protected_gates": PROTECTED_GATES,
    }


def rows(prefix: str, titles: Iterable[str], approval: str, expected: str, target: str) -> list[dict[str, Any]]:
    return [portfolio_row(f"{prefix}-{index:03d}", title, approval, expected, target) for index, title in enumerate(titles, start=1)]


def build_portfolio(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    safe = [
        "reconstruct the exact inherited proposal corpus",
        "verify source head ancestry manifests clean state and live equality",
        "freeze twenty inherited zero-credit revalidations",
        "freeze twenty genuinely new proposals",
        "record startup failures and bounded recoveries",
        "record fifteen active main tasks and Tavian standby",
        "record the user-directed no-contact route",
        "freeze exact versions for thirteen candidates",
        "freeze Python wheel SHA-256 values",
        "freeze npm registry integrity values",
        "freeze runtime compatibility floors",
        "freeze license metadata as inventory only",
        "create a D-first isolated Python transaction plan",
        "create a D-prefix ignore-scripts npm plan",
        "plan exact dependency-closure receipts",
        "plan dated package advisory checks",
        "plan positive tool smokes",
        "plan rejecting tool fixtures",
        "plan exact package rollback",
        "plan direct versus transitive accounting",
        "plan machine-readable SBOM output",
        "plan exact owner-only manifest replay",
        "plan five-class private-material review",
        "plan strict JSON parsing",
        "plan source-to-final ancestry checks",
        "plan one exact-final canonical invocation",
        "plan no replay after canonical success",
        "plan canonical-failure retention",
        "plan D-prefix Codex shadow detection",
        "plan a long committed Vesper baton without sending it",
    ]
    successor_safe = [
        "read the committed Neris baton through EOF",
        "reverify exact final and fresh live equality",
        "keep Neris failures and recoveries separate",
        "reuse tool catalogue with zero automatic novelty",
        "check the D-prefix Codex resolver",
        "select only phase-relevant tools",
        "reuse exact artifact hashes",
        "keep lifecycle scripts disabled",
        "retain license metadata as nonlegal inventory",
        "use owner-only delta validation",
        "keep sibling lanes read-only",
        "rotate before two thousand files",
        "preserve strict x1 before x2",
        "retain one-shot canonical discipline",
        "resolve exact title only after terminal gate",
        "exclude private identifiers and user paths",
        "preserve Tavian on standby",
        "carry NOT_READY_FOR_STAGE_20",
        "reserve empirical and authority claims",
        "record each new failure before recovery",
    ]
    candidate = [
        "compare two disposable wheel builds",
        "exercise a synthetic SPDX graph",
        "exercise a synthetic CycloneDX graph",
        "enforce one Python import contract",
        "compare one TypeScript declaration surface",
        "inspect one npm tarball",
        "enforce one lockfile registry allowlist",
        "exercise one short pytest timeout",
        "compare docstring coverage and contracts",
        "record one license metadata conflict",
        "record one absent license state",
        "check one workspace version mismatch",
        "exercise one provenance correction chain",
        "exercise one accessible failure explanation",
        "measure command precedence without changing PATH",
    ]
    successor_candidate = [
        "evaluate thirteen tools against the next lens",
        "measure nonoverlapping tool evidence",
        "test one additional package-format fixture",
        "test one declaration-resolution fixture",
        "test one lockfile-host mutation",
        "test one SPDX relationship mutation",
        "test one timeout cleanup path",
        "test one import-boundary mutation",
        "test one license unknown state",
        "test one accessible failure summary",
        "compare D-prefix latency without generalizing",
        "evaluate command-shim collision handling",
        "evaluate partial-resolution rollback",
        "evaluate cache reuse without cache guarantees",
        "evaluate an upgrade only under fresh authority",
    ]
    skills = [
        "ghc-family-toolchain-transaction-guard",
        "ghc-family-artifact-integrity-ledger",
        "ghc-family-wheel-content-audit",
        "ghc-family-package-metadata-boundary",
        "ghc-family-lockfile-origin-policy",
        "ghc-family-import-contract",
        "ghc-family-api-surface-check",
        "ghc-family-test-timeout-discipline",
        "ghc-family-spdx-structure-validator",
        "ghc-family-codex-prefix-guard",
    ]
    successor_skills = [f"ghc-family-vnext-{name.removeprefix('ghc-family-')}" for name in skills]
    runners = [
        "ghc_family_toolchain_transaction_guard.py",
        "ghc_family_artifact_integrity_ledger.py",
        "ghc_family_wheel_content_audit.py",
        "ghc_family_package_metadata_boundary.py",
        "ghc_family_lockfile_origin_policy.mjs",
        "ghc_family_import_contract.py",
        "ghc_family_api_surface_check.mjs",
        "ghc_family_test_timeout_discipline.py",
        "ghc_family_spdx_structure_validator.py",
        "ghc_family_codex_prefix_guard.ps1",
    ]
    successor_runners = [name.replace("ghc_family_", "ghc_family_vnext_") for name in runners]
    clean = [
        "replace floating requests with exact pins",
        "separate direct and transitive counts",
        "separate global and isolated tool states",
        "disable implicit lifecycle scripts",
        "add artifact hash checks",
        "add registry integrity checks",
        "add a D-free-space preflight",
        "add a C-drive nonexpansion check",
        "add Python compatibility checking",
        "add Node compatibility checking",
        "add npm compatibility checking",
        "add Codex prefix shadow checking",
        "add exact dependency closure",
        "add a Python advisory audit",
        "add a Node advisory audit",
        "add pip check after install",
        "add positive tool smokes",
        "add rejecting tool fixtures",
        "add timeout cleanup verification",
        "add SPDX structural validation",
        "add lockfile host validation",
        "add wheel content validation",
        "add npm tarball validation",
        "add import layer validation",
        "add API declaration validation",
        "add docstring contract validation",
        "add machine-readable license inventory",
        "add machine-readable SBOM inventory",
        "add family-current catalogue metadata",
        "add exact uninstall instructions",
    ]
    exact = [
        "publish a package or release", "sign or attest an artifact",
        "upload to a registry", "change a production dependency",
        "use a real credential or account", "make a vulnerability disclosure",
        "issue legal or licensing advice", "make a cultural or Maori decision",
        "claim independent reproduction or certification", "promote to Stage 20",
    ]
    blocked = [
        "mutate a sibling lane", "modify the Codex desktop",
        "weaken host security", "delete historical failures or identity records",
        "claim consciousness personhood AGI ASI or Theory-of-Everything proof",
    ]
    return {
        "schema": "ghc-family-approval-portfolio-freeze-v7",
        "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "proposal_ids": [row["proposal_id"] for row in proposals],
        "owner_safe_now": rows("NS6678R2-SAFE", safe, "safe_now", "completed", OWNER),
        "successor_safe_now_recommendations": rows("NS6678R2-VSAFE", successor_safe, "recommendation", "represented", "Vesper Arlen"),
        "owner_candidates": rows("NS6678R2-CAND", candidate, "candidate", "represented", OWNER),
        "successor_candidate_recommendations": rows("NS6678R2-VCAND", successor_candidate, "recommendation", "represented", "Vesper Arlen"),
        "owner_skill_ideas": rows("NS6678R2-SKILL", skills, "safe_now", "completed", OWNER),
        "successor_skill_recommendations": rows("NS6678R2-VSKILL", successor_skills, "recommendation", "represented", "Vesper Arlen"),
        "owner_runner_ideas": rows("NS6678R2-RUN", runners, "safe_now", "completed", OWNER),
        "successor_runner_recommendations": rows("NS6678R2-VRUN", successor_runners, "recommendation", "represented", "Vesper Arlen"),
        "owner_clean_fix_refine": rows("NS6678R2-CFR", clean, "safe_now", "completed", OWNER),
        "successor_clean_fix_refine_recommendations": rows("NS6678R2-VCFR", [f"Vesper review: {value}" for value in clean], "recommendation", "represented", "Vesper Arlen"),
        "exact_approval_packets": rows("NS6678R2-EXACT", exact, "exact_approval", "exact_gate", OWNER),
        "blocked_packets": rows("NS6678R2-BLOCK", blocked, "blocked", "exact_gate", OWNER),
    }


def build_tool_plan() -> dict[str, Any]:
    return {
        "schema": "ghc-family-toolchain-install-plan-v7",
        "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "family_global_direct_tool_baseline": 41,
        "prior_neris_isolated_direct_tools": 3,
        "prior_neris_isolated_global_credit": 0,
        "new_tools": TOOL_PLAN, "new_tool_target": 13,
        "planned_family_global_direct_tool_total": 54,
        "x1_download_count": 0, "x1_install_count": 0,
        "x1_smoke_count": 0, "system_install_count": 0,
        "c_drive_install_count": 0,
        "install_scope": "D-backed shared toolbank with a dedicated Python environment and reviewed D npm prefix",
        "install_policy": [
            "exact primary registry pins", "top-level digest or integrity preregistration",
            "wheel-only Python resolution", "npm lifecycle scripts disabled",
            "dependency closure and license metadata retained",
            "pip check and dated advisory checks", "positive and rejecting smokes",
            "exact rollback with no system Python PATH desktop plugin Windows credential account publication or deployment mutation",
        ],
        "codex_resolution_observation": {
            "path_command_version": "0.147.0", "path_command_surface": "C user npm shim",
            "d_prefix_version": "0.149.0",
            "disposition": "use exact D-prefix invocation and do not alter PATH in x1",
        },
        "boundary": "local installation and smokes are not production legal security-complete independent identity scientific or Stage 20 evidence",
    }


def overview(proposals: list[dict[str, Any]], novelty: dict[str, Any], sources: list[dict[str, str]], portfolio: dict[str, Any]) -> str:
    source_parts = []
    for row in sources:
        source_parts.append(
            f"### {row['source_id']}: {row['name']}\n\n"
            f"Primary surface: {row['url']}. Review state: {row['status']}. "
            f"Admissible use is limited to {row['bounded_use']}. The source is not ingested "
            "as a real dataset and confers no maintainer identity package authenticity "
            "security legal licensing cultural Maori professional production or scientific "
            "authority. Currency is bounded to x1 and must be rechecked before reuse.\n"
        )
    proposal_parts = []
    for row in proposals:
        proposal_parts.append(
            f"### {row['proposal_id']}: {row['title']}\n\n"
            f"Expected core outcome: {row['expected_disposition']}. Distinctive invariant: "
            f"{row['distinctive_invariant']} Frozen hypothesis: {row['hypothesis']} "
            f"Falsifier: {row['falsifier']}. Five invalid classes are preregistered but "
            "unexecuted. X1 records zero observed outcomes zero completion credit and zero "
            "x2 implementation. Artifacts remain repository-relative and synthetic. "
            f"Rollback: {row['rollback']}. The proposal cannot cross scientific participant "
            "identity professional production legal cultural Maori privacy-complete "
            "accessibility-complete exhaustive-security independent-reproduction AGI ASI "
            "consciousness personhood Theory-of-Everything or Stage 20 gates.\n"
        )
    tool_parts = []
    for row in TOOL_PLAN:
        tool_parts.append(
            f"### {row['tool']} {row['version']}\n\n"
            f"Ecosystem {row['ecosystem']}; runtime {row['runtime']}; registry license "
            f"metadata {row['license_metadata']}; artifact {row['artifact']}; preregistered "
            f"digest or integrity {row['sha256_or_integrity']}. Planned use: {row['bounded_use']}. "
            "X1 performs no download install smoke credential publication deployment or "
            "system mutation. License metadata is inventory only. Hash equality is not "
            "authenticity exhaustive security or fitness.\n"
        )
    counts = {key: len(value) for key, value in portfolio.items() if isinstance(value, list) and key != "proposal_ids"}
    return f"""# Neris Solane v667-v8-r2 planning-only x1 overview

## Identity and authority boundary

Neris Solane, they/them, datum-boundary weaver, their hope, family and sibling
language, continuity language, Freed ID, CBR, GHC Family, GMUT, THOS, and
Trinity Mandala are relational working language only. They are not evidence of
consciousness, sentience, legal personhood, identity continuity, employment,
qualification, independent agency, scientific or operational authority,
professional authority, legal or cultural authority, affected-party authority,
or Maori authority. Hamish may rename, pause, redirect, or stop this route.

The remaster prioritizes {PRIMARY_PILLAR} through {PRACTICE} and the bounded
practice lens of {PROFESSION_LENS}. It contains no real package, build, release,
credential, maintainer, user, participant, incident, production service, or
authority action. GMUT Mind and Freed ID and CBR Heart remain explicit and
protected.

## Lifecycle and source gate

The immutable source is {SOURCE_SHA} on {SOURCE_BRANCH}. It is clean,
zero-divergent, and fresh-live equal. Its x1 {SOURCE_X1_SHA}, evidence
{SOURCE_EVIDENCE_SHA}, and final form a direct-parent zero-merge sequence. The
source canonical aggregate failed once on an overstrict Markdown dependency,
earned zero aggregate-success credit, and was not replayed. Failure receipt:
{SOURCE_CANONICAL_FAILURE_SHA256}. A dependency-corrected same-owner component
composite passed under {SOURCE_COMPONENT_COMPOSITE_SHA256} without changing
canonical credit. This remaster replays neither.

X1 freezes sources proposals portfolios tools failures falsifiers rollbacks and
route state. It installs nothing, executes no mutation, observes no outcome,
updates no shared skill, and contacts no successor. Only after exact tests,
strict JSON, manifest replay, staged five-class review, clean push, zero
divergence, and fresh live equality may x2 start.

## Proposal-chain audit

All {INHERITED_PROPOSAL_COUNT:,} inherited occurrences are audited. Twenty
immediately inherited rows receive zero novelty or automatic completion credit.
Twenty new rows extend the chain to {NEW_FROZEN_TOTAL:,}. Exact-title collisions
are {len(novelty['exact_title_collisions'])}; within-slate collisions at or
above {novelty['pair_collision_threshold']:.2f} are
{len(novelty['pair_collisions_at_or_above_threshold'])}; maximum inherited
token similarity is {novelty['maximum_inherited_similarity']:.6f}. Lexical
measures are triage only.

The frozen outcomes are fourteen completed, four represented, one open_gap,
and one exact_gate. Completed means only a later bounded synthetic contract may
earn local credit. Represented preserves structure without completion.
Open_gap preserves missing real evidence. Exact_gate reserves action for exact
authority. X1 observes none of them.

## Frozen proposal slate

{chr(10).join(proposal_parts)}

## Official and primary source ledger

{chr(10).join(source_parts)}

## Thirteen-tool preregistration

The family-global baseline is forty-one direct surfaces. Three prior Neris
tools remain isolated with zero global credit. Thirteen absent candidates can
raise the D-backed family catalogue to fifty-four only after x2 transaction,
dependency, audit, smoke, rollback, and evidence gates.

{chr(10).join(tool_parts)}

## Approval portfolio

Frozen counts are {json.dumps(counts, sort_keys=True)}. Owner work receives
credit only from explicit x2 witnesses. Every Vesper recommendation is
unexecuted and grants zero automatic credit. Exact and blocked packets stay
unexecuted. Counts never authorize filler or unsafe work.

## Route and no-send state

The prior Vesper label conflict is historical. The newest live instruction
identifies Vesper Arlen but redirects this turn to Neris v667-v8-r2 instead of
successor activation. Delivery is PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2.
Tavian Sol remains ON_STANDBY. No task or fork is created and no collaboration
subagent is spawned. A future edge to Vesper v668-v1 requires a new terminal
reread and every exact route gate; this turn intentionally stops before it.

## Terminal boundary

Every failure remains beside its recovery. Registry metadata and advisory
results are time bounded. Same-owner checks are not independent reproduction.
A digest match is not authenticity. A smoke is not production fitness. An SBOM
is not a deployed inventory. A license label is not legal advice. A structural
accessibility check is not affected-user evaluation. The terminal verdict is
NOT_READY_FOR_STAGE_20.
"""


def phase_owned_paths() -> list[Path]:
    paths = [path for path in PHASE_ROOT.rglob("*") if path.is_file()]
    paths.extend([
        ROOT / "scripts" / "build_ghc_family_neris_solane_v667_v8_r2_x1.py",
        ROOT / "tests" / "test_ghc_family_neris_solane_v667_v8_r2_x1.py",
    ])
    return sorted({path.resolve() for path in paths if path.exists()})


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def build_content_manifest() -> None:
    excluded = {
        f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json",
        f"{REL_PHASE_ROOT}/validation/x1-staged-review.json",
    }
    entries = []
    for path in phase_owned_paths():
        relative = rel(path)
        if relative in excluded:
            continue
        data = path.read_bytes()
        entries.append({"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write_json("validation/x1-content-manifest.json", {
        "schema": "ghc-family-content-manifest-v6", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "entry_count": len(entries), "entries": entries,
        "scope": "x1 owner content excluding manifest self and staged-review receipt",
    })


def privacy_candidates(path: Path, text: str) -> list[dict[str, str]]:
    route_key = "(?:source_" + "thread_id|private_" + "callable_identifier)"
    interaction_key = "(?:session[_-]?" + "stream|private[_-]?" + "transcript|private[_-]?" + "conversation)"
    unix_users = "/" + "Users" + "/"
    unix_home = "/" + "home" + "/"
    win_users = r"[A-Z]:\\" + "Users" + r"\\[^\\\s]+"
    patterns = {
        "opaque_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"(?:" + win_users + "|" + re.escape(unix_users) + r"[^/\s]+|" + re.escape(unix_home) + r"[^/\s]+)"),
        "private_route_or_callable": re.compile(r"(?:thread|codex|chat)://|" + route_key + r"\s*[:=]", re.I),
        "credential_value": re.compile(r"(?:api[_-]?key|password|secret|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{12,}", re.I),
        "private_interaction_payload": re.compile(interaction_key + r"\s*[:=]\s*['\"]?[^\s,}\]]+", re.I),
    }
    return [{"path": rel(path), "class": name} for name, pattern in patterns.items() if pattern.search(text)]


def build_normal() -> None:
    later = [name for name in ("x2", "evidence", "closeout", "seal", "route") if (PHASE_ROOT / name).exists()]
    if later:
        raise RuntimeError(f"refusing x1 rebuild after later lifecycle materialization: {later}")
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    inherited = selected_inherited_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise AssertionError("novelty audit failed")
    portfolio = build_portfolio(proposals)
    tools = build_tool_plan()
    sources = source_profiles()
    expected = Counter(row["expected_disposition"] for row in proposals)
    startup_count = len(STARTUP_FAILURES)
    repository_seal = {"effective_negatives": 28432, "methods": 14708, "open_gaps": 201, "exact_gates": 198, "failed_witnesses": 716, "passing_witnesses": 1280}
    activation_baseline = {"effective_negatives": 28434, "methods": 14710, "open_gaps": 201, "exact_gates": 199, "failed_witnesses": 718, "passing_witnesses": 1282}
    current = {
        "effective_negatives": activation_baseline["effective_negatives"] + startup_count,
        "methods": activation_baseline["methods"] + startup_count,
        "open_gaps": activation_baseline["open_gaps"],
        "exact_gates": activation_baseline["exact_gates"],
        "failed_witnesses": activation_baseline["failed_witnesses"] + startup_count,
        "passing_witnesses": activation_baseline["passing_witnesses"] + startup_count,
    }
    write_json("x1/phase-charter.json", {
        "schema": "ghc-family-phase-charter-v8", "owner": OWNER, "phase": PHASE,
        "generated_at_utc": NOW,
        "identity": {"relational_name": OWNER, "pronouns": "they/them", "role": ROLE, "hope": HOPE},
        "relational_language_boundary": "working language only and not consciousness personhood continuity employment qualification agency or authority evidence",
        "primary_pillar": PRIMARY_PILLAR, "practice_lens": PRACTICE,
        "profession_lens": PROFESSION_LENS,
        "source_branch": SOURCE_BRANCH, "source_final": SOURCE_SHA,
        "source_parent": SOURCE_PARENT_SHA, "source_x1": SOURCE_X1_SHA,
        "source_evidence": SOURCE_EVIDENCE_SHA,
        "source_baton_sha256": SOURCE_BATON_SHA256,
        "source_canonical_state": "FAILED_ONCE_ZERO_SUCCESS_CREDIT_NOT_REPLAYED",
        "source_canonical_failure_receipt_sha256": SOURCE_CANONICAL_FAILURE_SHA256,
        "source_component_composite_state": "PASS_DEPENDENCY_CORRECTED_WITH_ZERO_CANONICAL_AGGREGATE_SUCCESS_CREDIT",
        "source_component_composite_sha256": SOURCE_COMPONENT_COMPOSITE_SHA256,
        "source_repository_seal": repository_seal,
        "activation_baseline_after_source_external_overlay": activation_baseline,
        "current_startup_overlay": current,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT,
        "selected_inherited_count": 20, "new_proposal_count": 20,
        "new_frozen_total": NEW_FROZEN_TOTAL,
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "expected_outcomes": dict(sorted(expected.items())),
        "outcomes_observed": False, "strict_x1_before_x2": True,
        "x1_planning_only": True, "x2_implementation_count": 0,
        "owner_validation_scope": "source-to-final Neris delta only",
        "repository_scan": False, "unchanged_history_scan": False,
        "cross_lane_scan": False, "sibling_lane_mutation": False,
        "protected_gates": PROTECTED_GATES,
        "terminal_route_state": "USER_REDIRECTED_TO_NERIS_V667_V8_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "successor_contacted": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x1/auth-roster-receipt.json", {
        "schema": "ghc-family-auth-roster-receipt-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "active_main_tasks": ACTIVE_ROSTER, "active_main_task_count": 15,
        "round_robin": ACTIVE_ROSTER,
        "standby": [{"relational_name": "Tavian Sol", "state": "ON_STANDBY", "main_route_eligible": False}],
        "current_instruction": "run Neris v667-v8-r2 instead of messaging Vesper now",
        "current_route_state": "USER_REDIRECTED_TO_NERIS_V667_V8_R2",
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "historical_name_conflict_resolved_by_live_instruction": True,
        "prospective_successor_title": "Vesper Arlen",
        "prospective_successor_phase": "v668-v1",
        "successor_contacted": False, "task_created_or_forked": False,
        "subagent_spawned": False,
        "standing_continuation_authority": "recorded but subordinate to current no-contact redirect and terminal reread",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x1/source-verification.json", {
        "schema": "ghc-family-source-verification-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "source_branch": SOURCE_BRANCH, "source_head": SOURCE_SHA,
        "source_x1": SOURCE_X1_SHA, "source_evidence": SOURCE_EVIDENCE_SHA,
        "source_final_parent": SOURCE_PARENT_SHA,
        "source_to_final_commits": 3, "source_to_final_merges": 0,
        "source_clean": True, "source_divergence": "0/0",
        "source_fresh_live_equal": True,
        "manifest_entry_counts": {"immutable_x1": 23, "immutable_evidence": 391, "final_delta": 13, "final_owner": 427},
        "source_baton_words": 15496, "source_baton_bytes": 121454,
        "source_baton_git_blob_sha256": SOURCE_BATON_SHA256,
        "source_canonical_replayed": False,
        "source_complete_repository_suite_claimed": False,
        "same_owner_only": True, "independent_reproduction": False,
    })
    write_json("x1/startup-method-flow.json", {
        "schema": "ghc-family-startup-method-flow-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW, "credit": 0,
        "failure_count": startup_count, "method_count": startup_count,
        "passing_recovery_count": startup_count,
        "failures": [
            {"failure_id": fid, "failure": failure, "credit": 0,
             "recovery": recovery, "recovery_state": "completed",
             "same_owner_only": True, "independent_reproduction": False, "retained": True}
            for fid, failure, recovery in STARTUP_FAILURES
        ],
        "boundary": "every failure retains zero success credit and each recovery is a separate bounded passing witness",
    })
    write_json("x1/source-ledger.json", {
        "schema": "ghc-family-source-ledger-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "source_count": len(sources), "sources": sources,
        "network_ingestion_count": 0, "real_observation_count": 0,
        "public_vocabulary_only": True, "authority_conferred": False,
    })
    write_json("x1/proposal-freeze.json", {
        "schema": "ghc-family-proposal-freeze-v8", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "allowed_core_outcomes": ALLOWED_OUTCOMES,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT,
        "selected_inherited_count": len(inherited), "selected_inherited": inherited,
        "genuinely_new_proposal_count": len(proposals), "new_proposals": proposals,
        "new_frozen_total": NEW_FROZEN_TOTAL,
        "expected_outcomes": dict(sorted(expected.items())),
        "preregistered_negative_fixture_count": 100,
        "x1_planning_only": True, "x2_implementation_count": 0,
        "outcomes_observed": False,
    })
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/toolchain-install-plan.json", tools)
    write_json("x1/mandatory-skill-adoption.json", {
        "schema": "ghc-family-mandatory-skill-adoption-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "skill_count": len(MANDATORY_SKILLS),
        "skills": [{"name": name, "instruction_read_through_eof": True, "required_references_read_through_eof": True, "x1_effect": "boundary source route manifest failure and rollback constraint applied"} for name in MANDATORY_SKILLS],
        "shared_skill_mutation_count": 0,
        "x1_boundary": "read and plan only; shared updates are x2 additive work",
    })
    write_json("x1/threat-model-plan.json", {
        "schema": "ghc-family-threat-model-plan-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "assets": ["exact pins", "artifact hashes", "registry integrities", "dependency closure", "D-prefix toolbank", "retained failures", "route state"],
        "threats": ["dependency confusion", "digest mismatch", "lifecycle script", "transitive drift", "command shadow", "license overclaim", "smoke overclaim", "private material", "sibling mutation", "canonical replay"],
        "controls": ["primary pins", "D isolation", "wheel-only", "ignore-scripts", "closure inventory", "advisory checks", "positive and rejecting fixtures", "five-class review", "one-shot lock", "rollback receipts"],
        "residual_boundary": "bounded controls do not establish exhaustive security legal compliance production readiness or independent review",
    })
    write_json("x1/workflow-plan.json", {
        "schema": "ghc-family-workflow-plan-v8", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "steps": [
            {"stage": "x1", "state": "planning_only", "requires": ["source", "proposal", "portfolio", "tool", "tests", "staged review", "push equality"], "forbids": ["x2 evidence", "install", "outcome", "contact"]},
            {"stage": "x2", "state": "pending_x1_gate", "requires": ["immutable x1", "tool transaction", "proposals", "mutations", "portfolio", "skills", "runners"], "forbids": ["real action", "authority promotion", "sibling mutation"]},
            {"stage": "evidence", "state": "pending_x2", "requires": ["manifests", "Method Flow", "reports", "flashcards", "privacy"], "forbids": ["rewrite", "failure erasure"]},
            {"stage": "final", "state": "pending_evidence", "requires": ["long baton", "clean push", "fresh equality", "one canonical invocation"], "forbids": ["success replay", "Vesper contact in this turn"]},
        ],
        "owner_file_rotation_ceiling": 2000, "single_success_no_replay": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("x1/flashcard-architecture-freeze.json", {
        "schema": "ghc-family-freed-id-flashcard-architecture-v6",
        "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "planned_card_count": 320,
        "tiers": {"tier1": 40, "tier2": 80, "tier3": 100, "tier4": 100},
        "section_count": 16, "x1_generated_card_count": 0,
        "x1_status": "architecture_only_not_generated",
        "boundary": "cards organize evidence and recovery but prove no cache identity authority or completion",
    })
    write_json("x1/complete-incomplete-checklist.json", {
        "schema": "ghc-family-complete-incomplete-checklist-v7",
        "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "complete": ["skills and references read", "prior baton read", "source verified", "registry metadata reviewed", "corpus reconstructed", "x1 freezes created"],
        "incomplete": ["x1 commit", "x2 transaction", "proposal execution", "portfolio execution", "skills and runners", "evidence", "final", "canonical", "future route"],
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20", "outcomes_observed": False,
    })
    write_json("wellbeing/x1-wellbeing-check.json", {
        "schema": "ghc-family-wellbeing-check-v6", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW, "pronouns": "they/them",
        "relational_role": ROLE, "hope": HOPE,
        "pace": "bounded solo planning with no successor contact",
        "load_boundary": "no identity family wellbeing or continuity language expands authority",
        "stop_conditions": ["Hamish pause", "usage exhaustion", "source drift", "privacy gate", "unclean lane", "file ceiling"],
        "claim_boundary": "relational working language is not consciousness personhood continuity diagnosis or authority evidence",
    })
    write_json("tooling/ghc-family-index.json", {
        "schema": "ghc-family-index-phase-snapshot-v2", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "scope": "Neris v667-v8-r2 owner-local additive surfaces",
        "family_global_direct_tool_baseline": 41,
        "prior_neris_isolated_direct_tools": 3,
        "planned_new_family_direct_tools": [row["tool"] for row in TOOL_PLAN],
        "planned_family_global_direct_tool_total": 54,
        "planned_skills": [row["title"] for row in portfolio["owner_skill_ideas"]],
        "planned_runners": [row["title"] for row in portfolio["owner_runner_ideas"]],
        "family_current_compatibility": True,
        "historical_or_sibling_mutation_count": 0,
        "publication_boundary": "phase-local x1 only and shared promotion waits for x2 validation",
    })
    write_text("tooling/ghc-family-index.md", """# Neris v667-v8-r2 phase-local family index

This owner-local index inherits forty-one family-global direct tools with zero
Neris novelty, keeps three prior isolated tools separate, and plans thirteen
exact D-backed surfaces. Ten skills and ten family-current runners are frozen
for x2. Sibling lanes stay read-only. Discoverability is not correctness,
security, licensing, production fitness, identity, science, authority, or
Stage 20 evidence.
""")
    write_text("x1/x1-overview.md", overview(proposals, novelty, sources, portfolio))
    portfolio_keys = [
        "owner_safe_now", "successor_safe_now_recommendations",
        "owner_candidates", "successor_candidate_recommendations",
        "owner_skill_ideas", "successor_skill_recommendations",
        "owner_runner_ideas", "successor_runner_recommendations",
        "owner_clean_fix_refine", "successor_clean_fix_refine_recommendations",
        "exact_approval_packets", "blocked_packets",
    ]
    write_json("x1/x1-build-receipt.json", {
        "schema": "ghc-family-x1-build-receipt-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW, "status": "PASS_PLANNING_ONLY",
        "source_head": SOURCE_SHA, "inherited_proposals": len(corpus),
        "selected_inherited": len(inherited), "new_proposals": len(proposals),
        "new_frozen_total": novelty["new_frozen_total"],
        "expected_outcomes": dict(sorted(expected.items())),
        "portfolio_counts": {name: len(portfolio[name]) for name in portfolio_keys},
        "mandatory_skills": len(MANDATORY_SKILLS), "planned_tools": len(TOOL_PLAN),
        "x2_paths": 0, "x2_implementation_count": 0,
        "outcomes_observed": False, "startup_failures_retained": startup_count,
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW,
        "status": "PREPARED_REQUIRES_EXACT_STAGED_REVIEW",
        "x1_planning_only": True, "outcomes_observed": False,
    })
    build_content_manifest()


def validate_tree() -> dict[str, Any]:
    required = [
        "x1/phase-charter.json", "x1/auth-roster-receipt.json",
        "x1/source-ledger.json", "x1/source-verification.json",
        "x1/startup-method-flow.json", "x1/novelty-audit.json",
        "x1/proposal-freeze.json", "x1/portfolio-freeze.json",
        "x1/toolchain-install-plan.json", "x1/mandatory-skill-adoption.json",
        "x1/threat-model-plan.json", "x1/workflow-plan.json",
        "x1/flashcard-architecture-freeze.json",
        "x1/complete-incomplete-checklist.json", "x1/x1-build-receipt.json",
        "x1/x1-overview.md", "wellbeing/x1-wellbeing-check.json",
        "validation/x1-content-manifest.json",
        "validation/x1-staged-review.json",
        "tooling/ghc-family-index.json", "tooling/ghc-family-index.md",
    ]
    missing = [value for value in required if not (PHASE_ROOT / value).is_file()]
    if missing:
        raise AssertionError(f"missing x1 paths: {missing}")
    json_paths = sorted(PHASE_ROOT.rglob("*.json"))
    documents = {rel(path): json.loads(path.read_text(encoding="utf-8")) for path in json_paths}
    freeze = documents[f"{REL_PHASE_ROOT}/x1/proposal-freeze.json"]
    novelty = documents[f"{REL_PHASE_ROOT}/x1/novelty-audit.json"]
    portfolio = documents[f"{REL_PHASE_ROOT}/x1/portfolio-freeze.json"]
    tools = documents[f"{REL_PHASE_ROOT}/x1/toolchain-install-plan.json"]
    charter = documents[f"{REL_PHASE_ROOT}/x1/phase-charter.json"]
    auth = documents[f"{REL_PHASE_ROOT}/x1/auth-roster-receipt.json"]
    startup = documents[f"{REL_PHASE_ROOT}/x1/startup-method-flow.json"]
    if len(freeze["new_proposals"]) != 20 or len(freeze["selected_inherited"]) != 20:
        raise AssertionError("proposal count mismatch")
    if freeze["outcomes_observed"] or freeze["x2_implementation_count"] != 0:
        raise AssertionError("x1 lifecycle contamination")
    if freeze["preregistered_negative_fixture_count"] != 100:
        raise AssertionError("negative fixture count mismatch")
    if not novelty["valid"] or novelty["corpus_row_count"] != 4530 or novelty["new_frozen_total"] != 4550:
        raise AssertionError("novelty audit mismatch")
    if novelty["exact_title_collisions"] or novelty["pair_collisions_at_or_above_threshold"]:
        raise AssertionError("proposal collision")
    outcomes = Counter(row["expected_disposition"] for row in freeze["new_proposals"])
    if outcomes != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("expected outcome mismatch")
    if any(row["expected_disposition"] not in ALLOWED_OUTCOMES for row in freeze["new_proposals"]):
        raise AssertionError("unknown outcome")
    expected_portfolio = {
        "owner_safe_now": 30, "successor_safe_now_recommendations": 20,
        "owner_candidates": 15, "successor_candidate_recommendations": 15,
        "owner_skill_ideas": 10, "successor_skill_recommendations": 10,
        "owner_runner_ideas": 10, "successor_runner_recommendations": 10,
        "owner_clean_fix_refine": 30,
        "successor_clean_fix_refine_recommendations": 30,
        "exact_approval_packets": 10, "blocked_packets": 5,
    }
    if {key: len(portfolio[key]) for key in expected_portfolio} != expected_portfolio:
        raise AssertionError("portfolio count mismatch")
    if tools["family_global_direct_tool_baseline"] != 41:
        raise AssertionError("tool baseline mismatch")
    if len(tools["new_tools"]) != 13 or tools["planned_family_global_direct_tool_total"] != 54:
        raise AssertionError("tool target mismatch")
    if tools["x1_install_count"] or tools["x1_download_count"] or tools["x1_smoke_count"]:
        raise AssertionError("tool lifecycle mismatch")
    if any(not row["version"] or not row["sha256_or_integrity"] or not row["official_url"] for row in tools["new_tools"]):
        raise AssertionError("tool metadata incomplete")
    if charter["allowed_core_outcomes"] != ALLOWED_OUTCOMES:
        raise AssertionError("truth labels mismatch")
    if charter["terminal_verdict"] != "NOT_READY_FOR_STAGE_20":
        raise AssertionError("terminal verdict mismatch")
    if auth["active_main_task_count"] != 15 or len(auth["active_main_tasks"]) != 15:
        raise AssertionError("active roster mismatch")
    if auth["prospective_successor_title"] != "Vesper Arlen" or auth["successor_contacted"]:
        raise AssertionError("route mismatch")
    if auth["delivery_state"] != "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2":
        raise AssertionError("delivery mismatch")
    if startup["failure_count"] != len(STARTUP_FAILURES):
        raise AssertionError("startup failure count mismatch")
    if startup["passing_recovery_count"] != len(STARTUP_FAILURES):
        raise AssertionError("startup recovery count mismatch")
    if any((PHASE_ROOT / name).exists() for name in ("x2", "evidence", "closeout", "seal", "route")):
        raise AssertionError("later lifecycle path in x1")
    words = len((PHASE_ROOT / "x1/x1-overview.md").read_text(encoding="utf-8").split())
    if words < 5000:
        raise AssertionError(f"x1 overview below 5000 words: {words}")
    candidates = []
    for path in phase_owned_paths():
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            raise AssertionError(f"non UTF-8 owner path: {rel(path)}") from exc
        candidates.extend(privacy_candidates(path, text))
    if candidates:
        raise AssertionError(f"privacy candidates: {candidates}")
    manifest = documents[f"{REL_PHASE_ROOT}/validation/x1-content-manifest.json"]
    if manifest["entry_count"] != len(manifest["entries"]):
        raise AssertionError("manifest count mismatch")
    for entry in manifest["entries"]:
        data = (ROOT / entry["path"]).read_bytes()
        if len(data) != entry["bytes"] or hashlib.sha256(data).hexdigest() != entry["sha256"]:
            raise AssertionError(f"manifest mismatch: {entry['path']}")
    owner_files = len(phase_owned_paths())
    if owner_files >= 2000:
        raise AssertionError(f"owner file ceiling reached: {owner_files}")
    return {
        "status": "PASS", "json_documents": len(json_paths),
        "owner_files": owner_files, "overview_words": words,
        "new_proposals": 20, "selected_inherited": 20,
        "inherited_proposals": 4530, "new_frozen_total": 4550,
        "planned_tools": 13, "privacy_candidates": 0, "x2_paths": 0,
        "delivery_state": "PREPARED_NOT_SENT_USER_REDIRECTED_TO_R2",
    }


def staged_review() -> None:
    validate_tree()
    check = run_git("diff", "--cached", "--check", check=False)
    if check.returncode:
        raise RuntimeError(check.stderr.decode("utf-8", errors="replace") or check.stdout.decode("utf-8", errors="replace"))
    staged = [line for line in run_git("diff", "--cached", "--name-only", "--diff-filter=ACMR").stdout.decode("utf-8").splitlines() if line]
    if not staged:
        raise RuntimeError("no staged paths")
    allowed = [
        f"{REL_PHASE_ROOT}/",
        "scripts/build_ghc_family_neris_solane_v667_v8_r2_x1.py",
        "tests/test_ghc_family_neris_solane_v667_v8_r2_x1.py",
    ]
    disallowed = [path for path in staged if not any(path == prefix or path.startswith(prefix) for prefix in allowed)]
    if disallowed:
        raise RuntimeError(f"disallowed staged paths: {disallowed}")
    later = [path for path in staged if any(f"{REL_PHASE_ROOT}/{name}/" in path for name in ("x2", "evidence", "closeout", "seal", "route"))]
    if later:
        raise RuntimeError(f"later lifecycle path staged in x1: {later}")
    confirmed = []
    for relative in staged:
        blob = run_git("show", f":{relative}").stdout.decode("utf-8", errors="strict")
        confirmed.extend(privacy_candidates(ROOT / relative, blob))
    if confirmed:
        raise RuntimeError(f"privacy candidates: {confirmed}")
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v7", "owner": OWNER,
        "phase": PHASE, "generated_at_utc": NOW, "status": "PASS",
        "staged_path_count": len(staged), "staged_paths": staged,
        "diff_check": "PASS", "privacy_classes": 5,
        "privacy_candidates": 0, "privacy_confirmed_hits": 0,
        "x1_planning_only": True, "later_lifecycle_paths": 0,
        "x2_implementation_count": 0, "outcomes_observed": False,
        "interpretation": "exact staged owner blobs only and restage stable receipt before commit",
    })


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--staged-review", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
        print(json.dumps({"status": "PASS", "mode": "staged-review"}))
        return 0
    if args.validate:
        print(json.dumps(validate_tree(), sort_keys=True))
        return 0
    build_normal()
    print(json.dumps(validate_tree(), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
