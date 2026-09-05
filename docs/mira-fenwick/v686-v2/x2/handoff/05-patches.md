# 05 Atomic synthetic patch transactions

These are in-memory operations over copies. Root removal and unknown operation members are refused by a stricter local profile. RFC-style numeric test equality and strict receipt-byte equality are deliberately separate.

## MF6862-N041 — add a new object member

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 1
}
```

Observed result:

```json
{
  "a": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `38bbbeac62a47cf5ba039c8f12d927ee73b8f10e86c0a9e4bdf891c4a807d816`, input digest `4c858a734de107e421fe885406a969a4854f0e02a4452f12b5ed7a63e1c26328`, and result digest `015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N042 — add replaces an existing object member

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "add",
      "path": "/a",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 2
}
```

Observed result:

```json
{
  "a": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7a692dc56de67179bccbae9c4d185e7d1e7c62d49b7335e0640599871471894e`, input digest `f0294fd6a003d758f91b2b23dc0f788180f9547d38940dd611cc211ba16a5096`, and result digest `7e8059f495589fcd981232cc11d00b00da3802c01d688fa1cf1f6bed6e5bb33c`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N043 — insert at the front shifts existing array elements

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": [
    2,
    3
  ],
  "operations": [
    {
      "op": "add",
      "path": "/0",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
[
  1,
  2,
  3
]
```

Observed result:

```json
[
  1,
  2,
  3
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `e55adbcf6843c3a87b9eab97ea58c5f1bd13ccc103b868d9f192c598ad2c5ba1`, input digest `5096f60c51b069edb5e059ccc63f9806f3a17a0385f4f7125bf31973ee7dab63`, and result digest `a615eeaee21de5179de080de8c3052c8da901138406ba71c38c032845f7d54f4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N044 — insert into the middle retains both neighbors

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": [
    1,
    3
  ],
  "operations": [
    {
      "op": "add",
      "path": "/1",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
[
  1,
  2,
  3
]
```

Observed result:

```json
[
  1,
  2,
  3
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `f62eed85b9a2c6322fcc3425b529f022599712068e6596b6c9a693061a30369b`, input digest `65ae94bd59b5e8fe5f3141f409a83de106afd0f0966214a51ee7db1b270072d9`, and result digest `a615eeaee21de5179de080de8c3052c8da901138406ba71c38c032845f7d54f4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N045 — append marker adds exactly one last element

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": [
    1
  ],
  "operations": [
    {
      "op": "add",
      "path": "/-",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
[
  1,
  2
]
```

Observed result:

```json
[
  1,
  2
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `bb8cf7e791e3d06e73bfb8d563cf60f062f9059da3d41eb9e86e37584b13908b`, input digest `97893d9340e0a447b4fa3d898140339aa54036a5f3e84aecd2357d6981a64eaf`, and result digest `49a64717d5d4cb19952e6eac2946415cf6879adacf9908e7d872332d32c6e684`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N046 — numeric index equal to length appends

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": [
    1
  ],
  "operations": [
    {
      "op": "add",
      "path": "/1",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
[
  1,
  2
]
```

Observed result:

```json
[
  1,
  2
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d04051321928cebc26b7e72954a46abf81a5c6c7229e8fe5e7f5755e1bf8b413`, input digest `fb6a6d59ba83ef61f33ecd0fc8702e369a289f232d2fc12fac99905b0886f549`, and result digest `49a64717d5d4cb19952e6eac2946415cf6879adacf9908e7d872332d32c6e684`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N047 — missing intermediate parent is not manufactured

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a/b",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d0356dc4e4f18372fe22b33eff3372d3e27e91de34d5c91a15f5a53ae816a519`, input digest `93c64dc065a2c7b5fc6d7e1b29e305ca7146ce1e81a6fea7da5df181209cdf25`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N048 — root add replaces the synthetic document

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": {
    "old": 1
  },
  "operations": [
    {
      "op": "add",
      "path": "",
      "value": [
        1
      ]
    }
  ]
}
```

Frozen expected result:

```json
[
  1
]
```

Observed result:

```json
[
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `290abf9906ce6f616e3bfed4abf6d8e38a78bd27f5147677fa1011ccf433e2b9`, input digest `73a9801e2576896bf71e6a10e9d5ac581817892fe162f8b10bc56e60eed692d0`, and result digest `080a9ed428559ef602668b4c00f114f1a11c3f6b02a435f0bdc154578e4d7f22`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N049 — escaped destination slash is a literal key

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a~1b",
      "value": false
    }
  ]
}
```

Frozen expected result:

```json
{
  "a/b": false
}
```

Observed result:

```json
{
  "a/b": false
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7a65724506c4f71c2ebcbcdbe1d88a991ffdf33d75d64b44198d39b5e4a25a76`, input digest `18134b1718731700bf0c0f55e623389371fba4881b70452758a30e2b204100e1`, and result digest `df583415c28c6c27dcd2945c1e1fb96ac73ff1a8a6cff6a155d43cdc574bd97a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N050 — array insertion cannot skip vacant positions

Family `patch_add_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Stage JSON add operations on a copy with exact parent and array insertion semantics.

Frozen input:

```json
{
  "document": [],
  "operations": [
    {
      "op": "add",
      "path": "/2",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `9bf86bf8585ac83ccd3324afd4df908434aaea51b62a0c35dc3c8900573824c0`, input digest `22dfd7bcd76fad2145eac7706060eee86dc579a3fe9b6e9c829cae79952558bc`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N051 — remove an object member retains its sibling

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": {
    "a": 1,
    "b": 2
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "b": 2
}
```

Observed result:

```json
{
  "b": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `36e9ff9b8c815cec7ce94f9920d6c7b029b55ae6ef6c4795492110ee699e37c8`, input digest `a6b773b08f4faa96e14de9162d05095b36e57b4ec9bb2d3d4526600b9710a019`, and result digest `0ab1a6d394cd30195f0642b67ae1180c375ffadf5dd7f39c390668b5fdb6da93`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N052 — remove the first array element shifts the remainder

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": [
    1,
    2
  ],
  "operations": [
    {
      "op": "remove",
      "path": "/0"
    }
  ]
}
```

Frozen expected result:

```json
[
  2
]
```

Observed result:

```json
[
  2
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `feaf2e23a8eae6a4d4ca8794214c30976f65b76f4dd1bce241d883722c4de76f`, input digest `0d6b116b944f7f16f019d370478db4d88af650a0913c65b93efceeacdf1e844b`, and result digest `038966de9f6b9a901b20b4c6ca8b2a46009feebe031babc842d43690c0bc222b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N053 — remove the last array element retains earlier values

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": [
    1,
    2
  ],
  "operations": [
    {
      "op": "remove",
      "path": "/1"
    }
  ]
}
```

Frozen expected result:

```json
[
  1
]
```

Observed result:

```json
[
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `bfc42c04c952946185f3839eb7e213b2f1e68a431d89327c1b5cb56fe19c81ab`, input digest `30d843a288f889995a3173bec69314a1cce75f80f771e6003076560f2b333e1d`, and result digest `080a9ed428559ef602668b4c00f114f1a11c3f6b02a435f0bdc154578e4d7f22`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N054 — remove a nested leaf keeps its empty parent

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": {
    "a": {
      "x": 1
    }
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a/x"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": {}
}
```

Observed result:

```json
{
  "a": {}
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4d2f88b2484c503c3f61db2afde5f8f0af272bfa3139d0827d092d42531a530d`, input digest `f1cbb8ab4e7cb8e1e66494ce90c005a142808ed79b569463697de6c4e8cd2247`, and result digest `5d8171b9fc362e385a79ccd9d7992c96bcb4afca51d6278068bd1df49863b3a7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N055 — remove an explicit null without treating it as absent

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": {
    "a": null
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a"
    }
  ]
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `1260a331f86843d56be6a66abd5cb0e2a7a8ed4301476e6e8ceb669bba905482`, input digest `669fc34e4efe1f3298c39065ab2daf2ba88fc1e4ecf9758a7ee61a3b973ea68c`, and result digest `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N056 — missing object removal is rejected

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "remove",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4dc44cc88ec90071e0784d4d40286a765902f5e363205fb0cb511e4545903b44`, input digest `1f641d14861a2624cb4693016de5934ce0433d08a91d4bb1419b73de054100cb`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N057 — out-of-range array removal is rejected

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": [
    1
  ],
  "operations": [
    {
      "op": "remove",
      "path": "/1"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `8366fd8784e739ed6319235e28864619c9bd3fd9c293f51728111d1ec9e33cbc`, input digest `51cbe635ccec481d1ba6100f653fcc2e40fd40620946e6e2416823ae8aa19698`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N058 — append marker is not a removable member

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": [
    1
  ],
  "operations": [
    {
      "op": "remove",
      "path": "/-"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "invalid_index"
}
```

Observed result:

```json
{
  "error": "invalid_index"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7d94abd21c5370a07611f0f87fc8da097c9b7d564852971b61e700d0f2363dd6`, input digest `ee3459db5435248ceb6b772293ea621b7023893325901d15c8008bde60a74698`, and result digest `9b7c35000fc1afe6dd5f68d24b544c32d8456662cdd5f3bba0f415ba90d1da1d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N059 — root deletion is reserved by the owner profile

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "remove",
      "path": ""
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "root_removal_reserved"
}
```

Observed result:

```json
{
  "error": "root_removal_reserved"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `31b804d0821afb30eada37871878610d23885494db524a624cc3c1f22af67d5a`, input digest `c65f4401285c1c54ac5ac5d19e51180a9ef2be643e41026ad8dea91d94e88d4c`, and result digest `a67e2e6ec74cdb96a46e50e567400942b20482f93339c33590ef7836e231295f`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N060 — remove a slash-bearing member by escaped pointer

Family `patch_remove_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Remove only existing synthetic targets; reserve root deletion in this local profile.

Frozen input:

```json
{
  "document": {
    "a/b": 1
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a~1b"
    }
  ]
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `be13e57e5497c7f7720dcf7461f54181e5e1fc6260ce2e854b4c2e98b13f3e2b`, input digest `00429a7c05cd841d216d3e34f0c66bbe9fc2e79194b7ca089e17c12fc01f28d2`, and result digest `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N061 — replace an object value

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "replace",
      "path": "/a",
      "value": 3
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 3
}
```

Observed result:

```json
{
  "a": 3
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a389cbc5b46abed55188f5ae56c393dc3a1c1e5c0401192c43bd1e4f9b6817f1`, input digest `b7d47e7473fc3e4335af4553bef3bc2a99f7eb46dc294426308bb640188c661c`, and result digest `70778ce01ad8d1a82c80a3500bee476f34651238edeb936c4a7b0161b1395169`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N062 — replace an array slot without shifting

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": [
    1,
    2
  ],
  "operations": [
    {
      "op": "replace",
      "path": "/0",
      "value": 4
    }
  ]
}
```

Frozen expected result:

```json
[
  4,
  2
]
```

Observed result:

```json
[
  4,
  2
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ecaf238fc5d78a8a85d57a5ca4c5d53fa2146b9f4aaffd86fdf7fa0c0f502541`, input digest `bee3d9aef85232bead3a323ae6a633e8069de623f3d7eef0a5a7d7ebc1ef32a1`, and result digest `044d15dbf5c3b7e70206179fce34d75eb5ad3d40bca2ba915e9cc6f75293a9a7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N063 — replace a complete root with null

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "replace",
      "path": "",
      "value": null
    }
  ]
}
```

Frozen expected result:

```json
null
```

Observed result:

```json
null
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `5d5559db91094cdb546a9da14bad893e5b75a5815592252b7d9e5499fa2a7c04`, input digest `51081567d33363dced592d59a288dd2f65b8d214b40c47ac94783dd9b1cc7a61`, and result digest `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N064 — replace false with zero preserves the intended type

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {
    "a": false
  },
  "operations": [
    {
      "op": "replace",
      "path": "/a",
      "value": 0
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 0
}
```

Observed result:

```json
{
  "a": 0
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2239ed0580353bac45f0dd6c56b85e3d3a6a8307d07628f601b78442c6c187c1`, input digest `d96ccded24782b077c6d489e23f48e6a33f24a92fb7cb1c5872cf17d8ce3a259`, and result digest `45b619e97b5d9b029af4522e9ffb02fa99ff2bf226c82ee22a7cc10269a557e8`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N065 — replace zero with false preserves the intended type

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {
    "a": 0
  },
  "operations": [
    {
      "op": "replace",
      "path": "/a",
      "value": false
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": false
}
```

Observed result:

```json
{
  "a": false
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `685454a9cc5a608ae09230bbecbf35df4933f193cbf987e20506e8606a75662c`, input digest `7d51c8116c947ac050f627de466fe343fb1ca4f06e1aadb853b35638fa048e20`, and result digest `5cd40cde8aebb4b90dfb1cf75cb2f0580d58a86bda6f6f19bf872ab9e041fa32`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N066 — replace null with an empty list

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {
    "a": null
  },
  "operations": [
    {
      "op": "replace",
      "path": "/a",
      "value": []
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": []
}
```

Observed result:

```json
{
  "a": []
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `788e9a871b185c1e121a0c36ad37f1fb8407a944d12ec5fd47b8e7676114b2a3`, input digest `716b73fd923ced671048d18ea10283f0d6054217dcf9bb68978551317fdab826`, and result digest `50e8660084976a10f0b3b9b3a6352d5881cbd219b5587a26224971a60ff2cc55`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N067 — replace refuses an absent object field

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "replace",
      "path": "/a",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `8642b971f894234c5bcccb0a581602df918566020d8f26c49eed66a2407789e0`, input digest `940f9e04a20096c6824920774123ec6dc3c365ea7c5f20af83fd6d3caf8596b5`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N068 — replace refuses an append marker

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": [
    1
  ],
  "operations": [
    {
      "op": "replace",
      "path": "/-",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "invalid_index"
}
```

Observed result:

```json
{
  "error": "invalid_index"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4bbd5cdbcee1b6fd11f407494a6bf93755521650785c2405e097a593acc8bd75`, input digest `3cd97214413cb826a891e26c3b7c22bd7451951fea76fa17bf74a8c5f0d5124c`, and result digest `9b7c35000fc1afe6dd5f68d24b544c32d8456662cdd5f3bba0f415ba90d1da1d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N069 — replace refuses missing intermediate context

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "replace",
      "path": "/a/b",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `381e47d83cd9d991caf2536d6a08cda3031a2fd45655b97a6a350bfe3b11700c`, input digest `a7bc24422a9b106981235790ff27aabadb7ffdfe7e0848698446a1356bf2d5bb`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N070 — replace an empty-name member

Family `patch_replace_targets`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Replace an existing value without inventing a missing target or coercing its type.

Frozen input:

```json
{
  "document": {
    "": 1
  },
  "operations": [
    {
      "op": "replace",
      "path": "/",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "": 2
}
```

Observed result:

```json
{
  "": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `0fd17236f0269bd2bd05829b3667e0304e2042830e6f36b898a8dedcdc6310fa`, input digest `6be8851c02d711a6d876bda92b1f0b7fc8bba50f9484cdc5f2bac1c8d51959ab`, and result digest `cfd6d63ed693596ba47f553c434fd852b232b903dfc952811ba3def019660d1c`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N071 — matching scalar test preserves document

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": 3
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": 3
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 3
}
```

Observed result:

```json
{
  "a": 3
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `1d08d0ac89a90feca9020f9b7f6ea1e1c732002e30a70c005dcf0237ef81b355`, input digest `e16b1368949b5d5d97f6c3513434b5389d4043661748a9ac8506988be5acdb56`, and result digest `70778ce01ad8d1a82c80a3500bee476f34651238edeb936c4a7b0161b1395169`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N072 — mismatched scalar test is rejected

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": 3
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": 4
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `342e761fb8dace712e72de0b8b16eb78e68a6b217fa239b2971b445230f5b403`, input digest `00e3ffe0a9de518fa3ff056f56420f4900775ae546d451f7b2858c67fcb94940`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N073 — true never equals numeric one

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": true
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d626359a864b577c59551a26290569591ea84e792123aed7ffd63ac82c4c1a5c`, input digest `e6b3bfbb53c0b490efb97581f3e4c7287523d385445154fa44a13df5aa5287e5`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N074 — false never equals numeric zero

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": false
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": 0
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `c8d7959cab6d16d893beccb730b7428bf72d32eb47ffddfa12eb7f7c6c5d8131`, input digest `5d86d769481f49497c5d6b7ffcf1fb04568a7b5b12be04d099275163474a6cac`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N075 — equal integer and finite decimal are JSON numeric equals

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": 1.0
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 1
}
```

Observed result:

```json
{
  "a": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `1705d74cb7b5ea4bc5aca0bc403dca754ed937770532d9a0cf67fe4191761106`, input digest `f20a0655ca1b927af0fc7fc4c9de4893c301194c5af0c60eabda379d64d17fa9`, and result digest `015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N076 — object member ordering does not change equality

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": {
      "x": 1,
      "y": 2
    }
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": {
        "x": 1,
        "y": 2
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": {
    "x": 1,
    "y": 2
  }
}
```

Observed result:

```json
{
  "a": {
    "x": 1,
    "y": 2
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `bafaa146ba5cc2c46df346d41aaa4cb4f81f67902f45f90d2d056c84a50a1865`, input digest `9f8f522db110c390dff2ec46a9b8885cb3605d8fb91dad873a9b1535017ac106`, and result digest `a9fdcd2ed3b1c70bdf32595fe6ad510857975eda307bf160f5c63b066732ea47`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N077 — array element ordering remains significant

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": [
      1,
      2
    ]
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": [
        2,
        1
      ]
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `579a4ba7b6704930d299602a5fd9844b9d37e785267d73dcae226ef60372d61d`, input digest `6528988a2a35b2f7b1b5f6348972bcaff1175516f6951e3b0803f7ff51f6655b`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N078 — null test passes only at an existing null

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": null
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": null
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": null
}
```

Observed result:

```json
{
  "a": null
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7526b4d52305434c4a3e840f51f0f1239b41f31beb1b1905bf7d662e362a08b3`, input digest `83a7855dd4429aab7e47ca1cffddd50870b3e304d23dddc55ecb9daba2807f67`, and result digest `d091f9c83c091f79652fe8786375b3fe4ce0861a56f5bfbafedbe431877ff0e8`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N079 — missing field is not equivalent to null

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": null
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `30c9ac321618002fe74d80d472f6908a0d584c56905ef148f771c13d9345c6da`, input digest `ccacd7390279987a94976e1e785a858f68b029ff7a368831e281a5b451224c76`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N080 — nested boolean and numeric values stay unequal

Family `patch_typed_tests`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Check JSON test predicates with booleans separated from numbers and finite numeric equality.

Frozen input:

```json
{
  "document": {
    "a": [
      true
    ]
  },
  "operations": [
    {
      "op": "test",
      "path": "/a",
      "value": [
        1
      ]
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `5bb04e7463ff0c51121935240d7a7cea3e097da57287cd5ac1af6266236a4fb7`, input digest `ae87913495efbfd71bab495bb07973aacfe0b4e9403921aa4a7780b164eceefb`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N081 — copy object member retains the source

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 1,
  "b": 1
}
```

Observed result:

```json
{
  "a": 1,
  "b": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a0caff61198c9d87a2d044b1b7053427796a0052c31d654bf99f86ccdd4941fe`, input digest `66ad1fec5feb71031cc2061c3ce479abffef65c6377c1698bfc4d2168e8d5c34`, and result digest `4dad51ac41eb73862fce375fae85ba13711fd19f1b26d8e4b1f9fa405c3d5adf`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N082 — copy nested list creates a separate target

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": [
      1
    ]
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b"
    },
    {
      "op": "add",
      "path": "/b/-",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": [
    1
  ],
  "b": [
    1,
    2
  ]
}
```

Observed result:

```json
{
  "a": [
    1
  ],
  "b": [
    1,
    2
  ]
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `03965ced222c62d59af1af1b1edb10a1aff8d443e1c7591c8249f93d406fe72c`, input digest `dc3c88817033c3ff9a9290ef1680d2d76fd2f764895e4836bcbfac34ed06be3d`, and result digest `b6029300f7d632aebaeabadbe0fc07991c6a27b7fe21b686f3df4b54f5ad4331`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N083 — copy an array member to its end

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": [
    1,
    2
  ],
  "operations": [
    {
      "from": "/0",
      "op": "copy",
      "path": "/-"
    }
  ]
}
```

Frozen expected result:

```json
[
  1,
  2,
  1
]
```

Observed result:

```json
[
  1,
  2,
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `532c0c717d765c57782c8fc17b08e3c2b3a40ff5763fbc187ced345ed828cbe9`, input digest `3eb95f2b1a8719ab73fb31b6a876054810be33a819366d4fce9a54d0b33b0b55`, and result digest `f49b9dc62ee7904aeb02fbcc8b7ebaf9eb91d9ba12129d9961d5940ad48854ba`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N084 — copy over an existing object value

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": 1,
    "b": 2
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 1,
  "b": 1
}
```

Observed result:

```json
{
  "a": 1,
  "b": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ae6dfba7b90bb565152459fb47485a0f4ef3560e0e976831c53d48fc63256e12`, input digest `771b01092e9135b134fa0c890d9028ff720c99d172c72b8a71514e3aaf770584`, and result digest `4dad51ac41eb73862fce375fae85ba13711fd19f1b26d8e4b1f9fa405c3d5adf`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N085 — copy a null value remains explicit

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": null
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": null,
  "b": null
}
```

Observed result:

```json
{
  "a": null,
  "b": null
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `34070ece1270ad2465d42745f25ab400d885fc8de6b9e5b62a5e4eaabf54c509`, input digest `41cba113b47d6d04ac5aa28ae5623b1ec999c4f000bf9aab3a7467afa3561ee4`, and result digest `052c4bd5e6ded53bd884485af8b1667a7b70ba3a8573b54bd878f6d2c705c2df`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N086 — copy from missing source is rejected

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a5068f8b5bb77a5d2fd30d245020aaba87516111664d0c6f2e6eae3747e26371`, input digest `dfb5619ad52dd3bbb39a5fe191b79b754162e1ab3d55b9ff25b89ee0a089cb63`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N087 — copy to missing parent is rejected

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b/x"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `5c55d142d27abd776b71ae46ccbd89344b4d1e04e00abc548f0f7c28a1985dbd`, input digest `2ef6cc229de3aa5f0ba9cb5deb4726eead1715e04b7cdd63fd6f08176dce5f56`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N088 — copy source to itself is stable

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": [
      1
    ]
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": [
    1
  ]
}
```

Observed result:

```json
{
  "a": [
    1
  ]
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `84c63a8d25d3ab0862cdccafe436f6e59831641331777409316ee7572deb42ba`, input digest `bef65464c532fc300e1bc26c16d66befe18126b8055d0a5e69d5e3fb1d9230e6`, and result digest `ff5464c34287e9ec505b9f76573a4cb0bd408c96c6537b458fdd993fc7c615ce`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N089 — copy root into a descendant uses a finite deep copy

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "from": "",
      "op": "copy",
      "path": "/snapshot"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 1,
  "snapshot": {
    "a": 1
  }
}
```

Observed result:

```json
{
  "a": 1,
  "snapshot": {
    "a": 1
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `baa37214a83320c54b291ee16d6b400d81929605404f6dd4345870fb15020481`, input digest `cc61ce92228f11dd7882551b10fdfa28dc9b0106a2fbdbb7af53c4426713d581`, and result digest `076ab429ecf6c39fb60fb495788829e8f4cab5b9b60a5afee66c7dd640a691b0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N090 — copy escaped source key into an empty key

Family `patch_copy_isolation`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Copy synthetic values deeply and retain the source on all successful copies.

Frozen input:

```json
{
  "document": {
    "a/b": false
  },
  "operations": [
    {
      "from": "/a~1b",
      "op": "copy",
      "path": "/"
    }
  ]
}
```

Frozen expected result:

```json
{
  "": false,
  "a/b": false
}
```

Observed result:

```json
{
  "": false,
  "a/b": false
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `3a7788f6f20035a7472cef64df46e4f3ddae14dd0fe4a3bc9dc412df990d09a1`, input digest `05903d7cc6b3a254b593ca0a05d8168b0d6be4ef05cb64ebaaf5349c38ab6ce7`, and result digest `d2c305d0fa62cb036086be9d75715485ec8df4f631bfbde81040b8f992b490b4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N091 — move object member consumes the source

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": "/b"
    }
  ]
}
```

Frozen expected result:

```json
{
  "b": 1
}
```

Observed result:

```json
{
  "b": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `8deb0cac6c5b3812562c7824e80a37feebea8bd8bcb4333a48a6dda7cb4fea30`, input digest `f9b8df5cde09b687121837b11bef793851547c9f7cb09c5aa97b944d86d4229b`, and result digest `eb8ed3ccb5023093b56f490a46501e88d09736687e609fdbc1c71b3df8b9ccd3`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N092 — move array element uses the post-removal index

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": [
    1,
    2,
    3
  ],
  "operations": [
    {
      "from": "/0",
      "op": "move",
      "path": "/2"
    }
  ]
}
```

Frozen expected result:

```json
[
  2,
  3,
  1
]
```

Observed result:

```json
[
  2,
  3,
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `dd9bec40567ee5fc7a43acdf2d1aeb9c8477f2c0964fdfa37a8d5f7517b07466`, input digest `19b002dad466062707898c6cb70b4c07cd9d29ce20bf9d4c5e8c3ddef4db9b31`, and result digest `bc8c0f85a2d4fa08ad1143292014b4e8b5b9b4da11bbb98c903c319a7bdbb7b0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N093 — move last array member to its front

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": [
    1,
    2,
    3
  ],
  "operations": [
    {
      "from": "/2",
      "op": "move",
      "path": "/0"
    }
  ]
}
```

Frozen expected result:

```json
[
  3,
  1,
  2
]
```

Observed result:

```json
[
  3,
  1,
  2
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4b78b778fada2fd29d90f3b153d237844d5490b56898948b154616f9ccde2a5d`, input digest `afc1e1b5ebd3fb1c512abc70a18f0a732248afcf2a7c52bab02e87b7b990e6e2`, and result digest `51bda7ab4e44726cde71fcb6e4b515357059bb6b6dd5146d1fc50f73f11678c6`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N094 — move to append marker uses remaining array length

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": [
    1,
    2
  ],
  "operations": [
    {
      "from": "/0",
      "op": "move",
      "path": "/-"
    }
  ]
}
```

Frozen expected result:

```json
[
  2,
  1
]
```

Observed result:

```json
[
  2,
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4d5d5fceef2a11f5fdd515f4639c5c223e4a09eee2c8d8345428b6936f94ef12`, input digest `cccedbc01beeec821fa74ae795f15cde0b2175ab2c579fb0ebdfc0f5f036fc57`, and result digest `af1a1fc110b6094c48582b0ef83553cb7908d7a4365424eef28e76ef6c88d630`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N095 — move value to itself validates then preserves it

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 1
}
```

Observed result:

```json
{
  "a": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `e79b4264675dba5abf417af577ec5565157607bbc02fa9ddaac2bb67179fddba`, input digest `bfb6763e1d5cf139f365566b69ab170f87661d564450d863c0667186c1b45c4f`, and result digest `015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N096 — move into a descendant is refused

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {
    "a": {
      "b": 1
    }
  },
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": "/a/c"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "move_into_descendant"
}
```

Observed result:

```json
{
  "error": "move_into_descendant"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `6cb77d67dffc8e7f1d10cc2d0e493261d6d054a29ed485fab8a824063b2f3659`, input digest `9bb74d500eaebb9e1c0cea0a6f47cec7a0860a6ca5c05346f96061be3105a546`, and result digest `e88785997b97c9c88c3b70c74b2d7cf16b02eaaee634c3c2f73812536138e1af`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N097 — lexical prefix alone does not imply descent

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {
    "a": 1,
    "ab": {}
  },
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": "/ab/x"
    }
  ]
}
```

Frozen expected result:

```json
{
  "ab": {
    "x": 1
  }
}
```

Observed result:

```json
{
  "ab": {
    "x": 1
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a79784ac8945397a0319e976309959b0bebf9d5919b3818da2617cd13dc03cc8`, input digest `dacbe8e825383051342d984a97b673c9389afafa46cb2faa7703f48749440c4c`, and result digest `b880875b70dc90a5914d22c06d719dd9cffc1f45705cfd93b73ac074aab38360`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N098 — move with missing source is refused

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": "/b"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `108343025ea8b7072f6c8caccf409fa26d9c61979ec945a2d015cde749dca544`, input digest `f2c978a397dc438ed19ed4f3383b23566cf44b9de37ef7491c787cc7686ad07a`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N099 — move to missing parent rolls back source removal

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": "/b/x"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d17e219939b2c21c3cfb1791eefe3f2422d56c7286ed5dda9c42c190222b5d88`, input digest `4b0f5142e44c503ec73a9ad77a123158d018ada8c1e8dee059edb4c2686d0deb`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N100 — move nested value into root replaces the document

Family `patch_move_ordering`; operation `patch`; pillar Freed ID and CBR Heart; practice provenance librarian; core disposition `completed`.

Move after source removal with token-aware descendant refusal and atomic rollback.

Frozen input:

```json
{
  "document": {
    "a": [
      1
    ]
  },
  "operations": [
    {
      "from": "/a",
      "op": "move",
      "path": ""
    }
  ]
}
```

Frozen expected result:

```json
[
  1
]
```

Observed result:

```json
[
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4419e1cbcbc638b6da0fa19c518ae2834c06ff7475c8fa5ce1bddbc6993ad07a`, input digest `7598df84ddaeb0efe341ccc97fb2ea8e8e756e7c69aae6c7d1da786654a021ef`, and result digest `080a9ed428559ef602668b4c00f114f1a11c3f6b02a435f0bdc154578e4d7f22`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N101 — test then replace forms a bounded compare-and-set

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "v": 1
  },
  "operations": [
    {
      "op": "test",
      "path": "/v",
      "value": 1
    },
    {
      "op": "replace",
      "path": "/v",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "v": 2
}
```

Observed result:

```json
{
  "v": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `265b748ae8400f0744c9645270f6ee17142e30390df0a2be913e2a1718f2a157`, input digest `cda244d24472fa82d64f90d72628ded1f8d934d113f886c045750f47464cf505`, and result digest `2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N102 — a failed precondition blocks the later replacement

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "v": 1
  },
  "operations": [
    {
      "op": "test",
      "path": "/v",
      "value": 9
    },
    {
      "op": "replace",
      "path": "/v",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ea45b2cbe3927f0161be4c953735708ecc1eaac6219fc6fe95f1061f593b413d`, input digest `3bd664bf13cfabdca0eca2ab7f36691276831d970a40cf246ab4ec8f4f82d020`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N103 — later failed test rolls back an earlier add

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a",
      "value": 1
    },
    {
      "op": "test",
      "path": "/a",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "test_failed"
}
```

Observed result:

```json
{
  "error": "test_failed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `54819a088f74369db81301a236b79a3f713974aa1728e3e86b6b7afbd056eb60`, input digest `7c047112967689d4d129564a3c31491e6a347c42b48e4189dab99eeb29edbee6`, and result digest `12d59dd7d86030daad85cc6345f6b01f641bb3526a96efa006c34138301c9ff2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N104 — remove then add explicitly replaces a value

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a"
    },
    {
      "op": "add",
      "path": "/a",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": 2
}
```

Observed result:

```json
{
  "a": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `70cb6c0ac4b4d1c509fce727145888ca01703405503d0f076121d453ac0a24d1`, input digest `1c32d374ba33608a602e71318a7977f975680ce029eef809cffb24c172ab6e93`, and result digest `7e8059f495589fcd981232cc11d00b00da3802c01d688fa1cf1f6bed6e5bb33c`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N105 — second removal of the same member rolls back both

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a"
    },
    {
      "op": "remove",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `478a86627186ad9b36afe2389dfe9ca4d5200d9d70bc9879b74363e8193d1972`, input digest `257b85906ff3ea8d7b1c473bb837033a926738a1e79f4865828650d5746c5edd`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N106 — empty operation list preserves the document

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "operations": []
}
```

Frozen expected result:

```json
{
  "a": 1
}
```

Observed result:

```json
{
  "a": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `e7fe064c2f2256a6cf3841d9aef0bff9cbd374bc40872573614fc8eb20959afe`, input digest `26d33cc2498744a27a6a46050e209499dcaec7a7400724f69b8bba74124fbee6`, and result digest `015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N107 — root replace permits subsequent indexed insertion

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "replace",
      "path": "",
      "value": []
    },
    {
      "op": "add",
      "path": "/-",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
[
  1
]
```

Observed result:

```json
[
  1
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `97cf8a65bd53772a482e2ee8ce311b50c12aa59d9f48a250bb6c15285bfc6db1`, input digest `c708491ba78038f2fe28286a48162a70aeff76090ac249b127ee357b4d39035a`, and result digest `080a9ed428559ef602668b4c00f114f1a11c3f6b02a435f0bdc154578e4d7f22`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N108 — parent created earlier is available to a later step

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a",
      "value": {}
    },
    {
      "op": "add",
      "path": "/a/b",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": {
    "b": 2
  }
}
```

Observed result:

```json
{
  "a": {
    "b": 2
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `1a072570409ddf60b5fe1a47a61762cfc0a9f60a8ce18cffce6136be0cef2714`, input digest `14152f7a71c336fca9d94b33e986ec91d78949527d3f417aac8dbfb34485897f`, and result digest `6377e7d18f737adcad5a0930c5d8ce72150fffe1fa2dc1c65d9c5f81d52346f5`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N109 — deleted parent cannot accept a later child

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "a": {}
  },
  "operations": [
    {
      "op": "remove",
      "path": "/a"
    },
    {
      "op": "add",
      "path": "/a/b",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `65fd885478e21842dda2233c62583e8409ebc6d1e98a96d189791b012a76aec3`, input digest `0d32f45fec6399d77e7d4e4a98bd883946d7b0179c402353b52599d146552a0d`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N110 — copy followed by source mutation preserves the snapshot

Family `patch_atomic_sequences`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Return no partially applied result when any in-memory patch step fails.

Frozen input:

```json
{
  "document": {
    "a": {
      "v": 1
    }
  },
  "operations": [
    {
      "from": "/a",
      "op": "copy",
      "path": "/b"
    },
    {
      "op": "replace",
      "path": "/a/v",
      "value": 2
    }
  ]
}
```

Frozen expected result:

```json
{
  "a": {
    "v": 2
  },
  "b": {
    "v": 1
  }
}
```

Observed result:

```json
{
  "a": {
    "v": 2
  },
  "b": {
    "v": 1
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `12b7ccaaf2abdc7086b8e1e4527d9f1d2e38051147a98d0dc75dbcdb11946caf`, input digest `2124be7be5167bb3cc9c4e787056a41edeed65ee2fc3fb233bc39f83d4b70c03`, and result digest `737ff16f95043472ca0e8aec40c2be89abc6366660e52f37bba2e70bbbc3f219`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N111 — allowed subtree accepts a nested correction

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "allowed": [
    "/public"
  ],
  "document": {
    "public": {}
  },
  "operations": [
    {
      "op": "add",
      "path": "/public/x",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "public": {
    "x": 1
  }
}
```

Observed result:

```json
{
  "public": {
    "x": 1
  }
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `c612dc421fcaea52a1b110b80f3b5fb3ef6183a02f29784ed26f85d38d51235e`, input digest `a033e02c913291870ab923e63fdb16ba4963d5dad83c20ebf1e6995422d923b8`, and result digest `ebc707f7079d2621ca84279d94890bbd9c12c61d1c068016637b649c0f68c79d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N112 — unlisted subtree refuses a write

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "allowed": [
    "/public"
  ],
  "document": {
    "private": {}
  },
  "operations": [
    {
      "op": "add",
      "path": "/private/x",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "path_not_allowed"
}
```

Observed result:

```json
{
  "error": "path_not_allowed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `c5e24b5d7a4291b70b5dc39aaa7221fb69aea1931eecd9170ea2add0e06f9e01`, input digest `b4355418a20cd295e1b383a5f07585b257eba0eeaaf4c833a9f7f3e60c918a07`, and result digest `0af679f01800de746694e4891ccbeb431830c1b70f5215b492477943533515c0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N113 — allowed lexical prefix does not permit another key

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "allowed": [
    "/public"
  ],
  "document": {
    "publicity": {}
  },
  "operations": [
    {
      "op": "add",
      "path": "/publicity/x",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "path_not_allowed"
}
```

Observed result:

```json
{
  "error": "path_not_allowed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7566bb2743375ef55e43ffb3976c2ff3fb9bf67d3b2714632df02844fcfe7def`, input digest `87c760cceb03d881bde89aa0c6afc4c8ff413b0df5a84be53dbde5280db69396`, and result digest `0af679f01800de746694e4891ccbeb431830c1b70f5215b492477943533515c0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N114 — copy cannot read from an unlisted subtree

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "allowed": [
    "/public"
  ],
  "document": {
    "private": 1,
    "public": {}
  },
  "operations": [
    {
      "from": "/private",
      "op": "copy",
      "path": "/public/x"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "path_not_allowed"
}
```

Observed result:

```json
{
  "error": "path_not_allowed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2de90aac3e9819d396822facd6733fe53d5a594e149a4ee24a92567fc0bdde17`, input digest `f6ea3950186eb80c8b1424b16b5b1cf8ff0e9aca8936662c156983aa1ebf34cb`, and result digest `0af679f01800de746694e4891ccbeb431830c1b70f5215b492477943533515c0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N115 — unknown operation is rejected

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "execute",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "unknown_operation"
}
```

Observed result:

```json
{
  "error": "unknown_operation"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `6bbfbf6c264eecfacd05a206beb0a4966cd65bdaeeb7a89d59de01b826ab4269`, input digest `99918f679aacde3df6e9c33d30e36cd90fdfd4ca19cfc94089be0b1e8926f268`, and result digest `0aedc34b88a7ef8d5166613afd5d29c4fa7ba1d21d00c46db53420c9fecf8b6a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N116 — missing add value is rejected

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_value"
}
```

Observed result:

```json
{
  "error": "missing_value"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ba6acdfc0c4fc3f71cf10edb97a7710dd81679adb7d3c14aa47bdb55a2bf69e3`, input digest `2e4d228568df9404fe3ff560b944820b7449cdcd813508583835628241d68a14`, and result digest `40b016ccb5e7a96a30a4245bdff268a4be40ca0f63262a93af8415bf41952efa`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N117 — missing copy source is rejected

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "copy",
      "path": "/a"
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "missing_from"
}
```

Observed result:

```json
{
  "error": "missing_from"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `a43f8cc6b8899f4d77a6df947bab17070435ebd2a33639a34dc87605b790d5b0`, input digest `57a8e2f966d34096e37459332e6aa876e6a3be9005579fed9cebeae406e91c95`, and result digest `b059231e197eb88dedac05b1926abba52afbcabaf608a9b4a65be4653d6e59cd`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N118 — operation list must not be a mapping

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "document": {},
  "operations": {
    "op": "add"
  }
}
```

Frozen expected result:

```json
{
  "error": "invalid_operations"
}
```

Observed result:

```json
{
  "error": "invalid_operations"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `6dcb2d48d974039cb60f84d079943be662cd065c0d71440aed63c877d380061a`, input digest `e97e11e4f6b03f9f2b7ba86cd7d4a433f161eec2bdbe30f136ca1d01158042e6`, and result digest `104bf2d471b81b086fdaf89f086592fa17e24e5ed0ff2623a125db769771a95d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N119 — empty permission list authorizes no target

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "allowed": [],
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a",
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "path_not_allowed"
}
```

Observed result:

```json
{
  "error": "path_not_allowed"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `571bfabea1d9b9922e209f87d44e79497c1bb7c9a33ce76269d981d623caa173`, input digest `1f244443c4bd227fdf5038091c5ce701b80b628eb7fa68795d7a593a7ba9ed72`, and result digest `0af679f01800de746694e4891ccbeb431830c1b70f5215b492477943533515c0`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N120 — unsupported operation members fail this stricter local profile

Family `patch_owner_policy`; operation `patch`; pillar Freed ID and CBR Heart; practice interface test designer; core disposition `completed`.

Restrict patch operations to explicit writable subtrees and safe bounded input shapes.

Frozen input:

```json
{
  "document": {},
  "operations": [
    {
      "op": "add",
      "path": "/a",
      "unexpected": true,
      "value": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "error": "unknown_operation_member"
}
```

Observed result:

```json
{
  "error": "unknown_operation_member"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `88c9e7254947866a8d675190358d573ba80dfff7d8a6f65f6833f08806c96e17`, input digest `7d8d18c77a93ff375f7ca51ec329cb9509299a694c8dd7895755ea2f237cd947`, and result digest `cf839fe66f92933fac7a84bd706831aa6d679faff46ee596cc38918a2662c95e`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6902) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.
