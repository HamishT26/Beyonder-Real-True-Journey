#!/usr/bin/env python3
"""Lyren v655-v2 source, proposal, portfolio, and startup-negative catalogue."""

from __future__ import annotations


OFFICIAL_SOURCES = [
    {
        "source_id": "REPAIR-CAFE-ABOUT",
        "title": "About Repair Café",
        "publisher": "Repair Café International Foundation",
        "url": "https://www.repaircafe.org/en/about/",
        "status": "current",
        "use": (
            "community repair, visitor participation, volunteer assistance, "
            "tool access, learning, and item-scope vocabulary"
        ),
    },
    {
        "source_id": "REPAIR-CAFE-HOUSE-RULES",
        "title": "Repair Café house rules",
        "publisher": "Repair Café International Foundation",
        "url": "https://www.repaircafe.org/en/house-rules/",
        "status": "current",
        "use": (
            "voluntary work, visitor participation, repair refusal, item custody, "
            "materials, local-law override, and no-guarantee boundary vocabulary"
        ),
    },
    {
        "source_id": "RCANZ-RESOURCES",
        "title": "Repair Café Aotearoa resources",
        "publisher": "Repair Café Aotearoa New Zealand",
        "url": "https://www.repaircafeaotearoa.co.nz/resources",
        "status": "current",
        "use": (
            "Aotearoa repair-community resources, safe end-of-life routing, te reo "
            "Māori resource context, and local community-authority reservation"
        ),
    },
    {
        "source_id": "WORKSAFE-NZECP50",
        "title": (
            "NZECP 50:2004 — Repair and maintenance of domestic electrical "
            "appliances by the owner"
        ),
        "publisher": "WorkSafe New Zealand / Energy Safety",
        "url": (
            "https://www.worksafe.govt.nz/laws-and-regulations/"
            "electrical-and-gas-codes-of-practice/electricity-codes-of-practice/"
        ),
        "status": "current",
        "use": (
            "owner-repair scope, testing-before-reuse, competence, electrical "
            "hazard, and no-return-to-service-without-evidence boundaries"
        ),
    },
    {
        "source_id": "WORKSAFE-APPLIANCES",
        "title": "Electrical equipment and appliances",
        "publisher": "WorkSafe New Zealand",
        "url": (
            "https://www.worksafe.govt.nz/managing-health-and-safety/consumers/"
            "safe-living-with-electricity/electrical-equipment-and-appliances/"
        ),
        "status": "current",
        "use": (
            "visible hazard, disconnect, qualified repair, certificate, damaged "
            "cord, heat, shock, fire, and stop-use vocabulary"
        ),
    },
    {
        "source_id": "WORKSAFE-LI-ION",
        "title": "Safe use of lithium-ion batteries and battery products",
        "publisher": "WorkSafe New Zealand",
        "url": (
            "https://www.worksafe.govt.nz/topic-and-industry/energy-safety/"
            "safe-use-of-lithium-ion-batteries-and-battery-products/"
        ),
        "status": "current",
        "use": (
            "damaged-battery refusal, charger compatibility, thermal, fire, toxic "
            "smoke, handling, and escalation boundaries"
        ),
    },
    {
        "source_id": "NZ-MFE-PRODUCT-STEWARDSHIP",
        "title": "About product stewardship in Aotearoa New Zealand",
        "publisher": "New Zealand Ministry for the Environment",
        "url": (
            "https://environment.govt.nz/what-government-is-doing/areas-of-work/"
            "waste/product-stewardship/about-product-stewardship-in-new-zealand/"
        ),
        "status": "current",
        "use": (
            "reuse, repair, repurposing, recycling, producer responsibility, "
            "end-of-life routing, and circular-value boundaries"
        ),
    },
    {
        "source_id": "EU-DIR-2024-1799",
        "title": "Directive (EU) 2024/1799 on common rules promoting repair of goods",
        "publisher": "European Union / EUR-Lex",
        "url": (
            "https://eur-lex.europa.eu/legal-content/EN/TXT/"
            "?uri=CELEX%3A32024L1799"
        ),
        "status": "current",
        "use": (
            "repair information, parts choice, software or hardware impediments, "
            "repairer choice, and jurisdiction-specific legal reservation"
        ),
    },
    {
        "source_id": "FTC-NIXING-THE-FIX",
        "title": "Nixing the Fix: An FTC Report to Congress on Repair Restrictions",
        "publisher": "United States Federal Trade Commission",
        "url": (
            "https://www.ftc.gov/reports/nixing-fix-ftc-report-congress-"
            "repair-restrictions"
        ),
        "status": "stable",
        "use": (
            "parts, tools, diagnostics, software locks, adhesive, warranty, "
            "competition, and evidence-specific repair-restriction vocabulary"
        ),
    },
    {
        "source_id": "NIST-SP800-88R2",
        "title": "NIST SP 800-88 Rev. 2 — Guidelines for Media Sanitization",
        "publisher": "National Institute of Standards and Technology",
        "url": "https://csrc.nist.gov/pubs/sp/800/88/r2/final",
        "status": "current",
        "use": (
            "media-sanitization programme, information sensitivity, clear, purge, "
            "destroy, validation, disposal, and confidentiality boundaries"
        ),
    },
    {
        "source_id": "ISO-59004-2024",
        "title": (
            "ISO 59004:2024 — Circular economy — Vocabulary, principles and "
            "guidance for implementation"
        ),
        "publisher": "International Organization for Standardization",
        "url": "https://www.iso.org/standard/80648.html",
        "status": "watch",
        "use": (
            "circular-economy terminology, value networks, stakeholder engagement, "
            "continuous improvement, and revision-watch boundary"
        ),
    },
    {
        "source_id": "NZ-CGA-1993",
        "title": "Consumer Guarantees Act 1993",
        "publisher": "New Zealand Legislation",
        "url": (
            "https://www.legislation.govt.nz/act/public/1993/0091/latest/"
            "DLM312815.html"
        ),
        "status": "current",
        "use": (
            "repair and spare-parts guarantees, reasonable care and skill, redress, "
            "and explicit no-legal-advice reservation"
        ),
    },
    {
        "source_id": "W3C-PROV-O",
        "title": "PROV-O: The PROV Ontology",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/prov-o/",
        "status": "stable",
        "use": (
            "entity, activity, agent, derivation, revision, responsibility, and "
            "repair-event provenance vocabulary"
        ),
    },
    {
        "source_id": "W3C-WCAG-22",
        "title": "Web Content Accessibility Guidelines 2.2",
        "publisher": "W3C",
        "url": "https://www.w3.org/TR/WCAG22/",
        "status": "stable",
        "use": (
            "text alternatives, structure, status messages, input assistance, "
            "help routes, and manual-evaluation reservations"
        ),
    },
    {
        "source_id": "NZ-OPC-PRINCIPLES-2026",
        "title": "New Zealand Privacy Act 2020 principles including IPP 3A",
        "publisher": "Office of the Privacy Commissioner New Zealand",
        "url": "https://www.privacy.org.nz/privacy-principles/",
        "status": "current",
        "use": (
            "purpose, direct and indirect collection notice, security, access, "
            "correction, retention, disclosure, and identifier minimization"
        ),
    },
    {
        "source_id": "TMR-PRINCIPLES",
        "title": "Principles of Māori Data Sovereignty",
        "publisher": "Te Mana Raraunga",
        "url": (
            "https://www.temanararaunga.maori.nz/"
            "principles-of-maori-data-sovereignty"
        ),
        "status": "current",
        "use": (
            "Māori rights, interests, collective benefit, governance, control, "
            "jurisdiction, and authority reservation only"
        ),
    },
]


PROPOSAL_ROWS = [
    (
        1,
        "Repair-café item intake passport with presented-owner claim, product "
        "class, visible condition, accessory count, data-bearing flag, custody "
        "limit, and no-work-start rule",
        "repair-cafe-item-intake",
        "THOS Body",
        "completed",
        "repair-café intake, claimed ownership, and custody boundary",
        [
            "REPAIR-CAFE-ABOUT",
            "REPAIR-CAFE-HOUSE-RULES",
            "W3C-PROV-O",
            "NZ-OPC-PRINCIPLES-2026",
        ],
    ),
    (
        2,
        "Appliance hazard triage card with mains, stored energy, battery, heat, "
        "sharp, pressure, contamination, competence route, isolation hold, and "
        "repair refusal",
        "appliance-hazard-triage",
        "THOS Body",
        "completed",
        "appliance hazard triage and competence routing",
        ["WORKSAFE-APPLIANCES", "WORKSAFE-NZECP50", "WORKSAFE-LI-ION"],
    ),
    (
        3,
        "Fault-symptom chronology board with user observation, operating context, "
        "intermittency, prior intervention, uncertainty, reproduction refusal, "
        "and no-diagnosis promotion",
        "fault-symptom-chronology",
        "THOS Body",
        "completed",
        "fault symptom chronology and observation boundary",
        ["REPAIR-CAFE-HOUSE-RULES", "W3C-PROV-O"],
    ),
    (
        4,
        "Disassembly preflight map with enclosure layer, hidden fastener, cable "
        "route, adhesive boundary, stored-energy marker, image plan, rollback "
        "point, and opening refusal",
        "disassembly-preflight-map",
        "THOS Body",
        "completed",
        "reversible disassembly preflight and opening hold",
        ["WORKSAFE-APPLIANCES", "FTC-NIXING-THE-FIX", "W3C-PROV-O"],
    ),
    (
        5,
        "Fastener and removed-part custody tray with location map, orientation, "
        "quantity, material, damage signal, substitution hold, reassembly link, "
        "and loss refusal",
        "fastener-part-custody",
        "THOS Body",
        "completed",
        "fastener and removed-part custody",
        ["W3C-PROV-O", "FTC-NIXING-THE-FIX"],
    ),
    (
        6,
        "Electrical isolation and stored-energy proxy with plug state, capacitor "
        "placeholder, discharge interval, lockout cue, competent-person gap, "
        "witness field, and energization refusal",
        "electrical-isolation-proxy",
        "THOS Body",
        "represented",
        "electrical isolation and stored-energy proxy",
        ["WORKSAFE-APPLIANCES", "WORKSAFE-NZECP50"],
    ),
    (
        7,
        "Repair-tool status proxy with tool class, insulation placeholder, "
        "calibration status, lead condition, range limit, expiry, competence hold, "
        "and measurement refusal",
        "repair-tool-status-proxy",
        "THOS Body",
        "represented",
        "repair tool calibration and condition proxy",
        ["WORKSAFE-NZECP50", "WORKSAFE-APPLIANCES"],
    ),
    (
        8,
        "Electrostatic-discharge bench proxy with device sensitivity placeholder, "
        "work-surface state, wrist-path placeholder, humidity note, packaging, "
        "monitoring gap, and protection-claim refusal",
        "esd-bench-proxy",
        "THOS Body",
        "represented",
        "electrostatic-discharge bench-state proxy",
        ["FTC-NIXING-THE-FIX", "W3C-PROV-O"],
    ),
    (
        9,
        "Lithium-battery condition and quarantine proxy with chemistry, charger "
        "match, impact, swelling, heat, odour, smoke cue, isolation placeholder, "
        "and handling refusal",
        "lithium-battery-quarantine-proxy",
        "THOS Body",
        "represented",
        "lithium-battery damage and quarantine proxy",
        ["WORKSAFE-LI-ION", "NZ-MFE-PRODUCT-STEWARDSHIP"],
    ),
    (
        10,
        "Thermal, current, voltage, and continuity measurement-plan proxy with "
        "test point, range, instrument placeholder, uncertainty, energization "
        "state, stop threshold, and result-claim refusal",
        "repair-measurement-plan-proxy",
        "THOS Body",
        "represented",
        "repair measurement plan and instrument proxy",
        ["WORKSAFE-NZECP50", "WORKSAFE-APPLIANCES"],
    ),
    (
        11,
        "Replacement-part compatibility matrix with manufacturer reference, "
        "original or reused status, rating, geometry, firmware dependency, "
        "provenance, counterfeit signal, and substitution refusal",
        "part-compatibility-matrix",
        "THOS Body",
        "completed",
        "replacement-part compatibility and substitution boundary",
        ["EU-DIR-2024-1799", "FTC-NIXING-THE-FIX", "ISO-59004-2024"],
    ),
    (
        12,
        "Firmware and configuration preservation ledger with device version, "
        "settings digest, diagnostic mode, update source, rollback image "
        "placeholder, lock signal, and unauthorized-flash refusal",
        "firmware-configuration-ledger",
        "THOS Body",
        "completed",
        "firmware and configuration preservation boundary",
        ["FTC-NIXING-THE-FIX", "EU-DIR-2024-1799", "W3C-PROV-O"],
    ),
    (
        13,
        "Data-bearing repair privacy envelope with media class, data-owner claim, "
        "collection purpose, access prohibition, backup placeholder, sanitization "
        "decision gap, return, and disclosure refusal",
        "data-bearing-repair-privacy",
        "Freed ID and CBR Heart",
        "completed",
        "data-bearing repair privacy and sanitization boundary",
        ["NIST-SP800-88R2", "NZ-OPC-PRINCIPLES-2026", "W3C-PROV-O"],
    ),
    (
        14,
        "Diagnostic branch provenance graph with symptom node, observation edge, "
        "test proposal, skipped branch, conflicting signal, confidence refusal, "
        "review gap, and no-silent-conclusion rule",
        "diagnostic-branch-provenance",
        "GMUT Mind",
        "completed",
        "diagnostic branch provenance and conclusion firewall",
        ["W3C-PROV-O", "REPAIR-CAFE-HOUSE-RULES"],
    ),
    (
        15,
        "Reversible intervention change set with component baseline, proposed "
        "delta, tool need, compatibility evidence, abort point, inverse action, "
        "residual uncertainty, and execution hold",
        "reversible-intervention-change-set",
        "THOS Body",
        "completed",
        "reversible repair intervention and rollback boundary",
        ["W3C-PROV-O", "ISO-59004-2024"],
    ),
    (
        16,
        "Seal, adhesive, clip, and fastener reassembly docket with original state, "
        "replacement material, cure placeholder, torque source, ingress effect, "
        "tamper evidence, and restored-rating refusal",
        "reassembly-integrity-docket",
        "THOS Body",
        "completed",
        "reassembly material and integrity boundary",
        ["FTC-NIXING-THE-FIX", "WORKSAFE-APPLIANCES", "W3C-PROV-O"],
    ),
    (
        17,
        "Fail-closed post-repair test charter with visual check, protective "
        "feature, continuity placeholder, functional criterion, anomaly, competent "
        "review gap, and return-to-service refusal",
        "post-repair-test-charter",
        "THOS Body",
        "completed",
        "post-repair test and return-to-service boundary",
        ["WORKSAFE-NZECP50", "WORKSAFE-APPLIANCES"],
    ),
    (
        18,
        "Repair handover and residual-risk packet with work summary, unresolved "
        "fault, removed part, use restriction, warning, follow-up, visitor "
        "readback, and guarantee refusal",
        "repair-handover-packet",
        "THOS Body",
        "completed",
        "repair handover and residual-risk communication",
        ["REPAIR-CAFE-HOUSE-RULES", "NZ-CGA-1993", "W3C-PROV-O"],
    ),
    (
        19,
        "Volunteer, visitor, and item-role ledger with participation preference, "
        "assistance boundary, competence placeholder, consent notice, privacy "
        "minimum, readback, withdrawal, and role-conflation refusal",
        "repair-participation-role-ledger",
        "Freed ID and CBR Heart",
        "completed",
        "repair-café participant role and consent boundary",
        [
            "REPAIR-CAFE-ABOUT",
            "REPAIR-CAFE-HOUSE-RULES",
            "NZ-OPC-PRINCIPLES-2026",
        ],
    ),
    (
        20,
        "Unrepaired-item circular routing board with repair refusal reason, "
        "reusable component, hazardous material cue, battery state, take-back "
        "option, recycler placeholder, custody transfer, and disposal refusal",
        "unrepaired-item-circular-routing",
        "Freed ID and CBR Heart",
        "completed",
        "unrepaired item end-of-life and circular routing",
        ["NZ-MFE-PRODUCT-STEWARDSHIP", "ISO-59004-2024", "WORKSAFE-LI-ION"],
    ),
    (
        21,
        "GMUT appliance fault-propagation hypergraph with component node, energy "
        "edge, symptom projection, intervention cut, cycle, boundary condition, "
        "unit declaration, and causal-claim firewall",
        "gmut-fault-propagation-hypergraph",
        "GMUT Mind",
        "completed",
        "appliance fault-propagation hypergraph firewall",
        ["W3C-PROV-O", "WORKSAFE-APPLIANCES"],
    ),
    (
        22,
        "GMUT electro-thermal signal field with source symbol, current path, "
        "resistance placeholder, heat term, battery source, dissipation boundary, "
        "unit, and physical-prediction firewall",
        "gmut-electro-thermal-field",
        "GMUT Mind",
        "completed",
        "electro-thermal repair signal field firewall",
        ["WORKSAFE-LI-ION", "WORKSAFE-APPLIANCES"],
    ),
    (
        23,
        "GMUT diagnostic observation operator with latent fault state, test "
        "mapping, instrument placeholder, uncertainty kernel, identifiability "
        "hold, update rule, unit, and likelihood firewall",
        "gmut-diagnostic-observation-operator",
        "GMUT Mind",
        "completed",
        "diagnostic observation operator and likelihood firewall",
        ["W3C-PROV-O", "WORKSAFE-NZECP50"],
    ),
    (
        24,
        "THOS reversible repair job charter with item scope, safety prerequisites, "
        "evidence inputs, permitted delta, authority ceiling, abort path, witness "
        "predicate, and live-work refusal",
        "thos-repair-job-charter",
        "THOS Body",
        "completed",
        "typed reversible repair job charter",
        ["W3C-PROV-O", "REPAIR-CAFE-HOUSE-RULES"],
    ),
    (
        25,
        "THOS fail-closed repair queue governor with hazard class, competence "
        "route, tool dependency, visitor participation, workload cap, accessibility "
        "need, cancellation, and no-auto-assignment invariant",
        "thos-repair-queue-governor",
        "THOS Body",
        "completed",
        "fail-closed repair queue and workload governor",
        ["REPAIR-CAFE-ABOUT", "REPAIR-CAFE-HOUSE-RULES", "W3C-WCAG-22"],
    ),
    (
        26,
        "Freed ID appliance-part-firmware-repair relation profile with namespace "
        "source, product instance, component, configuration, repair event, "
        "collision, resolver placeholder, privacy, and nonproduction refusal",
        "freed-id-repair-relation-profile",
        "Freed ID and CBR Heart",
        "completed",
        "repair asset identifier and referent separation",
        ["W3C-PROV-O", "NIST-SP800-88R2", "FTC-NIXING-THE-FIX"],
    ),
    (
        27,
        "CBR repair decision and remedy provenance ledger with visitor instruction, "
        "alternative, safety refusal, material loss, warranty note, legal-review "
        "gap, correction, withdrawal, and no-rights-adjudication rule",
        "cbr-repair-remedy-provenance",
        "Freed ID and CBR Heart",
        "completed",
        "repair decision provenance, correction, and remedy hold",
        [
            "NZ-CGA-1993",
            "FTC-NIXING-THE-FIX",
            "NZ-OPC-PRINCIPLES-2026",
            "W3C-PROV-O",
        ],
    ),
    (
        28,
        "Accessible repair-café status record with plain-language hazard summary, "
        "reading order, nonvisual part map, input help, progress message, warning "
        "cue, contact route, and manual-evaluation hold",
        "accessible-repair-cafe-record",
        "THOS Body",
        "completed",
        "accessible repair-café status and handover structure",
        ["W3C-WCAG-22", "RCANZ-RESOURCES"],
    ),
    (
        29,
        "Real community repair-café pilot adapter with organiser authorization, "
        "venue safety plan, qualified electrical role, real items, participant "
        "consent, calibrated tools, outcome follow-up, independent review, and "
        "zero-action firewall",
        "real-repair-cafe-pilot-adapter",
        "THOS Body",
        "open_gap",
        "real community repair-café evidence readiness",
        [
            "RCANZ-RESOURCES",
            "REPAIR-CAFE-HOUSE-RULES",
            "WORKSAFE-NZECP50",
            "NZ-CGA-1993",
        ],
    ),
    (
        30,
        "Tangata whenua, iwi, hapū, Māori authority, community ownership, taonga "
        "item, repair knowledge, te reo Māori, material provenance, recording, "
        "reuse, disposal, access, correction, remedy, and data-governance reservation",
        "maori-repair-authority-reservation",
        "Freed ID and CBR Heart",
        "exact_gate",
        "Māori repair knowledge, material, and affected-party authority reservation",
        [
            "TMR-PRINCIPLES",
            "RCANZ-RESOURCES",
            "NZ-OPC-PRINCIPLES-2026",
            "NZ-MFE-PRODUCT-STEWARDSHIP",
        ],
    ),
]


SKILL_IDEAS = [
    "ghc-family-repair-cafe-intake-boundary",
    "ghc-family-appliance-hazard-triage",
    "ghc-family-repair-part-custody",
    "ghc-family-battery-quarantine-proxy",
    "ghc-family-data-bearing-repair-privacy",
    "ghc-family-repair-decision-provenance",
    "ghc-family-repair-handover",
    "ghc-family-repair-accessibility",
    "ghc-family-repair-identifier-profile",
    "ghc-family-repair-evidence-firewall",
]


RUNNER_IDEAS = [
    "ghc_family_repair_cafe_intake_boundary.py",
    "ghc_family_appliance_hazard_triage.py",
    "ghc_family_repair_part_custody.py",
    "ghc_family_battery_quarantine_proxy.py",
    "ghc_family_data_bearing_repair_privacy.py",
    "ghc_family_repair_decision_provenance.py",
    "ghc_family_repair_handover.py",
    "ghc_family_repair_accessibility.py",
    "ghc_family_repair_identifier_profile.py",
    "ghc_family_v655_v2_suite.py",
]


CLEAN_SURFACES = [
    "repair intake vocabulary",
    "hazard and competence triage",
    "parts and fastener custody",
    "battery quarantine proxy",
    "data-bearing item privacy",
    "rollback wording",
    "manifest coverage",
    "failure retention",
    "source status",
    "Māori-authority refusal",
]


X1_OPERATIONAL_NEGATIVES = [
    {
        "negative_id": "V6552-X1-N01",
        "signature": "combined_activation_metadata_git_status_probe_timeout",
        "failed": (
            "The first combined activation metadata, source identity, and "
            "cleanliness probe exceeded its bound and returned no usable evidence."
        ),
        "recovery": (
            "Split exact UTF-8 baton metadata, source branch, head, and cleanliness "
            "into long-bound scalar probes."
        ),
        "recurrence_guard": (
            "Do not combine archive-backed file reads and Git status in one short "
            "startup wrapper."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N02",
        "signature": "parallel_baton_metadata_line_count_timeout",
        "failed": (
            "The parallel activation-file metadata and line-count probe timed out "
            "without a complete result."
        ),
        "recovery": (
            "Use one exact .NET UTF-8 ReadAllText operation, then verify byte, "
            "character, line, and final-newline counts."
        ),
        "recurrence_guard": (
            "Use a single direct .NET file read for a known archive-backed baton."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N03",
        "signature": "parallel_source_branch_head_probe_timeout",
        "failed": (
            "The parallel source identity probe emitted only the branch before "
            "timing out and therefore earned no complete branch-plus-head credit."
        ),
        "recovery": (
            "Run branch and head as separate scalar Git commands with archive-sized "
            "timeouts; both then matched the activation."
        ),
        "recurrence_guard": (
            "Require complete scalar outputs rather than crediting a partial "
            "multi-command identity probe."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N04",
        "signature": "parallel_source_cleanliness_probe_timeout",
        "failed": (
            "The parallel full source status probe exceeded its short bound and "
            "returned no cleanliness witness."
        ),
        "recovery": (
            "Run status alone with a longer bound and materialize only porcelain "
            "row count; the source then proved clean."
        ),
        "recurrence_guard": (
            "Keep archive-backed cleanliness separate from identity and metadata "
            "probes."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N05",
        "signature": "ripgrep_option_boundary_pattern_error",
        "failed": (
            "A read-only runner inspection passed a pattern beginning with --out "
            "without the rg option terminator, so rg rejected it as a flag."
        ),
        "recovery": (
            "Use rg -n -- followed by the literal pattern and exact file; the "
            "bounded runner inspection then completed."
        ),
        "recurrence_guard": (
            "Insert the rg option terminator before any pattern that can begin "
            "with a hyphen."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N06",
        "signature": "powershell_foreach_receipt_projection_parser_error",
        "failed": (
            "A multi-receipt projection piped directly from a PowerShell foreach "
            "block and failed at parse time with an empty pipe element."
        ),
        "recovery": (
            "Materialize receipt rows in an array, then pipe that array to the "
            "formatter; the six exact receipts parsed."
        ),
        "recurrence_guard": (
            "Materialize PowerShell foreach output before piping it."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N07",
        "signature": "semantic_domain_query_missing_closing_brace",
        "failed": (
            "The first frozen-title semantic-domain query omitted a closing "
            "PowerShell block brace and produced no novelty evidence."
        ),
        "recovery": (
            "Use a materialized Where-Object result with balanced syntax; the "
            "complete 1,960-title seed-domain audit then returned."
        ),
        "recurrence_guard": (
            "Prefer a short materialized filter over nested one-line foreach and "
            "if blocks for title audits."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N08",
        "signature": "unicode_multi_hunk_patch_context_rejection",
        "failed": (
            "The first multi-hunk phase-data correction was rejected atomically "
            "because one Unicode-bearing context line did not match display-"
            "decoded text; no file changed."
        ),
        "recovery": (
            "Apply small exact UTF-8 hunks for identity, source, practice, "
            "disposition, and catalogue aliases; the owned file updates passed."
        ),
        "recurrence_guard": (
            "Use exact UTF-8 source context and split unrelated patches when a "
            "terminal display may have decoded Unicode differently."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N09",
        "signature": "combined_catalogue_ast_status_probe_timeout",
        "failed": (
            "The first combined catalogue metadata, Python AST, and Git-status "
            "verification exceeded its wrapper bound before emitting evidence."
        ),
        "recovery": (
            "Split the verification into a literal file probe, a direct UTF-8 "
            "structure read, and one bounded AST parse; the catalogue was intact."
        ),
        "recurrence_guard": (
            "Keep archive-backed metadata, interpreter, and Git checks as "
            "separate scalar probes."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N10",
        "signature": "novelty_report_console_encoding_error",
        "failed": (
            "The first read-only novelty pre-audit computed comparisons but could "
            "not emit its complete report because the Windows console codec could "
            "not encode a Māori-character source title."
        ),
        "recovery": (
            "Set the Python standard-stream encoding explicitly to UTF-8 and rerun "
            "the unchanged read-only comparison."
        ),
        "recurrence_guard": (
            "Declare UTF-8 standard-stream encoding for Unicode-bearing evidence "
            "reports on Windows."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N11",
        "signature": "x1_manifest_worktree_line_ending_mismatch",
        "failed": (
            "The first focused x1 suite compared prospective normalized Git-blob "
            "sizes with CRLF working-tree sizes and failed one manifest assertion."
        ),
        "recovery": (
            "Validate each manifest row against the exact prospective Git blob "
            "used by the manifest, while the staged review separately audits the "
            "eventual index blobs."
        ),
        "recurrence_guard": (
            "State and test the content basis of byte manifests explicitly when "
            "core.autocrlf is active."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
    {
        "negative_id": "V6552-X1-N12",
        "signature": "powershell_system_text_json_type_unavailable",
        "failed": (
            "The first manifest-mismatch diagnostic selected a System.Text.Json "
            "type unavailable in the active PowerShell host and produced no audit."
        ),
        "recovery": (
            "Use the host-supported ConvertFrom-Json parser and literal file "
            "metadata; it identified four line-ending-only mismatches."
        ),
        "recurrence_guard": (
            "Use PowerShell's native JSON cmdlets unless an assembly-backed type "
            "has first been verified."
        ),
        "credit": "retained_negative_zero_initial_pass_credit",
    },
]
