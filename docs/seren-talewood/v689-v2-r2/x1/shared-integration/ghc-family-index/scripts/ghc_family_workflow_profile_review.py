"""Read-only validation of current workflow profiles and consecutive route tables."""
import argparse
import json
import sys
from pathlib import Path
from ghc_family_workflow_core import ContractError, array, integer, labels, ordinal, require, strict_json, text, cycle_assignments

RANGED=['inherited_proposals','new_proposals','safe_now_x1','safe_now_x2','candidate_x2',
        'clean_fix_refine_x1','clean_fix_refine_x2','skills_x1','skills_x2','runners_x1','runners_x2']

def validate(profile,route):
    try:
        require(type(profile) is dict and type(route) is dict,'root_shape')
        require(profile.get('schema')=='ghc.family.workflow-profile.v3','profile_schema')
        require(route.get('schema')=='ghc.family.thirty-seat-route.v3','route_schema')
        require(route.get('user_confirmed_normalization') is True,'unconfirmed_route')
        cycle=labels(route.get('cycle'),30);require(len(cycle)==30,'seat_count')
        limits=profile.get('limits');targets=profile.get('phase_targets')
        require(type(limits) is dict and type(targets) is dict,'limits_shape')
        for key in RANGED:
            bounds=array(limits.get(key),2);require(len(bounds)==2,'range_shape')
            low=integer(bounds[0],0,1000);high=integer(bounds[1],0,1000)
            require(low<=high,'range_order');value=integer(targets.get(key),0,1000)
            require(low<=value<=high,'target_outside_range')
        for key in ['exact_packets','blocked_packets']:
            bounds=array(limits.get(key),2);require(len(bounds)==2,'range_shape')
            low=integer(bounds[0],0,1000);high=integer(bounds[1],0,1000)
            require(low<=targets.get(key, -1)<=high,'packet_target')
        require(integer(limits.get('owner_file_ceiling'),1,2000)<=2000,'file_ceiling')
        words=array(limits.get('baton_words'),2);require(len(words)==2,'baton_range')
        require(10000<=integer(words[0])<=integer(words[1])<=100000,'baton_range')
        require(limits.get('own_practices')==4 and limits.get('next_practices')==1,'practice_rule')
        for key in ['web_searches_x1_maximum','web_searches_x2_maximum']:integer(limits.get(key),0,500)
        require(set(labels(profile.get('outcomes')))=={'completed','represented','open_gap','exact_gate'},'outcomes')
        require(profile.get('terminal_verdict')=='NOT_READY_FOR_STAGE_20','evidence_boundary')
        require(profile.get('task_creation') is False and profile.get('subagents') is False,'endpoint_policy')
        require(profile.get('automations') is False,'automation_policy')
        first=ordinal(route.get('start'));last=ordinal(route.get('terminal'));require(last>=first,'phase_range')
        rows=array(route.get('assignments'),500);require(len(rows)==last-first+1,'assignment_count')
        require(bool(rows),'empty_route')
        expected=cycle_assignments({'cycle':cycle,'start':rows[0].get('owner'),'phase':route['start'],'count':len(rows)})
        for i,(row,wanted) in enumerate(zip(rows,expected),1):
            require(type(row) is dict,'assignment_shape')
            require(row.get('phase')==wanted['phase'] and row.get('owner')==wanted['owner'],'assignment_mismatch')
            require(type(row.get('ordinal')) is int and row['ordinal']==i,'assignment_ordinal')
            require(row.get('endpoint_kind')=='main_task' and row.get('state')=='prospective','assignment_evidence')
        outbound=route.get('current_outbound');require(type(outbound) is dict,'outbound_shape')
        require(outbound.get('owner')==rows[0]['owner'] and outbound.get('phase')==rows[0]['phase'],'outbound_mismatch')
        require(route.get('variant_consumes_slot') is False,'variant_slot')
        require(route.get('current_owner')==profile.get('owner'),'owner_mismatch')
        return {'valid':True,'issues':[],'assignments':len(rows),'seats':len(cycle),
                'delivery_verified':False,'permission_granted':False,'independent_reproduction':False}
    except (ContractError,KeyError,TypeError,AttributeError) as error:
        # Malformed supplied records are rejected; values and private paths are not echoed.
        return {'valid':False,'issues':[str(error) if isinstance(error,ContractError) else 'malformed_record'],
                'delivery_verified':False,'permission_granted':False,'independent_reproduction':False}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--profile',type=Path,required=True)
    parser.add_argument('--route',type=Path,required=True)
    args=parser.parse_args()
    try:
        raw_profile=args.profile.read_bytes();raw_route=args.route.read_bytes()
        require(len(raw_profile)<=1048576 and len(raw_route)<=1048576,'input_budget')
        result=validate(strict_json(raw_profile),strict_json(raw_route))
    except (OSError,ValueError,RecursionError):
        result={'valid':False,'issues':['unreadable_or_invalid_json'],'delivery_verified':False,'permission_granted':False,'independent_reproduction':False}
    print(json.dumps(result,sort_keys=True))
    return 0 if result['valid'] else 2

if __name__=='__main__':sys.exit(main())
