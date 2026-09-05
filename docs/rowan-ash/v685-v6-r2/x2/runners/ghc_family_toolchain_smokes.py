"""Exercise the ten new Python libraries using trusted offline fixtures."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import math

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    rows=[]
    def record(name,good,bad,detail):
        rows.append({"package":name,"version":importlib.metadata.version(name),
                     "positive_pass":bool(good),"adverse_rejected":bool(bad),"detail":detail,
                     "network_retrievals":0,"independent_reproduction":False})
    import sympy as sp
    t=sp.Symbol("t", real=True); alpha=t*t; xi=t**3
    deriv=sp.diff(alpha*xi,t)
    correct=sp.diff(alpha,t)*xi+alpha*sp.diff(xi,t)
    wrong=alpha*sp.diff(xi,t)
    record("sympy",sp.simplify(deriv-correct)==0,sp.simplify(deriv-wrong)!=0,"Variable-coupling product rule with its omitted-derivative counterexample")
    import mpmath as mp
    with mp.workdps(50):
        exact=mp.mpf(1)/10
        recovered=(mp.mpf("1e30")+exact)-mp.mpf("1e30")
        record("mpmath",abs(recovered-exact)<mp.mpf("1e-20"),abs(mp.mpf(float(1e30)+.1)-mp.mpf(1e30)-exact)>mp.mpf(".09"),"High-precision cancellation compared with a binary64 counterexample")
    import scipy.integrate as si
    import scipy.optimize as so
    value,error=si.quad(math.sin,0,math.pi)
    rejected=False
    try: so.root_scalar(lambda x:x*x+1,bracket=[-1,1])
    except ValueError: rejected=True
    record("scipy",abs(value-2)<1e-12 and error<1e-10,rejected,"Quadrature of sine and refusal of a root bracket with no sign change")
    import numpy as np
    import statsmodels.api as sm
    x=np.arange(10,dtype=float); X=sm.add_constant(x); y=1+2*x
    fit=sm.OLS(y,X).fit(); rejected=False
    try: sm.OLS(y[:-1],X)
    except ValueError: rejected=True
    record("statsmodels",np.allclose(fit.params,[1,2],rtol=0,atol=1e-12),rejected,"Trusted linear regression and mismatched sample dimensions")
    from rdflib import Graph, Namespace, Literal
    from rdflib.namespace import RDF, XSD
    g=Graph().parse(data='@prefix ex: <urn:example:> . ex:a ex:p 3 .',format="turtle"); rejected=False
    try: Graph().parse(data='@prefix ex: <urn:example:> . ex:a ex:p [',format="turtle")
    except Exception: rejected=True
    record("rdflib",len(g)==1,rejected,"Inline Turtle parsing and malformed syntax; no location argument")
    from pyld import jsonld
    loader_calls=[]
    def offline_loader(url, options=None):
        loader_calls.append(url)
        raise ValueError("Context not in the offline allowlist")
    obj={"@context":{"label":"urn:example:label"},"@id":"urn:example:a","label":"sample"}
    expanded=jsonld.expand(obj,options={"documentLoader":offline_loader})
    rejected=False
    try: jsonld.expand({"@context":"urn:example:unknown-context","label":"sample"},options={"documentLoader":offline_loader})
    except jsonld.JsonLdError: rejected=True
    record("PyLD",expanded[0]["urn:example:label"][0]["@value"]=="sample",rejected and len(loader_calls)==1,"Inline JSON LD expansion and offline rejection of an unknown context; zero network calls")
    from pyshacl import validate
    shapes=Graph().parse(data='''@prefix ex: <urn:example:> .
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
ex:Shape a sh:NodeShape ; sh:targetNode ex:a ;
sh:property [ sh:path ex:age ; sh:datatype xsd:integer ; sh:minCount 1 ] .''',format="turtle")
    valid=Graph().parse(data='@prefix ex: <urn:example:> . ex:a ex:age 20 .',format="turtle")
    invalid=Graph().parse(data='@prefix ex: <urn:example:> . ex:a ex:age "twenty" .',format="turtle")
    opts=dict(shacl_graph=shapes,advanced=False,js=False,do_owl_imports=False,inference="none")
    record("pyshacl",validate(valid,**opts)[0],not validate(invalid,**opts)[0],"SHACL integer constraint and its string-valued counterexample with imports and JS disabled")
    from prov.model import ProvDocument
    doc=ProvDocument();doc.add_namespace("ex","urn:example:")
    doc.entity("ex:e");doc.activity("ex:a");doc.wasGeneratedBy("ex:e","ex:a")
    parsed=ProvDocument.deserialize(content=doc.serialize(format="json"),format="json")
    rejected=False
    try: ProvDocument().entity("unregistered:name")
    except Exception: rejected=True
    record("prov",len(list(parsed.get_records()))==3,rejected,"Provenance serialization roundtrip and an unregistered namespace")
    import rfc8785
    canonical=rfc8785.dumps({"b":2,"a":1});rejected=False
    try: rfc8785.dumps({"x":float("nan")})
    except rfc8785.CanonicalizationError: rejected=True
    record("rfc8785",canonical==b'{"a":1,"b":2}',rejected,"Canonical object order and nonfinite-number refusal")
    import msgspec
    class Sample(msgspec.Struct):
        count:int
    dec=msgspec.json.Decoder(Sample);rejected=False
    try: dec.decode(b'{"count":"three"}')
    except msgspec.ValidationError: rejected=True
    record("msgspec",dec.decode(b'{"count":3}').count==3,rejected,"Typed decoding and a wrong-type counterexample")
    out={"schema":"ghc.family.python-toolchain-smokes.v1","status":"PASS" if all(r["positive_pass"] and r["adverse_rejected"] for r in rows) else "FAIL","rows":rows,"direct_packages":len(rows),"scientific_discovery_credit":0}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes((json.dumps(out,indent=2)+"\n").encode())
    print(json.dumps(out))
    return out["status"]!="PASS"

if __name__=="__main__":
    raise SystemExit(main())
