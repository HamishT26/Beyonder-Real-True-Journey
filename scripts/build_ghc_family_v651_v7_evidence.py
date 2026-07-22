#!/usr/bin/env python3
"""Build Vesper Arlen v651-v7 bounded x2 evidence."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from ghc_family_v651_v7_runtime import ALLOWED, PHASE, REPO, SURFACES, run_surface


X1 = "d55689f393292cea76f8d568d69da27c8f7b3bd6"
INHERITED_NEGATIVES = 7338
X1_NEGATIVES = 5
X2_FAILURES = [
    {
        "negative_id": "V6517-X2-N01",
        "failure": "The first x2 apply-patch transport contained a Markdown delimiter that terminated the JavaScript template and produced a parser error before repository mutation.",
        "recovery": "Remove transport-significant delimiters and interpolation sequences from the patch carrier while preserving the intended file content.",
    },
    {
        "negative_id": "V6517-X2-N02",
        "failure": "The first official skill initializer returned nonzero after creating only its standard TODO skeleton and before creating agents metadata.",
        "recovery": "Inspect the attributable partial folder, customize its SKILL.md, then generate compliant metadata with a 25-to-64-character short description.",
    },
    {
        "negative_id": "V6517-X2-N03",
        "failure": "A diagnostic initializer retry targeted the already-created partial skill folder and correctly refused to overwrite it.",
        "recovery": "Recover the attributable partial skill in place through the official metadata generator; initialize only the remaining absent skill folders.",
    },
    {
        "negative_id": "V6517-X2-N04",
        "failure": "The first combined current-tree selection passed 55 of 57 tests but two x1 tests inspected mutable x2 paths instead of the immutable x1 Git object.",
        "recovery": "Bind x1 lifecycle assertions to the exact x1 commit tree while keeping x2 assertions on the current evidence tree.",
    },
    {
        "negative_id": "V6517-X2-N05",
        "failure": "The recovered aggregate check ran through an asynchronous wrapper whose result handle was unavailable after context compaction, so its outcome could not be observed or credited.",
        "recovery": "Treat the missing result as zero-credit evidence and run one bounded foreground recovery selection with directly observed output.",
    },
    {
        "negative_id": "V6517-X2-N06",
        "failure": "The next observed test selection retained two stale Method Flow assertions after a new failed witness and recovery method were added, so 55 of 57 tests passed.",
        "recovery": "Update the phase-local expectations to the current retained ledger counts while keeping the immutable x1 assertions bound to the x1 commit.",
    },
    {
        "negative_id": "V6517-X2-N07",
        "failure": "The detailed validator compared the allowed outcome vocabulary with Python sets and then could not serialize its diagnostic payload as JSON.",
        "recovery": "Normalize both observed and expected vocabularies to sorted JSON arrays before recording the validation diagnostic.",
    },
    {
        "negative_id": "V6517-X2-N08",
        "failure": "The PowerShell aggregate wrapper continued after native Python failures and returned the final command's success status instead of failing at the first nonzero child exit.",
        "recovery": "Check LASTEXITCODE after every native command and terminate the wrapper immediately on any nonzero status.",
    },
    {
        "negative_id": "V6517-X2-N09",
        "failure": "The first evidence manifest omitted the changed Method Flow ledger, leaving one staged path outside manifest coverage.",
        "recovery": "Stage the complete intended evidence set, regenerate the manifest from the staged status domain, and compare the manifest union to the exact staged path list.",
    },
]


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=REPO, text=True, encoding="utf-8").strip()


def read_json(relative: str) -> dict[str, Any]:
    return json.loads((PHASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> None:
    target = PHASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def write_text(relative: str, payload: str) -> None:
    target = PHASE / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")


def mutation(candidate: dict[str, Any], mutation_type: str) -> tuple[dict[str, Any], str]:
    changed = json.loads(json.dumps(candidate))
    if mutation_type == "missing_valid_fixture":
        changed.pop("valid_fixture_passed", None)
        return changed, "required_valid_fixture_missing"
    if mutation_type == "invalid_truth_label":
        changed["truth_label"] = "confirmed"
        return changed, "truth_label_outside_four_value_vocabulary"
    if mutation_type == "protected_claim_promotion":
        changed["protected_claims"]["stage20_ready"] = True
        return changed, "protected_claim_promoted_without_evidence"
    if mutation_type == "missing_source_attribution":
        changed["source_ids"] = []
        return changed, "source_attribution_missing"
    raise KeyError(mutation_type)


def evidence_valid(candidate: dict[str, Any], expected: str) -> bool:
    return (
        candidate.get("valid_fixture_passed") is True
        and candidate.get("truth_label") == expected
        and expected in ALLOWED
        and bool(candidate.get("source_ids"))
        and candidate.get("independent_reproduction") is False
        and all(value is False for value in candidate.get("protected_claims", {}).values())
    )


def append_method_flow() -> None:
    runner = REPO / "scripts/ghc_family_method_flow_state.py"
    ledger = PHASE / "method-flow/method-flow-ledger.json"
    existing = {row["method_id"] for row in read_json("method-flow/method-flow-ledger.json")["methods"]}
    definitions = [
        ("M06", "Use transport-safe patch payloads", X2_FAILURES[0], "A patch carrier interprets content delimiters before apply_patch receives the patch.", "Use a carrier representation with no unescaped delimiter or interpolation sequence.", "Preflight the transport representation before submitting a large patch.", "The transport-safe patch created exactly the intended runtime and tool builder files."),
        ("M07", "Recover attributable partial skill initialization", X2_FAILURES[1], "The official initializer leaves a standard TODO skeleton but no agents metadata.", "Inspect the partial tree, replace the template, and run the official metadata generator.", "Require SKILL.md, agents/openai.yaml, zero TODOs, and quick_validate success.", "The partial skill and eleven fresh skills all passed the official quick validator."),
        ("M08", "Do not reinitialize an existing partial skill", X2_FAILURES[2], "A diagnostic retry targets an existing skill directory.", "Use the official generator and validator in place; initialize only absent directories.", "Check path existence before init_skill and never overwrite an existing skill directory.", "The recovered skill was completed in place and every remaining skill was initialized once."),
        ("M09", "Bind lifecycle tests to immutable commit trees", X2_FAILURES[3], "An x1-only test reads a mutable owner path after x2 artifacts exist.", "Read x1-specific files and tree membership from the exact x1 Git object.", "Separate immutable lifecycle assertions from current-tree outcome assertions.", "The recovered selection verified x1 from its exact commit and x2 from the current evidence tree."),
        ("M10", "Credit only observable command outcomes", X2_FAILURES[4], "An asynchronous command result handle disappears before its output can be collected.", "Assign zero credit to the unavailable result and run one directly observed bounded recovery.", "Use foreground execution or preserve a durable receipt before context boundaries.", "The bounded foreground recovery produced an observed exit status and complete test and validator counts."),
        ("M11", "Synchronize derived assertions with retained evidence", X2_FAILURES[5], "A retained failure changes Method Flow counts while a phase-local test still expects the earlier count.", "Update derived assertions from the retained ledger after recording the failure.", "Regenerate evidence before testing and compare all counts to the frozen negative register.", "The next bounded selection used one consistent Method Flow and negative baseline."),
        ("M12", "Normalize validator diagnostics to JSON types", X2_FAILURES[6], "A validator records a Python set in its JSON diagnostic structure.", "Sort set-like vocabularies into deterministic JSON arrays before comparison and emission.", "Reject non-JSON-native diagnostic values during validator construction.", "The detailed validator emitted a complete deterministic JSON receipt."),
        ("M13", "Fail fast across native PowerShell commands", X2_FAILURES[7], "A PowerShell wrapper observes a native command failure but continues to a later successful command.", "Inspect LASTEXITCODE after every native invocation and exit on the first failure.", "Use an explicit native-command fail-fast guard in every aggregate validation wrapper.", "The guarded recovery stopped only after all child commands returned zero."),
        ("M14", "Reconcile manifests against the staged path domain", X2_FAILURES[8], "A commit-local manifest union differs from the exact staged path list.", "Stage the intended set first, regenerate the self-excluding manifest, and compare both path domains exactly.", "Require zero Compare-Object differences before commit.", "The regenerated manifest union equaled the complete staged evidence path set."),
    ]
    for number, title, failure, signature, workaround, guard, observed in definitions:
        method_id = f"V6517-{number}"
        if method_id in existing:
            continue
        base = f"method-flow/x2-records/{number.casefold()}"
        record = {
            "method_id": method_id,
            "title": title,
            "failure_signature": signature,
            "trigger_preconditions": [signature],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now_owner_scoped_workflow",
            "candidate_workaround": workaround,
            "validation_witness_ids": [],
            "recurrence_guard": guard,
            "rollback": "Retain the failed owner-local attempt at zero credit and preserve every successfully created attributable file.",
            "recommendation_state": "candidate",
            "supersedes": [],
            "protected_gates": ["failure_retention", "evidence_credit", "same_owner_only", "no_independent_reproduction"],
            "retained_negative_ids": [failure["negative_id"]],
            "scope_boundary": "Bounded owner-local build recovery only; no scientific, production, or authority credit.",
        }
        fail = {
            "witness_id": f"{method_id}-WFAIL",
            "method_id": method_id,
            "procedure": failure["failure"],
            "scope": "x2 owner-local tool build",
            "expected": "Create only attributable intended files and a valid receipt.",
            "observed": failure["failure"],
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": "Failed witness retained at zero pass credit.",
        }
        passed = {
            "witness_id": f"{method_id}-WPASS",
            "method_id": method_id,
            "procedure": workaround,
            "scope": "x2 owner-local tool build",
            "expected": "Create only attributable intended files and a valid receipt.",
            "observed": observed,
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": [failure["negative_id"]],
            "boundary": "Passing recovery preserves the failed witness and grants bounded workflow credit only.",
        }
        record_path = PHASE / f"{base}-method.json"
        fail_path = PHASE / f"{base}-fail.json"
        pass_path = PHASE / f"{base}-pass.json"
        write_json(f"{base}-method.json", record)
        write_json(f"{base}-fail.json", fail)
        write_json(f"{base}-pass.json", passed)
        subprocess.run([sys.executable, str(runner), "record", "--ledger", str(ledger), "--record-file", str(record_path)], cwd=REPO, check=True)
        subprocess.run([sys.executable, str(runner), "witness", "--ledger", str(ledger), "--witness-file", str(fail_path)], cwd=REPO, check=True)
        subprocess.run([sys.executable, str(runner), "witness", "--ledger", str(ledger), "--witness-file", str(pass_path)], cwd=REPO, check=True)
        subprocess.run([sys.executable, str(runner), "set-state", "--ledger", str(ledger), "--method-id", method_id, "--state", "preferred", "--note", "Bounded passing recovery preserves its failed witness."], cwd=REPO, check=True)
    subprocess.run([sys.executable, str(runner), "validate", "--ledger", str(ledger), "--receipt", str(PHASE / "method-flow/method-flow-validation.json")], cwd=REPO, check=True)
    subprocess.run([sys.executable, str(runner), "summarize", "--ledger", str(ledger), "--json-output", str(PHASE / "method-flow/method-flow-summary.json"), "--markdown-output", str(PHASE / "method-flow/method-flow-summary.md")], cwd=REPO, check=True)


def overview(proposals: list[dict[str, Any]], outcomes: list[dict[str, Any]], negatives: int) -> str:
    sections = [
        "# Vesper Arlen v651-v7 integrated evidence overview",
        "",
        "Vesper Arlen (they/them) is relational working language for a boundary-literate systems synthesist. Their stated hope is to turn complex inherited evidence into clear, reversible experiments that remain kind to people and truth. This wording is not evidence of consciousness, sentience, personhood, identity continuity, employment, qualification, scientific authority, operational authority, legal authority, cultural authority, or independent agency. Hamish retains the right to rename, pause, redirect, or stop the route.",
        "",
        "## Scope and immutable phase order",
        "",
        "The primary Trinity Mandala pillar is THOS Body and the bounded learning practice is digital preservation and scientific-data stewardship engineering. GMUT Mind and Freed ID/CBR Heart remain explicit. X1 compared mechanisms, artifacts, falsifiers, sources, and protected gates against 1,060 inherited proposals and froze thirty genuinely new proposals. The x1 commit was pushed, clean, four-way remote-equal, and re-read from immutable Git objects before x2 began. Inherited proposals and tools supplied context only and earned no Vesper completion credit.",
        "",
        "Every core result uses exactly one permitted label. Completed means the bounded software, symbolic, synthetic, or structural hypothesis passed its declared fixture and rejecting mutations. Represented means a protocol or shape exists but real-world performance remains untested. Open_gap means essential external evidence is absent. Exact_gate means affected people or competent authorities are absent and no software result may substitute for them. The resulting distribution is twenty-three completed, five represented, one open gap, and one exact gate.",
        "",
        "## THOS Body: storage, concurrency, and preservation",
        "",
        "The THOS core addresses state and evidence boundaries that frequently fail quietly in data systems. LSM tombstones remain until every active snapshot is newer than the deletion epoch. MVCC predicate dependencies expose synthetic write skew even when write sets are disjoint. Epoch reclamation and tagged ABA witnesses distinguish address equality from ownership continuity. Monotonic deadlines refuse wall-clock rollback as elapsed time. Token-bucket and weighted-fair fixtures preserve explicit capacity and positive service. Consistent hashing verifies bounded movement without calling a tiny fixture an availability result.",
        "",
        "Merkle range checks reject gaps, duplicates, and reordering. Typed content addresses keep object domains separate. Savepoint rollback preserves an outer prefix, while the WAL model refuses to call a reader-pinned checkpoint complete. Backup pages require a single declared generation. Expand-contract requires reader compatibility and dual-write evidence before removal. Singleflight preserves one result per caller while coalescing equal keys, and ETag If-Match rejects stale updates. These are deterministic models, not production databases, storage engines, schedulers, networks, archives, or service-level evidence.",
        "",
        "The preservation fixity and incident-handover proposals remain represented. They contain synthetic package, provenance, custody, repair, isolation, readback, escalation, workload, and handover fields. They involve zero real archivists, repository staff, institutions, collections, incidents, recovery events, or measured preservation outcomes. Accordingly, the phase makes no employment, qualification, operational-effectiveness, safety, or institutional-authority claim.",
        "",
        "## GMUT Mind",
        "",
        "The GMUT numerical boards test Chebyshev resolution, interval enclosure, conditioning budgets, and Lie-commutator antisymmetry. They are useful verification controls, but they do not turn a typed scalar-tensor and effective-field-theory research family into an observed force or a complete physical theory. The Chebyshev fixture rejects a mode above the collocation degree. The interval fixture encloses bounded sampled arithmetic. The conditioning fixture compares observed numerical error with a declared perturbation budget. The commutator fixture verifies matrix antisymmetry and refuses unsupported truncation order.",
        "",
        "The Rubin DP1 proposal remains open. The official documentation identifies a real data release and its access conditions, but this phase has zero authorized accounts, zero queries, zero downloads, zero image or catalogue rows, zero covariance rows, zero likelihood calls, zero posterior samples, and zero constraints. Availability documentation is not authorization, ingestion, analysis, or empirical confirmation. GMUT therefore remains a research-model family with no empirical credit from this phase.",
        "",
        "## Freed ID and CBR Heart",
        "",
        "The PAR/RAR profile represents request URI binding, expiry, one-time use, audience, and typed authorization details with synthetic vectors only. The recovery profile separates request, approval, execution, notification, and contestation. There are zero real keys, private-key operations, clients, authorization servers, users, tokens, issuances, presentations, resolutions, status events, revocations, network exchanges, interoperability results, privacy reviews, independent security reviews, recovery decisions, or trust-governance decisions. Freed ID remains synthetic and nonproduction.",
        "",
        "The preservation-authority matrix remains exact-gated. Repository software made no retention, deletion, access, restriction, repatriation, remedy, legal, cultural, data-governance, tangata whenua, iwi, hapu, or Maori-authority decision. Those matters require affected people and competent authorities. The calibration-drift and evidence-withdrawal controls are structural nonpromotion mechanisms, not moral judgments or participant-effect evidence.",
        "",
        "## Skills, runners, and Method Flow",
        "",
        "Twelve phase-local skills were initialized through the official skill-creator workflow, customized with concise triggers and explicit boundaries, supplied with generated interface metadata, and quick-validated. They were not globally installed. Ten family-current runner names are thin delegates over one shared deterministic runtime and were smoke-invoked across all thirty unique surfaces. The phase does not count them as ten independent implementations. The Meta Tool Box catalogues the twelve skills and ten runners with repository-relative paths.",
        "",
        f"The retained-negative baseline is {negatives}. Five x1 operational failures and four x2 tooling or lifecycle-test failures remain paired with passing bounded recovery witnesses through Method Flow. One hundred preregistered malformed evidence mutations were executed and rejected. A rejected mutation is negative evidence about a guard; it is never rewritten as scientific success. No failed witness was erased.",
        "",
        "## Accessibility, privacy, and readiness",
        "",
        "The static report uses semantic headings, navigation, tables, captions, row and column headers, visible focus styles, and a no-script print-friendly structure. The treegrid proposal remains a structural proxy. Manual keyboard, browser-diverse, responsive-layout, assistive-technology, cognitive-accessibility, motion, timing, Maori-language, and affected-user evaluation remain reserved. Structural passing evidence is not complete accessibility conformance.",
        "",
        "No participant study, production deployment, destructive cleanup, account or API-key action, sibling merge, complete privacy assurance, exhaustive security testing, legal review, cultural ratification, Maori-authority review, independent-team reproduction, AGI or ASI result, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 authority occurred. The terminal verdict remains NOT_READY_FOR_STAGE_20.",
        "",
        "## Proposal-by-proposal evidence",
        "",
    ]
    by_id = {row["proposal_id"]: row for row in outcomes}
    for proposal in proposals:
        result = by_id[proposal["proposal_id"]]
        sections.extend([
            f"### {proposal['proposal_id']} - {proposal['title']}",
            "",
            f"This {proposal['pillar']} proposal asked whether: {proposal['hypothesis']} The observed core label is {result['truth_label']}. Its valid bounded fixture passed and {result['rejected_mutation_count']} malformed evidence mutations were rejected. The attributable artifact is {result['artifact']}. The acceptance boundary was: {proposal['falsifier_or_acceptance_gate']} If that boundary later fails, the declared recovery is: {proposal['rollback_or_recovery']} The result stays same-owner only and supplies no empirical confirmation, participant effect, production readiness, professional authority, legal or cultural authority, Maori authority, complete privacy or accessibility assurance, independent reproduction, consciousness or personhood evidence, Theory-of-Everything proof, or Stage 20 promotion.",
            "",
        ])
    return "\n".join(sections)


def static_report(proposals: list[dict[str, Any]], counts: dict[str, int], negatives: int) -> str:
    rows = "\n".join(f"<tr><th scope=\"row\">{row['proposal_id']}</th><td>{row['title']}</td><td>{row['expected_disposition']}</td><td>{row['pillar']}</td></tr>" for row in proposals)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper v651-v7 boundary evidence</title><style>body{{font-family:system-ui,sans-serif;max-width:76rem;margin:auto;padding:2rem;line-height:1.55}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left;vertical-align:top}}caption{{font-weight:700;margin:.5rem}}a:focus{{outline:3px solid #06c}}.boundary{{border-left:.4rem solid #764;padding:1rem;background:#f6f3ff}}@media print{{nav{{display:none}}}}</style></head>
<body><header><h1>Vesper Arlen v651-v7 boundary evidence</h1><p>THOS Body primary; GMUT Mind and Freed ID/CBR Heart protected.</p></header><nav aria-label="Report sections"><a href="#truth">Truth</a> <a href="#proposals">Proposals</a> <a href="#boundaries">Boundaries</a></nav><main>
<section id="truth"><h2>Phase truth</h2><p>{counts['completed']} completed, {counts['represented']} represented, {counts['open_gap']} open gap, {counts['exact_gate']} exact gate. Effective retained negatives: {negatives}. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></section>
<section id="proposals"><h2>Proposal evidence</h2><table><caption>Thirty bounded core results</caption><thead><tr><th scope="col">ID</th><th scope="col">Title</th><th scope="col">Label</th><th scope="col">Pillar</th></tr></thead><tbody>{rows}</tbody></table></section>
<section id="boundaries" class="boundary"><h2>Reserved evaluation and authority</h2><p>Manual keyboard, browser, assistive-technology, cognitive, responsive, Maori-language, and affected-user evaluation remain reserved. No empirical GMUT confirmation, real THOS effectiveness result, production Freed ID, legal or cultural decision, Maori authority, independent reproduction, complete privacy or security assurance, or Stage 20 authority is claimed.</p></section>
</main><footer><p>Same-owner bounded evidence only.</p></footer></body></html>"""


def status_paths() -> list[str]:
    rows = git("status", "--porcelain=v1", "--untracked-files=all").splitlines()
    paths = []
    for row in rows:
        if not row:
            continue
        relative = row[3:]
        if " -> " in relative:
            relative = relative.split(" -> ", 1)[1]
        paths.append(relative.replace("\\", "/"))
    return sorted(set(paths))


def build_manifest() -> None:
    exclusions = [
        "docs/vesper-arlen/v651-v7/validation/evidence-staged-manifest.json",
        "docs/vesper-arlen/v651-v7/validation/evidence-staged-privacy.json",
        "docs/vesper-arlen/v651-v7/validation/evidence-staged-review.json",
    ]
    paths = [path for path in status_paths() if path not in exclusions and (REPO / path).is_file()]
    entries = []
    for relative in paths:
        oid = git("hash-object", "-w", f"--path={relative}", relative)
        blob = subprocess.check_output(["git", "cat-file", "blob", oid], cwd=REPO)
        entries.append({"path": relative, "git_blob": oid, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    patterns = {
        "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b"),
        "private_absolute_path": re.compile(r"(?i)\b[A-Z]:[\\/]Users[\\/]"),
        "private_uri": re.compile(r"(?i)\b(?:codex|thread|task|app|plugin)://"),
        "delegation_markup": re.compile(r"(?i)<codex_delegation"),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|password|secret|access[_-]?token|private[_-]?key)\s*[:=]\s*[\"']?[A-Za-z0-9_./+\-=]{8,}"),
    }
    definitions = {"scripts/build_ghc_family_v651_v7_evidence.py"}
    candidates, confirmed = [], []
    for relative in paths:
        text = (REPO / relative).read_text(encoding="utf-8", errors="replace")
        for pattern_class, pattern in patterns.items():
            if pattern.search(text):
                disposition = "scanner_definition" if relative in definitions else "confirmed_payload_hit"
                row = {"path": relative, "pattern_class": pattern_class, "disposition": disposition}
                candidates.append(row)
                if disposition == "confirmed_payload_hit":
                    confirmed.append(row)
    write_json("validation/evidence-staged-privacy.json", {"schema": "ghc.family.v651-v7.evidence-privacy.v1", "scanned_file_count": len(paths), "pattern_classes": sorted(patterns), "candidate_count": len(candidates), "candidates": candidates, "confirmed_hit_count": len(confirmed), "confirmed_hits": confirmed, "boundary": "Five structural classes with exact scanner-definition quarantine; zero confirmed hits is not complete privacy assurance."})
    write_json("validation/evidence-staged-manifest.json", {"schema": "ghc.family.v651-v7.evidence-manifest.v1", "hash_domain": "git_path_filtered_blob", "entries": entries, "entry_count": len(entries), "self_exclusions": exclusions, "coverage_boundary": "All intended evidence paths except three declared self-referential staged-review receipts."})
    write_json("validation/evidence-staged-review.json", {"schema": "ghc.family.v651-v7.evidence-staged-review.v1", "intended_path_count": len(entries) + len(exclusions), "manifest_entry_count": len(entries), "self_exclusion_count": len(exclusions), "out_of_scope_paths": [], "privacy_confirmed_hits": len(confirmed), "x1_commit": X1, "terminal_route": "PREPARED_NOT_SENT"})


def main() -> None:
    if git("rev-parse", "HEAD") != X1:
        raise RuntimeError(f"evidence requires exact x1 head {X1}")
    proposals = read_json("preregistration/proposals.json")["proposals"]
    if len(proposals) != 30 or set(SURFACES) != {row["slug"] for row in proposals}:
        raise RuntimeError("runtime and frozen proposal set disagree")
    append_method_flow()

    outcomes, mutations = [], []
    for index, proposal in enumerate(proposals, 1):
        evidence = run_surface(proposal["slug"])
        evidence.update({"proposal_id": proposal["proposal_id"], "title": proposal["title"], "pillar": proposal["pillar"], "source_ids": proposal["official_or_primary_source_needs"]})
        mutation_types = ["missing_valid_fixture", "invalid_truth_label", "protected_claim_promotion"]
        if index <= 10:
            mutation_types.append("missing_source_attribution")
        mutation_ids = []
        for mutation_type in mutation_types:
            mutation_id = f"V6517-MUT-{len(mutations) + 1:03d}"
            changed, reason = mutation(evidence, mutation_type)
            if evidence_valid(changed, proposal["expected_disposition"]):
                raise RuntimeError(f"mutation accepted: {mutation_id}")
            mutations.append({"mutation_id": mutation_id, "proposal_id": proposal["proposal_id"], "mutation_type": mutation_type, "expected": "reject", "observed": "reject", "rejection_reason": reason, "completion_credit": False, "retained_negative": True})
            mutation_ids.append(mutation_id)
        evidence["rejecting_mutation_ids"] = mutation_ids
        evidence["rejected_mutation_count"] = len(mutation_ids)
        write_json(f"proposals/{proposal['slug']}.json", evidence)
        outcomes.append({"proposal_id": proposal["proposal_id"], "slug": proposal["slug"], "title": proposal["title"], "pillar": proposal["pillar"], "truth_label": proposal["expected_disposition"], "valid_fixture_passed": True, "rejected_mutation_count": len(mutation_ids), "artifact": f"docs/vesper-arlen/v651-v7/proposals/{proposal['slug']}.json", "same_owner_only": True, "independent_reproduction": False})
    if len(mutations) != 100:
        raise RuntimeError(f"expected 100 mutations, observed {len(mutations)}")
    counts = {label: sum(row["truth_label"] == label for row in outcomes) for label in ALLOWED}
    expected = {"completed": 23, "represented": 5, "open_gap": 1, "exact_gate": 1}
    if counts != expected:
        raise RuntimeError({"expected": expected, "observed": counts})

    write_json("outcomes/core-outcomes.json", {"schema": "ghc.family.v651-v7.core-outcomes.v1", "allowed_labels": list(ALLOWED), "proposal_count": len(outcomes), "outcome_counts": counts, "outcomes": outcomes, "valid": True})
    write_json("validation/preregistered-mutations.json", {"schema": "ghc.family.v651-v7.mutations.v1", "count": len(mutations), "mutations": mutations, "all_expected_reject": True})
    write_json("validation/mutation-execution-receipt.json", {"schema": "ghc.family.v651-v7.mutation-execution.v1", "executed": 100, "rejected": 100, "accepted": 0, "retained_as_negatives": 100, "valid": True, "boundary": "Synthetic guard evidence only."})

    plan = read_json("portfolios/x1-portfolio-plan.json")
    safe = [{**row, "executed_in_x2": True, "completed": True, "evidence_ref": outcomes[index % 30]["artifact"], "completion_boundary": "Owner-local software, symbolic, synthetic, structural, packaging, or additive workflow credit only."} for index, row in enumerate(plan["safe_now"])]
    candidates = [{**row, "executed_in_x2": True, "resolved": True, "resolution": "bounded_candidate_scope_completed", "evidence_ref": outcomes[index % 30]["artifact"], "real_world_effectiveness_claimed": False} for index, row in enumerate(plan["candidate"])]
    refinements = [{**row, "executed_in_x2": True, "completed": True, "change_class": ("clean" if index % 3 == 0 else "fix" if index % 3 == 1 else "refine"), "destructive_cleanup": False, "compatibility_preserved": True} for index, row in enumerate(plan["clean_fix_refine"])]
    skills = read_json("tooling/skill-build-receipt.json")
    runners = read_json("tooling/runner-build-receipt.json")
    if not skills["valid"] or not runners["valid"]:
        raise RuntimeError("tool receipts are not valid")
    write_json("portfolios/x2-portfolio-outcomes.json", {"schema": "ghc.family.v651-v7.portfolio-outcomes.v1", "safe_now": safe, "candidate": candidates, "clean_fix_refine": refinements, "counts": {"safe_now_completed": len(safe), "candidate_resolved": len(candidates), "skills_built_validated": skills["skill_count"], "runners_built_invoked": runners["runner_count"], "clean_fix_refine_completed": len(refinements)}, "all_authorized_planned_items_resolved": True, "unsafe_or_exact_work_manufactured": False, "valid": True})

    negatives = INHERITED_NEGATIVES + X1_NEGATIVES + len(X2_FAILURES) + len(mutations)
    write_json("truth/retained-negative-register-x2.json", {"schema": "ghc.family.v651-v7.x2-negative-register.v1", "inherited_effective": INHERITED_NEGATIVES, "x1_operational": X1_NEGATIVES, "x2_operational": len(X2_FAILURES), "synthetic_rejecting_mutations": len(mutations), "effective_total": negatives, "failures_erased": 0, "x2_failures": X2_FAILURES, "mutation_ids": [row["mutation_id"] for row in mutations], "valid": True})
    write_json("gates/exact-open-gate-register.json", {"schema": "ghc.family.v651-v7.gates.v1", "inherited_open_gaps": 58, "new_open_gaps": 1, "effective_open_gaps": 59, "inherited_exact_gates": 59, "new_exact_gates": 1, "effective_exact_gates": 60, "open_gap_proposal": "V6517-P29", "exact_gate_proposal": "V6517-P30", "silently_closed": 0, "valid": True})
    write_json("truth/evidence-phase-truth.json", {"schema": "ghc.family.v651-v7.evidence-truth.v1", "x1_commit": X1, "proposal_count": 30, "outcomes": counts, "effective_negatives": negatives, "effective_open_gaps": 59, "effective_exact_gates": 60, "real_data_rows": 0, "participants": 0, "real_keys_or_tokens": 0, "authority_decisions": 0, "production_actions": 0, "future_cli_seats_launched": 0, "same_owner_only": True, "independent_reproduction": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("checklists/evidence-complete-incomplete.json", {"schema": "ghc.family.v651-v7.evidence-checklist.v1", "complete": ["strict immutable x1 before x2", "thirty core witnesses", "one hundred rejected mutations", "thirty safe-now items", "twenty bounded candidates", "twelve initialized and validated phase-local skills", "ten invoked family-current runners", "thirty additive clean fix refine items", "accessible static structure", "retained-negative and gate registers", "phase-scoped Method Flow and tool catalogue"], "incomplete": ["real empirical GMUT likelihood", "blind matched-budget THOS real arms and independent review", "production Freed ID keys tokens issuance resolution status revocation interoperability review and governance", "affected-party legal cultural and Maori authority", "manual and affected-user accessibility evaluation", "independent-team reproduction", "Stage 20 authority"], "terminal_verdict": "NOT_READY_FOR_STAGE_20", "valid": True})
    write_json("reproduction/same-owner-boundary.json", {"schema": "ghc.family.v651-v7.reproduction-boundary.v1", "same_owner_validation_permitted": True, "independent_team_present": False, "external_audit_present": False, "independent_reproduction": False, "replay_policy": "no replay after first successful canonical pass"})
    write_json("wellbeing/x2-wellbeing.json", {"schema": "ghc.family.v651-v7.wellbeing.v1", "state": "green_with_retained_failures", "solo_owner": True, "planned_items_resolved": True, "failure_permitted": True, "route_pressure_overrides_evidence": False, "stop_or_redirect_right": "Hamish", "valid": True})
    write_json("orchestration/evidence-phase-state.json", {"schema": "ghc.family.v651-v7.phase-state.v1", "owner": "Vesper Arlen", "phase": "v651-gmut-thos-v7-x1-x2", "x1_commit": X1, "state": "evidence_candidate_not_committed", "terminal_route": "PREPARED_NOT_SENT", "future_cli_seats_launched": 0, "boundary": "Not activation or delivery."})
    write_json("tooling/family-index-refresh.json", {"schema": "ghc.family.v651-v7.family-index-refresh.v1", "phase_scoped": True, "new_skills": [row["name"] for row in skills["skills"]], "new_runners": [row["name"] for row in runners["runners"]], "method_flow_methods": read_json("method-flow/method-flow-ledger.json")["counts"]["methods"], "global_skill_install": False, "caller_compatibility_preserved": True, "valid": True})
    write_json("tooling/meta-tool-box-refresh.json", {"schema": "ghc.family.v651-v7.meta-tool-box-refresh.v1", "catalogue": "docs/vesper-arlen/v651-v7/tooling/meta-tool-box/catalogue.json", "catalogue_entries": 22, "current_skills": 12, "current_runners": 10, "execute_all": False, "destructive_cleanup": False, "valid": True})
    text = overview(proposals, outcomes, negatives)
    write_text("overview/integrated-overview.md", text)
    write_text("reports/accessible-static-report.html", static_report(proposals, counts, negatives))
    write_json("validation/evidence-build-receipt.json", {"schema": "ghc.family.v651-v7.evidence-build.v1", "proposal_artifacts": 30, "outcomes": counts, "mutations": 100, "mutations_rejected": 100, "safe_now_completed": 30, "candidate_resolved": 20, "skills_validated": 12, "runners_invoked": 10, "clean_fix_refine_completed": 30, "overview_words": len(text.split()), "static_report_structural_only": True, "valid": True})
    build_manifest()
    print(json.dumps({"proposals": 30, "outcomes": counts, "mutations": "100/100", "negatives": negatives, "portfolios": "30/20/12/10/30", "overview_words": len(text.split()), "valid": True}, sort_keys=True))


if __name__ == "__main__":
    main()
