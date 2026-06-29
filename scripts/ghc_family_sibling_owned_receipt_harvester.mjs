#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { parseArgs, readJsonIfPresent, repoRoot, writeFamilyReceipt } from "./ghc_family_runner_common.mjs";

const args = parseArgs();
const root = args.get("--root") || repoRoot(import.meta.url);
const sourceReceipt = args.get("--source-receipt");
const sibling = args.get("--sibling") || "Mira Rowan";
const sourceX1 = args.get("--source-x1") || "v577-gmut-thos-v2-x1";
const sourceX2 = args.get("--source-x2") || "v577-gmut-thos-v2-x2";
const nextPhase = args.get("--next-phase") || "v577-gmut-thos-v3-x1";
const nextSibling = args.get("--next-sibling") || "Mira Vale";
const traceDir = join(root, "docs", "trinity-live-traces");
const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");

if (!sourceReceipt) {
  console.error("Usage: node scripts/ghc_family_sibling_owned_receipt_harvester.mjs --source-receipt <relative-json>");
  process.exit(2);
}

const receipt = readJsonIfPresent(root, sourceReceipt) || {};
const receiptStatus = receipt.status || receipt.overall_status || "";
const receiptSourceX1 = receipt.active_x1 || receipt.outputs?.sourceX1 || receipt.source_x1 || receipt.source_x1_phase;
const receiptSourceX2 = receipt.active_x2 || receipt.outputs?.closingX2 || receipt.phase_slug || receipt.source_x2;
const hasCompactCompletion = receiptStatus === "completed_ready_for_harvest";
const hasCloseoutBuilderCompletion = /^PASS_GHC_FAMILY_SOLO_X2_CLOSED/.test(receiptStatus);
const hasPrivateBoundary = receipt.validation?.private_material_published === false
  || receipt.publication_boundary?.raw_private_material_published === false;
const sharedBranchesClean = receipt.validation?.shared_branches_mutated !== true;
const majorGatesOpen = receipt.validation?.proof_canon_legal_deployment_account_api_key_purchase_private_raw_destructive_sibling_merge_gates_open === true
  || receipt.claim_boundary?.full_goal_completion === "not_claimed"
  || receipt.claim_boundary?.proof_canon_legal_deployment_account_api_key_private_gates === "open";
const checks = [
  { label: "source_receipt_present", status: existsSync(join(root, sourceReceipt)) ? "PASS" : "OPEN_GAP" },
  { label: "sibling_status_completed", status: hasCompactCompletion || hasCloseoutBuilderCompletion ? "PASS" : "OPEN_GAP", observed: receiptStatus },
  { label: "active_x1_matches", status: receiptSourceX1 === sourceX1 ? "PASS" : "OPEN_GAP", observed: receiptSourceX1 },
  { label: "active_x2_matches", status: receiptSourceX2 === sourceX2 ? "PASS" : "OPEN_GAP", observed: receiptSourceX2 },
  { label: "safe_count_or_closeout_evidence_present", status: receipt.counts?.safe >= 25 || hasCloseoutBuilderCompletion ? "PASS" : "OPEN_GAP", observed: receipt.counts?.safe || receipt.outputs?.closeoutClaimed },
  { label: "candidate_count_or_closeout_evidence_present", status: receipt.counts?.candidate >= 15 || hasCloseoutBuilderCompletion ? "PASS" : "OPEN_GAP", observed: receipt.counts?.candidate || receipt.outputs?.closeoutClaimed },
  { label: "private_material_not_published", status: hasPrivateBoundary ? "PASS" : "OPEN_GAP" },
  { label: "shared_branches_not_mutated", status: sharedBranchesClean ? "PASS" : "OPEN_GAP" },
  { label: "major_gates_open", status: majorGatesOpen ? "PASS" : "OPEN_GAP" }
];
const open = checks.filter((check) => check.status !== "PASS").map((check) => check.label);
const status = open.length === 0
  ? "PASS_GHC_FAMILY_SIBLING_OWNED_RECEIPT_HARVESTED"
  : "OPEN_GAP_GHC_FAMILY_SIBLING_OWNED_RECEIPT_NOT_HARVESTED";

const harvest = {
  artifact_type: "ghc_family_sibling_owned_receipt_harvest",
  generated_utc: generatedUtc,
  source_receipt: sourceReceipt,
  sibling,
  source_x1: sourceX1,
  source_x2: sourceX2,
  next_phase: nextPhase,
  next_sibling: nextSibling,
  status,
  checks,
  open_checks: open,
  counts: receipt.counts || {},
  validation: receipt.validation || {},
  handoff: receipt.handoff || {},
  exact_and_blocked_gates: "queued",
  publication_boundary: {
    raw_browser_routes_published: false,
    private_urls_published: false,
    private_ids_published: false,
    raw_transcripts_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
    raw_app_state_published: false,
    hidden_reasoning_published: false
  },
  claim_boundary: {
    full_v576_v600_goal_complete: false,
    proof_canon_legal_deployment_account_api_key_private_gates: "open"
  }
};

const baseName = `${sourceX2}-ghc-family-sibling-owned-receipt-harvest-v1`;
writePair(baseName, harvest, renderHarvest(harvest));

writeFamilyReceipt({
  root,
  phaseSlug: sourceX2,
  runnerName: "ghc_family_sibling_owned_receipt_harvester.mjs",
  purpose: "Harvest a sibling-owned solo x1/x2 receipt into main sanitized phase truth.",
  status,
  checks,
  outputs: {
    sourceReceipt,
    sibling,
    sourceX1,
    sourceX2,
    nextPhase,
    nextSibling,
    openChecks: open,
    harvestJson: `docs/trinity-live-traces/${baseName}.json`,
    harvestMd: `docs/trinity-live-traces/${baseName}.md`
  },
  note: "This harvester accepts only sanitized receipt fields and does not publish private thread handles or raw app state."
});

if (open.length === 0) {
  refreshBeacons([`docs/trinity-live-traces/${baseName}.json`, `docs/trinity-live-traces/${baseName}.md`]);
}

console.log(JSON.stringify({ status, source_x2: sourceX2, next_phase: nextPhase, next_sibling: nextSibling, open_checks: open }, null, 2));

function writePair(baseName, json, md) {
  mkdirSync(traceDir, { recursive: true });
  writeFileSync(join(traceDir, `${baseName}.json`), `${JSON.stringify(json, null, 2)}\n`, "utf8");
  writeFileSync(join(traceDir, `${baseName}.md`), md, "utf8");
}

function refreshBeacons(lookupFiles) {
  const targets = [
    ["docs/omega-mini-index/omega-mini-current-state-v1.json", "current_lookup_files"],
    ["docs/omega-mini-index/omega-mini-latest-updates-beacon-v1.json", "latest_lookup_files"],
    ["docs/trinity-live-traces/ghc-current-state-beacon-v1.json", "current_lookup_files"]
  ];
  for (const [relativePath, lookupKey] of targets) {
    const file = join(root, relativePath);
    if (!existsSync(file)) continue;
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
    doc.generated_utc = generatedUtc;
    doc.latest_closed_phase = sourceX2;
    doc.latest_completed_x1_phase = sourceX1;
    doc.latest_completed_x2_phase = sourceX2;
    doc.current_active_phase = nextPhase;
    doc.current_active_phase_status = `${nextSibling} handoff ready after ${sibling} owned receipt harvest`;
    doc.full_goal_complete = false;
    doc.latest_sibling_owned_receipt_harvest = {
      status,
      sibling,
      source_x1: sourceX1,
      source_x2: sourceX2,
      next_phase: nextPhase,
      next_sibling: nextSibling,
      exact_and_blocked_gates: "queued"
    };
    doc[lookupKey] = unique([...(doc[lookupKey] || []), ...lookupFiles]);
    doc.latest_action_summary = unique([
      `Harvested ${sibling} owned receipt for ${sourceX2}; ${nextPhase} is ready for ${nextSibling}.`,
      ...(doc.latest_action_summary || [])
    ]).slice(0, 140);
    writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`, "utf8");
  }
}

function renderHarvest(payload) {
  return `# ${payload.source_x2} ${payload.sibling} Owned Receipt Harvest

Status: \`${payload.status}\`

Source x1: \`${payload.source_x1}\`

Source x2: \`${payload.source_x2}\`

Next phase: \`${payload.next_phase}\` for ${payload.next_sibling}.

## Checks

${payload.checks.map((check) => `- ${check.label}: \`${check.status}\``).join("\n")}

Exact and blocked gates remain queued. No raw private material, private ids, local path values, screenshots, credentials, raw app state, or hidden reasoning are published.
`;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}
