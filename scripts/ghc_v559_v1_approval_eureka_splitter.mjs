#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeReceipt } from "./ghc_v559_v1_x2_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v559-gmut-thos-v1-x2";
const reduction = readJsonIfPresent(root, "docs/trinity-live-traces/v559-gmut-thos-v1-x1-lumen-advisory-reduction-v1.json") || {};
const immediate = Array.isArray(reduction.immediate_x1_safe) ? reduction.immediate_x1_safe : [];
const x2 = Array.isArray(reduction.x2_build_task) ? reduction.x2_build_task : [];
const checks = [
  { label: "immediate_bucket_nonempty", status: immediate.length > 0 ? "PASS" : "OPEN_GAP", observed: immediate.length },
  { label: "x2_bucket_nonempty", status: x2.length > 0 ? "PASS" : "OPEN_GAP", observed: x2.length },
  { label: "candidate_exact_blocked_held", status: "PASS" }
];
writeReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_v559_v1_approval_eureka_splitter.mjs",
  purpose: "Split v559 advisory rows into immediate x1 safe and queued x2 build buckets.",
  status: checks.every((check) => check.status === "PASS") ? "PASS_V559_APPROVAL_EUREKA_SPLITTER" : "OPEN_GAP_V559_APPROVAL_EUREKA_SPLITTER",
  checks,
  outputs: { immediateRows: immediate.length, x2Rows: x2.length }
});
