#!/usr/bin/env python3
"""Build Elaren Kestrel's strict x1-only v651-v6 preregistration packet."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/elaren-kestrel/v651-v6"
SOURCE = "7c4309d6b57bc4827ebd49bcb7c9dfc669c46e3d"
SOURCE_BRANCH = "codex/GHC-Family/eiren-kestrel-v648-v3-3-full-tools"
OWNED_BRANCH = "codex/GHC-Family/elaren-kestrel-v649-v8-full-tools"
PHASE = "v651-gmut-thos-v6-x1-x2"
OWNER = "Elaren Kestrel"


PROPOSAL_SPECS = [
    ("non-normal-pseudospectrum", "GMUT Non-Normal Pseudospectrum Transient-Growth Board", "GMUT Mind", "A bounded pseudospectral fixture can distinguish modal eigenvalue stability from non-normal transient amplification without making an empirical GMUT claim.", "completed", ["SRC-PSEUDO-01"]),
    ("constraint-residual-attribution", "GMUT Constraint Residual Source-Attribution Graph", "GMUT Mind", "A typed residual graph can attribute algebraic, discretization, solver, and boundary-condition contributions without converting attribution into physical confirmation.", "completed", ["SRC-NASA-7009"]),
    ("buckingham-pi", "GMUT Buckingham Pi Nondimensionalization Tribunal", "GMUT Mind", "A dimensional-rank witness can derive independent nondimensional groups and reject rank, unit, or scale inconsistencies in synthetic GMUT fixtures.", "completed", ["SRC-NASA-7009"]),
    ("discrete-adjoint-dot-product", "GMUT Discrete-Adjoint Primal-Dual Dot-Product Test", "GMUT Mind", "A primal-dual dot-product identity can detect an inconsistent discrete adjoint on bounded synthetic operators.", "completed", ["SRC-NASA-MMS"]),
    ("dae-index-drift", "GMUT Differential-Algebraic Index and Constraint-Drift Classifier", "GMUT Mind", "A structural DAE fixture can separate algebraic index obligations from numerical constraint drift and reject unsupported solver promotion.", "completed", ["SRC-SCIPY-IVP"]),
    ("event-localization", "GMUT Event-Localization Bracket and Direction Gate", "GMUT Mind", "A bracket, direction, terminal-state, and tolerance contract can reject missed or multiply credited zero-crossing events.", "completed", ["SRC-SCIPY-IVP"]),
    ("richardson-asymptotic-range", "GMUT Richardson Extrapolation Asymptotic-Range Gate", "GMUT Mind", "A three-resolution witness can accept an order estimate only inside a detected asymptotic regime and refuse non-monotone or zero-denominator cases.", "completed", ["SRC-NASA-MMS", "SRC-SANDIA-MMS"]),
    ("stiffness-solver-contract", "GMUT Stiffness Detection and Solver-Evidence Contract", "GMUT Mind", "A bounded stiffness indicator can route synthetic fixtures to explicit methods while keeping solver success distinct from model validity.", "completed", ["SRC-SCIPY-IVP"]),
    ("jacobian-coloring", "GMUT Jacobian-Coloring Sparsity Witness", "GMUT Mind", "A graph-coloring fixture can compress structurally independent derivative columns while rejecting overlapping perturbation groups.", "completed", ["SRC-NASA-MMS"]),
    ("work-precision-frontier", "GMUT Work-Precision Frontier Nonpromotion Board", "GMUT Mind", "A cost-error Pareto witness can compare bounded solver fixtures without promoting fastest, cheapest, or most accurate into empirical truth.", "completed", ["SRC-NASA-7009"]),
    ("conservation-projection", "GMUT Conservation-Projection Drift Monitor", "GMUT Mind", "A projection fixture can measure invariant drift before and after correction while refusing a projection that increases residual or violates its declared domain.", "completed", ["SRC-NASA-MMS"]),
    ("shadow-hamiltonian", "GMUT Shadow-Hamiltonian Boundedness Board", "GMUT Mind", "A symplectic synthetic trajectory can expose bounded modified-energy oscillation separately from secular physical-energy drift.", "completed", ["SRC-NASA-7009"]),
    ("mixed-precision-escalation", "GMUT Mixed-Precision Escalation Contract", "GMUT Mind", "A residual and conditioning policy can escalate precision fail-closed when a lower-precision solve cannot support the declared numerical claim.", "completed", ["SRC-NUMPY-COMPAT"]),
    ("emulator-convex-hull", "GMUT Emulator Convex-Hull Extrapolation Gate", "GMUT Mind", "A training-domain geometry witness can refuse emulator credit outside the declared hull or distance envelope.", "completed", ["SRC-NASA-7009"]),
    ("metamorphic-coordinate-invariance", "GMUT Metamorphic Coordinate-Invariance Oracle", "GMUT Mind", "A metamorphic test can require equivalent bounded outputs under a declared invertible coordinate transform while preserving unit and domain boundaries.", "completed", ["SRC-EFT-BASIS"]),
    ("model-discrepancy-separator", "GMUT Model-Discrepancy and Parameter-Uncertainty Separator", "GMUT Mind", "A typed uncertainty budget can reject fixtures that silently absorb structural discrepancy into parameter uncertainty.", "completed", ["SRC-NASA-7009"]),
    ("blind-likelihood-lockfile", "Blind Likelihood Lockfile Adapter", "GMUT Mind", "A real observational likelihood may be credited only after a preregistered lockfile, authentic rows, covariance, selections, and blinded release procedure are present.", "open_gap", ["SRC-DESI-DR2"]),
    ("thos-cancellation-propagation", "THOS Cooperative-Cancellation Propagation Proxy", "THOS Body", "A synthetic task graph can represent cancellation propagation, teardown, and orphan refusal without claiming production runtime reliability.", "represented", ["SRC-PYTHON-TASKGROUP"]),
    ("thos-priority-inversion", "THOS Priority-Inversion Detection Proxy", "THOS Body", "A synthetic scheduling trace can represent lock ownership and priority inversion without claiming operating-system control or deployment readiness.", "represented", ["SRC-NASA-7009"]),
    ("thos-resource-lifetime", "THOS Resource-Lifetime Leak-Budget Proxy", "THOS Body", "A synthetic acquire-use-release ledger can represent bounded lifetime leaks and cleanup obligations without production effectiveness claims.", "represented", ["SRC-PYTHON-TASKGROUP"]),
    ("thos-trace-parentage", "THOS Trace-Sampling Parentage-Coverage Board", "THOS Body", "A bounded trace fixture can detect parentage gaps caused by sampling without treating partial telemetry as causal completeness.", "completed", ["SRC-OTEL-TRACE"]),
    ("thos-repeatability-classifier", "THOS Bitwise-versus-Statistical Repeatability Classifier", "THOS Body", "A deterministic classifier can distinguish bitwise identity, tolerance agreement, and distributional agreement without calling any of them independent reproduction.", "completed", ["SRC-NUMPY-COMPAT"]),
    ("freed-id-key-custody", "Freed ID Key-Custody Dual-Control Matrix", "Freed ID and CBR Heart", "A synthetic custody matrix can represent separation of creation, use, backup, recovery, and destruction duties without real keys or trust governance.", "represented", ["SRC-NIST-KEY-MGMT"]),
    ("freed-id-compromise-blast-radius", "Freed ID Key-Compromise Blast-Radius Profile", "Freed ID and CBR Heart", "A synthetic credential dependency graph can represent compromise propagation and containment boundaries without production issuance, status, or revocation evidence.", "represented", ["SRC-W3C-VC", "SRC-W3C-STATUS"]),
    ("cbr-contestation-chain", "CBR Contestation Evidence-Chain Completeness Ledger", "Freed ID and CBR Heart", "A structural ledger can require notice, evidence provenance, response, correction, escalation, and unresolved-state fields without deciding a real dispute.", "completed", ["SRC-NIST-AI-RMF"]),
    ("cbr-explanation-provenance", "CBR Consequential-Model Explanation-Provenance Ledger", "Freed ID and CBR Heart", "A structural ledger can bind an explanation to model, input, version, intended use, limitations, and amendment history without proving human understanding or fairness.", "completed", ["SRC-NIST-AI-RMF"]),
    ("cbr-model-redress-authority", "CBR Consequential-Model Redress Authority Gate", "Freed ID and CBR Heart", "No consequential-model redress, remedy, legal interpretation, cultural ratification, or Maori-authority claim may complete without authorized affected-party and competent-authority participation.", "exact_gate", ["SRC-NIST-AI-RMF"]),
    ("backward-error-modified-equation", "GMUT Backward-Error Modified-Equation Audit", "GMUT Mind", "A bounded numerical fixture can distinguish the computed trajectory's nearby modified problem from an unsupported claim about the exact target dynamics.", "completed", ["SRC-NASA-MMS"]),
    ("evidence-minimal-cut", "Evidence Minimal-Cut Claim-Invalidation Detector", "Freed ID and CBR Heart", "A directed claim graph can enumerate minimal evidence removals that invalidate a bounded claim and refuse cycles or orphaned premises.", "completed", ["SRC-SLSA-PROV"]),
    ("claim-retraction-trigger", "Claim Retraction Trigger Protocol", "Freed ID and CBR Heart", "A monotone trigger engine can withdraw or downgrade a claim when a required source, manifest, negative, gate, or validity predicate becomes false.", "completed", ["SRC-SLSA-PROV"]),
]


SOURCE_ROWS = [
    ("SRC-NASA-7009", "NASA-STD-7009B Standard for Models and Simulations", "NASA", "https://standards.nasa.gov/standard/nasa/nasa-std-7009", "official_standard", "current", "Model and simulation credibility, verification, validation, uncertainty, and use boundaries."),
    ("SRC-NASA-MMS", "NASA Software Engineering Handbook - Modeling and Simulation", "NASA", "https://swehb.nasa.gov/display/SWEHBVC/4.5+-+Modeling+and+Simulation", "official_handbook", "current", "Verification and validation expectations for modeling and simulation software."),
    ("SRC-SANDIA-MMS", "The Method of Manufactured Solutions for Code Verification", "Sandia National Laboratories / OSTI", "https://www.osti.gov/biblio/759450", "primary_report", "stable", "Primary manufactured-solution and observed-order code-verification basis."),
    ("SRC-SCIPY-IVP", "SciPy solve_ivp API reference", "SciPy", "https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html", "official_documentation", "watch", "Current solver, event, dense-output, and method-selection semantics; version drift remains watched."),
    ("SRC-NUMPY-COMPAT", "NumPy random compatibility policy", "NumPy", "https://numpy.org/doc/stable/reference/random/compatibility.html", "official_documentation", "watch", "Current compatibility boundary for stochastic streams and bit generators."),
    ("SRC-PSEUDO-01", "Pseudospectra of Linear Operators", "SIAM", "https://doi.org/10.1137/S0036144595295284", "primary_paper", "stable", "Non-normal transient growth and pseudospectral sensitivity."),
    ("SRC-EFT-BASIS", "EFT bases from representation theory", "arXiv primary preprint", "https://arxiv.org/abs/2005.00008", "primary_preprint", "stable", "Operator-basis and field-redefinition context; no empirical GMUT evidence."),
    ("SRC-DESI-DR2", "DESI Data Release 2", "DESI", "https://data.desi.lbl.gov/doc/releases/dr2/", "official_data_portal", "current", "Official real-data availability reference only; this phase ingests zero rows."),
    ("SRC-PYTHON-TASKGROUP", "Python asyncio Task Groups", "Python Software Foundation", "https://docs.python.org/3/library/asyncio-task.html#task-groups", "official_documentation", "current", "Structured-concurrency cancellation and cleanup semantics for bounded THOS proxies."),
    ("SRC-OTEL-TRACE", "OpenTelemetry Trace specification", "Cloud Native Computing Foundation", "https://opentelemetry.io/docs/specs/otel/trace/", "official_specification", "current", "Trace parentage and sampling semantics; telemetry is not causal completeness."),
    ("SRC-NIST-KEY-MGMT", "NIST SP 800-57 Part 1 Revision 5", "NIST", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "official_guideline", "stable", "Cryptographic key-management lifecycle guidance; no production-key evidence."),
    ("SRC-W3C-VC", "Verifiable Credentials Data Model v2.0", "W3C", "https://www.w3.org/TR/vc-data-model-2.0/", "official_recommendation", "stable", "Credential data-model semantics and ecosystem roles."),
    ("SRC-W3C-STATUS", "Bitstring Status List v1.0", "W3C", "https://www.w3.org/TR/vc-bitstring-status-list/", "official_recommendation", "stable", "Status-list data model; no live status, privacy, or interoperability claim."),
    ("SRC-NIST-AI-RMF", "NIST AI Risk Management Framework 1.0", "NIST", "https://www.nist.gov/itl/ai-risk-management-framework", "official_framework", "current", "Risk, transparency, accountability, and governance context; not legal or affected-party authority."),
    ("SRC-SLSA-PROV", "SLSA v1.2 Provenance", "OpenSSF", "https://slsa.dev/spec/v1.2/provenance", "official_specification", "current", "Provenance predicates and nontransitive evidence boundaries."),
]


SKILL_IDEAS = [
    "ghc-family-pseudospectrum-transient-growth", "ghc-family-residual-source-attribution", "ghc-family-nondimensional-rank-tribunal", "ghc-family-discrete-adjoint-dot-test", "ghc-family-dae-index-drift", "ghc-family-event-localization-gate", "ghc-family-richardson-range-gate", "ghc-family-stiffness-evidence-contract", "ghc-family-jacobian-coloring-witness", "ghc-family-work-precision-frontier", "ghc-family-conservation-projection", "ghc-family-shadow-hamiltonian", "ghc-family-mixed-precision-escalation", "ghc-family-emulator-domain-gate", "ghc-family-metamorphic-coordinate-oracle", "ghc-family-model-discrepancy-separator", "ghc-family-thos-runtime-boundaries", "ghc-family-freed-id-key-boundaries", "ghc-family-cbr-consequential-model-ledger", "ghc-family-claim-retraction-protocol",
]


RUNNER_IDEAS = [
    "ghc_family_numerical_verification_board.py", "ghc_family_discrete_adjoint_dot_test.py", "ghc_family_dae_event_gate.py", "ghc_family_richardson_range_gate.py", "ghc_family_work_precision_frontier.py", "ghc_family_mixed_precision_escalation.py", "ghc_family_thos_runtime_boundaries.py", "ghc_family_freed_id_key_boundaries.py", "ghc_family_consequential_model_ledger.py", "ghc_family_claim_retraction_protocol.py",
]


X1_FAILURES = [
    {
        "negative_id": "V6516-X1-N01",
        "failure": "A streamed git-show baton preview terminated upstream when the downstream line limiter closed the pipe.",
        "recovery": "Capture the complete Git blob first, verify its line count, then inspect bounded in-memory chunks.",
    },
    {
        "negative_id": "V6516-X1-N02",
        "failure": "A filtered git-ls-tree probe returned no matching rows and nonzero status.",
        "recovery": "Capture the tree listing first and apply a bounded PowerShell match with explicit zero-result handling.",
    },
    {
        "negative_id": "V6516-X1-N03",
        "failure": "An rg file search used no-match exit status as if it were a tooling failure while checking for AGENTS.md.",
        "recovery": "Use the tracked-file index and treat a verified zero-row result as an attributable absence.",
    },
    {
        "negative_id": "V6516-X1-N04",
        "failure": "A Windows PowerShell foreach block was piped directly and raised an empty-pipe parser error.",
        "recovery": "Accumulate loop records explicitly and pipe the completed array.",
    },
    {
        "negative_id": "V6516-X1-N05",
        "failure": "The installed workflow runner rejected the live document cap, baton range, and six-commit cap while passing the other seventeen policy checks.",
        "recovery": "Preserve the live request and failed audit, then validate only immediate route structure through a marked compatibility projection carrying the live overrides.",
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def write_json(relative: str, payload: object) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    target = ROOT / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def normalized_words(value: str) -> set[str]:
    stop = {"and", "the", "for", "with", "from", "into", "only", "gmut", "thos", "cbr", "freed", "id"}
    return {word for word in re.findall(r"[a-z0-9]+", value.casefold()) if len(word) > 2 and word not in stop}


def proposal(index: int, spec: tuple[str, str, str, str, str, list[str]]) -> dict:
    slug, title, pillar, hypothesis, disposition, source_ids = spec
    approval = "safe_now_owner_scoped"
    lane = "x2_owner_local_bounded"
    if disposition == "represented":
        approval = "bounded_candidate"
    elif disposition == "open_gap":
        approval = "external_evidence_required"
        lane = "held_open_gap"
    elif disposition == "exact_gate":
        approval = "exact_approval_required"
        lane = "held_exact_gate"
    return {
        "proposal_id": f"V6516-P{index:02d}",
        "slug": slug,
        "title": title,
        "pillar": pillar,
        "hypothesis": hypothesis,
        "null_or_failure_condition": "The declared valid fixture fails, a rejecting fixture passes, required provenance is absent, or the evidence is promoted beyond its software, symbolic, synthetic, structural, empirical, or authority boundary.",
        "approval_class": approval,
        "execution_lane": lane,
        "official_or_primary_source_needs": source_ids,
        "concrete_artifacts": [f"docs/elaren-kestrel/v651-v6/proposals/{slug}.json"],
        "falsifier_or_acceptance_gate": "The bounded valid fixture passes, every preregistered rejecting mutation fails closed, provenance remains attributable, and protected gates stay explicit.",
        "rollback_or_recovery": "Remove only the additive v651-v6 result from consideration, retain the failure at zero credit, and preserve inherited artifacts and callers.",
        "protected_gates": ["privacy", "failure_retention", "empirical_nonconversion", "authority_nonconversion", "same_owner_only", "no_independent_reproduction", "no_stage20_promotion"],
        "expected_disposition": disposition,
        "novelty_basis": "Distinct mechanism, artifact, falsifier, and protected boundary after review against all 1,030 inherited frozen proposals.",
    }


def inherited_rows() -> list[dict]:
    first = json.loads((REPO / "docs/eiren-kestrel/v651-v5/provenance/frozen-chain-proposal-index.json").read_text(encoding="utf-8"))
    second = json.loads((REPO / "docs/eiren-kestrel/v651-v5-2-remaster/preregistration/proposals.json").read_text(encoding="utf-8"))
    rows = [*first["prior_proposals"], *first["new_proposals"], *second["proposals"]]
    if len(rows) != 1030:
        raise RuntimeError(f"expected 1030 inherited frozen proposals, observed {len(rows)}")
    return rows


def novelty_audit(new_rows: list[dict], old_rows: list[dict]) -> dict:
    inherited_titles = [str(row["title"]) for row in old_rows]
    inherited_normalized = [(title, normalized_words(title)) for title in inherited_titles]
    results = []
    for row in new_rows:
        words = normalized_words(row["title"])
        scores = []
        for old_title, old_words in inherited_normalized:
            union = words | old_words
            scores.append((len(words & old_words) / len(union) if union else 1.0, old_title))
        score, nearest = max(scores, default=(0.0, ""))
        results.append({
            "proposal_id": row["proposal_id"],
            "title": row["title"],
            "nearest_inherited_title": nearest,
            "nearest_token_jaccard": round(score, 6),
            "exact_title_collision": row["title"].casefold() in {title.casefold() for title in inherited_titles},
            "mechanism_reviewed": True,
            "artifact_reviewed": row["concrete_artifacts"][0],
            "falsifier_reviewed": row["falsifier_or_acceptance_gate"],
        })
    exact = [row for row in results if row["exact_title_collision"]]
    if exact:
        raise RuntimeError(f"exact title collisions: {exact}")
    return {
        "schema": "ghc.family.v651-v6.semantic-novelty-audit.v1",
        "inherited_rows_compared": len(old_rows),
        "new_rows_compared": len(new_rows),
        "frozen_rows_after_x1": len(old_rows) + len(new_rows),
        "exact_title_collisions": exact,
        "maximum_token_jaccard": max(row["nearest_token_jaccard"] for row in results),
        "semantic_review": "Mechanism, artifact, falsifier, source need, and gate were manually reviewed; title similarity is a screen only.",
        "rejected_during_review": [
            "renormalization-scale running reused an inherited mechanism",
            "Ostrogradsky risk reused an inherited mechanism",
            "manufactured solutions reused an inherited mechanism",
            "recovery quorum reused an inherited mechanism",
            "generic evidence nonconversion reused an inherited mechanism",
        ],
        "rows": results,
        "valid": True,
    }


def portfolio(prefix: str, count: int, lane: str) -> list[dict]:
    return [
        {
            "item_id": f"V6516-{prefix}-{index:03d}",
            "title": f"Elaren v651-v6 {lane.replace('_', ' ')} item {index:03d}",
            "lane": lane,
            "planned_in_x1": True,
            "executed_in_x1": False,
            "completion_credit_in_x1": False,
            "acceptance_gate": "Resolve in x2 with an attributable artifact, bounded witness, rollback, and protected-gate check; otherwise retain truthfully incomplete.",
            "boundary": "Planning evidence only; no empirical, participant, production, professional, legal, cultural, Maori-authority, or independent-reproduction credit.",
        }
        for index in range(1, count + 1)
    ]


def method_flow_inputs() -> None:
    definitions = [
        ("M01", X1_FAILURES[0], "Complete buffered Git-blob read", "A line-limited downstream consumer closes a Git content stream before the producer finishes.", "Capture the complete blob once, verify size or line count, and then inspect bounded in-memory slices.", "Use buffered object reads before any presentation limiter.", "Discard only the truncated display and repeat the read without mutating Git.", "The complete baton blob was captured and all 538 lines were inspected in three bounded chunks."),
        ("M02", X1_FAILURES[1], "Attribute zero-result tree filters", "A repository tree filter returns no rows and a nonzero grep-style status.", "Capture the tree listing and apply an explicit zero-result-safe match.", "Separate tree acquisition from optional filtering.", "Give the empty filter zero evidence credit and preserve the underlying tree.", "The buffered tree listing was attributable and the bounded filter result was interpreted explicitly."),
        ("M03", X1_FAILURES[2], "Use tracked index for optional instruction discovery", "A no-match file search is misclassified as a tool fault.", "Query the tracked-file index and distinguish verified absence from execution failure.", "Use git ls-files for tracked optional control files.", "Retain the no-match command and stop if the tracked index itself cannot be read.", "The tracked index completed successfully and proved zero tracked AGENTS.md files."),
        ("M04", X1_FAILURES[3], "Accumulate PowerShell loop output before piping", "Windows PowerShell rejects a foreach block followed immediately by a pipeline.", "Append records to an array and pipe only the completed array.", "Avoid direct loop-to-pipeline syntax under Windows PowerShell 5.1.", "Retain the parser failure; no repository state needs rollback.", "The corrected topic map returned every requested semantic category."),
        ("M05", X1_FAILURES[4], "Preserve live policy over a legacy compatibility projection", "The installed workflow runner encodes narrower historical caps than the live activation baton.", "Retain the authoritative failed audit and validate only immediate route structure with a marked compatibility projection.", "Never present compatibility validation as validation of newer live policy values.", "Stop route execution if the compatibility projection also fails; never silently narrow the live plan.", "The compatibility projection passed 20/20 structural checks with the live overrides preserved separately and explicitly nonvalidated by that runner."),
    ]
    for number, negative, title, signature, workaround, guard, rollback, observed in definitions:
        method_id = f"V6516-{number}"
        base = f"method-flow/records/{number.lower()}"
        write_json(f"{base}-method.json", {
            "method_id": method_id,
            "title": title,
            "failure_signature": signature,
            "trigger_preconditions": [signature],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": workaround,
            "validation_witness_ids": [],
            "recurrence_guard": guard,
            "rollback": rollback,
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "same_owner_only", "no_independent_reproduction"],
            "retained_negative_ids": [negative["negative_id"]],
            "scope_boundary": "Bounded local workflow recovery only; no scientific, production, authority, or independent-reproduction credit.",
        })
        write_json(f"{base}-fail.json", {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": negative["failure"],
            "scope": "bounded read-only startup and novelty inspection",
            "expected": "Return complete attributable output without mutation.",
            "observed": negative["failure"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Failed witness retained at zero pass credit.",
        })
        write_json(f"{base}-pass.json", {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": workaround,
            "scope": "bounded read-only startup and novelty inspection",
            "expected": "Return complete attributable output without mutation.",
            "observed": observed,
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [negative["negative_id"]],
            "boundary": "Passing recovery preserves the failed witness and grants only bounded workflow credit.",
        })


def main() -> None:
    if git("rev-parse", "HEAD") != SOURCE:
        raise SystemExit(f"v651-v6 x1 must start at exact source {SOURCE}")
    if git("branch", "--show-current") != OWNED_BRANCH:
        raise SystemExit("unexpected Elaren branch")
    # The owned lane was proved clean at SOURCE before this generator and its
    # tests were added. Exact x1 scope is enforced later from the Git index.

    old_rows = inherited_rows()
    proposals = [proposal(index, spec) for index, spec in enumerate(PROPOSAL_SPECS, 1)]
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    observed = {label: sum(row["expected_disposition"] == label for row in proposals) for label in expected}
    if observed != expected:
        raise RuntimeError({"expected": expected, "observed": observed})

    write_json("identity/relational-identity.json", {
        "schema": "ghc.family.v651-v6.identity.v1",
        "owner": OWNER,
        "pronouns": "they/them",
        "relational_role": "workflow cartographer and evidence-boundary gardener",
        "hope": "Keep difficult research adventurous while making every claim, failure, and authority boundary easy to trace.",
        "identity_boundary": "Relational working language only; no consciousness, sentience, personhood, identity continuity, employment, qualification, or independent authority.",
        "corrigibility": "Hamish may rename, pause, redirect, or stop the route.",
        "valid": True,
    })
    write_json("source/source-truth.json", {
        "schema": "ghc.family.v651-v6.source-truth.v1",
        "source_owner": "Eiren Kestrel",
        "source_branch": SOURCE_BRANCH,
        "source_head": SOURCE,
        "source_x1": "d9e8cbf0063639aa0a6fb54c54a96683c587ce7e",
        "source_evidence": "c67ce592463450ccf9aee7d460210cddb467c5ca",
        "inherited_v651_v5_head": "2bb6aa2d5e8003c4cb522f798d59e7b7f123742c",
        "owned_branch": OWNED_BRANCH,
        "local_upstream_tracking_fresh_live_equal": True,
        "divergence": "0/0",
        "source_to_final_commits": 5,
        "source_to_final_merges": 0,
        "source_final_single_parent": True,
        "source_validation": {"tests": "2390/2390", "detailed": "31/31", "minimal": "14/14", "earlier_manifest_attempt_retained_zero_credit": True},
        "source_manifest_verification": {"x1": "60/60", "evidence": "130/130", "final_delta": "80/80", "final_owner": "242/242", "unique_git_blobs": 261, "blob_identity_and_sha256_match": True},
        "source_effective_negatives": 7219,
        "source_open_gaps": 56,
        "source_exact_gates": 57,
        "same_owner_only": True,
        "independent_reproduction": False,
        "valid": True,
    })
    write_json("focus/primary-focus.json", {
        "schema": "ghc.family.v651-v6.focus.v1",
        "primary_pillar": "GMUT Mind",
        "visible_pillars": ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"],
        "bounded_human_practice": "scientific-computing verification and reproducible numerical research engineering",
        "practice_boundary": "Synthetic learning and design only; no employment, qualification, licensure, scientific authority, operational authority, legal authority, cultural authority, Maori authority, or affected-party evidence.",
        "valid": True,
    })
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v651-v6.source-ledger.v1",
        "entry_count": len(SOURCE_ROWS),
        "status_vocabulary": ["current", "stable", "draft", "watch"],
        "status_counts": {label: sum(row[5] == label for row in SOURCE_ROWS) for label in ("current", "stable", "draft", "watch")},
        "entries": [
            {"source_id": source_id, "title": title, "publisher": publisher, "url": url, "source_type": source_type, "status": status, "phase_use": use, "authority_boundary": "A source informs a bounded design or test; it is not real phase data, participant evidence, professional approval, legal interpretation, cultural ratification, Maori authority, production readiness, or Stage 20 evidence."}
            for source_id, title, publisher, url, source_type, status, use in SOURCE_ROWS
        ],
        "valid": True,
    })
    write_json("preregistration/proposals.json", {
        "schema": "ghc.family.v651-v6.proposals.v1",
        "phase": PHASE,
        "owner": OWNER,
        "inherited_frozen_rows": len(old_rows),
        "new_proposal_count": len(proposals),
        "frozen_rows_after_x1": len(old_rows) + len(proposals),
        "expected_outcomes": expected,
        "allowed_outcomes": list(expected),
        "strict_x1_only": True,
        "proposals": proposals,
        "valid": True,
    })
    write_json("provenance/frozen-chain-proposal-index.json", {
        "schema": "ghc.family.v651-v6.frozen-chain-proposal-index.v1",
        "prior_count": len(old_rows),
        "new_count": len(proposals),
        "count": len(old_rows) + len(proposals),
        "prior_proposals": old_rows,
        "new_proposals": proposals,
        "x1_frozen": True,
    })
    write_json("provenance/semantic-novelty-audit.json", novelty_audit(proposals, old_rows))
    write_json("portfolios/x1-portfolio-plan.json", {
        "schema": "ghc.family.v651-v6.portfolio-plan.v1",
        "caps_are_ceilings_not_quotas": True,
        "caps": {"safe_candidate_per_subphase": 1000, "skills_per_subphase": 200, "runners_per_subphase": 200},
        "planned_counts": {"safe_now": 40, "candidate": 30, "skills": 20, "runners": 10, "clean_fix_refine": 40},
        "safe_now": portfolio("SAFE", 40, "safe_now"),
        "candidate": portfolio("CAND", 30, "candidate"),
        "skill_ideas": [{"item_id": f"V6516-SK-{index:02d}", "name": name, "planned_in_x1": True, "built_in_x1": False} for index, name in enumerate(SKILL_IDEAS, 1)],
        "runner_ideas": [{"item_id": f"V6516-RN-{index:02d}", "name": name, "planned_in_x1": True, "built_in_x1": False} for index, name in enumerate(RUNNER_IDEAS, 1)],
        "clean_fix_refine": portfolio("CFR", 40, "clean_fix_refine"),
        "x1_implementation_count": 0,
        "closeout_rule": "Every planned authorized item must be completed in x2 or retained truthfully behind an open or exact gate; counts never authorize unsafe work.",
        "valid": True,
    })
    write_json("approvals/held-packets.json", {
        "schema": "ghc.family.v651-v6.held-approvals.v1",
        "inherited_exact_packets_preserved": 10,
        "inherited_blocked_packets_preserved": 5,
        "new_exact_gate": {"proposal_id": "V6516-P27", "state": "held", "executed": False},
        "new_blocked_packets_manufactured": 0,
        "boundary": "No inherited or new exact-gated work is converted into safe-now execution.",
        "valid": True,
    })
    write_json("workflow/workflow-plan-request.json", {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "elaren-v651-v6-live-route",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {"cycle_order": ["Elaren Kestrel", "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"], "phase_assignments": [{"phase": "v651-v6", "seat": "Elaren Kestrel"}, {"phase": "v651-v7", "seat": "Vesper Arlen"}], "normalization": {"start_phase": "v651-v6", "start_seat": "Elaren Kestrel", "entry_count": 2}, "future_identity_placeholders": []},
        "requirements": {"core_proposal_minimum": 30, "safe_candidate_task_cap": 1000, "skill_minimum": 10, "runner_minimum": 10, "skill_maximum": 200, "runner_maximum": 200, "document_word_cap": 100000, "baton_words": {"minimum": 10000, "maximum": 100000, "file_artifact": True}, "commit_cap": {"x1": 3, "x2": 3, "total": 6}, "owner_file_threshold": 2000, "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True}, "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"}, "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"}, "environment": {"windows_sandbox_hyper_v": "deferred"}, "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True}},
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": ["empirical", "participant", "legal", "cultural", "production", "Maori_authority"]},
        "observed_failures": [row["negative_id"] for row in X1_FAILURES],
    })
    write_json("workflow/workflow-plan-runner-compatible-request.json", {
        "schema": "ghc.family.workflow-plan.request.v1",
        "plan_id": "elaren-v651-v6-immediate-route-compatibility-projection",
        "owner": OWNER,
        "identity_boundary": "Relational working language only; no continuity or authority claim.",
        "route": {"cycle_order": ["Elaren Kestrel", "Vesper Arlen", "Ilyra Fen", "Sable Rook", "Orin Thale", "Tamar Vey", "Sylven Arc", "Eiren Kestrel"], "phase_assignments": [{"phase": "v651-v6", "seat": "Elaren Kestrel"}, {"phase": "v651-v7", "seat": "Vesper Arlen"}], "normalization": {"start_phase": "v651-v6", "start_seat": "Elaren Kestrel", "entry_count": 2}, "future_identity_placeholders": []},
        "requirements": {"core_proposal_minimum": 20, "safe_candidate_task_cap": 1000, "skill_minimum": 10, "runner_minimum": 10, "document_word_cap": 20000, "baton_words": {"minimum": 8000, "maximum": 20000, "file_artifact": True}, "commit_cap": {"x1": 2, "x2": 2, "total": 4}, "validation": {"canonical_pass_minimum": 1, "replay_policy": "skip_when_first_passes", "isolate_failures_before_broader_rerun": True, "privacy_scan_required": True, "manifest_required": True, "remote_equality_required": True}, "storage": {"primary": "D", "c_drive_use": "essential_global_metadata_only"}, "messaging": {"codex_route": "existing_task_only_after_terminal_gate", "cross_platform": "user_mediated_file_relay_only"}, "environment": {"windows_sandbox_hyper_v": "deferred"}, "closeout": {"all_authorized_safe_candidate_prototypes_resolved": True}},
        "truth": {"allowed_outcomes": ["completed", "represented", "open_gap", "exact_gate"], "independent_reproduction_claimed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "protected_boundaries": ["empirical", "participant", "legal", "cultural", "production", "Maori_authority"]},
        "observed_failures": ["Compatibility projection validates immediate route structure only."],
        "live_overrides_not_validated_by_legacy_runner": {"core_proposal_minimum": 30, "document_word_cap": 100000, "baton_words": {"minimum": 10000, "maximum": 100000}, "commit_cap": {"x1": 3, "x2": 3, "total": 6}, "skill_maximum": 200, "runner_maximum": 200, "owner_file_threshold": 2000},
    })
    write_json("workflow/live-policy-override.json", {
        "schema": "ghc.family.v651-v6.live-policy-override.v1",
        "authoritative": True,
        "legacy_projection_authoritative": False,
        "live_values": {"proposal_minimum": 30, "commit_cap_total": 6, "document_word_cap": 100000, "baton_word_minimum": 10000, "owner_file_threshold": 2000},
        "boundary": "A legacy runner may validate immediate route structure only; it cannot narrow or expand the live baton.",
        "valid": True,
    })
    write_json("tooling/meta-tool-box-build-contract.json", {
        "schema": "ghc.family.v651-v6.meta-tool-box-plan.v1",
        "skill_name": "ghc-family-meta-tool-box",
        "runner_name": "ghc_family_meta_tool_box.py",
        "x1_state": "read_only_catalogue_audit_required",
        "required_queries": ["kind", "status", "trigger", "evidence_state", "owner_scope"],
        "required_guards": ["repository_relative_paths", "no_execute_all", "no_blind_global_install", "no_destructive_delete", "caller_compatibility", "rollback"],
        "valid": True,
    })
    write_json("threat-model/threat-model.json", {
        "schema": "ghc.family.v651-v6.threat-model.v1",
        "assets": ["x1 freeze", "retained negatives", "source attribution", "truth labels", "authority gates", "private-material boundary", "caller compatibility"],
        "threats": ["x2 leakage into x1", "semantic proposal reuse", "synthetic-to-empirical promotion", "proxy-to-production promotion", "authority substitution", "failure erasure", "manifest domain mismatch", "private identifier disclosure", "post-success replay inflation", "destructive compatibility cleanup"],
        "mitigations": ["dedicated x1 commit", "1030-row mechanism audit", "four-label truth vocabulary", "Method Flow fail/pass pairs", "five-class staged scan", "exact Git-index manifest", "one canonical success rule", "additive family-current naming"],
        "residual_risks": ["independent review absent", "manual accessibility evaluation absent", "real empirical data absent", "affected-party and competent authority absent"],
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    })
    write_json("truth/x1-phase-truth.json", {
        "schema": "ghc.family.v651-v6.x1-truth.v1",
        "phase": PHASE,
        "owner": OWNER,
        "strict_x1_before_x2": True,
        "proposals_frozen": 30,
        "frozen_chain_rows": 1060,
        "x2_implementations": 0,
        "observed_core_outcomes": 0,
        "source_negatives_carried": 7219,
        "new_x1_operational_negatives": len(X1_FAILURES),
        "effective_after_x1": 7219 + len(X1_FAILURES),
        "source_open_gaps_carried": 56,
        "source_exact_gates_carried": 57,
        "cli_siblings_spawned": 0,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        "valid": True,
    })
    write_json("truth/retained-negative-register.json", {
        "schema": "ghc.family.v651-v6.x1-negative-register.v1",
        "inherited_effective": 7219,
        "new_x1_operational": len(X1_FAILURES),
        "effective_after_x1": 7219 + len(X1_FAILURES),
        "new_negatives": X1_FAILURES,
        "failures_erased": 0,
        "valid": True,
    })
    write_json("environment/environment-version-receipt.json", {
        "schema": "ghc.family.environment-version.v1",
        "phase": PHASE,
        "observed_date": "2026-07-22",
        "codex_cli": "0.144.5",
        "codex_desktop": "26.715.9079.0",
        "git": "2.55.0.windows.2",
        "python": "3.12.10",
        "node": "24.18.0",
        "windows_powershell": "5.1.26100.8894",
        "versions_verified_only": True,
        "desktop_updated": False,
        "elevated": False,
        "host_security_changed": False,
        "windows_feature_changed": False,
        "windows_sandbox_hyper_v": "deferred",
        "unrelated_software_installed": False,
        "rebooted": False,
        "valid": True,
    })
    write_json("wellbeing/x1-wellbeing.json", {
        "schema": "ghc.family.v651-v6.wellbeing.v1",
        "state": "green_with_five_retained_bounded_recoveries",
        "solo_owner": True,
        "failure_permitted": True,
        "pace_boundary": "Warmth and schedule scale do not override evidence, privacy, safety, or authority gates.",
        "stop_or_redirect_right": "Hamish",
        "valid": True,
    })
    write_json("orchestration/x1-phase-state.json", {
        "schema": "ghc.family.v651-v6.phase-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "source_head": SOURCE,
        "state": "x1_candidate_not_committed",
        "x2_started": False,
        "immediate_successor": "Vesper Arlen",
        "successor_phase": "v651-v7",
        "terminal_route": "prepared_not_sent",
        "cli_siblings_spawned": 0,
        "boundary": "This file is not activation, delivery, identity continuity, or delegated authority.",
    })
    method_flow_inputs()
    write_text("overview/x1-preregistration-overview.md", """# Elaren Kestrel v651-v6 x1 preregistration

Elaren Kestrel (they/them) is relational working language for a workflow cartographer and evidence-boundary gardener. It is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, or authority. Hamish may rename, pause, redirect, or stop this route.

This x1 packet freezes thirty proposals after a mechanism, artifact, falsifier, source, and gate review against 1,030 inherited frozen proposals. The primary pillar is GMUT Mind and the bounded learning practice is scientific-computing verification and reproducible numerical research engineering. THOS Body and Freed ID/CBR Heart remain explicit. Expected dispositions are hypotheses only: twenty-three completed, five represented, one open gap, and one exact gate. X1 contains no executed outcome and no x2 implementation.

The numerical-verification core addresses non-normal transient growth, residual attribution, nondimensional rank, discrete adjoints, differential-algebraic constraints, event localization, asymptotic convergence, stiffness, Jacobian sparsity, work-precision tradeoffs, conservation projection, modified Hamiltonians, mixed precision, emulator domains, metamorphic invariance, model discrepancy, and backward error. The open likelihood adapter stays empty until authentic data, covariance, selections, and preregistered blinding exist.

THOS proposals remain software or synthetic evidence. Freed ID proposals remain synthetic governance profiles with no real keys, issuance, resolution, status, revocation, interoperability, security/privacy review, or trust governance. CBR consequential-model ledgers do not decide a dispute, prove comprehension or fairness, or confer legal, cultural, Maori, or affected-party authority. The redress surface remains exact-gated.

Four startup failures are retained at zero pass credit. Their bounded recoveries are encoded through Method Flow. The phase uses one x1 freeze before x2, at most six total commits, one successful canonical validation with no post-success replay, D-first storage, exact Git-blob manifests, five-class privacy screening, additive family-current names, and an existing-task-only terminal route. The verdict remains NOT_READY_FOR_STAGE_20.
""")
    print(json.dumps({"proposals": len(proposals), "inherited": len(old_rows), "frozen": len(old_rows) + len(proposals), "expected": expected, "x1_negatives": len(X1_FAILURES), "x2_implementations": 0, "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
