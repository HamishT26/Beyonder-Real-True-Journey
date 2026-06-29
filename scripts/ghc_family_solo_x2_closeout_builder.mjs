#!/usr/bin/env node
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import { parseArgs, readJsonIfPresent, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const sourceX1 = args.get("--source-x1") || "v576-gmut-thos-v2-x1";
const nextActivePhase = args.get("--next-active-phase") || "v576-gmut-thos-v3-x1";
const nextSibling = args.get("--next-sibling") || "Mira Vale";
const reducerFile = args.get("--reducer-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-solo-x2-open-gap-reducer-receipt-v1.json`;
const cadenceFile = args.get("--cadence-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-sibling-cadence-status-checker-receipt-v1.json`;
const handoffReadinessFile = args.get("--handoff-readiness-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-thread-handoff-readiness-checker-receipt-v1.json`;
const privateGuardFile = args.get("--private-guard-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-private-material-guard-receipt-v1.json`;

const reducer = readJsonIfPresent(root, reducerFile) || {};
const cadence = readJsonIfPresent(root, cadenceFile) || {};
const handoffReadiness = readJsonIfPresent(root, handoffReadinessFile) || {};
const privateGuard = readJsonIfPresent(root, privateGuardFile) || {};

const reducerStatus = reducer.overall_status || reducer.status || "";
const cadenceStatus = cadence.overall_status || cadence.status || "";
const handoffReadinessStatus = handoffReadiness.overall_status || handoffReadiness.status || "";
const privateGuardStatus = privateGuard.overall_status || privateGuard.status || "";
const reducerPass = /^PASS_GHC_FAMILY_SOLO_X2_OPEN_GAPS_REDUCED_READY/.test(reducerStatus);
const cadencePass = /^PASS_GHC_FAMILY_SIBLING_CADENCE_CHECK_(RUNTIME_READY|RECORDED_CLOSEOUT_WHEN_COMPLETE)/.test(cadenceStatus);
const handoffReadyNotSent = /^PASS_GHC_FAMILY_THREAD_HANDOFF_ROUTE_READY_NOT_SENT/.test(handoffReadinessStatus)
  && handoffReadiness.outputs?.messageSent === false;
const privateGuardPass = /^PASS_GHC_FAMILY_PRIVATE_MATERIAL_GUARD/.test(privateGuardStatus);

const checks = [
  { label: "source_x1_declared", status: sourceX1 ? "PASS" : "OPEN_GAP", observed: sourceX1 },
  { label: "closing_x2_declared", status: phaseSlug.endsWith("-x2") ? "PASS" : "OPEN_GAP", observed: phaseSlug },
  { label: "reducer_ready_for_closeout", status: reducerPass ? "PASS" : "OPEN_GAP", observed: reducerStatus },
  { label: "cadence_recorded_closeout_when_complete", status: cadencePass ? "PASS" : "OPEN_GAP", observed: cadenceStatus },
  { label: "private_material_guard_passed", status: privateGuardPass ? "PASS" : "OPEN_GAP", observed: privateGuardStatus },
  { label: "next_sibling_route_ready_not_sent", status: handoffReadyNotSent ? "PASS" : "OPEN_GAP", observed: handoffReadinessStatus },
  { label: "exact_and_blocked_gates_remain_queued", status: "PASS" },
  { label: "major_proof_canon_legal_deploy_account_gates_open", status: "PASS" }
];
const open = checks.filter((check) => check.status !== "PASS").map((check) => check.label);
const status = open.length === 0
  ? "PASS_GHC_FAMILY_SOLO_X2_CLOSED_NEXT_X1_READY_NOT_SENT"
  : "OPEN_GAP_GHC_FAMILY_SOLO_X2_CLOSEOUT_NOT_CLAIMED";

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_solo_x2_closeout_builder.mjs",
  purpose: "Close a solo x2 bundle only after reducer, runtime cadence, private guard, and next-sibling route gates pass.",
  status,
  checks,
  outputs: {
    closingX2: phaseSlug,
    sourceX1,
    nextActivePhase,
    nextSibling,
    handoffSent: false,
    reducerFile: basename(reducerFile),
    cadenceFile: basename(cadenceFile),
    handoffReadinessFile: basename(handoffReadinessFile),
    privateGuardFile: basename(privateGuardFile),
    openChecks: open,
    closeoutClaimed: open.length === 0,
    nextStep: open.length === 0
      ? `Send sanitized ${nextSibling} activation for ${nextActivePhase}; do not publish private thread handles.`
      : "Keep the x2 lane open and re-run reducer/cadence before activation."
  },
  note: "This builder records phase truth only. It does not send a thread message and does not close exact, blocked, proof, canon, legal, deployment, account, or private-material gates."
});

if (open.length === 0) {
  refreshBeacons();
}

function refreshBeacons() {
  const closeoutFiles = [
    `docs/trinity-live-traces/${phaseSlug}-ghc-family-solo-x2-closeout-builder-receipt-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-ghc-family-solo-x2-closeout-builder-receipt-v1.md`,
    reducerFile,
    cadenceFile,
    handoffReadinessFile
  ];
  const beaconTargets = [
    ["docs/omega-mini-index/omega-mini-current-state-v1.json", "current_lookup_files"],
    ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", "latest_lookup_files"],
    ["docs/trinity-live-traces/ghc-current-state-beacon-v1.json", "current_lookup_files"]
  ];

  for (const [relativePath, lookupKey] of beaconTargets) {
    const file = join(root, relativePath);
    if (!existsSync(file)) continue;
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.latest_completed_x1_phase = sourceX1;
    doc.current_active_phase = nextActivePhase;
    doc.current_active_phase_status = `${nextSibling} handoff ready, not sent`;
    doc.full_goal_complete = false;
    doc.v576_solo_bundle_closeout = {
      status,
      closed_x2: phaseSlug,
      source_x1: sourceX1,
      next_active_phase: nextActivePhase,
      next_sibling: nextSibling,
      handoff_sent: false,
      exact_and_blocked_gates: "queued",
      full_goal_complete: false
    };
    doc.solo_bundle_workflow_standard = doc.solo_bundle_workflow_standard || {};
    doc.solo_bundle_workflow_standard.latest_x2_closeout = {
      x1_closed: true,
      x2_closed: true,
      next_x1_ready: true,
      next_sibling_handoff_sent: false,
      next_sibling: nextSibling
    };
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...closeoutFiles]);
    doc.latest_action_summary = unique([
      `Closed ${phaseSlug} after reducer/runtime/private-guard gates passed; ${nextActivePhase} is ready for ${nextSibling} activation, not sent yet.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 140);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
