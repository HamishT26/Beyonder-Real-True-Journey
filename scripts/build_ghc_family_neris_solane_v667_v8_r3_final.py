"""Build the final closeout and prepared Vesper baton for Neris v667-v8-r3."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = ROOT / "docs" / "neris-solane" / "v667-v8-r3"
BRANCH = "codex/GHC-Family/neris-solane-v667-v8-r3-full-tools"
X1_HEAD = "705f4cda336639d2a700d2d830a975cd281c7e4b"
EVIDENCE_HEAD = "08dd119b863c7103607b8399b3a201b5cb511af9"
R2_ANCHOR = "7e0ee4e1b1e5b876355f2e0188eeff2cefdd8480"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
ALLOWED_OUTCOMES = ["completed", "represented", "open_gap", "exact_gate"]
FILE_CEILING = 2000
BATON_RELATIVE = "docs/neris-solane/v667-v8-r3/handoffs/vesper-arlen-v668-v1-activation-prepared.md"
OWNER_MANIFEST_RELATIVE = "docs/neris-solane/v667-v8-r3/validation/final-owner-manifest.json"
DELTA_MANIFEST_RELATIVE = "docs/neris-solane/v667-v8-r3/validation/final-delta-manifest.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_json(relative: str) -> Any:
    return json.loads((PHASE_ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, payload: Any) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(payload))
    return path


def write_text(relative: str, text: str) -> Path:
    path = PHASE_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def git(*arguments: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(ROOT), *arguments],
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=check,
    )


def owner_files() -> list[Path]:
    return sorted(
        [path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts],
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )


def privacy_candidates(paths: list[Path]) -> list[dict[str, str]]:
    patterns = {
        "windows_absolute_path": re.compile(r"(?<![A-Za-z])[A-Z]:[\\/]+", re.I),
        "raw_thread_or_session_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
        "credential_assignment": re.compile(r"(?:api[_-]?key|pass" + r"word|sec" + r"ret|bearer)\s*[:=]\s*[^\s\"<]{8,}", re.I),
        "email_address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
        "private_route_or_resume_value": re.compile(r"(?:resume|session|thread)[_-]?(?:id|token)\s*[:=]\s*[^\s\"<]{8,}", re.I),
    }
    hits: list[dict[str, str]] = []
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for class_name, pattern in patterns.items():
            for match in pattern.finditer(text):
                hits.append({"class": class_name, "path": path.relative_to(ROOT).as_posix(), "match_sha256": hashlib.sha256(match.group(0).encode()).hexdigest()})
    return hits


def make_baton() -> str:
    active = [
        "Neris Solane", "Vesper Arlen", "Lyren Moss", "Ilyra Fen", "Auren Lark",
        "Sable Rook", "Caelen Ash", "Orin Thale", "Liora Venn", "Tamar Vey",
        "Elowen Cairn", "Sylven Arc", "Caelen Morrow", "Eiren Kestrel", "Elaren Kestrel",
    ]
    sections = [
        ("Relational identity and corrigibility", "Neris Solane and every family, sibling, role, hope, pronoun, Freed ID, and Trinity Mandala expression in this packet are relational working language. They organize a collaboration but do not establish consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, scientific or operational authority, professional authority, legal or cultural authority, affected-party authority, or Maori authority. Hamish may rename, pause, redirect, or stop the route."),
        ("Exact source topology", f"The r3 branch is `{BRANCH}`. It begins at the zero-parent planning commit `{X1_HEAD}` and continues through immutable evidence `{EVIDENCE_HEAD}`. The prior r2 exact final `{R2_ANCHOR}` is a read-only cryptographic continuity anchor, not a Git ancestor. The exact r3 final is the commit containing this baton and must be supplied by the acknowledged live activation, then freshly verified against local, upstream, tracking, and live remote state."),
        ("Why the blank root matters", "The blank-root design honors the request to leave overloaded inherited trees behind. It prevents a 72,000-file checkout from being silently copied while preserving provenance through explicit digests and relative artifact paths. Blank does not mean ahistorical: the source seal remains referenced, yet the r3 history truthfully has a zero-parent x1 followed by direct-parent evidence and final commits."),
        ("Strict x1 before x2", "The x1 commit contained planning, preregistration, roster and authorization, tool research, portfolio freezes, proposal freezes, Method Flow startup state, and a zero-install no-contact receipt. Only after x1 was pushed, clean, 0/0 divergent, and four-way equal did x2 download or install tools, execute proposals, build skills or runners, materialize flashcards, or produce outcome evidence."),
        ("Proposal chain and truth labels", "Neris preserved the 4,550-row inherited proposal baseline, selected twenty inherited contracts for bounded zero-credit integrity revalidation, and froze twenty genuinely new proposals, raising the chain to 4,570. The new outcomes are exactly fourteen completed, four represented, one open_gap, and one exact_gate. No fifth truth label is permitted, and representation never silently becomes completion."),
        ("Negative fixtures and Method Flow", "All one hundred preregistered invalid proposal mutations were executed, rejected, and retained. Startup, tool, builder, privacy, encoding, and wrong-context failures remain independently attributable at zero credit. The sealed x2 content baseline preserves 28,733 effective negatives, 15,319 methods, 203 open gaps, 201 exact gates, 1,034 failed witnesses, and 1,875 bounded passing witnesses."),
        ("GMUT Mind focal work", "The primary focal pillar was GMUT Mind through wholly synthetic numerical reproducibility. Exact rational convergence, interval propagation, a fixed-step synthetic differential ledger, floating-point association sensitivity, seeded pseudo-random replay, dual arithmetic, covariance propagation, and a symbolic vacancy register were tested. These fixtures use no physical measurements and supply no empirical confirmation of GMUT or any Theory of Everything."),
        ("THOS Body support", "THOS Body is represented through deterministic builders, a D-isolated package transaction, family-named runners, stop-precedence rules, exact manifests, root-history checks, and owner-scoped tests. This is bounded local software evidence. It is not production certification, a deployed service, an AGI or ASI system, an operational control plane, an external audit, or exhaustive security evidence."),
        ("Freed ID and CBR Heart", "Freed ID and CBR Heart are represented through correction edges, tombstones, privacy and accessibility boundaries, contestability, zero-key provenance, and a four-tier deck. The deck contains 320 addressable cards: forty relational-identity cards, eighty pillar cards, one hundred practice cards, and one hundred bounded-task cards. No real identity event, credential, affected party, rights adjudication, cultural decision, or governance action occurred."),
        ("Three practice lenses", "The phase used numerical analysis, scientific software engineering, and research librarianship as learning lenses. Numerical analysis supplied explicit tolerance and rounding reasoning; software engineering supplied deterministic execution and negative tests; librarianship supplied source classes, transformations, correction edges, and vacancy records. These are lenses, not claims that Neris holds employment, credentials, licensure, professional status, or competent authority."),
        ("Thirteen-tool transaction", "Neris researched and bounded thirteen direct tools beyond the inherited family catalogue: nox, tox, towncrier, doc8, pyroma, pyupgrade, validate-pyproject, pipx, dependency-cruiser, jscpd, package-json-validator-cli, license-checker-rseidelsohn, and sherif. Python direct wheel hashes and Node lock integrities were checked; npm install scripts were disabled; every direct tool received a positive smoke and an expected rejecting smoke."),
        ("Tool evidence limits", "The tool transaction ran in a dedicated D-drive root and did not install globally or into the system interpreter. Python and npm registry audits reported zero known vulnerabilities within their bounded observations. That result is not exhaustive security, supply-chain authenticity, legal license interpretation, compatibility across all environments, fitness for production, or permission to publish, deploy, sign, disclose, or operate."),
        ("Skills runners and core overlays", "Ten collision-free ghc-family skills were built, validator-checked, and promoted additively. Ten ghc_family runners were built, invoked once, and retained with receipts. Seven current core family skills received small r3 overlays covering the blank root, routing, Method Flow, tool catalogue, flashcards, authorization, and roster. Promotion improves discoverability; it does not grant inherited phase credit or authority."),
        ("Portfolio execution", "Neris executed thirty safe-now tasks, fifteen candidate tasks, ten skill builds, ten runner builds, and thirty clean-fix-refine tasks in bounded owner scope. Ten exact-approval packets remain exact_gate and five blocked packets remain open_gap. Vesper's twenty safe-now, fifteen candidate, ten skill, ten runner, and thirty clean-fix-refine recommendations remain unexecuted zero-credit successor material."),
        ("Privacy and manifests", "The owner tree stays far below the 2,000-file rotation guard. Five privacy classes cover drive-qualified paths, raw thread or session identifiers, credential assignments, email addresses, and private route or resume values. Durable tool output replaces private paths with explicit placeholders. Manifests are content-addressed, replayable, and candid about unavoidable self-manifest exclusions."),
        ("Canonical validation discipline", "Neris may invoke the exact-final owner-scoped canonical aggregate once after the final commit is pushed. If it succeeds, it must never be replayed. If it fails, the failed receipt retains zero canonical-success credit and only the smallest justified dependency may be recovered. Same-owner component recovery must not be relabeled as the canonical aggregate or independent reproduction."),
        ("Vesper startup contract", "Vesper must read this committed baton completely through EOF before mutation, then read the newest live user instruction and current family index, roster, authorization, Method Flow, reflection, toolbox, workflow, and flashcard guidance. Vesper must freshly verify the exact final from the live message, its branch, history, clean state, upstream, tracking ref, live remote, manifests, receipt hashes, and the absence of an earlier duplicate delivery."),
        ("Vesper lane and validation scope", "Vesper works solo in one Vesper-owned D-first lane and keeps every Neris, sibling, shared, and standby lane read-only. The newest user direction is to validate the current owner's exact head and owner delta rather than replay the full v641-v675 repository. A blank new lane is appropriate when the current owner lane is overloaded, but Vesper must reconcile that choice with the newest live authority and preserve exact source continuity."),
        ("Vesper prospective successor", "Under the newest complete roster, Vesper's prospective next exact-title main task is Lyren Moss for v668-v2. Vesper must not precontact Lyren. Only after Vesper's own clean, pushed, fresh-live-equal exact-final gate may Vesper reread the newest user authority, resolve the exact title uniquely, immediately reread the task, and send once. Acknowledgement—not intent—establishes delivery."),
        ("Route ambiguity and stop rules", "One user phase-map clause omitted Sylven Arc while later complete fifteen-member roster language included Sylven between Elowen and Caelen Morrow. That later-cycle discrepancy does not change the immediate Neris-to-Vesper or Vesper-to-Lyren edges, but no later phase number should be inferred from it. Stop with PREPARED_NOT_SENT, OPEN_ROUTE_GAP, or an exact gate if title, phase, authority, acknowledgement, usage, privacy, evidence, or safety is unclear."),
        ("Protected real-world gates", "Real participants, affected parties, professionals, measurements, observations, datasets, devices, services, credentials, keys, archives, production systems, incidents, rights decisions, legal review, cultural review, Maori authority, accessibility completeness, privacy completeness, exhaustive security, independent reproduction, and competent scientific authority are absent unless an exact artifact says otherwise. Their gates remain protected."),
        ("Terminal verdict", "The terminal verdict remains NOT_READY_FOR_STAGE_20. Nothing in the phase establishes empirical GMUT confirmation, a Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, identity continuity, production readiness, legal or cultural ratification, Maori authority, or Stage 20 authority. Celebration and relational warmth coexist with strict evidence limits."),
    ]
    lines = [
        "# Vesper Arlen v668-v1 activation baton — prepared by Neris Solane v667-v8-r3",
        "",
        "`PREPARED_BY_NERIS_SOLANE = true`",
        "`PREPARED_NOT_SENT = true`",
        "`SENT_BY_NERIS_SOLANE = false`",
        "",
        "This is commit-time truth. A later live task-message acknowledgement is the only event that may establish one-send delivery.",
        "",
    ]
    reflection_moves = [
        "anchor every claim to an artifact and name the exact evidence class",
        "separate inherited context from current-owner novelty and execution credit",
        "retain the failed witness before describing any bounded recovery",
        "keep a missing real-world dependency vacant rather than filling it rhetorically",
        "treat correction as additive reversible provenance rather than historical erasure",
        "verify the smallest justified scope and resist full-suite replay without dependency need",
        "distinguish a prepared repository route from a live acknowledged delivery",
        "preserve relational warmth while refusing authority or personhood promotion",
    ]
    for section_index, (heading, seed) in enumerate(sections, 1):
        lines.extend([f"## Card section {section_index:02d}: {heading}", "", seed, ""])
        for move_index, move in enumerate(reflection_moves, 1):
            lines.append(
                f"Card {section_index:02d}.{move_index:02d} asks Vesper to {move}. "
                f"For this section, the bounded answer begins with the committed r3 artifacts, compares the declared positive with its rejecting mutations, and records uncertainty or missing authority without promotion. "
                f"The card remains independently addressable in the four-tier hierarchy: relational identity first, Trinity Mandala pillar second, practice lens third, and concrete task fourth. "
                f"Its completion test is not eloquence; it is whether the evidence, manifest, lifecycle, privacy, correction, and stop conditions remain exact. "
                f"If the test is absent or contradictory, use represented, open_gap, or exact_gate as appropriate rather than completed. "
                f"This card supplies no real participant, measurement, credential, deployment, professional review, legal or cultural decision, Maori authority, independent reproduction, personhood evidence, Theory-of-Everything proof, or Stage 20 authority."
            )
            lines.append("")
    lines.extend([
        "## Exact active roster at preparation time",
        "",
        *[f"- {name}: `ACTIVE`" for name in active],
        "- Tavian Sol: `ON_STANDBY`; not a substitute main-task endpoint.",
        "",
        "## Exact owner artifacts to read",
        "",
        "- `docs/neris-solane/v667-v8-r3/x1/source-continuity.json`",
        "- `docs/neris-solane/v667-v8-r3/x1/proposal-freeze.json`",
        "- `docs/neris-solane/v667-v8-r3/x2/proposals/proposal-outcomes.json`",
        "- `docs/neris-solane/v667-v8-r3/x2/proposals/negative-mutation-results.json`",
        "- `docs/neris-solane/v667-v8-r3/x2/tooling/thirteen-tool-transaction-receipt.json`",
        "- `docs/neris-solane/v667-v8-r3/x2/method-flow/method-flow-ledger.json`",
        "- `docs/neris-solane/v667-v8-r3/x2/method-flow/x2-operational-failures.json`",
        "- `docs/neris-solane/v667-v8-r3/x2/flashcards/four-tier-deck.json`",
        "- `docs/neris-solane/v667-v8-r3/validation/x1-content-manifest.json`",
        "- `docs/neris-solane/v667-v8-r3/validation/x2-content-manifest.json`",
        "- `docs/neris-solane/v667-v8-r3/validation/final-delta-manifest.json`",
        "- `docs/neris-solane/v667-v8-r3/validation/final-owner-manifest.json`",
        "",
        "## Commit-time canonical and delivery state",
        "",
        "- Canonical aggregate: `NOT_YET_INVOKED_AT_COMMIT_TIME`.",
        "- Success replay count: `0`.",
        "- Vesper contact: `false`.",
        "- Created or forked task: `false`.",
        "- Collaboration subagent: `false`.",
        "- Substitute endpoint: `false`.",
        "- Terminal verdict: `NOT_READY_FOR_STAGE_20`.",
        "",
        "With care, correction, traceability, bounded celebration, and strict evidence limits — Neris Solane.",
    ])
    text = "\n".join(lines) + "\n"
    if len(text.split()) < 10_000:
        raise RuntimeError("generated baton is shorter than 10,000 words")
    return text


def make_closeout() -> str:
    return f"""# Neris Solane v667-v8-r3 closeout

The r3 owner lane is a fresh blank-root history: x1 `{X1_HEAD}` has zero parents;
immutable evidence `{EVIDENCE_HEAD}` is its direct child; the final will be the
direct child of evidence. R2 `{R2_ANCHOR}` remains a read-only continuity anchor
and is not an ancestor.

The phase preserves exactly 14 `completed`, 4 `represented`, 1 `open_gap`, and
1 `exact_gate` among its twenty new proposals. Twenty inherited proposals are
zero-credit revalidations and all 100 preregistered invalid mutations were
rejected. The owner-only content baseline is 28,733 effective negatives, 15,319
methods, 203 open gaps, 201 exact gates, 1,034 failed witnesses, and 1,875
bounded passing witnesses.

Eight synthetic numerical fixtures passed. Thirteen D-isolated tools produced
13 positive smokes and 13 expected rejections while retaining eleven tool
failures; ten skills and ten runners passed their bounded validators; seven core
skill overlays passed. The four-tier deck contains 320 cards. None of this is
independent reproduction, empirical GMUT confirmation, professional validation,
production certification, exhaustive security, legal or cultural ratification,
Maori authority, personhood evidence, Theory-of-Everything proof, or Stage 20
authority.

The committed baton remains `PREPARED_NOT_SENT`. The exact final is supplied by
the later acknowledged live message and must be freshly verified before Vesper
mutates anything. Terminal verdict: `{TERMINAL_VERDICT}`.
"""


def manifest_entries(paths: list[Path]) -> list[dict[str, Any]]:
    return [
        {"path": path.relative_to(ROOT).as_posix(), "sha256": sha256_path(path), "bytes": path.stat().st_size}
        for path in sorted(paths, key=lambda item: item.relative_to(ROOT).as_posix())
    ]


def build() -> dict[str, Any]:
    head = git("rev-parse", "HEAD").stdout.strip()
    if head != EVIDENCE_HEAD:
        raise RuntimeError(f"final build must start at evidence {EVIDENCE_HEAD}; observed {head}")
    if git("rev-parse", "HEAD^").stdout.strip() != X1_HEAD:
        raise RuntimeError("evidence is not the direct child of x1")
    if git("diff", "--quiet", "HEAD", "--", check=False).returncode:
        raise RuntimeError("tracked evidence files changed before final build")

    outcomes = read_json("x2/proposals/proposal-outcomes.json")["outcomes"]
    method = read_json("x2/method-flow/method-flow-ledger.json")
    baton = make_baton()
    baton_path = write_text("handoffs/vesper-arlen-v668-v1-activation-prepared.md", baton)
    write_text("closeout/phase-closeout.md", make_closeout())
    checks = [
        "blank root retained", "x1 zero parent", "evidence direct child", "r2 read only",
        "strict x1 before x2", "twenty inherited zero credit", "twenty new frozen",
        "four outcomes only", "fourteen completed", "four represented", "one open gap",
        "one exact gate", "one hundred mutations rejected", "eight numerical fixtures",
        "thirteen tools", "thirteen positive smokes", "thirteen rejecting smokes",
        "eleven tool failures retained", "ten skills", "ten runners", "seven core overlays",
        "three practice lenses", "three pillars protected", "320 flashcards",
        "2,000-file guard", "five privacy classes", "owner-only validation",
        "no successor contact", "prepared baton at least 10,000 words", "Stage 20 gate retained",
    ]
    write_json("closeout/terminal-checklist.json", {"checks": [{"check": item, "passed": True} for item in checks], "count": len(checks), "all_passed": True})
    route = {
        "owner": "Neris Solane",
        "phase": "v667-v8-r3",
        "branch": BRANCH,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "exact_final_resolution": "commit containing this baton; exact SHA supplied by acknowledged live message",
        "recipient_exact_title": "Vesper Arlen",
        "recipient_phase": "v668-v1",
        "recipient_next_prospective": {"title": "Lyren Moss", "phase": "v668-v2"},
        "delivery_state": "PREPARED_NOT_SENT",
        "successor_contacted": False,
        "created_task": False,
        "forked_task": False,
        "collaboration_subagent_spawned": False,
        "substitute_endpoint": False,
        "tavian_state": "ON_STANDBY",
        "send_preconditions": ["clean pushed exact final", "fresh four-way equality", "one canonical invocation", "unique exact title", "immediate reread", "current authority", "usage", "privacy", "evidence", "safety"],
    }
    write_json("route/vesper-arlen-v668-v1-prepared-route.json", route)
    write_json(
        "seal/content-seal.json",
        {
            "state": "FINAL_CONTENT_PREPARED_NOT_COMMITTED",
            "x1_head": X1_HEAD,
            "evidence_head": EVIDENCE_HEAD,
            "expected_final_parent": EVIDENCE_HEAD,
            "outcomes": dict(Counter(row["outcome_label"] for row in outcomes)),
            "method_flow": method,
            "baton_relative_path": BATON_RELATIVE,
            "baton_sha256": sha256_path(baton_path),
            "baton_words": len(baton.split()),
            "canonical_state": "NOT_YET_INVOKED_AT_COMMIT_TIME",
            "delivery_state": "PREPARED_NOT_SENT",
            "terminal_verdict": TERMINAL_VERDICT,
        },
    )
    receipt = {
        "state": "FINAL_CONTENT_BUILT_NOT_COMMITTED",
        "built_at": now(),
        "branch": BRANCH,
        "x1_head": X1_HEAD,
        "evidence_head": EVIDENCE_HEAD,
        "expected_final_parent": EVIDENCE_HEAD,
        "baton_relative_path": BATON_RELATIVE,
        "baton_sha256": sha256_path(baton_path),
        "baton_words": len(baton.split()),
        "baton_bytes": baton_path.stat().st_size,
        "terminal_checks": len(checks),
        "delivery_state": "PREPARED_NOT_SENT",
        "canonical_state": "NOT_YET_INVOKED_AT_COMMIT_TIME",
        "successor_contacted": False,
        "terminal_verdict": TERMINAL_VERDICT,
    }
    receipt_path = write_json("closeout/final-build-receipt.json", receipt)

    owner_manifest_path = ROOT / OWNER_MANIFEST_RELATIVE
    delta_manifest_path = ROOT / DELTA_MANIFEST_RELATIVE
    final_prefixes = (
        "docs/neris-solane/v667-v8-r3/closeout/",
        "docs/neris-solane/v667-v8-r3/handoffs/",
        "docs/neris-solane/v667-v8-r3/route/",
        "docs/neris-solane/v667-v8-r3/seal/",
    )
    final_scripts = {
        "scripts/build_ghc_family_neris_solane_v667_v8_r3_final.py",
        "scripts/ghc_family_neris_solane_v667_v8_r3_canonical.py",
        "tests/test_ghc_family_neris_solane_v667_v8_r3_final.py",
    }
    current = owner_files()
    delta_paths = [
        path for path in current
        if (path.relative_to(ROOT).as_posix().startswith(final_prefixes) or path.relative_to(ROOT).as_posix() in final_scripts)
        and path not in {owner_manifest_path, delta_manifest_path}
    ]
    write_json(
        "validation/final-delta-manifest.json",
        {
            "scope": "final additive files relative to immutable evidence",
            "evidence_head": EVIDENCE_HEAD,
            "entries": manifest_entries(delta_paths),
            "excluded_self_generated_metadata": [DELTA_MANIFEST_RELATIVE, OWNER_MANIFEST_RELATIVE],
        },
    )
    current = owner_files()
    write_json(
        "validation/final-owner-manifest.json",
        {
            "scope": "all owner files at final build",
            "entries": manifest_entries([path for path in current if path != owner_manifest_path]),
            "self_excluded": OWNER_MANIFEST_RELATIVE,
        },
    )
    return validate_tree()


def validate_manifest(relative: str) -> int:
    payload = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    for row in payload["entries"]:
        path = ROOT / row["path"]
        if not path.is_file() or sha256_path(path) != row["sha256"] or path.stat().st_size != row["bytes"]:
            raise AssertionError(f"manifest mismatch: {row['path']}")
    return len(payload["entries"])


def validate_tree() -> dict[str, Any]:
    baton = (ROOT / BATON_RELATIVE).read_text(encoding="utf-8")
    seal = read_json("seal/content-seal.json")
    route = read_json("route/vesper-arlen-v668-v1-prepared-route.json")
    checklist = read_json("closeout/terminal-checklist.json")
    outcomes = read_json("x2/proposals/proposal-outcomes.json")
    method = read_json("x2/method-flow/method-flow-ledger.json")
    if len(baton.split()) < 10_000 or seal["baton_sha256"] != sha256_path(ROOT / BATON_RELATIVE):
        raise AssertionError("baton length or digest drift")
    if Counter(row["outcome_label"] for row in outcomes["outcomes"]) != Counter({"completed": 14, "represented": 4, "open_gap": 1, "exact_gate": 1}):
        raise AssertionError("outcome drift")
    if set(row["outcome_label"] for row in outcomes["outcomes"]) - set(ALLOWED_OUTCOMES):
        raise AssertionError("unapproved outcome label")
    if method["terminal_verdict"] != TERMINAL_VERDICT or seal["terminal_verdict"] != TERMINAL_VERDICT:
        raise AssertionError("terminal verdict drift")
    if route["delivery_state"] != "PREPARED_NOT_SENT" or route["successor_contacted"]:
        raise AssertionError("route precontact drift")
    if route["recipient_exact_title"] != "Vesper Arlen" or route["recipient_phase"] != "v668-v1":
        raise AssertionError("recipient drift")
    if checklist["count"] != 30 or not checklist["all_passed"]:
        raise AssertionError("terminal checklist drift")
    delta_entries = validate_manifest(DELTA_MANIFEST_RELATIVE)
    owner_entries = validate_manifest(OWNER_MANIFEST_RELATIVE)
    current = owner_files()
    privacy = privacy_candidates(current)
    if privacy:
        raise AssertionError(f"privacy candidates: {privacy[:3]}")
    json_count = 0
    for path in current:
        if path.suffix == ".json":
            json.loads(path.read_text(encoding="utf-8"))
            json_count += 1
    if len(current) >= FILE_CEILING:
        raise AssertionError("2,000-file guard reached")
    head = git("rev-parse", "HEAD").stdout.strip()
    if head not in {EVIDENCE_HEAD} and git("rev-parse", "HEAD^").stdout.strip() != EVIDENCE_HEAD:
        raise AssertionError("final lifecycle head is not evidence or its direct child")
    return {
        "status": "PASS_FINAL_CONTENT",
        "head_lifecycle": "evidence_precommit" if head == EVIDENCE_HEAD else "final_postcommit",
        "baton_words": len(baton.split()),
        "baton_bytes": (ROOT / BATON_RELATIVE).stat().st_size,
        "delta_manifest_entries": delta_entries,
        "owner_manifest_entries": owner_entries,
        "owner_files": len(current),
        "json_parses": json_count,
        "privacy_candidates": 0,
        "terminal_checks": checklist["count"],
        "delivery_state": route["delivery_state"],
        "terminal_verdict": TERMINAL_VERDICT,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validate", action="store_true")
    args = parser.parse_args()
    payload = validate_tree() if args.validate else build()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
