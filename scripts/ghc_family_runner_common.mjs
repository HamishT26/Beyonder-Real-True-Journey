#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, join } from "node:path";

export function repoRoot(metaUrl) {
  return new URL("..", metaUrl).pathname.replace(/^\/([A-Za-z]:)/, "$1");
}

export function parseArgs(argv = process.argv) {
  const args = new Map();
  for (let index = 2; index < argv.length; index += 2) {
    args.set(argv[index], argv[index + 1]);
  }
  return args;
}

export function readJsonIfPresent(root, relativePath) {
  const file = join(root, relativePath);
  if (!existsSync(file)) return undefined;
  return JSON.parse(readFileSync(file, "utf8"));
}

export function writeFamilyReceipt({ root, phaseSlug, runnerName, purpose, status, checks = [], outputs = {}, note = "" }) {
  const generatedUtc = new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
  const traceDir = join(root, "docs", "trinity-live-traces");
  const receipt = {
    artifact_type: "ghc_family_runner_receipt",
    generated_utc: generatedUtc,
    phase_slug: phaseSlug,
    runner_name: runnerName,
    purpose,
    overall_status: status,
    checks,
    outputs,
    note,
    publication_boundary: {
      raw_browser_routes_published: false,
      private_urls_published: false,
      raw_transcripts_published: false,
      screenshots_published: false,
      credentials_published: false,
      local_absolute_paths_published: false,
      private_callable_ids_published: false,
      raw_private_material_published: false
    },
    claim_boundary: {
      full_goal_completion: "not_claimed",
      gmut_empirical_closure: "not_claimed",
      final_physics: "not_claimed",
      consciousness_proof: "not_claimed",
      legal_closure: "not_claimed",
      canon_promotion: "not_claimed",
      deployment_closure: "not_claimed",
      sibling_identity_replacement_or_merge: "not_claimed"
    }
  };
  const stem = `${phaseSlug}-${runnerName.replace(/\.mjs$/, "").replace(/_/g, "-")}-receipt-v1`;
  const jsonPath = join(traceDir, `${stem}.json`);
  const mdPath = join(traceDir, `${stem}.md`);
  mkdirSync(dirname(jsonPath), { recursive: true });
  writeFileSync(jsonPath, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
  writeFileSync(
    mdPath,
    [
      `# ${phaseSlug} ${runnerName}`,
      "",
      `Status: \`${status}\``,
      "",
      `Purpose: ${purpose}`,
      "",
      "## Checks",
      "",
      ...(checks.length ? checks.map((check) => `- ${check.label}: \`${check.status}\``) : ["- no checks recorded"]),
      "",
      "## Boundary",
      "",
      "No raw browser routes, private URLs, transcripts, screenshots, credentials, local absolute paths, private IDs, or raw private material are published. Major proof/canon/legal/deployment/account/private gates remain open.",
      ""
    ].join("\n"),
    "utf8"
  );
  console.log(JSON.stringify({ status, receipt: basename(jsonPath), checks: checks.length }, null, 2));
}
