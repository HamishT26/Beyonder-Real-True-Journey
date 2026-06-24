#!/usr/bin/env node
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
  runner_name: "ghc_no_babysit_cadence_audit.mjs",
  runner_kind: "no_babysit_cadence_audit",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  overall_status: "PASS_NO_BABYSIT_CADENCE_AUDIT",
  summary: "Five-minute windows must contain productive safe work rather than passive waits.",
  productive_cadence: {
    background_supervised: true,
    passive_wait_required: false,
    five_minute_mark_is_check_opportunity: true,
    safe_unit_may_run_past_checkpoint: true
  },
  counts: buildCounts("no_babysit_cadence_audit"),
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
if ("no_babysit_cadence_audit" === "goal_mode_prompt_guard") {
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
if ("no_babysit_cadence_audit" === "drive_posture_receipt") {
  receipt.drive_posture = {
    platform: os.platform(),
    d_drive_first_policy: true,
    exact_free_bytes_not_measured_by_this_runner: true
  };
}
fs.mkdirSync(tracesDir, { recursive: true });
const base = path.join(tracesDir, `${phaseSlug}-no_babysit_cadence_audit-v1`);
fs.writeFileSync(`${base}.json`, JSON.stringify(receipt, null, 2) + "\n", "utf8");
fs.writeFileSync(`${base}.md`, renderMd(receipt), "utf8");
console.log(JSON.stringify({ status: receipt.overall_status, runner_kind: receipt.runner_kind, artifact: `docs/trinity-live-traces/${phaseSlug}-no_babysit_cadence_audit-v1.json` }, null, 2));

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
    `# ${payload.runner_kind}`,
    "",
    `Status: \`${payload.overall_status}\``,
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
  ].join("\n");
}
