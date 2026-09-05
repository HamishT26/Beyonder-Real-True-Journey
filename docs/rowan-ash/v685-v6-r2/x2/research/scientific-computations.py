"""Trusted finite scientific calculations for the current research note."""
import json
from pathlib import Path
import sympy as s
import numpy as np
from statsmodels.stats.multitest import multipletests
t=s.Symbol("t", real=True)
alpha=s.Function("alpha")(t);xi=s.Function("xi")(t)
expanded=s.diff(alpha*xi,t)
expected=s.diff(alpha,t)*xi+alpha*s.diff(xi,t)
j=np.array([2.,3.]);cov=np.array([[1.,.5],[.5,4.]])
variance=float(j@cov@j);diagonal_only=float(j@np.diag(np.diag(cov))@j)
p=np.array([.01,.04,.03])
out={
"schema":"ghc.family.rowan-remaster.scientific-calculations.v1",
"status":"PASS" if s.simplify(expanded-expected)==0 and variance==46 and diagonal_only==40 else "FAIL",
"variable_coupling":{"expanded":str(expanded),"expected":str(expected),"difference":str(s.simplify(expanded-expected)),"scope":"Trusted scalar flat-component illustration, not a covariant tensor derivation"},
"uncertainty":{"jacobian":j.tolist(),"covariance":cov.tolist(),"eigenvalues":np.linalg.eigvalsh(cov).tolist(),"propagated_variance":variance,"standard_uncertainty":float(np.sqrt(variance)),"diagonal_only_variance":diagonal_only,"omitted_covariance_error":variance-diagonal_only,"scope":"Synthetic two-variable first-order example"},
"multiplicity":{"raw":p.tolist(),"holm":multipletests(p,method="holm")[1].tolist(),"benjamini_hochberg":multipletests(p,method="fdr_bh")[1].tolist(),"scope":"Synthetic illustrative P values, no empirical population"},
"real_observations":0,"new_physical_laws":0,"universal_conjectures_solved":0,"independent_reproductions":0}
dest=Path(__file__).resolve().with_name("scientific-calculations.json")
dest.write_bytes((json.dumps(out,indent=2)+"\n").encode())
print(json.dumps(out))
