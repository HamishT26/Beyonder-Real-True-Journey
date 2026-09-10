"""Bounded package smokes for the isolated Lyren v690-v1 D environment."""

from __future__ import annotations

import argparse
import copy
import importlib.metadata
import json
from pathlib import Path

from bitstring import Bits
from crccheck.crc import Crc32
from reedsolo import ReedSolomonError, RSCodec


def run() -> dict[str, object]:
    records: list[dict[str, object]] = []

    source_bits = "101001"
    parsed = Bits(bin=source_bits)
    records.append(
        {
            "package": "bitstring",
            "kind": "positive",
            "input": source_bits,
            "observed": {"bin": parsed.bin, "ones": parsed.count(1), "length": len(parsed)},
            "passed": parsed.bin == source_bits and parsed.count(1) == 3 and len(parsed) == 6,
        }
    )
    invalid_bits = "10x1"
    invalid_copy = copy.deepcopy(invalid_bits)
    try:
        Bits(bin=invalid_bits)
        rejected = False
        error_type = None
    except ValueError as exc:
        rejected = True
        error_type = type(exc).__name__
    records.append(
        {
            "package": "bitstring",
            "kind": "adverse",
            "input": invalid_bits,
            "input_unchanged": invalid_bits == invalid_copy,
            "observed": {"rejected": rejected, "error_type": error_type},
            "original_success_credit": 0,
            "passed": rejected and invalid_bits == invalid_copy,
        }
    )

    codec = RSCodec(8)
    message = b"Lyren"
    encoded = codec.encode(message)
    one_error = bytearray(encoded)
    one_error[1] ^= 0x07
    decoded = bytes(codec.decode(bytes(one_error))[0])
    records.append(
        {
            "package": "reedsolo",
            "kind": "positive",
            "input_hex": message.hex(),
            "observed": {"decoded_hex": decoded.hex(), "ecc_symbols": 8},
            "passed": decoded == message,
            "boundary": "One synthetic corruption under one exact codec configuration; not a channel benchmark.",
        }
    )
    too_many = bytearray(encoded)
    for index in range(5):
        too_many[index] ^= (index + 1) * 3
    try:
        codec.decode(bytes(too_many))
        rejected = False
        error_type = None
    except ReedSolomonError as exc:
        rejected = True
        error_type = type(exc).__name__
    records.append(
        {
            "package": "reedsolo",
            "kind": "adverse",
            "input_hex": bytes(too_many).hex(),
            "observed": {"rejected": rejected, "error_type": error_type},
            "original_success_credit": 0,
            "passed": rejected,
        }
    )

    standard = b"123456789"
    checksum = Crc32.calc(standard)
    records.append(
        {
            "package": "crccheck",
            "kind": "positive",
            "input_hex": standard.hex(),
            "observed": {"crc32": checksum, "hex": f"{checksum:08x}"},
            "passed": checksum == 0xCBF43926,
        }
    )
    invalid_crc_input = "not-bytes"
    try:
        Crc32.calc(invalid_crc_input)
        rejected = False
        error_type = None
    except (TypeError, ValueError) as exc:
        rejected = True
        error_type = type(exc).__name__
    records.append(
        {
            "package": "crccheck",
            "kind": "adverse",
            "input": invalid_crc_input,
            "observed": {"rejected": rejected, "error_type": error_type},
            "original_success_credit": 0,
            "passed": rejected,
        }
    )

    versions = {
        name: importlib.metadata.version(name)
        for name in ["bitarray", "bitstring", "crccheck", "reedsolo", "tibs"]
    }
    return {
        "schema": "ghc.family.lyren.package-smokes.v1",
        "versions": versions,
        "records": records,
        "passed": all(record["passed"] for record in records),
        "positive_witnesses": sum(record["kind"] == "positive" for record in records),
        "adverse_subjects": sum(record["kind"] == "adverse" for record in records),
        "boundary": "Isolated same-owner package evidence only; no exhaustive security, production, cryptographic, empirical, professional, or independent-reproduction claim.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = run()
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
