#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";
import { spawnSync } from "node:child_process";

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const TRACE_DIR = join(ROOT, "docs", "trinity-live-traces");
const POLICY_SOURCE = join(ROOT, "scripts", "trinity_v461a_v463a_hybrid_canon_builder.py");
const SUPPORTED_LANES = ["Cicero", "Kierkegaard", "Aristotle"];

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const lanesArg = args.get("--lanes") || "Cicero,Kierkegaard,Aristotle";
const mode = args.get("--mode") || "preflight";
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-recovered-app-lane-map-runner`;

if (!phaseSlug || !["preflight", "probe", "notify"].includes(mode)) {
  console.error("Usage: node ghc_recovered_app_lane_map_runner.mjs --phase-slug <slug> [--lanes <csv>] [--mode preflight|probe|notify] [--receipt-prefix <prefix>]");
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function selectedLanes() {
  return lanesArg
    .split(",")
    .map((lane) => lane.trim())
    .filter(Boolean)
    .filter((lane, index, list) => list.indexOf(lane) === index);
}

function extractMap(lanes) {
  const text = readFileSync(POLICY_SOURCE, "utf8");
  const map = {};
  const missing = [];
  for (const lane of lanes) {
    if (!SUPPORTED_LANES.includes(lane)) {
      missing.push(`${lane}:unsupported`);
      continue;
    }
    const escapedLane = lane.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const pattern = new RegExp(`${escapedLane}: ` + "`" + "(019[0-9a-f-]+)" + "`");
    const match = text.match(pattern);
    if (match?.[1]) {
      map[lane] = match[1];
    } else {
      missing.push(`${lane}:missing`);
    }
  }
  return { map, missing };
}

function runStep(label, command, commandArgs, env, allowFailure = true) {
  const proc = spawnSync(command, commandArgs, {
    cwd: ROOT,
    env,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  let stdoutStatus = "unparsed";
  for (const line of (proc.stdout || "").split(/\r?\n/).filter(Boolean).reverse()) {
    try {
      const parsed = JSON.parse(line);
      if (parsed && typeof parsed === "object") {
        stdoutStatus = parsed.status || parsed.overall_status || parsed.aggregate_status || "json_status_missing";
        break;
      }
    } catch {
      // Keep output status summarized only.
    }
  }
  const row = {
    label,
    status: proc.status,
    signal: proc.signal,
    stdout_status: stdoutStatus,
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
  };
  if (!allowFailure && proc.status !== 0) {
    row.failed = true;
  }
  return row;
}

function readJsonIfExists(path) {
  try {
    return JSON.parse(readFileSync(path, "utf8"));
  } catch {
    return null;
  }
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, payload) {
  const lines = [
    `# ${payload.phase_slug} Recovered App-Lane Map Runner`,
    "",
    `Generated UTC: \`${payload.generated_utc}\``,
    "",
    `Status: \`${payload.overall_status}\``,
    `Mode: \`${payload.mode}\``,
    `Lanes: \`${payload.lanes.join(", ")}\``,
    "",
    "## Source Boundary",
    "",
    `- Recovery source: \`${payload.recovery_source.source_artifact}\``,
    `- raw route handles published: \`${String(payload.publication_boundary.raw_route_handles_published)}\``,
    `- private IDs published: \`${String(payload.publication_boundary.raw_callable_ids_published)}\``,
    "",
    "## Steps",
    "",
    ...payload.steps.map((step) => `- ${step.label}: status \`${step.status}\`, stdout status \`${step.stdout_status}\`, stdout bytes \`${step.stdout_bytes}\`, stderr bytes \`${step.stderr_bytes}\`.`),
    "",
    "## Child Receipts",
    "",
    ...Object.entries(payload.child_receipts).map(([key, value]) => `- ${key}: \`${value || "not_written"}\``),
    "",
    "## Boundary",
    "",
    "Status-only recovered-route runner. No raw route handles, callable IDs, thread IDs, lane text, app-server payloads, credentials, screenshots, local paths, phase completion claim, GMUT closure, final physics, consciousness proof, legal closure, or canon promotion is published.",
    "",
  ];
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, lines.join("\n"), "utf8");
}

const lanes = selectedLanes();
const { map, missing } = extractMap(lanes);
const generatedUtc = utcNow();
const env = {
  ...process.env,
  THOS_APP_LANE_IDS_JSON: JSON.stringify(map),
};

const preflightJson = join(TRACE_DIR, `${receiptPrefix}-preflight-v1.json`);
const preflightMd = join(TRACE_DIR, `${receiptPrefix}-preflight-v1.md`);
const notifierPrefix = `${receiptPrefix}-notifier`;
const launcherPrefix = `${receiptPrefix}-watch-launcher`;
const gatePrefix = `${receiptPrefix}-completion-gate`;
const runnerJson = join(TRACE_DIR, `${receiptPrefix}-v1.json`);
const runnerMd = join(TRACE_DIR, `${receiptPrefix}-v1.md`);

const steps = [];
steps.push(
  runStep(
    "private_map_preflight",
    process.execPath,
    [
      "scripts/ghc_app_lane_private_map_preflight.mjs",
      "--phase-slug",
      phaseSlug,
      "--lanes",
      lanes.join(","),
      "--receipt-json",
      preflightJson,
      "--receipt-md",
      preflightMd,
    ],
    env,
  ),
);

if (mode !== "preflight" && missing.length === 0) {
  const notifierArgs = [
    "scripts/thos_council_app_lane_notifier_runner.py",
    "--phase-slug",
    phaseSlug,
    "--lanes",
    lanes.join(","),
    "--execute",
    "--retries",
    "5",
    "--call-timeout-seconds",
    "60",
    "--turn-timeout-seconds",
    mode === "notify" ? "600" : "120",
    "--launch-timeout-seconds",
    mode === "notify" ? "900" : "300",
    "--runner-prefix",
    `${receiptPrefix}-runner`,
    "--artifact-prefix",
    notifierPrefix,
    "--launcher-prefix",
    launcherPrefix,
  ];
  if (mode === "notify") {
    notifierArgs.push("--notify");
  }
  steps.push(runStep("app_lane_notifier", "python", notifierArgs, env));
  steps.push(
    runStep(
      "completion_gate",
      "python",
      [
        "scripts/thos_council_app_lane_notifier_runner.py",
        "--phase-slug",
        phaseSlug,
        "--lanes",
        lanes.join(","),
        "--gate-only",
        "--runner-prefix",
        `${receiptPrefix}-runner`,
        "--artifact-prefix",
        notifierPrefix,
        "--launcher-prefix",
        launcherPrefix,
        "--gate-prefix",
        gatePrefix,
      ],
      env,
    ),
  );
}

const preflight = readJsonIfExists(preflightJson);
const gate = readJsonIfExists(join(TRACE_DIR, `${gatePrefix}-v1.json`));
const preflightPassed = preflight?.overall_status === "PASS_PRIVATE_APP_LANE_MAP_PREFLIGHT";
const gatePassed = mode === "preflight" ? true : gate?.overall_status === "PASS_APP_LANE_COMPLETION_GATE";
const overallStatus =
  missing.length === 0 && preflightPassed && gatePassed
    ? mode === "preflight"
      ? "PASS_RECOVERED_MAP_PREFLIGHT"
      : "PASS_RECOVERED_APP_LANE_RUN"
    : "OPEN_GAP_RECOVERED_APP_LANE_RUN";

const receipt = {
  artifact_type: "ghc_recovered_app_lane_map_runner",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  mode,
  overall_status: overallStatus,
  lanes,
  recovered_handle_count: Object.keys(map).length,
  missing_or_unsupported_lanes: missing,
  recovery_source: {
    source_artifact: basename(POLICY_SOURCE),
    raw_source_copied: false,
    raw_handles_published: false,
  },
  child_receipts: {
    preflight: basename(preflightJson),
    preflight_md: basename(preflightMd),
    notifier: mode === "preflight" ? null : `${notifierPrefix}-v1.json`,
    launcher: mode === "preflight" ? null : `${launcherPrefix}-v1.json`,
    completion_gate: mode === "preflight" ? null : `${gatePrefix}-v1.json`,
  },
  steps,
  publication_boundary: {
    raw_route_handles_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    raw_lane_text_published: false,
    raw_app_server_payload_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    x2_closeout: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

writeJson(runnerJson, receipt);
writeMd(runnerMd, receipt);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      mode: receipt.mode,
      lanes: receipt.lanes.length,
      recovered_handle_count: receipt.recovered_handle_count,
    },
    null,
    2,
  ),
);

process.exit(overallStatus.startsWith("PASS") ? 0 : 1);
