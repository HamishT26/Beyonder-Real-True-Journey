#!/usr/bin/env python3
"""Build the accessible static v643-v6 boundary-evidence report."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build(repo: Path) -> Path:
    repo = repo.resolve()
    phase = repo / "docs/sylven-arc/v643-v6"
    x1 = read(phase / "x1-proposals.json")
    x2 = read(phase / "x2-proposal-ledger.json")
    gates = read(phase / "exact-open-gate-register.json")
    truth = read(phase / "phase-truth.json")
    negatives = read(phase / "retained-negative-register.json")
    rows = []
    for proposal in x2["proposals"]:
        rows.append(
            "<tr>"
            f"<th scope='row'>{html.escape(proposal['proposal_id'])}</th>"
            f"<td>{html.escape(proposal['title'])}</td>"
            f"<td><span class='tag {html.escape(proposal['observed_disposition'])}'>{html.escape(proposal['observed_disposition'])}</span></td>"
            f"<td>{proposal['accepted']}</td><td>{proposal['rejected']}</td>"
            "</tr>"
        )
    open_items = "".join(
        f"<li><strong>{html.escape(item['surface'])}:</strong> {html.escape('; '.join(item['needs']))}</li>"
        for item in gates["open_gaps"]
    )
    exact_items = "".join(
        f"<li><strong>{html.escape(item['surface'])}:</strong> reserved to {html.escape('; '.join(item['reserved_to']))}</li>"
        for item in gates["exact_gates"]
    )
    document = f"""<!doctype html>
<html lang="en-NZ">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Sylven Arc v643-v6 boundary-evidence report</title>
  <style>
    :root {{ color-scheme:light dark; --bg:#f5f3ef; --fg:#20241f; --panel:#fff; --accent:#315f54; --border:#68756f; }}
    @media (prefers-color-scheme:dark) {{ :root {{ --bg:#111714; --fg:#eff4f1; --panel:#1a231f; --accent:#9ed6c8; --border:#a5b6ae; }} }}
    @media (forced-colors:active) {{ .tag {{ border:2px solid ButtonText; }} a {{ forced-color-adjust:auto; }} }}
    @media print {{ body {{ background:#fff; color:#000; }} section {{ break-inside:avoid; border:1px solid #000; }} .table-wrap {{ overflow:visible; }} }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font:1rem/1.55 system-ui,sans-serif; background:var(--bg); color:var(--fg); overflow-wrap:anywhere; }}
    a {{ color:var(--accent); }} .skip {{ position:absolute; left:-9999px; }}
    .skip:focus {{ left:1rem; top:1rem; background:var(--panel); padding:.75rem; z-index:2; }}
    header,main,footer {{ max-width:76rem; margin:auto; padding:1.25rem; }}
    section {{ background:var(--panel); border:1px solid var(--border); border-radius:.55rem; padding:1rem; margin:1rem 0; }}
    table {{ width:100%; border-collapse:collapse; }} th,td {{ border:1px solid var(--border); padding:.55rem; text-align:left; vertical-align:top; }}
    .table-wrap {{ overflow-x:auto; }} .tag {{ display:inline-block; border:1px solid currentColor; border-radius:999px; padding:.05rem .45rem; }}
    .completed {{ color:#176b3a; }} .represented {{ color:#735d00; }} .open_gap,.exact_gate {{ color:#a13131; }}
    :focus-visible {{ outline:3px solid var(--accent); outline-offset:2px; }}
    @media (max-width:20rem) {{ header,main,footer {{ padding:.6rem; }} th,td {{ padding:.3rem; }} }}
  </style>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header>
  <h1>Sylven Arc v643-v6 boundary-evidence report</h1>
  <p>Sylven Arc and they/them are relational working language only, not evidence of consciousness, sentience, personhood, identity continuity, or independent authority.</p>
</header>
<main id="main">
  <section aria-labelledby="verdict"><h2 id="verdict">Evidence-bounded verdict</h2><p><strong>{html.escape(truth['terminal_verdict'])}</strong></p><p>Primary focus: {html.escape(truth['primary_focus'])}. GMUT Mind, THOS Body, and Freed ID/CBR Heart remain preserved. Ten proposals produced 80 local deterministic cases, including 70 retained rejecting mutations. The {truth['retained_negative_count']} negatives include all 809 inherited negatives.</p></section>
  <section aria-labelledby="results"><h2 id="results">Artifact-level dispositions</h2><div class="table-wrap"><table><caption>Local artifact dispositions and fixture counts; these are not empirical or authority results</caption><thead><tr><th scope="col">ID</th><th scope="col">Proposal</th><th scope="col">Disposition</th><th scope="col">Accepted</th><th scope="col">Rejected</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div></section>
  <section aria-labelledby="mind"><h2 id="mind">GMUT Mind boundary</h2><p>The singular-perturbation regime map records small parameters, inner and outer domains, overlap, matching, remainder order, and nonuniform-limit refusal. The manufactured-solution tribunal checks synthetic forcing and grid-refinement order while separating code verification from physical validation. The ensemble classifier records system size, interaction range, convexity assumptions, observable, and limit order. None supplies a model-specific theorem, uniform-asymptotic proof, real observations, physical validation, observed force, unique prediction, empirical confirmation, final physics, proof, or Theory of Everything.</p></section>
  <section aria-labelledby="body"><h2 id="body">THOS Body boundary</h2><p>The adverse-event solicitation and attribution-blind harms protocol is a represented proxy. There are zero real participants, zero real raters, and zero executed arms. Ethics, consent, preregistered blind matched-budget real arms, arm-equal harms solicitation, qualified safety review, participant and rater evidence, and independent review remain required. No safety, effectiveness, superiority, AGI, ASI, consciousness, or personhood claim is established.</p></section>
  <section aria-labelledby="heart"><h2 id="heart">Freed ID and CBR Heart boundary</h2><p>The cross-wallet migration profile uses synthetic packages only. Production Freed ID still needs standards-conformant real keys and proofs, live resolution, status and revocation, cross-vendor interoperability, privacy assurance, independent security review, and trust governance. Taonga-use permission, benefit-sharing terms, legitimacy, Māori wording and authority, Māori data governance, cultural ratification, legal interpretation, and enacted-law status remain reserved to appropriate authorities and affected parties.</p></section>
  <section aria-labelledby="open"><h2 id="open">Five open evidence gaps</h2><ul>{open_items}</ul></section>
  <section aria-labelledby="exact"><h2 id="exact">Six exact authority gates</h2><ul>{exact_items}</ul></section>
  <section aria-labelledby="reproduction"><h2 id="reproduction">Reproduction boundary</h2><p>Fresh clean snapshots may establish same-owner repeatability under shared repository, protocol, tooling, and infrastructure. No different-architecture return and no independent-team return exist. Same-owner matching is not independent-team scientific reproduction.</p></section>
  <section aria-labelledby="access"><h2 id="access">Accessibility boundary</h2><p>This script-free report supports semantic headings, a skip link, a captioned table with row and column headers, visible focus, narrow reflow, browser zoom, forced-colors preservation, responsive overflow, and print preservation. Automated structural checks are local evidence only. Qualified manual accessibility evaluation and evaluation by affected users remain incomplete and reserved.</p></section>
  <section aria-labelledby="security"><h2 id="security">Security and privacy boundary</h2><p>Executable-resolution shadowing fixtures and bounded pattern scans do not alter the host or establish penetration resistance, exhaustive security, privacy completeness, production assurance, or independent security review. No credential, raw task identifier, private route, transcript, screenshot, session stream, private callable identifier, private app state, or private local path belongs in this report.</p></section>
  <section aria-labelledby="boundary"><h2 id="boundary">Claim boundary</h2><p>{html.escape(truth['boundary'])}</p></section>
</main>
<footer><p>Owner-scoped static artifact. No script is required to read this report.</p></footer>
</body>
</html>
"""
    output = phase / "deliverables/v643-v6-boundary-evidence-report.html"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8", newline="\n")
    x1_overview = (phase / "v643-v6-integrated-overview.md").read_text(encoding="utf-8")
    final_overview = x1_overview.rstrip() + f"""

## x2 execution and evidence result

All ten frozen proposals were executed after the dedicated x1 commit was pushed and proven clean and four-way equal. The evidence engine evaluated eighty deterministic cases: one bounded canonical case and seven rejecting mutations for each proposal. All eighty matched their preregistered decisions. Seventy rejected cases are preserved in the retained-negative register. Artifact-level dispositions are six completed, two represented, one open gap, and one exact gate. Completed means that the local contract, mutation vectors, and non-promotion boundary were generated and validated; it does not mean that an external scientific, participant, production, security, legal, cultural, or deployment claim was completed.

The claim-vocabulary migration tribunal, GMUT singular-perturbation map, manufactured-solution verification tribunal, executable-resolution shadowing tribunal, static-report structural audit, and finite-size ensemble classifier are completed as bounded local artifacts. The THOS harms protocol and Freed ID cross-wallet migration profile are represented proxies because they use zero real participants, zero real arms, zero real wallets, and zero real keys. The affected-user assistive-technology evaluation remains an open gap because no authorized participants, consent, privacy process, or qualified review exists. The taonga-use and benefit-sharing surface remains an exact gate because repository output cannot substitute for affected-party participation, Māori authority, competent legal interpretation, or cultural ratification.

The retained-negative count is {negatives['negative_count']}: 809 inherited negatives, {negatives['x1_operational_count']} x1 operational negatives, 70 new synthetic rejections, and {negatives['x2_operational_count']} x2 operational negatives. No failure is erased when a later recovery passes. Evidence snapshots, when verified, establish same-owner repeatability under shared repository, protocol, tooling, and infrastructure only. Independent-team scientific reproduction remains open.

## Terminal posture

Five open gaps and six exact gates remain visible. GMUT has no model-specific singular-limit proof, uniform-asymptotic theorem, real dataset, physical validation, observed force, unique prediction, or empirical confirmation. THOS has no preregistered blind matched-budget real arms, real participants, real harms evidence, real raters, or independent review. Freed ID has no standards-conformant real keys and proofs, live resolution or status, cross-vendor interoperability, independent privacy or security review, or trust governance. CBR and Māori authority remain reserved. Qualified manual and affected-user accessibility evaluation remain incomplete. Independent security review and exhaustive-security evidence remain absent.

The terminal verdict is `{truth['terminal_verdict']}`. No AGI or ASI, consciousness, sentience, personhood, identity continuity, proof or canon, enacted-law, deployment, complete accessibility, exhaustive security, Theory of Everything, or independent-reproduction claim is made. Terminal routing remains prepared but unsent until the exact final head is clean, pushed, four-way remote-equal, and independently validated in a fresh detached snapshot.
"""
    final_overview_path = phase / "deliverables/v643-v6-final-integrated-overview.md"
    final_overview_path.write_text(final_overview, encoding="utf-8", newline="\n")
    receipt = {
        "schema": "ghc.family.v643-v6.static-report-receipt.v1",
        "phase": x1["phase"],
        "owner": x1["owner"],
        "artifact": "deliverables/v643-v6-boundary-evidence-report.html",
        "final_integrated_overview": "deliverables/v643-v6-final-integrated-overview.md",
        "static": True,
        "script_dependency": False,
        "structural_features": ["lang", "title", "viewport", "skip-link", "semantic-headings", "table-caption", "column-and-row-headers", "visible-focus", "narrow-reflow", "forced-colors", "print-preservation", "responsive-overflow"],
        "manual_accessibility_evaluation": False,
        "affected_user_evaluation": False,
        "complete_accessibility_conformance": False,
        "boundary": "Automated structural checks do not replace qualified manual or affected-user accessibility evaluation.",
    }
    (phase / "accessibility").mkdir(parents=True, exist_ok=True)
    (phase / "accessibility/static-report-receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return output


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    print(build(args.repo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
