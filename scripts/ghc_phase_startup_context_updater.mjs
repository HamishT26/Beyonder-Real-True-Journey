#!/usr/bin/env node
import { appendFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const root = args.get("--root") || ROOT;
const phaseSlug = args.get("--phase-slug");
const event = args.get("--event") || "startup";
const agent = args.get("--agent") || "Aevren Vale";
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-startup-context-updater`;

if (!phaseSlug) {
  console.error(
    "Usage: node ghc_phase_startup_context_updater.mjs --phase-slug <slug> [--event startup|resume|compact-pause] [--agent <name>] [--receipt-prefix <prefix>] [--root <repo>]",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function nzNow() {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  })
    .formatToParts(new Date())
    .reduce((acc, part) => {
      if (part.type !== "literal") acc[part.type] = part.value;
      return acc;
    }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function statusOf(file) {
  if (!existsSync(file)) return "missing";
  try {
    const payload = readJson(file);
    return payload.overall_status || payload.status || payload.schema || "status_missing";
  } catch {
    return "unreadable";
  }
}

const traceDir = join(root, "docs", "trinity-live-traces");
const current = readJson(join(root, "docs", "omega-mini-index", "omega-mini-current-state-v1.json"));
const beacon = readJson(join(root, "docs", "omega-mini-index", "omega-mini-latest-updates-beacon-v1.json"));

const lookupFiles = Array.isArray(current.current_lookup_files) ? current.current_lookup_files : [];
const lookupStatuses = lookupFiles.slice(0, 24).map((relative) => ({
  file: relative,
  status: statusOf(join(root, relative)),
}));

const generatedUtc = utcNow();
const generatedNz = nzNow();
const receipt = {
  artifact_type: "ghc_phase_startup_context_updater",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  event,
  agent,
  overall_status: "PASS_STARTUP_CONTEXT_UPDATED",
  timestamp_flow: {
    recorded_agent_start: event === "startup" || event === "resume",
    recorded_compact_pause: event === "compact-pause",
    utc: generatedUtc,
    nz: generatedNz,
  },
  current_state_snapshot: {
    current_active_phase: current.current_active_phase,
    latest_closed_phase: current.latest_closed_phase,
    latest_completed_x1_phase: current.latest_completed_x1_phase,
    latest_completed_x2_phase: current.latest_completed_x2_phase,
    next_expected_scope: current.next_expected_scope,
    next_x1_lane_after_x2: current.next_x1_lane_after_x2,
    status: current.status,
  },
  rule_set_snapshot: {
    branch: current.branch,
    archive_fallback_rule: current.archive_fallback_rule,
    background_runner_standard: current.background_runner_standard || null,
    no_new_agents_without_explicit_request: true,
    watcher_start_is_completion_proof: false,
    proof_and_deployment_gates_remain_open: true,
  },
  lookup_statuses: lookupStatuses,
  beacon_status: beacon.status || "status_missing",
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
  },
};

const receiptJson = join(traceDir, `${receiptPrefix}-v1.json`);
const receiptMd = join(traceDir, `${receiptPrefix}-v1.md`);
mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} Startup Context Updater`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Generated NZ: \`${generatedNz}\``,
  "",
  `Status: \`${receipt.overall_status}\``,
  `Event: \`${event}\``,
  `Agent: \`${agent}\``,
  "",
  "## Current State",
  "",
  `- active phase: \`${receipt.current_state_snapshot.current_active_phase}\``,
  `- latest closed phase: \`${receipt.current_state_snapshot.latest_closed_phase}\``,
  `- latest completed x1: \`${receipt.current_state_snapshot.latest_completed_x1_phase}\``,
  `- latest completed x2: \`${receipt.current_state_snapshot.latest_completed_x2_phase}\``,
  `- next expected scope: \`${receipt.current_state_snapshot.next_expected_scope}\``,
  "",
  "## Rule Snapshot",
  "",
  "- no new agents without explicit request: `true`",
  "- watcher-start is completion proof: `false`",
  "- proof/canon/legal/deployment gates remain open: `true`",
  "",
  "## Boundary",
  "",
  "Status-only updater. No private routes, private lane body content, raw transcripts, browser routes, credentials, or local absolute paths are published.",
  "",
].join("\n");
writeFileSync(receiptMd, md, "utf8");

const logPath = join(traceDir, "ghc-phase-startup-log-v1.jsonl");
appendFileSync(
  logPath,
  `${JSON.stringify({
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    event,
    agent,
    receipt: basename(receiptJson),
    status: receipt.overall_status,
  })}\n`,
  "utf8",
);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      event,
      phase_slug: phaseSlug,
      receipt: basename(receiptJson),
    },
    null,
    2,
  ),
);
