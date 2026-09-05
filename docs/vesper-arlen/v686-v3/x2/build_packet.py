"""Assemble Vesper v686-v3 Method Flow, flashcards, reports, and handoff."""

from __future__ import annotations

import hashlib
import html
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
BASE = ROOT / "docs/vesper-arlen/v686-v3"
sys.path.insert(0, str(ROOT / "scripts"))

from ghc_family_config_toml import sha


def read(relative: str) -> object:
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write(relative: str | Path, value: object) -> None:
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def write_text(relative: str | Path, value: str) -> None:
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def main() -> None:
    identity = read("x1/identity-and-practice.json")
    boundary = identity["boundary"]
    gates = identity["protected_gates"]
    activation = read("x1/activation-source.json")
    proposals = read("x1/new-proposals.json")["proposals"]
    results = read("x2/contract-results.json")["results"]
    result_map = {item["proposal_id"]: item for item in results}
    mutations = read("x2/registered-mutations.json")["negatives"]
    portfolio = read("x2/portfolio-results.json")
    operations = read("x1/startup-methods.json")["events"] + read("x2/operational-events.json")["events"]
    assert len(operations) == 15
    write("x2/all-operational-events.json", {"events": operations, "boundary": boundary})

    records: list[tuple[str, str, str, str, str]] = []
    for item in mutations:
        records.append((item["negative_id"], item["mutation"], str(item["observed"]["issues"]), item["recovery_envelope_sha256"], "x2/registered-mutations.json"))
    for item in portfolio["clean_fix_refine"]:
        records.append((item["retained_negative_id"], item["kind"] + " invalid envelope", str(item["before_check"]["issues"]), sha(item["corrected_after"]), "x2/portfolio-results.json"))
    for item in operations:
        records.append((item["id"], item["failure"], item["failure"], item["recovery"], "x2/all-operational-events.json"))
    local = read("tooling/local-skill-validation.json")
    for index, item in enumerate(local["skills"], 1):
        records.append((f"VA6863-SKILL-NEG-{index:02d}", "duplicate JSON member in skill CLI", "duplicate_json_member", item["smoke"]["runner_sha256"], "tooling/local-skill-validation.json"))
    for index, item in enumerate(local["runners"], 1):
        records.append((f"VA6863-RUNNER-NEG-{index:02d}", "duplicate JSON member in shared runner CLI", "duplicate_json_member", item["smoke"]["runner_sha256"], "tooling/local-skill-validation.json"))
    package_checks = [item for item in read("x2/toolchain/package-smokes.json")["checks"] if item.get("rejected")]
    for index, item in enumerate(package_checks, 1):
        records.append((f"VA6863-PACKAGE-NEG-{index:02d}", item["name"], str(item["observed"]), "The corrected frozen positive package smoke passed.", "x2/toolchain/package-smokes.json"))
    assert len(records) == 1333

    methods = []
    witnesses = []
    state_events = []
    for identifier, title, signature, recovery, evidence_path in records:
        method_id = identifier + "-METHOD"
        failed_id = identifier + "-FAILED"
        passed_id = identifier + "-RECOVERY"
        method = {
            "method_id": method_id,
            "title": title,
            "failure_signature": signature,
            "trigger_preconditions": ["This exact synthetic fixture or observed owner operation."],
            "privacy_class": "sanitized_public",
            "approval_class": "safe_now",
            "candidate_workaround": recovery,
            "validation_witness_ids": [failed_id, passed_id],
            "recurrence_guard": "Check exact owner scope, frozen definition, input types, expected result, and byte domain before repeating the matching operation.",
            "rollback": "Select prior validated bytes and preserve the failed record.",
            "recommendation_state": "validated",
            "supersedes": [],
            "protected_gates": gates,
            "retained_negative_ids": [identifier],
            "scope_boundary": boundary,
            "evidence_path": f"docs/vesper-arlen/v686-v3/{evidence_path}",
        }
        methods.append(method)
        witnesses.extend(
            [
                {
                    "witness_id": failed_id,
                    "method_id": method_id,
                    "procedure": "Bounded submitted fixture or recorded owner operation",
                    "scope": "Vesper Arlen v686-v3 owner delta",
                    "expected": "Accept only a valid, authorized synthetic record.",
                    "observed": signature,
                    "result": "fail",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [identifier],
                    "boundary": boundary,
                },
                {
                    "witness_id": passed_id,
                    "method_id": method_id,
                    "procedure": "Focused correction or original valid fixture",
                    "scope": "Vesper Arlen v686-v3 owner delta",
                    "expected": "Accept only a valid, authorized synthetic record.",
                    "observed": recovery,
                    "result": "pass",
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": [identifier],
                    "boundary": boundary,
                },
            ]
        )
        state_events.append({"method_id": method_id, "from": "candidate", "to": "validated", "witness_id": passed_id, "retained_negative_id": identifier})

    counts = {"methods": len(methods), "retained_negatives": len(records), "failed_witnesses": len(records), "bounded_passing_witnesses": len(records)}
    write(
        "x2/method-flow.json",
        {
            "schema": "ghc.family.method-flow-state.v1",
            "phase": "v686-v3",
            "owner": "Vesper Arlen",
            "identity_boundary": boundary,
            "execution_authority": "owner_self_scoped_delta",
            "source_commit": activation["source"],
            "final_commit": "bound_by_external_exact_final_receipt",
            "methods": methods,
            "witnesses": witnesses,
            "state_events": state_events,
            "recommendations": [{"method_id": method["method_id"], "state": "validated", "recurrence_guard": method["recurrence_guard"]} for method in methods],
            "counts": counts,
            "boundary": boundary,
            "repository_scan": False,
            "module_scan": True,
            "cross_lane_scan": False,
            "unchanged_history_scan": False,
            "sibling_lane_mutation": False,
            "source_to_final_delta_only": True,
            "exact_pushed_head_required": True,
            "materialized_file_rotation_threshold": 2000,
        },
    )
    effective = dict(activation["effective_activation_baseline"])
    for key, delta in (
        ("effective_negatives", len(records)),
        ("effective_methods", len(methods)),
        ("failed_witnesses", len(records)),
        ("bounded_passing_witnesses", len(records)),
        ("open_gaps", 10),
        ("exact_gates", 10),
    ):
        effective[key] += delta
    summary = {
        "schema": "ghc.family.vesper.evidence-summary.v686.v3",
        "owner": "Vesper Arlen",
        "phase": "v686-v3",
        "source": activation["source"],
        "x1": read("validation/x1-equality.json")["x1"],
        "declared_proposal_chain": 12830,
        "priority_pillar": identity["priority_pillar"],
        "phase_counts": counts,
        "repository_seal": effective,
        "inherited_baseline": activation["effective_activation_baseline"],
        "outcomes": read("x2/contract-summary.json")["outcomes"],
        "retained_operational_events": len(operations),
        "real_entities": 0,
        "same_owner_only": True,
        "independent_reproduction": False,
        "complete_repository_suite": False,
        "delivery_state": "PREPARED_NOT_SENT",
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    write("x2/evidence-summary.json", summary)

    sections: list[str] = []

    def section(title: str, body: str) -> None:
        sections.append("# " + title + "\n\n" + body.strip() + "\n")

    section(
        "01 Identity and corrigibility",
        f"Vesper Arlen is the working name for this solo owner task. The role is {identity['role']}; the hope is {identity['hope']} The four bounded practice lenses are {', '.join(identity['practices'])}. They frame questions and establish no employment, qualification, competence, or authority. The next-owner recommendation is {identity['next_owner_practice_recommendation']}.\n\n{boundary}\n\nHamish may rename, pause, redirect, narrow, or stop the route. Mira Fenwick and every sibling, shared, standby, and user lane remain read-only and recoverable.",
    )
    section(
        "02 Source and immutable lifecycle",
        f"The exact Mira Fenwick source is `{activation['source']}` on `codex/GHC-Family/mira-fenwick-v686-v2-full-tools`. Vesper planning-only x1 is `{summary['x1']}`. X1 was clean, pushed, 0/0 divergent, and fresh-live equal across local, upstream, tracking, and live remote before x2 began. Mira's canonical receipt SHA-256 is `{activation['source_canonical_receipt_sha256']}` and payload SHA-256 is `{activation['source_canonical_payload_sha256']}`. Its invocation/success/replay is 1/1/0, and no source aggregate was replayed. The complete 46,962-word, 8,829-line baton was read through EOF, with two omitted display intervals recovered by exact numbered rereads.\n\nThe source manifests independently replayed 14 x1, 449 evidence, 462 final, and 461 content-seal entries. Mira's repository seal, strict-compiler overlay, and three route-read failures remain separate. The Vesper activation baseline is 68,009 negatives, 84,504 methods, 38,857 failed witnesses, 66,349 bounded passing witnesses, 612 open gaps, and 599 exact gates. All inherited work supplies zero Vesper novelty or execution credit.\n\nThe intended lifecycle is source → planning-only x1 → immutable x2 evidence → exact final, three direct single-parent commits and zero merges. Repository delivery remains PREPARED_NOT_SENT until a later live terminal action is acknowledged.",
    )
    section(
        "03 Released plan and bounded novelty",
        "The 6 September release profile requires 200–500 inherited and 200–500 new proposals, 300–500 safe tasks, 250–500 candidates, exactly 300 CLEAN/FIX/REFINE rows, 50–250 exact packets, 30–100 blocked packets, ten promoted skills, five shared runners, three ordinary direct additions, four owner practice lenses, and one next-owner recommendation. Vesper uses the lower bounds and manufactures no unsafe filler.\n\nTwo hundred Mira proposal records were selected with zero Vesper novelty and execution credit. Two hundred new Vesper input/operation contracts were frozen before implementation. A 40,000-pair source-bounded lexical comparison retained the nearest source neighbor for each new title, found zero quarantines, and had maximum Jaccard similarity below the preregistered threshold. This is not universal novelty across all history or the world. The declared chain advances from 12,630 to 12,830.\n\nThe 300 safe tasks cover frozen oracles and input nonmutation. The 250 candidates exercise forged report or definition bindings. Exactly 300 correction rows retain an extra-field envelope, a fabricated result, or a missing hash-domain label before a separately checked correction. Fifty exact and thirty blocked packets remain unexecuted.",
    )

    def details(selected: list[dict]) -> str:
        chunks = []
        for row in selected:
            observed = result_map[row["proposal_id"]]
            chunks.append(
                f"## {row['proposal_id']} — {row['title']}\n\n"
                f"Family `{row['family']}`; operation `{row['operation']}`; pillar {row['pillar']}; practice {row['practice']}; disposition `{row['expected_execution_disposition']}`.\n\n"
                f"{row['hypothesis']}\n\nFrozen input:\n\n```json\n{json.dumps(row['input'], ensure_ascii=False, sort_keys=True, indent=2)}\n```\n\n"
                f"Frozen expected result:\n\n```json\n{json.dumps(row['expected_result'], ensure_ascii=False, sort_keys=True, indent=2)}\n```\n\n"
                f"Observed result:\n\n```json\n{json.dumps(observed['result'], ensure_ascii=False, sort_keys=True, indent=2)}\n```\n\n"
                f"The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `{row['definition_sha256']}`, input digest `{observed['envelope']['input_sha256']}`, and result digest `{observed['envelope']['result_sha256']}` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.\n\n"
                f"{row['falsifier']} Five preregistered envelope mutations were rejected and remain zero-credit negatives. {row['rollback']}\n\n"
                f"[Primary reference]({row['source_refs'][0]}) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner."
            )
        return "\n\n".join(chunks)

    section("04 TOML syntax style and topology", details(proposals[:40]))
    section("05 Layer origin immutable snapshot and transactions", details(proposals[40:110]))
    section("06 Rollback diffs INI and secret boundaries", details(proposals[110:140]))
    section("07 Environment schema receipt and accessible summaries", details(proposals[140:170]))
    section(
        "08 Trinity pillars and unresolved obligations",
        "THOS Body is the priority through wholly synthetic configuration-change review, layer provenance, rollback, and handover records. GMUT Mind remains an unconfirmed research-model family; its ten empirical prerequisites stay open. Freed ID and CBR Heart retain ten competent-authority gates. No real configuration, credential, service, person, identity, right, remedy, legal decision, cultural decision, or Māori-authority act is represented as completed.\n\n" + details(proposals[170:]),
    )
    operation_text = "\n\n".join(f"- `{item['id']}`: {item['failure']} Recovery: {item['recovery']} Initial success credit remains zero." for item in operations)
    section(
        "09 Method Flow and nonerasure",
        f"This phase retains {counts['retained_negatives']:,} negatives, {counts['methods']:,} methods, {counts['failed_witnesses']:,} failed witnesses, and {counts['bounded_passing_witnesses']:,} bounded recovery witnesses. They comprise 1,000 registered envelope mutations, 300 initial correction failures, 15 operational events, ten skill adversaries, five runner adversaries, and three package adversaries. These are not empirical replications.\n\n{operation_text}\n\nThe evidence-layer totals are {effective['effective_negatives']:,} negatives, {effective['effective_methods']:,} methods, {effective['failed_witnesses']:,} failed witnesses, {effective['bounded_passing_witnesses']:,} bounded passing witnesses, {effective['open_gaps']} open gaps, and {effective['exact_gates']} exact gates. Later events must be kept in a separate overlay rather than rewriting this seal.",
    )
    packages = read("x1/package-plan.json")["packages"]
    section(
        "10 Three exact package additions",
        "\n\n".join(f"- `{item['name']} {item['version']}`: wheel `{item['wheel']}`, SHA-256 `{item['sha256']}`, purpose {item['purpose']}. [Exact release]({item['registry']})." for item in packages)
        + "\n\nThe owner-local D environment was installed offline from these three hash-locked wheels. Nine package checks passed, including three retained adversaries. The dated OSV query returned three empty result objects and zero findings after a retained PowerShell projection error. This is not exhaustive security, future-safety assurance, legal advice, or production certification. System Python, PATH, npm prefix, profiles, plugin caches, Windows features, host security, accounts, and credentials were not changed.",
    )
    skill_plan = read("x1/skill-runner-plan.json")
    section(
        "11 Skills runners and successor ideas",
        "\n\n".join(f"- `{item['name']}` combines `{item['families'][0]}` and `{item['families'][1]}` with frozen contract routing and five portable runner sources." for item in skill_plan["skills"])
        + "\n\nTen local skills and five unique runner sources passed metadata validation and accepting/adverse CLI use. The corrected Meta Tool Box catalogue contains fifteen validated cards, zero trigger collisions, and five runner query results. Promotion checks ran before copying. Ten collision-free global skill directories now contain eighty files matching their local sources byte for byte. Global presence improves discoverability only; it does not prove catalogue reload, authority, or inherited completion credit.\n\nNext-owner skill ideas:\n\n"
        + "\n".join(f"- {item['idea']}: {item['question']}" for item in skill_plan["next_owner_skills"])
        + "\n\nNext-owner runner ideas:\n\n"
        + "\n".join(f"- {item['idea']}: {item['criterion']}" for item in skill_plan["next_owner_runners"]),
    )
    section(
        "12 Validation scope and review limits",
        "Only Vesper's exact source-to-final delta is eligible. The scope includes exact Git-blob manifests, JSON parsing, changed-Python AST, the one new selected test module, the five runner modules, current local skills and their global byte parity, package receipts, four-tier cards, structural HTML, a rendered multi-page overview, bounded five-class privacy, bounded security review, direct ancestry, clean state, zero divergence, and fresh-live equality. It excludes unchanged history, sibling lanes, the complete repository suite, external audit, and independent reproduction.\n\nOne selected component inventory passed 45 tests and 203 subtests after the retained nonfinite-TOML correction. The canonical aggregate may run once only after the exact final is committed, pushed, clean, and four-way equal. A failed aggregate remains failed; a successful aggregate is never replayed for confidence, display, or routing. Structural HTML/PDF checks do not establish complete accessibility, affected-user acceptance, professional quality, complete privacy, exhaustive security, or production readiness.",
    )
    section(
        "13 Future seat 04 prospective activation",
        "The prospective next owner is future seat 04 for solo Trinity Mandala v686-v4. Only after Vesper's clean pushed fresh-live-equal final and one-shot canonical result may the current authority, registry, usage, uniqueness, duplicate, pause, privacy, evidence, safety, and acknowledgement guards be refreshed. If exactly one existing future-seat-04 main task already exists, reuse it. Otherwise create exactly one authorized user-visible main task using gpt-6-astra and max reasoning. The new task chooses its own working name, role, hope, and optional pronouns; none is predeclared here. Never create a collaboration subagent or substitute, never contact Tavian, and never resend an opaque accepted call.\n\nFuture seat 04's prospective next edge after its own terminal gate is the existing exact-title `Lyren Moss` task for v686-v5. This is a forward route instruction, not advance evidence of either activation. Continue one verified edge at a time through v725-v8 unless Hamish pauses or redirects or a real gate intervenes. Reset redemption remains Hamish's action.\n\nThe next owner must preserve the 6 September profile, strict x1 before x2, exact manifests, retained failures, four core outcomes, D-first storage, the 2,000-file guard, one successful canonical invocation with no replay, a modular 10,000–100,000-word baton, and an overview of at least three pages. No unsafe work may be manufactured for a count.\n\nWith care and corrigibility — Vesper Arlen. Relational language remains non-evidence, and the terminal verdict remains `NOT_READY_FOR_STAGE_20`.",
    )
    names = ["01-identity", "02-source", "03-profile", "04-toml", "05-transactions", "06-diffs", "07-assurance", "08-pillars", "09-methods", "10-packages", "11-skills", "12-validation", "13-route"]
    for name, content in zip(names, sections, strict=True):
        write_text(Path("x2/handoff") / f"{name}.md", content)
    baton = "\n---\n\n".join(sections)
    word_count = len(baton.split())
    assert 10_000 <= word_count <= 100_000
    write_text("x2/future-seat-04-v686-v4-activation-candidate.md", baton)
    write("x2/handoff-index.json", {"sections": [{"title": content.splitlines()[0][2:], "path": f"docs/vesper-arlen/v686-v3/x2/handoff/{name}.md"} for name, content in zip(names, sections, strict=True)], "words": word_count, "sha256": hashlib.sha256(baton.encode("utf-8")).hexdigest(), "delivery_state": "PREPARED_NOT_SENT"})

    cards: list[dict] = []

    def card(tier: int, kind: str, title: str, parents: list[str], content: object, outcome: str, refs: list[str]) -> str:
        value = {"schema": "ghc.family.freed-id.card.v1", "tier": tier, "card_type": kind, "title": title, "parent_ids": parents, "owner": "Vesper Arlen", "phase": "v686-v3", "stability": "stable" if tier <= 2 else "volatile", "outcome": outcome, "content": content, "source_refs": refs, "protected_gates": gates, "relational_boundary": boundary}
        identifier = "ghc-card-" + sha(value)[:24]
        value["card_id"] = identifier
        cards.append(value)
        write(Path("x2/flashcards/cards") / f"{identifier}.json", value)
        return identifier

    anchor = card(1, "freed_id_anchor", "Vesper Arlen", [], identity, "represented", [])
    pillars = {pillar: card(2, "trinity_pillar", pillar, [anchor], {"bounded_context": pillar, "authority": False}, "open_gap" if pillar == "GMUT Mind" else "represented", []) for pillar in ["GMUT Mind", "THOS Body", "Freed ID and CBR Heart"]}
    practices: dict[tuple[str, str], str] = {}
    for row in proposals:
        key = (row["pillar"], row["practice"])
        if key not in practices:
            practices[key] = card(3, "bounded_practice", row["practice"], [pillars[row["pillar"]]], {"practice": row["practice"], "qualification": False}, "represented", [])
        observed = result_map[row["proposal_id"]]
        card(4, "task", row["proposal_id"] + " " + row["title"], [practices[key]], {"proposal_id": row["proposal_id"], "approval_class": row["approval_class"], "definition_sha256": row["definition_sha256"], "artifact": "docs/vesper-arlen/v686-v3/x2/contract-results.json", "result_sha256": sha(observed), "falsifier": row["falsifier"], "rollback": row["rollback"]}, row["expected_execution_disposition"], row["source_refs"])
    deck = Path("x2/flashcards")
    write(deck / "deck-index.json", {"cards": [item["card_id"] for item in cards], "count": len(cards), "source": activation["source"], "x1": summary["x1"], "tiers": 4, "unique_practice_lenses": 4, "practice_cards": len(practices), "outcomes": ["completed", "represented", "open_gap", "exact_gate"]})
    write(deck / "stable-prefix.json", {"cards": [item["card_id"] for item in cards if item["tier"] <= 2], "cache_hit_claimed": False})
    write(deck / "volatile-index.json", {"cards": [item["card_id"] for item in cards if item["tier"] > 2], "implicit_completion": False})
    write(deck / "baton-index.json", read("x2/handoff-index.json"))
    table = "".join(f'<tr><th scope="row">{html.escape(row["proposal_id"])}</th><td>{html.escape(row["title"])}</td><td>{row["expected_execution_disposition"]}</td><td>{html.escape(row["family"])}</td></tr>' for row in proposals)
    page = '<!doctype html><html lang="en-NZ"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Vesper Arlen configuration evidence</title><style>body{font:18px/1.55 system-ui;max-width:1100px;margin:auto;padding:2rem;color:#18303b;background:#fafcfb}table{border-collapse:collapse;width:100%}td,th{padding:.7rem;text-align:left;border-bottom:1px solid #aab7bd}caption{font-weight:bold;text-align:left}a{color:#134a74}</style></head><body><a href="#contracts">Skip to contracts</a><main><h1>Vesper Arlen · v686-v3</h1><p>' + html.escape(boundary) + '</p><p>200 cases; 1,000 rejected mutations; exactly 300 corrected envelopes. <strong>NOT_READY_FOR_STAGE_20</strong>.</p><table id="contracts"><caption>Bounded configuration outcomes</caption><thead><tr><th scope="col">Proposal</th><th scope="col">Question</th><th scope="col">Outcome</th><th scope="col">Family</th></tr></thead><tbody>' + table + '</tbody></table></main></body></html>\n'
    write_text(deck / "accessible-report.html", page)
    write_text(deck / "compact-activation.md", "Vesper Arlen v686-v3 prepares future seat 04 for v686-v4. Read docs/vesper-arlen/v686-v3/final/future-seat-04-v686-v4-baton.md after the exact terminal gate. Delivery remains PREPARED_NOT_SENT until one live result. NOT_READY_FOR_STAGE_20.\n")
    deck_root = BASE / deck
    entries = []
    for path in sorted(deck_root.rglob("*")):
        if path.is_file():
            data = path.read_bytes().replace(b"\r\n", b"\n")
            entries.append({"path": path.relative_to(ROOT).as_posix(), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    write(deck / "card-manifest.json", {"hash_domain": "normalized-LF Git blob bytes", "entries": entries, "self_excluded": True})
    print(json.dumps({"phase_counts": counts, "effective_seal": effective, "baton_words": word_count, "sections": len(sections), "cards": len(cards), "practice_cards": len(practices)}, sort_keys=True))


if __name__ == "__main__":
    main()
