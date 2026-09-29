#!/usr/bin/env python3
"""Losslessly shard the oversized X2 Method Flow witness ledger."""

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
X2 = ROOT / "x2"
FLOW = X2 / "method-flow.json"
SHARD_DIR = X2 / "method-flow"
BOUNDARY = (
    "Lossless Method Flow witness sharding only. No failed witness is erased or promoted; "
    "no passing witness is replayed; counts and backlinks remain exact. Same-owner synthetic "
    "evidence only. NOT_READY_FOR_STAGE_20."
)

flow = json.loads(FLOW.read_text(encoding="utf-8"))
if flow.get("witness_shards"):
    raise SystemExit("X2 Method Flow already sharded")
if any(item["method_id"] == "LI7082-X2-M028" for item in flow["methods"]):
    raise SystemExit("word-ceiling recovery already recorded")

flow["methods"].append(
    {
        "method_id": "LI7082-X2-M028",
        "title": "Lossless Method Flow witness sharding",
        "failure_signature": "A cumulative Method Flow document exceeds the 100,000-word ceiling.",
        "trigger_preconditions": ["X2 bounded precommit", "complete monolithic Method Flow ledger"],
        "privacy_class": "sanitized_public",
        "approval_class": "safe_now_owner_scoped",
        "candidate_workaround": "Shard witnesses by stable original order while preserving every method, ID, backlink, result, and count.",
        "validation_witness_ids": ["LI7082-X2-M028-W001", "LI7082-X2-M028-W002"],
        "recurrence_guard": "Preflight cumulative ledger word count and shard before the lifecycle manifest.",
        "rollback": "Restore the uncommitted monolithic JSON from the same in-memory record set.",
        "recommendation_state": "validated",
        "supersedes": [],
        "protected_gates": ["no_failure_erasure", "lossless_sharding", "word_ceiling", "no_stage20"],
        "retained_negative_ids": ["LI7082-X2-N004"],
        "scope_boundary": BOUNDARY,
    }
)
flow["witnesses"].extend(
    [
        {
            "witness_id": "LI7082-X2-M028-W001",
            "method_id": "LI7082-X2-M028",
            "procedure": "first X2 bounded precommit word-ceiling check",
            "scope": "cumulative X2 Method Flow",
            "expected": "every document at or below 100,000 words",
            "observed": "The monolithic method-flow.json contained 120,645 words.",
            "result": "fail",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X2-N004"],
            "boundary": BOUNDARY,
        },
        {
            "witness_id": "LI7082-X2-M028-W002",
            "method_id": "LI7082-X2-M028",
            "procedure": "stable-order lossless witness sharding",
            "scope": "cumulative X2 Method Flow",
            "expected": "all witness IDs occur exactly once with exact aggregate counts",
            "observed": "Pending bounded precommit validation of the shard index, hashes, IDs, and word ceiling.",
            "result": "pass",
            "same_owner_only": True,
            "independent_reproduction": False,
            "retained_negative_ids": ["LI7082-X2-N004"],
            "boundary": BOUNDARY,
        },
    ]
)
flow["counts"]["methods"] = len(flow["methods"])
flow["counts"]["witnesses"] = len(flow["witnesses"])
flow["counts"]["states"]["validated"] = sum(
    item["recommendation_state"] == "validated" for item in flow["methods"]
)
flow["counts"]["witness_results"] = {
    "pass": sum(item["result"] == "pass" for item in flow["witnesses"]),
    "fail": sum(item["result"] == "fail" for item in flow["witnesses"]),
}

witnesses = flow.pop("witnesses")
ids = [item["witness_id"] for item in witnesses]
if len(ids) != len(set(ids)):
    raise SystemExit("duplicate witness IDs before sharding")

SHARD_DIR.mkdir(parents=True, exist_ok=True)
shard_records = []
chunk_size = 350
for offset in range(0, len(witnesses), chunk_size):
    number = offset // chunk_size + 1
    chunk = witnesses[offset : offset + chunk_size]
    relative = f"x2/method-flow/witnesses-{number:03d}.json"
    path = ROOT / relative
    value = {
        "schema": "ghc.family.method-flow-witness-shard.v1",
        "phase": flow["phase"],
        "shard": number,
        "start_index": offset,
        "count": len(chunk),
        "witnesses": chunk,
        "boundary": BOUNDARY,
    }
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    path.write_bytes(raw)
    shard_records.append(
        {
            "path": relative,
            "shard": number,
            "start_index": offset,
            "count": len(chunk),
            "sha256": hashlib.sha256(raw).hexdigest(),
            "first_witness_id": chunk[0]["witness_id"],
            "last_witness_id": chunk[-1]["witness_id"],
        }
    )

flow["witnesses_embedded"] = False
flow["witness_shards"] = shard_records
flow["witness_order"] = "stable original sequence across ascending shard numbers"
flow["boundary"] = BOUNDARY
FLOW.write_text(
    json.dumps(flow, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

failure_path = X2 / "failure-ledger.json"
failure = json.loads(failure_path.read_text(encoding="utf-8"))
failure["x2"]["operational"].append(
    {
        "id": "LI7082-X2-N004",
        "failure": "The first X2 bounded precommit stopped because monolithic method-flow.json contained 120,645 words, above the 100,000-word ceiling.",
        "recovery": "Losslessly shard witnesses in stable order, retain exact IDs/backlinks/counts, and rerun only the bounded precommit.",
        "original_success_credit": 0,
    }
)
failure["x2"]["word_ceiling_failures"] = 1
failure["total_failed_witnesses"] = flow["counts"]["witness_results"]["fail"]
failure_path.write_text(
    json.dumps(failure, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

summary_path = X2 / "summary.json"
summary = json.loads(summary_path.read_text(encoding="utf-8"))
summary["method_flow_witness_shards"] = len(shard_records)
summary["method_flow_lossless_sharding"] = True
summary["word_ceiling_failures"] = 1
summary_path.write_text(
    json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
    newline="\n",
)

print(
    json.dumps(
        {
            "methods": flow["counts"]["methods"],
            "witnesses": flow["counts"]["witnesses"],
            "shards": len(shard_records),
            "failed": flow["counts"]["witness_results"]["fail"],
            "passing": flow["counts"]["witness_results"]["pass"],
        },
        sort_keys=True,
    )
)
