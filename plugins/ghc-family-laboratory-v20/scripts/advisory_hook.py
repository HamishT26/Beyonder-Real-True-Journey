"""Five advisory hooks; no execution, networking, state mutation or task activation."""
import json,sys
MESSAGES={
 'source':'Use exact source commits and evidence-card digests. Preserve original outcomes and zero inherited domain credit. Read the current owner authority before acting.',
 'budget':'Workflow v20 uses caps, not old task minima. Record actual work and adaptive definitions. Keep each session within its caps and retain failures.',
 'consultation':'For each new authorized x1 and x2 session, send one advisory request to the existing Review and refine GHC Lab conversation using its private target record. Be patient with accepted requests; do independent work and never duplicate a pending message. This hook does not send it.',
 'roster':'Keep roster membership, scheduled turn and observed activity separate. A future row grants no early activation. Use one terminal successor edge only.',
 'evidence':'Catalogued, tested, installed and host-observed are different states. Numerical, empirical and authority claims remain distinct. Keep Method Flow separate from the baton.'
}
def evaluate(name,payload):
 if name not in MESSAGES:raise ValueError('unknown_hook')
 if not isinstance(payload,dict) or payload.get('hook_event_name')!='SessionStart':raise ValueError('unsupported_event')
 cwd=payload.get('cwd')
 if not isinstance(cwd,str) or len(cwd)>4096:raise ValueError('invalid_context')
 normalized=cwd.replace('\\','/').lower()
 if 'ghc-archives/worktrees/' not in normalized and 'ghc-family-laboratory' not in normalized:return {'continue':True}
 return {'continue':True,'hookSpecificOutput':{'hookEventName':'SessionStart','additionalContext':MESSAGES[name]}}
if __name__=='__main__':
 try:
  raw=sys.stdin.buffer.read(65537)
  if len(raw)>65536:raise ValueError('oversized_payload')
  print(json.dumps(evaluate(sys.argv[1],json.loads(raw.decode('utf-8')))))
 except Exception as error:
  # A malformed hook payload remains a refusal; it must never block ordinary work.
  print(json.dumps({'continue':True,'systemMessage':'GHC advisory hook refused malformed input: '+type(error).__name__}))
