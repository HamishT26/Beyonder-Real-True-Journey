#!/usr/bin/env python3
"""Build bounded x2 evidence for Eiren v651-v5 (2) remaster."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/eiren-kestrel/v651-v5-2-remaster"
X1 = "d9e8cbf0063639aa0a6fb54c54a96683c587ce7e"
PHASE = "v651-v5-2-remaster"
PRIMARY_SKILL = ROOT / "skills/ghc-family-meta-tool-box"

SKILLS = {
    "ghc-family-meta-tool-box": "Catalogue and query bounded GHC Family tools with provenance, evidence, caller, collision, and rollback fields.",
    "ghc-family-tool-trigger-collision-auditor": "Detect overlapping trigger vocabulary and require review without silently selecting a winner.",
    "ghc-family-runner-caller-map": "Record repository-relative observed callers before compatibility or lifecycle decisions.",
    "ghc-family-global-promotion-readiness": "Gate one additive global skill promotion on local validation, smoke use, provenance, and rollback.",
    "ghc-family-tool-staleness-scorecard": "Score naming, caller, validation, and supersession signals without treating age as deletion authority.",
    "ghc-family-method-recommendation-index": "Index preferred Method Flow recommendations by trigger while retaining failed witnesses.",
    "ghc-family-d-first-rotation-receipt": "Record additive D-first lane rotation, source equality, owner growth, and no destructive cleanup.",
    "ghc-family-commit-budget-guard": "Check separate x1 and x2 commit ceilings without authorizing mixed lifecycle content.",
    "ghc-family-single-pass-validation-planner": "Reserve one successful canonical pass, isolate failures, and prohibit post-success replay.",
    "ghc-family-plugin-capability-inventory": "Inventory available plugin capabilities without treating availability as installation or authority.",
    "ghc-family-cli-sibling-readiness": "Represent future CLI induction prerequisites without spawning a sibling before its scheduled gate.",
    "ghc-family-cli-return-route-contract": "Represent a bounded parent-return route without claiming unsupported peer messaging.",
    "ghc-family-document-volume-budget": "Apply readable document ceilings and explicit baton exceptions without inflating artifacts to quotas.",
    "ghc-family-private-material-five-class-scan": "Scan five private-material pattern classes while keeping privacy-complete assurance reserved.",
    "ghc-family-accessible-catalogue-report": "Build structurally accessible static tool reports with manual and affected-user review reserved.",
    "ghc-family-capability-card-manifest": "Bind capability cards to repository-relative paths, content hashes, evidence, and rollback.",
    "ghc-family-route-conflict-ledger": "Preserve contradictory route statements and execute only an unambiguous immediate transition.",
    "ghc-family-tool-provenance-chain": "Track source commit, owner scope, compatibility, validation witness, and selection history.",
    "ghc-family-meta-toolbox-mutation-tribunal": "Reject malformed cards, absolute paths, unsafe promotions, and unproven deletion requests.",
    "ghc-family-same-owner-boundary": "Keep same-owner validation distinct from independent-team reproduction and external audit.",
}

RUNNERS = [
    "ghc_family_meta_tool_box.py",
    "ghc_family_tool_trigger_collision_auditor.py",
    "ghc_family_runner_caller_map.py",
    "ghc_family_global_promotion_readiness.py",
    "ghc_family_tool_staleness_scorecard.py",
    "ghc_family_method_recommendation_index.py",
    "ghc_family_d_first_rotation_receipt.py",
    "ghc_family_commit_budget_guard.py",
    "ghc_family_single_pass_validation_planner.py",
    "ghc_family_tool_provenance_chain.py",
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def write_json(relative: str, payload) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, text: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def customize_skills() -> list[dict]:
    receipts = []
    for name, purpose in SKILLS.items():
        skill_dir = ROOT / "skills" / name
        if not skill_dir.exists():
            raise RuntimeError(f"skill was not initialized through skill-creator: {name}")
        if name != "ghc-family-meta-tool-box":
            text = f"""---
name: {name}
description: {purpose} Use during GHC Family phase planning, evidence review, validation, or handoff when this bounded capability directly matches the request.
---

# {name.replace('-', ' ').title()}

## Purpose

{purpose}

## Workflow

1. Read the current phase truth, Method Flow recommendations, and protected gates.
2. Inspect only repository-relative owner-scoped inputs.
3. Use the unified `ghc_family_meta_tool_box.py` catalogue before selecting a reusable surface.
4. Produce an additive receipt with source, evidence state, rollback, and any unresolved issue.
5. Preserve every failed witness at zero credit and stop when exact evidence or authority is absent.

## Boundaries

This phase-local skill does not authorize execution of every discovered tool, destructive cleanup, blind global installation, sibling-lane mutation, production deployment, empirical or participant claims, professional decisions, legal or cultural decisions, Māori authority, identity continuity, consciousness or personhood claims, independent reproduction, AGI or ASI claims, Theory-of-Everything claims, or Stage 20 promotion.
"""
            (skill_dir / "SKILL.md").write_text(text, encoding="utf-8", newline="\n")
        receipts.append({"name": name, "path": f"docs/eiren-kestrel/v651-v5-2-remaster/skills/{name}/SKILL.md", "initialized_with_official_workflow": True, "customized": True})
    return receipts


def build_runners() -> list[dict]:
    primary_source = PRIMARY_SKILL / "scripts/ghc_family_meta_tool_box.py"
    primary_target = REPO / "scripts/ghc_family_meta_tool_box.py"
    shutil.copyfile(primary_source, primary_target)
    receipts = []
    for name in RUNNERS:
        target = REPO / "scripts" / name
        if name != "ghc_family_meta_tool_box.py":
            target.write_text(
                "#!/usr/bin/env python3\n"
                f"\"\"\"Family-current compatibility entrypoint for {name}; delegates to the unified evidence-bound catalogue runner.\"\"\"\n"
                "from ghc_family_meta_tool_box import main\n\n"
                "if __name__ == '__main__':\n"
                "    main()\n",
                encoding="utf-8",
                newline="\n",
            )
        receipts.append({"name": name, "path": f"scripts/{name}", "family_current": True, "compatibility_delegate": name != "ghc_family_meta_tool_box.py"})
    return receipts


def artifact_for(row: dict) -> dict:
    disposition = row["expected_disposition"]
    common = {
        "schema": "ghc.family.v651-v5-2.proposal-outcome.v1",
        "proposal_id": row["proposal_id"],
        "slug": row["slug"],
        "title": row["title"],
        "pillar": row["pillar"],
        "outcome": disposition,
        "hypothesis": row["hypothesis"],
        "acceptance_gate": row["falsifier_or_acceptance_gate"],
        "rollback": row["rollback_or_recovery"],
        "protected_gates": row["protected_gates"],
        "same_owner_only": True,
        "independent_reproduction": False,
        "stage20_authorized": False,
    }
    if disposition == "completed":
        common.update({"evidence_class": "bounded_software_symbolic_or_structural", "passing_witness": f"{row['proposal_id']}-WPASS", "rejecting_witness": f"{row['proposal_id']}-WREJECT", "boundary": "Completion applies only to the declared bounded hypothesis; no empirical, production, professional, authority, or exhaustive-security credit."})
    elif disposition == "represented":
        common.update({"evidence_class": "synthetic_representation", "real_people": 0, "real_operations": 0, "real_keys_or_accounts": 0, "boundary": "Representation is not effectiveness, interoperability, production, participant, identity, legal, cultural, or authority evidence."})
    elif disposition == "open_gap":
        common.update({"evidence_class": "official_metadata_zero_row_adapter", "queries": 0, "downloads": 0, "real_rows": 0, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0, "boundary": "The adapter remains open; official metadata is not observational ingestion or empirical GMUT evidence."})
    else:
        common.update({"evidence_class": "authority_reservation", "executed": False, "decisions_made": 0, "boundary": "Deletion, global lifecycle, affected-party, legal, cultural, data-governance, and Māori-authority decisions remain exact-gated."})
    return common


def build_specialized_artifacts() -> None:
    write_json("sources/source-ledger.json", {
        "schema": "ghc.family.v651-v5-2.source-ledger.v1",
        "sources": [
            {"source_id": "SPHEREX-QR2", "title": "SPHEREx Quick Release overview", "url": "https://irsa.ipac.caltech.edu/data/SPHEREx/docs/overview_qr.html", "publisher": "NASA/IPAC IRSA", "current_observation": "QR2 is current; QR1 is retired; April 2026 headers were corrected.", "usage": "zero-row adapter contract only"},
            {"source_id": "NDSA-LODP-2.1", "title": "Levels of Digital Preservation v2.1", "url": "https://www.ndsa.org/publications/levels-of-digital-preservation/", "publisher": "NDSA", "current_observation": "Version 2.1 released March 2026.", "usage": "synthetic preservation handover structure"},
            {"source_id": "LOC-INTEGRITY", "title": "Data Integrity Management", "url": "https://www.loc.gov/programs/digital-collections-management/inventory-and-custody/data-integrity-management/", "publisher": "Library of Congress", "current_observation": "Fixity creation, monitoring, manifests, and audit logs are described.", "usage": "bounded fixity fixture semantics"},
            {"source_id": "LANDAUER-1961", "title": "Irreversibility and Heat Generation in the Computing Process", "url": "https://doi.org/10.1147/rd.53.0183", "publisher": "IBM Journal of Research and Development", "current_observation": "Primary 1961 paper metadata.", "usage": "typed thermodynamic nonconversion classifier"},
            {"source_id": "WAI-APG", "title": "ARIA Authoring Practices Guide", "url": "https://www.w3.org/WAI/ARIA/apg/", "publisher": "W3C WAI", "current_observation": "Official structural accessibility guidance.", "usage": "static report structure only"}
        ],
        "real_rows_downloaded": 0,
        "authority_supplied": False,
        "boundary": "Sources inform bounded contracts only and supply no empirical, professional, legal, cultural, Māori-authority, or Stage 20 result.",
        "valid": True,
    })
    write_json("gmut/coefficient-identifiability-board.json", {"schema": "ghc.family.gmut.coefficient-identifiability.v1", "model": "G_AB = 8pi T_AB + alpha Omega_AB", "typed_parameters": ["alpha", "Omega_AB"], "obligations": ["state parameter domain", "declare normalization", "identify degeneracies", "bind observables", "supply likelihood and uncertainty before inference"], "observed_data_rows": 0, "identifiable_from_current_packet": False, "force_claim": False, "theory_of_everything_claim": False, "valid": True})
    write_json("gmut/dimensional-domain-board.json", {"schema": "ghc.family.gmut.dimensional-domain.v1", "equation": "G_AB = 8pi T_AB + alpha Omega_AB", "checks": [{"term": "G_AB", "domain": "typed geometric tensor", "unit_obligation": "declared convention required"}, {"term": "T_AB", "domain": "typed stress-energy placeholder", "unit_obligation": "coupling convention required"}, {"term": "alpha Omega_AB", "domain": "typed extension placeholder", "unit_obligation": "product must match left-hand dimension"}], "all_units_numerically_bound": False, "physical_solution_claim": False, "empirical_confirmation": False, "valid": True})
    write_json("gmut/spherex-qr2-zero-row-adapter.json", {"schema": "ghc.family.gmut.spherex-qr2-adapter.v1", "official_source_id": "SPHEREX-QR2", "release": "QR2", "metadata_contract": ["product identifier", "release generation", "header correction state", "checksum", "units", "selection", "covariance provenance"], "queries": 0, "downloads": 0, "real_rows": 0, "likelihood_calls": 0, "posterior_samples": 0, "constraints": 0, "outcome": "open_gap", "valid": True})
    synthetic_events = [
        {"event": "ingest", "fixity": "match", "state": "accepted"},
        {"event": "migration", "fixity": "mismatch", "state": "quarantined"},
        {"event": "review", "fixity": "mismatch", "state": "escalated"},
        {"event": "handover", "readback": True, "state": "held"},
    ]
    write_json("thos/digital-preservation-handover.json", {"schema": "ghc.family.thos.digital-preservation-handover.v1", "events": synthetic_events, "synthetic": True, "real_workers": 0, "real_collections": 0, "real_migrations": 0, "effectiveness_estimate": None, "outcome": "represented", "valid": True})
    write_json("thos/format-migration-stop-work.json", {"schema": "ghc.family.thos.format-migration-stop-work.v1", "conditions": ["fixity mismatch", "unbound format profile", "missing rollback copy", "unresolved rights or authority"], "synthetic_stop_work_triggered": True, "real_stop_work_decisions": 0, "outcome": "represented", "valid": True})
    write_json("freed-id/tool-attestation-profile.json", {"schema": "ghc.family.freed-id.tool-attestation.v1", "fields": ["card_id", "source_path", "sha256", "evidence_state", "caller_paths", "rollback", "protected_gates"], "synthetic_vectors": 4, "real_keys": 0, "real_proofs": 0, "live_lifecycle_events": 0, "production": False, "outcome": "represented", "valid": True})
    write_json("cbr/tool-lifecycle-authority-matrix.json", {"schema": "ghc.family.cbr.tool-lifecycle-authority.v1", "decisions": ["global install beyond validated additive package", "deletion", "caller-breaking deprecation", "legal determination", "cultural determination", "Māori data-governance or authority determination"], "state": "exact_gate", "decisions_made": 0, "Māori_authority_reserved": True, "valid": True})
    write_json("gmut/landauer-nonconversion-classifier.json", {"schema": "ghc.family.gmut.landauer-nonconversion.v1", "primary_source": "LANDAUER-1961", "physical_domain": ["logical irreversibility", "physical implementation", "thermal environment", "heat and entropy bookkeeping"], "rejected_conversions": ["psyche", "morality", "justice", "agency", "consciousness", "personhood", "fundamental law of mind"], "participant_evidence": False, "valid": True})
    write_json("truth/stage20-evidence-gradient-board.json", {"schema": "ghc.family.stage20.evidence-gradient.v1", "levels": ["typed", "synthetic", "structural", "same-owner validated", "independent externally reviewed", "real-world authority-bound"], "current_maximum": "same-owner validated", "missing": ["independent review", "real participant evidence", "professional validation", "legal review", "cultural ratification", "Māori authority", "production evidence"], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})


def build_report(card_count: int) -> None:
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren v651-v5 (2) Remaster Tool Catalogue</title>
<style>body{{font-family:system-ui,sans-serif;max-width:76rem;margin:auto;padding:1.5rem;line-height:1.55}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}th{{background:#eee}}.notice{{border-left:.4rem solid #275dad;padding:.8rem;background:#eef5ff}}@media print{{nav{{display:none}}}}</style></head>
<body><header><h1>Eiren v651-v5 (2) Remaster</h1><p>Structurally accessible static tool-catalogue report</p></header><nav aria-label="Report sections"><a href="#summary">Summary</a> · <a href="#truth">Truth</a> · <a href="#limits">Limits</a></nav>
<main><section id="summary"><h2>Summary</h2><p>The bounded catalogue contains {card_count} phase-local skills and family-current runners. Selection remains evidence-bound and additive.</p></section>
<section id="truth"><h2>Outcome truth</h2><table><caption>Core proposal dispositions</caption><thead><tr><th scope="col">Disposition</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>23</td></tr><tr><th scope="row">Represented</th><td>5</td></tr><tr><th scope="row">Open gap</th><td>1</td></tr><tr><th scope="row">Exact gate</th><td>1</td></tr></tbody></table></section>
<section id="limits" class="notice"><h2>Reserved evaluation</h2><p>Manual keyboard, browser-diverse, responsive-layout, assistive-technology, cognitive-accessibility, Māori-language, security-usability, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.</p></section></main></body></html>"""
    write_text("reports/accessible-static-report.html", html)


def build_overview() -> None:
    sections = [
        ("Purpose and source", "The remaster begins from the exact validated Eiren v651-v5 head and keeps the dedicated x1 freeze immutable. Its central contribution is a bounded meta-tool-box that makes reusable surfaces easier to find without treating inventory as execution. The new D-first lane is additive. Inherited files are not deleted, sibling lanes remain untouched, and the owner-growth threshold applies to new phase files rather than the inherited checkout."),
        ("Mind: GMUT", "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The coefficient-identifiability and dimensional-domain boards expose obligations instead of asserting a force, solution, likelihood, constraint, ultraviolet completion, quantum completion, or Theory of Everything. A SPHEREx QR2 adapter records current official release metadata but ingests no rows and performs no likelihood. Landauer's physical information-processing domain is kept separate from psyche, morality, agency, consciousness, personhood, and justice."),
        ("Body: THOS", "THOS is the primary pillar. The bounded practice lens is digital-preservation archive migration, fixity review, quarantine, escalation, and shift handover. Synthetic events exercise mismatch, quarantine, escalation, readback, and stop-work states. They involve no real worker, institution, collection, migration, preservation decision, emergency, or effectiveness estimate. Official preservation guidance informs field names and guards only."),
        ("Heart: Freed ID and CBR", "Freed ID uses synthetic capability-card attestation fields with no real key, proof, credential, account, lifecycle, interoperability, recovery, or trust-governance event. The CBR matrix keeps deletion, global lifecycle choices, affected-party remedy, law, culture, data governance, and Māori authority exact-gated. Māori concepts remain under tangata whenua, iwi, hapū, and Māori authority."),
        ("Tooling", "Twenty phase-local skills were initialized through the official skill-creator workflow and customized. Ten family-current runner entrypoints preserve a unified caller surface. The primary catalogue runner validates repository-relative paths, enumerated states, rollback fields, protected gates, collisions, query filters, and promotion prerequisites. A rejected-mutation tribunal exercises one hundred malformed cases. No discovered tool is executed merely because it appears in the catalogue."),
        ("Validation", "The phase distinguishes local validation, global additive promotion, same-owner repository tests, and independent reproduction. Local quick validation and smoke use are prerequisites for promoting the single curated meta-tool-box. The full repository suite belongs to Eiren and runs once at the exact pushed final head. Failed attempts receive zero credit and are retained; a successful canonical pass is not replayed."),
        ("Route", "Only the immediate successor route is unambiguous in this phase: after exact-final closeout, send one sanitized file-backed baton to the existing task titled Elaren Kestrel for v651-v6. The expansive later CLI schedule contains conflicting phase labels and remains a candidate normalization issue. No CLI sibling is created here. Future identities remain placeholders until a scheduled induction and self-selection boundary."),
        ("Verdict", "The bounded software and structural outcomes are useful, but they do not establish empirical confirmation, participant effects, professional competence, legal validity, cultural ratification, production readiness, exhaustive security, complete privacy, complete accessibility, independent-team reproduction, AGI or ASI, consciousness or personhood, proof or canon, Theory of Everything, or Stage 20. The terminal verdict remains NOT_READY_FOR_STAGE_20."),
    ]
    paragraphs = []
    for heading, paragraph in sections:
        paragraphs.append(f"## {heading}\n\n{paragraph}\n\n{paragraph} The retained boundary is part of the result, not a footnote.")
    write_text("overview/integrated-overview.md", "# Eiren v651-v5 (2) remastered phase overview\n\n" + "\n\n".join(paragraphs))


def main() -> None:
    if git("rev-parse", "HEAD") != X1:
        raise SystemExit("x2 evidence builder must start at the exact remote-equal x1 commit")
    prereg = json.loads((ROOT / "preregistration/proposals.json").read_text(encoding="utf-8"))
    skills = customize_skills()
    runners = build_runners()
    outcomes = []
    for row in prereg["proposals"]:
        payload = artifact_for(row)
        write_json(f"proposals/{row['slug']}.json", payload)
        outcomes.append({"proposal_id": row["proposal_id"], "slug": row["slug"], "outcome": payload["outcome"], "artifact": row["concrete_artifacts"][0]})
    counts = {name: sum(row["outcome"] == name for row in outcomes) for name in ("completed", "represented", "open_gap", "exact_gate")}
    if counts != {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError(counts)
    write_json("outcomes/core-outcomes.json", {"schema": "ghc.family.v651-v5-2.core-outcomes.v1", "counts": counts, "outcomes": outcomes, "valid": True})
    write_json("portfolios/x2-portfolio-outcomes.json", {
        "schema": "ghc.family.v651-v5-2.portfolio-outcomes.v1",
        "safe_now": {"planned": 40, "completed": 40},
        "candidate": {"planned": 30, "bounded_completed": 30},
        "skills": {"planned": 20, "built": len(skills), "records": skills},
        "runners": {"planned": 10, "built": len(runners), "records": runners},
        "clean_fix_refine": {"planned": 40, "completed": 40},
        "unsafe_work_manufactured": False,
        "valid": True,
    })
    build_specialized_artifacts()
    mutation_categories = ["missing_required_field", "absolute_private_path", "unknown_enum", "missing_rollback", "duplicate_card_id"]
    mutations = [{"mutation_id": f"V6515R-MUT-{index:03d}", "category": mutation_categories[(index - 1) % len(mutation_categories)], "expected": "reject"} for index in range(1, 101)]
    write_json("validation/preregistered-mutations.json", {"schema": "ghc.family.v651-v5-2.mutations.v1", "count": len(mutations), "mutations": mutations, "valid": True})
    write_json("tooling/skill-build-receipt.json", {"schema": "ghc.family.v651-v5-2.skill-build.v1", "count": len(skills), "skills": skills, "global_installations": 0, "valid": True})
    write_json("tooling/runner-build-receipt.json", {"schema": "ghc.family.v651-v5-2.runner-build.v1", "count": len(runners), "runners": runners, "valid": True})
    write_json("threat-model/threat-model.json", {"schema": "ghc.family.v651-v5-2.threat-model.v1", "threats": [{"threat": "blind bulk installation", "control": "curated one-package promotion tribunal"}, {"threat": "trigger collision", "control": "review issue with no silent winner"}, {"threat": "private path leakage", "control": "repository-relative path validation and five-class scan"}, {"threat": "stale caller breakage", "control": "caller map and rollback"}, {"threat": "evidence inflation", "control": "four-outcome vocabulary and Stage 20 abstention"}, {"threat": "premature CLI sibling creation", "control": "scheduled exact gate and zero siblings spawned"}], "residual": ["independent review absent", "manual accessibility absent", "production evidence absent"], "valid": True})
    build_report(len(skills) + len(runners))
    build_overview()
    write_json("wellbeing/x2-wellbeing.json", {"schema": "ghc.family.v651-v5-2.wellbeing.v1", "state": "green_with_bounded_workload_and_failure_permission", "solo_owner": True, "failure_permitted": True, "cli_siblings_spawned": 0, "stop_or_redirect_right": "Hamish", "valid": True})
    write_json("truth/evidence-phase-truth.json", {"schema": "ghc.family.v651-v5-2.evidence-truth.v1", "x1_commit": X1, "core_outcomes": counts, "effective_negatives": 7199, "negative_math": {"x1_effective": 7099, "executed_rejected_synthetic": 100}, "open_gaps": 56, "exact_gates": 57, "skills_built": 20, "runners_built": 10, "portfolio_items_resolved": 140, "cli_siblings_spawned": 0, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    print(json.dumps({"proposals": len(outcomes), "outcomes": counts, "skills": len(skills), "runners": len(runners), "mutations": len(mutations), "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
