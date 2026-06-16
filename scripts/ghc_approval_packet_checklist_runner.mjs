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
    "Usage: node ghc_approval_packet_checklist_runner.mjs --phase-slug <slug> --source-json <json> [--source-json <json> ...] --receipt-json <json> --receipt-md <md>",
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

function normalizeScopeBucket(packet) {
  const statusText = compactText(packet.status);
  if (statusText.includes("needs_exact_packet") || statusText.includes("exact packet required") || statusText.includes("separate exact packet")) {
    return "needs_exact_packet";
  }
  if (statusText.includes("blocked") || statusText.includes("blocker") || statusText.includes("failed") || statusText.includes("open_gap") || statusText.includes("open gap") || statusText.includes("denied") || statusText.includes("unsafe")) {
    return "blocked";
  }
  if (statusText.includes("defer") || statusText.includes("standby") || statusText.includes("later") || statusText.includes("hold")) {
    return "defer";
  }
  if (statusText.includes("pending") || statusText.includes("candidate") || statusText.includes("approval needed") || statusText.includes("approval_needed") || statusText.includes("review required") || statusText.includes("proposed")) {
    return "candidate";
  }
  if (statusText.includes("safe_now") || statusText.includes("safe now") || statusText.includes("approved") || statusText.includes("authorized") || statusText.includes("ready") || statusText.startsWith("pass") || statusText.includes("materialized") || statusText.includes("completed") || statusText.includes("implemented") || statusText.includes("closed")) {
    return "safe_now";
  }
  const text = compactText(packet.status, packet.scope, packet.title, packet.reason, packet.result, packet.purpose);
  if (/\b(needs[_ -]?exact[_ -]?packet|exact packet required|separate exact packet|outside approved scope)\b/u.test(text)) {
    return "needs_exact_packet";
  }
  if (/\b(blocked|blocker|failed|open gap|open_gap|denied|unsafe|not approved)\b/u.test(text)) {
    return "blocked";
  }
  if (/\b(defer|deferred|standby|later|hold)\b/u.test(text)) {
    return "defer";
  }
  if (/\b(pending|candidate|approval needed|approval-needed|approval_needed|review required|proposed)\b/u.test(text)) {
    return "candidate";
  }
  if (/\b(safe_now|safe now|approved|authorized|ready|pass|materialized|completed|implemented|closed)\b/u.test(text)) {
    return "safe_now";
  }
  return "candidate";
}

function normalizeCompletionBucket(packet) {
  const text = compactText(packet.completion, packet.completed, packet.status, packet.result, packet.evidence, packet.title);
  if (/\b(false|uncompleted|incomplete|pending|candidate|defer|deferred|blocked|failed|open gap|open_gap)\b/u.test(text)) {
    return "uncompleted";
  }
  if (/\b(true|completed|complete|closed|built|implemented|approved|authorized)\b/u.test(text) || text.startsWith("pass") || text.includes("materialized") || text.includes("approved_user_authorized")) {
    return "completed";
  }
  return "uncompleted";
}

function titleOf(value, fallback) {
  return value?.title || value?.name || value?.id || value?.task_id || fallback;
}

function idOf(value, fallback) {
  return value?.id || value?.packet_id || value?.task_id || value?.artifact || fallback;
}

function collectArrayPackets(payload, sourceRef) {
  const fields = [
    "approval_candidates",
    "approval_packets",
    "approval_packet_candidates",
    "approval_packet_scope",
    "packets",
  ];
  const rows = [];
  for (const field of fields) {
    const value = payload[field];
    if (!Array.isArray(value)) continue;
    value.forEach((packet, index) => {
      if (!packet || typeof packet !== "object") return;
      rows.push({
        id: idOf(packet, `${field}-${index + 1}`),
        title: titleOf(packet, "Untitled approval packet"),
        status: packet.status || packet.state || "candidate",
        purpose: packet.purpose || packet.scope || packet.result || packet.build_use || "",
        source_ref: sourceRef,
        source_field: field,
        source_order: index + 1,
      });
    });
  }
  return rows;
}

function collectTopLevelPacket(payload, sourceRef) {
  const text = compactText(payload.artifact_type, payload.artifact, payload.title, payload.task_id, sourceRef);
  if (!/\bapproval\b/u.test(text)) return [];
  return [
    {
      id: idOf(payload, basename(sourceRef, ".json")),
      title: titleOf(payload, "Approval packet artifact"),
      status: payload.status || "candidate",
      purpose: payload.purpose || payload.scope || payload.result || payload.build_use || "",
      source_ref: sourceRef,
      source_field: "top_level_approval_artifact",
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
const packets = [];

for (const sourceJson of sourceJsons) {
  const sourceRef = publicSourceRef(sourceJson);
  if (!existsSync(sourceJson)) {
    sourceReports.push({ source_ref: sourceRef, status: "MISSING_SKIPPED", packet_count: 0 });
    continue;
  }
  const payload = readJson(sourceJson);
  const extracted = [...collectArrayPackets(payload, sourceRef), ...collectTopLevelPacket(payload, sourceRef)];
  extracted.forEach((packet) => {
    const scope_bucket = normalizeScopeBucket(packet);
    const completion_bucket = normalizeCompletionBucket(packet);
    packets.push({
      order: packets.length + 1,
      id: packet.id,
      title: packet.title,
      status: packet.status,
      scope_bucket,
      completion_bucket,
      source_ref: packet.source_ref,
      source_field: packet.source_field,
      source_order: packet.source_order,
      purpose: packet.purpose,
    });
  });
  sourceReports.push({ source_ref: sourceRef, status: "READ", packet_count: extracted.length });
}

const scopeBuckets = ["safe_now", "candidate", "defer", "blocked", "needs_exact_packet"];
const completionBuckets = ["completed", "uncompleted"];
const scopeCounts = Object.fromEntries(scopeBuckets.map((bucket) => [bucket, 0]));
Object.assign(scopeCounts, countBy(packets, "scope_bucket"));
const completionCounts = Object.fromEntries(completionBuckets.map((bucket) => [bucket, 0]));
Object.assign(completionCounts, countBy(packets, "completion_bucket"));

const receipt = {
  schema: "ghc.approval_packet_checklist.v1",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  status: packets.length > 0 ? "PASS_APPROVAL_PACKET_CHECKLIST_READY" : "PASS_APPROVAL_PACKET_CHECKLIST_EMPTY",
  packet_count: packets.length,
  scope_counts: scopeCounts,
  completion_counts: completionCounts,
  source_reports: sourceReports,
  packets,
  next_actions: [
    "Use safe_now completed rows as execution evidence only when their source receipt supports it.",
    "Use safe_now uncompleted rows as near-term work candidates under existing guard rails.",
    "Keep candidate, defer, blocked, and needs_exact_packet rows out of execution until their scope is resolved.",
    "Refresh this checklist whenever new approval packets are proposed, authorized, blocked, or completed.",
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

const tableRows = packets.map(
  (packet) =>
    `| ${packet.order} | ${packet.id} | ${packet.title} | ${packet.scope_bucket} | ${packet.completion_bucket} | ${packet.status} | ${packet.source_ref} |`,
);
const md = [
  `# ${phaseSlug} Approval Packet Checklist`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  `Status: \`${receipt.status}\``,
  `Packet count: \`${receipt.packet_count}\``,
  "",
  "## Scope Buckets",
  "",
  ...scopeBuckets.map((bucket) => `- ${bucket}: \`${scopeCounts[bucket] || 0}\``),
  "",
  "## Completion Buckets",
  "",
  ...completionBuckets.map((bucket) => `- ${bucket}: \`${completionCounts[bucket] || 0}\``),
  "",
  "## Checklist",
  "",
  "| # | ID | Title | Scope | Completion | Source Status | Source |",
  "|---:|---|---|---|---|---|---|",
  ...(tableRows.length ? tableRows : ["| 0 | none | No approval packets found | candidate | uncompleted | none | none |"]),
  "",
  "## Next Actions",
  "",
  ...receipt.next_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "- Status-only checklist. No private route data, raw sibling content, credentials, screen-capture files, session traces, or local absolute paths are published.",
  "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(JSON.stringify({ status: receipt.status, packet_count: receipt.packet_count, scope_counts: scopeCounts, completion_counts: completionCounts }, null, 2));
