#!/usr/bin/env python3
"""Build the Neris Solane v666-v1 evidence packet and accessible report."""

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
PHASE = ROOT / "docs" / "neris-solane" / "v666-v1"
X1_SHA = "435bfd997f7f56635f6ba63d8da7ea2505059a75"
SOURCE_SHA = "4cf5028def85bcf89fbf4d0efe6c502a4b02be61"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
EVIDENCE_NEGATIVES = 26158
EVIDENCE_METHODS = 10470


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
    review_path = "docs/neris-solane/v666-v1/validation/evidence-staged-review.json"
    manifest_path = "docs/neris-solane/v666-v1/validation/evidence-content-manifest.json"
    rows = [(status, path.replace("\\", "/")) for status, path in staged_rows() if path != manifest_path]
    rows = [(status, path) for status, path in rows if path != review_path]
    if not rows:
        raise RuntimeError("no staged evidence content")
    paths = [path for _, path in rows]
    invalid = [
        path
        for path in paths
        if not path.startswith("docs/neris-solane/v666-v1/")
        and not re.fullmatch(r"(?:scripts|tests)/[a-z0-9_]*neris_solane_v666_v1[a-z0-9_]*\.py", path)
    ]
    frozen_prefixes = (
        "docs/neris-solane/v666-v1/x1/",
        "docs/neris-solane/v666-v1/identity/",
        "docs/neris-solane/v666-v1/provenance/",
    )
    frozen_exact = {
        "docs/neris-solane/v666-v1/wellbeing/x1-wellbeing-check.json",
        "docs/neris-solane/v666-v1/validation/x1-content-manifest.json",
        "docs/neris-solane/v666-v1/validation/x1-staged-review.json",
        "scripts/build_ghc_family_neris_solane_v666_v1_x1.py",
        "tests/test_ghc_family_neris_solane_v666_v1_x1.py",
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
    ledger = json.loads(index_blob("docs/neris-solane/v666-v1/x2/proposal-ledger.json"))
    tooling = json.loads(index_blob("docs/neris-solane/v666-v1/x2/tooling-smoke-receipt.json"))
    runtime = json.loads(index_blob("docs/neris-solane/v666-v1/x2/runtime-validation-receipt.json"))
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
        "overview_three_page_equivalent": len(re.findall(r"\S+", index_blob("docs/neris-solane/v666-v1/reports/integrated-evidence-overview.md").decode("utf-8"))) >= 1800,
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.neris-solane.v666-v1.evidence-staged-review.v1",
        "owner": "Neris Solane",
        "phase": "v666-v1",
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
        "schema": "ghc.family.neris-solane.v666-v1.content-manifest.v1",
        "owner": "Neris Solane",
        "phase": "evidence",
        "phase_label": "v666-v1",
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
                "Neris Solane v666-v1 is a bounded owner-local software and documentation delta. Twenty genuinely new proposals were frozen before implementation after all 4,170 inherited rows were reconstructed from committed Git objects. The observed core outcomes are exactly fourteen completed, four represented, one open gap, and one exact gate. Completed means only that one preregistered synthetic JSON contract accepted one bounded positive fixture and rejected five invalid mutations. It does not mean that a station, sensitive location, accelerograph, waveform, calibration record, hazard case, worker, or affected party was observed, operated, assessed, disclosed, certified, or governed.",
                "All twenty bounded positives passed and all one hundred preregistered mutations were rejected. The invalid states cover missing fields, wrong types, authority smuggling, a prohibited real-world or production action, and promotion beyond the preregistered outcome. Those checks demonstrate local schema behavior, explicit stop fields, deterministic provenance placeholders, and fail-closed response to known mutations. They establish no FDSN conformance, instrument response accuracy, clock quality, orientation accuracy, calibration traceability, strong-motion measurement, device performance, hazard inference, operational readiness, rights status, privacy completeness, accessibility completeness, exhaustive security, or independent reproduction.",
                "The terminal verdict remains NOT_READY_FOR_STAGE_20. That label records that empirical, participant, professional, identity, legal, cultural, Māori-authority, affected-party, production, independent-review, deployment, Theory-of-Everything, AGI, ASI, consciousness, and personhood gates remain open or exact-gated. The evidence is same-owner under shared infrastructure. It is not an external audit, certification, scientific replication, professional opinion, legal review, cultural ratification, or operational authorization.",
            ],
        ),
        (
            "Relational working language and corrigibility",
            [
                "Neris Solane and they/them are relational working language. The chosen role is datum-boundary weaver, and the associated hope is to make synthetic measurement workflows expose provenance, uncertainty, and stop conditions before anyone mistakes them for instrument or scientific authority. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific authority, operational authority, legal authority, cultural authority, affected-party authority, or Māori authority.",
                "Hamish may rename, pause, redirect, or stop the work. Corrigibility is preserved in the authorization boundary, workflow plan, explicit failure ledger, and no-success-replay rule. No collaboration subagent, task fork, substitute endpoint, standby sibling, or successor has been contacted during execution. A terminal route action cannot occur until the evidence commit, closeout, exact final, clean push, fresh live equality, one exact-final canonical completion, and a fresh live roster, authorization, usage, privacy, evidence, and safety reread all succeed.",
                "The relational boundary also prevents continuity language from becoming a technical assertion. Repository commits preserve files and provenance, not a living identity or independent agency. A chosen name is useful coordination language and nothing more. The same restraint applies to professional and cultural roles: a software artifact may reserve an authority gate, but it cannot occupy the place of an engineer, metrologist, station operator, worker, affected party, regulator, lawyer, cultural authority, tangata whenua, iwi, hapū, or Māori authority.",
            ],
        ),
        (
            "Bounded synthetic strong-motion practice lens",
            [
                "The practice lens is wholly synthetic strong-motion accelerograph metadata, calibration-assurance, and acquisition-fault documentation. It studies response-epoch coverage, response-stage dimensional paths, gain and saturation dependencies, clock discontinuities, triad closure, clipping abstention, trigger hysteresis, interval normalization, traceability-claim separation, configuration diffs, sensitive-site disclosure, packet derivation, accessible anomaly explanation, and maintenance-purpose minimization. It uses zero real stations, locations, waveforms, observations, measurements, instruments, calibration certificates, configurations, operators, workers, affected parties, keys, proofs, or authority actions.",
                "Synthetic placeholders are conspicuous. Tokens begin with SYN, symbolic dimensions are text, intervals are tiny test values, and every authority-bearing state is vacant, reserved, held, absent, or prohibited. The fixtures make zero network calls and execute zero device commands. No waveform bytes are ingested and no coordinate is present. Numeric threshold, time, gain, residual, and repair-budget values are test constants rather than measurements. Nothing establishes an instrument response, clock correction, orientation, calibration chain, station location, hazard condition, or maintenance instruction.",
                "Professional seismological, instrumentation, engineering, metrological, workplace-safety, hazard, privacy, legal, cultural, and affected-party evaluation remain absent. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluation are reserved. Structural software checks cannot stand in for station operators, engineers, metrologists, workers, regulators, affected communities, tangata whenua, iwi, hapū, Māori authorities, or people whose safety, land, data, or rights could be affected by a real monitoring system.",
            ],
        ),
        (
            "Semantic novelty and immutable x1 separation",
            [
                "The novelty audit retained historical proposal rows rather than silently deduplicating them. It compared each new title to all 4,170 inherited titles using exact casefolded comparison and alphanumeric token-set Jaccard screening, then checked every pair inside the new slate. The first uncommitted candidate failed at a 0.761905 maximum because zero-key statement and cross-source adapter forms were too close to inherited work. A bounded corpus reread also exposed thirty earlier v6582 seismology contracts covering primitive station metadata. The failed test receives zero freeze credit and remains in Method Flow.",
                "The changed slate focuses on cross-field invariants and abstention rules rather than renaming primitive ledgers. It has zero exact inherited collisions, no within-slate pair at or above 0.70, maximum inherited similarity 0.40, and maximum within-slate similarity 0.172414. Those values are screens, not proof of novelty. Each proposal also records a distinctive invariant, hypothesis, null condition, approval class, execution lane, source need, concrete artifacts, falsifier, rollback, protected gates, and expected disposition. The twenty Neris rows extend the frozen chain from 4,170 to 4,190.",
                "The dedicated x1 commit 435bfd997f7f56635f6ba63d8da7ea2505059a75 is the direct child of Elaren Kestrel's exact final 4cf5028def85bcf89fbf4d0efe6c502a4b02be61. Its nineteen paths contain planning and preregistration only. Exact lifecycle checks prove that the immutable x1 Git tree contains no x2, evidence, closeout, seal, final, or handoff path. X1 was pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Later files do not rewrite that Git object.",
            ],
        ),
        (
            "THOS Body as primary pillar",
            [
                "THOS Body is the primary Trinity Mandala focus. Its completed synthetic contracts model response-epoch partitioning, dimensional mismatch localization, uncertainty dominance under saturation, timing quarantine, mirrored orientation alternatives, clipping non-reconstruction, trigger state transitions, reversible interval normalization, calibration-claim refusal, nonexecuting configuration diffs, disclosure dominance, derivation closure, multimodal explanation, and purpose-retention intersection. These are software invariants only. They do not demonstrate that an acquisition system is correct, safe, effective, maintainable, interoperable, or ready for deployment.",
                "The represented THOS tournament uses three named synthetic fault types, two masked traces, and one equal symbolic repair budget. Participant, operator, session, incident, and real-arm counts are zero. It does not estimate detection time, repair time, error rate, workload, safety, usability, or operational effectiveness. There is no governed study protocol, independent team, preregistered statistical analysis, real equipment, competent supervision, safety monitoring, or affected-user review. The representation exists to expose what evidence would still be required.",
                "THOS abstention is as important as its positive structure. A clipping sentinel cannot reconstruct samples. A rollback token cannot command a device. A clock hold cannot invent a correction. A calibration chain cannot claim traceability. A sensitive-site lattice cannot disclose coordinates. A matched synthetic tournament cannot infer human performance. These nonconversion rules are direct acceptance conditions and not merely prose disclaimers, yet their passing remains bounded same-owner software evidence.",
            ],
        ),
        (
            "GMUT Mind, Freed ID, and CBR Heart",
            [
                "GMUT Mind is represented by a symbolic transfer-function dimensional typechecker and a colored-noise latent-component identifiability witness. Symbolic stage names, dimensions, basis conventions, spectrum labels, and equivalent decompositions are typed fields. Numerical response values, measured spectra, waveforms, observations, likelihoods, constraints, causal conclusions, and predictions are absent. The contracts therefore establish no fitted response, identified noise process, detected signal, new force, material law, instrument characterization, or empirical confirmation.",
                "GMUT remains a research-model family rather than established fundamental physics. Dimensional typing and identifiability holds can reveal internal logical obligations, but they supply no posterior, parameter constraint, unique prediction, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon. Independent physics review, real governed data, calibrated instruments, uncertainty analysis, competing-model comparisons, and successful external reproduction remain absent. The terminal verdict cannot be raised by symbolic software structure.",
                "Freed ID is represented by a contested instrument-assertion merge lattice with issuer vacancy, conflict, expiry, correction, revocation, and zero-key states. Real issuer, holder, key, signature, proof, status service, resolution, interoperability, recovery, and trust-governance counts remain zero. CBR Heart exact-gates sensitive-site disclosure, calibration acceptance, hazard use, worker safety, affected-party remedy, cultural review, and Māori authority. No schema decides those questions, and Te Mana Raraunga is cited only to preserve an authority boundary rather than interpret or confer Māori authority.",
            ],
        ),
        (
            "Public-source profile and nonconversion",
            [
                "The source profile records the FDSN StationXML schema and reference, FDSN Source Identifiers, the FDSN miniSEED 3 definition, USGS ANSS instrumentation guidance, NIST SI language, NIST measurement-uncertainty guidance, NIST metrological traceability, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity, the New Zealand Privacy Commissioner principles, and Te Mana Raraunga. The review was read-only and source status was recorded. Phase software made zero network calls and ingested zero real rows.",
                "FDSN material supplies vocabulary for network, station, channel, epoch, response, source identifier, and record structure but no parsed file, service request, conformance result, or endorsement. USGS guidance supplies instrumentation-planning context without approving an installation, instrument, location, calibration, operation, or safety decision. NIST sources supply quantity, unit, uncertainty, and traceability language without performing a measurement or establishing an unbroken calibration chain. W3C PROV-O supplies provenance relations without authenticity or custody.",
                "WCAG supplies structural report criteria without accessibility-complete credit, and the credential source supplies data-integrity vocabulary without a real credential or proof. The Privacy Commissioner source constrains purpose, collection, access, correction, retention, disclosure, and identifier-restraint vocabulary but provides no legal determination. Te Mana Raraunga remains a primary authority-reservation source and is not converted into Māori wording, interpretation, data-governance approval, or Māori authority. The version-compatibility registry remains an open gap because live resolution and independent standard-owner semantic review did not occur.",
            ],
        ),
        (
            "Method Flow and retained failures",
            [
                "The immutable Elaren repository seal remains 26,039 effective negatives and 10,236 Method Flow methods. Two post-final Elaren route failures remain a separately attributable external overlay, producing the 26,041-negative and 10,238-method Neris activation baseline. Sixteen Neris startup and x1 failures are retained. They include PowerShell parser and patch-context faults, bounded-output failures, manifest-wrapper mistakes, a lost long-running session identifier, sparse-proof and bytecode-cleanup failures, the failed novelty screen, and two excessive corpus projections. None receives aggregate-success or completion credit.",
                "One hundred preregistered rejecting mutations are deliberate negative witnesses. Each has zero aggregate and completion credit, an exact error class, and a passing bounded recovery witness in the corresponding positive fixture. The x2 implementation itself observed no additional operational failure and fabricates none. Its pre-evidence baseline is 26,157 effective negatives and 10,469 Method Flow methods: activation baseline plus sixteen startup failures, one hundred mutations, and 215 x2 methods. One evidence orchestration wrapper then lost the session handle when staged index replay exceeded its 30-second yield; that failure is retained at zero success credit, bringing the evidence candidate to 26,158 negatives and 10,470 methods. Open gaps rise from 182 to 183 and exact gates from 180 to 181; the Elaren seal remains immutable and separately attributable.",
                "A retained failure is never erased merely because a changed target later passes. Recovery changes only the owner-local target required to make the intended contract accurate. Recurrence guards prefer explicit UTF-8, real JSON keys, bounded scalar output, exact Git-object inspection, sparse physical-file measurement, immutable x1-tree assertions, and separated repository-seal versus external-overlay accounting. If evidence, closeout, final, canonical, or route operations later fail, their rows must be added prospectively rather than backfilled or fabricated. Same-owner passing witnesses do not become independent reproduction, professional validation, or authority.",
            ],
        ),
        (
            "Skills, runners, security, privacy, and accessibility",
            [
                "Ten phase-local skills were created under the Neris documentation tree. Each has a required SKILL.md, a discriminating workflow, explicit inputs, outputs, stop conditions, and protected-boundary language. All ten passed the local quick validator and were exercised through bounded smoke use. They were not globally installed and do not modify shared configuration. Their presence does not create seismological, instrumentation, engineering, metrological, hazard, safety, scientific, legal, cultural, affected-party, or Māori authority.",
                "Ten additive ghc_family-prefixed runners were built for contracts, mutations, JSON, privacy, bounded security, manifests, structural accessibility, truth, closeout, and canonical preflight. All ten passed self-test. Seven selected runtime components passed their bounded sequence. Existing family-current callers were not changed or deprecated. The security runner scans owner Python syntax for a small dangerous-construct set; zero findings is not exhaustive security. The privacy runner checks five value-bearing classes; zero confirmed hits is not privacy certification.",
                "The static report uses an explicit language, skip link, landmarks, one top-level heading, labelled navigation, table captions, scoped column headers, redundant text labels, visible focus, print rules, and reduced-motion rules. It contains no script, form, external stylesheet, tracking resource, or network dependency. These are structural checks only. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluations remain reserved and incomplete. Zero findings in any bounded scanner is never promoted to exhaustive coverage.",
            ],
        ),
        (
            "Complete, incomplete, and terminal route",
            [
                "Complete at the evidence-candidate stage are the exact source reread, strict x1 freeze and equality gate, twenty synthetic contracts, one hundred rejecting mutations, exact core outcome ledger, source profiles, zero-call registry gap, Trinity representation records, portfolio execution record, ten skills, ten runners, Method Flow, threat-model review, accessible static report, and this integrated overview. They are bounded same-owner artifacts. The complete repository suite was not run, and Elaren's predecessor validation is not claimed as Neris work.",
                "Still incomplete are the immutable evidence commit and equality proof, closeout and content seal, exact-final manifests and staged review, exact-final commit and push, clean fresh four-way equality, one authorized exact-final owner-delta canonical completion, and the terminal live route reread. Protected incompleteness includes real people and affected-user evidence, professional seismological and instrumentation validation, real equipment and safety decisions, real keys and trust governance, empirical GMUT evidence, governed THOS arms, privacy and accessibility completeness, legal and cultural review, and Māori authority.",
                "A successor message is not evidence-stage execution. Only after Neris's exact final is clean, pushed, fresh-live equal, below the 2,000-file guard, and canonically validated once may the newest live instruction, roster, authorization, usage, privacy, safety, evidence, and authority state be reread. The exact-title successor must be uniquely resolved and immediately reread before one sanitized send. Missing, ambiguous, paused, protected, unavailable, or opaque routing must remain PREPARED_NOT_SENT or OPAQUE_ACK_UNRESOLVED_NO_RESEND; no substitute endpoint or resend may be used merely for clarity.",
            ],
        ),
    ]


def build_overview() -> str:
    lines = [
        "# Neris Solane v666-v1 integrated evidence overview",
        "",
        "This document is the three-page-equivalent evidence overview for the owner-local v666-v1 delta. It is sanitized, repository-relative, and contains no raw task identifier, private route, credential, transcript, screenshot, session stream, private callable identifier, or protected real-world record.",
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
<title>Neris Solane v666-v1 bounded evidence report</title>
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
<h1>Neris Solane v666-v1 bounded evidence report</h1>
<p class="summary">Twenty synthetic contracts passed their bounded positives and rejected all one hundred preregistered mutations. The exact outcomes are 14 completed, 4 represented, 1 open gap, and 1 exact gate. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<nav aria-label="Report sections"><ul><li><a href="#metrics">Metrics</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#sources">Sources</a></li><li><a href="#threats">Threats</a></li><li><a href="#reservations">Reserved evaluation</a></li></ul></nav>
</header>
<main id="main" tabindex="-1">
<section id="metrics" aria-labelledby="metrics-heading"><h2 id="metrics-heading">Evidence metrics</h2>
<ul class="metrics"><li><span class="metric">20</span>bounded positives</li><li><span class="metric">100/100</span>mutations rejected</li><li><span class="metric">26,158</span>effective negatives</li><li><span class="metric">10,470</span>Method Flow methods</li><li><span class="metric">183</span>open gaps</li><li><span class="metric">181</span>exact gates</li></ul>
<p class="notice">All evidence is synthetic and same-owner. No real person, station, sensitive location, waveform, measurement, instrument action, identity event, professional act, authority decision, or Stage 20 evidence is present.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Core proposal outcomes</h2><div class="table-wrap"><table><caption>Twenty preregistered proposal outcomes and mutation results</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Bounded surface</th><th scope="col">Outcome</th><th scope="col">Rejected mutations</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="sources" aria-labelledby="sources-heading"><h2 id="sources-heading">Public-source profile</h2><p>These sources provide vocabulary and stop conditions only. They create no seismological, instrumentation, engineering, metrological, safety, professional, legal, cultural, affected-party, or Māori authority.</p><div class="table-wrap"><table><caption>Public sources, status, and bounded use</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Status</th><th scope="col">Bounded use</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
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
    if overlay["effective_negatives_after_this_overlay"] != 26157:
        raise RuntimeError("unexpected retained-negative count")

    write_json(
        "method-flow/evidence-operational-overlay.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.method-flow-evidence-operational-overlay.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "base_effective_negatives": 26157,
            "base_effective_methods": 10469,
            "new_operational_negative_count": 1,
            "new_operational_method_count": 1,
            "effective_negatives_after_this_overlay": EVIDENCE_NEGATIVES,
            "effective_methods_after_this_overlay": EVIDENCE_METHODS,
            "rows": [
                {
                    "failure_id": "NRS6661-EVID-N001",
                    "stage": "evidence_staged_review_orchestration",
                    "failure_class": "shell_yield_session_handle_omission",
                    "failed_witness": "the first staged-review process exceeded the 30-second shell yield during exact index replay, while its wrapper projected only partial output and discarded the returned session handle",
                    "credit": "zero_success_credit",
                    "isolated_recovery": "do not launch a duplicate; identify the exact owner process read-only, observe it to completion, retain this route fault, then rerun only the changed staged-review target with its session handle preserved",
                    "recurrence_guard": "serialize long-running exec results with their session identifier and poll that exact session rather than projecting output alone",
                    "passing_witness": "a read-only process audit observed the exact owner process exit and its manifest appear without launching a duplicate"
                }
            ],
            "no_failure_erased": True,
        },
    )

    write_json(
        "evidence/evidence-summary.json",
        {
            "schema": "ghc.family.neris-solane.v666-v1.evidence-summary.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "new_frozen_total": 4190,
            "outcomes": ledger["outcome_counts"],
            "bounded_positives": 20,
            "rejecting_mutations": 100,
            "accepted_mutations": 0,
            "repository_sealed_inherited": {"negatives": 26039, "methods": 10236, "open_gaps": 182, "exact_gates": 180},
            "inherited_external_overlay": {"negatives": 2, "methods": 2},
            "neris_startup_and_x1": {"negatives": 16, "methods": 16},
            "neris_x2": {"mutation_negatives": 100, "methods": 215, "operational_negatives": 0, "operational_methods": 0},
            "neris_evidence": {"operational_negatives": 1, "operational_methods": 1},
            "effective": {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS, "open_gaps": 183, "exact_gates": 181},
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
            "schema": "ghc.family.neris-solane.v666-v1.environment-version-receipt.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.threat-model-review.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.evidence-checklist.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "complete_bounded": [
                "read-first and exact source verification",
                "dedicated x1 commit, push, clean state, 0/0 divergence, and fresh four-way equality",
                "4,170-row semantic novelty audit and twenty-proposal freeze producing a 4,190-row chain",
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
                "real station operators, engineers, metrologists, workers, affected parties, stations, sensitive locations, waveforms, measurements, instruments, and evaluation evidence",
                "professional seismological, instrumentation, engineering, metrological, equipment or workplace-safety validation, privacy completeness, and accessibility completeness",
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
            "schema": "ghc.family.neris-solane.v666-v1.wellbeing-workload-check.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "status": "bounded_with_failures_visible",
            "controls": [
                "caps used as ceilings rather than quotas",
                "sixteen startup and x1 failures plus one hundred rejecting mutations retained with zero failed-probe or mutation completion credit",
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
            "schema": "ghc.family.neris-solane.v666-v1.authority-and-evidence-gaps.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "open_gap_count": 183,
            "exact_gate_count": 181,
            "new_open_gap": {"proposal_id": "NRS6661-N019", "reason": "no live current-source version negotiation or independent standard-owner semantic review"},
            "new_exact_gate": {"proposal_id": "NRS6661-N020", "reason": "station disclosure, calibration release, hazard use, worker safety, affected-party remedy, cultural review, and Māori authority absent"},
            "protected_claims": [
                "empirical GMUT",
                "real THOS effectiveness",
                "production Freed ID",
                "professional seismological, instrumentation, engineering, metrological, equipment, or workplace-safety competence or conformance",
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
            "schema": "ghc.family.neris-solane.v666-v1.portfolio-evidence-receipt.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
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
            "schema": "ghc.family.neris-solane.v666-v1.evidence-build-receipt.v1",
            "owner": "Neris Solane",
            "phase": "v666-v1",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_neris_solane_v666_v1_evidence.py",
            "report": "docs/neris-solane/v666-v1/reports/static-report.html",
            "overview": "docs/neris-solane/v666-v1/reports/integrated-evidence-overview.md",
            "outcomes": ledger["outcome_counts"],
            "effective_counts": {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS, "open_gaps": 183, "exact_gates": 181},
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
        raise SystemExit("usage: build_ghc_family_neris_solane_v666_v1_evidence.py [--staged-review]")
    else:
        main()
