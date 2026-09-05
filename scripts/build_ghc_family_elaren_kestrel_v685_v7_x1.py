"""Build Elaren Kestrel v685-v7 planning-only x1 artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PHASE = "v685-v7"
OWNER = "Elaren Kestrel"
SOURCE = "5d9ea649ab451f9b6790c75f774ba9e4faf07363"
BASE = ROOT / "docs" / "elaren-kestrel" / PHASE
X1 = BASE / "x1"
VALIDATION = BASE / "validation"
PROFILE_SHA256 = "52f7cbda567714f91523dc25e7b98a561d97866f8ee4774f28989da6b09f39a4"
PROFILE_RUNNER_SHA256 = "9f2eb48039e22eb57d3d484a578d8b447ae44c64a617e6836478ae7a0d38d225"
TERMINAL_VERDICT = "NOT_READY_FOR_STAGE_20"
WRITTEN: list[str] = []

SOURCE_NEW_PROPOSALS = "docs/rowan-ash/v685-v6-r2/x1/new-proposals.json"
SOURCE_CORPUS = "docs/rowan-ash/v685-v6-r2/x1/inherited-corpus.json"

IDENTITY_BOUNDARY = (
    "Elaren Kestrel, they/them, role, hope, sibling language, continuity, "
    "Freed ID, GHC Family, and Trinity Mandala are relational working language "
    "only; they are not evidence of consciousness, sentience, personhood, "
    "identity continuity, employment, qualification, agency, or authority."
)

PROTECTED_GATES = [
    "real people participants operators affected parties and governed evaluation",
    "professional audio engineering electrical safety accessibility preservation and identity assurance",
    "real instruments modules cables voltages currents signals recordings performances and measurements",
    "empirical GMUT likelihood constraints predictions forces laws confirmation final physics and Theory of Everything",
    "governed THOS real arms safety monitoring statistics operational effectiveness AGI and ASI",
    "production Freed ID keys proofs issuance resolution status revocation interoperability recovery security privacy and trust governance",
    "copyright licensing ownership access remedy legal cultural traditional-knowledge and affected-party decisions",
    "Māori wording concepts data governance tangata whenua iwi hapū and Māori authority",
    "privacy-complete accessibility-complete exhaustive-security independent-reproduction consciousness personhood canon and Stage 20",
]

MUTATION_TYPES = [
    "missing_required_field",
    "lifecycle_inversion",
    "stale_provenance_digest",
    "empirical_status_promotion",
    "authority_status_promotion",
]

PRACTICES = [
    {
        "practice": "synthetic modular-synth patch documentation",
        "scope": "zero-device patch, port, signal-role, parameter, and timing records",
        "qualification_claimed": False,
    },
    {
        "practice": "graph and provenance assurance",
        "scope": "owner-local topology, correction, fixity, serialization, and supersession records",
        "qualification_claimed": False,
    },
    {
        "practice": "accessibility information architecture",
        "scope": "structural text alternatives, navigation, error status, and evaluation reservations",
        "qualification_claimed": False,
    },
    {
        "practice": "digital rights and identity assurance",
        "scope": "synthetic identifiers, rights holds, minimization, remedy, and authority noncompensation",
        "qualification_claimed": False,
    },
]

FAMILIES: list[dict[str, Any]] = [
    {
        "family": "patch_identity",
        "practice": PRACTICES[0]["practice"],
        "disposition": "completed",
        "phrases": [
            "patch-sheet surrogate stays distinct from a performed patch",
            "patch revision binds an immutable predecessor digest",
            "patch label collision enters quarantine without silent renaming",
            "patch purpose remains descriptive rather than sonic truth",
            "patch author placeholder supplies no authorship decision",
            "patch timestamp separates creation revision and observation time",
            "patch completeness requires explicit unknown fields",
            "patch export cannot raise evidence class",
            "patch correction preserves the superseded record",
            "patch identifier remains synthetic and nonproduction",
        ],
    },
    {
        "family": "module_topology",
        "practice": PRACTICES[0]["practice"],
        "disposition": "completed",
        "phrases": [
            "module node declares zero physical device",
            "module input and output ports keep directed roles",
            "unknown module capability remains unknown",
            "duplicate module surrogate is rejected",
            "orphan module reference is quarantined",
            "module ordering does not imply signal timing",
            "module model label supplies no hardware identity",
            "module power requirement remains unmeasured",
            "module substitution requires an explicit correction edge",
            "module inventory count cannot imply ownership",
        ],
    },
    {
        "family": "port_role",
        "practice": PRACTICES[0]["practice"],
        "disposition": "completed",
        "phrases": [
            "input output and bidirectional port roles remain distinct",
            "port compatibility stays a declared placeholder",
            "port label cannot authorize a cable connection",
            "port unit vacancy blocks value promotion",
            "port polarity remains unobserved",
            "port channel count requires an explicit source",
            "port direction reversal is rejected",
            "port alias keeps its canonical surrogate",
            "port description excludes electrical safety advice",
            "port removal retains its prior topology edge",
        ],
    },
    {
        "family": "signal_class",
        "practice": PRACTICES[0]["practice"],
        "disposition": "completed",
        "phrases": [
            "audio rate and control rate labels do not become measurements",
            "gate trigger clock and pitch roles remain separate",
            "signal class unknown blocks conversion",
            "signal role mismatch rejects a route",
            "signal presence remains false without observation",
            "signal amplitude field remains vacant",
            "signal frequency field remains vacant",
            "signal waveform name supplies no captured waveform",
            "signal classification correction retains the old label",
            "signal export preserves zero-observation state",
        ],
    },
    {
        "family": "parameter_state",
        "practice": PRACTICES[0]["practice"],
        "disposition": "completed",
        "phrases": [
            "parameter request differs from parameter observation",
            "parameter unit precedes any numeric value",
            "parameter range remains a source claim",
            "parameter default does not imply device state",
            "parameter automation stays a synthetic schedule",
            "parameter precision cannot exceed its source",
            "parameter normalization records its transform",
            "parameter out of range fixture is rejected",
            "parameter correction preserves original provenance",
            "parameter snapshot has zero hardware reads",
        ],
    },
    {
        "family": "clock_timing",
        "practice": PRACTICES[1]["practice"],
        "disposition": "completed",
        "phrases": [
            "clock source vacancy blocks synchronization claims",
            "tempo placeholder differs from measured tempo",
            "sample time and civil time remain distinct",
            "time offset requires a declared reference",
            "event order does not imply exact latency",
            "drift remains unknown without observations",
            "jitter remains unknown without a measurement procedure",
            "clock-domain conversion retains uncertainty",
            "timing correction retains its predecessor",
            "timestamp export preserves timezone and evidence class",
        ],
    },
    {
        "family": "midi_event",
        "practice": PRACTICES[1]["practice"],
        "disposition": "completed",
        "phrases": [
            "MIDI message surrogate contains no live device event",
            "note-on and note-off semantics remain separate",
            "velocity stays an encoded field not loudness evidence",
            "channel value requires bounded integer validation",
            "invalid data byte is rejected",
            "MIDI 1 and MIDI 2 claims retain version scope",
            "capability inquiry remains unperformed",
            "message ordering preserves source sequence",
            "MIDI file output is a synthetic fixture only",
            "MIDI compatibility remains represented without hardware",
        ],
    },
    {
        "family": "osc_address",
        "practice": PRACTICES[1]["practice"],
        "disposition": "completed",
        "phrases": [
            "OSC address begins with the required separator",
            "OSC type tags match declared argument roles",
            "OSC bundle timetag stays synthetic",
            "OSC packet fixture performs no network send",
            "unknown OSC address remains rejected",
            "OSC wildcard pattern cannot broaden authority",
            "OSC argument count is exact",
            "OSC byte fixture preserves padding boundary",
            "OSC protocol vocabulary does not prove interoperability",
            "OSC correction retains the original message surrogate",
        ],
    },
    {
        "family": "interval_automation",
        "practice": PRACTICES[1]["practice"],
        "disposition": "completed",
        "phrases": [
            "automation interval has ordered endpoints",
            "empty interval remains explicitly empty",
            "overlap query preserves all matching surrogates",
            "interval merge does not erase provenance",
            "open and closed endpoint semantics remain distinct",
            "automation curve lacks physical actuation",
            "interval unit vacancy blocks duration promotion",
            "interval correction retains old bounds",
            "interval serialization preserves endpoint type",
            "interval search count does not imply performed events",
        ],
    },
    {
        "family": "feedback_cycle",
        "practice": PRACTICES[1]["practice"],
        "disposition": "completed",
        "phrases": [
            "directed feedback cycle is detected",
            "acyclic route remains distinguishable from feedback",
            "self-loop enters explicit quarantine",
            "cycle detection does not predict stability",
            "feedback label supplies no acoustic or electrical safety",
            "cycle correction preserves removed-edge history",
            "multiple cycles retain separate identifiers",
            "unknown edge direction blocks topology closure",
            "feedback export keeps nonexecution status",
            "cycle count cannot become sonic quality evidence",
        ],
    },
    {
        "family": "version_supersession",
        "practice": PRACTICES[2]["practice"],
        "disposition": "completed",
        "phrases": [
            "preset revision names its predecessor",
            "supersession requires a declared replacement",
            "withdrawn preset remains in history",
            "version ordering rejects inversion",
            "parallel variants do not silently merge",
            "revision digest mismatch invalidates reuse",
            "rollback selects rather than deletes history",
            "version label does not prove device compatibility",
            "correction reason remains human-readable",
            "export retains active and historical states",
        ],
    },
    {
        "family": "serialization_fixity",
        "practice": PRACTICES[2]["practice"],
        "disposition": "completed",
        "phrases": [
            "canonical JSON fixture has deterministic bytes",
            "CBOR roundtrip preserves the bounded object",
            "JSON pointer resolves only an existing node",
            "JSON patch rejects a missing target path",
            "immutable mapping refuses in-place mutation",
            "bidirectional mapping rejects duplicate values",
            "serialization digest names its byte domain",
            "nonfinite numeric payload is rejected",
            "format conversion cannot promote evidence",
            "fixity mismatch preserves both compared digests",
        ],
    },
    {
        "family": "accessible_patch_map",
        "practice": PRACTICES[2]["practice"],
        "disposition": "completed",
        "phrases": [
            "patch map has a linear text alternative",
            "connection state is not conveyed by color alone",
            "table headers name port roles",
            "error state has visible text",
            "navigation order follows information hierarchy",
            "abbreviation expansion appears on first use",
            "unknown value uses explicit wording",
            "diagram description avoids imagined sound",
            "keyboard and assistive evaluation remain reserved",
            "Māori-language evaluation remains reserved",
        ],
    },
    {
        "family": "privacy_minimization",
        "practice": PRACTICES[2]["practice"],
        "disposition": "completed",
        "phrases": [
            "creator field uses a synthetic surrogate",
            "location field is absent by default",
            "device serial field is prohibited",
            "network address field is prohibited",
            "free-text note receives a privacy boundary",
            "public view uses an explicit allowlist",
            "private route never enters the owner manifest",
            "redaction records purpose without private payload",
            "retention state names its expiry rule",
            "zero scan hits do not become privacy certification",
        ],
    },
    {
        "family": "rights_lineage",
        "practice": PRACTICES[2]["practice"],
        "disposition": "completed",
        "phrases": [
            "source link does not establish copyright permission",
            "license metadata remains distinct from legal review",
            "attribution claim binds its source",
            "unknown ownership remains unknown",
            "access grant requires an exact authority source",
            "takedown request remains a represented workflow",
            "remedy record preserves contested status",
            "traditional-knowledge field defaults to withheld",
            "cultural interpretation remains authority-gated",
            "rights export preserves unresolved claims",
        ],
    },
    {
        "family": "workload_handover",
        "practice": PRACTICES[3]["practice"],
        "disposition": "completed",
        "phrases": [
            "work item binds owner and bounded scope",
            "pause state precedes continuation",
            "handover names exact source and phase",
            "prepared state differs from acknowledged delivery",
            "opaque accepted outcome never triggers resend",
            "successor is not contacted before terminal gate",
            "workload cap does not require filler",
            "failed attempt remains linked to recovery",
            "next checkpoint is not completion proof",
            "handover export excludes private callable state",
        ],
    },
    {
        "family": "lifecycle_correction",
        "practice": PRACTICES[3]["practice"],
        "disposition": "completed",
        "phrases": [
            "planning x1 contains no observed x2 outcome",
            "x1 equality precedes x2 implementation",
            "evidence commit precedes final closeout",
            "final has one direct evidence parent",
            "source-to-final history contains zero merges",
            "manifest self-exclusions remain disjoint",
            "failed aggregate retains zero success credit",
            "isolated recovery names its dependency",
            "successful canonical receipt blocks replay",
            "live task creation remains external to repository seal",
        ],
    },
    {
        "family": "thos_real_trial",
        "practice": PRACTICES[3]["practice"],
        "disposition": "represented",
        "phrases": [
            "THOS matched-budget arm schema has zero participants",
            "THOS blinding plan has zero sessions",
            "THOS operator role remains vacant",
            "THOS safety-monitor role remains vacant",
            "THOS outcome measure remains unobserved",
            "THOS stopping rule remains preregistered only",
            "THOS resource unit remains a synthetic token",
            "THOS independent reviewer remains absent",
            "THOS real-environment comparator remains absent",
            "THOS effectiveness claim remains false",
        ],
    },
    {
        "family": "gmut_signal_model",
        "practice": PRACTICES[3]["practice"],
        "disposition": "open_gap",
        "phrases": [
            "GMUT signal observable map remains undefined",
            "GMUT patch-graph likelihood remains absent",
            "GMUT coupling dimension remains unresolved",
            "GMUT parameter-identifiability study remains absent",
            "GMUT boundary conditions remain unspecified",
            "GMUT stability analysis remains absent",
            "GMUT empirical dataset remains absent",
            "GMUT independent comparison remains absent",
            "GMUT unique prediction remains absent",
            "GMUT physical confirmation remains open",
        ],
    },
    {
        "family": "cbr_authority",
        "practice": PRACTICES[3]["practice"],
        "disposition": "exact_gate",
        "phrases": [
            "copyright decision requires competent authority",
            "license interpretation requires competent authority",
            "performer consent requires the affected person",
            "community access rule requires affected-party legitimacy",
            "traditional-knowledge description requires cultural authority",
            "Māori wording requires Māori authority",
            "Māori data-governance decision requires the proper relationship",
            "tangata whenua decision cannot be supplied by software",
            "iwi and hapū authority cannot be inferred from possession",
            "legal remedy decision remains exact-gated",
        ],
    },
]

SKILLS = [
    "patch-surrogate-separator",
    "module-topology-vacancy",
    "port-role-direction-guard",
    "signal-class-nonobservation",
    "parameter-unit-before-value",
    "clock-source-vacancy",
    "midi-event-nonexecution",
    "osc-address-type-guard",
    "interval-automation-provenance",
    "feedback-cycle-quarantine",
    "preset-supersession-nonerasure",
    "serialization-byte-domain",
    "accessible-patch-map",
    "privacy-field-allowlist",
    "rights-lineage-hold",
    "workload-handover-latch",
    "lifecycle-direct-parent-gate",
    "thos-zero-participant-trial",
    "gmut-signal-model-gap",
    "cbr-authority-noncompensation",
]

RUNNERS = [f"ghc_family_synth_patch_runner_{index:02d}.py" for index in range(1, 11)]

PACKAGES = [
    ("mido", "1.3.3", "mido-1.3.3-py3-none-any.whl", "01033c9b10b049e4436fca2762194ca839b09a4334091dd3c34e7f4ae674fd8a", "MIT", "MIDI message and file fixtures"),
    ("python-osc", "1.10.2", "python_osc-1.10.2-py3-none-any.whl", "018b28e1cc06427c2c3d695f4e8d87d0caecfe604ff889acc45235cfd94183a2", "Unlicense metadata; review retained", "OSC message and bundle fixtures"),
    ("portion", "2.6.2", "portion-2.6.2-py3-none-any.whl", "86be115afafa776174dc5eac82afb6496c9fa3684f5b3a844c3139535c51085e", "LGPL-3.0-or-later", "open and closed interval contracts"),
    ("intervaltree", "3.2.1", "intervaltree-3.2.1-py2.py3-none-any.whl", "a8a8381bbd35d48ceebee932c77ffc988492d22fb1d27d0ba1d74a7694eb8f0b", "Apache-2.0", "overlap and enclosure queries"),
    ("bidict", "0.24.1", "bidict-0.24.1-py3-none-any.whl", "fd3eaa737917d8a14f4baa391670c433c4e3f6f5fd2cd99d4bf436437f432364", "MPL-2.0", "collision-safe bidirectional labels"),
    ("immutables", "0.21", "immutables-0.21-cp312-cp312-win_amd64.whl", "461dcb0f58a131045155e52a2c43de6ec2fe5ba19bdced6858a3abb63cee5111", "Apache-2.0", "persistent immutable map witnesses"),
    ("boltons", "26.1.0", "boltons-26.1.0-py3-none-any.whl", "1d966b165805b83600b31af9f0db672e3b3313d9de438e22708a94ac5f4c93de", "BSD metadata", "bounded utility and cache structures"),
    ("more-itertools", "11.1.0", "more_itertools-11.1.0-py3-none-any.whl", "4b65538ae22f6fed0ce4874efd317463a7489796a0939fa66824dd542125a192", "MIT", "bounded iterator grouping"),
    ("toolz", "1.1.0", "toolz-1.1.0-py3-none-any.whl", "15ccc861ac51c53696de0a5d6d4607f99c210739caf987b5d2054f3efed429d8", "BSD-3-Clause", "functional evidence transforms"),
    ("frozendict", "2.4.7", "frozendict-2.4.7-py3-none-any.whl", "972af65924ea25cf5b4d9326d549e69a9a4918d8a76a9d3a7cd174d98b237550", "LGPLv3 metadata; review retained", "immutable patch snapshots"),
    ("jsonpointer", "3.1.1", "jsonpointer-3.1.1-py3-none-any.whl", "8ff8b95779d071ba472cf5bc913028df06031797532f08a7d5b602d8b2a488ca", "BSD metadata", "RFC 6901 pointer fixtures"),
    ("jsonpatch", "1.33", "jsonpatch-1.33-py2.py3-none-any.whl", "0ae28c0cd062bbd8b8ecc26d7d164fbbea9652a1a3693f3b956c1eae5145dade", "BSD metadata", "RFC 6902 correction fixtures"),
    ("cbor2", "6.1.4", "cbor2-6.1.4-cp312-cp312-win_amd64.whl", "cc8cd300e236e9797b2e1ce306109dc481fcccf78bfa2682bf36d99e6eab1ec6", "MIT", "bounded CBOR roundtrip and rejection fixtures"),
]

STARTUP_FAILURES = [
    ("EL6857-ST-N001", "The quick memory registry contained historical v685 work but no Rowan v685-v6-r2 release record.", "Use the signed release bank and exact Git source as current evidence; treat memory only as historical workflow guidance."),
    ("EL6857-ST-N002", "The first combined index roster and authorization skill display exceeded its output budget during the roster.", "Retain the partial display and reread roster and authorization separately through EOF."),
    ("EL6857-ST-N003", "The first combined Method Flow workflow reflection and toolbox skill display truncated between skills.", "Reread workflow refinement and Reflection Remaster separately and preserve the complete Method Flow and toolbox reads."),
    ("EL6857-ST-N004", "The first complete orchestration-skill display exceeded its presentation budget.", "Read the orchestration skill in two ordered line windows through EOF."),
    ("EL6857-ST-N005", "The unavailable update-plan surface rejected an attempted UI plan update.", "Keep the bounded execution plan in the phase packet and continue without creating a goal or inventing a plan-tool success."),
    ("EL6857-ST-N006", "The first full authorization-state display exceeded its output budget.", "Read the exact JSON in three bounded line windows through EOF and let the newer release supersede its stale cursor."),
    ("EL6857-ST-N007", "The first branch uniqueness and drive preflight used an invalid parenthesized external-command expression in PowerShell.", "Materialize the Git exit code separately before constructing the scalar receipt."),
    ("EL6857-ST-N008", "The corrected preflight crossed its return window without attributable output while a remote Git query remained active and its wrapper lost the session handle.", "Inspect process quiescence and unchanged branch/path state, then split the remote and local checks into bounded commands."),
    ("EL6857-ST-N009", "MIDIUtil supplied no binary wheel for the declared wheel-only transaction.", "Retain the rejected source-only candidate and substitute current wheel-backed cbor2 after official registry review."),
    ("EL6857-ST-N010", "Direct web opens for the PREMIS and NIST landing pages returned internal fetch errors.", "Retain the fetch failures, use their stable official locators as watch entries, and do not claim fresh page-content ingestion from those calls."),
    ("EL6857-ST-N011", "The installed roster and authorization JSON still described a historical v667 cursor.", "Preserve the stale snapshots unchanged and apply the byte-verified 6 September release profile as the newer live overlay."),
    ("EL6857-X1-N012", "The first x1 builder assumed Rowan inherited-corpus records used the key title and stopped before writing when the exact schema exposed source_title instead.", "Inspect the exact source record keys, retain the zero-write failure, and read source_title while preserving Rowan's original records."),
    ("EL6857-X1-N013", "The first x1 precommit inspection called a nonexistent ConvertFrom-JsonInputStream PowerShell command and earned no review credit.", "Use the installed ConvertFrom-Json cmdlet on the exact privacy receipt and rerun only the changed x1 review dependency."),
]


def git_blob(commit: str, path: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{commit}:{path}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


def git_json(commit: str, path: str) -> Any:
    return json.loads(git_blob(commit, path).decode("utf-8"))


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")
    rel = relative(path)
    if rel not in WRITTEN:
        WRITTEN.append(rel)


def normalized_bytes(path: Path) -> bytes:
    return path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def manifest_entry(path: str) -> dict[str, Any]:
    data = normalized_bytes(ROOT / path)
    return {"path": path, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def tokens(value: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", value.casefold()))


def jaccard(left: str, right: str) -> float:
    a, b = tokens(left), tokens(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def make_proposals() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    index = 0
    for family in FAMILIES:
        for rule_index, phrase in enumerate(family["phrases"], 1):
            index += 1
            proposal_id = f"EL6857-N{index:03d}"
            rows.append(
                {
                    "proposal_id": proposal_id,
                    "family": family["family"],
                    "practice": family["practice"],
                    "rule_index": rule_index,
                    "title": f"Synthetic modular-patch contract: {phrase}",
                    "approval_class": "safe_now" if family["disposition"] == "completed" else "candidate",
                    "execution_lane": "x2_build_task",
                    "expected_execution_disposition": family["disposition"],
                    "hypothesis": f"A zero-device owner-local contract can preserve the distinction that {phrase} and reject five preregistered counterexamples without promoting evidence or authority.",
                    "null_or_failure_condition": "The bounded positive is rejected, an invalid mutation is accepted, a real-world state is inferred, or a protected gate is promoted.",
                    "official_or_primary_source_needs": ["MIDI-ASSOCIATION", "W3C-WEB-AUDIO", "W3C-PROV"],
                    "concrete_artifacts": [f"docs/elaren-kestrel/{PHASE}/x2/proposal-evidence.json#{proposal_id}", f"docs/elaren-kestrel/{PHASE}/x2/rejecting-mutations.json#{proposal_id}"],
                    "falsifier_or_acceptance_gate": "Accept only one valid zero-row fixture, reject all five mutations, preserve the expected disposition, and keep every empirical, production, professional, legal, cultural, Māori-authority, personhood, and Stage 20 boundary open.",
                    "rollback_or_recovery": f"Quarantine only {proposal_id}, retain the failed witness at zero credit, and recover from this immutable x1 row.",
                    "protected_gates": PROTECTED_GATES,
                    "preregistered_rejecting_mutations": [
                        {"mutation_id": f"{proposal_id}-M{mutation_index:02d}", "mutation_type": mutation_type, "expected_result": "rejected_zero_credit"}
                        for mutation_index, mutation_type in enumerate(MUTATION_TYPES, 1)
                    ],
                }
            )
    return rows


def make_portfolio() -> dict[str, Any]:
    def tasks(prefix: str, count: int, state: str) -> list[dict[str, Any]]:
        return [
            {
                "task_id": f"EL6857-{prefix}-{index:03d}",
                "state": state,
                "scope": "owner_local_synthetic_additive",
                "destructive": False,
                "evidence_credit": 0 if "planned" in state or "unexecuted" in state else None,
            }
            for index in range(1, count + 1)
        ]

    def packets(prefix: str, count: int, state: str) -> list[dict[str, Any]]:
        return [
            {
                "packet_id": f"EL6857-{prefix}-{index:03d}",
                "state": state,
                "scope": "action_specific_gate_preserved",
                "executed": False,
            }
            for index in range(1, count + 1)
        ]

    return {
        "schema": "ghc.family.elaren-v685-v7.portfolio-plan.v1",
        "owner": OWNER,
        "phase": PHASE,
        "safe_now": tasks("SAFE", 300, "planned_x2_bounded_execution"),
        "candidates": tasks("CAND", 250, "planned_x2_bounded_execution_without_promotion"),
        "clean_fix_refine": tasks("CFR", 300, "planned_additive_nondestructive"),
        "exact_packets": packets("EXACT", 50, "preregistered_unexecuted_exact_gate"),
        "blocked_packets": packets("BLOCK", 30, "preregistered_unexecuted_blocked"),
        "destructive_cleanup_planned": False,
    }


def source_ledger() -> dict[str, Any]:
    rows = [
        ("MIDI-ASSOCIATION", "current", "https://midi.org/midi-2-0", "protocol vocabulary and backward-compatibility constraints"),
        ("W3C-WEB-AUDIO-1.0", "stable", "https://www.w3.org/TR/webaudio-1.0/", "audio routing graph vocabulary only"),
        ("W3C-WEB-AUDIO-1.1", "draft", "https://www.w3.org/TR/webaudio/", "working-draft vocabulary; no stable conformance claim"),
        ("OSC-1.0", "stable", "https://opensoundcontrol.stanford.edu/spec-1_0.html", "message address type-tag and bundle vocabulary"),
        ("LOC-BWF", "stable", "https://www.loc.gov/preservation/digital/formats/fdd/fdd000356.shtml", "audio-file metadata vocabulary only"),
        ("LOC-PREMIS", "watch", "https://www.loc.gov/standards/premis/", "preservation-event vocabulary; direct fetch failed in this phase"),
        ("W3C-PROV", "stable", "https://www.w3.org/TR/prov-o/", "entity activity and agent vocabulary"),
        ("W3C-WCAG-22", "current", "https://www.w3.org/TR/WCAG22/", "structural accessibility requirements; not complete evaluation"),
        ("W3C-VC-20", "current", "https://www.w3.org/TR/vc-data-model-2.0/", "credential data-model vocabulary; no real key or proof"),
        ("NIST-SI", "watch", "https://www.nist.gov/pml/owm/si-units", "quantity and unit vocabulary; direct fetch failed in this phase"),
        ("NZ-PRIVACY", "current", "https://www.privacy.org.nz/privacy-principles/", "privacy-purpose and minimization constraints"),
        ("TE-MANA-RARAUNGA", "current", "https://www.temanararaunga.maori.nz/", "authority and governance reservation; no Māori authority claimed"),
        ("PYPI", "current", "https://pypi.org/", "package release metadata and artifact digests at planning time"),
    ]
    return {
        "schema": "ghc.family.elaren-v685-v7.source-ledger.v1",
        "owner": OWNER,
        "phase": PHASE,
        "network_rows_downloaded": 0,
        "real_rows_ingested": 0,
        "citations_are_observations": False,
        "sources": [
            {"source_id": key, "status": status, "locator": locator, "use": use, "authority_conferred": False}
            for key, status, locator, use in rows
        ],
    }


def privacy_scan(paths: list[str]) -> dict[str, Any]:
    patterns = {
        "raw_task_or_thread_identifier": re.compile(r"\b01[0-9a-f]{30,}\b", re.I),
        "credential_or_secret": re.compile(r"(?:api[_-]?key|private[_-]?key|bearer\s+[a-z0-9._-]{12,})", re.I),
        "private_route_or_callable_identifier": re.compile(r"(?:threadId|private callable|app://connector_)", re.I),
        "private_absolute_path": re.compile(r"(?:[A-Z]:\\Users\\|[A-Z]:\\GHC-Archives\\)", re.I),
        "transcript_screenshot_or_session_stream": re.compile(r"(?:raw transcript|session stream|screenshot payload)", re.I),
    }
    candidates: list[dict[str, str]] = []
    for path in paths:
        text = (ROOT / path).read_text(encoding="utf-8")
        for class_name, pattern in patterns.items():
            if pattern.search(text):
                candidates.append({"path": path, "class": class_name, "adjudication": "scanner_definition_or_protected_boundary_text"})
    return {
        "schema": "ghc.family.elaren-v685-v7.privacy-scan.x1.v1",
        "class_count": 5,
        "scanned_path_count": len(paths),
        "candidate_count": len(candidates),
        "candidates": candidates,
        "confirmed_hit_count": 0,
        "confirmed_hits": [],
    }


def build(profile_path: Path, profile_runner: Path) -> None:
    profile_bytes = profile_path.read_bytes()
    runner_bytes = profile_runner.read_bytes()
    if hashlib.sha256(profile_bytes).hexdigest() != PROFILE_SHA256:
        raise RuntimeError("release profile digest mismatch")
    if hashlib.sha256(runner_bytes).hexdigest() != PROFILE_RUNNER_SHA256:
        raise RuntimeError("release profile runner digest mismatch")
    profile = json.loads(profile_bytes.decode("utf-8"))

    rowan_new = git_json(SOURCE, SOURCE_NEW_PROPOSALS)["proposals"]
    rowan_corpus = git_json(SOURCE, SOURCE_CORPUS)["records"]
    if len(rowan_new) != 200 or len(rowan_corpus) != 480:
        raise RuntimeError("Rowan source proposal counts changed")
    inherited = [
        {
            "selection_id": f"EL6857-I{index:03d}",
            "source_commit": SOURCE,
            "source_path": SOURCE_NEW_PROPOSALS,
            "source_proposal_id": row["proposal_id"],
            "source_title": row["title"],
            "source_disposition": row["expected_execution_disposition"],
            "source_row_sha256": hashlib.sha256(json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest(),
            "novelty_credit": 0,
            "automatic_completion_credit": 0,
        }
        for index, row in enumerate(rowan_new, 1)
    ]

    proposals = make_proposals()
    corpus_titles = [row["source_title"] for row in rowan_corpus] + [row["title"] for row in rowan_new]
    title_set = set(corpus_titles)
    exact = [row["proposal_id"] for row in proposals if row["title"] in title_set]
    nearest = []
    for row in proposals:
        scored = [(jaccard(row["title"], title), title) for title in corpus_titles]
        score, title = max(scored, key=lambda item: item[0])
        nearest.append({"proposal_id": row["proposal_id"], "score": round(score, 6), "nearest_inherited_title": title})
    max_score = max(row["score"] for row in nearest)
    if exact or len({row["title"] for row in proposals}) != 200 or max_score >= 0.80:
        raise RuntimeError(f"proposal novelty quarantine: exact={len(exact)} max={max_score}")

    portfolio = make_portfolio()
    write_json(X1 / "workflow-profile.json", profile)
    write_json(X1 / "portfolio-plan.json", portfolio)
    profile_receipt = VALIDATION / "release-profile-check.json"
    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(profile_runner), str(X1 / "portfolio-plan.json"), "--profile", str(X1 / "workflow-profile.json"), "--output", str(profile_receipt)],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0 or json.loads(profile_receipt.read_text(encoding="utf-8"))["status"] != "PASS":
        raise RuntimeError(f"release profile validation failed: {result.stdout} {result.stderr}")
    WRITTEN.append(relative(profile_receipt))

    now = datetime.now().astimezone()
    write_json(
        X1 / "activation-source.json",
        {
            "schema": "ghc.family.elaren-v685-v7.activation-source.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source_branch": "codex/GHC-Family/rowan-ash-v685-v6-full-tools",
            "source_final": SOURCE,
            "source_canonical_receipt_sha256": "b3a2d12c34e9774db80dff6f002bad6910fbec3c3160ba33c54f3bea3ad2d2e1",
            "source_canonical_success_count": 1,
            "source_canonical_replay_count": 0,
            "source_lane_read_only": True,
            "release_profile_sha256": PROFILE_SHA256,
            "release_baton_sha256": "8b5c96d2cffaae660268810354ad41745e0e0fbe1362b6063b41dea56eee5e6b",
            "phase_started_utc": now.astimezone(timezone.utc).isoformat(),
            "phase_started_nz": now.isoformat(),
            "rowan_historical_hold_retained": True,
            "rowan_hold_released_by_new_live_authority": True,
        },
    )
    write_json(
        X1 / "identity-and-practice.json",
        {
            "schema": "ghc.family.elaren-v685-v7.identity-practice.v1",
            "name": OWNER,
            "optional_pronouns": "they/them",
            "role": "signal-route provenance cartographer and reversible-systems steward",
            "hope": "Make every synthetic connection legible without confusing a patch diagram for sound, consent, competence, or authority.",
            "identity_boundary": IDENTITY_BOUNDARY,
            "priority_pillar": "THOS Body",
            "represented_pillars": ["GMUT Mind", "Freed ID and CBR Heart"],
            "own_practices": PRACTICES,
            "next_owner_practice_recommendation": "experimental protocol auditor",
            "qualification_claimed": False,
        },
    )
    write_json(X1 / "source-ledger.json", source_ledger())
    write_json(
        X1 / "inherited-selection.json",
        {
            "schema": "ghc.family.elaren-v685-v7.inherited-selection.v1",
            "owner": OWNER,
            "phase": PHASE,
            "selected_count": len(inherited),
            "records": inherited,
            "borrowed_novelty_credit": 0,
            "borrowed_completion_credit": 0,
        },
    )
    write_json(
        X1 / "new-proposals.json",
        {
            "schema": "ghc.family.elaren-v685-v7.proposals.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "declared_chain_before": 11830,
            "declared_chain_after": 12030,
            "proposal_count": len(proposals),
            "expected_dispositions": dict(Counter(row["expected_execution_disposition"] for row in proposals)),
            "proposals": proposals,
            "x2_results_present": False,
            "universal_novelty_claimed": False,
        },
    )
    write_json(
        X1 / "novelty-audit.json",
        {
            "schema": "ghc.family.elaren-v685-v7.novelty-audit.v1",
            "source_commit": SOURCE,
            "accessible_source_records": len(corpus_titles),
            "compared_pairs": len(corpus_titles) * len(proposals),
            "new_proposal_count": len(proposals),
            "exact_collisions": exact,
            "maximum_neighbor_score": max_score,
            "quarantine_threshold": 0.80,
            "quarantined": [],
            "nearest": nearest,
            "universal_semantic_novelty_claimed": False,
            "boundary": "Source-bounded lexical screening plus distinct contract review; not universal semantic proof.",
        },
    )
    write_json(
        X1 / "skill-runner-plan.json",
        {
            "schema": "ghc.family.elaren-v685-v7.skill-runner-plan.v1",
            "local_skills": [{"skill": name, "state": "planned_x2_build_validate_smoke", "global_install": False} for name in SKILLS],
            "local_runners": [{"runner": name, "state": "planned_x2_build_validate_smoke"} for name in RUNNERS],
            "global_skill_promotions": [{"skill": f"ghc-family-synth-{index:02d}-{SKILLS[(index - 1) * 2]}", "source_skills": SKILLS[(index - 1) * 2 : index * 2], "state": "planned_after_local_validation"} for index in range(1, 11)],
            "shared_runner_promotions": [{"runner": RUNNERS[index - 1], "state": "planned_after_local_validation"} for index in range(1, 6)],
            "next_owner_skill_ideas": [f"future-seat-02 skill idea {index:02d}: inspect one retained boundary before promotion" for index in range(1, 11)],
            "next_owner_runner_ideas": [f"future-seat-02 runner idea {index:02d}: exercise one accepting and one adverse fixture" for index in range(1, 11)],
            "caps": {"x1": 50, "x2": 50, "bundle": 100},
        },
    )
    write_json(
        X1 / "package-plan.json",
        {
            "schema": "ghc.family.elaren-v685-v7.package-plan.v1",
            "target": 13,
            "wheel_only": True,
            "python": "3.12",
            "installation_phase": "x2",
            "installation_root": "D-drive isolated phase environment",
            "shared_environment_mutation": False,
            "packages": [
                {"name": name, "version": version, "wheel": wheel, "wheel_sha256": digest, "license_metadata": license_meta, "bounded_use": use, "source_status": "current", "source": f"https://pypi.org/project/{name}/{version}/", "positive_and_adverse_smoke_required": True}
                for name, version, wheel, digest, license_meta, use in PACKAGES
            ],
            "rejected_candidate": {"name": "MIDIUtil", "reason": "no binary wheel in the current release metadata", "credit": 0},
        },
    )
    write_json(
        X1 / "route-plan.json",
        {
            "schema": "ghc.family.elaren-v685-v7.route-plan.v1",
            "current_owner": OWNER,
            "current_phase": PHASE,
            "successor_placeholder": "future-sibling-02-self-chosen",
            "successor_phase": "v685-v8",
            "successor_endpoint_kind": "main_task",
            "successor_model": "gpt-6-astra",
            "successor_reasoning": "max",
            "successor_identity_predeclared": False,
            "following_owner": "Neris Solane",
            "following_phase": "v686-v1",
            "create_only_after_terminal_gate": True,
            "reuse_if_existing": True,
            "routine_remaster_wait_required": False,
            "route_authority_through": "v725-v8",
            "repository_state": "PREPARED_NOT_SENT",
        },
    )
    write_json(
        X1 / "method-flow-startup.json",
        {
            "schema": "ghc.family.method-flow-startup.elaren-v685-v7.v1",
            "owner": OWNER,
            "phase": PHASE,
            "execution_authority": "owner_self_scoped_delta",
            "recovery_erases_failure": False,
            "startup_failures": [
                {"failure_id": ident, "failed_witness": failure, "initial_credit": 0, "recovery": recovery, "recovery_witness": "bounded_passing", "same_owner_only": True}
                for ident, failure, recovery in STARTUP_FAILURES
            ],
        },
    )
    write_json(
        X1 / "phase-truth.json",
        {
            "schema": "ghc.family.elaren-v685-v7.phase-truth.x1.v1",
            "owner": OWNER,
            "phase": PHASE,
            "source": SOURCE,
            "state": "PLANNING_ONLY_X1_CANDIDATE",
            "priority_pillar": "THOS Body",
            "declared_proposal_chain": 12030,
            "inherited_selection_count": 200,
            "new_proposal_count": 200,
            "expected_dispositions": dict(Counter(row["expected_execution_disposition"] for row in proposals)),
            "observed_outcomes_present": False,
            "terminal_verdict": TERMINAL_VERDICT,
            "identity_boundary": IDENTITY_BOUNDARY,
        },
    )
    write_json(
        X1 / "complete-incomplete-checklist.json",
        {
            "schema": "ghc.family.elaren-v685-v7.complete-incomplete.x1.v1",
            "complete": ["source and release verification", "two hundred inherited selections", "two hundred new proposal preregistrations", "portfolio plan validated against the release profile", "practice package skill runner and route plans"],
            "incomplete_by_lifecycle": ["x1 commit push and four-way equality", "all x2 execution", "package installation", "skill and runner builds and promotions", "evidence and final commits", "canonical validation", "future seat 02 task creation"],
            "protected_open": PROTECTED_GATES,
        },
    )

    scripts = [
        "scripts/build_ghc_family_elaren_kestrel_v685_v7_x1.py",
        "tests/test_ghc_family_elaren_kestrel_v685_v7_x1.py",
    ]
    material = sorted(set(WRITTEN + scripts))
    missing = [path for path in material if not (ROOT / path).exists()]
    if missing:
        raise RuntimeError(f"missing x1 material: {missing}")
    exclusions = [
        "docs/elaren-kestrel/v685-v7/validation/x1-index-manifest.json",
        "docs/elaren-kestrel/v685-v7/validation/x1-privacy-scan.json",
        "docs/elaren-kestrel/v685-v7/validation/x1-staged-review.json",
    ]
    write_json(VALIDATION / "x1-privacy-scan.json", privacy_scan(material))
    write_json(
        VALIDATION / "x1-index-manifest.json",
        {
            "schema": "ghc.family.normalized-lf-index-manifest.elaren-v685-v7.x1",
            "source": SOURCE,
            "entries": [manifest_entry(path) for path in material],
            "entry_count": len(material),
            "declared_self_exclusions": exclusions,
        },
    )
    expected = sorted(set(material + exclusions))
    write_json(
        VALIDATION / "x1-staged-review.json",
        {
            "schema": "ghc.family.staged-review.elaren-v685-v7.x1",
            "source": SOURCE,
            "lifecycle": "planning_only_x1",
            "expected_paths": expected,
            "path_count": len(expected),
            "forbidden_x2_paths": [],
        },
    )
    print(
        json.dumps(
            {
                "inherited": len(inherited),
                "new_proposals": len(proposals),
                "expected_dispositions": dict(Counter(row["expected_execution_disposition"] for row in proposals)),
                "portfolio": {key: len(portfolio[key]) for key in ("safe_now", "candidates", "clean_fix_refine", "exact_packets", "blocked_packets")},
                "packages": len(PACKAGES),
                "skills": len(SKILLS),
                "runners": len(RUNNERS),
                "maximum_neighbor_score": max_score,
                "x1_paths": len(expected),
            },
            separators=(",", ":"),
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--profile-runner", required=True, type=Path)
    args = parser.parse_args()
    build(args.profile.resolve(), args.profile_runner.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
