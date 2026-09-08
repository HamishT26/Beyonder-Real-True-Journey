"""Exercise the selected wheel APIs on disposable in-memory fixtures only."""
import argparse
import copy
import importlib.metadata
import json
import sys
from pathlib import Path

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    site=args.site.resolve()
    sys.path[:]=[str(site)]+[p for p in sys.path if 'site-packages' not in p.lower()]
    rows=[]
    def check(package,name,expected,observed,subject='pass'):
        row=dict(package=package,case=name,expected=expected,observed=observed,
                 matched=expected==observed,subject_result=subject,original_success_credit=1 if subject=='pass' else 0)
        rows.append(row)
        if not row['matched']:raise AssertionError(name)
    def refusal(package,name,fn,exception_name):
        observed=None
        try:fn()
        except Exception as e:observed=type(e).__name__
        check(package,name,exception_name,observed,'fail')
    try:
        import immutables
        base=immutables.Map({'a':1});derived=base.set('a',2)
        check('immutables','derived mapping preserves original',[1,2],[base['a'],derived['a']])
        def map_assign():base['a']=3
        refusal('immutables','immutable binding assignment',map_assign,'TypeError')

        from frozendict import frozendict
        fixed=frozendict(a=1)
        check('frozendict','stable value mapping',{'a':1},dict(fixed))
        def frozen_assign():fixed['a']=2
        refusal('frozendict','immutable binding assignment',frozen_assign,'TypeError')
        child=[];shallow=frozendict(child=child);child.append('changed')
        check('frozendict','deep immutability preclaim is false',True,shallow['child']==['changed'],'fail')

        from bidict import bidict
        mapping=bidict({'a':1})
        check('bidict','inverse lookup','a',mapping.inverse[1])
        def duplicate_value():mapping['b']=1
        refusal('bidict','duplicate value mapping',duplicate_value,'ValueDuplicationError')
        check('bidict','failed assignment preserves mapping',{'a':1},dict(mapping))

        from boltons.iterutils import remap
        source={'items':[{'keep':1,'cache':9}]};before=copy.deepcopy(source)
        transformed=remap(source,visit=lambda path,key,value:False if key=='cache' else (key,value))
        check('boltons','detached structural remap',{'items':[{'keep':1}]},transformed)
        check('boltons','source remains unchanged',before,source)
        def rejecting_visit(path,key,value):
            if key=='forbidden':raise ValueError('rejected fixture field')
            return key,value
        refusal('boltons','rejecting visit callback propagates',lambda:remap({'forbidden':1},visit=rejecting_visit,reraise_visit=True),'ValueError')

        import toolz
        check('toolz','finite partitions',[[1,2],[3]],[list(x) for x in toolz.partition_all(2,[1,2,3])])
        refusal('toolz','empty first item',lambda:toolz.first([]),'StopIteration')

        import more_itertools
        check('more-itertools','overlapping source windows',[[1,2,3],[2,3,4]],[list(x) for x in more_itertools.windowed([1,2,3,4],3)])
        refusal('more-itertools','exact-one rejects two records',lambda:more_itertools.one([1,2]),'ValueError')

        import portion as intervals
        overlap=intervals.closed(0,2000)&intervals.closed(1800,2200)
        check('portion','inclusive capacity interval',True,overlap==intervals.closed(1800,2000))
        check('portion','touching half-open intervals do not overlap',True,(intervals.closedopen(0,1)&intervals.closedopen(1,2))==intervals.empty(),'fail')

        from intervaltree import IntervalTree
        tree=IntervalTree.from_tuples([(0,2,'a'),(2,4,'b')])
        check('intervaltree','half-open point lookup',['b'],sorted(i.data for i in tree.at(2)))
        refusal('intervaltree','zero-length interval',lambda:tree.addi(2,2,'empty'),'ValueError')

        from transitions import Machine
        class Guarded:
            permitted=False
            def reviewed(self):return self.permitted
        item=Guarded()
        machine=Machine(item,states=['draft','sealed','closed'],initial='draft',auto_transitions=False,
            transitions=[dict(trigger='seal',source='draft',dest='sealed',conditions='reviewed'),
                         dict(trigger='close',source='sealed',dest='closed')])
        check('transitions','false guard keeps draft',[False,'draft'],[item.seal(),item.state],'fail')
        item.permitted=True;item.seal();item.close()
        check('transitions','ordered lifecycle','closed',item.state)
        refusal('transitions','repeat after terminal state',lambda:item.seal(),'MachineError')

        from statemachine import StateMachine,State
        class Steps(StateMachine):
            draft=State(initial=True)
            sealed=State()
            closed=State(final=True)
            seal=draft.to(sealed)
            close=sealed.to(closed)
        steps=Steps()
        refusal('python-statemachine','skip intermediate state',lambda:steps.close(),'TransitionNotAllowed')
        steps.seal();steps.close()
        check('python-statemachine','ordered lifecycle','closed',steps.current_state.id)

        from dictdiffer import diff,patch,revert
        initial={'count':1,'items':['a']};after={'count':2,'items':['a','b']};before=copy.deepcopy(initial)
        delta=list(diff(initial,after,tolerance=0))
        check('dictdiffer','detached patch',after,patch(delta,initial))
        check('dictdiffer','exact revert',initial,revert(delta,after))
        check('dictdiffer','source preserved',before,initial)
        changed=patch([('change','count',(1,3))],initial)
        check('dictdiffer','changed target does not match the intended after state',False,changed==after,'fail')
        check('dictdiffer','type-strict equality preclaim is false',[],list(diff({'a':True},{'a':1},tolerance=0)),'fail')

        import rustworkx as rx
        graph=rx.PyDiGraph(check_cycle=True);graph.add_nodes_from(['a','b','c']);graph.add_edge(0,1,None);graph.add_edge(1,2,None)
        check('rustworkx','dependency descendants',[1,2],sorted(rx.descendants(graph,0)))
        refusal('rustworkx','cycle checking blocks a back edge',lambda:graph.add_edge(2,0,None),'DAGWouldCycle')

        from anytree import Node
        root=Node('owner');pillar=Node('body',parent=root);practice=Node('practice',parent=pillar);task=Node('task',parent=practice)
        check('anytree','four-tier depth',[0,1,2,3],[n.depth for n in [root,pillar,practice,task]])
        def parent_cycle():root.parent=task
        refusal('anytree','ancestor cycle',parent_cycle,'LoopError')
        check('anytree','failed cycle preserves root',None,root.parent)
        versions={d.metadata['Name']:d.version for d in importlib.metadata.distributions(path=[str(site)])}
        result=dict(schema='ghc.family.remaster.package-smokes.v1',rows=rows,versions=versions,
           selected_packages_exercised=len({r['package'] for r in rows}),all_matched=all(r['matched'] for r in rows),
           real_data_used=False,filesystem_mutations_by_fixtures=False,network_actions=False,
           native_launchers_executed=False,independent_reproduction=False,
           limitations=['Immutable mappings can retain mutable child values','Dictdiffer equality is not the owner type-strict JSON relation',
                        'Library state transitions and trees are local models, not task activation or authority evidence'])
    except Exception as error:
        result=dict(schema='ghc.family.remaster.package-smokes-failure.v1',rows=rows,
           error_type=type(error).__name__,error=str(error),original_success_credit=0,all_matched=False)
        with args.output.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,sort_keys=True,indent=2)
        raise
    with args.output.open('x',encoding='utf-8',newline='\n') as f:json.dump(result,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(dict(packages=result['selected_packages_exercised'],checks=len(rows),all_matched=True,
             failed_subjects=sum(r['subject_result']=='fail' for r in rows))))

if __name__=='__main__':main()
