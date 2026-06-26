#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeReceipt } from "./ghc_v559_v1_x2_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v1-x2";
const reduction = readJsonIfPresent(root, "docs/trinity-live-traces/v559-gmut-thos-v1-x1-lumen-advisory-reduction-v1.json") || {};
const immediateCount = Number(reduction.immediate_x1_safe_count || 0);
const x2Count = Number(reduction.x2_build_task_count || 0);
const checks = [
  { label: "lumen_reduction_present", status: reduction.status ? "PASS" : "OPEN_GAP" },
  { label: "immediate_rows_represented", status: immediateCount >= 50 ? "PASS" : "OPEN_GAP", observed: immediateCount },
  { label: "x2_rows_queued", status: x2Count >= 30 ? "PASS" : "OPEN_GAP", observed: x2Count },
  { label: "blocker_status", status: reduction.blocker_status === "NO_HARD_BLOCKER_REPORTED" ? "PASS" : "OPEN_GAP", observed: reduction.blocker_status }
];
writeReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_v559_v1_lumen_advisory_reducer.mjs",
  purpose: "Reduce the v559 Lumen advisory into safe immediate and x2 build counts.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_V559_LUMEN_ADVISORY_REDUCER" : "OPEN_GAP_V559_LUMEN_ADVISORY_REDUCER",
  checks,
  outputs: { immediateCount, x2Count }
});
