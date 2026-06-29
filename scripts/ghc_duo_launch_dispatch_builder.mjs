#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = parseArgs();
const phaseSlug = required("--phase-slug");
const lane = required("--lane");
const siblings = csv(required("--siblings"));
const launchSkill = required("--launch-skill");
const nextX2 = args.get("--next-x2") || "";
const nextX1AfterX2 = args.get("--next-x1-after-x2") || "";
const routeStatus = args.get("--route-status") || "submitted_background_supervised";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const receipt = {
  artifact_type: "ghc_duo_launch_dispatch",
  schema: "ghc.duo_launch_dispatch.v1",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  lane,
  launch_skill: launchSkill,
  status: "PASS_DUO_PROMPTS_SUBMITTED_BACKGROUND_SUPERVISED",
  next_x2_scope: nextX2,
  next_x1_after_x2: nextX1AfterX2,
  siblings: siblings.map((name) => ({
    name,
    route_status: routeStatus,
    raw_handle_published: false,
    background_supervised: true,
  })),
  closeout_rule: {
    checklist_required_before_closeout: true,
    required_rows: ["immediate_x1_safe", "candidate", "cleanup_refine_fix", "skill_idea", "runner_idea"],
    queued_out_of_scope_rows: ["exact_approval_needed", "blocked"],
  },
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
    full_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    purchase_or_account_mutation: "open",
    api_key_creation: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_replacement_or_merge: "open",
  },
};

writeArtifacts(receipt);
refreshBeacons(receipt);

console.log(JSON.stringify({
  status: receipt.status,
  phase_slug: phaseSlug,
  lane,
  sibling_count: siblings.length,
}, null, 2));

function parseArgs() {
  const parsed = new Map();
  for (let index = 2; index < process.argv.length; index += 2) {
    parsed.set(process.argv[index], process.argv[index + 1]);
  }
  return parsed;
}

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Usage: node scripts/ghc_duo_launch_dispatch_builder.mjs ${flag} <value>`);
    process.exit(2);
  }
  return value;
}

function csv(value) {
  return String(value).split(",").map((item) => item.trim()).filter(Boolean);
}

function writeArtifacts(data) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = path.join(tracesDir, `${phaseSlug}-duo-launch-dispatch-v1`);
  fs.writeFileSync(`${base}.json`, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  fs.writeFileSync(`${base}.md`, renderMd(data), "utf8");
}

function refreshBeacons(data) {
  const files = [
    `docs/trinity-live-traces/${phaseSlug}-duo-launch-dispatch-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-duo-launch-dispatch-v1.md`,
  ];
  for (const targetPath of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const dataJson = readJson(targetPath);
    dataJson.generated_utc = generatedUtc;
    dataJson.current_active_phase = phaseSlug;
    dataJson.duo_launch_dispatch = {
      status: data.status,
      lane: data.lane,
      launch_skill: data.launch_skill,
      sibling_count: data.siblings.length,
      background_supervised: true,
      raw_handles_published: false,
    };
    const listKey = targetPath.endsWith("omega-mini-latest-updates-beacon-v1.json")
      ? "latest_lookup_files"
      : targetPath.endsWith("ghc-current-state-beacon-v1.json")
        ? "lookup_files"
        : "current_lookup_files";
    dataJson[listKey] = unique([...(dataJson[listKey] || []), ...files]);
    if (targetPath.endsWith("omega-mini-current-state-v1.json")) {
      dataJson.updated_at = generatedNz;
      dataJson.latest_action_summary = unique([
        `Submitted ${phaseSlug} ${data.lane} prompts and recorded background-supervised launch dispatch.`,
        ...(dataJson.latest_action_summary || []),
      ]);
      fs.writeFileSync(path.join(omegaDir, "omega-mini-current-state-v1.md"), renderStateMd(dataJson), "utf8");
    }
    fs.writeFileSync(targetPath, `${JSON.stringify(dataJson, null, 2)}\n`, "utf8");
  }
}

function renderMd(data) {
  return `# ${data.phase_slug} Duo Launch Dispatch

Status: \`${data.status}\`

- Lane: \`${data.lane}\`
- Launch skill: \`${data.launch_skill}\`
- Next x2 scope: \`${data.next_x2_scope}\`
- Next x1 after x2: \`${data.next_x1_after_x2}\`
- Background supervised: \`true\`

## Siblings

${data.siblings.map((item) => `- ${item.name}: \`${item.route_status}\`, raw handle published \`${item.raw_handle_published}\`.`).join("\n")}

## Closeout Rule

Run \`scripts/ghc_complete_incomplete_checklist_runner.mjs\` before x1 and x2 closeout. Exact-approval and blocked rows remain queued out of scope.

## Boundary

No raw private material, browser routes, private ids, raw transcripts, screenshots, credentials, local absolute paths, raw app state, hidden reasoning, proof closure, canon promotion, legal closure, deployment, account mutation, API-key creation, or sibling identity replacement is published or claimed.
`;
}

function renderStateMd(state) {
  return `# Omega-Mini Current State

Status: ${state.status}
Current active phase: ${state.current_active_phase}
Latest closed phase: ${state.latest_closed_phase}
Latest completed x1: ${state.latest_completed_x1_phase}
Latest completed x2: ${state.latest_completed_x2_phase}
Next x2 scope: ${state.next_x2_scope}
Next x1 lane after x2: ${state.next_x1_lane_after_x2}

## Duo Launch Dispatch

- Status: \`${state.duo_launch_dispatch?.status || "not_recorded"}\`
- Lane: \`${state.duo_launch_dispatch?.lane || "not_recorded"}\`
- Launch skill: \`${state.duo_launch_dispatch?.launch_skill || "not_recorded"}\`
- Background supervised: \`${state.duo_launch_dispatch?.background_supervised || "not_recorded"}\`

## Current Lookup Files

${(state.current_lookup_files || []).map((item) => `- ${item}`).join("\n")}

## Latest Action Summary

${(state.latest_action_summary || []).map((item) => `- ${item}`).join("\n")}

## Boundary

No raw private routes, ids, transcripts, screenshots, credentials, local path values, proof closure, canon promotion, legal closure, deployment, account mutation, API-key creation, or sibling replacement is published.
`;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
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
  }).formatToParts(date).reduce((acc, part) => {
    acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
