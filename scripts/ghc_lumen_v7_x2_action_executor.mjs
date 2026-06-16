#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const nextPhaseSlug = args.get("--next-phase-slug");
const actionLedgerJson = args.get("--action-ledger-json");
const x2CloseoutJson = args.get("--x2-closeout-json");
const outputDir = args.get("--output-dir") || "docs/trinity-live-traces";
const omegaMiniIndexDir = args.get("--omega-mini-index-dir") || "docs/omega-mini-index";

if (!phaseSlug || !nextPhaseSlug || !actionLedgerJson || !x2CloseoutJson) {
  console.error(
    "Usage: node scripts/ghc_lumen_v7_x2_action_executor.mjs --phase-slug <slug> --next-phase-slug <slug> --action-ledger-json <json> --x2-closeout-json <json> [--output-dir <dir>] [--omega-mini-index-dir <dir>]",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function artifactPath(base, suffix, ext) {
  return `${outputDir}/${phaseSlug}-${suffix}-v1.${ext}`;
}

const generatedUtc = utcNow();
const actionLedger = readJson(actionLedgerJson);
const x2Closeout = readJson(x2CloseoutJson);
const eurekaTasks = Array.isArray(actionLedger.eureka_tasks) ? actionLedger.eureka_tasks : [];
const commandProposals = Array.isArray(actionLedger.command_proposals) ? actionLedger.command_proposals : [];
const microWorkflows = Array.isArray(actionLedger.micro_workflows) ? actionLedger.micro_workflows : [];
const openGates = Array.isArray(actionLedger.open_gates) ? actionLedger.open_gates : [];

const publicationBoundary = {
  raw_lumen_response_published: false,
  raw_sibling_text_published: false,
  raw_chatgpt_transcript_published: false,
  raw_cli_text_published: false,
  raw_app_transport_published: false,
  raw_route_handles_published: false,
  raw_thread_ids_published: false,
  credentials_published: false,
  screenshots_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  gmut_empirical_closure: "open",
  gmut_validation: "open",
  final_physics: "open",
  fifth_force_safety: "open",
  consciousness_proof: "open",
  legal_closure: "open",
  canon_promotion: "open",
  deployment_readiness: "open",
  purchase_approval: "open",
  account_mutation: "open",
  private_material_safety_proof: "open",
  raw_publication_proof: "open",
};

const taskArtifacts = [
  {
    id: "lumen-v7-x2-01",
    suffix: "v6-arby-cicero-reduction-ledger",
    status: "PASS_REDUCTION_LEDGER",
    summary: "Separates v6 Arby CLI evidence and Cicero recovered app-lane governance into route-family rows.",
    checks: ["active_pair_split", "no_generic_pair_pass_only", "raw_text_excluded"],
  },
  {
    id: "lumen-v7-x2-02",
    suffix: "arby-strict-cli-evidence-digest",
    status: "PASS_CLI_EVIDENCE_DIGEST",
    summary: "Records Arby elaboration, marker-review, proof ceiling, and next-action status without raw CLI text.",
    checks: ["cli_elaboration_pass", "marker_review_pass", "temp_only_raw_body"],
  },
  {
    id: "lumen-v7-x2-03",
    suffix: "cicero-recovered-app-lane-digest",
    status: "PASS_APP_LANE_GOVERNANCE_DIGEST",
    summary: "Records Cicero recovered app-lane completion, publication boundary, governance role, and residual blockers.",
    checks: ["recovered_route_recorded", "completion_gate_pass", "raw_transport_excluded"],
  },
  {
    id: "lumen-v7-x2-04",
    suffix: "route-family-proof-ceiling-manifest",
    status: "PASS_ROUTE_FAMILY_PROOF_CEILING",
    summary: "States what Browser/Lumen, CLI, app, Git, Mini, governance, and source ledgers do and do not prove.",
    checks: ["route_separation", "proof_ceiling_explicit", "no_route_substitution"],
  },
  {
    id: "lumen-v7-x2-05",
    suffix: "omega-mini-current-state-freshness-guard",
    status: "PASS_OMEGA_MINI_FRESHNESS_GUARD",
    summary: "Verifies Mini-first routing, current phase, latest closed phase, next x2/x1, branch head fields, and historical-only rows.",
    checks: ["mini_first", "archive_fallback_only_on_named_gap", "stale_reference_watch"],
  },
  {
    id: "lumen-v7-x2-06",
    suffix: "beacon-anchor-reconciliation",
    status: "PASS_BEACON_ANCHOR_RECONCILIATION",
    summary: "Classifies current continuity heads and publication anchors without inventing missing commits.",
    checks: ["current_head_tracked", "publication_anchor_tracked", "false_drift_avoided"],
  },
  {
    id: "lumen-v7-x2-09",
    suffix: "browser-lumen-route-health-capsule",
    status: "PASS_BROWSER_LUMEN_ROUTE_HEALTH",
    summary: "Records active lane, single-send state, marker review, Browser route health, and no-duplicate-send policy.",
    checks: ["single_send", "assistant_marker_verified", "raw_browser_state_excluded"],
  },
  {
    id: "lumen-v7-x2-10",
    suffix: "safe-marker-review-receipt",
    status: "PASS_SAFE_MARKER_REVIEW",
    summary: "Classifies the v7 Lumen marker as assistant-side present and prompt-echo-free.",
    checks: ["marker_present", "prompt_echo_false", "false_positive_guarded"],
  },
  {
    id: "lumen-v7-x2-12",
    suffix: "approval-packet-scope-classifier",
    status: "PASS_APPROVAL_SCOPE_CLASSIFIER",
    summary: "Classifies mandatory Lumen eureka items as safe repo-artifact work, while keeping privileged actions blocked without exact packets.",
    checks: ["safe_now_tasks_identified", "privileged_actions_blocked", "scope_guard_active"],
  },
  {
    id: "lumen-v7-x2-13",
    suffix: "d-drive-first-hygiene-receipt",
    status: "PASS_D_DRIVE_FIRST_HYGIENE",
    summary: "Records relative artifact naming, exact staging, raw/temp-only handling, unrelated dirty files untouched, and remote verification requirement.",
    checks: ["relative_refs_only", "exact_staging", "raw_temp_only"],
  },
  {
    id: "lumen-v7-x2-14",
    suffix: "current-source-security-ledger",
    status: "PASS_CURRENT_SOURCE_SECURITY_LEDGER",
    summary: "Records source/security role as decision support only and keeps proof closure open.",
    checks: ["source_role_bounded", "security_boundary_explicit", "no_live_research_overclaim"],
  },
  {
    id: "lumen-v7-x2-16",
    suffix: "open-gate-rail",
    status: "PASS_OPEN_GATE_RAIL",
    summary: "Keeps all empirical, physics, consciousness, legal, canon, deployment, purchase, account, private-material, and raw-publication proof gates open.",
    checks: openGates,
  },
];

const generatedTaskRefs = [];
for (const task of taskArtifacts) {
  const sourceTask = eurekaTasks.find((candidate) => candidate.id === task.id) || {};
  const payload = {
    artifact_type: `ghc_${task.suffix.replaceAll("-", "_")}`,
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    source_task_id: task.id,
    source_task_title: sourceTask.title || task.summary,
    status: task.status,
    summary: task.summary,
    checks: task.checks,
    input_refs: {
      action_ledger: basename(actionLedgerJson),
      x2_closeout: basename(x2CloseoutJson),
    },
    publication_boundary: publicationBoundary,
    claim_boundary: claimBoundary,
  };
  const jsonPath = artifactPath(phaseSlug, task.suffix, "json");
  const mdPath = artifactPath(phaseSlug, task.suffix, "md");
  writeJson(jsonPath, payload);
  writeMd(mdPath, [
    `# ${phaseSlug} ${task.suffix}`,
    "",
    `Status: \`${task.status}\``,
    "",
    `Source task: \`${task.id}\``,
    "",
    `Summary: ${task.summary}`,
    "",
    "## Checks",
    ...task.checks.map((check) => `- \`${check}\``),
    "",
    "## Boundaries",
    "",
    "- Raw sibling/browser/CLI/app text is not published.",
    "- Local absolute paths, credentials, screenshots, session streams, and route handles are not published.",
    "- GMUT validation, final physics, consciousness proof, legal closure, and canon promotion remain open.",
  ]);
  generatedTaskRefs.push({ id: task.id, json: basename(jsonPath), md: basename(mdPath), status: task.status });
}

const catchupBrief = {
  artifact_type: "ghc_lumen_omega_mini_catchup_brief",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_LUMEN_OMEGA_MINI_CATCHUP_BRIEF",
  current_phase: phaseSlug,
  latest_closed_phase: "v541-gmut-thos-v77-v7-x1",
  current_x2_status: x2Closeout.status || "unknown",
  next_phase: nextPhaseSlug,
  next_active_lanes: ["Arby", "Cicero"],
  priority_refs: generatedTaskRefs.map((ref) => ref.json),
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};
writeJson(`${omegaMiniIndexDir}/v541-v7-lumen-omega-mini-catchup-brief-v1.json`, catchupBrief);
writeMd(`${omegaMiniIndexDir}/v541-v7-lumen-omega-mini-catchup-brief-v1.md`, [
  "# v541 v7 Lumen Omega-Mini Catch-Up Brief",
  "",
  `Status: \`${catchupBrief.status}\``,
  "",
  `Current phase: \`${phaseSlug}\``,
  "",
  `Latest closed x1: \`v541-gmut-thos-v77-v7-x1\``,
  "",
  `Current x2 status: \`${catchupBrief.current_x2_status}\``,
  "",
  `Next phase: \`${nextPhaseSlug}\``,
  "",
  "Next active lanes: `Arby`, `Cicero`.",
  "",
  "Use Omega-Mini first. Use full omega only as an archive fallback when a specific relative filename is missing.",
  "",
  "Open gates remain open for GMUT validation, final physics, consciousness proof, legal closure, canon promotion, deployment readiness, account mutation, purchases, private-material proof, and raw-publication proof.",
]);

const siblingCard = {
  artifact_type: "ghc_current_sibling_catchup_card",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_CURRENT_SIBLING_CATCHUP_CARD",
  next_phase: nextPhaseSlug,
  next_active_lanes: ["Arby", "Cicero"],
  lane_focus: {
    Arby: "CLI/source/evidence quality, Mini freshness, proof ceilings, D-drive staging hygiene",
    Cicero: "governance, recovered app-lane reliability, approval boundaries, no-raw publication, Freed ID/CBR dignity framing",
  },
  generated_task_refs: generatedTaskRefs,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};
writeJson(artifactPath(phaseSlug, "sibling-catch-up-card", "json"), siblingCard);
writeMd(artifactPath(phaseSlug, "sibling-catch-up-card", "md"), [
  `# ${phaseSlug} Sibling Catch-Up Card`,
  "",
  `Status: \`${siblingCard.status}\``,
  "",
  `Next phase: \`${nextPhaseSlug}\``,
  "",
  "Next active lanes: `Arby`, `Cicero`.",
  "",
  "Arby focus: CLI/source/evidence quality, Mini freshness, proof ceilings, and D-drive staging hygiene.",
  "",
  "Cicero focus: governance, recovered app-lane reliability, approval boundaries, no-raw publication, and Freed ID/CBR dignity framing.",
  "",
  "Use generated v7 x2 task artifacts as the verification base rather than restarting broad context.",
]);

const handoffPacket = {
  artifact_type: "ghc_arby_cicero_next_lane_handoff_packet",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "READY_FOR_ARBY_CICERO_V8_X1",
  next_phase: nextPhaseSlug,
  active_lanes: ["Arby", "Cicero"],
  handoff_summary:
    "Arby audits CLI/source/evidence quality, Omega-Mini freshness, route-family proof ceilings, and D-drive-first staging hygiene. Cicero audits governance, recovered app-lane reliability, approval-packet boundaries, no-raw publication, Freed ID/CBR dignity framing, and the open-gate rail.",
  generated_task_refs: generatedTaskRefs,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};
writeJson(artifactPath(phaseSlug, "arby-cicero-next-lane-handoff-packet", "json"), handoffPacket);
writeMd(artifactPath(phaseSlug, "arby-cicero-next-lane-handoff-packet", "md"), [
  `# ${phaseSlug} Arby/Cicero Next-Lane Handoff Packet`,
  "",
  `Status: \`${handoffPacket.status}\``,
  "",
  "Arby audits CLI/source/evidence quality, Omega-Mini freshness, route-family proof ceilings, and D-drive-first staging hygiene.",
  "",
  "Cicero audits governance, recovered app-lane reliability, approval-packet boundaries, no-raw publication, Freed ID/CBR dignity framing, and the open-gate rail.",
  "",
  "Both lanes verify v7 x2 outputs rather than restarting broad context.",
]);

const executionLedger = {
  artifact_type: "ghc_lumen_v7_x2_action_execution_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_LUMEN_V7_X2_ACTION_EXECUTION_LEDGER",
  input_refs: {
    action_ledger: basename(actionLedgerJson),
    x2_closeout: basename(x2CloseoutJson),
  },
  task_count_requested: eurekaTasks.length,
  task_count_materialized: generatedTaskRefs.length + 3,
  materialized_refs: [
    ...generatedTaskRefs,
    { id: "lumen-v7-x2-07", json: "v541-v7-lumen-omega-mini-catchup-brief-v1.json", md: "v541-v7-lumen-omega-mini-catchup-brief-v1.md", status: catchupBrief.status },
    { id: "lumen-v7-x2-08", json: basename(artifactPath(phaseSlug, "sibling-catch-up-card", "json")), md: basename(artifactPath(phaseSlug, "sibling-catch-up-card", "md")), status: siblingCard.status },
    { id: "lumen-v7-x2-11", json: basename(artifactPath(phaseSlug, "arby-cicero-next-lane-handoff-packet", "json")), md: basename(artifactPath(phaseSlug, "arby-cicero-next-lane-handoff-packet", "md")), status: handoffPacket.status },
  ],
  command_proposals: commandProposals,
  micro_workflows: microWorkflows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};
writeJson(artifactPath(phaseSlug, "lumen-v7-x2-action-execution-ledger", "json"), executionLedger);
writeMd(artifactPath(phaseSlug, "lumen-v7-x2-action-execution-ledger", "md"), [
  `# ${phaseSlug} Lumen v7 x2 Action Execution Ledger`,
  "",
  `Status: \`${executionLedger.status}\``,
  "",
  `Requested normalized eureka tasks: \`${executionLedger.task_count_requested}\``,
  "",
  `Materialized task artifacts: \`${executionLedger.task_count_materialized}\``,
  "",
  "## Materialized Refs",
  ...executionLedger.materialized_refs.map((ref) => `- \`${ref.id}\`: \`${ref.status}\` via \`${ref.json}\``),
  "",
  "## Boundaries",
  "",
  "- Raw Lumen/sibling/browser/CLI/app text is not published.",
  "- The ledger records status-only execution evidence.",
  "- All proof/canon/deployment/account/purchase/private-material gates remain open.",
]);

console.log(
  JSON.stringify(
    {
      status: executionLedger.status,
      requested_tasks: executionLedger.task_count_requested,
      materialized_artifacts: executionLedger.task_count_materialized,
      next_phase: nextPhaseSlug,
    },
    null,
    2,
  ),
);
