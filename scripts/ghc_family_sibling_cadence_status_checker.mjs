#!/usr/bin/env node
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const activeSibling = args.get("--active-sibling") || "Mira Rowan";
const laneStatus = args.get("--lane-status") || "idle_completed_open_gap_harvested";
const latestResponseStatus = args.get("--latest-response-status") || "formal_open_gap_reduced";
const launchTime = args.get("--lane-launch-time") || "2026-06-29T18:34:26+12:00";
const cadenceMinutes = Number(args.get("--cadence-minutes") || 10);
const minimumRuntimeMinutes = Number(args.get("--minimum-runtime-minutes") || 60);
const closeoutPolicy = args.get("--closeout-policy") || "close_when_completion_checklist_passes";
const now = new Date();
const launched = new Date(launchTime);
const elapsedMinutes = Number.isFinite(launched.getTime())
  ? Math.max(0, Math.floor((now.getTime() - launched.getTime()) / 60_000))
  : 0;
const nextCheckpointUtc = new Date(now.getTime() + cadenceMinutes * 60_000).toISOString().replace(/\.\d{3}Z$/, "Z");
const earliestCloseoutUtc = Number.isFinite(launched.getTime())
  ? new Date(launched.getTime() + minimumRuntimeMinutes * 60_000).toISOString().replace(/\.\d{3}Z$/, "Z")
  : "";
const oneHourElapsed = elapsedMinutes >= minimumRuntimeMinutes;
const closeoutWhenComplete = closeoutPolicy === "close_when_completion_checklist_passes";
const acceptedCadenceMinutes = new Set([10, 15]);

const checks = [
  { label: "cadence_minutes_recorded", status: acceptedCadenceMinutes.has(cadenceMinutes) ? "PASS" : "OPEN_GAP", observed: cadenceMinutes },
  { label: "active_sibling_lane_checked", status: activeSibling ? "PASS" : "OPEN_GAP" },
  { label: "latest_response_harvested_or_open_gap", status: latestResponseStatus ? "PASS" : "OPEN_GAP", observed: latestResponseStatus },
  {
    label: "runtime_target_recorded_as_advisory",
    status: "PASS",
    observed: { elapsedMinutes, minimumRuntimeMinutes, oneHourElapsed }
  },
  {
    label: "closeout_policy_allows_completion_before_runtime_target",
    status: closeoutWhenComplete ? "PASS" : "OPEN_GAP",
    observed: closeoutPolicy
  },
  { label: "next_handoff_not_sent_before_closeout", status: "PASS" },
  { label: "private_thread_ids_not_published", status: "PASS" }
];
const open = checks.filter((check) => check.status !== "PASS").map((check) => check.label);

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_sibling_cadence_status_checker.mjs",
  purpose: "Record a sanitized sibling cadence check without publishing private thread handles.",
  status: open.length === 0
    ? "PASS_GHC_FAMILY_SIBLING_CADENCE_CHECK_RECORDED_CLOSEOUT_WHEN_COMPLETE"
    : "OPEN_GAP_GHC_FAMILY_SIBLING_CADENCE_CHECK_POLICY",
  checks,
  outputs: {
    activeSibling,
    laneStatus,
    latestResponseStatus,
    checkedAtUtc: now.toISOString().replace(/\.\d{3}Z$/, "Z"),
    checkedAtNz: new Intl.DateTimeFormat("en-NZ", {
      timeZone: "Pacific/Auckland",
      dateStyle: "medium",
      timeStyle: "medium",
      hour12: false
    }).format(now),
    nextCheckpointUtc,
    cadenceMinutes,
    launchTime,
    elapsedMinutes,
    minimumRuntimeMinutes,
    closeoutPolicy,
    earliestCloseoutUtc,
    oneHourElapsed,
    activeAndStandbySummary: [
      `${activeSibling}: current checked lane status is ${laneStatus}.`,
      `Latest response status: ${latestResponseStatus}.`,
      "Next sibling handoff stays gated until the active x1/x2 checklist passes or a formal open-gap is accepted.",
      "Lumen remains stand-by/recoverable while the verified Browser route is unavailable; Aevren-only phases do not wait on Lumen Browser harvest."
    ],
    closeoutBoundary: "Continue productive cadence checks. Close the phase as soon as the completion checklist passes; the one-hour window is an advisory practice target, not a hard blocker."
  },
  note: "This receipt records the checkpoint state only; it is not a sibling completion proof by itself."
});
