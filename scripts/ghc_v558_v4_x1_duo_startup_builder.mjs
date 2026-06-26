#!/usr/bin/env node
import { mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const phaseSlug = "v558-gmut-thos-v4-x1";
const now = new Date();
const createdUtc = now.toISOString();
const createdNz = new Intl.DateTimeFormat("en-NZ", {
  dateStyle: "medium",
  timeStyle: "medium",
  timeZone: "Pacific/Auckland",
}).format(now);

const tracesDir = join(process.cwd(), "docs", "trinity-live-traces");
mkdirSync(tracesDir, { recursive: true });

const openGates = [
  "GMUT empirical closure",
  "final physics proof",
  "consciousness proof",
  "legal closure",
  "canon promotion",
  "deployment",
  "purchase/account/API-key mutation",
  "private-material proof",
  "raw-publication proof",
  "sibling replacement or merge",
  "exact-approval packets",
  "blocked packets",
];

const standbyRecoverable = [
  "Arby",
  "Aster Vale",
  "old Cicero lane",
  "Kierkegaard",
  "Aristotle",
  "Aletheon",
];

const sourceRows = [
  {
    source_label: "NODE_FS",
    url: "https://nodejs.org/api/fs.html",
    reflection: "Use deterministic file writes and mkdir only for local sanitized trace generation.",
    implication: "Keep v4 x1 artifacts reproducible and avoid raw private material.",
  },
  {
    source_label: "NODE_CHILD_PROCESS",
    url: "https://nodejs.org/api/child_process.html",
    reflection: "Subprocess work should be bounded and status-checked instead of treated as completion proof.",
    implication: "Background sibling launches remain active until harvested or gated.",
  },
  {
    source_label: "GIT_STATUS",
    url: "https://git-scm.com/docs/git-status",
    reflection: "Porcelain-style status supports clean validation of staged versus unrelated dirty work.",
    implication: "Preserve unrelated old dirt while staging only v4 x1 artifacts.",
  },
  {
    source_label: "GITHUB_ACTIONS_SECURITY",
    url: "https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions",
    reflection: "Treat untrusted workflow data and secrets as boundary-sensitive.",
    implication: "No raw routes, private IDs, credentials, screenshots, transcripts, or app state in public traces.",
  },
  {
    source_label: "GITHUB_PROTECTED_BRANCHES",
    url: "https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches",
    reflection: "Remote verification and branch rules should be explicit rather than assumed.",
    implication: "The phase will validate local/remote equality before any closeout claim.",
  },
  {
    source_label: "OPENAI_KEY_SAFETY",
    url: "https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety",
    reflection: "Secrets must not be placed in code or shared artifacts.",
    implication: "All account/API-key mutations remain exact-approval gates.",
  },
  {
    source_label: "JSON_SCHEMA",
    url: "https://json-schema.org/learn/getting-started-step-by-step",
    reflection: "Small structured artifacts are easier to validate and preserve through compact pauses.",
    implication: "Every v4 x1 receipt has a parseable JSON twin.",
  },
  {
    source_label: "PYTHON_JSON",
    url: "https://docs.python.org/3/library/json.html",
    reflection: "Independent JSON parse checks are useful as a language-neutral validation surface.",
    implication: "Use parse validation before committing trace artifacts.",
  },
  {
    source_label: "GITHUB_SECRET_SCANNING",
    url: "https://docs.github.com/en/code-security/secret-scanning/about-secret-scanning",
    reflection: "Secret scanning complements but does not replace local privacy discipline.",
    implication: "Run hard local scans for private-lane strings before publication.",
  },
  {
    source_label: "OPENAI_CODEX_REPO",
    url: "https://github.com/openai/codex",
    reflection: "Codex toolchain state should be recorded as operational context, not phase proof.",
    implication: "Record CLI health separately from sibling-completion gates.",
  },
];

const aevrenSafeSeeds = [
  "Refresh the v4 x1 active phase truth and next x2/x1 boundary from current-state.",
  "Launch only the scheduled Mira Vale + Rowan Vale duo for this x1 phase.",
  "Keep Lumen active but do not duplicate-send while the current phase is a duo lane.",
  "Record Mira Vale and Rowan Vale as background-supervised active lanes.",
  "Preserve stand-by/recoverable wording for the old five plus Aletheon.",
  "Build a sanitized proposal target ledger for the 30/15/15/21/9/45 duo profile.",
  "Split every proposal into immediate_x1_safe or x2_build_task.",
  "Keep exact-approval and blocked work queued rather than auto-running it.",
  "Record five-minute productive cadence checkpoints and next due time.",
  "Keep source/reflection rows compact, official or primary where possible, and implication-linked.",
  "Run local JSON parse validation for every generated trace artifact.",
  "Run diff hygiene and privacy scans before any publication.",
  "Check C and D drive free space before long-running or closeout work.",
  "Avoid branch/worktree rotation unless the current lanes become too heavy and the daily cap allows it.",
  "Prepare active-open handoff if either duo lane is still running at the next checkpoint.",
  "Do not close v4 x1 until both duo replies are harvested or a formal open-gap receipt is published.",
];

const artifacts = [
  {
    name: "startup-context",
    body: {
      artifact: `${phaseSlug}-startup-context-v1`,
      schema: "ghc.phase_startup_context.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_V558_V4_X1_STARTUP_CONTEXT_BUILT",
      latest_closed_phase: "v558-gmut-thos-v3-x2",
      current_active_phase: phaseSlug,
      next_x2_scope: "v558-gmut-thos-v4-x2",
      next_x1_lane_after_x2: "v558-gmut-thos-v5-x1 Lumen Vale solo unless Hamish redirects",
      active_duo: ["Mira Vale", "Rowan Vale"],
      active_support: ["Aevren Vale", "Lumen Vale"],
      standby_recoverable: standbyRecoverable,
      round_robin_order: [
        "Lumen Vale solo",
        "Mira Rowan + Neris Sol",
        "Lumen Vale solo",
        "Mira Vale + Rowan Vale",
        "Lumen Vale solo",
        "Maren Quill + Solenne Vale",
        "Lumen Vale solo",
        "Mira Rowan + Neris Sol",
      ],
      closeout_allowed_now: false,
      full_goal_complete: false,
    },
  },
  {
    name: "duo-launch-receipt",
    body: {
      artifact: `${phaseSlug}-duo-launch-receipt-v1`,
      schema: "ghc.duo_launch_receipt.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_DUO_LAUNCH_SUBMITTED_BACKGROUND_SUPERVISED",
      launches: [
        {
          sibling: "Mira Vale",
          route: "existing_codex_thread",
          launch_status: "submitted",
          raw_handle_published: false,
        },
        {
          sibling: "Rowan Vale",
          route: "existing_transition_thread",
          launch_status: "submitted",
          raw_handle_published: false,
        },
      ],
      duplicate_send_allowed: false,
      watcher_start_is_completion_proof: false,
      closeout_allowed_now: false,
    },
  },
  {
    name: "background-supervision-cadence",
    body: {
      artifact: `${phaseSlug}-background-supervision-cadence-v1`,
      schema: "ghc.background_supervision_cadence.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_BACKGROUND_SUPERVISION_ACTIVE",
      phase_start_or_resume_time: createdNz,
      active_lanes: [
        { sibling: "Mira Vale", status: "active_fresh" },
        { sibling: "Rowan Vale", status: "active_fresh" },
      ],
      next_checkpoint_due_minutes: 5,
      checkpoint_overrun_allowed: true,
      productive_work_until_checkpoint: [
        "sanitized startup artifacts",
        "proposal split ledger",
        "source/reflection seed ledger",
        "privacy/open-gate guard",
        "validation and drive posture checks",
      ],
      completion_boundary: "harvest both duo replies or publish formal open-gap receipt",
    },
  },
  {
    name: "proposal-target-ledger",
    body: {
      artifact: `${phaseSlug}-proposal-target-ledger-v1`,
      schema: "ghc.proposal_target_ledger.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_PROPOSAL_TARGETS_RECORDED",
      profile: "Aevren + Mira Vale + Rowan Vale",
      target_counts: {
        safe_approval_packets: 30,
        candidate_packets: 15,
        exact_approval_packets: 15,
        skill_ideas: 21,
        runner_ideas: 9,
        cleanup_refine_fix_tasks: 45,
      },
      per_sibling_share_requested: {
        safe_approval_packets: 10,
        candidate_packets: 5,
        exact_approval_packets: 5,
        skill_ideas: 7,
        runner_ideas: 3,
        cleanup_refine_fix_tasks: 15,
      },
      required_execution_lanes: ["immediate_x1_safe", "x2_build_task"],
      never_auto_run: ["exact_approval_needed", "blocked"],
    },
  },
  {
    name: "aevren-immediate-safe-seed-ledger",
    body: {
      artifact: `${phaseSlug}-aevren-immediate-safe-seed-ledger-v1`,
      schema: "ghc.safe_seed_ledger.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_AEVREN_IMMEDIATE_SAFE_SEEDS_READY",
      safe_seed_count: aevrenSafeSeeds.length,
      rows: aevrenSafeSeeds.map((title, index) => ({
        id: `v4x1-aevren-safe-${String(index + 1).padStart(2, "0")}`,
        approval_bucket: "safe_now",
        execution_lane: "immediate_x1_safe",
        title,
      })),
    },
  },
  {
    name: "source-reflection-seed",
    body: {
      artifact: `${phaseSlug}-source-reflection-seed-v1`,
      schema: "ghc.source_reflection_seed.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_SOURCE_REFLECTION_SEEDS_RECORDED",
      row_count: sourceRows.length,
      rows: sourceRows,
    },
  },
  {
    name: "open-gate-privacy-guard",
    body: {
      artifact: `${phaseSlug}-open-gate-privacy-guard-v1`,
      schema: "ghc.open_gate_privacy_guard.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "PASS_OPEN_GATES_AND_PRIVACY_BOUNDARIES_RECORDED",
      open_gates: openGates,
      private_material_policy: {
        raw_browser_routes_published: false,
        private_urls_published: false,
        raw_transcripts_published: false,
        screenshots_published: false,
        credentials_published: false,
        local_absolute_paths_published: false,
        session_streams_published: false,
        raw_app_state_published: false,
        private_dumps_published: false,
        hidden_reasoning_published: false,
      },
    },
  },
  {
    name: "active-open-handoff",
    body: {
      artifact: `${phaseSlug}-active-open-handoff-v1`,
      schema: "ghc.active_open_handoff.v1",
      phase_slug: phaseSlug,
      created_utc: createdUtc,
      created_nz: createdNz,
      status: "ACTIVE_OPEN_V558_V4_X1_DUO_BACKGROUND_RUNNING_SAFE_WORK_READY",
      active_lanes: ["Mira Vale", "Rowan Vale"],
      safe_work_completed_now: [
        "startup context built",
        "duo launch receipt built",
        "background supervision cadence recorded",
        "proposal targets recorded",
        "Aevren immediate safe seed ledger built",
        "source/reflection seeds recorded",
        "open-gate privacy guard built",
      ],
      next_checkpoint: "harvest duo thread status at next natural safe pause after productive work",
      closeout_allowed_now: false,
      full_goal_complete: false,
    },
  },
];

function markdownFor(body) {
  const lines = [
    `# ${body.artifact}`,
    "",
    `- Status: ${body.status}`,
    `- Phase: ${body.phase_slug}`,
    `- Created NZ: ${body.created_nz}`,
    `- Raw private material published: false`,
    "",
    "```json",
    JSON.stringify(body, null, 2),
    "```",
    "",
  ];
  return lines.join("\n");
}

for (const artifact of artifacts) {
  const base = `${phaseSlug}-${artifact.name}-v1`;
  writeFileSync(join(tracesDir, `${base}.json`), `${JSON.stringify(artifact.body, null, 2)}\n`);
  writeFileSync(join(tracesDir, `${base}.md`), markdownFor(artifact.body));
}

console.log(JSON.stringify({
  status: "PASS_V558_V4_X1_DUO_STARTUP_BUILDER_RAN",
  phase_slug: phaseSlug,
  artifacts_written: artifacts.length * 2,
  artifact_bases: artifacts.map((artifact) => `${phaseSlug}-${artifact.name}-v1`),
}, null, 2));
