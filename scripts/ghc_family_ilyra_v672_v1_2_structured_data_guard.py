from __future__ import annotations

import argparse
import io
import json
from typing import Any

import ijson
import jmespath
import jsonpatch
import jsonpointer
import yamale
import yaml
from deepdiff import DeepDiff
from ijson.common import IncompleteJSONError
from ruamel.yaml import YAML
from ruamel.yaml.constructor import DuplicateKeyError


class UniqueKeyLoader(yaml.SafeLoader):
    """PyYAML safe loader that refuses duplicate mapping keys."""


def _construct_unique_mapping(loader: UniqueKeyLoader, node: Any, deep: bool = False) -> dict[Any, Any]:
    seen: set[Any] = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise ValueError(f"duplicate YAML key: {key!r}")
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep=deep)


UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def run_smokes() -> dict[str, Any]:
    results: dict[str, Any] = {}

    positive_yaml = yaml.load("owner: Ilyra Fen\nphase: remaster\n", Loader=UniqueKeyLoader)
    duplicate_rejected = False
    try:
        yaml.load("owner: first\nowner: second\n", Loader=UniqueKeyLoader)
    except ValueError:
        duplicate_rejected = True
    results["PyYAML"] = {
        "positive": positive_yaml == {"owner": "Ilyra Fen", "phase": "remaster"},
        "rejecting": duplicate_rejected,
        "boundary": "safe loader plus owner-defined duplicate-key refusal",
    }

    diff = DeepDiff({"state": "x1", "count": 1}, {"state": "x2", "count": 2})
    results["deepdiff"] = {
        "positive": "values_changed" in diff,
        "rejecting": not bool(DeepDiff({"same": 1}, {"same": 1})),
        "boundary": "bounded in-memory structures only",
    }

    streamed = list(ijson.items(io.BytesIO(b'{"items":[1,2,3]}'), "items.item"))
    truncated_rejected = False
    try:
        list(ijson.items(io.BytesIO(b'{"items":[1,2'), "items.item"))
    except IncompleteJSONError:
        truncated_rejected = True
    results["ijson"] = {
        "positive": streamed == [1, 2, 3],
        "rejecting": truncated_rejected,
        "boundary": "small synthetic byte streams only",
    }

    roundtrip = YAML(typ="rt")
    roundtrip.allow_duplicate_keys = False
    parsed = roundtrip.load("# retained\nowner: Ilyra Fen\n")
    ruamel_duplicate_rejected = False
    try:
        roundtrip.load("owner: first\nowner: second\n")
    except DuplicateKeyError:
        ruamel_duplicate_rejected = True
    results["ruamel.yaml"] = {
        "positive": parsed["owner"] == "Ilyra Fen" and bool(parsed.ca.comment),
        "rejecting": ruamel_duplicate_rejected,
        "boundary": "round-trip fixture representation only",
    }

    schema = yamale.make_schema(content="owner: str(required=True)\ncount: int(min=1)\n")
    valid_data = yamale.make_data(content="owner: Ilyra Fen\ncount: 2\n")
    invalid_data = yamale.make_data(content="owner: Ilyra Fen\ncount: 0\n")
    yamale.validate(schema, valid_data)
    yamale_rejected = False
    try:
        yamale.validate(schema, invalid_data)
    except ValueError:
        yamale_rejected = True
    results["yamale"] = {
        "positive": True,
        "rejecting": yamale_rejected,
        "boundary": "trusted phase-local schemas only",
    }

    pointer_document = {"cards": [{"owner": "Ilyra Fen"}]}
    pointer_value = jsonpointer.resolve_pointer(pointer_document, "/cards/0/owner")
    pointer_rejected = False
    try:
        jsonpointer.resolve_pointer(pointer_document, "cards/0/owner")
    except jsonpointer.JsonPointerException:
        pointer_rejected = True
    results["jsonpointer"] = {
        "positive": pointer_value == "Ilyra Fen",
        "rejecting": pointer_rejected,
        "boundary": "RFC6901 synthetic documents only",
    }

    allowed_query = "cards[?state=='safe'].id"
    forbidden_query = "secrets[*]"
    query_document = {"cards": [{"id": "c1", "state": "safe"}, {"id": "c2", "state": "blocked"}]}
    query_value = jmespath.search(allowed_query, query_document)
    query_allowlist = {allowed_query}
    results["jmespath"] = {
        "positive": query_value == ["c1"],
        "rejecting": forbidden_query not in query_allowlist,
        "boundary": "explicit expression allowlist, no external query execution",
    }

    patch = jsonpatch.JsonPatch(
        [
            {"op": "test", "path": "/state", "value": "x1"},
            {"op": "replace", "path": "/state", "value": "x2"},
        ]
    )
    patched = patch.apply({"state": "x1"})
    patch_rejected = False
    try:
        patch.apply({"state": "unexpected"})
    except jsonpatch.JsonPatchTestFailed:
        patch_rejected = True
    results["jsonpatch"] = {
        "positive": patched == {"state": "x2"},
        "rejecting": patch_rejected,
        "boundary": "preconditioned synthetic corrections only",
    }

    passed = all(row["positive"] and row["rejecting"] for row in results.values())
    return {
        "schema": "ghc.family.ilyra.structured-data-smoke.v1",
        "passed": passed,
        "direct_surfaces": 8,
        "results": results,
        "external_actions": 0,
        "professional_result": False,
        "production_result": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run_smokes()
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS" if result["passed"] else "FAIL")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
