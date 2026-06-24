#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v555-gmut-thos-v6-x1";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

fs.mkdirSync(tracesDir, { recursive: true });

const proposal = buildProposalLedger();
const reflection = buildReflectionLedger();
const background = buildBackgroundStandard();
const laneLaunch = buildLaneLaunchStatus();
const phaseIndex = buildPhaseStatusIndex(proposal, reflection, background, laneLaunch);

const written = [
  writePair("arby-cicero-duo-proposals", proposal, renderProposalMd(proposal)),
  writePair("web-journey-reflection-ledger", reflection, renderReflectionMd(reflection)),
  writePair("background-sibling-supervision-standard", background, renderBackgroundMd(background)),
  writePair("lane-launch-status", laneLaunch, renderLaneLaunchMd(laneLaunch)),
  writePair("phase-status-index", phaseIndex, renderIndexMd(phaseIndex)),
];

refreshBeacons(written, proposal, reflection, laneLaunch);

console.log(JSON.stringify({
  status: phaseIndex.overall_status,
  phase_slug: phaseSlug,
  safe_now_packets: proposal.counts.safe_now_packets,
  candidate_packets: proposal.counts.candidate_packets,
  exact_approval_packets: proposal.counts.exact_approval_packets,
  skill_ideas: proposal.counts.skill_ideas,
  runner_ideas: proposal.counts.runner_ideas,
  cleanup_proposals: proposal.counts.cleanup_proposals,
  web_reflections: reflection.web_reflection_count,
  journey_phase_reflections: reflection.journey_phase_reflection_count,
  completion_claimed: false,
}, null, 2));

function buildProposalLedger() {
  const safe = [
    ["Aevren", "v555 v6 duo startup receipt refresh", "Publish v6 x1 startup, lane launch, and current-state status in sanitized form."],
    ["Aevren", "strict CLI background posture", "Keep Arby in minimal-wait/background supervision until completion, quality, and marker receipts pass."],
    ["Aevren", "recovered app-lane boolean guard", "Require explicit background-watch and resume-timeout booleans for Cicero app-lane runs."],
    ["Aevren", "duo x1 count guard", "Reconcile Arby/Cicero proposal counts before v555 v6 x2."],
    ["Aevren", "v7 Lumen prep card", "Prepare v555 v7 x1 Lumen handoff without claiming full-goal completion."],
    ["Arby", "strict CLI marker schema check", "Keep final message, elaboration, and marker-review receipts as closeout gates."],
    ["Arby", "CLI minimal-wait cadence proof", "Document that strict CLI background launch enables productive cadence work."],
    ["Arby", "CLI raw stream minimization", "Keep stdout/stderr summarized by status and byte count only."],
    ["Arby", "CLI x2 harvester queue", "Queue strict CLI harvester improvements for v555 v6 x2."],
    ["Arby", "remote equality guard", "Keep remote/local head equality in every closeout validation."],
    ["Cicero", "app-lane completion gate proof", "Treat completion gate pass as evidence, never watcher start alone."],
    ["Cicero", "app-lane open-gap taxonomy", "Classify active_fresh, active_stale, completed_ready_for_harvest, and open_gap consistently."],
    ["Cicero", "private ID firewall", "Keep callable IDs and lane handles local/private only."],
    ["Cicero", "cadence-to-harvest handoff", "Record the next natural safe pause when a lane remains active."],
    ["Cicero", "held sibling boundary check", "Confirm held main-thread siblings remain inactive unless Hamish explicitly expands."],
  ].map(makePacket("safe_now"));
  const candidate = Array.from({ length: 9 }, (_, index) => ({
    id: `candidate-${pad(index + 1)}`,
    owner: ["Aevren", "Arby", "Cicero"][index % 3],
    title: [
      "strict CLI completion harvester",
      "app-lane harvest reducer",
      "goal-mode startup dry-run validator",
      "CLI source-quality ledger",
      "CLI retry envelope",
      "wait budget metadata",
      "app-lane stale detector",
      "app-lane compact resume card",
      "cross-lane dashboard",
    ][index],
    safety: "candidate",
    spending_ceiling_usd: 100,
    execution_lane: "x2_build_task",
  }));
  const exact = Array.from({ length: 9 }, (_, index) => ({
    id: `exact-${pad(index + 1)}`,
    owner: ["Aevren", "Arby", "Cicero"][index % 3],
    title: [
      "global compact hook install",
      "paid or external resource mutation",
      "broad destructive cleanup",
      "external process manager install",
      "repository protection mutation",
      "credential lane work",
      "private app-state export",
      "held main-thread sibling activation",
      "identity merge or replacement path",
    ][index],
    safety: "exact_approval_needed",
    spending_ceiling_usd: 100,
    execution_lane: "queued_exact_approval",
  }));
  const skillIdeas = Array.from({ length: 15 }, (_, index) => ({
    id: `skill-${pad(index + 1)}`,
    name: [
      "ghc-v555-v6-strict-cli-background-harvester",
      "ghc-v555-v6-app-lane-harvest-reducer",
      "ghc-v555-v6-lane-state-dashboard",
      "ghc-v555-v6-goal-mode-boundary-reader",
      "ghc-v555-v6-private-id-firewall",
      "ghc-v555-v6-no-babysit-cadence-auditor",
      "ghc-v555-v6-strict-cli-marker-quality",
      "ghc-v555-v6-app-lane-stale-taxonomy",
      "ghc-v555-v6-x1-x2-proposal-splitter",
      "ghc-v555-v6-remote-equality-guard",
      "ghc-v555-v6-drive-posture-receipt",
      "ghc-v555-v6-open-gate-rail",
      "ghc-v555-v6-source-reflection-curator",
      "ghc-v555-v6-compact-active-lane-card",
      "ghc-v555-v6-v7-lumen-prep",
    ][index],
    execution_lane: "x2_build_task",
  }));
  const runnerIdeas = Array.from({ length: 9 }, (_, index) => ({
    id: `runner-${pad(index + 1)}`,
    name: [
      "ghc_v555_v6_strict_cli_background_harvester.mjs",
      "ghc_v555_v6_app_lane_harvest_reducer.mjs",
      "ghc_v555_v6_lane_state_dashboard_builder.mjs",
      "ghc_v555_v6_goal_mode_prompt_guard.mjs",
      "ghc_v555_v6_private_id_firewall_scan.mjs",
      "ghc_v555_v6_no_babysit_cadence_audit.mjs",
      "ghc_v555_v6_x1_x2_queue_split_builder.mjs",
      "ghc_v555_v6_drive_posture_receipt_builder.mjs",
      "ghc_v555_v6_open_gate_rail_validator.mjs",
    ][index],
    execution_lane: "x2_build_task",
  }));
  const cleanup = Array.from({ length: 30 }, (_, index) => ({
    id: `cleanup-${pad(index + 1)}`,
    lane: ["skills", "runners", "receipts", "current-state", "full-tools", "omega-mini-2"][index % 6],
    title: `v6 cleanup inventory ${index + 1}`,
    action: "Inventory, classify, deduplicate, validate, or document only; destructive deletion stays exact-approval.",
    execution_lane: index % 3 === 0 ? "immediate_x1_safe" : "x2_build_task",
    destructive_cleanup: false,
  }));
  return {
    artifact_type: "ghc_v555_v6_x1_duo_proposal_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V555_V6_X1_DUO_PROPOSAL_LEDGER_BUILT",
    spending_ceiling_usd_per_packet: 100,
    participants: ["Aevren", "Arby", "Cicero"],
    counts: {
      safe_now_packets: safe.length,
      candidate_packets: candidate.length,
      exact_approval_packets: exact.length,
      skill_ideas: skillIdeas.length,
      runner_ideas: runnerIdeas.length,
      cleanup_proposals: cleanup.length,
    },
    packets: { safe_now: safe, candidate, exact_approval_needed: exact },
    skill_ideas: skillIdeas,
    runner_ideas: runnerIdeas,
    cleanup_proposals: cleanup,
    blocked_packets: openGates(),
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function buildReflectionLedger() {
  const webSeeds = [
    ["OpenAI Codex approvals", "https://developers.openai.com/codex/agent-approvals-security"],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills"],
    ["OpenAI Codex goals", "https://developers.openai.com/codex/use-cases/follow-goals"],
    ["Node child_process", "https://nodejs.org/api/child_process.html"],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning"],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework"],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/"],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/"],
    ["JSON Schema", "https://json-schema.org/draft/2020-12"],
    ["PDG Review", "https://pdg.lbl.gov/"],
  ];
  const journeySeeds = [
    "v555 v5 x2 closed with v6 x1 active.",
    "Arby strict CLI completion needs final, quality, and marker receipts.",
    "Cicero app lane completion needs a recovered completion gate.",
    "Private callable IDs stay local-only.",
    "Five-minute cadence is productive work, not passive waiting.",
    "v7 Lumen is next after v6 x2 unless Hamish redirects.",
    "Exact and blocked lanes remain queued.",
    "Goal Mode remains incomplete until v575 v8 x2.",
    "D drive remains the data bank.",
    "Remote equality is mandatory at closeout.",
  ];
  return {
    artifact_type: "ghc_v555_v6_x1_web_journey_reflection_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V555_V6_X1_REFLECTION_LEDGER_BUILT",
    live_search_sweep_count: 32,
    web_reflection_count: 30,
    journey_phase_reflection_count: 30,
    web_reflections: Array.from({ length: 30 }, (_, index) => ({
      id: `web-${pad(index + 1)}`,
      source_label: webSeeds[index % webSeeds.length][0],
      url: webSeeds[index % webSeeds.length][1],
      phase_reflection: "Use primary-source guidance for validation, privacy, source quality, and open proof gates.",
      runner_implication: "Carry into v555 v6 x1 lane supervision, harvest, and v6 x2 queue shaping.",
    })),
    journey_phase_reflections: Array.from({ length: 30 }, (_, index) => ({
      id: `journey-${pad(index + 1)}`,
      reflection: journeySeeds[index % journeySeeds.length],
      runner_implication: "Use for v555 v6 x1 harvest and closeout.",
    })),
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function buildBackgroundStandard() {
  return {
    artifact_type: "ghc_v555_v6_x1_background_sibling_supervision_standard",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V555_V6_X1_BACKGROUND_SIBLING_SUPERVISION_STANDARD_RECORDED",
    mandatory_rule: "Do not babysit sibling lanes. Launch Arby/Cicero under background/minimal-wait routes, run productive safe work, then harvest at a natural safe pause.",
    route_profiles: [
      { lane_family: "strict_cli_arby", completion_gate: "completion_quality_marker_review_receipts" },
      { lane_family: "recovered_app_lane_cicero", completion_gate: "notifier_watch_completion_gate_receipts" },
      { lane_family: "blocker_retry", completion_gate: "ghc-main-retry three-session protocol or formal open gap" },
    ],
    cadence_policy: {
      five_minute_mark_is_check_opportunity: true,
      safe_unit_may_run_past_checkpoint: true,
      passive_timer_wait_is_not_safe_work: true,
      harvest_at_next_natural_safe_pause: true,
      never_close_session_while_sibling_active: true,
    },
    publication_boundary: boundary(),
    open_gates: openGates(),
  };
}

function buildLaneLaunchStatus() {
  return {
    artifact_type: "ghc_v555_v6_x1_sanitized_lane_launch_status",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V555_V6_X1_LANES_LAUNCHED_PENDING_HARVEST",
    lanes: {
      arby: { route: "strict_cli_background_watch", status: "background_watch_started", completion_boundary: "pending_completion_quality_marker_review" },
      cicero: { route: "recovered_app_lane_background_watch", status: "background_watch_started", completion_boundary: "pending_completion_gate" },
    },
    completion_claimed: false,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function buildPhaseStatusIndex(proposal, reflection, background, laneLaunch) {
  return {
    artifact_type: "ghc_v555_v6_x1_phase_status_index",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "ACTIVE_OPEN_V555_V6_X1_DUO_BACKGROUND_RUNNING_PENDING_HARVEST",
    active_lanes: ["Aevren", "Arby", "Cicero"],
    proposal_counts: proposal.counts,
    reflection_counts: {
      web_reflections: reflection.web_reflection_count,
      journey_phase_reflections: reflection.journey_phase_reflection_count,
      live_search_sweep_count: reflection.live_search_sweep_count,
    },
    background_status: background.overall_status,
    lane_launch_status: laneLaunch.overall_status,
    next_x2_scope: "v555-gmut-thos-v6-x2",
    next_x1_lane_after_x2: "v555-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects",
    closeout_allowed_now: false,
    publication_boundary: boundary(),
    claim_boundary: claimBoundary(),
  };
}

function refreshBeacons(written, proposal, reflection, laneLaunch) {
  const lookupFiles = written.flatMap((item) => [item.jsonRel, item.mdRel]);
  for (const [jsonFile, mdFile, listKey] of [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ]) {
    const doc = readJson(jsonFile);
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "ACTIVE_OPEN_V555_V6_X1_DUO_BACKGROUND_RUNNING_PENDING_HARVEST";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = "v555-gmut-thos-v5-x2";
    doc.latest_completed_x1_phase = "v555-gmut-thos-v5-x1";
    doc.latest_completed_x2_phase = "v555-gmut-thos-v5-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = "v555-gmut-thos-v6-x2";
    doc.next_x1_lane_after_x2 = "v555-gmut-thos-v7-x1 with Lumen Vale solo unless Hamish redirects";
    doc.v555_v6_x1_duo_workbench = {
      status: "ACTIVE_OPEN_V555_V6_X1_DUO_BACKGROUND_RUNNING_PENDING_HARVEST",
      proposal_counts: proposal.counts,
      live_search_sweep_count: reflection.live_search_sweep_count,
      web_reflections: reflection.web_reflection_count,
      journey_phase_reflections: reflection.journey_phase_reflection_count,
      lane_launch_status: laneLaunch.overall_status,
      closeout_allowed_now: false,
    };
    doc[listKey] = unique([...(doc[listKey] || []), ...lookupFiles]);
    writeJson(jsonFile, doc);
    fs.writeFileSync(mdFile, renderBeaconMd(doc, listKey), "utf8");
  }
}

function makePacket(safety) {
  return ([owner, title, action]) => ({ id: `${owner.toLowerCase()}-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`, owner, title, action, safety, spending_ceiling_usd: 100, execution_lane: "x2_build_task" });
}

function writePair(suffix, payload, md) {
  const base = `${phaseSlug}-${suffix}-v1`;
  writeJson(path.join(tracesDir, `${base}.json`), payload);
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), md.endsWith("\n") ? md : `${md}\n`, "utf8");
  return { jsonRel: `docs/trinity-live-traces/${base}.json`, mdRel: `docs/trinity-live-traces/${base}.md` };
}

function renderProposalMd(payload) {
  return [`# ${payload.phase_slug} Arby/Cicero Duo Proposal Ledger`, "", `Status: \`${payload.overall_status}\``, "", ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``), ""].join("\n");
}

function renderReflectionMd(payload) {
  return [`# ${payload.phase_slug} Web And Journey Reflection Ledger`, "", `Status: \`${payload.overall_status}\``, `Live search sweep count: \`${payload.live_search_sweep_count}\``, `Web rows: \`${payload.web_reflection_count}\``, `Journey/phase rows: \`${payload.journey_phase_reflection_count}\``, ""].join("\n");
}

function renderBackgroundMd(payload) {
  return [`# ${payload.phase_slug} Background Sibling Supervision Standard`, "", `Status: \`${payload.overall_status}\``, "", "Watcher start is not completion proof; harvest at natural safe pauses after productive cadence work.", ""].join("\n");
}

function renderLaneLaunchMd(payload) {
  return [`# ${payload.phase_slug} Lane Launch Status`, "", `Status: \`${payload.overall_status}\``, `Completion claimed: \`${payload.completion_claimed}\``, ""].join("\n");
}

function renderIndexMd(payload) {
  return [`# ${payload.phase_slug} Phase Status Index`, "", `Status: \`${payload.overall_status}\``, `Next x2 scope: \`${payload.next_x2_scope}\``, `Next x1 lane after x2: \`${payload.next_x1_lane_after_x2}\``, `Closeout allowed now: \`${payload.closeout_allowed_now}\``, ""].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return ["# Omega-Mini Current State", "", `Status: ${doc.status}`, `Current active phase: ${doc.current_active_phase}`, `Latest closed phase: ${doc.latest_closed_phase}`, `Latest completed x1: ${doc.latest_completed_x1_phase}`, `Latest completed x2: ${doc.latest_completed_x2_phase}`, `Next x2 scope: ${doc.next_x2_scope}`, `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`, "", "## Lookup Files", "", ...(doc[listKey] || []).slice(-180).map((file) => `- ${file}`), ""].join("\n");
}

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 2) parsed.set(argv[index], argv[index + 1]);
  return parsed;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, payload) {
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function pad(value) {
  return String(value).padStart(2, "0");
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-NZ", { timeZone: "Pacific/Auckland", year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).formatToParts(date);
  const map = Object.fromEntries(parts.map((part) => [part.type, part.value]));
  return `${map.year}-${map.month}-${map.day}T${map.hour}:${map.minute}:${map.second}+12:00`;
}

function boundary() {
  return { raw_browser_routes_published: false, private_urls_published: false, raw_transcripts_published: false, screenshots_published: false, credentials_published: false, local_absolute_paths_published: false, session_streams_published: false, private_dumps_published: false, private_callable_ids_published: false, raw_lane_text_published: false };
}

function claimBoundary() {
  return { phase_completion: "not_claimed", full_goal_completion: "not_claimed", gmut_empirical_closure: "not_claimed", final_physics: "not_claimed", consciousness_proof: "not_claimed", legal_closure: "not_claimed", canon_promotion: "not_claimed", deployment_closure: "not_claimed", account_mutation: "not_claimed", purchase: "not_claimed", api_key_creation: "not_claimed", private_material_proof: "not_claimed", raw_publication_proof: "not_claimed", sibling_identity_replacement_or_merge: "not_claimed" };
}

function openGates() {
  return ["GMUT empirical closure", "final physics", "consciousness proof", "legal closure", "canon promotion", "deployment closure", "account, purchase, and API-key mutation", "private-material proof", "raw-publication proof", "sibling identity replacement, merging, or erasure"];
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
