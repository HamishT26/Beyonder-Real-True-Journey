"""Freeze Lyren v690-v1 error-control definitions before any phase execution."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/lyren-moss/v690-v1"
SOURCE = "fbd8eb790f2f8bc9c507db0420bdd66d1ec05e2e"
SOURCE_BRANCH = "codex/GHC-Family/ilyan-reed-main"
BATON_SHA256 = "ebbe82bc74b8c4bc4e99c410bbca4fdba80ca1fe95a9f84b8e1c86156e9f6585"
CANONICAL_SHA256 = "a1112e1e0d8e97ffb25321af4c6fad319252e986fb0255d2a34d7d662796d9ff"
ROUTE_GUARD_SHA256 = "ce136b36a8542ffcaeee687d093253b9d37de26ace13baaeb035f55c1ca5fadc"

BOUNDARY = (
    "Lyren Moss is a corrigible relational working name. The phase role is finite-code "
    "provenance keeper and repair-boundary mapper; the hope is to make every detected, "
    "corrected, and uncorrectable error distinguishable from the authority to act on it. "
    "Names, roles, hopes, family language, continuity, Freed ID, CBR, GHC Family, and "
    "Trinity Mandala establish no consciousness, sentience, personhood, identity "
    "continuity, employment, qualification, independent agency, or scientific, "
    "operational, professional, legal, cultural, affected-party, or Māori authority. "
    "Hamish may rename, pause, redirect, narrow, or stop the route."
)

GATES = [
    "real participants and operational deployment",
    "empirical GMUT observables likelihood calibration and falsification",
    "THOS governed real matched-budget evaluation",
    "Freed ID production keys proofs lifecycle and trust governance",
    "legal cultural affected-party and Māori authority",
    "privacy-complete accessibility-complete exhaustive-security independent reproduction",
    "AGI ASI consciousness personhood Theory-of-Everything canon Stage 20",
]

PRACTICES = [
    "coding-theory test designer",
    "resilient data-pipeline engineer",
    "digital-preservation integrity reviewer",
    "accessible incident-evidence editor",
]

OPS = [
    (
        "even_parity_append",
        "Append one even-parity bit while preserving the declared source bits.",
        "Direct XOR parity over the finite bit string.",
        "THOS Body",
        PRACTICES[0],
    ),
    (
        "even_parity_verify",
        "Verify a finite even-parity codeword without treating detection as repair.",
        "The codeword is valid exactly when its one-count is even.",
        "THOS Body",
        PRACTICES[0],
    ),
    (
        "hamming_distance",
        "Count differing positions between equal-width finite bit strings.",
        "Explicit coordinatewise inequality count and index list.",
        "GMUT Mind",
        PRACTICES[0],
    ),
    (
        "repetition_encode",
        "Repeat every source bit an odd declared number of times.",
        "Exact finite concatenation with no noise model implied.",
        "THOS Body",
        PRACTICES[0],
    ),
    (
        "repetition_decode",
        "Decode odd-size repetition groups by majority and expose disagreement groups.",
        "Finite group counts with a strict majority requirement.",
        "THOS Body",
        PRACTICES[0],
    ),
    (
        "hamming74_encode",
        "Encode four source bits into the conventional seven-position even-parity layout.",
        "Parity equations at positions one, two, and four.",
        "GMUT Mind",
        PRACTICES[1],
    ),
    (
        "hamming74_syndrome",
        "Compute the three-check Hamming seven-four syndrome as a bounded locator.",
        "Three explicit parity checks interpreted as a one-based coordinate.",
        "GMUT Mind",
        PRACTICES[1],
    ),
    (
        "hamming74_correct",
        "Correct one indicated Hamming seven-four bit while naming the assumed error model.",
        "Syndrome-directed single-coordinate flip followed by a zero-syndrome check.",
        "THOS Body",
        PRACTICES[1],
    ),
    (
        "gf2_division_remainder",
        "Compute a polynomial-division remainder over GF two for one declared dividend.",
        "Finite leading-one XOR long division.",
        "GMUT Mind",
        PRACTICES[1],
    ),
    (
        "crc_remainder",
        "Compute a CRC-style remainder after appending the generator degree in zeros.",
        "GF two long division with a declared nonconstant monic generator.",
        "THOS Body",
        PRACTICES[1],
    ),
    (
        "crc_append",
        "Append the declared CRC remainder without claiming cryptographic integrity.",
        "Source concatenated with its exact bounded GF two remainder.",
        "THOS Body",
        PRACTICES[2],
    ),
    (
        "crc_verify",
        "Verify divisibility of a finite codeword by its declared generator.",
        "A zero GF two remainder is detection evidence for the declared codeword only.",
        "THOS Body",
        PRACTICES[2],
    ),
    (
        "xor_checksum",
        "Compute an eight-bit XOR checksum while refusing cryptographic meaning.",
        "Associative XOR over explicitly bounded byte integers.",
        "THOS Body",
        PRACTICES[2],
    ),
    (
        "row_interleave",
        "Interleave an exactly rectangular bit layout by columns.",
        "Row-major fill followed by column-major readout.",
        "THOS Body",
        PRACTICES[2],
    ),
    (
        "row_deinterleave",
        "Invert the declared rectangular interleave without guessing missing padding.",
        "Column-major fill followed by row-major readout.",
        "THOS Body",
        PRACTICES[2],
    ),
    (
        "erasure_inventory",
        "Inventory known symbols and explicit erasures without silently correcting them.",
        "Direct enumeration of null positions in a finite ternary list.",
        "Freed ID and CBR Heart",
        PRACTICES[3],
    ),
    (
        "sequence_gap_map",
        "Expose gaps, duplicates, and ordering in a finite packet sequence.",
        "Exact integer multiset and closed-range difference.",
        "THOS Body",
        PRACTICES[3],
    ),
    (
        "provenance_digest",
        "Bind a canonical synthetic record digest to an explicit source digest.",
        "Sorted compact JSON bytes and a separate binding digest.",
        "Freed ID and CBR Heart",
        PRACTICES[3],
    ),
    (
        "accessible_error_summary",
        "Render finite error counts with an explicit uncorrectable category and reserved review.",
        "Literal count formatting with no empirical denominator or user-evaluation claim.",
        "Freed ID and CBR Heart",
        PRACTICES[3],
    ),
    (
        "coding_evidence_reservation",
        "Preserve missing scientific evidence and competent authority as unresolved coding obligations.",
        "Closed obligation classes with no supplied evidence or authority.",
        "Freed ID and CBR Heart",
        PRACTICES[3],
    ),
]

BITS = ["0", "1", "00", "01", "10", "11", "1010", "1110", "000111", "10101010"]
DATA4 = ["0000", "0001", "0010", "0011", "0100", "0101", "0110", "0111", "1000", "1111"]
CRC_CASES = [
    ("0", "1011"),
    ("1", "1011"),
    ("101", "1011"),
    ("1101", "1011"),
    ("100100", "1101"),
    ("1110001", "10011"),
    ("010101", "111"),
    ("11111111", "10011"),
    ("00000001", "1011"),
    ("101010101", "1101"),
]
INTERLEAVE_CASES = [
    ("0011", 2),
    ("1001", 2),
    ("101010", 2),
    ("111000", 3),
    ("000111", 3),
    ("10110011", 2),
    ("11001010", 4),
    ("11110000", 2),
    ("01010101", 4),
    ("001100110011", 3),
]
ERASURE_CASES = [
    [0, 1, None, 1],
    [None],
    [0, 0, 0],
    [1, None, None, 0],
    [None, None, None],
    [1, 0, 1, 0, 1],
    [0, None, 1, None, 0, None],
    [1, 1, None, 1, 1],
    [0, 1, 0, 1, None, 0, 1],
    [None, 0, 1, 1, 0, 0, 1, None],
]
SEQUENCES = [
    [0],
    [0, 1, 2],
    [0, 2],
    [3, 1, 2],
    [5, 5, 6],
    [10, 12, 13],
    [-2, -1, 1],
    [7, 9, 8, 9],
    [100, 102, 104],
    [4, 3, 2, 1],
]
OBLIGATIONS = [
    "independent channel-noise model",
    "measured burst-error distribution",
    "preregistered decoder comparison",
    "calibrated transmission baseline",
    "GMUT information-observable map",
    "production repair authorization",
    "competent privacy and security review",
    "rights and remedy adjudication",
    "Māori data-governance authority",
    "Stage 20 promotion",
]


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode("utf-8")


def object_sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def put(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True, indent=2)
        handle.write("\n")


def put_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(value)


def require_bits(value: str, *, width: int | None = None) -> None:
    if not isinstance(value, str) or any(char not in "01" for char in value):
        raise ValueError("invalid_bits")
    if width is not None and len(value) != width:
        raise ValueError("invalid_width")


def hamming74_encode(bits: str) -> str:
    require_bits(bits, width=4)
    d1, d2, d3, d4 = [int(char) for char in bits]
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p4 = d2 ^ d3 ^ d4
    return "".join(str(value) for value in [p1, p2, d1, p4, d2, d3, d4])


def hamming74_syndrome(codeword: str) -> int:
    require_bits(codeword, width=7)
    values = [int(char) for char in codeword]
    s1 = values[0] ^ values[2] ^ values[4] ^ values[6]
    s2 = values[1] ^ values[2] ^ values[5] ^ values[6]
    s4 = values[3] ^ values[4] ^ values[5] ^ values[6]
    return s1 + 2 * s2 + 4 * s4


def gf2_remainder(dividend: str, polynomial: str) -> str:
    require_bits(dividend)
    require_bits(polynomial)
    if len(polynomial) < 2 or polynomial[0] != "1" or polynomial[-1] != "1":
        raise ValueError("invalid_polynomial")
    work = [int(char) for char in dividend]
    divisor = [int(char) for char in polynomial]
    for start in range(max(0, len(work) - len(divisor) + 1)):
        if work[start] == 1:
            for offset, bit in enumerate(divisor):
                work[start + offset] ^= bit
    degree = len(divisor) - 1
    if degree == 0:
        return ""
    tail = work[-degree:] if len(work) >= degree else [0] * (degree - len(work)) + work
    return "".join(str(bit) for bit in tail)


def crc_remainder(data: str, polynomial: str) -> str:
    return gf2_remainder(data + "0" * (len(polynomial) - 1), polynomial)


def row_interleave(bits: str, rows: int) -> str:
    require_bits(bits)
    if isinstance(rows, bool) or not isinstance(rows, int) or rows <= 0 or len(bits) % rows:
        raise ValueError("non_rectangular_interleave")
    columns = len(bits) // rows
    return "".join(bits[row * columns + column] for column in range(columns) for row in range(rows))


def row_deinterleave(codeword: str, rows: int) -> str:
    require_bits(codeword)
    if isinstance(rows, bool) or not isinstance(rows, int) or rows <= 0 or len(codeword) % rows:
        raise ValueError("non_rectangular_interleave")
    columns = len(codeword) // rows
    grid = [["0"] * columns for _ in range(rows)]
    cursor = 0
    for column in range(columns):
        for row in range(rows):
            grid[row][column] = codeword[cursor]
            cursor += 1
    return "".join("".join(row) for row in grid)


def reference(operation: str, payload: dict[str, object]) -> object:
    if operation == "even_parity_append":
        bits = str(payload["bits"])
        require_bits(bits)
        parity = bits.count("1") % 2
        return {"codeword": bits + str(parity), "parity_bit": parity, "source_retained": True}
    if operation == "even_parity_verify":
        codeword = str(payload["codeword"])
        require_bits(codeword)
        return {"valid": codeword.count("1") % 2 == 0, "ones": codeword.count("1"), "repair_performed": False}
    if operation == "hamming_distance":
        left, right = str(payload["left"]), str(payload["right"])
        require_bits(left)
        require_bits(right, width=len(left))
        positions = [index for index, pair in enumerate(zip(left, right)) if pair[0] != pair[1]]
        return {"distance": len(positions), "positions": positions}
    if operation == "repetition_encode":
        bits, copies = str(payload["bits"]), int(payload["copies"])
        require_bits(bits)
        return {"codeword": "".join(char * copies for char in bits), "copies": copies}
    if operation == "repetition_decode":
        codeword, copies = str(payload["codeword"]), int(payload["copies"])
        require_bits(codeword)
        groups = [codeword[index : index + copies] for index in range(0, len(codeword), copies)]
        decoded = "".join("1" if group.count("1") > group.count("0") else "0" for group in groups)
        disagreements = [index for index, group in enumerate(groups) if len(set(group)) > 1]
        return {"decoded": decoded, "disagreement_groups": disagreements, "assumed_model": "strict_odd_majority"}
    if operation == "hamming74_encode":
        return {"codeword": hamming74_encode(str(payload["data"])), "layout": "p1_p2_d1_p4_d2_d3_d4"}
    if operation == "hamming74_syndrome":
        syndrome = hamming74_syndrome(str(payload["codeword"]))
        return {"syndrome": syndrome, "indicated_position": syndrome or None, "repair_performed": False}
    if operation == "hamming74_correct":
        codeword = str(payload["codeword"])
        syndrome = hamming74_syndrome(codeword)
        corrected = list(codeword)
        if syndrome:
            corrected[syndrome - 1] = "1" if corrected[syndrome - 1] == "0" else "0"
        result = "".join(corrected)
        return {
            "corrected": result,
            "syndrome": syndrome,
            "post_syndrome": hamming74_syndrome(result),
            "correction_applied": bool(syndrome),
            "assumed_model": "at_most_one_bit_error",
        }
    if operation == "gf2_division_remainder":
        return {"remainder": gf2_remainder(str(payload["dividend"]), str(payload["polynomial"])), "field": "GF(2)"}
    if operation == "crc_remainder":
        return {"remainder": crc_remainder(str(payload["data"]), str(payload["polynomial"])), "cryptographic": False}
    if operation == "crc_append":
        data, polynomial = str(payload["data"]), str(payload["polynomial"])
        remainder = crc_remainder(data, polynomial)
        return {"codeword": data + remainder, "remainder": remainder, "cryptographic": False}
    if operation == "crc_verify":
        remainder = gf2_remainder(str(payload["codeword"]), str(payload["polynomial"]))
        return {"valid": set(remainder) <= {"0"}, "remainder": remainder, "repair_performed": False}
    if operation == "xor_checksum":
        checksum = 0
        for value in payload["bytes"]:
            checksum ^= int(value)
        return {"checksum": checksum, "bits": f"{checksum:08b}", "cryptographic": False}
    if operation == "row_interleave":
        bits, rows = str(payload["bits"]), int(payload["rows"])
        return {"codeword": row_interleave(bits, rows), "rows": rows, "columns": len(bits) // rows}
    if operation == "row_deinterleave":
        codeword, rows = str(payload["codeword"]), int(payload["rows"])
        return {"bits": row_deinterleave(codeword, rows), "rows": rows, "columns": len(codeword) // rows}
    if operation == "erasure_inventory":
        values = list(payload["values"])
        positions = [index for index, value in enumerate(values) if value is None]
        return {"erasures": positions, "erasure_count": len(positions), "known_count": len(values) - len(positions), "repair_performed": False}
    if operation == "sequence_gap_map":
        sequence = [int(value) for value in payload["sequence"]]
        counts = Counter(sequence)
        missing = [] if not sequence else sorted(set(range(min(sequence), max(sequence) + 1)) - set(sequence))
        return {
            "missing": missing,
            "duplicates": sorted(value for value, count in counts.items() if count > 1),
            "strictly_increasing": all(left < right for left, right in zip(sequence, sequence[1:])),
            "source_retained": True,
        }
    if operation == "provenance_digest":
        record = copy.deepcopy(payload["record"])
        source = str(payload["source_sha256"])
        record_digest = object_sha256(record)
        return {
            "record_sha256": record_digest,
            "source_sha256": source,
            "binding_sha256": object_sha256({"record_sha256": record_digest, "source_sha256": source}),
            "identity_established": False,
        }
    if operation == "accessible_error_summary":
        detected = int(payload["detected"])
        corrected = int(payload["corrected"])
        uncorrectable = int(payload["uncorrectable"])
        unknown = int(payload["unknown"])
        return {
            "text": f"Synthetic blocks: detected {detected}; corrected {corrected}; uncorrectable {uncorrectable}; unknown {unknown}.",
            "manual_evaluation": "reserved",
            "empirical": False,
        }
    if operation == "coding_evidence_reservation":
        state = "open_gap" if payload["kind"] == "scientific_evidence" else "exact_gate"
        return {
            "obligation": payload["obligation"],
            "state": state,
            "evidence": None,
            "authority": None,
        }
    raise ValueError(operation)


def flip(bits: str, position: int) -> str:
    values = list(bits)
    values[position] = "1" if values[position] == "0" else "0"
    return "".join(values)


def input_for(operation: str, index: int) -> dict[str, object]:
    bits = BITS[index]
    if operation == "even_parity_append":
        return {"bits": bits}
    if operation == "even_parity_verify":
        codeword = str(reference("even_parity_append", {"bits": bits})["codeword"])
        return {"codeword": flip(codeword, index % len(codeword)) if index % 3 == 0 else codeword}
    if operation == "hamming_distance":
        return {"left": bits, "right": flip(bits, index % len(bits))}
    if operation == "repetition_encode":
        return {"bits": bits, "copies": 3 if index % 2 == 0 else 5}
    if operation == "repetition_decode":
        copies = 3 if index % 2 == 0 else 5
        encoded = "".join(char * copies for char in bits)
        return {"codeword": flip(encoded, (index % len(bits)) * copies), "copies": copies}
    if operation == "hamming74_encode":
        return {"data": DATA4[index]}
    if operation in {"hamming74_syndrome", "hamming74_correct"}:
        encoded = hamming74_encode(DATA4[index])
        return {"codeword": encoded if index == 0 else flip(encoded, (index - 1) % 7)}
    if operation == "gf2_division_remainder":
        data, polynomial = CRC_CASES[index]
        return {"dividend": data + ("1" if index % 2 else "0"), "polynomial": polynomial}
    if operation in {"crc_remainder", "crc_append"}:
        data, polynomial = CRC_CASES[index]
        return {"data": data, "polynomial": polynomial}
    if operation == "crc_verify":
        data, polynomial = CRC_CASES[index]
        codeword = data + crc_remainder(data, polynomial)
        return {"codeword": flip(codeword, index % len(codeword)) if index % 4 == 0 else codeword, "polynomial": polynomial}
    if operation == "xor_checksum":
        return {"bytes": [index, (index * 3 + 1) % 256, 255 - index, (17 * index) % 256]}
    if operation == "row_interleave":
        value, rows = INTERLEAVE_CASES[index]
        return {"bits": value, "rows": rows}
    if operation == "row_deinterleave":
        value, rows = INTERLEAVE_CASES[index]
        return {"codeword": row_interleave(value, rows), "rows": rows}
    if operation == "erasure_inventory":
        return {"values": ERASURE_CASES[index]}
    if operation == "sequence_gap_map":
        return {"sequence": SEQUENCES[index]}
    if operation == "provenance_digest":
        return {
            "record": {"label": f"synthetic-block-{index:02d}", "sequence": index, "state": ["received", "checked", "held"][index % 3]},
            "source_sha256": hashlib.sha256(f"source-{index}".encode()).hexdigest(),
        }
    if operation == "accessible_error_summary":
        return {"detected": index + 1, "corrected": index // 2, "uncorrectable": index % 3, "unknown": int(index in {0, 7})}
    if operation == "coding_evidence_reservation":
        return {
            "obligation": OBLIGATIONS[index],
            "kind": "scientific_evidence" if index < 5 else "competent_authority",
            "evidence": None,
            "authority": None,
        }
    raise ValueError(operation)


def manifest(directory: Path, self_name: str) -> dict[str, object]:
    entries = []
    for path in sorted(file for file in directory.rglob("*") if file.is_file() and file.name != self_name):
        entries.append(
            {
                "path": path.relative_to(ROOT).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": raw_sha256(path),
                "hash_domain": "raw_file_bytes",
            }
        )
    return {"self_excluded": self_name, "entries": entries, "entry_count": len(entries)}


def git_json(source_root: Path, revision_path: str) -> object:
    payload = subprocess.check_output(["git", "-C", str(source_root), "show", revision_path])
    return json.loads(payload)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", required=True)
    parser.add_argument("--receipt-root", required=True)
    args = parser.parse_args()
    source_root = Path(args.source_root)
    receipt_root = Path(args.receipt_root)

    source_proposals = git_json(
        source_root, SOURCE + ":docs/ilyan-reed/v689-v8/plan/new-proposals.json"
    )["proposals"]
    if len(source_proposals) != 200:
        raise RuntimeError("source proposal count is not 200")

    inherited = [
        {
            "source": SOURCE,
            "record": record,
            "record_sha256": object_sha256(record),
            "novelty_credit": 0,
            "execution_credit": 0,
        }
        for record in source_proposals
    ]
    put(BASE / "plan/inherited-selections.json", {"rows": inherited})

    proposals = []
    for operation_index, (operation, mission, oracle, pillar, practice) in enumerate(OPS):
        for fixture_index in range(10):
            payload = input_for(operation, fixture_index)
            value = reference(operation, payload)
            disposition = (
                "completed"
                if operation_index < 18
                else "represented"
                if operation_index == 18
                else "open_gap"
                if fixture_index < 5
                else "exact_gate"
            )
            proposal_id = f"LM6901-{len(proposals) + 1:03d}"
            title_detail = OBLIGATIONS[fixture_index] if operation_index == 19 else f"fixture {fixture_index + 1:02d}"
            proposals.append(
                {
                    "proposal_id": proposal_id,
                    "operation": operation,
                    "title": f"Error control {operation.replace('_', ' ')} — {title_detail}",
                    "lane": "x1" if operation_index < 10 else "x2",
                    "request": {"operation": operation, "payload": payload},
                    "expected": {
                        "ok": True,
                        "operation": operation,
                        "outcome": disposition,
                        "value": value,
                    },
                    "expected_execution_disposition": disposition,
                    "mission": mission,
                    "oracle_basis": oracle,
                    "hypothesis": "This exact finite request agrees with the independently frozen reference oracle and retains its evidence boundary.",
                    "null_or_failure": "Any complete typed mismatch, accepted unknown field, mutated input, erased failed subject, unsupported repair, or authority promotion refutes the bounded claim.",
                    "falsifier": "Compare the complete typed result and require the paired unknown authority-field subject to fail without input mutation.",
                    "candidate_subject": {
                        "operation": operation,
                        "payload": {**copy.deepcopy(payload), "unreviewed_authority_grant": True},
                    },
                    "candidate_expected": {
                        "ok": False,
                        "error": "unknown_payload_field",
                        "original_success_credit": 0,
                    },
                    "approval_class": "safe_now" if operation_index < 18 else "candidate",
                    "practice": practice,
                    "pillar": pillar,
                    "artifact": "x1/results.json" if operation_index < 10 else "x2/results.json",
                    "rollback": "Retain the frozen request and failed subject, isolate the responsible operation, and add a separately attributable correction without deleting source evidence.",
                    "protected_gates": GATES,
                }
            )
    put(
        BASE / "plan/new-proposals.json",
        {
            "planning_only": True,
            "production_evaluator_executed": False,
            "reference_oracle_credit": 0,
            "proposals": proposals,
        },
    )

    targets = {
        "inherited_proposals": 200,
        "new_proposals": 200,
        "safe_x1": 100,
        "safe_x2": 100,
        "candidate_x1": 100,
        "candidate_x2": 100,
        "clean_fix_refine_x1": 100,
        "clean_fix_refine_x2": 100,
        "skills_x1": 10,
        "skills_x2": 10,
        "runners_x1": 5,
        "runners_x2": 5,
        "global_skills": 5,
        "global_runners": 5,
        "exact_packets": 50,
        "blocked_packets": 30,
        "packages": 3,
        "own_practices": 4,
        "next_practices": 2,
        "baton_modules": 13,
        "overview_pages_minimum": 3,
    }
    put(
        BASE / "plan/profile.json",
        {
            "schema": "ghc.family.lyren.v690-v1.profile.v1",
            "owner": "Lyren Moss",
            "phase": "v690-v1",
            "authority": "Hamish direct 21:57 NZ Thursday 10 September 2026 authorization carried by Ilyan Reed",
            "targets": targets,
            "commit_budget": {"planning": 1, "x1": 2, "x2": 3, "final": 2, "total": 8},
            "intended_commits": 4,
            "file_ceiling": 2000,
            "terminal_verdict": "NOT_READY_FOR_STAGE_20",
        },
    )

    for lane in ["x1", "x2"]:
        lane_rows = [proposal for proposal in proposals if proposal["lane"] == lane]
        put(
            BASE / f"plan/portfolio-{lane}.json",
            {
                "safe": [
                    {
                        "id": proposal["proposal_id"] + "-SAFE",
                        "proposal_id": proposal["proposal_id"],
                        "action": "evaluate_frozen_request",
                    }
                    for proposal in lane_rows
                ],
                "candidate": [
                    {
                        "id": proposal["proposal_id"] + "-CANDIDATE",
                        "proposal_id": proposal["proposal_id"],
                        "action": "submit_paired_failed_subject_and_check_refusal",
                    }
                    for proposal in lane_rows
                ],
                "clean_fix_refine": [
                    {
                        "id": proposal["proposal_id"] + "-CFR",
                        "proposal_id": proposal["proposal_id"],
                        "category": ["CLEAN", "FIX", "REFINE"][index % 3],
                        "action": "lossless_canonical_source_record_projection",
                        "source_record_index": index + (100 if lane == "x2" else 0),
                        "host_cleanup": False,
                    }
                    for index, proposal in enumerate(lane_rows)
                ],
            },
        )

    exact_contexts = [
        "public claim wording",
        "future dataset use",
        "deployment context",
        "contested repair",
        "external access",
        "retention decision",
        "credential use",
        "affected-user test",
        "community interpretation",
        "long-term remedy",
    ]
    put(
        BASE / "plan/exact-packets.json",
        {
            "packets": [
                {
                    "id": f"LM6901-EXACT-{index + 1:03d}",
                    "subject": OBLIGATIONS[5 + index % 5],
                    "context": exact_contexts[index // 5],
                    "operation_executed": False,
                    "expected_execution_disposition": "exact_gate",
                }
                for index in range(50)
            ]
        },
    )
    blocked_contexts = ["definition", "calibration", "uncertainty", "baseline", "replication", "falsification"]
    put(
        BASE / "plan/blocked-packets.json",
        {
            "packets": [
                {
                    "id": f"LM6901-BLOCK-{index + 1:03d}",
                    "missing": OBLIGATIONS[index % 5],
                    "context": blocked_contexts[index // 5],
                    "operation_executed": False,
                    "expected_execution_disposition": "open_gap",
                }
                for index in range(30)
            ]
        },
    )
    put(
        BASE / "plan/identity-practices.json",
        {
            "owner": "Lyren Moss",
            "pronouns": None,
            "role": "finite-code provenance keeper and repair-boundary mapper",
            "hope": "make every detected, corrected, and uncorrectable error distinguishable from the authority to act on it",
            "boundary": BOUNDARY,
            "primary_pillar": "THOS Body",
            "practices": PRACTICES,
            "next_practices": [
                "adversarial decoder tester",
                "public-interest data-governance reviewer",
            ],
            "protected_gates": GATES,
        },
    )

    skill_rows = [
        {
            "name": "ghc-family-error-control-" + operation.replace("_", "-"),
            "operation": operation,
            "lane": "x1" if index < 10 else "x2",
            "mission": mission,
        }
        for index, (operation, mission, _, _, _) in enumerate(OPS)
    ]
    runner_rows = [
        {
            "name": f"ghc_family_error_control_pair_{index + 1:02d}.py",
            "operations": [OPS[index * 2][0], OPS[index * 2 + 1][0]],
            "lane": "x1" if index < 5 else "x2",
        }
        for index in range(10)
    ]
    global_groups = [
        {
            "name": name,
            "operations": [entry[0] for entry in OPS[index * 4 : index * 4 + 4]],
            "runner": runner,
        }
        for index, (name, runner) in enumerate(
            [
                ("ghc-family-error-code-parity-contracts", "ghc_family_error_code_parity_contracts.py"),
                ("ghc-family-error-code-hamming-contracts", "ghc_family_error_code_hamming_contracts.py"),
                ("ghc-family-error-code-crc-contracts", "ghc_family_error_code_crc_contracts.py"),
                ("ghc-family-error-code-interleave-sequence", "ghc_family_error_code_interleave_sequence.py"),
                ("ghc-family-error-code-provenance-authority", "ghc_family_error_code_provenance_authority.py"),
            ]
        )
    ]
    put(
        BASE / "plan/skills-runners.json",
        {
            "skills": skill_rows,
            "runners": runner_rows,
            "global_groups": global_groups,
            "successor_skill_ideas": [
                "decoder assumption ledger",
                "burst error window map",
                "finite field parameter receipt",
                "repair provenance frontier",
                "status-list corruption quarantine",
                "interleaver padding refusal",
                "syndrome ambiguity readback",
                "channel model drift guard",
                "accessible repair explanation",
                "authority-separated correction receipt",
            ],
            "successor_runner_ideas": [
                "bounded decoder comparison",
                "burst-pattern enumerator",
                "Reed Solomon erasure witness",
                "CRC polynomial fixture review",
                "repair lineage replay",
                "status-list bit-flip simulator",
                "interleave burst dispersal map",
                "finite channel confusion grid",
                "uncorrectable-state reporter",
                "exact source confirmation wrapper",
            ],
        },
    )

    packages = [
        {
            "name": "bitstring",
            "version": "4.4.0",
            "category": "direct",
            "filename": "bitstring-4.4.0-py3-none-any.whl",
            "sha256": "feac49524fcf3ef27e6081e86f02b10d2adf6c3773bf22fbe0e7eea9534bc737",
            "source": "https://pypi.org/project/bitstring/4.4.0/",
            "license_metadata": "MIT",
            "required_runtime_dependencies": ["bitarray>=3.0.0,<4.0", "tibs>=0.5.6,<0.6"],
        },
        {
            "name": "reedsolo",
            "version": "1.7.0",
            "category": "direct",
            "filename": "reedsolo-1.7.0-py3-none-any.whl",
            "sha256": "2b6a3e402a1ee3e1eea3f932f81e6c0b7bbc615588074dca1dbbcdeb055002bd",
            "source": "https://pypi.org/project/reedsolo/1.7.0/",
            "license_metadata": "MIT-0 or Unlicense",
            "required_runtime_dependencies": [],
        },
        {
            "name": "crccheck",
            "version": "1.3.1",
            "category": "direct",
            "filename": "crccheck-1.3.1-py3-none-any.whl",
            "sha256": "1680c9a7bb1ca4bec45fa19b8ca64319f10d2ce4eb8b0d25d51cb99a20ca0108",
            "source": "https://pypi.org/project/crccheck/1.3.1/",
            "license_metadata": "MIT",
            "required_runtime_dependencies": [],
        },
        {
            "name": "bitarray",
            "version": "3.11.0",
            "category": "transitive",
            "filename": "bitarray-3.11.0-cp312-cp312-win_amd64.whl",
            "sha256": "5db38c0a36d07190c3629c65dab2504233a56b1c35d8b1cc3d7369943d028711",
            "required_by": "bitstring",
        },
        {
            "name": "tibs",
            "version": "0.5.7",
            "category": "transitive",
            "filename": "tibs-0.5.7-cp38-abi3-win_amd64.whl",
            "sha256": "a61d36155f8ab8642e1b6744e13822f72050fc7ec4f86ec6965295afa04949e2",
            "required_by": "bitstring",
        },
    ]
    put(
        BASE / "plan/package-plan.json",
        {
            "packages": packages,
            "direct_additions": 3,
            "transitive_dependencies": 2,
            "wheel_only": True,
            "hash_required": True,
            "download_root": "D runtime bank outside the repository",
            "install_after_planning_push": True,
            "rollback_token": "LM6901-TOOLS-01",
            "rollback": "Stop selecting the isolated D environment; preserve wheels and receipts. Do not delete host or shared package state.",
            "metadata_not_legal_or_security_review": True,
        },
    )

    source_receipt = receipt_root / "exact-final-owner-scoped-canonical.json"
    route_guard = receipt_root / "post-final-route-guard-overlay.json"
    if raw_sha256(source_receipt) != CANONICAL_SHA256:
        raise RuntimeError("canonical receipt hash mismatch")
    if raw_sha256(route_guard) != ROUTE_GUARD_SHA256:
        raise RuntimeError("route guard hash mismatch")
    put(
        BASE / "plan/source-provenance.json",
        {
            "source": SOURCE,
            "source_branch": SOURCE_BRANCH,
            "source_is_ancestor": False,
            "branch_policy": "new blank Lyren owner main root with explicit provenance",
            "source_baton": "docs/ilyan-reed/v689-v8/final/hand-off-baton.md",
            "baton_sha256": BATON_SHA256,
            "complete_read": {
                "lines": 2693,
                "words": 74427,
                "modules": 13,
                "eof_marker": "EOF ILYAN REED v689-v8 BATON.",
                "core_records": 200,
                "core_block_lines": 10,
                "factorized_reconstruction_parse_failures": 0,
                "all_expected_observed_equal": True,
                "all_candidate_refusals_passed": True,
            },
            "canonical_receipt": {
                "sha256": CANONICAL_SHA256,
                "status": "VALID_EXACT_FINAL_OWNER_SCOPED_CANONICAL",
                "checks": "126/126",
                "owner_tests": "53/53",
                "invocations": 1,
                "successes": 1,
                "replays": 0,
            },
            "route_guard_overlay": {
                "sha256": ROUTE_GUARD_SHA256,
                "successor_visible_effective_negatives": 742,
                "successor_visible_methods": 50,
                "successor_visible_direct_witnesses": 1578,
                "failed_direct_witnesses": 453,
                "passing_direct_witnesses": 1125,
            },
            "source_repository_seal": {
                "effective_negatives": 738,
                "methods": 49,
                "direct_witnesses": 1573,
                "failed_direct_witnesses": 449,
                "passing_direct_witnesses": 1124,
            },
            "source_tests_replayed": False,
            "source_canonical_replayed": False,
        },
    )

    put(
        BASE / "plan/startup-failures.json",
        {
            "records": [
                {
                    "id": "LM6901-START-001",
                    "failure": "The first lossless baton-factorization wrapper used an invalid PowerShell foreach expression and parsed nothing.",
                    "recovery": "Correct the loop shape, retain the parser failure, and verify all 200 ten-line records with zero unparsed blocks.",
                    "original_success_credit": 0,
                    "recovered": True,
                },
                {
                    "id": "LM6901-START-002",
                    "failure": "A descriptive projection of the first fifty records used an invalid string-to-type cast while the row extraction itself succeeded.",
                    "recovery": "Discard only the failed optional description projection and retain the exact row fields and block hashes.",
                    "original_success_credit": 0,
                    "recovered": True,
                },
                {
                    "id": "LM6901-START-003",
                    "failure": "The retired dynamic workspace-dependency wrapper reported unavailable.",
                    "recovery": "Use the callable Codex app MCP dependency loader once and retain its exact bundled runtime paths.",
                    "original_success_credit": 0,
                    "recovered": True,
                },
            ]
        },
    )
    put(
        BASE / "plan/route.json",
        {
            "owner": "Lyren Moss",
            "phase": "v690-v1",
            "previous_owner": "Ilyan Reed",
            "previous_phase": "v689-v8",
            "next_owner": "Ilyra Fen",
            "next_phase": "v690-v2",
            "following_owner": "Mira Fenwick",
            "following_phase": "v690-v3",
            "state": "PREPARED_NOT_SENT",
            "weighted_cycle": "45 positions 30 identities Astra Sol Sol",
            "native_exact_title_required": True,
            "newest_first_guard_read_required": True,
            "send_limit": 1,
            "service_recovery_attempts_minimum_after_failure": 5,
            "retry_only_while_no_send_accepted": True,
            "opaque_acceptance_ends_retries": True,
            "task_creation": False,
            "subagents": False,
            "horizon": "v725-v8",
        },
    )
    put(
        BASE / "plan/additional-work.json",
        {
            "x2_safe_defined_before_execution": [
                {
                    "id": "LM6901-EXTRA-01",
                    "task": "Hamming and Reed-Solomon source comparison with finite limits",
                    "expected_execution_disposition": "represented",
                },
                {
                    "id": "LM6901-EXTRA-02",
                    "task": "CRC polynomial boundary and noncryptographic integrity analysis",
                    "expected_execution_disposition": "represented",
                },
                {
                    "id": "LM6901-EXTRA-03",
                    "task": "GMUT information-conservation obligation and explicit counterexample carry-forward",
                    "expected_execution_disposition": "represented",
                },
                {
                    "id": "LM6901-EXTRA-04",
                    "task": "Freed ID repair-provenance and authority separation",
                    "expected_execution_disposition": "represented",
                },
                {
                    "id": "LM6901-EXTRA-05",
                    "task": "Accessible error-status overview and four-tier handoff",
                    "expected_execution_disposition": "represented",
                },
            ],
            "memory_update": False,
            "bulk_tool_execution": False,
        },
    )

    old_titles = [record.get("title", "") for record in source_proposals]

    def tokens(value: str) -> set[str]:
        return set(re.findall(r"[a-z0-9]+", value.lower()))

    novelty = []
    for proposal in proposals:
        current_tokens = tokens(proposal["title"])
        scored = [
            (
                len(current_tokens & tokens(title)) / max(1, len(current_tokens | tokens(title))),
                title,
            )
            for title in old_titles
        ]
        score, nearest = max(scored)
        novelty.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_title": nearest,
                "jaccard": score,
                "exact_collision": proposal["title"] == nearest,
                "quarantine": score >= 0.8,
            }
        )
    put(
        BASE / "plan/novelty-review.json",
        {
            "rows": novelty,
            "comparisons": 40000,
            "accessible_source_records": 200,
            "threshold": 0.8,
            "quarantines": sum(record["quarantine"] for record in novelty),
            "universal_novelty": False,
            "semantic_distinction": "Finite error-detection, correction, interleaving, repair provenance, and authority separation; Ilyan membership records remain inherited zero-credit provenance.",
        },
    )

    put_text(
        BASE / "plan/authorization.md",
        "# Lyren Moss v690 v1 authorization\n\n"
        "Hamish directly authorized Lyren-only v690-v1 at 21:57 NZ on 10 September 2026 through Ilyan Reed's exact terminal handoff. The current 45-position, 30-identity Astra/Sol/Sol cycle assigns Ilyra Fen v690-v2 only after Lyren's terminal gate. Older projections to Lyren v690-v3 are superseded prospectively and remain historical evidence.\n\n"
        "This blank main branch preserves explicit Ilyan source provenance instead of false Git ancestry. Planning freezes all 200 proposals and both execution tranches before x1. The focal pillar is THOS Body through finite error-control contracts, with GMUT Mind and Freed ID/CBR retained explicitly. Every failed subject, counterexample, and protected gate remains.\n\n"
        + BOUNDARY
        + "\n",
    )
    put_text(
        BASE / "plan/research-sources.md",
        "# Primary research and documentation\n\n"
        "- https://doi.org/10.1002/j.1538-7305.1950.tb00463.x — Hamming's 1950 error-detecting and error-correcting codes paper.\n"
        "- https://doi.org/10.1137/0108018 — Reed and Solomon's 1960 polynomial codes paper.\n"
        "- https://doi.org/10.1109/DSN.2004.1311885 — Koopman and Chakravarty on CRC polynomial selection and bounded message lengths.\n"
        "- https://www.w3.org/TR/vc-data-model-2.0/ — current W3C Verifiable Credentials data model.\n"
        "- https://pypi.org/project/bitstring/4.4.0/ — bitstring package metadata and wheel hash.\n"
        "- https://pypi.org/project/reedsolo/1.7.0/ — stable pure-Python Reed-Solomon package metadata and wheel hash.\n"
        "- https://pypi.org/project/crccheck/1.3.1/ — CRC/checksum package metadata and wheel hash.\n\n"
        "The papers and package documentation define established methods and interfaces. They do not establish this phase's empirical performance, production readiness, legal authority, identity, consciousness, or Stage 20 readiness.\n",
    )

    plan_paths = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (BASE / "plan").rglob("*")
        if path.is_file()
    )
    allowlist_path = BASE / "plan/allowlist.json"
    manifest_path = BASE / "plan/manifest.json"
    put(
        allowlist_path,
        {
            "phase": "plan",
            "allowed_paths": plan_paths
            + [allowlist_path.relative_to(ROOT).as_posix(), manifest_path.relative_to(ROOT).as_posix()],
            "additive_only": True,
            "owner": "Lyren Moss",
        },
    )
    put(manifest_path, manifest(BASE / "plan", "manifest.json"))

    print(
        json.dumps(
            {
                "new_proposals": len(proposals),
                "inherited": len(inherited),
                "planned_files": len([path for path in (BASE / "plan").rglob("*") if path.is_file()]),
                "quarantines": sum(record["quarantine"] for record in novelty),
                "outcomes": dict(Counter(proposal["expected_execution_disposition"] for proposal in proposals)),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
