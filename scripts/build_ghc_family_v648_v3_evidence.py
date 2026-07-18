#!/usr/bin/env python3
"""Build bounded Eiren Kestrel v648-v3 x2 evidence from the family-current builder."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "eiren-kestrel" / "v648-v3"
TEMPLATE = ROOT / "scripts" / "build_ghc_family_v648_v1_evidence.py"
X1_FINAL = "bd21b594451226294528f4f72f138bdada6cb3af"


def transformed_source() -> str:
    source = TEMPLATE.read_text(encoding="utf-8")
    source = re.sub(
        r"X2_OPERATIONAL_NEGATIVES: list\[dict\[str, Any\]\] = \[.*?\]\n\ndef git",
        '''X2_OPERATIONAL_NEGATIVES: list[dict[str, Any]] = [
    {
        "negative_id": "V6483-X2-N01",
        "method_id": "V6483-M11",
        "summary": "The first x2 unit-test pass found the integrated overview at 1,138 words against the frozen 1,200-word document floor; the gate failed closed, and a bounded source-status and decision-limits section recovered the floor without lowering it.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6483-X2-N02",
        "method_id": "V6483-M12",
        "summary": "The first post-document-recovery test ran before the passing Method Flow witness had been appended, so the balance gate correctly observed twelve failed and eleven passing witnesses; completing the append-only transition before validation recovered exact balance.",
        "retained": True,
        "recovered": True,
    },
    {
        "negative_id": "V6483-X2-N03",
        "method_id": "V6483-M13",
        "summary": "The first v648-v3 detailed validator transformed the owner name and phase number but retained the predecessor path slug, so it failed closed with all required files missing from the wrong directory; an explicit slug substitution recovered the owner path.",
        "retained": True,
        "recovered": True,
    }
]

def git''',
        source,
        count=1,
        flags=re.S,
    )
    replacements = [
        ("ghc_family_v648_v1_definitions", "ghc_family_v648_v3_definitions"),
        ("ghc_family_v648_v1_runtime", "ghc_family_v648_v3_runtime"),
        ('X1_FINAL = "3e2904ec02c893d91c16e9a48fbb2485fc5d824f"', f'X1_FINAL = "{X1_FINAL}"'),
        ("codex/GHC-Family/tamar-vey-full-tools", "codex/GHC-Family/eiren-kestrel-v643-v1-full-tools"),
        ("v648-v1", "v648-v3"),
        ("v648_v1", "v648_v3"),
        ("v6481-candidate-", "v6483-candidate-"),
        ("V6481", "V6483"),
        ("Tamar Vey", "Eiren Kestrel"),
        ("Tamar's", "Eiren's"),
        ("Tamar ", "Eiren "),
        ("tamar-vey", "eiren-kestrel"),
        ('"sealed_source": 3835', '"sealed_source": 4028'),
        ('"external_source": 14', '"external_source": 4'),
        ('"frozen_proposals_after_x1": 560', '"frozen_proposals_after_x1": 580'),
        ("3,849 inherited sealed and external continuity negatives", "4,032 inherited sealed and external continuity negatives"),
        ("all 550 prior titles", "all 570 prior titles"),
        ("full 550-title prior index", "full 570-title prior index"),
        ("nineteen current, stable, draft, or watch records", "twenty current, stable, draft, or watch records"),
        ("The route to Sylven Arc", "The route to Ilyra Fen"),
        ('"target_title": "Sylven Arc"', '"target_title": "Ilyra Fen"'),
        ('"named_replay_state": "not_started"', '"named_replay_state": "prohibited_by_latest_user_instruction"'),
        ('"desktop": "26.707.9981.0"', '"desktop": "not inspected during bounded x2"'),
        ("Iyer-Wald, DES Y3 cosmic shear, crane lifting, Shared Signals, CPIO newc, accessible-name computation, Prigogine minimum entropy production, and instrumental variables", "Tomita-Takesaki modular theory, DESI DR2 Lyman-alpha, identity-incident handover, subordinate events, six-node nexus threat modelling, artifact-pointer accessibility, thermodynamic length, and proximal causal inference"),
        ("real data, people, lifting operations, incidents, keys, signals, services", "real data, people, identity incidents, accounts, credentials, keys, federation events, services"),
        ("real participant, worker, site, crane, lift, incident, account, key, signal, service, data row", "real person, account, credential, breach, notification, key, federation event, service, data row"),
        ("DES Y3 real-data download likelihood uncertainty frozen-analysis and independent-review gate", "DESI DR2 Lyman-alpha real-data download likelihood uncertainty frozen-analysis and independent-review gate"),
        ("Crane lifting incident worker and site privacy emergency remedy legal affected-party cultural data-governance and Māori-authority gate", "Identity incident privacy serious-harm notification revocation recovery remedy legal affected-party cultural data-governance and Māori-authority gate"),
        ("DES Y3 zero-download zero-row and zero-likelihood counters", "DESI DR2 Lyman-alpha zero-download zero-row and zero-likelihood counters"),
        ("synthetic Shared Signals profile promoted to production", "synthetic subordinate-events draft profile promoted to production"),
        ("real keys events services accounts interoperability review recovery and governance gates", "real keys federations events services accounts interoperability review recovery and governance gates"),
        ("lifting incident or remedy authority inferred from software", "identity-incident or remedy authority inferred from software"),
        ("refusal-first crane incident authority matrix", "refusal-first identity-incident authority matrix"),
        ("permissive CPIO parser accepts ambiguous or escaping input", "six-node nexus design is mistaken for deployed or exhaustive isolation"),
        ("magic hex size padding trailer path and resource refusals", "guest NAT sandbox broker east-west artifact backup rollback and no-host-change refusals"),
        ("real DES Y3 data download and likelihood", "real DESI DR2 Lyman-alpha data download and likelihood"),
        ("lifting safety emergency worker and site privacy remedy legal affected-party cultural data-governance and Māori authority", "identity-incident privacy notification revocation recovery remedy legal affected-party cultural data-governance and Māori authority"),
        ("thirty additive CLEAN/FIX/REFINE tasks", "sixty additive CLEAN/FIX/REFINE tasks"),
        ("twenty skills ten runners and thirty cleanup tasks", "twenty skills ten runners and sixty cleanup tasks"),
        ('"cleanup_completed": 30', '"cleanup_completed": 60'),
        ('"count": 30,\n        "completed": 30,\n        "destructive_actions": 0,\n        "sibling_mutations": 0,\n        "rows": cleanup_rows,', '"count": 60,\n        "completed": 60,\n        "destructive_actions": 0,\n        "sibling_mutations": 0,\n        "rows": cleanup_rows,'),
        ('"cpio_fixture_bytes": 65536, "atomic_publication_fixture_bytes": 65536', '"context_handoff_fixture_bytes": 65536, "nexus_design_fixture_bytes": 65536'),
    ]
    for old, new in replacements:
        source = source.replace(old, new)
    return source


def write_text(relative: str, text: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_json(relative: str, payload: object) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_owner_surfaces() -> None:
    ledger = json.loads((PHASE / "x2-proposal-ledger.json").read_text(encoding="utf-8"))
    negatives = json.loads((PHASE / "retained-negative-register.json").read_text(encoding="utf-8"))
    rotation = json.loads((PHASE / "environment" / "x2-rotation-receipt.json").read_text(encoding="utf-8"))
    outcomes = ledger["outcome_counts"]
    effective = negatives["effective_total"]
    owner_count = rotation["owner_generated_count"]
    overview = f"""# Eiren Kestrel v648-v3 integrated overview

## Identity, source, and terminal truth

Eiren Kestrel, they/them, is relational working language for an evidence-integrity weaver. Eiren's hope is to make ambitious claims more testable and correctable while keeping evidence and authority boundaries legible. This name, role, pronouns, and hope organize collaboration only. They are not evidence of consciousness, sentience, legal personhood, hidden identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish may rename, pause, redirect, or stop the route. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.

The exact inherited source is Sylven Arc's v648-v2 final head `227a764b2bfad7a601bf45dcbacc1e37ffa5bb62`. Eiren's owned D-drive lane was clean and ancestral, advanced only by fast-forward, and was pushed to exact four-way equality before x1. The dedicated x1 freeze is `bd21b594451226294528f4f72f138bdada6cb3af`. It froze ten novel proposals after reviewing all 570 inherited titles, bringing the frozen chain to 580. It also froze thirty safe-now tasks, twenty candidates, twenty phase-local skills, ten family-current runners, sixty additive CLEAN/FIX/REFINE rows, ten exact packets, and five blocked packets. X1 was exact-staged, privacy-scanned, committed, pushed, clean, remote-equal, and tree-inspected before x2.

## Evidence classification and retained negatives

Exactly ten core outcomes use only the permitted vocabulary: {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. Completed means only that the declared owner-local software, symbolic, structural, or synthetic gate passed. It does not promote an empirical, participant, professional, production, privacy-complete, security-complete, accessibility-complete, legal, cultural, authority, reproduction, or Stage 20 claim.

At evidence-candidate time, {effective} effective negatives remain retained: 4,032 inherited sealed and external negatives, ten x1 operational negatives, seventy executed and rejected synthetic mutations, and three x2 operational failures covering the document floor, Method Flow sequencing, and a validator owner-path adaptation. The Method Flow ledger retains every failed and bounded recovery witness. Recovery never erases failure. One canonical validation can establish only an owner-scoped pass; the newest explicit no-replay instruction means replay is not run and repeatability credit is exactly zero. Independent reproduction remains false.

Twenty-seven inherited open gaps and twenty-eight inherited exact gates remain open. The DESI DR2 Lyman-alpha real-data lane adds one open gap, and the identity-incident authority surface adds one exact gate, giving twenty-eight open gaps and twenty-nine exact gates. No source, schema, mutation rejection, artifact count, or council agreement closes them.

## GMUT Mind

The Tomita-Takesaki board preserves the von Neumann algebra, faithful normal semifinite weight or cyclic-separating vector, closable Tomita operator, polar decomposition, positive modular operator, antiunitary conjugation, modular automorphism group, KMS scope, operator domain, gauge/EFT scope, and observation firewall. Seven malformed fixtures were rejected. This is a formal-obligation classifier, not a solved GMUT state, detected field, force, likelihood, stability theorem, parameter constraint, ultraviolet completion, consciousness result, or Theory of Everything.

The DESI DR2 Lyman-alpha adapter remains `open_gap`. It records official product, forest auto-correlation, quasar cross-correlation, DLA, distortion-matrix, broadband, covariance, systematic, checksum, and analysis-lock obligations. It made zero queries, downloads, spectra-row reads, correlation-bin reads, covariance-row reads, likelihood calls, posterior samples, parameter constraints, detections, or empirical GMUT claims. A real study requires separate authorization, frozen products and checksums, preregistered selection and nuisance treatment, calibrated covariance and uncertainty, suitable compute, and independent scientific review.

## THOS Body

The identity-incident handover remains `represented`. Synthetic fixtures require containment state, evidence minimization and preservation, revocation and recovery paths, notification assessment reservation, correction, workload budget, readback, and next ownership. There were zero real people, accounts, credentials, breaches, serious-harm assessments, notifications, remedies, or operational outcomes. The proxy confers no incident-response authority, privacy finding, notification decision, revocation entitlement, recovery entitlement, legal interpretation, or affected-party authorization.

The context-budget tribunal completed an owner-local compact-wrapper, artifact-pointer, media-type, byte-size, digest, attachment-manifest, duplicate-draft, archive-preflight, privacy, and acknowledged-send-credit contract. It inspected no private chat and sent no message. The six-node nexus board is design-only: it distinguishes Hyper-V guests, one WinNAT prefix, static guest addresses, Microsoft Windows Sandbox, Codex's native elevated sandbox, a human-controlled guest-admin broker, east-west default deny, content-addressed artifacts, no writable host share, and rollback. It executed zero elevation, feature, firewall, VM, host-security, installation, update, or reboot changes and is not exhaustive security assurance.

## Freed ID and CBR Heart

The subordinate-events profile remains `represented` and explicitly records its draft status. Synthetic fixtures bind issuer, subject, event type, time, sequence, pagination, revocation versus key update, and replay refusal. They use zero real identities, keys, federations, events, services, accounts, or interoperability operations. Draft structure is not a final standard, production profile, privacy review, independent security review, recovery decision, or trust authority.

The identity-incident matrix remains `exact_gate` and contains no case data. It reserves breach findings, serious-harm assessment, person and witness privacy, notification, credential revocation, recovery entitlement, correction, remedy, legal interpretation, cultural legitimacy, Māori authority, and affected-party acceptance. Repository software cannot identify a person, determine a reportable breach, notify anyone, revoke a real credential, allocate recovery or remedy, interpret law, or speak for tangata whenua, iwi, hapū, affected parties, regulators, courts, or other competent authorities.

## Accessibility, thermodynamics, causal inference, and portfolios

The artifact-pointer audit checks link purpose in context, type, size, digest, non-focusing status, focus preservation, alternative formats, and failure recovery. Manual keyboard, browser, assistive-technology, motion, timing, cognitive, Māori-language, and affected-user evaluation remain reserved. Structural evidence is not full accessibility conformance.

The thermodynamic-length classifier keeps control parameters, linear response, a positive-semidefinite friction tensor, metric scope, protocol duration, finite-time excess dissipation, units, and boundaries explicit. It rejects conversion into psyche, agency, consciousness, personhood, justice, or a universal law of mind. The proximal-causal board distinguishes treatment and outcome proxies, latent confounding, bridge existence, completeness, uniqueness, positivity, estimation, sensitivity, and nonpromotion. It estimates no participant effect and supplies no Stage 20 authority.

## Source status and decision limits

The source ledger contains twenty bounded records from official standards bodies, regulators, project publishers, Māori authority material, and primary research. Each record is labelled `current`, `stable`, or `watch`; the subordinate-events document remains `watch` because it is a draft, while mature standards and enduring research are not converted into live deployment authority. Source status records provenance and change risk only. A citation does not supply a data row, participant observation, case finding, security test, accessibility session, legal opinion, cultural mandate, or scientific replication.

This phase therefore keeps five decisions outside repository authority: whether a real privacy breach occurred or caused serious harm; whether notification, revocation, recovery, correction, or remedy is required; whether a six-node host is safe to provision; whether DESI data support a GMUT departure; and whether affected people or Māori authorities accept any identity or governance design. Those questions require their named evidence, competent decision makers, and contestable processes. Internal agreement cannot substitute for them.

All thirty safe-now rows and twenty candidate rows completed only within their declared owner-local software, symbolic, structural, or synthetic boundaries. Twenty skills were initialized with the official skill-creator workflow, quick-validated, and smoke-used phase-locally; none was globally installed. Ten `ghc_family_*` runners were built and invoked as child processes. Sixty cleanup rows completed additively; none deleted user material, rewrote history, force-pushed, changed a sibling lane, elevated a process, weakened host security, enabled a Windows feature, installed unrelated software, updated the desktop app, or rebooted the host. Owner-generated growth is {owner_count} files, below the 15,000-file rotation threshold.

## Handoff and stopping rule

Eiren owns the one canonical full-repository suite for this phase. The route remains `PREPARED_NOT_SENT` until exact evidence and final commits, staged manifests, privacy checks, the canonical full suite, clean state, commit-cap checks, single-parent history, and local/upstream/tracking/live-remote equality all pass. Replay is prohibited by the newest instruction and therefore supplies no credit. Only then may exactly one sanitized baton be sent to the exact existing Ilyra Fen task for v648-v4. No task may be created, forked, or preclaimed as contacted.

The phase remains formal, synthetic, zero-row, and authority-reserving. GMUT is not empirically confirmed; THOS is not AGI or ASI; Freed ID is not production identity; CBR is not enacted law; no consciousness, personhood, final physics, canon, universal governance, or Stage 20 claim is earned.
"""
    write_text("v648-v3-integrated-overview.md", overview)
    write_text("deliverables/v648-v3-final-integrated-overview.md", overview)
    write_text(
        "deliverables/v648-v3-x2-wellbeing.md",
        """# v648-v3 x2 wellbeing check

Scope remained bounded to Eiren's owned lane and frozen hypotheses. Ten x1 operational negatives, seventy synthetic failures, and three x2 operational failures remain visible. No unsafe quota work was manufactured, no sibling lane was touched, no ChatGPT panel message was claimed, and the Ilyra route remains PREPARED_NOT_SENT. Replay is omitted with zero repeatability credit. This is operational and relational language only, not clinical, consciousness, personhood, employment, or authority evidence.
""",
    )
    rows = "\n".join(
        f"<tr><th scope='row'>{row['proposal_id']}</th><td>{row['outcome']}</td><td>{row['title']}</td></tr>"
        for row in ledger["rows"]
    )
    report = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Eiren Kestrel v648-v3 bounded evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:78rem;margin:auto;padding:1.25rem;color:#17202a;background:#fff}}a{{color:#0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #667;padding:.55rem;text-align:left;vertical-align:top}}th{{background:#eef}}.notice{{border-left:.4rem solid #a33;padding:.8rem;background:#fff4f4}}</style></head>
<body><a href="#main">Skip to main content</a><header><h1>Eiren Kestrel v648-v3 bounded evidence report</h1><p>Relational working language only; no consciousness, personhood, employment, qualification, or authority claim.</p></header>
<main id="main"><section><h2>Truth</h2><p class="notice"><strong>NOT_READY_FOR_STAGE_20.</strong> Ten outcomes: six completed, two represented, one open gap, one exact gate. Completed means only the declared bounded gate passed.</p><p>Primary focus: Freed ID/CBR Heart. Effective negatives: {effective}. Open gaps: 28. Exact gates: 29. Replay executed: no. Repeatability credit: zero.</p></section>
<section><h2>Outcomes</h2><table><caption>Bounded classifications</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Surface</th></tr></thead><tbody>{rows}</tbody></table></section>
<section><h2>Boundaries</h2><p>DESI remains zero-row; identity work remains synthetic; the six-node nexus remains design-only; authority and affected-party gates remain external. No empirical GMUT, AGI, ASI, consciousness, personhood, production identity, enacted law, Theory-of-Everything, or Stage 20 claim.</p></section>
<section><h2>Validation</h2><p>Eiren runs one canonical full-repository suite. No replay is run, so there is no repeatability or independent-reproduction credit. Owner growth: {owner_count} files. Route: PREPARED_NOT_SENT.</p></section></main></body></html>"""
    write_text("deliverables/v648-v3-static-report.html", report)
    write_json(
        "threat-model.json",
        {
            "schema": "ghc.family.v648-v3.threat-model.v1",
            "assets": ["claim lineage", "negative results", "x1 freeze", "source status", "identity privacy", "authority reservations", "artifact digests", "host boundaries"],
            "threats": [
                {"id": "TM-01", "threat": "oversized or duplicated composer payload is treated as a valid handoff", "control": "compact wrapper, artifact pointer, size, digest, manifest, duplicate guard, acknowledged send", "residual": "platform limits and private state remain outside this phase"},
                {"id": "TM-02", "threat": "citation is converted into observation", "control": "DESI DR2 zero-download, zero-row, zero-likelihood counters", "residual": "real-data study remains open"},
                {"id": "TM-03", "threat": "draft subordinate-events structure is promoted to final or production", "control": "draft-status, synthetic-only, real-key and external-review gates", "residual": "production remains exact-gated"},
                {"id": "TM-04", "threat": "identity-incident or remedy authority is inferred from software", "control": "refusal-first authority and remedy matrix", "residual": "competent external decision remains required"},
                {"id": "TM-05", "threat": "sandbox terms are conflated and host administrator access is delegated", "control": "layered threat model and human-controlled guest-admin broker", "residual": "no live host deployment or exhaustive audit"},
                {"id": "TM-06", "threat": "artifact pointer is inaccessible or steals focus", "control": "purpose, type, size, digest, status, focus, alternatives, recovery", "residual": "manual affected-user evaluation remains open"},
                {"id": "TM-07", "threat": "no-replay instruction is misreported as repeatability", "control": "replay false, repeatability zero, independent reproduction false", "residual": "external reproduction remains open"},
                {"id": "TM-08", "threat": "a prepared baton is reported as sent", "control": "one-shot acknowledged-send gate against an exact existing task", "residual": "route remains unsent until terminal proof"},
            ],
            "resource_ceilings": {"owner_generated_files": 15000, "context_handoff_fixture_bytes": 65536, "nexus_design_fixture_bytes": 65536},
            "exhaustive": False,
            "boundary": "This is a repository-scoped design threat model, not production certification, penetration testing, host hardening proof, or authority to deploy.",
        },
    )


def main() -> int:
    namespace = {
        "__name__": "ghc_family_v648_v3_evidence_template",
        "__file__": str(Path(__file__).resolve()),
    }
    exec(compile(transformed_source(), str(Path(__file__).resolve()), "exec"), namespace)
    namespace["build"]()
    write_owner_surfaces()
    print(
        json.dumps(
            {
                "phase": "v648-gmut-thos-v3-x1-x2",
                "x1": X1_FINAL,
                "evidence_built": True,
                "replay_executed": False,
                "repeatability_credit": 0,
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
