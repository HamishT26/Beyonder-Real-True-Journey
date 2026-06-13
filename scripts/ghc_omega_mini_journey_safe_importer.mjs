#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

function parseArgs(argv) {
  const args = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) {
      args.set(key, "true");
    } else {
      args.set(key, next);
      index += 1;
    }
  }
  return args;
}

function requireArg(args, key) {
  const value = args.get(key);
  if (!value) {
    console.error(`Missing required argument --${key}`);
    process.exit(2);
  }
  return value;
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function listJourneyFiles(sourceDirs) {
  const seen = new Map();
  for (const sourceDir of sourceDirs) {
    if (!fs.existsSync(sourceDir)) continue;
    for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
      if (!entry.isFile()) continue;
      if (!/^Beyonder-Real-True Journey v.*\.txt$/i.test(entry.name)) continue;
      const fullPath = path.join(sourceDir, entry.name);
      const stat = fs.statSync(fullPath);
      const current = seen.get(entry.name);
      if (!current || stat.mtimeMs > current.mtimeMs || stat.size > current.size) {
        seen.set(entry.name, {
          name: entry.name,
          fullPath,
          size: stat.size,
          mtimeMs: stat.mtimeMs,
        });
      }
    }
  }
  return [...seen.values()].sort((a, b) =>
    a.name.localeCompare(b.name, "en", { numeric: true, sensitivity: "base" }),
  );
}

const redactionRules = [
  {
    id: "token_shape",
    pattern: /sk-[A-Za-z0-9_-]{20,}/g,
    replacement: "[REDACTED_TOKEN]",
  },
  {
    id: "private_chatgpt_url",
    pattern: /https?:\/\/chatgpt\.com\/c\/[0-9A-Za-z:_-]+/gi,
    replacement: "[REDACTED_PRIVATE_CHAT_URL]",
  },
  {
    id: "local_absolute_path",
    pattern: /[A-Z]:[\\/](?:Users[\\/]hamis|GHC-Archives)[\\/][^\s"'<>)]*/gi,
    replacement: "[REDACTED_LOCAL_PATH]",
  },
  {
    id: "session_stream_extension",
    pattern: new RegExp(`\\.${"jsonl"}\\b`, "gi"),
    replacement: "[REDACTED_SESSION_FILE_EXT]",
  },
];

function redact(text) {
  const counts = Object.fromEntries(redactionRules.map((rule) => [rule.id, 0]));
  let safe = text;
  for (const rule of redactionRules) {
    safe = safe.replace(rule.pattern, () => {
      counts[rule.id] += 1;
      return rule.replacement;
    });
  }
  safe = `${safe.replace(/\r\n/g, "\n").replace(/\r/g, "\n").replace(/[ \t]+$/gm, "").replace(/\n+$/g, "")}\n`;
  return { safe, counts };
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

function writeMd(filePath, lines) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${lines.join("\n")}\n`, "utf8");
}

const args = parseArgs(process.argv.slice(2));
const sourceDirs = requireArg(args, "source-dirs").split(";").filter(Boolean);
const destTextsDir = requireArg(args, "dest-texts-dir");
const miniManifestJson = requireArg(args, "mini-manifest-json");
const miniManifestMd = requireArg(args, "mini-manifest-md");
const fullReceiptJson = requireArg(args, "full-receipt-json");
const fullReceiptMd = requireArg(args, "full-receipt-md");
const miniReceiptJson = requireArg(args, "mini-receipt-json");
const miniReceiptMd = requireArg(args, "mini-receipt-md");
const phaseSlug = requireArg(args, "phase-slug");

fs.mkdirSync(destTextsDir, { recursive: true });

const generatedUtc = new Date().toISOString();
const files = listJourneyFiles(sourceDirs);
const imported = [];
const totals = Object.fromEntries(redactionRules.map((rule) => [rule.id, 0]));

for (const file of files) {
  const raw = fs.readFileSync(file.fullPath, "utf8");
  const { safe, counts } = redact(raw);
  for (const [key, value] of Object.entries(counts)) {
    totals[key] += value;
  }
  const targetPath = path.join(destTextsDir, file.name);
  const existedBefore = fs.existsSync(targetPath);
  fs.writeFileSync(targetPath, safe, "utf8");
  imported.push({
    file_name: file.name,
    existed_before: existedBefore,
    source_sha256_12: sha256(raw).slice(0, 12),
    safe_sha256_12: sha256(safe).slice(0, 12),
    source_bytes: Buffer.byteLength(raw, "utf8"),
    safe_bytes: Buffer.byteLength(safe, "utf8"),
    redactions: counts,
  });
}

const manifest = {
  schema: "ghc.omega_mini_journey_safe_import_manifest.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_SAFE_JOURNEY_IMPORT",
  source_boundary: "user_supplied_journey_texts_only",
  destination_boundary: "omega_mini_journey_texts",
  imported_count: imported.length,
  redaction_totals: totals,
  imported,
  publication_boundary: {
    raw_session_streams_published: false,
    private_chat_urls_published: false,
    local_absolute_paths_published: false,
    credentials_published: false,
  },
};

const receipt = {
  schema: "ghc.omega_mini_journey_safe_import_receipt.v1",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  status: "PASS_SAFE_JOURNEY_IMPORT_RECEIPT",
  imported_count: imported.length,
  redaction_totals: totals,
  manifest_file: path.basename(miniManifestJson),
  carry_forward: [
    "Use omega-mini as the fast current-state branch.",
    "Keep full omega as the archival branch.",
    "Import Journey texts through the safe redaction path only.",
    "Do not publish raw session streams, credentials, private routes, screenshots, or local absolute paths.",
  ],
};

writeJson(miniManifestJson, manifest);
writeJson(fullReceiptJson, receipt);
writeJson(miniReceiptJson, receipt);

writeMd(miniManifestMd, [
  `# ${phaseSlug} Omega-Mini Journey Safe Import Manifest`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${manifest.status}\``,
  "",
  `Imported Journey text files: \`${imported.length}\``,
  "",
  "## Redactions",
  "",
  ...Object.entries(totals).map(([key, value]) => `- ${key}: \`${value}\``),
  "",
  "## Boundary",
  "",
  "Only user-supplied Journey text files were imported. Token-shaped strings, private ChatGPT URLs, local absolute paths, and session-stream filename extensions were redacted before writing to omega-mini.",
  "",
  "## Imported Files",
  "",
  ...imported.map((item) => `- ${item.file_name} | safe hash \`${item.safe_sha256_12}\``),
]);

const receiptMdLines = [
  `# ${phaseSlug} Omega-Mini Journey Safe Import Receipt`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Imported Journey text files: \`${receipt.imported_count}\``,
  "",
  "## Redactions",
  "",
  ...Object.entries(totals).map(([key, value]) => `- ${key}: \`${value}\``),
  "",
  "## Carry Forward",
  "",
  ...receipt.carry_forward.map((item) => `- ${item}`),
];

writeMd(fullReceiptMd, receiptMdLines);
writeMd(miniReceiptMd, receiptMdLines);

console.log(JSON.stringify({
  status: receipt.status,
  imported_count: imported.length,
  redaction_totals: totals,
}, null, 2));
