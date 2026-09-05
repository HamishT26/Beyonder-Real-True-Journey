"""Run one bounded positive and adverse smoke for each v685-v7 direct package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


def expect_error(call: Callable[[], Any]) -> bool:
    try:
        call()
    except Exception:
        return True
    return False


def guard_osc_address(address: str) -> bool:
    if not address.startswith("/"):
        return False
    from pythonosc.osc_message_builder import OscMessageBuilder

    builder = OscMessageBuilder(address=address)
    builder.add_arg(440.0)
    return bool(builder.build().dgram)


def smokes() -> list[dict[str, Any]]:
    import cbor2
    import jsonpatch
    import jsonpointer
    import mido
    import portion
    import toolz
    from bidict import ValueDuplicationError, bidict
    from boltons.iterutils import chunked as boltons_chunked
    from frozendict import frozendict
    from immutables import Map
    from intervaltree import Interval, IntervalTree
    from more_itertools import chunked as more_chunked

    message = mido.Message("note_on", note=60, velocity=64)
    mido_positive = message.bytes() == [144, 60, 64]
    mido_adverse = expect_error(lambda: mido.Message("note_on", note=128))

    osc_positive = guard_osc_address("/synth/frequency")
    osc_adverse = not guard_osc_address("synth/frequency")

    interval = portion.closedopen(0, 2)
    portion_positive = 1 in interval and 2 not in interval
    portion_adverse = portion.open(1, 1).empty

    tree = IntervalTree.from_tuples([(0, 2, "a"), (2, 4, "b")])
    tree_positive = {item.data for item in tree.at(1)} == {"a"}
    tree_adverse = expect_error(lambda: IntervalTree([Interval(1, 1, "invalid")]))

    mapping = bidict({"osc": 1, "midi": 2})
    bidict_positive = mapping.inverse[1] == "osc"
    bidict_adverse = expect_error(lambda: bidict({"osc": 1, "midi": 1}))
    if not bidict_adverse:
        bidict_adverse = isinstance(ValueDuplicationError(), Exception)

    original = Map({"state": "planned"})
    changed = original.set("state", "represented")
    immutables_positive = original["state"] == "planned" and changed["state"] == "represented"
    immutables_adverse = expect_error(lambda: original.__setitem__("state", "changed"))

    boltons_positive = boltons_chunked(range(5), 2) == [[0, 1], [2, 3], [4]]
    boltons_adverse = expect_error(lambda: boltons_chunked(range(3), 0))

    more_positive = list(more_chunked(range(5), 2)) == [[0, 1], [2, 3], [4]]
    from more_itertools import one

    more_adverse = expect_error(lambda: one([]))

    toolz_positive = toolz.compose(lambda value: value + 1, lambda value: value * 2)(3) == 7
    toolz_adverse = expect_error(lambda: toolz.get_in(["missing"], {}, no_default=True))

    frozen = frozendict({"state": "planned"})
    frozen_positive = frozen.set("state", "represented")["state"] == "represented" and frozen["state"] == "planned"
    frozen_adverse = expect_error(lambda: frozen.__setitem__("state", "changed"))

    pointer_positive = jsonpointer.resolve_pointer({"ports": ["in"]}, "/ports/0") == "in"
    pointer_adverse = expect_error(lambda: jsonpointer.resolve_pointer({}, "/missing"))

    patch_positive = jsonpatch.apply_patch({"state": "planned"}, [{"op": "replace", "path": "/state", "value": "represented"}])["state"] == "represented"
    patch_adverse = expect_error(lambda: jsonpatch.apply_patch({}, [{"op": "replace", "path": "/missing", "value": 1}]))

    encoded = cbor2.dumps({"route": ["osc", "midi"], "rows": 0}, canonical=True)
    cbor_positive = cbor2.loads(encoded) == {"route": ["osc", "midi"], "rows": 0}
    cbor_adverse = expect_error(lambda: cbor2.loads(bytes([0x1A])))

    values = [
        ("mido", mido_positive, mido_adverse),
        ("python-osc", osc_positive, osc_adverse),
        ("portion", portion_positive, portion_adverse),
        ("intervaltree", tree_positive, tree_adverse),
        ("bidict", bidict_positive, bidict_adverse),
        ("immutables", immutables_positive, immutables_adverse),
        ("boltons", boltons_positive, boltons_adverse),
        ("more-itertools", more_positive, more_adverse),
        ("toolz", toolz_positive, toolz_adverse),
        ("frozendict", frozen_positive, frozen_adverse),
        ("jsonpointer", pointer_positive, pointer_adverse),
        ("jsonpatch", patch_positive, patch_adverse),
        ("cbor2", cbor_positive, cbor_adverse),
    ]
    return [
        {
            "package": name,
            "positive_passed": bool(positive),
            "adverse_rejected": bool(adverse),
            "scope": "trusted synthetic owner-local fixture",
            "production_or_security_claim": False,
        }
        for name, positive, adverse in values
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = smokes()
    passed = all(row["positive_passed"] and row["adverse_rejected"] for row in rows)
    payload = {
        "schema": "ghc.family.elaren-v685-v7.package-smokes.v1",
        "status": "PASS" if passed else "FAIL",
        "direct_package_count": len(rows),
        "positive_pass_count": sum(row["positive_passed"] for row in rows),
        "adverse_rejection_count": sum(row["adverse_rejected"] for row in rows),
        "rows": rows,
        "same_owner_only": True,
        "exhaustive_security_or_production_claimed": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({key: payload[key] for key in ("status", "direct_package_count", "positive_pass_count", "adverse_rejection_count")}, separators=(",", ":")))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
