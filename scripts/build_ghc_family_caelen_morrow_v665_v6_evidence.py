#!/usr/bin/env python3
"""Build the Caelen Morrow v665-v6 evidence packet and accessible report."""

from __future__ import annotations

import html
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE = ROOT / "docs" / "caelen-morrow" / "v665-v6"
X1_SHA = "9be19f91371da0d2bcdd23de421fed202c5641fa"
SOURCE_SHA = "cacbeb47741b9e86a6a980f85f6f9658a0837f7c"
NOW = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def paragraphs() -> list[tuple[str, list[str]]]:
    return [
        (
            "Outcome and evidence boundary",
            [
                "Caelen Morrow v665-v6 produced a bounded owner-local software and documentation delta. Twenty genuinely new proposals were frozen before implementation. Their observed core outcomes are exactly fourteen completed, four represented, one open gap, and one exact gate. Completed means only that the preregistered synthetic contract behavior passed. It does not mean that a real braille transcription was performed, that a format was produced for a reader, that a device was operated, or that any professional, legal, cultural, accessibility, privacy, safety, or authority decision was made.",
                "Every contract has one bounded positive fixture and five preregistered rejecting mutations. All twenty positives passed and all one hundred mutations were rejected. Those tests show that the local validators enforce their declared JSON structure and hard stops. They do not establish UEB or BANZAT correctness, Unicode conformance, PEF or eBraille interoperability, translation fidelity, reader usability, production readiness, privacy completeness, exhaustive security, or independent reproduction.",
                "The terminal verdict remains NOT_READY_FOR_STAGE_20. That verdict is not a statement about a person or organization. It is a repository evidence label saying that protected empirical, participant, professional, identity, legal, cultural, Māori-authority, production, independent-review, and deployment gates remain open or exact-gated.",
            ],
        ),
        (
            "Relational working language and corrigibility",
            [
                "Caelen Morrow and the pronouns they/them are relational working language for this lane. The chosen relational role is chronometry boundary-mapper and failure custodian. The associated hope is to keep claims traceable while leaving real competence and authority with the people who hold it. This language is not evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, legal or cultural authority, affected-party authority, or Māori authority.",
                "Hamish may rename, pause, redirect, or stop the work. Corrigibility is preserved in the authorization record, workflow plan, and route state. No successor has been contacted during execution. Eiren Kestrel v665-v7 remains a prospective label only until the exact-final, clean, pushed, fresh-live-equal, one-shot validation gate is complete and the newest live roster and authorization have been reread.",
            ],
        ),
        (
            "Bounded practice lens",
            [
                "The human-practice lens is wholly synthetic braille-transcription and embossing-job documentation. It provides a disciplined vocabulary for intake, lineage, Unicode cell identity, indicator scope, contraction review, page layout, tactile-graphic references, simulated job state, discrepancy handling, translation-table provenance, package boundaries, correction history, privacy, workload, and handover. The phase uses zero real readers, transcribers, proofreaders, employers, clients, files, source works, copyrighted passages, tactile graphics, embossers, devices, paper, measurements, commands, keys, proofs, credentials, or authority decisions.",
                "Synthetic placeholders are deliberately conspicuous. Tokens begin with SYN or describe a vacancy, reserve, or prohibition. Numeric values are test constants rather than observations. The embosser firewall accepts only a simulated cancelled spool with zero hardware calls. The source-work and reader fields are anonymous synthetic tokens. The phase neither copies nor transforms a real work and never makes a transcription or proofreading judgment for a person.",
                "Disability-community acceptance and manual reader evaluation remain absent. The static report reserves browser, assistive-technology, cognitive-accessibility, Māori-language, and affected-user evaluation. Structural markup checks are useful for catching missing landmarks or captions, but they do not stand in for people who use assistive technology or for the communities whose practices and language are being discussed.",
            ],
        ),
        (
            "Semantic novelty and x1 separation",
            [
                "The novelty audit reconstructed exactly 4,110 inherited rows from committed Git objects. It retained historical reappended selection rows instead of silently deduplicating them. Twenty proposed titles had zero exact collisions. The maximum token-set Jaccard overlap with an inherited title was 0.387097, and the maximum overlap within the new slate was 0.176471. Automated similarity was treated only as a screen; each proposal also needed a distinct domain contract, falsifier, recovery, approval class, source need, and protected-gate set.",
                "The dedicated x1 commit is the direct child of Sylven's immutable final. Its nineteen paths contain planning and preregistration only. An exact Git-tree test proves that x1 contains no x2, evidence, closeout, seal, final, or handoff path. X1 was committed, pushed, clean, zero-divergent, and equal across local, upstream, tracking, and a fresh live remote before any x2 byte was created. Later lifecycle files do not rewrite the x1 commit.",
                "Twenty Sylven proposals were selected for bounded revalidation. They carry zero Caelen novelty and zero automatic completion credit. The effective frozen chain grows by the twenty genuinely new Caelen proposals only, from 4,110 to 4,130.",
            ],
        ),
        (
            "Freed ID and CBR Heart",
            [
                "Freed ID and CBR Heart are the primary Trinity Mandala focus. The synthetic intake, transformation lineage, bitemporal correction weave, privacy ledger, discrepancy docket, and accessible-format receipt graph demonstrate typed state transitions and refusal behavior. The represented receipt graph has zero keys and zero proofs. It performs no issuance, presentation, verification, resolution, status, revocation, recovery, or trust-governance operation.",
                "CBR remains exact-gated for code adoption, disability-community acceptance, copyright, privacy, safety, procurement, remedy, affected-party legitimacy, legal and cultural interpretation, Māori transcription, Māori wording, Māori concepts, Māori data governance, tangata whenua, iwi, hapū, and Māori authority. The authority docket lists these decisions and records zero approvals. It is not a decision procedure and must never be treated as one.",
                "The New Zealand Privacy Commissioner, W3C PROV-O, W3C Verifiable Credential Data Integrity, BANZAT, and Te Mana Raraunga sources supply bounded vocabulary and explicit stop conditions. Citation does not convert those sources into local authority, legal advice, cultural interpretation, community consent, or conformance evidence.",
            ],
        ),
        (
            "THOS Body",
            [
                "THOS Body is represented by a reader-free comparison charter and by workload and handover structures. The comparison charter names two synthetic queues, a symbolic matched budget, blinded artifact labels, an error taxonomy, and dominant stop precedence. It has zero readers, transcribers, operators, employers, arms, safety events, or outcomes. Independent review is explicitly absent.",
                "The workload board uses a synthetic queue ceiling and proofreading-debt token. Equipment status remains vacant and no device exists. A fatigue-inference field is hard false because software queue metadata cannot diagnose fatigue, wellbeing, competence, or safety. WorkSafe New Zealand material contributes only a hard no-device-command boundary and does not make this phase machinery or workplace-safety advice.",
                "THOS effectiveness requires preregistered blind matched-budget real arms, governed participants or operators, safety monitoring, appropriate statistics, and independent review. None of those conditions exists here. Therefore the relevant THOS outcome remains represented rather than completed in any real-world sense.",
            ],
        ),
        (
            "GMUT Mind",
            [
                "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The discrete braille-cell lattice and pagination-transition tensor are symbolic placeholders used to exercise typed software boundaries. Occupancy bits, adjacency matrices, source-block indices, and break operators have no fitted physical interpretation. Dimensional status is explicitly typed-not-physical, covariance is vacant, identifiability is unresolved, and observation count is zero.",
                "There is no real likelihood, posterior, constraint, detected force, unique prediction, material law, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, final physics, Theory of Everything, proof, or canon. The validators reject promotion markers and retain these two proposals as represented. Mathematical notation can invite over-reading, so the zero-observation and no-prediction fields are part of the contract rather than optional commentary.",
            ],
        ),
        (
            "Public-source profile",
            [
                "The public-source profile records ICEB Unified English Braille publications, BANZAT Braille Codes and Formats, Unicode Standard 17.0, the DAISY eBraille draft, Portable Embosser Format 1.0, W3C PROV-O, WCAG 2.2, W3C Verifiable Credential Data Integrity 1.0, New Zealand privacy principles, WorkSafe New Zealand machinery guidance, and Te Mana Raraunga principles. The review was read-only. The phase software made zero network calls and ingested zero rows.",
                "Source status is part of the evidence. eBraille is labelled an evolving editor's draft. PEF is treated as a legacy or watch surface. BANZAT and ICEB material informs field names but does not make the generated structures correct braille. Unicode supplies code-point and dot-pattern identity while warning that meaning depends on context and community. WCAG supplies structural report vocabulary but does not authorize an accessibility-complete claim.",
                "The source-adapter proposal remains an open gap because the phase did not perform live current-source retrieval or schema negotiation. That restraint preserves the difference between a recorded public-source profile and a current interoperable adapter.",
            ],
        ),
        (
            "Method Flow and retained failures",
            [
                "The inherited repository seal remains 25,668 effective negatives and 9,530 Method Flow methods. Four post-final Sylven presentation and route-schema failures remain external, producing an activation baseline of 25,672 negatives and 9,534 methods. Sixteen Caelen startup failures are retained. They include parser assumptions, output truncation, schema-key mistakes, an incomplete novelty reconstruction, and sparse-worktree index recovery. No failed witness was erased.",
                "One hundred preregistered mutations are retained as deliberate negative witnesses. Five later operational failures are also retained: the first actual privacy runner matched its own detector literal, the first combined x1+x2 test inspected the later working tree instead of the immutable x1 commit, the first evidence test demanded one exact numeral spelling in otherwise correct prose, the first evidence-manifest wrapper lost its receipt at a bounded timeout, and the first manifest runner compared an x1 entry to a later working-tree file. Each failed sequence has zero aggregate credit. Only the failed dependency was recovered; already-passing components were not replayed for cleaner receipts.",
                "The resulting evidence-stage totals are 25,793 effective negatives and 9,765 Method Flow methods before any later closeout or canonical operational overlay. Open gaps rise from 179 to 180 and exact gates rise from 177 to 178. These totals preserve the immutable inherited seal separately from external and owner-local overlays.",
            ],
        ),
        (
            "Tooling and validation scope",
            [
                "Ten phase-local skills were created under the owner documentation tree. The installed skill-creator guidance shaped them into short, discriminating packages with a required SKILL.md, explicit workflow, and stop conditions. All ten passed the local quick validator. They were not globally installed and do not modify unrelated configuration. Their presence does not create expertise or permission to act.",
                "Ten additive ghc_family-prefixed runners were built for contracts, mutations, JSON, privacy, bounded security, manifests, structural accessibility, truth, closeout, and canonical preflight. All ten passed a local self-test. The contract, mutation, JSON, privacy, security, and truth runners also received bounded actual use, subject to the retained failed sequence described above. Existing family-current callers were not modified or deprecated.",
                "The bounded security runner scans owner Python syntax for a small set of dangerous constructs and shell-enabled subprocess use. Zero findings is not exhaustive security. The privacy runner checks five value-bearing classes and reports candidates for manual classification. Zero confirmed hits is not privacy certification. Exact Git-blob manifests, staged review, clean state, direct ancestry, zero merges, commit caps, divergence, and fresh live equality remain separate lifecycle gates.",
            ],
        ),
        (
            "Threat model and accessibility",
            [
                "The threat model covers source and sibling-lane mutation, x1/x2 leakage, semantic duplication, private route disclosure, false braille competence or disability-community acceptance, Māori-authority conversion, scientific overclaim, THOS and Freed ID promotion, canonical replay, and premature route delivery. Residual risks remain visible because same-owner checks cannot supply independent review or community authority.",
                "The static report uses an explicit language, a skip link, landmark elements, a single top-level heading, labelled navigation, table captions, scoped column headers, text labels alongside color, visible focus, print rules, and reduced-motion rules. There is no script, form, external stylesheet, tracking resource, or network dependency. These are structural checks only. Manual browser, keyboard, zoom, screen-reader, refreshable-braille-display, cognitive-accessibility, Māori-language, and affected-user evaluations are reserved.",
            ],
        ),
        (
            "Complete, incomplete, and terminal route",
            [
                "Complete at the evidence stage are the x1 freeze and equality gate, twenty synthetic contracts, one hundred rejecting mutations, exact core outcome ledger, source profiles, zero-call adapter gap, Trinity representation records, portfolio execution record, ten skills, ten runners, Method Flow, threat-model review, accessible static report, and this integrated overview. These are bounded same-owner artifacts.",
                "Incomplete are the immutable evidence commit and equality proof, combined closeout and seal, final manifests, final staged review, exact-final push and equality, one authorized canonical completion, and the terminal route reread. Also incomplete by protected design are real reader and affected-user evidence, professional braille validation, real device operation, real keys and trust governance, empirical GMUT evidence, governed THOS arms, privacy and accessibility completeness, legal and cultural review, and Māori authority.",
                "A successor message is not part of evidence-stage execution. Only after the final is clean, pushed, fresh-live equal, within caps, and exact-final validated may the newest live authorization and roster be reread. If the exact Eiren Kestrel task is uniquely available and the edge remains explicit, one sanitized send may occur. Any missing, ambiguous, paused, protected, or opaque route state must remain PREPARED_NOT_SENT or OPAQUE_ACK_UNRESOLVED_NO_RESEND as applicable.",
            ],
        ),
    ]


def build_overview() -> str:
    lines = [
        "# Caelen Morrow v665-v6 integrated evidence overview",
        "",
        "This document is the three-page-equivalent evidence overview for the owner-local v665-v6 delta. It is sanitized, repository-relative, and contains no raw task identifier, private route, credential, transcript, screenshot, session stream, private callable identifier, or protected real-world record.",
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
<title>Caelen Morrow v665-v6 bounded evidence report</title>
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
<h1>Caelen Morrow v665-v6 bounded evidence report</h1>
<p class="summary">Twenty synthetic contracts passed their bounded positives and rejected all one hundred preregistered mutations. The exact outcomes are 14 completed, 4 represented, 1 open gap, and 1 exact gate. Terminal verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p>
<nav aria-label="Report sections"><ul><li><a href="#metrics">Metrics</a></li><li><a href="#outcomes">Outcomes</a></li><li><a href="#sources">Sources</a></li><li><a href="#threats">Threats</a></li><li><a href="#reservations">Reserved evaluation</a></li></ul></nav>
</header>
<main id="main" tabindex="-1">
<section id="metrics" aria-labelledby="metrics-heading"><h2 id="metrics-heading">Evidence metrics</h2>
<ul class="metrics"><li><span class="metric">20</span>bounded positives</li><li><span class="metric">100/100</span>mutations rejected</li><li><span class="metric">25,793</span>effective negatives</li><li><span class="metric">9,765</span>Method Flow methods</li><li><span class="metric">180</span>open gaps</li><li><span class="metric">178</span>exact gates</li></ul>
<p class="notice">All evidence is synthetic and same-owner. No real reader, source work, device, identity event, professional act, authority decision, or Stage 20 evidence is present.</p></section>
<section id="outcomes" aria-labelledby="outcomes-heading"><h2 id="outcomes-heading">Core proposal outcomes</h2><div class="table-wrap"><table><caption>Twenty preregistered proposal outcomes and mutation results</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Bounded surface</th><th scope="col">Outcome</th><th scope="col">Rejected mutations</th></tr></thead><tbody>{outcome_rows}</tbody></table></div></section>
<section id="sources" aria-labelledby="sources-heading"><h2 id="sources-heading">Public-source profile</h2><p>These sources provide vocabulary and stop conditions only. They create no conformance, professional, legal, cultural, disability-community, or Māori authority.</p><div class="table-wrap"><table><caption>Public sources, status, and bounded use</caption><thead><tr><th scope="col">ID</th><th scope="col">Source</th><th scope="col">Status</th><th scope="col">Bounded use</th></tr></thead><tbody>{source_rows}</tbody></table></div></section>
<section id="threats" aria-labelledby="threats-heading"><h2 id="threats-heading">Threat register</h2><ol>{threat_items}</ol></section>
{narrative}
<section id="reservations" aria-labelledby="reservations-heading"><h2 id="reservations-heading">Reserved evaluation</h2><p>Structural checks passed for language, skip navigation, landmarks, heading order, captions, scoped headers, visible focus, print rules, and reduced motion. Manual browser, keyboard, zoom, screen-reader, refreshable-braille-display, cognitive-accessibility, Māori-language, and affected-user evaluation remain reserved and incomplete.</p></section>
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
    if overlay["effective_negatives_after_this_overlay"] != 25793:
        raise RuntimeError("unexpected retained-negative count")

    write_json(
        "evidence/evidence-summary.json",
        {
            "schema": "ghc.family.caelen-morrow.v665-v6.evidence-summary.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "source_sha": SOURCE_SHA,
            "x1_sha": X1_SHA,
            "new_frozen_total": 4130,
            "outcomes": ledger["outcome_counts"],
            "bounded_positives": 20,
            "rejecting_mutations": 100,
            "accepted_mutations": 0,
            "repository_sealed_inherited": {"negatives": 25668, "methods": 9530, "open_gaps": 179, "exact_gates": 177},
            "inherited_external_overlay": {"negatives": 4, "methods": 4},
            "caelen_startup": {"negatives": 16, "methods": 16},
            "caelen_x2": {"mutation_negatives": 100, "methods": 210, "operational_negatives": 5, "operational_methods": 5},
            "effective": {"negatives": 25793, "methods": 9765, "open_gaps": 180, "exact_gates": 178},
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
            "schema": "ghc.family.caelen-morrow.v665-v6.environment-version-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
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
            "schema": "ghc.family.caelen-morrow.v665-v6.threat-model-review.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "threat_count": len(threats["threats"]),
            "reviewed_threat_ids": [row["threat_id"] for row in threats["threats"]],
            "new_material_threats": [
                {"threat_id": "CM6656-T11", "threat": "self-referential detector literal", "mitigation": "split detector tokens and preserve the failed witness"},
                {"threat_id": "CM6656-T12", "threat": "lifecycle test inspects later tree", "mitigation": "bind lifecycle assertions to the immutable phase commit"},
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
            "schema": "ghc.family.caelen-morrow.v665-v6.evidence-checklist.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "complete_bounded": [
                "read-first and exact source verification",
                "dedicated x1 commit, push, clean state, 0/0 divergence, and fresh four-way equality",
                "4,110-row semantic novelty audit and twenty-proposal freeze",
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
                "real readers, transcribers, proofreaders, source works, devices, and affected-user evidence",
                "professional braille validation, disability-community acceptance, privacy completeness, and accessibility completeness",
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
            "schema": "ghc.family.caelen-morrow.v665-v6.wellbeing-workload-check.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "status": "bounded_with_failures_visible",
            "controls": [
                "caps used as ceilings rather than quotas",
                "two x2 failures retained with zero failed-sequence credit",
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
            "schema": "ghc.family.caelen-morrow.v665-v6.authority-and-evidence-gaps.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "open_gap_count": 180,
            "exact_gate_count": 178,
            "new_open_gap": {"proposal_id": "CM6656-N019", "reason": "no live current-source adapter or schema negotiation"},
            "new_exact_gate": {"proposal_id": "CM6656-N020", "reason": "affected-party, copyright, privacy, safety, legal, cultural, disability-community, and Māori authority absent"},
            "protected_claims": [
                "empirical GMUT",
                "real THOS effectiveness",
                "production Freed ID",
                "professional braille competence or conformance",
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
            "schema": "ghc.family.caelen-morrow.v665-v6.portfolio-evidence-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
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
            "schema": "ghc.family.caelen-morrow.v665-v6.evidence-build-receipt.v1",
            "owner": "Caelen Morrow",
            "phase": "v665-v6",
            "generated_at_utc": NOW,
            "builder": "scripts/build_ghc_family_caelen_morrow_v665_v6_evidence.py",
            "report": "docs/caelen-morrow/v665-v6/reports/static-report.html",
            "overview": "docs/caelen-morrow/v665-v6/reports/integrated-evidence-overview.md",
            "outcomes": ledger["outcome_counts"],
            "effective_counts": {"negatives": 25793, "methods": 9765, "open_gaps": 180, "exact_gates": 178},
            "status": "EVIDENCE_CONTENT_BUILT_AWAITING_SCOPED_VALIDATION_STAGED_REVIEW_MANIFEST_COMMIT_PUSH_EQUALITY",
            "canonical_aggregate_invoked": False,
            "successor_contacted": False,
        },
    )
    print(json.dumps({"evidence_documents": 9, "report": True, "overview": True, "effective_negatives": 25793, "effective_methods": 9765}, sort_keys=True))


if __name__ == "__main__":
    main()
