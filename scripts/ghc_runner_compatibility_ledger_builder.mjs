#!/usr/bin/env node
import { mkdirSync, readdirSync, statSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const scriptsDir = args.get("--scripts-dir") || "scripts";
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_runner_compatibility_ledger_builder.mjs --phase-slug <slug> --scripts-dir <dir> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

const currentEssential = new Set([
  "ghc_source_reflection_ledger_builder.mjs",
  "ghc_x1_cadence_work_queue_builder.mjs",
  "ghc_approval_activation_carry_gate.mjs",
  "ghc_read_only_lane_authorization_intake.mjs",
  "ghc_phase_start_readiness_gate.mjs",
  "ghc_approval_candidate_index.mjs",
  "ghc_phase_prep_queue_builder.mjs",
  "ghc_compact_refresh_card_builder.mjs",
  "ghc_blocker_boundary_packet_builder.mjs",
  "ghc_no_replacement_sibling_guard.mjs",
  "ghc_route_family_status_board.mjs",
  "ghc_phase_advance_guard.mjs",
]);

const routeRecovery = new Set([
  "ghc_app_server_capability_probe.mjs",
  "ghc_app_lane_private_map_preflight.mjs",
  "ghc_route_family_validator.mjs",
  "ghc_strict_cli_lane_cycle.mjs",
  "ghc_marker_source_validator.mjs",
  "ghc_live_adapter_repair_checklist_builder.mjs",
  "ghc_phase_boundary_orchestrator.mjs",
  "ghc_live_adapter_no_advance_gate.mjs",
  "ghc_v507_round_robin_route_planner.mjs",
  "ghc_route_state_validator.mjs",
  "ghc_v506_readiness_node_entrypoint.mjs",
]);

function classify(name) {
  if (currentEssential.has(name)) {
    return {
      tier: "current_v508_essential",
      recommendation: "Use first for v508-v515 preparation, guards, receipts, and compact-refresh handoffs.",
      enabled_for_v508: true,
    };
  }
  if (routeRecovery.has(name)) {
    return {
      tier: "route_recovery_or_fallback",
      recommendation: "Use only when current route recovery requires this narrower probe or validator.",
      enabled_for_v508: true,
    };
  }
  return {
    tier: "unclassified_legacy_or_experimental",
    recommendation: "Do not use by default; review before invoking in a live phase.",
    enabled_for_v508: false,
  };
}

const runnerRows = readdirSync(scriptsDir)
  .filter((name) => /^ghc_.*\.mjs$/u.test(name))
  .sort((a, b) => a.localeCompare(b))
  .map((name) => {
    const relative_path = `${scriptsDir}/${name}`;
    const stats = statSync(join(scriptsDir, name));
    const classification = classify(name);
    return {
      name,
      relative_path,
      size_bytes: stats.size,
      last_write_epoch_ms: Math.trunc(stats.mtimeMs),
      ...classification,
      node_entrypoint: true,
      windows_entrypoint_required: false,
      raw_output_publication_allowed: false,
      destructive_action_allowed: false,
    };
  });

const tierCounts = runnerRows.reduce((counts, row) => {
  counts[row.tier] = (counts[row.tier] || 0) + 1;
  return counts;
}, {});

const receipt = {
  artifact_type: "ghc_runner_compatibility_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "RUNNER_COMPATIBILITY_LEDGER_READY",
  scripts_dir: scriptsDir,
  runner_count: runnerRows.length,
  tier_counts: tierCounts,
  node_entrypoint_policy: {
    default_entrypoint: "Node",
    windows_entrypoint_fallback: "Only when a Node helper does not cover the required safe action.",
    deletion_or_cleanup_allowed: false,
    process_control_allowed: false,
  },
  recommended_v508_sequence: [
    "approval activation and carry gate",
    "read-only lane authorization intake",
    "x1 cadence work queue",
    "current source reflection ledger",
    "route-family status board",
    "no-replacement, exposure, and no-overclaim guards",
    "compact-refresh card",
  ],
  runners: runnerRows,
  v508_usage_rules: [
    "Use current_v508_essential runners before older route-recovery helpers.",
    "Use route_recovery_or_fallback runners only to refresh evidence or publish blocker receipts.",
    "Do not invoke unclassified runners in live phase work without a fresh receipt or approval packet.",
    "Do not let any runner publish raw lane text, private IDs, credentials, screenshots, local absolute paths, or raw app-server payloads.",
    "Do not use any runner output as phase completion proof unless a phase gate explicitly says it is sufficient.",
  ],
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    v508_full_phase_start: "not_claimed",
    x2_build_closeout: "not_claimed",
    runner_completeness: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const rowsByTier = runnerRows.reduce((groups, row) => {
  groups[row.tier] ||= [];
  groups[row.tier].push(row);
  return groups;
}, {});

const md = [
  `# ${phaseSlug} Runner Compatibility Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Runner count: \`${receipt.runner_count}\``,
  "",
  "## Node Entrypoint Policy",
  "",
  `- Default entrypoint: ${receipt.node_entrypoint_policy.default_entrypoint}.`,
  `- Windows fallback: ${receipt.node_entrypoint_policy.windows_entrypoint_fallback}`,
  "- No deletion, cleanup, or process-control authority is granted by this ledger.",
  "",
  "## Recommended v508 Sequence",
  "",
  ...receipt.recommended_v508_sequence.map((step) => `- ${step}`),
  "",
  "## Runners By Tier",
  "",
  ...Object.entries(rowsByTier).flatMap(([tier, rows]) => [
    `### ${tier}`,
    "",
    ...rows.map((row) => `- ${row.name}: ${row.recommendation}`),
    "",
  ]),
  "## Usage Rules",
  "",
  ...receipt.v508_usage_rules.map((rule) => `- ${rule}`),
  "",
  "## Boundary",
  "",
  "This ledger classifies runners for v508-v515 preparation. It does not prove every helper is complete, does not start or close v508, does not delete or mutate old helpers, and does not publish raw or private material.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status: receipt.status,
      runner_count: receipt.runner_count,
      tier_counts: receipt.tier_counts,
    },
    null,
    2,
  ),
);
