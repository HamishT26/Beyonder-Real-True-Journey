"""Exercise all thirteen additions using explicit disposable inputs."""
import argparse,io,json,os,pathlib,sys,time

def run(target,scratch):
    sys.path.insert(0,str(target));scratch.mkdir(parents=True,exist_ok=False)
    import simpy,heapdict,cacheout,rapidjson,jsonlines,glom,dpath,box,pyrsistent,parsy,pyperf,psutil,zict
    rows=[]
    def check(name,purpose,condition,observed):
        rows.append({'package':name,'purpose':purpose,'passed':bool(condition),'observed':observed,'independent_reproduction':False})
        if not condition:raise AssertionError(name+': '+purpose)
    def rejects(name,purpose,exc,fn):
        try:fn()
        except exc as e:check(name,purpose,True,type(e).__name__)
        else:check(name,purpose,False,'accepted')
    env=simpy.Environment();resource=simpy.Resource(env,capacity=1);events={}
    def job(i,arrival,duration):
        yield env.timeout(arrival)
        with resource.request() as request:
            yield request;start=env.now;yield env.timeout(duration);events[i]=[start,env.now]
    for i,(a,d) in enumerate([(0,3),(1,2),(1,1)]):env.process(job(i,a,d))
    env.run();actual=[events[i] for i in range(3)]
    check('simpy','Independent serial queue timeline',actual==[[0,3],[3,5],[5,6]],actual)
    rejects('simpy','Negative timeout refused',ValueError,lambda:env.timeout(-1))
    h=heapdict.heapdict();h['a']=(3,0);h['b']=(5,1);h['b']=(1,1);value=h.popitem()
    check('heapdict','Decrease key changes next priority',value==('b',(1,1)),repr(value))
    h.clear();rejects('heapdict','Empty priority queue has no invented item',IndexError,h.popitem)
    clock=[0];cache=cacheout.Cache(ttl=5,timer=lambda:clock[0]);cache.set('x',3)
    check('cacheout','Declared key can be retrieved',cache.get('x')==3,cache.get('x'))
    clock[0]=6;check('cacheout','Synthetic clock expires TTL',cache.get('x') is None,cache.get('x'))
    value={'large':2**60,'flag':False,'missing':None};back=rapidjson.loads(rapidjson.dumps(value))
    check('python-rapidjson','Typed integer JSON roundtrip',back==value and type(back['large']) is int,back)
    rejects('python-rapidjson','Nonfinite serialization refused',ValueError,lambda:rapidjson.dumps(float('nan'),allow_nan=False))
    reader=jsonlines.Reader(io.StringIO('{"x":1}\nnot-json\n'));first=reader.read()
    check('jsonlines','First record remains independent',first=={'x':1},first)
    rejects('jsonlines','Malformed next line is visible',jsonlines.InvalidLineError,reader.read)
    value={'a':{'b':3}};got=glom.glom(value,'a.b')
    check('glom','Declared nested projection',got==3 and value=={'a':{'b':3}},got)
    rejects('glom','Missing path refused',glom.PathAccessError,lambda:glom.glom(value,'a.missing'))
    value={'a/b':{'c':4}};got=dpath.get(value,['a/b','c'])
    check('dpath','Separator is literal in segment list',got==4,got)
    rejects('dpath','Missing explicit path refused',KeyError,lambda:dpath.get(value,['missing']))
    original={'a':{'b':4}};bx=box.Box(original)
    check('python-box','Dot access agrees with original dictionary',bx.a.b==4 and bx.to_dict()==original,bx.to_dict())
    rejects('python-box','Absent attribute is not a value',AttributeError,lambda:bx.missing)
    original={'a':[1]};frozen=pyrsistent.freeze(original);updated=frozen.set('a',frozen['a'].append(2))
    check('pyrsistent','Nested persistent update leaves source intact',pyrsistent.thaw(frozen)==original and pyrsistent.thaw(updated)=={'a':[1,2]},pyrsistent.thaw(updated))
    detached=pyrsistent.thaw(frozen);detached['a'].append(9)
    check('pyrsistent','Thawed edit cannot mutate frozen oracle',pyrsistent.thaw(frozen)=={'a':[1]},pyrsistent.thaw(frozen))
    parser=parsy.seq(version=parsy.string('v')>>parsy.regex('[1-9][0-9]*').map(int),slot=parsy.string('-v')>>parsy.regex('[1-8]').map(int))
    got=parser.parse('v725-v8');check('parsy','Complete phase parse',got=={'version':725,'slot':8},got)
    rejects('parsy','Trailing phase text refused',parsy.ParseError,lambda:parser.parse('v725-v8x'))
    durations=[]
    for _ in range(5):
        start=time.perf_counter();sum(i*i for i in range(1000));durations.append(time.perf_counter()-start)
    run=pyperf.Run(durations,metadata={'name':'owner-square-sum'},collect_metadata=False);benchmark=pyperf.Benchmark([run])
    check('pyperf','Measured local samples retain finite mean',benchmark.mean()>0,{'mean_seconds':benchmark.mean(),'values':durations})
    check('pyperf','Recorded sample count stays explicit',benchmark.get_nvalue()==5,benchmark.get_nvalue())
    process=psutil.Process(os.getpid());rss=process.memory_info().rss;cpu=process.cpu_times()
    check('psutil','Own helper memory sample',rss>0,{'rss_bytes':rss,'scope':'current helper process only'})
    check('psutil','Own helper CPU sample',cpu.user>=0 and cpu.system>=0,{'user_seconds':cpu.user,'system_seconds':cpu.system})
    files=zict.File(str(scratch/'zict'));payload=json.dumps({'record':'synthetic','value':7},sort_keys=True).encode('utf-8');files['entry']=payload
    got=bytes(files['entry']);check('zict','Explicit JSON bytes roundtrip without pickle',got==payload,json.loads(got))
    rejects('zict','Absent stored key stays missing',KeyError,lambda:files['absent'])
    files.close()
    return {'checks':rows,'count':len(rows),'all_passed':all(r['passed'] for r in rows),'direct_packages':13,'diskcache_executed':False,'token_usage_measured':False,'energy_measured':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--target',required=True);ap.add_argument('--scratch',required=True);ap.add_argument('--out',required=True);a=ap.parse_args()
    try:r=run(pathlib.Path(a.target),pathlib.Path(a.scratch))
    except Exception as ex:
        r={'all_passed':False,'error':type(ex).__name__,'message':str(ex)}
        with pathlib.Path(a.out).open('x',encoding='utf-8',newline='\n') as f:json.dump(r,f,indent=2);f.write('\n')
        raise
    with pathlib.Path(a.out).open('x',encoding='utf-8',newline='\n') as f:json.dump(r,f,indent=2);f.write('\n')
    print(json.dumps({k:r[k] for k in ['count','all_passed','direct_packages']},indent=2))
