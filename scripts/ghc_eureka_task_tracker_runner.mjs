#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname } from "node:path";

const args = parseArgs(process.argv.slice(2));

const phaseSlug = requireArg("--phase-slug");
const receiptJson = requireArg("--receipt-json");
const receiptMd = requireArg("--receipt-md");
const sourceJsons = args.get("--source-json") || [];

if (sourceJsons.length === 0) {
  console.error(
    "Usage: node ghc_eureka_task_tracker_runner.mjs --phase-slug <slug> --source-json <json> [--source-json <json> ...] --receipt-json <json> --receipt-md <md>",
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

function normalizeScopeBucket(task) {
  const statusText = compactText(task.status);
  if (statusText.includes("needs_exact_packet") || statusText.includes("exact packet required") || statusText.includes("separate exact packet")) {
    return "needs_exact_packet";
  }
  if (statusText.includes("blocked") || statusText.includes("blocker") || statusText.includes("failed") || statusText.includes("open_gap") || statusText.includes("open gap") || statusText.includes("denied") || statusText.includes("unsafe")) {
    return "blocked";
  }
  if (statusText.includes("defer") || statusText.includes("standby") || statusText.includes("later") || statusText.includes("hold")) {
    return "defer";
  }
  if (statusText.includes("pending") || statusText.includes("candidate") || statusText.includes("approval needed") || statusText.includes("approval_needed") || statusText.includes("review required") || statusText.includes("proposed") || statusText.includes("x2_build_candidate")) {
    return "candidate";
  }
  if (statusText.includes("safe_now") || statusText.includes("safe now") || statusText.includes("approved") || statusText.includes("authorized") || statusText.includes("ready") || statusText.startsWith("pass") || statusText.includes("materialized") || statusText.includes("completed") || statusText.includes("implemented") || statusText.includes("closed")) {
    return "safe_now";
  }
  const text = compactText(task.status, task.scope, task.title, task.reason, task.result, task.x2_action, task.build_use);
  if (/\b(needs[_ -]?exact[_ -]?packet|exact packet required|separate exact packet|outside approved scope)\b/u.test(text)) {
    return "needs_exact_packet";
  }
  if (/\b(blocked|blocker|failed|open gap|open_gap|denied|unsafe|not approved)\b/u.test(text)) {
    return "blocked";
  }
  if (/\b(defer|deferred|standby|later|hold)\b/u.test(text)) {
    return "defer";
  }
  if (/\b(pending|candidate|approval needed|approval-needed|approval_needed|review required|proposed|x2_build_candidate)\b/u.test(text)) {
    return "candidate";
  }
  if (/\b(safe_now|safe now|approved|authorized|ready|pass|materialized|completed|implemented|closed)\b/u.test(text)) {
    return "safe_now";
  }
  return "candidate";
}

function normalizeCompletionBucket(task, sourceField) {
  if (sourceField === "implemented_tasks") return "completed";
  const text = compactText(task.completion, task.completed, task.status, task.result, task.evidence, task.title);
  if (/\b(false|uncompleted|incomplete|pending|candidate|defer|deferred|blocked|failed|open gap|open_gap)\b/u.test(text)) {
    return "uncompleted";
  }
  if (/\b(true|completed|complete|closed|built|implemented|approved|authorized)\b/u.test(text) || text.startsWith("pass") || text.includes("materialized")) {
    return "completed";
  }
  return "uncompleted";
}

function titleOf(value, fallback) {
  return value?.title || value?.source_task || value?.name || value?.id || value?.task_id || fallback;
}

function idOf(value, fallback) {
  return value?.id || value?.task_id || value?.output || value?.artifact || fallback;
}

function taskAction(value) {
  return value?.x2_action || value?.build_use || value?.result || value?.purpose || value?.scope || "";
}

function collectArrayTasks(payload, sourceRef) {
  const fields = ["eureka_tasks", "implemented_tasks", "tasks"];
  const rows = [];
  for (const field of fields) {
    const value = payload[field];
    if (!Array.isArray(value)) continue;
    value.forEach((task, index) => {
      if (!task || typeof task !== "object") return;
      rows.push({
        id: idOf(task, `${field}-${index + 1}`),
        title: titleOf(task, "Untitled Eureka task"),
        status: task.status || (field === "implemented_tasks" ? "implemented" : "candidate"),
        action: taskAction(task),
        source_ref: sourceRef,
        source_field: field,
        source_order: index + 1,
      });
    });
  }
  return rows;
}

function collectTopLevelTask(payload, sourceRef) {
  const text = compactText(payload.artifact_type, payload.artifact, payload.title, payload.task_id, sourceRef);
  if (!/\b(eureka|task|materialization)\b/u.test(text)) return [];
  return [
    {
      id: idOf(payload, basename(sourceRef, ".json")),
      title: titleOf(payload, "Task artifact"),
      status: payload.status || "candidate",
      action: taskAction(payload),
      source_ref: sourceRef,
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

const sourceReports = [];
const tasks = [];

for (const sourceJson of sourceJsons) {
  const sourceRef = publicSourceRef(sourceJson);
  if (!existsSync(sourceJson)) {
    sourceReports.push({ source_ref: sourceRef, status: "MISSING_SKIPPED", task_count: 0 });
    continue;
  }
  const payload = readJson(sourceJson);
  const extracted = [...collectArrayTasks(payload, sourceRef), ...collectTopLevelTask(payload, sourceRef)];
  extracted.forEach((task) => {
    const scope_bucket = normalizeScopeBucket(task);
    const completion_bucket = normalizeCompletionBucket(task, task.source_field);
    tasks.push({
      order: tasks.length + 1,
      id: task.id,
      title: task.title,
      status: task.status,
      scope_bucket,
      completion_bucket,
      source_ref: task.source_ref,
      source_field: task.source_field,
      source_order: task.source_order,
      action: task.action,
    });
  });
  sourceReports.push({ source_ref: sourceRef, status: "READ", task_count: extracted.length });
}

const scopeBuckets = ["safe_now", "candidate", "defer", "blocked", "needs_exact_packet"];
const completionBuckets = ["completed", "uncompleted"];
const scopeCounts = Object.fromEntries(scopeBuckets.map((bucket) => [bucket, 0]));
Object.assign(scopeCounts, countBy(tasks, "scope_bucket"));
const completionCounts = Object.fromEntries(completionBuckets.map((bucket) => [bucket, 0]));
Object.assign(completionCounts, countBy(tasks, "completion_bucket"));

const receipt = {
  schema: "ghc.eureka_task_tracker.v1",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  status: tasks.length > 0 ? "PASS_EUREKA_TASK_TRACKER_READY" : "PASS_EUREKA_TASK_TRACKER_EMPTY",
  task_count: tasks.length,
  scope_counts: scopeCounts,
  completion_counts: completionCounts,
  source_reports: sourceReports,
  tasks,
  next_actions: [
    "Use completed rows as build/use evidence only within their recorded source scope.",
    "Use safe_now uncompleted rows as next x2 implementation candidates.",
    "Keep candidate, defer, blocked, and needs_exact_packet rows queued until their scope is resolved.",
    "Refresh this tracker whenever a sibling proposes, completes, defers, or blocks a Eureka task.",
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
    eureka_completion: "status_only_from_sources",
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

const tableRows = tasks.map(
  (task) =>
    `| ${task.order} | ${task.id} | ${task.title} | ${task.scope_bucket} | ${task.completion_bucket} | ${task.status} | ${task.source_ref} |`,
);
const md = [
  `# ${phaseSlug} Eureka Task Tracker`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  `Status: \`${receipt.status}\``,
  `Task count: \`${receipt.task_count}\``,
  "",
  "## Scope Buckets",
  "",
  ...scopeBuckets.map((bucket) => `- ${bucket}: \`${scopeCounts[bucket] || 0}\``),
  "",
  "## Completion Buckets",
  "",
  ...completionBuckets.map((bucket) => `- ${bucket}: \`${completionCounts[bucket] || 0}\``),
  "",
  "## Tracker",
  "",
  "| # | ID | Title | Scope | Completion | Source Status | Source |",
  "|---:|---|---|---|---|---|---|",
  ...(tableRows.length ? tableRows : ["| 0 | none | No Eureka tasks found | candidate | uncompleted | none | none |"]),
  "",
  "## Next Actions",
  "",
  ...receipt.next_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "- Status-only tracker. No private route data, raw sibling content, credentials, screen-capture files, session traces, or local absolute paths are published.",
  "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: receipt.status, task_count: receipt.task_count, scope_counts: scopeCounts, completion_counts: completionCounts }, null, 2));
