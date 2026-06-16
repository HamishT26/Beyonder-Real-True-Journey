#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

function requireArg(name) {
  const value = args.get(name);
  if (!value) {
    console.error(`Missing ${name}`);
    process.exit(2);
  }
  return value;
}

const phaseSlug = requireArg("--phase-slug");
const nextX2 = requireArg("--next-x2");
const orderJson = requireArg("--order-json");
const currentJson = requireArg("--current-json");
const arbyTempDir = requireArg("--arby-temp-dir");
const outPrefix = requireArg("--out-prefix");

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function readJsonMaybe(path) {
  try {
    return readJson(path);
  } catch {
    return null;
  }
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function fileInfoSafe(path) {
  if (!existsSync(path)) return { exists: false, bytes: 0 };
  const stat = statSync(path);
  return { exists: true, bytes: stat.size };
}

function tempStatus(dir) {
  if (!existsSync(dir)) {
    return { temp_dir_present: false, file_count: 0, files: [] };
  }
  const files = readdirSync(dir)
    .filter((name) => name.startsWith("Arby-"))
    .sort()
    .map((name) => ({
      name,
      ...fileInfoSafe(join(dir, name)),
    }));
  const expected = files.find((row) => row.name === "Arby-last-message.txt");
  return {
    temp_dir_present: true,
    file_count: files.length,
    files,
    advisory_output_present: Boolean(expected?.exists && expected.bytes > 0),
    advisory_output_bytes: expected?.bytes || 0,
  };
}

function executionSlice(rows) {
  const executable = rows.filter((row) => row.execution_bucket === "authorized_execution_queue");
  const categories = [
    {
      name: "omega_mini_freshness",
      pattern: /omega-mini|current-state|beacon|lookup|freshness/i,
      target_count: 8,
    },
    {
      name: "approval_eureka_integrity",
      pattern: /approval|eureka|checklist|stack|selector|dedupe|firewall/i,
      target_count: 8,
    },
    {
      name: "runner_notifier_resilience",
      pattern: /runner|watcher|notifier|lane|route|sibling|handoff/i,
      target_count: 8,
    },
    {
      name: "skill_command_system_expansion",
      pattern: /skill|command|system|workflow|micro/i,
      target_count: 8,
    },
    {
      name: "source_security_reflection",
      pattern: /source|web|github|security|guard|boundary|reflection/i,
      target_count: 8,
    },
  ];
  return categories.map((category) => ({
    category: category.name,
    target_count: category.target_count,
    rows: executable
      .filter((row) => category.pattern.test(`${row.title || ""} ${row.id || ""} ${row.source_phase || ""}`))
      .slice(0, category.target_count)
      .map((row) => ({
        execution_order: row.execution_order,
        kind: row.kind,
        id: row.id,
        title: row.title,
        source_phase: row.source_phase,
      })),
  }));
}

const generatedUtc = utcNow();
const current = readJson(currentJson);
const order = readJson(orderJson);
const arby = tempStatus(arbyTempDir);
const ciceroRunner = readJsonMaybe(`docs/trinity-live-traces/${phaseSlug}-cicero-app-lane-v1.json`);
const ciceroPreflight = readJsonMaybe(`docs/trinity-live-traces/${phaseSlug}-cicero-app-lane-preflight-v1.json`);
const ciceroNotifier = readJsonMaybe(`docs/trinity-live-traces/${phaseSlug}-cicero-app-lane-notifier-v1.json`);
const ciceroLauncher = readJsonMaybe(`docs/trinity-live-traces/${phaseSlug}-cicero-app-lane-watch-launcher-v1.json`);
const ciceroGate = readJsonMaybe(`docs/trinity-live-traces/${phaseSlug}-cicero-app-lane-completion-gate-v1.json`);

const publicationBoundary = {
  raw_lane_content_published: false,
  raw_cli_stdout_published: false,
  raw_cli_stderr_published: false,
  raw_chatgpt_transcript_published: false,
  raw_route_handles_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  x1_complete: false,
  x2_complete: false,
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const sourceRefresh = [
  {
    topic: "Codex changelog and CLI/app update monitoring",
    source: "OpenAI Developers Codex changelog",
    url: "https://developers.openai.com/codex/changelog",
    use: "Track Codex app/CLI behavior that affects goal mode, app-server, Browser, and CLI lanes.",
  },
  {
    topic: "Browser developer mode and CDP",
    source: "OpenAI Developers Codex app Browser docs",
    url: "https://developers.openai.com/codex/app/browser",
    use: "Use CDP-oriented Browser diagnostics for live-adapter route health without raw route publication.",
  },
  {
    topic: "MCP roadmap and scalable sessions",
    source: "Model Context Protocol roadmap/spec materials",
    url: "https://modelcontextprotocol.io/development/roadmap",
    use: "Inform app-server/session continuity, stateless handoff, and connector boundary design.",
  },
  {
    topic: "Agentic AI threat modeling",
    source: "OWASP Agentic AI Threats and Mitigations",
    url: "https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/",
    use: "Keep multi-agent autonomy bounded by least privilege, monitoring, reversibility, and human authorization gates.",
  },
  {
    topic: "Agentic application top risks",
    source: "OWASP Top 10 for Agentic Applications 2026",
    url: "https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/",
    use: "Feed held-row firewall, exposure guard, and runner permission design.",
  },
];

const laneLaunch = {
  schema: "ghc.v544_v4_lane_launch_status.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "OPEN_X1_LANES_RUNNING_STATUS_ONLY",
  current_state_status: current.status,
  active_lanes: current.current_active_lanes || ["Arby", "Cicero"],
  arby_cli: {
    route_family: "strict read-only Codex CLI lane",
    launch_status: "started_by_strict_launcher",
    temp_bridge_status: arby,
  },
  cicero_app: {
    route_family: "existing app lane through recovered map runner",
    runner_status: ciceroRunner?.overall_status || ciceroRunner?.status || "pending",
    preflight_status: ciceroPreflight?.overall_status || ciceroPreflight?.status || "pending",
    notifier_status: ciceroNotifier?.overall_status || ciceroNotifier?.status || "pending",
    launcher_status: ciceroLauncher?.overall_status || ciceroLauncher?.status || "pending",
    gate_status: ciceroGate?.overall_status || ciceroGate?.status || "pending",
  },
  check_policy: {
    next_status_check_minutes: 5,
    aletheon_productive_waiting_required: true,
    do_not_babysit_between_checks: true,
  },
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const waitPrep = {
  schema: "ghc.v544_v4_productive_wait_prep.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  next_x2_scope: nextX2,
  status: "PASS_PRODUCTIVE_WAIT_PREP_READY",
  lane_status_summary: {
    arby_output_present: arby.advisory_output_present,
    cicero_gate_status: laneLaunch.cicero_app.gate_status,
  },
  source_refresh: sourceRefresh,
  x2_execution_slices: executionSlice(order.ordered_rows || []),
  immediate_x2_candidate_batch: [
    "Publish v544 v4 x1 launch and wait-prep receipts.",
    "Harvest Arby/Cicero completion at the five-minute check without raw lane publication.",
    "Convert completed x1 advisory signals into a v544 v4 x2 build/use closeout.",
    "Keep omega-mini current-state and latest-updates beacon synchronized after every commit.",
    "Continue held-row firewall and exact-packet gating for hard-boundary rows.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const launchJson = `${outPrefix}-lane-launch-status-v1.json`;
const launchMd = `${outPrefix}-lane-launch-status-v1.md`;
const waitJson = `${outPrefix}-productive-wait-prep-v1.json`;
const waitMd = `${outPrefix}-productive-wait-prep-v1.md`;

writeJson(launchJson, laneLaunch);
writeJson(waitJson, waitPrep);
writeMd(launchMd, [
  `# ${phaseSlug} Lane Launch Status`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${laneLaunch.status}\``,
  "",
  "## Active Lanes",
  "",
  "- Arby: strict read-only CLI lane launched; raw output remains temp-only.",
  `- Cicero: recovered app-lane runner status \`${laneLaunch.cicero_app.runner_status}\`; completion gate \`${laneLaunch.cicero_app.gate_status}\`.`,
  "",
  "## Check Policy",
  "",
  "- Next status check target: 5 minutes.",
  "- Aletheon continues productive x2 preparation between checks.",
  "- This receipt does not claim x1 completion.",
  "",
  "## Boundaries",
  "",
  "- No raw lane content, stdout/stderr, route handles, credentials, or local absolute paths are published.",
]);
writeMd(waitMd, [
  `# ${phaseSlug} Productive Wait Prep`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${waitPrep.status}\``,
  "",
  "## Source Refresh",
  "",
  ...sourceRefresh.map((row) => `- ${row.topic}: ${row.source} (${row.url})`),
  "",
  "## X2 Execution Slices",
  "",
  ...waitPrep.x2_execution_slices.flatMap((slice) => [
    `### ${slice.category}`,
    "",
    ...slice.rows.map((row) => `- ${row.execution_order}. ${row.id}: ${row.title}`),
    "",
  ]),
  "## Immediate X2 Candidate Batch",
  "",
  ...waitPrep.immediate_x2_candidate_batch.map((item) => `- ${item}`),
  "",
  "## Boundaries",
  "",
  "- This is planning/prep only. It does not claim Arby/Cicero completion or GMUT/physics/consciousness/canon closure.",
]);

console.log(
  JSON.stringify(
    {
      status: waitPrep.status,
      arby_output_present: arby.advisory_output_present,
      cicero_gate_status: laneLaunch.cicero_app.gate_status,
      source_count: sourceRefresh.length,
      x2_slice_count: waitPrep.x2_execution_slices.length,
    },
    null,
    2,
  ),
);
