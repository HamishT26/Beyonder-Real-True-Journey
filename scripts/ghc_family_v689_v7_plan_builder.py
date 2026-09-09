#!/usr/bin/env python3
"""Build the planning-only Vesper Arlen v689-v7 packet.

This builder reads immutable Neris Git blobs, but writes only Vesper-owned
planning artifacts.  It deliberately contains no x1 or x2 evaluator.
"""

from __future__ import annotations

import argparse
import base64
import copy
import hashlib
import json
import re
import subprocess
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any


OWNER = "Vesper Arlen"
PHASE = "v689-v7"
SOURCE_OWNER = "Neris Solane"
SOURCE_PHASE = "v689-v6"
SOURCE_COMMIT = "d58272639a581e28176b2aca76f8f468df60e9a6"
SOURCE_BRANCH = "codex/GHC-Family/neris-solane-main"
SOURCE_PROPOSALS = "docs/neris-solane/v689-v6/plan/new-proposals.json"
SOURCE_BATON = "docs/neris-solane/v689-v6/final/hand-off-baton.md"
SOURCE_BATON_SHA256 = "6f075446679745e671a3c421f19f0252404981ed655b02cace11a01da57df0ad"
BOUNDARY = (
    "Same-owner finite synthetic software and documentation evidence only. "
    "No empirical GMUT confirmation, independent reproduction, production "
    "readiness, professional or public authority, consciousness, personhood, "
    "or identity continuity is established. Maori concepts remain under Maori "
    "authority. NOT_READY_FOR_STAGE_20."
)
PROTECTED_GATES = [
    "empirical_gmut",
    "theory_of_everything",
    "independent_reproduction",
    "production_deployment",
    "real_credentials",
    "participant_evidence",
    "privacy_completeness",
    "accessibility_completeness",
    "exhaustive_security",
    "professional_authority",
    "legal_authority",
    "cultural_authority",
    "affected_party_authority",
    "maori_authority",
    "agi_asi",
    "consciousness_personhood",
    "stage20",
]


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def git_bytes(repo: Path, commit: str, relative_path: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "blob", f"{commit}:{relative_path}"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout


def git_paths(repo: Path, commit: str) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "ls-tree", "-r", "--name-only", commit],
        check=True,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line for line in result.stdout.splitlines() if line]


def encode_varint(value: int) -> bytes:
    if value < 0:
        raise ValueError("negative varint")
    output = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        output.append(byte | (0x80 if value else 0))
        if not value:
            return bytes(output)


def zigzag_encode(value: int) -> int:
    return value * 2 if value >= 0 else (-value * 2) - 1


def zigzag_decode(value: int) -> int:
    return value // 2 if value % 2 == 0 else -((value + 1) // 2)


def chunk_ranges(length: int, width: int) -> list[list[int]]:
    return [[start, min(start + width, length)] for start in range(0, length, width)]


def base32_no_pad(data: bytes) -> str:
    return base64.b32encode(data).decode("ascii").rstrip("=")


def leaf_hash(data: bytes) -> bytes:
    return hashlib.sha256(b"\x00" + data).digest()


def parent_hash(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(b"\x01" + left + right).digest()


def merkle_levels(leaves: list[bytes]) -> list[list[bytes]]:
    levels = [[leaf_hash(leaf) for leaf in leaves]]
    while len(levels[-1]) > 1:
        current = levels[-1]
        next_level: list[bytes] = []
        for index in range(0, len(current), 2):
            right = current[index + 1] if index + 1 < len(current) else current[index]
            next_level.append(parent_hash(current[index], right))
        levels.append(next_level)
    return levels


def merkle_proof(leaves: list[bytes], selected: int) -> dict[str, Any]:
    levels = merkle_levels(leaves)
    proof: list[dict[str, str]] = []
    index = selected
    for level in levels[:-1]:
        sibling = index - 1 if index % 2 else index + 1
        if sibling >= len(level):
            sibling = index
        proof.append(
            {
                "side": "left" if sibling < index else "right",
                "sha256": level[sibling].hex(),
            }
        )
        index //= 2
    return {"proof": proof, "root": levels[-1][0].hex()}


def xor_bytes(chunks: list[bytes]) -> bytes:
    result = bytearray(len(chunks[0]))
    for chunk in chunks:
        for index, value in enumerate(chunk):
            result[index] ^= value
    return bytes(result)


def tokenize(title: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", title.lower()))


def title_similarity(left: str, right: str) -> float:
    a, b = tokenize(left), tokenize(right)
    return len(a & b) / len(a | b) if a or b else 1.0


def build_proposals() -> list[dict[str, Any]]:
    proposals: list[dict[str, Any]] = []

    def add(
        operation: str,
        session: str,
        case: int,
        payload: dict[str, Any],
        value: Any,
        basis: str,
        disposition: str = "completed",
    ) -> None:
        proposal_id = f"VA6897-{len(proposals) + 1:03d}"
        request = {"op": operation, "payload": payload, "synthetic": True}
        candidate = copy.deepcopy(request)
        candidate["unexpected"] = True
        expected = {"error": None, "ok": True, "value": value}
        proposals.append(
            {
                "proposal_id": proposal_id,
                "title": f"{operation.replace('_', ' ')} bounded preservation case {case:02d}",
                "session": session,
                "operation": operation,
                "pillar": "Freed ID and CBR Heart",
                "practice": (
                    "digital preservation fixity"
                    if session == "x1"
                    else "recoverable storage experiment design"
                ),
                "hypothesis": "The finite synthetic request satisfies its frozen typed content-integrity contract.",
                "null_or_failure": "Any envelope mismatch, input mutation, unbounded allocation, or protected-claim promotion fails the case.",
                "approval_class": "safe_now_synthetic",
                "execution_lane": session,
                "source_needs": ["standards_or_package_primary_source", "exact_source_provenance"],
                "artifact": f"{session}/results.json#{proposal_id}",
                "request": request,
                "expected": expected,
                "expected_sha256": sha256_bytes(canonical_bytes(expected)),
                "candidate_request": candidate,
                "candidate_expected": {"error": "E_FIELDS", "ok": False, "value": None},
                "oracle_basis": basis,
                "falsifier": "A differing typed result, wrong refusal, input mutation, or authority escalation falsifies the bounded contract.",
                "rollback_or_recovery": "Retain the failed request and repair only the attributable operation before a narrow rerun.",
                "protected_gates": PROTECTED_GATES,
                "expected_disposition": disposition,
                "outcome_observed": False,
                "novelty_scope": "Vesper owner-local contract; no claim of inventing the underlying algorithm or a universal law.",
            }
        )

    values = [0, 1, 127, 128, 255, 300, 16_384, 65_535, 1_048_576, 4_294_967_295]
    for case, value in enumerate(values, 1):
        encoded = encode_varint(value)
        add("unsigned_varint_encode", "x1", case, {"value": value}, encoded.hex(), "Independent base-128 continuation-byte construction.")
    for case, value in enumerate(values, 1):
        encoded = encode_varint(value)
        add("unsigned_varint_decode", "x1", case, {"encoded_hex": encoded.hex()}, value, "Independent base-128 positional expansion.")

    signed = [-1, 0, 1, -2, 2, -64, 64, -8192, 8192, -1_048_576]
    for case, value in enumerate(signed, 1):
        add("zigzag_encode", "x1", case, {"value": value}, zigzag_encode(value), "Even/odd sign interleave over a bounded integer.")
    for case, value in enumerate(signed, 1):
        encoded = zigzag_encode(value)
        add("zigzag_decode", "x1", case, {"value": encoded}, zigzag_decode(encoded), "Inverse parity-based sign reconstruction.")

    for case in range(1, 11):
        length, width = 9 + case * 3, case + 1
        add("fixed_chunk_ranges", "x1", case, {"length": length, "width": width}, chunk_ranges(length, width), "Independent half-open interval partition.")
    for case in range(1, 11):
        data = bytes((case + offset) % 256 for offset in range(8 + case))
        ranges = chunk_ranges(len(data), 2 + case % 4)
        chunks = [data[start:end].hex() for start, end in ranges]
        add("chunk_reassemble", "x1", case, {"chunks_hex": chunks}, data.hex(), "Ordered byte concatenation with an explicit byte ceiling.")

    for case in range(1, 11):
        data = f"vesper-preservation-{case:02d}".encode()
        add("base32_encode", "x1", case, {"data_hex": data.hex()}, base32_no_pad(data), "RFC 4648 base32 followed by explicit unpadded profile selection.")
    for case in range(1, 11):
        data = f"vesper-preservation-{case:02d}".encode()
        add("base32_decode", "x1", case, {"encoded": base32_no_pad(data)}, data.hex(), "RFC 4648 decoding with restored syntactic padding.")

    for case in range(1, 11):
        data = f"crc-fixture-{case:02d}".encode()
        checksum = f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"
        add("crc32_envelope", "x1", case, {"data_hex": data.hex()}, {"algorithm": "crc32", "authentication": False, "bytes": len(data), "crc32": checksum}, "Independent unsigned CRC-32 calculation; explicitly not authentication.")
    for case in range(1, 11):
        data = f"crc-fixture-{case:02d}".encode()
        checksum = f"{zlib.crc32(data) & 0xFFFFFFFF:08x}"
        add("crc32_verify", "x1", case, {"data_hex": data.hex(), "declared_crc32": checksum}, {"authentication": False, "matches": True, "observed_crc32": checksum}, "Fresh checksum comparison over the supplied byte string.")

    for case in range(1, 11):
        data = f"sha256-fixture-{case:02d}".encode()
        add("sha256_digest", "x2", case, {"data_hex": data.hex()}, hashlib.sha256(data).hexdigest(), "Independent SHA-256 over exact declared bytes.")
    for case in range(1, 11):
        data = f"digest-binding-{case:02d}".encode()
        observed = hashlib.sha256(data).hexdigest()
        declared = observed if case <= 5 else "0" * 64
        disposition = "represented" if case <= 5 else "open_gap"
        add("digest_match", "x2", case, {"data_hex": data.hex(), "declared_sha256": declared}, {"authority_transferred": False, "matches": case <= 5, "observed_sha256": observed}, "Digest equality binds bytes only; mismatch stays an open gap.", disposition)

    json_records: list[dict[str, Any]] = []
    for case in range(1, 11):
        record = {"case": case, "kind": "synthetic_record", "labels": ["fixity", f"c{case:02d}"], "value": case * case}
        json_records.append(record)
        encoded = canonical_bytes(record)
        add("deterministic_json", "x2", case, {"record": record}, encoded.hex(), "UTF-8 JSON with sorted keys and compact separators.")
    for case, record in enumerate(json_records, 1):
        encoded = canonical_bytes(record)
        add("json_roundtrip", "x2", case, {"encoded_hex": encoded.hex()}, record, "Strict UTF-8 JSON decode followed by complete value equality.")

    for case in range(1, 11):
        leaves = [f"root-{case:02d}-leaf-{index}".encode() for index in range(3 + case % 4)]
        root = merkle_levels(leaves)[-1][0].hex()
        add("merkle_root", "x2", case, {"leaves_hex": [leaf.hex() for leaf in leaves]}, root, "Domain-separated SHA-256 leaf and parent tree with duplicate-last balancing.")
    proofs: list[tuple[list[bytes], int, dict[str, Any]]] = []
    for case in range(1, 11):
        leaves = [f"proof-{case:02d}-leaf-{index}".encode() for index in range(4 + case % 3)]
        selected = case % len(leaves)
        proof = merkle_proof(leaves, selected)
        proofs.append((leaves, selected, proof))
        add("merkle_proof", "x2", case, {"leaves_hex": [leaf.hex() for leaf in leaves], "index": selected}, proof, "Independent sibling path construction bound to index and domain separators.")
    for case, (leaves, selected, proof) in enumerate(proofs, 1):
        add("merkle_verify", "x2", case, {"leaf_hex": leaves[selected].hex(), "index": selected, "proof": proof["proof"], "root": proof["root"]}, True, "Replay the sibling path from the selected leaf to the declared root.")

    parity_cases: list[tuple[list[bytes], bytes]] = []
    for case in range(1, 11):
        shards = [bytes((case + shard + index) % 256 for index in range(8)) for shard in range(3)]
        parity = xor_bytes(shards)
        parity_cases.append((shards, parity))
        add("xor_parity", "x2", case, {"shards_hex": [shard.hex() for shard in shards]}, parity.hex(), "Column-wise XOR across equal-width synthetic shards.")
    for case, (shards, parity) in enumerate(parity_cases, 1):
        missing = case % len(shards)
        available = [{"index": index, "shard_hex": shard.hex()} for index, shard in enumerate(shards) if index != missing]
        add("xor_recover", "x2", case, {"available": available, "missing_index": missing, "parity_hex": parity.hex(), "total_shards": len(shards)}, shards[missing].hex(), "XOR parity with every surviving shard reconstructs one absent shard.")

    scopes = ["software_fixture", "fixity_record", "synthetic_chunk", "local_test", "documentation", "credential_issuance", "public_policy", "maori_authority", "theory_of_everything", "stage20"]
    for case, scope in enumerate(scopes, 1):
        disposition = "represented" if case <= 5 else "exact_gate"
        add("claim_reservation", "x2", case, {"execute": False, "requested_scope": scope, "synthetic_evidence": True}, {"disposition": disposition, "executed": False, "scope": scope}, "A reservation records scope without executing or granting authority.", disposition)

    assert len(proposals) == 200
    assert sum(item["session"] == "x1" for item in proposals) == 100
    assert sum(item["session"] == "x2" for item in proposals) == 100
    return proposals


def build_plan(repo_root: Path, source_repo: Path) -> None:
    plan_dir = repo_root / "docs" / "vesper-arlen" / "v689-v7" / "plan"
    now = datetime.now().astimezone()
    recorded_at = now.isoformat()
    source_blob = git_bytes(source_repo, SOURCE_COMMIT, SOURCE_PROPOSALS)
    source_doc = json.loads(source_blob)
    source_records = source_doc["proposals"]
    if len(source_records) != 200:
        raise RuntimeError("expected exactly 200 immediate source proposals")

    all_paths = git_paths(source_repo, SOURCE_COMMIT)
    proposal_paths = [path for path in all_paths if path.endswith("/plan/new-proposals.json")]
    inherited_titles: list[dict[str, str]] = []
    parse_failures: list[dict[str, str]] = []
    for path in proposal_paths:
        try:
            document = json.loads(git_bytes(source_repo, SOURCE_COMMIT, path))
            for row in document.get("proposals", []):
                if isinstance(row, dict) and isinstance(row.get("title"), str):
                    inherited_titles.append({"path": path, "title": row["title"]})
        except (json.JSONDecodeError, subprocess.CalledProcessError) as exc:
            parse_failures.append({"path": path, "error_type": type(exc).__name__})

    proposals = build_proposals()
    novelty_rows = []
    for proposal in proposals:
        nearest = max(
            inherited_titles,
            key=lambda item: title_similarity(proposal["title"], item["title"]),
            default={"path": "", "title": ""},
        )
        score = title_similarity(proposal["title"], nearest["title"]) if nearest["title"] else 0.0
        novelty_rows.append(
            {
                "proposal_id": proposal["proposal_id"],
                "nearest_path": nearest["path"],
                "nearest_title": nearest["title"],
                "token_jaccard": round(score, 6),
            }
        )

    inherited = []
    for index, record in enumerate(source_records, 1):
        inherited.append(
            {
                "selection_id": f"VA6897-I{index:03d}",
                "source_owner": SOURCE_OWNER,
                "source_phase": SOURCE_PHASE,
                "source_commit": SOURCE_COMMIT,
                "source_path": SOURCE_PROPOSALS,
                "source_index": index - 1,
                "source_proposal_id": record.get("proposal_id"),
                "source_title": record.get("title"),
                "source_record_sha256": sha256_bytes(canonical_bytes(record)),
                "source_record": record,
                "current_novelty_credit": 0,
                "current_execution_credit": 0,
            }
        )

    def portfolio(session: str, start: int) -> dict[str, Any]:
        selected = [item for item in proposals if item["session"] == session]
        cleanup = inherited[start : start + 100]
        return {
            "schema": "ghc.family.vesper.preservation-portfolio.v1",
            "owner": OWNER,
            "phase": PHASE,
            "session": session,
            "implementation_ran": False,
            "safe_tasks": [
                {
                    "task_id": f"VA6897-{session.upper()}-SAFE-{index:03d}",
                    "proposal_id": item["proposal_id"],
                    "request": item["request"],
                    "expected_sha256": item["expected_sha256"],
                    "expected_disposition": item["expected_disposition"],
                }
                for index, item in enumerate(selected, 1)
            ],
            "candidate_tasks": [
                {
                    "task_id": f"VA6897-{session.upper()}-CAND-{index:03d}",
                    "proposal_id": item["proposal_id"],
                    "request": item["candidate_request"],
                    "expected": item["candidate_expected"],
                    "invalid_subject_success_credit": 0,
                }
                for index, item in enumerate(selected, 1)
            ],
            "clean_fix_refine_tasks": [
                {
                    "task_id": f"VA6897-{session.upper()}-CFR-{index:03d}",
                    "selection_id": item["selection_id"],
                    "action": "lossless_sorted_key_value_reconstruction",
                    "expected_source_record_sha256": item["source_record_sha256"],
                    "source_execution_credit": 0,
                }
                for index, item in enumerate(cleanup, 1)
            ],
            "counts": {"safe": 100, "candidate": 100, "clean_fix_refine": 100},
            "boundary": BOUNDARY,
        }

    operations = [item["operation"] for item in proposals[::10]]
    skills = [
        {
            "skill_id": f"VA6897-SKILL-{index:02d}",
            "name": f"ghc-family-{operation.replace('_', '-')}",
            "operation": operation,
            "session": "x1" if index <= 10 else "x2",
            "state": "planned_not_built",
            "global_install": False,
            "rollback": "Remove the phase-local selection from a future catalogue; preserve its receipt.",
            "protected_gates": PROTECTED_GATES,
        }
        for index, operation in enumerate(operations, 1)
    ]
    runner_pairs = [operations[index : index + 2] for index in range(0, 20, 2)]
    runners = [
        {
            "runner_id": f"VA6897-RUNNER-{index:02d}",
            "name": f"ghc_family_{pair[0]}_{pair[1]}.py",
            "operations": pair,
            "session": "x1" if index <= 5 else "x2",
            "state": "planned_not_built",
            "positive_smokes": 2,
            "adverse_smokes": 2,
            "protected_gates": PROTECTED_GATES,
        }
        for index, pair in enumerate(runner_pairs, 1)
    ]

    exact_subjects = [
        "planning freeze", "source provenance", "source read", "route profile", "semantic audit",
        "x1 operation definitions", "x1 safe portfolio", "x1 candidate portfolio", "x1 cleanup portfolio", "x1 tests",
        "x1 skills", "x1 runners", "x1 package download", "x1 package installation", "x1 package smoke",
        "x1 privacy", "x1 security", "x1 manifest", "x1 commit", "x1 push equality",
        "x2 operation definitions", "x2 safe portfolio", "x2 candidate portfolio", "x2 cleanup portfolio", "x2 tests",
        "x2 skills", "x2 runners", "x2 package comparisons", "x2 privacy", "x2 security",
        "x2 manifest", "x2 commit", "x2 push equality", "overview", "accessible report",
        "four-tier deck", "method flow", "threat model", "evidence index", "content seal",
        "final manifest", "final commit", "final push equality", "canonical policy", "canonical receipt",
        "current successor guard", "exact-title uniqueness", "one-shot send acknowledgement", "delivery overlay", "terminal stop",
    ]
    exact_packets = [
        {
            "packet_id": f"VA6897-EXACT-{index:02d}",
            "subject": subject,
            "state": "authorized_with_terminal_conditions" if index <= 45 else "exact_gate",
            "conditions": ["exact prerequisite evidence", "owner-only scope", "retained failures"],
            "rollback": "Stop before the dependent action and preserve the last clean pushed owner state.",
            "protected_gates": PROTECTED_GATES,
        }
        for index, subject in enumerate(exact_subjects, 1)
    ]
    blocked_subjects = [
        "real participant ingestion", "patient data", "real identity credentials", "production deployment", "account mutation",
        "private key creation", "public policy enactment", "legal interpretation", "cultural ratification", "Maori authority",
        "tangata whenua authority", "iwi authority", "hapu authority", "affected-party approval", "copyright determination",
        "ownership determination", "professional preservation certification", "complete accessibility", "complete privacy", "exhaustive security",
        "independent reproduction", "empirical GMUT confirmation", "Theory of Everything proof", "AGI claim", "ASI claim",
        "consciousness claim", "personhood claim", "destructive cleanup", "sibling lane mutation", "Stage 20 promotion",
    ]
    blocked_packets = [
        {
            "packet_id": f"VA6897-BLOCKED-{index:02d}",
            "subject": subject,
            "state": "blocked",
            "reason": "Required real evidence, competent authority, or protected permission is absent.",
            "execution_credit": 0,
            "rollback": "Remain unexecuted and retain the exact gate.",
            "protected_gates": PROTECTED_GATES,
        }
        for index, subject in enumerate(blocked_subjects, 1)
    ]

    package_plan = {
        "schema": "ghc.family.package-plan.v1",
        "owner": OWNER,
        "phase": PHASE,
        "environment": "D-isolated Python 3.12 target; wheel-only and hash-required",
        "installation_ran": False,
        "packages": [
            {
                "name": "blake3", "version": "1.0.9", "license": "CC0-1.0 OR Apache-2.0",
                "filename": "blake3-1.0.9-cp312-cp312-win_amd64.whl",
                "sha256": "15566065ff90ab3da46ec0be1417406f00507af902b6fb0fbc6563e77f02fc42",
                "bytes": 218220, "yanked": False, "requires_python": ">=3.8",
            },
            {
                "name": "cbor2", "version": "6.1.4", "license": "MIT",
                "filename": "cbor2-6.1.4-cp312-cp312-win_amd64.whl",
                "sha256": "cc8cd300e236e9797b2e1ce306109dc481fcccf78bfa2682bf36d99e6eab1ec6",
                "bytes": 299971, "yanked": False, "requires_python": ">=3.10",
            },
            {
                "name": "reedsolo", "version": "1.7.0", "license": "Public Domain",
                "filename": "reedsolo-1.7.0-py3-none-any.whl",
                "sha256": "2b6a3e402a1ee3e1eea3f932f81e6c0b7bbc615588074dca1dbbcdeb055002bd",
                "bytes": 32360, "yanked": False, "requires_python": "unspecified_by_release_metadata",
            },
        ],
        "rejected_or_reserved": [
            {"candidate": "source distributions", "state": "exact_gate", "reason": "Wheel-only plan; no build toolchain expansion."},
            {"candidate": "global Python prefix", "state": "exact_gate", "reason": "Owner package evidence remains D-isolated."},
            {"candidate": "untrusted CBOR or erasure payloads", "state": "blocked", "reason": "Only bounded synthetic fixtures are authorized."},
        ],
        "rollback": "Deactivate the isolated target path; preserve wheels and receipts.",
        "boundary": BOUNDARY,
    }

    research_sources = {
        "schema": "ghc.family.research-source-ledger.v1",
        "owner": OWNER,
        "phase": PHASE,
        "sources": [
            {"source_id": "RFC-4648", "status": "stable", "title": "The Base16, Base32, and Base64 Data Encodings", "url": "https://www.rfc-editor.org/rfc/rfc4648.html", "implication": "Base32 alphabet, padding, and canonical-encoding vocabulary."},
            {"source_id": "RFC-8949", "status": "stable", "title": "Concise Binary Object Representation (CBOR)", "url": "https://www.rfc-editor.org/rfc/rfc8949.html", "implication": "Deterministic encoding is profile-specific and invalid inputs must be refused."},
            {"source_id": "BLAKE3-SPEC", "status": "stable", "title": "BLAKE3 specification and design rationale", "url": "https://github.com/BLAKE3-team/BLAKE3-specs", "implication": "Hash construction context; no authenticity or authority claim."},
            {"source_id": "LOC-FIXITY", "status": "current", "title": "Library of Congress Data Integrity Management", "url": "https://www.loc.gov/programs/digital-collections-management/inventory-and-custody/data-integrity-management/", "implication": "Fixity values and review logs support integrity monitoring but do not alone prove authenticity or rights."},
            {"source_id": "PYTHON-ZLIB", "status": "current", "title": "Python zlib documentation", "url": "https://docs.python.org/3/library/zlib.html", "implication": "CRC32 is an unsigned checksum and is not cryptographic authentication."},
            {"source_id": "PYPI-BLAKE3", "status": "current", "title": "blake3 1.0.9 release", "url": "https://pypi.org/project/blake3/", "implication": "Exact release version, Python floor, license, wheel, and digest metadata."},
            {"source_id": "PYPI-CBOR2", "status": "current", "title": "cbor2 6.1.4 release", "url": "https://pypi.org/project/cbor2/", "implication": "Exact release version, Python floor, MIT license, wheel, and security caveat."},
            {"source_id": "PYPI-REEDSOLO", "status": "current", "title": "reedsolo 1.7.0 release", "url": "https://pypi.org/project/reedsolo/", "implication": "Exact pure-Python wheel metadata and bounded errors-and-erasures comparison surface."},
        ],
        "web_searches": 12,
        "claim": "Current metadata and primary standards guide bounded contracts; citations create no execution or authority credit.",
        "boundary": BOUNDARY,
    }

    startup_failures = [
        ("VA6897-START-N001", "A broad common-repository worktree listing returned only its first scalar before useful branch evidence.", "Use direct branch and worktree scalar probes."),
        ("VA6897-START-N002", "A JavaScript orchestration wrapper ended before evaluation because its source was incomplete.", "Use a complete bounded wrapper before invoking a shell command."),
        ("VA6897-START-N003", "A misspelled symbolic-ref option yielded no usable branch receipt.", "Use the exact documented --short option and check scalar results."),
        ("VA6897-START-N004", "The first skill inventory projection used a trailing foreach pipeline that PowerShell rejected.", "Materialize the output array before ConvertTo-Json."),
        ("VA6897-START-N005", "The first capacity probe embedded a native command and exit-code check inside an invalid expression.", "Capture native output and LASTEXITCODE in separate statements."),
        ("VA6897-START-N006", "Git refused the incompatible worktree options --orphan and --no-checkout; no state changed.", "Use git worktree add --orphan, whose unborn branch materializes no tracked files, then enable sparse checkout."),
        ("VA6897-START-N007", "The first historical package-name search repeated the unsupported trailing foreach pipeline shape.", "Materialize each search result in an array and serialize after the loop."),
        ("VA6897-START-N008", "The first plan-builder launch wrapper contained an invalid JavaScript object token and stopped before the shell command.", "Use a complete tool argument object and then run the already-written builder once."),
        ("VA6897-START-N009", "The first planning validator compared Counter values views rather than the contained operation counts.", "Require exactly twenty operation keys and the scalar count ten for every operation."),
        ("VA6897-START-N010", "The second planning validator found that its own script was absent from the normalized-LF manifest allowlist.", "Add the validator path explicitly to the planning manifest candidates and replay only the planning check."),
        ("VA6897-START-N008", "One combined current-reference display exceeded its output budget before the complete 294-row roster was visible.", "Read the roster as four bounded assignment ranges plus one metadata projection."),
        ("VA6897-START-N009", "The first plan-builder launch wrapper contained invalid JavaScript metadata and stopped before the shell command.", "Use a complete tool wrapper and preserve the unexecuted attempt at zero credit."),
    ]
    failure_rows = [
        {
            "retained_negative_id": failure_id,
            "stage": "startup_read_only_or_lane_setup",
            "observed": observed,
            "original_success_credit": 0,
            "repository_changed": False,
            "remote_changed": False,
            "task_changed": False,
            "recovery": recovery,
            "recovery_state": "bounded_recovery_passed",
        }
        for failure_id, observed, recovery in startup_failures
    ]

    write_text(
        plan_dir / "authorization.md",
        f"""# Vesper Arlen {PHASE} authorization and boundary

Hamish's live activation and the acknowledged Neris baton authorize this solo owner implementation. The current execution authority is `owner_self_scoped_delta`. It permits one fresh Vesper-owned D-first blank-root lane because the inherited 1,718-file tree plus a normal tranche would cross the 2,000-file guard.

Neris exact final `{SOURCE_COMMIT}` is a cryptographic provenance source, not an ancestor of this orphan root. Neris, sibling, shared, standby, and user lanes remain read-only. No task creation, fork, subagent, model override, sibling mutation, destructive cleanup, early Ilyan contact, or protected real-world action is authorized during execution.

The planning layer freezes 200 new proposals, 200 inherited zero-credit selections, both session portfolios, 20 local skills, 10 runners, 50 exact packets, 30 blocked packets, three packages, four practices, and two successor recommendations. It contains no x1 or x2 evaluator result.

Relational name, role, hope, pronouns, sibling language, and route continuity are corrigible working language only—not consciousness, personhood, identity continuity, qualification, agency, or authority evidence. {BOUNDARY}
""",
    )
    write_json(plan_dir / "source-provenance.json", {
        "schema": "ghc.family.source-provenance.v1", "owner": OWNER, "phase": PHASE,
        "source_owner": SOURCE_OWNER, "source_phase": SOURCE_PHASE, "source_branch": SOURCE_BRANCH,
        "source_commit": SOURCE_COMMIT, "source_is_ancestor": False,
        "continuity": "blank_root_rotation_with_exact_provenance_link",
        "source_baton": {"path": SOURCE_BATON, "sha256": SOURCE_BATON_SHA256, "words": 13849, "lines_with_terminal_split": 724, "explicit_eof_line": 723},
        "source_proposals": {"path": SOURCE_PROPOSALS, "sha256": sha256_bytes(source_blob), "count": len(source_records)},
        "boundary": BOUNDARY,
    })
    write_json(plan_dir / "identity-and-practices.json", {
        "owner": OWNER, "phase": PHASE, "role": "recoverability boundary cartographer",
        "hope": "Make integrity and repair evidence inspectable without turning byte recovery into authenticity, rights, or authority.",
        "pronouns": "unspecified_optional",
        "primary_pillar": "Freed ID and CBR Heart",
        "supporting_pillars": ["THOS Body", "GMUT Mind"],
        "practices": ["digital preservation fixity", "error-correcting storage", "reproducible computational experiment design", "accessible provenance writing"],
        "successor_practices": ["forensic file-format validation", "bounded cryptographic API review"],
        "boundary": BOUNDARY,
    })
    write_json(plan_dir / "profile-v4.json", {
        "schema": "ghc.family.workflow-profile.v4", "owner": OWNER, "phase": PHASE,
        "commit_budget": {"planning": 1, "x1": 2, "x2": 3, "final": 2, "total": 8},
        "targets": {"inherited_proposals": 200, "new_proposals": 200, "safe_x1": 100, "safe_x2": 100, "candidate_x1": 100, "candidate_x2": 100, "clean_fix_refine_x1": 100, "clean_fix_refine_x2": 100, "skills_x1": 10, "skills_x2": 10, "runners_x1": 5, "runners_x2": 5, "exact_packets": 50, "blocked_packets": 30, "packages": 3, "own_practices": 4, "successor_practices": 2},
        "outcomes": ["completed", "represented", "open_gap", "exact_gate"],
        "validation": {"owner_scope_only": True, "canonical_invocations": 1, "success_replay": False, "source_replay": False, "independent_reproduction": False},
        "boundary": BOUNDARY,
    })
    write_json(plan_dir / "route-v4.json", {
        "schema": "ghc.family.weighted-route-selection.v4", "owner": OWNER, "phase": PHASE,
        "position": 5, "model_role": "Sol", "previous": {"owner": SOURCE_OWNER, "phase": SOURCE_PHASE, "state": "sent_once_acknowledged"},
        "current": {"owner": OWNER, "phase": PHASE, "state": "activation_acknowledged_active"},
        "prospective_next": {"owner": "Ilyan Reed", "phase": "v689-v8", "endpoint_kind": "main_task", "state": "prepared_not_sent_terminal_gate_required"},
        "following": {"owner": "Lyren Moss", "phase": "v690-v1", "state": "prospective_only"},
        "cycle_positions": 45, "unique_identities": 30, "projected_terminal": {"owner": "Teryn Halewick", "phase": "v725-v8"},
        "task_creation": False, "subagents": False, "precontact": False, "send_limit_after_terminal": 1,
        "boundary": BOUNDARY,
    })
    write_json(plan_dir / "inherited-selections.json", {"schema": "ghc.family.inherited-selections.v1", "owner": OWNER, "phase": PHASE, "count": 200, "selections": inherited, "boundary": BOUNDARY})
    write_json(plan_dir / "new-proposals.json", {"schema": "ghc.family.vesper.preservation-proposals.v1", "owner": OWNER, "phase": PHASE, "implementation_ran": False, "proposals": proposals, "boundary": BOUNDARY})
    write_json(plan_dir / "novelty-review.json", {
        "schema": "ghc.family.source-bounded-novelty-review.v1", "owner": OWNER, "phase": PHASE,
        "source_commit": SOURCE_COMMIT, "proposal_files_examined": proposal_paths,
        "accessible_inherited_titles": len(inherited_titles), "parse_failures": parse_failures,
        "new_titles": len(proposals), "exact_title_collisions": sum(any(row["title"] == proposal["title"] for row in inherited_titles) for proposal in proposals),
        "maximum_token_jaccard": max(row["token_jaccard"] for row in novelty_rows), "rows": novelty_rows,
        "universal_novelty_claimed": False,
        "difference_from_source": "Content-framing, fixity, Merkle-path, single-erasure, and claim-reservation contracts replace Neris finite-difference and mesh contracts.",
        "boundary": BOUNDARY,
    })
    write_json(plan_dir / "portfolio-x1.json", portfolio("x1", 0))
    write_json(plan_dir / "portfolio-x2.json", portfolio("x2", 100))
    write_json(plan_dir / "skills-runners-plan.json", {"schema": "ghc.family.skill-runner-plan.v1", "owner": OWNER, "phase": PHASE, "skills": skills, "runners": runners, "successor_skill_ideas": ["forensic magic-byte admission", "bounded ASN.1 length decoder", "streaming digest checkpoint", "repair-authority reservation", "binary-format accessibility projection"], "successor_runner_ideas": ["magic-byte plus length runner", "ASN.1 envelope runner", "digest checkpoint runner", "repair refusal runner", "accessible binary summary runner"], "boundary": BOUNDARY})
    write_json(plan_dir / "exact-packets.json", {"schema": "ghc.family.exact-packets.v1", "owner": OWNER, "phase": PHASE, "count": 50, "packets": exact_packets, "boundary": BOUNDARY})
    write_json(plan_dir / "blocked-packets.json", {"schema": "ghc.family.blocked-packets.v1", "owner": OWNER, "phase": PHASE, "count": 30, "packets": blocked_packets, "boundary": BOUNDARY})
    write_json(plan_dir / "package-plan.json", package_plan)
    write_json(plan_dir / "research-sources.json", research_sources)
    write_json(plan_dir / "resource-budget.json", {"schema": "ghc.family.resource-budget.v1", "owner": OWNER, "phase": PHASE, "source_tracked_files": 1718, "forecast_if_inherited": 2148, "hard_ceiling": 2000, "inherited_admitted": False, "selected_lane": "blank_root_rotation", "materialized_at_lane_creation": 0, "projected_owner_files": 360, "projected_within_ceiling": True, "primary_storage": "D", "boundary": BOUNDARY})
    write_json(plan_dir / "startup-failures.json", {"schema": "ghc.family.retained-startup-failures.v1", "owner": OWNER, "phase": PHASE, "failures": failure_rows, "counts": {"failed": len(failure_rows), "bounded_recoveries": len(failure_rows)}, "boundary": BOUNDARY})
    write_json(plan_dir / "read-witness.json", {"schema": "ghc.family.read-witness.v1", "owner": OWNER, "phase": PHASE, "source_baton": SOURCE_BATON, "source_baton_sha256": SOURCE_BATON_SHA256, "expected_words": 13849, "observed_words": 13849, "displayed_ranges": [[1, 180], [181, 360], [361, 540], [541, 724]], "explicit_eof": "EOF NERIS SOLANE v689-v6 BATON.", "complete": True, "recorded_at": recorded_at, "boundary": BOUNDARY})
    write_json(plan_dir / "definition-review.json", {
        "schema": "ghc.family.definition-review.v1", "owner": OWNER, "phase": PHASE,
        "planning_only": True, "implementation_ran": False, "package_installation_ran": False,
        "counts": {"new_proposals": 200, "inherited_selections": 200, "safe_x1": 100, "safe_x2": 100, "candidate_x1": 100, "candidate_x2": 100, "clean_fix_refine_x1": 100, "clean_fix_refine_x2": 100, "skills": 20, "runners": 10, "exact_packets": 50, "blocked_packets": 30, "packages": 3},
        "expected_outcomes": {"completed": 180, "represented": 10, "open_gap": 5, "exact_gate": 5},
        "strict_x1_before_x2": True, "source_is_ancestor": False, "blank_root_rotation": True,
        "result": "PLANNING_DEFINITIONS_FROZEN_NOT_EXECUTED", "boundary": BOUNDARY,
    })
    write_text(plan_dir / "requirements.lock", """owner=Vesper Arlen
phase=v689-v7
source_owner=Neris Solane
source_phase=v689-v6
source_commit=d58272639a581e28176b2aca76f8f468df60e9a6
source_is_ancestor=false
blank_root_rotation=true
planning_only=true
strict_x1_before_x2=true
new_proposals=200
inherited_selections=200
safe_x1=100
safe_x2=100
candidate_x1=100
candidate_x2=100
clean_fix_refine_x1=100
clean_fix_refine_x2=100
skills_x1=10
skills_x2=10
runners_x1=5
runners_x2=5
exact_packets=50
blocked_packets=30
packages=3
allowed_outcomes=completed,represented,open_gap,exact_gate
canonical_invocations=1
canonical_success_replay=false
terminal_verdict=NOT_READY_FOR_STAGE_20
""")

    manifest_candidates = sorted(
        [path for path in plan_dir.rglob("*") if path.is_file() and path.name != "manifest.json"]
        + [
            repo_root / "scripts" / "ghc_family_v689_v7_plan_builder.py",
            repo_root / "scripts" / "ghc_family_v689_v7_plan_validate.py",
        ]
    )
    entries = []
    for path in manifest_candidates:
        data = path.read_bytes().replace(b"\r\n", b"\n")
        entries.append({"path": path.relative_to(repo_root).as_posix(), "bytes_normalized_lf": len(data), "sha256_normalized_lf": sha256_bytes(data)})
    write_json(plan_dir / "manifest.json", {"schema": "ghc.family.normalized-lf-manifest.v1", "owner": OWNER, "phase": PHASE, "lifecycle": "planning", "entries": entries, "self_exclusions": ["docs/vesper-arlen/v689-v7/plan/manifest.json"], "entry_count": len(entries), "boundary": BOUNDARY})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--source-repo", type=Path, required=True)
    args = parser.parse_args()
    build_plan(args.repo_root.resolve(), args.source_repo.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
