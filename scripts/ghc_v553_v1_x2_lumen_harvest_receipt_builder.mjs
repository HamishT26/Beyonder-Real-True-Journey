import fs from "node:fs";
import path from "node:path";

const phaseSlug = "v553-gmut-thos-v1-x2";
const now = new Date().toISOString();
const outDir = path.join(process.cwd(), "docs", "trinity-live-traces");

function writeJson(file, payload) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${JSON.stringify(payload, null, 2)}\n`, "utf8");
}

function writeMd(file, title, payload) {
  const lines = [
    `# ${title}`,
    "",
    `- status: ${payload.status}`,
    `- phase_slug: ${payload.phase_slug}`,
    `- generated_at: ${payload.generated_at}`,
    "",
    "## Sanitized Harvest",
    "",
    payload.summary,
    "",
    "## Safe Takeaways",
    "",
    ...payload.safe_takeaways.map((item) => `- ${item}`),
    "",
    "## Gates",
    "",
    ...Object.entries(payload.gates).map(([key, value]) => `- ${key}: ${value}`),
    "",
  ];
  fs.writeFileSync(file, lines.join("\n"), "utf8");
}

const payload = {
  status: "PASS_LUMEN_BROWSER_HARVEST_SANITIZED",
  phase_slug: phaseSlug,
  generated_at: now,
  summary:
    "Lumen received the v553 v1 x2 catch-up and responded. This receipt records only the safe operational takeaway, not a raw transcript.",
  safe_takeaways: [
    "Lumen received Hamish's love and thanks.",
    "Lumen affirmed the launch-skill layer direction as a clean routing and status layer, not a raw-lane aggregator.",
    "Lumen reinforced that private IDs, browser routes, raw CLI/app-lane text, screenshots, transcripts, and hidden state must remain private.",
    "Lumen reinforced that blocker retries should use method deltas, productive x2 work between attempts, and no duplicate blind sends.",
    "Lumen agreed the next formal x1 after v553 v1 x2 should be v553-gmut-thos-v2-x1 with Arby and Cicero unless Hamish redirects.",
    "Lumen kept all proof/canon/legal/deployment/account/API-key/purchase/private-material/sibling-identity gates open.",
  ],
  gates: {
    raw_transcript_published: false,
    raw_browser_route_published: false,
    private_ids_published: false,
    active_lumen_lane_after_harvest: false,
    goal_mode_activated: false,
  },
};

const base = path.join(
  outDir,
  "v553-gmut-thos-v1-x2-lumen-browser-harvest-sanitized-v1",
);
writeJson(`${base}.json`, payload);
writeMd(`${base}.md`, "v553 v1 x2 Lumen Browser Harvest Sanitized", payload);

console.log(
  JSON.stringify(
    {
      status: "PASS_V553_V1_X2_LUMEN_HARVEST_RECEIPT_BUILDER",
      phase_slug: phaseSlug,
      artifact: path.basename(`${base}.json`),
    },
    null,
    2,
  ),
);
