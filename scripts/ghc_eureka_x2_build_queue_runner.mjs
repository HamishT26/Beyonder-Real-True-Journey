#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 1) {
  const key = process.argv[index];
  if (!key.startsWith("--")) continue;
  const value = process.argv[index + 1];
  if (!value || value.startsWith("--")) {
    args.set(key, "true");
    continue;
  }
  args.set(key, value);
  index += 1;
}

function requireArg(key) {
  const value = args.get(key);
  if (!value) {
    console.error(`Missing required argument: ${key}`);
    process.exit(2);
  }
  return value;
}

const phaseSlug = requireArg("--phase-slug");
const targetPhaseSlug = requireArg("--target-phase-slug");
const trackerJson = requireArg("--tracker-json");
const checklistJson = requireArg("--checklist-json");
const receiptJson = requireArg("--receipt-json");
const receiptMd = requireArg("--receipt-md");

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

function bucketFor(task) {
  const text = `${task.title || ""} ${task.action || ""}`.toLowerCase();
  if (/current-state|current state|beacon|head|omega-mini|freshness|reconciliation/u.test(text)) {
    return "state_and_beacon_freshness";
  }
  if (/catch-up|catchup|handoff|sibling|prompt/u.test(text)) {
    return "sibling_catchup_and_handoff";
  }
  if (/browser|route|marker|lane|health/u.test(text)) {
    return "route_marker_and_lane_health";
  }
  if (/source|security|exposure|guard|gate|proof|d-drive|hygiene/u.test(text)) {
    return "source_security_and_gate_rails";
  }
  if (/intake|closeout|digest|reduce|summarize/u.test(text)) {
    return "intake_digest_and_closeout";
  }
  return "general_x2_build_use";
}

function queueReason(task) {
  if (task.scope_bucket !== "safe_now") return "not_safe_now";
  if (task.completion_bucket === "completed") return "already_completed";
  return "safe_now_uncompleted";
}

function countBy(rows, field) {
  return rows.reduce((counts, row) => {
    counts[row[field]] = (counts[row[field]] || 0) + 1;
    return counts;
  }, {});
}

const tracker = readJson(trackerJson);
const checklist = readJson(checklistJson);
const tasks = Array.isArray(tracker.tasks) ? tracker.tasks : [];
const approvalPackets = Array.isArray(checklist.packets) ? checklist.packets : [];

const queueRows = tasks.map((task, index) => {
  const reason = queueReason(task);
  return {
    tracker_order: task.order || index + 1,
    id: task.id || `task-${index + 1}`,
    title: task.title || "Untitled Eureka task",
    scope_bucket: task.scope_bucket || "candidate",
    completion_bucket: task.completion_bucket || "uncompleted",
    queue_status:
      reason === "safe_now_uncompleted" ? "queued_for_x2_build_use" : reason === "already_completed" ? "evidence_only_completed" : "held_from_x2_queue",
    x2_execution_bucket: bucketFor(task),
    source_ref: task.source_ref || "",
    action: task.action || "",
  };
});

const queued = queueRows.filter((row) => row.queue_status === "queued_for_x2_build_use");
const completed = queueRows.filter((row) => row.queue_status === "evidence_only_completed");
const held = queueRows.filter((row) => row.queue_status === "held_from_x2_queue");
const queuedWithOrder = queued.map((row, index) => ({ ...row, x2_execution_order: index + 1 }));
const allRows = queueRows.map((row) => {
  const queuedRow = queuedWithOrder.find((candidate) => candidate.id === row.id);
  return queuedRow || { ...row, x2_execution_order: null };
});

const receipt = {
  schema: "ghc.eureka_x2_build_queue.v1",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  target_phase_slug: targetPhaseSlug,
  status: "PASS_EUREKA_X2_BUILD_QUEUE_READY",
  tracker_source_ref: publicSourceRef(trackerJson),
  checklist_source_ref: publicSourceRef(checklistJson),
  tracker_task_count: tasks.length,
  approval_packet_count: approvalPackets.length,
  queued_for_x2_count: queued.length,
  completed_evidence_count: completed.length,
  held_from_x2_count: held.length,
  queue_bucket_counts: countBy(queued, "x2_execution_bucket"),
  queue_rows: allRows,
  execution_rule: [
    "Execute queued_for_x2_build_use rows during the target x2 phase under exact repo validation guards.",
    "Treat evidence_only_completed rows as already-built source evidence, not new work.",
    "Do not execute held_from_x2_queue rows until their scope is safe_now and no exact-packet blocker remains.",
    "Refresh the Eureka tracker after x2 work materializes new completed evidence.",
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

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const mdRows = allRows.map(
  (row) =>
    `| ${row.x2_execution_order ?? ""} | ${row.id} | ${row.title} | ${row.queue_status} | ${row.x2_execution_bucket} | ${row.source_ref} |`,
);

const md = [
  `# ${targetPhaseSlug} Eureka X2 Build Queue`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  `Status: \`${receipt.status}\``,
  `Source phase: \`${phaseSlug}\``,
  `Target phase: \`${targetPhaseSlug}\``,
  "",
  `Queued for x2 build/use: \`${receipt.queued_for_x2_count}\``,
  `Completed evidence rows: \`${receipt.completed_evidence_count}\``,
  `Held from x2 queue: \`${receipt.held_from_x2_count}\``,
  "",
  "## Queue Buckets",
  "",
  ...Object.entries(receipt.queue_bucket_counts).map(([bucket, count]) => `- ${bucket}: \`${count}\``),
  "",
  "## Queue",
  "",
  "| X2 order | ID | Title | Queue status | Execution bucket | Source |",
  "|---:|---|---|---|---|---|",
  ...mdRows,
  "",
  "## Execution Rule",
  "",
  ...receipt.execution_rule.map((rule) => `- ${rule}`),
  "",
  "## Boundary",
  "",
  "- This artifact queues x2 work; it does not claim the queued tasks are complete.",
  "- No private route data, raw sibling content, credentials, screen-capture files, session traces, or local absolute paths are published.",
  "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status: receipt.status,
      queued_for_x2_count: receipt.queued_for_x2_count,
      completed_evidence_count: receipt.completed_evidence_count,
      held_from_x2_count: receipt.held_from_x2_count,
    },
    null,
    2,
  ),
);
