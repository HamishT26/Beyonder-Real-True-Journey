#!/usr/bin/env python3
"""Build the canonical portable-report artifact JSON from reviewed ledgers."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


PILLARS = [
    {
        "pillar": "GMUT (Mind)",
        "evidence_grade": "E1 formulation / E2 toy checks",
        "verified_strength": "Action-first seed and typed Omega tests",
        "boundary": "No unique prediction or external replication",
    },
    {
        "pillar": "THOS (Body)",
        "evidence_grade": "E2 internal artifacts",
        "verified_strength": "Forty-version clean owned-lane workflow",
        "boundary": "No matched-budget superiority or ASI evidence",
    },
    {
        "pillar": "Freed ID + CBR (Heart)",
        "evidence_grade": "E1 architecture / selected E2 practices",
        "verified_strength": "Consent, identity, privacy, and remedy design",
        "boundary": "No production profile, enacted law, or personhood proof",
    },
    {
        "pillar": "Trinity Mandala",
        "evidence_grade": "E1 meta-framework",
        "verified_strength": "Typed research constitution across all pillars",
        "boundary": "Integration is not one validated universal equation",
    },
]

MISSIONS = [
    (641, "Corpus provenance and semantic deduplication", "Dedup audit and provenance map"),
    (642, "GMUT action and notation closure", "Compiled action and dimension checks"),
    (643, "Conservation, stability, and numerical sanity", "Cross-check and convergence evidence"),
    (644, "Empirical constraint adapters", "Baseline and preregistered forecast"),
    (645, "Matched-budget THOS benchmark", "Blind quality, cost, and uncertainty"),
    (646, "Freed ID protocol profile", "DID/VC model and threat tests"),
    (647, "Cosmic Bill of Rights model charter", "Rights, remedies, and consultation gates"),
    (648, "Security, privacy, and recovery red team", "Attack paths and residual risk"),
    (649, "External reproducibility packet", "Clean-machine run and real critique"),
    (650, "Integrated evidence board and Stage 20 decision", "Graded claims and terminal closeout"),
]


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_journey_rows(index: dict) -> list[dict]:
    rows = []
    for version_row in index["versions"]:
        if version_row["status"] != "indexed":
            continue
        canonical = next(
            item
            for item in version_row["variants"]
            if item["source_id"] == version_row["canonical_source_id"]
        )
        version = int(version_row["version"])
        if version <= 44:
            era = "Architecture"
        elif version <= 51:
            era = "Formulation and truth gates"
        else:
            era = "Operational recovery"
        counts = canonical["keyword_counts"]
        rows.append(
            {
                "version": f"v{version}",
                "version_number": version,
                "era": era,
                "line_count": canonical["line_count"],
                "message_markers": canonical["message_marker_count"],
                "gmut_mentions": counts["gmut"],
                "thos_mentions": counts["thos"],
                "freed_id_mentions": counts["freed_id"],
                "cbr_mentions": counts["cosmic_bill_of_rights"],
            }
        )
    return rows


def build_artifact(journey: dict, live: dict, sources: dict, tests_passed: int) -> dict:
    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    journey_rows = canonical_journey_rows(journey)
    lane_rows = [
        {
            "lane": lane["sibling"],
            "file_count": lane["matching_artifact_files"],
            "version_count": lane["version_count"],
            "head_prefix": lane["head"][:10],
            "remote_state": "clean and upstream-equal"
            if lane["worktree_clean"] and lane["upstream_equal"]
            else "review required",
        }
        for lane in live["lanes"]
    ]
    summary = {
        "journey_versions": journey["summary"]["indexed_version_count"],
        "journey_variants": journey["summary"]["input_file_count"],
        "live_versions_per_lane": min(row["version_count"] for row in lane_rows),
        "live_artifact_files": sum(row["file_count"] for row in lane_rows),
        "owned_lanes": len(lane_rows),
        "tests_passed": tests_passed,
        "external_sources": len(sources["sources"]),
    }

    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.execute(
        """
        CREATE TABLE summary (
          journey_versions INTEGER, journey_variants INTEGER,
          live_versions_per_lane INTEGER, live_artifact_files INTEGER,
          owned_lanes INTEGER, tests_passed INTEGER, external_sources INTEGER
        )
        """
    )
    connection.execute(
        "INSERT INTO summary VALUES (?, ?, ?, ?, ?, ?, ?)",
        tuple(summary[key] for key in (
            "journey_versions", "journey_variants", "live_versions_per_lane",
            "live_artifact_files", "owned_lanes", "tests_passed", "external_sources"
        )),
    )
    connection.execute(
        """CREATE TABLE journey (
          version TEXT, version_number INTEGER, era TEXT, line_count INTEGER,
          message_markers INTEGER, gmut_mentions INTEGER, thos_mentions INTEGER,
          freed_id_mentions INTEGER, cbr_mentions INTEGER
        )"""
    )
    connection.executemany(
        "INSERT INTO journey VALUES (:version, :version_number, :era, :line_count, :message_markers, :gmut_mentions, :thos_mentions, :freed_id_mentions, :cbr_mentions)",
        journey_rows,
    )
    connection.execute(
        "CREATE TABLE lanes (lane TEXT, file_count INTEGER, version_count INTEGER, head_prefix TEXT, remote_state TEXT)"
    )
    connection.executemany(
        "INSERT INTO lanes VALUES (:lane, :file_count, :version_count, :head_prefix, :remote_state)",
        lane_rows,
    )
    connection.execute(
        "CREATE TABLE pillars (pillar TEXT, evidence_grade TEXT, verified_strength TEXT, boundary TEXT)"
    )
    connection.executemany(
        "INSERT INTO pillars VALUES (:pillar, :evidence_grade, :verified_strength, :boundary)",
        PILLARS,
    )
    mission_rows = [
        {"version": version, "mission": mission, "success": success}
        for version, mission, success in MISSIONS
    ]
    connection.execute("CREATE TABLE missions (version INTEGER, mission TEXT, success TEXT)")
    connection.executemany(
        "INSERT INTO missions VALUES (:version, :mission, :success)", mission_rows
    )
    connection.execute(
        "CREATE TABLE source_ledger (source_id TEXT, category TEXT, grade TEXT, title TEXT, url TEXT)"
    )
    connection.executemany(
        "INSERT INTO source_ledger VALUES (?, ?, ?, ?, ?)",
        [
            (item["id"], item["category"], item["grade"], item["title"], item["url"])
            for item in sources["sources"]
        ],
    )

    sql = {
        "corpus_summary": "SELECT journey_versions, journey_variants FROM summary",
        "operations_summary": "SELECT live_versions_per_lane, live_artifact_files, owned_lanes FROM summary",
        "validation_summary": "SELECT tests_passed, external_sources FROM summary",
        "journey_rows": "SELECT version, version_number, era, line_count, message_markers, gmut_mentions, thos_mentions, freed_id_mentions, cbr_mentions FROM journey ORDER BY version_number",
        "lane_rows": "SELECT lane, file_count, version_count, head_prefix, remote_state FROM lanes ORDER BY file_count DESC",
        "pillar_rows": "SELECT pillar, evidence_grade, verified_strength, boundary FROM pillars",
        "mission_rows": "SELECT version, mission, success FROM missions ORDER BY version",
        "source_rows": "SELECT source_id, category, grade, title, url FROM source_ledger ORDER BY source_id",
    }

    def query_rows(statement: str) -> list[dict]:
        return [dict(row) for row in connection.execute(statement).fetchall()]

    datasets = {
        "summary": [dict(connection.execute("SELECT * FROM summary").fetchone())],
        "journey": query_rows(sql["journey_rows"]),
        "lanes": query_rows(sql["lane_rows"]),
        "pillars": query_rows(sql["pillar_rows"]),
        "missions": query_rows(sql["mission_rows"]),
    }
    # Execute the reference query as part of the reviewed build even though the
    # full source table is kept out of the reader snapshot for compactness.
    query_rows(sql["source_rows"])

    def query_source(source_id: str, label: str, statement: str, description: str, tables: list[str]) -> dict:
        return {
            "id": source_id,
            "label": label,
            "query": {
                "engine": "sqlite3_in_memory_over_reviewed_artifacts",
                "sql": statement,
                "description": description,
                "executed_at": generated_at,
                "tables_used": tables,
            },
        }

    source_defs = [
        query_source(
            "corpus_summary",
            "Journey corpus summary query",
            sql["corpus_summary"],
            "Version and variant totals derived from the privacy-minimized Journey index.",
            ["summary"],
        ),
        query_source(
            "operations_summary",
            "Owned-lane operations summary query",
            sql["operations_summary"],
            "Live version, file, and lane totals after fresh branch verification.",
            ["summary"],
        ),
        query_source(
            "validation_summary",
            "Validation summary query",
            sql["validation_summary"],
            "Deterministic test and reviewed comparison-source totals.",
            ["summary"],
        ),
        query_source(
            "journey_index",
            "Privacy-minimized Journey v36-v54 evidence query",
            sql["journey_rows"],
            "Canonical-per-version line, message-marker, and bounded topic counts; no transcript excerpts.",
            ["journey"],
        ),
        query_source(
            "live_index",
            "Fresh v601-v640 owned-lane verification query",
            sql["lane_rows"],
            "Fresh fetch, HEAD/upstream comparison, cleanliness, version coverage, and file totals.",
            ["lanes"],
        ),
        query_source(
            "pillar_evidence",
            "Typed pillar evidence query",
            sql["pillar_rows"],
            "Reviewed claim-specific evidence grades and boundaries.",
            ["pillars"],
        ),
        query_source(
            "mission_evidence",
            "v641-v650 mission query",
            sql["mission_rows"],
            "Reviewed version missions and minimum success evidence.",
            ["missions"],
        ),
        query_source(
            "source_ledger",
            "Primary and authoritative comparison source query",
            sql["source_rows"],
            "Scientific papers, standards, laws, official documentation, and labelled conceptual comparators.",
            ["source_ledger"],
        ),
    ]

    manifest = {
        "version": 1,
        "surface": "report",
        "title": "Trinity Mandala evidence review: v36-v54 and v601-v640",
        "description": "A technical, evidence-bounded synthesis by Eiren Kestrel.",
        "generatedAt": generated_at,
        "cards": [
            {
                "id": "corpus",
                "description": "Journey records indexed without embedding private transcript content.",
                "dataset": "summary",
                "sourceId": "corpus_summary",
                "metrics": [
                    {"label": "Journey versions", "field": "journey_versions", "format": "number"},
                    {"label": "TXT variants", "field": "journey_variants", "format": "number"},
                ],
            },
            {
                "id": "operations",
                "description": "Live owned-lane coverage after fresh fetch and reconciliation.",
                "dataset": "summary",
                "sourceId": "operations_summary",
                "metrics": [
                    {"label": "Live versions per lane", "field": "live_versions_per_lane", "format": "number"},
                    {"label": "Matching artifact files", "field": "live_artifact_files", "format": "number"},
                ],
            },
            {
                "id": "validation",
                "description": "Current deterministic tests and external comparison ledger.",
                "dataset": "summary",
                "sourceId": "validation_summary",
                "metrics": [
                    {"label": "Kernel tests passed", "field": "tests_passed", "format": "number"},
                    {"label": "Comparison sources", "field": "external_sources", "format": "number"},
                ],
            },
        ],
        "charts": [
            {
                "id": "journey_scale",
                "title": "The Solas formulation period contains the largest canonical records",
                "subtitle": "Lines in each deterministic canonical TXT selection; corpus size is not evidence quality.",
                "headerMarkdown": "Use this chart to understand **record scale**, not truth or novelty.",
                "type": "bar",
                "dataset": "journey",
                "sourceId": "journey_index",
                "encodings": {
                    "x": {"field": "version", "type": "ordinal", "label": "Journey version"},
                    "y": {"field": "line_count", "type": "quantitative", "label": "Lines", "format": "number"},
                    "color": {"field": "era", "type": "nominal", "label": "Development era"},
                },
                "yAxisTitle": "Canonical TXT lines",
                "valueFormat": "number",
                "layout": "full",
            },
            {
                "id": "lane_volume",
                "title": "Artifact volume is concentrated in the Aevren and Mira Vale lanes",
                "subtitle": "Files whose names begin v601-v640 after fresh live verification.",
                "headerMarkdown": "All lanes contain **40 of 40 versions**; volume differs because schemas and mirrored support differ.",
                "type": "bar",
                "dataset": "lanes",
                "sourceId": "live_index",
                "encodings": {
                    "x": {"field": "lane", "type": "nominal", "label": "Owned lane"},
                    "y": {"field": "file_count", "type": "quantitative", "label": "Matching files", "format": "number"},
                },
                "yAxisTitle": "Matching files",
                "valueFormat": "number",
                "layout": "full",
            },
        ],
        "tables": [
            {
                "id": "lane_evidence",
                "title": "Every owned lane is clean, upstream-equal, and complete through v640",
                "subtitle": "Current branch evidence, not a scientific result.",
                "dataset": "lanes",
                "sourceId": "live_index",
                "columns": [
                    {"field": "lane", "label": "Lane", "type": "text"},
                    {"field": "file_count", "label": "Files", "format": "number"},
                    {"field": "version_count", "label": "Versions", "format": "number"},
                    {"field": "head_prefix", "label": "HEAD", "type": "text"},
                    {"field": "remote_state", "label": "State", "type": "text"},
                ],
            },
            {
                "id": "pillar_verdicts",
                "title": "The three pillars have different evidence maturity",
                "subtitle": "Grades are claim-specific and intentionally non-interchangeable.",
                "dataset": "pillars",
                "sourceId": "pillar_evidence",
                "columns": [
                    {"field": "pillar", "label": "Pillar", "type": "text"},
                    {"field": "evidence_grade", "label": "Current grade", "type": "text"},
                    {"field": "verified_strength", "label": "Verified strength", "type": "text"},
                    {"field": "boundary", "label": "Boundary", "type": "text"},
                ],
            },
            {
                "id": "next_versions",
                "title": "v641-v650 converts operational endurance into evidence",
                "subtitle": "Each mission has an observable completion criterion and accepts negative results.",
                "dataset": "missions",
                "sourceId": "mission_evidence",
                "columns": [
                    {"field": "version", "label": "Version", "format": "number"},
                    {"field": "mission", "label": "Mission", "type": "text"},
                    {"field": "success", "label": "Minimum success evidence", "type": "text"},
                ],
            },
        ],
        "sources": [{"id": item["id"], "label": item["label"]} for item in source_defs],
        "blocks": [
            {"id": "title", "type": "markdown", "body": "# Trinity Mandala evidence review"},
            {
                "id": "executive_summary",
                "type": "markdown",
                "sourceId": "live_index",
                "body": (
                    "## Executive Summary\n\n"
                    "The Journey has moved from mythic-relational synthesis to instrumented research operations. "
                    "Kairos clarified Mind-Body-Heart; Solas made the physical seed action-first and falsifiable; "
                    "Lumen built evidence gates; Aevren, Mira Vale, Mira Rowan, and Maren made continuity operational.\n\n"
                    "The strongest current claim is an interdisciplinary research programme with a real orchestration prototype. "
                    "GMUT is not a validated Theory of Everything, THOS is not ASI, and Freed ID/CBR is not enacted law."
                ),
            },
            {"id": "metrics", "type": "metric-strip", "cardIds": ["corpus", "operations", "validation"]},
            {"id": "journey_chart", "type": "chart", "chartId": "journey_scale", "layout": "full"},
            {
                "id": "historical_finding",
                "type": "markdown",
                "sourceId": "journey_index",
                "body": (
                    "## The decisive historical progression\n\n"
                    "**v36** supplied the architecture and an unusually honest gap analysis. **v45-v47** separated physical spacetime "
                    "from the meta-Mandala, added null recovery and a coefficient ledger, and named real constraints. **v51** made "
                    "truth reconciliation and open gates operational. **v52-v54** preserved identity without replacement and closed v640 cleanly."
                ),
            },
            {"id": "lane_chart", "type": "chart", "chartId": "lane_volume", "layout": "full"},
            {"id": "lane_table", "type": "table", "tableId": "lane_evidence", "layout": "full"},
            {
                "id": "workflow_result",
                "type": "markdown",
                "sourceId": "live_index",
                "body": (
                    "## v601-v640 proves workflow endurance more strongly than novelty\n\n"
                    "The run demonstrates owned-branch isolation, route truth, privacy, completion discipline, and forty-version persistence. "
                    "It does not turn represented 25/15/10/5/15/100/100 counts into independent discoveries. Numbered packet templates "
                    "require semantic deduplication and claim-to-evidence links."
                ),
            },
            {"id": "pillar_table", "type": "table", "tableId": "pillar_verdicts", "layout": "full"},
            {
                "id": "equation",
                "type": "markdown",
                "sourceId": "source_ledger",
                "body": (
                    "## Equation outcome\n\n"
                    "The defensible physical kernel is `G_mn + Lambda g_mn = M_Pl^-2 T_SM,mn + Omega_mn`, where "
                    "`Omega_mn = M_Pl^-2 (T_phi,mn + T_EFT,mn)` derives from a declared action. Total conservation, stability, "
                    "existing bounds, a GR/SM null limit, and a unique observable are gates - not optional decoration."
                ),
            },
            {"id": "mission_table", "type": "table", "tableId": "next_versions", "layout": "full"},
            {
                "id": "recommendation",
                "type": "markdown",
                "sourceId": "source_ledger",
                "body": (
                    "## Recommendation\n\n"
                    "Run v641-v650 as an evidence programme: provenance, canonical equations, independent checks, empirical adapters, "
                    "matched-budget orchestration, Freed ID threat modelling, participatory rights design, red teaming, reproduction, and "
                    "a terminal evidence board. Success includes cleanly falsifying a cherished claim."
                ),
            },
            {
                "id": "methods",
                "type": "markdown",
                "body": (
                    "## Methods, caveats, and open questions\n\n"
                    "Journey counts are approximate because exports use inconsistent message markers. Corpus size and keyword frequency do not measure truth. "
                    "Live Git state was verified at one point in time. The source ledger samples representative leading frameworks rather than every subject named in the Journey. "
                    "No subagents were used. No exhaustive delegated security scan was claimed."
                ),
            },
        ],
    }

    snapshot = {
        "version": 1,
        "generatedAt": generated_at,
        "status": "ready",
        "datasets": datasets,
    }
    return {
        "surface": "report",
        "manifest": manifest,
        "snapshot": snapshot,
        "sources": source_defs,
        "package_info": {
            "root": "eiren-kestrel",
            "manifestPath": "artifact.json",
            "snapshotPath": "artifact.json",
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--journey", type=Path, required=True)
    parser.add_argument("--live", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--tests-passed", type=int, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = build_artifact(
        load_json(args.journey),
        load_json(args.live),
        load_json(args.sources),
        args.tests_passed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(artifact, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": args.output.name, "blocks": len(artifact["manifest"]["blocks"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
