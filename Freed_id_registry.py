"""
     2 freed_id_registry.py
     3 ====================
     4
     5 Minimal in-memory Freed ID registry implementation.
     6 """
     7
     8 from dataclasses import dataclass, field
     9 from typing import Dict, List, Optional
    10 import uuid
    11
    12 from freed_id_audit_log import FreedIDAuditLedger
    13 from freed_id_minimum_disclosure import (
    14     MinimumDisclosurePolicy,
    15     build_minimum_disclosure_presentation,
    16 )
    17
    18
    19 @dataclass
    20 class DIDDocument:
    21     """A simplified representation of a Freed ID DID Document."""
    22
    23     did: str
    24     controller: str
    25     verification_methods: List[Dict[str, str]] = field(default_factory=list)
    26     services: List[Dict[str, str]] = field(default_factory=list)
    27     revoked: bool = False
    28
    29     def to_dict(self) -> Dict[str, object]:
    30         return {
    31             "@context": "https://www.w3.org/ns/did/v1",
    32             "id": self.did,
    33             "controller": self.controller,
    34             "verificationMethod": self.verification_methods,
    35             "service": self.services,
    36             "revoked": self.revoked,
    37         }
    38
    39
    40 class FreedIDRegistry:
    41     """A simple in-memory registry for Freed ID DID Documents."""
    42
    43     def __init__(self, audit_ledger_path: Optional[str] = None) -> None:
    44         self._store: Dict[str, DIDDocument] = {}
    45         self._audit_ledger = (
    46             FreedIDAuditLedger(audit_ledger_path) if audit_ledger_path else None
    47         )
    48
    49     def _audit(self, action: str, did: str, details: Optional[Dict[str, object]] = None) -> None:
    50         if self._audit_ledger is None:
    51             return
    52         self._audit_ledger.append(action=action, did=did, details=details or {})
    53
    54     def _generate_did(self) -> str:
    55         return f"did:freed:{uuid.uuid4().hex}"
    56
    57     def register(self, doc: DIDDocument) -> str:
    58         did = doc.did or self._generate_did()
    59         if did in self._store and not self._store[did].revoked:
    60             raise ValueError(f"DID {did} already exists and is active")
    61         doc.did = did
    62         self._store[did] = doc
    63         self._audit(
    64             "register",
    65             did,
    66             {
    67                 "controller": doc.controller,
    68                 "verification_method_count": len(doc.verification_methods),
    69                 "service_count": len(doc.services),
    70             },
    71         )
    72         return did
    73
    74     def resolve(self, did: str) -> Optional[DIDDocument]:
    75         return self._store.get(did)
    76
    77     def update(self, did: str, new_doc: DIDDocument) -> None:
    78         if did not in self._store or self._store[did].revoked:
    79             raise KeyError(f"DID {did} does not exist or is revoked")
    80         if did != new_doc.did:
    81             raise ValueError("DID mismatch in update")
    82         self._store[did] = new_doc
    83         self._audit(
    84             "update",
    85             did,
    86             {
    87                 "verification_method_count": len(new_doc.verification_methods),
    88                 "service_count": len(new_doc.services),
    89             },
    90         )
    91
    92     def revoke(self, did: str) -> None:
    93         doc = self._store.get(did)
    94         if not doc:
    95             raise KeyError(f"DID {did} does not exist")
    96         doc.revoked = True
    97         self._audit("revoke", did, {"revoked": True})
    98
    99     def list_active(self) -> List[str]:
   100         return [did for did, doc in self._store.items() if not doc.revoked]
   101
   102     def issue_credential(self, did: str, credential: Dict[str, object]) -> None:
   103         doc = self._store.get(did)
   104         if not doc or doc.revoked:
   105             raise KeyError(f"DID {did} does not exist or is revoked")
   106         credential_id = f"{did}#cred-{len(doc.services)}"
   107         doc.services.append(
   108             {
   109                 "id": credential_id,
   110                 "type": "FreedIDCredential",
   111                 "credential": credential,
   112             }
   113         )
   114         self._audit(
   115             "issue_credential",
   116             did,
   117             {
   118                 "credential_id": credential_id,
   119                 "credential_keys": sorted(str(key) for key in credential.keys()),
   120             },
   121         )
   122
   123     def verify_credential(self, did: str, credential_id: str) -> bool:
   124         doc = self._store.get(did)
   125         if not doc or doc.revoked:
   126             return False
   127         return any(s.get("id") == credential_id for s in doc.services)
   128
   129     def build_credential_presentation(
   130         self,
   131         did: str,
   132         credential_id: str,
   133         requested_fields: List[str],
   134         policy: MinimumDisclosurePolicy,
   135     ) -> Dict[str, object]:
   136         doc = self.resolve(did)
   137         if not doc:
   138             raise KeyError(f"DID not found: {did}")
   139
   140         credential_service = next(
   141             (s for s in doc.services if s.get("id") == credential_id), None
   142         )
   143         if not credential_service:
   144             raise KeyError(f"Credential not found: {credential_id}")
   145
   146         claims = credential_service.get("credential", {})
   147         if not isinstance(claims, dict):
   148             raise TypeError("claims must be a dict")
   149
   150         self._audit(
   151             "build_presentation",
   152             did,
   153             {
   154                 "credential_id": credential_id,
   155                 "requested_fields": requested_fields,
   156             },
   157         )
   158         return build_minimum_disclosure_presentation(
   159             subject_did=did,
   160             credential_id=credential_id,
   161             claims=claims,
   162             requested_fields=requested_fields,
   163             policy=policy,
   164         )
