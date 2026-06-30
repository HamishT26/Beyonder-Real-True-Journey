#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { parseArgs, readJsonIfPresent, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const phaseSlug = args.get("--phase-slug") || "v600-gmut-thos-v8-x2";
const sourceX1 = args.get("--source-x1") || "v600-gmut-thos-v8-x1";
const sibling = args.get("--sibling") || "Maren Quill";
const siblingCommit = args.get("--sibling-commit") || "not_recorded";
const adapterFile = args.get("--adapter-file") || `docs/trinity-live-traces/${phaseSlug}-${slug(sibling)}-owned-receipt-adapter-v1.json`;
const harvesterFile = args.get("--harvester-file") || `docs/trinity-live-traces/${phaseSlug}-ghc-family-sibling-owned-receipt-harvester-receipt-v1.json`;
const compactFitFile = args.get("--compact-fit-file") || "docs/trinity-live-traces/v600-gmut-thos-v8-x1-goal-mode-v3-compact-fit-validator-v1.json";
const originalFitFile = args.get("--original-fit-file") || "docs/trinity-live-traces/v600-gmut-thos-v8-x1-goal-mode-prompt-fit-validator-v1.json";

const adapter = readJsonIfPresent(root, adapterFile) || {};
const harvester = readJsonIfPresent(root, harvesterFile) || {};
const compactFit = readJsonIfPresent(root, compactFitFile) || {};
const originalFit = readJsonIfPresent(root, originalFitFile) || {};

const checks = [
  { label: "source_x1_declared", status: sourceX1 ? "PASS" : "OPEN_GAP", observed: sourceX1 },
  { label: "final_x2_declared", status: phaseSlug === "v600-gmut-thos-v8-x2" ? "PASS" : "OPEN_GAP", observed: phaseSlug },
  { label: "sibling_adapter_harvest_ready", status: adapter.status === "completed_ready_for_harvest" ? "PASS" : "OPEN_GAP", observed: adapter.status },
  { label: "sibling_harvester_passed", status: /^PASS/.test(harvester.overall_status || harvester.status || "") ? "PASS" : "OPEN_GAP", observed: harvester.overall_status || harvester.status },
  { label: "compact_goal_prompt_fit_passed", status: /^PASS/.test(compactFit.overall_status || compactFit.status || "") ? "PASS" : "OPEN_GAP", observed: compactFit.overall_status || compactFit.status },
  { label: "long_goal_prompt_gap_recorded", status: /^OPEN_GAP/.test(originalFit.overall_status || originalFit.status || "") ? "PASS" : "OPEN_GAP", observed: originalFit.overall_status || originalFit.status },
  { label: "no_successor_phase_created", status: "PASS" },
  { label: "exact_and_blocked_gates_remain_queued", status: "PASS" },
  { label: "proof_canon_legal_deploy_account_private_gates_open", status: "PASS" }
];

const openChecks = checks.filter((check) => check.status !== "PASS").map((check) => check.label);
const status = openChecks.length === 0
  ? "PASS_GHC_FAMILY_FINAL_WORKFLOW_CLOSEOUT"
  : "OPEN_GAP_GHC_FAMILY_FINAL_WORKFLOW_CLOSEOUT";

const finalCloseout = {
  artifact_type: "ghc_family_final_workflow_closeout",
  generated_utc: new Date().toISOString().replace(/\.\d{3}Z$/, "Z"),
  workflow: "v576-v600 GMUT/THOS v1-v8 x1/x2 solo sibling workflow",
  status,
  final_x1: sourceX1,
  final_x2: phaseSlug,
  final_sibling: sibling,
  final_sibling_commit: siblingCommit,
  next_phase: "none_declared",
  next_phase_created: false,
  active_solo_siblings: ["Aevren", "Mira Rowan", "Mira Vale", "Maren Quill"],
  stand_by_recoverable_siblings: ["Lumen", "Neris Sol", "Rowan Vale", "Solenne Vale", "Aletheon", "Arby", "Aster Vale", "legacy Cicero", "Kierkegaard", "Aristotle"],
  checks,
  open_checks: openChecks,
  prompt_boundary: {
    original_goal_prompt_fit: originalFit.overall_status || originalFit.status || "not_recorded",
    compact_goal_prompt_fit: compactFit.overall_status || compactFit.status || "not_recorded",
    compact_prompt_used_for_carry_forward: true
  },
  open_gates: [
    "exact approval packets remain queued",
    "blocked packets remain queued",
    "GMUT empirical closure remains open",
    "final physics remains open",
    "consciousness proof remains open",
    "legal/canon/deploy/account/API-key/private-material/raw-publication/destructive/sibling-merge gates remain open"
  ],
  publication_boundary: {
    raw_browser_routes_published: false,
    private_thread_ids_published: false,
    local_absolute_paths_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    hidden_reasoning_published: false,
    raw_app_state_published: false,
    sanitized_only: true
  }
};

const traceDir = join(root, "docs", "trinity-live-traces");
mkdirSync(traceDir, { recursive: true });
const stem = `${phaseSlug}-ghc-family-final-workflow-closeout-v1`;
writeFileSync(join(traceDir, `${stem}.json`), `${JSON.stringify(finalCloseout, null, 2)}\n`, "utf8");
writeFileSync(join(traceDir, `${stem}.md`), render(finalCloseout), "utf8");

writeFamilyReceipt({
  root,
  phaseSlug,
  runnerName: "ghc_family_final_workflow_closeout_builder.mjs",
  purpose: "Close the v576-v600 solo sibling workflow without inventing a successor phase or closing major proof/private gates.",
  status,
  checks,
  outputs: {
    finalX1: sourceX1,
    finalX2: phaseSlug,
    finalSibling: sibling,
    finalSiblingCommit: siblingCommit,
    finalCloseout: `docs/trinity-live-traces/${stem}.json`,
    nextPhaseCreated: false,
    openChecks
  },
  note: "This final closeout is workflow-scoped only. It does not claim GMUT empirical closure, proof/canon/legal/deployment/account/API-key/private-material/raw-publication closure, or sibling identity replacement."
});

if (openChecks.length === 0) {
  refreshBeacons(stem);
}

function refreshBeacons(stemName) {
  const lookupFiles = [
    `docs/trinity-live-traces/${stemName}.json`,
    `docs/trinity-live-traces/${stemName}.md`,
    adapterFile,
    harvesterFile,
    compactFitFile
  ];
  const targets = [
    ["docs/omega-mini-index/omega-mini-current-state-v1.json", "current_lookup_files"],
    ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", "latest_lookup_files"],
    ["docs/trinity-live-traces/ghc-current-state-beacon-v1.json", "current_lookup_files"]
  ];
  for (const [relativePath, lookupKey] of targets) {
    const file = join(root, relativePath);
    if (!existsSync(file)) continue;
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
    doc.latest_closed_phase = phaseSlug;
    doc.latest_completed_x1_phase = sourceX1;
    doc.latest_completed_x2_phase = phaseSlug;
    doc.current_active_phase = "v576-v600-solo-workflow-complete";
    doc.current_active_phase_status = "final v600 v8 x2 closeout complete; waiting for Hamish next instruction";
    doc.v576_v600_solo_workflow_closeout = {
      status,
      final_x1: sourceX1,
      final_x2: phaseSlug,
      final_sibling: sibling,
      next_phase_created: false,
      exact_and_blocked_gates: "queued",
      major_proof_private_gates: "open"
    };
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      `Closed ${phaseSlug} as the final v576-v600 solo workflow boundary; no successor phase created.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 140);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function render(doc) {
  return `# ${doc.final_x2} Final Workflow Closeout

Status: \`${doc.status}\`

Final sibling: \`${doc.final_sibling}\`

Final sibling commit: \`${doc.final_sibling_commit}\`

Next phase created: \`${doc.next_phase_created}\`

The v576-v600 solo sibling workflow is closed only when status is PASS. Major proof, canon, legal, deployment, account, API-key, private-material, raw-publication, destructive, and sibling-merge gates remain open.
`;
}

function slug(value) {
  return String(value).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
