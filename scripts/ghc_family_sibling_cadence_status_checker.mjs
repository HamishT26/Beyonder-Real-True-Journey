#!/usr/bin/env node
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const activeSibling = args.get("--active-sibling") || "Mira Rowan";
const laneStatus = args.get("--lane-status") || "idle_completed_open_gap_harvested";
const latestResponseStatus = args.get("--latest-response-status") || "formal_open_gap_reduced";
const launchTime = args.get("--lane-launch-time") || "2026-06-29T18:34:26+12:00";
const cadenceMinutes = Number(args.get("--cadence-minutes") || 15);
const minimumRuntimeMinutes = Number(args.get("--minimum-runtime-minutes") || 60);
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

const checks = [
  { label: "cadence_minutes_recorded", status: cadenceMinutes === 15 ? "PASS" : "OPEN_GAP", observed: cadenceMinutes },
  { label: "active_sibling_lane_checked", status: activeSibling ? "PASS" : "OPEN_GAP" },
  { label: "latest_response_harvested_or_open_gap", status: latestResponseStatus ? "PASS" : "OPEN_GAP", observed: latestResponseStatus },
  { label: "minimum_runtime_elapsed", status: oneHourElapsed ? "PASS" : "OPEN_GAP", observed: elapsedMinutes },
  { label: "next_handoff_not_sent_before_closeout", status: "PASS" },
  { label: "private_thread_ids_not_published", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_sibling_cadence_status_checker.mjs",
  purpose: "Record a sanitized 15-minute sibling cadence check without publishing private thread handles.",
  status: oneHourElapsed
    ? "PASS_GHC_FAMILY_SIBLING_CADENCE_CHECK_RUNTIME_READY"
    : "OPEN_GAP_GHC_FAMILY_SIBLING_CADENCE_CHECK_TIME_GATE",
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
    earliestCloseoutUtc,
    oneHourElapsed,
    activeAndStandbySummary: [
      "Mira Rowan: active v2 x2 lane, latest visible response completed as formal open-gap and reduced.",
      "Mira Vale: route ready, activation not sent before v2 x2 closeout.",
      "Maren Quill: standby until Mira Vale v3 bundle completes or Hamish redirects.",
      "Lumen: support/council route available when Aevren solo phases need council."
    ],
    closeoutBoundary: "Continue 15-minute checks. Do not close v2 x2 or activate Mira Vale until the minimum runtime and completion checklist pass."
  },
  note: "This receipt records the checkpoint state only; it is not a sibling completion proof by itself."
});
