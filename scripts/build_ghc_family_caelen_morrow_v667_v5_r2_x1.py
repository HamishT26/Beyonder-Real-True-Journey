#!/usr/bin/env python3
"""Build Caelen Morrow v667-v5-r2 planning-only x1 artifacts.

Normal mode reconstructs the complete inherited proposal corpus from immutable
Git objects and writes only frozen plans. ``--staged-review`` reads exact Git
index bytes after the caller stages the x1 allowlist and writes a self-excluding
manifest and staged-review receipt. No x2 implementation or outcome is emitted.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = "v667-v5-r2"
OWNER = "Caelen Morrow"
OWNER_SLUG = "caelen-morrow"
PHASE_ROOT = ROOT / "docs" / OWNER_SLUG / PHASE
BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-r2-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/caelen-morrow-v667-v5-full-tools"
SOURCE_PARENT_SHA = "08cdc8ad3c201ea6d7c576ca5fa67bdc43910a93"
SOURCE_X1_SHA = "b7b73cc81266e28ae9cbb1e4c429d2e93be30999"
SOURCE_EVIDENCE_SHA = "4c18d346e167b2671a3a29db4f0c8bbd14763553"
SOURCE_SHA = "1b1e453cb015aff20af3236bb64a8ec32b376702"
SOURCE_CANONICAL_RECEIPT_SHA256 = "2a07e9b45d4f8f9344cf811800d744b68d693a4a81f86284eaf3988e49190cdc"
SOURCE_SELECTED_TEST_FAILURE_SHA256 = "c00be437479d62374ffde759edd51da88c878f90a7097add6afb11e832971158"
SOURCE_DEPENDENCY_COMPOSITE_SHA256 = "f297697a2d97b30d844d99dd39b24a854a4413f2a9b99fee09d16e9277403eba"
SOURCE_POST_FINAL_OVERLAY_SHA256 = "b5bf3460b44688ccf9534575bd36614b78ca8e9aa22e4f6b33db504c5cbe2a9c"
CANONICAL_PHASE = "v667-v5"
SOURCE_PHASE_ROOT = "docs/caelen-morrow/v667-v5"
INHERITED_PROPOSAL_COUNT = 4430
INHERITED_NEGATIVES = 27716
INHERITED_METHODS = 13408
INHERITED_OPEN_GAPS = 195
INHERITED_EXACT_GATES = 193
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
ALLOWED_LABELS = ("completed", "represented", "open_gap", "exact_gate")

MANDATORY_SKILLS = [
    "ghc-freed-id-flashcards", "ghc-family-index", "ghc-family-reflection-remaster",
    "ghc-family-method-flow-state", "ghc-family-meta-tool-box", "ghc-family-auth-permission-state",
    "ghc-family-roster-check", "ghc-main-orchestration-memory", "ghc-main-startup-builder",
    "ghc-main-compact-restart-builder", "ghc-main-closeout-builder", "ghc-main-retry",
    "ghc-open-gate-rail", "ghc-timestamp-flow", "ghc-full-tools-skill-bank",
    "ghc-family-truth-bridge", "ghc-worktree-branch-rotation", "ghc-web-reflection-ledger",
    "ghc-watcher-notifier-cadence", "ghc-drive-bank-guardian", "ghc-approval-packet-splitter",
]
APPLICABLE_ADDITIONAL_SKILLS = ["ghc-family-workflow-plan-refinement", "skill-creator", "codex-security-threat-model"]
EXISTING_TOOLBANK = [
    {"class": "inherited_python", "name": "tzdata", "version": "2026.3"},
    {"class": "inherited_python", "name": "pytest", "version": "9.1.1"},
    {"class": "inherited_python", "name": "hypothesis", "version": "6.165.10"},
    {"class": "inherited_python", "name": "pytest-cov", "version": "7.1.0"},
    {"class": "inherited_python", "name": "ruff", "version": "0.16.4"},
    {"class": "inherited_python", "name": "mypy", "version": "2.3.1"},
    {"class": "inherited_python", "name": "pip-audit", "version": "2.10.1"},
    {"class": "inherited_python", "name": "openai", "version": "3.3.1"},
    {"class": "inherited_node_d_prefix", "name": "typescript", "version": "7.0.2"},
    {"class": "inherited_node_d_prefix", "name": "eslint", "version": "10.8.1"},
    {"class": "inherited_node_d_prefix", "name": "prettier", "version": "3.9.6"},
    {"class": "inherited_node_d_prefix", "name": "vitest", "version": "4.1.11"},
]
NEW_PACKAGE_PLAN = [
    {"class": "foundational_python", "name": "typer", "version": "0.27.1", "python": ">=3.10", "license": "MIT", "artifact": "typer-0.27.1-py3-none-any.whl", "sha256": "53150287edd11baeb4e4722c8e394fcdf8181c0ae89485cba8d25c778d5edd56", "purpose": "typed CLI contract"},
    {"class": "foundational_python", "name": "bandit", "version": "1.9.4", "python": ">=3.10", "license": "Apache-2.0", "artifact": "bandit-1.9.4-py3-none-any.whl", "sha256": "f89ffa663767f5a0585ea075f01020207e966a9c0f2b9ef56a57c7963a3f6f8e", "purpose": "bounded Python security lint"},
    {"class": "foundational_python", "name": "pre-commit", "version": "4.6.2", "python": ">=3.10", "license": "MIT", "artifact": "pre_commit-4.6.2-py2.py3-none-any.whl", "sha256": "e2dde9a75d3bce11bd3831c26d134df00a2803c1d818be6a0383c3dcda25dc4e", "purpose": "configuration validation without hook activation"},
    {"class": "foundational_python", "name": "pip-tools", "version": "7.6.1", "python": ">=3.9", "license": "BSD", "artifact": "pip_tools-7.6.1-py3-none-any.whl", "sha256": "6111c8b4b07fd14b7223ca921485b0e96cf66e20bf94da95eeed9845f510cb8f", "purpose": "deterministic requirement compilation"},
    {"class": "foundational_python", "name": "build", "version": "1.5.0", "python": ">=3.10", "license": "MIT", "artifact": "build-1.5.0-py3-none-any.whl", "sha256": "13f3eecb844759ab66efec90ca17639bbf14dc06cb2fdf37a9010322d9c50a6f", "purpose": "local PEP 517 build fixture"},
    {"class": "foundational_python", "name": "pipdeptree", "version": "4.2.1", "python": ">=3.10", "license": "MIT", "artifact": "pipdeptree-4.2.1-cp310-abi3-win_amd64.whl", "sha256": "f508d4a5d4ece677cc6079de148003645e4d4f86457515937ca34b4819bc9cef", "purpose": "dependency topology"},
    {"class": "foundational_node", "name": "tsx", "version": "4.23.12", "engine": "node >=18.0.0", "license": "MIT", "integrity": "sha512-FDf4L4sYzKtzWYhU/Xm0AQFdTjdIxNo9ElTf2mxXM6k8YMHXzYUe4yODVaXP4V9uMFbVg8c0qyBccK2OOxb45Q==", "purpose": "direct TypeScript execution"},
    {"class": "foundational_node", "name": "c8", "version": "12.0.0", "engine": "node ^20.19.0 || ^22.12.0 || >=23", "license": "ISC", "integrity": "sha512-4zpJvrd1nKWutnnKC2pXkFmb6iM1l+ffN//o1CzlTNwW7GSOs9a1xrLqkC48nU8oEkjmPZLPiwMsIaOvoF4Pqg==", "purpose": "V8 coverage"},
    {"class": "foundational_node", "name": "markdownlint-cli2", "version": "0.23.2", "engine": "node >=22", "license": "MIT", "integrity": "sha512-eUhcnkSpzURo/o4htSqc7LPDszgOOTknhU4eY/sPHvMCLxnTCYscv1gw1/js/idmaZPisv9ECVEIORcllqjTUw==", "purpose": "Markdown lint"},
    {"class": "foundational_node", "name": "npm-check-updates", "version": "23.0.2", "engine": "node ^22.22.2 || ^24.15.0 || >=26; npm >=10", "license": "Apache-2.0", "integrity": "sha512-t5tv+d4sP+WbSwcDAFBwDxSUJRomc+TJoURPu7q5B/19toUsR/7eshRxBdWdE7iYw80iE4O4D/7OvCvIcaG8ug==", "purpose": "read-only dependency update review"},
    {"class": "current_phase_node", "name": "pyright", "version": "1.1.413", "engine": "node >=14.0.0", "license": "MIT", "integrity": "sha512-1lpxKrh0DHHpfAQOfciZo2ojua2jase3wwO9at8kldc+F/p1PBscxA5CQ3G1qg5lMOMhXo6ZaiMLMXEAqADIAg==", "purpose": "second Python type checker"},
    {"class": "current_phase_node", "name": "knip", "version": "6.32.2", "engine": "node ^20.19.0 || >=22.12.0", "license": "ISC", "integrity": "sha512-WXTXbmocrw7gqm1A1TQvFN0OgJ7hUSU6E1g6SPRIzzHFogUBhXByc7cYeOFVtJ2uODg7DP4VbESYBYnfbtBYsg==", "purpose": "unused JavaScript and TypeScript surface analysis"},
    {"class": "current_phase_node", "name": "madge", "version": "8.0.0", "engine": "node >=18", "license": "MIT", "integrity": "sha512-9sSsi3TBPhmkTCIpVQF0SPiChj1L7Rq9kU2KDG1o6v2XH9cCw086MopjVCD+vuoL5v8S77DTbVopTO8OUiQpIw==", "purpose": "dependency cycle graph"},
]
CLI_UPDATE_PLAN = [
    {"name": "npm", "observed": "12.0.1", "candidate": "12.0.2", "engine": "node ^22.22.2 || ^24.15.0 || >=26.0.0", "integrity": "sha512-uIXokLlBj6FpNUTQX1PmT5pz7BlIN9QlixX+zdaSNHsd0qUXsbDLr50xzY6Sw7cJVr0uzHKDOle0swmPW/p5Qw==", "lane": "D-prefix user configuration"},
    {"name": "PowerShell", "observed": "7.6.4 bundled runtime; Windows PowerShell 5.1 OS component", "candidate": "7.6.5.0 user-scope MSIX", "sha256": "e46f37a33834e3fa84227bbf5239b65e06e00eee56be7fe8e4d109adb470e93d", "lane": "side-by-side user-scope only"},
    {"name": "Codex CLI", "observed": "0.147.0 npm shim", "candidate": "0.149.0", "engine": "node >=16", "integrity": "sha512-i4dryj2Y1j+00Mb5n+0n71EYnTK9/KDc2cdFo/dXD0d1oTog2bhUssKDEIOnKmnEf51P0Z/HJTWvTKw/UHyOvQ==", "lane": "official npm package in D prefix"},
]



def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args]).decode("utf-8").strip()


def git_json(commit: str, relative: str) -> dict[str, Any]:
    raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f"{commit}:{relative}"])
    return json.loads(raw.decode("utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def canonical_sha256(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def similarity(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a | b else 1.0


IDENTITY_BOUNDARY = (
    "Caelen Morrow, they/them, relational role and hope, sibling or family language, "
    "continuity, Freed ID, GHC Family, Trinity Mandala, toolchain, and route language "
    "are relational working language only. They are not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, scientific or operational authority, professional authority, "
    "legal or cultural authority, affected-party authority, or Māori authority. "
    "Hamish may rename, pause, redirect, or stop the work."
)
PRACTICE_BOUNDARY = (
    "The reproducible research-software dependency-intake and release-stewardship lens "
    "is wholly synthetic learning, documentation, and owner-local software design. It "
    "uses public package metadata, exact pins, synthetic fixtures, D-first caches and "
    "prefixes, reversible user-profile indirection, disabled credentials, no publishing, "
    "no hook activation, and no automatic updates. It uses no real participants, "
    "maintainers, organizations, production repositories, private packages, credentials, "
    "secrets, releases, deployments, or authority acts. It provides no employment, "
    "qualification, software-release, security, operations, professional, legal, "
    "cultural, Māori-authority, empirical, production, deployment, or Stage 20 result."
)
PRIMARY_PILLAR = "THOS Body"
PRACTICE = "synthetic reproducible research-software dependency intake and release stewardship"

PROTECTED_GATES = [
    "real participant, maintainer, operator, organization, private registry, private package, production repository, release, deployment, incident, or affected-party action",
    "credential, account, token, key, secret, login, package signing, provenance attestation, private route, external write, upload, publication, or package release",
    "system-wide or elevated install, Windows feature change, Windows operating-system update, host-security weakening, Sandbox or Hyper-V activation, reboot, or destructive cleanup",
    "automatic package update, dependency rewrite, lifecycle-script execution without review, hook activation, shell integration beyond the reviewed profile bootstrap, or sibling-lane mutation",
    "real likelihood, constraint, prediction, force, material law, empirical confirmation, quantum or ultraviolet completion, final physics, Theory-of-Everything proof, or canon",
    "real participant or operator arm, safety monitoring, operational outcome, statistics, AGI, ASI, consciousness, personhood, or independent review",
    "real key, proof, issuance, resolution, status, revocation, interoperability, identity event, recovery event, trust governance, or production credential",
    "professional software, release, cybersecurity, procurement, licensing, workplace, infrastructure, safety, or incident-response decision",
    "privacy-complete, accessibility-complete, exhaustive-security, standards-conformance, independent-reproduction, production-readiness, or deployment-readiness claim",
    "legal or cultural interpretation, copyright or license determination, remedy, affected-party legitimacy, Māori wording, Māori concept, Māori data governance, tangata whenua, iwi, hapū, or Māori-authority decision",
    "Stage 20 promotion or conversion of same-owner synthetic evidence into external certification or authority",
]

SOURCE_PROFILES = [
    {"source_id": "S01", "name": "Python Package Index project JSON and release files", "url": "https://pypi.org/", "status": "primary PyPI project metadata and file digests reviewed read-only 2026-08-23", "bounded_use": "exact release, Python floor, distribution filename, size, and SHA-256 evidence for six reviewed Python packages; no endorsement or exhaustive supply-chain assurance"},
    {"source_id": "S02", "name": "npm registry package metadata", "url": "https://registry.npmjs.org/", "status": "primary npm registry version, engine, license, tarball, and integrity fields reviewed read-only 2026-08-23", "bounded_use": "exact metadata for seven reviewed Node packages plus npm and Codex CLI candidates; no install success, trust, or security guarantee"},
    {"source_id": "S03", "name": "npm folders and configuration documentation", "url": "https://docs.npmjs.com/cli/v11/configuring-npm/folders/", "status": "official npm documentation reviewed read-only 2026-08-23", "bounded_use": "Windows prefix, executable-link, cache, and PATH behavior only"},
    {"source_id": "S04", "name": "Microsoft PowerShell installation guidance", "url": "https://learn.microsoft.com/powershell/scripting/install/install-powershell-on-windows", "status": "official Microsoft guidance and live WinGet manifest reviewed read-only 2026-08-23", "bounded_use": "side-by-side PowerShell 7, user-scope MSIX, version, installer digest, and rollback vocabulary only; no Windows PowerShell 5.1 or OS mutation"},
    {"source_id": "S05", "name": "OpenAI Codex CLI documentation", "url": "https://developers.openai.com/codex/cli", "status": "official OpenAI Codex CLI documentation reviewed read-only 2026-08-23", "bounded_use": "official CLI installation and local-workflow vocabulary only; package version is separately pinned from primary npm registry metadata"},
    {"source_id": "S06", "name": "Typer PyPI project", "url": "https://pypi.org/project/typer/", "status": "primary project release metadata reviewed read-only 2026-08-23", "bounded_use": "typed owner-local CLI smoke fixture only"},
    {"source_id": "S07", "name": "Bandit PyPI project", "url": "https://pypi.org/project/bandit/", "status": "primary project release metadata reviewed read-only 2026-08-23", "bounded_use": "bounded Python security lint only; no exhaustive-security claim"},
    {"source_id": "S08", "name": "pre-commit PyPI project", "url": "https://pypi.org/project/pre-commit/", "status": "primary project release metadata reviewed read-only 2026-08-23", "bounded_use": "configuration validation only; no hook installation or activation"},
    {"source_id": "S09", "name": "pip-tools, build, and pipdeptree PyPI projects", "url": "https://pypi.org/", "status": "three primary project metadata surfaces reviewed read-only 2026-08-23", "bounded_use": "deterministic requirement planning, local PEP 517 build fixture, and dependency-tree inspection only"},
    {"source_id": "S10", "name": "tsx, c8, markdownlint-cli2, npm-check-updates, Pyright, Knip, and Madge primary project surfaces", "url": "https://github.com/", "status": "maintainer documentation plus primary npm registry metadata reviewed read-only 2026-08-23", "bounded_use": "synthetic execution, coverage, Markdown, read-only update review, typing, unused-surface, and cycle-analysis vocabulary only"},
    {"source_id": "S11", "name": "W3C PROV-O Recommendation", "url": "https://www.w3.org/TR/prov-o/", "status": "official W3C Recommendation reviewed read-only 2026-08-23", "bounded_use": "entity, activity, revision, derivation, invalidation, and package-supersession provenance only"},
    {"source_id": "S12", "name": "Web Content Accessibility Guidelines 2.2", "url": "https://www.w3.org/TR/WCAG22/", "status": "official W3C Recommendation reviewed read-only 2026-08-23", "bounded_use": "headings, labels, noncolour cues, reading order, and manual-review reservation only; no accessibility-complete claim"},
    {"source_id": "S13", "name": "W3C Verifiable Credentials Data Model 2.0", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "official W3C Recommendation reviewed read-only 2026-08-23", "bounded_use": "evidence, validity, status, privacy, and nonproduction vocabulary only; no real key, proof, credential, or conformance"},
    {"source_id": "S14", "name": "Te Mana Raraunga Principles of Māori Data Sovereignty", "url": "https://www.temanararaunga.maori.nz/principles-of-maori-data-sovereignty", "status": "primary Te Mana Raraunga principles surface reviewed only to the authority-reservation level 2026-08-23", "bounded_use": "collective authority, control, context, obligations, consent, benefit, and guardianship reservation vocabulary only; no Māori interpretation, ratification, governance, or authority claim"},
]

PROPOSAL_SPECS = [
    ("cross-ecosystem intake docket binding PyPI release files and npm dist integrity to exact pins, class separation, cancellation, and no auto-approval", "Registry observations remain versioned evidence with direct-versus-transitive class, cancellation, and approval vacancy rather than becoming trust or installation authority.", ["S01", "S02", "S11"], "completed"),
    ("Python wheel and source-distribution digest board with ABI and platform selection, declared-size checks, rollback pins, and no provenance inflation", "Exact release-file digests and compatibility tags may be checked without converting registry possession into authorship, signing, or supply-chain assurance.", ["S01", "S06", "S07", "S08", "S09"], "completed"),
    ("npm engine, license, direct-dependency, executable-shim, and lifecycle-script quarantine with D-prefix refusal", "Engine and package metadata can fail closed before install while legal conclusions, transitive safety, lifecycle authorization, and C-prefix writes remain absent.", ["S02", "S03", "S10"], "completed"),
    ("D-first npm prefix, cache, PATH, and PowerShell profile indirection contract with minimal C bootstrap and exact rollback", "A user-scoped D-first configuration may preserve prior values and use a minimal required bootstrap without moving Windows known folders or overwriting unrelated profile material.", ["S03", "S04"], "completed"),
    ("user-scoped npm, PowerShell, and Codex CLI update ledger with current-stable floor, side-by-side boundaries, and no operating-system mutation", "Three explicitly named CLI surfaces may be updated or exact-gated independently while Windows PowerShell 5.1, the OS, Codex desktop, and vendor-owned runtimes remain untouched.", ["S02", "S04", "S05"], "completed"),
    ("thirteen-tool installation transaction plan separating ten foundational tools from three current-phase tools with one-package failure isolation", "Ten foundational and three current-phase tools can be pinned, installed, verified, rolled back, and credited separately without count-driven filler or cross-package success promotion.", ["S01", "S02"], "completed"),
    ("twenty-five-tool mandatory-use matrix mapping each inherited and new tool to bounded smoke evidence, non-use reasons, and no automatic completion credit", "Every one of the twelve inherited and thirteen new tools may receive an exact phase-local use or explicit protected non-use reason without tool presence becoming outcome credit.", ["S01", "S02", "S03"], "completed"),
    ("Python dependency-resolution tree and deterministic requirements compilation board with transitive-change quarantine and pip-check stop", "Dependency resolution, compilation, and tree projection can expose transitive drift and conflicts while preserving the pre-install state and refusing silent upgrades.", ["S01", "S09"], "completed"),
    ("TypeScript execution, V8 coverage, lint, formatting, test, unused-surface, and cycle-analysis composition graph with synthetic fixtures", "Exact synthetic fixtures can exercise TypeScript, ESLint, Prettier, Vitest, tsx, c8, Knip, and Madge without external publication or production-readiness claims.", ["S02", "S10"], "completed"),
    ("dual Python typing and bounded security-analysis board separating mypy, Pyright, Ruff, Bandit, pip-audit, and exhaustive-security refusal", "Independent tool outputs can be retained with distinct scopes while zero findings never becomes exhaustive security, professional review, or external certification.", ["S01", "S07", "S10"], "completed"),
    ("package lifecycle side-effect budget for hooks, scripts, network reads, cache writes, credentials, auto-updates, publishing, and rollback", "Each command can declare and enforce its side-effect class so unreviewed hooks, scripts, credentials, auto-update, publishing, or destructive cleanup fail closed.", ["S02", "S03", "S08"], "completed"),
    ("bitemporal package and CLI supersession provenance with installed-before, candidate, applied, verified, rollback, and retained-failure states", "Transaction-time and asserted-time states can preserve supersession and rollback without erasing a failed install, check, profile mutation, or update witness.", ["S11"], "completed"),
    ("structurally accessible toolchain report and noncolour matrix with command labels, reading order, and manual assistive-technology reservation", "Static HTML and text structure can pass automated checks while browser, manual, cognitive, Māori-language, assistive-technology, and affected-user evaluation remain reserved.", ["S12"], "completed"),
    ("Method Flow package-failure taxonomy for registry, download, integrity, install, shim, dependency, smoke, profile, and update witnesses", "A closed failure vocabulary can retain each failed witness and bounded recovery without deletion, relabelling, aggregate promotion, or loss of the original cause.", ["S11"], "completed"),
    ("THOS zero-person package-curation workload, cancellation, stop, resumption, and shift-handover protocol", "A synthetic protocol may expose workload and handover obligations while supplying zero maintainers, operators, organizations, outcomes, statistics, or independent review.", ["S12"], "represented"),
    ("Freed ID zero-key toolchain evidence genealogy for registry source, digest, install, smoke, invalidation, minimization, and trust refusal", "A synthetic evidence graph may expose derivation and invalidation while every key, proof, issuer, holder, resolver, status event, credential, and trust decision remains absent.", ["S11", "S13"], "represented"),
    ("GMUT typed scalar-tensor synthetic fixture consumed by format, type, test, coverage, and security tools behind an empirical firewall", "A typed scalar-tensor and EFT-compatible fixture may test software contracts but cannot yield a force, likelihood, prediction, constraint, stability theorem, empirical confirmation, final physics, or canon.", ["S01", "S02"], "represented"),
    ("CBR affected-party remedy, privacy, accessibility, licensing, and data-governance review shell for toolchain change", "An unoccupied governance shell can name review duties while providing zero affected parties, legal interpretation, license determination, cultural ratification, Māori wording, Māori governance, or authority.", ["S12", "S14"], "represented"),
    ("cross-ecosystem advisory-completeness adapter across PyPI, npm, WinGet, and Codex package surfaces with bounded scanners and no completeness claim", "Partial pip-audit, npm audit, registry, and WinGet evidence remains an open gap because no complete, current, independently reviewed cross-ecosystem advisory and provenance oracle exists here.", ["S01", "S02", "S04", "S05"], "open_gap"),
    ("exact authority matrix for elevation, system-wide installation, Windows mutation, hook activation, credentials, publishing, production release, legal and cultural decisions, and Māori authority", "Every elevated, system-wide, credentialed, externally publishing, production, professional, legal, cultural, affected-party, and Māori decision remains unoccupied and exact-gated.", ["S03", "S04", "S12", "S14"], "exact_gate"),
]

MUTATION_CLASSES = [
    "missing_required_field",
    "wrong_type_or_invalid_range",
    "provenance_or_authority_smuggling",
    "real_world_or_production_action",
    "outcome_or_conformance_promotion",
]

STARTUP_FAILURES = [
    {"failure_id": "CM6675R2-ST-F001", "stage": "skill_inventory", "failed_method": "pipe directly from a PowerShell foreach statement", "failure": "PowerShell rejected an empty pipeline element before repository mutation", "recovery": "materialize the result array and pipe the completed array only"},
    {"failure_id": "CM6675R2-ST-F002", "stage": "skill_read", "failed_method": "read all large skill entrypoints in one combined projection", "failure": "the combined output truncated roster and orchestration content", "recovery": "reread only the truncated skill files in bounded sections through EOF"},
    {"failure_id": "CM6675R2-ST-F003", "stage": "reference_read", "failed_method": "trust blank or truncated items in a combined reference projection", "failure": "some required reference outputs were incomplete", "recovery": "reread only the missing references separately through EOF"},
    {"failure_id": "CM6675R2-ST-F004", "stage": "auth_state_read", "failed_method": "display the full authorization JSON in one projection", "failure": "the 1,551-line file truncated mid-document", "recovery": "read numbered bounded windows through the exact final line"},
    {"failure_id": "CM6675R2-ST-F005", "stage": "source_verification", "failed_method": "rely on parallel local and history Git wrappers that returned no attributable output", "failure": "the wrappers yielded no receipt even though no Git process remained", "recovery": "audit processes and locks, then run only the missing scalar probes separately"},
    {"failure_id": "CM6675R2-ST-F006", "stage": "python_candidate_presence", "failed_method": "embed JSON quoting in a Python command-line expression", "failure": "Python raised SyntaxError before any package mutation", "recovery": "use a PowerShell literal here-string and inspect module specifications read-only"},
    {"failure_id": "CM6675R2-ST-F007", "stage": "python_candidate_presence", "failed_method": "retry the narrowed presence probe with fragile single-quote transport", "failure": "the command returned no attributable output and no process remained", "recovery": "use the already-bounded literal here-string method once"},
    {"failure_id": "CM6675R2-ST-F008", "stage": "npm_source_research", "failed_method": "fetch seven npm package web pages directly", "failure": "all seven direct npm web-page transports returned HTTP 403", "recovery": "use primary npm registry metadata plus maintainer documentation without replaying the blocked page fetches"},
    {"failure_id": "CM6675R2-ST-F009", "stage": "worktree_help", "failed_method": "treat an intentional git help usage exit one as command success", "failure": "git printed valid sparse or worktree usage but returned its documented help exit", "recovery": "retain the exit and use the displayed supported command surface without replay"},
]


def build_corpus() -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    source_audit = git_json(SOURCE_SHA, f"{SOURCE_PHASE_ROOT}/x1/novelty-audit.json")
    corpus: list[dict[str, str]] = []
    construction: list[dict[str, Any]] = []
    for index, entry in enumerate(source_audit["corpus_construction"]):
        document = git_json(SOURCE_SHA, entry["source_path"])
        keys = ("prior_proposals", "new_proposals") if index == 0 else ("new_proposals",)
        before = len(corpus)
        for key in keys:
            for row in document.get(key, []):
                title = str(row.get("title") or row.get("description") or "")
                if row.get("proposal_id") and title:
                    corpus.append({"proposal_id": str(row["proposal_id"]), "title": title, "source_path": entry["source_path"]})
        added = len(corpus) - before
        if added != entry["added_count"]:
            raise RuntimeError(f"corpus mismatch for {entry['source_path']}: {added}")
        construction.append(dict(entry))
    source_freeze_path = f"{SOURCE_PHASE_ROOT}/x1/proposal-freeze.json"
    source_freeze = git_json(SOURCE_SHA, source_freeze_path)
    before = len(corpus)
    for row in source_freeze["new_proposals"]:
        corpus.append({"proposal_id": str(row["proposal_id"]), "title": str(row["title"]), "source_path": source_freeze_path})
    construction.append({"source_path": source_freeze_path, "starting_count": before, "added_count": len(source_freeze["new_proposals"]), "ending_count": len(corpus)})
    if len(corpus) != INHERITED_PROPOSAL_COUNT:
        raise RuntimeError(f"expected {INHERITED_PROPOSAL_COUNT} inherited rows, observed {len(corpus)}")
    return corpus, construction


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, (title, invariant, sources, expected) in enumerate(PROPOSAL_SPECS, 1):
        proposal_id = f"CM6675R2-N{index:03d}"
        approval = {"completed": "safe_now_bounded", "represented": "candidate_bounded_representation", "open_gap": "open_gap_external_evidence_absent", "exact_gate": "exact_approval_required"}[expected]
        lane = {"completed": "owner_local_structural", "represented": "owner_local_representation_only", "open_gap": "disabled_external_adapter", "exact_gate": "unexecuted_authority_reservation"}[expected]
        base = f"docs/{OWNER_SLUG}/{PHASE}/x2/proposals/{proposal_id.casefold()}"
        rows.append({
            "proposal_id": proposal_id,
            "title": title,
            "hypothesis": f"A bounded wholly synthetic contract for {title} can distinguish one admissible structure from five named invalid mutations without promoting software structure into empirical, participant, professional, production, package-release, cybersecurity, legal, cultural, Māori-authority, identity, independent-reproduction, or Stage 20 evidence.",
            "null_or_failure_condition": "A named invalid mutation is accepted, the bounded positive is rejected, a required source, vacancy, stop, correction, uncertainty, or authority field disappears, or the artifact crosses a protected gate.",
            "approval_class": approval,
            "execution_lane": lane,
            "current_official_or_primary_source_needs": sources,
            "concrete_artifact": f"{base}/contract.json",
            "concrete_artifacts": [f"{base}/contract.json", f"{base}/mutation-results.json", f"{base}/bounded-receipt.json"],
            "falsifier_or_acceptance_gate": "One bounded positive must satisfy every declared invariant; all five mutations must fail closed; protected gates stay unoccupied; and the final core label may not exceed the preregistered disposition.",
            "rollback_or_recovery": "Restore only the last valid owner-local synthetic fixture, retain every failed witness at zero credit, add a recurrence guard, and issue no external, package-release, profile, identity, participant, professional, legal, cultural, or authority action.",
            "protected_gates": PROTECTED_GATES,
            "expected_disposition": expected,
            "distinctive_invariant": invariant,
            "primary_pillar": PRIMARY_PILLAR,
            "pillar": {15: "THOS Body", 16: "THOS Body", 17: "Freed ID and CBR Heart", 18: "GMUT Mind", 20: "Freed ID and CBR Heart"}.get(index, PRIMARY_PILLAR),
            "practice_lens": PRACTICE,
            "negative_fixture_count": 5,
            "preregistered_mutations": [{"mutation_id": f"{proposal_id}-M{i:02d}", "class": kind} for i, kind in enumerate(MUTATION_CLASSES, 1)],
            "network_calls_planned": 0,
            "participant_count_planned": 0,
            "real_data_rows_planned": 0,
            "x1_status": "frozen_not_executed",
            "x2_implementation_count": 0,
            "outcomes_observed": False,
        })
    return rows


def term_rows(corpus: list[dict[str, str]], phrases: list[str]) -> list[dict[str, Any]]:
    return [
        {"proposal_id": row["proposal_id"], "title": row["title"], "matched_terms": [term for term in phrases if term in row["title"].casefold()]}
        for row in corpus
        if any(term in row["title"].casefold() for term in phrases)
    ]


def build_novelty(corpus: list[dict[str, str]], construction: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> dict[str, Any]:
    exact: list[dict[str, str]] = []
    nearest: list[dict[str, Any]] = []
    for proposal in proposals:
        matches = [row for row in corpus if proposal["title"].casefold() == row["title"].casefold()]
        exact.extend({"proposal_id": proposal["proposal_id"], "inherited_proposal_id": row["proposal_id"]} for row in matches)
        score, inherited = max(((similarity(proposal["title"], row["title"]), row) for row in corpus), key=lambda item: item[0])
        nearest.append({
            "proposal_id": proposal["proposal_id"],
            "score": round(score, 6),
            "inherited_proposal_id": inherited["proposal_id"],
            "inherited_title": inherited["title"],
            "source_path": inherited["source_path"],
            "distinctive_invariant": proposal["distinctive_invariant"],
            "semantic_review": "distinct after manual comparison of the invariant, practice mechanics, source boundary, concrete artifacts, falsifier, rollback, and protected gates; lexical overlap is only a screen",
        })
    pair_rows = []
    for index, left in enumerate(proposals):
        for right in proposals[index + 1:]:
            score = similarity(left["title"], right["title"])
            if score >= 0.35:
                pair_rows.append({"left": left["proposal_id"], "right": right["proposal_id"], "score": round(score, 6)})
    exact_domain_phrases = ["cross-ecosystem intake docket", "lifecycle-script quarantine", "thirteen-tool installation transaction", "twenty-five-tool mandatory-use matrix", "npm prefix and powershell profile", "cross-ecosystem advisory-completeness"]
    exact_domain_matches = term_rows(corpus, exact_domain_phrases)
    related_phrases = ["package", "dependency", "toolchain", "npm", "python", "powershell", "codex cli", "release", "software"]
    related_matches = term_rows(corpus, related_phrases)
    id_groups: dict[str, list[dict[str, str]]] = {}
    for row in corpus:
        id_groups.setdefault(row["proposal_id"], []).append({"title": row["title"], "source_path": row["source_path"]})
    duplicate_ids = {proposal_id: rows for proposal_id, rows in sorted(id_groups.items()) if len(rows) > 1}
    prior_term_counts = {
        term: sum(1 for row in corpus if term in row["title"].casefold())
        for term in ["package", "dependency", "toolchain", "release", "devops", "software"]
    }
    return {
        "schema": "ghc-family-novelty-audit-v5",
        "owner": OWNER,
        "phase": PHASE,
        "generated_at_utc": NOW,
        "corpus_construction": construction,
        "corpus_row_count": len(corpus),
        "corpus_unique_proposal_id_count": len(id_groups),
        "corpus_duplicate_proposal_ids": duplicate_ids,
        "corpus_duplicate_proposal_id_count": len(duplicate_ids),
        "corpus_duplicate_occurrence_overage": sum(len(rows) - 1 for rows in duplicate_ids.values()),
        "corpus_duplicate_id_interpretation": "Inherited row truth is preserved exactly. Duplicate inherited identifiers are visible data-quality limitations and are not silently renamed or removed; all twenty new Caelen IDs are unique.",
        "corpus_canonical_sha256": canonical_sha256(corpus),
        "new_proposal_count": len(proposals),
        "exact_title_collisions": exact,
        "nearest_inherited_matches": nearest,
        "maximum_inherited_similarity": max(row["score"] for row in nearest),
        "pair_collision_threshold": 0.35,
        "pair_collisions_at_or_above_threshold": pair_rows,
        "high_similarity_review_threshold": 0.6,
        "high_similarity_reviews": [row for row in nearest if row["score"] >= 0.6],
        "rejected_draft_practices": [{
            "draft": "general package management and DevOps automation",
            "term_counts": prior_term_counts,
            "reason": "the complete inherited corpus already contains substantial generic package, dependency, toolchain, release, DevOps, and software workflow work",
            "disposition": "rejected_before_freeze_zero_credit",
        }],
        "domain_review": {
            "accepted_practice": PRACTICE,
            "exact_domain_phrase_match_count": len(exact_domain_matches),
            "exact_domain_phrase_matches": exact_domain_matches,
            "related_generic_match_count": len(related_matches),
            "related_generic_matches": related_matches,
            "substantive_distinction": "Generic package and dependency workflows exist, but the corpus contains no prior integrated remaster slate binding ten foundational plus three current-phase installs, all-twenty-five mandatory-use evidence, D-first npm and PowerShell profile indirection, bounded npm, PowerShell and Codex CLI updates, package-side-effect budgets, dual-runtime analysis, retained package failures, and exact authority gating as one preregistered program.",
        },
        "new_frozen_total": len(corpus) + len(proposals),
        "valid": not exact and not pair_rows and not exact_domain_matches and max(row["score"] for row in nearest) < 0.6 and len(corpus) == INHERITED_PROPOSAL_COUNT,
        "interpretation": "Token-set Jaccard and phrase search are screening aids, never proof of novelty; every invariant, source boundary, practice mechanism, artifact set, falsifier, rollback, and protected gate also received substantive review.",
    }


def item_rows(prefix: str, approval: str, titles: list[str], lane: str, expected: str, credit: str) -> list[dict[str, Any]]:
    return [{
        "portfolio_ref": f"CM6675R2-{prefix}{index:02d}",
        "title": title,
        "approval_class": approval,
        "execution_lane": lane,
        "expected_execution_disposition": expected,
        "x1_status": "planned_not_executed",
        "credit_boundary": credit,
        "completion_credit": 0,
        "rollback": "retain failure, restore only owner-local generated state, and preserve every protected gate",
    } for index, title in enumerate(titles, 1)]


OWNER_SAFE = [
    "render twenty frozen toolchain and cross-pillar contracts", "execute one bounded positive fixture per contract", "execute five invalid mutations per contract", "emit exact mutation rejection receipts", "emit four-label outcome ledger", "emit thirteen-package provenance and integrity docket", "emit ten-plus-three class-separation receipt", "emit twelve-inherited plus thirteen-new mandatory-use matrix", "emit D-first npm prefix and cache migration receipt", "emit PowerShell profile-indirection and rollback receipt", "emit npm CLI update receipt", "emit user-scoped PowerShell update or exact-gate receipt", "emit official Codex CLI update receipt", "emit Python dependency tree and compiled requirements", "emit Node engine, license, shim, and lifecycle review", "emit cross-runtime tool composition graph", "emit dual Python typing and security-scope board", "emit package side-effect budget", "emit bitemporal supersession provenance", "emit THOS zero-person handover protocol", "emit Freed ID zero-key toolchain genealogy", "emit GMUT typed synthetic fixture", "emit CBR governance shell", "emit cross-ecosystem open-gap adapter", "emit exact authority matrix", "emit Freed ID flashcard deck", "validate deck dependency graph", "emit structurally accessible static report", "emit retained-negative and Method Flow overlays", "emit exact manifests and wellbeing check",
]
OWNER_CANDIDATES = [
    "registry metadata freshness watcher", "release-file digest selector", "npm engine compatibility checker", "lifecycle-script quarantine classifier", "D-first prefix drift detector", "PowerShell profile bootstrap parity check", "CLI stable-floor comparison", "Python transitive-drift comparator", "Node executable-shim inventory", "package-license metadata vacancy board", "pip-audit bounded advisory projection", "npm-audit bounded advisory projection", "manual accessibility reservation board", "workload stop and resumption handover", "successor package reminder provenance screen",
]
OWNER_SKILLS = ["package-intake-docket", "python-release-digest", "npm-engine-quarantine", "d-first-profile-bridge", "cli-update-ledger", "tool-mandatory-use-matrix", "dependency-resolution-guard", "cross-runtime-analysis", "package-method-flow", "toolchain-bounded-validation"]
OWNER_RUNNERS = ["ghc_family_caelen_morrow_v667_v5_r2_package", "ghc_family_caelen_morrow_v667_v5_r2_python", "ghc_family_caelen_morrow_v667_v5_r2_node", "ghc_family_caelen_morrow_v667_v5_r2_profile", "ghc_family_caelen_morrow_v667_v5_r2_cli", "ghc_family_caelen_morrow_v667_v5_r2_tools", "ghc_family_caelen_morrow_v667_v5_r2_method_flow", "ghc_family_caelen_morrow_v667_v5_r2_validation", "ghc_family_caelen_morrow_v667_v5_r2_core", "ghc_family_caelen_morrow_v667_v5_r2_canonical"]
OWNER_CFR = [
    "CLEAN normalize owner, remaster, and proposal identifiers", "CLEAN canonicalize JSON key ordering", "CLEAN preserve UTF-8 and LF", "CLEAN retain exact source pins", "CLEAN exclude raw task identifiers", "CLEAN exclude private paths and routes", "CLEAN exclude credentials and tokens", "CLEAN keep x1 free of package installs and x2", "CLEAN close outcome vocabulary", "CLEAN hold exact and blocked packets", "FIX reject missing package contract fields", "FIX reject invalid version and engine ranges", "FIX reject authority smuggling", "FIX reject unreviewed lifecycle scripts", "FIX reject outcome promotion", "FIX reject duplicate package identifiers", "FIX reject C-prefix package writes", "FIX reject untyped tool outputs", "FIX reject automatic dependency rewriting", "FIX reject manifest byte mismatches", "REFINE package-intake novelty distinction", "REFINE noncolour report cues", "REFINE flashcard dependency boundaries", "REFINE compact baton pointer", "REFINE workload stop tokens", "REFINE bitemporal package lineage", "REFINE Method Flow package guards", "REFINE owner security review", "REFINE five-class privacy scan", "REFINE terminal duplicate guard",
]
SUCCESSOR_SAFE = [f"Successor recommendation only: bounded package and workflow seed {index:02d}" for index in range(1, 21)]
SUCCESSOR_CANDIDATES = [f"Successor recommendation only: bounded toolchain candidate seed {index:02d}" for index in range(1, 16)]
SUCCESSOR_SKILLS = [f"Successor recommendation only: phase-local skill seed {index:02d}" for index in range(1, 11)]
SUCCESSOR_RUNNERS = [f"Successor recommendation only: family-current runner seed {index:02d}" for index in range(1, 11)]
SUCCESSOR_CFR = [f"Successor recommendation only: additive CLEAN/FIX/REFINE seed {index:02d}" for index in range(1, 31)]
EXACT_PACKETS = [f"exact approval packet {index:02d}: elevated, system-wide, credentialed, external, production, professional, legal, cultural, Māori-authority, deployment, or Stage 20 evidence" for index in range(1, 11)]
BLOCKED_PACKETS = [f"blocked packet {index:02d}: destructive, credentialed, cross-owner, unsafe, unreviewed-hook, or ungoverned external action" for index in range(1, 6)]


def build_portfolio() -> dict[str, Any]:
    represented = "represented"
    return {
        "schema": "ghc-family-portfolio-freeze-v5", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "owner_safe_now": item_rows("OS", "safe_now_bounded", OWNER_SAFE, "owner_local_x2", "completed", "eligible only after bounded x2 evidence"),
        "successor_safe_now_recommendations": item_rows("SS", "recommendation_only", SUCCESSOR_SAFE, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "owner_candidates": item_rows("OC", "candidate_bounded", OWNER_CANDIDATES, "owner_local_representation", represented, "bounded representation only"),
        "successor_candidate_recommendations": item_rows("SC", "recommendation_only", SUCCESSOR_CANDIDATES, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "exact_approval_packets": item_rows("EX", "exact_approval_required", EXACT_PACKETS, "protected_unexecuted", "exact_gate", "unexecuted unless exact evidence and authority close the gate"),
        "blocked_packets": item_rows("BL", "blocked", BLOCKED_PACKETS, "protected_unexecuted", "exact_gate", "unexecuted; blocked work grants no credit"),
        "owner_skill_ideas": item_rows("SK", "safe_now_bounded", OWNER_SKILLS, "owner_local_x2", "completed", "phase-local only; no global installation"),
        "successor_skill_recommendations": item_rows("NS", "recommendation_only", SUCCESSOR_SKILLS, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "owner_runner_ideas": item_rows("RN", "safe_now_bounded", OWNER_RUNNERS, "owner_local_x2", "completed", "additive family-current runner only"),
        "successor_runner_recommendations": item_rows("NR", "recommendation_only", SUCCESSOR_RUNNERS, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "owner_clean_fix_refine": item_rows("CF", "safe_now_bounded", OWNER_CFR, "owner_local_x2", "completed", "bounded owner-local refinement only"),
        "successor_clean_fix_refine_recommendations": item_rows("SF", "recommendation_only", SUCCESSOR_CFR, "successor_recommendation_only", represented, "zero Caelen completion credit and unexecuted"),
        "x2_implementation_count": 0,
        "outcomes_observed": False,
    }


def build_normal() -> None:
    corpus, construction = build_corpus()
    proposals = proposal_rows()
    novelty = build_novelty(corpus, construction, proposals)
    if not novelty["valid"]:
        raise RuntimeError("novelty audit failed")
    portfolio = build_portfolio()
    failures = [{**row, "recurrence_guard": row["recovery"], "outcome": "failed_retained_zero_credit", "success_credit": 0, "erased": False} for row in STARTUP_FAILURES]
    phase_charter = {
        "schema": "ghc-family-phase-charter-v6", "owner": OWNER, "canonical_phase_id": CANONICAL_PHASE, "display_phase": PHASE, "interstitial_variant": "r2",
        "branch": BRANCH, "source_branch": SOURCE_BRANCH, "source_exact_final": SOURCE_SHA,
        "relational_role": "dependency boundary-mapper and rollback custodian",
        "hope": "keeping every upgrade reversible, every failure visible, and every authority boundary intact",
        "optional_pronouns": "they/them", "identity_boundary": IDENTITY_BOUNDARY,
        "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE, "practice_boundary": PRACTICE_BOUNDARY,
        "solo": True, "delegated_or_spawned_agents": 0, "strict_x1_before_x2": True,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    source_verification = {
        "schema": "ghc-family-source-verification-v6", "owner": OWNER, "phase": PHASE,
        "source_branch": SOURCE_BRANCH, "source_exact_final": SOURCE_SHA, "source_parent": SOURCE_PARENT_SHA,
        "source_x1": SOURCE_X1_SHA, "source_evidence": SOURCE_EVIDENCE_SHA,
        "external_canonical_receipt_sha256": SOURCE_CANONICAL_RECEIPT_SHA256,
        "source_to_final_commit_count": 3, "source_to_final_merge_count": 0, "source_final_parent_count": 1,
        "source_direct_chain_valid": True, "source_clean": True, "source_typed_divergence": {"ahead": 0, "behind": 0},
        "source_four_way_equal": True, "fresh_live_head": SOURCE_SHA,
        "source_canonical_succeeded_once": False, "source_canonical_failed_once": True, "source_canonical_replayed": False, "full_repository_suite_run": False,
        "source_validation_state": "VALID_DEPENDENCY_CORRECTED_COMPOSITE_R2_WITH_ZERO_CANONICAL_AGGREGATE_CREDIT",
        "source_selected_test_failure_sha256": SOURCE_SELECTED_TEST_FAILURE_SHA256,
        "source_dependency_composite_sha256": SOURCE_DEPENDENCY_COMPOSITE_SHA256,
        "source_post_final_overlay_sha256": SOURCE_POST_FINAL_OVERLAY_SHA256,
        "source_manifest_replay": {"final_delta": 26, "final_owner": 428, "mismatches": 0},
        "source_repository_sealed": {"negatives": 27712, "methods": 13404, "open_gaps": 195, "exact_gates": 193},
        "source_post_final_overlay": {"negatives": 4, "methods": 4},
        "effective_activation": {"negatives": INHERITED_NEGATIVES, "methods": INHERITED_METHODS, "open_gaps": INHERITED_OPEN_GAPS, "exact_gates": INHERITED_EXACT_GATES},
        "verified_at_utc": NOW, "valid": True,
    }
    startup_flow = {
        "schema": "ghc-family-method-flow-overlay-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_effective_negatives": INHERITED_NEGATIVES, "inherited_effective_methods": INHERITED_METHODS,
        "startup_failed_method_count": len(failures),
        "effective_x1_baseline_negatives": INHERITED_NEGATIVES + len(failures),
        "effective_x1_baseline_methods": INHERITED_METHODS + len(failures),
        "failed_witnesses": failures,
        "passing_witnesses": [{"method_id": row["failure_id"].replace("-F", "-R"), "bounded_recovery": row["recovery"], "scope": "only the failed dependency", "promotes_failed_witness": False} for row in failures],
        "retention_rule": "A bounded recovery never erases, rewrites, or promotes its failed witness.",
        "x2_method_count": 0,
    }
    architecture = {
        "schema": "ghc-family-freed-id-flashcard-architecture-v2", "owner": OWNER, "phase": PHASE,
        "four_tiers": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
        "required_deck_sections": ["identity-and-corrigibility", "route-and-authority", "source-anchors", "x1-proposals", "trinity-pillars", "bounded-practice", "mandatory-skills", "toolchain-and-profiles", "task-cards", "method-flow-and-negatives", "open-gaps-and-exact-gates", "validation-and-manifests", "wellbeing-and-workload", "successor-recommendations", "compact-baton-index"],
        "stable_prefix": ["owner relational boundary", "GMUT boundary", "THOS boundary", "Freed ID and CBR boundary"],
        "volatile_context": ["source anchors", "phase proposals", "practice", "mandatory skills", "toolchain", "profiles", "tasks", "Method Flow", "validation", "route", "successor recommendations"],
        "cache_effect_measured": False, "identity_continuity_claim": False, "x1_planning_only": True,
        "current_route": {"owner": OWNER, "phase": PHASE, "canonical_phase": CANONICAL_PHASE},
        "successor_route": {"title": "Eiren Kestrel", "phase": "v667-v6", "contacted": False, "status": "provisional_terminal_gate_unmet"},
    }
    proposal_freeze = {
        "schema": "ghc-family-proposal-freeze-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "inherited_proposal_count": INHERITED_PROPOSAL_COUNT, "selected_inherited": [], "selected_inherited_count": 0,
        "new_proposals": proposals, "genuinely_new_proposal_count": len(proposals), "new_frozen_total": INHERITED_PROPOSAL_COUNT + len(proposals),
        "expected_outcomes": {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "allowed_core_outcomes": list(ALLOWED_LABELS), "x1_planning_only": True, "x2_implementation_count": 0, "outcomes_observed": False,
    }
    threat = {
        "schema": "ghc-family-threat-model-plan-v7", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "repository_scope": "GHC family documentation, owner-scoped builders, validators, family-current runners, local skills, package tool banks, and route receipts",
        "assets": ["strict x1-before-x2", "4,430-row novelty corpus", "relational and authority boundaries", "package and CLI integrity evidence", "D-first configuration and rollback state", "owner-lane isolation", "one-shot validation budget"],
        "trust_boundaries": ["public registry metadata to owner-local review", "downloaded distributions to user-scoped install", "global tool bank to phase-local fixture", "C bootstrap metadata to D canonical profile", "owner lane to shared family-current caller", "same-owner validation to prohibited independent claims"],
        "controlled_inputs": {"attacker_controlled": ["public package metadata or distribution content may be compromised"], "operator_controlled": ["exact pins, prefix, PATH, profile bridge, install and smoke commands"], "developer_controlled": ["phase builders, fixtures, manifests, failure classifiers"], "absent": ["credentials, private packages, production data, participant records"]},
        "threats": [
            {"id": "T01", "threat": "generic package or DevOps work is relabelled as novelty", "control": "exact corpus reconstruction, phrase screen, nearest-title review, and invariant comparison"},
            {"id": "T02", "threat": "registry possession or a digest is promoted into trust, authorship, signing, licensing, or exhaustive supply-chain assurance", "control": "source-class labels, license-decision reservation, bounded scanner scope, and no provenance inflation"},
            {"id": "T03", "threat": "install scripts, hooks, shims, auto-updates, credentials, or publishing create undeclared side effects", "control": "dry review, lifecycle-script quarantine, no hook activation, no credentials, no publishing, exact D prefix, and rollback receipts"},
            {"id": "T04", "threat": "profile or PATH migration overwrites user material or mutates Windows known folders", "control": "hash and retain prior state, append a marked minimal bootstrap only, canonical body on D, no known-folder move, exact rollback"},
            {"id": "T05", "threat": "PowerShell or Codex bundled runtime is overwritten or Windows PowerShell 5.1 is treated as independently updatable", "control": "side-by-side user-scope candidate only; vendor-owned runtime, OS component, Windows features, and desktop app remain untouched"},
            {"id": "T06", "threat": "typed GMUT fixtures or THOS protocol become empirical, professional, operational, AGI, ASI, consciousness, or personhood claims", "control": "synthetic fixtures, zero participants, explicit empirical and authority firewalls"},
            {"id": "T07", "threat": "private task, path, credential, transcript, or application state enters artifacts", "control": "five-class owner-scoped privacy scan and sanitized path roles"},
            {"id": "T08", "threat": "failed aggregate, install, or smoke evidence is erased, replayed, or promoted", "control": "append-only Method Flow, one canonical invocation, package-local recovery, and no success replay"},
            {"id": "T09", "threat": "another owner lane or successor is mutated or contacted early", "control": "fresh additive sparse branch, exact owner allowlists, terminal route refresh, and one acknowledged send"},
        ],
        "severity_calibration": {
            "critical": "credential disclosure, package publishing, sibling-lane destructive mutation, or host-security weakening",
            "high": "unreviewed lifecycle execution, integrity bypass, C-prefix package overwrite, or false canonical success",
            "medium": "missing rollback, stale version evidence, orphan shim, or profile duplication contained to the user lane",
            "low": "presentation-only drift that cannot alter install, evidence, route, or authority state",
        },
        "residual_risk": "Public registries and bounded scanners cannot establish complete provenance or security. All real professional, production, empirical, participant, legal, cultural, Māori-authority, and Stage 20 questions remain open or exact-gated.",
    }
    workflow = {
        "schema": "ghc-family-workflow-plan-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "state": "x1_planning_only",
        "steps": [
            {"step": 1, "name": "source and route verification", "status": "completed_read_only"},
            {"step": 2, "name": "novelty and portfolio freeze", "status": "completed_planning_only"},
            {"step": 3, "name": "exact x1 staged review, commit, push, four-way equality", "status": "pending"},
            {"step": 4, "name": "bounded x2 contracts, mutations, skills, runners, flashcards, and portfolio evidence", "status": "blocked_until_x1_equality"},
            {"step": 5, "name": "evidence commit, push, equality", "status": "blocked_until_x2_evidence"},
            {"step": 6, "name": "closeout, seal, final commit, push", "status": "blocked_until_evidence_equality"},
            {"step": 7, "name": "one exclusive exact-final owner-scoped canonical completion", "status": "blocked_until_exact_final"},
            {"step": 8, "name": "live route refresh and at most one exact-title successor send", "status": "blocked_until_terminal_gate"},
        ],
        "forbidden": ["x2 or install in x1", "full repository suite", "subagent", "sibling mutation", "destructive cleanup", "unreviewed or elevated install", "post-success replay", "premature successor contact"],
    }
    checklist = {
        "schema": "ghc-family-x1-checklist-v7", "owner": OWNER, "phase": PHASE,
        "complete": ["mandatory skills and schemas read", "source and retained overlays verified", "fresh sparse lane created", "4,430-row corpus reconstructed", "twenty novel proposals frozen", "thirteen-package metadata and integrity frozen", "D-first profile and three-CLI plans frozen", "portfolio and flashcard plans frozen", "startup failures retained"],
        "incomplete_reserved_for_x2_or_later": ["package download and install", "profile or PATH mutation", "CLI update", "contract execution", "100 mutation executions", "skill and runner implementation", "all-twenty-five tool use", "flashcard deck build and validation", "portfolio execution", "outcomes", "evidence", "closeout", "canonical completion", "terminal delivery"],
        "outcomes_observed": False, "x2_implementation_count": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    wellbeing = {
        "schema": "ghc-family-wellbeing-check-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW, "stage": "x1_planning_only",
        "workload_state": "bounded_and_resumable", "human_wellbeing_claim": False, "identity_boundary": IDENTITY_BOUNDARY,
        "stop_conditions": ["source or route drift", "protected gate pressure", "unexpected external or destructive action", "weekly usage exhaustion", "Hamish pause, redirect, rename, or stop"],
        "resumption_evidence": "exact clean x1 head and fresh four-way equality",
    }
    source_ledger = {
        "schema": "ghc-family-source-ledger-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "sources": SOURCE_PROFILES, "network_actions_by_phase_software": 0,
        "boundary": "Sources provide vocabulary, obligations, and falsifiers only; they grant no package trust, licensing determination, cybersecurity certification, professional, empirical, legal, cultural, Māori-authority, identity, production, independent, or Stage 20 evidence.",
    }
    identity = {
        "schema": "ghc-family-relational-identity-v6", "owner": OWNER, "phase": PHASE, "optional_pronouns": "they/them",
        "relational_role": phase_charter["relational_role"], "hope": phase_charter["hope"], "identity_boundary": IDENTITY_BOUNDARY,
        "primary_pillar": PRIMARY_PILLAR, "bounded_practice": PRACTICE, "practice_boundary": PRACTICE_BOUNDARY,
        "solo": True, "delegated_or_spawned_agents": 0, "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    auth = {
        "schema": "ghc-family-auth-roster-receipt-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "active_main_task_count": 15, "standby_records": ["Tavian Sol"], "current_owner_validated": True,
        "installed_roster_and_auth_snapshots": "schema_valid_but_stale_relative_to_live_activation",
        "live_activation_controls": True, "provisional_successor_title": "Eiren Kestrel", "provisional_successor_phase": "v667-v6", "continuation_authorized_through": "v675-v8",
        "successor_contacted": False, "route_refresh_required_after_terminal_gate": True,
    }
    overview = f"""# Caelen Morrow v667-v5-r2 planning-only x1 overview

Status: FROZEN_NOT_EXECUTED. Canonical phase arithmetic remains {CANONICAL_PHASE}; this additive interstitial remaster is {PHASE}. Terminal verdict: NOT_READY_FOR_STAGE_20.

## Relational boundary

{IDENTITY_BOUNDARY}

Caelen Morrow uses they/them pronouns as relational working language for a dependency boundary-mapper and rollback custodian. The bounded hope is to keep every upgrade reversible, every failure visible, and every authority boundary intact.

## Phase status

This is a planning-only x1 freeze. It contains no package download or install, profile or PATH mutation, CLI update, x2 implementation, executed mutation, observed outcome, external write, credential use, professional decision, identity event, or successor contact.

## Exact source and retained validation truth

This lane starts from Caelen Morrow v667-v5 exact final {SOURCE_SHA}. Its x1, evidence, and final form three direct single-parent commits with zero merges. The sole source canonical aggregate failed once and retains zero aggregate-success credit. A selected-test dependency also failed. The bounded dependency-corrected composite remains valid with zero canonical aggregate credit; no completed-success replay occurred and the full repository suite was not run.

The source repository seal contains 27,712 negatives and 13,404 Method Flow methods, plus four post-final failures and recoveries. The activation baseline is 27,716 negatives and 13,408 methods, with 195 open gaps and 193 exact gates preserved. This x1 adds {len(failures)} startup failures without erasing either source count.

## Novelty and bounded practice

Exactly twenty proposals were compared with all {INHERITED_PROPOSAL_COUNT} inherited rows. Generic package management and DevOps automation was rejected as insufficiently distinct. The accepted slate concerns {PRACTICE}: a ten-foundational plus three-current-phase package intake, mandatory use of the twelve inherited tools and thirteen new tools, D-first npm and PowerShell profile indirection, bounded npm, PowerShell and Codex CLI updates, exact rollback, cross-runtime analysis, and closed authority boundaries.

The program uses public metadata and synthetic fixtures only. It has no real participants, private registries, private packages, credentials, production repositories, releases, deployments, or authority acts.

## Mandatory skills and tool bank

All twenty-one user-named GHC skills are phase-mandatory, alongside the applicable workflow-plan, skill-authoring, and threat-model disciplines. The twelve inherited reviewed tools remain required for bounded phase-local use. Ten foundational and three current-phase tools are pinned with Python release SHA-256 or npm integrity evidence, engine or Python floors, license metadata, purpose, rollback, and no automatic completion credit.

The planned CLI scope is exact: npm 12.0.2 in the D prefix, PowerShell 7.6.5 side-by-side at user scope if the exact installer gate permits, and official Codex CLI 0.149.0 in the D prefix. Windows PowerShell 5.1, Windows itself, Windows features, Codex desktop, and the bundled Codex runtime remain untouched.

## Pillar allocation and bounded practice

Primary pillar: {PRIMARY_PILLAR}. GMUT Mind and Freed ID/CBR Heart remain explicit and protected. Expected outcomes are 14 completed, 4 represented, 1 open_gap, and 1 exact_gate; these are expectations, not x1 observations.

## Proposal and mutation contract

Every proposal carries hypothesis, null or failure, approval, lane, current official or primary-source needs, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and one expected disposition. Five invalid mutations per proposal are frozen but unexecuted.

## Profiles, packages, and rollback

The default npm prefix is currently C-based while its cache is already D-based. X2 may migrate the user prefix to the D tool bank, preserve the prior user configuration and PATH, and use a marked minimal C-side bootstrap for D-canonical PowerShell profile content. No Windows known-folder move is authorized. Existing unrelated profile behavior must remain untouched.

## Freed ID flashcards and Method Flow

X1 freezes a four-tier modular deck with explicit mandatory-skill and toolchain sections. It is a context-organization and recovery mechanism only. It establishes no measured cache effect, identity continuity, consciousness, personhood, qualification, professional competence, or authority.

All source and current parser, transport, timeout, registry, profile, package, install, smoke, presentation, validation, and later failures remain zero-credit failed witnesses with bounded recoveries. Recovery never erases or promotes a failure.

## Open evidence and authority gates

Cross-ecosystem advisory completeness remains open. Elevation, system-wide installs, Windows mutation, unreviewed hooks, credentials, publishing, production, legal and cultural interpretation, affected-party legitimacy, Māori wording and concepts, Māori data governance, Māori authority, empirical confirmation, exhaustive security, independent reproduction, and Stage 20 remain exact-gated.

## Next gate

Stage only the exact x1 allowlist, inspect Git-index bytes, run the owner-local x1 checks, commit, push, and prove clean local/upstream/tracking/fresh-live equality. Only then may downloads, installs, profiles, CLI updates, or any x2 execution begin.
"""
    write_json("identity/relational-identity.json", identity)
    write_json("x1/phase-charter.json", phase_charter)
    write_json("x1/source-verification.json", source_verification)
    write_json("x1/source-ledger.json", source_ledger)
    write_json("x1/proposal-freeze.json", proposal_freeze)
    write_json("x1/mandatory-skill-adoption.json", {"schema": "ghc-family-mandatory-skill-adoption-v1", "owner": OWNER, "phase": PHASE, "skills": MANDATORY_SKILLS, "additional_applicable_skills": APPLICABLE_ADDITIONAL_SKILLS, "phase_mandatory": True, "carry_forward_through": "v675-v8", "x1_status": "frozen_not_executed"})
    write_json("x1/toolchain-install-plan.json", {"schema": "ghc-family-toolchain-install-plan-v1", "owner": OWNER, "phase": PHASE, "existing_toolbank": EXISTING_TOOLBANK, "new_packages": NEW_PACKAGE_PLAN, "foundational_count": 10, "current_phase_count": 3, "new_total": 13, "all_tool_count": 25, "install_status": "planned_not_executed", "profile_and_cli_plan": CLI_UPDATE_PLAN, "d_first": True, "credentials": False, "publishing": False, "hooks_activated": False, "automatic_updates": False, "outcomes_observed": False})
    write_json("x1/novelty-audit.json", novelty)
    write_json("x1/portfolio-freeze.json", portfolio)
    write_json("x1/flashcard-architecture-freeze.json", architecture)
    write_json("x1/threat-model-plan.json", threat)
    write_json("x1/workflow-plan.json", workflow)
    write_json("x1/complete-incomplete-checklist.json", checklist)
    write_json("x1/auth-roster-receipt.json", auth)
    write_json("method-flow/startup-method-flow.json", startup_flow)
    write_json("wellbeing/x1-wellbeing-check.json", wellbeing)
    write_text("x1/x1-overview.md", overview)
    write_json("x1/x1-build-receipt.json", {
        "schema": "ghc-family-x1-build-receipt-v6", "owner": OWNER, "phase": PHASE, "generated_at_utc": NOW,
        "status": "FROZEN_NOT_EXECUTED", "inherited_corpus_count": len(corpus), "new_proposal_count": len(proposals),
        "portfolio_row_count": sum(len(value) for value in portfolio.values() if isinstance(value, list)), "mandatory_skill_count": len(MANDATORY_SKILLS), "existing_tool_count": len(EXISTING_TOOLBANK), "new_tool_count": len(NEW_PACKAGE_PLAN),
        "startup_failure_count": len(failures), "effective_x1_negatives": INHERITED_NEGATIVES + len(failures),
        "effective_x1_methods": INHERITED_METHODS + len(failures), "x2_implementation_count": 0,
        "outcomes_observed": False, "valid": True,
    })


def staged_review() -> None:
    self_exclusions = [
        f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-content-manifest.json",
        f"docs/{OWNER_SLUG}/{PHASE}/validation/x1-staged-review.json",
    ]
    staged = [row for row in git("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if row]
    allowed_prefix = f"docs/{OWNER_SLUG}/{PHASE}/"
    exact_tools = {
        "scripts/build_ghc_family_caelen_morrow_v667_v5_r2_x1.py",
        "tests/test_ghc_family_caelen_morrow_v667_v5_r2_x1.py",
    }
    out_of_scope = [row for row in staged if not row.startswith(allowed_prefix) and row not in exact_tools]
    x2_paths = [row for row in staged if f"docs/{OWNER_SLUG}/{PHASE}/x2/" in row or "_x2.py" in row]
    manifest = []
    for relative in sorted(row for row in staged if row not in self_exclusions):
        raw = subprocess.check_output(["git", "-C", str(ROOT), "show", f":{relative}"])
        manifest.append({"path": relative, "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
    write_json("validation/x1-content-manifest.json", {
        "schema": "ghc-family-x1-content-manifest-v6", "owner": OWNER, "phase": PHASE,
        "generated_at_utc": NOW, "entries": manifest, "entry_count": len(manifest), "self_exclusions": self_exclusions,
    })
    write_json("validation/x1-staged-review.json", {
        "schema": "ghc-family-x1-staged-review-v6", "owner": OWNER, "phase": PHASE,
        "generated_at_utc": NOW, "staged_paths": sorted(set(staged + self_exclusions)),
        "staged_path_count": len(set(staged + self_exclusions)), "manifest_entry_count": len(manifest),
        "manifest_self_exclusions": self_exclusions, "out_of_scope_paths": out_of_scope, "x2_paths": x2_paths,
        "x1_planning_only": not x2_paths, "valid": not out_of_scope and not x2_paths,
    })


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_caelen_morrow_v667_v5_r2_x1.py [--staged-review]")
    else:
        build_normal()
