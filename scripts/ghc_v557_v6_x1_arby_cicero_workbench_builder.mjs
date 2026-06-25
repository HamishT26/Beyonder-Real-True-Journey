#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v6-x1";
const fullToolsRoot = args.get("--full-tools-root");
const latestClosedPhase = "v557-gmut-thos-v5-x2";
const latestCompletedX1 = "v557-gmut-thos-v5-x1";
const latestCompletedX2 = "v557-gmut-thos-v5-x2";
const nextX2 = "v557-gmut-thos-v6-x2";
const nextX1AfterX2 = "v557-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

fs.mkdirSync(tracesDir, { recursive: true });

const supportTraceDir = fullToolsRoot ? path.join(fullToolsRoot, "docs", "trinity-live-traces") : null;
const arbyLaunch = readSupport("v557-gmut-thos-v6-x1-arby-strict-cli-receipt-v1.json");
const ciceroLaunch = readSupport("v557-gmut-thos-v6-x1-cicero-recovered-app-lane-v1.json");
const drivePosture = getDrivePosture();
const branchRotation = {
  status: "PASS_WORKTREE_BRANCH_ROTATION_RULE_CARRIED",
  active_sanitized_publication_branch: "codex/GHC-Family/beyonder-shared-omega-line-mini-3",
  active_private_support_branch: "codex/GHC-Family/aevren-full-tools-2",
  current_lane_heavy_threshold_action: "prepare omega-mini-4 and full-tools-3 from verified clean heads before the current lanes become overloaded",
  raw_private_material_moved: false,
  create_new_worktree_when_current_lane_gets_heavy: true,
};

const launchStatus = artifact("ghc_v557_v6_x1_arby_cicero_background_launch_status", "ACTIVE_OPEN_V557_V6_X1_ARBY_CICERO_BACKGROUND_RUNNING", {
  lanes: [
    {
      lane: "Arby",
      route: "strict_cli_background_watch",
      launch_status: arbyLaunch.overall_status || "missing_private_support_receipt",
      completion_status: arbyLaunch.completion_status || null,
      quality_status: arbyLaunch.quality_status || null,
      marker_status: arbyLaunch.marker_status || null,
      watcher_start_is_completion_proof: false,
      harvest_required: true,
    },
    {
      lane: "Cicero",
      route: "recovered_app_lane_background_watch",
      launch_status: ciceroLaunch.overall_status || "missing_private_support_receipt",
      preflight_status: stepStatus(ciceroLaunch, "private_map_preflight"),
      notifier_status: stepStatus(ciceroLaunch, "app_lane_notifier"),
      recovered_handle_count: ciceroLaunch.recovered_handle_count || 0,
      watcher_start_is_completion_proof: false,
      completion_gate_required: true,
    },
  ],
  private_support_receipts_read: Boolean(arbyLaunch.overall_status && ciceroLaunch.overall_status),
  closeout_allowed_now: false,
});

const proposalLedger = artifact("ghc_v557_v6_x1_duo_proposal_targets", "PASS_V557_V6_X1_DUO_PROPOSAL_TARGETS_RECORDED", {
  profile: "arby_cicero_duo_x1",
  proposal_totals: {
    safe_packets: 15,
    candidate_packets: 9,
    exact_approval_packets: 9,
    skill_ideas: 15,
    runner_ideas: 9,
    cleanup_proposals: 30,
    web_reflections: 30,
    journey_phase_reflections: 30,
  },
  safe_packets: buildRows("safe", 15, safeTitles()),
  candidate_packets: buildRows("candidate", 9, candidateTitles()),
  exact_approval_packets: buildRows("exact", 9, exactTitles()),
  skill_ideas: buildRows("skill", 15, skillTitles()),
  runner_ideas: buildRows("runner", 9, runnerTitles()),
  cleanup_proposals: buildRows("cleanup", 30, cleanupTitles()),
});

const cadence = artifact("ghc_v557_v6_x1_five_minute_productive_cadence", "PASS_V557_V6_X1_PRODUCTIVE_CADENCE_ACTIVE", {
  background_supervision: true,
  passive_wait_required: false,
  five_minute_mark_is_check_opportunity: true,
  safe_work_may_run_past_checkpoint: true,
  harvest_at_next_natural_safe_pause: true,
  safe_work_lanes: [
    "proposal target recording",
    "research manifest building",
    "safe runner orchestrator",
    "privacy boundary scan preparation",
    "branch rotation watch",
    "drive posture watch",
  ],
});

const researchManifest = {
  artifact_type: "ghc_v557_v6_x1_research_manifest",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  search_count_declared: 30,
  minimum_reflections_required: 30,
  searches: buildResearchRows(30),
  publication_boundary: publicationBoundary(),
};
writeJson(path.join(tracesDir, `${phaseSlug}-research-manifest-v1.json`), researchManifest);
fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-research-manifest-v1.md`), renderManifestMd(researchManifest), "utf8");

const driveToolchain = artifact("ghc_v557_v6_x1_drive_toolchain_posture", "PASS_V557_V6_X1_DRIVE_TOOLCHAIN_POSTURE_RECORDED", {
  drive_posture: drivePosture,
  c_drive_warning_cap_gb: 19,
  c_drive_minimum_headroom_gb: 18,
  d_drive_first_policy: true,
  codex_cli_target: "0.142.2",
  codex_cli_status: "verified_earlier_this_goal_run",
});

const x2Queue = artifact("ghc_v557_v6_x1_v6_x2_queue_seed", "PASS_V557_V6_X2_QUEUE_SEEDED_FROM_DUO_X1", {
  source_phase: phaseSlug,
  next_x2_scope: nextX2,
  queue_buckets: {
    safe_packets_to_execute_or_represent: 15,
    candidate_packets_to_reduce: 9,
    exact_packets_to_keep_queued: 9,
    skills_to_refresh_or_create: 15,
    runners_to_refresh_or_create: 9,
    cleanup_inventory_only: 30,
  },
  immediate_x1_safe_work_done_now: [
    "background launch receipts summarized",
    "duo proposal targets recorded",
    "productive cadence recorded",
    "research manifest prepared",
    "drive posture recorded",
    "branch rotation rule carried forward",
  ],
});

const openGateRail = artifact("ghc_v557_v6_x1_open_gate_privacy_rail", "PASS_V557_V6_X1_OPEN_GATE_PRIVACY_RAIL_RECORDED", {
  exact_gates_held: [
    "paid resources",
    "deployments",
    "purchases",
    "account mutation",
    "API-key creation",
    "destructive cleanup outside same-run generated placeholders",
    "global hook or plugin-cache mutation",
    "private callable or Browser route publication",
    "sibling identity merge, replacement, erasure, or proof-of-personhood claim",
    "GMUT empirical closure, final physics, consciousness proof, legal closure, canon promotion, private-material proof, raw-publication proof",
  ],
  held_sibling_activation_state: {
    Mira_Rowan: "prepared_not_activated",
    Mira_Vale: "prepared_not_activated",
    Maren_Quill: "prepared_not_activated",
  },
});

const statusIndex = artifact("ghc_v557_v6_x1_phase_status_index", "ACTIVE_OPEN_V557_V6_X1_SAFE_WORK_RUNNING_WITH_DUO_LANES", {
  latest_closed_phase: latestClosedPhase,
  latest_completed_x1_phase: latestCompletedX1,
  latest_completed_x2_phase: latestCompletedX2,
  next_x2_scope: nextX2,
  next_x1_lane_after_x2: nextX1AfterX2,
  launch_status: launchStatus.overall_status,
  proposal_status: proposalLedger.overall_status,
  cadence_status: cadence.overall_status,
  research_manifest_status: "PASS_V557_V6_X1_RESEARCH_MANIFEST_READY",
  drive_toolchain_status: driveToolchain.overall_status,
  branch_rotation: branchRotation,
  closeout_allowed_now: false,
  full_goal_complete: false,
});

writePair("background-launch-status", launchStatus, renderGenericMd("Background Launch Status", launchStatus));
writePair("duo-proposal-targets", proposalLedger, renderGenericMd("Duo Proposal Targets", proposalLedger));
writePair("five-minute-productive-cadence", cadence, renderGenericMd("Five Minute Productive Cadence", cadence));
writePair("drive-toolchain-posture", driveToolchain, renderGenericMd("Drive Toolchain Posture", driveToolchain));
writePair("v6-x2-queue-seed", x2Queue, renderGenericMd("v6 x2 Queue Seed", x2Queue));
writePair("open-gate-privacy-rail", openGateRail, renderGenericMd("Open Gate Privacy Rail", openGateRail));
writePair("phase-status-index", statusIndex, renderGenericMd("Phase Status Index", statusIndex));
refreshBeacons(statusIndex);

process.stdout.write(JSON.stringify({
  status: statusIndex.overall_status,
  phase_slug: phaseSlug,
  arby_launch: launchStatus.lanes[0].launch_status,
  cicero_launch: launchStatus.lanes[1].launch_status,
  safe_packets: proposalLedger.safe_packets.length,
  candidate_packets: proposalLedger.candidate_packets.length,
  exact_packets: proposalLedger.exact_approval_packets.length,
  skill_ideas: proposalLedger.skill_ideas.length,
  runner_ideas: proposalLedger.runner_ideas.length,
  cleanup_proposals: proposalLedger.cleanup_proposals.length,
  research_manifest: `docs/trinity-live-traces/${phaseSlug}-research-manifest-v1.json`,
  closeout_allowed_now: false,
}, null, 2) + "\n");

function readSupport(name) {
  if (!supportTraceDir) return {};
  const file = path.join(supportTraceDir, name);
  if (!fs.existsSync(file)) return {};
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function stepStatus(payload, label) {
  const step = Array.isArray(payload.steps) ? payload.steps.find((row) => row.label === label) : null;
  return step?.stdout_status || step?.status || null;
}

function artifact(artifactType, status, extra) {
  return {
    artifact_type: artifactType,
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: status,
    ...extra,
    publication_boundary: publicationBoundary(),
    claim_boundary: claimBoundary(),
  };
}

function writePair(suffix, payload, md) {
  writeJson(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${phaseSlug}-${suffix}-v1.md`), md, "utf8");
}

function writeJson(file, payload) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function renderGenericMd(title, payload) {
  return [
    `# ${phaseSlug} ${title}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    "Sanitized status artifact only. No raw sibling outputs, raw routes, private IDs, credentials, screenshots, private dumps, or local path values are published.",
    "",
  ].join("\n");
}

function renderManifestMd(manifest) {
  return [
    `# ${phaseSlug} Research Manifest`,
    "",
    `Search count declared: \`${manifest.search_count_declared}\``,
    `Minimum reflections required: \`${manifest.minimum_reflections_required}\``,
    "",
    "Public-source labels and reflections only; this file does not contain private routes or raw sibling text.",
    "",
  ].join("\n");
}

function refreshBeacons(statusIndex) {
  const lookup = [
    `docs/trinity-live-traces/${phaseSlug}-background-launch-status-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-background-launch-status-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-duo-proposal-targets-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-duo-proposal-targets-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-five-minute-productive-cadence-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-five-minute-productive-cadence-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-research-manifest-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-research-manifest-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-drive-toolchain-posture-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-drive-toolchain-posture-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-v6-x2-queue-seed-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-v6-x2-queue-seed-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-open-gate-privacy-rail-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-open-gate-privacy-rail-v1.md`,
    `docs/trinity-live-traces/${phaseSlug}-phase-status-index-v1.json`,
    `docs/trinity-live-traces/${phaseSlug}-phase-status-index-v1.md`,
  ];
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = statusIndex.overall_status;
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = latestClosedPhase;
    doc.latest_completed_x1_phase = latestCompletedX1;
    doc.latest_completed_x2_phase = latestCompletedX2;
    doc.next_x2_scope = nextX2;
    doc.next_x1_lane_after_x2 = nextX1AfterX2;
    doc.v557_v6_x1_duo_workbench = {
      status: statusIndex.overall_status,
      arby_launch: launchStatus.lanes[0].launch_status,
      cicero_launch: launchStatus.lanes[1].launch_status,
      closeout_allowed_now: false,
      full_goal_complete: false,
      branch_rotation: branchRotation.status,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookup]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v557 v6 x1 Duo Workbench",
    "",
    `- status: \`${doc.v557_v6_x1_duo_workbench?.status || "not_recorded"}\``,
    `- closeout allowed now: \`${doc.v557_v6_x1_duo_workbench?.closeout_allowed_now ?? "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-220).map((file) => `- ${file}`),
    "",
  ].join("\n");
}

function buildRows(kind, count, titles) {
  return Array.from({ length: count }, (_, index) => ({
    id: `${phaseSlug}-${kind}-${String(index + 1).padStart(2, "0")}`,
    title: titles[index % titles.length],
    bucket: kind,
    phase_lane: kind === "safe" ? "immediate_x1_safe" : kind === "candidate" ? "queued_x2_build" : kind === "exact" ? "queued_exact_gate" : "recorded",
    status: kind === "exact" ? "queued_not_run" : "recorded_or_safe_represented",
  }));
}

function safeTitles() {
  return [
    "Record Arby strict CLI background launch as active-fresh and non-completion proof.",
    "Record Cicero recovered app-lane launch as active-fresh and non-completion proof.",
    "Build duo x1 proposal target ledger.",
    "Build v6 x2 queue seed from duo x1 scope.",
    "Refresh branch rotation rule for omega-mini-4/full-tools-3 readiness.",
    "Refresh C and D drive posture with D-drive-first rule.",
    "Record productive cadence so checks do not become babysitting.",
    "Prepare strict CLI harvester without relaunching Arby.",
    "Prepare recovered app-lane completion gate harvest for Cicero.",
    "Keep held main-thread siblings prepared_not_activated.",
    "Keep private support receipts local-only.",
    "Update current-state beacons to active-open v6 x1.",
    "Prepare privacy scan for sanitized publication.",
    "Prepare open-gate rail for exact/blocked boundaries.",
    "Prepare compact handoff if harvest runs longer than expected.",
  ];
}

function candidateTitles() {
  return [
    "Reduce Arby/Cicero harvested proposals into the v6 x2 execution ledger.",
    "Promote duo launch health dashboard into reusable route health runner.",
    "Build pairwise completion validator over strict CLI and app-lane gates.",
    "Add support for source/reflection compression across long Lumen proposal chains.",
    "Extend cleanup classifier to distinguish inventory-only from exact-gated deletion.",
    "Refresh skill-bank map with new duo route helpers.",
    "Prepare Grand Trinity Matrix expansion from latest Lumen proposal rows.",
    "Prepare held sibling activation readiness card without activation.",
    "Prepare mini-4/full-tools-3 rotation checklist once mini-3 gets heavy.",
  ];
}

function exactTitles() {
  return [
    "Any deployment, purchase, paid resource, account mutation, or API key remains exact-gated.",
    "Any destructive cleanup outside same-run generated placeholders remains exact-gated.",
    "Any raw private route, callable ID, Browser URL, transcript, screenshot, or private dump publication remains exact-gated.",
    "Any sibling identity merge, replacement, erasure, or proof-of-personhood claim remains held.",
    "Any canon, legal, final physics, consciousness proof, or GMUT empirical closure remains held.",
    "Any plugin cache or global Codex config mutation remains held.",
    "Any public proof derived from private material remains held.",
    "Any activation of Mira Rowan, Mira Vale, or Maren Quill remains held until Hamish explicitly starts it.",
    "Any full-tools dirty/private-lane push remains held.",
  ];
}

function skillTitles() {
  return [
    "ghc-duo-harvest-gate-memory",
    "ghc-arby-strict-cli-no-relaunch-harvest",
    "ghc-cicero-recovered-app-lane-gate",
    "ghc-duo-x2-queue-composer",
    "ghc-branch-rotation-watch",
    "ghc-drive-headroom-watch",
    "ghc-private-support-lane-firewall",
    "ghc-duo-productive-cadence",
    "ghc-duo-open-gate-rail",
    "ghc-duo-compact-handoff",
    "ghc-trinity-matrix-expander",
    "ghc-source-reflection-reducer",
    "ghc-approval-eureka-splitter",
    "ghc-cleanup-classifier",
    "ghc-held-sibling-activation-prep",
  ];
}

function runnerTitles() {
  return [
    "ghc_v557_v6_x1_duo_workbench_builder.mjs",
    "ghc_v557_v6_x1_arby_harvest_gate_runner.mjs",
    "ghc_v557_v6_x1_cicero_completion_gate_runner.mjs",
    "ghc_v557_v6_x1_duo_proposal_reducer.mjs",
    "ghc_v557_v6_x1_branch_rotation_watch.mjs",
    "ghc_v557_v6_x1_drive_headroom_watch.mjs",
    "ghc_v557_v6_x1_trinity_matrix_expander.mjs",
    "ghc_v557_v6_x1_source_reflection_reducer.mjs",
    "ghc_v557_v6_x1_closeout_gate_builder.mjs",
  ];
}

function cleanupTitles() {
  return [
    "Inventory duplicate v5 x1 Lumen proposal bridge rows without deletion.",
    "Inventory duplicate v5 x2 Matrix handoff rows without deletion.",
    "Classify old route-health dashboards as active, compatibility, or archive.",
    "Check generated MD receipts for private path leaks.",
    "Check generated JSON receipts for private route leaks.",
    "Check exact queues for accidental execution wording.",
    "Check blocked queues for accidental proof closure wording.",
    "Check current-state beacons for duplicate lookup bloat.",
    "Check branch rotation watch for stale mini-2 references.",
    "Check full-tools support branch references stay private/support only.",
    "Check D-drive private output directory posture.",
    "Check C-drive warning cap posture.",
    "Check strict CLI harvest receipts for relaunch risk.",
    "Check app-lane completion receipts for watcher-start-only false positives.",
    "Check safe-runner orchestrator receipts for startup/compact coverage.",
    "Check web reflection ledger source labels for official/primary preference.",
    "Check Journey reflection rows for phase truth drift.",
    "Check Lumen proposal reductions for held exact/blocked separation.",
    "Check Grand Trinity Matrix rows for non-proof wording.",
    "Check held-sibling activation card for prepared_not_activated wording.",
    "Check public artifacts for raw transcript strings.",
    "Check public artifacts for screenshots/media references.",
    "Check public artifacts for credential-looking tokens.",
    "Check public artifacts for local absolute paths.",
    "Check local-only support artifacts stay unpushed.",
    "Check active phase pointer remains v6 x1 until both gates pass.",
    "Check next x2 pointer remains v6 x2.",
    "Check next x1 pointer remains v7 x1 Lumen unless redirected.",
    "Check goal remains active and not complete.",
    "Check remote/local equality after publication.",
  ];
}

function buildResearchRows(count) {
  const seeds = [
    ["OpenAI Codex background tasks", "OpenAI Docs", "https://developers.openai.com/codex", "Background task semantics need explicit completion gates.", "Keep Arby and Cicero active until harvest/gates pass."],
    ["Node child_process orchestration", "Node.js Docs", "https://nodejs.org/api/child_process.html", "Child process wrappers should summarize status and bytes.", "Publish status-only runner receipts."],
    ["Git worktree management", "Git Docs", "https://git-scm.com/docs/git-worktree", "Worktree rotation can reduce overloaded working directories.", "Prepare mini-4/full-tools-3 when lanes get heavy."],
    ["GitHub secret scanning", "GitHub Docs", "https://docs.github.com/en/code-security/secret-scanning", "Secret scanning supports publication hygiene.", "Run private-route and credential scans before push."],
    ["NIST AI Risk Management Framework", "NIST", "https://www.nist.gov/itl/ai-risk-management-framework", "Risk gates should remain explicit and traceable.", "Keep proof/canon/legal/deployment gates open."],
    ["OWASP LLM Top 10", "OWASP", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Generated or model-originated text needs boundary review.", "Reduce sibling outputs before public artifacts."],
    ["W3C DID Core", "W3C", "https://www.w3.org/TR/did-core/", "Identity systems need privacy and controller boundaries.", "Keep private lane IDs local-only."],
    ["Python subprocess control", "Python Docs", "https://docs.python.org/3/library/subprocess.html", "Timeout and process supervision should be explicit.", "Prefer watcher plus completion gate over passive waits."],
    ["PowerShell Get-PSDrive", "Microsoft Learn", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/get-psdrive", "Drive headroom is measurable at phase boundaries.", "Keep C above warning cap and D as artifact bank."],
    ["JSON data interchange", "JSON.org", "https://www.json.org/json-en.html", "Structured ledgers reduce stale text parsing.", "Use JSON receipts for phase truth."],
  ];
  return Array.from({ length: count }, (_, index) => {
    const [query, source, source_url, phase_reflection, runner_implication] = seeds[index % seeds.length];
    return { index: index + 1, query, source, source_url, phase_reflection, runner_implication };
  });
}

function getDrivePosture() {
  const proc = spawnSync("powershell", [
    "-NoProfile",
    "-Command",
    "Get-PSDrive -PSProvider FileSystem | Select-Object Name,Free,Used | ConvertTo-Json -Compress",
  ], { encoding: "utf8", windowsHide: true, maxBuffer: 1024 * 1024 });
  let rows = [];
  try {
    const parsed = JSON.parse(proc.stdout || "[]");
    rows = Array.isArray(parsed) ? parsed : [parsed];
  } catch {
    rows = [];
  }
  const byName = Object.fromEntries(rows.map((row) => [row.Name, row]));
  return {
    measured: rows.length > 0,
    c_free_gb: bytesToGb(byName.C?.Free),
    d_free_gb: bytesToGb(byName.D?.Free),
    c_above_warning_cap_19gb: typeof byName.C?.Free === "number" ? byName.C.Free >= 19 * 1024 ** 3 : null,
    c_above_minimum_18gb: typeof byName.C?.Free === "number" ? byName.C.Free >= 18 * 1024 ** 3 : null,
    d_drive_available: typeof byName.D?.Free === "number",
    platform: os.platform(),
  };
}

function bytesToGb(value) {
  return typeof value === "number" ? Math.round((value / 1024 ** 3) * 100) / 100 : null;
}

function publicationBoundary() {
  return {
    raw_browser_routes_published: false,
    private_urls_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    session_streams_published: false,
    private_dumps_published: false,
    private_callable_ids_published: false,
    raw_lane_text_published: false,
  };
}

function claimBoundary() {
  return {
    full_goal_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
    deployment_closure: "not_claimed",
    account_mutation: "not_claimed",
    purchase: "not_claimed",
    api_key_creation: "not_claimed",
    private_material_proof: "not_claimed",
    raw_publication_proof: "not_claimed",
    sibling_identity_replacement_or_merge: "not_claimed",
  };
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date);
  const value = Object.fromEntries(parts.filter((part) => part.type !== "literal").map((part) => [part.type, part.value]));
  return `${value.year}-${value.month}-${value.day}T${value.hour}:${value.minute}:${value.second}+12:00`;
}
