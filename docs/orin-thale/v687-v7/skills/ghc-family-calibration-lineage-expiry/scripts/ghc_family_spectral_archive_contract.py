#!/usr/bin/env python3
"""Finite synthetic spectral archive contract engine."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

OPERATIONS = ['spectral_axis_monotonicity', 'spectral_unit_roundtrip', 'flux_missingness_boundary', 'spectral_bin_topology', 'calibration_lineage_expiry', 'spectral_segment_fixity', 'uncertainty_covariance_shape', 'provenance_frontier', 'accessible_spectrum_summary', 'release_authority_reservation']

def disposition(ordinal):
    if ordinal <= 125: return "completed"
    if ordinal <= 164: return "represented"
    if ordinal <= 184: return "open_gap"
    return "exact_gate"

def evaluate(payload):
    if not isinstance(payload, dict):
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"INVALID_PAYLOAD","source_preserved":True}
    operation=payload.get("operation"); ordinal=payload.get("ordinal")
    if operation not in OPERATIONS:
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"UNKNOWN_OPERATION","source_preserved":True}
    if not isinstance(ordinal,int) or isinstance(ordinal,bool) or not 1 <= ordinal <= 200:
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"INVALID_ORDINAL","source_preserved":True}
    if payload.get("source_kind") != "synthetic" or payload.get("request") != "inspect" or payload.get("retained") is not True:
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"INPUT_BOUNDARY","source_preserved":True}
    expected_id=f"synthetic-{operation}-{((ordinal-1)%20)+1:02d}"
    if payload.get("record_id") != expected_id:
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"PROVENANCE_ID_MISMATCH","source_preserved":True}
    outcome=disposition(ordinal)
    if outcome == "open_gap":
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"MISSING_EXTERNAL_EVIDENCE","source_preserved":True}
    if outcome == "exact_gate":
        return {"decision":"HOLD","details":None,"external_credit":False,"reason":"COMPETENT_AUTHORITY_REQUIRED","source_preserved":True}
    return {"decision":"BOUNDED_VIEW","details":{"operation":operation,"ordinal":ordinal,"representation_only":outcome=="represented","empirical_established":False,"professional_authority":False,"normalized_value":f"{ordinal}/{ordinal+1}"},"external_credit":False,"reason":None,"source_preserved":True}

def strict_load(path):
    def hook(pairs):
        out={}
        for key,value in pairs:
            if key in out: raise ValueError("duplicate key")
            out[key]=value
        return out
    return json.loads(Path(path).read_text(encoding="utf-8"),object_pairs_hook=hook,parse_constant=lambda value: (_ for _ in ()).throw(ValueError("nonfinite")))

def cli(allowed=None):
    ap=argparse.ArgumentParser(); ap.add_argument("--input",required=True); ap.add_argument("--output"); a=ap.parse_args()
    payload=strict_load(a.input)
    if allowed is not None and payload.get("operation") not in allowed: raise SystemExit("operation outside runner contract")
    result=evaluate(payload); text=json.dumps(result,sort_keys=True,ensure_ascii=False,allow_nan=False)+"\n"
    if a.output: Path(a.output).write_text(text,encoding="utf-8",newline="\n")
    else: print(text,end="")

if __name__ == "__main__": cli()
