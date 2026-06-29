#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = required("--phase-slug");
const nextX2 = required("--next-x2");
const nextX1AfterX2 = required("--next-x1-after-x2");
const privateResponse = required("--private-response");
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

if (!existsSync(privateResponse)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_PRIVATE_LUMEN_RESPONSE_MISSING",
    phase_slug: phaseSlug,
    raw_response_published: false,
  }, null, 2));
  process.exit(2);
}

const raw = readFileSync(privateResponse, "utf8").replace(/^\uFEFF/, "");
const now = new Date();
const generatedUtc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
const generatedNz = nzTimestamp(now);
const digest = createHash("sha256").update(raw).digest("hex");
const lines = raw.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);

const expectedProfile = {
  safe_approval_packets: 50,
  candidate_packets: 30,
  exact_approval_packets_queued: 20,
  blocked_packets_queued: 10,
  skill_ideas: 20,
  runner_ideas: 10,
  cleanup_refine_fix_tasks: 30,
};

const detectedSignalCounts = {
  immediate_x1_safe: count(/immediate_x1_safe/gi),
  x2_build_task: count(/x2_build_task/gi),
  safe_mentions: count(/\bsafe\b|safe_now|safe approval/gi),
  candidate_mentions: count(/candidate/gi),
  exact_mentions: count(/exact[- ]approval|exact approval|exact_approval_needed|exact/gi),
  blocked_mentions: count(/blocked|open gate/gi),
  skill_mentions: count(/\bskill\b|\bskills\b/gi),
  runner_mentions: count(/\brunner\b|\brunners\b/gi),
  cleanup_mentions: count(/cleanup|clean up|refine|fix/gi),
};

const headings = lines
  .filter((line) => line.length <= 140)
  .filter((line) => /^[A-Z0-9][A-Z0-9 _/()&:+-]{4,}$/.test(line) || /^(safe|candidate|exact|blocked|skill|runner|cleanup|handoff|readiness)/i.test(line))
  .map(sanitizeLine)
  .slice(0, 60);

const proposalLines = lines
  .filter((line) => /immediate_x1_safe|x2_build_task|safe approval|candidate|exact|blocked|skill|runner|cleanup|refine|fix/i.test(line))
  .map((line) => sanitizeLine(line))
  .filter((line) => line.length > 0);

const rows = proposalLines.map((line, index) => {
  const approvalBucket = approvalBucketFor(line);
  return {
    id: `${phaseSlug}-lumen-row-${String(index + 1).padStart(3, "0")}`,
    source: "lumen_private_response_reduction",
    kind: kindFor(line),
    approval_bucket: approvalBucket,
    execution_lane: executionLaneFor(line, approvalBucket),
    summary: line,
    raw_text_published: false,
  };
});

const queueCounts = rows.reduce((acc, row) => {
  acc.total += 1;
  acc.by_approval_bucket[row.approval_bucket] = (acc.by_approval_bucket[row.approval_bucket] || 0) + 1;
  acc.by_execution_lane[row.execution_lane] = (acc.by_execution_lane[row.execution_lane] || 0) + 1;
  acc.by_kind[row.kind] = (acc.by_kind[row.kind] || 0) + 1;
  return acc;
}, { total: 0, by_approval_bucket: {}, by_execution_lane: {}, by_kind: {} });

const reduction = artifact("lumen-harvest-reduction", "ghc.lumen_harvest_reduction.v2", "PASS_LUMEN_RESPONSE_HARVESTED_AND_REDUCED_SANITIZED", {
  private_response_basename: basename(privateResponse),
  private_response_sha256: digest,
  raw_response_published: false,
  response_character_count: raw.length,
  response_line_count: lines.length,
  expected_profile: expectedProfile,
  detected_signal_counts: detectedSignalCounts,
  sanitized_heading_signals: headings,
  queue_counts: queueCounts,
  harvest_status: "completed_ready_for_harvest",
});

const queue = artifact("lumen-sanitized-proposal-queue", "ghc.lumen_sanitized_proposal_queue.v2", "PASS_LUMEN_QUEUE_REDUCED_FOR_NEXT_X2", {
  source_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  expected_profile: expectedProfile,
  queue_counts: queueCounts,
  rows,
});

const prep = artifact("closeout-prep", "ghc.lumen_x1_closeout_prep.v2", "PASS_LUMEN_X1_CLOSEOUT_PREP_READY", {
  source_phase: phaseSlug,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  closeout_allowed_after_harvest: true,
  required_next_steps: [
    `close ${phaseSlug} with Lumen harvested`,
    `advance active phase to ${nextX2}`,
    "carry Lumen refresh/status-first Browser route into startup, compact, and closeout receipts",
    "run immediate x1-safe validation/status/queue hygiene now where safe",
    "carry x2 build/use/test/install/prototype rows into the x2 build bundle",
    "keep exact and blocked gates queued unless Hamish freshly authorizes those gates",
  ],
});

for (const doc of [reduction, queue, prep]) writePair(doc);

console.log(JSON.stringify({
  status: "PASS_LUMEN_X1_PRIVATE_RESPONSE_REDUCED_SANITIZED",
  phase_slug: phaseSlug,
  response_character_count: raw.length,
  response_line_count: lines.length,
  queue_rows: rows.length,
  immediate_x1_safe_rows: queueCounts.by_execution_lane.immediate_x1_safe || 0,
  x2_build_task_rows: queueCounts.by_execution_lane.x2_build_task || 0,
  artifacts_written: 6,
}, null, 2));

function parseArgs(argv) {
  const out = new Map();
  for (let i = 0; i < argv.length; i += 1) {
    const key = argv[i];
    if (!key.startsWith("--")) continue;
    const value = argv[i + 1];
    if (!value || value.startsWith("--")) out.set(key, "true");
    else {
      out.set(key, value);
      i += 1;
    }
  }
  return out;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_lumen_x1_private_response_reducer.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function count(pattern) {
  return (raw.match(pattern) || []).length;
}

function approvalBucketFor(line) {
  if (/blocked/i.test(line)) return "blocked";
  if (/exact_approval_needed|exact[- ]approval|exact approval|\bexact\b/i.test(line)) return "exact_approval_needed";
  if (/candidate/i.test(line)) return "candidate";
  return "safe_now";
}

function executionLaneFor(line, approvalBucket) {
  if (approvalBucket === "blocked" || approvalBucket === "exact_approval_needed") return "x2_build_task";
  if (/x2_build_task/i.test(line)) return "x2_build_task";
  return "immediate_x1_safe";
}

function kindFor(line) {
  if (/blocked/i.test(line)) return "blocked_packet";
  if (/exact/i.test(line)) return "exact_approval_packet";
  if (/candidate/i.test(line)) return "candidate_packet";
  if (/skill/i.test(line)) return "skill_idea";
  if (/runner/i.test(line)) return "runner_idea";
  if (/cleanup|clean up|refine|fix/i.test(line)) return "cleanup_task";
  return "safe_approval_packet";
}

function sanitizeLine(line) {
  return line
    .replace(/https?:\/\/\S+/g, "[url-redacted]")
    .replace(/[A-Za-z]:\\[^\s]+/g, "[local-path-redacted]")
    .replace(/\b[0-9a-f]{24,}\b/gi, "[id-or-hash-redacted]")
    .replace(/\s+/g, " ")
    .slice(0, 280);
}

function artifact(suffix, schema, status, extra = {}) {
  return {
    artifact: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1`,
    schema,
    phase_slug: phaseSlug,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    status,
    publication_boundary: {
      raw_private_material_published: false,
      raw_browser_routes_published: false,
      private_ids_published: false,
      raw_transcripts_published: false,
      screenshots_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
      raw_app_state_published: false,
      hidden_reasoning_published: false,
    },
    claim_boundary: {
      full_goal_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      legal_closure: "not_claimed",
      canon_promotion: "not_claimed",
      deployment_closure: "not_claimed",
      account_mutation: "not_claimed",
      api_key_creation: "not_claimed",
      private_material_proof: "not_claimed",
      raw_publication_proof: "not_claimed",
      sibling_identity_replacement_or_merge: "not_claimed",
    },
    ...extra,
  };
}

function writePair(doc) {
  const base = join(process.cwd(), doc.artifact);
  writeFileSync(`${base}.json`, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  const linesOut = [
    `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}`,
    "",
    `Status: ${doc.status}`,
    "",
    `Generated NZ: ${doc.generated_nz}`,
    "",
    "Boundary: sanitized reduction only. Raw Lumen text, browser routes, private URLs, private IDs, screenshots, credentials, local private paths, session streams, app state, and hidden reasoning are not published.",
    "",
  ];
  if (doc.queue_counts) {
    linesOut.push("## Queue Counts", "");
    linesOut.push(`- total: ${doc.queue_counts.total}`);
    for (const [key, value] of Object.entries(doc.queue_counts.by_execution_lane || {})) linesOut.push(`- ${key}: ${value}`);
    for (const [key, value] of Object.entries(doc.queue_counts.by_approval_bucket || {})) linesOut.push(`- ${key}: ${value}`);
    linesOut.push("");
  }
  if (doc.expected_profile) {
    linesOut.push("## Expected Profile", "");
    for (const [key, value] of Object.entries(doc.expected_profile)) linesOut.push(`- ${key}: ${value}`);
    linesOut.push("");
  }
  if (doc.next_x2_scope) linesOut.push(`Next x2 scope: ${doc.next_x2_scope}`, "");
  if (doc.next_x1_lane_after_x2) linesOut.push(`Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "");
  writeFileSync(`${base}.md`, `${linesOut.join("\n")}\n`, "utf8");
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
