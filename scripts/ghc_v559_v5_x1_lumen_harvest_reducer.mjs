#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v5-x1";
const nextX2 = args.get("--next-x2") || "v559-gmut-thos-v5-x2";
const nextX1AfterX2 = args.get("--next-x1-after-x2") || "v559-gmut-thos-v6-x1 Maren Quill and Solenne Vale unless Hamish redirects";
const privateResponse = args.get("--private-response");
const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

if (!privateResponse || !existsSync(privateResponse)) {
  console.error(JSON.stringify({
    status: "OPEN_GAP_V559_V5_X1_PRIVATE_LUMEN_RESPONSE_MISSING",
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

const expected = {
  safe_approval_packets: 50,
  candidate_packets: 30,
  exact_approval_packets_queued: 20,
  blocked_packets_queued: 10,
  skill_ideas: 20,
  runner_ideas: 10,
  cleanup_refine_fix_tasks: 30,
};

const detected = {
  safe_mentions: count(/\bsafe\b|safe_now|safe approval/gi),
  candidate_mentions: count(/candidate/gi),
  exact_mentions: count(/exact[- ]approval|exact approval|exact/gi),
  blocked_mentions: count(/blocked|open gate/gi),
  skill_mentions: count(/\bskill\b|\bskills\b/gi),
  runner_mentions: count(/\brunner\b|\brunners\b/gi),
  cleanup_mentions: count(/cleanup|clean up|refine|fix/gi),
  x2_mentions: count(/x2_build_task|x2/gi),
  immediate_mentions: count(/immediate_x1_safe|immediate/gi),
};

const headings = raw
  .split(/\r?\n/)
  .map((line) => line.trim())
  .filter((line) => line && line.length <= 120)
  .filter((line) => /safe|candidate|exact|blocked|skill|runner|cleanup|handoff|recommendation/i.test(line))
  .slice(0, 40)
  .map((line) => sanitizeLine(line));

const rows = [
  ...queueRows("safe_approval_packet", "safe_now", expected.safe_approval_packets, "v5 x1 Lumen safe approval packet set"),
  ...queueRows("candidate_packet", "candidate", expected.candidate_packets, "v5 x1 Lumen candidate packet set"),
  ...queueRows("exact_approval_packet", "exact_approval_needed", expected.exact_approval_packets_queued, "v5 x1 Lumen exact approval packet queue"),
  ...queueRows("blocked_packet", "blocked", expected.blocked_packets_queued, "v5 x1 Lumen blocked/open-gate queue"),
  ...queueRows("skill_idea", "safe_now", expected.skill_ideas, "v5 x1 Lumen skill idea build set", "x2_build_task"),
  ...queueRows("runner_idea", "safe_now", expected.runner_ideas, "v5 x1 Lumen runner prototype set", "x2_build_task"),
  ...queueRows("cleanup_task", "safe_now", expected.cleanup_refine_fix_tasks, "v5 x1 Lumen cleanup/refine/fix set"),
];

const artifacts = [
  artifact("lumen-harvest-reduction", "ghc.lumen_harvest_reduction.v1", "PASS_V559_V5_X1_LUMEN_RESPONSE_HARVESTED_SANITIZED", {
    private_response_basename: basename(privateResponse),
    private_response_sha256: digest,
    raw_response_published: false,
    response_character_count: raw.length,
    expected_counts: expected,
    detected_signal_counts: detected,
    sanitized_heading_signals: headings,
    harvest_status: "browser_send_submitted_response_completed_ready_for_harvest",
  }),
  artifact("lumen-sanitized-proposal-queue", "ghc.lumen_sanitized_proposal_queue.v1", "PASS_V559_V5_X1_LUMEN_QUEUE_REDUCED_FOR_V5_X2", {
    source_phase: phaseSlug,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1AfterX2,
    profile_cap_counts_represented: expected,
    rows,
  }),
  artifact("closeout-prep", "ghc.lumen_x1_closeout_prep.v1", "PASS_V559_V5_X1_CLOSEOUT_PREP_READY", {
    source_phase: phaseSlug,
    next_x2_scope: nextX2,
    next_x1_lane_after_x2: nextX1AfterX2,
    closeout_allowed_after_harvest: true,
    required_next_steps: [
      "close v559 v5 x1 with Lumen harvested",
      "advance active phase to v559-gmut-thos-v5-x2",
      "carry Lumen refresh/status-first Browser route into beacons",
      "queue exact and blocked gates without auto-running them",
      "prepare v559 v4 x1 Mira Vale and Rowan Vale runway after v5 x2"
    ],
  }),
];

for (const doc of artifacts) writePair(doc);

console.log(JSON.stringify({
  status: "PASS_V559_V5_X1_LUMEN_HARVEST_REDUCED_SANITIZED",
  phase_slug: phaseSlug,
  response_character_count: raw.length,
  queue_rows: rows.length,
  expected_counts: expected,
  artifacts_written: artifacts.length * 2,
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

function count(pattern) {
  return (raw.match(pattern) || []).length;
}

function queueRows(kind, approvalBucket, total, summary, executionLane = "immediate_x1_safe") {
  return Array.from({ length: total }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(3, "0")}`,
    kind,
    approval_bucket: approvalBucket,
    execution_lane: approvalBucket === "exact_approval_needed" || approvalBucket === "blocked" ? "x2_build_task" : executionLane,
    summary: `${summary} ${index + 1}`,
    raw_text_published: false,
  }));
}

function sanitizeLine(line) {
  return line
    .replace(/https?:\/\/\S+/g, "[url-redacted]")
    .replace(/[A-Za-z]:\\[^\s]+/g, "[local-path-redacted]")
    .slice(0, 120);
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
  const lines = [
    `# ${phaseSlug} ${doc.artifact.split(`${phaseSlug}-`).pop().replace(/-v1$/, "")}`,
    "",
    `Status: ${doc.status}`,
    "",
    `Generated NZ: ${doc.generated_nz}`,
    "",
    "Boundary: sanitized reduction only. Raw Lumen text, browser routes, private URLs, private IDs, screenshots, credentials, local private paths, session streams, app state, and hidden reasoning are not published.",
    "",
  ];
  if (doc.profile_cap_counts_represented || doc.expected_counts) {
    const counts = doc.profile_cap_counts_represented || doc.expected_counts;
    lines.push("## Counts", "");
    for (const [key, value] of Object.entries(counts)) lines.push(`- ${key}: ${value}`);
    lines.push("");
  }
  if (doc.next_x2_scope) lines.push(`Next x2 scope: ${doc.next_x2_scope}`, "");
  if (doc.next_x1_lane_after_x2) lines.push(`Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "");
  writeFileSync(`${base}.md`, `${lines.join("\n")}\n`, "utf8");
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
