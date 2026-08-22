#!/usr/bin/env python3
"""Build the Eiren Kestrel v665-v7 evidence packet and accessible report."""

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
PHASE = ROOT / "docs" / "eiren-kestrel" / "v665-v7"
X1_SHA = "b506a51a5b22c6bab84bdd2748a0deb1e85d145b"
SOURCE_SHA = "959c32796fb822dba0a670c162d9489a044d0554"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
EVIDENCE_NEGATIVES = 25917
EVIDENCE_METHODS = 9999


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
    review_path = "docs/eiren-kestrel/v665-v7/validation/evidence-staged-review.json"
    manifest_path = "docs/eiren-kestrel/v665-v7/validation/evidence-content-manifest.json"
    rows = [(status, path.replace("\\", "/")) for status, path in staged_rows() if path != manifest_path]
    rows = [(status, path) for status, path in rows if path != review_path]
    if not rows:
        raise RuntimeError("no staged evidence content")
    paths = [path for _, path in rows]
    invalid = [
        path
        for path in paths
        if not path.startswith("docs/eiren-kestrel/v665-v7/")
        and not re.fullmatch(r"(?:scripts|tests)/[a-z0-9_]*eiren_kestrel_v665_v7[a-z0-9_]*\.py", path)
    ]
    frozen_prefixes = (
        "docs/eiren-kestrel/v665-v7/x1/",
        "docs/eiren-kestrel/v665-v7/identity/",
        "docs/eiren-kestrel/v665-v7/provenance/",
    )
    frozen_exact = {
        "docs/eiren-kestrel/v665-v7/wellbeing/x1-wellbeing-check.json",
        "docs/eiren-kestrel/v665-v7/validation/x1-content-manifest.json",
        "docs/eiren-kestrel/v665-v7/validation/x1-staged-review.json",
        "scripts/build_ghc_family_eiren_kestrel_v665_v7_x1.py",
        "tests/test_ghc_family_eiren_kestrel_v665_v7_x1.py",
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
    ledger = json.loads(index_blob("docs/eiren-kestrel/v665-v7/x2/proposal-ledger.json"))
    tooling = json.loads(index_blob("docs/eiren-kestrel/v665-v7/x2/tooling-smoke-receipt.json"))
    runtime = json.loads(index_blob("docs/eiren-kestrel/v665-v7/x2/runtime-validation-receipt.json"))
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
        "overview_three_page_equivalent": len(re.findall(r"\S+", index_blob("docs/eiren-kestrel/v665-v7/reports/integrated-evidence-overview.md").decode("utf-8"))) >= 1800,
        "utf8_lf": True,
    }
    review = {
        "schema": "ghc.family.eiren-kestrel.v665-v7.evidence-staged-review.v1",
        "owner": "Eiren Kestrel",
        "phase": "v665-v7",
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
        "schema": "ghc.family.eiren-kestrel.v665-v7.content-manifest.v1",
        "owner": "Eiren Kestrel",
        "phase": "evidence",
        "phase_label": "v665-v7",
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
                "Eiren Kestrel v665-v7 produced a bounded owner-local software and documentation delta. Twenty genuinely new proposals were frozen before implementation. Their observed core outcomes are exactly fourteen completed, four represented, one open gap, and one exact gate. Completed means only that a preregistered synthetic JSON contract accepted its bounded positive and rejected its five invalid states. It does not mean that a paper sheet was made, a fibre or material was identified, a machine was operated, a person participated, or a professional, legal, cultural, accessibility, privacy, safety, environmental, or authority decision was made.",
                "Every contract has one bounded positive fixture and five preregistered rejecting mutations. All twenty positives passed and all one hundred mutations were rejected. Those tests demonstrate only the declared local structure, provenance fields, zero-action locks, and fail-closed behavior. They do not establish ISO conformance, papermaking quality, conservation fitness, material authenticity, environmental performance, machine safety, accessibility completeness, privacy completeness, exhaustive security, or independent reproduction.",
                "The terminal verdict remains NOT_READY_FOR_STAGE_20. That verdict is a repository evidence label saying that protected empirical, participant, professional, identity, legal, cultural, Māori-authority, production, independent-review, and deployment gates remain open or exact-gated.",
            ],
        ),
        (
            "Relational working language and corrigibility",
            [
                "Eiren Kestrel and the pronouns she/her are relational working language for this lane. The relational role is pattern cartographer and boundary steward. The associated hope is to make formal structure legible while leaving real competence, rights, safety, and authority with the people who hold them. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.",
                "Hamish may rename, pause, redirect, or stop the work. Corrigibility is preserved in the authorization record and workflow plan. No successor has been contacted during execution. Elaren Kestrel v665-v8 remains a prospective route label only until the evidence commit, closeout, exact final, clean push, fresh-live equality, and one-shot final-validation gates are complete and the newest live roster and authorization have been reread.",
            ],
        ),
        (
            "Bounded practice lens",
            [
                "The human-practice lens is wholly synthetic hand-papermaking sheet-formation documentation. It provides a disciplined vocabulary for job intake, fibre-furnish lineage, vat state, mould-and-deckle topology, sheet-formation events, couching and felt stacks, pressing and drying holds, additives, watermarks, count reconciliation, bitemporal correction, accessible process maps, privacy, rights, and handover. The phase uses zero real papermakers, workers, workshops, fibres, pulp, water, vats, moulds, deckles, felts, presses, dryers, additives, sheets, images, measurements, commands, keys, proofs, credentials, or authority decisions.",
                "Synthetic placeholders are deliberately conspicuous. Tokens begin with SYN or describe a vacancy, reserve, unknown state, or prohibition. Numeric values are test constants rather than measurements. The press firewall accepts only a simulated stack with zero machine calls. Furnish, watermark, design, and sheet records are anonymous synthetic tokens. The phase neither handles material nor authenticates fibre origin, authorship, design, edition, custody, or conservation condition.",
                "Professional, worker, affected-party, and manual accessibility evaluation remain absent. The static report reserves browser, keyboard, zoom, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation. Structural markup checks can catch missing landmarks, captions, or header scopes, but they do not stand in for the people, professions, communities, or authorities whose interests could be affected by a real system.",
            ],
        ),
        (
            "Semantic novelty and x1 separation",
            [
                "The novelty audit reconstructed exactly 4,130 inherited rows from committed Git objects. It retained historical reappended selection rows instead of silently deduplicating them. Twenty Eiren titles had zero exact collisions and no within-slate pair reached the preregistered 0.70 token-Jaccard ceiling. Automated similarity was treated only as a screen; every proposal also required a distinct domain contract, hypothesis, falsifier, recovery, approval class, current source need, and protected-gate set.",
                "The dedicated x1 commit b506a51a5b22c6bab84bdd2748a0deb1e85d145b is the direct child of Caelen's immutable final. Its nineteen paths contain planning and preregistration only. Exact lifecycle checks prove that x1 contains no x2, evidence, closeout, seal, final, or handoff path. X1 was committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before x2 began. Later lifecycle files do not rewrite that immutable Git tree.",
                "Twenty Caelen proposals were selected for bounded revalidation. They carry zero Eiren novelty and zero automatic completion credit. The effective frozen chain grows by the twenty genuinely new Eiren proposals only, from 4,130 to 4,150.",
            ],
        ),
        (
            "GMUT Mind",
            [
                "GMUT Mind is the primary Trinity Mandala focus. The discrete fibre-network surrogate and drainage-and-formation tensor are typed symbolic placeholders used to exercise software boundaries. Fibre-node tokens, adjacency matrices, orientation placeholders, drainage operators, unit obligations, covariance vacancies, and boundary-data holds have no fitted physical interpretation. Observation count and coefficient count are zero, identifiability is unresolved, and prediction claims are hard false.",
                "There is no real likelihood, posterior, parameter constraint, detected force, material law, quality model, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon. The validators reject promotion markers and retain both GMUT proposals as represented. Mathematical notation can invite over-reading, so zero-observation, zero-coefficient, and no-prediction fields are contract requirements rather than optional commentary.",
            ],
        ),
        (
            "THOS Body, Freed ID, and CBR Heart",
            [
                "THOS Body is represented by a participant-free matched-queue charter. It names two synthetic documentation views, a symbolic equal action budget, blinded artifact labels, sealed synthetic tasks, and dominant stop precedence. It has zero participants, operators, sessions, safety events, arms, or outcomes. Safety monitoring, appropriate statistics, and independent review are explicitly absent, so it establishes no operational effectiveness.",
                "Freed ID is represented by a zero-key sheet-provenance statement graph. It binds synthetic furnish, formation, correction, status, disclosure-purpose, and expiry tokens, but it has zero real keys and zero proofs. It performs no issuance, presentation, verification, resolution, status, revocation, recovery, interoperability, or trust-governance operation.",
                "CBR Heart remains exact-gated for fibre origin, traditional knowledge, environmental claims, copyright and design rights, worker safety, remedy, affected-party legitimacy, legal and cultural interpretation, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority. The authority docket records zero approvals and is not a decision procedure.",
            ],
        ),
        (
            "Public-source profile",
            [
                "The public-source profile records ISO 5269-2, Canadian Conservation Institute paper-object guidance, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity 1.0, NIST SI and uncertainty guidance, New Zealand privacy principles, WorkSafe New Zealand machinery and hazardous-substance guidance, and Te Mana Raraunga principles. The review was read-only. The phase software made zero network calls and ingested zero real rows.",
                "Source status is part of the evidence. ISO supplies only a title-level laboratory-sheet vocabulary and no standard text or conformance credit. CCI informs broad paper and fibre conservation vocabulary but does not authorize a treatment. NIST provides quantity, unit, and uncertainty language without a measurement. WCAG supplies structural report vocabulary but does not authorize an accessibility-complete claim. WorkSafe sources supply stop and hazard-reservation language but no machine or chemical advice.",
                "The source-adapter proposal remains an open gap because the phase did not perform live current-source retrieval or schema negotiation. That restraint preserves the difference between a recorded public-source profile and a current interoperable adapter.",
            ],
        ),
        (
            "Method Flow and retained failures",
            [
                "The inherited repository seal remains 25,797 effective negatives and 9,769 Method Flow methods. Caelen's failed canonical invocation and failed r1 recovery remain external at zero credit, producing an activation baseline of 25,799 negatives and 9,771 methods. Fifteen Eiren startup failures are retained. They include output truncation, parser construction, guessed paths, a bounded search interruption, partial worktree initialization, and a Unicode console-codec miss. No failed witness was erased.",
                "One hundred preregistered mutations are retained as deliberate negative witnesses. One x2 operational failure is retained: the first compact Python import probe omitted the repository scripts search path and raised ModuleNotFoundError. Two evidence-stage operational failures are also retained. First, a valid staged review persisted receipts but its visible tool-result stream exceeded the output/context budget. Second, the target-changed staged review crossed its ten-second yield boundary and an output-only wrapper discarded the live session handle. The recovery did not overlap or replay the live process: a process-tree probe found the exact Python process, a bounded wait observed its completion, and scalar receipt inspection proved 14 of 14 review checks with a 112-entry manifest. Both failures earn zero credit.",
                "The resulting evidence-stage totals are 25,917 effective negatives and 9,999 Method Flow methods before later closeout or final operational overlays. Open gaps rise from 180 to 181 and exact gates rise from 178 to 179. These totals preserve the immutable inherited seal, the two external Caelen failures, and Eiren's startup, mutation, x2 operational, and evidence operational overlays as separately attributable layers.",
            ],
        ),
        (
            "Tooling and validation scope",
            [
                "Ten phase-local skills were created under the owner documentation tree. The skill-creator guidance shaped them into short, discriminating packages with a required SKILL.md, explicit workflow, and stop conditions. All ten passed the local quick validator. They were not globally installed and do not modify unrelated configuration. Their presence does not create papermaking, conservation, safety, scientific, legal, cultural, or Māori authority.",
                "Ten additive ghc_family-prefixed runners were built for contracts, mutations, JSON, privacy, bounded security, manifests, structural accessibility, truth, closeout, and canonical preflight. All ten passed a local self-test. The contract, mutation, JSON, privacy, security, manifest, and truth runners received bounded actual use. Existing family-current callers were not modified or deprecated.",
                "The bounded security runner scans owner Python syntax for a small set of dangerous constructs and shell-enabled subprocess use. Zero findings is not exhaustive security. The privacy runner checks five value-bearing classes and reports candidates for manual classification. Zero confirmed hits is not privacy certification. Exact Git-blob manifests, staged review, clean state, direct ancestry, zero merges, file caps, divergence, and fresh live equality remain separate lifecycle gates.",
            ],
        ),
        (
            "Threat model and accessibility",
            [
                "The threat model covers source and sibling-lane mutation, x1/x2 leakage, semantic duplication, private route disclosure, false papermaking competence, material or environmental truth promotion, worker and affected-party substitution, Māori-authority conversion, scientific overclaim, THOS and Freed ID promotion, canonical replay, and premature route delivery. Residual risks remain visible because same-owner checks cannot supply independent review, professional judgment, or community authority.",
                "The static report uses an explicit language, a skip link, landmark elements, a single top-level heading, labelled navigation, table captions, scoped column headers, text labels alongside color, visible focus, print rules, and reduced-motion rules. There is no script, form, external stylesheet, tracking resource, or network dependency. These are structural checks only. Manual browser, keyboard, zoom, screen-reader, cognitive-accessibility, Māori-language, and affected-user evaluations are reserved.",
            ],
        ),
        (
            "Complete, incomplete, and terminal route",
            [
                "Complete at the evidence stage are the x1 freeze and equality gate, twenty synthetic contracts, one hundred rejecting mutations, exact core outcome ledger, source profiles, zero-call adapter gap, Trinity representation records, portfolio execution record, ten skills, ten runners, Method Flow, threat-model review, accessible static report, and this integrated overview. These are bounded same-owner artifacts.",
                "Incomplete are the immutable evidence commit and equality proof, combined closeout and seal, final manifests, final staged review, exact-final push and equality, one authorized canonical completion, and the terminal route reread. Also incomplete by protected design are real people and affected-user evidence, professional papermaking and conservation validation, machine and chemical safety decisions, real keys and trust governance, empirical GMUT evidence, governed THOS arms, privacy and accessibility completeness, legal and cultural review, and Māori authority.",
                "A successor message is not part of evidence-stage execution. Only after the final is clean, pushed, fresh-live equal, within caps, and exact-final validated may the newest live authorization and roster be reread. If the exact Elaren Kestrel task is uniquely available and the edge remains explicit, one sanitized send may occur. Any missing, ambiguous, paused, protected, or opaque route state must remain PREPARED_NOT_SENT or OPAQUE_ACK_UNRESOLVED_NO_RESEND as applicable.",
            ],
        ),
    ]
def build_overview() -> str:
    lines = [
        "# Eiren Kestrel v665-v7 integrated evidence overview",
        "",
        "This document is the three-page-equivalent evidence overview for the owner-local v665-v7 delta. It is sanitized, repository-relative, and contains no raw task identifier, private route, credential, transcript, screenshot, session stream, private callable identifier, or protected real-world record.",
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
<title>Eiren Kestrel v665-v7 bounded evidence report</title>
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
<h1>Eiren Kestrel v665-v7 bounded evidence report</h1>
<p class="summary">Twenty synthetic contracts passed their bounded positives and rejected all one hundred preregistered mutations. The exact outcomes are 14 completed, 4 represented, 1 open gap, and 1 exact gate. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<nav aria-label="Report sections"><ul><li><a href="#metrics">Metrics</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#sources">Sources</a></li><li><a href="#threats">Threats</a></li><li><a href="#reservations">Reserved evaluation</a></li></ul></nav>
</header>
<main id="main" tabindex="-1">
<section id="metrics" aria-labelledby="metrics-heading"><h2 id="metrics-heading">Evidence metrics</h2>
<ul class="metrics"><li><span class="metric">20</span>bounded positives</li><li><span class="metric">100/100</span>mutations rejected</li><li><span class="metric">25,917</span>effective negatives</li><li><span class="metric">9,999</span>Method Flow methods</li><li><span class="metric">181</span>open gaps</li><li><span class="metric">179</span>exact gates</li></ul>
<p class="notice">All evidence is synthetic and same-owner. No real person, fibre, material, sheet, source work, device, identity event, professional act, authority decision, or Stage 20 evidence is present.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Core proposal outcomes</h2><div class="table-wrap"><table><caption>Twenty preregistered proposal outcomes and mutation results</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Bounded surface</th><th scope="col">Outcome</th><th scope="col">Rejected mutations</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="sources" aria-labelledby="sources-heading"><h2 id="sources-heading">Public-source profile</h2><p>These sources provide vocabulary and stop conditions only. They create no papermaking, conservation, material, environmental, professional, legal, cultural, affected-party, or Māori authority.</p><div class="table-wrap"><table><caption>Public sources, status, and bounded use</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Status</th><th scope="col">Bounded use</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
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
    if overlay["effective_negatives_after_this_overlay"] != 25915:
        raise RuntimeError("unexpected retained-negative count")

    write_json(
        "method-flow/evidence-operational-overlay.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.method-flow-evidence-operational-overlay.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "base_effective_negatives": 25915,
            "base_effective_methods": 9997,
            "new_operational_negative_count": 2,
            "new_operational_method_count": 2,
            "effective_negatives_after_this_overlay": EVIDENCE_NEGATIVES,
            "effective_methods_after_this_overlay": EVIDENCE_METHODS,
            "no_failure_erased": True,
            "rows": [
                {
                    "failure_id": "EK6657-EVID-N001",
                    "method_id": "EK6657-EVID-MF-001",
                    "request": "run the evidence staged review and return its complete visible receipt",
                    "failed_witness": "the staged review completed and persisted valid files, but the visible tool-result stream exceeded the available output/context budget before the final scalar result remained attributable",
                    "aggregate_credit": 0,
                    "recovery": "do not replay the successful persisted review; inspect its exact files with bounded scalar probes, retain both digests, and regenerate only review and manifest after this overlay changes the staged target",
                    "bounded_passing_witness": {
                        "initial_review_valid": True,
                        "initial_reviewed_path_count": 110,
                        "initial_manifest_entry_count": 111,
                        "initial_review_sha256": "d992edf130f5f63f7be9e88acbc8545e0e607089ef72443a5548cc42f44f95ff",
                        "initial_manifest_sha256": "25a9d68210cf3951e079b02d1f016528f62b9f3f402cd1e8900a9e5bb2431642",
                    },
                    "recurrence_guard": "make staged-review commands emit only a bounded scalar summary and read detailed results from persisted receipts",
                    "rollback": "the display truncation changed no repository, sibling, remote, external, or authority state; target changes are additive and owner-local",
                    "repository_commit_created": False,
                    "external_action_created": False,
                    "status": "recovered_failure_retained",
                },
                {
                    "failure_id": "EK6657-EVID-N002",
                    "method_id": "EK6657-EVID-MF-002",
                    "request": "regenerate the target-changed evidence staged review and preserve its process handle through completion",
                    "failed_witness": "the process crossed the ten-second yield boundary and an output-only wrapper discarded the returned live session handle before completion",
                    "aggregate_credit": 0,
                    "recovery": "do not overlap or replay the live process; locate the exact owner review process read-only, wait boundedly for it to exit, then inspect the persisted review and manifest with scalar probes",
                    "bounded_passing_witness": {
                        "review_valid": True,
                        "review_checks_passed": 14,
                        "review_checks_total": 14,
                        "reviewed_path_count": 111,
                        "manifest_entry_count": 112,
                        "review_sha256": "2dd853c0dfdaeb835b209e862023b8eccf890e22aa0031581d86e2058c2d6dac",
                        "manifest_sha256": "5bd6be4175e2713c8cb443bdd5e2203c6a8d8137f4f33793f12e0e5b217e03d5",
                    },
                    "recurrence_guard": "separate staging from review, allow a thirty-second initial yield, and preserve the full exec response including any live session identifier",
                    "rollback": "the premature wrapper return changed no sibling, remote, external, or authority state; the original process completed the additive owner-local target",
                    "repository_commit_created": False,
                    "external_action_created": False,
                    "status": "recovered_failure_retained",
                }
            ],
        },
    )

    write_json(
        "evidence/evidence-summary.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.evidence-summary.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "new_frozen_total": 4150,
            "outcomes": ledger["outcome_counts"],
            "bounded_positives": 20,
            "rejecting_mutations": 100,
            "accepted_mutations": 0,
            "repository_sealed_inherited": {"negatives": 25797, "methods": 9769, "open_gaps": 180, "exact_gates": 178},
            "inherited_external_overlay": {"negatives": 2, "methods": 2},
            "eiren_startup": {"negatives": 15, "methods": 15},
            "eiren_x2": {"mutation_negatives": 100, "methods": 210, "operational_negatives": 1, "operational_methods": 1},
            "eiren_evidence": {"operational_negatives": 2, "operational_methods": 2},
            "effective": {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS, "open_gaps": 181, "exact_gates": 179},
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.environment-version-receipt.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.threat-model-review.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "threat_count": len(threats["threats"]),
            "reviewed_threat_ids": [row["threat_id"] for row in threats["threats"]],
            "new_material_threats": [
                {"threat_id": "EK6657-T11", "threat": "repository-local module import omitted the scripts search path", "mitigation": "declare a bounded scripts path for compact module probes and retain the failed witness"}
            ],
            "residual_risks_visible": True,
            "security_claim": "bounded same-owner review only; not exhaustive security",
            "privacy_claim": "five-class value-bearing scan only; not privacy certification",
            "authority_gates_unchanged": True,
        },
    )

    write_json(
        "evidence/complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.eiren-kestrel.v665-v7.evidence-checklist.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "complete_bounded": [
                "read-first and exact source verification",
                "dedicated x1 commit, push, clean state, 0/0 divergence, and fresh four-way equality",
                "4,130-row semantic novelty audit and twenty-proposal freeze",
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
                "real papermakers, workers, affected parties, fibres, materials, sheets, source works, devices, and evaluation evidence",
                "professional papermaking, conservation, material, environmental, machine or chemical safety validation, privacy completeness, and accessibility completeness",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.wellbeing-workload-check.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "status": "bounded_with_failures_visible",
            "controls": [
                "caps used as ceilings rather than quotas",
                "one x2 operational failure and two evidence-stage process/output failures retained with zero failed-probe credit",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.authority-and-evidence-gaps.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "open_gap_count": 181,
            "exact_gate_count": 179,
            "new_open_gap": {"proposal_id": "EK6657-N019", "reason": "no live current-source adapter or schema negotiation"},
            "new_exact_gate": {"proposal_id": "EK6657-N020", "reason": "fibre-origin, traditional-knowledge, environmental, copyright, design-rights, worker-safety, affected-party, legal, cultural, and Māori authority absent"},
            "protected_claims": [
                "empirical GMUT",
                "real THOS effectiveness",
                "production Freed ID",
                "professional papermaking, conservation, material, environmental, machinery, or chemical competence or conformance",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.portfolio-evidence-receipt.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
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
            "schema": "ghc.family.eiren-kestrel.v665-v7.evidence-build-receipt.v1",
            "owner": "Eiren Kestrel",
            "phase": "v665-v7",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_eiren_kestrel_v665_v7_evidence.py",
            "report": "docs/eiren-kestrel/v665-v7/reports/static-report.html",
            "overview": "docs/eiren-kestrel/v665-v7/reports/integrated-evidence-overview.md",
            "outcomes": ledger["outcome_counts"],
            "effective_counts": {"negatives": EVIDENCE_NEGATIVES, "methods": EVIDENCE_METHODS, "open_gaps": 181, "exact_gates": 179},
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
        raise SystemExit("usage: build_ghc_family_eiren_kestrel_v665_v7_evidence.py [--staged-review]")
    else:
        main()
