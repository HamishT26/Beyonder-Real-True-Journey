#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
    args[key.slice(2)] = value;
  }
  return args;
}

function need(args, key) {
  if (!args[key]) throw new Error(`Missing --${key}`);
  return args[key];
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8"));
}

function writeJson(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
}

function writeText(file, value) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, value);
}

function publicRef(file) {
  const normalized = file.replace(/\\/g, "/");
  const docs = normalized.lastIndexOf("docs/");
  if (docs >= 0) return normalized.slice(docs);
  const scripts = normalized.lastIndexOf("scripts/");
  if (scripts >= 0) return normalized.slice(scripts);
  return path.basename(normalized);
}

function bucketFor(row) {
  const text = `${row.title || ""} ${row.action_summary || ""} ${row.action || ""}`.toLowerCase();
  if (/current-state|current state|beacon|omega-mini|freshness|mirror/u.test(text)) return "state_and_beacon_freshness";
  if (/catch-up|catchup|handoff|sibling|prompt/u.test(text)) return "sibling_catchup_and_handoff";
  if (/browser|route|marker|lane|health/u.test(text)) return "route_marker_and_lane_health";
  if (/source|security|exposure|guard|gate|proof|d-drive|hygiene/u.test(text)) return "source_security_and_gate_rails";
  if (/status index|index|closeout|digest|summarize/u.test(text)) return "intake_digest_and_closeout";
  return "general_x2_build_use";
}

function queueRow(row, index, kind) {
  return {
    tracker_order: row.order || row.selector_order || index + 1,
    id: `${kind}-${row.id || index + 1}`,
    title: row.title || "Untitled safe-now row",
    scope_bucket: "safe_now",
    completion_bucket: "uncompleted",
    queue_status: "queued_for_x2_build_use",
    x2_execution_bucket: bucketFor(row),
    source_ref: row.source_ref || "",
    action: row.action_summary || row.action || "",
    x2_execution_order: index + 1,
    source_kind: kind,
  };
}

function countBy(rows, field) {
  return rows.reduce((acc, row) => {
    acc[row[field]] = (acc[row[field]] || 0) + 1;
    return acc;
  }, {});
}

function markdown(report) {
  const lines = [];
  lines.push(`# ${report.phase_slug} Safe-Now Queue`);
  lines.push("");
  lines.push(`Status: ${report.status}`);
  lines.push(`Target phase: ${report.target_phase_slug}`);
  lines.push(`Queued rows: ${report.queued_for_x2_count}`);
  lines.push("");
  lines.push("## Queue Buckets");
  lines.push("");
  for (const [bucket, count] of Object.entries(report.queue_bucket_counts)) {
    lines.push(`- ${bucket}: ${count}`);
  }
  lines.push("");
  lines.push("## Queue Rows");
  lines.push("");
  for (const row of report.queue_rows) {
    lines.push(`- ${row.x2_execution_order}. ${row.id}: ${row.title} (${row.x2_execution_bucket})`);
  }
  lines.push("");
  lines.push("## Boundary");
  lines.push("");
  lines.push("- Queue rows are derived from selected safe_now uncompleted approval/Eureka rows only.");
  lines.push("- No raw sibling text, raw browser routes, screenshots, session traces, credentials, or local absolute paths are published.");
  lines.push("- This queue is execution planning evidence; empirical GMUT closure and canon promotion remain open.");
  return `${lines.join("\n")}\n`;
}

function main() {
  const args = parseArgs(process.argv);
  const phaseSlug = need(args, "phase-slug");
  const targetPhaseSlug = need(args, "target-phase-slug");
  const selectorJson = need(args, "selector-json");
  const receiptJson = need(args, "receipt-json");
  const receiptMd = need(args, "receipt-md");
  const selector = readJson(selectorJson);
  const approvals = Array.isArray(selector.selected_rows)
    ? selector.selected_rows.filter((row) => row.kind === "approval_packet")
    : [];
  const eurekas = Array.isArray(selector.selected_rows)
    ? selector.selected_rows.filter((row) => row.kind === "eureka_task")
    : [];
  const queueRows = [...approvals, ...eurekas].map((row, index) => queueRow(row, index, row.kind || "selected"));
  const report = {
    schema: "ghc.safe_now_selection_queue.v1",
    generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
    phase_slug: phaseSlug,
    target_phase_slug: targetPhaseSlug,
    status: "PASS_SAFE_NOW_SELECTION_QUEUE_READY",
    selector_source_ref: publicRef(selectorJson),
    selected_approval_count: approvals.length,
    selected_eureka_count: eurekas.length,
    queued_for_x2_count: queueRows.length,
    completed_evidence_count: 0,
    held_from_x2_count: 0,
    queue_bucket_counts: countBy(queueRows, "x2_execution_bucket"),
    queue_rows: queueRows,
    execution_rule: [
      "Execute queue rows as status-only x2 build/use artifacts under exact repo validation guards.",
      "Do not treat queue duration or row count as empirical GMUT proof, canon closure, or consciousness proof.",
      "Rows outside safe_now selection remain outside execution.",
    ],
    publication_boundary: {
      raw_lane_content_published: false,
      raw_chatgpt_transcript_published: false,
      raw_browser_routes_published: false,
      raw_route_handles_published: false,
      screen_capture_files_published: false,
      session_trace_files_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
    },
    claim_boundary: {
      x2_execution: "queued_not_completed",
      phase_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      legal_closure: "not_claimed",
      canon_promotion: "not_claimed",
    },
  };
  writeJson(receiptJson, report);
  writeText(receiptMd, markdown(report));
  console.log(JSON.stringify({
    status: report.status,
    queued_for_x2_count: report.queued_for_x2_count,
    selected_approval_count: report.selected_approval_count,
    selected_eureka_count: report.selected_eureka_count,
  }, null, 2));
}

main();
