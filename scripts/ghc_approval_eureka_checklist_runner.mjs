#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const name = key.slice(2);
    const value = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
    args[name] = value;
  }
  return args;
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

function inc(map, key) {
  map[key] = (map[key] || 0) + 1;
}

function matrix(rows) {
  const byScope = {};
  const byCompletion = {};
  const byScopeCompletion = {};
  for (const row of rows) {
    const scope = String(row.scope_bucket || row.status || "uncategorized");
    const completion = String(row.completion_bucket || "uncompleted");
    inc(byScope, scope);
    inc(byCompletion, completion);
    byScopeCompletion[scope] ||= {};
    inc(byScopeCompletion[scope], completion);
  }
  return { by_scope: byScope, by_completion: byCompletion, by_scope_completion: byScopeCompletion };
}

function sanitizeRow(row) {
  return {
    order: row.order,
    kind: row.kind,
    id: row.id,
    title: row.title || "Untitled",
    scope_bucket: row.scope_bucket || row.status || "uncategorized",
    completion_bucket: row.completion_bucket || "uncompleted",
    source_phase: row.source_phase || "unknown"
  };
}

function countExecutable(rows) {
  return rows.filter((row) => row.scope_bucket === "safe_now" && row.completion_bucket !== "completed").length;
}

function makeMarkdown(report) {
  const lines = [];
  lines.push(`# ${report.phase_slug} Approval/Eureka Checklist`);
  lines.push("");
  lines.push(`Status: ${report.status}`);
  lines.push(`Generated UTC: ${report.generated_utc}`);
  lines.push("");
  lines.push("## Counts");
  lines.push("");
  lines.push(`- Approval packets: ${report.counts.approval_packets}`);
  lines.push(`- Eureka tasks: ${report.counts.eureka_tasks}`);
  lines.push(`- Total rows: ${report.counts.total_rows}`);
  lines.push(`- Safe-now uncompleted approval packets: ${report.counts.safe_now_uncompleted_approval_packets}`);
  lines.push(`- Safe-now uncompleted Eureka tasks: ${report.counts.safe_now_uncompleted_eureka_tasks}`);
  lines.push("");
  lines.push("## Approval Matrix");
  lines.push("");
  lines.push("```json");
  lines.push(JSON.stringify(report.approval_matrix, null, 2));
  lines.push("```");
  lines.push("");
  lines.push("## Eureka Matrix");
  lines.push("");
  lines.push("```json");
  lines.push(JSON.stringify(report.eureka_matrix, null, 2));
  lines.push("```");
  lines.push("");
  lines.push("## Next Safe Approval Rows");
  lines.push("");
  for (const row of report.next_safe_approval_rows) {
    lines.push(`- ${row.id}: ${row.title} (${row.source_phase})`);
  }
  if (report.next_safe_approval_rows.length === 0) lines.push("- None.");
  lines.push("");
  lines.push("## Next Safe Eureka Rows");
  lines.push("");
  for (const row of report.next_safe_eureka_rows) {
    lines.push(`- ${row.id}: ${row.title} (${row.source_phase})`);
  }
  if (report.next_safe_eureka_rows.length === 0) lines.push("- None.");
  lines.push("");
  lines.push("## Boundaries");
  lines.push("");
  lines.push("- This checklist publishes status-only row IDs, titles, phase labels, and counts.");
  lines.push("- It does not publish raw sibling responses, raw browser routes, screenshots, session streams, credentials, or private dumps.");
  lines.push("- Candidate, defer, blocked, and needs_exact_packet rows are planning or approval surfaces only, not execution approval.");
  return `${lines.join("\n").replace(/\n+$/u, "")}\n`;
}

function main() {
  const args = parseArgs(process.argv);
  const required = ["phase-slug", "stack-json", "receipt-json", "receipt-md"];
  for (const key of required) {
    if (!args[key]) throw new Error(`Missing --${key}`);
  }
  const limit = Number(args.limit || 40);
  const stack = readJson(args["stack-json"]);
  const approvals = Array.isArray(stack.approval_packets) ? stack.approval_packets : [];
  const eurekas = Array.isArray(stack.eureka_tasks) ? stack.eureka_tasks : [];
  const approvalMatrix = matrix(approvals);
  const eurekaMatrix = matrix(eurekas);
  const safeApprovals = approvals
    .filter((row) => row.scope_bucket === "safe_now" && row.completion_bucket !== "completed")
    .slice(0, limit)
    .map(sanitizeRow);
  const safeEurekas = eurekas
    .filter((row) => row.scope_bucket === "safe_now" && row.completion_bucket !== "completed")
    .slice(0, limit)
    .map(sanitizeRow);

  const report = {
    schema: "ghc.approval_eureka_checklist.v1",
    generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
    phase_slug: args["phase-slug"],
    status: "PASS_APPROVAL_EUREKA_CHECKLIST_READY",
    source_stack_ref: args["stack-json"],
    counts: {
      approval_packets: approvals.length,
      eureka_tasks: eurekas.length,
      total_rows: approvals.length + eurekas.length,
      safe_now_uncompleted_approval_packets: countExecutable(approvals),
      safe_now_uncompleted_eureka_tasks: countExecutable(eurekas)
    },
    approval_matrix: approvalMatrix,
    eureka_matrix: eurekaMatrix,
    next_safe_approval_rows: safeApprovals,
    next_safe_eureka_rows: safeEurekas,
    publication_boundary: {
      raw_lane_content_published: false,
      raw_chatgpt_transcript_published: false,
      raw_browser_routes_published: false,
      screen_capture_files_published: false,
      session_trace_files_published: false,
      credentials_published: false,
      local_absolute_paths_published: false
    },
    claim_boundary: {
      x2_phase_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      canon_promotion: "not_claimed"
    }
  };

  writeJson(args["receipt-json"], report);
  writeText(args["receipt-md"], makeMarkdown(report));
  console.log(JSON.stringify({
    status: report.status,
    approval_packets: approvals.length,
    eureka_tasks: eurekas.length,
    safe_now_uncompleted_approval_packets: report.counts.safe_now_uncompleted_approval_packets,
    safe_now_uncompleted_eureka_tasks: report.counts.safe_now_uncompleted_eureka_tasks
  }, null, 2));
}

main();
