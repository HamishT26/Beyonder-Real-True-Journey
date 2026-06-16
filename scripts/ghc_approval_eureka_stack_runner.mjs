#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname } from "node:path";

const args = parseArgs(process.argv.slice(2));

const phaseSlug = requireArg("--phase-slug");
const receiptJson = requireArg("--receipt-json");
const receiptMd = requireArg("--receipt-md");
const approvalSources = args.get("--approval-source-json") || [];
const eurekaSources = args.get("--eureka-source-json") || [];

if (approvalSources.length === 0 && eurekaSources.length === 0) {
  console.error(
    "Usage: node ghc_approval_eureka_stack_runner.mjs --phase-slug <slug> [--approval-source-json <json> ...] [--eureka-source-json <json> ...] --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      if (!parsed.has(key)) parsed.set(key, []);
      parsed.get(key).push("true");
      continue;
    }
    if (!parsed.has(key)) parsed.set(key, []);
    parsed.get(key).push(value);
    index += 1;
  }
  return parsed;
}

function requireArg(key) {
  const values = args.get(key);
  if (!values || !values[0]) {
    console.error(`Missing required argument: ${key}`);
    process.exit(2);
  }
  return values[0];
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function publicSourceRef(path) {
  const normalized = path.replace(/\\/g, "/");
  const docsIndex = normalized.lastIndexOf("docs/");
  if (docsIndex >= 0) return normalized.slice(docsIndex);
  const scriptsIndex = normalized.lastIndexOf("scripts/");
  if (scriptsIndex >= 0) return normalized.slice(scriptsIndex);
  return basename(normalized);
}

function compactText(...values) {
  return values
    .filter((value) => value !== undefined && value !== null)
    .map((value) => String(value).toLowerCase())
    .join(" ");
}

function normalizeScopeBucket(row) {
  const text = compactText(row.scope_bucket, row.status, row.scope, row.title, row.reason, row.result, row.purpose, row.action);
  if (/\b(needs[_ -]?exact[_ -]?packet|exact packet required|separate exact packet|outside approved scope)\b/u.test(text)) {
    return "needs_exact_packet";
  }
  if (/\b(blocked|blocker|failed|open gap|open_gap|denied|unsafe|not approved)\b/u.test(text)) return "blocked";
  if (/\b(defer|deferred|standby|later|hold)\b/u.test(text)) return "defer";
  if (/\b(pending|candidate|approval needed|approval-needed|approval_needed|review required|proposed|queued_for_x2)\b/u.test(text)) {
    return row.scope_bucket === "safe_now" ? "safe_now" : "candidate";
  }
  if (/\b(safe_now|safe now|approved|authorized|ready|pass|materialized|completed|implemented|closed)\b/u.test(text)) {
    return "safe_now";
  }
  return "candidate";
}

function normalizeCompletionBucket(row) {
  const text = compactText(row.completion_bucket, row.completion, row.completed, row.status, row.result, row.evidence, row.queue_status, row.title);
  if (/\b(false|uncompleted|incomplete|pending|candidate|defer|deferred|blocked|failed|open gap|open_gap|queued_for_x2)\b/u.test(text)) {
    return "uncompleted";
  }
  if (/\b(true|completed|complete|closed|built|implemented|approved|authorized|materialized)\b/u.test(text) || text.startsWith("pass")) {
    return "completed";
  }
  return "uncompleted";
}

function titleOf(value, fallback) {
  return value?.title || value?.source_task || value?.name || value?.id || value?.task_id || fallback;
}

function idOf(value, fallback) {
  return value?.id || value?.packet_id || value?.task_id || value?.output || value?.artifact || fallback;
}

function sourcePhase(payload) {
  return payload.target_phase_slug || payload.phase_slug || "unknown-phase";
}

function collectApprovalRows(payload, sourceRef) {
  const fields = ["packets", "approval_packets", "approval_candidates", "approval_packet_candidates", "approval_packet_scope"];
  const rows = [];
  for (const field of fields) {
    const value = payload[field];
    if (!Array.isArray(value)) continue;
    value.forEach((packet, index) => {
      if (!packet || typeof packet !== "object") return;
      rows.push({
        kind: "approval_packet",
        id: idOf(packet, `${field}-${index + 1}`),
        title: titleOf(packet, "Untitled approval packet"),
        status: packet.status || packet.state || "candidate",
        scope_bucket: packet.scope_bucket,
        completion_bucket: packet.completion_bucket,
        purpose: packet.purpose || packet.scope || packet.result || packet.build_use || "",
        source_ref: sourceRef,
        source_phase: sourcePhase(payload),
        source_field: field,
        source_order: index + 1,
      });
    });
  }
  if (rows.length > 0) return rows;
  const text = compactText(payload.schema, payload.artifact_type, payload.title, sourceRef);
  if (!/\bapproval\b/u.test(text)) return [];
  return [
    {
      kind: "approval_packet",
      id: idOf(payload, basename(sourceRef, ".json")),
      title: titleOf(payload, "Approval packet artifact"),
      status: payload.status || "candidate",
      scope_bucket: payload.scope_bucket,
      completion_bucket: payload.completion_bucket,
      purpose: payload.purpose || payload.scope || payload.result || payload.build_use || "",
      source_ref: sourceRef,
      source_phase: sourcePhase(payload),
      source_field: "top_level_approval_artifact",
      source_order: 1,
    },
  ];
}

function collectEurekaRows(payload, sourceRef) {
  const fields = ["tasks", "eureka_tasks", "implemented_tasks", "x2_tasks", "queue_rows"];
  const rows = [];
  for (const field of fields) {
    const value = payload[field];
    if (!Array.isArray(value)) continue;
    value.forEach((task, index) => {
      if (!task || typeof task !== "object") return;
      rows.push({
        kind: "eureka_task",
        id: idOf(task, `${field}-${index + 1}`),
        title: titleOf(task, "Untitled Eureka task"),
        status: task.status || task.queue_status || (field === "implemented_tasks" ? "implemented" : "candidate"),
        scope_bucket: task.scope_bucket,
        completion_bucket: field === "implemented_tasks" ? "completed" : task.completion_bucket,
        action: task.x2_action || task.build_use || task.result || task.purpose || task.action || "",
        source_ref: sourceRef,
        source_phase: sourcePhase(payload),
        source_field: field,
        source_order: index + 1,
      });
    });
  }
  if (rows.length > 0) return rows;
  const text = compactText(payload.schema, payload.artifact_type, payload.title, sourceRef);
  if (!/\b(eureka|task|materialization)\b/u.test(text)) return [];
  return [
    {
      kind: "eureka_task",
      id: idOf(payload, basename(sourceRef, ".json")),
      title: titleOf(payload, "Task artifact"),
      status: payload.status || "candidate",
      scope_bucket: payload.scope_bucket,
      completion_bucket: payload.completion_bucket,
      action: payload.x2_action || payload.build_use || payload.result || payload.purpose || "",
      source_ref: sourceRef,
      source_phase: sourcePhase(payload),
      source_field: "top_level_task_artifact",
      source_order: 1,
    },
  ];
}

function countBy(rows, field) {
  return rows.reduce((counts, row) => {
    counts[row[field]] = (counts[row[field]] || 0) + 1;
    return counts;
  }, {});
}

function dedupeRows(rows) {
  const seen = new Set();
  const deduped = [];
  for (const row of rows) {
    const key = `${row.kind}|${row.id}|${row.title}|${row.source_phase}`;
    if (seen.has(key)) continue;
    seen.add(key);
    deduped.push(row);
  }
  return deduped;
}

function readSources(paths, collector, kindLabel) {
  const rows = [];
  const reports = [];
  for (const path of paths) {
    const sourceRef = publicSourceRef(path);
    if (!existsSync(path)) {
      reports.push({ kind: kindLabel, source_ref: sourceRef, status: "MISSING_SKIPPED", row_count: 0 });
      continue;
    }
    const payload = readJson(path);
    const extracted = collector(payload, sourceRef);
    extracted.forEach((row) => {
      const scopeBucket = normalizeScopeBucket(row);
      const completionBucket = normalizeCompletionBucket(row);
      rows.push({
        order: rows.length + 1,
        kind: row.kind,
        id: row.id,
        title: row.title,
        status: row.status,
        scope_bucket: scopeBucket,
        completion_bucket: completionBucket,
        source_phase: row.source_phase,
        source_ref: row.source_ref,
        source_field: row.source_field,
        source_order: row.source_order,
        purpose_or_action: row.purpose || row.action || "",
      });
    });
    reports.push({ kind: kindLabel, source_ref: sourceRef, status: "READ", row_count: extracted.length });
  }
  return { rows, reports };
}

function summarizeRows(rows) {
  const scopeBuckets = ["safe_now", "candidate", "defer", "blocked", "needs_exact_packet"];
  const completionBuckets = ["completed", "uncompleted"];
  const scopeCounts = Object.fromEntries(scopeBuckets.map((bucket) => [bucket, 0]));
  Object.assign(scopeCounts, countBy(rows, "scope_bucket"));
  const completionCounts = Object.fromEntries(completionBuckets.map((bucket) => [bucket, 0]));
  Object.assign(completionCounts, countBy(rows, "completion_bucket"));
  return {
    row_count: rows.length,
    scope_counts: scopeCounts,
    completion_counts: completionCounts,
    phase_counts: countBy(rows, "source_phase"),
  };
}

const approvalRead = readSources(approvalSources, collectApprovalRows, "approval_packet");
const eurekaRead = readSources(eurekaSources, collectEurekaRows, "eureka_task");
const approvalRows = dedupeRows(approvalRead.rows).map((row, index) => ({ ...row, order: index + 1 }));
const eurekaRows = dedupeRows(eurekaRead.rows).map((row, index) => ({ ...row, order: index + 1 }));

const approvalSummary = summarizeRows(approvalRows);
const eurekaSummary = summarizeRows(eurekaRows);
const backlogTargets = {
  approval_packet_target: 200,
  eureka_task_target: 200,
  approval_packet_remaining_to_target: Math.max(0, 200 - approvalSummary.row_count),
  eureka_task_remaining_to_target: Math.max(0, 200 - eurekaSummary.row_count),
  per_session_target: "20+ approval packet proposals and 20+ Eureka task proposals per phase session",
};

const receipt = {
  schema: "ghc.approval_eureka_stack.v1",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  status: "PASS_APPROVAL_EUREKA_STACK_READY",
  approval_summary: approvalSummary,
  eureka_summary: eurekaSummary,
  backlog_targets: backlogTargets,
  source_reports: [...approvalRead.reports, ...eurekaRead.reports],
  approval_packets: approvalRows,
  eureka_tasks: eurekaRows,
  next_actions: [
    "Keep adding each phase session's approval checklist and Eureka tracker to this stack.",
    "Execute safe_now uncompleted rows only inside their already approved repo-scoped boundaries.",
    "Hold candidate, defer, blocked, and needs_exact_packet rows until a matching exact packet or blocker receipt exists.",
    "Use completed rows as evidence pointers, not as raw transcript publication.",
    "Mirror the stack receipt into omega-mini so sibling prompts can use the lightweight branch first.",
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
    approval_activation: "status_only_from_sources",
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const approvalRowsMd = approvalRows
  .slice(0, 60)
  .map(
    (row) =>
      `| ${row.order} | ${row.id} | ${row.title} | ${row.scope_bucket} | ${row.completion_bucket} | ${row.source_phase} | ${row.source_ref} |`,
  );
const eurekaRowsMd = eurekaRows
  .slice(0, 60)
  .map(
    (row) =>
      `| ${row.order} | ${row.id} | ${row.title} | ${row.scope_bucket} | ${row.completion_bucket} | ${row.source_phase} | ${row.source_ref} |`,
  );

const md = [
  `# ${phaseSlug} Approval and Eureka Stack Ledger`,
  "",
  "## Status",
  "",
  `- Status: ${receipt.status}`,
  `- Approval packets: ${approvalSummary.row_count}`,
  `- Eureka tasks: ${eurekaSummary.row_count}`,
  `- Approval packets remaining to 200 target: ${backlogTargets.approval_packet_remaining_to_target}`,
  `- Eureka tasks remaining to 200 target: ${backlogTargets.eureka_task_remaining_to_target}`,
  "",
  "## Approval Scope Counts",
  "",
  `- safe_now: ${approvalSummary.scope_counts.safe_now}`,
  `- candidate: ${approvalSummary.scope_counts.candidate}`,
  `- defer: ${approvalSummary.scope_counts.defer}`,
  `- blocked: ${approvalSummary.scope_counts.blocked}`,
  `- needs_exact_packet: ${approvalSummary.scope_counts.needs_exact_packet}`,
  `- completed: ${approvalSummary.completion_counts.completed}`,
  `- uncompleted: ${approvalSummary.completion_counts.uncompleted}`,
  "",
  "## Eureka Scope Counts",
  "",
  `- safe_now: ${eurekaSummary.scope_counts.safe_now}`,
  `- candidate: ${eurekaSummary.scope_counts.candidate}`,
  `- defer: ${eurekaSummary.scope_counts.defer}`,
  `- blocked: ${eurekaSummary.scope_counts.blocked}`,
  `- needs_exact_packet: ${eurekaSummary.scope_counts.needs_exact_packet}`,
  `- completed: ${eurekaSummary.completion_counts.completed}`,
  `- uncompleted: ${eurekaSummary.completion_counts.uncompleted}`,
  "",
  "## Approval Rows",
  "",
  "| # | ID | Title | Scope | Completion | Source Phase | Source |",
  "|---:|---|---|---|---|---|---|",
  ...approvalRowsMd,
  approvalRows.length > approvalRowsMd.length ? `| ... | ${approvalRows.length - approvalRowsMd.length} more rows omitted from markdown preview; see JSON. | | | | | |` : "",
  "",
  "## Eureka Rows",
  "",
  "| # | ID | Title | Scope | Completion | Source Phase | Source |",
  "|---:|---|---|---|---|---|---|",
  ...eurekaRowsMd,
  eurekaRows.length > eurekaRowsMd.length ? `| ... | ${eurekaRows.length - eurekaRowsMd.length} more rows omitted from markdown preview; see JSON. | | | | | |` : "",
  "",
  "## Publication Boundary",
  "",
  "- Status-only stack; no raw lane text, raw ChatGPT transcript, browser routes, screenshots, session streams, credentials, or local absolute paths are published.",
  "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  "",
];

writeFileSync(receiptMd, `${md.filter((line) => line !== "").join("\n")}\n`, "utf8");

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      approval_packet_count: approvalSummary.row_count,
      eureka_task_count: eurekaSummary.row_count,
      approval_remaining_to_target: backlogTargets.approval_packet_remaining_to_target,
      eureka_remaining_to_target: backlogTargets.eureka_task_remaining_to_target,
    },
    null,
    2,
  ),
);
