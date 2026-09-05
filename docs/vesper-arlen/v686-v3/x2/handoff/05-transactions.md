# 05 Layer origin immutable snapshot and transactions

## VA6863-N041 — Configuration review case 41 — layer precedence 00 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 0,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-0"
      }
    },
    {
      "service": {
        "enabled": true
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 0,
  "service": {
    "enabled": true,
    "mode": "review-0",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 0,
  "service": {
    "enabled": true,
    "mode": "review-0",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `1ffa211bece249603773396e5505d645d5869aa6b8ecb256eaf5c6f5e2a321ba`, input digest `af785d3c55e8aa25cfdc9d85c9f8b09779fba1fb066c41e8ac00c515360b847a`, and result digest `51d6b27bb56fa8c0823acfa92db3d569265890c1ef4e7c1699c5572bb9c781ce` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N042 — Configuration review case 42 — layer precedence 01 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 1,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-1"
      }
    },
    {
      "service": {
        "enabled": false
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 1,
  "service": {
    "enabled": false,
    "mode": "review-1",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 1,
  "service": {
    "enabled": false,
    "mode": "review-1",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `c70bc0bce7fbe5d8457864f7d123fd3d94548b178f7fb3c1dfb67e2f1103f764`, input digest `9954e554f29b86f753fbc9a2a0121d80ab951c2167845b4d6e7640b15b233eff`, and result digest `a5436d9ec6091b464daf7a505004033a230c361a423f21b2e9b6079f71e6a122` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N043 — Configuration review case 43 — layer precedence 02 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 2,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-2"
      }
    },
    {
      "service": {
        "enabled": true
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 2,
  "service": {
    "enabled": true,
    "mode": "review-2",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 2,
  "service": {
    "enabled": true,
    "mode": "review-2",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `3496c2470987a761102f8e3a3d3b49f60f0ea9474caad5fa9f669978b01582d9`, input digest `93a955a3826974c6e7cad3eeb396b00d0adb915b9e7f70228a6695488bd6aa1e`, and result digest `27c1cd5eebb099ad858484fd3e2bf51b95803c87c78b5b38552c151899b96455` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N044 — Configuration review case 44 — layer precedence 03 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 3,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-3"
      }
    },
    {
      "service": {
        "enabled": false
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 3,
  "service": {
    "enabled": false,
    "mode": "review-3",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 3,
  "service": {
    "enabled": false,
    "mode": "review-3",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `3cf0d2bb25f2875010b89f5395f7966e5a9aec32cca8dcff71a29041596204b1`, input digest `6de1e8df6e570f408d867f272d87e3dde707288bf809bca45d2293e679dfad18`, and result digest `2cb8380da78449564e10f7eaddadeeb2d95268a9214819366527e1e97919e27a` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N045 — Configuration review case 45 — layer precedence 04 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 4,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-4"
      }
    },
    {
      "service": {
        "enabled": true
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 4,
  "service": {
    "enabled": true,
    "mode": "review-4",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 4,
  "service": {
    "enabled": true,
    "mode": "review-4",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `770f38975b1ae002dd3c8fff5f42df80cff15546b083a24e1de9c47ac6bc8eff`, input digest `24e5294a5d6591a60e3ed253a76593eb35a354898f497243129919aa8c840e13`, and result digest `2446bbbef8e767fe274be55e8b2861b313e9b8ca1e7db36907e3a2b54e19e6bc` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N046 — Configuration review case 46 — layer precedence 05 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 5,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-5"
      }
    },
    {
      "service": {
        "enabled": false
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 5,
  "service": {
    "enabled": false,
    "mode": "review-5",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 5,
  "service": {
    "enabled": false,
    "mode": "review-5",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `2c74fb249242bd92754158a8f65960fbee71e5b8c0414bec62e28ae96cb592f3`, input digest `6597b89d9e299ed24e91edbe38e34a1cb16cd64550ab218d3e6c2c3d6f73e25f`, and result digest `5363eb29e3f5cc08def8ed98ecde84023a839a78e55db0385a3a3539fae41a2c` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N047 — Configuration review case 47 — layer precedence 06 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 6,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-6"
      }
    },
    {
      "service": {
        "enabled": true
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 6,
  "service": {
    "enabled": true,
    "mode": "review-6",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 6,
  "service": {
    "enabled": true,
    "mode": "review-6",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `f4a8b38d9d02214f0ecf9f5e962bff0a9226872ac17012412b5d2bea3f882af5`, input digest `00f51a971cf0f3197744094c00c59d1d109551aaf9eddc3eacc828a70b29c5ad`, and result digest `96e229d9c767fa93364b659d5a35adf9b055bbc640e481f8bbaf32b0240a2a3a` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N048 — Configuration review case 48 — layer precedence 07 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 7,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-7"
      }
    },
    {
      "service": {
        "enabled": false
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 7,
  "service": {
    "enabled": false,
    "mode": "review-7",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 7,
  "service": {
    "enabled": false,
    "mode": "review-7",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `5a1f98abef7fb473166b8b5ca3dfed7bf00eac57625d29e2faa1334edb0c8c16`, input digest `b055785b78bc40235478a99ff84b4181459c705206115362da2fbd7d309763db`, and result digest `0a0f53492c8336409e6d132cccc5890c368c834df50f8aaa1e2b7617ccff3a01` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N049 — Configuration review case 49 — layer precedence 08 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 8,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-8"
      }
    },
    {
      "service": {
        "enabled": true
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 8,
  "service": {
    "enabled": true,
    "mode": "review-8",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 8,
  "service": {
    "enabled": true,
    "mode": "review-8",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `8c5bd077473423ee3eff1a9e12a33ac8a52a0d81d55023052fa1461bfd957a7d`, input digest `1a4fa7ed78d94affd5ced2177f2a170fd3f9d8470d88bdeff0f6af83c291ee79`, and result digest `763b2a069e2d97153dd715c0a6c936ad320be34ecd8b57bf7975dc3c5577a5e4` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N050 — Configuration review case 50 — layer precedence 09 keeps unrelated base keys

Family `config_layer_merge`; operation `merge`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Merge declared low-to-high-precedence synthetic layers without mutating a source layer.

Frozen input:

```json
{
  "layers": [
    {
      "case": 9,
      "service": {
        "mode": "base",
        "port": 8000
      }
    },
    {
      "service": {
        "mode": "review-9"
      }
    },
    {
      "service": {
        "enabled": false
      }
    }
  ],
  "precedence": [
    "base",
    "review",
    "local"
  ]
}
```

Frozen expected result:

```json
{
  "case": 9,
  "service": {
    "enabled": false,
    "mode": "review-9",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "case": 9,
  "service": {
    "enabled": false,
    "mode": "review-9",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `7d603f584128d0d8ad1641e007d3f46cf3dc2227ccf557e31ff85bd86757a0bc`, input digest `5a4aad56a5a489288f65051bd0c888476776ecce551ab0398c06185467f35c97`, and result digest `9b10d86da9af05f353cc38365516d501affb989a2b9a53ffccb13076e2745629` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N051 — Configuration review case 51 — origin trace 00 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 0,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8100
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 0
  },
  "service.port": {
    "origin": "review",
    "value": 8100
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 0
  },
  "service.port": {
    "origin": "review",
    "value": 8100
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `39e39593800b939459b2463ef59637b81f9c5f3d14600ec4353108cf42b4c914`, input digest `4216b410e83a20f17c04b0d7a087a8c140d2476216ee58d74a3be9c2ea817976`, and result digest `2668cfd9ec349119f6c93e8dac374e97aba178b73042a54ba9b624c9524b8c85` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N052 — Configuration review case 52 — origin trace 01 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 1,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8101
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 1
  },
  "service.port": {
    "origin": "review",
    "value": 8101
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 1
  },
  "service.port": {
    "origin": "review",
    "value": 8101
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `6f40b65e60e20112e82595fcbdbc199a455c70acc4261e0a56c5366062f54971`, input digest `f5edc673254db9d5c2d052e969da40bfa517158ce21b7751c35c678e8b767a5d`, and result digest `2bd982702053dc9ce99c3585f800cb70c6a2d86a29a9efb761203b914256ffbe` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N053 — Configuration review case 53 — origin trace 02 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 2,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8102
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 2
  },
  "service.port": {
    "origin": "review",
    "value": 8102
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 2
  },
  "service.port": {
    "origin": "review",
    "value": 8102
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `ea4a7bd8d1ff3d7ffa6f7e706908350b024fa87c76c824b99fe4237d5d69e5d7`, input digest `c285d46c412e265f94b955c1c77ae5745182e52b4c27a2a63360a35aa7143e62`, and result digest `f96d73586c5dd37264ba2d5b76ea2a890057447193b372430b02fb8b8703ccc0` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N054 — Configuration review case 54 — origin trace 03 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 3,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8103
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 3
  },
  "service.port": {
    "origin": "review",
    "value": 8103
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 3
  },
  "service.port": {
    "origin": "review",
    "value": 8103
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `b9fc0d992a9c7da88d5504bdae81a4978bc3811cb727e218d5a16446820c009a`, input digest `6268557f18a3d02962dcac5bccda2bc432098424dbffdb37f51cdaec924afbcf`, and result digest `d4c38cd6d149125cb740780b18859d0d8e3a2980fa5f836a1c7694b598314031` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N055 — Configuration review case 55 — origin trace 04 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 4,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8104
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 4
  },
  "service.port": {
    "origin": "review",
    "value": 8104
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 4
  },
  "service.port": {
    "origin": "review",
    "value": 8104
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `09678a0216346008710dd617567cf37e080eca07449a002969d52bbf8178985d`, input digest `96e168ef2bd6cbc8e272fd4031ccd64bef0808286acdb0e9ac61e57094e2d829`, and result digest `71445f74a8eccffbf436c86ff4f6f75f404f0d2332186155c6e6f0a006fc78e9` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N056 — Configuration review case 56 — origin trace 05 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 5,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8105
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 5
  },
  "service.port": {
    "origin": "review",
    "value": 8105
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 5
  },
  "service.port": {
    "origin": "review",
    "value": 8105
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `ee9cb70e0e43efeb9ec26f9be834548695f47b1f973b71e78dea2fd25777cc31`, input digest `11a6dbcc2406c8348200dbfa5cdedd348977416bdbc5f10198ffe542ce92ec42`, and result digest `6918750dcf78f9e6cc30d6fcf381c441809fd407e7e6c804f8691ef5f599fdb3` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N057 — Configuration review case 57 — origin trace 06 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 6,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8106
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 6
  },
  "service.port": {
    "origin": "review",
    "value": 8106
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 6
  },
  "service.port": {
    "origin": "review",
    "value": 8106
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `63d76f62b0346a1e0e6bd28a5564fff17ed33698b44c61a9c315f2851271e463`, input digest `133d4d6ec8d50b2baccdfcde20d566db7c6ec337ecfe80117eabed14094fb8b3`, and result digest `27ef6958d1f6b9d0e1e18fdd4bf8f6d92ba1957e731a9a507681d8e41c05c0d9` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N058 — Configuration review case 58 — origin trace 07 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 7,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8107
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 7
  },
  "service.port": {
    "origin": "review",
    "value": 8107
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 7
  },
  "service.port": {
    "origin": "review",
    "value": 8107
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `5c87fc59d7981fa4f490d9461134d5a05a82d31395ea795a4a699173897dc61c`, input digest `da11af385ae03c1abba406568df3a27e90a0995f22d684cd9f934e665abe8b99`, and result digest `5c00dd754e69a1adf6cb0f094306214c30278879195f15710003221a6a96a87e` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N059 — Configuration review case 59 — origin trace 08 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 8,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8108
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 8
  },
  "service.port": {
    "origin": "review",
    "value": 8108
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 8
  },
  "service.port": {
    "origin": "review",
    "value": 8108
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `3f535498b0a2c41bb0e4d96e701a51a327df9f7cf80988f92eb9447f9ce4b7db`, input digest `bb5971583b27e3c1de76f51ac83dd90f38e555adbbab4b1f0586414df6fcb433`, and result digest `6e2481bd759ca8a7166880fa7f6b208d184e4dd27b77f55a0a1fa289f5b55702` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N060 — Configuration review case 60 — origin trace 09 identifies the winning layer

Family `config_origin_trace`; operation `origins`; pillar THOS Body; practice release-configuration maintainer; disposition `completed`.

Return the winning value and named layer for each synthetic configuration leaf.

Frozen input:

```json
{
  "layers": [
    {
      "name": "base",
      "values": {
        "case": 9,
        "service": {
          "port": 8000
        }
      }
    },
    {
      "name": "review",
      "values": {
        "service": {
          "port": 8109
        }
      }
    }
  ]
}
```

Frozen expected result:

```json
{
  "case": {
    "origin": "base",
    "value": 9
  },
  "service.port": {
    "origin": "review",
    "value": 8109
  }
}
```

Observed result:

```json
{
  "case": {
    "origin": "base",
    "value": 9
  },
  "service.port": {
    "origin": "review",
    "value": 8109
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `6229354545823b90845d9f628708d452a89b9226f0705540a0d83fe1bc7453e1`, input digest `18b4f47b5dec4ddc12408b798d0a6d04853868821b763f0c15d694aa21785eaf`, and result digest `b1654d08c022c84a933372ff09cc768a4bfc7eeb8c576141e29abcc00892885d` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N061 — Configuration review case 61 — immutable snapshot 00 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 0,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 0,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 0,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 0,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 0,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `789b2893ae7612d8ff62c83458ffb604436c0a48331dcc0f5327171e7a41fde1`, input digest `346bac053ea577a1b705e4164b7c6caace634d0452dc109a81e6da2232c7ed80`, and result digest `0c398f6ac926280e1ee9f25c436642ae502e88681704008200cbb3d3baa6fb27` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N062 — Configuration review case 62 — immutable snapshot 01 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 1,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 1,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 1,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 1,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 1,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `c90ef3f6b8ca3bace771a43808f2ca470244b463b7ce80e5ecc77d8afc6ca2d1`, input digest `4a771aa624d184c0ff2a323b7af921417bce8b7f5f13333b634b9e42ced07d7e`, and result digest `aa93ca9739e99ad1bdf4ef1585af8e9c48a2962ededabe7b564a99c58eae4217` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N063 — Configuration review case 63 — immutable snapshot 02 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 2,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 2,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 2,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 2,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 2,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `b0bd4b0c9479ce4db54a1a60b2ea00a23c5b40f31c880bf16c5613c9a9e69489`, input digest `253313354ab1b6d1cf515f45a58550147a014a62b8b6e187a3ed8c4ba757265f`, and result digest `4cad280c248e58a78e008d0a9d5f9da81fb9737455bc8e61e4aa69e80810b989` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N064 — Configuration review case 64 — immutable snapshot 03 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 3,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 3,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 3,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 3,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 3,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `5f7ee5cc516e05fa2b2d8f5b3ea297e46ab189ef7d53c2ca3fab11bd5f96344b`, input digest `91e4b2688e2dd4d5ecba3f2daea84c4e1b5be64baca733a70af73ec730169e9d`, and result digest `002c028e75b72daa76b971be03cecc5b696a06d099edc710f9daec44869f65ff` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N065 — Configuration review case 65 — immutable snapshot 04 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 4,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 4,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 4,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 4,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 4,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `7b2eda667a245e9fadcb725b44504fb40a4a66c9ac94510c9613d81d9b51e420`, input digest `5431c2302dcbf96d247ca6dcfe51ab8d3dfadaee0a3a00f2e953e5e749d151b4`, and result digest `69e7bab92526dbd2476a3321f2eaa62d3a2bc3580a44e9a8569119caa36ec636` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N066 — Configuration review case 66 — immutable snapshot 05 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 5,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 5,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 5,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 5,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 5,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `066a37af9d4212300c6df1b6d18d9e72372964ae61e6319f3ee0f297624ce95c`, input digest `756e9f47bc6d2b2bcad049f4ceb11b6163c009bc607f4dd262b916d8ada6411c`, and result digest `0b34e687e088977346e0117aed65953011b7d228bcd57c20c13d68cf535be1c9` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N067 — Configuration review case 67 — immutable snapshot 06 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 6,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 6,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 6,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 6,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 6,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `64631e7ab2a944941185471f40b8edad9e7a63e2cbdeb17c47f0234950c5ac84`, input digest `bef6d31629af0359fbd58374447a0a7183a6124bd0bcd0439291fe61f8d32e1e`, and result digest `b94c4ca6dd3ad5292cf24af00a949054553137563d9005e6254890b14f82591b` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N068 — Configuration review case 68 — immutable snapshot 07 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 7,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 7,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 7,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 7,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 7,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `46390d3f9b4775b93338ede526d418ffe4c25928a1176aaca62c680246cba7e3`, input digest `5ed9d4e2b82d774780efc1dca5e6d8f044064a6db8e0d1446db0f855e53b8097`, and result digest `8ed2b2736dec0d9f40da8b226b1401586731b428ace795845f2811e2bbe88629` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N069 — Configuration review case 69 — immutable snapshot 08 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 8,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 8,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 8,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 8,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 8,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `149f577be0fc9f7ff37228d9806a9fea235b00be85f0903fa572cbd68a580de0`, input digest `fb1992c89ff51e20c784c3c1225ee549a4d183ad834fc88c51f7ed2e6f323ccb`, and result digest `54692100fb236a1ff69721816d4bc4b469c344ddbb2d4d8d5c3edd9f2fb18660` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N070 — Configuration review case 70 — immutable snapshot 09 retains its predecessor

Family `immutable_snapshot`; operation `snapshot`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Derive a new immutable mapping while retaining the exact prior synthetic mapping.

Frozen input:

```json
{
  "base": {
    "count": 9,
    "mode": "base"
  },
  "set": {
    "approved": false,
    "mode": "review"
  }
}
```

Frozen expected result:

```json
{
  "base": {
    "count": 9,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 9,
    "mode": "review"
  }
}
```

Observed result:

```json
{
  "base": {
    "count": 9,
    "mode": "base"
  },
  "base_unchanged": true,
  "derived": {
    "approved": false,
    "count": 9,
    "mode": "review"
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `4b6ba7c2ddae17d40de0d4c8b122ab65da2020e8e900706de70d2b1ce7a269c8`, input digest `e7c636fd21efb74791c6ef06f9b3b8d37eab4acaea1c42c36f5f823015785997`, and result digest `a8f6ec271eba736d69e29f415a28c63139524519f60cfc29ed964b2d176216d4` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://pypi.org/project/immutables/0.21/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N071 — Configuration review case 71 — atomic change set 00 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-0"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8000
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-0",
    "port": 8000
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-0",
    "port": 8000
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `13025a690fe66b2aafdc0b7208bf6f8004ccb92c7044d033cac63d1446f66621`, input digest `5eeb46a5d43c1e65ff0ce7bd8bcf1a80f40555eb6415916038cf09e0a24182ab`, and result digest `7fc9419c4fe08f1172b79b0255108d0ca1b25acfc6f89fc5cc8fd80a49d5a0e7` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N072 — Configuration review case 72 — atomic change set 01 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-1"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8001
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-1",
    "port": 8001
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-1",
    "port": 8001
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `1c70d19d0343ef3e4972db922161e2a8061a6af62f1af630aa67302acf83a038`, input digest `de1fb81733f5ccda4c561df387e0c922aa1d6491efd80700dde953c52da3f3d0`, and result digest `2b1590ea97ac6bcf1ef30c9d38dc3680bde2c00a6b768e8de537eec39ea5f9b7` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N073 — Configuration review case 73 — atomic change set 02 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-2"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8002
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-2",
    "port": 8002
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-2",
    "port": 8002
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `1b82ac7e99c3f46be038a4855d1b894c091b431557ad1478b54bec651e75a0a7`, input digest `804e40dd661798c84811ca2b121169ee3220189e9e6c4880c79d1494888ce4ab`, and result digest `ed531224942b4ec1029b7a6fcf58043a67f234cb539c9f3bfc9fd20b1b66fda0` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N074 — Configuration review case 74 — atomic change set 03 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-3"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8003
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-3",
    "port": 8003
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-3",
    "port": 8003
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `9a1f5c947c9241a24b55f313bd517ecb2309e19535927b6001ceab8572208476`, input digest `4aae0a98d894e6a0f7c8bb424e8a91c0370bb625692b910824db1e2b12ceb214`, and result digest `e3e6ad5044c9f75938e72365c2652e1c55b55108f04076a2a87b96ca6282cce1` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N075 — Configuration review case 75 — atomic change set 04 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-4"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8004
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-4",
    "port": 8004
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-4",
    "port": 8004
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `e3c9172011fee314d425c4efef0c5ecee6ed0b06492466b8dd3e24f2003ae0b1`, input digest `d1d1660c0d97b28d4c83c9d7ef1edb4717dd98984be919e2c922246e4abbf536`, and result digest `871834c7c817c214ca69b1b39021e073b35e75b554afd80c811172d79f008b8a` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N076 — Configuration review case 76 — atomic change set 05 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-5"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8005
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-5",
    "port": 8005
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-5",
    "port": 8005
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `5cc2f36ddd5763ed14d68fb59551919021f3a17c199ba8113018a96585c9b9b8`, input digest `f59efb9c94589b008c00b5c3ed332da2b0bb3ecfe596dc6936ec39f381fbefe3`, and result digest `924b26fed8cf9aafbfab4771b63b068e6e326c45ddad73bc94a680cffb66e5db` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N077 — Configuration review case 77 — atomic change set 06 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-6"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8006
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-6",
    "port": 8006
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-6",
    "port": 8006
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `41ef5e72e7c844164a3ba0e9d0e90e1292b9b552eb75ca5f9122e74856737f32`, input digest `abe09cf3160d34671b207cbd116144f27b4db4fb021bb5e153c7cacfbd1d73be`, and result digest `331d3c02c795398d73b1d568843f4f51c1e16b718224b51a582c4dfa99b90e6c` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N078 — Configuration review case 78 — atomic change set 07 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-7"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8007
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-7",
    "port": 8007
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-7",
    "port": 8007
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `b9ed927f358f2343be6309c26d7aa124ac4dbc54adf76d7b9ba4ebb6ef832333`, input digest `11c548c679af2754c5bfbfc765bfee9bd1302b170c9aed51dc37213037ff8f93`, and result digest `546666259b6ca4800fe209dce74261eaf9eacaad7e8515eb1a874a8dae9eeb1d` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N079 — Configuration review case 79 — atomic change set 08 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-8"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8008
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-8",
    "port": 8008
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-8",
    "port": 8008
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `20b5257eef6711e0b5f09c916fd19a91808477eede77df0aae05d379234a0e9a`, input digest `f39486fee5e66d7bde929d14b27c8b550b6348a0bf1800f27daa27f37a7dcd65`, and result digest `8f387dcba76fd1d640bd17d104dbce06fa4604ac37cacdee5273cc05fdce51d3` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N080 — Configuration review case 80 — atomic change set 09 commits both planned leaves

Family `change_set_atomic`; operation `apply`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Apply a bounded synthetic change set to a deep copy or return one whole refusal.

Frozen input:

```json
{
  "changes": [
    {
      "op": "set",
      "path": "service.enabled",
      "value": true
    },
    {
      "op": "set",
      "path": "service.label",
      "value": "case-9"
    }
  ],
  "document": {
    "service": {
      "enabled": false,
      "port": 8009
    }
  }
}
```

Frozen expected result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-9",
    "port": 8009
  }
}
```

Observed result:

```json
{
  "service": {
    "enabled": true,
    "label": "case-9",
    "port": 8009
  }
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `6e309951542f31f3beef99a086ecc87ffb31279ce6a89438fb3b897c64f5a40b`, input digest `67b11638b93aa98e54156d074081e42f801b897c1c046f6c7c0df72780eb3d0c`, and result digest `76434a9db59432dbcdfd01e5a2e5cf87ee1a02ffdc5fcb0197b75efd8a8b195b` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N081 — Configuration review case 81 — allowlist 00 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option0"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option0"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option0"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `e0c6f1a29d3cbb3dd022e7c42eb2245bd765ef5b1ec5ff8dfc0012a7572e3d21`, input digest `9ee470cf7fdbaec7e56647fbbb0c33ff70893e0f6e4a33751015a68a864f160e`, and result digest `241f9682f30af3243240965b15debc0b563f24653e3c2ede60093a76d7ec916b` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N082 — Configuration review case 82 — allowlist 01 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option1"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option1"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option1"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `209bd5b962f78b849e932097ca421d4473f9cb6902c9be748c08db4f5dc1a146`, input digest `ea2020863dad91caa4d065f814603be8ec5198cf29d5f3b8f13be0197b775ef2`, and result digest `ac913f389b2fd2c050d4edf3931bb59280a9deeca7a985f8fdbb0299613b8885` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N083 — Configuration review case 83 — allowlist 02 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option2"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option2"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option2"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `25f79d3376423dcf083b3d62b238b6192833421f5b5e8d8487acd9c9935b73ba`, input digest `9bdc65002632abd9d960bc395fb807fb5178d490c8277670ff0df71360002a0e`, and result digest `17ed831b2996a721f9028e803146a9e31cd0757234dd58e69b00293723699e92` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N084 — Configuration review case 84 — allowlist 03 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option3"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option3"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option3"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `f3a7f8e0a85a2828d09bf83590360366bc9c1e9747f2a3b2bd97c0049674efce`, input digest `6ae262b50b2f3db1ba9c87806ffcdaa97abb44442362c8e35753badc8ed60302`, and result digest `0541d93d0f0185ede695dda0f63a5b4ef58aa7f109b95958f392b66dcfc46df0` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N085 — Configuration review case 85 — allowlist 04 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option4"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option4"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option4"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `2b68ab3ae9ee023266d3d015c52b651044655cffdf61bf0beaf826827ef3fc6d`, input digest `36b39c9999e13e3ed9ed8d517299c88db8475fda1e8b77a944ca5fb5474fbfb7`, and result digest `51ac62e6ebdc3c29ada0306bb0d18a4c6ea8bbd9543dd96686283bb038f946ec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N086 — Configuration review case 86 — allowlist 05 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option5"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option5"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option5"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `1f058c10682a0126e5a41a0d8eb17797777c6c712b85bbc0347283e387b9cc2d`, input digest `90b4a4ee8dae180bbca6c3e3101e7b20768fd5926987c9dec4382a95393aa5fc`, and result digest `d2f111e8adc8b10d1b27910179b679cf23932825d62057994cfbbbe359d53e69` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N087 — Configuration review case 87 — allowlist 06 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option6"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option6"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option6"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `d90792e0bbbccb815b7e578924617c8bde9198bd22ad6d77a159732d9e63220a`, input digest `d8b936d3a648de1511e15ba1c753de0ddd89674204aa3ac61b7fa26f0e859f16`, and result digest `7dafca440078f6e042516ecde11b79f20615d9d7d2229660799c5f37673121bf` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N088 — Configuration review case 88 — allowlist 07 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option7"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option7"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option7"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `c626658aba89cf2dbbc7610fb122ef761b90095ea51f095f6f6117107d230332`, input digest `6dec06b93a20111a1993d3525145fa03f964175e9a3251ab99cacd7c3b40669c`, and result digest `5b0a6113ea03b10ac654fd2ef6df68c24be9c712684a3f96ad116f4f4ae59258` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N089 — Configuration review case 89 — allowlist 08 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option8"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option8"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option8"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `933e19fdd152d08e717d2af19fa72c364de97e729fb404f4df33cf90a0454376`, input digest `5f565484d06b2242d2e9cf26a7cedb94a3d66147624cc02aea00dbce95148238`, and result digest `483e9c2e279101fd81ad439972c73c191acfd7080c9a1613e406e06e813db41e` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N090 — Configuration review case 90 — allowlist 09 distinguishes token ancestry from text prefix

Family `change_allowlist`; operation `authorize`; pillar Freed ID and CBR Heart; practice configuration-change reviewer; disposition `completed`.

Authorize only token-aware descendants of an explicit synthetic configuration prefix.

Frozen input:

```json
{
  "allowed": [
    "service"
  ],
  "paths": [
    "service.option9"
  ],
  "requested_by": "synthetic-reviewer"
}
```

Frozen expected result:

```json
{
  "authorized": true,
  "paths": [
    "service.option9"
  ]
}
```

Observed result:

```json
{
  "authorized": true,
  "paths": [
    "service.option9"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `7a76be7ae01c031df58492aa83402266d22c0c6e401c54325b72d9c52ca5b765`, input digest `699e9538ac6713b150665a3fd99fdda7455e576714209917107e527bf3477933`, and result digest `9d50314654bcad0214336f7995dd99360028b24956eae917c7a28fcf3046c454` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/glossary/term/configuration_control) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N091 — Configuration review case 91 — rollback chain 00 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "8605404486711b4eb3f96e4e6df9f613f23814ab7d3bc1ef37188720c5c5da75",
      "ordinal": 1,
      "parent_sha256": "6f80b3e4cd7ae04d5165899acc379dd76fbb10bcc8f1bf38b5ef9259ddf0c823",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 0,
      "revision": 0
    },
    {
      "case": 0,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "6f80b3e4cd7ae04d5165899acc379dd76fbb10bcc8f1bf38b5ef9259ddf0c823",
  "tip_sha256": "8605404486711b4eb3f96e4e6df9f613f23814ab7d3bc1ef37188720c5c5da75"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "6f80b3e4cd7ae04d5165899acc379dd76fbb10bcc8f1bf38b5ef9259ddf0c823",
  "tip_sha256": "8605404486711b4eb3f96e4e6df9f613f23814ab7d3bc1ef37188720c5c5da75"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `82699a52466cc6887a470c7d611bacf35d77a3c83d470dff06f4fa4289eda200`, input digest `334c8ff92bacdf31fa0dcea0f847d4483988a505f460844b6e9fa993613c4bca`, and result digest `0e2a48eecda6c3d5d8bee92e3bc1fa4e45ca930e3543966cc0e4dca597b5ace1` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N092 — Configuration review case 92 — rollback chain 01 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "a444f9f1f3936c1d72f3490fd4c2f552d45efae8a1ae1f45387c57137613d04a",
      "ordinal": 1,
      "parent_sha256": "1c05231e3fd066d77a377c6e0cffa1c560d592317c034ec37e47a828f3a497bb",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 1,
      "revision": 0
    },
    {
      "case": 1,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "1c05231e3fd066d77a377c6e0cffa1c560d592317c034ec37e47a828f3a497bb",
  "tip_sha256": "a444f9f1f3936c1d72f3490fd4c2f552d45efae8a1ae1f45387c57137613d04a"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "1c05231e3fd066d77a377c6e0cffa1c560d592317c034ec37e47a828f3a497bb",
  "tip_sha256": "a444f9f1f3936c1d72f3490fd4c2f552d45efae8a1ae1f45387c57137613d04a"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `fbd499caad5a7f247bb6f9789008f5d089659e0f6a61e2e81d9ae6c63c4c4c23`, input digest `24af0abd8280cef77967dbac0d33d209d6d9a8a57a0140c341f980e4b856fe62`, and result digest `0d1676cf91cc16a2b6b7da42e000f53f2f31a14bea340aade11ab5ed055cec6c` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N093 — Configuration review case 93 — rollback chain 02 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "64d632e6098bfcc584dfbec6837a263085c5a86af7bc1f3cc436d1fb32d1210c",
      "ordinal": 1,
      "parent_sha256": "d56efab682e03dee17bd85278c62931537bff2afd21fefefa55853ad7ad8d664",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 2,
      "revision": 0
    },
    {
      "case": 2,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "d56efab682e03dee17bd85278c62931537bff2afd21fefefa55853ad7ad8d664",
  "tip_sha256": "64d632e6098bfcc584dfbec6837a263085c5a86af7bc1f3cc436d1fb32d1210c"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "d56efab682e03dee17bd85278c62931537bff2afd21fefefa55853ad7ad8d664",
  "tip_sha256": "64d632e6098bfcc584dfbec6837a263085c5a86af7bc1f3cc436d1fb32d1210c"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `7e963ed7662597438fcbd45c9c3f3ded23214e396a64337dfcf714ecdcf07681`, input digest `0868de018bc9ce9d54e42472a645c7d382ea3fc1512d1016bc3c18f57a607d1f`, and result digest `d7401b9049d39652a68c41f7c03f9fa024714e7688c4a648e44c685b1148595b` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N094 — Configuration review case 94 — rollback chain 03 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "8074b699a9b532c5f03584d91e3b5c051c9ce0b695acc2dede05b37fd585cde2",
      "ordinal": 1,
      "parent_sha256": "e1394566c4f5d945d970dd8490b77f032c1036d1dd9150500c004451627f3ab4",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 3,
      "revision": 0
    },
    {
      "case": 3,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "e1394566c4f5d945d970dd8490b77f032c1036d1dd9150500c004451627f3ab4",
  "tip_sha256": "8074b699a9b532c5f03584d91e3b5c051c9ce0b695acc2dede05b37fd585cde2"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "e1394566c4f5d945d970dd8490b77f032c1036d1dd9150500c004451627f3ab4",
  "tip_sha256": "8074b699a9b532c5f03584d91e3b5c051c9ce0b695acc2dede05b37fd585cde2"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `f21085ab6e8e9998b36c8f8bfd3675847f73f6421c49c57ec4aa678b459c2433`, input digest `3589aee8c97a28c68ec280ac04f0d9a02b036a4d012f7821eba9b2fe970e3505`, and result digest `3d2e26ee0401bcb1e64c9de1b8a0f1978027fdfd57d215b69e3bcf59753812ef` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N095 — Configuration review case 95 — rollback chain 04 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "17efa2bd33d558f031eba573fce61705442a49eb8dbc6a73579b9302f12964ce",
      "ordinal": 1,
      "parent_sha256": "550b862807baf317d1824ef1f3ce5f05b39bdc68beb73b130c1f38405707fd23",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 4,
      "revision": 0
    },
    {
      "case": 4,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "550b862807baf317d1824ef1f3ce5f05b39bdc68beb73b130c1f38405707fd23",
  "tip_sha256": "17efa2bd33d558f031eba573fce61705442a49eb8dbc6a73579b9302f12964ce"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "550b862807baf317d1824ef1f3ce5f05b39bdc68beb73b130c1f38405707fd23",
  "tip_sha256": "17efa2bd33d558f031eba573fce61705442a49eb8dbc6a73579b9302f12964ce"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `4fc2ca621a43d63d47f8670df154413b82b78a931a34d8e93fe61c8a2f65d0af`, input digest `fe01fa51e6026b85cd64663c1fea6d425daa601868d3a3e11ad09c66378ffff0`, and result digest `2fd59488a3dc1e2cf45988d455ca119585a6bca729a63d6443d5219b71f9278d` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N096 — Configuration review case 96 — rollback chain 05 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "1b159e259e364dbc7ef89df92d3fb3781b9a9907a5782dcc745a6b7559d8d1b1",
      "ordinal": 1,
      "parent_sha256": "a8e0023108dd61d684de9fa60becbe7faa02b65e2e20ce44b2ff214c72b41211",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 5,
      "revision": 0
    },
    {
      "case": 5,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "a8e0023108dd61d684de9fa60becbe7faa02b65e2e20ce44b2ff214c72b41211",
  "tip_sha256": "1b159e259e364dbc7ef89df92d3fb3781b9a9907a5782dcc745a6b7559d8d1b1"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "a8e0023108dd61d684de9fa60becbe7faa02b65e2e20ce44b2ff214c72b41211",
  "tip_sha256": "1b159e259e364dbc7ef89df92d3fb3781b9a9907a5782dcc745a6b7559d8d1b1"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `3dff6dd389b9fab4167344feab7f8da850c304363cc6f29abd80e9d63b909238`, input digest `2e7c6f9c4cec1f7d344fbef384defe6207fa244ceb69f39582112317a4448ac1`, and result digest `cbd3adc7fa58738e850eacb0ec7ed6b3dfbdb3e71ede435ab3e6009786f11c72` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N097 — Configuration review case 97 — rollback chain 06 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "2fd43631d65516ee4a19180e6b450dbd9b1893fe39c6f6e6b409d083081ebbf0",
      "ordinal": 1,
      "parent_sha256": "be06494b5954554927f372d4bda37ae924493dcf0d79070f03b1bd337c118634",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 6,
      "revision": 0
    },
    {
      "case": 6,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "be06494b5954554927f372d4bda37ae924493dcf0d79070f03b1bd337c118634",
  "tip_sha256": "2fd43631d65516ee4a19180e6b450dbd9b1893fe39c6f6e6b409d083081ebbf0"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "be06494b5954554927f372d4bda37ae924493dcf0d79070f03b1bd337c118634",
  "tip_sha256": "2fd43631d65516ee4a19180e6b450dbd9b1893fe39c6f6e6b409d083081ebbf0"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `16000ffe1a70f823939c91bb621feea7aa84d7655ef30da9e5b1b897384764b7`, input digest `8237bbfde1358662e813fb6268714e4ab6948d3597cc6b3e77ca8ecdea3a66ec`, and result digest `78492d8eb44e1b7b35cb9490cc8a88133789c731dec1b945032d4262b657f3f1` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N098 — Configuration review case 98 — rollback chain 07 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "94f6e9718e568f0fb376bba0ff90af92d0352bbb3faf6006530236ac6f93e75d",
      "ordinal": 1,
      "parent_sha256": "8126f4515e96b52fb35517b2e2ac1d8380efe0c9c35e369958468f88f58c95f1",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 7,
      "revision": 0
    },
    {
      "case": 7,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "8126f4515e96b52fb35517b2e2ac1d8380efe0c9c35e369958468f88f58c95f1",
  "tip_sha256": "94f6e9718e568f0fb376bba0ff90af92d0352bbb3faf6006530236ac6f93e75d"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "8126f4515e96b52fb35517b2e2ac1d8380efe0c9c35e369958468f88f58c95f1",
  "tip_sha256": "94f6e9718e568f0fb376bba0ff90af92d0352bbb3faf6006530236ac6f93e75d"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `ddd520af08e469c440960c428e6d44d5621e9b85268c855da70641bd68410def`, input digest `4f9712f2e5af7da9409bc49ef4448cbd7258abff471c661a1a9e2a0dce432660`, and result digest `63b9139d972435e006a78472c715b55292f5a5524cede94cbb4a752f181b4724` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N099 — Configuration review case 99 — rollback chain 08 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "21df0dfb0fcc4f853947c902f32704fbc4e48559916a91fdfeb4f1523e747d15",
      "ordinal": 1,
      "parent_sha256": "ce63fcd59986b962a27be3ec102eaedd34009a31aac82ae70dda40204878d1b7",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 8,
      "revision": 0
    },
    {
      "case": 8,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "ce63fcd59986b962a27be3ec102eaedd34009a31aac82ae70dda40204878d1b7",
  "tip_sha256": "21df0dfb0fcc4f853947c902f32704fbc4e48559916a91fdfeb4f1523e747d15"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "ce63fcd59986b962a27be3ec102eaedd34009a31aac82ae70dda40204878d1b7",
  "tip_sha256": "21df0dfb0fcc4f853947c902f32704fbc4e48559916a91fdfeb4f1523e747d15"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `8621220cdf779835b56a7b15f50ee2f92154f8bf09a60d60cd4af2397b6e857e`, input digest `fbb2302510f21ab4b51e3afeae4f65de019ca8887695aa92f0cba043d4609b6d`, and result digest `60ea28467c6e3ea858dafa46858c80170dcb104b999ed79508588fde820dc56a` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N100 — Configuration review case 100 — rollback chain 09 binds the prior snapshot

Family `rollback_digest_chain`; operation `chain`; pillar THOS Body; practice rollback-drill recorder; disposition `completed`.

Bind retained predecessor and successor snapshots with exact digests and rollback intent.

Frozen input:

```json
{
  "links": [
    {
      "child_sha256": "9c42837d8fcb79e5e6c142deee9d6d738e26fed66dfcbe95b42dff2fb53539be",
      "ordinal": 1,
      "parent_sha256": "6e0a8d6c567a7a3300806cae0253acf1b7189faa70a750e7ec40cf5b67f7b042",
      "reason": "synthetic reviewed change"
    }
  ],
  "snapshots": [
    {
      "case": 9,
      "revision": 0
    },
    {
      "case": 9,
      "revision": 1
    }
  ]
}
```

Frozen expected result:

```json
{
  "links": 1,
  "rollback_sha256": "6e0a8d6c567a7a3300806cae0253acf1b7189faa70a750e7ec40cf5b67f7b042",
  "tip_sha256": "9c42837d8fcb79e5e6c142deee9d6d738e26fed66dfcbe95b42dff2fb53539be"
}
```

Observed result:

```json
{
  "links": 1,
  "rollback_sha256": "6e0a8d6c567a7a3300806cae0253acf1b7189faa70a750e7ec40cf5b67f7b042",
  "tip_sha256": "9c42837d8fcb79e5e6c142deee9d6d738e26fed66dfcbe95b42dff2fb53539be"
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `cedbdcb149e131c9f60335f60972ef289c87a8e581a0fac614ba36c5088beab9`, input digest `3477ffce35c8fd493261764fa2a198fe39fe610917c1195b2c9ff06aa91e0460`, and result digest `bc566364446fc281f4838936eddf0fb3f5edde7f849fdf19de9c56831827647f` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://www.w3.org/TR/prov-o/) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N101 — Configuration review case 101 — semantic diff 00 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 0,
    "service": {
      "label": "new",
      "port": 8001
    }
  },
  "before": {
    "case": 0,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `745eea2d1225e898b0ddc4a77ca4fc3289301baddb468580d5fe1079f297d473`, input digest `e02f84f7a964cb1bfe937c10ba7ba7f76c7e69d29236c459a3e562c4017c317c`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N102 — Configuration review case 102 — semantic diff 01 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 1,
    "service": {
      "label": "new",
      "port": 8002
    }
  },
  "before": {
    "case": 1,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `b86350fdc646a274bf7f6f544574b16de797957d712b38618aa86dc518f9c8fd`, input digest `a100584d21b82d87c67f59cd3d1d82f5df042bd8aa9865951a17d2d90a42c73d`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N103 — Configuration review case 103 — semantic diff 02 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 2,
    "service": {
      "label": "new",
      "port": 8003
    }
  },
  "before": {
    "case": 2,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `b9e7c8fa72c7493e9b5e7350ff181ff11128fdc64f825fc64ff330dbd8759118`, input digest `6ea2892ad4d2ad06e810b938105ed8fe863e203f3a0e3c6170190a36132ac124`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N104 — Configuration review case 104 — semantic diff 03 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 3,
    "service": {
      "label": "new",
      "port": 8004
    }
  },
  "before": {
    "case": 3,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `fd0cbca46fceabcd8649e41b94f2c3a41a4223413c9d2f90fe3a40bc6af94f8f`, input digest `be1596258fa14666ecead8fc2d9f3fa181ddab9d33ac730011276391a1346292`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N105 — Configuration review case 105 — semantic diff 04 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 4,
    "service": {
      "label": "new",
      "port": 8005
    }
  },
  "before": {
    "case": 4,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `6541d1b3df09fce4ae21ed96d9b2fbc47ab5f2619d4c58a53aea4ee48052db7f`, input digest `83a068355087e5ce3ff8447e01cfeb331c92fd717007df83af6ebc118b2fe8c6`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N106 — Configuration review case 106 — semantic diff 05 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 5,
    "service": {
      "label": "new",
      "port": 8006
    }
  },
  "before": {
    "case": 5,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `22886b3dfedfb719c22fcb7696ae55b4f03d46dd9d5efd3ebbde54ace9c61c17`, input digest `91645e6c902c400acf252106eea81e437a86fe199e819dc822a8e59460cde0b9`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N107 — Configuration review case 107 — semantic diff 06 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 6,
    "service": {
      "label": "new",
      "port": 8007
    }
  },
  "before": {
    "case": 6,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `19d470791b5038b98334c125958f79f54e37ce9ca38ccd3fd810e805ea34d8a7`, input digest `780baf64781d8a08b8b27458e678017f69fb2e034cf40a1d7fd5a847d4cbb4ba`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N108 — Configuration review case 108 — semantic diff 07 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 7,
    "service": {
      "label": "new",
      "port": 8008
    }
  },
  "before": {
    "case": 7,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `9c6689899abba83febcc2663a2b5ea4363681decaccd1a7d1db6fee12b573b4f`, input digest `bb738abe6ddfd1424b8ff1d97216f41a052f8749097cd6e87863551919ec8f35`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N109 — Configuration review case 109 — semantic diff 08 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 8,
    "service": {
      "label": "new",
      "port": 8009
    }
  },
  "before": {
    "case": 8,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `7cf9271546435787c076a3c6f5d937f67c11b4246424ee5f1178ef418017f93b`, input digest `19863a5ec881fb97e4569cd7ecee7bf879d7e064098126540c8f7f7bc5a2924f`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.

## VA6863-N110 — Configuration review case 110 — semantic diff 09 reports only changed leaves

Family `semantic_diff_class`; operation `diff`; pillar THOS Body; practice configuration-change reviewer; disposition `completed`.

Classify exact synthetic leaf changes without treating presentation order as a semantic change.

Frozen input:

```json
{
  "after": {
    "case": 9,
    "service": {
      "label": "new",
      "port": 8010
    }
  },
  "before": {
    "case": 9,
    "service": {
      "label": "old",
      "port": 8000
    }
  },
  "breaking_prefixes": [
    "service.port"
  ]
}
```

Frozen expected result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

Observed result:

```json
{
  "classification": "breaking",
  "paths": [
    "service.label",
    "service.port"
  ]
}
```

The frozen oracle and input-nonmutation witnesses passed. The report is bound by definition digest `60f4ba58cde0e34c34cc59175daaea0e11a4fcb9fb49a0d8cba2e211d8907a56`, input digest `f0814c32b45ff43ca2e09a504255b9cae49c528aefcbfb2f143d62bd8361c667`, and result digest `5b16b3bd64cc1d12ca78be3de43fe75824566de6de52834b043b6baa67404cec` in the declared compact UTF-8 JSON domain. These digests bind bytes, not an external claim.

A value, JSON type, refusal code, input digest, definition digest, or protected-gate state differs from the frozen contract. Five preregistered envelope mutations were rejected and remain zero-credit negatives. Retain the failed fixture and select the prior validated bytes; add a separately hashed correction without erasure.

[Primary reference](https://csrc.nist.gov/pubs/sp/800/128/upd1/final) supplies vocabulary or exact package metadata only; the concrete fixture and restrictive profile remain attributable to this owner.
