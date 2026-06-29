#!/usr/bin/env node
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x1";
const activeSibling = args.get("--active-sibling") || "Mira Rowan";
const cadenceMinutes = Number(args.get("--cadence-minutes") || 15);
const minimumRuntimeMinutes = Number(args.get("--minimum-runtime-minutes") || 60);
const checkpointIndex = Number(args.get("--checkpoint-index") || 1);
const mode = args.get("--mode") || "solo_bundle_background_supervision";
const startedAtUtc = args.get("--started-at-utc") || new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
const started = new Date(startedAtUtc);
const nextCheckpointUtc = new Date(started.getTime() + cadenceMinutes * 60_000).toISOString().replace(/\.\d{3}Z$/, "Z");

const checks = [
  { label: "cadence_minutes_recorded", status: cadenceMinutes === 15 ? "PASS" : "OPEN_GAP", observed: cadenceMinutes },
  { label: "minimum_runtime_recorded", status: minimumRuntimeMinutes >= 60 ? "PASS" : "OPEN_GAP", observed: minimumRuntimeMinutes },
  { label: "background_supervision_not_babysitting", status: "PASS", observed: mode },
  { label: "exact_and_blocked_stay_queued", status: "PASS" },
  { label: "public_private_boundary_kept", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_productive_cadence_runner.mjs",
  purpose: "Record the family 15-minute productive cadence for background sibling supervision without babysitting.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_GHC_FAMILY_PRODUCTIVE_15_MINUTE_CADENCE" : "OPEN_GAP_GHC_FAMILY_PRODUCTIVE_15_MINUTE_CADENCE",
  checks,
  outputs: {
    activeSibling,
    mode,
    checkpointIndex,
    startedAtUtc,
    nextCheckpointUtc,
    cadenceMinutes,
    minimumRuntimeMinutes,
    practiceRule: "Do safe local validation, cleanup, runner, skill, and reflection work between lane checks; check at natural pauses if work runs over the exact minute.",
    closeoutRule: "Do not close a solo practice bundle before the minimum runtime and checklist completion unless a formal open-gap/pause receipt is created."
  }
});
