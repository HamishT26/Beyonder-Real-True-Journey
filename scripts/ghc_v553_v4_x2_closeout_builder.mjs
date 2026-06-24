#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v4-x2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  `${phaseSlug}-safe-execution-reducer-v1.json`,
  `${phaseSlug}-skill-runner-use-board-v1.json`,
  `${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
  `${phaseSlug}-private-open-gate-rail-v1.json`,
  `${phaseSlug}-v5-x1-lumen-prep-card-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  `${phaseSlug}-lane_state_dashboard-v1.json`,
  `${phaseSlug}-strict_cli_background_harvest-v1.json`,
  `${phaseSlug}-app-lane-completion-reconciler-v1.json`,
  `${phaseSlug}-open-gate-claim-linter-v1.json`,
];
const docs = Object.fromEntries(required.map((name) => [name, readOptional(name)]));
const missing = required.filter((name) => !docs[name]);
const openGap = required.filter((name) => docs[name] && !String(docs[name].overall_status || docs[name].status || "").startsWith("PASS"));
const pass = missing.length === 0 && openGap.length === 0;

const receipt = {
  artifact_type: "ghc_v553_v4_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V553_V4_X2_CLOSED_V5_X1_READY" : "OPEN_GAP_V553_V4_X2_CLOSEOUT",
  latest_closed_phase: pass ? phaseSlug : "v553-gmut-thos-v4-x1",
  latest_completed_x1_phase: "v553-gmut-thos-v4-x1",
  latest_completed_x2_phase: pass ? phaseSlug : "v553-gmut-thos-v3-x2",
  next_active_phase: pass ? "v553-gmut-thos-v5-x1" : phaseSlug,
  next_x2_scope: "v553-gmut-thos-v5-x2",
  next_x1_lane_after_x2: "v553-gmut-thos-v6-x1 with Arby and Cicero unless Hamish redirects",
  checks: {
    required_artifacts: required.length,
    missing_artifacts: missing.length,
    open_gap_artifacts: openGap.length,
    safe_runner_orchestrator: docs[`${phaseSlug}-safe-runner-orchestrator-v1.json`]?.overall_status || "missing",
    open_gate_linter: docs[`${phaseSlug}-open-gate-claim-linter-v1.json`]?.overall_status || "missing",
  },
  v5_lumen_prep: {
    phase: "v553-gmut-thos-v5-x1",
    route: "ghc-lumen-launch; Browser live send only after explicit authorization",
    target_counts: {
      safe: 50,
      candidate: 30,
      exact: 20,
      blocked: 10,
      skills: 20,
      runners: 10,
      cleanup: 30,
    },
  },
  publication_boundary: {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    local_absolute_paths_published: false,
    screenshots_published: false,
    credentials_published: false,
  },
  claim_boundary: {
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    identity_merge_or_replacement: "not_claimed",
  },
};

writePair(`${phaseSlug}-closeout`, receipt);
refreshState(receipt);
process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: receipt.next_active_phase,
  missing: missing.length,
  open_gap: openGap.length,
}, null, 2) + "\n");
process.exit(pass ? 0 : 1);

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
  } catch {
    return null;
  }
}

function writePair(baseName, payload) {
  fs.mkdirSync(tracesDir, { recursive: true });
  fs.writeFileSync(path.join(tracesDir, `${baseName}-v1.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(
    path.join(tracesDir, `${baseName}-v1.md`),
    [
      `# ${phaseSlug} Closeout`,
      "",
      `Status: \`${payload.overall_status}\``,
      `Next active phase: \`${payload.next_active_phase}\``,
      `Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``,
      "",
      `- required artifacts: \`${payload.checks.required_artifacts}\``,
      `- missing artifacts: \`${payload.checks.missing_artifacts}\``,
      `- open-gap artifacts: \`${payload.checks.open_gap_artifacts}\``,
      "",
      "No raw transcripts, private route handles, callable IDs, local paths, screenshots, credentials, proof closures, or identity merge claims are published.",
      "",
    ].join("\n"),
    "utf8",
  );
}

function refreshState(payload) {
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
    doc.next_x2_scope = payload.next_x2_scope;
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v553_v4_x2_closeout = {
      status: payload.overall_status,
      checks: payload.checks,
      next_active_phase: payload.next_active_phase,
      next_x1_lane_after_x2: payload.next_x1_lane_after_x2,
    };
    doc.current_lookup_files = [...new Set([...(doc.current_lookup_files || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
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
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
