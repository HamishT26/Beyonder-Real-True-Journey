# resolution_receipt

Bind a decision to exact base, left, right and decision digests.

The data profile admits null, booleans, safe decimal integers, strings, arrays and objects. Fractions, exponent lexemes, negative zero and reserved object keys are outside this profile. Limits are one MiB, depth 32, 128 collection members and 4096 string units. This narrower profile is not a claim that all refused subjects are invalid JSON.

The following frozen cases show complete input and output, including deliberate business holds.

## A decision binds to all four exact contexts

Request:
```json
{
  "op": "resolution_receipt",
  "record": {
    "base": {
      "v": 1,
      "k": 0
    },
    "left": {
      "v": 2,
      "k": 0
    },
    "right": {
      "v": 1,
      "k": 0
    }
  },
  "args": {
    "decisions": {
      "v": "left"
    },
    "claims": {
      "base": "e8dcb54b754f09cf0eaabadd25c51650d24a635f587c0af65a723e02a7b6c470",
      "left": "48fef3934e4ac7805ece610d2a4d24d81123ed9f7cf8773a9f1cd6f721c70068",
      "right": "e8dcb54b754f09cf0eaabadd25c51650d24a635f587c0af65a723e02a7b6c470",
      "decisions": "d47d2877dc462fa3ee89c65a93544e0aba53ac344947fde0de623e2d7ca2c7e8"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "bound": true,
    "mismatch_domains": [],
    "actual": {
      "base": "e8dcb54b754f09cf0eaabadd25c51650d24a635f587c0af65a723e02a7b6c470",
      "left": "48fef3934e4ac7805ece610d2a4d24d81123ed9f7cf8773a9f1cd6f721c70068",
      "right": "e8dcb54b754f09cf0eaabadd25c51650d24a635f587c0af65a723e02a7b6c470",
      "decisions": "d47d2877dc462fa3ee89c65a93544e0aba53ac344947fde0de623e2d7ca2c7e8"
    },
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## A changed left context invalidates its receipt

Request:
```json
{
  "op": "resolution_receipt",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 2
    }
  },
  "args": {
    "decisions": {},
    "claims": {
      "base": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "left": "0000000000000000000000000000000000000000000000000000000000000000",
      "right": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "decisions": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "bound": false,
    "mismatch_domains": [
      "left"
    ],
    "actual": {
      "base": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "left": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "right": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "decisions": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
    },
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## A missing right digest stays unbound

Request:
```json
{
  "op": "resolution_receipt",
  "record": {
    "base": {
      "v": 1
    },
    "left": {
      "v": 2
    },
    "right": {
      "v": 3
    }
  },
  "args": {
    "decisions": {
      "v": "right"
    },
    "claims": {
      "base": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "left": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "right": null,
      "decisions": "f8c2e199aa54daff9d1b30e84a2a3571f8324b992a00351b150ff7abe2f62b9d"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "bound": false,
    "mismatch_domains": [
      "right"
    ],
    "actual": {
      "base": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "left": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "right": "ff3acadf3b29fc4fa59d5b9612db39960c223344122be86dfaf4075be7c50279",
      "decisions": "f8c2e199aa54daff9d1b30e84a2a3571f8324b992a00351b150ff7abe2f62b9d"
    },
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## A changed decision digest cannot reuse an earlier binding

Request:
```json
{
  "op": "resolution_receipt",
  "record": {
    "base": {
      "v": 1
    },
    "left": {},
    "right": {
      "v": 2
    }
  },
  "args": {
    "decisions": {
      "v": "right"
    },
    "claims": {
      "base": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "left": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
      "right": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "decisions": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "bound": false,
    "mismatch_domains": [
      "decisions"
    ],
    "actual": {
      "base": "afbf9d0f3560b0fd7795e81c42a0a79ee6b6fc67e064f77826aee642cad28d91",
      "left": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
      "right": "2b5442799fccc3af2e7e790017697373913b7afcac933d72fb5876de994f659a",
      "decisions": "f8c2e199aa54daff9d1b30e84a2a3571f8324b992a00351b150ff7abe2f62b9d"
    },
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Four contradictory digest claims remain separately visible

Request:
```json
{
  "op": "resolution_receipt",
  "record": {
    "base": {},
    "left": {
      "v": null
    },
    "right": {
      "v": false
    }
  },
  "args": {
    "decisions": {
      "v": "right"
    },
    "claims": {
      "base": "0000000000000000000000000000000000000000000000000000000000000000",
      "left": "0000000000000000000000000000000000000000000000000000000000000000",
      "right": "0000000000000000000000000000000000000000000000000000000000000000",
      "decisions": "0000000000000000000000000000000000000000000000000000000000000000"
    }
  }
}
```

Expected complete envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "bound": false,
    "mismatch_domains": [
      "base",
      "decisions",
      "left",
      "right"
    ],
    "actual": {
      "base": "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a",
      "left": "aae9e223dcdc02dfd8149da8c25b9536533a7232b0c9137ee6b2cd5c2a2629eb",
      "right": "eeb0deb9cb259a55fdff2c5ed5d0a08dba3ff585aafa0821cc51889f7660739e",
      "decisions": "f8c2e199aa54daff9d1b30e84a2a3571f8324b992a00351b150ff7abe2f62b9d"
    },
    "external_authority": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
