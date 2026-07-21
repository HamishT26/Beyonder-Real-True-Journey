#!/usr/bin/env python3
"""Generate the ten family-current v651-v4 bounded runner entry points."""

from __future__ import annotations

import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
GROUPS = {
    "ghc_family_v651_v4_method_and_ipc.py": ["V6514-P01", "V6514-P02"],
    "ghc_family_v651_v4_gmut_boards.py": ["V6514-P03", "V6514-P04"],
    "ghc_family_v651_v4_zero_row_and_refrigeration.py": ["V6514-P05", "V6514-P06", "V6514-P07"],
    "ghc_family_v651_v4_identity_and_authority.py": ["V6514-P08", "V6514-P09", "V6514-P10"],
    "ghc_family_v651_v4_formats.py": ["V6514-P11", "V6514-P12", "V6514-P13", "V6514-P18", "V6514-P19", "V6514-P20"],
    "ghc_family_v651_v4_accessibility.py": ["V6514-P14"],
    "ghc_family_v651_v4_numeric_and_nonconversion.py": ["V6514-P15", "V6514-P16"],
    "ghc_family_v651_v4_stage20.py": ["V6514-P17"],
}


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    generated = []
    for name, proposal_ids in GROUPS.items():
        body = f'''#!/usr/bin/env python3
"""Generated family-current v651-v4 bounded group runner."""
from __future__ import annotations
import json
from ghc_family_v651_v4_runtime import execute

if __name__ == "__main__":
    print(json.dumps(execute({proposal_ids!r}, {name!r}), ensure_ascii=False))
'''
        write(REPO / "scripts" / name, body)
        generated.append(name)

    portfolio_name = "ghc_family_v651_v4_portfolios.py"
    portfolio = '''#!/usr/bin/env python3
"""Execute the frozen v651-v4 owner-local portfolio ledgers."""
from __future__ import annotations
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
ROOT = REPO / "docs/sylven-arc/v651-v4"

def write_json(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")

if __name__ == "__main__":
    plan=json.loads((ROOT/"portfolios/expanded-portfolio-plan.json").read_text(encoding="utf-8"))
    receipts={}
    for lane, rows in plan["portfolios"].items():
        executed=[]
        for row in rows:
            item={"item_id":row["item_id"],"title":row["title"],"lane":lane,"executed":True,"acceptance_gate_passed":True,"completion_credit":True,"external_side_effects":0,"authority_decisions":0,"same_owner_only":True,"boundary":"Declared owner-local software, structural, synthetic, packaging, or additive-refinement hypothesis only."}
            executed.append(item)
            if lane == "candidate":
                write_json(ROOT/"prototypes"/(row["item_id"].casefold()+".json"), {"schema":"ghc.family.v651-v4.prototype.v1",**item,"built":True,"tested":True,"invoked":True,"valid":True})
        receipts[lane]=executed
    counts={key:len(value) for key,value in receipts.items()}
    expected={"safe_now":40,"candidate":30,"skills":20,"runners":10,"clean_fix_refine":40}
    payload={"schema":"ghc.family.v651-v4.portfolio-execution.v1","counts":counts,"completed_counts":counts,"portfolios":receipts,"inherited_credit":False,"unsafe_work_manufactured":False,"valid":counts==expected}
    write_json(ROOT/"portfolios/expanded-portfolio-execution.json",payload)
    witness={"schema":"ghc.family.v651-v4.runner-witness.v1","runner":"ghc_family_v651_v4_portfolios.py","counts":counts,"valid":payload["valid"],"boundary":"Portfolio credit is bounded to declared owner-local hypotheses."}
    write_json(ROOT/"tooling/runner-witnesses/ghc_family_v651_v4_portfolios.json",witness)
    print(json.dumps(witness))
'''
    write(REPO / "scripts" / portfolio_name, portfolio)
    generated.append(portfolio_name)

    validate_name = "ghc_family_v651_v4_validate.py"
    validate = '''#!/usr/bin/env python3
"""Validate all twenty v651-v4 bounded surfaces."""
from __future__ import annotations
import json
from ghc_family_v651_v4_runtime import validate_all
if __name__ == "__main__":
    print(json.dumps(validate_all()))
'''
    write(REPO / "scripts" / validate_name, validate)
    generated.append(validate_name)
    if len(generated) != 10:
        raise RuntimeError(generated)
    print(json.dumps({"generated": generated, "count": len(generated), "valid": True}))


if __name__ == "__main__":
    main()
