"""Bounded Lyren error-control pair 05: gf2_division_remainder, crc_remainder."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from ghc_family_error_control_x1 import run

ALLOWED=['gf2_division_remainder', 'crc_remainder']
def main():
    p=argparse.ArgumentParser();p.add_argument("--request-json");p.add_argument("--input");p.add_argument("--output");a=p.parse_args()
    if bool(a.request_json)==bool(a.input):raise SystemExit("provide exactly one request source")
    request=json.loads(a.request_json) if a.request_json else json.loads(Path(a.input).read_text(encoding="utf-8"))
    result=run(request) if request.get("operation") in ALLOWED else {"ok":False,"error":"operation_outside_pair","original_success_credit":0}
    payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if a.output:Path(a.output).write_text(payload,encoding="utf-8",newline="\n")
    else:print(payload,end="")
if __name__=="__main__":main()
