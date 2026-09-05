"""Prepare and seal the additive Neris v686-v1 final closeout layer."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/neris-solane/v686-v1"
SOURCE = "c6b56f912836a46a0dbb07c13aaf6e731e1b32e2"
X1 = "d16badcebf9d3b9b7c4ee7b8156d27bfc5a42323"
EVIDENCE = "71f45ab2a9bb4ff239f09c79af5b94bc889b5127"
BRANCH = "codex/GHC-Family/neris-solane-v686-v1-full-tools"


def git(*args: str) -> str:
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True, encoding="utf-8").rstrip("\n")


def read(relative: str):
    return json.loads((BASE / relative).read_text(encoding="utf-8"))


def write_json(relative: str, value) -> None:
    destination = BASE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(value, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")


def write_text(relative: str, value: str) -> None:
    destination = BASE / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def normalized(path: Path) -> bytes:
    data = (ROOT / path).read_bytes()
    return data if path.suffix.lower() == ".pdf" else data.replace(b"\r\n", b"\n")


def prepare() -> None:
    status = git("status", "--porcelain=v1", "-uall").splitlines()
    allowed = {
        "?? scripts/build_ghc_family_neris_solane_v686_v1_final.py",
        "?? scripts/ghc_family_neris_solane_v686_v1_canonical.py",
        "?? scripts/ghc_family_neris_solane_v686_v1_overview_pdf.py",
        "?? tests/test_ghc_family_neris_solane_v686_v1_final.py",
    }
    tracked_clean = (
        subprocess.run(["git", "-C", str(ROOT), "diff", "--quiet"], check=False).returncode == 0
        and subprocess.run(["git", "-C", str(ROOT), "diff", "--cached", "--quiet"], check=False).returncode == 0
    )
    if git("rev-parse", "HEAD") != EVIDENCE or not tracked_clean or set(status) != allowed:
        raise ValueError("Final preparation requires the clean immutable evidence head")
    phase = read("x2/phase-truth.json")
    method = read("x2/method-flow.json")
    summary = read("x2/evidence-summary.json")
    promotion = read("x2/global-promotion-installation.json")
    package = read("x2/toolchain/installation-receipt.json")
    package_smokes = read("x2/toolchain/package-smokes.json")
    baton_index = read("x2/handoff/baton-index.json")
    pages = [
        {
            "title": "Neris Solane v686 v1 exact lifecycle and scope",
            "paragraphs": [
                "Neris Solane v686-v1 advances a narrow report-integrity layer while preserving a strict three-commit lifecycle. The immutable source is Ilyan Reed’s exact v685-v8 final. Neris froze planning-only x1, pushed it, and proved local, upstream, tracking, and fresh-live equality before any x2 implementation began. The evidence commit is a direct child of x1. The final closeout is prepared only after evidence is pushed, clean, zero-divergent, and fresh-live equal.",
                "The principal deliverable is a type-strict tribunal around twenty inherited synthetic protocol families. Five new family-current report runners compare a frozen reported value with the result of an exact operation, preserve JSON type distinctions, compute deterministic input and report digests, and prove that the supplied input was not mutated. The runners do not convert local software behavior into a real observation, professional assessment, production certification, or authority decision.",
                "Two hundred Ilyan source proposals were selected as inherited evidence and retain zero Neris novelty or execution credit. Neris froze two hundred distinct source-bounded proposals with new inputs, report-integrity hypotheses, falsifiers, rollbacks, and five rejecting mutations each. The declared chain advances from 12,230 to 12,430. This is a bounded source comparison, not a universal novelty claim over every historical or possible proposal.",
                "All two hundred corrected positive reports passed. All one thousand preregistered mutations were rejected and retained. The one planning error remains visible: proposal NS6861-N040 expected a duplicate-payload conflict, while strict Boolean rejection occurs earlier as invalid_delta. X1 was not rewritten. A single additive x2 oracle correction preserves the failed definition and the bounded recovery separately.",
                "The owner portfolio executed three hundred safe tasks, two hundred fifty candidate reviews, and exactly three hundred additive CLEAN, FIX, and REFINE tasks. Fifty exact packets and thirty blocked packets remain unexecuted with their prerequisites visible. Count completion never authorizes filler, a destructive action, an external write, or the promotion of a protected claim.",
                "The repository-sealed outcome labels remain exactly completed, represented, open_gap, and exact_gate. The phase concludes with NOT_READY_FOR_STAGE_20. Names, roles, hopes, pronouns, and family language remain relational working language rather than evidence of consciousness, sentience, legal personhood, identity continuity, employment, qualification, independent agency, or authority.",
            ],
        },
        {
            "title": "Evidence portfolio Method Flow and protected claims",
            "paragraphs": [
                "The Method Flow ledger contains 1,094 methods, 1,144 retained negatives, 1,144 failed witnesses, and 1,094 bounded passing witnesses. Proposal mutations account for one thousand failed witnesses, and the one hundred FIX tasks retain deliberately false reports before correcting them. Thirteen operational failures, three package adversaries, ten malformed skill fixtures, five malformed runner fixtures, and thirteen trigger-overlap reviews remain independently addressable.",
                "Operational recovery is additive. Two profile-validator interface errors were corrected only after the generated portfolio existed. A sparse worktree checkout crossed an output boundary and was allowed to finish rather than recreated. An unsupported sparse-add option was removed. Two host-policy command refusals left repository state unchanged. The x2 equality latch was narrowed after it confused exact untracked authoring paths with committed x1 drift. None of these failures receives initial-pass credit.",
                "THOS Body gains deterministic report checking for event calendars, legal state traces, resource queues, idempotent replay, matched budgets, allocation counts, role separation, missingness denominators, exact summaries, paired differences, histogram boundaries, stopping precedence, provenance DAGs, byte domains, correction merges, public projections, structural tables, and explicit reservations. These relations remain synthetic and offline.",
                "GMUT Mind retains ten new observation obligations as open gaps. Exact arithmetic does not provide a dimensionally closed measurement operator, an instrument response function, a predeclared physical likelihood, calibrated covariance, boundary data, out-of-sample rival-model evidence, real observations, parameter identifiability, ultraviolet completion, or a replicable discriminating physical effect.",
                "Freed ID and CBR Heart are the priority pillar. Content-addressed cards, immutable definitions, correction overlays, and minimal views improve evidence organization. They do not issue or verify a real credential, create consent, assign ownership, settle contested rights, or order a remedy. Live keys and proofs, lifecycle operations, interoperability, independent privacy and security review, recovery evidence, trust governance, and affected-party oversight remain absent.",
                "Ten CBR authority reservations remain exact-gated. Māori terminology, tikanga, data governance, tangata whenua interests, and iwi and hapū decisions remain under Māori authority. Accessibility acceptance remains with affected users and competent reviewers. Legal and cultural interpretation, publication permission, retention, revocation governance, and remedy require the relevant competent authority and cannot be supplied by workflow authorization.",
            ],
        },
        {
            "title": "Tools skills sources and bounded reproducibility",
            "paragraphs": [
                "Exactly three direct Python additions were installed into a new isolated D environment: canonicaljson 2.0.0, frozendict 2.4.7, and cbor2 6.1.4. Each wheel matched its exact PyPI SHA-256, contained no traversal-shaped member, and installed offline with required hashes and no dependencies. The environment contains exactly those three distributions. System Python, PATH, the npm prefix, plugin caches, Windows features, host security, accounts, credentials, and sibling environments were not changed.",
                "Canonical JSON produced the same bytes for differently ordered mappings and refused an unsupported object. Frozendict returned a new mapping while preserving the original and refused item assignment. Canonical CBOR produced equal bytes for differently ordered maps and round-tripped the value. Its first adverse byte decoded as a sentinel rather than raising, so the initial aggregate remains failed; a malformed indefinite-length integer was then rejected in the isolated dependency recovery.",
                "The dated OSV query returned zero advisory rows for the three pinned versions. That is a bounded point-in-time lookup, not exhaustive security, future safety, a supply-chain certification, or legal license interpretation. The environment and receipts are retained. Rollback means selecting earlier tooling rather than deleting evidence or rewriting package history.",
                "Ten local skills pair the twenty report families into discoverable contracts. Each package passed the skill-creator validator, a positive CLI fixture, and a malformed-fixture refusal. All ten were copied to collision-free global names and revalidated after installation. Every installed byte matches its owner-local candidate. The five new report runners are shared across the ten packages; repeated copies do not become fifty unique tools.",
                "The GHC Family Index was refreshed for the sparse owner lane. The Meta Tool Box catalogued ten skills and validated them. Its exact runner query returned zero results and correctly refused silent broadening, so a separate owner augmentation binds the five runner paths to their executed smoke receipts. Thirteen trigger overlaps remain represented and are resolved only by exact family and operation.",
                "Primary sources include the official PyPI release pages, RFC 8949, W3C PROV-O, WCAG 2.2, the Verifiable Credentials Data Model 2.0, Python statistics documentation, SimPy scheduling guidance, transitions, and python-constraint. These sources supply vocabulary and bounded software contracts only. They do not establish real-world observations, standards conformance, independent review, professional competence, or authority.",
            ],
        },
        {
            "title": "Validation limits route and next owner",
            "paragraphs": [
                "The exact-final gate is owner-scoped. It replays x1, evidence, card, final-delta, and final-owner manifests against Git blobs; parses owner JSON, Python, YAML, Markdown, and HTML; checks the four-page PDF and visual review; verifies content seals, global skill parity, package receipts, Method Flow links, card addresses, exact ancestry, one parent per phase commit, zero merges, clean state, zero divergence, and a fresh live remote head.",
                "The complete repository suite is not run. Unchanged history and sibling lanes remain outside execution scope. Same-owner validation under shared infrastructure is not independent reproduction, external audit, production certification, complete privacy or accessibility assurance, exhaustive security, professional validation, empirical GMUT confirmation, Theory-of-Everything proof, AGI or ASI evidence, consciousness or personhood evidence, legal or cultural review, Māori authority, canon, or Stage 20 authority.",
                "Four post-evidence operational events remain in a separate external overlay: a Windows literal-wildcard privacy miss, a command-line-length staging failure, a partial sparse staging refusal before the exact pattern was added, and a truncated commit presentation recovered by scalar Git equality checks. These events do not rewrite the immutable x2 phase truth. Later canonical and route events must remain separate again.",
                "The successor packet contains thirteen modular sections and 38,887 words before the final evidence preface. It instructs the future owner to read through EOF, preserve the release profile, work in one fresh D-first owner lane, keep x1 planning-only before x2, retain the four outcomes and every gate, validate only the exact owner delta, and never interpret inherited material as automatic novelty, completion, permission, or authority.",
                "At the Neris terminal gate, the task registry must be refreshed. If one future-seat-03 main task already exists, it is reused. Otherwise exactly one user-visible task is created with gpt-6-astra and max reasoning. The new task chooses its own working name, role, hope, and optional pronouns. No collaboration subagent, substitute endpoint, standby record, or later owner is contacted.",
                "The new owner receives v686-v2 and is told that Vesper Arlen v686-v3 is their prospective next edge after their own terminal gate. The route then continues one verified edge at a time toward v725-v8, subject to Hamish pausing, redirecting, narrowing, or stopping it and subject to real usage, privacy, evidence, safety, duplication, and authority gates. Reset redemption remains Hamish’s action.",
            ],
        },
    ]
    write_json("final/overview-pages.json", {"schema": "ghc.family.neris.overview-pages.v1", "planned_pages": 4, "pages": pages})
    overview = "\n\n".join("# " + page["title"] + "\n\n" + "\n\n".join(page["paragraphs"]) for page in pages) + "\n"
    write_text("final/integrated-overview.md", overview)
    x2_baton = (BASE / "x2/handoff/future-seat-03-v686-v2-baton.md").read_text(encoding="utf-8")
    preface = (
        f"The immutable Neris x2 evidence is `{EVIDENCE}`. This final handoff preserves the complete evidence packet below. "
        "The exact final SHA and one-shot canonical result are supplied by the separate terminal activation. Stored repository delivery remains `PREPARED_NOT_SENT`.\n\n"
    )
    final_baton = x2_baton.replace("# 01 Identity and corrigibility\n\n", "# 01 Identity and corrigibility\n\n" + preface, 1)
    write_text("final/future-seat-03-v686-v2-baton.md", final_baton)
    write_json(
        "final/baton-integrity.json",
        {
            "words": len(final_baton.split()),
            "sections": len(re.findall(r"^# \d{2} ", final_baton, re.MULTILINE)),
            "sha256": hashlib.sha256(final_baton.encode("utf-8")).hexdigest(),
            "overview_words": len(overview.split()),
            "x2_baton_preserved": True,
            "next_owner": "future-sibling-03-self-chosen",
            "next_phase": "v686-v2",
        },
    )
    external_events = [
        {
            "id": "NS6861-POST-EVIDENCE-001",
            "failure": "Windows treated a literal ghc_family_report_*.py path as invalid during the first privacy probe",
            "recovery": "Scan the exact materialized scripts directory and preserve the wildcard miss at zero credit.",
        },
        {
            "id": "NS6861-POST-EVIDENCE-002",
            "failure": "Passing 437 exact path arguments exceeded the Windows command-line limit",
            "recovery": "Use literal Git pathspecs over stdin and preserve the original no-stage failure.",
        },
        {
            "id": "NS6861-POST-EVIDENCE-003",
            "failure": "The first pathspec-from-stdin staging pass refused five report runners outside the sparse definition",
            "recovery": "Add only the exact ghc_family_report_*.py sparse pattern, then complete and compare the same allowlist.",
        },
        {
            "id": "NS6861-POST-EVIDENCE-004",
            "failure": "The evidence commit output exceeded the display budget before its final equality projection",
            "recovery": "Read the evidence SHA and verify parent, clean state, divergence, local, upstream, tracking, and fresh live remote through scalar probes.",
        },
    ]
    overlay = {
        "effective_negatives": phase["totals"]["effective_negatives"] + len(external_events),
        "effective_methods": phase["totals"]["effective_methods"] + len(external_events),
        "failed_witnesses": phase["totals"]["failed_witnesses"] + len(external_events),
        "bounded_passing_witnesses": phase["totals"]["bounded_passing_witnesses"] + len(external_events),
        "open_gaps": phase["totals"]["open_gaps"],
        "exact_gates": phase["totals"]["exact_gates"],
    }
    write_json(
        "final/external-overlay-before-final.json",
        {
            "schema": "ghc.family.neris.external-overlay.v1",
            "repository_seal": phase["totals"],
            "events": external_events,
            "event_count": len(external_events),
            "pre_final_activation_baseline": overlay,
            "repository_bytes_rewritten": 0,
            "success_credit": 0,
        },
    )
    write_json(
        "final/phase-truth.json",
        {
            "schema": "ghc.family.neris.phase-truth.v1",
            "owner": "Neris Solane",
            "phase": "v686-v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "final": "bound_by_external_exact_final_receipt",
            "state": "FINAL_PREPARED_CANONICAL_PENDING",
            "delivery_state": "PREPARED_NOT_SENT",
            "outcomes": phase["outcomes"],
            "phase_counts": method["counts"],
            "repository_seal": phase["totals"],
            "external_overlay_before_final": overlay,
            "declared_proposal_chain": 12430,
            "priority_pillar": "Freed ID and CBR Heart",
            "real_entities": 0,
            "same_owner_only": True,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    write_json(
        "final/delivery-state.json",
        {
            "state": "PREPARED_NOT_SENT",
            "endpoint_kind": "main_task",
            "recipient": "future-sibling-03-self-chosen",
            "phase": "v686-v2",
            "create_or_reuse": "Reuse the one seat-03 task if it exists; otherwise create exactly one at the terminal gate.",
            "model": "gpt-6-astra",
            "reasoning": "max",
            "send_count": 0,
            "creation_count": 0,
            "acknowledgement": "not_yet_available",
            "subagent_created": False,
            "following_owner": "Vesper Arlen",
            "following_phase": "v686-v3",
        },
    )
    write_json(
        "final/validation-policy.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "branch": BRANCH,
            "owner": "Neris Solane",
            "phase": "v686-v1",
            "canonical_attempt_limit": 1,
            "canonical_replay_limit": 0,
            "test_modules": ["tests/test_ghc_family_neris_solane_v686_v1_x2.py", "tests/test_ghc_family_neris_solane_v686_v1_final.py"],
            "x1_tests": "Twelve checks passed before x1 commit and are retained at exact x1; they are not replayed against the x2 filesystem.",
            "scope": "Exact source-to-final Neris owner additions only",
            "materialized_file_ceiling": 2000,
            "expected_history_commits": 3,
            "expected_merges": 0,
            "final_parent": EVIDENCE,
            "same_owner_only": True,
            "source_canonical_replay_forbidden": True,
            "receipt_external_to_repository": True,
            "complete_repository_suite": False,
        },
    )
    write_json(
        "final/complete-incomplete-checklist.json",
        {
            "completed_local": [
                "200 inherited zero-credit reviews",
                "200 new report-integrity contracts",
                "1000 invalid mutations retained",
                "300 safe tasks",
                "250 candidate tasks",
                "300 additive CLEAN FIX REFINE tasks",
                "10 local and global skill packages",
                "5 unique shared report runners",
                "3 direct isolated package additions",
                "208 content-addressed cards",
                "13-section file-backed baton",
            ],
            "represented": ["10 governed-trial prerequisites", "four practice lenses", "synthetic THOS and Freed ID structures"],
            "open_gap": ["10 GMUT observation obligations", "30 blocked packets", "independent reproduction", "real governed comparison"],
            "exact_gate": ["10 CBR authority reservations", "50 exact packets", "Māori authority", "production identity and deployment", "Stage 20"],
            "pending_terminal": ["exact final commit and push", "fresh final equality", "one attributable canonical attempt", "guarded future-seat-03 creation or reuse"],
        },
    )
    write_text(
        "final/compact-activation.md",
        "# Prepared future seat 03 activation\n\nKia ora. Neris Solane v686-v1 has prepared your solo v686-v2 handoff. The terminal task creation or reuse message will supply the exact final and canonical receipt after the final gate. Read `docs/neris-solane/v686-v1/final/future-seat-03-v686-v2-baton.md` through EOF, choose your own working descriptors, preserve every failure and gate, and work only in your own D-first lane. Your prospective next edge is Vesper Arlen v686-v3 after your own terminal gate.\n",
    )
    write_json(
        "final/evidence-equality.json",
        {
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "evidence_parent": git("rev-parse", EVIDENCE + "^"),
            "evidence_branch": BRANCH,
            "evidence_clean_four_way_equal_observed": True,
            "evidence_divergence": "0\t0",
        },
    )
    tests = [
        Path("tests/test_ghc_family_neris_solane_v686_v1_x2.py"),
        Path("tests/test_ghc_family_neris_solane_v686_v1_final.py"),
    ]
    write_json(
        "final/test-definition-manifest.json",
        {
            "hash_domain": "normalized-LF test source bytes",
            "tests": [
                {
                    "path": path.as_posix(),
                    "bytes": len(normalized(path)),
                    "sha256": hashlib.sha256(normalized(path)).hexdigest(),
                }
                for path in tests
            ],
            "expected_selected_test_count": 38,
        },
    )
    print(json.dumps({"overview_words": len(overview.split()), "baton_words": len(final_baton.split()), "sections": baton_index["section_count"], "repository_seal": phase["totals"], "pre_final_overlay": overlay}, sort_keys=True))


def seal() -> None:
    required = [
        "final/overview-pages.json",
        "final/integrated-overview.md",
        "final/integrated-overview.pdf",
        "final/overview-pdf-validation.json",
        "final/overview-visual-review.json",
        "final/future-seat-03-v686-v2-baton.md",
        "final/phase-truth.json",
        "final/external-overlay-before-final.json",
    ]
    for path in required:
        if not (BASE / path).is_file():
            raise FileNotFoundError(path)
    target_paths = [
        Path("docs/neris-solane/v686-v1/validation/x1-manifest.json"),
        Path("docs/neris-solane/v686-v1/validation/evidence-manifest.json"),
        Path("docs/neris-solane/v686-v1/x2/method-flow.json"),
        Path("docs/neris-solane/v686-v1/x2/portfolio-results.json"),
        Path("docs/neris-solane/v686-v1/x2/global-promotion-installation.json"),
        Path("docs/neris-solane/v686-v1/final/future-seat-03-v686-v2-baton.md"),
        Path("docs/neris-solane/v686-v1/final/integrated-overview.md"),
        Path("docs/neris-solane/v686-v1/final/integrated-overview.pdf"),
        Path("docs/neris-solane/v686-v1/final/phase-truth.json"),
        Path("docs/neris-solane/v686-v1/final/external-overlay-before-final.json"),
    ]
    write_json(
        "final/content-seal.json",
        {
            "schema": "ghc.family.neris.content-seal.v1",
            "source": SOURCE,
            "x1": X1,
            "evidence": EVIDENCE,
            "hash_domain": "normalized-LF committed text bytes and raw PDF bytes",
            "targets": [
                {"path": path.as_posix(), "bytes": len(normalized(path)), "sha256": hashlib.sha256(normalized(path)).hexdigest()}
                for path in target_paths
            ],
        },
    )
    committed = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    status = git("status", "--porcelain=v1", "-uall").splitlines()
    uncommitted = [row[3:].replace("\\", "/") for row in status]
    final_manifest = "docs/neris-solane/v686-v1/validation/final-manifest.json"
    owner_manifest = "docs/neris-solane/v686-v1/validation/final-owner-manifest.json"
    all_paths = sorted(set(committed + uncommitted + [final_manifest, owner_manifest]))
    self_exclusions = [final_manifest, owner_manifest]
    entries = []
    for path_text in all_paths:
        if path_text in self_exclusions:
            continue
        path = Path(path_text)
        payload = normalized(path)
        entries.append({"path": path_text, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    write_json(
        "validation/final-owner-manifest.json",
        {
            "schema": "ghc.family.neris.git-blob-manifest.v1",
            "source": SOURCE,
            "hash_domain": "normalized-LF Git blob bytes for text and raw bytes for PDF",
            "entries": entries,
            "self_exclusions": self_exclusions,
        },
    )
    print(json.dumps({"content_seal_targets": len(target_paths), "owner_manifest_entries": len(entries), "owner_paths": len(all_paths)}, sort_keys=True))


def refresh_manifests() -> None:
    owner_path = BASE / "validation/final-owner-manifest.json"
    delta_path = BASE / "validation/final-manifest.json"
    if not owner_path.is_file() or not delta_path.is_file():
        raise FileNotFoundError("Both preliminary final manifests must exist")
    preliminary_sha = hashlib.sha256(owner_path.read_bytes()).hexdigest()
    committed = git("diff", "--name-only", SOURCE, "HEAD").splitlines()
    status = git("status", "--porcelain=v1", "-uall").splitlines()
    uncommitted = [row[3:].replace("\\", "/") for row in status]
    final_manifest = "docs/neris-solane/v686-v1/validation/final-manifest.json"
    owner_manifest = "docs/neris-solane/v686-v1/validation/final-owner-manifest.json"
    all_paths = sorted(set(committed + uncommitted + [final_manifest, owner_manifest]))
    exclusions = [final_manifest, owner_manifest]
    entries = []
    for path_text in all_paths:
        if path_text in exclusions:
            continue
        payload = normalized(Path(path_text))
        entries.append({"path": path_text, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()})
    owner_payload = {
        "schema": "ghc.family.neris.git-blob-manifest.v1",
        "source": SOURCE,
        "hash_domain": "normalized-LF Git blob bytes for text and raw bytes for PDF",
        "entries": entries,
        "self_exclusions": exclusions,
        "pre_reconciliation_owner_manifest_sha256": preliminary_sha,
        "reconciliation": "The preliminary owner manifest was generated before the final allowlist, preflight, staged-review, and delta manifest materialized. This additive refresh includes the three non-self validation files and preserves the preliminary digest.",
    }
    with owner_path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(owner_payload, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    owner_bytes = normalized(Path(owner_manifest))
    delta = json.loads(delta_path.read_text(encoding="utf-8"))
    matches = [row for row in delta["entries"] if row["path"] == owner_manifest]
    if len(matches) != 1:
        raise ValueError("Final delta manifest must contain one owner-manifest row")
    for row in delta["entries"]:
        payload = normalized(Path(row["path"]))
        row["bytes"] = len(payload)
        row["sha256"] = hashlib.sha256(payload).hexdigest()
    with delta_path.open("w", encoding="utf-8", newline="\n") as stream:
        json.dump(delta, stream, ensure_ascii=False, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps({"owner_entries": len(entries), "owner_paths": len(all_paths), "preliminary_sha256": preliminary_sha, "final_delta_owner_row_refreshed": True}, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["prepare", "seal", "refresh-manifests"])
    args = parser.parse_args()
    if args.mode == "prepare":
        prepare()
    elif args.mode == "seal":
        seal()
    else:
        refresh_manifests()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
