"""Build Sylven Arc v674-v8's planning-only x1 freeze.

The builder is owner-delta scoped and fail-closed. It requires Elowen Cairn's
exact v674-v7 final, the exact Sylven branch, and an absent x2/closeout tree. It
does not stage, commit, push, route, contact a task, or perform an external
write.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OWNER_ROOT = ROOT / "docs" / "sylven-arc" / "v674-v8"
OWNER = "Sylven Arc"
PHASE = "v674-v8"
BRANCH = "codex/GHC-Family/sylven-arc-v674-v8-full-tools"
SOURCE_BRANCH = "codex/GHC-Family/elowen-cairn-v674-v7-full-tools"
SOURCE_START = "c7412530cbb3a549ad681ae7b98c29b64e31ad4d"
SOURCE_X1 = "d293bfaefa278b1d2e5bd086c25625df30dbe3e9"
SOURCE_EVIDENCE = "0c2974df83cdcf558fb63b8354016602ef9415e5"
SOURCE_FINAL = "1a5e801d2c52119c05a505baaaa072ef6420795d"
ACTIVATION_PATH = "docs/elowen-cairn/v674-v7/handoffs/sylven-arc-v674-v8-activation-candidate.md"
ACTIVATION_SHA256 = "cc3d8753b73526964be98012997415109709e7fefbdecab898e7e627c08b1c67"
SOURCE_CANONICAL_SHA256 = "4427b8d3cdb0dd6dc3b7e5af5a7ca9d38da9d56011d99e0bfb93d2f167b1e18b"
SOURCE_CANONICAL_PAYLOAD_SHA256 = "4958076e46b836f8d7313b5e469c312d9c54642f903c9aeff270eeb8ccaf73e5"
SOURCE_TREE_CORPUS_SHA256 = "0b1070cea21beae31944be5d61efdd93f7e2ea7c197df391ad863aad23195a14"
OUTCOMES = {"completed": 42, "represented": 12, "open_gap": 3, "exact_gate": 3}
CORE_LABELS = ["completed", "represented", "open_gap", "exact_gate"]

IDENTITY_BOUNDARY = (
    "Sylven Arc, they/them, relational boundary cartographer and evidence steward, "
    "is relational working language only. It is not evidence of consciousness, "
    "sentience, legal personhood, identity continuity, employment, qualification, "
    "independent agency, or scientific, operational, legal, cultural, affected-party, "
    "or Māori authority."
)
HOPE = "map the boundary between evidence and possibility so every claim remains inspectable, corrigible, and safely retractable"
BOUNDARY = (
    "Software, symbolic, synthetic, same-owner, citation, inherited, or composite "
    "evidence is not empirical confirmation, participant evidence, professional or "
    "scientific authority, production readiness, legal or cultural ratification, "
    "Māori authority, affected-party approval, complete privacy or accessibility "
    "assurance, exhaustive security, independent reproduction, AGI/ASI, consciousness "
    "or personhood evidence, Theory-of-Everything proof, proof/canon, or Stage 20 authority."
)

REPOSITORY_SEAL = {
    "proposal_chain": 6970,
    "effective_negatives": 39648,
    "effective_methods": 27867,
    "failed_witnesses": 11309,
    "bounded_passing_witnesses": 15150,
    "open_gaps": 328,
    "exact_gates": 321,
    "terminal_verdict": "NOT_READY_FOR_STAGE_20",
}
ACTIVATION_OVERLAY = {
    **REPOSITORY_SEAL,
    "effective_negatives": 39655,
    "effective_methods": 27874,
    "failed_witnesses": 11316,
    "bounded_passing_witnesses": 15157,
    "external_zero_credit_failures": 7,
    "external_bounded_passing_witnesses": 7,
    "repository_seal_rewritten": False,
}

TEMPLATE_STARTUP_FAILURES_UNUSED = [
    (
        "SA6748-START-N001",
        "The first PowerShell skill-path projection piped a foreach statement in an invalid form and failed before reading any skill.",
        "Materialize the literal skill-path rows first and then project or count them.",
        "Every required skill and reference was read through EOF in bounded windows before mutation.",
        "Do not pipe a PowerShell foreach language statement directly; bind its output before a pipeline.",
    ),
    (
        "SA6748-START-N002",
        "A combined authorization-schema and current-state display exceeded its bounded output and was truncated.",
        "Read the schema and state independently in complete bounded windows.",
        "The complete authorization schema and current state were recovered without mutation.",
        "Partition large state and schema reads and require an explicit EOF witness for each.",
    ),
    (
        "SA6748-START-N003",
        "The first complete Method Flow guidance read exceeded its display bound.",
        "Resume from the exact unread line and continue through EOF without restarting the completed prefix.",
        "The Method Flow skill and schema were completely read before recording Elowen state.",
        "Use deterministic line windows for instruction files whose first projection is truncated.",
    ),
    (
        "SA6748-START-N004",
        "A combined immutable-evidence-manifest read exceeded its output bound.",
        "Read each exact Git blob independently in deterministic entry windows.",
        "All 146 immutable evidence entries and declared exclusions were read and later replayed.",
        "Never infer manifest completion from a truncated combined display.",
    ),
    (
        "SA6748-START-N005",
        "An owner-manifest window wrapper treated an array expression as scalar arithmetic and failed before projection.",
        "Compute the array count in a separate scalar and then derive each window boundary.",
        "The 188-entry owner manifest and four exclusions were read through EOF.",
        "Normalize PowerShell collection cardinality before subtraction or range construction.",
    ),
    (
        "SA6748-START-N006",
        "A combined owner-manifest projection exceeded its display bound after producing only a prefix.",
        "Recover each remaining entry window independently and verify the terminal exclusions.",
        "All owner-manifest entries and exclusions were recovered without replaying Liora validation.",
        "Treat partial manifest output as incomplete, never as an EOF witness.",
    ),
    (
        "SA6748-START-N007",
        "A divergence wrapper allowed the literal upstream selector to be misparsed as a revision payload.",
        "Resolve the exact tracking ref first and pass that scalar ref to rev-list.",
        "The source branch proved typed zero-ahead and zero-behind against its exact tracking ref.",
        "Never embed the upstream revision selector inside a transport wrapper that may reinterpret braces.",
    ),
    (
        "SA6748-START-N008",
        "The first read-only manifest verifier completed outside its attributable result window and returned no usable receipt.",
        "Use one bounded cat-file batch communicate call and emit only final scalar counts.",
        "All four commit-local manifests replayed with zero missing blobs or digest mismatches.",
        "Silent or detached process completion earns no validation credit; require an attributable payload.",
    ),
    (
        "SA6748-START-N009",
        "A sparse-working-tree ripgrep audit misleadingly returned zero proposal hits because predecessor proposal files were not materialized.",
        "Audit exact Git-tree blob paths at the immutable source rather than sparse checkout bytes.",
        "The exact-tree audit parsed 1,709 proposal JSON blobs and recovered 2,095 proposal identifiers and 1,969 titles.",
        "Use Git-object scope for inherited semantic audits in sparse worktrees.",
    ),
    (
        "SA6748-START-N010",
        "A PowerShell foreach-to-pipeline neighbor-count wrapper failed to parse before computing any semantic score.",
        "Materialize normalized title rows first and compute comparisons in one explicit UTF-8 program.",
        "All forty proposed titles had zero neighbors at or above the 0.72 threshold.",
        "Keep PowerShell iteration and pipeline stages syntactically separate.",
    ),
    (
        "SA6748-START-N011",
        "The first Git cat-file audit wrote all requests before draining stdout and deadlocked its exact owner-started process pair.",
        "Stop only that exact process pair and use communicate so input and output drain together.",
        "The recovery parsed every candidate blob with zero malformed JSON.",
        "Use communicate for bounded bidirectional Git plumbing; never fill both pipes sequentially.",
    ),
    (
        "SA6748-START-N012",
        "A default Windows text projection raised UnicodeEncodeError while rendering Māori macrons after the data had been read.",
        "Repeat only the presentation step under explicit UTF-8 input and output encoding.",
        "The exact title audit completed with Māori text preserved and no repository mutation.",
        "Set explicit UTF-8 for any Windows presentation surface containing non-ASCII text.",
    ),
    (
        "SA6748-START-N013",
        "The first web-result forwarding projection assumed a content-array envelope and displayed no source result.",
        "Inspect the actual result shape and forward the bounded text payload directly.",
        "Official and primary source pages were recovered read-only with zero dataset rows or external writes.",
        "Inspect tool-result keys before projection and never equate an empty wrapper with an empty source.",
    ),
    (
        "SA6748-START-N014",
        "A later builder-size PowerShell foreach-pipeline expression repeated the earlier parser signature.",
        "Apply the already preferred materialize-then-pipe method and retain the recurrence separately.",
        "The bounded file-size projection recovered both predecessor template surfaces.",
        "A repeated signature is a new retained witness even when its preferred recovery is already known.",
    ),
    (
        "SA6748-START-N015",
        "A combined branch path and worktree-registry probe returned no attributable registry payload.",
        "Run branch refs, literal path existence, and worktree registry checks as separate scalar probes.",
        "The Elowen branch, remote ref, target path, and worktree registration were all absent before creation.",
        "Do not combine registry enumeration with ref and filesystem predicates in one opaque wrapper.",
    ),
    (
        "SA6748-START-N016",
        "The first all-row proposal projection exceeded its display bound before every new title was visible.",
        "Project only proposal identifiers, titles, expected dispositions, and maximum-neighbor scalars.",
        "All forty titles and their exact disposition distribution were recovered without changing the slate.",
        "Use concise all-row projections for prefreeze human review.",
    ),
    (
        "SA6748-START-N017",
        "A template-path inspection used command expressions separated by commas inside a PowerShell array and produced one malformed combined path.",
        "Use an explicit literal string array for the two predecessor template paths.",
        "Both exact predecessor template files were found and their line and byte counts were recovered.",
        "Do not append comma tokens to command expressions inside PowerShell array literals.",
    ),
    (
        "SA6748-START-N018",
        "The first template copy assumed sparse checkout had already materialized new owner scripts and tests directories.",
        "Create only the two missing Elowen-owned directories and repeat the bounded copy.",
        "Only the planning x1 builder and test were copied; no x2, final, validator, or closeout file was introduced.",
        "Create owner-only sparse target directories explicitly before copying a new lifecycle file.",
    ),
    (
        "SA6748-X1-N001",
        "The first multi-section source-constant patch included one stale context line and failed verification without changing a byte.",
        "Split the edit into smaller exact-context patches against the current mechanical template.",
        "Source anchors, counts, and lifecycle wording were updated through attributable patch receipts.",
        "Apply substantive edits in section-bounded patches after mechanical renaming.",
    ),
]

TEMPLATE_ACTIVE_FAILURES_UNUSED = [
    (
        "SA6748-X1-N001",
        "The first broad memory-registry projection exceeded its display budget and was truncated.",
        "Use a bounded exact-key Select-String projection over the primary memory registry.",
        "The current v674-to-v725 route note and Sylven successor consistency were recovered without repository mutation.",
        "Search the primary registry with exact phase and route keys before opening any rollout summary.",
    ),
    (
        "SA6748-X1-N002",
        "A combined source-equality wrapper returned no attributable payload within its result window.",
        "Run exact branch, head, divergence, clean-state, and fresh-live probes as separate bounded scalars.",
        "Every source equality scalar was attributable and local, upstream, tracking, and fresh live all matched the exact final.",
        "Do not combine remote refresh and multiple equality projections inside one opaque wrapper.",
    ),
    (
        "SA6748-X1-N003",
        "A PowerShell file-metadata foreach statement was piped directly into ConvertTo-Json and failed to parse.",
        "Materialize the metadata rows before sending them through the JSON pipeline.",
        "The exact required packet file metadata was recovered in a bounded UTF-8 projection.",
        "Bind foreach output to a collection before any PowerShell pipeline.",
    ),
    (
        "SA6748-X1-N004",
        "The inherited per-entry manifest helper exceeded its attribution window and emitted no usable completion payload.",
        "Replay each declared Git-blob domain with one bounded cat-file batch and emit only aggregate scalars.",
        "The immutable x1, corrected evidence, final owner, and final delta manifests replayed exactly.",
        "Prefer one tree/object batch to thousands of per-entry Git processes.",
    ),
    (
        "SA6748-X1-N005",
        "The first cat-file batch implementation wrote every request before draining stdout and deadlocked its exact helper process.",
        "Stop only the attributable helper and use subprocess communicate so input and output drain together.",
        "The recovery completed the exact Git-object replay with no missing or mismatched corrected-domain entries.",
        "Use communicate for bounded bidirectional Git plumbing and inspect process state before retry.",
    ),
    (
        "SA6748-X1-N006",
        "The first inline original-manifest diagnostic was rejected by PowerShell command parsing before Python executed.",
        "Pass the exact UTF-8 program through a PowerShell here-string to Python stdin.",
        "The original first-evidence manifest was shown to retain exactly twenty normalized-blob mismatches and zero parity credit.",
        "Use literal here-strings for multiline Python rather than nested command-line quoting.",
    ),
    (
        "SA6748-X1-N007",
        "The first branch-and-path existence probe used an invalid parenthesized PowerShell statement expression.",
        "Capture each branch, remote-ref, path, and worktree-registry result sequentially.",
        "The Elowen branch, target path, and registration were proven absent before additive creation.",
        "Keep state-changing prerequisites as separately attributable scalar probes.",
    ),
    (
        "SA6748-X1-N008",
        "A combined multi-skill and current-state display was truncated before every required EOF witness.",
        "Read each selected skill, schema, and current overlay independently in bounded UTF-8 windows.",
        "Every selected instruction and required reference was read completely through EOF before owner mutation.",
        "Treat a truncated combined read as incomplete and resume only its exact unread ranges.",
    ),
    (
        "SA6748-X1-N009",
        "A Git worktree registry probe was first invoked from the non-repository Codex home directory.",
        "Discover the exact D-drive source worktree and rerun Git probes from that repository.",
        "The immutable Liora source worktree and fresh Elowen target were then verified without touching sibling state.",
        "Resolve and verify the repository working directory before any Git topology command.",
    ),
    (
        "SA6748-X1-N010",
        "The first inherited proposal-freeze projection guessed a rows field and attempted to index a null collection.",
        "Inspect the exact JSON object keys and then read its proposals collection.",
        "All sixty Liora proposal contracts were recovered from the immutable freeze without mutation.",
        "Inspect schema keys before indexing inherited JSON whose shape may have evolved.",
    ),
    (
        "SA6748-X1-N011",
        "The first x1 builder invocation assumed a positional build subcommand that the inherited CLI did not expose.",
        "Inspect the argparse surface and invoke the default build path without a positional argument.",
        "The builder entered its owner-local fail-closed build path on the next invocation.",
        "Inspect inherited command surfaces before assuming a newer subcommand convention.",
    ),
    (
        "SA6748-X1-N012",
        "The first real x1 build rejected the proposed slate because inherited semantic-neighbor collisions crossed the 0.72 threshold.",
        "Project each proposed title's exact best neighbor and rewrite only colliding proposals before refreezing.",
        "The isolated collision report identified the affected cross-pillar titles without creating a frozen x1 packet.",
        "Run the semantic collision gate before staging or claiming novelty.",
    ),
    (
        "SA6748-X1-N013",
        "A premature all-x1 test selection ran before staged receipts existed and also exposed one stale expected manifest-entry count.",
        "Correct the exact 714-entry source replay assertion, generate staged receipts in lifecycle order, and rerun only the x1 selection.",
        "All non-lifecycle-dependent x1 assertions passed, while the missing-receipt errors and stale count remained zero-credit failures.",
        "Do not include receipt-dependent tests until their declared staged lifecycle artifacts exist.",
    ),
]

STARTUP_FAILURES = [('SA6748-X1-N001',
  'The first grouped required-skill projection exceeded its bounded display before every selected instruction had '
  'reached EOF.',
  'Reread the two truncated skills individually and preserve an explicit EOF witness for every selected instruction.',
  'Every selected current skill and directly required reference was completely read before repository mutation.',
  'Partition instruction reads by file and never infer completion from a grouped truncated projection.'),
 ('SA6748-X1-N002',
  'A JavaScript reference-inventory wrapper contained an invalid template expression and failed before its shell '
  'probe ran.',
  'Use one literal PowerShell array and project only the bounded file metadata required for the audit.',
  'The exact required-reference inventory was recovered without changing any source or owner file.',
  'Keep wrapper composition literal when paths or expressions contain nested quoting.'),
 ('SA6748-X1-N003',
  'The first current authorization-state projection exceeded its display budget and returned only a prefix.',
  'Resume the same file in deterministic nonoverlapping line windows through EOF.',
  'The complete authorization state and schema were read without rewriting the stale stored snapshot.',
  'Large mutable state files require explicit window bounds and an EOF witness.'),
 ('SA6748-X1-N004',
  'The first final-overview projection exceeded its bounded output after returning only an initial prefix.',
  'Read the exact immutable overview in bounded nonoverlapping line windows.',
  'All overview sections were recovered through EOF without replaying Elowen validation.',
  'Treat a truncated source packet as incomplete even when its visible prefix looks coherent.'),
 ('SA6748-X1-N005',
  'One grouped overview recovery window also exceeded its result budget before exposing its complete terminal '
  'section.',
  'Reread only the exact unread final line window and compare its boundary to the earlier prefix.',
  'The previously unread overview tail was recovered exactly once.',
  'After a second truncation, narrow the next read to the smallest demonstrably unread interval.'),
 ('SA6748-X1-N006',
  'A first local Method Flow projection treated null witness identifiers on method-recorded candidate events as '
  'broken references.',
  'Inspect the current schema semantics and allow only null witness identifiers whose reason is exactly method '
  'recorded.',
  'All 870 source events passed the corrected schema-aware projection, including 33 declared method-recorded events.',
  'Validate optional identifiers against event type and reason instead of applying one unconditional referential '
  'rule.'),
 ('SA6748-X1-N007',
  'The first broad novelty grep wrapper projected stdout only at its yield boundary and discarded the still-running '
  'session handle.',
  'Wait for the exact process to finish, then run one attributable bounded exact-tree corpus audit with a preserved '
  'handle.',
  'The source-bounded corpus audit completed with exact counts and no competing process.',
  'Always surface a session identifier for a Git-tree scan that can outlive its initial yield.'),
 ('SA6748-X1-N008',
  'An unbounded new-proposal and portfolio projection exceeded the model-visible context before its complete '
  'structures were inspected.',
  'Project only top-level keys, array counts, category counts, and one first and last exemplar.',
  'The sixty-row proposal schema and all portfolio category counts were recovered without rereading unrelated '
  'payloads.',
  'Inspect large JSON by schema keys and bounded exemplars rather than emitting the full document.'),
 ('SA6748-X1-N009',
  'A combined branch preflight embedded external commands inside a parenthesized PowerShell value expression and '
  'failed to parse.',
  'Resolve each exit code and existence scalar in a separate statement before serialization.',
  'The target path, local branch, tracking ref, worktree registration, and live remote branch were all proven '
  'absent.',
  'Keep external-command statements outside PowerShell scalar expression parentheses.'),
 ('SA6748-X1-N010',
  'The corrected combined branch-state wrapper completed without emitting an attributable payload.',
  'Run the path, local ref, tracking ref, and worktree-registry checks as independent scalar probes.',
  'Four independently attributable probes proved the fresh additive lane was absent before creation.',
  'A zero-exit wrapper with no evidence receives no preflight credit.'),
 ('SA6748-X1-N011',
  'The first no-checkout sparse initialization left a brand-new empty index represented as staged deletions across '
  'inherited history.',
  'Repopulate only the new lane index from its immutable HEAD through the already-declared sparse patterns.',
  'The isolated new worktree returned to a clean index at the exact source head with two intended inherited helper '
  'files materialized.',
  'After no-checkout sparse creation, verify status before edits and repair only the empty new index when '
  'necessary.'),
 ('SA6748-X1-N012',
  'The proposed historical-typewriter practice was already extensively represented in reachable proposal evidence.',
  'Reject the practice before freeze and compare alternative practice terms against the exact source-tree proposal '
  'corpus.',
  'Synthetic sailmaking documentation showed zero exact reachable practice-title hits while adjacent rigging terms '
  'remained explicitly separated.',
  'A collision-free wording rewrite does not rescue a practice domain that is already materially represented.'),
 ('SA6748-X1-N013',
  'The proper typewriter grep completed with over seventy thousand tokens and its presentation was truncated despite '
  'containing enough rejection evidence.',
  'Use the exact proposal-JSON corpus extractor and report only per-practice term counts and bounded examples.',
  'The bounded corpus projection returned 2,788 unique titles and exact candidate-term counts without another '
  'overbroad display.',
  'Prefer structured corpus scalars over repository-wide textual match streams.'),
 ('SA6748-X1-N014',
  'The first template generator failed closed because its overview-function boundary expression did not account for '
  "the source file's exact line-ending form.",
  'Use an anchored multiline function boundary that is independent of CRLF versus LF representation.',
  'The corrected generator located exactly one overview block and still wrote no owner artifact until all guards '
  'passed.',
  'Template transforms must require exactly one structural match and retain a zero-match failure.'),
 ('SA6748-X1-N015',
  'The first generated overview was syntactically invalid because regular-expression replacement processing '
  'interpreted a literal newline escape in the replacement payload.',
  'Supply the generated function through a callable replacement so its backslashes remain literal source bytes.',
  'The regenerated owner builder and test both compiled under UTF-8.',
  'Use callable replacements whenever generated source contains backslash escapes.'),
 ('SA6748-X1-N016',
  'A regeneration wrapper invoked the template script as a target-worktree-relative path even though the helper '
  'lives in the local Codex workspace.',
  'Invoke the helper by its exact absolute local path while keeping generated owner files D-first.',
  'The same generator then wrote the two intended owner source files and compiled them.',
  'Bind helper location independently from the target worktree before invocation.'),
 ('SA6748-X1-N017',
  'One corrective apply-patch was rejected atomically because its expected context did not match the live generator '
  'line containing literal patch markers.',
  'Inspect the exact live line window and patch the smallest matching block.',
  'The corrected generator now updates the activation path, source seal scalars, corpus threshold, and official '
  'source row exactly.',
  'After a context mismatch, reread live bytes before issuing a narrower patch.'),
 ('SA6748-X1-N018',
  'The first planning build rejected one cultural-authority proposal whose token-Jaccard score was 0.923077 against '
  'an inherited exact-gate title.',
  'Rewrite only that proposed title to bind the sailmaking-specific context while preserving the exact gate and all '
  'preregistration fields.',
  'A bounded collision report named only SA6748-N060 before any x1 artifact was written.',
  'Run the semantic gate before every freeze and never credit a generic authority packet as novel.')]

TEMPLATE_NEW_TITLES_UNUSED = [
    "synthetic stained-glass window bay light panel and piece identity lattice with conflation refusal",
    "lead-came node edge junction boundary and panel topology with orphan-edge rejection",
    "panel-cartoon coordinate frame orientation scale and registration-uncertainty contract",
    "glass-piece polygon adjacency overlap gap and out-of-frame geometry refusal",
    "colour and transmission descriptor ledger with instrument calibration and observation vacancies",
    "fracture bowing bulge corrosion loss and repair-cue register separated from diagnosis",
    "support-bar saddle tie ventilator and protective-glazing relation graph with fitness abstention",
    "panel-image rectification crop rotation and derivative lineage with no dimensional inference",
    "window-location panel-orientation and viewpoint map with privacy and sacred-space holds",
    "maker workshop date iconography and attribution vacancy ledger with contestation and correction",
    "synthetic dry-stone section course face hearting through-stone batter and cope identity topology",
    "stone placement support-contact and load-path conjecture graph with unsupported-node quarantine",
    "course elevation station offset datum and dimensional-unit vacancy ledger",
    "void bulge displacement lean washout and drainage-cue register without stability assessment",
    "terrain boundary land-parcel archaeology habitat and precise-location privacy hold matrix",
    "dry-stone vocabulary provenance and named-tradition abstention board",
    "synthetic ornamental-plaster room surface cornice medallion coffer and cast-unit identity lattice",
    "lath substrate scratch brown finish coat and support relation graph with missing-layer vacancy",
    "mould template cast piece assembly and reassembly provenance with source-ambiguity quarantine",
    "crack delamination stain detachment movement and loss cue register without diagnosis or treatment",
    "pigment gilding paint finish and composition claim firewall with sampling and material vacancies",
    "environment humidity temperature vibration water-ingress and duration observation vacancy across three lenses",
    "canonical heritage-document JSON profile with duplicate-key numeric-domain and ordering refusal",
    "PROV entity activity derivation correction and invalidation braid across three synthetic lenses",
    "accessibly structured condition-map dossier with text equivalents table headers and noncolour cues",
    "pseudonymous zero-key role capability validity status and revocation-vacancy profile",
    "privacy minimizer rejecting personal identifiers live precise locations free text credentials and private routes",
    "work-cap pause stop readback handover and unresolved-hold queue across three synthetic lenses",
    "GMUT discrete-exterior-calculus cochain coboundary and Hodge-star obligation board on a synthetic came network",
    "GMUT spectral-graph Laplacian mode analogy across synthetic panel and wall support networks",
    "GMUT signed-distance curvature and level-set surrogate for ornamental relief with zero recovered shape",
    "GMUT scalar-tensor boundary pullback unit gauge and EFT obligation board with zero likelihood",
    "THOS three-lens dependency DAG challenge response workload budget and handover with zero participants",
    "Freed ID zero-key provenance custody role expiry status and revocation-vacancy representation",
    "CBR notice contest correction withdrawal access and remedy-vacancy matrix for heritage documentation",
    "static accessibility evaluation matrix reserving manual assistive-technology language and affected-user review",
    "Library of Congress architectural-image adapter with zero calls zero downloads zero rows and schema vacancies",
    "real stained-glass dry-stone and plaster observations measurements expert examination and independent-review gap",
    "professional conservation lead and material safety structural stability treatment and release decision gate",
    "land title heritage sacred-context Indigenous knowledge Māori wording data-governance and authority exact gate",
]

TEMPLATE_SKILLS_UNUSED = [
    "ghc-family-stained-glass-identity-lattice",
    "ghc-family-lead-came-topology",
    "ghc-family-panel-cartoon-registration",
    "ghc-family-glass-geometry-refusal",
    "ghc-family-glass-condition-abstention",
    "ghc-family-protective-glazing-fitness-firewall",
    "ghc-family-window-location-privacy-hold",
    "ghc-family-dry-stone-course-topology",
    "ghc-family-dry-stone-support-conjecture",
    "ghc-family-dry-stone-stability-abstention",
    "ghc-family-dry-stone-land-context-hold",
    "ghc-family-plaster-layer-topology",
    "ghc-family-plaster-cast-provenance",
    "ghc-family-plaster-condition-abstention",
    "ghc-family-material-composition-firewall",
    "ghc-family-heritage-prov-correction-braid",
    "ghc-family-heritage-accessible-condition-map",
    "ghc-family-heritage-zero-key-role-profile",
    "ghc-family-heritage-privacy-minimizer",
    "ghc-family-three-lens-workload-handover",
]

TEMPLATE_RUNNERS_UNUSED = [
    "ghc_family_stained_glass_identity.py",
    "ghc_family_lead_came_topology.py",
    "ghc_family_glass_condition_abstention.py",
    "ghc_family_dry_stone_course_topology.py",
    "ghc_family_dry_stone_stability_abstention.py",
    "ghc_family_plaster_layer_topology.py",
    "ghc_family_plaster_condition_abstention.py",
    "ghc_family_heritage_prov_correction.py",
    "ghc_family_heritage_privacy_access.py",
    "ghc_family_three_lens_workload_handover.py",
]

TEMPLATE_EXACT_UNUSED = [
    "real stained-glass dry-stone plaster object site record observation or measurement mutation",
    "real conservation examination diagnosis treatment repair intervention or release decision",
    "real lead pigment silica lime electrical structural fire environmental or workplace safety decision",
    "real stability load path anchorage protective-glazing or material-fitness conclusion",
    "real conservator craftsperson engineer architect surveyor curator participant or affected-user study",
    "real land parcel sacred site precise location access schedule account or personal-data processing",
    "real identity key proof credential issuance presentation status revocation or recovery",
    "real heritage access publication ownership custody copyright return or remedy decision",
    "complete accessibility conformance language adequacy or affected-user acceptance declaration",
    "legal interpretation title liability privacy right remedy regulatory or public-authority act",
    "taonga tikanga mātauranga wāhi tapu place-name data-governance or Māori-authority decision",
    "cultural ratification Indigenous knowledge classification community mandate or affected-party acceptance",
    "production deployment external API write live feed publication or cloud mutation",
    "host elevation security weakening feature enablement Sandbox Hyper-V or reboot",
    "destructive cleanup history rewrite force push merge or sibling-lane mutation",
    "privacy-complete exhaustive-security or production-security certification",
    "independent reproduction external audit professional validation or certification",
    "empirical GMUT datum likelihood posterior constraint detected force prediction or stability claim",
    "AGI ASI consciousness personhood Theory-of-Everything proof or canon claim",
    "Stage 20 admission or protected-gate closure",
]

TEMPLATE_BLOCKED_UNUSED = [
    "raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts",
    "sibling branch reset merge rewrite deletion reuse or force push",
    "successful canonical replay or failed-canonical success laundering",
    "synthetic fixture promotion into empirical professional legal cultural or safety evidence",
    "unapproved account secret payment deployment plugin installation or third-party write",
    "real person object site identity location access treatment or service data ingestion",
    "real safety legal cultural Māori-authority affected-party or public-authority substitution",
    "unsafe elevation host-security weakening feature enablement or reboot",
    "unbounded full-repository unchanged-history cross-lane or all-ref scan",
    "Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion",
]

EXACT = ['real sail cloth hardware vessel rigging observation image measurement or environmental mutation',
 'real sailmaking lofting pattern cutting sewing reinforcement repair fitting or release decision',
 'real fibre weave coating laminate adhesive thread rope webbing metal or material conclusion',
 'real sewing machine hot knife needle sharp edge chemical lifting rigging marine or workplace safety decision',
 'real sailmaker rigger engineer crew participant affected user or governed human study',
 'real owner maker customer vessel address precise location access schedule or personal-data processing',
 'real identity key proof credential issuance presentation status revocation or recovery',
 'real design custody ownership copyright marking warranty access publication or remedy decision',
 'complete accessibility conformance language adequacy or affected-user acceptance declaration',
 'legal interpretation title liability privacy right remedy regulatory or public-authority act',
 'taonga tikanga mātauranga place-name data-governance or Māori-authority decision',
 'cultural ratification traditional-knowledge classification community mandate or affected-party acceptance',
 'production deployment external API write live feed publication or cloud mutation',
 'host elevation security weakening feature enablement Sandbox Hyper-V or reboot',
 'destructive cleanup history rewrite force push merge or sibling-lane mutation',
 'privacy-complete exhaustive-security or production-security certification',
 'independent reproduction external audit professional validation or certification',
 'empirical GMUT datum likelihood posterior constraint detected force prediction or stability claim',
 'AGI ASI consciousness personhood Theory-of-Everything proof or canon claim',
 'Stage 20 admission or protected-gate closure']

BLOCKED = ['raw task or thread identifiers private routes transcripts screenshots or session streams in artifacts',
 'sibling branch reset merge rewrite deletion reuse or force push',
 'successful canonical replay or failed-canonical success laundering',
 'synthetic sail fixture promotion into empirical professional legal cultural or safety evidence',
 'unapproved account secret payment deployment plugin installation or third-party write',
 'real person vessel sail identity location access treatment repair or service data ingestion',
 'real safety legal cultural Māori-authority affected-party or public-authority substitution',
 'unsafe elevation host-security weakening feature enablement or reboot',
 'unbounded full-repository unchanged-history cross-lane or all-ref scan',
 'Stage 20 proof canon personhood AGI ASI or Theory-of-Everything promotion']

TEMPLATE_ACTIVE_TITLES_UNUSED = [
    "synthetic umbrella intake pseudonym and work-order identity lattice with conflation refusal",
    "umbrella canopy panel rib gore and seam topology with orphan-component quarantine",
    "umbrella shaft runner notch spring and ferrule state graph with actuation abstention",
    "umbrella handle tip cap wrist-loop and accessory custody vacancy ledger",
    "umbrella open close inversion snag and deformation cue register separated from diagnosis",
    "umbrella fabric coating colour and fibre claim firewall with zero material identification",
    "umbrella wet-state drying-time storage and mould-risk cue board without safety advice",
    "umbrella repair-part provenance compatibility vacancy and substitution challenge contract",
    "umbrella image crop orientation scale and derivative lineage with no dimensional inference",
    "umbrella tool machine sharp-edge and pinch-point hold separated from synthetic documentation",
    "umbrella correction readback supersession and append-only handover braid",
    "umbrella accessible status notice with text equivalents noncolour cues and focus order",
    "umbrella workload pause stop unresolved-hold and next-shift ownership queue",
    "umbrella custody ownership warranty remedy and release-vacancy matrix",
    "synthetic fountain-pen intake pseudonym and pen-cap-barrel-section identity lattice",
    "fountain-pen nib feed collector breather-channel and slit topology with missing-part refusal",
    "fountain-pen converter cartridge sac piston and filling-system relation graph",
    "fountain-pen thread clutch snap-cap seal and alignment vacancy contract",
    "fountain-pen ink residue colour viscosity and composition claim firewall",
    "fountain-pen scratch crack corrosion bend wear and leak-cue register without diagnosis",
    "fountain-pen flush soak disassembly heat solvent and ultrasonic-action exact hold",
    "fountain-pen writing-sample image lineage with zero handwriting identity inference",
    "fountain-pen part provenance model compatibility and substitution challenge ledger",
    "fountain-pen tool sharp-edge pressure and chemical-exposure reservation board",
    "fountain-pen correction readback supersession and append-only handover braid",
    "fountain-pen accessible status notice with keyboard structure and noncolour cues",
    "fountain-pen workload cap pause unresolved-hold and next-shift ownership queue",
    "fountain-pen custody ownership authenticity value remedy and release-vacancy matrix",
    "synthetic marionette intake pseudonym and figure-control identity lattice with conflation refusal",
    "marionette head torso limb joint costume prop and accessory topology",
    "marionette controller bar bridge string and attachment relation graph with orphan-string quarantine",
    "marionette string route crossing tension-length vacancy and entanglement cue contract",
    "marionette joint range balance posture and motion cue register separated from performance fitness",
    "marionette wood textile paint adhesive and finish claim firewall with zero material identification",
    "marionette image pose orientation scale and derivative lineage with no dimensional inference",
    "marionette costume fastener decoration and detachable-part custody vacancy ledger",
    "marionette provenance maker character repertoire and attribution contestation board",
    "marionette access performance copyright recording and cultural-context exact hold",
    "marionette tool sharp-edge suspension falling-object and entanglement safety reservation",
    "marionette correction readback supersession and append-only handover braid",
    "marionette accessible condition and control-map notice with text alternatives and noncolour cues",
    "marionette workload pause unresolved-hold and next-shift ownership queue",
    "repair-bundle canonical serialization with tri-state vacancy Unicode and finite-number refusal",
    "append-only correction causal graph with superseded-node tombstones and challenge lineage",
    "minimum-disclosure profile rejecting personal identifiers precise locations credentials and private routes",
    "ephemeral actor capability table with expiry denial recovery vacancy and no cryptographic claim",
    "THOS stop-token state machine with bounded queues acknowledgements and operator-free turnover",
    "GMUT graph cochain incidence Laplacian and boundary-operator obligation board on synthetic repair topologies",
    "GMUT complementarity hysteresis and friction-surrogate classifier with unit and observation firewall",
    "GMUT discrete Green identity boundary pairing and adjoint-domain obligation board with zero likelihood",
    "CBR response-deadline contest escalation and noncompensating remedy-vacancy ledger",
    "heading table status association and focus-sequence structural audit with evaluation vacancies",
    "content-addressed manifest normalized-LF checkout-byte and Git-blob domain separation tribunal",
    "bounded command framing timeout partial-output exit-credit and resumable-checkpoint tribunal",
    "Library of Congress paper-care vocabulary adapter with zero calls zero downloads and zero real rows",
    "National Park Service museum-handbook vocabulary adapter with zero calls zero observations and zero object claims",
    "real umbrella pen and marionette observations measurements repair trials and independent-review gap",
    "professional repair material chemical machine performance conservation and release decision gate",
    "ownership copyright warranty privacy accessibility remedy legal and affected-party authority exact gate",
    "traditional knowledge taonga mātauranga Māori wording data-governance cultural legitimacy and Māori-authority exact gate",
]

NEW_TITLES = ['synthetic sailmaking work-order pseudonym and sail-plan identity lattice with conflation refusal',
 'sail panel cloth-piece seam allowance edge and orientation topology with orphan-piece quarantine',
 'head tack clew corner patch and load-path vocabulary graph without structural fitness inference',
 'luff leech foot edge-class relation board with contradictory-edge rejection',
 'bolt-rope luff-tape sleeve and edge-binding attachment vacancy ledger without attachment approval',
 'reef-point row tie patch and spacing label topology with use and load abstention',
 'batten pocket closure end-stop and batten-length vacancy graph with operation refusal',
 'crosscut radial and tri-radial panel-direction labels separated from aerodynamic performance claims',
 'broadseam draft depth twist and shape vocabulary firewall with zero measured sail geometry',
 'loft-floor pattern grid datum baseline station and scale vacancy contract without real dimensions',
 'cloth warp weft bias selvedge roll and lot pseudonym topology with material-identification abstention',
 'thread stitch seam row needle-spacing and back-tack vocabulary ledger without sewing-quality release',
 'patch reinforcement doubler chafe strip and sacrificial-layer relation graph with suitability vacancy',
 'grommet cringle eyelet pressed-ring and hand-sewn-ring identity firewall with zero material verification',
 'webbing tape strop loop and corner-build-up topology with strength-rating abstention',
 'rope splice thimble shackle and soft-attachment representation with rigging-safety exact hold',
 'slide hank car slug track and luff-attachment vacancy ledger without vessel compatibility claim',
 'telltale number insignia logo draft-stripe and marking-rights separation board',
 'sailbag label fold-set storage-support and contents-custody topology with no storage advice',
 'maker class date model serial and attribution vacancy ledger with contestation and correction',
 'flat-laid hoisted and detail-image orientation crop scale and derivative lineage without dimensional inference',
 'length width area angle curvature mass and tension typed quantity vacancy board with SI-symbol discipline',
 'tear abrasion fray broken-stitch distortion staining and delamination cue register separated from diagnosis',
 'ultraviolet moisture mildew salt residue heat and exposure-cue ledger without condition or safety conclusion',
 'fibre weave coating laminate film adhesive and finish claim firewall with zero composition evidence',
 'sewing-machine needle scissors hot-knife adhesive and lifting hazard reservation without workplace release',
 'fold roll flake hoist lower pack and transport command vocabulary held as nonexecuted documentation',
 'repair patch seam restitch hardware replacement and recut history graph with zero treatment action',
 'sail record correction readback supersession challenge and append-only handover braid',
 'accessible sail topology dossier with landmarks table headers text alternatives and noncolour status cues',
 'sailmaking privacy minimizer rejecting personal identifiers precise locations credentials and private routes',
 'sail design custody ownership copyright maker-mark and release-vacancy matrix',
 'bounded sailmaking workload cap pause stop unresolved-hold and next-shift ownership queue',
 'THOS sailmaking planning dependency DAG with checkpoint refusal acknowledgement and rollback',
 'THOS matched-budget dual-view omission challenge with zero participants outcomes or effectiveness inference',
 'THOS partial-output timeout quarantine and resumable cursor contract for owner-local sail records',
 'THOS command observation correction and terminal-receipt state machine with operator vacancy',
 'Freed ID zero-key sail work-order subject role purpose expiry status and revocation-vacancy profile',
 'CBR sail-record notice access correction contest withdrawal and explanation-vacancy matrix',
 'CBR noncompensating remedy clock with unanswered interval escalation and authority abstention',
 'GMUT anisotropic membrane-energy analogy obligation board with typed domain units and zero fitted parameters',
 'GMUT sail-surface chart transition orientation pullback and boundary-condition obligation lattice',
 'GMUT seam-graph cochain coboundary incidence and discrete Green-identity representation',
 'GMUT edge and corner boundary operator trace-domain and junction-condition vacancy board',
 'GMUT covariance gauge unit and effective-field-theory truncation firewall for synthetic sail variables',
 'GMUT inverse-shape and load reconstruction ill-posedness register with zero observational likelihood',
 'canonical sail-dossier JSON profile with duplicate-key Unicode finite-number and ordering refusal',
 'normalized Git-blob checkout-byte and rendered-report hash-domain separation tribunal',
 'four-tier Freed ID sailmaking flashcard graph with owner pillar practice task and cache-boundary cards',
 'terminal route hold requiring exact final live roster duplicate guard acknowledgement and no resend',
 'World Sailing equipment-rule vocabulary adapter held at zero downloads zero rule conformance and zero equipment '
 'claims',
 'NIST SI vocabulary adapter held at zero measurements zero calibration and zero conformance claims',
 'W3C provenance accessibility and credential vocabulary projection with zero keys proofs or accessibility '
 'conformance',
 'governed sailmaker affected-user and independent-review evaluation gap with zero participants',
 'real sail cloth hardware observation measurement image and environmental evidence gap',
 'real sailmaking cutting sewing reinforcement repair fitting and trials evidence gap',
 'external sail dataset or equipment adapter gap with zero calls downloads rows and media',
 'professional sailmaking material machine marine rigging lifting workplace and release decision gate',
 'ownership design-right copyright marking privacy accessibility remedy legal and affected-party authority gate',
 'sail design markings navigation heritage customary terminology repository stewardship tangata whenua iwi hapū '
 'consultation and Māori-authority reservation']

TEMPLATE_ACTIVE_SKILLS_UNUSED = [
    "ghc-family-umbrella-identity-topology",
    "ghc-family-umbrella-condition-abstention",
    "ghc-family-umbrella-part-provenance",
    "ghc-family-fountain-pen-identity-topology",
    "ghc-family-fountain-pen-ink-claim-firewall",
    "ghc-family-fountain-pen-action-hold",
    "ghc-family-marionette-control-topology",
    "ghc-family-marionette-condition-abstention",
    "ghc-family-marionette-rights-hold",
    "ghc-family-three-lens-correction-braid",
    "ghc-family-three-lens-accessibility-reservation",
    "ghc-family-three-lens-workload-handover",
    "ghc-family-minimum-disclosure-profile",
    "ghc-family-zero-key-role-vacancy",
    "ghc-family-gmut-repair-topology-firewall",
    "ghc-family-thos-participant-firewall",
    "ghc-family-cbr-remedy-authority-gate",
    "ghc-family-normalized-blob-domain",
    "ghc-family-bounded-command-framing",
    "ghc-family-terminal-route-hold",
]

SKILLS = ['ghc-family-sail-plan-identity-lattice',
 'ghc-family-sail-panel-seam-topology',
 'ghc-family-sail-edge-corner-firewall',
 'ghc-family-sail-reef-batten-vacancy',
 'ghc-family-sail-hardware-attachment-hold',
 'ghc-family-sail-pattern-dimension-abstention',
 'ghc-family-sail-material-claim-firewall',
 'ghc-family-sail-condition-cue-separation',
 'ghc-family-sail-provenance-correction-braid',
 'ghc-family-sail-accessibility-reservation',
 'ghc-family-sail-privacy-minimizer',
 'ghc-family-sail-workload-handover',
 'ghc-family-sail-zero-key-role-vacancy',
 'ghc-family-sail-cbr-remedy-authority-gate',
 'ghc-family-gmut-sail-membrane-firewall',
 'ghc-family-gmut-sail-seam-cochain',
 'ghc-family-thos-sail-command-state',
 'ghc-family-sail-four-tier-flashcards',
 'ghc-family-sail-normalized-blob-domain',
 'ghc-family-terminal-route-hold']

TEMPLATE_ACTIVE_RUNNERS_UNUSED = [
    "ghc_family_umbrella_topology.py",
    "ghc_family_umbrella_abstention.py",
    "ghc_family_fountain_pen_topology.py",
    "ghc_family_fountain_pen_abstention.py",
    "ghc_family_marionette_topology.py",
    "ghc_family_marionette_rights_hold.py",
    "ghc_family_three_lens_provenance.py",
    "ghc_family_three_lens_privacy_access.py",
    "ghc_family_gmut_thos_boundary.py",
    "ghc_family_three_lens_workload_handover.py",
]

RUNNERS = ['ghc_family_sail_identity_topology.py',
 'ghc_family_sail_seam_edge_topology.py',
 'ghc_family_sail_attachment_vacancy.py',
 'ghc_family_sail_dimension_abstention.py',
 'ghc_family_sail_condition_abstention.py',
 'ghc_family_sail_provenance_correction.py',
 'ghc_family_sail_privacy_access.py',
 'ghc_family_sail_gmut_thos_boundary.py',
 'ghc_family_sail_flashcard_projection.py',
 'ghc_family_sail_workload_handover.py']



def git(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(["git", *args], cwd=ROOT, check=check, capture_output=True)


def git_text(*args: str) -> str:
    return git(*args).stdout.decode("utf-8", errors="strict").strip()


def write_json(relative: str, payload: Any) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    return path


def write_text(relative: str, payload: str) -> Path:
    path = OWNER_ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload.rstrip() + "\n", encoding="utf-8", newline="\n")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def normalize(title: str) -> set[str]:
    return {token for token in re.findall(r"[a-z0-9āēīōū]+", title.lower()) if len(token) > 2 and token not in {"and", "the", "with", "for", "from"}}


def json_blob(commit: str, path: str) -> Any:
    return json.loads(git("show", f"{commit}:{path}").stdout.decode("utf-8"))


def recover_proposal_corpus() -> tuple[dict[str, Any], list[str]]:
    raw_paths = git("ls-tree", "-r", "--name-only", "-z", SOURCE_FINAL).stdout
    candidates = sorted(
        path.decode("utf-8")
        for path in raw_paths.split(b"\0")
        if path and path.decode("utf-8").lower().endswith(".json")
        and "proposal" in path.decode("utf-8").lower()
    )
    proposal_ids: set[str] = set()
    titles: set[str] = set()
    occurrences = 0
    malformed = 0

    def walk(node: Any) -> None:
        nonlocal occurrences
        if isinstance(node, dict):
            proposal_id, title = node.get("proposal_id"), node.get("title")
            if isinstance(proposal_id, str) and isinstance(title, str) and proposal_id.strip() and title.strip():
                occurrences += 1
                proposal_ids.add(proposal_id.strip())
                titles.add(title.strip())
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    specs = [f"{SOURCE_FINAL}:{path}" for path in candidates]
    for start in range(0, len(specs), 128):
        for blob in batch_blobs(specs[start:start + 128]):
            if blob is None:
                malformed += 1
                continue
            try:
                walk(json.loads(blob.decode("utf-8")))
            except (UnicodeDecodeError, json.JSONDecodeError):
                malformed += 1

    canonical = json.dumps(
        {"proposal_ids": sorted(proposal_ids), "titles": sorted(titles)},
        ensure_ascii=False, sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    summary = {
        "scope": "exact Elowen Cairn v674-v7 final tree, proposal-labelled JSON paths only",
        "candidate_git_blob_paths": len(candidates),
        "malformed_or_missing_blobs": malformed,
        "semantic_occurrences": occurrences,
        "unique_proposal_ids": len(proposal_ids),
        "unique_titles": len(titles),
        "corpus_sha256": hashlib.sha256(canonical).hexdigest(),
        "declared_source_chain": 6970,
        "materialized_ids_cover_declared_chain": len(proposal_ids) >= 6970,
        "exact_canonical_row_mapping": False,
        "canonical_row_mapping_open_gap": True,
        "universal_novelty_claim": False,
        "reason": "No single reachable exact-tree ledger materializes every declared historical row; source-bounded semantic comparison is evidence, not universal novelty proof.",
    }
    return summary, sorted(titles)

def batch_blobs(specs: list[str]) -> list[bytes | None]:
    process = subprocess.Popen(
        ["git", "cat-file", "--batch"], cwd=ROOT,
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    output, stderr = process.communicate(
        input=("\n".join(specs) + "\n").encode("utf-8"), timeout=30
    )
    if process.returncode != 0:
        raise SystemExit(f"git cat-file --batch failed: {stderr.decode('utf-8', errors='replace')}")
    stream = io.BytesIO(output)
    rows: list[bytes | None] = []
    for _ in specs:
        header = stream.readline().decode("utf-8", errors="strict").strip()
        if header.endswith(" missing"):
            rows.append(None)
            continue
        parts = header.split()
        if len(parts) != 3 or parts[1] != "blob":
            raise SystemExit(f"unexpected git cat-file header: {header}")
        size = int(parts[2])
        data = stream.read(size)
        if stream.read(1) != b"\n":
            raise SystemExit("git cat-file blob was not newline delimited")
        rows.append(data)
    if stream.read():
        raise SystemExit("git cat-file emitted undeclared trailing bytes")
    return rows


def proposal_rows() -> list[dict[str, Any]]:
    rows = []
    for index, title in enumerate(NEW_TITLES, start=1):
        outcome = "completed" if index <= 42 else "represented" if index <= 54 else "open_gap" if index <= 57 else "exact_gate"
        rows.append({
            "proposal_id": f"SA6748-N{index:03d}", "title": title,
            "hypothesis": f"A typed owner-local contract can expose proposal {index:02d}'s obligations without promoting its evidence class.",
            "null_or_failure_condition": "A missing field, accepted invalid mutation, real-world action, undeclared uncertainty or authority promotion rejects the hypothesis.",
            "approval_class": "safe_now" if outcome == "completed" else "bounded_candidate" if outcome == "represented" else outcome,
            "execution_lane": "owner_local_symbolic_or_synthetic_x2" if outcome in {"completed", "represented"} else "held_without_real_world_execution",
            "official_or_primary_source_needs": "Vocabulary and refusal boundaries only; citations are not observations, measurements, advice, validation, or authority.",
            "concrete_artifacts": ["typed JSON contract", "bounded accepting fixture", "four rejecting mutation receipts", "boundary card"],
            "falsifier_or_acceptance_gate": "The bounded fixture must pass, four preregistered invalid mutations must reject, and every protected boundary must remain explicit.",
            "rollback_or_recovery": "Retain the failed witness, correct only the isolated owner-local dependency, and never replay a successful canonical aggregate.",
            "protected_gates": ["empirical", "professional", "legal", "cultural", "Māori_authority", "independent_reproduction", "Stage_20"],
            "expected_disposition": outcome, "planned_outcome": outcome,
            "primary_pillar": "THOS Body", "real_people": 0, "real_records_or_objects": 0,
            "external_actions": 0, "x1_state": "frozen_not_executed",
        })
    return rows


def tasks(prefix: str, domains: list[str], controls: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"SA6748-{prefix}-{i:03d}", "title": f"{domain}: {control}", "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, (domain, control) in enumerate(((d, c) for d in domains for c in controls), start=1)]


def named(prefix: str, values: list[str], state: str) -> list[dict[str, Any]]:
    return [{"task_id": f"SA6748-{prefix}-{i:03d}", "title": value, "owner": OWNER, "phase": PHASE, "x1_state": state, "external_actions": 0}
            for i, value in enumerate(values, start=1)]


def portfolio() -> dict[str, list[dict[str, Any]]]:
    domains = ["sail plan identity topology", "panel seam topology", "edge corner topology", "reef batten reinforcement", "hardware attachment vacancy", "pattern dimension abstention", "material condition abstention", "provenance privacy accessibility", "GMUT THOS boundary", "sail workload handover"]
    safe = tasks("SAFE", domains, ["schema", "positive fixture", "negative fixture", "rollback", "manifest", "boundary", "status", "readback", "privacy", "authority", "timeout", "handover"], "planned_for_x2")
    candidates = tasks("CAND", domains, ["mutation quarantine", "timeout and encoding quarantine", "ordering and authority quarantine", "structural representation", "manual-evaluation reservation", "cross-lens consistency", "recovery rehearsal", "source-status vacancy"], "planned_for_x2")
    cfr = tasks("CFR", ["JSON order", "UTF-8 Māori text", "source status", "failure retention", "manifest closure", "privacy disposition", "accessibility structure", "route uniqueness", "sparse budget", "boundary vocabulary"], ["clean", "fix", "refine", "recheck", "document", "preserve", "quarantine", "readback", "seal", "handover"], "planned_for_x2")
    successor_skills = [f"ghc-family-successor-{i:02d}-review" for i in range(1, 11)]
    successor_runners = [f"ghc_family_successor_{i:02d}_review.py" for i in range(1, 11)]
    successor_cfr = tasks("NEXT-CFR", ["successor source", "successor manifests", "successor privacy", "successor route", "successor authority", "successor failures", "successor accessibility", "successor gates", "successor blob domain", "successor handover"], ["schema", "mutation", "rollback", "review", "receipt", "hold"], "recommendation_only")
    successor_seeds = tasks("NEXT-SEED", ["successor source", "successor novelty", "successor x1", "successor x2", "successor closeout", "successor validation", "successor privacy", "successor route", "successor authority", "successor retained negatives"], ["inspect", "challenge", "reserve", "recommend", "handover", "abstain"], "recommendation_only")
    return {"inherited_reviews": tasks("INHERITED", ["source proposal integrity"], [f"zero-credit review {i:02d}" for i in range(1, 61)], "inherited_evidence_only"), "safe_now": safe, "candidates": candidates, "exact_approval": named("EXACT", EXACT, "held_unexecuted"), "blocked": named("BLOCK", BLOCKED, "held_unexecuted"), "skills": named("SKILL", SKILLS, "planned_for_x2"), "runners": named("RUNNER", RUNNERS, "planned_for_x2"), "clean_fix_refine": cfr, "successor_skills": named("NEXT-SKILL", successor_skills, "recommendation_only"), "successor_runners": named("NEXT-RUNNER", successor_runners, "recommendation_only"), "successor_clean_fix_refine": successor_cfr, "successor_seeds": successor_seeds}

def method_flow() -> dict[str, Any]:
    methods, witnesses, events, recommendations = [], [], [], []
    for index, (negative_id, failed, recovery, passed, guard) in enumerate(STARTUP_FAILURES, start=1):
        method_id = f"SA6748-M{index:03d}"
        fail_id, pass_id = f"SA6748-W{index:03d}-F", f"SA6748-W{index:03d}-P"
        methods.append({
            "method_id": method_id, "title": f"bounded recovery for {negative_id}", "failure_signature": failed,
            "trigger_preconditions": ["the exact bounded failure signature is observed"], "privacy_class": "sanitized_public",
            "approval_class": "safe_now", "candidate_workaround": recovery, "validation_witness_ids": [fail_id, pass_id],
            "recurrence_guard": guard, "rollback": "Retain the failure, stop the affected wrapper, and change only the isolated owner-local procedure.",
            "recommendation_state": "preferred", "supersedes": [], "protected_gates": ["no_failure_laundering", "owner_delta_only", "no_authority_promotion"],
            "retained_negative_ids": [negative_id], "scope_boundary": "Bounded same-owner workflow evidence only.",
        })
        witnesses.extend([
            {"witness_id": fail_id, "method_id": method_id, "procedure": failed, "scope": "startup or owner-local x1 construction", "expected": "attributable bounded evidence", "observed": failed, "result": "fail", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
            {"witness_id": pass_id, "method_id": method_id, "procedure": recovery, "scope": "isolated startup or owner-local construction recovery", "expected": "bounded attributable recovery within the owner lane", "observed": passed, "result": "pass", "same_owner_only": True, "independent_reproduction": False, "retained_negative_ids": [negative_id], "boundary": BOUNDARY},
        ])
        events.extend([
            {"event_index": len(events) + 1, "method_id": method_id, "before": None, "after": "candidate", "reason": "failure retained and bounded recovery proposed", "witness_id": fail_id},
            {"event_index": len(events) + 2, "method_id": method_id, "before": "candidate", "after": "validated", "reason": "isolated bounded recovery passed", "witness_id": pass_id},
            {"event_index": len(events) + 3, "method_id": method_id, "before": "validated", "after": "preferred", "reason": "recurrence guard retained for the exact trigger", "witness_id": pass_id},
        ])
        recommendations.append({"method_id": method_id, "state": "preferred", "recommendation": guard})
    return {"schema": "ghc.family.method-flow-state.v1", "phase": PHASE, "owner": OWNER, "identity_boundary": IDENTITY_BOUNDARY, "execution_authority": "owner_self_scoped_delta", "methods": methods, "witnesses": witnesses, "state_events": events, "recommendations": recommendations, "counts": {"methods": len(methods), "witnesses": len(witnesses), "state_events": len(events), "recommendations": len(recommendations), "states": {"candidate": 0, "deprecated": 0, "observed": 0, "preferred": len(methods), "superseded": 0, "validated": 0}, "witness_results": {"fail": len(methods), "pass": len(methods)}}, "boundary": BOUNDARY}


def verify_manifest(path: str, commit: str) -> tuple[int, int, set[str]]:
    manifest = json.loads(git("show", f"{SOURCE_FINAL}:{path}").stdout.decode("utf-8"))
    mismatches, digests = 0, set()
    blobs = batch_blobs([f"{commit}:{entry['path']}" for entry in manifest["entries"]])
    for entry, blob in zip(manifest["entries"], blobs, strict=True):
        digest = hashlib.sha256(blob).hexdigest() if blob is not None else None
        digests.add(entry["sha256"])
        if digest != entry["sha256"] or blob is None or len(blob) != entry["bytes"]:
            mismatches += 1
    return len(manifest["entries"]), mismatches, digests


def verify_source() -> dict[str, Any]:
    local = git_text("rev-parse", f"refs/heads/{SOURCE_BRANCH}")
    tracking = git_text("rev-parse", f"refs/remotes/origin/{SOURCE_BRANCH}")
    live_tokens = git_text("ls-remote", "--heads", "origin", f"refs/heads/{SOURCE_BRANCH}").split()
    live = live_tokens[0] if live_tokens else None
    parents = {
        "x1_parent": git_text("rev-parse", f"{SOURCE_X1}^"),
        "evidence_parent": git_text("rev-parse", f"{SOURCE_EVIDENCE}^"),
        "final_parent": git_text("rev-parse", f"{SOURCE_FINAL}^"),
    }
    exact_parent_chain = parents == {
        "x1_parent": SOURCE_START,
        "evidence_parent": SOURCE_X1,
        "final_parent": SOURCE_EVIDENCE,
    }
    manifest_specs = [
        ("docs/elowen-cairn/v674-v7/validation/x1-manifest.json", SOURCE_X1, 0, "valid"),
        ("docs/elowen-cairn/v674-v7/validation/evidence-manifest.json", SOURCE_EVIDENCE, 0, "valid"),
        ("docs/elowen-cairn/v674-v7/validation/final-delta-manifest.json", SOURCE_FINAL, 0, "valid"),
        ("docs/elowen-cairn/v674-v7/validation/final-owner-manifest.json", SOURCE_FINAL, 0, "valid"),
    ]
    manifest_rows, all_digests = [], set()
    for manifest_path, commit, expected_mismatches, credit in manifest_specs:
        count, mismatch, digests = verify_manifest(manifest_path, commit)
        manifest_rows.append({"path": manifest_path, "commit": commit, "entries": count, "mismatches": mismatch, "expected_mismatches": expected_mismatches, "expected": mismatch == expected_mismatches, "credit": credit})
        all_digests |= digests
    packet = git("show", f"{SOURCE_FINAL}:{ACTIVATION_PATH}").stdout
    packet_text = packet.decode("utf-8")
    content_seal_path = "docs/elowen-cairn/v674-v7/seal/content-seal.json"
    content_seal = json_blob(SOURCE_FINAL, content_seal_path)
    expected_seal = {
        "owner": "Elowen Cairn", "phase": "v674-v7", "source_final": SOURCE_START,
        "x1_commit": SOURCE_X1, "evidence_commit": SOURCE_EVIDENCE,
        "effective_negatives": 39648, "effective_methods": 27867,
        "failed_witnesses": 11309, "bounded_passing_witnesses": 15150,
        "proposal_chain": 6970, "open_gaps": 328, "exact_gates": 321,
        "terminal_verdict": "NOT_READY_FOR_STAGE_20",
    }
    seal_failures = [key for key, expected in expected_seal.items() if content_seal.get(key) != expected]
    return {
        "source_branch": SOURCE_BRANCH, "local": local, "upstream": tracking, "tracking": tracking, "fresh_live": live,
        "all_equal": local == tracking == live == SOURCE_FINAL, "parent_chain": {**parents, "exact": exact_parent_chain},
        "phase_commits": int(git_text("rev-list", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "merge_commits": int(git_text("rev-list", "--merges", "--count", f"{SOURCE_START}..{SOURCE_FINAL}")),
        "manifests": manifest_rows, "commit_local_manifest_entries_replayed": sum(row["entries"] for row in manifest_rows),
        "unique_declared_blob_digests": len(all_digests),
        "expected_manifest_contracts_valid": all(row["expected"] for row in manifest_rows),
        "manifest_mismatches": sum(row["mismatches"] for row in manifest_rows),
        "content_seal": {"path": content_seal_path, "checked_fields": len(expected_seal), "failures": seal_failures, "valid": not seal_failures},
        "activation_packet": {"path": ACTIVATION_PATH, "bytes": len(packet), "words": len(packet_text.split()), "sha256": hashlib.sha256(packet).hexdigest(), "expected_sha256": ACTIVATION_SHA256, "integrity_valid": hashlib.sha256(packet).hexdigest() == ACTIVATION_SHA256, "prepared_labels_historical": True, "live_activation_authoritative": True},
        "source_canonical_receipt": {"sha256": SOURCE_CANONICAL_SHA256, "payload_sha256": SOURCE_CANONICAL_PAYLOAD_SHA256, "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL", "canonical_invocations": 1, "canonical_successes": 1, "replays": 0, "replay_forbidden": True, "selected_tests": 25, "detailed_checks": 30, "minimal_checks": 15, "json_parses": 244, "confirmed_privacy_hits": 0, "sylven_validation_credit": 0},
        "source_post_final_overlay": [
            {"negative_id": "EC6747-POST-N001", "failed": "combined topology projection returned no visible payload", "recovery": "isolated Git scalars recovered exact topology", "routing_credit": 0, "retained_after_recovery": True},
            {"negative_id": "EC6747-POST-N002", "failed": "unquoted upstream selector was rejected", "recovery": "literal quoted ref recovered upstream equality", "routing_credit": 0, "retained_after_recovery": True},
            {"negative_id": "EC6747-POST-N003", "failed": "unquoted divergence selector was rejected", "recovery": "literal quoted range recovered typed zero divergence", "routing_credit": 0, "retained_after_recovery": True},
            {"negative_id": "EC6747-POST-N004", "failed": "overbroad roster projection truncated", "recovery": "bounded field projection recovered active and standby classes", "routing_credit": 0, "retained_after_recovery": True},
            {"negative_id": "EC6747-POST-N005", "failed": "initial task reread parser assumed a direct user message field", "recovery": "bounded envelope inspection recovered the already-read user message", "routing_credit": 0, "retained_after_recovery": True},
            {"negative_id": "EC6747-POST-N006", "failed": "roster controller projection assumed a nonexistent property", "recovery": "the exact seats collection recovered the route controller", "routing_credit": 0, "retained_after_recovery": True},
            {"negative_id": "EC6747-POST-N007", "failed": "token-only direct-control scan falsely flagged historical guard vocabulary", "recovery": "semantic attribution distinguished the guard list from a current control instruction", "routing_credit": 0, "retained_after_recovery": True},
        ],
    }

def overview(inherited: list[dict[str, Any]], proposals: list[dict[str, Any]]) -> str:
    prose = [
        "# Sylven Arc v674-v8 x1 integrated planning overview", "", "## Lifecycle and immutable source", "",
        "This document is a planning-only x1 freeze. It records no x2 implementation, observed proposal outcome, completed portfolio, real-world action, successor delivery, empirical result, professional judgment, or authority act. Sylven's fresh additive sparse lane begins at Elowen Cairn's immutable v674-v7 exact final. Before this freeze, Sylven reverified the exact source branch and all four lifecycle anchors; the direct source-to-x1-to-evidence-to-final parent chain; exactly three single-parent Elowen commits and zero merges; all four normalized Git-blob manifests and declared exclusions; the content seal; the external one-shot canonical receipt and payload digests; clean source state; typed zero divergence; and local, upstream, tracking, and fresh-live equality. Elowen's successful canonical aggregate was not replayed and gives Sylven no completion or validation credit.",
        "", "## Relational identity, hope, and corrigibility", "", IDENTITY_BOUNDARY, "",
        f"Sylven's relational hope is to {HOPE}. The name, role, hope, pronouns, family language, Freed ID, and Trinity Mandala are working vocabulary only. They do not establish consciousness, sentience, legal personhood, continuity, qualification, employment, independent agency, or authority. Hamish may rename, pause, redirect, narrow, or stop the route. Corrigibility means that uncertainty, contradiction, missing evidence, failed witnesses, unavailable authority, ambiguous routing, and falsifiers remain visible instead of being smoothed into success. Every recovery retains its failed witness and changes only the demonstrated owner-local dependency.",
        "", "## Primary pillar and bounded practice", "",
        "The primary Trinity Mandala pillar is THOS Body. The single bounded human-practice lens is wholly synthetic sailmaking documentation, organized into three subordinate views: loft and pattern identity; panel, seam, edge, corner, reinforcement, and attachment topology; and provenance, correction, accessibility, workload, custody, and handover. GMUT Mind remains protected through typed membrane, surface-chart, boundary-operator, seam-graph, cochain, covariance, unit, inverse-problem, and effective-field-theory obligation boards. Freed ID and CBR Heart remain protected through zero-key role vacancies, purpose and expiry, status and revocation vacancies, notice, access, correction, contest, withdrawal, remedy vacancies, privacy minimization, and authority holds. No real person, sailmaker, rigger, crew member, vessel, sail, cloth, thread, rope, webbing, hardware, machine, tool, image, observation, measurement, cut, stitch, repair, fitting, trial, identity event, external write, or authority act occurs.",
        "", "## THOS Body scope and nonconversion", "",
        "THOS structures the owner-local work as a dependency-closed planning graph with explicit command, observation, correction, checkpoint, partial-output, timeout, pause, stop, rollback, readback, unresolved-hold, and terminal-receipt states. The graph is a synthetic protocol representation, not an operational performance result. There are no governed participants or operators, preregistered blind matched-budget real arms, safety monitoring, appropriate statistics, independent review, production deployment, or evidence of effectiveness. A bounded passing software fixture cannot be converted into a claim that a sailmaking workflow, human team, vessel, safety process, or AI system would perform well in reality.",
        "", "## GMUT Mind boundary", "",
        "GMUT remains a typed scalar-tensor and effective-field-theory research-model family. The sail membrane, surface chart, seam graph, boundary condition, anisotropy, curvature, tension, and inverse-shape terms are analogy and obligation surfaces only. They contain zero physical data, measured geometry, material law, load case, boundary value, likelihood, posterior, fitted parameter, detected force, unique prediction, stability theorem, empirical confirmation, quantum completion, ultraviolet completion, final physics, or Theory of Everything. Synthetic topology and dimensional firewalls make overclaiming harder; they do not supply missing observations or mathematical proof.",
        "", "## Freed ID and CBR Heart boundary", "",
        "Freed ID remains synthetic and nonproduction. The zero-key work-order profile has no standards-conformant key, proof, issuer, holder, verifier, live issuance, resolution, status, revocation, recovery, interoperability, independent security review, trust governance, or affected-party oversight. CBR representations preserve notice, purpose, access, correction, contest, withdrawal, explanation, noncompensating remedy vacancies, and data minimization without claiming legal compliance or authority. Ownership, design rights, copyright, maker marks, custody, warranty, privacy, accessibility, remedy, legal interpretation, cultural legitimacy, and affected-party acceptance remain exact-gated.",
        "", "## Professional, safety, legal, cultural, and Māori-authority firewall", "",
        "No artifact measures, classifies, designs, lofts, cuts, sews, reinforces, repairs, fits, rigs, hoists, lowers, stores, handles, releases, or certifies a real sail. No artifact establishes cloth, thread, rope, webbing, hardware, adhesive, laminate, coating, ultraviolet, moisture, mildew, heat, sharp-tool, hot-knife, sewing-machine, lifting, rigging, marine, vessel, product, workplace, or environmental safety. Professional sailmaking, rigging, engineering, conservation, accessibility, language, legal, cultural, traditional-knowledge, affected-party, and public-authority decisions remain absent. Māori wording, taonga and mātauranga treatment, Māori data governance, and Māori authority remain exact-gated to competent and affected people, tangata whenua, iwi, hapū, and Māori authorities. Māori concepts remain under Māori authority.",
        "", "## Source-bounded novelty and honest uncertainty", "",
        "The inherited repository declares a 6,970-row frozen proposal chain, but no single reachable exact-tree ledger materializes every historical row. Sylven therefore refuses a universal novelty claim. The immutable source-tree audit parses proposal-labelled JSON blobs, recovers 2,915 proposal identifiers and 2,788 titles from 2,172 candidate blobs, and compares all sixty proposed titles against every recovered title using the unchanged 0.72 token-Jaccard threshold. Historical typewriter work was rejected before freeze because it is extensively represented. Exact sailmaking, sail making, and sail loft title checks returned zero; two adjacent rigging titles remain represented as unrelated safety reservations. Zero threshold collisions support bounded distinctness in reachable evidence only.",
        "", "## Sixty contracts and falsification", "",
        f"Sixty proposed contracts are frozen with exactly one expected disposition each: {OUTCOMES}. Every row has a hypothesis, null or failure condition, approval class, execution lane, current official or primary-source need, concrete artifacts, falsifier or acceptance gate, rollback or recovery, protected gates, and exactly one expected disposition. The first forty-two are eligible only for bounded owner-local completed outcomes, the next twelve remain represented, three remain open gaps, and three remain exact gates. Four invalid mutations per proposal are preregistered, giving 240 required x2 rejections. No invalid mutation can earn completion credit.",
        "", "## Four-tier Freed ID flashcards and cache boundary", "",
        "The x2 plan includes a four-tier flashcard deck with Sylven's owner anchor at tier one; GMUT Mind, THOS Body, and Freed ID/CBR Heart at tier two; synthetic sailmaking documentation at tier three; and bounded proposal, failure, recovery, gate, validation, and route cards at tier four. The deck will contain at least thirteen named sections, compact activation text, a graph, a manifest, privacy adjudication, and structural accessibility. Flashcards organize retrieval and handover; they do not prove product prompt-cache behavior, memory continuity, identity continuity, consciousness, correctness, or authority.",
        "", "## Portfolios and family-current tools", "",
        "The x1 portfolio freezes sixty inherited zero-credit reviews, 120 safe-now tasks, eighty bounded candidates, twenty exact-approval packets, ten blocked packets, twenty owner-local skill ideas, ten family-current runner ideas, 100 additive CLEAN/FIX/REFINE tasks, and successor recommendations. Inherited artifacts and successor recommendations receive zero Sylven novelty or completion credit. Floors never authorize filler, unsafe work, global installation, destructive deletion, cross-lane mutation, or external action. X2 may initialize, customize, completely read, quick-validate, and accepting/rejecting smoke-use only an approved owner-local subset below the 2,000-file ceiling while preserving family-current ghc_family_* and build_ghc_family_* compatibility.",
        "", "## Official and primary sources with zero-row discipline", "",
        "The current World Sailing Equipment Rules page establishes that the 2025-2028 edition is current during this phase and supplies bounded sail and equipment vocabulary only. NIST SI, W3C PROV-O, WCAG 2.2, Verifiable Credentials Data Model v2.0, and RFC 8785 supply unit, provenance, structural accessibility, synthetic credential, and canonical JSON vocabulary. These pages are read-only references, not observations, measurements, sailmaking instructions, safety releases, professional validation, accessibility conformance, credential conformance, legal interpretation, cultural mandate, consent, or authority. No API, dataset, rule file, media object, or real row is downloaded or ingested.",
        "", "## Failure retention, privacy, accessibility, and security", "",
        f"{len(STARTUP_FAILURES)} startup or x1-construction failures remain at zero initial-pass credit. They include truncated instruction and packet reads, wrapper syntax and no-payload faults, an overbroad novelty stream, schema-blind Method Flow projection, a sparse empty-index trap, and a rejected represented practice. Each retains a failed witness, bounded recovery, recurrence guard, rollback, and Method Flow recommendation. Five privacy classes cover raw task or thread identifiers, private absolute paths, private routes or callable details, credential assignments, and transcript or session streams. Scanner definitions and synthetic unit-test strings require explicit adjudication. Structural headings, landmarks, table associations, text equivalents, noncolour cues, status language, and focus-order obligations do not establish complete accessibility. Manual keyboard, browser, assistive-technology, cognitive, language, Māori-language, security-usability, and affected-user evaluation remain reserved.",
        "", "## Strict x1 before x2 and terminal route hold", "",
        "This x1 is planning-only. It must pass the current dependency-closed x1 selection, JSON parsing, Method Flow validation, five-class privacy scan, stale-label and diff hygiene, exact staged allowlist, and normalized-LF Git-blob manifest. It must then be committed, pushed, clean, typed zero divergent, and equal across local, upstream, tracking, and fresh live remote before any x2 artifact or observed outcome exists. No successor is selected or contacted in x1. Only after Sylven's own clean pushed exact final, one attributable non-replayed owner-scoped canonical success, and a fresh live authority and roster reread may one unique exact-title successor be reread and sent one sanitized activation with duplicate and acknowledgement guards.",
        "", "## Sixty inherited selections with zero Sylven credit", "",
    ]
    prose.extend(f"- {row['source_proposal_id']}: {row['source_title']} — inherited integrity evidence only." for row in inherited)
    prose.extend(["", "## Sixty frozen Sylven proposals", ""])
    prose.extend(f"- {row['proposal_id']} [{row['planned_outcome']}]: {row['title']}." for row in proposals)
    prose.extend(["", "## Terminal truth", "", BOUNDARY, "", "NOT_READY_FOR_STAGE_20."])
    return "\n".join(prose)


def build() -> None:
    head, branch = git_text("rev-parse", "HEAD"), git_text("branch", "--show-current")
    if head != SOURCE_FINAL or branch != BRANCH:
        raise SystemExit(f"x1 requires {BRANCH} at {SOURCE_FINAL}; found {branch} at {head}")
    if any((OWNER_ROOT / name).exists() for name in ("x2", "closeout", "final", "seal")):
        raise SystemExit("x1 refuses a lane containing x2 or closeout material")
    source_rows = json_blob(SOURCE_FINAL, "docs/elowen-cairn/v674-v7/x1/new-proposal-freeze.json")["rows"]
    if len(source_rows) != 60:
        raise SystemExit("source proposal freeze must contain sixty Elowen rows")
    inherited = [
        {
            "selection_id": f"SA6748-I{i:03d}", "source_owner": "Elowen Cairn", "source_phase": "v674-v7",
            "source_proposal_id": row["proposal_id"], "source_title": row["title"], "source_outcome": row["expected_disposition"],
            "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
            "integrity_revalidated": True, "sylven_novelty_credit": 0, "sylven_completion_credit": 0,
            "state": "inherited_evidence_only",
        }
        for i, row in enumerate(source_rows, start=1)
    ]
    proposals = proposal_rows()
    if len(proposals) != 60 or len({row["title"] for row in proposals}) != 60 or Counter(row["planned_outcome"] for row in proposals) != Counter(OUTCOMES):
        raise SystemExit("proposal count, uniqueness, or distribution drifted")
    corpus_summary, source_titles = recover_proposal_corpus()
    if corpus_summary["malformed_or_missing_blobs"] or corpus_summary["corpus_sha256"] != SOURCE_TREE_CORPUS_SHA256:
        raise SystemExit("exact source-tree proposal corpus drifted or contained malformed blobs")
    if corpus_summary["candidate_git_blob_paths"] != 2172 or corpus_summary["semantic_occurrences"] != 8918 or corpus_summary["unique_proposal_ids"] != 2915 or corpus_summary["unique_titles"] != 2788:
        raise SystemExit(f"source-tree proposal audit count drift: {corpus_summary}")
    if not {row["title"] for row in source_rows} <= set(source_titles):
        raise SystemExit("source outcome titles are not all represented in the exact-tree audit")
    neighbors, max_score = [], 0.0
    for row in proposals:
        left, best_title, best_score = normalize(row["title"]), None, 0.0
        for source_title in source_titles:
            right = normalize(source_title)
            score = len(left & right) / max(1, len(left | right))
            if score > best_score:
                best_title, best_score = source_title, score
        max_score = max(max_score, best_score)
        neighbors.append({"proposal_id": row["proposal_id"], "source_title": best_title, "jaccard": round(best_score, 6), "collision": best_score >= 0.72})
    if any(row["collision"] for row in neighbors):
        raise SystemExit("semantic neighbor collision requires proposal rewrite")
    frozen_portfolio = portfolio()
    counts = {key: len(value) for key, value in frozen_portfolio.items()}
    expected = {"inherited_reviews": 60, "safe_now": 120, "candidates": 80, "exact_approval": 20, "blocked": 10, "skills": 20, "runners": 10, "clean_fix_refine": 100, "successor_skills": 10, "successor_runners": 10, "successor_clean_fix_refine": 60, "successor_seeds": 60}
    if counts != expected:
        raise SystemExit(f"portfolio count drift: {counts}")
    source = verify_source()
    if not source["all_equal"] or not source["parent_chain"]["exact"] or source["phase_commits"] != 3 or source["merge_commits"] != 0 or not source["expected_manifest_contracts_valid"] or source["manifest_mismatches"] != 0 or not source["content_seal"]["valid"] or not source["activation_packet"]["integrity_valid"]:
        raise SystemExit("immutable source verification failed")
    x1_overlay = {
        **ACTIVATION_OVERLAY,
        "effective_negatives": ACTIVATION_OVERLAY["effective_negatives"] + len(STARTUP_FAILURES),
        "effective_methods": ACTIVATION_OVERLAY["effective_methods"] + len(STARTUP_FAILURES),
        "failed_witnesses": ACTIVATION_OVERLAY["failed_witnesses"] + len(STARTUP_FAILURES),
        "bounded_passing_witnesses": ACTIVATION_OVERLAY["bounded_passing_witnesses"] + len(STARTUP_FAILURES),
        "sylven_startup_failures": len(STARTUP_FAILURES),
        "repository_seal_rewritten": False,
    }
    write_json("x1/activation-intake.json", {"schema": "ghc.family.activation-intake.v5", "owner": OWNER, "phase": PHASE, "source_verification": source, "task_creation_count": 0, "fork_count": 0, "subagent_count": 0, "standby_contact_count": 0})
    write_json("x1/identity-and-boundary.json", {"schema": "ghc.family.identity-boundary.v4", "owner": OWNER, "phase": PHASE, "pronouns": "they/them", "relational_role": "relational boundary cartographer and evidence steward", "relational_hope": HOPE, "identity_boundary": IDENTITY_BOUNDARY, "corrigibility": "Hamish may rename, pause, redirect, or stop the route."})
    write_json("x1/source-count-overlay.json", {"schema": "ghc.family.source-count-overlay.v5", "repository_sealed": REPOSITORY_SEAL, "live_activation_overlay": ACTIVATION_OVERLAY, "sylven_x1_overlay": x1_overlay})
    write_json("x1/inherited-proposal-revalidation.json", {"schema": "ghc.family.inherited-proposal-revalidation.v6", "owner": OWNER, "phase": PHASE, "selected": 60, "novelty_credit": 0, "completion_credit": 0, "rows": inherited})
    write_json("x1/semantic-neighbor-audit.json", {"schema": "ghc.family.semantic-neighbor-audit.v7", "owner": OWNER, "phase": PHASE, "exact_source_tree_corpus": corpus_summary, "source_elowen_titles_verified": 60, "reachable_unique_titles": len(source_titles), "declared_source_chain": 6970, "new_titles": 60, "max_jaccard": round(max_score, 6), "collision_threshold": 0.72, "collisions": 0, "rows": neighbors, "candidate_practice_exact_hits": {"sailmaking": 0, "sail_making": 0, "sail_loft": 0, "adjacent_rigging": 2}, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True})
    write_json("x1/new-proposal-freeze.json", {"schema": "ghc.family.new-proposal-freeze.v7", "owner": OWNER, "phase": PHASE, "proposal_chain_before": 6970, "proposal_chain_after_if_evidence_frozen": 7030, "outcomes": OUTCOMES, "planned_invalid_mutations_per_proposal": 4, "planned_invalid_mutations": 240, "rows": proposals})
    write_json("x1/portfolio-freeze.json", {"schema": "ghc.family.remastered-portfolio-freeze.v7", "owner": OWNER, "phase": PHASE, "rows": frozen_portfolio, "counts": counts, "bounded_human_practice": "synthetic sailmaking documentation", "bounded_object_lenses": ["loft and pattern identity", "panel seam edge and attachment topology", "provenance correction and handover"], "successor_practice_recommendation": "successor chooses a distinct bounded synthetic practice after its own novelty audit", "successor_practice_recommendation_count": 1, "inherited_portfolio_completion_credit": 0, "successor_recommendation_completion_credit": 0, "filler_prohibited": True})
    write_json("x1/source-ledger.json", {"schema": "ghc.family.public-source-ledger.v7", "owner": OWNER, "phase": PHASE, "retrieved_nz_date": "2026-08-29", "sources": [
        {"title": "Equipment Rules of Sailing 2025-2028", "publisher": "World Sailing", "url": "https://www.sailing.org/inside-world-sailing/rules-regulations/equipment-rules-of-%20sailing", "status": "current_official_page_checked_2026-08-29", "use": "current sail and equipment definitions as vocabulary only with zero equipment or rule-conformance claim"},
        {"title": "SI Units", "publisher": "National Institute of Standards and Technology", "url": "https://www.nist.gov/pml/owm/metric-si/si-units", "status": "current_official_page_checked_2026-08-29", "use": "SI symbol and quantity vocabulary with measurement and conformance abstention"},
        {"title": "PROV-O: The PROV Ontology", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/prov-o/", "status": "stable_primary_recommendation", "use": "entity, activity, derivation, invalidation, and provenance vocabulary only"},
        {"title": "Web Content Accessibility Guidelines 2.2", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/WCAG22/", "status": "current_primary_recommendation_checked_2026-08-29", "use": "structural accessibility vocabulary and manual-evaluation reservation"},
        {"title": "Verifiable Credentials Data Model v2.0", "publisher": "World Wide Web Consortium", "url": "https://www.w3.org/TR/vc-data-model-2.0/", "status": "current_primary_recommendation_checked_2026-08-29", "use": "credential vocabulary for a zero-key nonproduction representation only"},
        {"title": "RFC 8785: JSON Canonicalization Scheme", "publisher": "RFC Editor", "url": "https://www.rfc-editor.org/rfc/rfc8785", "status": "stable_primary_standard_checked_2026-08-29", "use": "canonical JSON ordering and numeric-domain refusal vocabulary only"},
    ], "read_only_source_page_checks": 6, "api_calls": 0, "dataset_or_media_downloads": 0, "real_rows": 0, "external_writes": 0, "boundary": "Sources supply vocabulary and refusal conditions only; they are not observations, measurements, collections conformance, professional advice, safety release, legal interpretation, cultural legitimacy, consent, Māori authority, or Stage 20 evidence."})
    write_json("x1/threat-model.json", {"schema": "ghc.family.threat-model.v6", "owner": OWNER, "phase": PHASE, "assets": ["immutable source lineage", "planning-only x1 separation", "four truth labels", "retained failures", "synthetic-only fixtures", "authority vacancies", "route uniqueness"], "risks": [
        {"risk": "source or manifest drift", "control": "exact commits, normalized Git-blob replay, content-seal replay, and fresh live equality"},
        {"risk": "universal novelty overclaim", "control": "source-tree proposal-title comparison plus explicit unavailable canonical-row mapping gap"},
        {"risk": "registration cue promoted into diagnosis treatment release or safety", "control": "zero-object fixtures, typed vacancies, and professional exact gates"},
        {"risk": "instrument topology or symmetry analogy promoted into material or physical evidence", "control": "surrogate labels, zero measurements, unit vacancies, and GMUT observation firewall"},
        {"risk": "ownership or cultural vocabulary promoted into rights or authority", "control": "legal, affected-party, Māori, and competent-authority exact gates"},
        {"risk": "failure laundering", "control": "append-only Method Flow with paired failed and bounded passing witnesses"},
        {"risk": "private route identifier or precise-location leak", "control": "five-class exact-owner candidate adjudication and location minimization"},
        {"risk": "accessibility overclaim", "control": "structural-only checks with manual, language, assistive-technology, and affected-user evaluation reserved"},
        {"risk": "duplicate successor send", "control": "terminal live authority, exact-title reread, duplicate guard, acknowledgement, and no-resend"},
    ], "not_exhaustive_security": True})
    write_json("x1/method-flow-startup.json", method_flow())
    write_json("x1/workflow-plan.json", {"schema": "ghc.family.workflow-plan.v5", "owner": OWNER, "phase": PHASE, "steps": [{"step": "activation guidance and source verification", "state": "completed_read_only"}, {"step": "planning-only x1 freeze", "state": "in_progress_until_pushed_equal"}, {"step": "bounded x2 execution", "state": "blocked_by_x1_terminal_gate"}, {"step": "combined closeout and seal", "state": "pending"}, {"step": "one owner-scoped canonical aggregate", "state": "pending_not_invoked"}, {"step": "successor route", "state": "unresolved_until_terminal_live_authority"}], "commit_ceiling": 8, "planned_phase_commits": 3, "x1_commit_ceiling": 5, "x2_commit_ceiling": 5, "materialized_file_guard": 2000, "canonical_invocation_budget": 1, "canonical_success_budget": 1, "post_success_replay": False})
    write_json("x1/phase-truth.json", {"schema": "ghc.family.phase-truth.x1.v7", "owner": OWNER, "phase": PHASE, "primary_pillar": "THOS Body", "protected_pillars": ["GMUT Mind", "Freed ID and CBR Heart"], "bounded_human_practice": "synthetic sailmaking documentation", "bounded_object_lens_count": 3, "proposal_rows": {"inherited_zero_credit": 60, "new": 60}, "expected_outcomes": OUTCOMES, "core_truth_labels": CORE_LABELS, "proposal_chain": {"before": 6970, "after_if_frozen": 7030}, "universal_novelty_claim": False, "canonical_row_mapping_open_gap": True, "startup_operational_failures": len(STARTUP_FAILURES), "x1_completion_credit": 0, "x2_execution_started": False, "real_people": 0, "real_objects_or_sites": 0, "real_world_actions": 0, "external_writes": 0, "identity_boundary": IDENTITY_BOUNDARY, "terminal_verdict": "NOT_READY_FOR_STAGE_20"})
    write_json("x1/route-plan.json", {"schema": "ghc.family.route-plan.v5", "owner": OWNER, "phase": PHASE, "prospective_recipient_exact_title": None, "prospective_phase": None, "delivery_state": "UNRESOLVED_UNTIL_TERMINAL_LIVE_REFRESH", "successor_contact_count": 0, "task_creation_count": 0, "substitute_endpoint_count": 0, "standby_contact_count": 0, "required_gate": "clean pushed exact final, attributable terminal validation, newest live authority and roster, unique exact-title reread, duplicate guard, and acknowledged one-send"})
    text = overview(inherited, proposals)
    write_text("x1/integrated-overview.md", text)
    write_json("x1/build-receipt.json", {"schema": "ghc.family.x1-build-receipt.v7", "owner": OWNER, "phase": PHASE, "source_head": head, "branch": branch, "inherited_rows": 60, "new_rows": 60, "portfolio_counts": counts, "overview_words": len(text.split()), "read_only_source_page_checks": 6, "external_writes": 0, "x2_materialized": False})
    print(json.dumps({"owner": OWNER, "phase": PHASE, "new": 60, "outcomes": OUTCOMES, "portfolio": counts, "startup_failures": len(STARTUP_FAILURES), "overview_words": len(text.split()), "corpus": corpus_summary}, sort_keys=True))


def staged_paths() -> list[str]:
    return [line for line in git_text("diff", "--cached", "--name-only", "--diff-filter=ACMR").splitlines() if line]


def staged_review() -> None:
    paths = staged_paths()
    exact = {
        "scripts/build_ghc_family_sylven_arc_v674_v8_x1.py",
        "tests/test_ghc_family_sylven_arc_v674_v8_x1.py",
        "docs/sylven-arc/v674-v8/validation/x1-method-flow-validation.json",
        "docs/sylven-arc/v674-v8/validation/x1-validation-receipt.json",
        "docs/sylven-arc/v674-v8/validation/x1-staged-privacy.json",
        "docs/sylven-arc/v674-v8/validation/x1-staged-review.json",
        "docs/sylven-arc/v674-v8/validation/x1-manifest.json",
    }
    out = [path for path in paths if not (path.startswith("docs/sylven-arc/v674-v8/x1/") or path in exact)]
    mixed = [path for path in paths if any(part in path for part in ("/x2/", "/closeout/", "/final/", "/seal/")) or path.endswith(("_x2.py", "_final.py"))]
    payload = {"schema": "ghc.family.staged-review.v5", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "staged_before_self": paths, "staged_count_before_self": len(paths), "out_of_scope": out, "mixed_lifecycle": mixed, "valid": not out and not mixed}
    write_json("validation/x1-staged-review.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def manifest_from_index() -> None:
    exclusions = ["docs/sylven-arc/v674-v8/validation/x1-manifest.json", "docs/sylven-arc/v674-v8/validation/x1-staged-review.json"]
    entries = []
    for path in staged_paths():
        if path in exclusions:
            continue
        blob = git("show", f":{path}").stdout
        entries.append({"path": path, "bytes": len(blob), "sha256": hashlib.sha256(blob).hexdigest()})
    entries.sort(key=lambda row: row["path"])
    write_json("validation/x1-manifest.json", {"schema": "ghc.family.git-blob-manifest.v5", "domain": "x1 exact staged Git blobs before two declared self files", "hash_domain": "normalized_lf_exact_git_blob", "owner": OWNER, "phase": PHASE, "source_final": SOURCE_FINAL, "entry_count": len(entries), "entries": entries, "self_exclusions": exclusions})


def validation_receipt() -> None:
    json_paths = sorted((OWNER_ROOT / "x1").rglob("*.json"))
    text_paths = sorted(path for path in (OWNER_ROOT / "x1").rglob("*") if path.is_file())
    json_issues = []
    for path in json_paths:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            json_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": type(exc).__name__})
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    for path in text_paths:
        text = path.read_text(encoding="utf-8")
        for label, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path.relative_to(ROOT).as_posix(), "pattern_class": label})
    python_paths = [ROOT / "scripts" / "build_ghc_family_sylven_arc_v674_v8_x1.py", ROOT / "tests" / "test_ghc_family_sylven_arc_v674_v8_x1.py"]
    compile_issues = []
    for path in python_paths:
        try:
            compile(path.read_text(encoding="utf-8"), path.name, "exec")
        except SyntaxError as exc:
            compile_issues.append({"path": path.relative_to(ROOT).as_posix(), "issue": str(exc)})
    diff = git("diff", "--cached", "--check", check=False)
    materialized_files = len([path for path in ROOT.rglob("*") if path.is_file() and ".git" not in path.parts])
    ledger = load_json(OWNER_ROOT / "x1" / "method-flow-startup.json")
    method_issues = []
    if ledger.get("schema") != "ghc.family.method-flow-state.v1":
        method_issues.append("schema")
    if ledger.get("counts", {}).get("methods") != len(STARTUP_FAILURES):
        method_issues.append("method_count")
    if ledger.get("counts", {}).get("witness_results") != {"fail": len(STARTUP_FAILURES), "pass": len(STARTUP_FAILURES)}:
        method_issues.append("witness_result_count")
    write_json("validation/x1-method-flow-validation.json", {"schema": "ghc.family.method-flow-validation.v1", "owner": OWNER, "phase": PHASE, "methods": len(STARTUP_FAILURES), "failed_witnesses": len(STARTUP_FAILURES), "bounded_passing_witnesses": len(STARTUP_FAILURES), "issues": method_issues, "issue_count": len(method_issues), "valid": not method_issues})
    payload = {
        "schema": "ghc.family.x1-validation-receipt.v1", "owner": OWNER, "phase": PHASE,
        "json_documents": len(json_paths), "json_issues": json_issues,
        "text_files": len(text_paths), "privacy_pattern_classes": sorted(patterns),
        "privacy_candidates": candidates, "confirmed_privacy_hits": 0 if not candidates else None,
        "python_compiles": len(python_paths), "python_compile_issues": compile_issues,
        "staged_paths_before_receipt": len(staged_paths()), "diff_hygiene_exit": diff.returncode,
        "diff_hygiene_output": diff.stdout.decode("utf-8", errors="replace"),
        "materialized_files": materialized_files, "file_guard": 2000,
        "x2_absent": not (OWNER_ROOT / "x2").exists(),
        "valid": not json_issues and not candidates and not compile_issues and not method_issues and diff.returncode == 0 and materialized_files < 2000 and not (OWNER_ROOT / "x2").exists(),
        "boundary": BOUNDARY,
    }
    write_json("validation/x1-validation-receipt.json", payload)
    if not payload["valid"]:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def staged_privacy() -> None:
    self_path = "docs/sylven-arc/v674-v8/validation/x1-staged-privacy.json"
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\b", re.I),
        "private_absolute_path": re.compile(r"\b[A-Za-z]:[\\/](?:Users|GHC-Archives|Program Files)\b", re.I),
        "private_route_or_callable": re.compile(r"source_thread_id|<codex_delegation|\b(?:app|plugin)://", re.I),
        "credential_assignment": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token|password|secret)\b\s*[:=]\s*[\"'][^\"']+[\"']"),
        "transcript_or_session_stream": re.compile(r"(?i)\b(?:session_stream|private_transcript|private_conversation_dump)\b"),
    }
    candidates = []
    scanned = 0
    for path in staged_paths():
        if path == self_path or Path(path).suffix.lower() not in {".py", ".json", ".md", ".txt", ".html"}:
            continue
        blob = git("show", f":{path}").stdout
        try:
            text = blob.decode("utf-8")
        except UnicodeDecodeError:
            candidates.append({"path": path, "pattern_class": "non_utf8_text", "disposition": "confirmed_payload_hit"})
            continue
        scanned += 1
        for label, pattern in patterns.items():
            if pattern.search(text):
                scanner_surface = path in {
                    "scripts/build_ghc_family_sylven_arc_v674_v8_x1.py",
                    "tests/test_ghc_family_sylven_arc_v674_v8_x1.py",
                }
                candidates.append({"path": path, "pattern_class": label, "disposition": "scanner_definition_or_unit_test" if scanner_surface else "confirmed_payload_hit"})
    confirmed = [row for row in candidates if row["disposition"] == "confirmed_payload_hit"]
    payload = {"schema": "ghc.family.staged-privacy-scan.v2", "owner": OWNER, "phase": PHASE, "lifecycle": "x1", "hash_domain": "exact_staged_git_blob", "pattern_classes": sorted(patterns), "scanned_text_files": scanned, "candidates": candidates, "confirmed_hits": confirmed, "confirmed_hit_count": len(confirmed), "self_exclusions": [self_path], "valid": not confirmed, "boundary": "Scanner definitions and unit-test strings are candidates, never payload hits; every other match fails closed."}
    write_json("validation/x1-staged-privacy.json", payload)
    if confirmed:
        raise SystemExit(json.dumps(payload, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--staged-review", action="store_true")
    parser.add_argument("--manifest-from-index", action="store_true")
    parser.add_argument("--validation-receipt", action="store_true")
    parser.add_argument("--staged-privacy", action="store_true")
    args = parser.parse_args()
    if args.staged_review:
        staged_review()
    elif args.manifest_from_index:
        manifest_from_index()
    elif args.validation_receipt:
        validation_receipt()
    elif args.staged_privacy:
        staged_privacy()
    else:
        build()


if __name__ == "__main__":
    main()
