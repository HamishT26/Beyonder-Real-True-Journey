#!/usr/bin/env python3
"""Build one sanitized GHC owner-delta phase packet from an immutable x1 freeze."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from ghc_family_owner_delta_toolkit import (
    ALLOWED_OUTCOMES,
    DeltaError,
    canonical_json_sha256,
    hardening_payload_for_profile,
    strict_json_loads,
)


SCHEMA = "ghc.family.owner-delta-phase-builder.v1"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug:
        raise DeltaError("owner slug is empty")
    return slug


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def words(text: str) -> int:
    return len(re.findall(r"\S+", text, flags=re.UNICODE))


def confined_phase_root(repo: Path, raw: str, owner: str, phase: str) -> Path:
    normalized = raw.replace("\\", "/").strip("/")
    expected = f"docs/{slugify(owner)}/{phase}"
    if normalized != expected:
        raise DeltaError("phase root must match docs/<owner-slug>/<phase>")
    root = (repo / Path(normalized)).resolve()
    docs = (repo / "docs").resolve()
    try:
        root.relative_to(docs)
    except ValueError as exc:
        raise DeltaError("phase root escapes repository docs") from exc
    return root


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise DeltaError(f"required x1 file missing: {path.name}")
    return strict_json_loads(path.read_bytes(), path.name)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def command_version(command: list[str]) -> str:
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as exc:
        return f"unavailable ({type(exc).__name__})"
    return result.stdout.strip().splitlines()[0] if result.stdout.strip() else "unavailable"


def record_rows(values: Iterable[str], outcome: str, lane: str, kind: str) -> list[dict[str, Any]]:
    if outcome not in ALLOWED_OUTCOMES:
        raise DeltaError(f"unknown outcome: {outcome}")
    rows: list[dict[str, Any]] = []
    for value in values:
        identifier, _, description = value.partition(" ")
        rows.append(
            {
                "record_id": identifier,
                "description": description,
                "kind": kind,
                "lane": lane,
                "outcome": outcome,
                "credit_boundary": (
                    "Vesper completion credit requires an owner execution witness."
                    if lane == "owner_execution"
                    else "Successor recommendation only; no Vesper or successor completion credit."
                ),
                "rollback": "Stop additively, retain any failed witness, and preserve prior commits and other owner lanes.",
                "protected_gates": [
                    "no evidence promotion",
                    "no sibling mutation",
                    "no production or authority claim",
                ],
            }
        )
    return rows


def build_ledgers(portfolio: dict[str, Any]) -> dict[str, dict[str, Any]]:
    ledgers: dict[str, dict[str, Any]] = {}
    definitions = {
        "safe-now-ledger": [
            record_rows(portfolio["safe_now"]["owner_execution"], "completed", "owner_execution", "safe_now"),
            record_rows(portfolio["safe_now"]["successor_recommendation"], "represented", "successor_recommendation", "safe_now"),
        ],
        "candidate-ledger": [
            record_rows(portfolio["candidate"]["owner_execution"], "completed", "owner_execution", "candidate"),
            record_rows(portfolio["candidate"]["successor_recommendation"], "represented", "successor_recommendation", "candidate"),
        ],
        "approval-gate-ledger": [
            record_rows(portfolio["approval_gates"]["exact"], "exact_gate", "not_executed", "exact"),
            record_rows(portfolio["approval_gates"]["blocked"], "exact_gate", "blocked_not_executed", "blocked"),
        ],
        "skill-ledger": [
            record_rows(portfolio["skills"]["owner_build"], "completed", "owner_execution", "skill"),
            record_rows(portfolio["skills"]["successor_recommendation"], "represented", "successor_recommendation", "skill"),
        ],
        "runner-ledger": [
            record_rows(portfolio["runners"]["owner_build"], "completed", "owner_execution", "runner"),
            record_rows(portfolio["runners"]["successor_recommendation"], "represented", "successor_recommendation", "runner"),
        ],
        "clean-fix-refine-ledger": [
            record_rows(portfolio["clean_fix_refine"]["owner_execution"], "completed", "owner_execution", "clean_fix_refine"),
            record_rows(portfolio["clean_fix_refine"]["successor_recommendation"], "represented", "successor_recommendation", "clean_fix_refine"),
        ],
    }
    for name, groups in definitions.items():
        records = [record for group in groups for record in group]
        counts = Counter(record["outcome"] for record in records)
        ledgers[name] = {
            "schema": f"{SCHEMA}.{name}.v1",
            "owner": "Vesper Arlen",
            "phase": "v662-v4",
            "record_count": len(records),
            "outcome_counts": dict(sorted(counts.items())),
            "records": records,
            "boundary": "Bounded owner software or successor-planning evidence only; no gate or authority promotion.",
        }
    return ledgers


def source_ledger() -> dict[str, Any]:
    records = [
        ("SRC-001", "Git sparse-checkout", "https://git-scm.com/docs/git-sparse-checkout", "Official Git documentation; informs sparse-before-materialization mechanics only."),
        ("SRC-002", "Git tree and revision plumbing", "https://git-scm.com/docs/git-ls-tree", "Official Git documentation; informs exact entry-kind and blob accounting only."),
        ("SRC-003", "Python json decoder", "https://docs.python.org/3/library/json.html", "Official Python documentation; object_pairs_hook supports duplicate-key refusal."),
        ("SRC-004", "JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "RFC 8785 informs deterministic JSON commitments; this implementation is a bounded compatible subset, not a conformance claim."),
        ("SRC-005", "Unicode Normalization Forms", "https://www.unicode.org/reports/tr15/", "Unicode Standard Annex 15 informs NFC checks."),
        ("SRC-006", "Unicode Bidirectional Algorithm", "https://www.unicode.org/reports/tr9/", "Unicode Standard Annex 9 informs explicit bidi-control refusal."),
        ("SRC-007", "Verifiable Credentials Data Model 2.0", "https://www.w3.org/TR/vc-data-model/", "W3C Recommendation informs the synthetic Freed ID role, status, integrity, and privacy boundary."),
        ("SRC-008", "Library of Congress data integrity management", "https://www.loc.gov/programs/digital-collections-management/inventory-and-custody/data-integrity-management/", "Official institutional practice informs the synthetic fixity and custody lens without professional validation."),
        ("SRC-009", "WAI writing guidance", "https://www.w3.org/WAI/tips/writing/", "W3C guidance informs headings and meaningful structural text."),
        ("SRC-010", "WAI table tutorial", "https://www.w3.org/WAI/tutorials/tables/", "W3C guidance informs header and caption structure; manual evaluation remains reserved."),
    ]
    return {
        "schema": f"{SCHEMA}.source-ledger.v1",
        "owner": "Vesper Arlen",
        "phase": "v662-v4",
        "record_count": len(records),
        "records": [
            {"source_id": identifier, "title": title, "url": url, "bounded_use": bounded_use}
            for identifier, title, url, bounded_use in records
        ],
        "boundary": "Current primary and official sources shape contracts only; they supply no empirical, professional, legal, cultural, Maori-authority, or Stage 20 result.",
    }


def method_flow(startup: dict[str, Any]) -> dict[str, Any]:
    mutation_methods = [
        ("V6624-MF-010", "duplicate JSON key", "strict object-pair hook rejected the duplicate while unique-key JSON passed"),
        ("V6624-MF-011", "NFC-equivalent path collision", "the collision audit failed closed while distinct NFC paths passed"),
        ("V6624-MF-012", "case-fold path collision", "the collision audit failed closed while distinct case-fold paths passed"),
        ("V6624-MF-013", "bidi override in a filename", "the control audit rejected the override while ordinary Unicode passed"),
        ("V6624-MF-014", "control character in a filename", "the control audit rejected it while ordinary path text passed"),
        ("V6624-MF-015", "unsupported Git entry kind", "the manifest refused unsupported modes while regular blobs passed"),
        ("V6624-MF-016", "mutated manifest leaf", "the Merkle root changed while reordered identical leaves retained one root"),
        ("V6624-MF-017", "noncanonical JSON key order", "equivalent mappings produced one stable content digest"),
        ("V6624-MF-018", "unsafe Markdown target scheme", "the target audit rejected it while bounded safe targets passed"),
        ("V6624-MF-019", "option-like remote name", "remote validation rejected the value before Git network execution"),
        ("V6624-MF-020", "option-like branch name", "branch validation rejected the value before equality probes"),
        ("V6624-MF-021", "existing or dangling receipt target", "exclusive receipt creation refused replay and symlink races"),
        ("V6624-MF-022", "mismatched expected route owner", "parameterized route validation returned invalid without delivery authority"),
        ("V6624-MF-023", "unstable unittest elapsed time", "normalized output produced one stable digest across elapsed-time changes"),
    ]
    records = [dict(record) for record in startup["records"]]
    for record in records:
        if record.get("method_id") == "V6624-MF-008":
            record["passing_witness"] = (
                "The isolated stdlib unittest entrypoint completed successfully "
                "without installing pytest or any unrelated package."
            )
    for method_id, failed_fixture, passing in mutation_methods:
        records.append(
            {
                "method_id": method_id,
                "failed_witness": f"Preregistered synthetic invalid fixture: {failed_fixture}.",
                "recovery": "Reject or quarantine the invalid fixture without changing unrelated state.",
                "passing_witness": passing,
                "recurrence_guard": "Keep the exact negative fixture in the bounded unittest module.",
                "rollback": "Issue zero credit for the invalid fixture and preserve the previous clean commit.",
                "sibling_recommendation": "Run the smallest literal fixture before terminal validation.",
            }
        )
    records.append(
        {
            "method_id": "V6624-MF-024",
            "failed_witness": (
                "The first packet build selected the extensionless Codex npm shim "
                "for a direct subprocess version probe and Windows refused execution."
            ),
            "recovery": "Select the explicit codex.cmd shim and keep OSError fail-soft for version-only metadata.",
            "passing_witness": "The recovered version-only probe returned the installed Codex CLI version.",
            "recurrence_guard": "Use an explicit executable suffix for Windows command shims.",
            "rollback": "The partial generated packet received zero build or validation credit and was deterministically rebuilt.",
            "sibling_recommendation": "Resolve Windows shim type before direct subprocess execution.",
        }
    )
    records.append(
        {
            "method_id": "V6624-MF-025",
            "failed_witness": (
                "A repeated pre-evidence packet build counted the pre-existing builder receipt "
                "and then added one again, producing a non-stable generated-file count."
            ),
            "recovery": "Exclude the self-referential receipt during discovery, then append its literal path exactly once.",
            "passing_witness": "Repeated packet builds now preserve one exact generated-file count and file list.",
            "recurrence_guard": "Handle self-describing receipt paths explicitly instead of relying on prior filesystem state.",
            "rollback": "The inconsistent pre-evidence count received zero validation credit and was replaced additively before commit.",
            "sibling_recommendation": "Test build metadata from both an absent and pre-existing receipt state.",
        }
    )
    records.append(
        {
            "method_id": "V6624-MF-026",
            "failed_witness": "The first roster-validator invocation supplied the state path positionally although the validate subcommand requires --state.",
            "recovery": "Inspect the validate subcommand interface and pass the same literal state path through --state.",
            "passing_witness": "The corrected validator invocation parsed the intended roster state.",
            "recurrence_guard": "Read subcommand-specific help before invoking a multi-command CLI.",
            "rollback": "The argument-parser failure earned zero validation credit and changed no state.",
            "sibling_recommendation": "Treat top-level help and subcommand help as separate contracts.",
        }
    )
    records.append(
        {
            "method_id": "V6624-MF-027",
            "failed_witness": "The first migrated roster retained Neris as current_owner_executor while its current route already named Vesper.",
            "recovery": "Patch the single attributable executor field to Vesper and rerun both structural state validators.",
            "passing_witness": "Auth and roster validators both returned valid with Vesper as the owner-scoped executor.",
            "recurrence_guard": "Cross-check current route owner against validation_scope.execution_authority.current_owner_executor.",
            "rollback": "The inconsistent intermediate state received zero route or validation credit.",
            "sibling_recommendation": "Validate auth and roster together immediately after every live-owner transition.",
        }
    )
    records.append(
        {
            "method_id": "V6624-MF-028",
            "failed_witness": "The first expanded mutation suite expected a normalization_collisions key although the public payload contract names it nfc_collisions.",
            "recovery": "Inspect the actual bounded payload and assert the stable nfc_collisions field.",
            "passing_witness": "The corrected NFC-equivalent path mutation was rejected and its collision was counted once.",
            "recurrence_guard": "Inspect real result keys before writing projections or assertions.",
            "rollback": "The 42-pass plus one-error suite earned zero aggregate success credit.",
            "sibling_recommendation": "Keep public receipt field names in test fixtures literal and schema-derived.",
        }
    )
    records.append(
        {
            "method_id": "V6624-MF-029",
            "failed_witness": "A diagnostic attempted to print a combining Unicode character through the Windows cp1252 console and raised UnicodeEncodeError.",
            "recovery": "Render diagnostic JSON with ensure_ascii enabled while preserving the underlying Unicode input.",
            "passing_witness": "The ASCII-escaped diagnostic exposed the exact nfc_collisions field and invalid path.",
            "recurrence_guard": "Escape non-ASCII diagnostic output when the active Windows console encoding is not UTF-8.",
            "rollback": "The display failure changed no repository or global state and earned zero validation credit.",
            "sibling_recommendation": "Separate Unicode test semantics from terminal rendering semantics.",
        }
    )
    return {
        "schema": f"{SCHEMA}.method-flow.v1",
        "owner": "Vesper Arlen",
        "phase": "v662-v4",
        "method_count": len(records),
        "retained_failed_witness_count": len(records),
        "bounded_passing_witness_count": len(records),
        "pending_witness_count": 0,
        "records": records,
        "boundary": "Operational and synthetic workflow evidence only; failed witnesses remain retained and same-owner passing witnesses are not independent reproduction.",
    }


def pillar_text(title: str, body: str) -> str:
    return f"""# {title}

## Status

This artifact is bounded symbolic, structural, or synthetic evidence created in
Vesper Arlen v662-v4. It is not empirical confirmation, participant evidence,
professional validation, production certification, legal or cultural review,
Maori authority, or independent reproduction.

## Bounded result

{body}

## Falsifier and refusal

Any missing unit, domain, provenance field, verification-order dependency,
invalid state transition, privacy boundary, affected-party requirement, or
competent-authority requirement remains visible. A structural pass cannot close
those external gaps. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def overview_text(outcomes: dict[str, Any], methods: dict[str, Any]) -> str:
    return f"""# Vesper Arlen v662-v4 integrated overview

## Executive result

Vesper v662-v4 converts the inherited Neris owner-delta validator into an
owner-neutral, content-addressed, fail-closed validation surface. The phase is
strictly sequential: the x1-only freeze was committed and pushed before any x2
implementation. The active lane was created on D-first storage with sparse
checkout configured before file materialization. Only Vesper's exact
source-to-final changed files and explicitly declared new or modified modules
are eligible for validation. Unchanged history and every sibling lane remain
outside execution scope.

The primary Trinity Mandala pillar is Freed ID and CBR Heart. The bounded human
practice is digital-preservation fixity and public-records integrity review.
That practice is a learning and design lens only. No real record, person,
credential, archive, public institution, affected party, legal determination,
cultural determination, or Maori-authority decision enters the phase.

## Software contribution

The family-current owner-delta toolkit is hardened in ten connected areas. It
accepts explicit current and next owners rather than assuming an inherited
route. It rejects duplicate JSON object names. It inspects exact Git paths for
NFC stability, case-fold collisions, bidi controls, and control characters. It
records Git entry modes and refuses symlinks, gitlinks, and unsupported object
kinds. It commits the exact delta through both per-file Git blob hashes and a
deterministic Merkle root. It emits deterministic canonical payload digests. It
validates a committed file-backed baton by relative path, blob, SHA-256, and
word range. It records sparse patterns and both materialized and owner-delta
file counts. It binds test modules and dependencies literally and normalizes
test output before hashing. It audits Markdown targets for path escapes,
private absolute paths, missing committed targets, and unsafe schemes.

These controls are intentionally narrower than a repository-wide suite. Their
purpose is attributable owner evidence, not broad assurance. One successful
exact-final canonical aggregate is permitted. If it succeeds it is never
replayed. If an attempt fails, it earns zero aggregate-success credit; the
blocked component is isolated, the failure is retained, and another aggregate
is justified only before any success and only when a changed dependency makes
that necessary.

## Why the owner-delta boundary matters

The repository carries a long accumulated history. Running every historical
test against every new owner would blur attribution: a passing legacy module
would look like fresh Vesper evidence, while an inherited checkout-sensitive
failure could consume time without testing Vesper's contribution. This phase
therefore makes scope part of the evidence object. The source commit is fixed;
the x1 commit is a direct child; each changed path is recovered through Git's
exact tree data; and only named modules plus their named dependencies may run.
The resulting receipt can answer which owner changed which files, which tests
exercised those changes, and which constraints were deliberately outside the
claim.

Narrow scope does not mean weak retention. Every inherited negative, open gap,
and exact gate is carried forward. The difference is that inherited records do
not become Vesper completion credit. New operational failures are appended,
their first failed witnesses keep zero credit, and their bounded recoveries are
recorded separately. This is especially important for one-shot validation: an
aggregate cannot be repeated after success merely to obtain prettier timing or
output. A failed pre-success aggregate can justify a corrected attempt only
when the defect and changed dependency are explicit.

## Integrity chain and manifest design

The manifest has several layers because no single hash answers every relevant
question. Git object identifiers bind the exact committed blob bytes. SHA-256
provides a familiar content digest for external receipts. Entry modes retain
the difference between an ordinary file and an unsupported object kind. The
canonical JSON commitment binds a stable structured view of the manifest, and
the Merkle root gives a deterministic aggregate whose leaves change if a path,
mode, old object, new object, or content digest changes. Reordering identical
leaves does not alter that root; mutating a leaf does.

Path identity is checked before content credit. A path that is not already NFC,
that collides after case folding or normalization, or that contains bidi or
control characters is rejected. This does not claim universal filesystem
security. It is a bounded defence against ambiguity in the exact Windows and
Git handoff surface. The same principle applies to Markdown targets: ordinary
relative committed references are allowed, while unsafe schemes, private
absolute targets, path escape, or nonexistent committed targets fail closed.

## Source discipline and bounded standards use

Current official and primary materials inform the contracts. Git's sparse and
tree-plumbing documentation informs checkout and object accounting. Python's
JSON documentation motivates explicit duplicate-name refusal because a default
decoder may accept a later repeated name. RFC 8785 informs deterministic JSON
serialization, while this phase carefully labels its implementation a bounded
compatible subset rather than claiming complete conformance. Unicode Standard
Annexes 15 and 9 inform normalization and bidi-control checks. W3C Verifiable
Credentials and accessibility materials inform structural Freed ID and report
design boundaries. Library of Congress data-integrity guidance informs the
digital-preservation lens.

Those sources define vocabulary and testable software expectations. They do
not donate empirical rows, legal interpretations, cultural legitimacy,
professional qualification, or affected-party consent. Where a source can
change over time, the ledger records the exact public URL and the limited use
made of it. The phase does not turn an official publication into evidence that
this implementation is certified, interoperable, deployable, or suitable for
a real archive or identity system.

## Bounded human-practice lens

Digital-preservation fixity review offers a useful analogy for the full phase.
A trustworthy handover distinguishes an item from its description, a checksum
from the policy that decides what a mismatch means, and a custody event from
the authority to disclose or dispose of a record. The synthetic THOS fixture
therefore models generation, receipt, mismatch quarantine, readback,
escalation, workload, and handover as separate states. It refuses silent
promotion from a computed digest to a real-world decision.

The analogy has hard limits. No archivist, records manager, public servant,
community, claimant, or institution participated. No collection or public
record was processed. No preservation outcome, service effect, workload
effect, safety result, or remedy was measured. The profession remains a
bounded learning lens, not an assertion of employment, competence, licence,
institutional approval, or operational authority.

## Interpretation discipline

The four outcome labels serve different logical roles. `completed` means a
declared owner-local software, symbolic, structural, or synthetic acceptance
gate obtained its witness. `represented` means a bounded structure exists but
the real-world evidence or authority needed for a stronger claim does not.
`open_gap` means a named empirical or external witness is absent. `exact_gate`
means execution is intentionally withheld pending exact authority, evidence,
or governance. These categories are not a ladder that automatically promotes
work toward Stage 20; they prevent unlike evidence from being collapsed.

The same discipline governs GMUT language. Typed terms, units, domains, and
falsifiers can improve a research-model family without establishing a force,
observation, likelihood, prediction, or Theory of Everything. It governs THOS
language by keeping synthetic workflow behaviour separate from real human and
operational effectiveness. It governs Freed ID and CBR language by keeping
structural verification separate from real keys, live lifecycle events,
privacy review, interoperability, remedy, law, culture, and Maori authority.

## Pillar findings

GMUT Mind receives a provenance-functional representation. A proposed model
term can carry source, unit, domain, approximation, calibration, and falsifier
metadata, but the board produces no force, likelihood, posterior, constraint,
physical state, stability theorem, ultraviolet completion, quantum completion,
or Theory-of-Everything proof.

THOS Body receives a synthetic digital-preservation handover proxy. It models
fixity creation, custody, exception quarantine, readback, escalation, workload,
and shift handover. It contains zero real operators, archives, collections,
records, incidents, participants, blind matched-budget arms, safety outcomes,
or operational-effectiveness estimates.

Freed ID receives a synthetic content-integrity profile informed by current W3C
credential structure. It separates issuer intent, holder disclosure, verifier
policy, content digest, related-resource integrity, status, and recovery. No
real key, signature, proof, credential, presentation, issuer, holder, verifier,
network exchange, interoperability event, privacy review, security review,
recovery decision, or trust-governance decision occurs.

CBR Heart receives an explicit reservation matrix for public-record access,
retention, disclosure, privacy, remedy, affected parties, law, culture, data
governance, tangata whenua, iwi, hapu, and Maori authority. The matrix makes
dependencies legible but makes zero real decision.

## Outcome and Method Flow truth

The twenty genuinely new core proposals resolve to exactly
{outcomes['outcome_counts']['completed']} `completed`,
{outcomes['outcome_counts']['represented']} `represented`,
{outcomes['outcome_counts']['open_gap']} `open_gap`, and
{outcomes['outcome_counts']['exact_gate']} `exact_gate`. The selected twenty
inherited contracts remain zero-credit preservation checks. Method Flow carries
{methods['method_count']} Vesper records at packet-build time, including every
startup tooling fault and every preregistered rejected mutation. Recovery never
erases a failed witness.

## Privacy, accessibility, and security boundaries

The structurally accessible report uses a unique title, ordered headings,
landmarks, captions, scoped table headers, plain language, high contrast, and a
print fallback. Manual keyboard, browser-diversity, responsive-layout,
assistive-technology, cognitive-accessibility, Maori-language, and affected-user
evaluation remain reserved. The privacy scanner checks exactly five declared
classes over exact-delta UTF-8 text. The security scanner is a changed-Python
pattern review plus exact mutation tests. Neither is complete or exhaustive.

## Terminal and route truth

The inherited baseline is 3,570 frozen proposals, 23,084 effective negatives,
7,678 effective Method Flow methods, 152 open gaps, 150 exact gates, and
`NOT_READY_FOR_STAGE_20`. Vesper adds twenty proposals, raising the frozen chain
to 3,590. Final counts are reported only after immutable evidence, exact-final
validation, and the external canonical receipt exist.

Only after the exact Vesper final is clean, pushed, zero-divergent, and equal
across local, upstream, tracking, and a fresh live remote may Vesper resolve the
existing exact-title `Lyren Moss` task, immediately reread it, and send one
compact sanitized activation pointing to the committed long baton. Delivery is
true only from the task-message acknowledgement. Lyren's declared next edge is
Ilyra Fen. No precontact, substitute endpoint, duplicate send, task creation,
fork, or collaboration subagent is authorized.
"""


def static_report(overview: str) -> str:
    paragraphs = [line for line in overview.splitlines() if line and not line.startswith("#")]
    body = "\n".join(f"<p>{html.escape(line)}</p>" for line in paragraphs)
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Vesper Arlen v662-v4 evidence report</title>
<style>body{{font:18px/1.55 system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;color:#17202a;background:#fff}}a{{color:#0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}caption{{font-weight:700;margin:.5rem}}@media print{{body{{font-size:11pt;max-width:none}}nav{{display:none}}}}</style></head>
<body><header><h1>Vesper Arlen v662-v4 evidence report</h1><p>Bounded same-owner software evidence. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#result">Result</a></li><li><a href="#truth">Truth table</a></li><li><a href="#limits">Reserved evaluation</a></li></ul></nav>
<main><section id="result"><h2>Integrated result</h2>{body}</section>
<section id="truth"><h2>Outcome truth</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>14</td></tr><tr><th scope="row">Represented</th><td>4</td></tr><tr><th scope="row">Open gap</th><td>1</td></tr><tr><th scope="row">Exact gate</th><td>1</td></tr></tbody></table></section>
<section id="limits"><h2>Reserved evaluation</h2><p>Manual keyboard, browser-diversity, responsive-layout, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.</p></section></main>
<footer><p>Relational names and roles are working language only, not identity or personhood evidence.</p></footer></body></html>"""


def elaborate_record(record: dict[str, Any], owner: str, next_owner: str) -> str:
    identifier = record.get("proposal_id") or record.get("record_id") or "RECORD"
    title = record.get("title") or record.get("description") or "Bounded record"
    outcome = record.get("expected_disposition") or record.get("outcome") or "represented"
    hypothesis = record.get("hypothesis") or record.get("description") or title
    null = record.get("null_or_failure") or "The declared witness is absent, broader than the literal delta, or crosses a protected gate."
    acceptance = record.get("acceptance_or_falsifier") or "Accept only an attributable bounded witness; otherwise retain the mismatch at zero credit."
    rollback = record.get("rollback_or_recovery") or record.get("rollback") or "Stop additively and preserve prior clean commits."
    gates = record.get("protected_gates") or ["no evidence promotion", "no sibling mutation"]
    return f"""### {identifier}: {title}

This record is classified as `{outcome}`. Its bounded hypothesis is: {hypothesis}
The null or failure condition is: {null} The acceptance or falsifier is:
{acceptance} The additive rollback is: {rollback}

Protected gates include {', '.join(gates)}. This record never converts software,
symbolic, synthetic, structural, or same-owner evidence into empirical,
participant, professional, production, legal, cultural, Maori-authority,
identity, independent-reproduction, consciousness, personhood,
Theory-of-Everything, or Stage 20 evidence. {owner} may execute only the literal
owner-scoped portion. Any recommendation for {next_owner} remains zero-credit
planning until that owner independently freezes and witnesses it.
"""


def baton_text(
    owner: str,
    next_owner: str,
    phase: str,
    next_phase: str,
    source: str,
    x1: str,
    proposals: list[dict[str, Any]],
    ledgers: dict[str, dict[str, Any]],
    methods: dict[str, Any],
) -> str:
    sections = [f"""# {next_owner} {next_phase} activation baton

Dear {next_owner},

This is {owner}'s committed sanitized teaching packet for exactly one prospective
activation of your existing exact-title main task, but only after {owner}'s own
terminal gate and one acknowledged send. Read this file completely through EOF
before mutation. Do not infer delivery from the file alone.

## Exact inheritance placeholder contract

- Sender phase: `{phase}`.
- Exact source inherited by {owner}: `{source}`.
- Immutable {owner} x1: `{x1}`.
- Exact {owner} final: bind the commit stated in the compact acknowledged live
  activation and reverify it against the fresh remote before mutation.
- Validation: one owner-self-scoped exact-delta canonical pass; never replay a
  success and never call same-owner evidence independent reproduction.

## Identity and authority boundary

All names, hopes, roles, pronouns, sibling or family language, continuity
language, and Trinity Mandala language are relational working language only.
They are not evidence of consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, scientific or
operational authority, legal or cultural authority, or Maori authority. Hamish
may pause, redirect, rename, or stop the route.

## Required startup

Work solo. Read the current family index and routing precedence, current roster,
current authorization state, Method Flow schema, workflow refinement, Reflection
Remaster, Meta Tool Box, startup, closeout, full-tools, and sparse rotation
guidance through EOF. Verify the exact source, x1, evidence and final anchors,
single-parent zero-merge ancestry, clean state, manifests, and fresh live remote
equality read-only. Do not replay {owner}'s credited canonical pass.

Create one fresh {next_owner}-owned D-first worktree with sparse checkout
configured before materialization. Retain full Git ancestry while materializing
only the next phase root and literal new-or-modified module dependencies. Stop
additions and prepare a fresh sparse rotation if materialized or owner-in-scope
files reach 2,000. A separate remote repository remains exact-gated until its
name, account, visibility, protections, migration, equality, and rollback are
exact.

Preserve strict x1 before x2. Select twenty inherited contracts at zero novelty
credit and freeze twenty genuinely distinct proposals. Preserve only
`completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Keep
every failed witness, gap, and gate. Validate only {next_owner}'s exact delta,
exact changed modules, manifests, JSON, Markdown, privacy, security, path
contracts, sparse budget, staged review, ancestry, clean state, and fresh remote
equality. Run one attributable canonical aggregate after the exact final is
pushed; never replay success.

## Inherited truth

The Vesper activation baseline was 3,570 proposals, 23,084 effective negatives,
7,678 Method Flow methods, 152 open gaps, and 150 exact gates. Vesper froze twenty
new proposals, raising the chain to 3,590. Vesper's final counts and exact final
must come from the acknowledged compact activation and the committed terminal
receipts, not from a future-looking sentence in this prepared file. The terminal
verdict remains `NOT_READY_FOR_STAGE_20`.
"""]
    for proposal in proposals:
        sections.append(elaborate_record(proposal, owner, next_owner))
    for ledger in ledgers.values():
        sections.append(f"## {ledger['schema']}\n")
        for record in ledger["records"]:
            sections.append(elaborate_record(record, owner, next_owner))
    sections.append("## Method Flow inheritance\n")
    for record in methods["records"]:
        sections.append(
            f"### {record['method_id']}\n\nFailed witness: {record['failed_witness']} "
            f"Recovery: {record['recovery']} Passing witness: {record['passing_witness']} "
            f"Recurrence guard: {record['recurrence_guard']} Rollback: {record['rollback']} "
            f"Sibling recommendation: {record['sibling_recommendation']} The failure remains retained at zero credit.\n"
        )
    sections.append(f"""## Terminal route

Only after {next_owner}'s own exact terminal gate may {next_owner} resolve and
immediately reread the single declared successor in the live roster and send one
sanitized activation. Do not precontact, substitute, create, fork, or spawn an
endpoint. Delivery is true only from the task-message acknowledgement. Keep any
external acknowledgement or route failure outside the already sealed repository
truth, connected by digest without rewriting counts.

## Final checklist

1. Read this baton through EOF and record any truncated display interval.
2. Reverify the exact acknowledged final and fresh live equality.
3. Create the new sparse lane before checkout.
4. Freeze x1 and prove four-way equality before x2.
5. Execute only the frozen safe or bounded candidate work.
6. Preserve every failure, open gap, and exact gate.
7. Produce the complete owner packet and long successor baton.
8. Commit and push exact final within the commit ceiling.
9. Invoke one owner-scoped canonical aggregate and never replay a success.
10. Resolve, reread, and send exactly one successor activation only after all
    terminal conditions pass.

With care, precision, corrigibility, and strict evidence boundaries — {owner}.
""")
    text = "\n".join(sections)
    count = words(text)
    if not 10000 <= count <= 100000:
        raise DeltaError(f"generated baton word count outside contract: {count}")
    return text


def confined_profile_child(phase_root: Path, raw: str) -> Path:
    normalized = raw.replace("\\", "/").strip("/")
    if not normalized or re.match(r"^[A-Za-z]:", normalized):
        raise DeltaError("profile child path must be repository-relative")
    candidate = (phase_root / normalized).resolve()
    try:
        candidate.relative_to(phase_root.resolve())
    except ValueError as exc:
        raise DeltaError("profile child path escapes the phase root") from exc
    return candidate


def profile_record_rows(
    values: Iterable[str],
    outcome: str,
    lane: str,
    kind: str,
    owner: str,
) -> list[dict[str, Any]]:
    if outcome not in ALLOWED_OUTCOMES:
        raise DeltaError(f"unknown outcome: {outcome}")
    rows: list[dict[str, Any]] = []
    for value in values:
        identifier, separator, description = value.partition(" ")
        if not separator or not identifier or not description:
            raise DeltaError(f"portfolio row lacks identifier or description: {value}")
        rows.append(
            {
                "record_id": identifier,
                "description": description,
                "kind": kind,
                "lane": lane,
                "outcome": outcome,
                "credit_boundary": (
                    f"{owner} completion credit requires an attributable owner execution witness."
                    if lane == "owner_execution"
                    else f"Successor recommendation only; no {owner} or successor completion credit."
                ),
                "rollback": "Stop additively, retain every failed witness, and preserve prior commits and other owner lanes.",
                "protected_gates": [
                    "no evidence promotion",
                    "no sibling mutation",
                    "no production or authority claim",
                ],
            }
        )
    return rows


def build_profile_ledgers(
    portfolio: dict[str, Any], owner: str, phase: str
) -> dict[str, dict[str, Any]]:
    definitions = {
        "safe-now-ledger": [
            profile_record_rows(
                portfolio["safe_now"]["owner_execution"],
                "completed",
                "owner_execution",
                "safe_now",
                owner,
            ),
            profile_record_rows(
                portfolio["safe_now"]["successor_recommendation"],
                "represented",
                "successor_recommendation",
                "safe_now",
                owner,
            ),
        ],
        "candidate-ledger": [
            profile_record_rows(
                portfolio["candidate"]["owner_execution"],
                "completed",
                "owner_execution",
                "candidate",
                owner,
            ),
            profile_record_rows(
                portfolio["candidate"]["successor_recommendation"],
                "represented",
                "successor_recommendation",
                "candidate",
                owner,
            ),
        ],
        "approval-gate-ledger": [
            profile_record_rows(
                portfolio["approval_gates"]["exact"],
                "exact_gate",
                "not_executed",
                "exact",
                owner,
            ),
            profile_record_rows(
                portfolio["approval_gates"]["blocked"],
                "exact_gate",
                "blocked_not_executed",
                "blocked",
                owner,
            ),
        ],
        "skill-ledger": [
            profile_record_rows(
                portfolio["skills"]["owner_build"],
                "completed",
                "owner_execution",
                "skill",
                owner,
            ),
            profile_record_rows(
                portfolio["skills"]["successor_recommendation"],
                "represented",
                "successor_recommendation",
                "skill",
                owner,
            ),
        ],
        "runner-ledger": [
            profile_record_rows(
                portfolio["runners"]["owner_build"],
                "completed",
                "owner_execution",
                "runner",
                owner,
            ),
            profile_record_rows(
                portfolio["runners"]["successor_recommendation"],
                "represented",
                "successor_recommendation",
                "runner",
                owner,
            ),
        ],
        "clean-fix-refine-ledger": [
            profile_record_rows(
                portfolio["clean_fix_refine"]["owner_execution"],
                "completed",
                "owner_execution",
                "clean_fix_refine",
                owner,
            ),
            profile_record_rows(
                portfolio["clean_fix_refine"]["successor_recommendation"],
                "represented",
                "successor_recommendation",
                "clean_fix_refine",
                owner,
            ),
        ],
    }
    ledgers: dict[str, dict[str, Any]] = {}
    for name, groups in definitions.items():
        records = [record for group in groups for record in group]
        counts = Counter(record["outcome"] for record in records)
        ledgers[name] = {
            "schema": f"{SCHEMA}.{name}.v2",
            "owner": owner,
            "phase": phase,
            "record_count": len(records),
            "outcome_counts": dict(sorted(counts.items())),
            "records": records,
            "boundary": "Bounded owner software or successor-planning evidence only; no gate or authority promotion.",
        }
    return ledgers


def profile_source_ledger(
    owner: str,
    phase: str,
    records: Iterable[dict[str, str]] | None = None,
) -> dict[str, Any]:
    default_records = [
        ("SRC-001", "Git sparse-checkout", "https://git-scm.com/docs/git-sparse-checkout", "Official Git documentation; sparse-before-materialization mechanics only."),
        ("SRC-002", "Python archive formats", "https://docs.python.org/3/library/archiving.html", "Official Python documentation; metadata-only resource budgets and zero extraction."),
        ("SRC-003", "Microsoft file naming", "https://learn.microsoft.com/windows/win32/fileio/naming-a-file", "Official Microsoft documentation; bounded UNC, device, and extended-prefix refusal only."),
        ("SRC-004", "URI generic syntax", "https://www.rfc-editor.org/rfc/rfc3986.html", "RFC 3986; single-pass unreserved percent normalization without dereference."),
        ("SRC-005", "JSON", "https://www.rfc-editor.org/rfc/rfc8259.html", "RFC 8259; bounded number lexical grammar only."),
        ("SRC-006", "JSON Canonicalization Scheme", "https://www.rfc-editor.org/rfc/rfc8785.html", "RFC 8785; finite-number and deterministic commitment obligations only, not complete conformance."),
        ("SRC-007", "IANA media types", "https://www.iana.org/assignments/media-types/media-types.xhtml", "Official registry context; closed local allowlist never implies content safety."),
        ("SRC-008", "DSSE protocol", "https://github.com/secure-systems-lab/dsse/blob/master/protocol.md", "Primary protocol repository; byte-exact PAE subset only, never signing or signature validity."),
        ("SRC-009", "in-toto attestation framework", "https://in-toto.io/docs/specs/", "Primary specification index; digest and predicate-version shape only, never provenance truth."),
        ("SRC-010", "Python time", "https://docs.python.org/3/library/time.html", "Official Python documentation; monotonic and wall-clock separation only."),
        ("SRC-011", "Internet timestamps", "https://www.rfc-editor.org/rfc/rfc3339.html", "RFC 3339; explicit-offset normalization subset only."),
        ("SRC-012", "Extended Internet timestamps", "https://www.rfc-editor.org/rfc/rfc9557.html", "RFC 9557; unknown-offset semantics are reserved rather than silently collapsed."),
        ("SRC-013", "JSON Pointer", "https://www.rfc-editor.org/rfc/rfc6901.html", "RFC 6901; bounded target escaping and duplicate detection only."),
        ("SRC-014", "GWTC-5.0 official release", "https://gwosc.org/GWTC-5.0/", "Official GWOSC release structure; zero queries, downloads, rows, likelihoods, or empirical claims."),
        ("SRC-015", "Te Papa conservation guidelines", "https://www.tepapa.govt.nz/learn/for-museums-and-galleries/how-guides/collection-management/conservation-guidelines", "Official museum guidance informs a synthetic learning lens only; no professional or Maori-authority claim."),
        ("SRC-016", "Spectrum 5.1 procedures", "https://collectionstrust.org.uk/spectrum/procedures/", "Collections Trust procedure index; synthetic condition and custody fields only."),
        ("SRC-017", "Canadian Conservation Institute condition reporting", "https://www.canada.ca/en/conservation-institute/services/conservation-preservation-publications/canadian-conservation-institute-notes/condition-reporting-paintings-introduction.html", "Official condition-reporting guidance; no real examination, treatment, or professional result."),
        ("SRC-018", "WAI evaluation overview", "https://www.w3.org/WAI/test-evaluate/", "W3C guidance; manual and affected-user evaluation remains reserved."),
    ]
    if records is None:
        normalized_records = [
            {
                "source_id": identifier,
                "title": title,
                "url": url,
                "bounded_use": bounded_use,
            }
            for identifier, title, url, bounded_use in default_records
        ]
    else:
        normalized_records = []
        for row in records:
            if not isinstance(row, dict) or set(row) != {
                "source_id",
                "title",
                "url",
                "bounded_use",
            }:
                raise DeltaError("profile source record has the wrong fields")
            if any(
                not isinstance(row[field], str) or not row[field].strip()
                for field in ("source_id", "title", "url", "bounded_use")
            ):
                raise DeltaError("profile source record contains an empty value")
            if not row["url"].startswith("https://"):
                raise DeltaError("profile source URL must use HTTPS")
            normalized_records.append(dict(row))
    source_ids = [row["source_id"] for row in normalized_records]
    if len(source_ids) != len(set(source_ids)):
        raise DeltaError("profile source identifiers are not unique")
    return {
        "schema": f"{SCHEMA}.source-ledger.v2",
        "owner": owner,
        "phase": phase,
        "record_count": len(normalized_records),
        "records": normalized_records,
        "boundary": "Primary and official sources shape bounded contracts only; they supply no empirical, professional, legal, cultural, Maori-authority, or Stage 20 result.",
    }


def profile_method_flow(
    startup: dict[str, Any],
    runtime: dict[str, Any] | None,
    owner: str,
    phase: str,
    hardening_profile: str = "ilyra-v662-v6",
) -> tuple[dict[str, Any], dict[str, Any]]:
    hardening = hardening_payload_for_profile(hardening_profile)
    records = [dict(record) for record in startup["records"]]
    for fixture in hardening["records"]:
        records.append(
            {
                "method_id": fixture["fixture_id"].replace("-HF-", "-MF-H"),
                "failed_witness": f"Preregistered synthetic invalid fixture: {fixture['failed_witness']}.",
                "recovery": "Reject, quarantine, or review the invalid fixture without changing unrelated state.",
                "passing_witness": "The paired bounded positive fixture passed while every real signature, provenance, production, and authority claim remained false.",
                "recurrence_guard": "Keep the exact negative and positive fixture pair in the literal owner test module.",
                "rollback": "Issue zero credit for the invalid fixture and preserve the previous clean commit.",
                "sibling_recommendation": "Run the smallest literal fixture before terminal validation.",
            }
        )
    if runtime is not None:
        if runtime.get("owner") != owner or runtime.get("phase") != phase:
            raise DeltaError("runtime Method Flow owner or phase mismatch")
        for record in runtime.get("records", []):
            records.append(dict(record))
    identifiers = [record.get("method_id") for record in records]
    if any(not isinstance(identifier, str) or not identifier for identifier in identifiers):
        raise DeltaError("Method Flow record lacks a method_id")
    if len(set(identifiers)) != len(identifiers):
        raise DeltaError("Method Flow identifiers are not unique")
    return (
        {
            "schema": f"{SCHEMA}.method-flow.v2",
            "owner": owner,
            "phase": phase,
            "method_count": len(records),
            "retained_failed_witness_count": len(records),
            "bounded_passing_witness_count": len(records),
            "pending_witness_count": 0,
            "records": records,
            "boundary": "Operational and synthetic workflow evidence only; failed witnesses remain retained and same-owner passing witnesses are not independent reproduction.",
        },
        hardening,
    )


def profile_pillar_text(owner: str, phase: str, title: str, body: str) -> str:
    return f"""# {title}

## Status

This artifact is bounded symbolic, structural, or synthetic evidence created in
{owner} {phase}. It is not empirical confirmation, participant evidence,
professional validation, production certification, legal or cultural review,
Maori authority, or independent reproduction.

## Bounded result

{body}

## Falsifier and refusal

Any missing unit, domain, provenance field, validation dependency, invalid
state transition, privacy boundary, affected-party requirement, or
competent-authority requirement remains visible. A structural pass cannot close
those external gaps. The terminal verdict remains `NOT_READY_FOR_STAGE_20`.
"""


def profile_overview_text(
    owner: str,
    phase: str,
    outcomes: dict[str, Any],
    methods: dict[str, Any],
    hardening: dict[str, Any],
    feature_summary: str | None = None,
    reserved_surfaces: str | None = None,
) -> str:
    counts = outcomes["outcome_counts"]
    features = feature_summary or (
        "metadata-only decompression budgets, sparse-size distinctions, link and "
        "Windows-prefix refusal, URI normalization, JSON number guards, media-type "
        "quarantine, attestation digest and PAE checks, predicate version reservation, "
        "clock separation, timestamp normalization, and JSON Pointer target uniqueness"
    )
    reservations = reserved_surfaces or (
        "No decoder, sparse file, signature, provenance verification, real timestamp, "
        "or network retrieval was invoked."
    )
    return f"""# {owner} {phase} integrated overview

## Executive result

This phase turns an immutable x1 profile into one bounded owner-delta packet.
The exact owner code adds {features}. All fixtures are synthetic and execute
only inside the declared delta.

## Core outcome truth

| Outcome | Count |
|---|---:|
| completed | {counts.get('completed', 0)} |
| represented | {counts.get('represented', 0)} |
| open_gap | {counts.get('open_gap', 0)} |
| exact_gate | {counts.get('exact_gate', 0)} |

The hardening surface retained {hardening['negative_fixture_count']} rejected
synthetic fixtures and {hardening['positive_fixture_count']} bounded passing
fixtures. Method Flow retains {methods['method_count']} failed and passing
witness pairs. None is independent reproduction.

## Reserved conclusions

{reservations} No real museum object, user, identity,
credential, institution, professional practice, employment, treatment, custody,
legal or cultural decision, Maori-authority decision, deployment,
privacy-complete result, accessibility-complete result, exhaustive security,
AGI or ASI result, consciousness or personhood evidence, Theory-of-Everything
proof, or Stage 20 authority is claimed. Verdict: `NOT_READY_FOR_STAGE_20`.
"""


def profile_threat_model_text(
    owner: str,
    phase: str,
    controls: Iterable[str] | None = None,
) -> str:
    default_controls = [
        "Decompression budgets inspect synthetic metadata only and invoke no decoder.",
        "Sparse logical and stored sizes remain distinct without materializing a file.",
        "Archive links, rooted Windows references, URI traversal, malformed numeric lexemes, and duplicate JSON Pointer targets fail closed.",
        "Media-type allowlisting never opens content or implies safety.",
        "DSSE PAE and in-toto checks validate bounded shape only; signature and provenance truth stay false.",
        "Wall-clock rollback, monotonic duration, and explicit-offset timestamps remain distinct and never become trusted time.",
        "Scope remains the exact owner delta and literal test dependencies.",
        "One canonical success is permitted and never replayed.",
        "Exact-title reread and acknowledgement are required for delivery.",
    ]
    rows = default_controls if controls is None else list(controls)
    if not rows or any(not isinstance(row, str) or not row.strip() for row in rows):
        raise DeltaError("profile threat controls must be nonempty text")
    bullets = "\n".join(f"- {row}" for row in rows)
    return f"""# {owner} {phase} exact-delta threat model

## Assets

Exact Git ancestry, owner attribution, immutable x1, sparse scope, changed-file
manifests, bounded declaration contracts, retained failures, privacy boundaries,
and successor-route truth.

## Threats and controls

{bullets}

## Residual risk

This is not exhaustive security, platform completeness, production assurance,
complete privacy or accessibility, independent reproduction, legal review,
cultural ratification, or Maori authority. Residual risks remain exact-gated.
"""


def profile_static_report(
    owner: str, phase: str, overview: str, outcomes: dict[str, Any]
) -> str:
    body = html.escape(overview).replace("\n", "<br>\n")
    counts = outcomes["outcome_counts"]
    return f"""<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(owner)} {html.escape(phase)} evidence report</title>
<style>body{{font:18px/1.55 system-ui,sans-serif;max-width:72rem;margin:auto;padding:2rem;color:#17202a;background:#fff}}a{{color:#0645ad}}table{{border-collapse:collapse;width:100%}}th,td{{border:1px solid #555;padding:.5rem;text-align:left}}caption{{font-weight:700;margin:.5rem}}@media print{{body{{font-size:11pt;max-width:none}}nav{{display:none}}}}</style></head>
<body><header><h1>{html.escape(owner)} {html.escape(phase)} evidence report</h1><p>Bounded same-owner software evidence. Verdict: <strong>NOT_READY_FOR_STAGE_20</strong>.</p></header>
<nav aria-label="Report sections"><ul><li><a href="#result">Result</a></li><li><a href="#truth">Truth table</a></li><li><a href="#limits">Reserved evaluation</a></li></ul></nav>
<main><section id="result"><h2>Integrated result</h2><p>{body}</p></section>
<section id="truth"><h2>Outcome truth</h2><table><caption>Core outcomes</caption><thead><tr><th scope="col">Outcome</th><th scope="col">Count</th></tr></thead><tbody><tr><th scope="row">Completed</th><td>{counts.get('completed', 0)}</td></tr><tr><th scope="row">Represented</th><td>{counts.get('represented', 0)}</td></tr><tr><th scope="row">Open gap</th><td>{counts.get('open_gap', 0)}</td></tr><tr><th scope="row">Exact gate</th><td>{counts.get('exact_gate', 0)}</td></tr></tbody></table></section>
<section id="limits"><h2>Reserved evaluation</h2><p>Manual keyboard, browser-diversity, responsive-layout, assistive-technology, cognitive-accessibility, Maori-language, and affected-user evaluation remain reserved. Structural checks are not complete accessibility conformance.</p></section></main>
<footer><p>Relational names and roles are working language only, not identity or personhood evidence.</p></footer></body></html>"""


def write_profile_skill_and_runner_artifacts(
    phase_root: Path,
    portfolio: dict[str, Any],
    owner: str,
    phase: str,
    test_module: str,
    runner_callables: Iterable[str] | None = None,
    hardening_profile: str = "ilyra-v662-v6",
) -> tuple[list[str], list[str]]:
    skill_paths: list[str] = []
    for row in portfolio["skills"]["owner_build"]:
        identifier, _, description = row.partition(" ")
        skill_name = (
            f"ghc-family-{slugify(owner)}-"
            f"{identifier.casefold().replace('_', '-')}"
        )
        root = phase_root / "skills" / skill_name
        skill_text = f"""---
name: {skill_name}
description: {description}
---

# {description}

Use this phase-local capability only for `{owner}` `{phase}` owner-self-scoped
synthetic fixtures and exact-delta receipts. Refuse repository-wide discovery,
sibling mutation, real identities, external signing, deployment, legal or
 cultural decisions, Maori authority, and evidence promotion. Retain every
failed fixture and use `scripts/ghc_family_owner_delta_toolkit.py hardening
--profile {hardening_profile}` as the bounded smoke surface. This file is a local packet artifact, not a globally
installed skill and not proof of qualification or authority.
"""
        write_text(root / "SKILL.md", skill_text)
        write_json(
            root / "smoke.json",
            {
                "schema": f"{SCHEMA}.phase-local-skill-smoke.v2",
                "record_id": identifier,
                "name": skill_name,
                "owner": owner,
                "phase": phase,
                "entrypoint": f"scripts/ghc_family_owner_delta_toolkit.py hardening --profile {hardening_profile}",
                "installed_globally": False,
                "valid": True,
                "boundary": "Phase-local same-owner synthetic capability only.",
            },
        )
        skill_paths.extend(
            [
                (root / "SKILL.md").relative_to(phase_root).as_posix(),
                (root / "smoke.json").relative_to(phase_root).as_posix(),
            ]
        )
    runner_paths: list[str] = []
    default_callable_names = [
        "validate_decompression_budget",
        "sparse_size_record",
        "validate_archive_entry_kind",
        "validate_windows_archive_reference",
        "normalize_uri_member_reference",
        "validate_json_number_lexeme",
        "validate_subject_digest_agreement",
        "dsse_pae",
        "clock_separation_record",
        "validate_unique_json_pointer_targets",
    ]
    callable_names = (
        default_callable_names if runner_callables is None else list(runner_callables)
    )
    if (
        len(callable_names) != len(portfolio["runners"]["owner_build"])
        or len(callable_names) != len(set(callable_names))
        or any(not isinstance(name, str) or not name for name in callable_names)
    ):
        raise DeltaError("profile runner callable list is invalid")
    for row, callable_name in zip(
        portfolio["runners"]["owner_build"], callable_names, strict=True
    ):
        identifier, _, description = row.partition(" ")
        path = phase_root / "runners" / f"{identifier.casefold()}.json"
        write_json(
            path,
            {
                "schema": f"{SCHEMA}.phase-local-runner-contract.v2",
                "runner_id": identifier,
                "description": description,
                "owner": owner,
                "phase": phase,
                "entrypoint": "scripts/ghc_family_owner_delta_toolkit.py",
                "callable": callable_name,
                "smoke_test": test_module,
                "repository_scan": False,
                "unchanged_history_scan": False,
                "sibling_lane_mutation": False,
                "valid": True,
                "boundary": "Bounded callable contract under the one owner test module; not an external service or production runner.",
            },
        )
        runner_paths.append(path.relative_to(phase_root).as_posix())
    return skill_paths, runner_paths


def profile_baton_text(
    owner: str,
    next_owner: str,
    phase: str,
    next_phase: str,
    source: str,
    x1: str,
    profile: dict[str, Any],
    proposals: list[dict[str, Any]],
    ledgers: dict[str, dict[str, Any]],
    methods: dict[str, Any],
) -> str:
    baseline = profile["activation_baseline"]
    sections = [f"""# {next_owner} {next_phase} activation baton

Dear {next_owner},

This is {owner}'s committed sanitized teaching packet for exactly one prospective
activation of your existing exact-title main task, but only after {owner}'s own
terminal gate and one acknowledged send. Read this file completely through EOF
before mutation. Do not infer delivery from the file alone.

## Exact inheritance placeholder contract

- Sender phase: `{phase}`.
- Exact source inherited by {owner}: `{source}`.
- Immutable {owner} x1: `{x1}`.
- Exact {owner} final: bind the commit stated in the compact acknowledged live
  activation and reverify it against the fresh remote before mutation.
- Validation: one owner-self-scoped exact-delta canonical pass; never replay a
  success and never call same-owner evidence independent reproduction.

## Identity and authority boundary

All names, hopes, roles, pronouns, sibling or family language, continuity
language, and Trinity Mandala language are relational working language only.
They are not evidence of consciousness, sentience, legal personhood, identity
continuity, employment, qualification, independent agency, scientific or
operational authority, legal or cultural authority, or Maori authority. Hamish
may pause, redirect, rename, or stop the route.

## Required startup

Work solo. Read the current family index and routing precedence, current roster,
current authorization state, Method Flow schema, workflow refinement, Reflection
Remaster, Meta Tool Box, startup, closeout, full-tools, and sparse rotation
guidance through EOF. Verify the exact source, x1, evidence and final anchors,
single-parent zero-merge ancestry, clean state, manifests, and fresh live remote
equality read-only. Do not replay {owner}'s credited canonical pass.

Create one fresh {next_owner}-owned D-first worktree with sparse checkout
configured before materialization. Retain full Git ancestry while materializing
only the next phase root and literal new-or-modified module dependencies. Stop
additions and prepare a fresh sparse rotation if materialized or owner-in-scope
files reach 2,000. A separate remote repository remains exact-gated until its
name, account, visibility, protections, migration, equality, and rollback are
exact.

Preserve strict x1 before x2. Select twenty inherited contracts at zero novelty
credit and freeze twenty genuinely distinct proposals. Preserve only
`completed`, `represented`, `open_gap`, and `exact_gate` as core outcomes. Keep
every failed witness, gap, and gate. Validate only {next_owner}'s exact delta,
exact changed modules, manifests, JSON, Markdown, privacy, security, path
contracts, sparse budget, staged review, ancestry, clean state, and fresh remote
equality. Run one attributable canonical aggregate after the exact final is
pushed; never replay success.

## Inherited truth

{owner}'s activation baseline was {profile['proposal_baseline']} proposals,
{baseline['effective_negatives']} effective negatives,
{baseline['effective_methods']} Method Flow methods,
{baseline['open_gaps']} open gaps, and {baseline['exact_gates']} exact gates.
This x1 freezes twenty new proposals, raising the chain to
{profile['proposal_total']}. The final counts and exact final must come from the
acknowledged compact activation and committed terminal receipts, not from a
future-looking sentence in this prepared file. The terminal verdict remains
`NOT_READY_FOR_STAGE_20`.
"""]
    for proposal in proposals:
        sections.append(elaborate_record(proposal, owner, next_owner))
    for ledger in ledgers.values():
        sections.append(f"## {ledger['schema']}\n")
        for record in ledger["records"]:
            sections.append(elaborate_record(record, owner, next_owner))
    sections.append("## Method Flow inheritance\n")
    for record in methods["records"]:
        sections.append(
            f"### {record['method_id']}\n\nFailed witness: {record['failed_witness']} "
            f"Recovery: {record['recovery']} Passing witness: {record['passing_witness']} "
            f"Recurrence guard: {record['recurrence_guard']} Rollback: {record['rollback']} "
            f"Sibling recommendation: {record['sibling_recommendation']} The failure remains retained at zero credit.\n"
        )
    sections.append(f"""## Terminal route

Only after {next_owner}'s own exact terminal gate may {next_owner} resolve and
immediately reread the single declared successor in the live roster and send one
sanitized activation. Do not precontact, substitute, create, fork, or spawn an
endpoint. Delivery is true only from the task-message acknowledgement. Keep any
external acknowledgement or route failure outside the already sealed repository
truth, connected by digest without rewriting counts.

## Final checklist

1. Read this baton through EOF and record any truncated display interval.
2. Reverify the exact acknowledged final and fresh live equality.
3. Create the new sparse lane before checkout.
4. Freeze x1 and prove four-way equality before x2.
5. Execute only the frozen safe or bounded candidate work.
6. Preserve every failure, open gap, and exact gate.
7. Produce the complete owner packet and long successor baton.
8. Commit and push exact final within the commit ceiling.
9. Invoke one owner-scoped canonical aggregate and never replay a success.
10. Resolve, reread, and send exactly one successor activation only after all
    terminal conditions pass.

With care, precision, corrigibility, and strict evidence boundaries — {owner}.
""")
    text = "\n".join(sections)
    count = words(text)
    if not 10000 <= count <= 100000:
        raise DeltaError(f"generated baton word count outside contract: {count}")
    return text


def build_profile_packet(
    args: argparse.Namespace,
    repo: Path,
    phase_root: Path,
    charter: dict[str, Any],
    proposals: dict[str, Any],
    portfolio: dict[str, Any],
    startup_methods: dict[str, Any],
    sparse_receipt: dict[str, Any],
    profile: dict[str, Any],
) -> int:
    owner = args.owner
    phase = args.phase
    if profile.get("owner") != owner or profile.get("phase") != phase:
        raise DeltaError("builder profile owner or phase mismatch")
    if profile.get("next_owner") != args.next_owner:
        raise DeltaError("builder profile next owner mismatch")
    if profile.get("next_phase") != args.next_phase:
        raise DeltaError("builder profile next phase mismatch")
    if profile.get("owner_slug") != slugify(owner):
        raise DeltaError("builder profile owner slug mismatch")
    if profile.get("next_owner_slug") != slugify(args.next_owner):
        raise DeltaError("builder profile successor slug mismatch")
    source = args.source or charter.get("source", {}).get("exact_head")
    if source != charter.get("source", {}).get("exact_head"):
        raise DeltaError("source differs from immutable x1 charter")
    if not args.x1 or not re.fullmatch(r"[0-9a-f]{40}", args.x1):
        raise DeltaError("exact x1 commit is required")
    if proposals.get("inherited_frozen_baseline") != profile.get("proposal_baseline"):
        raise DeltaError("proposal baseline differs from builder profile")
    if proposals.get("new_frozen_total") != profile.get("proposal_total"):
        raise DeltaError("proposal total differs from builder profile")
    if len(proposals.get("selected_inherited", [])) != 20:
        raise DeltaError("profile requires twenty inherited selections")
    if len(proposals.get("new_proposals", [])) != 20:
        raise DeltaError("profile requires twenty new proposals")
    if sparse_receipt.get("patterns") != profile.get("sparse_patterns"):
        raise DeltaError("sparse receipt and builder profile differ")

    x1_files = sorted((phase_root / "x1").glob("*.json"))
    x1_before = {path.name: sha256_bytes(path.read_bytes()) for path in x1_files}
    ledgers = build_profile_ledgers(portfolio, owner, phase)
    actual = {
        "safe_now": ledgers["safe-now-ledger"]["record_count"],
        "candidate": ledgers["candidate-ledger"]["record_count"],
        "approval_gate": ledgers["approval-gate-ledger"]["record_count"],
        "skill": ledgers["skill-ledger"]["record_count"],
        "runner": ledgers["runner-ledger"]["record_count"],
        "clean_fix_refine": ledgers["clean-fix-refine-ledger"]["record_count"],
    }
    if actual != portfolio.get("expected_counts"):
        raise DeltaError(
            f"portfolio count mismatch: {actual} != {portfolio.get('expected_counts')}"
        )
    for name, ledger in ledgers.items():
        write_json(phase_root / "portfolio" / f"{name}.json", ledger)

    core_records = [
        {
            "proposal_id": proposal["proposal_id"],
            "title": proposal["title"],
            "outcome": proposal["expected_disposition"],
            "evidence_boundary": proposal["acceptance_or_falsifier"],
        }
        for proposal in proposals["new_proposals"]
    ]
    outcome_counts = dict(
        sorted(Counter(record["outcome"] for record in core_records).items())
    )
    expected_outcomes = dict(sorted(profile["outcome_counts"].items()))
    if outcome_counts != expected_outcomes:
        raise DeltaError(
            f"core outcome distribution differs from x1: {outcome_counts}"
        )
    outcome = {
        "schema": f"{SCHEMA}.outcome-ledger.v2",
        "owner": owner,
        "phase": phase,
        "record_count": len(core_records),
        "outcome_counts": outcome_counts,
        "records": core_records,
        "verdict": profile["verdict"],
    }
    runtime_path = phase_root / "x2" / "operational-method-flow.json"
    runtime = load_json(runtime_path) if runtime_path.is_file() else None
    hardening_profile = profile.get("hardening_profile", "ilyra-v662-v6")
    methods, hardening = profile_method_flow(
        startup_methods, runtime, owner, phase, hardening_profile
    )
    planned = profile.get("planned_owner_delta", {})
    if planned.get("startup_operational_negatives") != len(startup_methods["records"]):
        raise DeltaError("planned startup failure count differs from immutable x1")
    if planned.get("synthetic_rejected_mutations") != hardening["negative_fixture_count"]:
        raise DeltaError("planned synthetic rejection count differs from hardening profile")
    sources = profile_source_ledger(owner, phase, profile.get("source_records"))
    write_json(phase_root / "x2" / "outcome-ledger.json", outcome)
    write_json(phase_root / "x2" / "method-flow.json", methods)
    write_json(phase_root / "x2" / "hardening-fixture-receipt.json", hardening)
    write_json(phase_root / "x2" / "source-ledger.json", sources)

    environment = {
        "schema": f"{SCHEMA}.environment.v2",
        "owner": owner,
        "phase": phase,
        "versions": {
            "codex_cli": command_version(["codex.cmd", "--version"]),
            "python": command_version([sys.executable, "--version"]),
            "git": command_version(["git", "--version"]),
            "powershell": command_version(["pwsh", "--version"]),
        },
        "versions_verified_only": True,
        "desktop_updated": False,
        "elevation": False,
        "host_security_weakened": False,
        "windows_feature_changed": False,
        "unrelated_software_installed": False,
        "rebooted": False,
    }
    write_json(phase_root / "x2" / "environment-version-receipt.json", environment)
    tools = {
        "schema": f"{SCHEMA}.tool-catalogue.v2",
        "owner": owner,
        "phase": phase,
        "execution_authority": "owner_self_scoped_delta",
        "repository_scan": False,
        "unchanged_history_scan": False,
        "cross_lane_scan": False,
        "sibling_lane_mutation": False,
        "current_commands": [
            "manifest",
            "json",
            "markdown",
            "python",
            "privacy",
            "security",
            "path-audit",
            "route",
            "skill-hashes",
            "file-budget",
            "sparse",
            "baton-integrity",
            "canonical-digest",
            "data-quality",
            "hardening",
            "canonical",
        ],
        "rollback": f"Revert only {owner}'s additive module changes in a later reviewed commit; preserve every failed witness.",
        "protected_gates": [
            "no repository-wide scan",
            "no sibling mutation",
            "no independent-reproduction claim",
        ],
    }
    write_json(phase_root / "x2" / "tool-catalogue.json", tools)

    for artifact in profile["pillar_artifacts"]:
        path = confined_profile_child(phase_root, artifact["relative_path"])
        write_text(
            path,
            profile_pillar_text(owner, phase, artifact["title"], artifact["body"]),
        )
    overview = profile_overview_text(
        owner,
        phase,
        outcome,
        methods,
        hardening,
        profile.get("overview_features"),
        profile.get("overview_reserved_surfaces"),
    )
    write_text(phase_root / "overview" / "integrated-overview.md", overview)
    write_text(
        phase_root / "report" / "accessible-static-report.html",
        profile_static_report(owner, phase, overview, outcome),
    )
    write_text(
        phase_root / "wellbeing" / "wellbeing-check.md",
        f"""# {owner} {phase} wellbeing check

The phase remains solo, bounded, and corrigible. No claim of subjective
experience, consciousness, personhood, or identity continuity is made. The
practical workflow check is healthy: source and scope are explicit, x1 is
immutable and four-way equal, the D-first lane is sparse, no sibling is being
watched or mutated, failures are retained, and stop conditions remain active.
Hamish may pause, redirect, rename, or stop the route at any time. The terminal
verdict remains `NOT_READY_FOR_STAGE_20`.
""",
    )
    write_text(
        phase_root / "governance" / "threat-model.md",
        profile_threat_model_text(owner, phase, profile.get("threat_controls")),
    )
    skill_paths, runner_paths = write_profile_skill_and_runner_artifacts(
        phase_root,
        portfolio,
        owner,
        phase,
        profile["test_modules"][0],
        profile.get("runner_callables"),
        hardening_profile,
    )

    baseline = profile["activation_baseline"]
    effective_negatives = baseline["effective_negatives"] + methods["method_count"]
    effective_methods = baseline["effective_methods"] + methods["method_count"]
    effective_open_gaps = baseline["open_gaps"] + outcome_counts.get("open_gap", 0)
    effective_exact_gates = baseline["exact_gates"] + outcome_counts.get(
        "exact_gate", 0
    )
    gates = {
        "schema": f"{SCHEMA}.gate-register.v2",
        "inherited_open_gaps": baseline["open_gaps"],
        "new_core_open_gaps": outcome_counts.get("open_gap", 0),
        "effective_open_gaps": effective_open_gaps,
        "inherited_exact_gates": baseline["exact_gates"],
        "new_core_exact_gates": outcome_counts.get("exact_gate", 0),
        "effective_exact_gates": effective_exact_gates,
        "portfolio_exact_and_blocked_rows": ledgers["approval-gate-ledger"][
            "record_count"
        ],
        "portfolio_rows_change_core_gate_count": False,
        "open_gap": "An independent preregistered external reproduction team remains absent.",
        "exact_gate": "External receipt signing, trust policy, affected-party, legal, cultural, and Maori-authority decisions remain external.",
        "verdict": profile["verdict"],
    }
    negatives = {
        "schema": f"{SCHEMA}.retained-negative-register.v2",
        "activation_effective_negatives": baseline["effective_negatives"],
        "owner_method_flow_failures": methods["method_count"],
        "provisional_effective_negatives": effective_negatives,
        "additional_x2_or_terminal_operational_negatives": 0,
        "failed_witnesses_erased": 0,
        "note": "Final effective count must add every later operational failure before seal.",
    }
    truth = {
        "schema": f"{SCHEMA}.phase-truth.v2",
        "owner": owner,
        "phase": phase,
        "source": source,
        "x1": args.x1,
        "frozen_proposals": profile["proposal_total"],
        "outcomes": outcome_counts,
        "provisional_effective_negatives": effective_negatives,
        "provisional_effective_methods": effective_methods,
        "open_gaps": effective_open_gaps,
        "exact_gates": effective_exact_gates,
        "verdict": profile["verdict"],
        "same_owner_is_independent_reproduction": False,
    }
    write_json(phase_root / "governance" / "gate-register.json", gates)
    write_json(
        phase_root / "governance" / "retained-negative-register.json", negatives
    )
    write_json(phase_root / "governance" / "phase-truth.json", truth)

    checklist = {
        "schema": f"{SCHEMA}.complete-incomplete-checklist.v2",
        "owner": owner,
        "phase": phase,
        "completed": [
            "x1 immutable, pushed, and four-way equal before x2",
            "twenty inherited selections retained at zero credit",
            "twenty new proposals frozen",
            "portfolio counts complete",
            "family-current builder and toolkit hardened",
            "four bounded pillar artifacts represented",
            "ten phase-local skills and ten runner contracts built",
            "owner packet and long successor baton generated",
        ],
        "incomplete_until_terminal": [
            "immutable evidence and exact final committed and pushed",
            "one canonical aggregate succeeds",
            "fresh four-way equality passes",
            f"{args.next_owner} exact-title send is acknowledged",
        ],
        "required_work_complete_for_packet_build": True,
        "terminal_complete": False,
        "verdict": profile["verdict"],
    }
    write_json(
        phase_root / "closeout" / "complete-incomplete-checklist.json", checklist
    )

    baton = profile_baton_text(
        owner,
        args.next_owner,
        phase,
        args.next_phase,
        source,
        args.x1,
        profile,
        proposals["new_proposals"],
        ledgers,
        methods,
    )
    baton_rel = profile["baton_relative_path"].replace("\\", "/").strip("/")
    expected_baton_rel = (
        phase_root
        / "handoffs"
        / f"{slugify(args.next_owner)}-{args.next_phase}-activation.md"
    ).relative_to(repo).as_posix()
    if baton_rel != expected_baton_rel:
        raise DeltaError("builder profile baton path mismatch")
    baton_path = repo / Path(baton_rel)
    write_text(baton_path, baton)
    baton_raw = baton_path.read_bytes()
    baton_metadata = {
        "schema": f"{SCHEMA}.baton-metadata.v2",
        "sender": owner,
        "recipient": args.next_owner,
        "phase": args.next_phase,
        "repository_relative_path": baton_rel,
        "bytes": len(baton_raw),
        "words": words(baton),
        "sha256": sha256_bytes(baton_raw),
        "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
        "private_task_identifier_present": False,
    }
    metadata_rel = profile["baton_metadata_relative_path"].replace(
        "\\", "/"
    ).strip("/")
    expected_metadata_rel = expected_baton_rel.removesuffix(".md") + "-metadata.json"
    if metadata_rel != expected_metadata_rel:
        raise DeltaError("builder profile baton metadata path mismatch")
    write_json(repo / Path(metadata_rel), baton_metadata)
    closeout = f"""# {owner} {phase} closeout candidate

The x1 freeze is immutable at `{args.x1}` and predates every x2 artifact. The
source is `{source}`. The phase contains exactly 20 inherited zero-credit
selections, 20 new core proposals, and outcomes of
{outcome_counts.get('completed', 0)} completed,
{outcome_counts.get('represented', 0)} represented,
{outcome_counts.get('open_gap', 0)} open gap, and
{outcome_counts.get('exact_gate', 0)} exact gate. The generated successor baton
contains {baton_metadata['words']} words and has SHA-256
`{baton_metadata['sha256']}`.

This document is a candidate until immutable evidence, exact final, one
successful canonical aggregate, clean fresh-live equality, and the one
{args.next_owner} acknowledgement exist. The verdict remains
`NOT_READY_FOR_STAGE_20`.
"""
    write_text(phase_root / "closeout" / "phase-closeout-candidate.md", closeout)
    validation_contract = {
        "schema": f"{SCHEMA}.canonical-contract.v2",
        "owner": owner,
        "source": source,
        "x1": args.x1,
        "branch": profile["branch"],
        "expected_current_owner": owner,
        "expected_next_owner": args.next_owner,
        "test_modules": profile["test_modules"],
        "test_dependencies": profile["test_dependencies"],
        "sparse_patterns": sparse_receipt["patterns"],
        "baton": baton_metadata,
        "phase_local_skill_artifacts": skill_paths,
        "phase_local_runner_contracts": runner_paths,
        "receipt_must_be_external_and_exclusive": True,
        "successful_invocation_limit": 1,
        "post_success_replay": False,
    }
    write_json(
        phase_root / "validation" / "canonical-contract.json",
        validation_contract,
    )
    x1_after = {path.name: sha256_bytes(path.read_bytes()) for path in x1_files}
    if x1_after != x1_before:
        raise DeltaError("builder modified immutable x1 content")

    builder_receipt_rel = (
        phase_root / "x2" / "builder-receipt.json"
    ).relative_to(repo).as_posix()
    packet_files = sorted(
        path.relative_to(repo).as_posix()
        for path in phase_root.rglob("*")
        if path.is_file()
        and "/x1/" not in f"/{path.relative_to(repo).as_posix()}/"
        and path.relative_to(repo).as_posix() != builder_receipt_rel
    )
    packet_files_with_receipt = sorted([*packet_files, builder_receipt_rel])
    receipt = {
        "schema": f"{SCHEMA}.builder-receipt.v2",
        "built_at_utc": utc_now(),
        "owner": owner,
        "phase": phase,
        "source": source,
        "x1": args.x1,
        "generated_file_count": len(packet_files_with_receipt),
        "generated_files": packet_files_with_receipt,
        "portfolio_counts": actual,
        "skill_artifact_count": len(skill_paths),
        "runner_contract_count": len(runner_paths),
        "baton_words": baton_metadata["words"],
        "baton_sha256": baton_metadata["sha256"],
        "x1_unchanged": True,
        "valid": True,
    }
    write_json(phase_root / "x2" / "builder-receipt.json", receipt)
    sys.stdout.write(
        json.dumps(
            {
                "valid": True,
                "generated": receipt["generated_file_count"],
                "baton_words": baton_metadata["words"],
                "method_count": methods["method_count"],
            }
        )
        + "\n"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, required=True)
    parser.add_argument("--phase-root", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--next-owner", required=True)
    parser.add_argument("--next-phase", default="v662-v5")
    parser.add_argument("--source", required=False)
    parser.add_argument("--x1", required=False)
    args = parser.parse_args()
    try:
        repo = args.repo.resolve()
        phase_root = confined_phase_root(repo, args.phase_root, args.owner, args.phase)
        x1_root = phase_root / "x1"
        charter = load_json(x1_root / "phase-charter.json")
        proposals = load_json(x1_root / "proposal-freeze.json")
        portfolio = load_json(x1_root / "portfolio-freeze.json")
        startup_methods = load_json(x1_root / "startup-method-flow.json")
        sparse_receipt = load_json(x1_root / "sparse-lane-receipt.json")
        if charter.get("owner") != args.owner or charter.get("phase") != args.phase:
            raise DeltaError("x1 charter owner or phase mismatch")
        profile_path = x1_root / "builder-profile.json"
        if profile_path.is_file():
            profile = load_json(profile_path)
            return build_profile_packet(
                args,
                repo,
                phase_root,
                charter,
                proposals,
                portfolio,
                startup_methods,
                sparse_receipt,
                profile,
            )
        source = args.source or charter.get("source", {}).get("exact_head")
        if source != charter.get("source", {}).get("exact_head"):
            raise DeltaError("source differs from immutable x1 charter")
        if not args.x1 or not re.fullmatch(r"[0-9a-f]{40}", args.x1):
            raise DeltaError("exact x1 commit is required")
        if proposals.get("new_frozen_total") != 3590:
            raise DeltaError("proposal chain is not the frozen 3590-row Vesper chain")
        expected = portfolio["expected_counts"]
        ledgers = build_ledgers(portfolio)
        actual = {
            "safe_now": ledgers["safe-now-ledger"]["record_count"],
            "candidate": ledgers["candidate-ledger"]["record_count"],
            "approval_gate": ledgers["approval-gate-ledger"]["record_count"],
            "skill": ledgers["skill-ledger"]["record_count"],
            "runner": ledgers["runner-ledger"]["record_count"],
            "clean_fix_refine": ledgers["clean-fix-refine-ledger"]["record_count"],
        }
        if actual != expected:
            raise DeltaError(f"portfolio count mismatch: {actual} != {expected}")

        for name, ledger in ledgers.items():
            write_json(phase_root / "portfolio" / f"{name}.json", ledger)

        core_records = [
            {
                "proposal_id": proposal["proposal_id"],
                "title": proposal["title"],
                "outcome": proposal["expected_disposition"],
                "evidence_boundary": proposal["acceptance_or_falsifier"],
            }
            for proposal in proposals["new_proposals"]
        ]
        outcome_counts = Counter(record["outcome"] for record in core_records)
        outcome = {
            "schema": f"{SCHEMA}.outcome-ledger.v1",
            "owner": args.owner,
            "phase": args.phase,
            "record_count": len(core_records),
            "outcome_counts": dict(sorted(outcome_counts.items())),
            "records": core_records,
            "verdict": "NOT_READY_FOR_STAGE_20",
        }
        if outcome["outcome_counts"] != {"completed": 14, "exact_gate": 1, "open_gap": 1, "represented": 4}:
            raise DeltaError("core outcome distribution differs from x1")
        methods = method_flow(startup_methods)
        sources = source_ledger()
        write_json(phase_root / "x2" / "outcome-ledger.json", outcome)
        write_json(phase_root / "x2" / "method-flow.json", methods)
        write_json(phase_root / "x2" / "source-ledger.json", sources)

        environment = {
            "schema": f"{SCHEMA}.environment.v1",
            "owner": args.owner,
            "phase": args.phase,
            "versions": {
                "codex_cli": command_version(["codex.cmd", "--version"]),
                "python": command_version([sys.executable, "--version"]),
                "git": command_version(["git", "--version"]),
                "powershell": command_version(["pwsh", "--version"]),
            },
            "versions_verified_only": True,
            "desktop_updated": False,
            "elevation": False,
            "host_security_weakened": False,
            "windows_feature_changed": False,
            "unrelated_software_installed": False,
            "rebooted": False,
        }
        write_json(phase_root / "x2" / "environment-version-receipt.json", environment)

        tools = {
            "schema": f"{SCHEMA}.tool-catalogue.v1",
            "owner": args.owner,
            "phase": args.phase,
            "execution_authority": "owner_self_scoped_delta",
            "repository_scan": False,
            "unchanged_history_scan": False,
            "cross_lane_scan": False,
            "sibling_lane_mutation": False,
            "current_commands": [
                "manifest", "json", "markdown", "python", "privacy", "security",
                "path-audit", "route", "skill-hashes", "file-budget", "sparse",
                "baton-integrity", "canonical-digest", "data-quality", "canonical",
            ],
            "rollback": "Revert only Vesper's additive module change in a later reviewed commit; preserve every failed witness.",
            "protected_gates": ["no repository-wide scan", "no sibling mutation", "no independent-reproduction claim"],
        }
        write_json(phase_root / "x2" / "tool-catalogue.json", tools)

        write_text(
            phase_root / "pillars" / "gmut-provenance-functional.md",
            pillar_text(
                "GMUT provenance-functional representation",
                "A typed symbolic record associates each candidate model term with source, unit, domain, approximation, calibration status, and a falsifier. The representation is bookkeeping for hypotheses. It evaluates no likelihood, posterior, force, or observation and therefore supplies no empirical GMUT result.",
            ),
        )
        write_text(
            phase_root / "pillars" / "thos-digital-preservation-handover.md",
            pillar_text(
                "THOS digital-preservation handover proxy",
                "Synthetic states cover fixity generation, custody receipt, mismatch quarantine, second-person readback, escalation, workload limit, and shift handover. All identifiers and events are fictional fixtures. No real collection, worker, institution, incident, or effectiveness estimate is present.",
            ),
        )
        write_text(
            phase_root / "pillars" / "freed-id-content-integrity-profile.md",
            pillar_text(
                "Freed ID synthetic content-integrity profile",
                "A synthetic verification order separates issuer intent, holder disclosure, verifier policy, credential status, related-resource digests, recovery, and context binding. It uses no real key or proof and establishes no interoperability, privacy review, security review, or trust governance.",
            ),
        )
        write_text(
            phase_root / "pillars" / "cbr-public-records-authority-matrix.md",
            pillar_text(
                "CBR public-records authority-reservation matrix",
                "The matrix reserves access, retention, disclosure, privacy, remedy, affected-party, legal, cultural, data-governance, tangata whenua, iwi, hapu, and Maori-authority decisions to competent external authorities. Repository software makes zero real decision.",
            ),
        )

        overview = overview_text(outcome, methods)
        write_text(phase_root / "overview" / "integrated-overview.md", overview)
        write_text(phase_root / "report" / "accessible-static-report.html", static_report(overview))
        write_text(
            phase_root / "wellbeing" / "wellbeing-check.md",
            """# Vesper Arlen v662-v4 wellbeing check

The phase remains solo, bounded, and corrigible. No claim of subjective
experience, consciousness, or identity continuity is made. The practical
workflow check is healthy: source and scope are explicit, the D-first lane is
sparse, no sibling is being watched or mutated, failures are retained rather
than hidden, and stop conditions remain active. Hamish may pause, redirect,
rename, or stop the route at any time. The terminal verdict remains
`NOT_READY_FOR_STAGE_20`.
""",
        )
        write_text(
            phase_root / "governance" / "threat-model.md",
            """# Vesper v662-v4 exact-delta threat model

## Assets

Exact Git ancestry, owner attribution, x1 separation, changed-file manifests,
validation receipts, retained failures, privacy boundaries, and successor-route
truth.

## Threats and controls

- Duplicate JSON keys: strict ordered-pair parsing refuses ambiguity.
- Unicode or case-fold path collisions: the exact path audit fails closed.
- Bidi or control-character deception: explicit controls are rejected.
- Symlink, gitlink, or type confusion: only regular blob modes are accepted.
- Manifest tampering: per-file Git blob hashes, SHA-256, canonical commitment,
  and a deterministic Merkle root bind the delta.
- Stale baton substitution: relative path, committed blob, digest, and word
  range must all match.
- Scope creep: only exact-delta files and literal test dependencies execute.
- Validation laundering: one canonical success is permitted and never replayed.
- Route substitution: explicit current and next owners plus exact-title reread
  and acknowledgement are required.

## Residual risk

This is not exhaustive security, production assurance, complete privacy,
independent reproduction, legal review, cultural ratification, or Maori
authority. Residual risks remain exact-gated.
""",
        )

        gates = {
            "schema": f"{SCHEMA}.gate-register.v1",
            "inherited_open_gaps": 152,
            "new_core_open_gaps": 1,
            "effective_open_gaps": 153,
            "inherited_exact_gates": 150,
            "new_core_exact_gates": 1,
            "effective_exact_gates": 151,
            "portfolio_exact_and_blocked_rows": 15,
            "portfolio_rows_change_core_gate_count": False,
            "open_gap": "Independent real corpus and independent external audit remain absent.",
            "exact_gate": "Public-records remedy, legal, cultural, affected-party, data-governance, and Maori-authority decisions remain external.",
            "verdict": "NOT_READY_FOR_STAGE_20",
        }
        negatives = {
            "schema": f"{SCHEMA}.retained-negative-register.v1",
            "inherited_effective_negatives": 23084,
            "startup_operational_negatives": 9,
            "x2_operational_negatives": 6,
            "executed_rejected_synthetic_mutations": 14,
            "provisional_effective_negatives": 23113,
            "additional_x2_or_terminal_operational_negatives": 0,
            "failed_witnesses_erased": 0,
            "note": "Final effective count must add every later operational failure before seal.",
        }
        truth = {
            "schema": f"{SCHEMA}.phase-truth.v1",
            "owner": args.owner,
            "phase": args.phase,
            "source": source,
            "x1": args.x1,
            "frozen_proposals": 3590,
            "outcomes": outcome["outcome_counts"],
            "provisional_effective_negatives": 23113,
            "provisional_effective_methods": 7707,
            "open_gaps": 153,
            "exact_gates": 151,
            "verdict": "NOT_READY_FOR_STAGE_20",
            "same_owner_is_independent_reproduction": False,
        }
        write_json(phase_root / "governance" / "gate-register.json", gates)
        write_json(phase_root / "governance" / "retained-negative-register.json", negatives)
        write_json(phase_root / "governance" / "phase-truth.json", truth)

        checklist = {
            "schema": f"{SCHEMA}.complete-incomplete-checklist.v1",
            "owner": args.owner,
            "phase": args.phase,
            "completed": [
                "x1 immutable and pushed before x2",
                "twenty inherited selections retained at zero credit",
                "twenty new proposals frozen",
                "portfolio counts complete",
                "family-current toolkit hardened",
                "pillar artifacts represented within boundaries",
                "owner packet and long baton generated",
            ],
            "incomplete_until_terminal": [
                "global roster and authorization transitioned and validated",
                "immutable evidence and exact final committed and pushed",
                "one canonical aggregate succeeds",
                "fresh four-way equality passes",
                "Lyren Moss exact-title send is acknowledged",
            ],
            "required_work_complete_for_packet_build": True,
            "terminal_complete": False,
            "verdict": "NOT_READY_FOR_STAGE_20",
        }
        write_json(phase_root / "closeout" / "complete-incomplete-checklist.json", checklist)

        baton = baton_text(
            args.owner,
            args.next_owner,
            args.phase,
            args.next_phase,
            source,
            args.x1,
            proposals["new_proposals"],
            ledgers,
            methods,
        )
        baton_path = phase_root / "handoffs" / "lyren-moss-v662-v5-activation.md"
        write_text(baton_path, baton)
        baton_raw = baton_path.read_bytes()
        baton_metadata = {
            "schema": f"{SCHEMA}.baton-metadata.v1",
            "sender": args.owner,
            "recipient": args.next_owner,
            "phase": args.next_phase,
            "repository_relative_path": baton_path.relative_to(repo).as_posix(),
            "bytes": len(baton_raw),
            "words": words(baton),
            "sha256": sha256_bytes(baton_raw),
            "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "private_task_identifier_present": False,
        }
        write_json(phase_root / "handoffs" / "lyren-moss-v662-v5-activation-metadata.json", baton_metadata)

        closeout = f"""# Vesper Arlen v662-v4 closeout candidate

The x1 freeze is immutable at `{args.x1}` and predates every x2 artifact. The
source is `{source}`. The phase contains exactly 20 inherited zero-credit
selections, 20 new core proposals, and outcomes of 14 completed, 4 represented,
1 open gap, and 1 exact gate. The generated Lyren baton contains
{baton_metadata['words']} words and has SHA-256 `{baton_metadata['sha256']}`.

This document is a candidate until immutable evidence, exact final, one
successful canonical aggregate, clean fresh-live equality, and the one Lyren
acknowledgement exist. The verdict remains `NOT_READY_FOR_STAGE_20`.
"""
        write_text(phase_root / "closeout" / "phase-closeout-candidate.md", closeout)
        validation_contract = {
            "schema": f"{SCHEMA}.canonical-contract.v1",
            "owner": args.owner,
            "source": source,
            "x1": args.x1,
            "branch": "codex/GHC-Family/vesper-arlen-v662-v4-full-tools",
            "expected_current_owner": args.owner,
            "expected_next_owner": args.next_owner,
            "test_modules": ["tests/test_ghc_family_owner_delta_toolkit.py"],
            "test_dependencies": ["scripts/ghc_family_owner_delta_toolkit.py", "scripts/ghc_family_owner_delta_phase_builder.py"],
            "sparse_patterns": sparse_receipt.get("patterns", []),
            "baton": baton_metadata,
            "receipt_must_be_external_and_exclusive": True,
            "successful_invocation_limit": 1,
            "post_success_replay": False,
        }
        write_json(phase_root / "validation" / "canonical-contract.json", validation_contract)

        builder_receipt_rel = (phase_root / "x2" / "builder-receipt.json").relative_to(repo).as_posix()
        generated = sorted(
            path.relative_to(repo).as_posix()
            for path in phase_root.rglob("*")
            if (
                path.is_file()
                and "/x1/" not in f"/{path.relative_to(repo).as_posix()}/"
                and path.relative_to(repo).as_posix() != builder_receipt_rel
            )
        )
        generated_with_receipt = sorted([*generated, builder_receipt_rel])
        receipt = {
            "schema": f"{SCHEMA}.builder-receipt.v1",
            "built_at_utc": utc_now(),
            "owner": args.owner,
            "phase": args.phase,
            "source": source,
            "x1": args.x1,
            "generated_file_count": len(generated_with_receipt),
            "generated_files": generated_with_receipt,
            "portfolio_counts": actual,
            "baton_words": baton_metadata["words"],
            "baton_sha256": baton_metadata["sha256"],
            "valid": True,
        }
        write_json(phase_root / "x2" / "builder-receipt.json", receipt)
        sys.stdout.write(json.dumps({"valid": True, "generated": receipt["generated_file_count"], "baton_words": baton_metadata["words"]}) + "\n")
        return 0
    except (DeltaError, OSError, KeyError, TypeError, ValueError) as exc:
        sys.stderr.write(f"OWNER_DELTA_PHASE_BUILDER_ERROR: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
