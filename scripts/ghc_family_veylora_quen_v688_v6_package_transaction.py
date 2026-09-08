"""Exact x1-locked isolated package transaction. No global Python mutation."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,sys,urllib.request,datetime
X1="6d7f5b0fc67f78a22463d3c3c9cec21aade35d92"
REL="docs/veylora-quen/v688-v6"
def dump(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open("x",encoding="utf-8",newline="\n") as f:json.dump(obj,f,indent=2,sort_keys=True);f.write("\n")
def run(command,bank,label):
 p=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","PYTHONUTF8":"1"})
 (bank/(label+".stdout.txt")).write_bytes(p.stdout);(bank/(label+".stderr.txt")).write_bytes(p.stderr)
 if p.returncode:raise RuntimeError(label+"_exit_"+str(p.returncode))
 return p.stdout
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--bank",type=Path,required=True);args=ap.parse_args()
 root=Path(__file__).resolve().parents[1];bank=args.bank.resolve()
 if bank.drive.upper()!="D:":raise RuntimeError("D_first_owner_bank_required")
 plan_path=root/REL/"x1/tool-package-plan.json";plan=json.loads(plan_path.read_text())
 frozen=subprocess.check_output(["git","-C",str(root),"show",X1+":"+REL+"/x1/tool-package-plan.json"])
 if json.loads(frozen)!=plan:raise RuntimeError("frozen_package_plan_changed")
 equality=json.loads((bank/"x1-equality.json").read_text())
 if equality["head"]!=X1 or not equality["clean"] or equality["divergence"]!=[0,0]:raise RuntimeError("x1_gate")
 marker=bank/"package-transaction-invoked.json"
 dump(marker,{"x1":X1,"state":"STARTED","direct_count":3,"closure_count":7})
 wheels=bank/"wheels";wheels.mkdir(exist_ok=False)
 entries=[]
 try:
  for p in plan["packages"]:
   target=wheels/p["wheel"]
   with urllib.request.urlopen(p["url"],timeout=45) as r:data=r.read(32*1024*1024+1)
   if len(data)>32*1024*1024 or hashlib.sha256(data).hexdigest()!=p["sha256"]:raise RuntimeError("wheel_fixity_"+p["name"])
   with target.open("xb") as f:f.write(data)
   entries.append({"name":p["name"],"version":p["version"],"wheel":p["wheel"],"sha256":p["sha256"],"bytes":len(data),"direct":p["direct"]})
  lock=bank/"requirements.lock.txt"
  with lock.open("x",encoding="utf-8") as f:f.write("\n".join(p["name"]+"=="+p["version"]+" --hash=sha256:"+p["sha256"] for p in plan["packages"])+"\n")
  envroot=bank/"environment"
  if envroot.exists():raise RuntimeError("environment_destination_exists")
  run([sys.executable,"-B","-m","venv",str(envroot)],bank,"venv")
  py=envroot/"Scripts/python.exe"
  run([str(py),"-B","-m","pip","install","--no-index","--only-binary=:all:","--require-hashes","--find-links",str(wheels),"-r",str(lock)],bank,"pip-install")
  run([str(py),"-B","-m","pip","check"],bank,"pip-check")
  smoke = r'''
from io import StringIO
import importlib.metadata as md,json
from intelhex import IntelHex
import bincopy,bitstruct
ih=IntelHex();ih[0]=0x12;ih[1]=0x34
text=StringIO();ih.write_hex_file(text)
again=IntelHex(StringIO(text.getvalue()))
assert {a:again[a] for a in again.addresses()}=={0:0x12,1:0x34}
bad=":02000000123400\n:00000001FF\n"
try:IntelHex(StringIO(bad))
except Exception as e:ih_error=type(e).__name__
else:raise AssertionError("intelhex_bad_checksum_accepted")
b=bincopy.BinFile();b.add_ihex(text.getvalue())
assert bytes(b.as_binary())==b"\x12\x34"
s=b.as_srec();b2=bincopy.BinFile();b2.add_srec(s)
assert bytes(b2.as_binary())==b"\x12\x34"
try:bincopy.BinFile().add_srec("S903000000\n")
except Exception as e:bc_error=type(e).__name__
else:raise AssertionError("bincopy_bad_checksum_accepted")
assert bitstruct.pack("u16",0x1234)==b"\x12\x34"
assert bitstruct.unpack("u16",b"\x12\x34")== (0x1234,)
try:bitstruct.pack("u8",256)
except Exception as e:bs_error=type(e).__name__
else:raise AssertionError("bitstruct_overflow_accepted")
names=["intelhex","bincopy","bitstruct","humanfriendly","argparse-addons","pyelftools","pyreadline3"]
print(json.dumps({"versions":{n:md.version(n) for n in names},"direct_smokes":{"intelhex":{"accepting":True,"adverse_rejected":True,"error_class":ih_error},"bincopy":{"accepting":True,"adverse_rejected":True,"error_class":bc_error},"bitstruct":{"accepting":True,"adverse_rejected":True,"error_class":bs_error}},"hardware_execution":False,"independent_reproduction":False}))
'''
  smokes=json.loads(run([str(py),"-B","-X","utf8","-c",smoke],bank,"package-smokes"))
  for p in plan["packages"]:
   if smokes["versions"][p["name"]]!=p["version"]:raise RuntimeError("installed_version_mismatch")
  query={"queries":[{"package":{"name":p["name"],"ecosystem":"PyPI"},"version":p["version"]} for p in plan["packages"]]}
  request=urllib.request.Request("https://api.osv.dev/v1/querybatch",data=json.dumps(query).encode(),headers={"Content-Type":"application/json"})
  with urllib.request.urlopen(request,timeout=45) as response:advisory=json.load(response)
  if len(advisory.get("results",[]))!=7:raise RuntimeError("advisory_response_shape")
  advisories=[{"name":p["name"],"version":p["version"],"vulnerabilities":r.get("vulns",[])} for p,r in zip(plan["packages"],advisory["results"])]
  dump(bank/"package-advisory-snapshot.json",{"queried_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "source":"https://api.osv.dev/v1/querybatch","packages":advisories,"exhaustive_security":False})
  result={"schema":"ghc.family.firmware-package-transaction.v1","x1":X1,"state":"COMPLETE",
   "direct_count":3,"closure_count":7,"artifacts":entries,"smokes":smokes,"pip_check_passed":True,
   "advisory_query_count":7,"advisory_vulnerability_count":sum(len(r["vulnerabilities"]) for r in advisories),
   "install_scope":"new isolated D-first owner environment","global_python_mutated":False,
   "frozen_plan_changed":False,"hardware_execution":False,"canonical_invoked":False,
   "rollback":"Stop selecting the isolated owner environment and retain all receipts; no automatic deletion.",
   "boundary":"Same-owner software and observed advisory snapshot only; no exhaustive security, independent reproduction, real firmware safety, deployment or authority."}
  dump(bank/"package-transaction.json",result)
  print(json.dumps({"status":"COMPLETE","direct_packages":3,"closure":7,"positive_smokes":3,"adverse_smokes":3,"advisory_vulnerabilities":result["advisory_vulnerability_count"]}))
 except Exception as exc:
  dump(bank/"package-transaction-failure.json",{"state":"FAILED_RETAINED","error_class":type(exc).__name__,"signature":str(exc),"success_credit":0,"downloaded_artifacts":entries})
  raise
if __name__=="__main__":main()
