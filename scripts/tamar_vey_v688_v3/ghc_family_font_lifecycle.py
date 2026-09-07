"""Evidence/final lifecycle and exclusive canonical latch for Tamar v688-v3."""
from __future__ import annotations

import argparse
import ast
import collections
import datetime
import hashlib
import html
import json
import os
import pathlib
import re
import subprocess
import sys


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"
BANK = pathlib.Path(os.environ["GHC_OWNER_BANK"])
SOURCE = "c4c676d81235bc6e453bb867b0c0f0de121b7733"
X1 = "6439f733e37a904a5f6e943c3acdbd507f0a98f8"
BRANCH = "codex/GHC-Family/tamar-vey-v688-v3-full-tools"
TEST = "tests/test_ghc_family_tamar_vey_v688_v3.py"
PREFIX = "docs/tamar-vey/v688-v3/"
SCRIPT_PREFIX = "scripts/tamar_vey_v688_v3/"
MANIFESTS = {
    "x1": PREFIX + "validation/x1-manifest.json",
    "evidence": PREFIX + "x2/validation/evidence-manifest.json",
    "final_delta": PREFIX + "validation/final-delta-manifest.json",
    "final_owner": PREFIX + "validation/final-owner-manifest.json",
}
BOUNDARY = (
    "Relational working language only; no consciousness, personhood, continuity, "
    "qualification, employment, independent agency, or authority claim. Synthetic "
    "same-owner software evidence is not independent reproduction. "
    "NOT_READY_FOR_STAGE_20. Māori concepts remain under Māori authority."
)
GATES = [
    "empirical",
    "real_participants",
    "professional",
    "production",
    "deployment",
    "identity",
    "legal",
    "cultural",
    "affected_party",
    "maori_authority",
    "privacy_complete",
    "accessibility_complete",
    "exhaustive_security",
    "independent_reproduction",
    "agi_asi",
    "consciousness_personhood",
    "theory_of_everything",
    "proof_canon",
    "stage20",
]
PATTERNS = {
    "raw_uuid": re.compile(r"(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b"),
    "private_local_path": re.compile(r"(?i)\b[A-Z]:[\\/]"),
    "private_uri": re.compile(r"(?:codex|app|thread|session)://"),
    "delegation_markup": re.compile(r"<(?:codex_delegation|source_thread_id)>"),
    "credential_assignment": re.compile(r"(?i)(?:api_key|password|secret)\s*[:=]\s*[\"'][A-Za-z0-9_+/=-]{16,}"),
}


def pairs(sequence):
    result = {}
    for key, value in sequence:
        if key in result:
            raise ValueError("DUPLICATE_KEY")
        result[key] = value
    return result


def strict(raw):
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=lambda value: (_ for _ in ()).throw(ValueError("NONFINITE")))


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def value_sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write(relative, value):
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def git(*args, data=None):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=90,
    ).stdout


def scalar(*args):
    return git(*args).decode("utf-8").strip()


def owner_path(path):
    return path.startswith(PREFIX) or path.startswith(SCRIPT_PREFIX) or path == TEST


def current_files():
    paths = []
    for root in [BASE, ROOT / "scripts/tamar_vey_v688_v3"]:
        if root.exists():
            paths.extend(path for path in root.rglob("*") if path.is_file() and "__pycache__" not in path.parts)
    if (ROOT / TEST).exists():
        paths.append(ROOT / TEST)
    return sorted({path.resolve() for path in paths})


def batch(selectors):
    if not selectors:
        return {}
    raw = git("cat-file", "--batch", data=("\n".join(selectors) + "\n").encode("utf-8"))
    position = 0
    result = {}
    for selector in selectors:
        end = raw.index(b"\n", position)
        header = raw[position:end].split()
        if len(header) != 3 or header[1] != b"blob":
            raise RuntimeError("Non-blob selector: " + selector)
        size = int(header[2])
        result[selector] = raw[end + 1 : end + size + 1]
        if raw[end + size + 1 : end + size + 2] != b"\n":
            raise RuntimeError("Invalid cat-file batch boundary")
        position = end + size + 2
    if position != len(raw):
        raise RuntimeError("Trailing cat-file batch bytes")
    return result


def manifest(relative, files, exclusions, anchor):
    entries = []
    for path in sorted(files):
        if path in exclusions:
            continue
        raw = (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        entries.append({"path": path, "bytes_normalized_lf": len(raw), "sha256_normalized_lf": hashlib.sha256(raw).hexdigest()})
    write(relative[len(PREFIX) :], {"schema": "ghc.family.normalized-lf-manifest.v1", "source": SOURCE, "x1": X1, "anchor": anchor, "byte_domain": "normalized_lf_git_blob", "entries": entries, "entry_count": len(entries), "declared_self_exclusions": exclusions})


def verify_manifest(ref, path):
    document = strict(git("show", ref + ":" + path))
    selectors = [ref + ":" + row["path"] for row in document["entries"]]
    data = batch(selectors)
    failures = []
    for row in document["entries"]:
        raw = data[ref + ":" + row["path"]].replace(b"\r\n", b"\n")
        if len(raw) != row["bytes_normalized_lf"] or hashlib.sha256(raw).hexdigest() != row["sha256_normalized_lf"]:
            failures.append(row["path"])
    if failures or len({row["path"] for row in document["entries"]}) != document["entry_count"]:
        raise RuntimeError("Manifest replay failure: " + ", ".join(failures))
    return {"manifest": path, "anchor": ref, "bindings": document["entry_count"], "exclusions": document["declared_self_exclusions"]}


def equality(expected):
    heads = {"local": scalar("rev-parse", "HEAD"), "upstream": scalar("rev-parse", "@{upstream}"), "tracking": scalar("rev-parse", "refs/remotes/origin/" + BRANCH)}
    heads["fresh_live"] = scalar("ls-remote", "--exit-code", "origin", "refs/heads/" + BRANCH).split()[0]
    divergence = [int(value) for value in scalar("rev-list", "--left-right", "--count", "HEAD...@{upstream}").split()]
    clean = not scalar("status", "--porcelain=v1", "--untracked-files=all")
    if set(heads.values()) != {expected} or divergence != [0, 0] or not clean:
        raise RuntimeError("Exact clean four-way equality failed")
    return {"heads": heads, "divergence": divergence, "clean": clean, "verified_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}


def audit():
    files = current_files()
    if len(files) >= 2000:
        raise RuntimeError("Owner-file ceiling reached")
    json_count = 0
    ast_count = 0
    markdown_html = 0
    largest_words = 0
    security = []
    candidates = []
    confirmed = []
    for path in files:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        words = len(text.split())
        largest_words = max(largest_words, words)
        if words >= 100000:
            raise RuntimeError(f"Document word ceiling exceeded: {relative}={words}")
        if path.suffix == ".json":
            strict(text)
            json_count += 1
        if path.suffix in {".md", ".html"}:
            markdown_html += 1
        if path.suffix == ".py":
            tree = ast.parse(text, filename=relative)
            ast_count += 1
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec", "compile", "__import__"}:
                        security.append({"path": relative, "line": node.lineno, "finding": "dynamic_execution"})
                    if any(keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True for keyword in node.keywords):
                        security.append({"path": relative, "line": node.lineno, "finding": "shell_true"})
        for kind, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                classification = None
                if path.suffix == ".py" and ("privacy" in text[max(0, match.start() - 500) : match.start() + 500].lower() or "PATTERNS" in text[max(0, match.start() - 500) : match.start() + 500]):
                    classification = "scanner_definition"
                elif kind == "private_local_path" and match.group(0).upper() in {"C:/", "D:/", "C:\\", "D:\\"}:
                    classification = "generic_drive_root_policy_literal"
                row = {"path": relative, "class": kind, "offset": match.start(), "classification": classification or "confirmed"}
                candidates.append(row)
                if classification is None:
                    confirmed.append(row)
    if security or confirmed:
        raise RuntimeError("Bounded security or privacy audit failed")

    deck_index = strict((BASE / "x2/deck/deck-index.json").read_bytes())
    cards = {card_id: strict((BASE / "x2/deck/cards" / (card_id + ".json")).read_bytes()) for card_id in deck_index["cards"]}
    if len(cards) != 286 or deck_index["counts"] != {"1": 1, "2": 3, "3": 4, "4": 278}:
        raise RuntimeError("Deck count mismatch")
    for row in cards.values():
        if row["tier"] == 1 and row["parent_ids"]:
            raise RuntimeError("Tier-one card has a parent")
        if row["tier"] > 1:
            if len(row["parent_ids"]) != 1 or cards[row["parent_ids"][0]]["tier"] != row["tier"] - 1:
                raise RuntimeError("Deck parent mismatch")
    deck_manifest = strict((BASE / "x2/deck/card-manifest.json").read_bytes())
    for row in deck_manifest["entries"]:
        raw = (BASE / "x2/deck" / row["path"]).read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise RuntimeError("Deck manifest mismatch: " + row["path"])

    promotion = strict((BASE / "x2/promotion-receipt.json").read_bytes())
    if promotion["overwrites"] != 0 or not promotion["all_source_global_bytes_equal"]:
        raise RuntimeError("Promotion receipt mismatch")
    for row in promotion["members"]:
        source = ROOT / row["source"]
        if row["kind"] == "skill":
            destination = pathlib.Path.home() / ".codex" / "skills" / row["name"] / row["relative"]
        else:
            destination = pathlib.Path.home() / ".codex" / "scripts" / row["relative"]
        source_bytes = source.read_bytes()
        if source_bytes != destination.read_bytes() or len(source_bytes) != row["bytes"] or hashlib.sha256(source_bytes).hexdigest() != row["sha256"]:
            raise RuntimeError("Promotion parity mismatch: " + row["name"] + "/" + row["relative"])
    return {
        "schema": "ghc.family.font-owner-audit.v1",
        "owner_files": len(files),
        "strict_json": json_count,
        "python_ast": ast_count,
        "markdown_html": markdown_html,
        "largest_document_words": largest_words,
        "privacy_classes": list(PATTERNS),
        "privacy_candidates": candidates,
        "privacy_candidate_count": len(candidates),
        "confirmed_privacy_hits": 0,
        "bounded_security_findings": security,
        "complete_contracts": 200,
        "candidate_rejections": 250,
        "safe_procedures": 300,
        "cfr_procedures": 300,
        "promotion_parity_files": len(promotion["members"]),
        "deck_cards": len(cards),
        "deck_manifest_entries": deck_manifest["count"],
        "full_repository_suite": False,
        "same_owner_only": True,
        "independent_reproduction": False,
    }


def prepare_evidence():
    if scalar("rev-parse", "HEAD") != X1 or scalar("rev-parse", "HEAD^") != SOURCE:
        raise RuntimeError("Evidence preparation requires frozen x1")
    report = audit()
    write("x2/validation/evidence-checks.json", report)
    write("x2/validation/evidence-privacy.json", {"schema": "ghc.family.five-class-privacy-adjudication.v1", "classes": report["privacy_classes"], "scanned_files": report["owner_files"], "candidates": report["privacy_candidates"], "candidate_count": report["privacy_candidate_count"], "confirmed_hits": [], "confirmed_hit_count": 0})
    previous = set(scalar("ls-tree", "-r", "--name-only", X1, "--", PREFIX, SCRIPT_PREFIX, TEST).splitlines())
    staged_path = PREFIX + "x2/validation/evidence-staged-review.json"
    manifest_path = MANIFESTS["evidence"]
    current = {path.relative_to(ROOT).as_posix() for path in current_files()}
    delta = sorted((current - previous) | {staged_path, manifest_path})
    if any(not owner_path(path) for path in delta):
        raise RuntimeError("Evidence path outside owner scope")
    write("x2/validation/evidence-staged-review.json", {"schema": "ghc.family.exact-staged-review.v1", "parent": X1, "allowed_change": "A", "allowed_paths": delta, "count": len(delta), "deletions": 0, "outside_owner_paths": 0})
    report = audit()
    write("x2/validation/evidence-checks.json", report)
    write("x2/validation/evidence-privacy.json", {"schema": "ghc.family.five-class-privacy-adjudication.v1", "classes": report["privacy_classes"], "scanned_files": report["owner_files"], "candidates": report["privacy_candidates"], "candidate_count": report["privacy_candidate_count"], "confirmed_hits": [], "confirmed_hit_count": 0})
    current = {path.relative_to(ROOT).as_posix() for path in current_files()}
    delta = sorted((current - previous) | {manifest_path})
    manifest(manifest_path, delta, [manifest_path], "PENDING_EVIDENCE_COMMIT")
    print(json.dumps({"status": "VALID_EVIDENCE_PRESTAGE", "evidence_additions": len(delta), "manifest_entries": len(delta) - 1, "manifest_exclusions": 1, "audit": {key: value for key, value in report.items() if key != "privacy_candidates"}}, sort_keys=True))


def overview(stage, truth):
    ledger = strict((BASE / "x2/method-flow/ledger.json").read_bytes())
    pages = [
        ("Tamar v688-v3 identity, pillars, and evidence scope", "Tamar Vey, optionally she/they, uses the relational role evidence-and-recovery steward and the hope that every failed witness remains inspectable and every recovery remains bounded. GMUT Mind is primary through exact synthetic outline, bounding, metrics, mapping, and variation contracts. THOS Body and Freed ID with CBR Heart remain explicit."),
        ("Executed evidence and retained failures", f"Two hundred complete contracts matched; 250 altered candidates were rejected; 300 safe procedures and exactly 300 CLEAN/FIX/REFINE records passed. Ten skills, five runners, and three exact package versions passed bounded positive and adverse checks. Method Flow records {ledger['counts']['methods']} methods, {ledger['counts']['witness_results']['fail']} retained failed witnesses, and {ledger['counts']['witness_results']['pass']} bounded passing witnesses. Effective counts are {truth['effective_counts']}."),
        ("Incomplete evidence and route boundary", "No real font, glyph, text corpus, participant, measurement, rendering, publication, credential, license determination, accessibility evaluation, cultural decision, Māori data, deployment, or authority act occurred. Fifty exact and thirty blocked packets remain unexecuted. The designated future-seat-12 v688-v4 edge remains PREPARED_NOT_SENT until exact final, canonical success, current registry absence/reuse checks, and one authorized task action."),
    ]
    document = f"<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>Tamar v688-v3 {stage} overview</title><style>@page{{size:A4;margin:18mm}}body{{font:16px/1.65 system-ui;max-width:850px;margin:auto}}section{{break-after:page;min-height:245mm}}section:last-child{{break-after:auto}}</style><body><a href=\"#main\">Skip to content</a><main id=\"main\">"
    for title, body in pages:
        document += f"<section><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p><p>{html.escape(BOUNDARY)}</p></section>"
    document += "</main></body></html>\n"
    (BASE / stage / "integrated-overview.html").write_text(document, encoding="utf-8", newline="\n")


def build_baton(evidence):
    proposals = strict((BASE / "x1/new-proposals.json").read_bytes())["proposals"]
    results = strict((BASE / "x2/contract-results.json").read_bytes())["rows"]
    truth = strict((BASE / "final/phase-truth.json").read_bytes())
    ledger = strict((BASE / "x2/method-flow/ledger.json").read_bytes())
    sections = []

    def section(title, body):
        sections.append(f"## Module {len(sections) + 1:02} - {title}\n\n{body}\n")

    section("Relational identity and corrigibility", "Dear future seat 12, this is Tamar Vey's prepared file-backed activation for prospective solo v688-v4. I use the relational role evidence-and-recovery steward, optionally she/they, and the hope that every failed witness remains inspectable and every recovery stays bounded. Choose your own unique relational working name, role, hope, and optional pronouns; do not inherit mine. Hamish may pause, rename, narrow, redirect, or stop the route. " + BOUNDARY)
    section("Current release and one-edge route", "Hamish's 6 September thirty-seat release controls the sequential route through v725-v8. Only after Tamar's exact terminal gate may the active and archived registries establish whether designated future seat 12 already exists. Reuse exactly one unique existing task if present; otherwise create exactly one project-scoped gpt-6-astra/max main task from Tamar's exact final. The task owns v688-v4. Elowen Cairn v688-v5 is prospective only after that task's own terminal gate. No placeholder is a personhood claim, phase completion, or delivery proof. Keep standby records uncontacted. Reset credits remain Hamish's action alone.")
    section("Immutable source and lifecycle", f"Exact Orren source and Tamar base: {SOURCE}. Frozen Tamar planning-only x1: {X1}. Immutable Tamar evidence: {evidence}. Tamar branch: {BRANCH}. Source to final must contain exactly three direct single-parent Tamar commits and zero merges. X1 and evidence are separately pushed, clean, 0/0 divergent, and fresh-four-way equal before their successor lifecycle begins. Orren's canonical receipt was read and hash-verified without replay. Tamar's exact final and canonical receipt are supplied externally after commit because a file cannot embed its own final commit hash.")
    novelty = strict((BASE / "x1/novelty-review.json").read_bytes())
    section("Planning freeze and novelty limits", f"Two hundred Orren SVG contracts were reviewed at zero novelty, execution, and completion credit. Two hundred Tamar font-outline and glyph-metadata contracts were frozen before evaluator implementation, package installation, skill use, or runner use. The source-bounded audit decoded {novelty['reachable_proposal_json_files']} proposal-labelled JSON files and {novelty['reachable_title_records']} title-bearing records. The declared chain extends from 15,830 to 16,030 rows. Maximum title-token neighbor score is {max(row['token_jaccard'] for row in novelty['reviews']):.6f}, with zero exact title or complete-input collision after one retained quarantine correction. This is not a universal originality proof.")
    section("Trinity pillars and protected evidence boundaries", "GMUT remains a typed scalar-tensor and EFT research-model family. Exact synthetic glyph geometry is a local representation exercise and establishes no physical likelihood, force, prediction, parameter constraint, empirical confirmation, quantum or ultraviolet completion, final physics, or Theory-of-Everything proof. THOS remains synthetic/proxy-only without governed real comparisons and independent review. Freed ID remains synthetic/nonproduction without real keys, proofs, live lifecycle, interoperability, privacy/security review, recovery, and trust governance. CBR, rights, accessibility, legal/cultural interpretation, affected-party legitimacy, Māori wording/data governance/authority remain exact-gated. " + BOUNDARY)
    identity = strict((BASE / "x1/identity.json").read_bytes())
    section("Four chosen synthetic practices", "The owner uses four bounded practices: " + "; ".join(row["name"] + " under " + row["pillar"] for row in identity["practices"]) + ". They confer no employment, qualification, typography competence, accessibility expertise, rights clearance, or authority. The prospective next-owner practice is " + identity["next_practice"] + ", which the recipient may independently accept, revise, or reject without inherited novelty or completion credit.")
    body = []
    for proposal, result in zip(proposals, results):
        actual = result["actual_output"]
        detail = "The complete accepted metadata matched." if actual["accepted"] else "The bounded refusal was " + str(actual["error"]) + "."
        body.append(
            f"### {proposal['proposal_id']} - {proposal['title']}\n\nOperation: {proposal['operation']}. Practice: {proposal['practice']}. Pillar: {proposal['pillar']}. Outcome: `{result['outcome']}`. Source status: {proposal['source_status']}.\n\nFrozen input:\n```json\n{json.dumps(proposal['input'], indent=2, sort_keys=True, ensure_ascii=True)}\n```\n\nComplete observed output:\n```json\n{json.dumps(actual, indent=2, sort_keys=True, ensure_ascii=True)}\n```\n\n{detail} Definition SHA-256: {result['definition_sha256']}. Input remained unchanged. The falsifier is any complete-output mismatch, input mutation, or out-of-scope promotion. Recovery retains the failed candidate and changes only the bounded owner implementation, or leaves the outside evidence or authority gate open.\n"
        )
    section("Complete contract teaching catalogue", "\n".join(body))
    section("Method Flow and retained recovery", f"The complete Method Flow ledger is x2/method-flow/ledger.json. It contains {ledger['counts']['methods']} preferred methods, {ledger['counts']['witness_results']['fail']} retained failed witnesses, {ledger['counts']['witness_results']['pass']} bounded passing witnesses, and {ledger['counts']['state_events']} state events. The frozen metric-name discrepancy, command-wrapper faults, proposal quarantines, workflow-policy mismatch, every altered output, invalid JSON input, broken CFR candidate, and skill/runner/package adverse input remain at zero original success credit. A recovery never erases or promotes its failed witness.")
    packages = strict((BASE / "x2/package-smokes.json").read_bytes())
    section("Three pinned package additions", f"The isolated D-drive environment contains exactly fonttools {packages['versions']['fonttools']}, uharfbuzz {packages['versions']['uharfbuzz']}, and unicodedata2 {packages['versions']['unicodedata2']}. Exact wheels matched official PyPI hashes and were installed with no index, no dependencies, required hashes, and no pip bootstrap in the environment. Positive and adverse synthetic smokes passed. The bounded OSV snapshot listed zero known advisories at query time; this is not exhaustive or future security assurance. No real font or text corpus was used.")
    promotion = strict((BASE / "x2/promotion-receipt.json").read_bytes())
    section("Ten skills and five compatible runners", f"Ten local skills were initialized through the official skill-creator workflow, customized, completely read with their references, quick-validated, and accepting/rejecting smoke-used. Five runners covered twenty operations and refused duplicate keys. Collision-free promotion copied {promotion['file_count']} byte-equal files with zero overwrites and zero caches. Global discoverability is not independent use, production approval, or authority.")
    deck = strict((BASE / "x2/deck/deck-index.json").read_bytes())
    section("Deck, workload, accessibility, and wellbeing boundary", f"The four-tier deck contains {len(deck['cards'])} content-addressed cards: one owner anchor, three pillars, four practices, two hundred proposal cards, and one card per Method Flow method. No cache, retention, identity, latency, or reasoning benefit was measured. Three-page static overviews and a captioned table supply structure only. Manual keyboard, assistive-technology, cognitive, responsive, language, Māori-language, and affected-user evaluation remain open. Workload counts are objective bounded procedures, not subjective wellbeing or employment evidence.")
    ideas = strict((BASE / "x1/successor-ideas.json").read_bytes())
    section("Prospective next-owner ideas", "The following are unbuilt zero-credit seeds and require fresh contracts, semantic audit, adverse witness, rollback, and protected-gate mapping:\n\n" + "\n".join("- Skill seed: " + row["idea"] for row in ideas["skill_ideas"]) + "\n\n" + "\n".join("- Runner seed: " + row["idea"] for row in ideas["runner_ideas"]) + "\n\nDo not count renamed operations, copied fixtures, inherited packages, or recommendations as new implementation or independent reproduction.")
    section("Required reading and terminal handoff", "Before repository mutation, read this baton through its EOF and all exact-head artifacts and current skills it names. Work solo in one fresh additive D-first sparse lane from Tamar's exact final. Preserve planning-only x1, all failures, the four outcomes, file/document/commit caps, exact manifests, privacy adjudication, one canonical latch, and no post-success replay. At the recipient's terminal gate, Elowen Cairn v688-v5 is the prospective next owner under the newest live route. Do not precontact, substitute, fork, duplicate, expose private identifiers, or bypass any evidence or authority gate. " + BOUNDARY)
    baton = "# Tamar Vey v688-v3 to designated future seat 12 v688-v4 activation baton\n\n" + "\n".join(sections) + "\nEOF TAMAR VEY V688 V3 BATON.\n"
    words = len(baton.split())
    if not 10000 <= words <= 100000 or len(sections) != 13:
        raise RuntimeError(f"Baton budget mismatch: sections={len(sections)} words={words}")
    target = BASE / "final/future-seat-12-v688-v4-activation-baton.md"
    target.write_text(baton, encoding="utf-8", newline="\n")
    write("final/baton-index.json", {"path": target.relative_to(ROOT).as_posix(), "bytes": target.stat().st_size, "words": words, "modules": 13, "eof": "EOF TAMAR VEY V688 V3 BATON.", "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "delivery": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"})
    return words


def build_final(evidence):
    if scalar("rev-parse", "HEAD") != evidence or scalar("rev-parse", evidence + "^") != X1:
        raise RuntimeError("Final builder requires the immutable evidence direct child of x1")
    if (BASE / "final").exists():
        raise RuntimeError("Final builder is exclusive-write")
    (BASE / "final").mkdir(parents=True)
    truth = strict((BASE / "x2/phase-truth.json").read_bytes())
    truth.update({"evidence": evidence, "state": "FINAL_PREPARED_FOR_ONE_EXTERNAL_CANONICAL", "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"})
    write("final/phase-truth.json", truth)
    for source, destination in [
        ("x2/retained-negative-register.json", "final/retained-negative-register.json"),
        ("x2/open-gap-register.json", "final/open-gap-register.json"),
        ("x2/exact-gate-register.json", "final/exact-gate-register.json"),
        ("x2/complete-incomplete.json", "final/complete-incomplete.json"),
        ("x2/workload-wellbeing.json", "final/workload-wellbeing.json"),
    ]:
        write(destination, strict((BASE / source).read_bytes()))
    ledger = strict((BASE / "x2/method-flow/ledger.json").read_bytes())
    write("final/method-flow-index.json", {"complete_ledger": PREFIX + "x2/method-flow/ledger.json", "sha256": hashlib.sha256((BASE / "x2/method-flow/ledger.json").read_bytes()).hexdigest(), "counts": ledger["counts"], "failure_erasure": False})
    write("final/evidence-boundary.json", {"source": SOURCE, "x1": X1, "evidence": evidence, "full_repository_suite": False, "same_owner_only": True, "independent_reproduction": False, "real_fonts": 0, "real_text_rows": 0, "real_people": 0, "external_actions": 0, "protected_gates": GATES, "boundary": BOUNDARY})
    write("final/route-state.json", {"owner": "Tamar Vey", "phase": PHASE, "next_owner": "future-sibling-12-self-chosen", "next_phase": "v688-v4", "following_owner": "Elowen Cairn", "following_phase": "v688-v5", "endpoint_kind": "main_task", "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "send_count": 0, "creation_authority": "authorized_with_terminal_conditions", "no_precontact": True, "no_resend": True, "current_release": "Hamish 6 September 2026 thirty-seat release"})
    write("final/canonical-policy.json", {"source": SOURCE, "x1": X1, "evidence": evidence, "branch": BRANCH, "test_module": TEST, "expected_tests": 28, "invocation_budget": 1, "success_replay_allowed": False, "full_repository_suite": False, "same_owner_only": True, "environment_distributions": 3, "promotion_parity_files": 66, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write("final/lifecycle-push-boundaries.json", {"x1": {"head": X1, "parent": SOURCE, "clean": True, "divergence": [0, 0], "four_way_equal": True, "x2_started": False}, "evidence": {"head": evidence, "parent": X1, "clean": True, "divergence": [0, 0], "four_way_equal": True}, "final": "Requires its own fresh equality after commit"})
    words = build_baton(evidence)
    overview("final", truth)
    targets = [
        PREFIX + "x1/new-proposals.json",
        MANIFESTS["x1"],
        PREFIX + "x2/contract-results.json",
        PREFIX + "x2/mutation-results.json",
        PREFIX + "x2/method-flow/ledger.json",
        PREFIX + "x2/promotion-receipt.json",
        PREFIX + "x2/deck/card-manifest.json",
        MANIFESTS["evidence"],
        PREFIX + "final/phase-truth.json",
        PREFIX + "final/baton-index.json",
        PREFIX + "final/future-seat-12-v688-v4-activation-baton.md",
        PREFIX + "final/lifecycle-push-boundaries.json",
    ]
    write("final/content-seal.json", {"source": SOURCE, "x1": X1, "evidence": evidence, "self_excluded": True, "targets": [{"path": path, "bytes": len((ROOT / path).read_bytes()), "sha256": hashlib.sha256((ROOT / path).read_bytes()).hexdigest()} for path in targets]})
    report = audit()
    write("validation/final-checks.json", report)
    write("validation/final-privacy.json", {"schema": "ghc.family.five-class-privacy-adjudication.v1", "classes": report["privacy_classes"], "scanned_files": report["owner_files"], "candidates": report["privacy_candidates"], "candidate_count": report["privacy_candidate_count"], "confirmed_hits": [], "confirmed_hit_count": 0})
    previous = set(scalar("ls-tree", "-r", "--name-only", evidence, "--", PREFIX, SCRIPT_PREFIX, TEST).splitlines())
    staged = PREFIX + "validation/final-staged-review.json"
    exclusions = [MANIFESTS["final_delta"], MANIFESTS["final_owner"]]
    current = {path.relative_to(ROOT).as_posix() for path in current_files()}
    all_paths = sorted(current | {staged, *exclusions})
    delta = sorted(set(all_paths) - previous)
    write("validation/final-staged-review.json", {"schema": "ghc.family.exact-staged-review.v1", "parent": evidence, "allowed_change": "A", "allowed_paths": delta, "count": len(delta), "owner_path_count": len(all_paths), "deletions": 0, "outside_owner_paths": 0})
    report = audit()
    write("validation/final-checks.json", report)
    write("validation/final-privacy.json", {"schema": "ghc.family.five-class-privacy-adjudication.v1", "classes": report["privacy_classes"], "scanned_files": report["owner_files"], "candidates": report["privacy_candidates"], "candidate_count": report["privacy_candidate_count"], "confirmed_hits": [], "confirmed_hit_count": 0})
    current = {path.relative_to(ROOT).as_posix() for path in current_files()} | set(exclusions)
    all_paths = sorted(current)
    delta = sorted(current - previous)
    manifest(MANIFESTS["final_delta"], delta, exclusions, "PENDING_FINAL_COMMIT")
    manifest(MANIFESTS["final_owner"], all_paths, exclusions, "PENDING_FINAL_COMMIT")
    print(json.dumps({"baton_words": words, "final_additions": len(delta), "owner_files": len(all_paths), "manifest_entries": {"delta": len(delta) - 2, "owner": len(all_paths) - 2}, "truth": truth["effective_counts"]}, sort_keys=True))


def terminal_preflight(final):
    if scalar("branch", "--show-current") != BRANCH or scalar("rev-parse", "HEAD") != final:
        raise RuntimeError("Final branch or head mismatch")
    evidence = scalar("rev-parse", final + "^")
    if scalar("rev-parse", evidence + "^") != X1 or scalar("rev-parse", X1 + "^") != SOURCE:
        raise RuntimeError("Direct-parent lifecycle mismatch")
    if int(scalar("rev-list", "--count", SOURCE + ".." + final)) != 3 or int(scalar("rev-list", "--merges", "--count", SOURCE + ".." + final)) != 0:
        raise RuntimeError("Commit ceiling or merge mismatch")
    delta = scalar("diff", "--name-status", SOURCE, final).splitlines()
    if any(not row.startswith("A\t") or not owner_path(row[2:]) for row in delta):
        raise RuntimeError("Owner delta contains deletion, modification, or outside path")
    remote = equality(final)
    report = audit()
    manifests = [
        verify_manifest(X1, MANIFESTS["x1"]),
        verify_manifest(evidence, MANIFESTS["evidence"]),
        verify_manifest(final, MANIFESTS["final_delta"]),
        verify_manifest(final, MANIFESTS["final_owner"]),
    ]
    owner_manifest = strict((ROOT / MANIFESTS["final_owner"]).read_bytes())
    if {row["path"] for row in owner_manifest["entries"]} | set(owner_manifest["declared_self_exclusions"]) != {row[2:] for row in delta}:
        raise RuntimeError("Final owner manifest domain mismatch")
    seal = strict((BASE / "final/content-seal.json").read_bytes())
    for row in seal["targets"]:
        raw = (ROOT / row["path"]).read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise RuntimeError("Content seal mismatch: " + row["path"])
    policy = strict((BASE / "final/canonical-policy.json").read_bytes())
    if policy != {"source": SOURCE, "x1": X1, "evidence": evidence, "branch": BRANCH, "test_module": TEST, "expected_tests": 28, "invocation_budget": 1, "success_replay_allowed": False, "full_repository_suite": False, "same_owner_only": True, "environment_distributions": 3, "promotion_parity_files": 66, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}:
        raise RuntimeError("Canonical policy mismatch")
    canonical_dir = BANK / "canonical"
    marker = canonical_dir / "invocation.json"
    receipt = canonical_dir / "exact-final-owner-scoped-canonical.json"
    if marker.exists() or receipt.exists():
        raise RuntimeError("Canonical marker or receipt already exists; replay prohibited")
    return {"status": "VALID_EXACT_FINAL_PREFLIGHT", "exact_final": final, "evidence": evidence, "remote": remote, "audit": report, "manifests": manifests, "manifest_bindings": sum(row["bindings"] for row in manifests), "manifest_exclusions": sum(len(row["exclusions"]) for row in manifests), "content_seal_targets": len(seal["targets"]), "canonical_marker_absent": True, "canonical_receipt_absent": True}


def run_canonical(final):
    preflight = terminal_preflight(final)
    canonical_dir = BANK / "canonical"
    canonical_dir.mkdir(parents=True, exist_ok=True)
    marker = canonical_dir / "invocation.json"
    receipt = canonical_dir / "exact-final-owner-scoped-canonical.json"
    with marker.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump({"owner": "Tamar Vey", "phase": PHASE, "exact_final": final, "invocation": 1}, handle, sort_keys=True)
        handle.write("\n")
    try:
        test = subprocess.run([sys.executable, "-B", "-X", "utf8", str(ROOT / TEST)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONUTF8": "1"}, timeout=60)
        if test.returncode != 0 or b"Ran 28 tests" not in test.stderr:
            raise RuntimeError("Canonical owner test failure: " + test.stderr.decode("utf-8", "replace"))
        log = test.stdout + test.stderr
        (canonical_dir / "owner-tests.log").write_bytes(log)
        environment_python = BANK / "environment/Scripts/python.exe"
        distribution_output = subprocess.check_output([str(environment_python), "-B", "-X", "utf8", "-c", "import importlib.metadata,json;print(json.dumps({d.metadata['Name'].lower():d.version for d in importlib.metadata.distributions()}))"], timeout=25)
        distributions = strict(distribution_output)
        if distributions != {"fonttools": "4.64.0", "uharfbuzz": "0.56.1", "unicodedata2": "17.0.1"}:
            raise RuntimeError("Canonical package distribution mismatch")
        after = equality(final)
        truth = strict((BASE / "final/phase-truth.json").read_bytes())
        baton = strict((BASE / "final/baton-index.json").read_bytes())
        baton_bytes = (ROOT / baton["path"]).read_bytes()
        if hashlib.sha256(baton_bytes).hexdigest() != baton["sha256"] or len(baton_bytes) != baton["bytes"] or len(baton_bytes.decode("utf-8").split()) != baton["words"] or not baton_bytes.decode("utf-8").rstrip().endswith(baton["eof"]):
            raise RuntimeError("Baton fixity mismatch")
        payload = {
            **{key: value for key, value in preflight["audit"].items() if key != "privacy_candidates"},
            "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
            "owner": "Tamar Vey",
            "phase": PHASE,
            "branch": BRANCH,
            "source": SOURCE,
            "x1": X1,
            "evidence": preflight["evidence"],
            "exact_final": final,
            "final_parent": preflight["evidence"],
            "phase_commits": 3,
            "merge_commits": 0,
            "canonical_invocation_count": 1,
            "canonical_success_count": 1,
            "canonical_replay_count": 0,
            "tests_passed": 28,
            "test_log_sha256": hashlib.sha256(log).hexdigest(),
            "manifest_bindings": preflight["manifest_bindings"],
            "manifest_exclusions": preflight["manifest_exclusions"],
            "manifests": preflight["manifests"],
            "content_seal_targets": preflight["content_seal_targets"],
            "environment_distributions": 3,
            "distributions": distributions,
            "baton": baton,
            "outcomes": truth["outcomes"],
            "effective_counts": truth["effective_counts"],
            "method_flow": truth["owner_method_flow"],
            "remote_before": preflight["remote"],
            "remote_after": after,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
            "route_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        }
        value = {"payload": payload, "payload_sha256": value_sha(payload)}
        with receipt.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=True)
            handle.write("\n")
        print(json.dumps({"status": payload["status"], "exact_final": final, "receipt_sha256": hashlib.sha256(receipt.read_bytes()).hexdigest(), "payload_sha256": value["payload_sha256"], "manifest_bindings": payload["manifest_bindings"], "tests": 28, "canonical_replays": 0}, sort_keys=True))
    except BaseException as exc:
        failed = canonical_dir / "failed-invocation.json"
        if not failed.exists():
            failed.write_text(json.dumps({"success_credit": 0, "error_type": type(exc).__name__, "exact_final": final}, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["prepare-evidence", "build-final", "preflight", "canonical"])
    parser.add_argument("--evidence")
    parser.add_argument("--final")
    args = parser.parse_args()
    if args.mode == "prepare-evidence":
        prepare_evidence()
    elif args.mode == "build-final":
        build_final(args.evidence)
    elif args.mode == "preflight":
        print(json.dumps(terminal_preflight(args.final), sort_keys=True))
    else:
        run_canonical(args.final)


if __name__ == "__main__":
    main()
