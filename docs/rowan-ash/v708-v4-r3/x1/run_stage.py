"""Run only the frozen selected X1 model contracts; preserve every first receipt."""
from pathlib import Path
import argparse,ast,copy,datetime,hashlib,json,os,platform,runpy,sys,time,ctypes


def raw(d):
    return (json.dumps(d,sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode()


def sha(b):
    return hashlib.sha256(b).hexdigest()


def create(path,data):
    with path.open('xb') as f:
        f.write(raw(data))


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected-plan-sha256',required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--timing-log',type=Path,required=True)
    parser.add_argument('--only',nargs='*')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    planbytes=(root/'plan.json').read_bytes()
    if sha(planbytes)!=args.expected_plan_sha256:
        raise ValueError('Frozen plan source expectation mismatch')
    plan=json.loads(planbytes)
    if len(plan['models'])!=15 or plan['planned_final_distinct_checks']>500:
        raise ValueError('Model/test scope not admitted')
    source=root/'study_core.py';sourcebytes=source.read_bytes();ast.parse(sourcebytes.decode())
    ast.parse(Path(__file__).read_text())
    sourcehash=sha(sourcebytes);runnerhash=sha(Path(__file__).read_bytes())
    output=args.output.resolve()
    if output!=root/'results':
        raise ValueError('Outputs must be the owner stage results directory')
    output.mkdir(exist_ok=True)
    chosen=set(args.only or [m['id'] for m in plan['models']])
    if not chosen <= {m['id'] for m in plan['models']}:
        raise ValueError('Unknown selected model')
    started=time.perf_counter();cpu=time.process_time();startutc=utc()
    try:
        import psutil
        own_process=psutil.Process();rss_start=own_process.memory_info().rss
    except ImportError:
        own_process=None;rss_start=None
    log=args.timing_log.open('x',encoding='utf8',newline='\n')
    def event(name,**extra):
        log.write(json.dumps(dict(event=name,utc=utc(),elapsed_seconds=time.perf_counter()-started,**extra),sort_keys=True)+'\n');log.flush()
    event('pre_execution_source_check',plan_sha256=sha(planbytes),source_sha256=sourcehash,runner_sha256=runnerhash)
    C=runpy.run_path(str(source));encode=C['encode']
    invoked=cached=0;result_records=[]
    for i,m in enumerate(plan['models'],1):
        if m['id'] not in chosen:
            continue
        destination=output/(m['id']+'.json')
        if destination.exists():
            saved=json.loads(destination.read_bytes())
            if saved['source_sha256']!=sourcehash or saved['plan_sha256']!=sha(planbytes):
                raise ValueError('Saved receipt belongs to different bytes; review the dependency before resuming')
            cached+=1;result_records.append(saved);continue
        model_start=time.perf_counter();invoked+=1;params=copy.deepcopy(m['params']);request_before=sha(raw(params))
        checks=[];error=None;observed=None;negative=None;invalid=None
        try:
            result=C['FUNCTIONS'][i-1](params);observed=encode(result)
            if set(observed)!=set(m['expected']) or sha(raw(params))!=request_before:
                raise ValueError('Output field contract or immutable input violated')
            for key,expected in m['expected'].items():
                checks.append(dict(id=m['id']+'-'+key,kind='literal_expected_field',expected=expected,observed=observed[key],passed=type(observed[key]) is type(expected) and observed[key]==expected))
            bad=copy.deepcopy(m['params']);bad.update(copy.deepcopy(m['invalid_input']))
            try:
                badresult=C['FUNCTIONS'][i-1](bad)
                invalid=dict(request=bad,refused=False,output=encode(badresult),original_result='fail',original_credit=0)
            except (ValueError,TypeError,KeyError,ZeroDivisionError) as exc:
                invalid=dict(request=bad,refused=True,error_type=type(exc).__name__,reason=str(exc),original_result='fail',original_credit=0)
            checks.append(dict(id=m['id']+'-invalid-input',kind='refusal_predicate',expected=True,observed=invalid['refused'],passed=invalid['refused']))
            wrong=encode(C['mutant_value'](i,m['params'],result));field=m['negative_control']['field'];negative=dict(rule_index=i,field=field,observed_wrong_value=wrong,frozen_wrong_value=m['negative_control']['value'],correct_value=m['expected'][field],original_result='fail',original_credit=0,expected_failure=True,source_sha256=sourcehash)
            detected=wrong==m['negative_control']['value'] and wrong!=m['expected'][field]
            checks.append(dict(id=m['id']+'-wrong-rule',kind='negative_control_detection',expected=True,observed=detected,passed=detected))
        except Exception as exc:
            error=dict(error_type=type(exc).__name__,message=str(exc),original_credit=0)
        record=dict(schema='ghc.rowan.p03.x1.model-result.v1',model_id=m['id'],model_name=m['name'],model_family_count=1,source_sha256=sourcehash,runner_sha256=runnerhash,plan_sha256=sha(planbytes),input_sha256=request_before,parameters=m['params'],result=observed,checks=checks,invalid_subject=invalid,negative_control=negative,unexpected_error=error,complete=len(checks)==8 and all(c['passed'] for c in checks) and error is None,started_utc=startutc,model_wall_seconds=time.perf_counter()-model_start,execution_location='local Windows',independent_reproduction=False)
        create(destination,record);result_records.append(record);event('model_complete',model_id=m['id'],checks=len(checks),passed=sum(c['passed'] for c in checks),unexpected_error=error is not None)
        if not record['complete']:
            snapshot=output/(m['id']+'-first-failed-source.txt')
            with snapshot.open('xb') as f:f.write(sourcebytes)
    probe=output/'owned-write-probe.tmp';probe_ok=False
    with probe.open('xb') as f:f.write(b'owned D-first capability probe\n')
    probe_ok=probe.read_bytes()==b'owned D-first capability probe\n'
    probe.unlink()
    elapsed=time.perf_counter()-started;cpu_seconds=time.process_time()-cpu
    rss_end=own_process.memory_info().rss if own_process else None
    admin=bool(ctypes.windll.shell32.IsUserAnAdmin()) if os.name=='nt' else None
    runtime=dict(schema='ghc.rowan.p03.x1.runtime.v1',started_utc=startutc,ended_utc=utc(),os=platform.system(),python_version=platform.python_version(),logical_cpu_count=os.cpu_count(),actual_cpu_quota=None,administrator_token_observed=admin,owned_write_read_delete_probe=probe_ok,process_wall_seconds=elapsed,own_process_cpu_seconds=cpu_seconds,rss_start_bytes=rss_start,rss_end_bytes=rss_end,peak_RSS=None,requested_full_access=True,provided_sandbox_profile='danger-full-access',configured_fast_mode=True,configured_service_tier='priority',backend_fast_attested=False,backend_model_attested=False,new_paid_purchases_or_provider_jobs=0,inference_subscription_cost='not measured',source_sha256=sourcehash,runner_sha256=runnerhash)
    event('bounded_execution_complete',models_invoked=invoked,cached_records=cached,process_wall_seconds=elapsed)
    log.close()
    create(output/'runtime.json',runtime)
    total_checks=sum(len(r['checks']) for r in result_records);passed=sum(c['passed'] for r in result_records for c in r['checks'])
    summary=dict(models_invoked=invoked,cached_records=cached,model_families=len(result_records),final_distinct_checks=total_checks,passing_checks=passed,completed_models=sum(r['complete'] for r in result_records),deliberately_wrong_rule_originals=sum(r['negative_control'] is not None for r in result_records),invalid_input_originals=sum(r['invalid_subject'] is not None for r in result_records),unexpected_model_failures=sum(not r['complete'] for r in result_records),source_sha256=sourcehash,plan_sha256=sha(planbytes),runtime_record_sha256=sha(raw(runtime)),status='X1_EXECUTED_FOR_REVIEW' if all(r['complete'] for r in result_records) else 'FIRST_FAILURES_RETAINED')
    create(output/'summary.json',summary);print(json.dumps(summary));return 0 if all(r['complete'] for r in result_records) else 1


if __name__=='__main__':
    sys.exit(main())
