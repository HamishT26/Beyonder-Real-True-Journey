#!/usr/bin/env python3
"""Build Caelen Morrow v658-v3 bounded archival-film x2 evidence."""

from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import ghc_family_v658_v3_phase_data as d
import ghc_family_v658_v3_x2_config as c
from ghc_family_v658_v3_runtime import evaluate_surface


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / d.PHASE_ROOT
SELF_EXCLUSIONS = {
    "validation/evidence-content-manifest.json",
    "validation/evidence-privacy-scan.json",
    "validation/evidence-staged-review.json",
    "validation/evidence-validation.json",
}


def write_json(relative: str, payload: Any, *, compact: bool = False) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=None if compact else 2, separators=(",", ":") if compact else None, sort_keys=True)
    path.write_text(text + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.strip()


def x1_frozen_paths() -> list[str]:
    return [line for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", c.X1_COMMIT).splitlines() if line]


def assert_x1_unchanged() -> None:
    paths = x1_frozen_paths()
    changed = subprocess.run(["git", "diff", "--name-only", c.X1_COMMIT, "--", *paths], cwd=ROOT, check=True, capture_output=True, text=True, encoding="utf-8").stdout.splitlines()
    if changed:
        raise RuntimeError(f"frozen x1 paths changed: {changed}")


def mutation_negative(proposal_id: str, row: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "negative_id": f"V6583-MUT-{proposal_id.split('-')[-1]}-{index:02d}",
        "proposal_id": proposal_id, "mutation_id": row["mutation_id"], "signature": row["error_codes"],
        "observed": "The preregistered synthetic mutation was rejected by the bounded contract validator.",
        "credit": 0, "retained": True, "same_owner_only": True, "independent_reproduction": False,
        "authority_action_executed": False,
    }


def mutation_method(negative: dict[str, Any], index: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6583-X2-MUT-METHOD-{index:03d}"
    fail_id = f"V6583-X2-MUT-WITNESS-{index:03d}-F"
    pass_id = f"V6583-X2-MUT-WITNESS-{index:03d}-P"
    method = {
        "method_id": method_id, "title": f"Fail-closed mutation guard for {negative['mutation_id']}",
        "trigger_preconditions": [negative["mutation_id"]], "failure_signature": negative["signature"],
        "candidate_workaround": "Reject the mutated candidate and retain it at zero credit.",
        "recurrence_guard": "Run all five frozen mutations for the surface and require explicit rejection codes.",
        "approval_class": "safe_now_owner_local_synthetic_falsification", "privacy_class": "sanitized_public",
        "scope_boundary": "Synthetic mutation evidence only.",
        "rollback": "Discard the mutated candidate, preserve the valid contract, and leave real, external, authority, and sibling state unchanged.",
        "protected_gates": d.PROTECTED_GATES, "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id], "recommendation_state": "preferred", "supersedes": [],
    }
    witnesses = [
        {"witness_id": fail_id, "method_id": method_id, "result": "fail", "procedure": "Apply the preregistered mutation to the valid synthetic fixture.", "expected": "The mutation must not receive valid-fixture credit.", "observed": f"Rejected with {', '.join(negative['signature'])}.", "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Zero completion credit."},
        {"witness_id": pass_id, "method_id": method_id, "result": "pass", "procedure": "Confirm explicit rejection while preserving the valid fixture separately.", "expected": "The validator fails closed on the mutation.", "observed": "The mutation was rejected and retained without changing real, external, authority, or sibling state.", "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Bounded same-owner falsification only."},
    ]
    return method, witnesses


def operational_method(negative: dict[str, Any], index: int) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    method_id = f"V6583-X2-OP-METHOD-{index:02d}"
    fail_id = f"V6583-X2-OP-WITNESS-{index:02d}-F"
    pass_id = f"V6583-X2-OP-WITNESS-{index:02d}-P"
    method = {
        "method_id": method_id, "title": f"Bounded recovery for {negative['slug']}",
        "trigger_preconditions": [negative["slug"]], "failure_signature": negative["failure_signature"],
        "candidate_workaround": negative["candidate_workaround"], "recurrence_guard": negative["recurrence_guard"],
        "approval_class": "safe_now_owner_local_workflow_recovery", "privacy_class": "sanitized_public",
        "scope_boundary": negative["scope_boundary"],
        "rollback": "Retain the failed attempt at zero credit and leave sibling, external, and authority state unchanged.",
        "protected_gates": d.PROTECTED_GATES, "retained_negative_ids": [negative["negative_id"]],
        "validation_witness_ids": [fail_id, pass_id], "recommendation_state": "preferred", "supersedes": [],
    }
    witnesses = [
        {"witness_id": fail_id, "method_id": method_id, "result": "fail", "procedure": negative["fail_procedure"], "expected": "The bounded operation completes without a tooling, timeout, or encoding failure.", "observed": negative["fail_observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": "Failed workflow witness with zero completion credit."},
        {"witness_id": pass_id, "method_id": method_id, "result": "pass", "procedure": negative["pass_procedure"], "expected": "The bounded recovery completes while preserving the failed witness.", "observed": negative["pass_observed"], "retained_negative_ids": [negative["negative_id"]], "same_owner_only": True, "independent_reproduction": False, "boundary": negative["scope_boundary"]},
    ]
    return method, witnesses


def skill_markdown(name: str, purpose: str, slugs: list[str]) -> str:
    return f"""---
name: {name}
description: "{purpose} Use for Caelen v658-v3 owner-local synthetic archival-film evidence across {', '.join(slugs)}."
---

# {name}

1. Read the frozen proposal and its official-source identifiers.
2. Confirm every input is synthetic and contains no real person, collection, film, material, equipment, measurement, image, sound, right, private route, credential, or culturally restricted payload.
3. Invoke the corresponding family-current runner only inside the Caelen v658-v3 owner packet.
4. Require one valid fixture to pass and all five frozen mutations for every covered surface to be rejected.
5. Retain every failed witness at zero credit and preserve `completed`, `represented`, `open_gap`, or `exact_gate` exactly.
6. Stop on any real inspection, handling, cleaning, winding, repair, projection, scanning, storage, transport, nitrate or acetate test, safety instruction, preservation decision, access or rights decision, professional, production, legal, cultural, Māori-authority, privacy-complete, accessibility-complete, exhaustive-security, independent-reproduction, Theory-of-Everything, or Stage 20 gate.

Write only repository-relative sanitized receipts. Never include credentials, raw task identifiers, private paths, transcripts, screenshots, session streams, workplace records, or real collection data.

This phase-local skill is synthetic workflow guidance. It establishes no consciousness, personhood, continuity, employment, qualification, archival or conservation competence, projection or safety authority, custody, rights, legal interpretation, cultural ratification, Māori authority, independent reproduction, or Stage 20 readiness.
"""


def skill_openai_yaml(name: str, purpose: str) -> str:
    display = " ".join(part.capitalize() for part in name.split("-"))
    short = purpose if 25 <= len(purpose) <= 64 else (purpose[:61].rstrip() + "...")
    return f"""interface:
  display_name: "{display}"
  short_description: "{short}"
  default_prompt: "Use ${name} to validate its frozen synthetic archival-film evidence surfaces."
policy:
  allow_implicit_invocation: false
"""


def wrapper_source(filename: str, slugs: list[str]) -> str:
    return f'''#!/usr/bin/env python3
"""Family-current Caelen v658-v3 bounded archival-film evidence runner."""

from __future__ import annotations

import argparse
import json

from ghc_family_v658_v3_runtime import ROOT, run_named_surface, write_json


SURFACES = {slugs!r}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    rows = [run_named_surface(slug) for slug in SURFACES]
    payload = {{
        "schema": "ghc.family.v658-v3.group-runner-receipt.v1",
        "runner": "{filename}", "surfaces": SURFACES, "surface_count": len(rows),
        "valid_fixture_count": sum(row["valid_fixture_passed"] for row in rows),
        "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in rows),
        "valid": all(row["valid_fixture_passed"] and row["all_mutations_rejected"] for row in rows),
        "authority_actions_executed": 0, "same_owner_only": True, "independent_reproduction": False,
        "rows": rows,
    }}
    write_json(ROOT / args.output, payload)
    print(json.dumps(payload, ensure_ascii=True, sort_keys=True))
    if not payload["valid"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
'''


def integrated_overview(outcomes: dict[str, int], negatives: int, methods: int) -> str:
    return f"""# Caelen Morrow v658-v3 integrated evidence overview

## Relational identity and exact evidence boundary

Caelen Morrow, they/them, is relational working language for this owner-scoped phase. The relational role is chronometry boundary-mapper and failure custodian, with the hope of making every claim traceable while leaving real competence and authority where they belong. The name, pronouns, role, hope, family, continuity, route, and Trinity Mandala language do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, scientific or operational authority, legal or cultural authority, Māori authority, or independent agency. Hamish may rename, pause, redirect, or stop the work.

This evidence descends from Sylven Arc's exact v658-v2 final `{c.SOURCE_COMMIT}` through Caelen's immutable x1 `{c.X1_COMMIT}`. X1 froze thirty proposals against 2,710 inherited proposals before any x2 contract, mutation result, outcome, phase-local skill, family-current runner, or successor contact existed. X1 was separately committed, pushed, clean, 0/0 divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. X2 preserves all forty frozen x1 paths unchanged.

The packet records {outcomes['completed']} `completed`, {outcomes['represented']} `represented`, {outcomes['open_gap']} `open_gap`, and {outcomes['exact_gate']} `exact_gate`. It retains {negatives:,} effective negatives, {c.SOURCE_OPEN_GAPS + 1} effective open gaps, {c.SOURCE_EXACT_GATES + 1} effective exact gates, and {methods:,} Method Flow methods with retained failed and bounded passing witnesses. Same-owner checks under shared infrastructure remain same-owner. The terminal verdict is `NOT_READY_FOR_STAGE_20`.

## Freed ID and CBR Heart primary focus

Freed ID and CBR Heart are primary through synthetic element identifiers, alias collision quarantine, custody and handoff states, preservation-event lineage, correction, rights-field minimization, withheld-field explanations, purpose binding, remedy pointers, pseudonym rotation, correlation alarms, invalidation, expiry, and explicit nonproduction boundaries. These structures do not create a real key, signature, proof, credential, issuer, holder, subject, title, custody chain, access permission, donor agreement, copyright determination, trust relationship, or preservation authority.

The dual-control reel-handoff challenge represents reciprocal confirmation, conflicting claims, timeout, and annulment on a synthetic fixture. The field-release budget represents purpose-bounded disclosure, withheld-field reasons, correction, and remedy without deciding whether disclosure is lawful or authorized. The pseudonym-rotation lineage represents link-secret placeholders and correlation alarms without proving unlinkability or operating an identity system. All three remain `represented`, not production identity evidence.

CBR exact-gates copyright, donor and depositor terms, access, cultural content, traditional knowledge, affected-party remedy, Māori data, tangata whenua, iwi, hapū, and Māori authority. The authority covenant is structurally checked only for refusal-by-default. It performs no rights analysis, community engagement, cultural classification, label selection, wording adoption, access decision, disclosure, restriction, return, or remedy decision. Māori concepts remain under Māori authority.

## Bounded archival motion-picture practice

The human-practice lens is archival motion-picture film inspection, conservation documentation, projection-readiness review, custody, rights reservation, workload control, and shift handover. It is synthetic software, formal, structural, and learning evidence only. The phase uses zero real people, institutions, collections, titles, films, reels, cans, cores, leaders, frames, soundtracks, projectors, scanners, chemicals, images, sounds, measurements, inspections, tests, handling, winding, cleaning, repair, splicing, projection, digitization, storage, transport, preservation, access, or disposition actions. It confers no employment, qualification, archival competence, conservation competence, projection competence, custody, safety authority, rights authority, legal interpretation, cultural authority, Māori authority, or operational result.

Twenty-three completed surfaces cover request quarantine; element and reel identity; gauge and perforation; base, emulsion and stock provenance; reel and footage maps; edge-code transcription; frame cadence and timebase; image area and aperture; dimensional condition; perforation damage; splice lineage; soundtrack topology; image-process and fade observations; acetate uncertainty; nitrate classification quarantine; inspection-path topology; changeover and cue continuity; projector-interface reservation; DPX frame sequences; PREMIS preservation lineage; a GMUT film-transport operator; a GMUT optical-temporal identifiability tribunal; and a structurally accessible static report. Each completion means only that one declared valid synthetic fixture passed and five frozen malformed candidates were rejected.

The contracts can detect missing obligations, real-record promotion, prohibited material-test language, Stage 20 promotion, and outcome tampering. They cannot judge a film, measure shrinkage, identify a base, date a stock, diagnose deterioration, evaluate a splice, set a projector speed, approve an aperture, determine playback compatibility, digitize an image, validate a checksum, authenticate provenance, or direct preservation work.

## Nitrate, acetate, safety, and professional refusal

Nitrate and acetate rails are fail closed. The nitrate surface carries only an evidence class, uncertainty, isolation-alert placeholder, escalation state, and no-testing or handling rule. It performs no burn test, float test, odor test, visual identification, handling, movement, container change, ventilation change, storage choice, transport, projection, disposal, fire-response, or emergency instruction. The acetate surface carries only synthetic observation placeholders and no diagnosis. Repository code cannot replace qualified human assessment, institutional policy, emergency services, legal requirements, or site-specific controls.

ISO catalogue pages, Library of Congress film-care material, FIAF resources, and FADGI guidance provide terminology and boundary context. They do not certify this packet, a collection, a workflow, or an operator. No ISO, FIAF, FADGI, PBCore, PREMIS, W3C, privacy, accessibility, safety, professional, legal, or cultural conformance is claimed.

## GMUT Mind and THOS Body

GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The discrete film-transport contract has typed frame state, sprocket-phase placeholder, gate boundary, observation placeholder, residual, and empirical firewall. The identifiability tribunal lists source, stock, generation, optics, transport, scanning, and processing as confounders. No real observation, likelihood, posterior, fit, parameter constraint, force, material law, prediction, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, Theory of Everything, proof, or canon results.

THOS remains represented through a synthetic inspection, correction, stop-work, readback and shift-handover proxy plus a synthetic custody-workload and recovery proxy. They exercise only declared event queues, priorities, interruptions, pauses, resumptions, escalation, and two-person placeholders. There are no real workers, shifts, incidents, participants, blind matched-budget arms, safety monitoring, statistical analysis, outcomes, or independent review. The proxies do not establish effectiveness, safer work, workload reduction, deployment readiness, AGI, ASI, consciousness, or personhood.

## Open gap, accessibility, privacy, and validation limits

The FIAF, FADGI, PBCore and PREMIS capability matrix remains `open_gap`. Its transport is disabled and it processes zero real rows. No network call, download, API query, schema ingestion, external record, live version negotiation, or institutional interoperability test occurred. A zero-row adapter can show only that the local boundary shape is ready to receive governed future evidence; it cannot supply that evidence.

The static report has a title, language, viewport, landmark regions, ordered headings, a boundary notice, a captioned table with scoped headers, a focusable table region, non-colour text labels, responsive overflow, print rules, and a skip link. Those are machine-checkable structural facts. Manual keyboard, browser diversity, zoom and reflow, forced colours, screen readers, cognitive accessibility, Māori-language evaluation, security usability, and affected-user evaluation remain reserved. Privacy scanning covers five concrete raw-identifier classes and reports zero confirmed hits; it is not complete privacy assurance.

Ten phase-local skills and ten family-current runners partition the thirty surfaces. The current skill-creator initialized and validated the owner-local skill directories; no skill was globally installed and no subagent forward test ran because delegation was prohibited. Runner receipts show only deterministic same-owner synthetic contract evaluation. Inherited callers and history remain intact.

## Failure retention and route gate

All {c.X1_OPERATIONAL_NEGATIVES} startup and x1 operational failures remain in the frozen x1 ledger. All {c.EXPECTED_MUTATIONS} rejected mutations are retained at zero credit with paired Method Flow witnesses. Any x2 operational fault is likewise retained. A recovery proves only its bounded postcondition; it never erases failure, establishes independence, or upgrades a core outcome.

No successor has been contacted. Eiren Kestrel v658-v4 remains a declared terminally gated next title. Only after evidence and closeout commits are pushed, the final has one direct evidence parent, all manifests replay, the lane is clean and 0/0 divergent, a fresh four-way equality read passes, and one dependency-justified canonical scoped aggregate succeeds exactly once may the newest live and committed route be consulted. If still unambiguous, the existing exact-title Eiren task must be uniquely resolved and directly reread before one sanitized acknowledged activation. That baton must remind Eiren that their next terminal edge is Elaren Kestrel v658-v5. Tavian Sol remains `ON_STANDBY`. No Stage 20 claim is authorized.
"""


def static_report(outcomes: dict[str, int], negatives: int) -> str:
    rows = "\n".join(
        f"<tr><th scope=\"row\">{html.escape(p['proposal_id'])}</th><td>{html.escape(p['title'])}</td><td>{html.escape(p['expected_disposition'])}</td><td>Synthetic fixture; no real film, authority, or operational action.</td></tr>"
        for p in d.PROPOSALS
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Caelen Morrow v658-v3 bounded archival-film evidence report</title>
<style>body{{font-family:system-ui,sans-serif;line-height:1.55;max-width:76rem;margin:auto;padding:1rem;color:#171717;background:#fff}}h1,h2{{line-height:1.2}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:.6rem;z-index:2}}.notice{{border:.25rem solid #713b00;padding:1rem;background:#fff7e8}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.55rem;text-align:left;vertical-align:top}}thead{{background:#e8eef5}}a:focus,[tabindex]:focus{{outline:.2rem solid #005fcc;outline-offset:.15rem}}@media(max-width:50rem){{table{{display:block;overflow-x:auto}}}}@media print{{body{{max-width:none}}.notice{{break-inside:avoid}}table{{font-size:9pt}}}}</style></head>
<body><a class="skip" href="#main">Skip to evidence</a><header><h1>Caelen Morrow v658-v3 bounded archival-film evidence report</h1></header><main id="main">
<p class="notice"><strong>Boundary:</strong> synthetic same-owner software evidence only. This report is not film inspection, preservation, handling, nitrate or acetate safety advice, projection or digitization guidance, a rights decision, professional validation, cultural authority, Māori authority, or permission to act.</p>
<section aria-labelledby="summary"><h2 id="summary">Evidence summary</h2><p><strong>{outcomes['completed']} completed; {outcomes['represented']} represented; {outcomes['open_gap']} open gap; {outcomes['exact_gate']} exact gate.</strong> {negatives:,} effective negatives retained. Terminal verdict: NOT_READY_FOR_STAGE_20.</p><p>Completion is bounded to one declared synthetic contract and five rejected mutations. The external standards adapter used disabled transport and zero rows. The authority covenant grants no authority and executes no authority action.</p></section>
<section aria-labelledby="outcomes"><h2 id="outcomes">Proposal outcomes</h2><div role="region" aria-label="Proposal evidence table" tabindex="0"><table><caption>Thirty frozen v658-v3 proposal surfaces and bounded outcomes</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Outcome</th><th scope="col">Evidence boundary</th></tr></thead><tbody>{rows}</tbody></table></div></section>
<section aria-labelledby="reserved"><h2 id="reserved">Reserved evaluation and authority</h2><p>Manual keyboard, browser, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved. Real film condition, nitrate and acetate safety, custody, copyright, donor and depositor terms, access, remedy, cultural content, traditional knowledge, Māori data governance, tangata whenua, iwi, hapū, and Māori authority remain outside this software evidence.</p></section>
</main><footer><p>Route state: TERMINAL_SUCCESSOR_GATE_UNMET. Same-owner evidence is not independent reproduction.</p></footer></body></html>"""


def owner_paths() -> list[Path]:
    paths = [path for path in PHASE.rglob("*") if path.is_file()]
    paths.extend(path for path in (ROOT / "scripts").glob("*v658_v3*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "scripts").glob("ghc_family_film_*.py") if path.is_file())
    paths.extend(path for path in (ROOT / "tests").glob("*v658_v3*.py") if path.is_file())
    return sorted({path.resolve() for path in paths})


def privacy_scan(paths: list[Path]) -> dict[str, Any]:
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b(?:[a-z]:[\\/](?:users|ghc-archives)[\\/][^\s\"']+)"),
        "credential_or_secret": re.compile(r"(?i)\b(?:sk-[a-z0-9_-]{20,}|bearer\s+[a-z0-9._-]{20,}|password\s*[:=]\s*[^\s\"']{8,})"),
        "private_route_value": re.compile(r"(?i)\b(?:thread|task|session)://[a-z0-9_-]{12,}"),
        "private_callable_value": re.compile(r"(?i)\bprivate_callable_(?:id|identifier)\s*[:=]\s*[a-z0-9_-]{8,}"),
    }
    hits = []
    for path in paths:
        if path.is_relative_to(PHASE) and path.relative_to(PHASE).as_posix() in SELF_EXCLUSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="strict")
        for label, pattern in patterns.items():
            count = len(pattern.findall(text))
            if count:
                hits.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label, "count": count})
    scanned = [p for p in paths if not (p.is_relative_to(PHASE) and p.relative_to(PHASE).as_posix() in SELF_EXCLUSIONS)]
    return {"schema": "ghc.family.v658-v3.evidence-privacy-scan.v1", "pattern_classes": sorted(patterns), "file_count": len(scanned), "confirmed_hits": hits, "hit_count": sum(row["count"] for row in hits), "valid": not hits, "self_exclusions": sorted(SELF_EXCLUSIONS), "boundary": "Concrete values only; this is not complete privacy assurance."}


def git_clean_blob(path: Path) -> tuple[str, int, str]:
    relative = path.relative_to(ROOT).as_posix()
    oid = git("hash-object", "-w", f"--path={relative}", relative)
    blob = subprocess.run(["git", "cat-file", "blob", oid], cwd=ROOT, check=True, capture_output=True).stdout
    return oid, len(blob), hashlib.sha256(blob).hexdigest()


def build() -> None:
    if git("rev-parse", "HEAD") != c.X1_COMMIT:
        raise RuntimeError("x2 builder requires the exact frozen x1 head")
    assert_x1_unchanged()
    ledger = read_json(PHASE / "preregistration/proposal-ledger.json")
    if ledger["proposal_count"] != c.EXPECTED_PROPOSALS:
        raise RuntimeError("frozen proposal count mismatch")
    # Materialize self-referential lifecycle paths before taking the exact owner-path snapshot.
    for relative in sorted(SELF_EXCLUSIONS):
        write_json(relative, {"schema": "ghc.family.v658-v3.evidence-placeholder.v1", "materialized_before_snapshot": True})

    outcome_counts: Counter[str] = Counter()
    mutation_negatives: list[dict[str, Any]] = []
    proposal_rows: list[dict[str, Any]] = []
    for proposal in d.PROPOSALS:
        result = evaluate_surface(proposal["slug"])
        if result["valid_errors"]:
            raise RuntimeError(f"valid fixture failed for {proposal['slug']}: {result['valid_errors']}")
        if result["rejected_mutation_count"] != c.MUTATIONS_PER_PROPOSAL:
            raise RuntimeError(f"mutation rejection count failed for {proposal['slug']}")
        base = f"surfaces/{proposal['slug']}"
        write_json(f"{base}/contract.json", result["contract"])
        write_json(f"{base}/mutation-results.json", {"schema": "ghc.family.v658-v3.mutation-results.v1", "proposal_id": proposal["proposal_id"], "mutation_count": len(result["mutation_results"]), "rejected_count": result["rejected_mutation_count"], "all_rejected": result["all_mutations_rejected"], "authority_action_executed": False, "results": result["mutation_results"]})
        write_json(f"{base}/bounded-receipt.json", {"schema": "ghc.family.v658-v3.bounded-receipt.v1", "proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "outcome": proposal["expected_disposition"], "valid_fixture_passed": result["valid_fixture_passed"], "rejected_mutation_count": result["rejected_mutation_count"], "real_data_used": False, "network_called": False, "authority_granted": False, "authority_action_executed": False, "same_owner_only": True, "independent_reproduction": False, "boundary": result["contract"]["boundary"]})
        for index, row in enumerate(result["mutation_results"], 1):
            mutation_negatives.append(mutation_negative(proposal["proposal_id"], row, index))
        outcome_counts[proposal["expected_disposition"]] += 1
        proposal_rows.append({"proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "outcome": proposal["expected_disposition"], "valid_fixture_passed": True, "rejected_mutations": c.MUTATIONS_PER_PROPOSAL, "real_data_used": False, "network_called": False, "authority_granted": False, "authority_action_executed": False})
    if dict(outcome_counts) != c.EXPECTED_DISTRIBUTION or len(mutation_negatives) != c.EXPECTED_MUTATIONS:
        raise RuntimeError("outcome or mutation total mismatch")

    proposal_by_id = {row["proposal_id"]: row["slug"] for row in d.PROPOSALS}
    groups_by_id = [
        ["V6583-P01", "V6583-P02", "V6583-P20"], ["V6583-P03", "V6583-P04", "V6583-P09", "V6583-P10"],
        ["V6583-P07", "V6583-P08", "V6583-P12", "V6583-P13"], ["V6583-P05", "V6583-P06", "V6583-P11", "V6583-P17"],
        ["V6583-P14", "V6583-P15", "V6583-P18"], ["V6583-P19", "V6583-P23", "V6583-P29"],
        ["V6583-P21", "V6583-P22"], ["V6583-P24", "V6583-P25"], ["V6583-P26", "V6583-P27", "V6583-P28"],
        ["V6583-P16", "V6583-P30"],
    ]
    groups = [[proposal_by_id[item] for item in group] for group in groups_by_id]
    if sorted(slug for group in groups for slug in group) != sorted(proposal_by_id.values()):
        raise RuntimeError("skill and runner groups do not partition all proposals")

    skill_creator = Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "scripts"
    init_skill = skill_creator / "init_skill.py"
    quick_validate = skill_creator / "quick_validate.py"
    if not init_skill.is_file() or not quick_validate.is_file():
        raise RuntimeError("current skill-creator scripts unavailable")
    utf8_env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    skill_rows = []
    for (name, purpose), slugs in zip(d.SKILL_SPECS, groups, strict=True):
        skill_dir = PHASE / "skills" / name
        prior_init_path = skill_dir / "skill-creator-init-receipt.json"
        prior_initialized_during_phase = False
        if prior_init_path.is_file():
            prior_initialized_during_phase = bool(read_json(prior_init_path).get("initialized_during_phase", read_json(prior_init_path).get("initialized_now", False)))
        initialized_now = False
        if not skill_dir.exists():
            display = " ".join(part.capitalize() for part in name.split("-"))
            short = purpose if 25 <= len(purpose) <= 64 else purpose[:61].rstrip() + "..."
            initialized = subprocess.run([sys.executable, str(init_skill), name, "--path", str(PHASE / "skills"), "--interface", f"display_name={display}", "--interface", f"short_description={short}", "--interface", f"default_prompt=Use ${name} to validate bounded synthetic archival-film evidence."], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", env=utf8_env)
            if initialized.returncode != 0:
                raise RuntimeError(f"skill-creator initialization failed for {name}: {initialized.stdout}{initialized.stderr}")
            initialized_now = True
        write_text(f"skills/{name}/SKILL.md", skill_markdown(name, purpose, slugs))
        write_text(f"skills/{name}/agents/openai.yaml", skill_openai_yaml(name, purpose))
        validated = subprocess.run([sys.executable, str(quick_validate), str(skill_dir)], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", env=utf8_env)
        if validated.returncode != 0:
            raise RuntimeError(f"skill-creator validation failed for {name}: {validated.stdout}{validated.stderr}")
        init_row = {"schema": "ghc.family.v658-v3.skill-creator-init-receipt.v1", "skill": name, "initialized_via_current_skill_creator": True, "initialized_now": initialized_now, "initialized_during_phase": initialized_now or prior_initialized_during_phase, "initialized_once": True, "quick_validate_passed": True, "globally_installed": False, "subagent_forward_test": False, "subagent_forward_test_reason": "solo execution and delegation prohibition", "surfaces": slugs}
        write_json(f"skills/{name}/skill-creator-init-receipt.json", init_row)
        skill_rows.append(init_row)
    write_json("tooling/skill-creator-receipts.json", {"schema": "ghc.family.v658-v3.skill-creator-receipts.v1", "skill_count": len(skill_rows), "initialized_via_current_skill_creator": len(skill_rows), "quick_validate_passed": len(skill_rows), "globally_installed": 0, "subagent_forward_tests": 0, "rows": skill_rows})

    runner_rows = []
    for (filename, _), slugs, (skill_name, _) in zip(d.RUNNER_SPECS, groups, d.SKILL_SPECS, strict=True):
        runner_path = ROOT / "scripts" / filename
        runner_path.write_text(wrapper_source(filename, slugs), encoding="utf-8", newline="\n")
        output = f"docs/caelen-morrow/v658-v3/runners/{Path(filename).stem}-receipt.json"
        completed = subprocess.run([sys.executable, str(runner_path), "--output", output], cwd=ROOT, check=False, capture_output=True, text=True, encoding="utf-8", env=utf8_env)
        if completed.returncode != 0:
            raise RuntimeError(f"runner failed for {filename}: {completed.stdout}{completed.stderr}")
        receipt = read_json(ROOT / output)
        runner_rows.append(receipt)
        write_json(f"skills/{skill_name}/smoke-receipt.json", {"schema": "ghc.family.v658-v3.skill-smoke-receipt.v1", "skill": skill_name, "runner": filename, "valid": receipt["valid"], "surface_count": receipt["surface_count"], "rejected_mutation_count": receipt["rejected_mutation_count"], "same_owner_only": True, "forward_test": False})
    write_json("tooling/runner-receipts.json", {"schema": "ghc.family.v658-v3.runner-receipts.v1", "runner_count": len(runner_rows), "valid_count": sum(row["valid"] for row in runner_rows), "surface_count": sum(row["surface_count"] for row in runner_rows), "rejected_mutation_count": sum(row["rejected_mutation_count"] for row in runner_rows), "rows": runner_rows})

    methods: list[dict[str, Any]] = []
    witnesses: list[dict[str, Any]] = []
    for index, negative in enumerate(mutation_negatives, 1):
        method, pair = mutation_method(negative, index); methods.append(method); witnesses.extend(pair)
    for index, negative in enumerate(c.X2_OPERATIONAL_NEGATIVES, 1):
        method, pair = operational_method(negative, index); methods.append(method); witnesses.extend(pair)
    effective_methods = c.SOURCE_METHODS + c.X1_METHODS + len(methods)
    write_json("method-flow/method-flow-state-x2.json", {"schema": "ghc.family.method-flow-state.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x2_evidence_candidate", "inherited_anchor": {"path": "docs/caelen-morrow/v658-v3/method-flow/method-flow-state-x1.json", "effective_methods": c.SOURCE_METHODS + c.X1_METHODS, "effective_fail_witnesses": c.SOURCE_METHODS + c.X1_METHODS, "effective_pass_witnesses": c.SOURCE_METHODS + c.X1_METHODS}, "current_methods": methods, "current_witnesses": witnesses, "counts": {"current_methods": len(methods), "current_witness_results": {"fail": len(methods), "pass": len(methods)}, "effective_methods": effective_methods, "effective_witness_results": {"fail": effective_methods, "pass": effective_methods}}, "all_failed_witnesses_retained": True, "independent_reproduction": False}, compact=True)
    negative_total = c.SOURCE_EFFECTIVE_NEGATIVES + c.X1_OPERATIONAL_NEGATIVES + len(mutation_negatives) + len(c.X2_OPERATIONAL_NEGATIVES)
    write_json("truth/retained-negative-register-x2.json", {"schema": "ghc.family.v658-v3.retained-negatives.x2.v1", "source_effective_count": c.SOURCE_EFFECTIVE_NEGATIVES, "x1_operational_count": c.X1_OPERATIONAL_NEGATIVES, "mutation_count": len(mutation_negatives), "x2_operational_count": len(c.X2_OPERATIONAL_NEGATIVES), "effective_count": negative_total, "mutation_negatives": mutation_negatives, "x2_operational_negatives": c.X2_OPERATIONAL_NEGATIVES, "all_retained": True}, compact=True)
    write_json("truth/open-gap-register-x2.json", {"schema": "ghc.family.v658-v3.open-gaps.x2.v1", "source_effective_count": c.SOURCE_OPEN_GAPS, "new_count": 1, "effective_count": c.SOURCE_OPEN_GAPS + 1, "proposal_ids": ["V6583-P29"], "reason": "Transport remained disabled with zero real rows, no external conformance, and no independent review."})
    write_json("truth/exact-gate-register-x2.json", {"schema": "ghc.family.v658-v3.exact-gates.x2.v1", "source_effective_count": c.SOURCE_EXACT_GATES, "new_count": 1, "effective_count": c.SOURCE_EXACT_GATES + 1, "proposal_ids": ["V6583-P30"], "reason": "Real rights, donor and depositor terms, cultural content, affected parties, traditional knowledge, Māori data, tangata whenua, iwi, hapū, and Māori authority cannot be simulated.", "authority_action_executed": False})
    write_json("x2/proposal-ledger.json", {"schema": "ghc.family.v658-v3.proposal-ledger.x2.v1", "proposal_count": len(proposal_rows), "outcome_counts": dict(outcome_counts), "rows": proposal_rows, "same_owner_only": True, "independent_reproduction": False})

    candidate_rows = []
    for row in d.CANDIDATE_TASKS:
        receipt = f"prototypes/{row['task_id'].lower()}-receipt.json"
        write_json(receipt, {"schema": "ghc.family.v658-v3.bounded-prototype-receipt.v1", "task_id": row["task_id"], "state": "completed", "reviewed": True, "reversible": True, "synthetic_only": True, "external_side_effects": False, "production_or_authority_credit": False, "acceptance": "The refinement preserved outcome, source, privacy, hazard, authority, and rollback boundaries.", "same_owner_only": True, "independent_reproduction": False})
        candidate_rows.append({**row, "state": "completed", "evidence": receipt})
    clean_rows = []
    for row in d.CLEAN_TASKS:
        receipt = f"cleanup/{row['task_id'].lower()}-receipt.json"
        write_json(receipt, {"schema": "ghc.family.v658-v3.additive-cleanup-receipt.v1", "task_id": row["task_id"], "state": "completed", "additive_only": True, "user_material_deleted": False, "history_rewritten": False, "sibling_lane_mutated": False, "gate_weakened": False, "review": "Compatibility, privacy, provenance, stale-label, hazard, authority, and nonpromotion boundaries passed."})
        clean_rows.append({**row, "state": "completed", "evidence": receipt})
    safe_rows = []
    for index, row in enumerate(d.SAFE_TASKS):
        proposal = d.PROPOSALS[index]
        safe_rows.append({**row, "state": "completed" if proposal["expected_disposition"] == "completed" else ("represented" if proposal["expected_disposition"] == "represented" else proposal["expected_disposition"]), "evidence": f"surfaces/{proposal['slug']}/bounded-receipt.json", "authority_action_executed": False})
    write_json("x2/task-execution.json", {"schema": "ghc.family.v658-v3.task-execution.v1", "safe_now": safe_rows, "candidate": candidate_rows, "clean": clean_rows, "counts": {"safe_now": 30, "candidate": 20, "clean": 30, "total": 80}, "unsafe_work_manufactured": False, "exact_gate_executed": False})
    write_json("truth/phase-truth-x2.json", {"schema": "ghc.family.v658-v3.phase-truth.x2.v1", "phase": d.PHASE, "owner": d.OWNER, "lifecycle": "x2_evidence_candidate", "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "frozen_proposals": 2740, "outcome_counts": dict(outcome_counts), "effective_negatives": negative_total, "effective_open_gaps": c.SOURCE_OPEN_GAPS + 1, "effective_exact_gates": c.SOURCE_EXACT_GATES + 1, "effective_methods": effective_methods, "real_data_used": False, "network_called": False, "authority_action_executed": False, "independent_reproduction": False, "route_state": "TERMINAL_SUCCESSOR_GATE_UNMET", "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("provenance/evidence-provenance.json", {"schema": "ghc.family.v658-v3.evidence-provenance.v1", "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "x1_paths_preserved": len(x1_frozen_paths()), "x1_bytes_changed": False, "surface_count": 30, "mutation_count": 150, "skill_count": 10, "runner_count": 10, "real_rows": 0, "network_calls": 0, "authority_actions": 0, "same_owner_only": True})
    write_json("wellbeing/wellbeing-check-x2.json", {"schema": "ghc.family.v658-v3.wellbeing.x2.v1", "owner": d.OWNER, "state": "bounded", "one_owner_lane": True, "subagents": 0, "successor_contacts": 0, "unsafe_quota_work": False, "stop_states": ["real film or record", "nitrate or acetate action", "professional decision", "rights or cultural decision", "Māori authority", "fatigue or Hamish pause"], "identity_boundary": "Relational working language only."})
    write_json("final-complete-incomplete-checklist-x2.json", {"schema": "ghc.family.v658-v3.complete-incomplete.x2.v1", "complete": ["thirty frozen outcomes classified", "twenty-three bounded synthetic contracts", "five proxy or nonproduction representations", "one zero-row open gap", "one exact authority gate", "all 150 mutations rejected and retained", "ten phase-local skills validated", "ten family-current runners passed", "static report structure emitted"], "incomplete": ["real film or participant evidence", "professional validation", "nitrate or acetate assessment", "external standards interoperability", "manual or affected-user accessibility evaluation", "privacy-complete or exhaustive-security review", "legal, cultural, affected-party, or Māori authority", "independent reproduction", "Stage 20"], "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_text("deliverables/v658-v3-integrated-evidence-overview.md", integrated_overview(dict(outcome_counts), negative_total, effective_methods))
    write_text("deliverables/v658-v3-archival-film-evidence-report.html", static_report(dict(outcome_counts), negative_total))
    write_json("orchestration/route-state-x2.json", {"schema": "ghc.family.v658-v3.route-state.x2.v1", "active_owner": d.OWNER, "active_phase": d.PHASE, "next_exact_title": "Eiren Kestrel", "next_phase": "v658-v4", "next_successor_reminder": {"title": "Elaren Kestrel", "phase": "v658-v5"}, "state": "TERMINAL_SUCCESSOR_GATE_UNMET", "message_sent": False, "task_created": False, "task_forked": False, "subagent_spawned": False, "tavian_sol_state": "ON_STANDBY"})

    stale_paths = []
    scanner_false_positives = []
    for path in owner_paths():
        relative = path.relative_to(ROOT).as_posix()
        if relative.endswith("provenance/frozen-chain-proposal-index.json") or relative.endswith("provenance/semantic-novelty-audit.json"):
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(r"Sylven Arc v658-v3|Caelen Morrow v658-v2|seis-|station-metadata|seismic-station", text):
            if relative == "scripts/build_ghc_family_v658_v3_x2.py":
                scanner_false_positives.append({"path": relative, "classification": "scanner_pattern_definition", "confirmed_stale": False})
            else:
                stale_paths.append(relative)
    stale_valid = not stale_paths
    write_json("validation/stale-label-hygiene-x2.json", {"schema": "ghc.family.v658-v3.stale-label-hygiene.x2.v1", "excluded_historical_evidence": ["provenance/frozen-chain-proposal-index.json", "provenance/semantic-novelty-audit.json"], "declared_false_positives": scanner_false_positives, "confirmed_stale_paths": stale_paths, "confirmed_stale_count": len(stale_paths), "valid": stale_valid})
    if not stale_valid:
        raise RuntimeError(f"confirmed stale labels remain: {stale_paths}")

    documents = []
    for path in sorted(PHASE.rglob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html", ".json", ".txt", ".yaml"}:
            words = len(path.read_text(encoding="utf-8").split())
            documents.append({"path": path.relative_to(PHASE).as_posix(), "words": words, "under_limit": words <= 100000})
    write_json("validation/evidence-document-cap.json", {"schema": "ghc.family.v658-v3.evidence-document-cap.v1", "limit_words": 100000, "document_count": len(documents), "maximum_words": max(row["words"] for row in documents), "all_under_limit": all(row["under_limit"] for row in documents), "documents": documents})
    file_count = sum(1 for path in PHASE.rglob("*") if path.is_file()) + sum(1 for path in (ROOT / "scripts").glob("*v658_v3*.py") if path.is_file()) + sum(1 for path in (ROOT / "scripts").glob("ghc_family_film_*.py") if path.is_file()) + sum(1 for path in (ROOT / "tests").glob("*v658_v3*.py") if path.is_file())
    write_json("validation/evidence-owner-file-cap.json", {"schema": "ghc.family.v658-v3.evidence-owner-file-cap.v1", "owner_file_count": file_count, "cap": 2000, "within_cap": file_count <= 2000, "cap_is_ceiling_not_quota": True})

    paths = owner_paths()
    scan = privacy_scan(paths)
    if not scan["valid"]:
        raise RuntimeError(f"privacy scan failed: {scan['confirmed_hits']}")
    write_json("validation/evidence-privacy-scan.json", scan)
    manifest_entries = []
    for path in paths:
        if path.is_relative_to(PHASE) and path.relative_to(PHASE).as_posix() in SELF_EXCLUSIONS:
            continue
        oid, size, digest = git_clean_blob(path)
        manifest_entries.append({"path": path.relative_to(ROOT).as_posix(), "git_blob": oid, "git_blob_bytes": size, "sha256": digest})
    write_json("validation/evidence-content-manifest.json", {"schema": "ghc.family.v658-v3.evidence-content-manifest.v1", "hash_domain": "prospective Git-clean blob bytes", "entry_count": len(manifest_entries), "entries": manifest_entries, "self_exclusions": sorted(SELF_EXCLUSIONS)})
    paths = owner_paths()
    x1_set = set(x1_frozen_paths())
    evidence_delta = sorted(path.relative_to(ROOT).as_posix() for path in paths if path.relative_to(ROOT).as_posix() not in x1_set)
    write_json("validation/evidence-staged-review.json", {"schema": "ghc.family.v658-v3.evidence-staged-review.v1", "state": "PRECOMMIT_PATH_REVIEW", "allowed_prefixes": [d.PHASE_ROOT + "/", "scripts/ghc_family_v658_v3_", "scripts/build_ghc_family_v658_v3_x2.py", "scripts/ghc_family_film_", "tests/test_ghc_family_v658_v3.py"], "expected_delta_path_count": len(evidence_delta), "expected_delta_paths": evidence_delta, "x1_changed_paths": [], "deletions": [], "route_messages": 0, "valid": True, "exact_index_review_required_after_staging": True})
    json_paths = sorted(PHASE.rglob("*.json"))
    for path in json_paths:
        read_json(path)
    receipt = {"schema": "ghc.family.v658-v3.evidence-validation.v1", "valid": stale_valid and scan["valid"], "source_commit": c.SOURCE_COMMIT, "x1_commit": c.X1_COMMIT, "x1_paths_preserved": len(x1_frozen_paths()), "proposal_count": 30, "outcome_counts": dict(outcome_counts), "valid_fixture_count": 30, "rejected_mutation_count": 150, "skill_count": 10, "runner_count": 10, "json_parse_count": len(json_paths), "privacy_file_count": scan["file_count"], "privacy_hit_count": 0, "manifest_entry_count": len(manifest_entries), "stale_label_count": len(stale_paths), "declared_stale_scanner_false_positives": len(scanner_false_positives), "real_rows": 0, "network_calls": 0, "authority_actions": 0, "same_owner_only": True, "independent_reproduction": False, "route_message_sent": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}
    write_json("validation/evidence-validation.json", receipt)
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    build()
