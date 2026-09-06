"""Planning definitions only: hand-declared inputs and expected results for v687-v4."""
from copy import deepcopy

CASES = []

def add(operation, title, payload, result, decision="ACCEPT", disposition="completed"):
    CASES.append(dict(operation=operation, title=title, input=deepcopy(payload),
        expected_output=dict(decision=decision, result=deepcopy(result), source_preserved=True, external_credit=False),
        expected_execution_disposition=disposition))

def schema_cases():
    op="schema_transition_matrix"
    def c(title, instance, old, new, before=True, after=False):
        decision={(True,True):"BOTH_ACCEPT_SAMPLE",(True,False):"NEW_REJECTS_SAMPLE",(False,True):"NEW_ACCEPTS_SAMPLE",(False,False):"BOTH_REJECT_SAMPLE"}[before,after]
        add(op,title,dict(instance=instance,old_schema=old,new_schema=new),dict(old_valid=before,new_valid=after,universal_compatibility=False),decision)
    c("New required field breaks a formerly accepted record",{}, {"type":"object"},{"type":"object","required":["unit"]})
    c("Narrowing a union removes the integer branch",7,{"type":["integer","string"]},{"type":"string"})
    c("Raising an inclusive numeric minimum excludes its old boundary",0,{"minimum":0},{"minimum":1})
    c("Lowering a numeric maximum excludes the old endpoint",10,{"maximum":10},{"maximum":9})
    c("Removing an enum member breaks its existing record","old",{"enum":["old","new"]},{"enum":["new"]})
    c("A newly required string pattern rejects an unprefixed identifier","item",{"type":"string"},{"type":"string","pattern":"^urn:"})
    c("Removing a minimum length admits an empty value","",{"minLength":1},{"type":"string"},False,True)
    c("A tighter maximum string length excludes a longer value","abc",{"maxLength":3},{"maxLength":2})
    c("A minimum item count excludes the empty list",[],{"type":"array"},{"type":"array","minItems":1})
    c("Unique item enforcement rejects duplicate values",[1,1],{"type":"array"},{"type":"array","uniqueItems":True})
    c("Closing additional properties rejects an unlisted field",{"extra":1},{"type":"object"},{"type":"object","additionalProperties":False})
    c("A contains assertion requires an integer witness",["x"],{"type":"array"},{"type":"array","contains":{"type":"integer"}})
    c("Dependent required metadata becomes mandatory with the trigger",{"value":1},{"type":"object"},{"dependentRequired":{"value":["unit"]}})
    c("Conditional branches activate only when their discriminator matches",{"kind":"scalar"},{"type":"object"},{"if":{"properties":{"kind":{"const":"scalar"}},"required":["kind"]},"then":{"required":["value"]}})
    c("Overlapping oneOf branches reject an integer matched twice",1,{"anyOf":[{"type":"number"},{"type":"integer"}]},{"oneOf":[{"type":"number"},{"type":"integer"}]})
    c("Unevaluated properties remain closed after an allOf evaluation",{"a":1,"b":2},{"allOf":[{"properties":{"a":{"type":"integer"}}}]},{"allOf":[{"properties":{"a":{"type":"integer"}}}],"unevaluatedProperties":False})
    c("Changing a const discriminator rejects both unrelated revisions","third",{"const":"old"},{"const":"new"},False,False)
    c("Tuple position changes reject the former first item",[1],{"prefixItems":[{"type":"integer"}]},{"prefixItems":[{"type":"string"}]})
    c("A propertyNames pattern applies to field names",{"Upper":1},{"type":"object"},{"propertyNames":{"pattern":"^[a-z]+$"}})
    c("An unchanged maximum property bound retains the same sample",{"a":1},{"maxProperties":1},{"maxProperties":1},True,True)

def patch_cases():
    op="atomic_patch_preview"
    def c(title,doc,patch,out=None,reason=None,writes=None,reads=None,protected=None):
        payload=dict(document=doc,patch=patch,write_allowlist=[""] if writes is None else writes,read_allowlist=[""] if reads is None else reads,protected_paths=[] if protected is None else protected)
        add(op,title,payload,dict(document=doc if reason else out,reason=reason),"HOLD" if reason else "PREVIEW_ONLY")
    c("Nested replacement returns a detached preview",{"a":{"b":1}},[{"op":"replace","path":"/a/b","value":2}],{"a":{"b":2}})
    c("Array insertion preserves the displaced item",{"a":[1,3]},[{"op":"add","path":"/a/1","value":2}],{"a":[1,2,3]})
    c("The append marker extends only the selected array",{"a":[1]},[{"op":"add","path":"/a/-","value":2}],{"a":[1,2]})
    c("Copy needs read authority for its source",{"a":1},[{"op":"copy","from":"/a","path":"/b"}],reason="READ_OUTSIDE_ALLOWLIST",reads=["/other"])
    c("Move requires write permission for the removed source",{"a":1},[{"op":"move","from":"/a","path":"/b"}],reason="WRITE_OUTSIDE_ALLOWLIST",writes=["/b"])
    c("Removal produces an empty object without changing source",{"a":1},[{"op":"remove","path":"/a"}],{})
    c("A late failed test rolls back the entire preview",{"a":1},[{"op":"replace","path":"/a","value":2},{"op":"test","path":"/a","value":3}],reason="TEST_FAILED")
    c("Boolean and integer test values are distinct in the local profile",{"a":True},[{"op":"test","path":"/a","value":1}],reason="TEST_FAILED")
    c("Integer and floating representations are distinct in the local profile",{"a":1},[{"op":"test","path":"/a","value":1.0}],reason="TEST_FAILED")
    c("Invalid tilde escapes are refused before mutation",{"a":1},[{"op":"add","path":"/bad~2key","value":2}],reason="INVALID_POINTER")
    c("Root replacement needs explicit root write scope",{"a":1},[{"op":"replace","path":"","value":2}],reason="WRITE_OUTSIDE_ALLOWLIST",writes=["/a"])
    c("Unknown patch operations are refused",{},[{"op":"increment","path":"/a","value":1}],reason="INVALID_OPERATION")
    c("Undeclared operation fields are refused by the local profile",{},[{"op":"add","path":"/a","value":1,"extra":True}],reason="INVALID_OPERATION")
    c("Add without a value is not an implicit null",{},[{"op":"add","path":"/a"}],reason="INVALID_OPERATION")
    c("Replacing an absent location is a held preview",{},[{"op":"replace","path":"/a","value":1}],reason="PATCH_CONFLICT")
    c("An array index beyond its insertion boundary is held",{"a":[1]},[{"op":"add","path":"/a/3","value":2}],reason="PATCH_CONFLICT")
    c("Leading-zero array indices are refused",{"a":[1]},[{"op":"replace","path":"/a/00","value":2}],reason="INVALID_ARRAY_INDEX")
    c("A move into its own descendant is refused",{"a":{"b":1}},[{"op":"move","from":"/a","path":"/a/c"}],reason="DESCENDANT_MOVE")
    c("Path permission compares segments rather than string prefixes",{"ab":1},[{"op":"replace","path":"/ab","value":2}],reason="WRITE_OUTSIDE_ALLOWLIST",writes=["/a"])
    c("Ancestor replacement cannot overwrite a protected descendant",{"a":{"authority":False}},[{"op":"replace","path":"/a","value":{}}],reason="PROTECTED_PATH",protected=["/a/authority"])

def reference_cases():
    op="offline_reference_snapshot"
    def c(title,resources,ref,result=None,reason=None,base=""):
        add(op,title,dict(resources=resources,ref=ref,base=base),dict(resolved=result,reason=reason,network_requests=0),"HOLD" if reason else "RESOLVED_OFFLINE")
    def r(uri,content): return dict(uri=uri,contents=content)
    c("An explicitly registered URN resolves offline",[r("urn:sample:a",{"type":"integer"})],"urn:sample:a",{"type":"integer"})
    c("An HTTPS identifier can resolve from an in-memory entry",[r("https://example.invalid/a",{"type":"string"})],"https://example.invalid/a",{"type":"string"})
    c("An unregistered HTTPS reference performs no network retrieval",[],"https://example.invalid/missing",reason="UNRESOLVED")
    c("An unregistered URN is unresolved",[],"urn:sample:missing",reason="UNRESOLVED")
    c("A JSON Pointer fragment selects a declared definition",[r("urn:sample:a",{"$defs":{"item":{"type":"integer"}}})],"urn:sample:a#/$defs/item",{"type":"integer"})
    c("Escaped slash in a definition name remains one segment",[r("urn:sample:a",{"$defs":{"a/b":{"const":1}}})],"urn:sample:a#/$defs/a~1b",{"const":1})
    c("Escaped tilde in a definition name resolves literally",[r("urn:sample:a",{"$defs":{"a~b":{"const":2}}})],"urn:sample:a#/$defs/a~0b",{"const":2})
    c("Equal duplicate registration is explicitly refused",[r("urn:sample:a",True),r("urn:sample:a",True)],"urn:sample:a",reason="DUPLICATE_URI")
    c("Conflicting duplicate registration is explicitly refused",[r("urn:sample:a",True),r("urn:sample:a",False)],"urn:sample:a",reason="DUPLICATE_URI")
    c("A nested resource identifier is discovered within the registry",[r("https://example.invalid/root",{"$id":"https://example.invalid/root","$defs":{"child":{"$id":"child","type":"integer"}}})],"https://example.invalid/child",{"$id":"child","type":"integer"})
    c("An empty fragment resolves the whole resource",[r("urn:sample:a",{"type":"null"})],"urn:sample:a#",{"type":"null"})
    c("A declared anchor resolves its subschema",[r("urn:sample:a",{"$defs":{"x":{"$anchor":"item","type":"boolean"}}})],"urn:sample:a#item",{"$anchor":"item","type":"boolean"})
    c("An absent anchor yields an unresolved hold",[r("urn:sample:a",{})],"urn:sample:a#missing",reason="UNRESOLVED")
    c("A relative resource resolves against its explicit base",[r("https://example.invalid/dir/item",{"type":"array"})],"item",{"type":"array"},base="https://example.invalid/dir/")
    c("A relative resource without an absolute base is refused",[],"item",reason="ABSOLUTE_BASE_REQUIRED")
    c("A different declared dialect is outside this profile",[r("urn:sample:a",{"$schema":"http://json-schema.org/draft-07/schema#"})],"urn:sample:a",reason="UNSUPPORTED_DIALECT")
    c("Boolean true schemas remain boolean",[r("urn:sample:a",True)],"urn:sample:a",True)
    c("Boolean false schemas remain boolean",[r("urn:sample:a",False)],"urn:sample:a",False)
    c("A root identifier inconsistent with registration is refused",[r("urn:sample:a",{"$id":"urn:sample:b"})],"urn:sample:a",reason="IDENTIFIER_MISMATCH")
    c("Resolution returns a self-reference without recursively evaluating it",[r("urn:sample:a",{"$ref":"urn:sample:a"})],"urn:sample:a",{"$ref":"urn:sample:a"})

def rename_cases():
    op="lossless_field_migration"
    def c(title,record,rules,result=None,reason=None):
        add(op,title,dict(record=record,rules=rules),dict(record=record if reason else result,reason=reason),"HOLD" if reason else "MIGRATED_VIEW")
    def rule(a="old",b="new",required=True): return dict(source=a,target=b,required=required)
    c("Optional absent fields stay absent",{},[rule(required=False)],{})
    for label,value in [("null",None),("false",False),("zero",0),("empty string",""),("empty array",[]),("empty object",{})]:
        c("An explicit "+label+" survives the rename",{"old":value},[rule()],{"new":value})
    c("Canonical-equivalent Unicode names are not merged",{"é":1,"e\u0301":2},[rule("é","named")],{"named":1,"e\u0301":2})
    c("Slash and tilde remain literal top-level key characters",{"a/b~c":1},[rule("a/b~c","new")],{"new":1})
    c("An occupied destination is held even when its value is equal",{"old":1,"new":1},[rule()],reason="OCCUPIED_TARGET")
    c("Two source fields cannot target the same destination",{"a":1,"b":2},[rule("a","c"),rule("b","c")],reason="DUPLICATE_TARGET")
    c("A source cannot be consumed by two rules",{"a":1},[rule("a","b"),rule("a","c")],reason="DUPLICATE_SOURCE")
    c("A self-rename leaves its field intact",{"a":1},[rule("a","a")],{"a":1})
    c("A two-way swap reads both original values",{"a":1,"b":2},[rule("a","b"),rule("b","a")],{"a":2,"b":1})
    c("A rename chain uses simultaneous source values",{"a":1,"b":2},[rule("a","b"),rule("b","c")],{"b":1,"c":2})
    c("An empty rule set is an identity view",{"a":1},[],{"a":1})
    c("Numeric-looking property names remain strings",{"01":1},[rule("01","1")],{"1":1})
    c("A missing required source blocks the whole view",{},[rule()],reason="MISSING_SOURCE")
    c("An invalid rule shape has no implicit defaults",{"old":1},[{"source":"old","target":"new"}],reason="INVALID_RULE")
    c("Nested object values retain their entire internal structure",{"old":{"new":None}},[rule()],{"new":{"new":None}})

schema_cases()
patch_cases()
reference_cases()
rename_cases()

def graph_cases():
    op="migration_obligation_graph"
    def n(label,deps=None,artifacts=None,disposition="completed"):
        return dict(id=label,dependencies=deps or [],artifacts=["proof"] if artifacts is None else artifacts,disposition=disposition)
    def c(title,nodes,order=None,ready=None,held=None,reason=None,available=None):
        add(op,title,dict(nodes=nodes,available_artifacts=["proof"] if available is None else available),dict(order=order or [],ready=ready or [],held=held or {},reason=reason),"HOLD" if reason else "PLANNING_PROJECTION")
    c("An empty obligation graph has no implied work",[],[],[])
    c("One completed node requires a present artifact",[n("a")],["a"],["a"])
    c("Independent nodes use deterministic lexical ordering",[n("b"),n("a")],["a","b"],["a","b"])
    c("A chain places every dependency before its consumer",[n("b",["a"]),n("a")],["a","b"],["a","b"])
    c("A diamond releases the join only after both parents",[n("d",["b","c"]),n("c",["a"]),n("b",["a"]),n("a")],["a","b","c","d"],["a","b","c","d"])
    c("A missing artifact prevents the claiming node from releasing",[n("a",artifacts=["missing"])],["a"],[],{"a":["MISSING_ARTIFACT"]})
    c("A held dependency propagates a separate downstream hold",[n("a",artifacts=["missing"]),n("b",["a"])],["a","b"],[],{"a":["MISSING_ARTIFACT"],"b":["DEPENDENCY_HELD"]})
    c("A two-node dependency cycle is refused",[n("a",["b"]),n("b",["a"])],reason="CYCLE")
    c("Self-dependency is a cycle",[n("a",["a"])],reason="CYCLE")
    c("An undeclared dependency cannot be silently treated as complete",[n("a",["missing"])],reason="MISSING_DEPENDENCY")
    c("Duplicate node identifiers are refused",[n("a"),n("a")],reason="DUPLICATE_NODE")
    c("Duplicate dependency declarations are refused",[n("a"),n("b",["a","a"])],reason="DUPLICATE_DEPENDENCY")
    c("Represented work cannot release an execution dependency",[n("a",disposition="represented")],["a"],[],{"a":["REPRESENTED_ONLY"]})
    c("An open evidence gap remains held",[n("a",disposition="open_gap")],["a"],[],{"a":["OPEN_GAP"]})
    c("An exact authority gate remains held despite a file",[n("a",disposition="exact_gate")],["a"],[],{"a":["EXACT_GATE"]})
    c("Completion without an artifact declaration is held",[n("a",artifacts=[])],["a"],[],{"a":["EVIDENCE_REQUIRED"]})
    c("Duplicate artifact inventory entries are refused",[n("a")],reason="DUPLICATE_ARTIFACT",available=["proof","proof"])
    bad=n("a");bad["authority"]=True
    c("Undeclared authority fields invalidate a node",[bad],reason="INVALID_NODE")
    c("An empty node label is refused",[n("")],reason="INVALID_NODE")
    c("Non-string dependency identifiers are refused",[n("a",[1])],reason="INVALID_NODE")

def annotation_cases():
    op="schema_annotation_quarantine"
    def c(title,schema,view,removed):
        add(op,title,dict(schema=schema),dict(assertion_view=view,quarantined_paths=removed,annotations_are_evidence=False),"STRUCTURAL_VIEW")
    for key,value in [("title","Sample"),("description","Approved"),("default",0),("examples",[1]),("deprecated",True),("readOnly",True),("writeOnly",True),("$comment","review note"),("contentEncoding","base64"),("contentMediaType","application/json")]:
        c("Quarantine the "+key+" annotation without executing its wording",{"type":"integer",key:value},{"type":"integer"},["/"+key])
    c("A property named description is still an instance field",{"properties":{"description":{"type":"string","description":"note"}}},{"properties":{"description":{"type":"string"}}},["/properties/description/description"])
    c("Definitions are visited as schema positions",{"$defs":{"a":{"title":"A","type":"number"}}},{"$defs":{"a":{"type":"number"}}},["/$defs/a/title"])
    c("Applicator array members are visited as schemas",{"allOf":[{"description":"A","type":"number"},{"minimum":0}]},{"allOf":[{"type":"number"},{"minimum":0}]},["/allOf/0/description"])
    c("Conditional schema branches are visited",{"if":{"title":"trigger","type":"integer"},"then":{"default":1,"minimum":0}},{"if":{"type":"integer"},"then":{"minimum":0}},["/if/title","/then/default"])
    c("An enum literal containing annotation-like keys remains data",{"enum":[{"description":"literal"}]},{"enum":[{"description":"literal"}]},[])
    c("A const literal containing annotation-like keys remains data",{"const":{"default":1}},{"const":{"default":1}},[])
    c("Required property names are never treated as annotation keywords",{"required":["description","default"]},{"required":["description","default"]},[])
    c("Boolean schemas retain their logical value",False,False,[])
    c("Unrecognized extension claims are quarantined in schema positions",{"type":"object","x-authority":"approved"},{"type":"object"},["/x-authority"])
    c("Resource identity and references retain resolution semantics",{"$id":"urn:sample:a","$ref":"#/$defs/a","$defs":{"a":{"type":"integer"}}},{"$id":"urn:sample:a","$ref":"#/$defs/a","$defs":{"a":{"type":"integer"}}},[])

def interference_cases():
    op="migration_interference"
    def c(title,lread,lwrite,rread,rwrite,conflicts=None,reason=None):
        add(op,title,dict(left=dict(reads=lread,writes=lwrite),right=dict(reads=rread,writes=rwrite)),dict(conflicts=sorted(conflicts or []),reason=reason,execution_permitted=False),"HOLD" if reason else "STATIC_CONFLICT_VIEW")
    c("Disjoint sibling writes have no declared overlap",[],["/a"],[],["/b"])
    c("Equal write targets conflict",[],["/a"],[],["/a"],["WRITE_WRITE"])
    c("An ancestor write overlaps a descendant write",[],["/a"],[],["/a/b"],["WRITE_WRITE"])
    c("A descendant write overlaps an ancestor write",[],["/a/b"],[],["/a"],["WRITE_WRITE"])
    c("A left write conflicts with a right read",[],["/a"],["/a"],[],["LEFT_WRITE_RIGHT_READ"])
    c("A right write conflicts with a left read",["/a"],[],[],["/a"],["RIGHT_WRITE_LEFT_READ"])
    c("Concurrent reads alone have no write conflict",["/a"],[],["/a"],[])
    c("The root write overlaps every descendant",[],[""],[],["/a"],["WRITE_WRITE"])
    c("A root read sees any descendant write",[""],[],[],["/a"],["RIGHT_WRITE_LEFT_READ"])
    c("String prefixes do not imply segment ancestry",[],["/a"],[],["/ab"])
    c("Escaped slash keeps a key separate from nested keys",[],["/a~1b"],[],["/a/b"])
    c("Escaped tilde is decoded once",[],["/a~0b"],[],["/a~0b"],["WRITE_WRITE"])
    c("Distinct array positions have distinct declared paths",[],["/a/0"],[],["/a/1"])
    c("A whole-array write overlaps an element reader",[],["/a"],["/a/0"],[],["LEFT_WRITE_RIGHT_READ"])
    c("Mixed access creates three distinct conflict classes",["/a"],["/a"],["/a"],["/a"],["WRITE_WRITE","LEFT_WRITE_RIGHT_READ","RIGHT_WRITE_LEFT_READ"])
    c("An empty access set has no hidden conflict",[],[],[],[])
    c("Non-pointer strings are refused",[],["a"],[],[],reason="INVALID_POINTER")
    c("Invalid tilde escapes do not enter overlap reasoning",[],["/a~3"],[],[],reason="INVALID_POINTER")
    c("Wildcard syntax is not silently interpreted",[],["/a/*"],[],[],reason="WILDCARD_UNSUPPORTED")
    c("Array insertion markers require expanded effects",[],["/a/-"],[],[],reason="ARRAY_SHIFT_SCOPE_REQUIRED")

def reader_cases():
    op="dual_reader_equivalence"
    def c(title,left,right,differences):
        add(op,title,dict(left=left,right=right),dict(differences=differences,equivalent=not differences,relation="LOCAL_TYPE_STRICT_JSON"),"SAMPLE_COMPARISON")
    def d(path,kind):return dict(path=path,kind=kind)
    c("Boolean true differs from integer one",True,1,[d("","TYPE")])
    c("An integer differs from a floating representation",1,1.0,[d("","TYPE")])
    c("Null is distinct from an absent field",{"a":None},{},[d("/a","LEFT_ONLY")])
    c("Unicode normalization is not silently applied","é","e\u0301",[d("","VALUE")])
    c("Array order remains significant",[1,2],[2,1],[d("/0","VALUE"),d("/1","VALUE")])
    c("Object key order does not affect this declared relation",{"a":1,"b":2},{"b":2,"a":1},[])
    c("Nested changed values have an exact path",{"a":{"b":1}},{"a":{"b":2}},[d("/a/b","VALUE")])
    c("A changed nested array item has an exact index",{"a":[1,2]},{"a":[1,3]},[d("/a/1","VALUE")])
    c("A right-only object key is reported",{}, {"a":1},[d("/a","RIGHT_ONLY")])
    c("A left-only object key is reported",{"a":1},{},[d("/a","LEFT_ONLY")])
    c("A scalar-to-object change is a root type difference",1,{},[d("","TYPE")])
    c("An empty list is distinct from an empty object",[],{},[d("","TYPE")])
    c("A slash in an object key is escaped in the difference path",{"a/b":1},{"a/b":2},[d("/a~1b","VALUE")])
    c("A tilde in an object key is escaped in the difference path",{"a~b":1},{"a~b":2},[d("/a~0b","VALUE")])
    c("An appended array tail is right-only",[1],[1,2],[d("/1","RIGHT_ONLY")])
    c("A removed array tail is left-only",[1,2],[1],[d("/1","LEFT_ONLY")])
    c("Equal nulls retain equality",None,None,[])
    c("Equal empty strings retain equality","","",[])
    c("String and numeric representations remain distinct","1",1,[d("","TYPE")])
    c("A boolean false differs from integer zero inside a record",{"a":False},{"a":0},[d("/a","TYPE")])

graph_cases()
annotation_cases()
interference_cases()
reader_cases()

def gmut_cases():
    op="gmut_dimension_migration"
    def c(title,value,source,target,converted=None,shape=None,uncertainty=None,converted_uncertainty=None,reason=None,family="scalar_tensor_eft",claim="representation"):
        payload=dict(value=value,source_unit=source,target_unit=target,shape=[] if shape is None else shape,uncertainty=uncertainty,model_family=family,claim=claim)
        add(op,title,payload,dict(value=converted,uncertainty=converted_uncertainty,reason=reason,empirical=False),"HOLD" if reason else "REPRESENTATION_ONLY","represented")
    c("Metre to centimetre scaling preserves an exact rational","1","m","cm","100",uncertainty="1/10",converted_uncertainty="10")
    c("Centimetre to metre scaling remains fractional","1","cm","m","1/100")
    c("Fractional seconds remain exact when expressed in milliseconds","1/3","s","ms","1000/3")
    c("Minute-to-second conversion uses the declared ratio","2","min","s","120")
    c("Kilogram-to-gram conversion preserves a fractional input","1/2","kg","g","500")
    c("Velocity conversion binds length and time dimensions together","36","km/h","m/s","10")
    c("Vector conversion preserves shape and sign",["1","-2"],"m","mm",["1000","-2000"],shape=[2])
    c("Matrix conversion preserves rectangular tensor structure",[["100","200"],["-50","0"]],"cm","m",[["1","2"],["-1/2","0"]],shape=[2,2])
    c("A different research family cannot inherit this conversion profile","1","m","m",reason="MODEL_FAMILY_OUTSIDE_PROFILE",family="unified_proof")
    c("Dimensionless scaling does not create physical meaning","-1/2","1","1","-1/2")
    c("Incompatible dimensions are refused before arithmetic","1","m","s",reason="DIMENSION_MISMATCH")
    c("An undeclared unit remains outside the finite vocabulary","1","pc","m",reason="UNKNOWN_UNIT")
    c("Affine temperature conversion is outside the scale-only profile","1","degC","K",reason="AFFINE_OUTSIDE_PROFILE")
    c("Ragged tensors do not receive a fabricated shape",[["1"],["2","3"]],"m","cm",shape=[2,1],reason="RAGGED_TENSOR")
    c("Declared shape must match observed nested structure",["1","2"],"m","cm",shape=[3],reason="SHAPE_MISMATCH")
    c("Boolean values are not rational strings",True,"m","cm",reason="RATIONAL_STRING_REQUIRED")
    c("A zero denominator is refused","1/0","m","cm",reason="INVALID_RATIONAL")
    c("Absent uncertainty remains unknown after unit conversion","2","m","cm","200",uncertainty=None,converted_uncertainty=None)
    c("Negative uncertainty is refused","1","m","cm",uncertainty="-1",reason="NEGATIVE_UNCERTAINTY")
    c("A requested empirical promotion blocks the conversion claim","1","m","cm",reason="EXTERNAL_CLAIM_HELD",claim="empirical_confirmation")

def claim_cases():
    op="claim_binding_join"
    binding=dict(artifact="synthetic/record.json",head="a"*40,owner="synthetic-owner",phase="synthetic-phase",scope="synthetic-sample",byte_domain="normalized_lf_git_blob",digest="b"*64,profile="schema-2020-12",evidence_class="same_owner_software")
    receipt=dict(binding=deepcopy(binding),state="passed",issued=10,expires=30,revoked=False,reviewer_class="same_owner",signature_evidence="absent",authority_scope="none",revocation_observed=True,approval_document=False,affected_party_evidence=False)
    def c(title,cl=None,rc=None,reason=None,disposition="open_gap",claim_kind="software"):
        claim=dict(binding=deepcopy(binding) if cl is None else cl,kind=claim_kind)
        add(op,title,dict(claim=claim,receipt=deepcopy(receipt) if rc is None else rc,observed=20),dict(binding_match=reason is None,reason=reason,authority_granted=False),"HOLD" if reason else "DECLARED_BINDING_MATCH",disposition)
    c("All declared bindings can match without conferring authority",disposition="completed")
    for key,new in [("artifact","synthetic/other.json"),("head","c"*40),("owner","different-owner"),("phase","different-phase"),("scope","different-sample"),("byte_domain","checkout_bytes"),("digest","d"*64),("profile","draft-07")]:
        cl=deepcopy(binding);cl[key]=new
        c("A changed "+key+" cannot borrow the old receipt",cl=cl,reason="BINDING_MISMATCH:"+key)
    rc=deepcopy(receipt);rc["expires"]=19
    c("An expired receipt cannot support a current structural join",rc=rc,reason="RECEIPT_EXPIRED")
    variants=[
        ("A failed receipt is not rehabilitated by an authority request","state","failed","RECEIPT_NOT_PASSED"),
        ("Revoked evidence remains unusable for a promoted claim","revoked",True,"RECEIPT_REVOKED"),
        ("An unobserved revocation state cannot be inferred fresh","revocation_observed",False,"REVOCATION_UNOBSERVED"),
        ("A future-issued receipt cannot justify present authority","issued",21,"RECEIPT_NOT_YET_ISSUED"),
        ("An authority request still lacks independent review","reviewer_class","same_owner","INDEPENDENT_REVIEW_ABSENT"),
        ("A reviewer label alone is not signature evidence","reviewer_class","external_declared","SIGNATURE_EVIDENCE_ABSENT"),
        ("A declared signature marker is not verified cryptographic evidence","signature_evidence","declared_only","INDEPENDENT_REVIEW_ABSENT"),
        ("An approval scope label cannot replace an approval document","authority_scope","requested_scope","INDEPENDENT_REVIEW_ABSENT"),
        ("A supplied-document flag does not establish affected-party approval","approval_document",True,"INDEPENDENT_REVIEW_ABSENT"),
        ("A synthetic affected-party flag does not grant competent authority","affected_party_evidence",True,"INDEPENDENT_REVIEW_ABSENT"),
    ]
    for title,key,value,reason in variants:
        rc=deepcopy(receipt);rc[key]=value
        c(title,rc=rc,reason=reason,disposition="exact_gate",claim_kind="reserved_authority")

gmut_cases()
claim_cases()

assert len(CASES)==200
assert len({(c['operation'],c['title']) for c in CASES})==200

# Pre-freeze semantic review: retain the four shadowed drafts, then refine the
# preceding declared conditions so each case reaches its named refusal.
SHADOWED_PLANNING_DRAFTS=deepcopy(CASES[196:200])
for offset,row in enumerate(CASES[196:200]):
    receipt=row['input']['receipt']
    receipt['reviewer_class']='external_declared'
    if offset>=1: receipt['signature_evidence']='verified_external_declared'
    if offset>=2: receipt['authority_scope']=receipt['binding']['scope']
    if offset==3:
        receipt['approval_document']=True
        receipt['approval_document_digest']='f'*64
    row['expected_output']['result']['reason']=[
        'SIGNATURE_NOT_VERIFIED','AUTHORITY_SCOPE_MISMATCH',
        'APPROVAL_DOCUMENT_UNBOUND','AFFECTED_PARTY_EVIDENCE_UNVERIFIED'][offset]
