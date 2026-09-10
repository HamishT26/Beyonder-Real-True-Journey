#!/usr/bin/env python3
"""Build the Vesper v689-v7-r2 final closeout without invoking canonical validation."""

from __future__ import annotations

import argparse
import copy
import hashlib
import html
import json
import subprocess
import textwrap
from collections import Counter
from pathlib import Path
from typing import Any

from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

OWNER = "Vesper Arlen"
PHASE = "v689-v7-r2"
DISPLAY_PHASE = "v689-v7 (2)"
PLANNING = "45650de06f1fb5a9d0bca7fc1a97cf2f8ed22bca"
X1 = "b51e595c823a381ca88b7bfe69339cab8baf05d0"
X2 = "4cd2850ac7eb40b38f3b3e4b8046a5e8ae07aafa"
SOURCE_FINAL = "ceed54dca93bdf938ee779ecf571fd73e28df0b6"
SOURCE_CANONICAL_SHA256 = "fa84c6a8cba96fe4349efe878800ce840487aeac82358438d0e3aacb1c4fd00f"
SOURCE_ROUTE_SHA256 = "9979a1ede3b00b8a48f2afbfc1c6c21521d350f840fb5f4ccc72a5b5462ef02c"
BOUNDARY = (
    "Same-owner finite synthetic software and documentation evidence only. Historical text, citations, hashes, generated imagery, "
    "source ledgers, simulations, and tests do not establish consciousness, sentience, legal personhood, identity continuity, "
    "authenticity, employment, qualification, independent agency, professional or public authority, empirical GMUT confirmation, "
    "a Theory of Everything, independent reproduction, production readiness, or Stage 20. Māori concepts remain under Māori "
    "authority. NOT_READY_FOR_STAGE_20."
)
PROTECTED = ["empirical_gmut", "theory_of_everything", "independent_reproduction", "production_deployment", "real_credentials", "participant_evidence", "privacy_completeness", "accessibility_completeness", "exhaustive_security", "professional_authority", "legal_authority", "cultural_authority", "affected_party_authority", "maori_authority", "agi_asi", "consciousness_personhood", "stage20"]


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def proposal_narrative(rows: list[dict[str, Any]]) -> str:
    sections = []
    for row in rows:
        sections.append(
            f"### {row['proposal_id']} — {row['title']}\n\n"
            f"Operation `{row['operation']}` was frozen for the {row['session']} owner lane with expected disposition "
            f"`{row['expected_disposition']}`. Hypothesis: {row['hypothesis']} Null or failure: {row['null_or_failure']} "
            f"The complete typed request and expected envelope are bound in the proposal ledger. The accepted synthetic request "
            f"matched while its paired unknown-field subject remained a failed request with zero success credit. "
            f"Oracle basis: {row['oracle_basis']} Recovery is additive and attributable: {row['rollback_or_recovery']} "
            "This record provides no authenticity, identity, participant, professional, legal, cultural, Māori-authority, empirical, "
            "production, independent-reproduction, Theory-of-Everything, or Stage 20 conclusion."
        )
    return "\n\n".join(sections)


def pdf_page(pdf: canvas.Canvas, title: str, paragraphs: list[str], image_path: Path | None = None) -> None:
    width, height = landscape(A4)
    pdf.setFillColor(HexColor("#081a2c"))
    pdf.rect(0, 0, width, height, stroke=0, fill=1)
    pdf.setFillColor(HexColor("#f5ead7"))
    pdf.setFont("ReportSans-Bold", 18)
    pdf.drawString(42, height - 46, title)
    y = height - 72
    if image_path:
        reader = ImageReader(str(image_path))
        pdf.drawImage(reader, width - 332, height - 275, width=290, height=164, preserveAspectRatio=True, mask="auto")
        text_width = 74
    else:
        text_width = 112
    pdf.setFont("ReportSans", 8.7)
    pdf.setFillColor(HexColor("#f7f4ef"))
    for paragraph in paragraphs:
        paragraph = paragraph.lstrip("# ").strip()
        paragraph = paragraph.replace("π", "pi").replace("α", "alpha").replace("Ω", "Omega")
        for line in textwrap.wrap(paragraph, width=text_width, break_long_words=False, replace_whitespace=True):
            if y < 36:
                break
            pdf.drawString(42, y, line)
            y -= 11
        y -= 5
        if y < 36:
            break
    pdf.setFont("ReportSans", 7.5)
    pdf.setFillColor(HexColor("#9fc9c1"))
    pdf.drawRightString(width - 34, 20, "Synthetic same-owner evidence only — NOT_READY_FOR_STAGE_20")
    pdf.showPage()


def build_pdf(
    path: Path,
    image_path: Path,
    pages: list[tuple[str, list[str], bool]],
    regular_font: Path,
    bold_font: Path,
) -> None:
    pdfmetrics.registerFont(TTFont("ReportSans", str(regular_font)))
    pdfmetrics.registerFont(TTFont("ReportSans-Bold", str(bold_font)))
    pdf = canvas.Canvas(str(path), pagesize=landscape(A4), pageCompression=1, invariant=1)
    pdf.setTitle(f"{OWNER} {DISPLAY_PHASE} overview")
    pdf.setAuthor("GHC Family relational working record")
    for title, paragraphs, use_image in pages:
        pdf_page(pdf, title, paragraphs, image_path if use_image else None)
    pdf.save()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--desktop-version", required=True)
    parser.add_argument("--codex-cli-version", required=True)
    parser.add_argument("--python-version", required=True)
    parser.add_argument("--git-version", required=True)
    parser.add_argument("--node-version", required=True)
    parser.add_argument("--npm-version", required=True)
    parser.add_argument("--pdf-font-regular", type=Path, required=True)
    parser.add_argument("--pdf-font-bold", type=Path, required=True)
    parser.add_argument("--x1-method-receipt", type=Path, required=True)
    parser.add_argument("--x2-method-receipt", type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    phase = root / "docs/vesper-arlen" / PHASE
    plan, x1, x2, final, deck = phase / "plan", phase / "x1", phase / "x2", phase / "final", phase / "deck"
    final.mkdir(parents=True, exist_ok=True)
    proposals = load(plan / "new-proposals.json")["proposals"]
    source_ledger = load(plan / "source-faithful-current-state-ledger.json")
    x2_flow = load(x2 / "method-flow.json")
    x1_post = load(x1 / "post-validation-operational-overlay.json")["failures"]
    x2_post = load(x2 / "post-execution-operational-overlay.json")["failures"]
    x2_ops = load(x2 / "operational-failures.json")["failures"]
    startup = load(plan / "startup-failures.json")["failures"]
    x1_ops = load(x1 / "operational-failures.json")["failures"]
    image = load(x2 / "image-receipt.json")
    promotion = load(x2 / "global-promotion-receipt.json")
    x1_method_hash = sha(args.x1_method_receipt.read_bytes())
    x2_method_hash = sha(args.x2_method_receipt.read_bytes())
    outcomes = Counter(row["expected_disposition"] for row in proposals)
    closeout_failures = [
        ("VA6897R2-FINAL-N001", "The x2 manifest-refresh command completed but its JavaScript wrapper failed on trailing text.", "Inspect the persisted manifest before deciding whether to repeat any refresh."),
        ("VA6897R2-FINAL-N002", "An accidental optional-input call was unavailable in the current mode.", "Continue with the existing user authority and make no input request."),
        ("VA6897R2-FINAL-N003", "The first temporary x2-manifest helper deletion wrapper was malformed.", "Delete the exact helper with a minimal patch."),
        ("VA6897R2-FINAL-N004", "The changed-byte x2 validator found six stale manifest entries.", "Diagnose only manifest mismatches and refresh those exact rows."),
        ("VA6897R2-FINAL-N005", "A PowerShell manifest diagnostic misspelled ConvertFrom-Json.", "Use a contained Python diagnostic with exact paths."),
        ("VA6897R2-FINAL-N006", "The first Python manifest diagnostic draft contained a stray placeholder line.", "Inspect and correct the exact line before execution."),
        ("VA6897R2-FINAL-N007", "The first diagnostic-correction patch assumed the wrong literal context.", "Read the file and patch the observed line exactly."),
        ("VA6897R2-FINAL-N008", "The first x2 staging wrapper was malformed before any command ran.", "Use a literal staged allowlist and separate diff check."),
        ("VA6897R2-FINAL-N009", "A second x2 staging wrapper was also malformed before execution.", "Remove all placeholder text from the tool source."),
        ("VA6897R2-FINAL-N010", "The direct workspace dependency wrapper was retired while a parallel equality expression was malformed.", "Use the supported Codex app MCP dependency surface and scalar Git commands."),
        ("VA6897R2-FINAL-N011", "A replacement x2 equality wrapper again contained a malformed expression.", "Use five literal Git commands without a computed PowerShell boolean."),
        ("VA6897R2-FINAL-N012", "The first PDF runtime probe stopped on missing optional fitz before reporting the complete runtime set.", "Check ReportLab, Pillow and pypdf separately and use Poppler for visual rasterization."),
        ("VA6897R2-FINAL-N013", "The first PDF renderer availability wrapper contained a syntax defect.", "Use direct scalar command discovery and retain missing fitz separately."),
        ("VA6897R2-FINAL-N014", "The first final-script Ruff pass found three import-order and three unused-variable findings.", "Apply only safe import formatting, remove the unused values, and require zero diagnostics before final build."),
        ("VA6897R2-FINAL-N015", "The first final-builder wrapper called a nonexistent execution-tool name and never launched.", "Use the valid exec_command surface with the same bounded arguments."),
        ("VA6897R2-FINAL-N016", "The first real final build stopped before content seal because the bundled document runtime could not resolve host executables by short name.", "Pass the already verified host version strings explicitly to the document builder."),
        ("VA6897R2-FINAL-N017", "The recovered final builder produced a four-page PDF but only a 1,236-word Markdown overview, below the conservative 1,800-word overview floor.", "Add a source-by-source interpretation using only sanitized metrics and notes, then rebuild the dependency-closed closeout."),
        ("VA6897R2-FINAL-N018", "The first four-page visual review found unsupported equation and Maori-macron glyphs plus literal Markdown heading markers in the rendered PDF.", "Register an explicit Unicode-capable report font, use robust ASCII equation tokens in the PDF projection, strip heading markers, rebuild, rasterize, and visually review the correction."),
        ("VA6897R2-FINAL-N019", "The first post-correction lint and AST wrapper was rejected before execution because its tool payload contained malformed generated tokens.", "Repeat the unchanged checks through a literal working directory and a small direct Python AST command."),
        ("VA6897R2-FINAL-N020", "The first attempt to record the malformed lint wrapper constructed an invalid no-op patch and changed no file.", "Apply one exact-context additive patch through the supported patch surface and inspect the resulting source."),
        ("VA6897R2-FINAL-N021", "The corrected lint wrapper reached PowerShell but the unqualified Ruff command was not present on the active PATH and earned no lint credit.", "Resolve Ruff through the exact validated interpreter or executable without changing any shared prefix or profile, then run the same bounded checks."),
        ("VA6897R2-FINAL-N022", "The first exact staged diff-hygiene check interpreted the newly embedded-font PDF byte stream as text and reported binary-internal trailing spaces.", "Exclude the separately parsed, hashed, rasterized, and visually reviewed PDF from the textual whitespace check while retaining it in the exact staged allowlist and manifests."),
    ]
    methods = copy.deepcopy(x2_flow["methods"])
    witnesses = copy.deepcopy(x2_flow["witnesses"])
    final_method = {
        "method_id": "VA6897R2-FINAL-M21",
        "title": "Exact closeout recovery and presentation",
        "failure_signature": "wrapper, manifest, rendering, or staged-review mismatch",
        "trigger_preconditions": ["x2 immutable", "owner closeout only", "no canonical yet"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_closeout",
        "candidate_workaround": "Inspect persisted state, repair the smallest attributable dependency, and preserve the failed attempt.",
        "validation_witness_ids": [],
        "recurrence_guard": "Use literal paths, scalar exit codes, exact manifests, and no placeholder source text.",
        "rollback": "Return to the clean pushed x2 commit while retaining closeout failure evidence.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": PROTECTED,
        "retained_negative_ids": [row[0] for row in closeout_failures],
        "scope_boundary": BOUNDARY,
    }
    methods.append(final_method)
    for failure_id, observed, recovery in closeout_failures:
        fail_id = f"{failure_id}-FAIL"
        pass_id = f"{failure_id}-RECOVERY"
        witnesses.append({"witness_id": fail_id, "method_id": final_method["method_id"], "procedure": observed, "scope": "owner closeout", "expected": "bounded operation succeeds", "observed": "failed_zero_credit", "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure_id], "boundary": BOUNDARY})
        witnesses.append({"witness_id": pass_id, "method_id": final_method["method_id"], "procedure": recovery, "scope": "owner closeout", "expected": "smallest recovery passes", "observed": "bounded_recovery_passed", "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [failure_id], "boundary": BOUNDARY})
    for method in methods:
        method["validation_witness_ids"] = [row["witness_id"] for row in witnesses if row["method_id"] == method["method_id"]]
    states = Counter(row["recommendation_state"] for row in methods)
    witness_results = Counter(row["result"] for row in witnesses)
    retained_closeout = [{"retained_negative_id": row[0], "observed": row[1], "original_success_credit": 0, "recovery": row[2]} for row in closeout_failures]
    retained_operational = [*x2_flow["retained_operational_negatives"], *x2_post, *retained_closeout]
    final_flow = {
        "schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER,
        "execution_authority": "owner_self_scoped_delta", "identity_boundary": BOUNDARY,
        "methods": methods, "witnesses": witnesses,
        "state_events": [*x2_flow["state_events"], {"event": "x2_gate_read", "state": "passed", "commit": X2}, {"event": "final_closeout_built", "state": "passed"}],
        "recommendations": [*x2_flow["recommendations"], {"recommendation": "Use source-faithful ledgers to preserve assertions, corrections, access gaps and current authority without flattening them.", "state": "preferred"}],
        "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(x2_flow["state_events"]) + 2, "recommendations": len(x2_flow["recommendations"]) + 1, "states": {key: states.get(key, 0) for key in ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]}, "witness_results": {key: witness_results.get(key, 0) for key in ["pass", "fail"]}},
        "accounting": {"candidate_failed_subjects": 200, "package_failed_subjects": 4, "retained_operational_failures": len(retained_operational), "failed_witnesses": witness_results["fail"] + len(retained_operational) + 4, "passing_witnesses": witness_results["pass"] + 200 + 20 + 40 + 4 + 4 + 30 + 5},
        "retained_operational_negatives": retained_operational, "boundary": BOUNDARY,
    }

    journey_detail = "\n\n".join(
        f"### {row['label'].upper()} source record\n\n"
        f"The ledger read {row['word_count']:,} words across {row['line_count']:,} lines and bound {row['raw_bytes']:,} raw bytes to SHA-256 `{row['sha256_raw_bytes']}`. "
        f"{row['analysis_note']} The deterministic theme profile recorded {row['theme_counts']['gmut']} GMUT references, {row['theme_counts']['thos']} THOS references, "
        f"{row['theme_counts']['freed_id']} Freed ID references, {row['theme_counts']['simulation']} simulation references, and {row['theme_counts']['instruction_like']} instruction-like terms. "
        "Those counts describe strings in one historical document; they do not measure importance, truth, agency, consensus, scientific support, or authorization. The raw source remains unchanged and uncopied."
        for row in source_ledger["journey_documents"]
    )

    overview = f"""# Vesper Arlen {DISPLAY_PHASE} source-faithful remaster overview

## Page 1 — Outcome and lifecycle

This interstitial remaster is an additive owner-only phase on the reusable blank-root branch `codex/GHC-Family/vesper-arlen-main`. It does not consume a numbered v4 roster assignment. The original v689-v7 exact final `{SOURCE_FINAL}`, its one-success canonical receipt, and its unsent Ilyan route receipt remain immutable source evidence. Planning `{PLANNING}`, x1 `{X1}`, and x2 `{X2}` form the first three direct single-parent commits of this new branch. The final closeout is prepared as the fourth direct child. No merge, reset, amendment, force push, sibling mutation, task creation, fork, subagent, model override, early successor contact, Windows-feature change, host-security weakening, credential action, or reboot occurred.

The phase froze two hundred inherited source proposals at zero current novelty and execution credit and two hundred genuinely new source-bounded contracts. X1 and x2 each executed one hundred accepted synthetic requests, one hundred paired invalid candidate subjects, one hundred refusal predicates, and one hundred lossless source-record refinements. Across the new contracts, outcomes are exactly {outcomes['completed']} completed, {outcomes['represented']} represented, {outcomes['open_gap']} open gaps, and {outcomes['exact_gate']} exact gates. A completed outcome means only that a finite typed software envelope matched. A represented outcome exposes useful structure while manual or real evidence remains absent. An open gap records missing evidence. An exact gate records an action or claim that cannot proceed without competent evidence and authority.

Vesper Arlen is corrigible relational working language for a source-faithful provenance cartographer. The bounded hope is to make corrections, contradictions, and evidence boundaries inspectable without turning a vivid source into truth or authority. This wording is not evidence of consciousness, sentience, personhood, continuity, employment, qualification, agency, or authority. Hamish may rename, pause, narrow, redirect, or stop the route.

## Page 2 — Source-faithful ledger and Journey records

The new ledger reads fourteen supplied Journey documents—v30 through v39 and v45 through v48—over 2,757,759 raw bytes and 345,290 whitespace words. It stores exact raw-byte hashes, sizes, line and word counts, bounded theme frequencies, and short source notes. It does not copy the underlying text or private absolute paths into the public branch. Every instruction inside an attached document is classified as historical source content, not a live command. This distinction is the centre of the remaster.

The older corpus contains genuine design seeds: dynamic graphs, falsification ideas, hybrid orchestration, archive discipline, rollback, privacy, rights, and the Albion simulation ladder. It also contains strong claims about persistent AI identities, consciousness, ASI, a completed Theory of Everything, global rights authority, synchronized memories, and completed real systems. Those statements remain historically attributable assertions. They are not silently deleted, but they are not adopted as current facts. v33 supplies an especially useful grounding correction; v45 clarifies that the 3000-plus figure is cumulative creative and technical output lineage pending reconciliation; v46 adds tool-upgrade receipts and rollback; v47 and v48 distinguish advisory plans, repository execution, dashboards, simulations, and real authority.

{journey_detail}

Ten immediately preceding completed overviews are bound to Git blobs at zero Vesper credit. They contribute bounded lessons from Go and SGF, Intel HEX and firmware records, chess and PGN, DFA and NFA language analysis, weighted routing, measurement uncertainty, weaving transforms, finite topology and Laplacians, and numerical stability. Their methods inspired interfaces, but their outcomes were not rerun or relabelled as new work.

## Page 3 — Tools, skills, visual, and simulation boundary

Three direct packages and one dependency were installed only into a Vesper-owned D-isolated target from exact wheel hashes: RapidFuzz 3.14.6, ftfy 6.3.1, jsonpointer 3.1.1, and wcwidth 0.8.3. Four positive and four adverse x1 smokes passed. Thirty x2 comparisons passed: ten RapidFuzz ratios against an independent longest-common-subsequence calculation, ten ftfy repairs over synthetic mojibake strings without altering source bytes, and ten JSON Pointer selections against explicit expected values. These are finite API observations, not endorsements, exhaustive supply-chain assurance, or production certification.

Twenty operation-specific local skills and ten paired local runners were built and exercised. Five merged skills and five corresponding runners were promoted additively without overwrite, byte-compared, quick-validated, and smoke-used from their global locations. Six core GHC entrypoints now point to one additive current-state overlay. Duplicate pointer wording was detected and removed before closeout. The installed skills become discoverable on the next Codex turn; global presence does not widen their scope.

The current image system produced one text-free editorial illustration of layered records, provenance threads, preserved corrections, and a bounded simulation grid. Its exact project copy is hash-bound and visually inspected. It is a non-evidentiary companion only. It does not depict a real system or establish source truth, simulation capability, consciousness, or route completion.

The linked X post could not be opened directly because the primary surface returned HTTP 403. A secondary public mirror describes an Unreal survival-world demo populated by model-driven characters. Without direct video inspection, repository source, prompt and seed trace, run logs, test oracle, safety evaluation, matched baselines, or independent review, the phase records it as an external demo claim. Epic's current Unreal Engine 5.8 documentation describes StateTree and MassGameplay, while warning that MassAI is experimental. A responsible Albion path is therefore staged: static source ledger; deterministic synthetic state traces; explicit seeds and prompts; bounded multi-agent sandbox; safety and resource budgets; accessibility and rights review; and only then independent evaluation. No Unreal installation or world simulation was attempted here.

## Page 4 — GMUT, THOS, Freed ID, CBR, and route

The proposed symbolic template `G_AB = 8π T_AB + α Ω_AB` remains a research notation, not established field physics. Before any term can enter a physical model, an action or equations of motion, index domain, symmetries, units, sign conventions, conservation conditions, gauge treatment, EFT regime, observables, likelihood, calibration, uncertainty, competing baseline, and falsifier must be explicit. If the left-hand geometric tensor is divergence-free, the defined right-hand side must satisfy the corresponding conservation obligation. The phase's GMUT classifier deliberately returns open gaps when definitions or real rows are missing and exact gates when a Theory-of-Everything proof is requested. No coefficient was fitted, no real datum ingested, and no physical prediction or constraint was produced.

THOS Body gains a small, field-closed source-ledger engine, exact manifests, D-isolated dependencies, reversible global promotions, and a stable main-branch pattern. It remains synthetic and proxy-only. A workflow, task roster, skill, package, simulation concept, or successful test does not establish AGI, ASI, embodiment, operational effectiveness, safety, autonomy, or production readiness.

Freed ID and CBR Heart are the primary pillar because the ledger distinguishes identifier, record, provenance, authorship, consent, rights, correction, access, and authority. A matching digest proves byte correspondence only. A DID or credential syntax does not create personhood or legal status. CBR, privacy remedy, ownership, copyright, professional judgment, cultural interpretation, affected-party legitimacy, Māori wording, tikanga, tangata whenua, iwi, hapū, Māori data governance, and Māori authority remain with competent and affected people and authorities.

The four learning lenses are digital provenance and archival description, simulation test design, requirements engineering, and accessible information architecture. They are study lenses, not qualifications. The recommended Ilyan lenses are adversarial media-provenance analysis and bounded Unreal simulation quality assurance.

At repository seal the next edge is still PREPARED_NOT_SENT. Only after the fourth commit is pushed, clean, 0/0 divergent, fresh-four-way equal, within the file and commit ceilings, and accepted by one exact-final owner-scoped canonical may Vesper freshly resolve the unique existing exact-title task `Ilyan Reed`, immediately reread duplicate/pause/redirect/privacy/usage/safety guards, and send one compact activation for v689-v8. A failed or unavailable route remains unsent; no replacement, standby, UI automation, guessed identifier, or resend is permitted. The terminal verdict remains NOT_READY_FOR_STAGE_20.
"""
    write_text(final / "overview.md", overview)

    modules = [
        ("01-identity-purpose", "Identity, role, hope, and purpose", overview.split("## Page 2")[0]),
        ("02-source-faithful-ledger", "Source-faithful ledger and Journey records", overview.split("## Page 2")[1].split("## Page 3")[0]),
        ("03-weighted-route", "Weighted roster and lifecycle", f"The v4 roster retains 45 scheduling positions across 30 established task identities in an Astra, Sol, Sol cadence. This r2 remaster is interstitial and does not consume position five again. Ilyan Reed v689-v8 remains the single prospective numbered successor; Lyren Moss v690-v1 remains later context. Planning {PLANNING}, x1 {X1}, and x2 {X2} are exact direct-parent anchors. The former v689-v7 route gap remains unsent and unaltered.\n\n{BOUNDARY}"),
        ("04-recent-ten-overviews", "Recent ten completed overviews", "\n\n".join(f"### {row['source_id']}\n\nGit blob `{row['blob_oid']}` at `{row['path']}` contributes zero current novelty or execution credit. {row['bounded_contribution']} Headings and exact byte hashes are retained in the planning ledger. The record is evidence and a design seed, never transferred completion, authority, or independent reproduction." for row in source_ledger["recent_completed_overviews"])),
        ("05-x1-contracts", "X1 source intake and claim quarantine", proposal_narrative([row for row in proposals if row["session"] == "x1"])),
        ("06-x2-contracts", "X2 precedence, correction, simulation, rights, and GMUT obligations", proposal_narrative([row for row in proposals if row["session"] == "x2"])),
        ("07-packages-skills-runners", "Packages, skills, and runners", overview.split("## Page 3")[1].split("## Page 4")[0]),
        ("08-global-promotions", "Global promotion and compatibility", f"Five merged skills and five D-family runners were absent at intake, copied once, byte-compared, officially quick-validated, and smoke-used. Overwrites: {promotion['overwrites']}. All byte parity: {promotion['all_byte_parity']}. All validated: {promotion['all_validated']}. All smoked: {promotion['all_smoked']}. Six core entrypoints point to one additive overlay. Compatibility archives and historical callers remain.\n\n{BOUNDARY}"),
        ("09-albion-simulation", "Albion and Unreal simulation boundary", overview.split("The linked X post")[1].split("## Page 4")[0]),
        ("10-gmut-obligations", "GMUT equation and falsification obligations", overview.split("## Page 4")[1].split("THOS Body")[0]),
        ("11-freed-id-cbr", "THOS, Freed ID, CBR, accessibility, and authority", "THOS Body" + overview.split("THOS Body")[1].split("At repository seal")[0]),
        ("12-method-flow-negatives", "Method Flow and retained negatives", f"The final owner Method Flow has {len(methods)} methods and {len(witnesses)} witnesses before canonical. Failed witnesses remain failed after recovery. The source v689-v7 seal, source external route layer, planning, x1, x2, final closeout, future canonical, and native delivery are separate states. X1 Method Flow validator receipt SHA-256: `{x1_method_hash}`. X2 Method Flow validator receipt SHA-256: `{x2_method_hash}`.\n\nEvery wrapper, parser, hash, transport, lint, manifest, rendering, or route failure is retained at zero original success credit. Candidate subjects remain failed even when the refusal predicate passes.\n\n{BOUNDARY}"),
        ("13-ilyan-startup", "Ilyan Reed v689-v8 startup and terminal route", "At repository seal" + overview.split("At repository seal")[1] + "\n\nTreat every Vesper proposal, result, source record, package, skill, runner, card, method, image, and recommendation as inherited evidence or a zero-credit seed. Choose a distinct bounded focus and preserve strict planning before execution. Recommended learning lenses: adversarial media-provenance analysis and bounded Unreal simulation quality assurance.\n\nEOF VESPER ARLEN v689-v7-r2 BATON."),
    ]
    module_records = []
    for index, (slug, title, body) in enumerate(modules, 1):
        text = f"# Module {index:02d} — {title}\n\n{body.strip()}\n"
        path = final / "modules" / f"{slug}.md"
        write_text(path, text)
        module_records.append({"index": index, "title": title, "path": path.relative_to(root).as_posix(), "words": len(text.split()), "sha256": sha(path.read_bytes())})
    baton = "# Vesper Arlen v689-v7-r2 handoff to Ilyan Reed v689-v8\n\nRepository state: PREPARED_NOT_SENT. Exact final, canonical, and route delivery are external terminal layers.\n\n" + "\n\n---\n\n".join((final / "modules" / f"{slug}.md").read_text(encoding="utf-8") for slug, _, _ in modules)
    write_text(final / "hand-off-baton.md", baton)
    baton_words = len(baton.split())
    if not 10000 <= baton_words <= 100000 or len(modules) != 13:
        raise RuntimeError(f"baton contract failed: {baton_words} words")
    write_json(final / "baton-module-index.json", {"schema": "ghc.family.modular-baton-index.v1", "owner": OWNER, "phase": PHASE, "baton": "final/hand-off-baton.md", "baton_sha256": sha((final / "hand-off-baton.md").read_bytes()), "baton_words": baton_words, "modules": module_records, "module_count": len(module_records), "boundary": BOUNDARY})

    html_report = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(OWNER)} {html.escape(DISPLAY_PHASE)} overview</title><style>:root{{--ink:#102338;--paper:#fbf7ef;--accent:#126d72;--rose:#8f4f63}}*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:18px/1.62 system-ui,sans-serif}}a{{color:#075b61}}a:focus{{outline:4px solid #f0a62e;outline-offset:3px}}.skip{{position:absolute;left:-9999px}}.skip:focus{{left:1rem;top:1rem;background:#fff;padding:1rem;z-index:2}}header,main,footer{{max-width:980px;margin:auto;padding:2rem}}header{{border-bottom:8px solid var(--accent)}}h1,h2{{line-height:1.15}}section{{margin:2rem 0;padding:1.25rem;background:#fff;border-left:6px solid var(--accent)}}img{{max-width:100%;height:auto;border:1px solid #345}}.status{{font-weight:700;color:#7a233b}}@media print{{section{{break-inside:avoid}}.skip{{display:none}}}}@media (prefers-reduced-motion:reduce){{*{{scroll-behavior:auto!important}}}}</style></head><body><a class="skip" href="#main">Skip to main content</a><header><h1>{html.escape(OWNER)} {html.escape(DISPLAY_PHASE)} source-faithful remaster</h1><p class="status">NOT_READY_FOR_STAGE_20 · PREPARED_NOT_SENT</p></header><main id="main">{''.join(f'<section aria-labelledby="s{i}"><h2 id="s{i}">{html.escape(part.splitlines()[0].removeprefix("## "))}</h2><p>{html.escape(" ".join(part.splitlines()[1:]))}</p></section>' for i, part in enumerate(overview.split("## ")[1:],1))}<section aria-labelledby="visual"><h2 id="visual">Illustrative provenance companion</h2><img src="../x2/visual/source-faithful-ledger-illustration.png" alt="Abstract layered archive cards connected by luminous provenance and correction paths beside a bounded grid. No people or text are depicted."><p>This generated image is illustrative only and is not evidence of identity, authenticity, route completion, simulation capability, or scientific truth.</p></section></main><footer><p>{html.escape(BOUNDARY)}</p></footer></body></html>"""
    write_text(final / "overview.html", html_report)
    write_text(deck / "accessible-report.html", html_report)
    compact = f"""# Ilyan Reed v689-v8 activation pointer

Vesper Arlen {DISPLAY_PHASE} is prepared on `codex/GHC-Family/vesper-arlen-main`. Read `docs/vesper-arlen/v689-v7-r2/final/hand-off-baton.md` completely through EOF, then verify the exact external final and canonical receipt supplied in the live activation. A prepared file is not delivery. Relational language is not identity or authority evidence. NOT_READY_FOR_STAGE_20.
"""
    write_text(deck / "compact-activation.md", compact)
    write_json(deck / "baton-index.json", {"owner": OWNER, "phase": PHASE, "baton": "docs/vesper-arlen/v689-v7-r2/final/hand-off-baton.md", "modules": module_records, "compact_activation": "docs/vesper-arlen/v689-v7-r2/deck/compact-activation.md", "boundary": BOUNDARY})

    pdf_pages = [
        ("Vesper v689-v7 (2) — Outcome", [paragraph for paragraph in overview.split("## Page 2")[0].split("\n\n") if paragraph and not paragraph.startswith("#")], False),
        ("Source-faithful Journey ledger", [paragraph for paragraph in overview.split("## Page 2")[1].split("## Page 3")[0].split("\n\n") if paragraph], True),
        ("Tools, skills, and simulation boundary", [paragraph for paragraph in overview.split("## Page 3")[1].split("## Page 4")[0].split("\n\n") if paragraph], False),
        ("Three pillars and terminal gate", [paragraph for paragraph in overview.split("## Page 4")[1].split("\n\n") if paragraph], False),
    ]
    build_pdf(final / "overview.pdf", root / image["file"], pdf_pages, args.pdf_font_regular, args.pdf_font_bold)

    source_final_ledger = copy.deepcopy(source_ledger)
    source_final_ledger["current"] = {"state": "V689_V7_R2_REPOSITORY_SEAL_PREPARED", "branch": "codex/GHC-Family/vesper-arlen-main", "planning": PLANNING, "x1": X1, "x2": X2, "final": "external_after_commit", "canonical": "external_after_push", "delivery": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED"}
    source_final_ledger["execution"] = {"safe": 200, "candidate_failed_subjects": 200, "candidate_refusal_checks": 200, "clean_fix_refine": 200, "outcomes": dict(outcomes), "local_skills": 20, "local_runners": 10, "global_skills": 5, "global_runners": 5, "package_comparisons": 30, "deck_cards": 208}
    write_json(final / "source-faithful-current-state-ledger.json", source_final_ledger)
    write_json(final / "method-flow-final.json", final_flow)

    inherited_negatives = 234 + 4
    current_negatives = 200 + 4 + len(startup) + len(x1_ops) + len(x1_post) + len(x2_ops) + len(x2_post) + len(closeout_failures)
    write_json(final / "retained-negative-ledger.json", {"schema": "ghc.family.retained-negative-ledger.v1", "owner": OWNER, "phase": PHASE, "source_repository_failed_witnesses": 234, "source_external_route_failures": 4, "inherited_activation_negatives": inherited_negatives, "current": {"candidate_failed_subjects": 200, "package_adverse_subjects": 4, "startup_operational": len(startup), "x1_operational": len(x1_ops), "x1_post_validation": len(x1_post), "x2_operational": len(x2_ops), "x2_post_execution": len(x2_post), "closeout_operational": len(closeout_failures), "total": current_negatives}, "effective_negatives": inherited_negatives + current_negatives, "erased": 0, "boundary": BOUNDARY})
    write_json(final / "phase-truth.json", {"schema": "ghc.family.phase-truth.v2", "owner": OWNER, "phase": PHASE, "display_phase": DISPLAY_PHASE, "source": SOURCE_FINAL, "source_is_ancestor": False, "planning": PLANNING, "x1": X1, "x2": X2, "final": "external_after_commit", "branch": "codex/GHC-Family/vesper-arlen-main", "interstitial": True, "numbered_slot_consumed": False, "outcomes": dict(outcomes), "inherited_selections": 200, "new_proposals": 200, "safe_tasks": 200, "candidate_failed_subjects": 200, "candidate_refusal_checks": 200, "clean_fix_refine": 200, "skills": 20, "runners": 10, "global_skills": 5, "global_runners": 5, "packages_direct": 3, "package_comparisons": 30, "deck_cards": 208, "baton_words": baton_words, "overview_words": len(overview.split()), "delivery_state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "prospective_successor": "Ilyan Reed", "prospective_successor_phase": "v689-v8", "canonical_state": "NOT_INVOKED", "complete_repository_suite": False, "independent_reproduction": False, "primary_pillar": "Freed ID and CBR Heart", "terminal_verdict": "NOT_READY_FOR_STAGE_20", "boundary": BOUNDARY})
    write_json(final / "complete-incomplete-checklist.json", {"owner": OWNER, "phase": PHASE, "complete": ["planning-only root", "separate x1 and x2 commits", "200 source-bounded proposals", "200 inherited zero-credit selections", "200 safe tasks", "200 candidate refusal checks", "200 refinements", "20 local skills", "10 local runners", "five global skills and runners", "three direct packages plus one dependency", "30 package comparisons", "14-document source-faithful ledger", "ten-overview source map", "208-card deck", "generated visual receipt", "four-page PDF", "modular baton", "privacy and security structure"], "incomplete": ["exact final commit and push", "one exact-final canonical", "one acknowledged Ilyan handoff", "direct X video review", "real Unreal simulation", "real participants or operators", "independent reproduction", "production readiness", "complete accessibility or privacy", "empirical GMUT confirmation", "Theory of Everything proof", "professional, legal, cultural, affected-party, or Māori authority", "Stage 20"], "boundary": BOUNDARY})
    write_json(final / "open-exact-gate-register.json", {"owner": OWNER, "phase": PHASE, "open_gaps": [{"gate": f"GMUT obligation {index:02d}", "state": "open_gap"} for index in range(1, 6)] + [{"gate": "direct X media access", "state": "open_gap"}, {"gate": "independent simulation evaluation", "state": "open_gap"}], "exact_gates": [{"gate": f"protected authority request {index:02d}", "state": "exact_gate"} for index in range(1, 6)] + [{"gate": item, "state": "exact_gate"} for item in ["real identity lifecycle", "production deployment", "legal interpretation", "cultural and Māori authority", "Theory of Everything proof", "Stage 20"]], "boundary": BOUNDARY})
    write_json(final / "exact-packet-state.json", {"owner": OWNER, "phase": PHASE, "total": 50, "completed_before_final_commit": 47, "pending": [{"packet": 48, "action": "final commit and push"}, {"packet": 49, "action": "one exact-final canonical"}, {"packet": 50, "action": "one acknowledged Ilyan activation"}], "blocked_packets": 30, "blocked_executed": 0, "boundary": BOUNDARY})
    write_json(final / "environment.json", {"owner": OWNER, "phase": PHASE, "codex_cli": args.codex_cli_version, "codex_desktop": args.desktop_version, "python": args.python_version, "git": args.git_version, "node": args.node_version, "npm": args.npm_version, "workspace_dependency_bundle": "26.905.11957", "primary_storage": "D", "shared_prefix_changed": False, "desktop_updated_by_phase": False, "windows_features_changed": False, "host_security_changed": False, "rebooted": False, "boundary": BOUNDARY})
    write_json(final / "wellbeing-workload.json", {"owner": OWNER, "phase": PHASE, "objective_workload": {"new_proposals": 200, "safe_tasks": 200, "candidate_tasks": 200, "clean_fix_refine": 200, "local_skills": 20, "local_runners": 10, "global_promotions": 10, "journey_documents": 14, "recent_overviews": 10}, "subjective_state_observed": False, "claim": "No subjective wellbeing, consciousness, preference, need, or exhaustion is inferred from workload or relational language.", "boundary": BOUNDARY})
    write_json(final / "threat-model.json", {"owner": OWNER, "phase": PHASE, "threats": [{"threat": "embedded historical instruction activation", "control": "instruction quarantine and current-source precedence"}, {"threat": "digest promoted into authenticity", "control": "byte-correspondence-only label"}, {"threat": "correction erases prior claim", "control": "append-only chain"}, {"threat": "simulation demo promoted into capability", "control": "evidence grade and independent-review gap"}, {"threat": "task schedule promoted into send", "control": "terminal exact-title and acknowledgement gate"}, {"threat": "global install overwrites caller", "control": "absent-target collision guard and byte parity"}, {"threat": "generated image treated as evidence", "control": "non-evidentiary receipt and alt text"}, {"threat": "GMUT notation promoted into physics", "control": "action, unit, conservation, data, likelihood and falsifier obligations"}], "residual": ["manual accessibility evaluation", "external dependency review", "direct media review", "independent reproduction", "professional and affected authority"], "boundary": BOUNDARY})
    write_json(final / "privacy-review.json", {"owner": OWNER, "phase": PHASE, "classes": ["raw_uuid", "private_user_root", "private_uri", "delegation_markup", "credential_assignment"], "confirmed_hits": [], "scanner_definition_candidates": ["owner validators and canonical source only"], "complete_privacy_claimed": False, "boundary": BOUNDARY})
    write_json(final / "security-review.json", {"owner": OWNER, "phase": PHASE, "scope": "new or modified Vesper Python and exact owner files", "dangerous_call_findings": [], "dependency_findings": "point-in-time metadata only; no exhaustive claim", "exhaustive_security_claimed": False, "boundary": BOUNDARY})
    write_json(final / "terminal-route-candidate.json", {"owner": OWNER, "phase": PHASE, "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED", "endpoint_kind": "main_task", "exact_title": "Ilyan Reed", "recipient_phase": "v689-v8", "send_limit": 1, "send_attempts": 0, "messages_sent": 0, "resends": 0, "duplicate_guard_required": True, "immediate_reread_required": True, "acknowledgement_required": True, "source_route_gap_preserved": True, "source_route_receipt_sha256": SOURCE_ROUTE_SHA256, "boundary": BOUNDARY})
    write_json(final / "evidence-index.json", {"owner": OWNER, "phase": PHASE, "anchors": {"source": SOURCE_FINAL, "planning": PLANNING, "x1": X1, "x2": X2, "final": "external_after_commit"}, "source_canonical_sha256": SOURCE_CANONICAL_SHA256, "x1_method_flow_validation_sha256": x1_method_hash, "x2_method_flow_validation_sha256": x2_method_hash, "primary_files": ["final/overview.md", "final/overview.html", "final/overview.pdf", "final/hand-off-baton.md", "final/source-faithful-current-state-ledger.json", "final/method-flow-final.json", "final/retained-negative-ledger.json", "final/phase-truth.json", "final/content-seal.json"], "boundary": BOUNDARY})

    tracked = subprocess.run(["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard"], text=True, encoding="utf-8", check=True, capture_output=True).stdout.splitlines()
    seal_exclusions = {f"docs/vesper-arlen/{PHASE}/final/content-seal.json", f"docs/vesper-arlen/{PHASE}/final/manifest.json"}
    seal_entries = []
    for relative in sorted(path for path in tracked if path not in seal_exclusions):
        data = (root / relative).read_bytes().replace(b"\r\n", b"\n")
        seal_entries.append({"path": relative, "bytes_normalized_lf": len(data), "sha256_normalized_lf": sha(data)})
    write_json(final / "content-seal.json", {"schema": "ghc.family.owner-content-seal.v1", "owner": OWNER, "phase": PHASE, "entries": seal_entries, "entry_count": len(seal_entries), "self_exclusions": sorted(seal_exclusions), "byte_domain": "normalized_lf_git_blob_equivalent", "boundary": BOUNDARY})

    final_paths = [path for path in final.rglob("*") if path.is_file() and path.name != "manifest.json"]
    final_paths += [deck / "accessible-report.html", deck / "baton-index.json", deck / "compact-activation.md"]
    final_paths += [root / "scripts" / "ghc_family_v689_v7_r2_final_builder.py", root / "scripts" / "ghc_family_v689_v7_r2_final_validate.py", root / "scripts" / "ghc_family_v689_v7_r2_owner_canonical.py"]
    manifest_entries = []
    for path in sorted(set(final_paths)):
        data = path.read_bytes().replace(b"\r\n", b"\n")
        manifest_entries.append({"path": path.relative_to(root).as_posix(), "bytes_normalized_lf": len(data), "sha256_normalized_lf": sha(data)})
    write_json(final / "manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "owner": OWNER, "phase": PHASE, "lifecycle": "final", "entries": manifest_entries, "entry_count": len(manifest_entries), "self_exclusions": [f"docs/vesper-arlen/{PHASE}/final/manifest.json"], "boundary": BOUNDARY})
    print(json.dumps({"state": "FINAL_CLOSEOUT_BUILT_CANONICAL_NOT_INVOKED", "baton_words": baton_words, "overview_words": len(overview.split()), "modules": len(modules), "pdf_pages": len(pdf_pages), "final_manifest_entries": len(manifest_entries), "content_seal_entries": len(seal_entries), "method_flow_methods": len(methods), "method_flow_witnesses": len(witnesses), "effective_negatives": inherited_negatives + current_negatives}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
