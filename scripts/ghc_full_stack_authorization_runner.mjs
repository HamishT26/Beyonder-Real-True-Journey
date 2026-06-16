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
    console.error(`Missing ${key}`);
    process.exit(2);
  }
  return value;
}

const phaseSlug = requireArg("--phase-slug");
const stackJson = requireArg("--stack-json");
const queueJson = requireArg("--queue-json");
const activationJson = requireArg("--activation-json");
const activationMd = requireArg("--activation-md");
const orderJson = requireArg("--order-json");
const orderMd = requireArg("--order-md");
const closeoutJson = requireArg("--closeout-json");
const closeoutMd = requireArg("--closeout-md");

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function refName(path) {
  const normalized = path.replace(/\\/g, "/");
  const docsIndex = normalized.lastIndexOf("docs/");
  if (docsIndex >= 0) return normalized.slice(docsIndex);
  return basename(normalized);
}

function compact(row) {
  return `${row.kind || ""} ${row.id || ""} ${row.title || ""} ${row.status || ""} ${row.scope_bucket || ""} ${row.completion_bucket || ""} ${row.purpose || ""} ${row.action || ""}`.toLowerCase();
}

function hasHardBoundary(row) {
  return /\b(reset|rebase|force-push|delete|purge|destructive|purchase|deploy|public publish|account|gmail|calendar|plugin-cache|user-skill|credential|secret|raw transcript|raw lane|screenshot|session jsonl)\b/u.test(
    compact(row),
  );
}

function executionBucket(row) {
  if (row.completion_bucket === "completed") return "evidence_only_completed";
  if (row.scope_bucket === "blocked") return "held_blocked";
  if (row.scope_bucket === "needs_exact_packet") return "held_needs_exact_packet";
  if (hasHardBoundary(row)) return "held_hard_boundary";
  if (row.scope_bucket === "defer") return "deferred_authorized";
  return "authorized_execution_queue";
}

function orderPriority(row) {
  const text = compact(row);
  if (row.execution_bucket === "evidence_only_completed") return 10;
  if (/current-state|beacon|omega-mini|freshness|lookup/u.test(text)) return 20;
  if (/exposure|guard|security|open-gate|proof|boundary/u.test(text)) return 30;
  if (/queue|build|x2|execute|materialize/u.test(text)) return 40;
  if (/lane|lumen|arby|cicero|aster|kierkegaard|aristotle|handoff|catch.?up/u.test(text)) return 50;
  if (/source|web|github|research/u.test(text)) return 60;
  if (/skill|command|runner|system/u.test(text)) return 70;
  if (row.execution_bucket === "authorized_execution_queue") return 80;
  return 90;
}

function countBy(rows, field) {
  return rows.reduce((counts, row) => {
    counts[row[field]] = (counts[row[field]] || 0) + 1;
    return counts;
  }, {});
}

const stack = readJson(stackJson);
const queue = readJson(queueJson);
const generatedUtc = utcNow();
const rows = [
  ...(Array.isArray(stack.approval_packets) ? stack.approval_packets : []),
  ...(Array.isArray(stack.eureka_tasks) ? stack.eureka_tasks : []),
].map((row, index) => {
  const normalized = {
    original_order: row.order || index + 1,
    kind: row.kind,
    id: row.id,
    title: row.title || "Untitled row",
    source_phase: row.source_phase || stack.phase_slug || "unknown",
    source_ref: row.source_ref || refName(stackJson),
    status: row.status || "unknown",
    scope_bucket: row.scope_bucket || "candidate",
    completion_bucket: row.completion_bucket || "uncompleted",
    action: row.action || row.purpose || "",
  };
  normalized.execution_bucket = executionBucket(normalized);
  normalized.order_priority = orderPriority(normalized);
  return normalized;
});

const orderedRows = rows
  .slice()
  .sort((a, b) => a.order_priority - b.order_priority || a.original_order - b.original_order)
  .map((row, index) => ({ ...row, execution_order: index + 1 }));

const executableRows = orderedRows.filter((row) => row.execution_bucket === "authorized_execution_queue");
const heldRows = orderedRows.filter((row) => row.execution_bucket.startsWith("held_"));
const evidenceRows = orderedRows.filter((row) => row.execution_bucket === "evidence_only_completed");
const deferredRows = orderedRows.filter((row) => row.execution_bucket === "deferred_authorized");
const queuedPrior = Array.isArray(queue.queue_rows)
  ? queue.queue_rows.filter((row) => row.queue_status === "queued_for_x2_build_use")
  : [];

const publicationBoundary = {
  raw_lane_content_published: false,
  raw_chatgpt_transcript_published: false,
  raw_browser_routes_published: false,
  raw_route_handles_published: false,
  screen_capture_files_published: false,
  session_trace_files_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  authorization_is_completion: false,
  phase_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const activation = {
  schema: "ghc.full_stack_authorization.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_FULL_735_ROW_AUTHORIZATION_RECORDED",
  authorization_source_type: "active_thread_user_authorization",
  authorization_summary:
    "Hamish explicitly authorized all 735 rows and delegated execution ordering to Aletheon, while standing safety and publication boundaries remain active.",
  stack_source_ref: refName(stackJson),
  queue_source_ref: refName(queueJson),
  total_rows: orderedRows.length,
  approval_rows: orderedRows.filter((row) => row.kind === "approval_packet").length,
  eureka_rows: orderedRows.filter((row) => row.kind === "eureka_task").length,
  bucket_counts: countBy(orderedRows, "execution_bucket"),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const order = {
  schema: "ghc.full_stack_execution_order.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_FULL_STACK_EXECUTION_ORDER_READY",
  ordering_rule: [
    "Use completed rows as evidence first.",
    "Prioritize current-state, omega-mini freshness, exposure/security guards, x2 build queues, lane handoffs, source ledgers, then skill/command/runner work.",
    "Execute authorized rows only inside repo/local safe scope.",
    "Hold blocked, needs_exact_packet, and hard-boundary rows until a future exact packet or blocker fix exists.",
  ],
  ordered_rows: orderedRows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const closeout = {
  schema: "ghc.full_stack_authorization_closeout.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_FULL_STACK_AUTHORIZATION_QUEUE_MATERIALIZED_STATUS_ONLY",
  authorized_row_count: orderedRows.length,
  executable_row_count: executableRows.length,
  held_row_count: heldRows.length,
  evidence_only_row_count: evidenceRows.length,
  deferred_authorized_row_count: deferredRows.length,
  prior_queued_for_x2_count: queuedPrior.length,
  completed_this_pass: [
    "Recorded full 735-row authorization.",
    "Built deterministic execution ordering.",
    "Separated evidence-only, executable, deferred, held-blocked, held-needs-exact-packet, and held-hard-boundary rows.",
    "Preserved raw/private publication and overclaim boundaries.",
  ],
  next_execution_focus: executableRows.slice(0, 30).map((row) => ({
    execution_order: row.execution_order,
    id: row.id,
    title: row.title,
    kind: row.kind,
    source_phase: row.source_phase,
  })),
  held_summary: countBy(heldRows, "execution_bucket"),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

writeJson(activationJson, activation);
writeJson(orderJson, order);
writeJson(closeoutJson, closeout);

writeMd(activationMd, [
  `# ${phaseSlug} Full 735-Row Authorization`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${activation.status}\``,
  "",
  activation.authorization_summary,
  "",
  "## Counts",
  "",
  `- Total rows: \`${activation.total_rows}\``,
  `- Approval rows: \`${activation.approval_rows}\``,
  `- Eureka rows: \`${activation.eureka_rows}\``,
  "",
  "## Execution Buckets",
  "",
  ...Object.entries(activation.bucket_counts).map(([bucket, count]) => `- ${bucket}: \`${count}\``),
  "",
  "## Boundary",
  "",
  "- Authorization is permission, not completion proof.",
  "- Raw lane content, browser routes, credentials, screenshots, session traces, and local absolute paths remain unpublished.",
  "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
]);

writeMd(orderMd, [
  `# ${phaseSlug} Full Stack Execution Order`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${order.status}\``,
  "",
  "## Ordering Rule",
  "",
  ...order.ordering_rule.map((rule) => `- ${rule}`),
  "",
  "## First 50 Rows",
  "",
  "| Order | Bucket | Kind | ID | Title |",
  "|---:|---|---|---|---|",
  ...orderedRows.slice(0, 50).map((row) => `| ${row.execution_order} | ${row.execution_bucket} | ${row.kind} | ${row.id} | ${row.title} |`),
]);

writeMd(closeoutMd, [
  `# ${phaseSlug} Full Stack Authorization Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${closeout.status}\``,
  "",
  `Authorized rows: \`${closeout.authorized_row_count}\``,
  `Executable rows: \`${closeout.executable_row_count}\``,
  `Held rows: \`${closeout.held_row_count}\``,
  `Evidence-only rows: \`${closeout.evidence_only_row_count}\``,
  `Deferred authorized rows: \`${closeout.deferred_authorized_row_count}\``,
  "",
  "## Completed This Pass",
  "",
  ...closeout.completed_this_pass.map((item) => `- ${item}`),
  "",
  "## Next Execution Focus",
  "",
  ...closeout.next_execution_focus.map((row) => `- ${row.execution_order}. ${row.id}: ${row.title}`),
  "",
  "## Held Summary",
  "",
  ...Object.entries(closeout.held_summary).map(([bucket, count]) => `- ${bucket}: \`${count}\``),
]);

console.log(
  JSON.stringify(
    {
      status: activation.status,
      total_rows: activation.total_rows,
      executable_rows: closeout.executable_row_count,
      held_rows: closeout.held_row_count,
      evidence_only_rows: closeout.evidence_only_row_count,
      deferred_authorized_rows: closeout.deferred_authorized_row_count,
    },
    null,
    2,
  ),
);
