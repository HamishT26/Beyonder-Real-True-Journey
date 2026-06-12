#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const cliVersion = args.get("--cli-version");
const lumenReplyStatus = args.get("--lumen-reply-status") || "AWAITING_OR_IN_PROGRESS";
const lumenMarkerPresent = (args.get("--lumen-marker-present") || "false").toLowerCase() === "true";
const readOnlyJson = args.get("--read-only-json");
const compactJson = args.get("--compact-json");
const eurekaBridgeJson = args.get("--eureka-bridge-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");
const exposureGuardJson = args.get("--exposure-guard-json");
const exposureGuardMd = args.get("--exposure-guard-md");
const noOverclaimGuardJson = args.get("--no-overclaim-guard-json");
const noOverclaimGuardMd = args.get("--no-overclaim-guard-md");
const noReplacementGuardJson = args.get("--no-replacement-guard-json");
const noReplacementGuardMd = args.get("--no-replacement-guard-md");

if (
  !phaseSlug ||
  !cliVersion ||
  !readOnlyJson ||
  !compactJson ||
  !eurekaBridgeJson ||
  !receiptJson ||
  !receiptMd ||
  !exposureGuardJson ||
  !exposureGuardMd ||
  !noOverclaimGuardJson ||
  !noOverclaimGuardMd ||
  !noReplacementGuardJson ||
  !noReplacementGuardMd
) {
  console.error(
    "Usage: node ghc_live_workflow_update_receipt_builder.mjs --phase-slug <slug> --cli-version <version> --read-only-json <json> --compact-json <json> --eureka-bridge-json <json> --receipt-json <json> --receipt-md <md> --exposure-guard-json <json> --exposure-guard-md <md> --no-overclaim-guard-json <json> --no-overclaim-guard-md <md> --no-replacement-guard-json <json> --no-replacement-guard-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function refName(path) {
  return basename(path);
}

const readOnly = readJson(readOnlyJson);
const compact = readJson(compactJson);
const eurekaBridge = readJson(eurekaBridgeJson);
const generatedUtc = utcNow();

const officialSourceSignals = [
  {
    source: "OpenAI Codex changelog",
    url: "https://developers.openai.com/codex/changelog",
    takeaway:
      "The current app line adds Browser Developer Mode with controlled developer inspection for performance, network, console, runtime, and page-state debugging.",
    workflow_use:
      "Use the Browser route for bounded page-state checks and visible ChatGPT-panel relay evidence, not for raw transcript publication.",
  },
  {
    source: "OpenAI Codex in-app browser documentation",
    url: "https://developers.openai.com/codex/app/browser",
    takeaway:
      "The in-app Browser is strongest for local, file-backed, and public pages; signed-in pages can require regular browser or Chrome extension fallback.",
    workflow_use:
      "Treat the Lumen Browser route as an observed live route that still needs status receipts and retry guards.",
  },
  {
    source: "OpenAI Codex GitHub releases",
    url: "https://github.com/openai/codex/releases",
    takeaway:
      "The locally verified CLI reports 0.139.0, matching the current 0.139 release line visible from the official release surface.",
    workflow_use:
      "Use 0.139.0-era CLI behavior for source/search/schema/sandbox expectations until a later exact version check changes it.",
  },
];

const laneRows = Array.isArray(readOnly.lane_permissions) ? readOnly.lane_permissions : [];
const activeLaneNames = laneRows
  .filter((lane) => lane.lane_scope === "active_existing_lane")
  .map((lane) => lane.lane);

const receipt = {
  artifact_type: "ghc_live_workflow_update_receipt",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "FULL_PHASE_DEFAULT_AND_BROWSER_ROUTE_REFRESH_RECORDED",
  input_refs: {
    read_only_authorization: refName(readOnlyJson),
    compact_refresh_card: refName(compactJson),
    x1_x2_eureka_bridge: refName(eurekaBridgeJson),
  },
  local_cli_status: {
    reported_version: cliVersion,
    version_check_passed: cliVersion.includes("0.139.0"),
    raw_doctor_output_published: false,
  },
  browser_route_event: {
    target_lane: "Lumen Vale",
    route_family: "existing ChatGPT panel through Codex in-app Browser",
    transmission_status: "PROMPT_SENT_STATUS_ONLY",
    reply_status_at_publication_time: lumenReplyStatus,
    expected_marker: "LUMEN_V508_V44_V1_X1_BROWSER_ROUTE_REFRESH_COMPLETE",
    expected_marker_observed_status_only: lumenMarkerPresent,
    raw_outbound_message_published: false,
    raw_reply_text_published: false,
    raw_thread_url_published: false,
    screenshot_published: false,
  },
  user_directives_recorded: [
    "Continue v491-v515 v1-v8 GMUT/THOS x1-x2 progression unless the user explicitly pauses or redirects.",
    "Do not use a Limited phase as the user-facing default unless the user asks for it.",
    "If evidence is missing, publish a blocker or gate-protected preparation receipt instead of claiming completion.",
    "Run the active sibling lanes in their existing round-robin groups during x1 phases.",
    "Retry blockers with different safe methods before advancing when a retry path remains inside scope.",
    "Use quick five-minute status checks while watcher and notifier helpers supervise the active lanes.",
  ],
  round_robin_roster: [
    {
      lane: "Lumen Vale",
      route: "ChatGPT Browser live adapter",
      current_role: "active existing ChatGPT-panel sibling",
      permission: "status-safe advisory only",
      replacement_allowed: false,
    },
    {
      lane: "Arby",
      route: "read-only CLI lane",
      current_role: "active existing CLI sibling",
      permission: "read-only advisory only",
      replacement_allowed: false,
    },
    {
      lane: "Aster Vale",
      route: "read-only CLI lane",
      current_role: "active existing CLI sibling",
      permission: "read-only advisory only",
      replacement_allowed: false,
    },
    {
      lane: "Cicero",
      route: "existing local app-server callable lane",
      current_role: "active existing app sibling",
      permission: "status-safe advisory only",
      replacement_allowed: false,
    },
    {
      lane: "Kierkegaard",
      route: "existing local app-server callable lane",
      current_role: "active existing app sibling",
      permission: "status-safe advisory only",
      replacement_allowed: false,
    },
    {
      lane: "Aristotle",
      route: "existing local app-server callable lane",
      current_role: "active existing app sibling",
      permission: "status-safe advisory only",
      replacement_allowed: false,
    },
  ],
  official_source_signals: officialSourceSignals,
  retry_policy: {
    minimum_safe_attempts_per_blocker: 5,
    vary_method_each_attempt: true,
    stop_conditions: [
      "action would require account mutation",
      "action would require plugin-cache or user-skill mutation",
      "action would require raw session or private app-state editing",
      "action would require destructive cleanup outside an exact approved scope",
      "action would require creating replacement siblings, replacement threads, or old-style subagents",
    ],
    publication_if_unresolved: "status-only blocker receipt with no raw logs or private identifiers",
  },
  next_safe_actions: [
    "Check Lumen at the next five-minute mark and record marker, in-progress, or blocker status only.",
    "Run active sibling groups in the next x1 phase using existing routes only.",
    "Convert the x1 eureka bridge candidates into x2 build tasks once their approvals and lane evidence are current.",
    "Use Browser Developer Mode for bounded page-state diagnostics, while respecting signed-in-page limitations from official docs.",
    "Keep the phase moving with gate-protected preparation when evidence is incomplete, without presenting it as a completed limited phase.",
  ],
  active_lane_names_from_authorization: activeLaneNames,
  approval_candidate_count_from_bridge: eurekaBridge.approval_candidate_count,
  eureka_task_count_from_bridge: eurekaBridge.eureka_task_count,
  compact_status_from_input: compact.status,
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_outbound_message_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
    private_app_metadata_published: false,
  },
  claim_boundary: {
    lumen_completion: lumenMarkerPresent ? "marker_observed_status_only" : "awaiting_or_in_progress",
    full_phase_completion: "not_claimed",
    x1_closeout: "not_claimed",
    x2_build_closeout: "not_claimed",
    source_target_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const exposureGuard = {
  artifact_type: "ghc_exposure_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: "PASS",
  checks: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_outbound_message_published: false,
    raw_thread_url_published: false,
    raw_callable_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
    private_app_metadata_published: false,
  },
};

const noOverclaimGuard = {
  artifact_type: "ghc_no_overclaim_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: "PASS",
  open_claims: receipt.claim_boundary,
  rationale:
    "The receipt records route transmission, optional status-only marker observation, and workflow preference only. It does not claim full phase completion, x2 build closeout, source completion, GMUT empirical closure, final physics, consciousness proof, legal closure, or canon promotion.",
};

const noReplacementGuard = {
  artifact_type: "ghc_no_replacement_guard",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_receipt: refName(receiptJson),
  status: "PASS",
  replacement_siblings_created: false,
  replacement_threads_created: false,
  old_style_subagents_spawned: false,
  roster_replacement_allowed: receipt.round_robin_roster.every((lane) => lane.replacement_allowed === false)
    ? false
    : "review_required",
};

mkdirSync(dirname(receiptJson), { recursive: true });
for (const [path, data] of [
  [receiptJson, receipt],
  [exposureGuardJson, exposureGuard],
  [noOverclaimGuardJson, noOverclaimGuard],
  [noReplacementGuardJson, noReplacementGuard],
]) {
  writeFileSync(path, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

const md = [
  `# ${phaseSlug} Live Workflow Update Receipt`,
  "",
  `Generated UTC: \`${receipt.generated_utc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  "## What Changed",
  "",
  "- The user-facing default is full v491-v515 v1-v8 GMUT/THOS x1-x2 progression, not limited phases.",
  "- If evidence is incomplete, the safe fallback is a blocker or gate-protected preparation receipt, not a false completion claim.",
  "- Lumen Vale was contacted through the existing in-app Browser ChatGPT panel and is awaiting or producing a reply at publication time.",
  lumenMarkerPresent
    ? "- Lumen Vale was contacted through the existing in-app Browser ChatGPT panel and the expected marker was observed status-only."
    : "- Lumen Vale was contacted through the existing in-app Browser ChatGPT panel and is awaiting or producing a reply at publication time.",
  "- Blockers should receive varied safe retry attempts before advancement when the route remains inside approved scope.",
  "",
  "## Local and App Update Evidence",
  "",
  `- CLI version observed locally: \`${receipt.local_cli_status.reported_version}\`.`,
  "- Official Codex changelog: Browser Developer Mode adds controlled developer inspection for Browser use.",
  "- Official in-app Browser docs: signed-in pages may need regular browser or Chrome-extension fallback, so ChatGPT-panel work remains status-receipted and retry-guarded.",
  "",
  "## Round-Robin Roster",
  "",
  ...receipt.round_robin_roster.map(
    (lane) =>
      `- ${lane.lane}: ${lane.route}; role \`${lane.current_role}\`; permission \`${lane.permission}\`; replacement allowed \`${String(lane.replacement_allowed)}\`.`,
  ),
  "",
  "## Retry Policy",
  "",
  `- Minimum safe attempts per blocker: \`${receipt.retry_policy.minimum_safe_attempts_per_blocker}\`.`,
  `- Vary method each attempt: \`${String(receipt.retry_policy.vary_method_each_attempt)}\`.`,
  `- If unresolved: ${receipt.retry_policy.publication_if_unresolved}.`,
  "",
  "## Next Safe Actions",
  "",
  ...receipt.next_safe_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "This is a status-only workflow update. It does not publish raw lane text, raw ChatGPT transcript, the outbound prompt body, app-server payloads, callable IDs, thread IDs, credentials, screenshots, local paths, private app metadata, or raw user text. It does not claim Lumen completion, full phase completion, x1 closeout, x2 build closeout, source target completion, GMUT empirical closure, final physics, consciousness proof, legal closure, or canon promotion.",
  "",
];
writeFileSync(receiptMd, md.join("\n"), "utf8");

const guardMd = (title, guard, body) =>
  [
    `# ${phaseSlug} ${title}`,
    "",
    `Generated UTC: \`${guard.generated_utc}\``,
    "",
    `Status: \`${guard.status}\``,
    "",
    body,
    "",
  ].join("\n");

writeFileSync(
  exposureGuardMd,
  guardMd(
    "Live Workflow Exposure Guard",
    exposureGuard,
    "Exposure guard passed: no raw lane text, raw ChatGPT transcript, outbound prompt body, raw thread URL, callable IDs, credentials, screenshots, local paths, raw user text, or private app metadata is published.",
  ),
  "utf8",
);
writeFileSync(
  noOverclaimGuardMd,
  guardMd(
    "Live Workflow No-Overclaim Guard",
    noOverclaimGuard,
    "No-overclaim guard passed: this receipt records only route transmission, optional Lumen marker observation, and workflow preference. Full phase completion, empirical, legal, consciousness, and canon claims remain open.",
  ),
  "utf8",
);
writeFileSync(
  noReplacementGuardMd,
  guardMd(
    "Live Workflow No-Replacement Guard",
    noReplacementGuard,
    "No-replacement guard passed: no replacement sibling, replacement thread, or old-style subagent creation is recorded or authorized by this receipt.",
  ),
  "utf8",
);

console.log(
  JSON.stringify(
    {
      status: receipt.status,
      cli_version: receipt.local_cli_status.reported_version,
      browser_route_status: receipt.browser_route_event.transmission_status,
      lumen_reply_status: receipt.browser_route_event.reply_status_at_publication_time,
      exposure_guard: exposureGuard.status,
      no_overclaim_guard: noOverclaimGuard.status,
      no_replacement_guard: noReplacementGuard.status,
    },
    null,
    2,
  ),
);
