# 07 Receipt scope manifest and disclosure

Leaf selection is a structural disclosure proxy. It is not a cryptographic selective-disclosure proof or production credential presentation.

## MF6862-N141 — exact declared scope binds a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
true
```

Observed result:

```json
true
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `0f282c056f98559de9fd8c54885c887859c00f47bf2ee66f0e332c6fa7eab789`, input digest `585756033e0c82600851d35d4d1de436646da797e67a1f4144d976139f61fd1e`, and result digest `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N142 — mismatched owner does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "other-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `03ab7636c0076f53c52a5868205279193634c0574b2183015a4488aa34f8610f`, input digest `4f9203d012152c3b529e340ba891cd53bca4e48ed6769b5a1879c50e6c2a451d`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N143 — mismatched source does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "dddddddddddddddddddddddddddddddddddddddd",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4538222c94b33087295d7e9d987ee9499b96619e3a39de91ffc20689affc0ce1`, input digest `1ad07f99339f64187612550bf6c2419d10cd3bb1f54eae1ee27bcb5d195c4fab`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N144 — mismatched head does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "dddddddddddddddddddddddddddddddddddddddd",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d10d9bd4d4d3ed4b6ea6923be3ea31c27cdef3096401b544114357276badcc9a`, input digest `92fbdd7f9ea9ec33f171121c31b6041b45b0815c8cbbe4f5b7020d6100ca3628`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N145 — mismatched tree does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "dddddddddddddddddddddddddddddddddddddddd"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `c0fa6db476a9b8ed4f899b232f89ee9251c7c8fe7db408c3860b398721e3f28a`, input digest `783dee93369f865220c66d808d6b8f5dc5760d5c44dc55df8dad6edcadf6b975`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N146 — mismatched phase does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "other-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7fe2075090083a37af037f6a58dc11046873b11f582bb10233e404b39d0d028e`, input digest `e4dc116ab34708daa085c6d9899a63760ea5cc6526174e3b18be37bea48015ed`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N147 — mismatched same_owner_only does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": false,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `b3c626fac98230ccf7e7910133204f7b6369d9d390ec90e488a15470ca36b869`, input digest `573f1c11013a7cc015e03dbb3c0ce961244792171e093ea01b66aae485587d6e`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N148 — mismatched independent_reproduction does not bind a receipt

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": true,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `9087752113b19276de49bee92198994c764a00e9e4c61134487941762e557577`, input digest `4600f101745556b678f5f6def193c44eb2b6993c3779fffe62639cde59b2d238`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N149 — missing tree cannot inherit a default

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `c49ecbf718805df71f9c8bac536bd7a0225bb7ad0e055ef86ef45eefe28e1445`, input digest `f90fb7f6c7583061fd9ee1720b829f34bc3300980abe2d054806f54ae0bd8ee2`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N150 — extra authority claim is outside the receipt schema

Family `receipt_exact_scope`; operation `scope`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Compare complete declared owner/source/head/tree bindings without transferring any authority.

Frozen input:

```json
{
  "expected": {
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  },
  "receipt": {
    "authority": true,
    "head": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "independent_reproduction": false,
    "owner": "synthetic-owner",
    "phase": "synthetic-phase",
    "same_owner_only": true,
    "source": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "tree": "cccccccccccccccccccccccccccccccccccccccc"
  }
}
```

Frozen expected result:

```json
{
  "error": "scope_mismatch"
}
```

Observed result:

```json
{
  "error": "scope_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d96c094db961813ac8a836ef022b43e0420f33a96da5b6abbb818ef718ede787`, input digest `ce58bfdfb319de2501b0f7b0d79be4a61395e9d274d0db56b9557cb733ff4c72`, and result digest `e8a539f09a6419e7d5f2b5847544ec6d5ef2e4348a281ff38214079c85c2d766`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N151 — one literal path binds its declared bytes

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 2,
      "path": "a.json",
      "sha256": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    }
  ],
  "files": {
    "a.json": "{}"
  }
}
```

Frozen expected result:

```json
true
```

Observed result:

```json
true
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `aa74b07254cf8b0c1d9d5c916d8137c1f3ce804d9015908392fa523cc8fa8adc`, input digest `36c3b4c60c68a53f657b4bd2736f319220c79010fdf47be939f9127f8df3ab86`, and result digest `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N152 — two same-content paths remain two manifest entries

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "a",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    },
    {
      "bytes": 1,
      "path": "b",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }
  ],
  "files": {
    "a": "x",
    "b": "x"
  }
}
```

Frozen expected result:

```json
true
```

Observed result:

```json
true
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `38bcc71fe348c01d351c82e071bb49d8bddc32b8205b30fcd82187c4ea6c1970`, input digest `f2c89cdd79c5effcf6a1ec97d1a8787cfe1ce92d672380ef7617f00d8afdb329`, and result digest `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N153 — empty manifest is explicit and contains no inferred files

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [],
  "files": {}
}
```

Frozen expected result:

```json
true
```

Observed result:

```json
true
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `53b37c7db0cd05b5aa7c8e80d97d763c3752eeb9126fb9c1ae26f6ba474a7456`, input digest `957bf9bed621db370e8b043f52b16f24fd527742ce2f90c6954277202582a674`, and result digest `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N154 — wrong content digest rejects an entry

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "a",
      "sha256": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  ],
  "files": {
    "a": "x"
  }
}
```

Frozen expected result:

```json
{
  "error": "digest_mismatch"
}
```

Observed result:

```json
{
  "error": "digest_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `17b895a1afedfbd25128a8fffc5f99dc7d15cf7056f743b70b2045a912785c69`, input digest `09e020d6895deb8fa8446e39b871a8407d3f53dd9b55476720fbc6a5f71074cb`, and result digest `ab2b55bc99d08738a9bd96309df469733f82e13455ccfc3236c27653c19cae70`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N155 — wrong byte length rejects an entry

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 3,
      "path": "a",
      "sha256": "4a99557e4033c3539de2eb65472017cad5f9557f7a0625a09f1c3f6e2ba69c4c"
    }
  ],
  "files": {
    "a": "é"
  }
}
```

Frozen expected result:

```json
{
  "error": "size_mismatch"
}
```

Observed result:

```json
{
  "error": "size_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7195796f477b92aaf362449e879b0ad0bf5ebc3d3579131fa140a054042e37ec`, input digest `bc164c1f3b6c2c4f5c648ef2bbbd3a82285456bd83fe511599dae1d474e73e3c`, and result digest `6a1b83041daafeaff9a9b6b61b7bcf2efbce1f4c94693e6ef0791ad590a6c2be`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N156 — duplicate path refuses manifest ambiguity

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "a",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    },
    {
      "bytes": 1,
      "path": "a",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }
  ],
  "files": {
    "a": "x"
  }
}
```

Frozen expected result:

```json
{
  "error": "duplicate_path"
}
```

Observed result:

```json
{
  "error": "duplicate_path"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `fed3b3b5be1d8f23eb65c11740c7b4427bf07ddf82a8c3ed150eb1fdebca2ec2`, input digest `021e479fbd25d24f022bc51aefb2fcf98014cd79949867030fc0a7cc283e92fc`, and result digest `f945c0555ae28c809c766efaee41b1d98dfa8e7cb700bb8dec0bcaa1019cd617`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N157 — parent traversal path is rejected

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "../a",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }
  ],
  "files": {
    "../a": "x"
  }
}
```

Frozen expected result:

```json
{
  "error": "unsafe_path"
}
```

Observed result:

```json
{
  "error": "unsafe_path"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2f0ed5b808176c446a057fec6edf94890172a5d1b4319b4ae79538a969557854`, input digest `b37634e35cd89e9d4f2569a3c2c6fe97ea0debf5f8bee1fa07e22b6836dff1ee`, and result digest `80c5a4158ff1ee348176df18af89b31d0578a9f870365de3eb8037e8862f8e32`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N158 — absolute POSIX path is rejected

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "/a",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }
  ],
  "files": {
    "/a": "x"
  }
}
```

Frozen expected result:

```json
{
  "error": "unsafe_path"
}
```

Observed result:

```json
{
  "error": "unsafe_path"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2536a06e4ce6ff6daf32821906e11945b72582941e6c8548d9ee90a12ccaa9de`, input digest `629a530f2a47310a641ef37a372524f03e71f033953618377d9892532303ed0a`, and result digest `80c5a4158ff1ee348176df18af89b31d0578a9f870365de3eb8037e8862f8e32`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N159 — backslash path is outside the portable manifest domain

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "a\\b",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }
  ],
  "files": {
    "a\\b": "x"
  }
}
```

Frozen expected result:

```json
{
  "error": "unsafe_path"
}
```

Observed result:

```json
{
  "error": "unsafe_path"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `24f34822aa1eeec09745ba40768b9b2700072c46e1ec9217aae5f71ebaaeab44`, input digest `29d50abdb3f1d0c3dc5adb27fbad5d6875b214882bb8ce110fcaf702ea921dd4`, and result digest `80c5a4158ff1ee348176df18af89b31d0578a9f870365de3eb8037e8862f8e32`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N160 — unlisted file prevents full manifest coverage

Family `manifest_literal_paths`; operation `manifest`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Validate explicit relative POSIX file names, exact sizes and digests without filesystem traversal.

Frozen input:

```json
{
  "entries": [
    {
      "bytes": 1,
      "path": "a",
      "sha256": "2d711642b726b04401627ca9fbac32f5c8530fb1903cc4db02258717921a4881"
    }
  ],
  "files": {
    "a": "x",
    "b": "y"
  }
}
```

Frozen expected result:

```json
{
  "error": "coverage_mismatch"
}
```

Observed result:

```json
{
  "error": "coverage_mismatch"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `10ff268eda8167b70feef7dcafb3a3196f36cd23e4c7613522c9ad63b3c19a67`, input digest `f1bdc5baaede9d9dfaf034fc5c96c77135540c8560c78254ab992bc43f5b5865`, and result digest `92313fd742aef5f438f4c61fcf97075a02e969e6cf0036a16cfff3373bb9eb78`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N161 — one scalar disclosure stays within its budget

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 1,
  "document": {
    "a": 1,
    "b": 2
  },
  "pointers": [
    "/a"
  ]
}
```

Frozen expected result:

```json
{
  "/a": 1
}
```

Observed result:

```json
{
  "/a": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4071a5f45d94150f5bdf5bb611623eac3e62ce02378cf24edb696a5f798391a2`, input digest `46905bb9904ca649d9a10c270b20ff3ea8a2d29bf23c932f3a4ac380ed59354b`, and result digest `fe3ed7c1a13485350e1b0a199077b6cebfc1d030743fe8da8da5d97f15bf8cc0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N162 — two scalar selections use two budget units

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 2,
  "document": {
    "a": 1,
    "b": 2
  },
  "pointers": [
    "/a",
    "/b"
  ]
}
```

Frozen expected result:

```json
{
  "/a": 1,
  "/b": 2
}
```

Observed result:

```json
{
  "/a": 1,
  "/b": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d498817200b59431c89e98e7d27129942d18c19fd2031f338d72bb3d6f1eb848`, input digest `40b8a09da962f736eca6005d83ef3f3e476f7a6e9497eb4c20722732004f4bcf`, and result digest `f97e7e7c983bdcde3525be85f46568cfb5b0c8135d1bd48540a7b2fe67904a63`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N163 — over-budget selection is rejected as a whole

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 1,
  "document": {
    "a": 1,
    "b": 2
  },
  "pointers": [
    "/a",
    "/b"
  ]
}
```

Frozen expected result:

```json
{
  "error": "disclosure_budget"
}
```

Observed result:

```json
{
  "error": "disclosure_budget"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7b9098fb524d2493a85dae2d1ac6fa2d581bdb63d6cd5c61106ee93262f33af8`, input digest `b355fd5117d578f2f603a89757ec8c8de5d1883a0a38310a254f6b53d133529b`, and result digest `3fd3e036e18fae39915f906d53473a404bb488257d8d06add03b8ff5905e7bc7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N164 — container selection cannot smuggle unlisted descendants

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 1,
  "document": {
    "a": {
      "x": 1
    }
  },
  "pointers": [
    "/a"
  ]
}
```

Frozen expected result:

```json
{
  "error": "container_disclosure"
}
```

Observed result:

```json
{
  "error": "container_disclosure"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d114319fb90f7974f469744f1b736eca005b2fac5bfc2a26e1c9c974f455ff46`, input digest `f7678ce0db58a3264d8c47a97a8cd4d066366cf9959eb64f679569bafcadc3a4`, and result digest `7ce3e1df5a311f3e05603d881f3508f38d00b0e1e287465f862cd9a016d3a9c4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N165 — null leaf counts as one disclosed value

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 1,
  "document": {
    "a": null
  },
  "pointers": [
    "/a"
  ]
}
```

Frozen expected result:

```json
{
  "/a": null
}
```

Observed result:

```json
{
  "/a": null
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ea8834df1e8575ae1ca4420cb1bbf23ba6832f22b8e89042b97573091d756ad3`, input digest `f4a05b6228a2eac7081f933636578c055fe3818f470b17af26ca8a7ba60c3b40`, and result digest `47e4ce6cb1e16f6dc4afc7b40f88a806a95b787ebc2452e836fd2ffb1bc970e2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N166 — zero budget accepts an empty leaf selection

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 0,
  "document": {
    "a": 1
  },
  "pointers": []
}
```

Frozen expected result:

```json
{}
```

Observed result:

```json
{}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `783f6f52809006fc12efad7a2da32d1f0c98d55e7ae901fcd9ee0346ec7af57a`, input digest `df38db9f5c2f3e7388fd5c72ec297191fee154d9ac3880b66ebb71bd8c12bac5`, and result digest `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N167 — boolean budget is not a count

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": true,
  "document": {},
  "pointers": []
}
```

Frozen expected result:

```json
{
  "error": "invalid_budget"
}
```

Observed result:

```json
{
  "error": "invalid_budget"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a365eba3b0a9e74c8b0954af92ad0445a0b12ba2e3e81f9c7e6a7f74c58b8c9c`, input digest `9f06008bd421138e58e9aa8fd1eae7c0969668906ccc9d8ae46ad9bc651db218`, and result digest `143d81b7b074815cf902be4332a5240f3ecfa18d8baac3c2e9a0c9655a071334`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N168 — negative disclosure budget is refused

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": -1,
  "document": {},
  "pointers": []
}
```

Frozen expected result:

```json
{
  "error": "invalid_budget"
}
```

Observed result:

```json
{
  "error": "invalid_budget"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ae673cb126b4a2f0fc679dbff34bb48db7f3183eee6ed0954ad1d6be266469a6`, input digest `152c3b2df11e12c237d94ccc1e169f4da5b014af7413c7e7c08d58d5474783e1`, and result digest `143d81b7b074815cf902be4332a5240f3ecfa18d8baac3c2e9a0c9655a071334`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N169 — nested array leaf can be selected without its siblings

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 1,
  "document": {
    "a": [
      1,
      2
    ]
  },
  "pointers": [
    "/a/1"
  ]
}
```

Frozen expected result:

```json
{
  "/a/1": 2
}
```

Observed result:

```json
{
  "/a/1": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `85d73a465bd324359b1a798a09b7ba5ed1c7ca9622b44e83bec6aeaf9fc1219f`, input digest `af2a79a771bde0a8f26701a90d67b57ebec349b048be87bf23be7c405cc05366`, and result digest `01daa0d98349dc23026a15d67219f344b49b82c9faf8244a77005066d848e71b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N170 — duplicate disclosure pointer never spends one unit twice

Family `disclosure_leaf_budget`; operation `disclose`; pillar Freed ID and CBR Heart; practice accessible evidence editor; core disposition `completed`.

Allow only exact selected scalar leaves under a declared leaf budget; do not call this cryptographic disclosure.

Frozen input:

```json
{
  "budget": 2,
  "document": {
    "a": 1
  },
  "pointers": [
    "/a",
    "/a"
  ]
}
```

Frozen expected result:

```json
{
  "error": "duplicate_selector"
}
```

Observed result:

```json
{
  "error": "duplicate_selector"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2073ae52040af0c48a783233b4c81acf0879f05daf1b7b08a54973bed4e86bfb`, input digest `0f09c0094183aacbcc11787803072c2ca4247abe8a21e650cbec571d4cff90eb`, and result digest `ce758311e643915e08cde527e914c8ebd7c0dd3d8d93c18b56f52005f8f21ed4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.w3.org/TR/vc-data-model-2.0/) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.
