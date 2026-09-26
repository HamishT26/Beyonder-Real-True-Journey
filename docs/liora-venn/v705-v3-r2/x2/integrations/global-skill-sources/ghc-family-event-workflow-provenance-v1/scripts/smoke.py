from __future__ import annotations
import hashlib,json
record={"schema":"ghc.family.event-workflow.mega-smoke.v1","category":"provenance","states":["prepared","held"],"external_actions":0,"authority_actions":0}
payload=json.dumps(record,sort_keys=True,separators=(",",":")).encode("utf-8")
print(json.dumps({"ok":True,"category":"provenance","sha256":hashlib.sha256(payload).hexdigest(),"external_actions":0,"authority_actions":0}))
