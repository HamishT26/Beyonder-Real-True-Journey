# 06 Correction lineage and changed paths

## MF6862-N121 — one base snapshot has no correction links

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [],
  "snapshots": [
    {
      "v": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "corrections": 0,
  "tip": {
    "v": 1
  }
}
```

Observed result:

```json
{
  "corrections": 0,
  "tip": {
    "v": 1
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4b4ba6bb925f4d3f9c49a9e30e7fe6095e4e2e22dfc79ec9a7390263eabb8bec`, input digest `97af91901ab2b70772da7da8b638936af80a8446ea944a14c1489dc1e062c8d6`, and result digest `75ed8398db472a2c7e81601b26684684d8d3835abd790163f6319bfc768ec1a2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N122 — one additive correction binds its predecessor

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "ordinal": 1,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "corrections": 1,
  "tip": {
    "v": 2
  }
}
```

Observed result:

```json
{
  "corrections": 1,
  "tip": {
    "v": 2
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a30f08e283a8fb86191a6d04d3823a78862d40209bc2b530480ac719c57657d6`, input digest `7f3cfd16ad1149df7eae1bd9895d0cfd5773f11f01b520eb07db32fb930aa971`, and result digest `2ca2dd09e81fa47c822f1a90641172faa6438c8eb3b16dec2dc48bb8dd30db7a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N123 — two corrections retain both predecessor bindings

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "ordinal": 1,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": "Synthetic correction with retained predecessor."
    },
    {
      "child_sha256": "ff3acadf3b29fc4fa59d5b9612db39960c223344122be86dfaf4075be7c50279",
      "ordinal": 2,
      "parent_sha256": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 2
    },
    {
      "v": 3
    }
  ]
}
```

Frozen expected result:

```json
{
  "corrections": 2,
  "tip": {
    "v": 3
  }
}
```

Observed result:

```json
{
  "corrections": 2,
  "tip": {
    "v": 3
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `3ec945c6c714dd28bec082eb6e8e4f4ef1d2b4d2435dc4dea6f390e49836d1f3`, input digest `849c404d3b63ccb9717cefc929f451fda3342857123ea0f71074650e5f0ff2b2`, and result digest `7c85c53032d758862d0cb1e1b32f318d42356679cab0eaf81c58eb43a4c3e676`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N124 — stale parent digest is rejected

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "ordinal": 1,
      "parent_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "parent_digest_mismatch"
}
```

Observed result:

```json
{
  "error": "parent_digest_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2074f625f819baf4a63ad4d6ba0b7e058584ab4353aac42fa15ad4f9345d711b`, input digest `fff998958c5f4b1f7317713911ba0457aad549ba122f3c17d94ee95337fec644`, and result digest `1cbc956ad99ee279194d222d68576324d14c0a867b4eb84d99b0d69054104b6c`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N125 — wrong child digest is rejected

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
      "ordinal": 1,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "child_digest_mismatch"
}
```

Observed result:

```json
{
  "error": "child_digest_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `91c14fb29d7cb9a960025e333a1c076e953d3385b2121e526d62719f41a8157e`, input digest `f7ceb286abd5d2dac55c6e7baf518169945feafb5bf3d611abe1128948e361a7`, and result digest `920e31c3e30969f6beeb4ce8ae85ef4081ec5d340d7b2fcb55ccf9435e8711d8`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N126 — a correction cannot skip its ordinal

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "ordinal": 2,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "ordinal_mismatch"
}
```

Observed result:

```json
{
  "error": "ordinal_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `8a7e5ac27e7e0d6497e4e8d6be85cfd8151b355e5004888f8de660bcbdf88677`, input digest `077a6b5cf0b0efbd294bea77f02c6e5b272fc30b3cda385ed8fa0493cc29b5a0`, and result digest `e62263e6c58e82b2a071a021edd4e9e9bcae6634ccd293b6625abfec25992d89`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N127 — a correction needs a visible reason

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "ordinal": 1,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": " "
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_reason"
}
```

Observed result:

```json
{
  "error": "missing_reason"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `20fba21229ef3dd08c890bed3df3552feb6caecc9c4b5cb9e6ab90ed89390115`, input digest `32844e789eb50ba94c8278f46ec96b7363994a7aff89a938c246aab253ce3316`, and result digest `2fb89da62dba19a81a11f12689c350ee2c04b807785abfc95fbdcb49ffd736fa`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N128 — a vacant snapshot chain does not invent a base

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [],
  "snapshots": []
}
```

Frozen expected result:

```json
{
  "error": "empty_chain"
}
```

Observed result:

```json
{
  "error": "empty_chain"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `b2ec8801b3f7fc99a97163a0a5bb40956396ec69ddd0d9dfe4d74bdad49edc2c`, input digest `74447225d205257f9d13454dc04086fc93835cbf76510e7bfa803f87b2746ee9`, and result digest `823855f0eda1898e6bbf822a4801d3c7e8f3f0e6b51a987a80bb6411ea77b7dd`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N129 — extra correction link is rejected

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
      "ordinal": 1,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "link_count_mismatch"
}
```

Observed result:

```json
{
  "error": "link_count_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `cd158ecfc232cbf2f80d17b9b377ba5bf8abfec71965fe491aaff61ef495aead`, input digest `719ab8799c90c1799a959213abde9021d9e17877da0612fc5a33dd961c71e18c`, and result digest `7467655214d90ac7dcd61e4d737ef072af617862e3023d0d42391ef610a4f8b4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N130 — identical child snapshot is retained as explicit no-op

Family `correction_digest_lineage`; operation `chain`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Bind a sequence of immutable synthetic snapshots by exact ordinal, parent digest, and reason.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "ordinal": 1,
      "parent_sha256": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "reason": "Synthetic correction with retained predecessor."
    }
  ],
  "snapshots": [
    {
      "v": 1
    },
    {
      "v": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "corrections": 1,
  "tip": {
    "v": 1
  }
}
```

Observed result:

```json
{
  "corrections": 1,
  "tip": {
    "v": 1
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4526705e49f1ae3a6e5e7a3fe1b08673ab240b58ba81320c352e48007115fb15`, input digest `c913b2243e4225e96282ff9e5974bc214fab5c7fe350fc136d92d8fffcf157b8`, and result digest `f3d489470a23b6a57d528199bdd4eae7c983e90a71bdc44573f5f1af856e0ae8`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N131 — unchanged object has no changed paths

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a": 1
  },
  "before": {
    "a": 1
  }
}
```

Frozen expected result:

```json
[]
```

Observed result:

```json
[]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `3e12510cac7bbb6df9b2f84c29d23e049cd5c5e3c9bdec6a3121bddb4a78b01e`, input digest `e1cf6c23dedf959de3e0e2f426e15735fadb818afccc7d3b5fc10c6226a14347`, and result digest `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N132 — one nested scalar change identifies its leaf

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a": {
      "b": 2
    }
  },
  "before": {
    "a": {
      "b": 1
    }
  }
}
```

Frozen expected result:

```json
[
  "/a/b"
]
```

Observed result:

```json
[
  "/a/b"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `46ac984ead650418a17f33f0d798937ceb864f90c3b51352277d5f068823b15b`, input digest `fbf805731fa9870882796a3885a4e1c34d7a6efbc6006ef33871922c9d173f51`, and result digest `66f6f27ca6324d85a14199f2acf2c8c11cf7d28c9a9f7c98be99ebc60c434945`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N133 — added member identifies the added path

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a": 1
  },
  "before": {}
}
```

Frozen expected result:

```json
[
  "/a"
]
```

Observed result:

```json
[
  "/a"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `9724eee2a3e4c37c1317679fc853a935a623cfd2a09c7a0f532d44bee07df011`, input digest `4ec783f66961476fc25fc8da6d87b90fbefaad213a34682c80d7054a1f9319ce`, and result digest `0e17f6e6bd49eea9fdbc2a5a81225a8347ec40087e6a28352b28cc6f0667a881`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N134 — removed member identifies its former path

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {},
  "before": {
    "a": 1
  }
}
```

Frozen expected result:

```json
[
  "/a"
]
```

Observed result:

```json
[
  "/a"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `f5c14d4d534092558d6ba64dad48bbb3fb3c57eb040862034042b1defe44b346`, input digest `e47e433df179b2828fc89923cba19482a73ee105dc5e447b7817a7bc6f9a9792`, and result digest `0e17f6e6bd49eea9fdbc2a5a81225a8347ec40087e6a28352b28cc6f0667a881`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N135 — equal-length array change identifies its index

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": [
    1,
    3
  ],
  "before": [
    1,
    2
  ]
}
```

Frozen expected result:

```json
[
  "/1"
]
```

Observed result:

```json
[
  "/1"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4fd65c56b496bd4abc392e018cfc1c571cd1254747fc212ff70f11553809e732`, input digest `e6f61c10bd5487dcad3083773de5ad7fe3a851c75a253916a000794054aee4ee`, and result digest `7c4adecbbf7a7d15a2d49f129a6b703813f7db6ad5b3248b0586991071abbec1`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N136 — array length change identifies the array itself

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a": [
      1,
      2
    ]
  },
  "before": {
    "a": [
      1
    ]
  }
}
```

Frozen expected result:

```json
[
  "/a"
]
```

Observed result:

```json
[
  "/a"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `fe7a898672e6aa75f9de7ec74538d5b54660b993993c4b48e05c5cc695176bad`, input digest `e8d14127b86222956c12fab1264a0cf3b8db7aff4c5ecd0d27d539f1d3f83262`, and result digest `0e17f6e6bd49eea9fdbc2a5a81225a8347ec40087e6a28352b28cc6f0667a881`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N137 — boolean to number is an explicit type change

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": 0,
  "before": false
}
```

Frozen expected result:

```json
[
  ""
]
```

Observed result:

```json
[
  ""
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `359e982ecc6e194b111b4d1959b846c845597138de2138dd33e2866c483c9ef1`, input digest `2d708d6319945efecd2eaad3488f764b96b5270e9f0a8cb1b0629e8c4c626844`, and result digest `055539df4a0b804c58caf46c0cd2941af10d64c1395ddd8e50b5f55d945841e6`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N138 — escaped member path remains reconstructable

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a/b": 2
  },
  "before": {
    "a/b": 1
  }
}
```

Frozen expected result:

```json
[
  "/a~1b"
]
```

Observed result:

```json
[
  "/a~1b"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `8bd3dfabf88515b1035b39a346216f2e4af0a81f5a6dad0b9d7a3fbbf42605f2`, input digest `013acd628b832fb5a37c0bc1987d059fa256b536219d0f12ff90d05af01063f9`, and result digest `dfbe9594bb4b002df4d21f65467c42a8b494fecce35999a8cbb3c0e091fdbfff`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N139 — multiple changed paths sort deterministically

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a": 2,
    "z": 2
  },
  "before": {
    "a": 1,
    "z": 1
  }
}
```

Frozen expected result:

```json
[
  "/a",
  "/z"
]
```

Observed result:

```json
[
  "/a",
  "/z"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `11d2f1a01d81900063cf8c2224d1b15856bf01e99122370e09241d43152568a4`, input digest `e1434a7beadd1c7607f0896df8967cb808733a2014f7b500ecc9c850aa12bea5`, and result digest `0fa338fcf6741b688a50126ddd5bf4d9fc41495d3af896bd742a61874edcc5c7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N140 — container to scalar change is recorded at the parent

Family `correction_changed_paths`; operation `changes`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Enumerate exact changed JSON pointers, using one array path for structural length changes.

Frozen input:

```json
{
  "after": {
    "a": 4
  },
  "before": {
    "a": {
      "b": 1
    }
  }
}
```

Frozen expected result:

```json
[
  "/a"
]
```

Observed result:

```json
[
  "/a"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `24352ae9e71c93b1b05aa49bbe1281f26d7fe57cd5297cfe92e32fa7e8496634`, input digest `253deb5d17828a676f7f32d0016ce930c3b2dd3ef723ca3af938fe54a61b9ccc`, and result digest `0e17f6e6bd49eea9fdbc2a5a81225a8347ec40087e6a28352b28cc6f0667a881`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.
