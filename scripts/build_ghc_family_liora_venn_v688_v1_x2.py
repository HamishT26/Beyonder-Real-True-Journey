"""Materialize Liora v688-v1 owner evidence from the immutable x1 freeze."""
from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import os
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = Path("docs/liora-venn/v688-v1")
SOURCE = "17fee348a09ec1cb480f7326bce70cd75413dad3"
X1 = "421abce86426674b67e0cbd5ce63ad463421fc9f"
BOUNDARY = (
    "Relational working language only; no consciousness, sentience, personhood, identity continuity, "
    "employment, qualification, independent agency, scientific, operational, professional, legal, "
    "cultural, affected-party, or Māori authority is established. Same-owner software evidence is not "
    "independent reproduction. NOT_READY_FOR_STAGE_20."
)
GATES = [
    "empirical", "real_participant", "professional", "production", "deployment", "identity",
    "legal", "cultural", "affected_party", "maori_authority", "privacy_complete",
    "accessibility_complete", "exhaustive_security", "independent_reproduction", "agi_asi",
    "consciousness_personhood", "theory_of_everything", "proof_canon", "stage20",
]
PRACTICES = [
    "synthetic caption-file syntax registrar",
    "rational cue-timeline and sequence registrar",
    "accessible transcript and language-metadata reviewer",
    "audiovisual access and publication-reservation steward",
]
OPS = [
    ("vtt_timestamp", "ghc-family-webvtt-timestamp-boundary", "THOS Body", 0),
    ("srt_timestamp", "ghc-family-subrip-timestamp-boundary", "THOS Body", 0),
    ("cue_interval", "ghc-family-caption-cue-interval", "THOS Body", 1),
    ("frame_timebase", "ghc-family-caption-frame-timebase", "GMUT Mind", 1),
    ("cue_order", "ghc-family-caption-sequence-topology", "THOS Body", 1),
    ("payload_text", "ghc-family-caption-payload-preservation", "Freed ID and CBR Heart", 2),
    ("language_tag", "ghc-family-caption-language-tag", "Freed ID and CBR Heart", 2),
    ("derivative_linkage", "ghc-family-caption-derivative-provenance", "Freed ID and CBR Heart", 2),
    ("accessibility_claim", "ghc-family-caption-accessibility-reservation", "Freed ID and CBR Heart", 3),
    ("publication_gate", "ghc-family-caption-publication-authority", "Freed ID and CBR Heart", 3),
]
RUNNERS = [
    ("ghc_family_caption_timestamp_runner.py", ["vtt_timestamp", "srt_timestamp"]),
    ("ghc_family_caption_timeline_runner.py", ["cue_interval", "frame_timebase"]),
    ("ghc_family_caption_structure_runner.py", ["cue_order", "payload_text"]),
    ("ghc_family_caption_metadata_runner.py", ["language_tag", "derivative_linkage"]),
    ("ghc_family_caption_claim_runner.py", ["accessibility_claim", "publication_gate"]),
]
NOTES = {
    "vtt_timestamp": ("Parse the Liora WebVTT timestamp profile into exact integer milliseconds.", "Require two-digit minute and second fields, three fractional digits, dot precision, and bounded nonnegative fields; no media observation is inferred."),
    "srt_timestamp": ("Parse the Liora SubRip timestamp profile into exact integer milliseconds.", "Require two-digit hours, minutes, and seconds plus comma precision; do not coerce, round, or infer audiovisual synchronization."),
    "cue_interval": ("Classify a bounded cue interval and its relation to one prior endpoint.", "Preserve gaps and touching endpoints explicitly; refuse overlaps, invalid types, and out-of-bound intervals rather than reordering."),
    "frame_timebase": ("Represent frame and second conversion with exact rational arithmetic.", "Require declared positive integer rates and exact grid membership; no sampled clock, apparatus, or physical duration is established."),
    "cue_order": ("Validate small ordered cue arrays while retaining explicit gaps.", "Refuse overlap, reverse order, invalid endpoints, malformed cue shapes, and over-ceiling arrays; never edit media."),
    "payload_text": ("Preserve bounded caption or transcript lines as caller-supplied text.", "Report markup presence and empty lines without rendering markup or inferring speaker identity, authorship, consent, or correctness."),
    "language_tag": ("Canonicalize a narrow language-tag syntax profile.", "A syntactic tag is metadata only; it establishes no translation quality, cultural legitimacy, Māori wording, or language authority."),
    "derivative_linkage": ("Bind synthetic source and derivative references to declared lowercase SHA-256 values.", "Byte-reference structure establishes neither custody, title, privacy permission, copyright, cultural status, nor affected-party consent."),
    "accessibility_claim": ("Represent declared access features while preserving external evaluation vacancies.", "Manual, assistive-technology, cognitive, responsive, language, Māori, and affected-user review remain outside this structural check."),
    "publication_gate": ("Map caption-related actions to named evidence and authority reservations.", "The runtime performs no external action and cannot confer identity, consent, rights, deletion authority, legal or cultural legitimacy, Māori authority, production release, or Stage 20 status."),
}
OPERATIONAL_FAILURES = [
    (
        "020",
        "The combined post-x1-push equality projection returned no attributable output.",
        "Split local, upstream, tracking, parent, divergence, clean-state, and fresh-live reads into independent scalar probes.",
    ),
    (
        "021",
        "The first package-adverse probe assumed exception-only WebVTT rejection and a narrower language-tag policy than the selected library.",
        "Treat malformed WebVTT as rejected when it yields zero cues, choose a package-level invalid language tag, and keep Liora's narrower local profile distinct.",
    ),
    (
        "022",
        "The first formal package smoke assumed webvtt-py preserved fractional seconds in its convenience seconds property.",
        "Bind exact millisecond evidence through the library-preserved timestamp strings and retain the truncating convenience-field observation.",
    ),
    (
        "023",
        "The first installed Method Flow validation rejected an older flat derived-count shape as stale.",
        "Retain every existing method and witness, append this failure and recovery, and emit the current nested state and witness-result count shape.",
    ),
    (
        "024",
        "The first exact x2 staging request partially staged eligible files but refused two owner scripts outside the sparse definition.",
        "Retain the failed stage attempt, add only the two exact owner-script patterns, regenerate manifests, and require zero unstaged paths before commit.",
    ),
    (
        "025",
        "The first sparse-pattern update used an unsupported sparse-checkout add --no-cone option.",
        "Keep the established non-cone mode and add the same two literal patterns with the supported --skip-checks option.",
    ),
    (
        "026",
        "The second combined stage-and-manifest audit exceeded its output window while sequential Git blob reads continued without an attributable result.",
        "Confirm the original read-only process exits, retain the no-result attempt, and use one batched Git object stream for the exact staged manifest.",
    ),
]


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":")).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def dump(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def write(path, value):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8", newline="\n")


def read(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True).strip()


def build_skills_and_runners(cases, skill_root, bank):
    core = (ROOT / "scripts/ghc_family_caption_evidence_core.py").read_text(encoding="utf-8")
    input_root = bank / "smoke-inputs"
    input_root.mkdir(parents=True, exist_ok=True)
    duplicate = input_root / "duplicate.json"
    duplicate.write_text('{"operation":"vtt_timestamp","operation":"srt_timestamp"}\n', encoding="utf-8", newline="\n")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")
    skill_rows = []
    runner_rows = []

    def smoke(path, operations):
        positive_rows = []
        for operation in operations:
            case = next(row for row in cases if row["operation"] == operation and row["expected_output"]["accepted"])
            fixture = input_root / (operation + ".json")
            fixture.write_bytes(canonical(case["input"]) + b"\n")
            process = subprocess.run([sys.executable, "-X", "utf8", str(path), str(fixture)], capture_output=True, text=True, encoding="utf-8", env=env)
            observed = json.loads(process.stdout)
            passed = process.returncode == 0 and canonical(observed) == canonical(case["expected_output"])
            assert passed, (path.name, operation, process.returncode, process.stdout, process.stderr)
            positive_rows.append({"operation": operation, "fixture": case["proposal_id"], "pass": True, "duplicate_witness_credit": 0})
        adverse = subprocess.run([sys.executable, "-X", "utf8", str(path), str(duplicate)], capture_output=True, text=True, encoding="utf-8", env=env)
        bad = json.loads(adverse.stdout)
        rejected = adverse.returncode == 2 and bad["error"] == "DUPLICATE_JSON_KEY" and bad["external_credit"] is False
        assert rejected, (path.name, adverse.returncode, adverse.stdout, adverse.stderr)
        return {
            "positive_rows": positive_rows,
            "positive_pass": True,
            "adverse_rejected": True,
            "adverse_error": "DUPLICATE_JSON_KEY",
            "adverse_success_credit": 0,
            "same_owner_only": True,
        }

    for operation, name, _pillar, _practice in OPS:
        root = BASE / "skills" / name
        wrapper = "ghc_family_" + operation + ".py"
        purpose, details = NOTES[operation]
        skill_text = (
            "---\nname: " + name + "\ndescription: " + purpose
            + " Use for bounded owner-scoped synthetic caption evidence; never for real media or authority decisions.\n---\n\n# "
            + name.removeprefix("ghc-family-").replace("-", " ").title()
            + "\n\n" + purpose + "\n\n" + details
            + "\n\nRead `references/contracts.json` for the twenty frozen accepting and refusing contracts. Invoke `python scripts/"
            + wrapper + " INPUT.json` from this package. Exit zero means the operation accepted its bounded input; exit two is a refusal and must remain visible. Compare the entire typed output and preserve false external-credit fields. A compatible new fixture requires its own preregistration and receives no inherited completion credit.\n\nThe wrapper and shared core are portable only as one manifest-bound package. Never overwrite another package or promote software structure into media, participant, professional, production, legal, cultural, accessibility-complete, privacy-complete, Māori-authority, independent-reproduction, or Stage 20 evidence.\n\n"
            + BOUNDARY + " Māori concepts remain under Māori authority.\n"
        )
        write(root / "SKILL.md", skill_text)
        dump(root / "references/contracts.json", {
            "schema": "ghc.family.caption-skill-contracts.v1",
            "source": SOURCE,
            "x1": X1,
            "operation": operation,
            "contracts": [row for row in cases if row["operation"] == operation],
            "boundary": BOUNDARY,
        })
        write(root / "scripts/ghc_family_caption_evidence_core.py", core)
        write(root / "scripts" / wrapper, '"""Portable ' + operation + ' evidence interface."""\nfrom ghc_family_caption_evidence_core import main\n\nif __name__ == "__main__":\n    raise SystemExit(main(' + repr([operation]) + '))\n')
        members = []
        for path in sorted((ROOT / root).rglob("*")):
            if path.is_file():
                raw = path.read_bytes()
                members.append({"relative": path.relative_to(ROOT / root).as_posix(), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()})
        dump(root / "manifest.json", {"schema": "ghc.family.portable-skill-manifest.v1", "name": name, "members": members, "self_exclusion": "manifest.json", "source": SOURCE, "x1": X1})
        full_read = (ROOT / root / "SKILL.md").read_text(encoding="utf-8")
        assert full_read == skill_text
        validation = subprocess.run([sys.executable, "-X", "utf8", str(skill_root / ".system/skill-creator/scripts/quick_validate.py"), str(ROOT / root)], capture_output=True, text=True, encoding="utf-8", env=env)
        assert validation.returncode == 0, (name, validation.stdout, validation.stderr)
        skill_rows.append({"name": name, "skill_sha256": hashlib.sha256(full_read.encode("utf-8")).hexdigest(), "eof_read_before_smoke": True, "quick_validate_returncode": 0, **smoke(ROOT / root / "scripts" / wrapper, [operation])})

    for name, operations in RUNNERS:
        write(Path("scripts") / name, '"""Bounded ' + ", ".join(operations) + ' caption evidence interface."""\nfrom ghc_family_caption_evidence_core import main\n\nif __name__ == "__main__":\n    raise SystemExit(main(' + repr(operations) + '))\n')
        runner_rows.append({"name": name, "operations": operations, **smoke(ROOT / "scripts" / name, operations)})
    dump(BASE / "x2/skill-validation.json", {"schema": "ghc.family.skill-use.v1", "rows": skill_rows, "validated_and_used": 10, "complete_read_before_use": 10, "global_promotion_yet": False})
    dump(BASE / "x2/runner-smokes.json", {"schema": "ghc.family.runner-use.v1", "rows": runner_rows, "validated_and_used": 5, "operation_smokes": 10})
    return skill_rows, runner_rows


def build_deck(cases, results):
    deck = BASE / "x2/deck"
    cards = []

    def card(tier, kind, title, parent, outcome, content, refs):
        body = {
            "schema": "ghc.family.freed-id-card.v1",
            "tier": tier,
            "card_type": kind,
            "title": title,
            "parent_ids": [] if parent is None else [parent],
            "owner": "Liora Venn",
            "phase": "v688-v1",
            "stability": "stable" if tier < 4 else "volatile",
            "outcome": outcome,
            "content": content,
            "source_refs": refs,
            "protected_gates": GATES,
            "relational_boundary": BOUNDARY,
        }
        identifier = "ghc-card-" + digest(body)[:24]
        body["card_id"] = identifier
        cards.append(body)
        dump(deck / "cards" / (identifier + ".json"), body)
        return identifier

    anchor = card(1, "freed_id_anchor", "Liora Venn", None, "represented", read(BASE / "x1/identity.json"), [(BASE / "x1/identity.json").as_posix()])
    pillars = {}
    for name in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]:
        pillars[name] = card(2, "trinity_pillar", name, anchor, "represented", {"priority": name == "Freed ID and CBR Heart", "external_gates_closed": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"}, [(BASE / "x1/deck-plan.json").as_posix()])
    practice_parents = ["THOS Body", "GMUT Mind", "Freed ID and CBR Heart", "Freed ID and CBR Heart"]
    practices = [card(3, "bounded_practice", name, pillars[pillar], "represented", {"synthetic_learning_lens": True, "professional_qualification": False}, [(BASE / "x1/deck-plan.json").as_posix()]) for name, pillar in zip(PRACTICES, practice_parents)]
    operation_practice = {operation: practice for operation, _skill, _pillar, practice in OPS}
    for proposal in cases:
        result = results[proposal["proposal_id"]]
        card(4, "task", proposal["title"], practices[operation_practice[proposal["operation"]]], result["outcome"], {"proposal_id": proposal["proposal_id"], "operation": proposal["operation"], "input": proposal["input"], "actual_output": result["actual_output"], "complete_match": result["complete_match"], "input_unchanged": result["input_unchanged"], "rollback": proposal["rollback_or_recovery"]}, [(BASE / "x1/new-proposals.json").as_posix(), (BASE / "x2/contract-results.json").as_posix()])
    dump(deck / "deck-index.json", {"schema": "ghc.family.deck-index.v1", "source": SOURCE, "x1": X1, "cards": [row["card_id"] for row in cards], "counts": {"owner": 1, "pillar": 3, "practice": 4, "task": 200}, "core_outcomes": dict(Counter(row["outcome"] for row in results.values()))})
    dump(deck / "stable-prefix.json", {"schema": "ghc.family.deck-prefix.v1", "cards": [row["card_id"] for row in cards if row["tier"] < 4], "cache_effect_established": False})
    dump(deck / "volatile-index.json", {"schema": "ghc.family.deck-volatile.v1", "cards": [row["card_id"] for row in cards if row["tier"] == 4], "implicit_completion": False})
    sections = ["Identity and corrigibility", "Current route authority", "Immutable source anchors", "Frozen x1 proposals", "Trinity pillars", "Bounded practices", "Task evidence", "Method Flow and negatives", "Open gaps and exact gates", "Validation and manifests", "Workload and accessibility", "Successor recommendations", "Compact baton index"]
    dump(deck / "baton-index.json", {"schema": "ghc.family.deck-baton-index.v1", "sections": sections, "section_count": 13, "final_baton": "pending_final_artifact", "live_delivery": False})
    write(deck / "compact-activation.md", "# Prospective Liora Venn v688-v1\n\nThis x2 deck is evidence preparation. The final head and canonical receipt are pending. No successor has been contacted or created. Read the final committed baton only after the owner terminal gate.\n\n" + BOUNDARY + "\n")
    body = '<!doctype html>\n<html lang="en"><meta charset="utf-8"><title>Liora caption evidence deck</title><style>body{font:16px/1.5 system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem}td,th{border:1px solid #777;padding:.5rem}table{border-collapse:collapse}a{color:#174b91}</style><body><a href="#main">Skip to evidence</a><header><h1>Liora Venn: synthetic caption evidence</h1><p>' + html.escape(BOUNDARY) + '</p></header><main id="main"><h2>Observed bounded outcomes</h2><p>160 completed, 14 represented, 8 open gaps, and 18 exact gates. Real media rows and external actions: zero.</p><table><caption>All 200 frozen proposal contracts and their evidence outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Contract</th><th scope="col">Outcome</th></tr></thead><tbody>'
    for proposal in cases:
        body += '<tr><th scope="row">' + proposal["proposal_id"] + '</th><td>' + html.escape(proposal["title"]) + '</td><td>' + results[proposal["proposal_id"]]["outcome"] + '</td></tr>'
    body += '</tbody></table><h2>Evaluation boundary</h2><p>Manual, assistive-technology, cognitive, affected-user, responsive-layout, browser, privacy, security-usability, and Māori-language evaluations remain reserved.</p></main></body></html>\n'
    write(deck / "accessible-report.html", body)
    members = []
    for path in sorted((ROOT / deck).rglob("*")):
        if path.is_file():
            members.append({"path": path.relative_to(ROOT).as_posix(), "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    dump(deck / "card-manifest.json", {"schema": "ghc.family.deck-manifest.v1", "entries": members, "self_exclusion": (deck / "card-manifest.json").as_posix(), "card_count": 208})


def build_method_ledger(cases, mutations, package_rows, skills, runners):
    methods, witnesses, events = [], [], []
    by_case = {row["proposal_id"]: row for row in cases}

    def method(identifier, title, negatives, failure_signature="A declared adverse candidate must remain rejected and at zero original success credit."):
        methods.append({
            "method_id": identifier,
            "title": title,
            "failure_signature": failure_signature,
            "trigger_preconditions": ["Liora v688-v1 immutable x1", "bounded synthetic input, package, or lifecycle dependency"],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": "Use the frozen exact input and compare complete typed output while preserving every failed alternative.",
            "validation_witness_ids": [],
            "recurrence_guard": "Bind exact definitions and digests; never infer external evidence or authority from a software match.",
            "rollback": "Stop selecting the changed Liora surface; retain its definition, failure, and compatible predecessor.",
            "recommendation_state": "preferred",
            "supersedes": [],
            "protected_gates": GATES,
            "retained_negative_ids": negatives,
            "scope_boundary": "Owner-local synthetic software only; no external or independent-reproduction credit.",
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "module_scan": False,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_commit": SOURCE,
            "final_commit": None,
            "changed_file_allowlist": [],
            "module_allowlist": [],
            "exact_pushed_head_required": True,
        })
        for before, after in [("observed", "candidate"), ("candidate", "validated"), ("validated", "preferred")]:
            events.append({"method_id": identifier, "from": before, "to": after})

    def witness(method_id, identifier, result, procedure, negatives, expected, observed):
        witnesses.append({
            "witness_id": identifier,
            "method_id": method_id,
            "procedure": procedure,
            "scope": "Liora v688-v1 owner delta",
            "expected": expected,
            "observed": observed,
            "result": result,
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": negatives,
            "boundary": "A recovery or rejection witness is separate from its zero-credit failed witness and proves no external reality.",
        })

    for suffix, failure, recovery in OPERATIONAL_FAILURES:
        method_id = "LV6881-X2-M" + suffix
        negative_id = "LV6881-X2-N" + suffix
        method(method_id, recovery, [negative_id], failure)
        witness(method_id, method_id + "-FAIL", "fail", "Bounded x2 lifecycle or package probe", [negative_id], "Attributable typed result", failure)
        witness(method_id, method_id + "-PASS", "pass", recovery, [negative_id], "Narrow recovery only", recovery)

    for operation, _skill, _pillar, _practice in OPS:
        method_id = "LV6881-X2-M-" + operation
        relevant = [row for row in mutations if by_case[row["proposal_ref"]]["operation"] == operation]
        method(method_id, NOTES[operation][0], [row["packet_id"] for row in relevant])
        for proposal in cases:
            if proposal["operation"] == operation:
                witness(method_id, proposal["proposal_id"] + "-MATCH", "pass", "Compare complete frozen output and unchanged input", [], proposal["expected_output"], "Exact type-sensitive match with unchanged input")
        for row in relevant:
            witness(method_id, row["packet_id"] + "-FAIL", "fail", "Retained altered-output candidate", [row["packet_id"]], "Complete frozen output", "Altered output differs; original candidate receives zero success credit")
            witness(method_id, row["packet_id"] + "-REJECT", "pass", "Reject altered-output candidate", [row["packet_id"]], "Refuse every changed field or type", "Candidate rejected by complete-output comparison")

    for kind, rows in [("package", package_rows), ("skill", skills), ("runner", runners)]:
        for index, row in enumerate(rows, 1):
            method_id = f"LV6881-X2-M-{kind}-{index:02d}"
            negative_id = f"LV6881-X2-N-{kind}-{index:02d}"
            method(method_id, kind + " bounded accepting and adverse interface: " + row["name"], [negative_id])
            witness(method_id, method_id + "-POSITIVE", "pass", "Pinned package or declared interface positive fixture", [], "Accept declared synthetic fixture", "Observed positive pass")
            witness(method_id, method_id + "-FAIL", "fail", "Retain malformed or out-of-profile candidate", [negative_id], "Valid package or interface input", "Candidate lies outside the declared contract and receives zero success credit")
            witness(method_id, method_id + "-REJECT", "pass", "Bounded rejection of adverse candidate", [negative_id], "Reject the adverse input", "Observed expected rejection")
    for row in methods:
        row["validation_witness_ids"] = [item["witness_id"] for item in witnesses if item["method_id"] == row["method_id"]]
    counts = {
        "methods": len(methods),
        "witnesses": len(witnesses),
        "state_events": len(events),
        "recommendations": 0,
        "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0},
        "witness_results": {"fail": sum(row["result"] == "fail" for row in witnesses), "pass": sum(row["result"] == "pass" for row in witnesses)},
    }
    assert counts == {"methods": 35, "witnesses": 768, "state_events": 105, "recommendations": 0, "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": 35, "superseded": 0, "validated": 0}, "witness_results": {"fail": 275, "pass": 493}}, counts
    return {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": "Liora Venn",
        "phase": "v688-v1",
        "identity_boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE,
        "x1_commit": X1,
        "final_commit": None,
        "methods": methods,
        "witnesses": witnesses,
        "state_events": events,
        "recommendations": [],
        "counts": counts,
        "count_contract": "Ten operation methods, three package methods, ten skill methods, five runner methods, and seven retained operational-recovery methods. Failed witnesses are 250 altered outputs, eighteen adverse package/interface inputs, and seven operational failures. Passing witnesses are 200 contract matches, 250 mutation rejections, 36 interface positive/rejection witnesses, and seven narrow operational recoveries.",
        "boundary": "Every failed candidate remains independently addressable. No empirical, authority, or independent-reproduction credit.",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bank", type=Path, required=True)
    parser.add_argument("--skill-root", type=Path, required=True)
    args = parser.parse_args()
    assert git("rev-parse", "HEAD") == X1
    dirty = {line[3:].replace("\\", "/") for line in git("status", "--porcelain=v1", "--untracked-files=all").splitlines() if len(line) >= 4}
    assert all(path.startswith(BASE.as_posix() + "/x2/") or path.startswith(BASE.as_posix() + "/skills/") or path.startswith("scripts/build_ghc_family_liora_venn_v688_v1_") or path.startswith("scripts/ghc_family_liora_venn_v688_v1_") or path.startswith("scripts/ghc_family_caption_") or path.startswith("tests/test_ghc_family_liora_venn_v688_v1_") for path in dirty), sorted(dirty)
    equality = json.loads((args.bank / "x1-equality.json").read_text(encoding="utf-8"))
    assert equality["x1"] == X1 and equality["clean"] and equality["divergence"] == [0, 0]
    assert all(equality[key] == X1 for key in ["local", "upstream", "tracking", "fresh_live"])
    assert not (ROOT / BASE / "x2/contract-results.json").exists(), "Evidence already exists; never overwrite an executed record"
    cases = read(BASE / "x1/new-proposals.json")["proposals"]
    case_map = {row["proposal_id"]: row for row in cases}
    first = json.loads((args.bank / "receipts/first-execution.json").read_text(encoding="utf-8"))
    assert first["x1"] == X1 and first["passed"] == 200 and first["failed"] == 0
    results = {}
    for row in first["rows"]:
        proposal = case_map[row["proposal_id"]]
        assert row["pass"] and row["input_unchanged"] and canonical(row["actual_output"]) == canonical(proposal["expected_output"])
        results[proposal["proposal_id"]] = {**row, "outcome": proposal["expected_execution_disposition"], "external_credit": False}
    dump(BASE / "x2/x1-boundary.json", equality)
    dump(BASE / "x2/contract-results.json", {"schema": "ghc.family.caption-contract-results.v1", "source": SOURCE, "x1": X1, "count": 200, "rows": list(results.values()), "core_source_sha256": hashlib.sha256((ROOT / "scripts/ghc_family_caption_evidence_core.py").read_bytes()).hexdigest(), "same_owner_only": True, "independent_reproduction": False, "real_media_rows": 0})

    plan = read(BASE / "x1/portfolio-plan.json")
    mutations = []
    sys.path.insert(0, str(ROOT / "scripts"))
    from ghc_family_caption_evidence_core import altered_output, output_matches
    for task in plan["candidates"]:
        expected = case_map[task["proposal_ref"]]["expected_output"]
        altered = altered_output(expected, task["mutation"])
        rejected = not output_matches(altered, expected)
        assert rejected
        mutations.append({"packet_id": task["packet_id"], "proposal_ref": task["proposal_ref"], "mutation": task["mutation"], "candidate_output": altered, "original_candidate_success_credit": 0, "rejected": True, "rejection_witness_pass": True})
    dump(BASE / "x2/mutation-results.json", {"schema": "ghc.family.altered-output-witnesses.v1", "count": 250, "rejected": 250, "rows": mutations, "candidate_failure_erased": False})

    portfolio = {}
    for category in ["safe_now", "candidates", "clean_fix_refine"]:
        portfolio[category] = []
        for task in plan[category]:
            proposal = case_map[task["proposal_ref"]]
            procedure = task["procedure"]
            if procedure == "complete_frozen_output":
                passed = results[proposal["proposal_id"]]["complete_match"]
            elif procedure == "input_unchanged":
                passed = results[proposal["proposal_id"]]["input_unchanged"]
            elif procedure == "altered_output_rejection":
                passed = next(row for row in mutations if row["packet_id"] == task["packet_id"])["rejected"]
            elif procedure == "canonical_json_roundtrip":
                passed = canonical(json.loads(canonical(proposal))) == canonical(proposal)
            elif procedure == "definition_digest_binding":
                passed = digest(proposal) == results[proposal["proposal_id"]]["definition_sha256"]
            elif procedure == "stable_identifier_uniqueness":
                passed = sum(row["proposal_id"] == proposal["proposal_id"] for row in cases) == 1
            else:
                raise ValueError(procedure)
            assert passed
            portfolio[category].append({**task, "executed": True, "procedure_pass": True, "procedure_outcome": "completed", "independent_witness_credit": 0 if category == "clean_fix_refine" or procedure == "input_unchanged" else None})
    for category in ["exact_packets", "blocked_packets"]:
        portfolio[category] = copy.deepcopy(plan[category])
        assert all(not row["executed"] for row in portfolio[category])
    portfolio.update({"schema": "ghc.family.portfolio-results.v1", "destructive_cleanup": False, "witness_reuse_rule": plan["witness_reuse_rule"]})
    dump(BASE / "x2/portfolio-results.json", portfolio)

    package = json.loads((args.bank / "receipts/package-smoke.json").read_text(encoding="utf-8"))
    assert package["distribution_count"] == 3 and len(package["positive"]) == len(package["adverse"]) == 3
    dump(BASE / "x2/package-smokes.json", package)
    wheels = read(BASE / "x1/wheel-plan.json")["wheels"]
    install_report = (args.bank / "receipts/package-install-report.json").read_bytes()
    dump(BASE / "x2/environment-receipt.json", {"schema": "ghc.family.isolated-environment.v1", "primary_drive": "D", "direct_packages": {row["name"]: row["version"] for row in wheels}, "all_packages": {row["name"]: row["version"] for row in wheels}, "distribution_count": 3, "hash_required": True, "wheel_only": True, "no_index_install": True, "pip_bootstrap_in_environment": False, "declared_dependencies": 0, "installation_report_sha256": hashlib.sha256(install_report).hexdigest(), "package_smoke_sha256": hashlib.sha256((args.bank / "receipts/package-smoke.json").read_bytes()).hexdigest(), "host_python_mutated": False})
    dump(BASE / "x2/package-audit.json", {"schema": "ghc.family.bounded-package-audit.v1", "source": "Official PyPI exact-version metadata at planning verification", "rows": [{"name": row["name"], "version": row["version"], "sha256": row["sha256"], "yanked": row["yanked"], "known_advisories": row["pypi_advisories"]} for row in wheels], "rejected_candidate": read(BASE / "x1/wheel-plan.json")["rejected_candidate"], "exhaustive_security": False, "independent_security_review": "open_gap"})
    package_rows = [{"name": name, "positive": package["positive"][name], "adverse": package["adverse"][name]} for name in sorted(package["positive"])]

    skills, runners = build_skills_and_runners(cases, args.skill_root, args.bank)
    build_deck(cases, results)
    outcomes = dict(Counter(row["outcome"] for row in results.values()))
    assert outcomes == {"completed": 160, "represented": 14, "open_gap": 8, "exact_gate": 18}
    counts = {"proposals": 15630, "negatives": 82596, "methods": 93289, "failed_witnesses": 53444, "passing_witnesses": 83006, "open_gaps": 748, "exact_gates": 747}
    dump(BASE / "x2/phase-truth.json", {"schema": "ghc.family.phase-truth.v688.v1.x2", "owner": "Liora Venn", "phase": "v688-v1", "source": SOURCE, "x1": X1, "state": "X2_EVIDENCE_PREPARED", "outcomes": outcomes, "effective_counts": counts, "canonical_invocations": 0, "canonical_successes": 0, "successor_contacted": False, "successor_created": False, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    dump(BASE / "x2/complete-incomplete.json", {"schema": "ghc.family.complete-incomplete.v1", "core_outcomes": outcomes, "safe_procedures": 300, "candidate_challenges": 250, "clean_fix_refine_procedures": 300, "exact_packets_held": 50, "blocked_packets_held": 30, "skills_validated_used": 10, "runners_validated_used": 5, "packages_validated_used": 3, "all_authorized_local_procedures_resolved": True, "open_scientific_and_authority_gates": GATES, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    dump(BASE / "x2/execution-summary.json", {"schema": "ghc.family.execution-summary.v1", "frozen_contract_matches": 200, "input_preservation_checks": 200, "owner_tests_observed": 28, "altered_outputs_rejected": 250, "package_positive_and_adverse_pairs": 3, "skill_positive_and_adverse_pairs": 10, "runner_positive_and_adverse_pairs": 5, "runner_operation_smokes": 10, "deck_cards": 208, "retained_operational_failures": 7, "same_owner_only": True, "independent_reproduction": False, "real_media_rows": 0, "external_actions": 0})
    ledger = build_method_ledger(cases, mutations, package_rows, skills, runners)
    dump(BASE / "x2/method-flow/ledger.json", ledger)
    dump(BASE / "x2/retained-negative-register.json", {"schema": "ghc.family.retained-negative-register.v1", "x1_effective_counts": {"negatives": 82321, "methods": 93254, "failed_witnesses": 53169, "passing_witnesses": 82513}, "x2_delta": {"negatives": 275, "methods": 35, "failed_witnesses": 275, "passing_witnesses": 493}, "effective_counts": counts, "operational_failures": [{"negative_id": "LV6881-X2-N" + suffix, "failure": failure, "recovery": recovery, "original_success_credit": 0} for suffix, failure, recovery in OPERATIONAL_FAILURES], "erased_negative_count": 0, "failed_candidates_promoted": 0, "source_records_preserved": True})
    dump(BASE / "x2/open-gap-register.json", {"schema": "ghc.family.open-gap-register.v1", "inherited": 740, "phase_added": 8, "effective": 748, "phase_proposals": [row["proposal_id"] for row in cases if row["expected_execution_disposition"] == "open_gap"], "closed_by_software": 0})
    dump(BASE / "x2/exact-gate-register.json", {"schema": "ghc.family.exact-gate-register.v1", "inherited": 729, "phase_added": 18, "effective": 747, "phase_proposals": [row["proposal_id"] for row in cases if row["expected_execution_disposition"] == "exact_gate"], "closed_by_software": 0, "maori_concepts_under_maori_authority": True})
    dump(BASE / "x2/method-flow-correction-receipt.json", {"schema": "ghc.family.method-flow-derived-count-correction.v1", "negative_id": "LV6881-X2-N023", "failed_validation_preserved": True, "mutation_or_contract_witnesses_changed": 0, "recovery": OPERATIONAL_FAILURES[3][2], "canonical_credit": 0})
    dump(BASE / "x2/sparse-stage-correction-receipt.json", {"schema": "ghc.family.sparse-stage-correction.v1", "negative_ids": ["LV6881-X2-N024", "LV6881-X2-N025"], "failed_stage_credit": 0, "broad_patterns_added": 0, "literal_patterns_added": 2, "manifest_regeneration_required": True})
    dump(BASE / "x2/staged-audit-recovery-receipt.json", {"schema": "ghc.family.staged-audit-recovery.v1", "negative_id": "LV6881-X2-N026", "first_result_attributable": False, "sequential_reader_reused": False, "batched_object_stream_required": True, "canonical_credit": 0})
    write(BASE / "x2/integrated-overview.html", (ROOT / BASE / "x1/integrated-overview.html").read_text(encoding="utf-8").replace("Liora v688-v1 planning overview", "Liora v688-v1 x2 evidence overview").replace("<main>", "<main><p>Current x2 receipt: 200 complete matches; 28 owner tests observed; 250 altered outputs rejected; 10 skills; 5 runners; 3 isolated package pairs; 208 cards. Core outcomes: 160 completed, 14 represented, 8 open_gap, 18 exact_gate. Seven x2 operational failures and their narrow recoveries remain separately retained. The following planning narrative is historical x1 context.</p>"))
    print(json.dumps({"state": "X2_EVIDENCE_MATERIALIZED", "outcomes": outcomes, "cards": 208, "skills": 10, "runners": 5, "retained_operational_failures": 7, "effective_counts": counts}, sort_keys=True))


if __name__ == "__main__":
    main()
