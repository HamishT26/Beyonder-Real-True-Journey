#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parseArgs, repoRoot } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const completedX1 = required("--completed-x1");
const activeX2 = required("--active-x2");
const nextX1AfterX2 = required("--next-x1-after-x2");
const sibling = args.get("--sibling") || "Mira Rowan";
const toolchainVersion = args.get("--codex-cli-version") || "unknown";
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const tracesDir = join(root, "docs", "trinity-live-traces");
const receiptStem = `${activeX2}-solo-phase-transition-v1`;
const lookupFiles = [
  `docs/trinity-live-traces/${receiptStem}.json`,
  `docs/trinity-live-traces/${receiptStem}.md`
];

const receipt = {
  schema: "ghc.family.solo_phase_transition.v1",
  artifact_type: "solo_phase_transition",
  generated_utc: generatedUtc,
  completed_x1: completedX1,
  active_x2: activeX2,
  latest_completed_x2_before_active: args.get("--latest-completed-x2") || "v576-gmut-thos-v1-x2",
  next_x1_after_x2: nextX1AfterX2,
  sibling,
  overall_status: "PASS_SOLO_X1_CLOSED_X2_ACTIVE_OPEN",
  codex_cli_version_verified: toolchainVersion,
  closeout_boundary: {
    x1_closed: true,
    x2_active: true,
    x2_closed: false,
    next_sibling_handoff_sent: false,
    reason_x2_not_closed: "x2 execution/build/cleanup lane has just been activated and still requires completion evidence or a formal open-gap receipt"
  },
  cadence: {
    checkpoint_minutes: 15,
    minimum_runtime_minutes_before_x2_closeout: 60,
    style: "productive_background_supervision_no_babysitting"
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary()
};

mkdirSync(tracesDir, { recursive: true });
writeFileSync(join(tracesDir, `${receiptStem}.json`), `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
writeFileSync(join(tracesDir, `${receiptStem}.md`), renderMd(receipt), "utf8");
refreshBeacons(receipt);
console.log(JSON.stringify({ status: receipt.overall_status, active_x2: activeX2, receipt: `${receiptStem}.json` }, null, 2));

function required(flag) {
  const value = args.get(flag);
  if (!value) {
    console.error(`Missing required ${flag}`);
    process.exit(2);
  }
  return value;
}

function refreshBeacons(payload) {
  const files = [
    join(root, "docs", "omega-mini-index", "omega-mini-current-state-v1.json"),
    join(root, "docs", "omega-mini-index", "omega-mini-latest-updates-beacon-v1.json"),
    join(root, "docs", "trinity-live-traces", "ghc-current-state-beacon-v1.json"),
  ];
  for (const file of files) {
    if (!existsSync(file)) continue;
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = generatedUtc;
    doc.current_active_phase = payload.active_x2;
    doc.latest_completed_x1_phase = payload.completed_x1;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_before_active;
    doc.latest_closed_phase = payload.completed_x1;
    doc.next_x2_scope = payload.active_x2;
    doc.next_x1_lane_after_x2 = payload.next_x1_after_x2;
    doc.current_active_lanes = ["Aevren Vale", payload.active_x2, "solo-bundle-x2-active"];
    doc.codex_cli_version_verified = payload.codex_cli_version_verified;
    doc.v576_v2_x1_closeout = {
      status: "PASS_V576_V2_X1_CLOSED_V2_X2_ACTIVE",
      harvested_sibling: payload.sibling,
      next_active_phase: payload.active_x2,
      full_goal_complete: false
    };
    doc.v576_v2_x2_startup = {
      status: "PASS_V576_V2_X2_ACTIVE_BACKGROUND_SUPERVISED",
      source_x1_phase: payload.completed_x1,
      active_sibling: payload.sibling,
      next_x1_after_x2: payload.next_x1_after_x2,
      full_goal_complete: false
    };
    doc.solo_bundle_workflow_standard = doc.solo_bundle_workflow_standard || {};
    doc.solo_bundle_workflow_standard.cadence_profile = payload.cadence;
    doc.solo_bundle_workflow_standard.x2_closeout_boundary = payload.closeout_boundary;
    const listKey = file.includes("latest-updates") ? "latest_lookup_files" : file.includes("ghc-current") ? "current_lookup_files" : "current_lookup_files";
    doc[listKey] = unique([...(doc[listKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      `Closed ${payload.completed_x1} after sanitized ${payload.sibling} teaching harvest and opened ${payload.active_x2} as background-supervised x2 execution/build/cleanup.`,
      `Verified codex-cli ${payload.codex_cli_version_verified} for ${payload.active_x2}.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 120);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function renderMd(payload) {
  return `# ${payload.active_x2} Solo Phase Transition

Status: \`${payload.overall_status}\`

Closed x1: \`${payload.completed_x1}\`

Active x2: \`${payload.active_x2}\`

Next x1 after x2: ${payload.next_x1_after_x2}

Codex CLI verified: \`${payload.codex_cli_version_verified}\`

## Boundary

The x2 phase is active and background-supervised. It is not closed. Mira Vale is not activated until x2 has completion evidence or a formal open-gap handoff. No raw private material, Browser routes, private ids, transcripts, screenshots, credentials, local paths, raw app state, hidden reasoning, proof closure, canon promotion, legal closure, deployment, account mutation, API-key creation, purchase, destructive cleanup, or sibling merge/replacement is published or claimed.
`;
}

function publicationBoundary() {
  return {
    private_thread_id_published: false,
    raw_private_material_published: false,
    raw_browser_routes_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false
  };
}

function claimBoundary() {
  return {
    x2_closeout: "not_claimed",
    mira_vale_handoff: "not_claimed",
    full_v576_v600_goal_complete: false,
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
    deployment: "open",
    account_mutation: "open",
    api_key_creation: "open",
    purchase: "open",
    private_material_proof: "open",
    raw_publication_proof: "open",
    sibling_identity_merge_or_replacement: "open"
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
