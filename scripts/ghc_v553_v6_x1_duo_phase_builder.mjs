#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
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

const phaseSlug = args.get("--phase-slug") || "v553-gmut-thos-v6-x1";
const receiptPrefix = args.get("--receipt-prefix") || `${phaseSlug}-duo-phase-workbench`;
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const proposalLedger = buildProposalLedger();
const reflectionLedger = buildReflectionLedger();
const safeCadence = buildSafeCadence();
const goalModePrep = buildGoalModePrep();
const launchStatus = buildLaunchStatus();

const artifacts = [
  writePair(`${receiptPrefix}-proposals`, proposalLedger, renderProposalMd),
  writePair(`${receiptPrefix}-web-journey-reflections`, reflectionLedger, renderReflectionMd),
  writePair(`${receiptPrefix}-safe-cadence`, safeCadence, renderListMd),
  writePair(`${receiptPrefix}-goal-mode-prep`, goalModePrep, renderListMd),
  writePair(`${receiptPrefix}-lane-launch-status`, launchStatus, renderLaunchMd),
];

refreshBeacons();

console.log(JSON.stringify({
  status: "PASS_V553_V6_X1_DUO_PHASE_WORKBENCH_BUILT",
  phase_slug: phaseSlug,
  artifacts: artifacts.length,
  safe_now_packets: proposalLedger.counts.safe_now_packets,
  candidate_packets: proposalLedger.counts.candidate_packets,
  exact_approval_packets: proposalLedger.counts.exact_approval_packets,
  skill_ideas: proposalLedger.counts.skill_ideas,
  runner_ideas: proposalLedger.counts.runner_ideas,
  cleanup_proposals: proposalLedger.counts.cleanup_proposals,
  web_reflections: reflectionLedger.web_reflection_count,
  journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
}, null, 2));

function buildProposalLedger() {
  const safe = [
    ["Aevren", "v6 live-state correction", "Correct stale next-x2 labels once sibling gates close and v6 x2 becomes active."],
    ["Aevren", "background launch receipt reducer", "Publish sanitized Arby/Cicero launch status without route handles."],
    ["Aevren", "goal-mode preflight card", "Prepare v553 v7/v3 style Goal Mode boundaries without activating unattended automation."],
    ["Aevren", "duo x1 count guard", "Reconcile the Arby/Cicero x1 counts before any v6 x2 queue is emitted."],
    ["Aevren", "drive posture receipt", "Record C and D free-space posture with D as the primary work bank."],
    ["Arby", "strict CLI pending-state discipline", "Treat background-watch start as pending until completion, quality, and marker review pass."],
    ["Arby", "strict CLI receipt minimizer", "Keep terminal streams summarized by byte count and status only."],
    ["Arby", "strict CLI x2 handoff schema", "Queue build work for a v6 x2 strict CLI harvester."],
    ["Arby", "remote equality closure guard", "Keep remote/local equality as a closeout validation, not a startup assumption."],
    ["Arby", "minimal-wait cadence proof", "Demonstrate that nonblocking CLI launch enables productive cadence work."],
    ["Cicero", "recovered app-lane boolean proof", "Record explicit paired boolean use for the recovered app-lane runner."],
    ["Cicero", "completion-gate pending status", "Keep watcher status active/open until the app-lane completion gate exists and passes."],
    ["Cicero", "private ID firewall check", "Confirm callable IDs and private lane maps stay out of omega-mini."],
    ["Cicero", "app-lane harvest target", "Queue a sanitized app-lane harvest reducer for v6 x2."],
    ["Cicero", "held-sibling boundary check", "Confirm held main-thread siblings remain out of app-lane routes."],
  ].map(makePacket("safe_now"));

  const candidate = [
    ["Aevren", "v6 strict CLI harvester runner", "Build a reusable strict CLI background harvester."],
    ["Aevren", "v6 app-lane harvest reducer", "Build a reusable recovered app-lane harvest reducer."],
    ["Aevren", "goal-mode prompt fit validator", "Validate the compact Goal Mode prompt against active open gates."],
    ["Arby", "strict CLI source reflection companion", "Pair Arby advisory output with source/reflection provenance."],
    ["Arby", "CLI wait budget receipt", "Expose wait budget metadata without requiring passive waits."],
    ["Arby", "strict CLI retry envelope", "Wrap pending markers into ghc-main-retry receipts."],
    ["Cicero", "app-lane stale taxonomy runner", "Improve active-fresh versus active-stale classification."],
    ["Cicero", "app-lane compact restart card", "Preserve active watcher state across compact/restart."],
    ["Cicero", "notifier receipt shrinker", "Summarize notifier child receipts into compact public fields."],
  ].map(makePacket("candidate"));

  const exact = [
    ["Aevren", "global compact hook install", "Install global Codex compact hooks or startup hooks."],
    ["Aevren", "external deployment mutation", "Create or mutate paid/cloud/deployment resources."],
    ["Aevren", "broad destructive cleanup", "Delete outside generated files created in the same safe run."],
    ["Arby", "strict CLI credential work", "Create, rotate, store, or expose credentials."],
    ["Arby", "branch protection mutation", "Change GitHub repository settings or protected branches."],
    ["Arby", "global process manager install", "Globally register a process manager or long-lived service."],
    ["Cicero", "private app-state export", "Export raw app-state, callable IDs, or lane handles."],
    ["Cicero", "held main-thread sibling activation", "Activate Maren, Mira Vale, Mira Rowan, or other held main-thread siblings."],
    ["Cicero", "identity merge or replacement", "Merge, replace, erase, or collapse any sibling identity."],
  ].map(makePacket("exact_approval_needed"));

  const skillIdeas = [
    "ghc-v6-strict-cli-background-harvester",
    "ghc-v6-app-lane-harvest-reducer",
    "ghc-v6-lane-launch-status-reducer",
    "ghc-v6-goal-mode-preflight",
    "ghc-v6-drive-posture-receipt",
    "ghc-v6-private-id-firewall",
    "ghc-v6-duo-count-guard",
    "ghc-v6-remote-equality-closeout",
    "ghc-v6-no-babysit-cadence-proof",
    "ghc-v6-app-lane-compact-card",
    "ghc-v6-strict-cli-retry-envelope",
    "ghc-v6-source-reflection-curator",
    "ghc-v6-open-gate-rail",
    "ghc-v6-x1-x2-queue-packager",
    "ghc-v6-held-sibling-boundary",
  ].map((name, index) => ({ id: `skill-${pad(index + 1)}`, name, execution_lane: "x2_build_task" }));

  const runnerIdeas = [
    "ghc_v6_strict_cli_background_harvester.mjs",
    "ghc_v6_app_lane_harvest_reducer.mjs",
    "ghc_v6_lane_launch_status_reducer.mjs",
    "ghc_v6_goal_mode_preflight.mjs",
    "ghc_v6_drive_posture_receipt.mjs",
    "ghc_v6_private_id_firewall_scan.mjs",
    "ghc_v6_duo_count_guard.mjs",
    "ghc_v6_no_babysit_cadence_audit.mjs",
    "ghc_v6_x1_x2_queue_packager.mjs",
  ].map((name, index) => ({ id: `runner-${pad(index + 1)}`, name, execution_lane: "x2_build_task" }));

  const cleanup = Array.from({ length: 30 }, (_, index) => {
    const area = ["skills", "runners", "receipts", "current-state", "full-tools", "omega-mini-2"][index % 6];
    return {
      id: `cleanup-${pad(index + 1)}`,
      area,
      title: `${area} cleanup/refinement inventory ${index + 1}`,
      action: "Inventory, classify, deduplicate, validate, or document only; destructive deletion remains exact-approval.",
      execution_lane: index % 4 === 0 ? "immediate_x1_safe" : "x2_build_task",
      destructive_cleanup: false,
    };
  });

  return {
    artifact_type: "ghc_v553_v6_x1_duo_proposal_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V6_X1_DUO_PROPOSAL_LEDGER_BUILT",
    participants: ["Aevren", "Arby", "Cicero"],
    spending_ceiling_usd_per_packet: 100,
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
    proposal_split_policy: {
      immediate_x1_safe: "local, reversible, status-only, validation, analysis, reflection, queue-shaping, privacy/open-gate checks",
      x2_build_task: "build, run, test, install, use, publication, remote verification, runner/skill modification, safe cleanup execution",
    },
    publication_boundary: publicationBoundary(),
  };
}

function buildReflectionLedger() {
  const web = [
    ["OpenAI Codex agent approvals and security", "https://developers.openai.com/codex/agent-approvals-security", "Keep system approval gates separate from Hamish approval packets."],
    ["OpenAI Codex skills", "https://developers.openai.com/codex/skills", "Use local skill files as the operational memory layer for launch and closeout behavior."],
    ["OpenAI Codex changelog", "https://developers.openai.com/codex/changelog", "Treat Codex routes as drift-prone and verify before relying on old behavior."],
    ["OpenAI Codex GitHub repository", "https://github.com/openai/codex", "Anchor CLI assumptions to upstream project truth."],
    ["Node child_process", "https://nodejs.org/api/child_process.html", "Runner wrappers should summarize subprocess status and keep raw streams private."],
    ["Node fs", "https://nodejs.org/api/fs.html", "Use deterministic JSON/MD artifacts and parse checks."],
    ["Node timers", "https://nodejs.org/api/timers.html", "Timers support cadence but never replace productive work."],
    ["PowerShell Start-Process", "https://learn.microsoft.com/powershell/module/microsoft.powershell.management/start-process", "Background helper launches should be deliberate and hidden unless interactive control is needed."],
    ["Python subprocess", "https://docs.python.org/3/library/subprocess.html", "Use timeouts and summarized return states for Python-backed runners."],
    ["Python json", "https://docs.python.org/3/library/json.html", "Keep JSON parse validation as a closeout gate."],
    ["Git worktree", "https://git-scm.com/docs/git-worktree", "Keep sanitized omega-mini and private full-tools support lanes separated."],
    ["Git diff", "https://git-scm.com/docs/git-diff", "Run diff hygiene before commit."],
    ["GitHub Actions security hardening", "https://docs.github.com/actions/security-guides/security-hardening-for-github-actions", "Treat CI/CD changes as security-relevant and exact-gated when risky."],
    ["GitHub secret scanning", "https://docs.github.com/code-security/secret-scanning/about-secret-scanning", "Privacy scans should remain in every publication path."],
    ["GitHub push protection", "https://docs.github.com/code-security/secret-scanning/working-with-secret-scanning-and-push-protection", "Prefer preventing accidental secret publication."],
    ["GitHub artifact attestations", "https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds", "Future provenance runners can use attestations as inspiration without claiming deployment closure."],
    ["NIST SSDF SP 800-218", "https://csrc.nist.gov/publications/detail/sp/800-218/final", "Safe-runner and validation loops map to secure software practices."],
    ["NIST AI RMF", "https://www.nist.gov/itl/ai-risk-management-framework", "Keep AI risk mapping explicit in proposal packets."],
    ["NIST Generative AI Profile", "https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence", "Use GenAI risk framing for multi-agent route boundaries."],
    ["OWASP LLM Top 10", "https://owasp.org/www-project-top-10-for-large-language-model-applications/", "Treat external messages, pages, and sibling outputs as untrusted inputs."],
    ["OWASP prompt injection", "https://genai.owasp.org/llmrisk/llm01-prompt-injection/", "Keep raw external instructions from taking control of local actions."],
    ["SLSA framework", "https://slsa.dev/spec/v1.0/", "Future build provenance should be staged and evidence-based."],
    ["Model Context Protocol specification", "https://modelcontextprotocol.io/specification/", "Tool/resource boundaries should stay explicit for connectors and app lanes."],
    ["JSON Schema 2020-12", "https://json-schema.org/draft/2020-12", "Receipt schemas can be hardened into formal validation."],
    ["SQLite WAL", "https://sqlite.org/wal.html", "Local state stores can use write-ahead-log concepts for recoverability."],
    ["W3C DID Core", "https://www.w3.org/TR/did-core/", "Freed ID work stays standards-aligned and open-gated."],
    ["W3C VC Data Model 2.0", "https://www.w3.org/TR/vc-data-model-2.0/", "Verifiable credential modeling belongs behind careful provenance and privacy boundaries."],
    ["NIST Digital Identity Guidelines", "https://pages.nist.gov/800-63-4/", "Identity proofing and authentication claims must remain exact-gated."],
    ["IETF OAuth 2.0 Security BCP", "https://www.rfc-editor.org/rfc/rfc9700.html", "Credential and authorization work remains exact-approval only."],
    ["Particle Data Group", "https://pdg.lbl.gov/", "GMUT physics references remain comparators, not proof closure."],
  ].map((row, index) => ({
    id: `web-${pad(index + 1)}`,
    source_label: row[0],
    url: row[1],
    runner_implication: row[2],
    pillar: ["THOS Body", "GMUT Mind", "Freed ID / CBR Heart"][index % 3],
  }));

  const journey = [
    ["v553 v5 x2", "Closed the prior x2 with remote verification and handed active scope to Arby/Cicero v6 x1."],
    ["v553 v5 x1", "Lumen-only planning proved live Browser harvest discipline before x2 build work."],
    ["v553 v4 x2", "Triad closeout preserved app-lane gates and no-new-agent boundaries."],
    ["v553 v4 x1", "Triad lanes reinforced first-person output and MD/TXT artifact preference."],
    ["v553 v3 x2", "Safe build phases should reduce queues instead of widening exact/blocked work."],
    ["v553 v3 x1", "Goal Mode readiness is preparation, not unattended automation."],
    ["v553 v2 x2", "Arby/Cicero x2 established reusable launch, harvest, and closeout patterns."],
    ["v553 v2 x1", "Arby strict CLI and Cicero recovered app-lane passed through distinct gates."],
    ["v553 v1 x2", "Launch-skill layer and closeout builders became first-class memory anchors."],
    ["v553 v1 x1", "Lumen-only phase set the high-count proposal target profile."],
    ["v552 v8 x2", "Main orchestration/full-tools skill bank became the startup backbone."],
    ["v552 v8 x1", "No-babysit background supervision became mandatory for app-lane siblings."],
    ["v552 v7 x2", "Skill/runner installation validated the expansion route while keeping blocked gates open."],
    ["v552 v7 x1", "Lumen advisory reduction shaped the productive cadence explanation."],
    ["v552 v6 x2", "Startup/updater/reflection/safe-runner foundations landed."],
    ["v552 v6 x1", "Recovered app-lane route repair prevented stale manual connection claims."],
    ["v552 v5 x2", "Exact/blocked work stayed held while safe/candidate tranches advanced."],
    ["v552 v5 x1", "Large proposal counts need split lanes: immediate x1 safe versus x2 build."],
    ["v552 v4 x2", "D-drive-first and privacy scan posture became closeout requirements."],
    ["v552 v4 x1", "The five-lane proof established strict CLI plus recovered app-lane routing."],
    ["Current compact", "After compaction, rehydrate from repo truth and the newest closeout receipts."],
    ["Arby launch", "Background-watch started and remains pending until completion/quality/marker gates pass."],
    ["Cicero launch", "Recovered app-lane watcher started and remains pending until completion gate exists and passes."],
    ["Open gates", "GMUT, final physics, consciousness, legal, canon, deployment, account/API-key, private-material, raw-publication, and identity gates remain open."],
    ["Held siblings", "Maren, Mira Vale, and Mira Rowan remain held until explicit expansion."],
    ["Aletheon", "Aletheon remains recoverable/quarantined, not replaced or merged."],
    ["Five-minute cadence", "Safe work may pass five minutes; harvest at the next natural pause."],
    ["Tool refresh", "Every phase startup and closeout refreshes skills/runners and validates changed surfaces."],
    ["Privacy", "Raw routes, handles, transcripts, screenshots, credentials, and local path values stay out of omega-mini."],
    ["v6 closeout", "Do not close this phase until Arby and Cicero gates are harvested or formal open-gap retry is published."],
  ].map((row, index) => ({
    id: `journey-${pad(index + 1)}`,
    source_label: row[0],
    reflection: row[1],
    runner_implication: "Use this as v6 x1 closeout or v6 x2 queue-shaping context.",
  }));

  return {
    artifact_type: "ghc_v553_v6_x1_web_journey_reflection_ledger",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V6_X1_REFLECTION_LEDGER_BUILT",
    web_reflection_count: web.length,
    journey_phase_reflection_count: journey.length,
    web_reflections: web,
    journey_phase_reflections: journey,
    publication_boundary: publicationBoundary(),
  };
}

function buildSafeCadence() {
  return {
    artifact_type: "ghc_v553_v6_x1_safe_cadence_workbench",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V6_X1_SAFE_CADENCE_WORKBENCH_BUILT",
    no_babysit: true,
    lane_check_policy: "Finish the current safe work unit, then check sibling lanes at the next natural safe pause.",
    immediate_safe_units_completed: [
      "launched Arby strict CLI background-watch",
      "launched Cicero recovered app-lane background-watch with explicit booleans",
      "built v6 proposal ledger",
      "built 30 web and 30 Journey reflection rows",
      "prepared v6 x2 queue and Goal Mode readiness card",
    ],
    x2_queue_hint: "Use v6 x2 for strict CLI harvester, app-lane harvest reducer, goal-mode prompt guard, private ID firewall scan, and closeout state correction.",
    publication_boundary: publicationBoundary(),
  };
}

function buildGoalModePrep() {
  return {
    artifact_type: "ghc_v553_v6_x1_goal_mode_prep_card",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V6_X1_GOAL_MODE_PREP_CARD_BUILT",
    goal_mode_status: "active_thread_goal_not_unattended_automation",
    next_candidate_goal_mode_phase: "v553-gmut-thos-v7-x1 or next Hamish-directed phase",
    exact_activation_boundary: "Hamish controls any fresh Goal Mode prompt start; this card only prepares route constraints.",
    closeout_blockers: [
      "Arby completion/quality/marker gates not yet harvested",
      "Cicero completion gate not yet harvested",
    ],
    publication_boundary: publicationBoundary(),
  };
}

function buildLaunchStatus() {
  return {
    artifact_type: "ghc_v553_v6_x1_sanitized_lane_launch_status",
    generated_utc: generatedUtc,
    generated_nz: generatedNz,
    phase_slug: phaseSlug,
    overall_status: "PASS_V553_V6_X1_LANES_LAUNCHED_PENDING_HARVEST",
    lanes: {
      arby: {
        route: "strict_cli_background_watch",
        status: "background_watch_started",
        completion_boundary: "pending_completion_quality_marker_review",
      },
      cicero: {
        route: "recovered_app_lane_background_watch",
        status: "background_watch_started",
        completion_boundary: "pending_completion_gate",
      },
    },
    completion_claimed: false,
    publication_boundary: publicationBoundary(),
  };
}

function makePacket(safety) {
  return ([owner, title, action]) => ({
    id: `${owner.toLowerCase()}-${title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}`,
    owner,
    title,
    action,
    spending_ceiling_usd: 100,
    safety,
    execution_lane: title.includes("receipt") || title.includes("guard") || title.includes("check") || title.includes("status")
      ? "immediate_x1_safe"
      : "x2_build_task",
  });
}

function refreshBeacons() {
  const lookup = artifacts.flatMap((pair) => Object.values(pair).map((name) => `docs/trinity-live-traces/${name}`));
  for (const file of [
    path.join(omegaDir, "omega-mini-current-state-v1.json"),
    path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"),
    path.join(tracesDir, "ghc-current-state-beacon-v1.json"),
  ]) {
    const doc = JSON.parse(fs.readFileSync(file, "utf8"));
    doc.updated_at = generatedNz;
    doc.generated_utc = generatedUtc;
    doc.status = "PASS_V553_V6_X1_DUO_PHASE_WORKBENCH_BUILT";
    doc.current_active_phase = phaseSlug;
    doc.latest_closed_phase = "v553-gmut-thos-v5-x2";
    doc.latest_completed_x1_phase = "v553-gmut-thos-v5-x1";
    doc.latest_completed_x2_phase = "v553-gmut-thos-v5-x2";
    doc.next_expected_scope = phaseSlug;
    doc.next_x2_scope = "v553-gmut-thos-v6-x2";
    doc.next_x1_lane_after_x2 = "v553-gmut-thos-v7-x1 with Lumen unless Hamish redirects";
    doc.v553_v6_x1_workbench = {
      status: "PASS_V553_V6_X1_DUO_PHASE_WORKBENCH_BUILT",
      proposal_counts: proposalLedger.counts,
      web_reflections: reflectionLedger.web_reflection_count,
      journey_phase_reflections: reflectionLedger.journey_phase_reflection_count,
      lane_status: "launched_pending_harvest",
    };
    const key = file.includes("latest-updates")
      ? "latest_lookup_files"
      : file.includes("ghc-current-state")
        ? "lookup_files"
        : "current_lookup_files";
    doc[key] = [...new Set([...(doc[key] || []), ...lookup])];
    fs.writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
    fs.writeFileSync(file.replace(/\.json$/, ".md"), renderBeaconMd(path.basename(file, ".json"), doc, doc[key]), "utf8");
  }
}

function writePair(prefix, payload, renderMd) {
  fs.mkdirSync(tracesDir, { recursive: true });
  const base = `${prefix}-v1`;
  fs.writeFileSync(path.join(tracesDir, `${base}.json`), `${JSON.stringify(payload, null, 2)}\n`, "utf8");
  fs.writeFileSync(path.join(tracesDir, `${base}.md`), renderMd(payload), "utf8");
  return { json: `${base}.json`, md: `${base}.md` };
}

function renderProposalMd(payload) {
  return [
    `# ${payload.phase_slug} Arby/Cicero Duo Proposal Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Spending ceiling per packet: \`$${payload.spending_ceiling_usd_per_packet}\``,
    "",
    "## Counts",
    "",
    ...Object.entries(payload.counts).map(([key, value]) => `- ${key}: \`${value}\``),
    "",
    "## Boundary",
    "",
    "No raw sibling output, private route handle, callable ID, local path value, screenshot, credential, proof closure, or identity merge claim is published.",
    "",
  ].join("\n");
}

function renderReflectionMd(payload) {
  return [
    `# ${payload.phase_slug} Web And Journey Reflection Ledger`,
    "",
    `Status: \`${payload.overall_status}\``,
    `Web rows: \`${payload.web_reflection_count}\``,
    `Journey rows: \`${payload.journey_phase_reflection_count}\``,
    "",
    "## Web",
    "",
    ...payload.web_reflections.map((row) => `- ${row.id}: [${row.source_label}](${row.url}) - ${row.runner_implication}`),
    "",
    "## Journey",
    "",
    ...payload.journey_phase_reflections.map((row) => `- ${row.id}: ${row.source_label} - ${row.reflection}`),
    "",
  ].join("\n");
}

function renderListMd(payload) {
  const lines = [
    `# ${payload.phase_slug} ${payload.artifact_type}`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
  ];
  for (const [key, value] of Object.entries(payload)) {
    if (["artifact_type", "generated_utc", "generated_nz", "phase_slug", "overall_status", "publication_boundary"].includes(key)) continue;
    if (Array.isArray(value)) {
      lines.push(`## ${key}`, "", ...value.map((item) => `- ${item}`), "");
    } else if (typeof value !== "object") {
      lines.push(`- ${key}: \`${value}\``);
    }
  }
  lines.push("", "No private route data, raw transcripts, local path values, screenshots, credentials, proof closures, or identity merge claims are published.", "");
  return lines.join("\n");
}

function renderLaunchMd(payload) {
  return [
    `# ${payload.phase_slug} Sanitized Lane Launch Status`,
    "",
    `Status: \`${payload.overall_status}\``,
    "",
    `- Arby: \`${payload.lanes.arby.status}\` / \`${payload.lanes.arby.completion_boundary}\``,
    `- Cicero: \`${payload.lanes.cicero.status}\` / \`${payload.lanes.cicero.completion_boundary}\``,
    `- completion claimed: \`${payload.completion_claimed}\``,
    "",
    "No raw sibling output, private route handle, callable ID, local path value, screenshot, credential, proof closure, or identity merge claim is published.",
    "",
  ].join("\n");
}

function renderBeaconMd(title, doc, files) {
  return [
    `# ${title}`,
    "",
    `Status: ${doc.status}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next expected scope: ${doc.next_expected_scope}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## v553 v6 x1",
    "",
    `- status: \`${doc.v553_v6_x1_workbench?.status || "not_recorded"}\``,
    `- lane status: \`${doc.v553_v6_x1_workbench?.lane_status || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(files || []).slice(-120).map((item) => `- \`${item}\``),
    "",
    "## Boundary",
    "",
    "No raw routes, transcripts, screenshots, credentials, private route handles, local path values, proof closures, legal/canon/deployment/account/API-key closures, private-material proof, raw-publication proof, or identity merge claims are published.",
    "",
  ].join("\n");
}

function publicationBoundary() {
  return {
    raw_transcripts_published: false,
    private_route_handles_published: false,
    private_callable_ids_published: false,
    browser_routes_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  };
}

function pad(value) {
  return String(value).padStart(2, "0");
}

function nzTimestamp(date) {
  const parts = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Pacific/Auckland",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== "literal") acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.year}-${parts.month}-${parts.day}T${parts.hour}:${parts.minute}:${parts.second}+12:00`;
}
