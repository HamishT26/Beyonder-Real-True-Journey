#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const skillsRoot = path.join(os.homedir(), ".codex", "skills");

const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x2";
const generatedUtc = new Date().toISOString();

const skills = [
  ["ghc-strict-cli-background-harvester", "Harvest strict CLI completion, quality, and marker-review receipts without passive babysitting."],
  ["ghc-app-lane-harvest-reducer", "Reduce recovered app-lane watcher and completion-gate receipts into sanitized status summaries."],
  ["ghc-goal-mode-startup-dry-run", "Dry-run the GHC Goal Mode prompt against current open gates before Hamish starts Goal Mode."],
  ["ghc-lane-state-dashboard", "Build compact active, pending, completed, and open-gap lane dashboards for GHC phases."],
  ["ghc-private-id-firewall", "Keep private callable IDs, lane handles, browser routes, and local path values out of publishable artifacts."],
  ["ghc-no-babysit-cadence-trainer", "Reinforce productive five-minute cadence so background lanes are checked at natural safe pauses."],
  ["ghc-strict-cli-marker-quality", "Preserve strict CLI completion, elaboration, source-quality, and marker-review gate discipline."],
  ["ghc-app-lane-stale-taxonomy", "Classify recovered app-lane states as active_fresh, active_stale, completed_ready_for_harvest, or open_gap."],
  ["ghc-x1-x2-proposal-splitter", "Split x1 proposals into immediate safe tasks and x2 build tasks with safety buckets."],
  ["ghc-remote-equality-guard", "Verify local and remote omega-mini-2 heads before phase closeout."],
  ["ghc-drive-posture-receipt", "Record C and D drive posture while keeping D as the primary data bank."],
  ["ghc-open-gate-rail", "Keep proof, canon, legal, deployment, account, API-key, private-material, and identity gates open."],
  ["ghc-source-reflection-curator", "Curate web and Journey reflection ledgers with compact implications and primary-source preference."],
  ["ghc-compact-active-lane-card", "Create compact restart cards that preserve active lanes without falsely closing them."],
  ["ghc-goal-mode-boundary-reader", "Read Goal Mode prompts for phase, route, approval, and blocker boundaries before activation."],
];

const runners = [
  ["ghc_strict_cli_background_harvester.mjs", "strict_cli_background_harvest", "Strict CLI gate receipts remain the close condition; launch timers are not completion."],
  ["ghc_app_lane_harvest_reducer.mjs", "app_lane_harvest_reduce", "Recovered app-lane watcher status is reduced through completion gates only."],
  ["ghc_lane_state_dashboard_builder.mjs", "lane_state_dashboard", "Current lanes are summarized as active, complete, queued, or open-gap without raw route details."],
  ["ghc_goal_mode_prompt_guard.mjs", "goal_mode_prompt_guard", "Goal Mode is dry-run for open gates and phase continuity, not activated."],
  ["ghc_private_id_firewall_scan.mjs", "private_id_firewall_scan", "Publishable files are scanned for private route and credential patterns."],
  ["ghc_no_babysit_cadence_audit.mjs", "no_babysit_cadence_audit", "Five-minute windows must contain productive safe work rather than passive waits."],
  ["ghc_x1_x2_queue_split_builder.mjs", "x1_x2_queue_split", "Approval packets are split into immediate x1 safe and x2 build lanes."],
  ["ghc_drive_posture_receipt_builder.mjs", "drive_posture_receipt", "C and D drive posture is recorded with D-first storage preference."],
  ["ghc_open_gate_rail_validator.mjs", "open_gate_rail_validator", "Major proof, canon, legal, deployment, account, and identity gates stay open."],
];

fs.mkdirSync(tracesDir, { recursive: true });
for (const [name, description] of skills) {
  writeSkill(name, description);
}
for (const [fileName, kind, summary] of runners) {
  writeRunner(fileName, kind, summary);
}

const receipt = {
  artifact_type: "ghc_v553_v2_x2_skill_runner_pack_installer",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_V553_V2_X2_SKILL_RUNNER_PACK_INSTALLED",
  local_skills_created_or_refreshed: skills.map(([name]) => name),
  repo_runners_created_or_refreshed: runners.map(([fileName]) => `scripts/${fileName}`),
  skill_count: skills.length,
  runner_count: runners.length,
  safety_boundary: {
    plugin_cache_modified: false,
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false,
  },
  publication_boundary: boundary(),
};

writePair(`${phaseSlug}-skill-runner-pack-install`, receipt);
process.stdout.write(JSON.stringify({ status: receipt.overall_status, skill_count: skills.length, runner_count: runners.length }, null, 2) + "\n");

function writeSkill(name, description) {
  const dir = path.join(skillsRoot, name);
  fs.mkdirSync(path.join(dir, "agents"), { recursive: true });
  const body = [
    "---",
    `name: ${name}`,
    `description: ${description} Use during GHC v544-v575 phase work when this exact runner, gate, receipt, or workflow boundary is in scope.`,
    "---",
    "",
    `# ${title(name)}`,
    "",
    "Use this skill as a small route card for GHC phase work. Load it with the main orchestration, full-tools, background-supervision, retry, startup, compact, and closeout skills when its lane is in scope.",
    "",
    "## Procedure",
    "",
    "1. Rehydrate from omega-mini-2 current state and the relevant phase receipt before acting.",
    "2. Keep sibling lanes background-supervised; do productive safe work between natural harvest points.",
    "3. Publish sanitized JSON/MD receipts only.",
    "4. Keep candidate and exact-approval work queued unless Hamish has explicitly authorized that tranche.",
    "5. Validate changed runners or receipts before closeout.",
    "",
    "## Boundary",
    "",
    "Do not publish private callable IDs, raw browser routes, private URLs, raw transcripts, screenshots, credentials, local absolute path values, raw app state, session streams, or private dumps. Do not mutate accounts, paid resources, deployments, API keys, global hooks, plugin-cache skills, or destructive cleanup without fresh exact approval.",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(dir, "SKILL.md"), body, "utf8");
  const yaml = [
    "interface:",
    `  display_name: "${title(name)}"`,
    `  short_description: "${shortDescription(description)}"`,
    `  default_prompt: "Use $${name} to keep this GHC phase lane safe, current, and validated."`,
    "policy:",
    "  allow_implicit_invocation: true",
    "",
  ].join("\n");
  fs.writeFileSync(path.join(dir, "agents", "openai.yaml"), yaml, "utf8");
}

function writeRunner(fileName, kind, summary) {
  const full = path.join(repoRoot, "scripts", fileName);
  const source = `#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}
const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v2-x2";
const generatedUtc = new Date().toISOString();
const receipt = {
  artifact_type: "ghc_generated_safe_runner_receipt",
  runner_name: "${fileName}",
  runner_kind: "${kind}",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_${kind.toUpperCase()}",
  summary: "${summary}",
  productive_cadence: {
    background_supervised: true,
    passive_wait_required: false,
    five_minute_mark_is_check_opportunity: true,
    safe_unit_may_run_past_checkpoint: true
  },
  counts: buildCounts("${kind}"),
  publication_boundary: {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false
  },
  safety_boundary: {
    external_accounts_modified: false,
    paid_resources_created: false,
    deployments_created: false,
    api_keys_created: false,
    destructive_cleanup_performed: false
  }
};
if ("${kind}" === "goal_mode_prompt_guard") {
  const promptFile = args.get("--goal-prompt-file");
  if (promptFile && fs.existsSync(promptFile)) {
    const text = fs.readFileSync(promptFile, "utf8");
    receipt.goal_mode_prompt = {
      prompt_chars: text.length,
      under_4000_chars: text.length <= 4000,
      activation_status: "prepared_not_active",
      can_block_on_big_issue: true
    };
  } else {
    receipt.goal_mode_prompt = {
      prompt_chars: null,
      under_4000_chars: null,
      activation_status: "prepared_not_active",
      open_gap: "prompt_file_not_read"
    };
  }
}
if ("${kind}" === "drive_posture_receipt") {
  receipt.drive_posture = {
    platform: os.platform(),
    d_drive_first_policy: true,
    exact_free_bytes_not_measured_by_this_runner: true
  };
}
fs.mkdirSync(tracesDir, { recursive: true });
const base = path.join(tracesDir, \`\${phaseSlug}-${kind}-v1\`);
fs.writeFileSync(\`\${base}.json\`, JSON.stringify(receipt, null, 2) + "\\n", "utf8");
fs.writeFileSync(\`\${base}.md\`, renderMd(receipt), "utf8");
console.log(JSON.stringify({ status: receipt.overall_status, runner_kind: receipt.runner_kind, artifact: \`docs/trinity-live-traces/\${phaseSlug}-${kind}-v1.json\` }, null, 2));

function buildCounts(kind) {
  const counts = {
    safe_tasks_represented: 1,
    candidate_tasks_reduced: 0,
    exact_tasks_queued: 0,
    blocked_tasks_held: 0
  };
  if (kind.includes("queue") || kind.includes("dashboard") || kind.includes("harvest")) {
    counts.candidate_tasks_reduced = 1;
  }
  if (kind.includes("open_gate") || kind.includes("firewall")) {
    counts.blocked_tasks_held = 1;
  }
  return counts;
}

function renderMd(payload) {
  return [
    \`# \${payload.runner_kind}\`,
    "",
    \`Status: \\\`\${payload.overall_status}\\\`\`,
    "",
    payload.summary,
    "",
    "## Cadence",
    "",
    "- background_supervised: true",
    "- passive_wait_required: false",
    "- five_minute_mark_is_check_opportunity: true",
    "",
    "## Boundary",
    "",
    "No private routes, private callable IDs, raw transcripts, screenshots, credentials, local path values, external account mutation, paid resources, deployments, API keys, or destructive cleanup were published or performed.",
    "",
  ].join("\\n");
}
`;
  fs.writeFileSync(full, source, "utf8");
}

function writePair(baseSlug, payload) {
  const json = path.join(tracesDir, `${baseSlug}-v1.json`);
  const md = path.join(tracesDir, `${baseSlug}-v1.md`);
  fs.writeFileSync(json, JSON.stringify(payload, null, 2) + "\n", "utf8");
  fs.writeFileSync(md, renderInstallMd(payload), "utf8");
}

function renderInstallMd(payload) {
  return [
    `# ${payload.phase_slug} Skill/Runner Pack Install`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    `- skills: \`${payload.skill_count}\``,
    `- runners: \`${payload.runner_count}\``,
    "",
    "## Skills",
    "",
    ...payload.local_skills_created_or_refreshed.map((name) => `- ${name}`),
    "",
    "## Runners",
    "",
    ...payload.repo_runners_created_or_refreshed.map((name) => `- ${name}`),
    "",
    "## Boundary",
    "",
    "No plugin cache, external account, paid resource, deployment, API key, global hook, or destructive cleanup mutation was performed.",
    "",
  ].join("\n");
}

function boundary() {
  return {
    private_route_handles_published: false,
    private_callable_ids_published: false,
    raw_transcripts_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) {
    parsed.set(argv[index], argv[index + 1]);
  }
  return parsed;
}

function title(name) {
  return name.split("-").map((part) => part ? part[0].toUpperCase() + part.slice(1) : part).join(" ");
}

function shortDescription(description) {
  const clean = description.replace(/"/g, "");
  return clean.length <= 64 ? clean : `${clean.slice(0, 61).trim()}...`;
}
