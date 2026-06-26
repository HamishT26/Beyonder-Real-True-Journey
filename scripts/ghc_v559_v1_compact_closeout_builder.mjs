#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeReceipt } from "./ghc_v559_v1_x2_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v1-x2";
const closeout = readJsonIfPresent(root, "docs/trinity-live-traces/v559-gmut-thos-v1-x1-closeout-v1.json") || {};
const checks = [
  { label: "x1_closeout_present", status: closeout.status ? "PASS" : "OPEN_GAP" },
  { label: "next_active_phase_x2", status: closeout.next_active_phase === phaseSlug ? "PASS" : "OPEN_GAP", observed: closeout.next_active_phase },
  { label: "registered_closeout_gap_recorded", status: String(closeout.registered_closeout_builder_status || "").includes("OPEN_GAP") ? "PASS" : "OPEN_GAP" }
];
writeReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_v559_v1_compact_closeout_builder.mjs",
  purpose: "Build a compact closeout-readiness receipt from the v559 x1 manual closeout.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_V559_COMPACT_CLOSEOUT_BUILDER" : "OPEN_GAP_V559_COMPACT_CLOSEOUT_BUILDER",
  checks,
  outputs: { nextActivePhase: closeout.next_active_phase || null }
});
