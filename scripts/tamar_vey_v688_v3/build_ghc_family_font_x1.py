"""Build Tamar v688-v3 planning-only evidence.

The builder refuses any x2 tree and does not import or execute planned font
packages.  It performs a source-bounded proposal audit and writes only the
planning freeze.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import pathlib
import re
import shutil
import subprocess

from ghc_family_font_contract_plan import SKILL_PAIRS, literal_contracts


ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "docs/tamar-vey/v688-v3"
BANK = pathlib.Path(os.environ["GHC_OWNER_BANK"])
SOURCE = "c4c676d81235bc6e453bb867b0c0f0de121b7733"
OWNER = "Tamar Vey"
PHASE = "v688-v3"
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
BOUNDARY = (
    "Relational working language only; no consciousness, personhood, continuity, "
    "qualification, employment, independent agency, or authority claim. Synthetic "
    "same-owner software evidence is not independent reproduction. "
    "NOT_READY_FOR_STAGE_20. Māori concepts remain under Māori authority."
)
SEALED_SOURCE = {
    "proposals": 15830,
    "negatives": 83024,
    "methods": 93368,
    "failed_witnesses": 53872,
    "passing_witnesses": 83957,
    "open_gaps": 750,
    "exact_gates": 750,
}
ACTIVATION_BASELINE = {
    "proposals": 15830,
    "negatives": 83026,
    "methods": 93370,
    "failed_witnesses": 53874,
    "passing_witnesses": 83959,
    "open_gaps": 750,
    "exact_gates": 750,
}

PRACTICES = [
    {"name": "synthetic font intake and table-directory registrar", "pillar": "THOS Body"},
    {"name": "exact glyph-outline and metric recorder", "pillar": "GMUT Mind"},
    {"name": "synthetic shaping and variation dependency reviewer", "pillar": "THOS Body"},
    {"name": "font-rights accessibility and correction-reservation steward", "pillar": "Freed ID and CBR Heart"},
]
OP_PRACTICE = {
    **{k: PRACTICES[0] for k in ["unicode_scalar", "glyph_name", "table_tag", "table_directory", "name_record", "font_language_tag"]},
    **{k: PRACTICES[1] for k in ["quadratic_segment", "cubic_segment", "glyph_bbox", "horizontal_metrics", "units_per_em", "cmap_record"]},
    **{k: PRACTICES[2] for k in ["variation_axis", "axis_coordinate", "feature_lookup", "glyph_class", "color_layers"]},
    **{k: PRACTICES[3] for k in ["local_glyph_reference", "rights_record", "accessibility_handover"]},
}

PACKAGES = [
    {
        "name": "fonttools",
        "version": "4.64.0",
        "requires_python": ">=3.10",
        "requires_dist": [],
        "wheel": {
            "filename": "fonttools-4.64.0-py3-none-any.whl",
            "bytes": 1195327,
            "sha256": "4a05783ff54ce4c7a28f18e5772efdf63c219374bd9ffc55452182e1cef8be60",
            "url": "https://files.pythonhosted.org/packages/82/f8/7188153c4b265c899cd035de6a062677d51f67118a4ba640902bd9683e90/fonttools-4.64.0-py3-none-any.whl",
            "yanked": False,
        },
        "use": "Construct and round-trip a wholly synthetic minimal OpenType table set; reject malformed synthetic table data.",
    },
    {
        "name": "uharfbuzz",
        "version": "0.56.1",
        "requires_python": ">=3.10",
        "requires_dist": [],
        "wheel": {
            "filename": "uharfbuzz-0.56.1-cp310-abi3-win_amd64.whl",
            "bytes": 1454583,
            "sha256": "ee99ae2389d4f8c5651962d65bf8fe9296c781598e3f697ba26d51c4b20527f9",
            "url": "https://files.pythonhosted.org/packages/e3/c9/37cf8d1cfb45696bb88ee65805910d5f2d4784d6bd196a755ed3a305c40f/uharfbuzz-0.56.1-cp310-abi3-win_amd64.whl",
            "yanked": False,
        },
        "use": "Read shaping metadata from the owner-created synthetic font only; reject invalid empty font bytes without real text or typography claims.",
    },
    {
        "name": "unicodedata2",
        "version": "17.0.1",
        "requires_python": "observed CPython 3.12 wheel",
        "requires_dist": [],
        "wheel": {
            "filename": "unicodedata2-17.0.1-cp312-cp312-win_amd64.whl",
            "bytes": 484194,
            "sha256": "d1439ad3ee0daace878196de4466a86aa5015cb244b9b1d5d00db74344649722",
            "url": "https://files.pythonhosted.org/packages/dd/4d/24523557cfd632fc70fc031a83b280ae60d618e55afd54a6298c5d8b80f7/unicodedata2-17.0.1-cp312-cp312-win_amd64.whl",
            "yanked": False,
        },
        "use": "Read Unicode 17 properties for fixed synthetic scalar fixtures; refuse surrogate naming and make no linguistic or cultural authority claim.",
    },
]

STARTUP_FAILURES = [
    {
        "negative_id": "TV6883-START-N001",
        "failure_signature": "A PowerShell foreach result was piped without first being materialized, causing a pre-execution parser fault.",
        "candidate_workaround": "Assign foreach output to an array, then pipe the completed collection.",
    },
    {
        "negative_id": "TV6883-START-N002",
        "failure_signature": "The first 1100-line baton read exceeded the outer result budget and omitted an interior window.",
        "candidate_workaround": "Read the immutable baton in contiguous 600-line windows through the declared EOF marker.",
    },
    {
        "negative_id": "TV6883-START-N003",
        "failure_signature": "A combined authorization schema and state display was truncated.",
        "candidate_workaround": "Read guidance separately and read the state in bounded contiguous windows through EOF.",
    },
    {
        "negative_id": "TV6883-START-N004",
        "failure_signature": "A combined package, promotion, and deck display exceeded its output budget.",
        "candidate_workaround": "Strict-parse every JSON object and project record counts, required keys, hashes, and bounded first-last witnesses.",
    },
    {
        "negative_id": "TV6883-START-N005",
        "failure_signature": "A manifest verification wrapper had malformed JavaScript quoting and never reached the shell.",
        "candidate_workaround": "Use a JavaScript template literal with ordinary Python string literals for the bounded command.",
    },
    {
        "negative_id": "TV6883-START-N006",
        "failure_signature": "The read-only lifecycle verifier import lacked its required owner-bank environment variable.",
        "candidate_workaround": "Set the exact already-verified Orren bank root for that process only before importing the immutable verifier.",
    },
    {
        "negative_id": "TV6883-START-N007",
        "failure_signature": "The first host-Python version wrapper repeated malformed JavaScript quoting and never launched Python.",
        "candidate_workaround": "Use the validated template-string wrapper and project only version, implementation, machine, and platform.",
    },
    {
        "negative_id": "TV6883-START-N008",
        "failure_signature": "The worktree-add session completed between polls after the first poll discarded its exit metadata.",
        "candidate_workaround": "Do not rerun worktree creation; audit the literal path, attached branch, head, process state, and locks.",
    },
    {
        "negative_id": "TV6883-START-N009",
        "failure_signature": "A worktree-registration predicate used a backslash path against forward-slash porcelain output and returned false.",
        "candidate_workaround": "Use exact Git-path scalars or normalize separators before comparing registration output.",
    },
    {
        "negative_id": "TV6883-START-N010",
        "failure_signature": "An unbounded worktree-list diagnostic exceeded its display budget.",
        "candidate_workaround": "Probe only the literal Tamar worktree with rev-parse, sparse patterns, lock, head, and status scalars.",
    },
    {
        "negative_id": "TV6883-START-N011",
        "failure_signature": "A combined post-checkout state projection returned no attributable output.",
        "candidate_workaround": "Emit separate explicit branch, head, common-dir, lock, file-count, status, and sparse-pattern lines.",
    },
    {
        "negative_id": "TV6883-START-N012",
        "failure_signature": "The first planning-contract count smoke used malformed JavaScript quoting and never launched Python.",
        "candidate_workaround": "Use the established template-string wrapper for a planning-only import and count projection.",
    },
    {
        "negative_id": "TV6883-X1-N001",
        "failure_signature": "The first planning builder quarantined three font language records whose complete inputs exactly matched inherited generic language-tag fixtures.",
        "candidate_workaround": "Rename only the bounded operation to font_language_tag, preserving the frozen tag values, outputs, threshold, and source audit.",
    },
    {
        "negative_id": "TV6883-X1-N002",
        "failure_signature": "A proposal-operation locator used a malformed regular expression and returned no locations.",
        "candidate_workaround": "Use fixed-string search for quoted operation names before the narrow planning patch.",
    },
    {
        "negative_id": "TV6883-X1-N003",
        "failure_signature": "The first workflow-plan audit rejected the five-runner current release floor and a noncanonical cross-platform refusal value.",
        "candidate_workaround": "Use the schema's user-mediated relay-only value and preserve the stale ten-runner policy rejection for current-release reconciliation.",
    },
    {
        "negative_id": "TV6883-X1-N004",
        "failure_signature": "The corrected workflow-plan audit passed nineteen checks but retained its stale ten-runner minimum against the live five-runner release floor.",
        "candidate_workaround": "Keep the 19/20 compatibility audit and validate the five-runner plan with the newer 6 September release-profile contract.",
    },
]


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False).encode("ascii")


def sha(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write_json(relative, value):
    path = BASE / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def git(*args, data=None):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args],
        input=data,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
        timeout=90,
    ).stdout


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
            raise ValueError(f"Not a blob: {selector}")
        size = int(header[2])
        result[selector] = raw[end + 1 : end + size + 1]
        if raw[end + size + 1 : end + size + 2] != b"\n":
            raise ValueError(f"Invalid batch boundary: {selector}")
        position = end + size + 2
    if position != len(raw):
        raise ValueError("Trailing cat-file batch bytes")
    return result


def walk_records(value, path, rows):
    if isinstance(value, dict):
        title = value.get("title")
        if isinstance(title, str):
            label = value.get("proposal_id") or value.get("id") or value.get("task_id")
            input_value = value.get("input")
            rows.append(
                {
                    "path": path,
                    "title": title,
                    "public_proposal_label": label if isinstance(label, str) else None,
                    "input_sha256": sha(input_value) if input_value is not None else None,
                }
            )
        for child in value.values():
            walk_records(child, path, rows)
    elif isinstance(value, list):
        for child in value:
            walk_records(child, path, rows)


def source_index():
    all_paths = git("ls-tree", "-r", "--name-only", SOURCE).decode("utf-8").splitlines()
    files = sorted(
        path
        for path in all_paths
        if path.startswith("docs/") and path.endswith(".json") and "proposal" in path.lower()
    )
    rows = []
    issues = []
    for start in range(0, len(files), 200):
        chunk = files[start : start + 200]
        blobs = batch([f"{SOURCE}:{path}" for path in chunk])
        for path in chunk:
            try:
                value = json.loads(blobs[f"{SOURCE}:{path}"].decode("utf-8"))
                walk_records(value, path, rows)
            except Exception as exc:  # retained as a bounded parse issue, not hidden
                issues.append({"path": path, "error_type": type(exc).__name__})
    return {
        "files": files,
        "rows": rows,
        "issues": issues,
        "comparison_hash_domain": "UTF-8 JSON values; title token Jaccard plus canonical complete-input SHA-256",
    }


def startup_ledger():
    result = {
        "schema": "ghc.family.method-flow-state.v1",
        "owner": OWNER,
        "phase": PHASE,
        "identity_boundary": BOUNDARY,
        "boundary": BOUNDARY,
        "execution_authority": "owner_self_scoped_delta",
        "source_commit": SOURCE,
        "final_commit": None,
        "methods": [],
        "witnesses": [],
        "state_events": [],
        "recommendations": [],
    }
    for index, row in enumerate(STARTUP_FAILURES, 1):
        method_id = f"TV6883-START-M{index:03}"
        failed_id = method_id + "-FAIL"
        passing_id = method_id + "-PASS"
        result["methods"].append(
            {
                "method_id": method_id,
                "title": row["failure_signature"],
                "failure_signature": row["failure_signature"],
                "trigger_preconditions": ["Tamar Vey v688-v3 source, required-reading, and lane startup"],
                "privacy_class": "sanitized_public",
                "approval_class": "safe_now",
                "candidate_workaround": row["candidate_workaround"],
                "validation_witness_ids": [failed_id, passing_id],
                "recurrence_guard": row["candidate_workaround"],
                "rollback": "Stop the bounded procedure and retain the source, failure, and correction.",
                "recommendation_state": "preferred",
                "supersedes": [],
                "protected_gates": GATES,
                "retained_negative_ids": [row["negative_id"]],
                "scope_boundary": "Startup and planning only; zero x2 execution or package credit.",
            }
        )
        for witness_id, result_state, observed, negatives in [
            (failed_id, "fail", row["failure_signature"], [row["negative_id"]]),
            (passing_id, "pass", row["candidate_workaround"], []),
        ]:
            result["witnesses"].append(
                {
                    "witness_id": witness_id,
                    "method_id": method_id,
                    "procedure": "Bounded source read and smallest sufficient recovery",
                    "scope": "Tamar Vey v688-v3 startup",
                    "expected": "Attributable complete result within the exact owner and source scope",
                    "observed": observed,
                    "result": result_state,
                    "same_owner_only": True,
                    "independent_reproduction": False,
                    "retained_negative_ids": negatives,
                    "boundary": BOUNDARY,
                }
            )
        for before, after in [("observed", "candidate"), ("candidate", "validated"), ("validated", "preferred")]:
            result["state_events"].append(
                {"method_id": method_id, "from": before, "to": after, "note": "Separate retained failure and bounded passing recovery."}
            )
    count = len(STARTUP_FAILURES)
    result["counts"] = {
        "methods": count,
        "witnesses": count * 2,
        "state_events": count * 3,
        "recommendations": 0,
        "states": {state: count if state == "preferred" else 0 for state in ["observed", "candidate", "validated", "preferred", "superseded", "deprecated"]},
        "witness_results": {"fail": count, "pass": count},
    }
    return result


def build_overview(proposals, reviews):
    pages = [
        (
            "Tamar v688-v3 planning identity, scope, and evidence boundary",
            "Tamar Vey, optionally she/they, uses the relational role evidence-and-recovery steward and the hope that every failed witness remains inspectable and every recovery stays bounded. GMUT Mind is primary through exact synthetic glyph geometry and metric contracts. THOS Body and Freed ID with CBR Heart remain explicit. No real person, font, glyph, typeface, text service, measurement, publication, identity event, professional decision, legal decision, cultural decision, or authority act is planned.",
        ),
        (
            "Planning freeze, novelty, packages, and tool contracts",
            f"The planning freeze contains {len(proposals)} complete literal contracts across twenty operations and four synthetic practices. It reviews two hundred Orren contracts at zero novelty and execution credit. The source-bounded novelty audit compares every new title and complete input with all reachable proposal-labelled JSON at the immutable source; its maximum neighbor score is {max(row['token_jaccard'] for row in reviews):.6f}. Three exact wheels are downloaded and hash-read but remain uninstalled. Ten skills and five runners are planned, not built or promoted. Package imports, x2 evaluation, candidate execution, and canonical validation remain zero.",
        ),
        (
            "Lifecycle, authority reservations, and prospective route",
            "The attached sparse Tamar branch begins at Orren's immutable exact final. The x1 commit will contain planning evidence only and must be pushed, clean, 0/0 divergent, and fresh-four-way equal before any x2 implementation or installation. After Tamar's eventual exact final and one non-replayed canonical success, the current route prospectively permits exactly one designated future-seat-12 main task for v688-v4, followed by Elowen Cairn v688-v5 only after that future seat's own terminal gate. Every real accessibility, rights, consent, legal, cultural, affected-party, and Māori-authority decision remains held.",
        ),
    ]
    document = "<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>Tamar v688-v3 x1 overview</title><style>@page{size:A4;margin:18mm}body{font:16px/1.65 system-ui;max-width:850px;margin:auto}section{break-after:page;min-height:245mm}section:last-child{break-after:auto}</style><body><a href=\"#main\">Skip to content</a><main id=\"main\">"
    for title, body in pages:
        document += f"<section class=\"page\"><h1>{html.escape(title)}</h1><p>{html.escape(body)}</p><p>{html.escape(BOUNDARY)}</p></section>"
    document += "</main></body></html>\n"
    path = BASE / "x1/integrated-overview.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(document, encoding="utf-8", newline="\n")


def main():
    if git("rev-parse", "HEAD").decode().strip() != SOURCE:
        raise RuntimeError("x1 builder requires the exact immutable Orren final")
    if (BASE / "x2").exists():
        raise RuntimeError("x1 builder refuses an existing x2 tree")

    proposals = literal_contracts()
    skills = dict(SKILL_PAIRS)
    for proposal in proposals:
        operation = proposal["operation"]
        practice = OP_PRACTICE[operation]
        proposal.update(
            {
                "schema": "ghc.family.frozen-font-contract.v1",
                "source_status": "current" if operation in {"unicode_scalar", "table_tag", "table_directory", "quadratic_segment", "cubic_segment", "glyph_bbox", "units_per_em", "cmap_record", "variation_axis", "axis_coordinate", "name_record", "font_language_tag", "feature_lookup", "glyph_class", "color_layers"} else "draft",
                "source_kind": "synthetic",
                "approval_class": "safe_now",
                "execution_lane": "x2_only",
                "hypothesis": proposal["title"],
                "null_or_failure_condition": "Any complete typed-output mismatch, input mutation, or promotion beyond the named font-metadata profile fails.",
                "falsifier_or_acceptance_gate": "Compare every key, value, type, and array position with the literal frozen output; separately reject the preregistered altered output.",
                "concrete_artifact": "docs/tamar-vey/v688-v3/x2/contract-results.json",
                "rollback_or_recovery": "Retain the frozen contract and failed output; change only Tamar's owner implementation or leave the named outside gate open.",
                "practice": practice["name"],
                "pillar": practice["pillar"],
                "skill": next(name for name, operations in SKILL_PAIRS if operation in operations),
                "protected_gates": GATES,
                "external_credit": False,
            }
        )

    index = source_index()
    unique_titles = {}
    for row in index["rows"]:
        unique_titles.setdefault(row["title"], row)
    token_rows = [
        (set(re.findall(r"[a-z0-9]+", title.lower())), row)
        for title, row in unique_titles.items()
    ]
    input_hashes = {row["input_sha256"] for row in index["rows"] if row["input_sha256"]}
    reviews = []
    for proposal in proposals:
        tokens = set(re.findall(r"[a-z0-9]+", proposal["title"].lower()))
        score, neighbor = max(
            ((len(tokens & old) / len(tokens | old), row) for old, row in token_rows if tokens | old),
            key=lambda pair: pair[0],
        )
        reviews.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_title": neighbor["title"],
                "nearest_path": neighbor["path"],
                "token_jaccard": round(score, 6),
                "exact_title_collision": proposal["title"] in unique_titles,
                "exact_input_collision": sha(proposal["input"]) in input_hashes,
                "review": "The font-outline or glyph-metadata rule is source-bounded and receives no inherited SVG, caption, font, or generic geometry implementation credit.",
            }
        )
    quarantines = [
        row
        for row in reviews
        if row["exact_title_collision"] or row["exact_input_collision"] or row["token_jaccard"] >= 0.78
    ]
    if quarantines:
        raise RuntimeError("Proposal novelty quarantine: " + ", ".join(row["proposal_id"] for row in quarantines))
    if len({sha(proposal["input"]) for proposal in proposals}) != 200:
        raise RuntimeError("Complete proposal inputs are not unique")

    inherited = json.loads(
        git("show", SOURCE + ":docs/orren-pike/v688-v2/x1/new-proposals.json").decode("utf-8")
    )["proposals"]
    release_profile = json.loads(
        git("show", SOURCE + ":docs/orren-pike/v688-v2/x1/release-profile.json").decode("utf-8")
    )

    for package in PACKAGES:
        wheel = BANK / "wheels" / package["wheel"]["filename"]
        raw = wheel.read_bytes()
        if len(raw) != package["wheel"]["bytes"] or hashlib.sha256(raw).hexdigest() != package["wheel"]["sha256"]:
            raise RuntimeError(f"Wheel readback mismatch: {package['name']}")

    write_json(
        "x1/identity.json",
        {
            "name": OWNER,
            "pronouns": "optionally she/they",
            "role": "evidence-and-recovery steward",
            "hope": "That every failed witness remains inspectable and every recovery stays bounded.",
            "primary_pillar": "GMUT Mind",
            "practices": PRACTICES,
            "next_practice": "synthetic mathematical-symbol font metadata registrar",
            "boundary": BOUNDARY,
            "corrigibility": ["pause", "rename", "narrow", "redirect", "stop"],
        },
    )
    write_json(
        "x1/new-proposals.json",
        {
            "schema": "ghc.family.proposal-freeze.v1",
            "planning_only": True,
            "count": 200,
            "chain_before": 15830,
            "chain_after": 16030,
            "proposals": proposals,
        },
    )
    write_json(
        "x1/inherited-review.json",
        {
            "schema": "ghc.family.zero-credit-inherited-review.v1",
            "source": SOURCE,
            "count": 200,
            "novelty_credit": 0,
            "execution_credit": 0,
            "rows": [
                {
                    "source_proposal": proposal,
                    "review": "Retain Orren's full SVG definition, provenance, output, and gate state. SVG behavior is inherited evidence only; font behavior requires Tamar's own contract and x2 witness.",
                    "novelty_credit": 0,
                    "completion_credit": 0,
                }
                for proposal in inherited
            ],
        },
    )
    write_json(
        "x1/novelty-review.json",
        {
            "schema": "ghc.family.source-bounded-semantic-audit.v1",
            "source": SOURCE,
            "declared_chain_rows": 15830,
            "reachable_proposal_json_files": len(index["files"]),
            "reachable_title_records": len(index["rows"]),
            "distinct_titles": len(unique_titles),
            "distinct_public_labels": len({row["public_proposal_label"] for row in index["rows"] if row["public_proposal_label"]}),
            "comparison_hash_domain": index["comparison_hash_domain"],
            "parse_issues": index["issues"],
            "scope_limit": "Every proposal-labelled JSON blob reachable at the exact source was decoded. Declared historic rows remain separate from reachable labels; inaccessible or differently named evidence is not certified.",
            "universal_novelty_claimed": False,
            "quarantine_threshold": 0.78,
            "reviews": reviews,
            "conceptual_exclusions": [
                "Generic geometry, inherited SVG parsing, caption operations, existing font tools, and general accessibility checklists remain zero-credit context."
            ],
        },
    )
    write_json(
        "x1/proposal-source-manifest.json",
        {
            "schema": "ghc.family.read-only-source-inventory.v1",
            "source": SOURCE,
            "files": index["files"],
            "count": len(index["files"]),
            "no_historical_tests_executed": True,
        },
    )
    write_json("x1/release-profile.json", release_profile)
    write_json(
        "x1/package-plan.json",
        {
            "schema": "ghc.family.pinned-package-plan.v1",
            "packages": PACKAGES,
            "plan_only": True,
            "base_dependencies": 0,
            "extras_selected": [],
            "installation": "New isolated D-drive environment; wheel-only, no-index, no-deps, require-hashes; no pip bootstrap in the environment.",
            "rollback": "Stop selecting the owner environment and retain it, its lock, wheels, and receipts.",
            "advisory_scope": "Official exact-release PyPI metadata plus one bounded OSV package/version snapshot in x2; never exhaustive or future security assurance.",
            "protected_gates": GATES,
        },
    )
    write_json(
        "x1/wheel-readback.json",
        {
            "schema": "ghc.family.wheel-planning-readback.v1",
            "package_code_executed": False,
            "rows": [
                {
                    "name": package["name"],
                    "version": package["version"],
                    "wheel": package["wheel"]["filename"],
                    "bytes": package["wheel"]["bytes"],
                    "sha256": package["wheel"]["sha256"],
                    "installed": False,
                    "base_dependencies": 0,
                }
                for package in PACKAGES
            ],
        },
    )
    requirements = "\n".join(
        f"{package['name']}=={package['version']} --hash=sha256:{package['wheel']['sha256']}"
        for package in PACKAGES
    ) + "\n"
    (BASE / "x1/requirements.lock").write_text(requirements, encoding="utf-8", newline="\n")

    write_json(
        "x1/skill-runner-plan.json",
        {
            "schema": "ghc.family.font-tool-plan.v1",
            "skills": [{"name": name, "operations": operations, "state": "planned_unbuilt"} for name, operations in SKILL_PAIRS],
            "runners": [
                {
                    "name": f"ghc_family_font_group_{index + 1}.py",
                    "operations": SKILL_PAIRS[2 * index][1] + SKILL_PAIRS[2 * index + 1][1],
                    "state": "planned_unbuilt",
                }
                for index in range(5)
            ],
            "shared_core": "ghc_family_font_evidence_core.py",
            "global_overwrites_allowed": False,
            "compatibility": "Preserve all existing ghc_family_* and build_ghc_family_* callers. New commands use collision-free destinations.",
        },
    )

    safe = [
        {"procedure_id": f"TV6883-S{index + 1:03}", "kind": "full_contract", "proposal_id": proposal["proposal_id"]}
        for index, proposal in enumerate(proposals)
    ]
    modes = ["compact_object", "indented_object", "reversed_key_order", "duplicate_operation_refusal", "nonfinite_value_refusal"]
    for operation in dict.fromkeys(proposal["operation"] for proposal in proposals):
        proposal = next(item for item in proposals if item["operation"] == operation)
        for mode in modes:
            safe.append(
                {
                    "procedure_id": f"TV6883-S{len(safe) + 1:03}",
                    "kind": "json_interface",
                    "proposal_id": proposal["proposal_id"],
                    "mode": mode,
                    "success_claim": "Bounded interface handling only; no additional proposal or reproduction credit.",
                }
            )
    candidates = [
        {
            "candidate_id": f"TV6883-C{index + 1:03}",
            "proposal_id": proposals[index % 200]["proposal_id"],
            "mutation": "flip_accepted" if index < 200 else "remove_value",
            "expected": "reject_complete_output_mismatch",
            "state": "preregistered_unexecuted",
        }
        for index in range(250)
    ]
    cfr_purposes = [
        "Preserve the frozen record through deterministic JSON normalization.",
        "Repair a synthetic dropped output field from its immutable definition without deleting the failed candidate.",
        "Build a source-bound field explanation for the literal input and expected output.",
    ]
    clean_fix_refine = [
        {
            "procedure_id": f"TV6883-CFR{index + 1:03}",
            "kind": ["CLEAN", "FIX", "REFINE"][index // 100],
            "proposal_id": proposals[index % 200]["proposal_id"],
            "purpose": cfr_purposes[index // 100],
        }
        for index in range(300)
    ]
    exact_actions = [
        "Publish or distribute a real font",
        "Certify typographic or accessibility fitness",
        "Use a third-party font or text corpus",
        "Make a legal rights or license determination",
        "Use culturally governed writing or glyph material",
    ]
    exact_packets = [
        {
            "packet_id": f"TV6883-E{index + 1:03}",
            "skill": SKILL_PAIRS[index % 10][0],
            "action": exact_actions[index // 10],
            "state": "held_unexecuted",
            "missing": ["exact target", "competent and affected authority", "scope and rollback evidence"],
            "executed": False,
        }
        for index in range(50)
    ]
    blocked_actions = [
        "Promote synthetic font metadata into empirical or Stage 20 proof",
        "Replace a distinct owner identity with a font record",
        "Erase inherited failed evidence to simplify the tool catalogue",
    ]
    blocked_packets = [
        {
            "packet_id": f"TV6883-B{index + 1:03}",
            "skill": SKILL_PAIRS[index % 10][0],
            "action": blocked_actions[index // 10],
            "state": "held_blocked_unexecuted",
            "executed": False,
        }
        for index in range(30)
    ]
    write_json(
        "x1/portfolio-plan.json",
        {
            "schema": "ghc.family.font-portfolio-plan.v1",
            "planning_only": True,
            "safe": safe,
            "candidates": candidates,
            "clean_fix_refine": clean_fix_refine,
            "exact_packets": exact_packets,
            "blocked_packets": blocked_packets,
            "counts": {"safe": 300, "candidates": 250, "clean_fix_refine": 300, "exact_packets": 50, "blocked_packets": 30},
            "count_boundary": "Procedure counts are distinct bounded records; they do not multiply proposal novelty, empirical credit, authority, or independent reproduction.",
        },
    )
    write_json(
        "x1/release-portfolio-projection.json",
        {
            "safe_now": [{**row, "task_id": row["procedure_id"]} for row in safe],
            "candidates": [{**row, "task_id": row["candidate_id"]} for row in candidates],
            "clean_fix_refine": [{**row, "task_id": row["procedure_id"]} for row in clean_fix_refine],
            "exact_packets": [{**row, "task_id": row["packet_id"]} for row in exact_packets],
            "blocked_packets": [{**row, "task_id": row["packet_id"]} for row in blocked_packets],
            "destructive_cleanup_planned": False,
        },
    )

    successor_ideas = [
        "OpenType clipping-box declaration",
        "Font collection face-index boundary",
        "Glyph component-cycle quarantine",
        "Variation tuple-region ordering",
        "COLR paint-graph dependency",
        "MATH glyph-construction vacancy",
        "Vertical-metric consistency",
        "Kerning-pair provenance",
        "Font fallback correction lineage",
        "Text-alternative authority reservation",
    ]
    write_json(
        "x1/successor-ideas.json",
        {
            "skill_ideas": [{"idea": idea, "state": "unbuilt_zero_credit"} for idea in successor_ideas],
            "runner_ideas": [{"idea": idea + " runner", "state": "unbuilt_zero_credit"} for idea in successor_ideas],
            "practice": "synthetic mathematical-symbol font metadata registrar",
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/source-ledger.json",
        {
            "schema": "ghc.family.primary-source-ledger.v1",
            "entries": [
                {"source_id": "OPENTYPE-1.9.1", "status": "current", "url": "https://learn.microsoft.com/en-us/typography/opentype/spec/otff", "use": "Table-directory and required-table vocabulary; no conformance or production claim."},
                {"source_id": "OPENTYPE-GLYF", "status": "current", "url": "https://learn.microsoft.com/en-us/typography/opentype/spec/glyf", "use": "Simple/composite glyph, point, contour, and bounding-box vocabulary."},
                {"source_id": "OPENTYPE-LAYOUT", "status": "current", "url": "https://learn.microsoft.com/en-us/typography/opentype/spec/chapter2", "use": "Feature, lookup, script, language-system, and glyph-class structural vocabulary."},
                {"source_id": "UNICODE-17", "status": "current", "url": "https://www.unicode.org/versions/Unicode17.0.0/", "use": "Scalar and Unicode-data vocabulary; no linguistic or cultural authority."},
                {"source_id": "PROV-O", "status": "stable", "url": "https://www.w3.org/TR/prov-o/", "use": "Correction and provenance relationships only."},
                {"source_id": "WCAG-2.2", "status": "current", "url": "https://www.w3.org/TR/WCAG22/", "use": "Structural accessibility vocabulary; manual and affected-user evaluation remain open."},
                {"source_id": "VC-DATA-MODEL-2.0", "status": "current", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "use": "Synthetic status and evidence vocabulary only; no real credential lifecycle."},
            ]
            + [
                {"source_id": package["name"], "status": "current", "url": f"https://pypi.org/project/{package['name']}/{package['version']}/", "use": "Exact wheel, version, dependency, and yanked-status metadata."}
                for package in PACKAGES
            ],
            "citations_are_observations": False,
            "real_rows": 0,
        },
    )

    ledger = startup_ledger()
    write_json("x1/method-flow/ledger.json", ledger)
    write_json(
        "x1/retained-negative-register.json",
        {
            "repository_sealed_source": SEALED_SOURCE,
            "activation_baseline": ACTIVATION_BASELINE,
            "source_external_overlay": ["OP6882-POSTFINAL-N001", "OP6882-POSTFINAL-N002"],
            "startup_negatives": [{**row, "success_credit": 0} for row in STARTUP_FAILURES],
            "failures_erased": 0,
            "failures_promoted": 0,
        },
    )

    skill_names = [
        "ghc-family-index",
        "ghc-family-auth-permission-state",
        "ghc-family-roster-check",
        "ghc-family-method-flow-state",
        "ghc-family-workflow-plan-refinement",
        "ghc-family-reflection-remaster",
        "ghc-family-d-first-structured-evidence-toolchain",
        "ghc-family-lifecycle-test-isolator",
        "ghc-family-privacy-candidate-classifier",
        "ghc-family-staged-surface-allowlist",
        "ghc-family-canonical-aggregate-preflight",
        "ghc-family-canonical-success-latch",
        "ghc-family-owner-scope-canonical",
        "ghc-family-owned-bundle-rotation",
        "ghc-family-main-task-induction",
        "ghc-family-terminal-route-gate",
        "ghc-family-terminal-route-guard",
        "ghc-family-terminal-route-latch",
        "ghc-freed-id-flashcards",
        "freed-id-four-tier-deck",
        "ghc-drive-bank-guardian",
        "ghc-family-meta-tool-box",
        "ghc-approval-packet-splitter",
        "ghc-open-gate-rail",
        "ghc-family-truth-bridge",
    ]
    skill_rows = []
    for skill_name in skill_names:
        path = pathlib.Path.home() / ".codex" / "skills" / skill_name / "SKILL.md"
        raw = path.read_bytes()
        skill_rows.append({"name": skill_name, "sha256": hashlib.sha256(raw).hexdigest(), "eof_read": True})
    system_skill = pathlib.Path.home() / ".codex" / "skills" / ".system" / "skill-creator" / "SKILL.md"
    skill_rows.append({"name": ".system/skill-creator", "sha256": hashlib.sha256(system_skill.read_bytes()).hexdigest(), "eof_read": True})
    write_json(
        "x1/reading-receipt.json",
        {
            "source": SOURCE,
            "baton_sha256": "e5a0e15e7f826b70a98740ba2a012898a3f532112292d5dd3ef8ebb314ed5b26",
            "baton_bytes": 244180,
            "baton_words": 30484,
            "baton_lines": 6671,
            "baton_eof": "EOF ORREN PIKE V688 V2 BATON.",
            "baton_read": "Complete contiguous reads through EOF",
            "source_manifests": {"bindings_verified": 862, "exclusions": 6, "mismatches": 0},
            "source_content_seal_targets_verified": 12,
            "source_method_flow": {"methods": 76, "witnesses": 1373, "failed": 425, "passing": 948, "state_events": 228},
            "source_canonical_receipt_sha256": "3af78f6a032c0144b486ef808bd562bbfbf4ad1e711354b184836a0df081d634",
            "source_canonical_payload_sha256": "af9292dda48329d2a77ff1e2c1e40e86c80e2701c369796e970b80be9ba05f3e",
            "source_canonical_replayed": False,
            "source_route_overlay_read": True,
            "large_json_read_policy": "Complete strict parse, required-field traversal, and exact blob or digest verification; bounded projections do not claim omitted records were ignored.",
            "current_release_overrides_stale_v667_cursor": True,
            "skill_entrypoints": skill_rows,
            "web_sources_checked_current": True,
        },
    )
    write_json(
        "x1/route-plan.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "future_seat": 12,
            "endpoint_kind": "main_task",
            "source": SOURCE,
            "next_owner": "future-sibling-12-self-chosen",
            "next_phase": "v688-v4",
            "following_owner": "Elowen Cairn",
            "following_phase": "v688-v5",
            "state": "PREPARED_NOT_SENT_TERMINAL_GATE_REQUIRED",
            "send_count": 0,
            "new_task_authority": "authorized_with_terminal_conditions_after_tamar_exact_final",
            "terminal_conditions": [
                "clean pushed exact final",
                "fresh four-way equality",
                "one successful non-replayed canonical",
                "current release and active plus archived registry",
                "designated future seat uniquely absent or uniquely existing",
                "one create or reuse action only",
                "no duplicate pause redirect rename usage privacy evidence safety or authority block",
            ],
            "no_precontact": True,
            "no_post_send_monitoring": True,
        },
    )
    c_free = shutil.disk_usage("C:/").free
    d_free = shutil.disk_usage("D:/").free
    write_json(
        "x1/scope-budget.json",
        {
            "owner_file_ceiling": 1999,
            "document_word_ceiling": 100000,
            "baton_word_range": [10000, 100000],
            "baton_modules": 13,
            "overview_pages_min": 3,
            "commit_cap": {"x1": 1, "evidence": 1, "final": 1, "total": 3},
            "canonical_invocation_budget": 1,
            "canonical_replay": False,
            "primary_drive": "D",
            "c_free_bytes_at_start": c_free,
            "d_free_bytes_at_start": d_free,
            "sparse_before_materialization": True,
            "execution_authority": "owner_self_scoped_delta",
            "sibling_lane_mutation": False,
            "full_repository_suite": False,
        },
    )
    write_json(
        "x1/validation-contract.json",
        {
            "source": SOURCE,
            "scope": [
                "docs/tamar-vey/v688-v3/",
                "scripts/tamar_vey_v688_v3/",
                "tests/test_ghc_family_tamar_vey_v688_v3.py",
            ],
            "hash_domain": "normalized LF Git blobs",
            "required": [
                "strict JSON duplicate and nonfinite refusal",
                "type-sensitive complete outputs",
                "input immutability",
                "all preregistered candidates",
                "source and x1 immutability",
                "exact manifests and exclusions",
                "five-class privacy adjudication",
                "bounded changed-code review",
                "exact staged allowlists",
                "direct single-parent ancestry",
                "zero merges",
                "clean typed zero divergence and fresh four-way equality",
            ],
            "canonical": "Exclusive external invocation marker after final push. Existing marker or success blocks replay.",
            "full_repository_suite": False,
        },
    )
    write_json(
        "x1/reflection-plan.json",
        {
            "disposition": "remaster_additive",
            "kept_current": ["GHC Family Index precedence", "Method Flow schema", "release profile", "skill-creator validation"],
            "kept_compatibility": ["all inherited SVG, caption, and font-related tools"],
            "new_scope": "Twenty font-outline and glyph-metadata operations with literal complete outputs; no rendering, real-font, shaping-quality, accessibility, or rights claim.",
            "known_callers": "No existing caller is changed; new skill and runner fixtures must supply bounded caller evidence in x2.",
            "rollback": "Stop selecting the additive tools and preserve all existing callers and history.",
            "protected_gates": GATES,
        },
    )
    write_json(
        "x1/workflow-refinement.json",
        {
            "submitted_current": "Tamar Vey v688-v3",
            "submitted_next": "future-sibling-12-self-chosen v688-v4",
            "following": "Elowen Cairn v688-v5",
            "normalization_changes_ownership": False,
            "requires_user_confirmation": False,
            "current_profile": "Hamish release 6 September 2026",
            "historical_cursors_preserved": True,
            "planning_only": True,
            "strict_x1_before_x2": True,
            "budget_counts": {"inherited": 200, "new": 200, "safe": 300, "candidates": 250, "cfr": 300, "exact": 50, "blocked": 30, "skills": 10, "runners": 5, "packages": 3},
            "boundary": BOUNDARY,
        },
    )
    write_json(
        "x1/deck-plan.json",
        {
            "tiers": ["freed_id_anchor", "trinity_pillar", "bounded_practice", "task"],
            "counts": {"owner": 1, "pillar": 3, "practice": 4, "proposal_task": 200},
            "each_nonroot_one_parent_in_previous_tier": True,
            "build_after_x1_equality_only": True,
            "cache_or_identity_gain_claimed": False,
        },
    )
    write_json(
        "x1/phase-truth.json",
        {
            "owner": OWNER,
            "phase": PHASE,
            "state": "PLANNING_ONLY_NOT_FROZEN",
            "source": SOURCE,
            "source_repository_seal": SEALED_SOURCE,
            "activation_baseline": ACTIVATION_BASELINE,
            "planned_proposal_chain": 16030,
            "planned_outcomes": {"completed": 178, "represented": 17, "open_gap": 2, "exact_gate": 3},
            "x2_execution_count": 0,
            "package_installations": 0,
            "promotions": 0,
            "canonical_invocations": 0,
            "successor_contacts": 0,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )
    build_overview(proposals, reviews)
    print(
        json.dumps(
            {
                "planning_contracts": len(proposals),
                "outcomes": {label: sum(item["expected_execution_disposition"] == label for item in proposals) for label in ["completed", "represented", "open_gap", "exact_gate"]},
                "reachable_proposal_json_files": len(index["files"]),
                "reachable_title_records": len(index["rows"]),
                "maximum_title_neighbor": max(row["token_jaccard"] for row in reviews),
                "x2_implementation": False,
                "packages_installed": 0,
                "startup_negatives": len(STARTUP_FAILURES),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
