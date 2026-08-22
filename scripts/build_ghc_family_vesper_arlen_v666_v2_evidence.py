#!/usr/bin/env python3
"""Build the Vesper Arlen v666-v2 evidence packet and accessible report."""

from __future__ import annotations

import html
import hashlib
import json
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "vesper-arlen" / "v666-v2"
X1_SHA = "d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969"
SOURCE_SHA = "299fe38950f3919b4ce3d3074ed248a914dcb984"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
EVIDENCE_NEGATIVES = 26279
EVIDENCE_METHODS = 10706


def load(relative: str) -> Any:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value: Any) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(relative: str, value: str) -> None:
    path = PHASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def command_version(command: list[str]) -> dict[str, Any]:
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True, encoding="utf-8").strip()
        return {"available": True, "value": output, "exit_code": 0}
    except Exception as exc:
        return {"available": False, "error_class": type(exc).__name__, "exit_code": None}


def staged_rows() -> list[tuple[str, str]]:
    raw = subprocess.check_output(
        ["git", "-C", str(ROOT), "diff", "--cached", "--name-status", "--no-renames"]
    ).decode("utf-8")
    return [tuple(line.split("\t", 1)) for line in raw.splitlines()]


def index_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "-C", str(ROOT), "show", f":{path}"])


def build_evidence_staged_review() -> None:
    review_path = "docs/vesper-arlen/v666-v2/validation/evidence-staged-review.json"
    manifest_path = "docs/vesper-arlen/v666-v2/validation/evidence-content-manifest.json"
    rows = [(status, path.replace("\\", "/")) for status, path in staged_rows() if path != manifest_path]
    rows = [(status, path) for status, path in rows if path != review_path]
    if not rows:
        raise RuntimeError("no staged evidence content")
    paths = [path for _, path in rows]
    invalid = [
        path
        for path in paths
        if not path.startswith("docs/vesper-arlen/v666-v2/")
        and not re.fullmatch(r"(?:scripts|tests)/[a-z0-9_]*vesper_arlen_v666_v2[a-z0-9_]*\.py", path)
    ]
    frozen_prefixes = (
        "docs/vesper-arlen/v666-v2/x1/",
        "docs/vesper-arlen/v666-v2/identity/",
        "docs/vesper-arlen/v666-v2/provenance/",
    )
    frozen_exact = {
        "docs/vesper-arlen/v666-v2/wellbeing/x1-wellbeing-check.json",
        "docs/vesper-arlen/v666-v2/validation/x1-content-manifest.json",
        "docs/vesper-arlen/v666-v2/validation/x1-staged-review.json",
        "scripts/build_ghc_family_vesper_arlen_v666_v2_x1.py",
        "tests/test_ghc_family_vesper_arlen_v666_v2_x1.py",
    }
    x1_mutations = [path for path in paths if path.startswith(frozen_prefixes) or path in frozen_exact]
    privacy_patterns = {
        "raw_task_or_thread_identifier": re.compile(r'(?i)[\"\'](?:source_)?(?:task|thread)[_-]?id[\"\']\s*[:=]\s*[\"\'][^\"\']+[\"\']'),
        "private_absolute_path": re.compile(r"(?i)[A-Z]:\\(?:Users\\|GHC-Archives\\)"),
        "credential_or_token_value": re.compile(r"(?i)(?:bearer\s+[A-Za-z0-9._~-]{12,}|api[_-]?key\s*[:=]\s*[^\s,}]+)"),
        "session_identifier_value": re.compile(r'(?i)[\"\'](?:session|resume)[_-]?(?:id|value)[\"\']\s*[:=]\s*[\"\'][^\"\']+[\"\']'),
        "private_callable_identifier_value": re.compile(r'(?i)[\"\']private[_-]?callable[_-]?id[\"\']\s*[:=]\s*[\"\'][^\"\']+[\"\']'),
    }
    json_parsed = 0
    max_words = 0
    max_path = ""
    candidates = []
    for path in paths:
        blob = index_blob(path)
        text = blob.decode("utf-8")
        if "\r" in text:
            raise RuntimeError(f"non-LF staged blob: {path}")
        words = len(re.findall(r"\S+", text))
        if words > max_words:
            max_words, max_path = words, path
        if path.endswith(".json"):
            json.loads(text)
            json_parsed += 1
        for class_name, pattern in privacy_patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name})
    ledger = json.loads(index_blob("docs/vesper-arlen/v666-v2/x2/proposal-ledger.json"))
    tooling = json.loads(index_blob("docs/vesper-arlen/v666-v2/x2/tooling-smoke-receipt.json"))
    runtime = json.loads(index_blob("docs/vesper-arlen/v666-v2/x2/runtime-validation-receipt.json"))
    checks = {
        "additive_only": all(status == "A" for status, _ in rows),
        "all_json_parse": True,
        "document_word_cap": max_words <= 100000,
        "expected_14_4_1_1": ledger["outcome_counts"] == {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1},
        "five_class_scan_zero_confirmed_hits": not candidates,
        "owner_allowlist": not invalid,
        "owner_file_cap": len(paths) <= 2000,
        "x1_paths_unchanged": not x1_mutations,
        "x1_head_basis": subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "HEAD"]).decode().strip() == X1_SHA,
        "twenty_contracts_one_hundred_rejections": ledger["bounded_positive_count"] == 20 and ledger["rejected_mutation_count"] == 100,
        "tooling_smoke_10_and_10": tooling["status"] == "PASS" and tooling["skill_quick_validation"]["passed"] == 10 and tooling["runner_smoke"]["passed"] == 10,
        "bounded_runtime_7_of_7": runtime["passed_component_count"] == 7 and runtime["failed_component_count"] == 0 and not runtime["canonical_aggregate"],
        "overview_three_page_equivalent": len(re.findall(r"\S+", index_blob("docs/vesper-arlen/v666-v2/reports/integrated-evidence-overview.md").decode("utf-8"))) >= 1800,
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.vesper-arlen.v666-v2.evidence-staged-review.v1",
        "owner": "Vesper Arlen",
        "phase": "v666-v2",
        "lifecycle": "evidence",
        "generated_at_utc": NOW,
        "reviewed_from": "git_index_blobs",
        "reviewed_paths": paths,
        "reviewed_path_count": len(paths),
        "status_counts": {"A": sum(status == "A" for status, _ in rows)},
        "json_parsed": json_parsed,
        "maximum_document_words": max_words,
        "maximum_document_path": max_path,
        "privacy_scan_classes": list(privacy_patterns),
        "privacy_candidates": len(candidates),
        "privacy_confirmed_hits": len(candidates),
        "privacy_candidate_rows": candidates,
        "checks": checks,
        "self_exclusions": [review_path, manifest_path],
        "claim_boundary": "exact staged same-owner evidence review only; not exhaustive security, privacy, accessibility, professional validation, or independent reproduction",
        "valid": all(checks.values()),
    }
    if not review["valid"]:
        raise RuntimeError(json.dumps(review, ensure_ascii=False, sort_keys=True))
    write_json("validation/evidence-staged-review.json", review)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", review_path])
    entries = []
    current_rows = [(status, path.replace("\\", "/")) for status, path in staged_rows() if path != manifest_path]
    for status, path in current_rows:
        stage_line = subprocess.check_output(["git", "-C", str(ROOT), "ls-files", "--stage", "--", path]).decode().strip()
        mode, oid, stage_and_path = stage_line.split(" ", 2)
        stage, listed_path = stage_and_path.split("\t", 1)
        if stage != "0" or listed_path.replace("\\", "/") != path:
            raise RuntimeError(f"unexpected index stage for {path}")
        blob = index_blob(path)
        entries.append({"path": path, "git_mode": mode, "git_blob_oid": oid, "sha256": hashlib.sha256(blob).hexdigest(), "size_bytes": len(blob)})
    manifest = {
        "schema": "ghc.family.vesper-arlen.v666-v2.content-manifest.v1",
        "owner": "Vesper Arlen",
        "phase": "evidence",
        "phase_label": "v666-v2",
        "generated_at_utc": NOW,
        "source_sha": SOURCE_SHA,
        "x1_sha": X1_SHA,
        "hash_source": "actual_git_index_blobs",
        "entries": entries,
        "entry_count": len(entries),
        "deletion_count": 0,
        "additive_only": all(status == "A" for status, _ in current_rows),
        "self_exclusion": manifest_path,
    }
    write_json("validation/evidence-content-manifest.json", manifest)
    subprocess.check_call(["git", "-C", str(ROOT), "add", "--", manifest_path])
    print(json.dumps({"reviewed": len(paths), "manifest_entries": len(entries), "valid": True}))


def paragraphs() -> list[tuple[str, list[str]]]:
    return [
        (
            "Outcome and evidence boundary",
            [
                "Vesper Arlen v666-v2 is a bounded owner-local software and documentation delta. Twenty genuinely new proposals were frozen before implementation after all 4,190 inherited rows were reconstructed from committed Git objects. The observed core outcomes are exactly fourteen completed, four represented, one open gap, and one exact gate. Completed means only that one preregistered synthetic JSON contract accepted one bounded positive fixture and rejected five invalid mutations. It does not mean that an array, antenna, observatory, site, sky target, visibility, image, calibration record, worker, or affected party was observed, operated, assessed, disclosed, certified, or governed.",
                "All twenty bounded positives passed and all one hundred preregistered mutations were rejected. The invalid states cover missing fields, wrong types, authority smuggling, a prohibited real-world or production action, and promotion beyond the preregistered outcome. Those checks demonstrate local schema behavior, explicit stop fields, deterministic provenance placeholders, and fail-closed response to known mutations. They establish no MeasurementSet, IVOA, calibration, astrometric, flux, polarization, imaging, traceability, device-performance, observational, operational-readiness, rights, privacy-complete, accessibility-complete, exhaustive-security, or independent-reproduction claim.",
                "The terminal verdict remains NOT_READY_FOR_STAGE_20. That label records that empirical, participant, professional, identity, legal, cultural, Māori-authority, affected-party, production, independent-review, deployment, Theory-of-Everything, AGI, ASI, consciousness, and personhood gates remain open or exact-gated. The evidence is same-owner under shared infrastructure. It is not an external audit, certification, scientific replication, professional opinion, legal review, cultural ratification, or operational authorization.",
            ],
        ),
        (
            "Relational working language and corrigibility",
            [
                "Vesper Arlen and they/them are relational working language. The chosen role is spectral-boundary cartographer, and the associated hope is to make synthetic visibility workflows expose gauge freedom, provenance vacancies, uncertainty, and stop conditions before anyone mistakes them for astronomical, instrument, or scientific authority. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority.",
                "Hamish may rename, pause, redirect, or stop the work. Corrigibility is preserved in the authorization boundary, workflow plan, explicit failure ledger, and no-success-replay rule. No collaboration subagent, task fork, substitute endpoint, standby sibling, or successor has been contacted during execution. A terminal route action cannot occur until the evidence commit, closeout, exact final, clean push, fresh live equality, one exact-final canonical completion, and a fresh live roster, authorization, usage, privacy, evidence, and safety reread all succeed.",
                "The relational boundary also prevents continuity language from becoming a technical assertion. Repository commits preserve files and provenance, not a living identity or independent agency. A chosen name is useful coordination language and nothing more. The same restraint applies to professional and cultural roles: a software artifact may reserve an authority gate, but it cannot occupy the place of an astronomer, interferometrist, metrologist, observatory worker, affected party, regulator, lawyer, cultural authority, tangata whenua, iwi, hapū, or Māori authority.",
            ],
        ),
        (
            "Bounded synthetic radio-interferometry practice lens",
            [
                "The practice lens is wholly synthetic radio-interferometric visibility calibration, imaging-provenance, and shift-handover documentation. It studies baseline frame closure, channel-edge partitions, flag-reason precedence, calibration applicability, visibility quantities, closure-phase gauge cancellation, subtable references, bitemporal lineage, IVOA provenance closure, content-addressed snapshots, canonical metadata maps, accessible visibility states, observation-note minimisation, and Stage 20 negative controls. It uses zero real arrays, antennas, observatories, sites, coordinates, sky targets, visibilities, images, observations, measurements, instruments, calibration certificates, configurations, workers, affected parties, keys, proofs, or authority actions.",
                "Synthetic placeholders are conspicuous. Tokens begin with SYN, symbolic quantities are text or tiny fixture constants, and every authority-bearing state is vacant, reserved, held, absent, or prohibited. The fixtures make zero network calls and execute zero device commands. No MeasurementSet, archive row, visibility byte, image pixel, coordinate, or calibration table is ingested. Numeric channel edges, times, weights, cycle signs, and action budgets are test constants rather than measurements. Nothing establishes astrometry, flux, polarization, imaging quality, calibration validity, instrument response, observatory condition, source detection, or operational instruction.",
                "Professional astronomy, interferometry, imaging, instrumentation, metrology, workplace safety, siting, privacy, legal, cultural, and affected-party evaluation remain absent. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluation are reserved. Structural software checks cannot stand in for astronomers, interferometrists, observatory workers, metrologists, regulators, affected communities, tangata whenua, iwi, hapū, Māori authorities, or people whose safety, land, data, culture, or rights could be affected by a real observatory or archive.",
            ],
        ),
        (
            "Semantic novelty and immutable x1 separation",
            [
                "The novelty audit retained historical proposal rows rather than silently deduplicating them. It compared each new title to all 4,190 inherited titles using exact casefolded comparison and alphanumeric token-set Jaccard screening, then checked every pair inside the new slate. The first Vesper title for observation-log purpose and retention overlapped a Neris maintenance-purpose selector at 0.789474 and failed the less-than-0.70 assertion. It earned zero novelty credit and remains in Method Flow. The changed target is a field-state minimisation lattice with omit, retain-until, and contested-redaction semantics rather than another purpose-intersection selector.",
                "The committed slate has zero exact inherited collisions, no within-slate pair at or above 0.70, maximum inherited similarity 0.607143, and maximum within-slate similarity 0.166667. Those values are screens, not proof of novelty. Each proposal also records a distinctive invariant, hypothesis, null condition, approval class, execution lane, source need, concrete artifacts, falsifier, rollback, protected gates, and expected disposition. The twenty Vesper rows extend the frozen chain from 4,190 to 4,210.",
                "The dedicated x1 commit d327d6ca9f16dc6cf16f555aea1c9a41fc8f4969 is the direct child of Neris Solane's exact final 299fe38950f3919b4ce3d3074ed248a914dcb984. Its nineteen paths contain planning and preregistration only. Exact lifecycle checks prove that the immutable x1 Git tree contains no x2, evidence, closeout, seal, final, or handoff path. X1 was pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Later files do not rewrite that Git object.",
            ],
        ),
        (
            "GMUT Mind as primary pillar",
            [
                "GMUT Mind is the primary Trinity Mandala focus. Its completed synthetic contracts model baseline sign and frame closure, channel partitions, flag-reason preservation, calibration applicability, dimensional abstention, closure-phase gauge cancellation, referential integrity, bitemporal lineage, provenance closure, and negative-control nonpromotion. These are software and symbolic invariants only. They do not demonstrate that a visibility model, calibration system, sky reconstruction, array, archive, or scientific theory is correct, stable, identified, interoperable, or ready for use.",
                "The represented Källén-Lehmann board records positivity, subtraction, EFT-domain, and dispersion obligations without a physical spectral density, propagator, observation, likelihood, or constraint. The represented gain-sky witness preserves two symbolic factorizations on one gauge orbit and therefore forces an identifiability hold. It does not fit antenna gains, reconstruct a sky, detect a source, or infer causality. The absence of a prior and all real visibility rows is part of the acceptance condition rather than missing detail hidden by a completion label.",
                "GMUT abstention is as important as its typed structure. Gauge cancellation cannot create a source image. A spectral-positivity obligation cannot become a measured spectrum. Dimensional consistency cannot create a force or likelihood. An identifiability witness cannot choose one physical factorization. A negative-control board cannot authorize Stage 20. These nonconversion rules are direct acceptance conditions and not merely prose disclaimers, yet their passing remains bounded same-owner software evidence.",
            ],
        ),
        (
            "THOS Body, Freed ID, and CBR Heart",
            [
                "THOS Body is represented by a participant-free calibration-and-handover duel with three named synthetic fault types, two masked traces, and one equal symbolic action budget. Participant, operator, session, incident, and real-arm counts are zero. It does not estimate detection time, repair time, error rate, workload, safety, usability, or operational effectiveness. There is no governed study protocol, independent team, preregistered statistical analysis, real equipment, competent supervision, safety monitoring, or affected-user review. The representation exists to expose what evidence would still be required.",
                "GMUT remains a research-model family rather than established fundamental physics. Dimensional typing and identifiability holds can reveal internal logical obligations, but they supply no posterior, parameter constraint, unique prediction, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon. Independent physics review, real governed data, calibrated instruments, uncertainty analysis, competing-model comparisons, and successful external reproduction remain absent. The terminal verdict cannot be raised by symbolic software structure.",
                "Freed ID is represented by a zero-key observation-provenance statement graph with issuer vacancy, purpose binding, expiry, correction, revocation, and zero-key states. Real issuer, holder, key, signature, proof, status service, resolution, interoperability, recovery, and trust-governance counts remain zero. CBR Heart exact-gates observatory and sky disclosure, calibration release, worker safety, affected-party remedy, cultural review, and Māori authority. No schema decides those questions, and Te Mana Raraunga is cited only to preserve an authority boundary rather than interpret or confer Māori authority.",
            ],
        ),
        (
            "Public-source profile and nonconversion",
            [
                "The source profile records casacore MeasurementSet definition and API documentation, IVOA Provenance DM, ObsCore, and Data Origin, NIST SI language, NIST measurement-uncertainty guidance, NIST metrological traceability, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, the New Zealand Privacy Commissioner principles, and Te Mana Raraunga. The review was read-only and source status was recorded. Phase software made zero network calls and ingested zero real rows.",
                "casacore material supplies vocabulary for main tables, subtables, visibility metadata, references, flags, weights, and calibration relations but no table was opened and no format conformance is claimed. IVOA material supplies observation-discovery, provenance, origin, entity, activity, generation, usage, and citation vocabulary without a TAP query, archive row, interoperability event, quality grade, endorsement, or reproducibility claim. NIST sources supply quantity, unit, uncertainty, and traceability language without performing a measurement or establishing an unbroken calibration chain. W3C PROV-O supplies provenance relations without authenticity or custody.",
                "WCAG supplies structural report criteria without accessibility-complete credit, and the credential source supplies data-integrity vocabulary without a real credential or proof. The Privacy Commissioner source constrains purpose, collection, access, correction, retention, disclosure, and identifier-restraint vocabulary but provides no legal determination. Te Mana Raraunga remains a primary authority-reservation source and is not converted into Māori wording, interpretation, data-governance approval, or Māori authority. The casacore-IVOA adapter remains an open gap because live archive rows, version negotiation, interoperability testing, and independent standard-owner semantic review did not occur.",
            ],
        ),
        (
            "Method Flow and retained failures",
            [
                "The immutable Neris repository seal remains 26,160 effective negatives and 10,472 Method Flow methods. Four post-final Neris operational failures remain a separately attributable external overlay. The live activation named only one, so its 26,161-negative and 10,473-method paragraph is retained as stale by three; the exact successor-visible baseline is 26,164 negatives and 10,476 methods. Eleven Vesper startup and x1 failures are retained. They include bounded-output, receipt-search, PowerShell parser, sparse-index, patch-display, manifest-projection, activation-overlay, stale-roster, template-quarantine, and failed novelty witnesses. None receives aggregate-success or completion credit.",
                "One hundred preregistered rejecting mutations are deliberate negative witnesses. Each has zero aggregate and completion credit, an exact error class, and a passing bounded recovery witness in the corresponding positive fixture. Two x2 wrapper faults are retained: one upstream-token parsing error and one Windows wildcard search error. Two evidence-stage faults are also retained: a lost long-running session handle and an atomic patch-context rejection. The evidence candidate therefore contains 26,279 effective negatives and 10,706 Method Flow methods. Open gaps rise from 183 to 184 and exact gates from 181 to 182; the Neris seal remains immutable and separately attributable.",
                "A retained failure is never erased merely because a changed target later passes. Recovery changes only the owner-local target required to make the intended contract accurate. Recurrence guards prefer explicit UTF-8, real JSON keys, bounded scalar output, exact Git-object inspection, sparse physical-file measurement, immutable x1-tree assertions, and separated repository-seal versus external-overlay accounting. If evidence, closeout, final, canonical, or route operations later fail, their rows must be added prospectively rather than backfilled or fabricated. Same-owner passing witnesses do not become independent reproduction, professional validation, or authority.",
            ],
        ),
        (
            "Skills, runners, security, privacy, and accessibility",
            [
                "Ten phase-local skills were created under the Vesper documentation tree. Each has a required SKILL.md, a discriminating workflow, explicit inputs, outputs, stop conditions, and protected-boundary language. All ten passed the local quick validator and were exercised through bounded smoke use. They were not globally installed and do not modify shared configuration. Their presence does not create astronomical, interferometric, imaging, instrumentation, metrological, safety, scientific, legal, cultural, affected-party, or Māori authority.",
                "Ten additive ghc_family-prefixed runners were built for contracts, mutations, JSON, privacy, bounded security, manifests, structural accessibility, truth, closeout, and canonical preflight. All ten passed self-test. Seven selected runtime components passed their bounded sequence. Existing family-current callers were not changed or deprecated. The security runner scans owner Python syntax for a small dangerous-construct set; zero findings is not exhaustive security. The privacy runner checks five value-bearing classes; zero confirmed hits is not privacy certification.",
                "The static report uses an explicit language, skip link, landmarks, one top-level heading, labelled navigation, table captions, scoped column headers, redundant text labels, visible focus, print rules, and reduced-motion rules. It contains no script, form, external stylesheet, tracking resource, or network dependency. These are structural checks only. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluations remain reserved and incomplete. Zero findings in any bounded scanner is never promoted to exhaustive coverage.",
            ],
        ),
        (
            "Complete, incomplete, and terminal route",
            [
                "Complete at the evidence-candidate stage are the exact source reread, strict x1 freeze and equality gate, twenty synthetic contracts, one hundred rejecting mutations, exact core outcome ledger, source profiles, zero-call adapter gap, Trinity representation records, portfolio execution record, ten skills, ten runners, Method Flow, threat-model review, accessible static report, and this integrated overview. They are bounded same-owner artifacts. The complete repository suite was not run, and Neris's predecessor validation is not claimed as Vesper work.",
                "Still incomplete are the immutable evidence commit and equality proof, closeout and content seal, exact-final manifests and staged review, exact-final commit and push, clean fresh four-way equality, one authorized exact-final owner-delta canonical completion, and the terminal live route reread. Protected incompleteness includes real people and affected-user evidence, professional astronomy and interferometry validation, real equipment and safety decisions, real keys and trust governance, empirical GMUT evidence, governed THOS arms, privacy and accessibility completeness, legal and cultural review, and Māori authority.",
                "A successor message is not evidence-stage execution. Only after Vesper's exact final is clean, pushed, fresh-live equal, below the 2,000-file guard, and canonically validated once may the newest live instruction, roster, authorization, usage, privacy, safety, evidence, and authority state be reread. The exact-title successor must be uniquely resolved and immediately reread before one sanitized send. Missing, ambiguous, paused, protected, unavailable, or opaque routing must remain PREPARED_NOT_SENT or OPAQUE_ACK_UNRESOLVED_NO_RESEND; no substitute endpoint or resend may be used merely for clarity.",
            ],
        ),
    ]


def build_overview() -> str:
    lines = [
        "# Vesper Arlen v666-v2 integrated evidence overview",
        "",
        "This document is the three-page-equivalent evidence overview for the owner-local v666-v2 delta. It is sanitized, repository-relative, and contains no raw task identifier, private route, credential, transcript, screenshot, session stream, private callable identifier, or protected real-world record.",
        "",
    ]
    for heading, body in paragraphs():
        lines.extend([f"## {heading}", ""])
        for paragraph in body:
            lines.extend([paragraph, ""])
    return "\n".join(lines)


def build_html(ledger: dict[str, Any], profiles: dict[str, Any], threats: dict[str, Any]) -> str:
    outcome_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{html.escape(row['proposal_id'])}</th>"
        f"<td>{html.escape(row['title'])}</td>"
        f"<td><span class=\"tag {html.escape(row['observed_disposition'])}\">{html.escape(row['observed_disposition'])}</span></td>"
        f"<td>{row['rejected_mutations']}/5</td>"
        "</tr>"
        for row in ledger["rows"]
    )
    source_rows = "\n".join(
        "<tr>"
        f"<th scope=\"row\">{html.escape(row['source_id'])}</th>"
        f"<td>{html.escape(row['name'])}</td>"
        f"<td>{html.escape(row['status'])}</td>"
        f"<td>{html.escape(row['bounded_use'])}</td>"
        "</tr>"
        for row in profiles["profiles"]
    )
    threat_items = "\n".join(
        f"<li><strong>{html.escape(row['threat_id'])}: {html.escape(row['asset'])}.</strong> "
        f"{html.escape(row['threat'])} Mitigation: {html.escape(row['mitigation'])} "
        f"Residual risk: {html.escape(row['residual_risk'])}</li>"
        for row in threats["threats"]
    )
    sections = []
    for heading, body in paragraphs():
        paras = "".join(f"<p>{html.escape(text)}</p>" for text in body)
        sections.append(f"<section aria-labelledby=\"{html.escape(heading.casefold().replace(' ', '-').replace(',', ''))}\"><h2 id=\"{html.escape(heading.casefold().replace(' ', '-').replace(',', ''))}\">{html.escape(heading)}</h2>{paras}</section>")
    narrative = "\n".join(sections)
    return f"""<!doctype html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vesper Arlen v666-v2 bounded evidence report</title>
<style>
:root {{ color-scheme: light dark; --bg:#f7f8fb; --fg:#17202a; --card:#ffffff; --line:#34495e; --focus:#7b2cbf; --done:#075e3b; --rep:#174c8f; --gap:#7a4e00; --gate:#8b1e3f; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font:1rem/1.62 system-ui,-apple-system,"Segoe UI",sans-serif; background:var(--bg); color:var(--fg); }}
a {{ color:inherit; text-decoration-thickness:.12em; }}
a:focus-visible, summary:focus-visible {{ outline:.2rem solid var(--focus); outline-offset:.2rem; }}
.skip-link {{ position:absolute; left:.5rem; top:-5rem; padding:.75rem 1rem; background:#fff; color:#000; z-index:10; }}
.skip-link:focus {{ top:.5rem; }}
header, main, footer {{ max-width:76rem; margin:auto; padding:1.25rem; }}
header {{ border-bottom:.25rem solid var(--line); }}
nav ul {{ display:flex; flex-wrap:wrap; gap:.5rem 1rem; padding-left:1.2rem; }}
section {{ background:var(--card); padding:1rem 1.25rem; margin:1rem 0; border-left:.35rem solid var(--line); }}
.summary {{ font-size:1.1rem; max-width:70ch; }}
.metrics {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(12rem,1fr)); gap:.75rem; padding:0; list-style:none; }}
.metrics li {{ border:.12rem solid var(--line); padding:.75rem; background:var(--card); }}
.metric {{ display:block; font-size:1.7rem; font-weight:750; }}
.table-wrap {{ overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; min-width:48rem; }}
caption {{ text-align:left; font-weight:750; padding:.75rem 0; }}
th, td {{ border:.08rem solid var(--line); padding:.55rem; text-align:left; vertical-align:top; }}
.tag {{ display:inline-block; padding:.1rem .45rem; border:.1rem solid currentColor; font-weight:700; }}
.completed {{ color:var(--done); }} .represented {{ color:var(--rep); }} .open_gap {{ color:var(--gap); }} .exact_gate {{ color:var(--gate); }}
.notice {{ border:.2rem solid var(--gate); padding:1rem; font-weight:650; }}
@media (prefers-reduced-motion: reduce) {{ *,*::before,*::after {{ scroll-behavior:auto!important; transition:none!important; animation:none!important; }} }}
@media print {{ nav,.skip-link {{ display:none; }} body {{ background:#fff; color:#000; }} section {{ break-inside:avoid; border-color:#000; }} }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#10151b; --fg:#f2f4f7; --card:#18212b; --line:#a9bacb; --focus:#e6a8ff; --done:#78e6b0; --rep:#92c5ff; --gap:#ffd166; --gate:#ff9bb5; }} }}
</style>
</head>
<body>
<a class="skip-link" href="#main">Skip to main evidence</a>
<header>
<p>GHC Family · owner-local synthetic evidence</p>
<h1>Vesper Arlen v666-v2 bounded evidence report</h1>
<p class="summary">Twenty synthetic contracts passed their bounded positives and rejected all one hundred preregistered mutations. The exact outcomes are 14 completed, 4 represented, 1 open gap, and 1 exact gate. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<nav aria-label="Report sections"><ul><li><a href="#metrics">Metrics</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#sources">Sources</a></li><li><a href="#threats">Threats</a></li><li><a href="#reservations">Reserved evaluation</a></li></ul></nav>
</header>
<main id="main" tabindex="-1">
<section id="metrics" aria-labelledby="metrics-heading"><h2 id="metrics-heading">Evidence metrics</h2>
<ul class="metrics"><li><span class="metric">20</span>bounded positives</li><li><span class="metric">100/100</span>mutations rejected</li><li><span class="metric">26,279</span>effective negatives</li><li><span class="metric">10,706</span>Method Flow methods</li><li><span class="metric">184</span>open gaps</li><li><span class="metric">182</span>exact gates</li></ul>
<p class="notice">All evidence is synthetic and same-owner. No real person, array, antenna, observatory, site, sky target, visibility, image, measurement, instrument action, identity event, professional act, authority decision, or Stage 20 evidence is present.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Core proposal outcomes</h2><div class="table-wrap"><table><caption>Twenty preregistered proposal outcomes and mutation results</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Bounded surface</th><th scope="col">Outcome</th><th scope="col">Rejected mutations</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="sources" aria-labelledby="sources-heading"><h2 id="sources-heading">Public-source profile</h2><p>These sources provide vocabulary and stop conditions only. They create no astronomical, interferometric, imaging, instrumentation, metrological, safety, professional, legal, cultural, affected-party, or Māori authority.</p><div class="table-wrap"><table><caption>Public sources, status, and bounded use</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Status</th><th scope="col">Bounded use</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
<section id="threats" aria-labelledby="threats-heading"><h2 id="threats-heading">Threat register</h2><ol>{threat_items}</ol></section>
{narrative}
<section id="reservations" aria-labelledby="reservations-heading"><h2 id="reservations-heading">Reserved evaluation</h2><p>Structural checks passed for language, skip navigation, landmarks, heading order, captions, scoped headers, visible focus, print rules, and reduced motion. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved and incomplete.</p></section>
</main>
<footer><p>Sanitized owner-local evidence. No scripts, forms, tracking resources, external assets, or network dependency.</p></footer>
</body>
</html>"""


def main() -> None:
    ledger = load("x2/proposal-ledger.json")
    profiles = load("provenance/source-profiles.json")
    threats = load("x1/threat-model.json")
    overlay = load("method-flow/x2-operational-overlay.json")
    if ledger["outcome_counts"] != {"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}:
        raise RuntimeError("unexpected outcome counts")
    if overlay["effective_negatives_after_this_overlay"] != 26277:
        raise RuntimeError("unexpected retained-negative count")

    write_json(
        "method-flow/evidence-operational-overlay.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.method-flow-evidence-operational-overlay.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "base_effective_negatives": 26277,
            "base_effective_methods": 10704,
            "new_operational_negative_count": 2,
            "new_operational_method_count": 2,
            "effective_negatives_after_this_overlay": EVIDENCE_NEGATIVES,
            "effective_methods_after_this_overlay": EVIDENCE_METHODS,
            "rows": [
                {
                    "failure_id": "VSP6662-EVID-N001",
                    "stage": "evidence_staged_review_orchestration",
                    "failure_class": "shell_yield_session_handle_omission",
                    "failed_witness": "the first staged-review process crossed the shell yield while its wrapper exposed output without preserving the returned session handle",
                    "credit": "zero_success_credit",
                    "isolated_recovery": "do not launch a duplicate; identify the exact owner process read-only and wait for that process to finish",
                    "recurrence_guard": "preserve the session identifier for every long-running command and poll only that exact session",
                    "passing_witness": "the exact process ended, the valid staged review and manifest appeared, and no duplicate process was launched",
                },
                {
                    "failure_id": "VSP6662-EVID-N002",
                    "stage": "evidence_accounting_patch",
                    "failure_class": "atomic_patch_context_rejection",
                    "failed_witness": "the combined evidence accounting patch rejected one HTML-context hunk and changed no file",
                    "credit": "zero_success_credit",
                    "isolated_recovery": "split accounting, narrative, HTML, and test corrections into exact-context patches",
                    "recurrence_guard": "inspect current line anchors before composing a multi-surface patch",
                    "passing_witness": "the split patches applied to the changed target without partial drift",
                },
            ],
            "no_failure_erased": True,
        },
    )

    write_json(
        "evidence/evidence-summary.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.evidence-summary.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "new_frozen_total": 4210,
            "outcomes": ledger["outcome_counts"],
            "bounded_positives": 20,
            "rejecting_mutations": 100,
            "accepted_mutations": 0,
            "repository_sealed_inherited": {"negatives": 26160, "methods": 10472, "open_gaps": 183, "exact_gates": 181},
            "inherited_external_overlay": {"negatives": 4, "methods": 4},
            "activation_message_stale_overlay": {"negatives": 1, "methods": 1, "omitted_external_failures": 3},
            "vesper_startup_and_x1": {"negatives": 11, "methods": 11},
            "vesper_x2": {"mutation_negatives": 100, "methods": 215, "operational_negatives": 2, "operational_methods": 2},
            "vesper_evidence": {"operational_negatives": 2, "operational_methods": 2},
            "effective": {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS, "open_gaps": 184, "exact_gates": 182},
            "real_rows": 0,
            "participants": 0,
            "network_calls_by_phase_software": 0,
            "external_actions": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner": True,
            "independent_reproduction": False,
        },
    )

    write_json(
        "evidence/environment-version-receipt.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.environment-version-receipt.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "python": {"version": platform.python_version(), "implementation": platform.python_implementation()},
            "git": command_version(["git", "--version"]),
            "powershell": command_version(["powershell", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.ToString()"]),
            "platform_family": sys.platform,
            "version_checks_only": True,
            "software_installed": 0,
            "software_updated": 0,
            "host_security_changed": False,
            "sandbox_or_hyper_v_changed": False,
            "elevation_used": False,
            "rebooted": False,
            "private_host_or_path_recorded": False,
        },
    )

    write_json(
        "evidence/threat-model-review.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.threat-model-review.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "threat_count": len(threats["threats"]),
            "reviewed_threat_ids": [row["threat_id"] for row in threats["threats"]],
            "new_material_threats": [],
            "residual_risks_visible": True,
            "security_claim": "bounded same-owner review only; not exhaustive security",
            "privacy_claim": "five-class value-bearing scan only; not privacy certification",
            "authority_gates_unchanged": True,
        },
    )

    write_json(
        "evidence/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.evidence-checklist.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "complete_bounded": [
                "read-first and exact source verification",
                "dedicated x1 commit, push, clean state, 0/0 divergence, and fresh four-way equality",
                "4,190-row semantic novelty audit and twenty-proposal freeze producing a 4,210-row chain",
                "twenty synthetic contracts and one hundred rejected mutations",
                "exact 14/4/1/1 core outcome ledger",
                "ten phase-local skills and ten family-current runners built and locally validated",
                "source profile, zero-call adapter, Trinity representations, Method Flow, and threat-model review",
                "structurally accessible static report and integrated evidence overview",
            ],
            "incomplete_lifecycle": [
                "immutable evidence commit, push, and fresh four-way equality",
                "combined closeout and seal commit",
                "exact-final staged review, manifests, push, clean state, and four-way equality",
                "single canonical owner-scoped exact-final completion",
                "fresh terminal roster and authorization reread and any permitted one-send route",
            ],
            "incomplete_protected": [
                "real astronomers, interferometrists, observatory workers, metrologists, affected parties, arrays, antennas, observatories, sites, coordinates, sky targets, visibilities, images, measurements, instruments, and evaluation evidence",
                "professional astronomy, interferometry, imaging, instrumentation, metrology, equipment, siting, or workplace-safety validation, privacy completeness, and accessibility completeness",
                "real Freed ID keys, proofs, interoperability, recovery, security review, and trust governance",
                "empirical GMUT evidence and governed THOS arms with independent review",
                "legal, cultural, copyright, remedy, Māori-language, Māori-data-governance, and Māori-authority review",
            ],
            "successor_contacted": False,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    write_json(
        "evidence/wellbeing-workload-check.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.wellbeing-workload-check.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "status": "bounded_with_failures_visible",
            "controls": [
                "caps used as ceilings rather than quotas",
                "eleven startup and x1 failures, two x2 operational failures, and one hundred rejecting mutations retained with zero failed-probe or mutation completion credit",
                "only failed dependencies repeated",
                "no unsafe task manufactured to fill a portfolio",
                "no successor precontact",
                "Hamish may pause, redirect, rename, or stop",
            ],
            "real_worker_observations": 0,
            "fatigue_inference": False,
            "personhood_or_emotion_claim": False,
        },
    )

    write_json(
        "evidence/authority-and-evidence-gaps.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.authority-and-evidence-gaps.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "open_gap_count": 184,
            "exact_gate_count": 182,
            "new_open_gap": {"proposal_id": "VSP6662-N019", "reason": "no live casacore or IVOA archive rows, version negotiation, interoperability event, or independent standard-owner semantic review"},
            "new_exact_gate": {"proposal_id": "VSP6662-N020", "reason": "observatory and sky disclosure, calibration release, worker safety, affected-party remedy, cultural review, and Māori authority absent"},
            "protected_claims": [
                "empirical GMUT",
                "real THOS effectiveness",
                "production Freed ID",
                "professional astronomy, interferometry, imaging, instrumentation, metrology, equipment, siting, or workplace-safety competence or conformance",
                "privacy-complete or accessibility-complete",
                "legal, cultural, affected-party, or Māori authority",
                "AGI, ASI, consciousness, personhood, Theory of Everything, proof, canon, or Stage 20",
            ],
            "no_gate_promoted": True,
        },
    )

    write_json(
        "evidence/portfolio-evidence-receipt.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.portfolio-evidence-receipt.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "safe_now_completed_bounded": 30,
            "bounded_candidates": {"completed": 5, "represented": 4, "open_gap": 1},
            "exact_approval_unexecuted": 10,
            "blocked_unexecuted": 5,
            "phase_local_skills_built_validated_smoke_used": 10,
            "family_current_runners_built_validated_smoke_used": 10,
            "clean_fix_refine_completed_bounded": 30,
            "global_installations": 0,
            "inherited_material_credit": 0,
            "real_world_completion_credit": 0,
        },
    )

    write_text("reports/integrated-evidence-overview.md", build_overview())
    write_text("reports/static-report.html", build_html(ledger, profiles, threats))

    write_json(
        "evidence/evidence-build-receipt.json",
        {
            "schema": "ghc.family.vesper-arlen.v666-v2.evidence-build-receipt.v1",
            "owner": "Vesper Arlen",
            "phase": "v666-v2",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_vesper_arlen_v666_v2_evidence.py",
            "report": "docs/vesper-arlen/v666-v2/reports/static-report.html",
            "overview": "docs/vesper-arlen/v666-v2/reports/integrated-evidence-overview.md",
            "outcomes": ledger["outcome_counts"],
            "effective_counts": {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS, "open_gaps": 184, "exact_gates": 182},
            "status": "EVIDENCE_CONTENT_BUILT_AWAITING_SCOPED_VALIDATION_STAGED_REVIEW_MANIFEST_COMMIT_PUSH_EQUALITY",
            "canonical_aggregate_invoked": False,
            "successor_contacted": False,
        },
    )
    print(json.dumps({"evidence_documents": 9, "report": True, "overview": True, "effective_negatives": EVIDENCE_NEGATIVES, "effective_methods": EVIDENCE_METHODS}, sort_keys=True))


if __name__ == "__main__":
    if sys.argv[1:] == ["--staged-review"]:
        build_evidence_staged_review()
    elif sys.argv[1:]:
        raise SystemExit("usage: build_ghc_family_vesper_arlen_v666_v2_evidence.py [--staged-review]")
    else:
        main()
