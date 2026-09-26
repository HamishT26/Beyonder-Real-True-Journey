from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path

def canonical(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")
def evaluate(record):
    return {"category":"lifecycle","schema_present":isinstance(record.get("schema"),str),"external_actions":0,"authority_actions":0,"record_sha256":hashlib.sha256(canonical(record)).hexdigest(),"boundary":"Finite synthetic workflow assistance only. No live service, external action, empirical, production, professional, legal, cultural, affected-party or Maori authority, independent reproduction, complete privacy/accessibility/security, AGI/ASI, consciousness/personhood, Theory-of-Everything, canon or Stage 20 claim. NOT_READY_FOR_STAGE_20."}
def main():
    parser=argparse.ArgumentParser();parser.add_argument("--input");parser.add_argument("--self-test",action="store_true");args=parser.parse_args()
    if args.self_test:record={"schema":"ghc.family.event-workflow.runner-smoke.v1","category":"lifecycle"}
    elif args.input:record=json.loads(Path(args.input).read_text(encoding="utf-8"))
    else:parser.error("provide --self-test or --input")
    result=evaluate(record);print(json.dumps(result));raise SystemExit(0 if result["schema_present"] else 1)
if __name__=="__main__":main()
