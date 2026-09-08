"""Synthetic lifecycle predicate fixture; this is never a live canonical receipt."""
import argparse,copy,json,re
from pathlib import Path,PurePosixPath
def validate_fixture(data):
 issues=[]
 fields={"source","x1","evidence","final","parents","heads","clean","divergence","owner_delta_only","canonical_successes","canonical_replays"}
 if type(data) is not dict or set(data)!=fields:return {"valid":False,"issues":["field_set"],"live_receipt":False}
 anchors=[data[k] for k in ("source","x1","evidence","final")]
 if any(type(v) is not str or re.fullmatch("[a-f0-9]{40}",v) is None for v in anchors):issues.append("anchor_shape")
 if len(set(map(str,anchors)))!=4:issues.append("anchor_distinctness")
 if data["parents"]!=[[data["x1"],data["source"]],[data["evidence"],data["x1"]],[data["final"],data["evidence"]]]:issues.append("direct_chain")
 if type(data["heads"]) is not list or len(data["heads"])!=4 or any(v!=data["final"] for v in data["heads"]):issues.append("four_way_equality")
 if data["clean"] is not True:issues.append("clean")
 if data["owner_delta_only"] is not True:issues.append("owner_scope")
 if type(data["divergence"]) is not list or len(data["divergence"])!=2 or any(type(v) is not int or v!=0 for v in data["divergence"]):issues.append("zero_divergence")
 if type(data["canonical_successes"]) is not int or data["canonical_successes"]!=1:issues.append("one_success")
 if type(data["canonical_replays"]) is not int or data["canonical_replays"]!=0:issues.append("no_replay")
 return {"valid":not issues,"issues":issues,"live_receipt":False}
def safe_relative_paths(paths):
 if type(paths) is not list or len(paths)>2000 or len(paths)!=len(set(paths)):raise ValueError("allowlist_shape")
 for p in paths:
  if type(p) is not str or "\\" in p or ":" in p or PurePosixPath(p).is_absolute() or ".." in PurePosixPath(p).parts or not p:raise ValueError("allowlist_path")
 return paths
def self_test():
 s,x,e,f=[c*40 for c in "1234"]
 valid={"source":s,"x1":x,"evidence":e,"final":f,"parents":[[x,s],[e,x],[f,e]],"heads":[f]*4,
  "clean":True,"divergence":[0,0],"owner_delta_only":True,"canonical_successes":1,"canonical_replays":0}
 mutations=[]
 for field,value in [("parents",[[x,s],[e,s],[f,e]]),("heads",[f,f,f,e]),("owner_delta_only",False),("canonical_successes",2),("canonical_replays",1)]:
  bad=copy.deepcopy(valid);bad[field]=value;result=validate_fixture(bad)
  mutations.append({"field":field,"input":bad,"observed":result,"expected_rejection":True,"predicate_pass":not result["valid"],"candidate_success_credit":0})
 result=validate_fixture(valid)
 return {"schema":"ghc.family.synthetic-lifecycle-readiness.v1","fixture_kind":"synthetic_only",
  "accepting_input":valid,"accepting_result":result,"negative_controls":mutations,
  "valid":result["valid"] and all(r["predicate_pass"] for r in mutations),
  "live_head_verified":False,"canonical_invoked":False,"independent_reproduction":False}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,required=True);args=p.parse_args();result=self_test()
 with args.output.open("x",encoding="utf-8",newline="\n") as h:json.dump(result,h,indent=2,sort_keys=True);h.write("\n")
 print(json.dumps({"valid":result["valid"],"positive":1,"negative_controls":5,"live_receipt":False}))
 return not result["valid"]
if __name__=="__main__":raise SystemExit(main())
