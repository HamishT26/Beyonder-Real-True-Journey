"""Portable owner-scoped wrapper for unicode_scalar, glyph_name."""
from __future__ import annotations
import json,sys
from ghc_family_font_evidence_core import ContractError,bad,evaluate,_strict_loads

ALLOWED=['unicode_scalar', 'glyph_name']

def main():
    raw=sys.stdin.buffer.read()
    try:
        payload=_strict_loads(raw)
        if not isinstance(payload,dict) or payload.get("operation") not in ALLOWED:
            result=bad("OPERATION_SCOPE")
        else:
            result=evaluate(payload)
    except ContractError as exc:
        result=bad(str(exc))
    sys.stdout.write(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=True)+"\n")

if __name__=="__main__":main()
