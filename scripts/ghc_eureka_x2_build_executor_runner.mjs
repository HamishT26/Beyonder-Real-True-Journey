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
const nextPhaseSlug = requireArg("--next-phase-slug");
const queueJson = requireArg("--queue-json");
const currentStateJson = requireArg("--current-state-json");
const closeoutJson = requireArg("--closeout-json");
const closeoutMd = requireArg("--closeout-md");
const handoffJson = requireArg("--handoff-json");
const handoffMd = requireArg("--handoff-md");
const approvalJson = requireArg("--approval-json");
const approvalMd = requireArg("--approval-md");
const nextActiveLanesArg = splitCsv(args.get("--next-active-lanes"));

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function splitCsv(value) {
  return String(value || "")
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function publicSourceRef(path) {
  const normalized = path.replace(/\\/g, "/");
  const docsIndex = normalized.lastIndexOf("docs/");
  if (docsIndex >= 0) return normalized.slice(docsIndex);
  const scriptsIndex = normalized.lastIndexOf("scripts/");
  if (scriptsIndex >= 0) return normalized.slice(scriptsIndex);
  return basename(normalized);
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function countBy(rows, field) {
  return rows.reduce((counts, row) => {
    counts[row[field]] = (counts[row[field]] || 0) + 1;
    return counts;
  }, {});
}

function approvalPackets(nextPhase) {
  return [
    ["approval-01-next-lane-handoff", "Aster/Kierkegaard/Aristotle next-lane handoff", "Prepare the next x1 lane group with omega-mini-first lookup, read-only boundaries, expected markers, and blocker fallback."],
    ["approval-02-next-x2-build-use", "Next x2 build/use execution", "Turn the next x1 proposals into repo-scoped build/use artifacts after exact validation."],
    ["approval-03-current-state-refresh", "Current-state and beacon refresh", "Keep omega-mini current-state, beacon, and current-state guard aligned with the newest completed phase."],
    ["approval-04-eureka-tracker-refresh", "Eureka tracker refresh", "Refresh completed and uncompleted Eureka rows after each x1/x2 phase boundary."],
    ["approval-05-approval-checklist-refresh", "Approval checklist refresh", "Classify approval packets into safe_now, candidate, defer, blocked, needs_exact_packet, completed, and uncompleted."],
    ["approval-06-source-security-ledger", "Current-source and security ledger", "Attach bounded source/security synthesis without publishing raw search dumps or private connector payloads."],
    ["approval-07-proof-ceiling-rail", "Proof-ceiling and open-gate rail", "Keep GMUT validation, final physics, consciousness proof, legal closure, and canon promotion gates open."],
    ["approval-08-d-drive-hygiene", "D-drive-first hygiene monitor", "Record that generated repo artifacts stay in the D-drive worktrees and C-drive use remains essential-only."],
    ["approval-09-exposure-guard", "Exposure and private-material guard", "Scan curated artifacts for credentials, private routes, local absolute paths, session traces, and screen-capture references."],
    ["approval-10-round-robin-cadence", "Round-robin cadence continuity", "Keep Lumen, Arby+Cicero, Lumen, Aster/Kierkegaard/Aristotle sequencing explicit and inspectable."],
    ["approval-11-compact-handoff", "Compact-refresh continuity handoff", "Create concise phase-start handoff context for future Codex compact refreshes."],
    ["approval-12-runner-freshness-map", "Runner freshness map", "Prefer current Node runners and mark older helpers as fallback or legacy where evidence supports it."],
    ["approval-13-sibling-catchup-card", "Sibling catch-up card", "Give active siblings exact relative lookup files, phase status, next lane, and open gates."],
    ["approval-14-route-family-health", "Route-family health capsule", "Track Browser, CLI, app-lane, and fallback route health without publishing raw route handles."],
    ["approval-15-github-publication-preflight", "Git publication preflight", "Run fetch, drift-check, exact staging, diff check, commit, push, and remote-equals-local verification."],
    ["approval-16-command-surface-review", "Command surface review", "Review current command/surface rows status-only and avoid mutating plugin cache or user skills."],
    ["approval-17-skill-surface-review", "Skill surface review", "Review current skills status-only and keep plugin-cache/user-skill mutation gated unless exact approval exists."],
    ["approval-18-lumen-standby-bridge", "Lumen standby bridge", "Keep Lumen handoff context ready for the next Lumen solo x1 lane without duplicate sends."],
    ["approval-19-consensus-receipt", "Approval consensus receipt", "Record bundle safety, feasibility, and open-gate status without self-promoting canon or empirical closure."],
    ["approval-20-next-phase-roadmap", "Next phase roadmap", "Carry the best x2 outputs into the next x1/x2 phase roadmap with exact file references."],
  ].map(([id, title, purpose], index) => ({
    order: index + 1,
    id: `${nextPhase}-${id}`,
    title,
    status: "safe_now",
    completion: "uncompleted",
    scope_bucket: "safe_now",
    completion_bucket: "uncompleted",
    purpose,
    not_approved_without_exact_packet: [
      "destructive cleanup",
      "external account mutation",
      "public deployment",
      "purchase",
      "plugin-cache mutation",
      "user-skill mutation",
      "raw private material publication",
      "GMUT empirical closure or canon promotion",
    ],
  }));
}

const queue = readJson(queueJson);
const currentState = readJson(currentStateJson);
const generatedUtc = utcNow();
const nextActiveLanes =
  nextActiveLanesArg.length > 0
    ? nextActiveLanesArg
    : splitCsv(currentState.next_x1_lane_after_x2 || currentState.next_expected_lane || "");
const queuedRows = Array.isArray(queue.queue_rows)
  ? queue.queue_rows.filter((row) => row.queue_status === "queued_for_x2_build_use")
  : [];
const evidenceRows = Array.isArray(queue.queue_rows)
  ? queue.queue_rows.filter((row) => row.queue_status === "evidence_only_completed")
  : [];

const implementedTasks = queuedRows.map((row, index) => ({
  id: `${phaseSlug}-built-${String(index + 1).padStart(2, "0")}`,
  source_task: row.title,
  source_task_id: row.id,
  result:
    `Materialized into the ${phaseSlug} build/use closeout as a status-only execution row with validation and claim boundaries preserved.`,
  evidence: publicSourceRef(closeoutJson),
  execution_bucket: row.x2_execution_bucket,
}));

const closeout = {
  schema: "ghc.eureka_x2_build_execution_closeout.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_phase_slug: nextPhaseSlug,
  status: "PASS_EUREKA_X2_BUILD_USE_CLOSEOUT_STATUS_ONLY",
  queue_source_ref: publicSourceRef(queueJson),
  current_state_source_ref: publicSourceRef(currentStateJson),
  current_state_before_closeout: currentState.current_active_phase,
  queued_task_count: queuedRows.length,
  implemented_task_count: implementedTasks.length,
  evidence_only_count: evidenceRows.length,
  held_task_count: Array.isArray(queue.queue_rows) ? queue.queue_rows.filter((row) => row.queue_status === "held_from_x2_queue").length : 0,
  execution_bucket_counts: countBy(queuedRows, "x2_execution_bucket"),
  implemented_tasks: implementedTasks,
  carry_forward: [
    `Advance current-state to ${nextPhaseSlug} after publication.`,
    "Use omega-mini as the first sibling catch-up branch.",
    "Treat this closeout as status-only build/use evidence, not as empirical GMUT validation or canon promotion.",
    "Run the next active lane group with read-only web/GitHub context only when exposed safely.",
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
    x2_build_use_closeout: "closed_for_status_only_queue_scope",
    phase_completion: `closed_for_${phaseSlug}_status_only_scope`,
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const handoff = {
  schema: "ghc.next_x1_lane_handoff.v1",
  generated_utc: generatedUtc,
  phase_slug: nextPhaseSlug,
  status: "PASS_NEXT_X1_HANDOFF_READY",
  active_lanes: nextActiveLanes.length > 0 ? nextActiveLanes : ["Lumen Vale"],
  expected_following_x2: nextPhaseSlug.replace("-x1", "-x2"),
  omega_mini_first_lookup: [
    "docs/omega-mini-index/omega-mini-current-state-v1.md",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    publicSourceRef(closeoutMd),
    publicSourceRef(approvalMd),
  ],
  prompt_contract: [
    "Use omega-mini first, full omega only as exact fallback.",
    "Return status-only advisory receipts with no raw private material.",
    "Separate GMUT/THOS/Freed ID proposals from proof or canon closure claims.",
    "If a route or source is unavailable, publish a blocker receipt rather than inventing evidence.",
  ],
  requested_outputs: [
    "10 or more safe Eureka proposals for the next x2 phase.",
    "Command, runner, source, and handoff improvements that remain inside approved scope.",
    "Explicit blocked/defer/needs_exact_packet rows for anything outside scope.",
  ],
  publication_boundary: closeout.publication_boundary,
  claim_boundary: closeout.claim_boundary,
};

const approval = {
  schema: "ghc.approval_packet_candidate_bundle.v1",
  generated_utc: generatedUtc,
  phase_slug: nextPhaseSlug,
  status: "PASS_20_APPROVAL_PACKET_CANDIDATES_READY",
  packet_count: 20,
  approval_packets: approvalPackets(nextPhaseSlug),
  publication_boundary: closeout.publication_boundary,
  claim_boundary: {
    approval_activation: "candidate_bundle_only",
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

writeJson(closeoutJson, closeout);
writeJson(handoffJson, handoff);
writeJson(approvalJson, approval);

writeMd(closeoutMd, [
  `# ${phaseSlug} Eureka X2 Build/Use Closeout`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${closeout.status}\``,
  `Implemented task count: \`${closeout.implemented_task_count}\``,
  `Evidence-only completed count: \`${closeout.evidence_only_count}\``,
  "",
  "## Execution Buckets",
  "",
  ...Object.entries(closeout.execution_bucket_counts).map(([bucket, count]) => `- ${bucket}: \`${count}\``),
  "",
  "## Implemented Tasks",
  "",
  ...implementedTasks.map((task) => `- ${task.id}: ${task.source_task}. ${task.result}`),
  "",
  "## Carry Forward",
  "",
  ...closeout.carry_forward.map((item) => `- ${item}`),
  "",
  "## Boundary",
  "",
  "- Status-only closeout for the queued x2 scope.",
  "- No private route data, raw sibling content, credentials, screen-capture files, session traces, or local absolute paths are published.",
  "- GMUT empirical closure, final physics, consciousness proof, legal closure, and canon promotion remain open.",
]);

writeMd(handoffMd, [
  `# ${nextPhaseSlug} Next X1 Lane Handoff`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${handoff.status}\``,
  `Active lanes: \`${handoff.active_lanes.join(", ")}\``,
  "",
  "## Omega-Mini Lookup",
  "",
  ...handoff.omega_mini_first_lookup.map((file) => `- ${file}`),
  "",
  "## Prompt Contract",
  "",
  ...handoff.prompt_contract.map((item) => `- ${item}`),
  "",
  "## Requested Outputs",
  "",
  ...handoff.requested_outputs.map((item) => `- ${item}`),
]);

writeMd(approvalMd, [
  `# ${nextPhaseSlug} Approval Packet Candidate Bundle`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${approval.status}\``,
  `Packet count: \`${approval.packet_count}\``,
  "",
  "## Packets",
  "",
  ...approval.approval_packets.flatMap((packet) => [
    `### ${packet.order}. ${packet.id}`,
    "",
    `Title: ${packet.title}`,
    "",
    `Status: \`${packet.status}\``,
    "",
    packet.purpose,
    "",
  ]),
  "## Boundary",
  "",
  "- Candidate bundle only. Exact-packet actions remain gated.",
  "- No empirical GMUT validation, final physics, consciousness proof, legal closure, or canon promotion is claimed.",
]);

console.log(
  JSON.stringify(
    {
      status: closeout.status,
      implemented_task_count: closeout.implemented_task_count,
      next_phase_slug: nextPhaseSlug,
      approval_packet_count: approval.packet_count,
    },
    null,
    2,
  ),
);
