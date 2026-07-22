#!/usr/bin/env python3
"""Family-current bounded runner for Sable v652-v1: ghc_family_cruft_pack_guard.py."""
import argparse, json
import ghc_family_v652_v1_runtime as runtime

GROUP = ['V6521-P02']

def emit(payload): print(json.dumps(payload, ensure_ascii=False, sort_keys=True))
def main():
    parser=argparse.ArgumentParser(description="Offline bounded same-owner v652-v1 runner; no production or authority actions.")
    parser.add_argument("--json", action="store_true", help="Emit stable JSON.")
    sub=parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor", help="Report offline capability and boundary state.")
    runp=sub.add_parser("run", help="Run canonical bounded fixtures."); runp.add_argument("--proposal", action="append", default=[])
    insp=sub.add_parser("inspect", help="Read one canonical contract."); insp.add_argument("--proposal", required=True)
    reject=sub.add_parser("reject", help="Run one preregistered rejecting mutation."); reject.add_argument("--proposal", required=True); reject.add_argument("--dimension", choices=runtime.MUTATION_DIMENSIONS, required=True)
    args=parser.parse_args()
    if args.command=="doctor": payload={"schema":"ghc.family.v652-v1.runner-doctor.v1","runner":"ghc_family_cruft_pack_guard.py","offline":True,"auth_required":False,"network_actions":0,"group":GROUP,"ready":True}
    elif args.command=="run":
        selected=args.proposal or GROUP
        if any(pid not in GROUP for pid in selected): parser.error("proposal outside runner group")
        results=[runtime.execute(pid) for pid in selected]; payload={"schema":"ghc.family.v652-v1.runner-run.v1","runner":"ghc_family_cruft_pack_guard.py","count":len(results),"all_accepted":all(r["accepted"] for r in results),"results":results}
    elif args.command=="inspect":
        if args.proposal not in GROUP: parser.error("proposal outside runner group")
        proposal=runtime.proposal_by_id(args.proposal); payload={"schema":"ghc.family.v652-v1.runner-inspect.v1","proposal_id":args.proposal,"contract":runtime.canonical_fixture(proposal)}
    else:
        if args.proposal not in GROUP: parser.error("proposal outside runner group")
        payload={"schema":"ghc.family.v652-v1.runner-reject.v1",**runtime.rejection_witness(args.proposal,args.dimension)}
    emit(payload); return 0
if __name__=="__main__": raise SystemExit(main())
