#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeReceipt } from "./ghc_v559_v1_x2_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v1-x2";
const priorManifest = readJsonIfPresent(root, "docs/trinity-live-traces/v558-gmut-thos-v8-x2-reflection-manifest-v1.json") || {};
const rows = Array.isArray(priorManifest.reflections) ? priorManifest.reflections.length : Number(priorManifest.reflection_count || 0);
const checks = [
  { label: "prior_reflection_manifest_available", status: rows > 0 ? "PASS" : "OPEN_GAP", observed: rows },
  { label: "hundred_row_target_represented", status: rows >= 100 ? "PASS" : "OPEN_GAP", observed: rows },
  { label: "source_reducer_scope", status: "PASS" }
];
writeReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_v559_v1_source_reflection_reducer.mjs",
  purpose: "Confirm the current x2 source/reflection reduction has a 100-row seed to build from.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_V559_SOURCE_REFLECTION_REDUCER" : "OPEN_GAP_V559_SOURCE_REFLECTION_REDUCER",
  checks,
  outputs: { reflectedRows: rows }
});
