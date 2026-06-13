#!/usr/bin/env node
import { basename, dirname } from "node:path";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const sourcePhase = args.get("--source-phase");
const nextPhase = args.get("--next-phase");
const sourceReduction = args.get("--source-reduction");
const actionsJson = args.get("--actions-json");
const outputJson = args.get("--output-json");
const outputMd = args.get("--output-md");

if (!phaseSlug || !sourcePhase || !nextPhase || !actionsJson || !outputJson || !outputMd) {
  console.error(
    "Usage: node ghc_x2_build_use_action_ledger.mjs --phase-slug <slug> --source-phase <slug> --next-phase <slug> --actions-json <json> --output-json <json> --output-md <md> [--source-reduction <name>]",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function writeJson(path, payload) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(path, lines) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, `${lines.join("\n")}\n`, "utf8");
}

function readActions(path) {
  const parsed = JSON.parse(readFileSync(path, "utf8"));
  if (!Array.isArray(parsed.actions)) {
    throw new Error("actions-json must contain an actions array");
  }
  return parsed.actions.map((action, index) => ({
    id: String(action.id || `action-${String(index + 1).padStart(2, "0")}`),
    title: String(action.title || "untitled action"),
    category: String(action.category || "deferred"),
    outcome: String(action.outcome || "recorded"),
    evidence: String(action.evidence || "status-only"),
    mutation_performed: Boolean(action.mutation_performed),
    external_account_mutation: Boolean(action.external_account_mutation),
    raw_material_published: Boolean(action.raw_material_published),
  }));
}

const actions = readActions(actionsJson);
const actionCounts = actions.reduce((counts, action) => {
  counts[action.category] = (counts[action.category] || 0) + 1;
  return counts;
}, {});
const guardPass = actions.every(
  (action) => !action.external_account_mutation && !action.raw_material_published,
);

const payload = {
  schema: "ghc.x2_build_use_action_ledger.v1",
  generated_utc: utcNow(),
  phase_slug: phaseSlug,
  source_phase: sourcePhase,
  next_phase: nextPhase,
  source_reduction: sourceReduction || null,
  actions_source: basename(actionsJson),
  status: guardPass ? "PASS_X2_BUILD_USE_ACTION_LEDGER" : "OPEN_GAP_X2_BUILD_USE_ACTION_LEDGER",
  action_counts: actionCounts,
  actions,
  publication_boundary: {
    raw_lane_text_published: false,
    raw_stdout_stderr_published: false,
    raw_route_ids_published: false,
    screenshots_published: false,
    credentials_published: false,
    local_absolute_paths_published: false,
  },
  claim_boundary: {
    gmut_validation_claimed: false,
    final_physics_claimed: false,
    consciousness_proof_claimed: false,
    legal_closure_claimed: false,
    canon_promotion_claimed: false,
  },
};

writeJson(outputJson, payload);
writeMd(outputMd, [
  `# ${phaseSlug} X2 Build-Use Action Ledger`,
  "",
  `Generated UTC: \`${payload.generated_utc}\``,
  "",
  `Status: \`${payload.status}\``,
  "",
  `Source phase: \`${sourcePhase}\``,
  `Next phase: \`${nextPhase}\``,
  "",
  "## Actions",
  "",
  ...actions.map(
    (action) =>
      `- ${action.id}: ${action.title}. Category: \`${action.category}\`; outcome: ${action.outcome}; evidence: ${action.evidence}.`,
  ),
  "",
  "No raw lane text, stdout/stderr, raw route IDs, screenshots, credentials, local absolute paths, external account mutation, or closure claims are published here.",
]);

console.log(
  JSON.stringify(
    {
      status: payload.status,
      action_count: actions.length,
      action_counts: actionCounts,
    },
    null,
    2,
  ),
);
