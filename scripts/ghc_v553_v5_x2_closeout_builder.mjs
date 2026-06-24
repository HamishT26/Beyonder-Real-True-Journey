#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const phaseSlug = "v553-gmut-thos-v5-x2";
const sourceX1 = "v553-gmut-thos-v5-x1";
const nextX1 = "v553-gmut-thos-v6-x1";
const nextX1Lane = `${nextX1} with Arby and Cicero unless Hamish redirects`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const required = [
  `${phaseSlug}-safe-execution-reducer-v1.json`,
  `${phaseSlug}-skill-runner-use-board-v1.json`,
  `${phaseSlug}-web-journey-reflection-ledger-50-v1.json`,
  `${phaseSlug}-private-open-gate-rail-v1.json`,
  `${phaseSlug}-v6-arby-cicero-prep-card-v1.json`,
  `${phaseSlug}-safe-runner-orchestrator-v1.json`,
  `${phaseSlug}-open-gate-claim-linter-v1.json`,
];
const docs = Object.fromEntries(required.map((name) => [name, readOptional(name)]));
const missing = required.filter((name) => !docs[name]);
const openGap = required.filter((name) => docs[name] && !String(docs[name].overall_status || docs[name].status || "").startsWith("PASS"));
const pass = missing.length === 0 && openGap.length === 0;

const receipt = {
  artifact_type: "ghc_v553_v5_x2_closeout",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: pass ? "PASS_V553_V5_X2_CLOSED_V6_X1_READY" : "OPEN_GAP_V553_V5_X2_CLOSEOUT",
  latest_closed_phase: pass ? phaseSlug : sourceX1,
  latest_completed_x1_phase: sourceX1,
  latest_completed_x2_phase: pass ? phaseSlug : "v553-gmut-thos-v4-x2",
  next_active_phase: pass ? nextX1 : phaseSlug,
  next_x1_lane_after_x2: nextX1Lane,
  checks: {
    required_artifacts: required.length,
    missing_artifacts: missing.length,
    open_gap_artifacts: openGap.length,
    safe_runner_orchestrator: docs[`${phaseSlug}-safe-runner-orchestrator-v1.json`]?.overall_status || "missing",
    open_gate_linter: docs[`${phaseSlug}-open-gate-claim-linter-v1.json`]?.overall_status || "missing",
  },
  v6_arby_cicero_prep: {
    phase: nextX1,
    route: "ghc-arby-cicero-launch; Arby strict CLI plus Cicero recovered app-lane background supervision",
    target_counts: {
      safe: 15,
      candidate: 9,
      exact: 9,
      skills: 15,
      runners: 9,
      cleanup: 30,
    },
    private_ids_published: false,
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

writePair("closeout", receipt);
refreshBeacons(receipt);

process.stdout.write(JSON.stringify({
  status: receipt.overall_status,
  phase_slug: phaseSlug,
  next_active_phase: receipt.next_active_phase,
  missing: missing.length,
  open_gap: openGap.length,
}, null, 2) + "\n");
process.exit(pass ? 0 : 1);

function writePair(suffix, payload) {
  const base = `${phaseSlug}-${suffix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(
    path.join(tracesDir, `${base}.md`),
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
    doc.next_x1_lane_after_x2 = payload.next_x1_lane_after_x2;
    doc.goal_mode_status = "active_thread_goal_not_unattended_automation";
    doc.v553_v5_x2_closeout = {
      status: payload.overall_status,
      checks: payload.checks,
      next_active_phase: payload.next_active_phase,
      next_x1_lane_after_x2: payload.next_x1_lane_after_x2,
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

function renderBeaconMd(title, data, files) {
  return [
    `# ${title}`,
    "",
    `Status: ${data.status}`,
    `Current active phase: ${data.current_active_phase}`,
    `Latest closed phase: ${data.latest_closed_phase}`,
    `Latest completed x1: ${data.latest_completed_x1_phase}`,
    `Latest completed x2: ${data.latest_completed_x2_phase}`,
    `Next expected scope: ${data.next_expected_scope}`,
    `Next x1 lane after x2: ${data.next_x1_lane_after_x2}`,
    "",
    "## v553 v5 x2 Closeout",
    "",
    `- status: \`${data.v553_v5_x2_closeout?.status || "not_recorded"}\``,
    `- next active phase: \`${data.v553_v5_x2_closeout?.next_active_phase || "not_recorded"}\``,
    `- missing artifacts: \`${data.v553_v5_x2_closeout?.checks?.missing_artifacts ?? "not_recorded"}\``,
    `- open-gap artifacts: \`${data.v553_v5_x2_closeout?.checks?.open_gap_artifacts ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-100).map((item) => `- \`${item}\``),
    "",
    "## Boundary",
    "",
    "No raw transcripts, private route handles, callable IDs, local paths, screenshots, credentials, proof closures, legal/canon/deployment/account/API-key closures, private-material proof, raw-publication proof, or identity merge claims are published.",
    "",
  ].join("\n");
}

function readOptional(name) {
  try {
    return JSON.parse(fs.readFileSync(path.join(tracesDir, name), "utf8"));
  } catch {
    return null;
  }
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
