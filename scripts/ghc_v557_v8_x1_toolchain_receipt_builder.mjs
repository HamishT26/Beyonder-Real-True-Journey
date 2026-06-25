#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const tracesDir = path.join(repoRoot, "docs", "trinity-live-traces");
const omegaDir = path.join(repoRoot, "docs", "omega-mini-index");
const args = parseArgs(process.argv.slice(2));
const phaseSlug = args.get("--phase-slug") || "v557-gmut-thos-v8-x1";
const expectedCodexVersion = args.get("--expected-codex-version") || "0.142.2";
const generated = new Date();
const generatedUtc = generated.toISOString();
const generatedNz = nzTimestamp(generated);

const codexVersionRaw = runPowerShell("codex --version", { timeout: 60000 });
const npmRegistryVersion = runPowerShell("npm view @openai/codex version", { timeout: 120000 });
const npmGlobalList = runPowerShell("npm list -g @openai/codex --depth=0", { timeout: 120000 });
const driveHeadroom = collectDriveHeadroom();
const localCodexVersion = parseCodexVersion(codexVersionRaw.stdout);
const globalPackageVersion = parseGlobalPackageVersion(npmGlobalList.stdout);
const passed = localCodexVersion === expectedCodexVersion
  && npmRegistryVersion.stdout.trim() === expectedCodexVersion
  && globalPackageVersion === expectedCodexVersion
  && driveHeadroom.c.free_gb >= 18;

const payload = {
  artifact_type: "ghc_v557_v8_x1_toolchain_receipt",
  generated_utc: generatedUtc,
  generated_nz: generatedNz,
  phase_slug: phaseSlug,
  overall_status: passed ? "PASS_CODEX_CLI_0_142_2_VERIFIED" : "WARN_CODEX_CLI_VERSION_OR_HEADROOM_RECHECK_REQUIRED",
  expected_codex_version: expectedCodexVersion,
  codex_cli: {
    command_status: codexVersionRaw.status,
    local_version: localCodexVersion,
    raw_output_published: false,
  },
  npm_registry: {
    command_status: npmRegistryVersion.status,
    package: "@openai/codex",
    registry_version: npmRegistryVersion.stdout.trim() || null,
  },
  npm_global_install: {
    command_status: npmGlobalList.status,
    package: "@openai/codex",
    installed_version: globalPackageVersion,
    raw_global_path_published: false,
  },
  drive_headroom: driveHeadroom,
  c_drive_policy: {
    warning_cap_gb: 19,
    minimum_headroom_gb: 18,
    current_status: driveHeadroom.c.free_gb >= 19
      ? "PASS_ABOVE_WARNING_CAP"
      : driveHeadroom.c.free_gb >= 18
        ? "WARN_BETWEEN_WARNING_AND_MINIMUM"
        : "BLOCK_BELOW_MINIMUM",
  },
  d_drive_first_policy: true,
  publication_boundary: {
    local_absolute_paths_published: false,
    raw_private_material_published: false,
    credentials_published: false,
    private_browser_routes_published: false,
    private_callable_ids_published: false,
  },
};

const refs = writePair("toolchain-codex-cli-0-142-2-receipt", payload);
refreshBeacons(refs, payload);

process.stdout.write(JSON.stringify({
  status: payload.overall_status,
  codex_cli_version: payload.codex_cli.local_version,
  npm_registry_version: payload.npm_registry.registry_version,
  npm_global_version: payload.npm_global_install.installed_version,
  c_free_gb: payload.drive_headroom.c.free_gb,
  d_free_gb: payload.drive_headroom.d.free_gb,
}, null, 2) + "\n");

function refreshBeacons(refs, doc) {
  const specs = [
    [path.join(omegaDir, "omega-mini-current-state-v1.json"), path.join(omegaDir, "omega-mini-current-state-v1.md"), "current_lookup_files"],
    [path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.json"), path.join(omegaDir, "omega-mini-latest-updates-beacon-v1.md"), "latest_lookup_files"],
    [path.join(tracesDir, "ghc-current-state-beacon-v1.json"), path.join(tracesDir, "ghc-current-state-beacon-v1.md"), "lookup_files"],
  ];
  for (const [jsonFile, mdFile, listKey] of specs) {
    const data = readJson(jsonFile);
    data.updated_at = generatedNz;
    data.generated_utc = generatedUtc;
    data.v557_v8_x1_toolchain_receipt = {
      status: doc.overall_status,
      codex_cli_version: doc.codex_cli.local_version,
      npm_registry_version: doc.npm_registry.registry_version,
      npm_global_version: doc.npm_global_install.installed_version,
      c_drive_status: doc.c_drive_policy.current_status,
      raw_private_material_published: false,
    };
    data[listKey] = unique([...(data[listKey] || []), refs.json, refs.md]);
    writeJson(jsonFile, data);
    fs.writeFileSync(mdFile, renderBeaconMd(data, listKey), "utf8");
  }
}

function writePair(suffix, doc) {
  const base = path.join(tracesDir, `${phaseSlug}-${suffix}-v1`);
  writeJson(`${base}.json`, doc);
  fs.writeFileSync(`${base}.md`, renderArtifactMd(doc), "utf8");
  return {
    json: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.json`,
    md: `docs/trinity-live-traces/${phaseSlug}-${suffix}-v1.md`,
  };
}

function renderArtifactMd(doc) {
  return [
    `# ${doc.phase_slug} Codex CLI 0.142.2 Toolchain Receipt`,
    "",
    `Status: \`${doc.overall_status}\``,
    "",
    `Codex CLI version: \`${doc.codex_cli.local_version || "unknown"}\``,
    `npm registry @openai/codex version: \`${doc.npm_registry.registry_version || "unknown"}\``,
    `npm global @openai/codex version: \`${doc.npm_global_install.installed_version || "unknown"}\``,
    `C drive status: \`${doc.c_drive_policy.current_status}\``,
    `D drive first policy: \`${doc.d_drive_first_policy ? "true" : "false"}\``,
    "",
    "## Boundary",
    "",
    "No local absolute npm path, credential, private route, private callable ID, raw private material, account mutation, purchase, deployment, API key creation, history rewrite, or destructive cleanup was published or performed.",
    "",
  ].join("\n");
}

function renderBeaconMd(doc, listKey) {
  return [
    "# Omega-Mini Current State",
    "",
    `Status: ${doc.status}`,
    `Branch: ${doc.branch}`,
    `Full-tools support branch: ${doc.full_tools_support_branch}`,
    `Current active phase: ${doc.current_active_phase}`,
    `Latest closed phase: ${doc.latest_closed_phase}`,
    `Latest completed x1: ${doc.latest_completed_x1_phase}`,
    `Latest completed x2: ${doc.latest_completed_x2_phase}`,
    `Next x2 scope: ${doc.next_x2_scope}`,
    `Next x1 lane after x2: ${doc.next_x1_lane_after_x2}`,
    "",
    "## Toolchain Receipt",
    "",
    `Status: \`${doc.v557_v8_x1_toolchain_receipt?.status || "not_recorded"}\``,
    `Codex CLI version: \`${doc.v557_v8_x1_toolchain_receipt?.codex_cli_version || "not_recorded"}\``,
    `npm registry version: \`${doc.v557_v8_x1_toolchain_receipt?.npm_registry_version || "not_recorded"}\``,
    `C drive status: \`${doc.v557_v8_x1_toolchain_receipt?.c_drive_status || "not_recorded"}\``,
    "",
    "## Lookup Files",
    "",
    ...(doc[listKey] || []).slice(-240).map((ref) => `- ${ref}`),
    "",
  ].join("\n");
}

function collectDriveHeadroom() {
  const ps = [
    "-NoProfile",
    "-Command",
    "Get-PSDrive -Name C,D | ConvertTo-Json -Compress",
  ];
  const result = runText("powershell", ps, { timeout: 60000 });
  const rows = result.status === "ok" && result.stdout.trim() ? JSON.parse(result.stdout) : [];
  const list = Array.isArray(rows) ? rows : [rows];
  const byName = new Map(list.map((row) => [String(row.Name).toUpperCase(), row]));
  return {
    c: driveSummary(byName.get("C")),
    d: driveSummary(byName.get("D")),
  };
}

function driveSummary(row) {
  const free = Number(row?.Free || 0);
  const used = Number(row?.Used || 0);
  return {
    free_gb: Number((free / 1024 ** 3).toFixed(2)),
    used_gb: Number((used / 1024 ** 3).toFixed(2)),
  };
}

function runText(command, commandArgs, options = {}) {
  try {
    return {
      status: "ok",
      stdout: execFileSync(command, commandArgs, {
        encoding: "utf8",
        timeout: options.timeout || 60000,
        windowsHide: true,
      }),
    };
  } catch (error) {
    return {
      status: "error",
      stdout: "",
      error: String(error?.message || error).slice(0, 180),
    };
  }
}

function runPowerShell(command, options = {}) {
  return runText("powershell", ["-NoProfile", "-Command", command], options);
}

function parseCodexVersion(output) {
  const match = String(output || "").match(/(\d+\.\d+\.\d+)/);
  return match?.[1] || null;
}

function parseGlobalPackageVersion(output) {
  const match = String(output || "").match(/@openai\/codex@(\d+\.\d+\.\d+)/);
  return match?.[1] || null;
}

function readJson(file) {
  return JSON.parse(fs.readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function parseArgs(argv) {
  const out = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const key = argv[index];
    if (!key.startsWith("--")) continue;
    const value = argv[index + 1];
    if (!value || value.startsWith("--")) {
      out.set(key, "true");
    } else {
      out.set(key, value);
      index += 1;
    }
  }
  return out;
}

function nzTimestamp(date) {
  return new Intl.DateTimeFormat("en-NZ", {
    timeZone: "Pacific/Auckland",
    dateStyle: "medium",
    timeStyle: "medium",
    hour12: false,
  }).format(date);
}
