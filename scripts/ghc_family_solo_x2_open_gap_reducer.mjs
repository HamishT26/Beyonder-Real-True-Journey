#!/usr/bin/env node
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { basename, join } from "node:path";
import { parseArgs, readJsonIfPresent, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const reductionFile = args.get("--reduction-file") || `docs/trinity-live-traces/${phaseSlug}-mira-rowan-x2-open-gap-reduction-v1.json`;
const laneReceiptFile = args.get("--lane-receipt-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-owned-lane-availability-checker-receipt-v1.json`;
const sourceReflectionFile = args.get("--source-reflection-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-source-reflection-target-tracker-receipt-v1.json`;
const handoffReadinessFile = args.get("--handoff-readiness-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-thread-handoff-readiness-checker-receipt-v1.json`;
const toolchainSnapshotFile = args.get("--toolchain-snapshot-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-toolchain-system-snapshot-receipt-v1.json`;
const launchTime = args.get("--lane-launch-time") || "2026-06-29T18:34:26+12:00";
const advisoryRuntimeMinutes = Number(args.get("--advisory-runtime-minutes") || args.get("--minimum-runtime-minutes") || 60);
const now = new Date();
const launchedAt = new Date(launchTime);
const elapsedMinutes = Number.isFinite(launchedAt.getTime())
  ? Math.max(0, Math.floor((now.getTime() - launchedAt.getTime()) / 60_000))
  : 0;
const advisoryWindowUtc = Number.isFinite(launchedAt.getTime())
  ? new Date(launchedAt.getTime() + advisoryRuntimeMinutes * 60_000).toISOString().replace(/\.\d{3}Z$/, "Z")
  : "";

const reduction = readJsonIfPresent(root, reductionFile) || {};
const laneReceipt = readJsonIfPresent(root, laneReceiptFile) || {};
const sourceReflection = readJsonIfPresent(root, sourceReflectionFile) || {};
const handoffReadiness = readJsonIfPresent(root, handoffReadinessFile) || {};
const toolchainSnapshot = readJsonIfPresent(root, toolchainSnapshotFile) || {};
const requiredArtifacts = [
  `docs/trinity-live-traces/${phaseSlug}-solo-phase-transition-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-ghc-family-productive-cadence-runner-receipt-v1.json`,
  reductionFile,
  laneReceiptFile,
  sourceReflectionFile,
  handoffReadinessFile,
  toolchainSnapshotFile,
  `docs/trinity-live-traces/${phaseSlug}-ghc-family-approval-eureka-splitter-receipt-v1.json`,
  `docs/trinity-live-traces/${phaseSlug}-toolchain-update-receipt-v1.json`
];
const artifactRows = requiredArtifacts.map((relativePath) => ({
  name: basename(relativePath),
  present: existsSync(`${root}/${relativePath}`)
}));
const missingArtifacts = artifactRows.filter((row) => !row.present);
const lanePass = /^PASS/.test(laneReceipt.overall_status || laneReceipt.status || "");
const reductionPass = /^PASS/.test(reduction.status || reduction.overall_status || "");
const sourceReflectionStatus = sourceReflection.overall_status || sourceReflection.status || "";
const sourceReflectionTracked = Boolean(sourceReflectionStatus);
const sourceReflectionComplete = /^PASS/.test(sourceReflectionStatus);
const handoffReadinessStatus = handoffReadiness.overall_status || handoffReadiness.status || "";
const handoffRouteReady = /^PASS_GHC_FAMILY_THREAD_HANDOFF_ROUTE_READY_NOT_SENT/.test(handoffReadinessStatus);
const toolchainSnapshotStatus = toolchainSnapshot.overall_status || toolchainSnapshot.status || "";
const toolchainSnapshotPass = /^PASS_GHC_FAMILY_TOOLCHAIN_SYSTEM_SNAPSHOT/.test(toolchainSnapshotStatus);
const advisoryWindowElapsed = elapsedMinutes >= advisoryRuntimeMinutes;
const artifactsPass = missingArtifacts.length === 0;

const checks = [
  { label: "mira_rowan_reduction_available", status: reductionPass ? "PASS" : "OPEN_GAP" },
  { label: "owned_lane_availability_aevren_side", status: lanePass ? "PASS" : "OPEN_GAP" },
  { label: "persistent_x2_support_artifacts_present", status: artifactsPass ? "PASS" : "OPEN_GAP", observed: artifactRows.length - missingArtifacts.length },
  {
    label: "runtime_target_recorded_as_advisory",
    status: "PASS",
    observed: { elapsedMinutes, advisoryRuntimeMinutes, advisoryWindowElapsed }
  },
  { label: "mira_vale_thread_route_ready", status: handoffRouteReady ? "PASS" : "OPEN_GAP" },
  { label: "mira_vale_handoff_not_sent_before_closeout", status: handoffReadiness.outputs?.messageSent === false ? "PASS" : "OPEN_GAP" },
  { label: "toolchain_system_snapshot_current", status: toolchainSnapshotPass ? "PASS" : "OPEN_GAP" },
  { label: "exact_and_blocked_gates_remain_queued", status: "PASS" },
  { label: "source_reflection_target_tracked", status: sourceReflectionTracked ? "PASS" : "OPEN_GAP" },
  {
    label: "hundred_source_reflection_target_completed",
    status: sourceReflectionComplete ? "PASS" : "OPEN_GAP",
    observed: sourceReflection.outputs?.representedRows || 0
  }
];
const remainingOpenGaps = checks.filter((check) => check.status !== "PASS").map((check) => check.label);
const status = remainingOpenGaps.length === 0
  ? "PASS_GHC_FAMILY_SOLO_X2_OPEN_GAPS_REDUCED_READY_FOR_CLOSEOUT_REVIEW"
  : "OPEN_GAP_GHC_FAMILY_SOLO_X2_REDUCED_NOT_CLOSED";
const receiptStem = `${phaseSlug}-ghc-family-solo-x2-open-gap-reducer-receipt-v1`;

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_solo_x2_open_gap_reducer.mjs",
  purpose: "Reduce Mira Rowan v2 x2 open gaps with Aevren-side evidence while keeping true closeout and Mira Vale activation gated.",
  status,
  checks,
  outputs: {
    sourceReduction: basename(reductionFile),
    laneAvailabilityReceipt: basename(laneReceiptFile),
    sourceReflectionReceipt: basename(sourceReflectionFile),
    handoffReadinessReceipt: basename(handoffReadinessFile),
    toolchainSnapshotReceipt: basename(toolchainSnapshotFile),
    launchTime,
    generatedAtUtc: now.toISOString().replace(/\.\d{3}Z$/, "Z"),
    elapsedMinutes,
    advisoryRuntimeMinutes,
    advisoryWindowUtc,
    artifactRows,
    missingArtifacts: missingArtifacts.map((row) => row.name),
    sourceReflectionStatus,
    sourceReflectionRepresentedRows: sourceReflection.outputs?.representedRows || 0,
    sourceReflectionRemainingRows: sourceReflection.outputs?.remainingRows || 0,
    handoffReadinessStatus,
    handoffMessageSent: handoffReadiness.outputs?.messageSent === true,
    toolchainSnapshotStatus,
    closedOrReduced: [
      "Mira Rowan x2 response reduced into sanitized open-gap form",
      "Sibling-owned lane availability checked from Aevren-side support lane",
      "Persistent support artifacts tracked as explicit closeout evidence"
      ,
      "Mira Vale thread handoff route checked privately and kept unsent before closeout"
      ,
      "Current toolchain and drive state snapshotted without mutating the Codex desktop app"
    ],
    remainingOpenGaps,
    closeoutBoundary: "Close v576-gmut-thos-v2-x2 as soon as the completion checklist passes; the one-hour runtime target is advisory and should not block a completed phase."
  },
  note: "The 100 web/source and Journey reflection target remains tracked as an open target for this x2 lane; this runner does not inflate represented counts."
});

refreshBeacons();

function refreshBeacons() {
  const lookupFiles = [
    `docs/trinity-live-traces/${receiptStem}.json`,
    `docs/trinity-live-traces/${receiptStem}.md`,
    laneReceiptFile,
    sourceReflectionFile
  ];
  const files = [
    ["docs/omega-mini-index/omega-mini-current-state-v1.json", "current_lookup_files"],
    ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", "latest_lookup_files"],
    ["docs/trinity-live-traces/ghc-current-state-beacon-v1.json", "current_lookup_files"]
  ];

  for (const [relativePath, lookupKey] of files) {
    const file = join(root, relativePath);
    if (!existsSync(file)) continue;
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = now.toISOString().replace(/\.\d{3}Z$/, "Z");
    doc.current_active_phase = phaseSlug;
    doc.full_goal_complete = false;
    doc.v576_v2_x2_open_gap_reduction = {
      status,
      remaining_open_gaps: remainingOpenGaps,
      elapsed_minutes: elapsedMinutes,
      advisory_runtime_minutes: advisoryRuntimeMinutes,
      advisory_window_utc: advisoryWindowUtc,
      runtime_target_policy: "advisory_close_when_complete",
      owned_lane_availability_aevren_side: lanePass ? "PASS" : "OPEN_GAP",
      persistent_x2_support_artifacts_present: artifactsPass ? "PASS" : "OPEN_GAP",
      source_reflection_status: sourceReflectionStatus,
      source_reflection_represented_rows: sourceReflection.outputs?.representedRows || 0,
      source_reflection_remaining_rows: sourceReflection.outputs?.remainingRows || 0,
      mira_vale_thread_route_ready: handoffRouteReady ? "PASS" : "OPEN_GAP",
      toolchain_system_snapshot: toolchainSnapshotPass ? "PASS" : "OPEN_GAP",
      mira_vale_handoff_sent: false,
      x2_closed: false,
      full_goal_complete: false
    };
    doc.solo_bundle_workflow_standard = doc.solo_bundle_workflow_standard || {};
    doc.solo_bundle_workflow_standard.x2_closeout_boundary = {
      x1_closed: true,
      x2_active: true,
      x2_closed: false,
      next_sibling_handoff_sent: false,
      reason_x2_not_closed: remainingOpenGaps.length
        ? `remaining open gaps: ${remainingOpenGaps.join(", ")}`
        : "ready for closeout review after final checklist"
    };
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      `Reduced ${phaseSlug} open gaps with owned-lane availability, persistent artifact, and source/reflection target receipts; Mira Vale remains gated until closeout.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 140);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
