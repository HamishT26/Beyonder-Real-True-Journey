#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const ROOT = new URL("..", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const root = args.get("--root") || ROOT;
const phaseSlug = args.get("--phase-slug");
const manifest = args.get("--manifest");
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-safe-runner-orchestrator`;
const minReflections = args.get("--min-reflections");

if (!phaseSlug || !manifest) {
  console.error("Usage: node ghc_safe_runner_orchestrator.mjs --phase-slug <slug> --manifest <json>");
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function parseStatus(stdout) {
  try {
    return JSON.parse(stdout || "{}").status || "json_status_missing";
  } catch {
    return "unparsed";
  }
}

function run(label, commandArgs) {
  const proc = spawnSync(process.execPath, commandArgs, {
    cwd: root,
    encoding: "utf8",
    windowsHide: true,
    maxBuffer: 1024 * 1024,
  });
  return {
    label,
    status: proc.status,
    signal: proc.signal,
    stdout_status: parseStatus(proc.stdout),
    stdout_bytes: Buffer.byteLength(proc.stdout || "", "utf8"),
    stderr_bytes: Buffer.byteLength(proc.stderr || "", "utf8"),
  };
}

const generatedUtc = utcNow();
const steps = [
  run("startup_context_update", [
    join(root, "scripts", "ghc_phase_startup_context_updater.mjs"),
    "--root",
    root,
    "--phase-slug",
    phaseSlug,
    "--event",
    "startup",
    "--agent",
    "Aevren Vale",
    "--receipt-prefix",
    `${receiptPrefix}-startup-context`,
  ]),
  run("web_search_phase_reflection_ledger", [
    join(root, "scripts", "ghc_phase_reflection_ledger_builder.mjs"),
    "--root",
    root,
    "--phase-slug",
    phaseSlug,
    "--manifest",
    manifest,
    "--receipt-prefix",
    `${receiptPrefix}-reflection-ledger`,
    ...(minReflections ? ["--min-reflections", minReflections] : []),
  ]),
  run("compact_pause_context_update", [
    join(root, "scripts", "ghc_context_compact_pause_updater.mjs"),
    "--root",
    root,
    "--phase-slug",
    phaseSlug,
    "--agent",
    "Aevren Vale",
    "--receipt-prefix",
    `${receiptPrefix}-compact-pause`,
  ]),
];

const failed = steps.filter((step) => step.status !== 0);
const receipt = {
  artifact_type: "ghc_safe_runner_orchestrator",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: failed.length === 0 ? "PASS_SAFE_RUNNER_ORCHESTRATION" : "OPEN_GAP_SAFE_RUNNER_ORCHESTRATION",
  runner_count: steps.length,
  steps,
  policy: {
    creates_new_agents: false,
    mutates_accounts: false,
    deploys_resources: false,
    installs_global_hooks: false,
    publishes_private_routes: false,
    never_closes_active_sibling_lane: true,
    blocker_retry_minimum_sessions_before_pause: 3,
    blocker_retry_web_search_reflections_per_retry: 20,
    blocker_retry_journey_phase_reflections_per_retry: 20,
  },
  publication_boundary: {
    private_route_handles_published: false,
    private_lane_body_content_published: false,
    verbatim_conversation_logs_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const traceDir = join(root, "docs", "trinity-live-traces");
const receiptJson = join(traceDir, `${receiptPrefix}-v1.json`);
const receiptMd = join(traceDir, `${receiptPrefix}-v1.md`);
mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(
  receiptMd,
  [
    `# ${phaseSlug} Safe Runner Orchestrator`,
    "",
    `Generated UTC: \`${generatedUtc}\``,
    "",
    `Status: \`${receipt.overall_status}\``,
    "",
    "## Steps",
    "",
    ...steps.map((step) => `- ${step.label}: exit \`${step.status}\`, stdout status \`${step.stdout_status}\``),
    "",
    "## Blocker Retry Policy",
    "",
    "- Never close active sibling lanes: `true`",
    "- Minimum retry sessions before pause: `3`",
    "- Web-search reflections per retry: `20`",
    "- Journey/phase-document reflections per retry: `20`",
    "",
    "## Boundary",
    "",
    "Status-only runner orchestrator. No new agents, account mutations, deployments, global hooks, private routes, verbatim conversation logs, credentials, or local absolute paths are published.",
    "",
  ].join("\n"),
  "utf8",
);

console.log(
  JSON.stringify(
    {
      status: receipt.overall_status,
      runner_count: steps.length,
      receipt: basename(receiptJson),
    },
    null,
    2,
  ),
);
process.exit(failed.length === 0 ? 0 : 1);
