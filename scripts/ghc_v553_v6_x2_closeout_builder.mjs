#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v6-x2";
const nextX1 = "v553-gmut-thos-v7-x1";
const nextX1Lane = `${nextX1} with Lumen unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  `${phaseSlug}-safe-execution-reducer-v1.json`,
  `${phaseSlug}-skill-runner-build-board-v1.json`,
  `${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
  `${phaseSlug}-v7-lumen-prep-card-v1.json`,
  `${phaseSlug}-private-open-gate-rail-v1.json`,
  `${phaseSlug}-phase-status-index-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  `${phaseSlug}-open-gate-claim-linter-v1.json`,
  `${phaseSlug}-goal-mode-prompt-fit-validator-v1.json`,
  `${phaseSlug}-sanitized-lane-harvest-reducer-v1.json`,
];
const docs = Object.fromEntries(required.map((name) => [name, readOptional(name)]));
const missing = required.filter((name) => !docs[name]);
const openGap = required.filter((name) => docs[name] && !String(docs[name].overall_status || docs[name].status || "").startsWith("PASS"));
const reflection = docs[`${phaseSlug}-web-journey-reflection-ledger-50-v1.json`];
const pass = missing.length === 0 && openGap.length === 0 && reflection?.web_reflections?.length >= 50 && reflection?.journey_phase_reflections?.length >= 50;

const receipt = {
  artifact_type: "ghc_v553_v6_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V553_V6_X2_CLOSED_V7_X1_READY" : "OPEN_GAP_V553_V6_X2_CLOSEOUT",
  latest_closed_phase: pass ? phaseSlug : "v553-gmut-thos-v6-x1",
  latest_completed_x1_phase: "v553-gmut-thos-v6-x1",
  latest_completed_x2_phase: pass ? phaseSlug : "v553-gmut-thos-v5-x2",
  next_active_phase: pass ? nextX1 : phaseSlug,
  next_x1_lane_after_x2: nextX1Lane,
  checks: {
    required_artifacts: required.length,
    missing_artifacts: missing.length,
    open_gap_artifacts: openGap.length,
    web_reflections: reflection?.web_reflections?.length || 0,
    journey_phase_reflections: reflection?.journey_phase_reflections?.length || 0,
    goal_prompt_status: docs[`${phaseSlug}-goal-mode-prompt-fit-validator-v1.json`]?.overall_status || "missing",
    lane_harvest_status: docs[`${phaseSlug}-sanitized-lane-harvest-reducer-v1.json`]?.overall_status || "missing",
  },
  next_phase_prep: {
    phase: nextX1,
    lane: "Lumen unless Hamish redirects",
    launch_skill: "ghc-lumen-launch",
    goal_mode_prompt_fit: docs[`${phaseSlug}-goal-mode-prompt-fit-validator-v1.json`]?.overall_status || "missing",
  },
  publication_boundary: publicationBoundary(),
  claim_boundary: claimBoundary(),
};

writePair(`${phaseSlug}-closeout`, receipt);
refreshBeacons(receipt);

console.log(JSON.stringify({
  status: receipt.overall_status,
  next_active_phase: receipt.next_active_phase,
  missing: missing.length,
  open_gap: openGap.length,
  web_reflections: receipt.checks.web_reflections,
  journey_phase_reflections: receipt.checks.journey_phase_reflections,
}, null, 2));
process.exit(pass ? 0 : 1);

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
  } catch {
    return null;
  }
}

function writePair(prefix, payload) {
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${prefix}-v1.md`), renderCloseoutMd(payload), "utf8");
}

function refreshBeacons(payload) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-closeout-v1.md`,
  ];
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = payload.overall_status;
    doc.current_active_phase = payload.next_active_phase;
    doc.latest_closed_phase = payload.latest_closed_phase;
    doc.latest_completed_x1_phase = payload.latest_completed_x1_phase;
    doc.latest_completed_x2_phase = payload.latest_completed_x2_phase;
    doc.next_expected_scope = payload.next_active_phase;
    doc.next_x2_scope = "v553-gmut-thos-v7-x2";
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v553_v6_x2_closeout = {
      status: payload.overall_status,
      checks: payload.checks,
      next_active_phase: payload.next_active_phase,
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = [...new Set([...(doc[key] || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(file.replace(/\.json$/, ".md"), renderBeaconMd(path.basename(file, ".json"), doc, doc[key]), "utf8");
  }
}

function renderCloseoutMd(payload) {
  return [
    `# ${phaseSlug} Closeout`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Next active phase: \`${payload.next_active_phase}\``,
    "",
    `- required artifacts: \`${payload.checks.required_artifacts}\``,
    `- missing artifacts: \`${payload.checks.missing_artifacts}\``,
    `- open-gap artifacts: \`${payload.checks.open_gap_artifacts}\``,
    `- web reflections: \`${payload.checks.web_reflections}\``,
    `- Journey/phase reflections: \`${payload.checks.journey_phase_reflections}\``,
    "",
    "No raw sibling output, private route handle, callable ID, local path value, credential, screenshot, proof closure, deployment/account/API-key mutation, private-material proof, raw-publication proof, or identity merge claim is published.",
    "",
  ].join("\n");
}

function renderBeaconMd(title, doc, files) {
  return [
    `# ${title}`,
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v553 v6 x2 Closeout",
    "",
    `- status: \`${doc.v553_v6_x2_closeout?.status || "not_recorded"}\``,
    `- next active phase: \`${doc.v553_v6_x2_closeout?.next_active_phase || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-120).map((item) => `- \`${item}\``),
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, legal/canon/deployment/account/API-key closures, private-material proof, raw-publication proof, or identity merge claims are published.",
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function claimBoundary() {
  return {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_api_key_purchase_mutation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_merge_or_replacement: "not_claimed",
  };
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
