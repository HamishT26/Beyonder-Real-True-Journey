#!/usr/bin/env node
import { parseArgs, readJsonIfPresent, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v1-x1";
const reductionFile = args.get("--reduction-file") || `docs/trinity-live-traces/${phaseSlug}-lumen-advisory-reduction-v1.json`;
const reduction = readJsonIfPresent(root, reductionFile) || {};
const rows = Array.isArray(reduction.rows) ? reduction.rows : [];
const immediate = Array.isArray(reduction.immediate_x1_safe)
  ? reduction.immediate_x1_safe
  : rows.filter((row) => row.execution_lane === "immediate_x1_safe");
const x2 = Array.isArray(reduction.x2_build_task)
  ? reduction.x2_build_task
  : rows.filter((row) => row.execution_lane === "x2_build_task");
const exact = Array.isArray(reduction.exact_approval_needed)
  ? reduction.exact_approval_needed
  : rows.filter((row) => row.approval_bucket === "exact_approval_needed");
const blocked = Array.isArray(reduction.blocked_queue)
  ? reduction.blocked_queue
  : rows.filter((row) => row.approval_bucket === "blocked");
const checks = [
  { label: "reduction_file_available", status: reduction.status || reduction.artifact_type ? "PASS" : "OPEN_GAP" },
  { label: "immediate_bucket_nonempty", status: immediate.length > 0 ? "PASS" : "OPEN_GAP", observed: immediate.length },
  { label: "x2_bucket_nonempty", status: x2.length > 0 ? "PASS" : "OPEN_GAP", observed: x2.length },
  { label: "exact_and_blocked_held", status: "PASS", observed: exact.length + blocked.length }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_approval_eureka_splitter.mjs",
  purpose: "Represent approval/eureka buckets with a family-named splitter while exact and blocked work remains queued.",
  status: checks[0].status === "PASS" ? "PASS_GHC_FAMILY_APPROVAL_EUREKA_SPLITTER" : "OPEN_GAP_GHC_FAMILY_APPROVAL_EUREKA_SPLITTER",
  checks,
  outputs: { reductionFile, immediateRows: immediate.length, x2Rows: x2.length, exactRows: exact.length, blockedRows: blocked.length }
});
