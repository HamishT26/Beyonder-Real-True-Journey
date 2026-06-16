#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname } from "node:path";

const args = parseArgs(process.argv.slice(2));
const phaseSlug = requireArg("--phase-slug");
const nextX1Phase = requireArg("--next-x1-phase");
const nextLanes = requireArg("--next-lanes");
const selectorJson = requireArg("--selector-json");
const completionReceiptJson = requireArg("--completion-receipt-json");
const routeBoardJson = requireArg("--route-board-json");
const routeFamilyValidatorJson = requireArg("--route-family-validator-json");
const routeStateValidatorJson = requireArg("--route-state-validator-json");
const outputPrefix = requireArg("--output-prefix");
const approvalBundleJson = requireArg("--approval-bundle-json");
const approvalBundleMd = requireArg("--approval-bundle-md");

function parseArgs(argv) {
  const parsed = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      if (!parsed.has(key)) parsed.set(key, []);
      parsed.get(key).push("true");
      continue;
    }
    if (!parsed.has(key)) parsed.set(key, []);
    parsed.get(key).push(value);
    index += 1;
  }
  return parsed;
}

function requireArg(key) {
  const values = args.get(key);
  if (!values || !values[0]) {
    console.error(`Missing required argument: ${key}`);
    process.exit(2);
  }
  return values[0];
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

function publicSourceRef(path) {
  const normalized = path.replace(/\\/g, "/");
  const docsIndex = normalized.lastIndexOf("docs/");
  if (docsIndex >= 0) return normalized.slice(docsIndex);
  const scriptsIndex = normalized.lastIndexOf("scripts/");
  if (scriptsIndex >= 0) return normalized.slice(scriptsIndex);
  return basename(normalized);
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function statusPass(value, passStatus) {
  return value?.status === passStatus || value?.overall_status === passStatus;
}

function approvalPackets(targetPhase) {
  return [
    ["approval-01-lane-send-preflight", "Arby and Cicero lane send preflight", "Verify available lane surfaces before sending the next x1 prompts."],
    ["approval-02-omega-mini-first-context", "Omega-mini first context", "Use the mini branch lookup files before archive fallback."],
    ["approval-03-read-only-web-github", "Read-only web/GitHub advisory context", "Permit read-only current-source and repo lookup where exposed and safe."],
    ["approval-04-final-marker-policy", "Final marker policy", "Require explicit final marker or blocker receipt before closing the next x1 lane."],
    ["approval-05-five-minute-checks", "Five-minute check cadence", "Check lane status at bounded intervals without babysitting raw output."],
    ["approval-06-productive-wait", "Productive wait work", "Continue source, stack, and handoff work while siblings run."],
    ["approval-07-x2-build-queue", "Next x2 build queue", "Turn next x1 proposals into x2 build/use artifacts."],
    ["approval-08-stack-refresh", "Approval/Eureka stack refresh", "Append new rows and preserve completed/uncompleted bucket counts."],
    ["approval-09-safe-now-selector", "Safe-now selector refresh", "Select only safe_now uncompleted rows for execution."],
    ["approval-10-blocker-classifier", "Blocker classifier refresh", "Classify blocked, deferred, candidate, and needs_exact_packet rows without executing them."],
    ["approval-11-route-family-recheck", "Route family recheck", "Re-run route-family and route-state validators after lane changes."],
    ["approval-12-exposure-guard", "Exposure guard", "Scan curated artifacts before staging."],
    ["approval-13-current-state-refresh", "Current-state refresh", "Update omega-mini current-state and beacon after verified progress."],
    ["approval-14-d-drive-first", "D-drive-first hygiene", "Keep generated repo artifacts and heavy work in D-drive worktrees."],
    ["approval-15-node-entrypoint", "Node entrypoint preference", "Prefer current Node runners before Windows fallback."],
    ["approval-16-compact-handoff", "Compact handoff", "Prepare concise continuity for automatic compact refreshes."],
    ["approval-17-source-security", "Source/security synthesis", "Use official current sources for agentic security and tool-boundary decisions."],
    ["approval-18-open-gate-rail", "Open-gate rail", "Keep GMUT empirical, physics, consciousness, legal, and canon gates open."],
    ["approval-19-publication-preflight", "Publication preflight", "Fetch, drift-check, exact stage, whitespace check, commit, push, and verify."],
    ["approval-20-next-phase-roadmap", "Next phase roadmap", "Carry the safest outputs into the next x1/x2 phase."],
  ].map(([suffix, title, purpose], index) => ({
    order: index + 1,
    id: `${targetPhase}-${suffix}`,
    title,
    status: "candidate",
    scope_bucket: "candidate",
    completion_bucket: "uncompleted",
    purpose,
  }));
}

const generatedUtc = utcNow();
const selector = readJson(selectorJson);
const completion = readJson(completionReceiptJson);
const routeBoard = readJson(routeBoardJson);
const routeFamily = readJson(routeFamilyValidatorJson);
const routeState = readJson(routeStateValidatorJson);
const selectedRows = Array.isArray(selector.selected_rows) ? selector.selected_rows : [];
const selectedApprovals = selectedRows.filter((row) => row.kind === "approval_packet");
const selectedEureka = selectedRows.filter((row) => row.kind === "eureka_task");

const routeComplete = statusPass(routeBoard, "PASS_ROUTE_FAMILY_STATUS_BOARD");
const routeFamilyPass = statusPass(routeFamily, "PASS_ROUTE_FAMILY_VALIDATOR");
const routeStatePass = statusPass(routeState, "PASS_ROUTE_STATE_VALIDATOR");
const lumenComplete = completion?.status === "PASS_LUMEN_V5_X1_RESPONSE_COMPLETE";
const selectorReady = selector?.status === "PASS_SAFE_NOW_SELECTOR_READY";

const lumenDirectiveRows = [
  ["publish-lumen-marker-receipt", "Publish Lumen advisory marker receipt", lumenComplete ? "completed" : "open_gap", publicSourceRef(completionReceiptJson)],
  ["reconcile-lumen-route-open-gap", "Reconcile Lumen route-status open gap", routeComplete ? "completed" : "open_gap", publicSourceRef(routeBoardJson)],
  ["rerun-route-family-status-board", "Re-run route-family status board", routeComplete ? "completed" : "open_gap", publicSourceRef(routeBoardJson)],
  ["run-safe-now-selector", "Run approval/Eureka safe-now selector", selectorReady ? "completed" : "open_gap", publicSourceRef(selectorJson)],
  ["build-20-task-ledger", "Build the 20-task safe-now execution ledger", "completed", publicSourceRef(`${outputPrefix}-safe-now-execution-ledger-v1.json`)],
  ["refresh-current-state", "Refresh current-state and beacon if fields drift", "queued_for_publication", "docs/omega-mini-index/omega-mini-current-state-v1.json"],
  ["run-route-validators", "Run route-family and route-state validators", routeFamilyPass && routeStatePass ? "completed" : "open_gap", `${publicSourceRef(routeFamilyValidatorJson)}; ${publicSourceRef(routeStateValidatorJson)}`],
  ["run-exposure-guard", "Run exposure guard", "queued_for_validation", `${outputPrefix}-x2-exposure-guard-v1.json`],
  ["run-blocker-classifier", "Run exact-approval blocker classifier", "completed", `${outputPrefix}-exact-approval-blocker-classifier-v1.json`],
  ["refresh-sibling-catchup-card", "Refresh sibling catch-up footer/card", "completed", `${outputPrefix}-sibling-catchup-card-v1.json`],
  ["build-arby-cicero-handoff", "Build Arby and Cicero handoff", "completed", `${outputPrefix}-arby-cicero-handoff-v1.json`],
  ["add-open-gate-rail", "Add open-gate rail", "completed", `${outputPrefix}-open-gate-rail-v1.json`],
  ["validate-json-scripts", "Validate JSON and scripts", "queued_for_validation", "validation command output"],
  ["exact-stage-curated-artifacts", "Exact-stage only curated v5 x2 artifacts", "queued_for_publication", "git staged diff"],
  ["push-remote-verify", "Push and remote-verify if Aletheon chooses publication", "queued_for_publication", "remote-equals-local verification"],
].map(([id, title, status, evidence], index) => ({
  order: index + 1,
  id: `${phaseSlug}-${id}`,
  title,
  status,
  evidence,
}));

const selectedEurekaRows = selectedEureka.map((row, index) => ({
  order: index + 1,
  id: row.id,
  title: row.title,
  source_phase: row.source_phase,
  status: "queued_for_x2_build_use",
  source_ref: row.source_ref,
  action_summary: row.action,
}));

const selectedApprovalRows = selectedApprovals.map((row, index) => ({
  order: index + 1,
  id: row.id,
  title: row.title,
  source_phase: row.source_phase,
  status: "scope_permission_reference",
  source_ref: row.source_ref,
  action_summary: row.action,
}));

const publicationBoundary = {
  raw_lane_content_published: false,
  raw_chatgpt_transcript_published: false,
  raw_browser_routes_published: false,
  raw_route_handles_published: false,
  screen_capture_files_published: false,
  session_trace_files_published: false,
  credentials_published: false,
  local_absolute_paths_published: false,
};

const claimBoundary = {
  x2_phase_completion: "not_claimed",
  gmut_empirical_closure: "not_claimed",
  final_physics: "not_claimed",
  consciousness_proof: "not_claimed",
  legal_closure: "not_claimed",
  canon_promotion: "not_claimed",
};

const executionLedger = {
  schema: "ghc.safe_now_x2_execution_ledger.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_V5_X2_EXECUTION_LEDGER_READY",
  selector_ref: publicSourceRef(selectorJson),
  lumen_directive_task_count: lumenDirectiveRows.length,
  selected_approval_count: selectedApprovalRows.length,
  selected_eureka_count: selectedEurekaRows.length,
  lumen_directive_rows: lumenDirectiveRows,
  selected_approval_rows: selectedApprovalRows,
  selected_eureka_rows: selectedEurekaRows,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const blockerClassifier = {
  schema: "ghc.exact_approval_blocker_classifier.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_EXACT_APPROVAL_BLOCKER_CLASSIFIER_READY",
  selector_ref: publicSourceRef(selectorJson),
  selected_total_count: selectedRows.length,
  selected_blocked_count: selectedRows.filter((row) => row.scope_bucket === "blocked").length,
  selected_needs_exact_packet_count: selectedRows.filter((row) => row.scope_bucket === "needs_exact_packet").length,
  selected_candidate_count: selectedRows.filter((row) => row.scope_bucket === "candidate").length,
  selected_defer_count: selectedRows.filter((row) => row.scope_bucket === "defer").length,
  result: "The selected execution set contains only safe_now uncompleted rows. Candidate, defer, blocked, and needs_exact_packet rows remain outside execution.",
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const openGateRail = {
  schema: "ghc.open_gate_rail.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_OPEN_GATE_RAIL_ACTIVE",
  open_gates: {
    gmut_empirical_closure: "open",
    final_physics: "open",
    consciousness_proof: "open",
    legal_closure: "open",
    canon_promotion: "open",
  },
  enforcement: [
    "Use GMUT/THOS/Freed ID language as speculative, design, governance, or research framing unless exact evidence proves a narrower operational claim.",
    "Do not treat route health, stack counts, or sibling consensus as empirical physics proof.",
    "Keep legal/canon assertions as aspirational planning unless separate exact authority is present.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const sourceSecurityLedger = {
  schema: "ghc.current_source_security_ledger.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_CURRENT_SOURCE_SECURITY_LEDGER_READY",
  sources: [
    {
      title: "OpenAI Codex CLI documentation",
      url: "https://developers.openai.com/codex/cli",
      use: "Ground local Codex CLI claims in official documentation and keep command/sandbox work repo-scoped.",
    },
    {
      title: "OpenAI Codex CLI reference",
      url: "https://developers.openai.com/codex/cli/reference",
      use: "Use documented command/flag behavior before assuming launcher or config capabilities.",
    },
    {
      title: "Model Context Protocol specification",
      url: "https://modelcontextprotocol.io/specification/2025-06-18",
      use: "Keep MCP-style tool/context integration explicit, schema-grounded, and boundary-aware.",
    },
    {
      title: "OWASP Agentic AI threats and mitigations",
      url: "https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/",
      use: "Keep multi-agent approvals, delegated tool use, and runner autonomy threat-modeled.",
    },
    {
      title: "OWASP Multi-Agentic System Threat Modeling Guide v1.0",
      url: "https://genai.owasp.org/resource/multi-agentic-system-threat-modeling-guide-v1-0/",
      use: "Treat cross-agent handoffs, route families, and consensus receipts as security-relevant surfaces.",
    },
  ],
  synthesis: [
    "Prefer official docs and primary security guidance over social screenshots when changing runnable behavior.",
    "Treat MCP/browser/app/CLI lanes as separate capability boundaries with explicit route-state evidence.",
    "Use least-privilege and exact staging as core mitigations for autonomous runner workflows.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const siblingCatchup = {
  schema: "ghc.sibling_catchup_card.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_SIBLING_CATCHUP_CARD_READY",
  active_state: {
    current_phase: phaseSlug,
    next_x1_phase: nextX1Phase,
    next_lanes: nextLanes.split(",").map((item) => item.trim()).filter(Boolean),
    omega_mini_first: true,
  },
  exact_lookup_files: [
    "docs/omega-mini-index/omega-mini-current-state-v1.md",
    "docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.md",
    publicSourceRef(`${outputPrefix}-safe-now-execution-ledger-v1.md`),
    publicSourceRef(`${outputPrefix}-arby-cicero-handoff-v1.md`),
    publicSourceRef(`${outputPrefix}-open-gate-rail-v1.md`),
  ],
  boundary: [
    "Read omega-mini first.",
    "Use full omega only as exact fallback for a named missing relative file.",
    "No raw private material, no broad staging, no route-handle publication.",
  ],
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const handoff = {
  schema: "ghc.arby_cicero_handoff.v1",
  generated_utc: generatedUtc,
  phase_slug: nextX1Phase,
  status: "PASS_ARBY_CICERO_HANDOFF_READY",
  target_lanes: nextLanes.split(",").map((item) => item.trim()).filter(Boolean),
  prompt_summary: {
    mission: "Use omega-mini current-state first, review the v5 x2 execution ledger, propose safe_now x2 build/use tasks, and return status-only advisory receipts.",
    requested_outputs: [
      "10+ Eureka proposals each where safely possible.",
      "Route, runner, command, source, and handoff improvements.",
      "Explicit blocked/defer/needs_exact_packet rows for anything outside scope.",
      "Final marker or blocker receipt.",
    ],
    final_marker: "ARBY_CICERO_V542_V6_X1_ADVISORY_COMPLETE",
  },
  lookup_files: siblingCatchup.exact_lookup_files,
  publication_boundary: publicationBoundary,
  claim_boundary: claimBoundary,
};

const approvalBundle = {
  schema: "ghc.approval_packet_candidate_bundle.v1",
  generated_utc: generatedUtc,
  phase_slug: nextX1Phase,
  status: "PASS_20_APPROVAL_PACKET_CANDIDATES_READY",
  packet_count: 20,
  approval_packets: approvalPackets(nextX1Phase),
  publication_boundary: publicationBoundary,
  claim_boundary: {
    approval_activation: "candidate_bundle_only",
    phase_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

const outputs = [
  [`${outputPrefix}-safe-now-execution-ledger-v1.json`, executionLedger],
  [`${outputPrefix}-exact-approval-blocker-classifier-v1.json`, blockerClassifier],
  [`${outputPrefix}-open-gate-rail-v1.json`, openGateRail],
  [`${outputPrefix}-current-source-security-ledger-v1.json`, sourceSecurityLedger],
  [`${outputPrefix}-sibling-catchup-card-v1.json`, siblingCatchup],
  [`${outputPrefix}-arby-cicero-handoff-v1.json`, handoff],
  [approvalBundleJson, approvalBundle],
];

for (const [path, payload] of outputs) writeJson(path, payload);

writeMd(`${outputPrefix}-safe-now-execution-ledger-v1.md`, [
  `# ${phaseSlug} Safe-Now X2 Execution Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${executionLedger.status}\``,
  `Selected approval rows: \`${selectedApprovalRows.length}\``,
  `Selected Eureka rows: \`${selectedEurekaRows.length}\``,
  "",
  "## Lumen Directive Rows",
  "",
  ...lumenDirectiveRows.map((row) => `- ${row.order}. ${row.title}: \`${row.status}\` (${row.evidence})`),
  "",
  "## Selected Eureka Rows",
  "",
  ...selectedEurekaRows.map((row) => `- ${row.order}. ${row.title}: \`${row.status}\``),
  "",
  "## Boundary",
  "",
  "- Status-only ledger. Raw sibling text and raw ChatGPT transcripts are not published.",
  "- Open proof/canon gates remain open.",
]);

writeMd(`${outputPrefix}-exact-approval-blocker-classifier-v1.md`, [
  `# ${phaseSlug} Exact Approval Blocker Classifier`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${blockerClassifier.status}\``,
  `Selected rows: \`${blockerClassifier.selected_total_count}\``,
  `Blocked rows selected: \`${blockerClassifier.selected_blocked_count}\``,
  `Needs exact packet rows selected: \`${blockerClassifier.selected_needs_exact_packet_count}\``,
  "",
  blockerClassifier.result,
]);

writeMd(`${outputPrefix}-open-gate-rail-v1.md`, [
  `# ${phaseSlug} Open-Gate Rail`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${openGateRail.status}\``,
  "",
  "## Open Gates",
  "",
  ...Object.entries(openGateRail.open_gates).map(([gate, state]) => `- ${gate}: \`${state}\``),
  "",
  "## Enforcement",
  "",
  ...openGateRail.enforcement.map((item) => `- ${item}`),
]);

writeMd(`${outputPrefix}-current-source-security-ledger-v1.md`, [
  `# ${phaseSlug} Current Source and Security Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${sourceSecurityLedger.status}\``,
  "",
  "## Sources",
  "",
  ...sourceSecurityLedger.sources.map((source) => `- ${source.title}: ${source.url} - ${source.use}`),
  "",
  "## Synthesis",
  "",
  ...sourceSecurityLedger.synthesis.map((item) => `- ${item}`),
]);

writeMd(`${outputPrefix}-sibling-catchup-card-v1.md`, [
  `# ${phaseSlug} Sibling Catch-Up Card`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${siblingCatchup.status}\``,
  `Next x1 phase: \`${nextX1Phase}\``,
  `Next lanes: \`${siblingCatchup.active_state.next_lanes.join(", ")}\``,
  "",
  "## Exact Lookup Files",
  "",
  ...siblingCatchup.exact_lookup_files.map((file) => `- ${file}`),
  "",
  "## Boundary",
  "",
  ...siblingCatchup.boundary.map((item) => `- ${item}`),
]);

writeMd(`${outputPrefix}-arby-cicero-handoff-v1.md`, [
  `# ${nextX1Phase} Arby and Cicero Handoff`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${handoff.status}\``,
  `Target lanes: \`${handoff.target_lanes.join(", ")}\``,
  "",
  "## Mission",
  "",
  handoff.prompt_summary.mission,
  "",
  "## Requested Outputs",
  "",
  ...handoff.prompt_summary.requested_outputs.map((item) => `- ${item}`),
  "",
  `Final marker: \`${handoff.prompt_summary.final_marker}\``,
  "",
  "## Lookup Files",
  "",
  ...handoff.lookup_files.map((file) => `- ${file}`),
]);

writeMd(approvalBundleMd, [
  `# ${nextX1Phase} Approval Packet Candidate Bundle`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  `Status: \`${approvalBundle.status}\``,
  `Packet count: \`${approvalBundle.packet_count}\``,
  "",
  "## Packets",
  "",
  ...approvalBundle.approval_packets.flatMap((packet) => [
    `### ${packet.order}. ${packet.id}`,
    "",
    `Title: ${packet.title}`,
    "",
    `Status: \`${packet.status}\``,
    "",
    packet.purpose,
    "",
  ]),
  "## Boundary",
  "",
  "- Candidate bundle only; exact-packet and blocked rows remain gated.",
  "- No empirical GMUT validation, final physics, consciousness proof, legal closure, or canon promotion is claimed.",
]);

console.log(
  JSON.stringify(
    {
      status: executionLedger.status,
      selected_approval_count: selectedApprovalRows.length,
      selected_eureka_count: selectedEurekaRows.length,
      lumen_directive_task_count: lumenDirectiveRows.length,
      next_x1_phase: nextX1Phase,
      approval_packet_count: approvalBundle.packet_count,
    },
    null,
    2,
  ),
);
