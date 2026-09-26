from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
X1=Path(__file__).resolve().parents[1]; scripts=sorted((X1/"skills").glob("*/scripts/smoke.py")); passed=0
for script in scripts:
    result=subprocess.run([sys.executable,str(script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    passed += result.returncode==0
print(json.dumps({"runner":"skill","passed":passed,"total":len(scripts)}))
raise SystemExit(0 if len(scripts)==10 and passed==10 else 1)
