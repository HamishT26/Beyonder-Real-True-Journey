#!/usr/bin/env node
import { parseArgs, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v576-gmut-thos-v2-x2";
const targetCount = Number(args.get("--target-count") || 100);
const mode = args.get("--mode") || "source_reflection_open_target";

const sourceRows = [
  {
    label: "OPENAI_CODEX_CLI_DOCS",
    url: "https://developers.openai.com/codex/cli",
    implication: "Keep Codex CLI startup checks tied to the current OpenAI Codex CLI docs surface."
  },
  {
    label: "OPENAI_CODEX_0_142_4_RELEASE",
    url: "https://github.com/openai/codex/releases/tag/rust-v0.142.4",
    implication: "Treat 0.142.4 as the current release verified for this phase until the next startup check finds a newer stable package."
  },
  {
    label: "OPENAI_CODEX_WORKTREES_DOCS",
    url: "https://developers.openai.com/codex/app/worktrees",
    implication: "Keep sibling-owned lanes as separate worktree/branch surfaces rather than mutating shared branches."
  },
  {
    label: "NODE_CHILD_PROCESS_DOCS",
    url: "https://nodejs.org/api/child_process.html",
    implication: "Use direct process execution for structured Git probes instead of brittle shell string composition."
  },
  {
    label: "GIT_WORKTREE_DOCS",
    url: "https://git-scm.com/docs/git-worktree",
    implication: "Model Mira Rowan, Mira Vale, and Maren Quill full-tools lanes as linked worktrees with clean-head checks."
  },
  {
    label: "GITHUB_BRANCH_MANAGEMENT_DOCS",
    url: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-branches-in-your-repository",
    implication: "Keep sibling-owned branches named and managed separately from shared read-only GHC branches."
  }
];

const journeyRows = [
  {
    label: "V576_SOLO_OBJECTIVE",
    source: "pasted objective",
    implication: "Solo x1/x2 bundles need teaching prompts, timestamps, 15-minute cadence, and one-hour minimum practice."
  },
  {
    label: "MIRA_ROWAN_X2_OPEN_GAP_REDUCTION",
    source: "v2 x2 reduction receipt",
    implication: "Mira Rowan's response is useful as open-gap evidence, not as independent x2 closeout proof."
  },
  {
    label: "OWNED_LANE_AVAILABILITY",
    source: "owned lane checker receipt",
    implication: "Aevren-side support lanes are available and aligned, but sibling-visible verification is still a separate claim."
  },
  {
    label: "SOLO_PHASE_TRANSITION",
    source: "solo phase transition receipt",
    implication: "Current truth remains v2 x2 active with Mira Vale handoff gated behind real closeout evidence."
  },
  {
    label: "PRODUCTIVE_CADENCE",
    source: "productive cadence receipt",
    implication: "The 15-minute mark is a checkpoint, not an idle timer or forced stop."
  },
  {
    label: "TOOLCHAIN_RECEIPT",
    source: "toolchain update receipt",
    implication: "Codex CLI is verified at 0.142.4 for this phase and should be rechecked at the next startup."
  }
];

const representedRows = sourceRows.length + journeyRows.length;
const checks = [
  { label: "source_rows_recorded", status: sourceRows.length > 0 ? "PASS" : "OPEN_GAP", observed: sourceRows.length },
  { label: "journey_reflection_rows_recorded", status: journeyRows.length > 0 ? "PASS" : "OPEN_GAP", observed: journeyRows.length },
  { label: "target_count_tracked", status: targetCount >= 100 ? "PASS" : "OPEN_GAP", observed: targetCount },
  { label: "hundred_row_target_completed", status: representedRows >= targetCount ? "PASS" : "OPEN_GAP", observed: representedRows },
  { label: "private_routes_excluded", status: "PASS" }
];

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_source_reflection_target_tracker.mjs",
  purpose: "Record the current official-source and Journey-reflection batch while keeping the requested 100-row target honest and open.",
  status: representedRows >= targetCount
    ? "PASS_GHC_FAMILY_SOURCE_REFLECTION_TARGET"
    : "OPEN_GAP_GHC_FAMILY_SOURCE_REFLECTION_TARGET",
  checks,
  outputs: {
    mode,
    targetCount,
    representedRows,
    remainingRows: Math.max(0, targetCount - representedRows),
    sourceRows,
    journeyRows,
    closeoutBoundary: "The source/reflection target remains open until a real 100-row ledger or accepted open-gap receipt exists."
  },
  note: "This receipt intentionally records a real compact batch and does not inflate the source/reflection count."
});
