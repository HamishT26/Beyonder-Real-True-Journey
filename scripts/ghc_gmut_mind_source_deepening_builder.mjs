#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname } from "node:path";

const args = new Map();
for (let index = 2; index < process.argv.length; index += 2) {
  args.set(process.argv[index], process.argv[index + 1]);
}

const phaseSlug = args.get("--phase-slug");
const sourceReviewJson = args.get("--source-review-json");
const receiptJson = args.get("--receipt-json");
const receiptMd = args.get("--receipt-md");

if (!phaseSlug || !sourceReviewJson || !receiptJson || !receiptMd) {
  console.error(
    "Usage: node ghc_gmut_mind_source_deepening_builder.mjs --phase-slug <slug> --source-review-json <json> --receipt-json <json> --receipt-md <md>",
  );
  process.exit(2);
}

function utcNow() {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

function readJson(path) {
  return JSON.parse(readFileSync(path, "utf8"));
}

const sourceReview = readJson(sourceReviewJson);
const generatedUtc = utcNow();

const sources = [
  {
    id: "desi-dr2-results-guide",
    title: "DESI DR2 results guide",
    url: "https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/",
    source_family: "DESI",
    source_type: "official collaboration result guide",
    gmut_mind_axis: "cosmic expansion and dark energy",
    current_signal:
      "DESI DR2 reports baryon acoustic oscillation measurements across galaxies, quasars, and the Lyman-alpha forest, with the collaboration presenting stronger constraints on dark energy than the first release.",
    action_for_v508:
      "Use DESI as an external calibration anchor for GMUT cosmology language: keep dark-energy ideas framed as model comparison and uncertainty, not closure.",
  },
  {
    id: "desi-dr2-lyman-alpha-paper",
    title: "DESI DR2 Lyman-alpha cosmology analysis",
    url: "https://arxiv.org/html/2510.21976v3",
    source_family: "DESI",
    source_type: "primary research preprint",
    gmut_mind_axis: "large-scale structure and expansion history",
    current_signal:
      "The paper analyzes DESI DR2 Lyman-alpha forest baryon acoustic oscillation measurements with galaxy BAO, supernova, and CMB likelihood inputs.",
    action_for_v508:
      "Represent late-time expansion claims as hypothesis rows that require dataset provenance, likelihood boundaries, and independent replication.",
  },
  {
    id: "ligo-gwtc5-publications",
    title: "LIGO Scientific Collaboration publications index",
    url: "https://pnp.ligo.org/ppcomm/Papers.html",
    source_family: "LIGO Virgo KAGRA",
    source_type: "official collaboration publications index",
    gmut_mind_axis: "gravitational waves and compact objects",
    current_signal:
      "The publications index lists GWTC-5.0 O4 catalog papers from May 2026, including catalog and compact-object population updates.",
    action_for_v508:
      "Use LVK catalog growth as a measurement fabric for gravity-facing GMUT reflection, while keeping event catalogs separate from theory validation.",
  },
  {
    id: "ligo-gwtc5-news",
    title: "GWTC-5.0 updated LIGO Virgo KAGRA catalog",
    url: "https://www.ligo.caltech.edu/news/ligo20260526",
    source_family: "LIGO Virgo KAGRA",
    source_type: "official collaboration news",
    gmut_mind_axis: "observational gravity",
    current_signal:
      "The May 2026 GWTC-5.0 update reports 161 new O4b gravitational-wave events and 390 confirmed events across the network since 2015.",
    action_for_v508:
      "Track gravity evidence as expanding observational coverage, not as proof of any aspirational unification framework.",
  },
  {
    id: "ligo-o4-completion",
    title: "LIGO Virgo KAGRA fourth observing run completion",
    url: "https://www.ligo.caltech.edu/news/ligo20251118",
    source_family: "LIGO Virgo KAGRA",
    source_type: "official collaboration news",
    gmut_mind_axis: "gravitational-wave observing cadence",
    current_signal:
      "The O4 run began in May 2023 and continued through November 2025, giving the collaboration a long baseline for gravitational-wave discoveries and population studies.",
    action_for_v508:
      "Use long observing runs as a process analogy for phase cadence: durable evidence emerges from repeated clean observations, not a single celebratory handoff.",
  },
  {
    id: "cern-lhc-status",
    title: "CERN Large Hadron Collider overview",
    url: "https://home.cern/science/accelerators/large-hadron-collider/",
    source_family: "CERN",
    source_type: "official accelerator overview",
    gmut_mind_axis: "high-energy particle physics",
    current_signal:
      "CERN describes the LHC Run 3 programme and the transition toward Long Shutdown 3 and High-Luminosity LHC upgrades.",
    action_for_v508:
      "Keep particle-physics claims tied to accelerator run status, detector evidence, and official analysis releases.",
  },
  {
    id: "cern-lhc-run3-tag",
    title: "CERN LHC Run 3 reports",
    url: "https://home.cern/tag/lhc-run-3/",
    source_family: "CERN",
    source_type: "official CERN topic feed",
    gmut_mind_axis: "accelerator performance and Run 3 evidence",
    current_signal:
      "CERN reports Run 3 performance milestones, special running conditions, and the end of the proton physics programme in 2026.",
    action_for_v508:
      "Use Run 3 as a concrete measurement-state timeline when drafting GMUT-facing physics reflections.",
  },
  {
    id: "atlas-run3-start",
    title: "ATLAS Run 3 start statement",
    url: "https://atlas.cern/Updates/Press-Statement/LHC-Run3-Starts",
    source_family: "ATLAS CERN",
    source_type: "official experiment statement",
    gmut_mind_axis: "detector programme and collision energy",
    current_signal:
      "ATLAS stated that LHC Run 3 began with proton collisions at 13.6 TeV, marking the start of a new data-taking period.",
    action_for_v508:
      "Use detector and run metadata as evidence scaffolding; avoid leaping from collision energy to any unification claim.",
  },
  {
    id: "euclid-q1-release",
    title: "Euclid Quick Data Release 1",
    url: "https://www.euclid-ec.org/science/q1/",
    source_family: "Euclid Consortium",
    source_type: "official mission data release",
    gmut_mind_axis: "cosmic structure survey data",
    current_signal:
      "Euclid Q1 released 63.1 square degrees of wide-survey science data in March 2025, with millions of detections for astrophysical studies rather than cosmology conclusions.",
    action_for_v508:
      "Treat Euclid Q1 as a data-product and pipeline readiness source, not as a cosmology-closeout source.",
  },
  {
    id: "euclid-data-timeline",
    title: "Euclid data release timeline",
    url: "https://euclid.caltech.edu/page/data-release-timeline",
    source_family: "Euclid Consortium",
    source_type: "official mission timeline mirror",
    gmut_mind_axis: "cosmology release planning",
    current_signal:
      "The timeline lists future Euclid releases including Q2 in June 2026 and DR1 in October 2026, with later releases extending into 2029 and 2031.",
    action_for_v508:
      "Use future Euclid releases as explicit open gates for any later cosmology synthesis and do not close those gates early.",
  },
  {
    id: "esa-euclid-home",
    title: "ESA Euclid mission portal",
    url: "https://www.cosmos.esa.int/web/euclid",
    source_family: "ESA",
    source_type: "official mission portal",
    gmut_mind_axis: "dark universe survey mission",
    current_signal:
      "ESA frames Euclid as a mission to map the geometry of the dark universe through galaxy imaging, spectroscopy, and large-scale survey products.",
    action_for_v508:
      "Use Euclid mission framing to keep GMUT cosmology aspirations anchored in survey geometry, instrument limits, and staged releases.",
  },
  {
    id: "euclid-max-planck-release",
    title: "Euclid first comprehensive data release overview",
    url: "https://www.mpg.de/24349746/euclid-data-release",
    source_family: "Max Planck Society",
    source_type: "research institution release",
    gmut_mind_axis: "Euclid data products and future cosmology",
    current_signal:
      "The release emphasizes that Q1 is a selected quick release and that the first cosmology data is expected in a later major release.",
    action_for_v508:
      "Make future-source gates explicit in phase ledgers so current reflection does not outrun the data release calendar.",
  },
  {
    id: "desi-evolving-dark-energy-analysis",
    title: "Evolving dark energy analysis with DESI DR2",
    url: "https://link.springer.com/article/10.1140/epjc/s10052-026-15806-w",
    source_family: "European Physical Journal C",
    source_type: "peer-reviewed research article",
    gmut_mind_axis: "dark energy model comparison",
    current_signal:
      "The article analyzes DESI DR2 measurements and dark-energy parameterizations, while discussing underconstrained inference and model sensitivity.",
    action_for_v508:
      "Use this as a caution source: model preference is not model proof, and underconstrained inference must stay visible in GMUT reflection.",
  },
];

const axisCoverage = sources.reduce((acc, source) => {
  acc[source.gmut_mind_axis] = (acc[source.gmut_mind_axis] || 0) + 1;
  return acc;
}, {});

const receipt = {
  artifact_type: "ghc_gmut_mind_source_deepening_ledger",
  generated_utc: generatedUtc,
  phase_slug: phaseSlug,
  source_review_input: sourceReviewJson,
  status: "GMUT_MIND_SOURCE_DEEPENING_READY_FOR_REVIEW",
  source_count_this_batch: sources.length,
  prior_source_review_status: sourceReview.status,
  prior_warning_count: sourceReview.warning_count,
  prior_warnings: sourceReview.warnings,
  gmut_closure_claimed: false,
  sources,
  axis_coverage: axisCoverage,
  reflections: [
    {
      id: "gmut-reflection-01-cosmology-open-gates",
      summary:
        "DESI and Euclid sources sharpen GMUT cosmology work by making expansion history, dark-energy model comparison, and release calendars explicit open gates.",
    },
    {
      id: "gmut-reflection-02-gravity-observation-fabric",
      summary:
        "LVK sources expand the gravity-facing observation fabric, but catalog growth remains evidence for gravitational-wave astronomy rather than proof of a unification candidate.",
    },
    {
      id: "gmut-reflection-03-accelerator-discipline",
      summary:
        "CERN and ATLAS sources reinforce that particle-physics reflection must track accelerator run status, detector analyses, and staged evidence rather than speculative closure.",
    },
    {
      id: "gmut-reflection-04-future-release-discipline",
      summary:
        "Euclid future release dates should become explicit future gates in phase ledgers, preventing v508-v515 synthesis from closing evidence that is not public yet.",
    },
    {
      id: "gmut-reflection-05-mind-body-heart-mapping",
      summary:
        "GMUT-mind sources improve the Mind pillar, but THOS/body runner provenance and Freed ID/heart consent boundaries still govern how any synthesis can be used.",
    },
  ],
  next_actions: [
    "Merge these GMUT-mind rows into the next source-review guard pass.",
    "Add a future-source gate ledger for Euclid DR1 and later DESI/LVK releases before any cosmology synthesis closeout.",
    "Create a model-comparison caution card that separates hypotheses, datasets, likelihood assumptions, and direct observations.",
    "Keep every empirical, physics, consciousness, legal, and canon gate open unless future exact closure artifacts prove otherwise.",
  ],
  publication_boundary: {
    raw_lane_text_published: false,
    raw_chatgpt_transcript_published: false,
    raw_app_server_result_published: false,
    raw_app_server_error_published: false,
    raw_callable_ids_published: false,
    raw_thread_ids_published: false,
    credentials_published: false,
    screenshots_published: false,
    local_absolute_paths_published: false,
    raw_user_text_published: false,
    copyrighted_source_dump_published: false,
  },
  claim_boundary: {
    phase_completion: "not_claimed",
    v508_full_phase_start: "not_claimed",
    x2_build_closeout: "not_claimed",
    source_target_completion: "not_claimed",
    gmut_empirical_closure: "not_claimed",
    final_physics: "not_claimed",
    consciousness_proof: "not_claimed",
    legal_closure: "not_claimed",
    canon_promotion: "not_claimed",
  },
};

mkdirSync(dirname(receiptJson), { recursive: true });
writeFileSync(receiptJson, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");

const md = [
  `# ${phaseSlug} GMUT Mind Source Deepening Ledger`,
  "",
  `Generated UTC: \`${generatedUtc}\``,
  "",
  `Status: \`${receipt.status}\``,
  "",
  `Source count this batch: \`${receipt.source_count_this_batch}\``,
  `GMUT closure claimed: \`${String(receipt.gmut_closure_claimed)}\``,
  "",
  "## Sources",
  "",
  ...sources.flatMap((source) => [
    `### ${source.id}: ${source.title}`,
    "",
    `URL: ${source.url}`,
    "",
    `Family: ${source.source_family}`,
    "",
    `Type: ${source.source_type}`,
    "",
    `GMUT mind axis: ${source.gmut_mind_axis}`,
    "",
    `Current signal: ${source.current_signal}`,
    "",
    `Action for v508: ${source.action_for_v508}`,
    "",
  ]),
  "## Axis Coverage",
  "",
  ...Object.entries(axisCoverage).map(([axis, count]) => `- ${axis}: \`${count}\``),
  "",
  "## Reflections",
  "",
  ...receipt.reflections.map((reflection) => `- ${reflection.id}: ${reflection.summary}`),
  "",
  "## Next Actions",
  "",
  ...receipt.next_actions.map((action) => `- ${action}`),
  "",
  "## Boundary",
  "",
  "This ledger deepens GMUT-mind source coverage only. It does not claim phase completion, source-target completion, v508 full phase start, x2 closeout, empirical GMUT closure, final physics, consciousness proof, legal closure, canon promotion, raw lane publication, or private-material publication.",
  "",
].join("\n");

writeFileSync(receiptMd, md, "utf8");
console.log(
  JSON.stringify(
    {
      status: receipt.status,
      source_count_this_batch: receipt.source_count_this_batch,
      axis_count: Object.keys(axisCoverage).length,
      gmut_closure_claimed: receipt.gmut_closure_claimed,
    },
    null,
    2,
  ),
);
