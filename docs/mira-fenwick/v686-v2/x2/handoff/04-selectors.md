# 04 Exact selectors and nested projections

## MF6862-N001 — empty pointer denotes the document root

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": ""
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `3b0e9432abe658c866b1dd3df186afdc0906187011acbaf233bfe6108c0e51c1`, input digest `dd2b532eda131ba70f9236982e21ab7f2de6785ce4db88ea2121b8550b7e6ac6`, and result digest `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N002 — one slash denotes an empty member name

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/"
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `cdafd246a33b7ac6534362fc7e860be0a462da9b49736d244228e39516c786ea`, input digest `4af9dc4d3453d4115cfde0b5d977fdc5cdde511af0dce0372525ee1387a06bfc`, and result digest `055539df4a0b804c58caf46c0cd2941af10d64c1395ddd8e50b5f55d945841e6`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N003 — escaped slash stays inside one member

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/a~1b"
}
```

Frozen expected result:

```json
[
  "a/b"
]
```

Observed result:

```json
[
  "a/b"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `aa2ba6f02c1d553bdc9664ef6f35ba4035b9147e1ad6044130caf63bdc9d6de8`, input digest `cc5cdd7ea7a5ee9c3edfc0221ee1626fa9ec715bdc9405e1794546895fc6493d`, and result digest `1693b0cfc4dae1878cdb4234fe0c8d96b42766f997045bc65bc7db525d867213`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N004 — escaped tilde survives decoding

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/m~0n"
}
```

Frozen expected result:

```json
[
  "m~n"
]
```

Observed result:

```json
[
  "m~n"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `8e3437e9f8cfba1f8f6ce185e35c48d7f3406447fc82d1acf90896a883317230`, input digest `4b517c214563592a795e6ff88bb22f6938e92cb59ad17793d0922bec797cddde`, and result digest `c7f9eaf49ff33170c1cc1ac315987f92c43e4e9b4c940fe748bbbbeb146419f2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N005 — tilde zero one is decoded only once

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/~01"
}
```

Frozen expected result:

```json
[
  "~1"
]
```

Observed result:

```json
[
  "~1"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `3f489461193327ba920da45bc3a3f574f2bb123c5b86f37b92d50ba439145108`, input digest `f841cdb433fab4687272d24ccbad468a4cb8f7e1e3a093b08461f395bec1b771`, and result digest `d7f1ed6f737be535c13e013f04561609725f451fee75141439392dc12233109e`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N006 — consecutive slashes preserve an empty intermediate token

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/a//b"
}
```

Frozen expected result:

```json
[
  "a",
  "",
  "b"
]
```

Observed result:

```json
[
  "a",
  "",
  "b"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `3cde5ea2fe4e86ae23d6c910514b824b4c45fa5a81aca34ec63f261c08a171f0`, input digest `009a93bff6aa787ea592a66a66aa2ad99ec38f8d22af58010e28783d23be4022`, and result digest `80c0a11e7167d941ba4a73b4da0b26ace88ebe7863901271dfb782f74b3a8fd5`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N007 — percent digits remain literal outside a URI fragment

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/a%2Fb"
}
```

Frozen expected result:

```json
[
  "a%2Fb"
]
```

Observed result:

```json
[
  "a%2Fb"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `9d1851e8ffcd672dc2924b52c7d3314571e98e3b6cb098bd6143efbefe933525`, input digest `c5501f69818289ce8de5efd189185f720792f7d44d1ab89f312cab4320bf0512`, and result digest `a510e44e0502fe04e8d34441ff4a7bfc039f0d5ca00532217db96f632f16d5c2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N008 — macron-bearing token remains codepoint exact

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/Māori"
}
```

Frozen expected result:

```json
[
  "Māori"
]
```

Observed result:

```json
[
  "Māori"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `879e14ed5bbca621a3d84c350aae77ca37d4e324cb9bbf30fe0d8bfb0c77c90d`, input digest `f887249d9a5cd9160c6fbe983061d97ecc1c43f10161c38416f40f9b0882b72e`, and result digest `42eed2fd87ddcc7348fcde2f95ae3b03d92f75f203fd5002051e3def4cfc6b8d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N009 — numeric token retains its lexical leading zero

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/01"
}
```

Frozen expected result:

```json
[
  "01"
]
```

Observed result:

```json
[
  "01"
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `08ccf54cbeac71bb130920904a3d4a67418af5840b454afbe901fea3fc78a250`, input digest `de65dc99bd591537bb13b3446da2b72bb924e980c5e8d6c5f07d16c6a65ba74b`, and result digest `b340df083d8945981b45405a7352a5b917a579908d5aed11a1898ecddc36cec9`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N010 — whitespace member is not stripped

Family `pointer_token_codec`; operation `tokens`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Decode reference tokens without URI, Unicode, or filesystem reinterpretation.

Frozen input:

```json
{
  "pointer": "/ "
}
```

Frozen expected result:

```json
[
  " "
]
```

Observed result:

```json
[
  " "
]
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `beec69b408a59c2afadcfe8394e27bfee52379c68b24a75fe5e5fe35eb215842`, input digest `ab5b2aa2045be01b12b976ac60f72d4f527db5319d187ad8410f4a61a759536b`, and result digest `418386ee404c8f44a64ad6422cd07f032b6ce04f9ad1471397dcfb0a03a0d2f1`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N011 — root selection returns a complete synthetic object

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "pointer": ""
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `0d760e9a5e3dcc7c5a66f35f8c7242fd40a31a20721d66d17ebb512b99aa8d9b`, input digest `45c680b4a74643841f943200fdc74348d59a2e9f6dc3d9ecbd0ffd49e4501e63`, and result digest `015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N012 — empty object member can be selected

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "": 7
  },
  "pointer": "/"
}
```

Frozen expected result:

```json
7
```

Observed result:

```json
7
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `f1782c0ddf1f2bf38f98b278422d312217fb915082040e2e41874d6f01c1b904`, input digest `d927ebac620bba73d9df48f66a3e957f579bbadacea89c5e58273b6d8e3179ef`, and result digest `7902699be42c8a8e46fbbb4501726517e86b22c56a189f7625a6da49081b2451`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N013 — array element is selected by zero-based position

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "a": [
      "x",
      "y"
    ]
  },
  "pointer": "/a/1"
}
```

Frozen expected result:

```json
"y"
```

Observed result:

```json
"y"
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `45757821498a0fc89ed4cd9eb6b60e1a2c91e5f09c57976a4c21e7943f242a0e`, input digest `862e84cba24c80b5c1d69cf95c7baa994a518ecb7983ea98734de6ee42d207b3`, and result digest `2bc983a5942276eb00a75e2113a69694318cd28c7de0fc83c0598d9db50eb777`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N014 — slash-bearing member is distinct from a nested path

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "a/b": {
      "v": 2
    }
  },
  "pointer": "/a~1b/v"
}
```

Frozen expected result:

```json
2
```

Observed result:

```json
2
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `c7a249ef2a15eafb77ad2c933b5a962664062b53d30165869aa4b44248747dcf`, input digest `6de8ddfcc0e6d03cd8bf1ebd7f0922be7e6dbf7bdebbf20fef7819c0036e3b00`, and result digest `d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N015 — tilde-bearing key selects its literal value

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "~1": 3
  },
  "pointer": "/~01"
}
```

Frozen expected result:

```json
3
```

Observed result:

```json
3
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `965d9530cf4b4807cbd7b3b82152bda15761a6a87704e169b3bef62b96b491ff`, input digest `06779a64ab4c67a1d88a00ff46b0146a177d6a1cb6f9124c6a86a6e68516c48c`, and result digest `4e07408562bedb8b60ce05c1decfe3ad16b72230967de01f640b7e4729b49fce`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N016 — explicit null survives pointer resolution

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "n": null
  },
  "pointer": "/n"
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `14bf5cc791531df323d70292728bbe86a28ed98b9f3292e00836e552debfd8e9`, input digest `730bdb3b0d31bbe2d17890c0fe09786c6fed68cabf81d83e9f60d82e5c5cdedf`, and result digest `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N017 — false is returned without missing-value substitution

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "f": false
  },
  "pointer": "/f"
}
```

Frozen expected result:

```json
false
```

Observed result:

```json
false
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `6f75df0da0fd7ceb8d62db78ced286c3df3a03a7e29904078cb61436472b67c4`, input digest `58f2915b66de073efb24986adbe4cff086d8cd2e966d49c8b58994097247c4df`, and result digest `fcbcf165908dd18a9e49f7ff27810176db8e9f63b4352213741664245224f8aa`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N018 — zero is returned without truthiness substitution

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "z": 0
  },
  "pointer": "/z"
}
```

Frozen expected result:

```json
0
```

Observed result:

```json
0
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `06b1eacb59f79d093740b255a98373483e0cc12d92d46c145c8bbc9c7a1fb799`, input digest `d7660f2141c3529b6c7d25b2119f4916045bcec63d337ee6dbf594be8c80538a`, and result digest `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N019 — leading-zero object key remains a valid dictionary member

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": {
    "01": "label"
  },
  "pointer": "/01"
}
```

Frozen expected result:

```json
"label"
```

Observed result:

```json
"label"
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7e8bc6b05cf5eafb1b311efedc25fa907b333e3ad258bcee1da2a15ca18532b4`, input digest `9d37d7cfb0664da58e0a5754b68955ab97b80dfbe9dd029c3f4cbdb511ae73f5`, and result digest `bea6e6df225b3c3edb767a70498f641b55093a99e4f35e35f198db29eafeb17b`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N020 — nested array and object traversal preserves their roles

Family `pointer_value_resolution`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Resolve a nested JSON value while preserving null, false, zero, and array order.

Frozen input:

```json
{
  "document": [
    {
      "x": [
        4,
        5
      ]
    }
  ],
  "pointer": "/0/x/0"
}
```

Frozen expected result:

```json
4
```

Observed result:

```json
4
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `7d80da8d099960c8b993660421fe31c2240838e106686e2491375152362fce82`, input digest `a781aef3b5821ba9a07532e24bb705512cf160de7428f31540f97994fa72f788`, and result digest `4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N021 — unprefixed pointer is rejected

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": {},
  "pointer": "a"
}
```

Frozen expected result:

```json
{
  "error": "invalid_pointer"
}
```

Observed result:

```json
{
  "error": "invalid_pointer"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `90f9f7c7867d75d0ac4d9afe82df9a7e225f849198f7dce8b0368e54433f6323`, input digest `4b18cfbef4b948bc3556d8a8145a8d46588930f699eae9192c60f7886632f0f3`, and result digest `160c50a2177d888f6816ed1ae1215cf9e994e185c394ec3297708eae886164c7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N022 — unknown tilde escape is rejected

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": {},
  "pointer": "/~2"
}
```

Frozen expected result:

```json
{
  "error": "invalid_pointer"
}
```

Observed result:

```json
{
  "error": "invalid_pointer"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `f096b313df90695a82c277427379261b4e4c1d290670e49eeabeb394c0cd96a1`, input digest `7e4c6a21ef45a59de3bfefd47dbbcaed56769e1919c2284ca91fc3976e922e82`, and result digest `160c50a2177d888f6816ed1ae1215cf9e994e185c394ec3297708eae886164c7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N023 — dangling tilde is rejected

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": {},
  "pointer": "/a~"
}
```

Frozen expected result:

```json
{
  "error": "invalid_pointer"
}
```

Observed result:

```json
{
  "error": "invalid_pointer"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ebe05a52321e7b37f3cde98975faf264b942e97f82f5fc34545d7f54748cb4fc`, input digest `2be0b125c0b567b52a2e26639bc37280802a1a95562dec09ad09755b63421143`, and result digest `160c50a2177d888f6816ed1ae1215cf9e994e185c394ec3297708eae886164c7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N024 — fragment notation needs a separate decoder

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": {},
  "pointer": "#/a"
}
```

Frozen expected result:

```json
{
  "error": "invalid_pointer"
}
```

Observed result:

```json
{
  "error": "invalid_pointer"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `4fe0a906cd8d32b1b87902428e0189d78aca947e8804e17ff33733ae26a7c284`, input digest `019f377899b58ddce43ce51fd6334bbcb4d2f592748efa206f430d3a52941d87`, and result digest `160c50a2177d888f6816ed1ae1215cf9e994e185c394ec3297708eae886164c7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N025 — boolean is not a pointer string

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": {},
  "pointer": true
}
```

Frozen expected result:

```json
{
  "error": "invalid_pointer"
}
```

Observed result:

```json
{
  "error": "invalid_pointer"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `9de70f9bc74f483d6ccf8ca66836563e94a1d94f28c8b127ee1350edf92dab9d`, input digest `5463a228a10ec033ecb6a7d2f30555c73dd64ce04ff98b0e046e1a9d98c9960e`, and result digest `160c50a2177d888f6816ed1ae1215cf9e994e185c394ec3297708eae886164c7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N026 — leading-zero array index is rejected

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": [
    1,
    2
  ],
  "pointer": "/01"
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `2766196bf5d45f1b19abc6ee9dd21e04bb7a2b0d943c8b4fe7c32f0e22d11e4b`, input digest `45ee9ff74a70f46c506ef3cf654c4073a10bbb99e608f8e365092e7fdc5605c6`, and result digest `9b7c35000fc1afe6dd5f68d24b544c32d8456662cdd5f3bba0f415ba90d1da1d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N027 — negative array index is rejected

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": [
    1
  ],
  "pointer": "/-1"
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `12a3231e3e1ef4e166b275d15f974e4cd189df5f28a58956dc5200e48afc3b4a`, input digest `c29cfa6ab4197e3ea0ec7806ce878c8c15dec3085a5264a0488b87e4a77f4b8e`, and result digest `9b7c35000fc1afe6dd5f68d24b544c32d8456662cdd5f3bba0f415ba90d1da1d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N028 — append marker cannot resolve an existing element

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": [
    1
  ],
  "pointer": "/-"
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `275d350becbb1d660cbfea475ca76f2d2f3833cdf023c63f06889d7a2284f791`, input digest `8daaf8f6ae8193b26c4f865d226a3883c30b80c2f3645933cf3ec6d345c0d4ad`, and result digest `9b7c35000fc1afe6dd5f68d24b544c32d8456662cdd5f3bba0f415ba90d1da1d`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N029 — out-of-range array reference stays missing

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": [
    1
  ],
  "pointer": "/1"
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `d3ec270a271adee873071d42d91a89514578aaaf160797e97c233a827368665c`, input digest `ad826a41b638919ba9b9ffbd4a25360af5bee0be4b5c4b1bce8a7040001e93de`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N030 — a scalar cannot be traversed as a container

Family `pointer_failure_semantics`; operation `resolve`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Refuse invalid pointer syntax and nonexistent targets before any projection.

Frozen input:

```json
{
  "document": {
    "a": 0
  },
  "pointer": "/a/b"
}
```

Frozen expected result:

```json
{
  "error": "scalar_traversal"
}
```

Observed result:

```json
{
  "error": "scalar_traversal"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `66ece5e9b7be766de2d80ed98f4693b0575f1d35706605bdd4cd09b134767b0b`, input digest `9334b3236f31b690c22e36b889adb6a4c772a7316498eae54f68085cc98c0c7c`, and result digest `d1ebe0aa4cbd84b92e7330e8d1a5715aee8ac4a339f16358e52af3728733da25`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N031 — two nested leaves yield two labeled selections

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": {
    "a": {
      "x": 1,
      "y": 2
    }
  },
  "pointers": [
    "/a/x",
    "/a/y"
  ]
}
```

Frozen expected result:

```json
{
  "/a/x": 1,
  "/a/y": 2
}
```

Observed result:

```json
{
  "/a/x": 1,
  "/a/y": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `17bdd79344f7954e6778f3c40b8f5b8d083d7febca4291c4b33e588540a54e53`, input digest `177a3ca4ddd1a2bea3d4983ea1420e873140d75f953d7daaedf21ad1b2c1e234`, and result digest `54c3f5a03166c10c1ef6e7071270d3da0dd6b36fd610c0c4901886ff2712796f`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N032 — selected null retains its presence

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `312fb6bc77d4d5ee3d24f6d629e80ccb61a29efe2f0e8fecef3268c290136481`, input digest `512ef2b924e44cf053835e5187f86d8f4a5a239085fb6014b78a92134b591256`, and result digest `47e4ce6cb1e16f6dc4afc7b40f88a806a95b787ebc2452e836fd2ffb1bc970e2`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N033 — an empty selection discloses nothing

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `58407f39e7a615debfbe3ea75bb7df321927c80ca18c9bb8e3d00a56417ed76d`, input digest `753fda5efdc121ac2332e901c418a12e08054893a6d38bb0a1e50e1e7e2a8794`, and result digest `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N034 — duplicate selectors are rejected

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
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

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `95bd57d52753fb017536ec8287039fb958c154b3c846fdad35896cef8357179b`, input digest `0f3816fc14be56597bde894949b8087c88b593ac0402f4f9c9798f4ec45294f8`, and result digest `ce758311e643915e08cde527e914c8ebd7c0dd3d8d93c18b56f52005f8f21ed4`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N035 — ancestor and descendant cannot be silently double counted

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": {
    "a": {
      "b": 2
    }
  },
  "pointers": [
    "/a",
    "/a/b"
  ]
}
```

Frozen expected result:

```json
{
  "error": "overlapping_selectors"
}
```

Observed result:

```json
{
  "error": "overlapping_selectors"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `24db341d635b63bbbea7a5fb7310cb9fb57f8b987733d49779468a75ac8c3610`, input digest `fbc8bc6f38c905b5031d8fa9a73a12c6c9bf00c2dfc5cb2e4c381c450425f996`, and result digest `efedee95ff1eb3ce73959d49b086c041c95aeb9ab04925903c867a88d237ebb5`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N036 — root and child selection overlap explicitly

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": {
    "a": 1
  },
  "pointers": [
    "",
    "/a"
  ]
}
```

Frozen expected result:

```json
{
  "error": "overlapping_selectors"
}
```

Observed result:

```json
{
  "error": "overlapping_selectors"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `eceb4dfa7a3f0005d9cfbf6679e0cf2d13016f4a7bc5197813bcf0d2c45ce13d`, input digest `617820078c1e7dda6ff8d30403a33d1e62b1eab1012d3b586d8b85718f9b9316`, and result digest `efedee95ff1eb3ce73959d49b086c041c95aeb9ab04925903c867a88d237ebb5`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N037 — lexical prefix is not token ancestry

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": {
    "a": 1,
    "ab": 2
  },
  "pointers": [
    "/a",
    "/ab"
  ]
}
```

Frozen expected result:

```json
{
  "/a": 1,
  "/ab": 2
}
```

Observed result:

```json
{
  "/a": 1,
  "/ab": 2
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `f45331defff2df1b6738d31e8cdbb44ca5beca19be22d486b9314f85fcba0490`, input digest `c749d8c36a4f1fbfe559cd36e1df5d4a229d836b5ec89fce0c08132ac92910f2`, and result digest `07bcb453009424808a435b1ca27a136819bd7af4399cc3ef5a6c4342abd4ec3a`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N038 — missing selected value rejects the whole projection

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": {
    "a": 1
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
  "error": "missing_target"
}
```

Observed result:

```json
{
  "error": "missing_target"
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `e58e998ba24917c416ef16e34b933c3e2b479b405ae5a935c9c45f1313e475f3`, input digest `038da348e645894f97e21f81a99cef4024f08003450fbbd46851ec5c69d6adf7`, and result digest `4978915b998ba62a797d9df7b9f6920e8803c72f742512f5c8ac06d36cdd55e7`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N039 — array selections retain requested pointer labels

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": [
    5,
    6
  ],
  "pointers": [
    "/1",
    "/0"
  ]
}
```

Frozen expected result:

```json
{
  "/0": 5,
  "/1": 6
}
```

Observed result:

```json
{
  "/0": 5,
  "/1": 6
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `ee9e121ffde442dfeff8f719f78bca4991721bd899cda7eeaa043910c8f0844e`, input digest `a08e38d289b5d34322d000a0257558597b92a81aa92a603111ad9d5db365082f`, and result digest `9f9d1bbb0e09bb4fdffc6ecb1b87522a9f59a1555d637a0f3432b78ac9765938`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.

## MF6862-N040 — escaped slash selector does not expose sibling data

Family `pointer_projection_allowlist`; operation `project`; pillar Freed ID and CBR Heart; practice data-quality investigator; core disposition `completed`.

Project exact leaf or container pointers with explicit missing and overlap behavior.

Frozen input:

```json
{
  "document": {
    "a": {
      "b": 2
    },
    "a/b": 1
  },
  "pointers": [
    "/a~1b"
  ]
}
```

Frozen expected result:

```json
{
  "/a~1b": 1
}
```

Observed result:

```json
{
  "/a~1b": 1
}
```

The frozen oracle matched and the input-nonmutation witness passed. The reported value is bound by definition digest `5ea5f6e442d3d3ac726b204d49b40ebbfc3c4dd7ae113ac53d8abf8d0680c7c8`, input digest `aded7a2c84e9d69328b1c539e19035e3a8e2acee47c725f36d0aa11014d4d8f6`, and result digest `3b71084fe3d9a33c4b0b044e77226c68c8660164c61d2c72af878159873adfea`. These digests bind bytes in the declared sorted compact UTF-8 JSON domain, not the truth of an external claim.

An output differs from the frozen JSON value or error code, source input changes, a registered mutation passes, or a protected claim is promoted. Five registered mutations changed the report, input digest, definition digest, empirical flag, or authority flag. All five were rejected and remain in the zero-credit negative record. Retain the original fixture and failed witness; select the prior validated implementation and add a separately hashed correction.

[Primary reference](https://www.rfc-editor.org/rfc/rfc6901) supplies the stated syntax or provenance vocabulary. The concrete fixture and local restrictive profile remain attributable to this owner. A passed local check does not supply real evidence or authority for the named obligation.
