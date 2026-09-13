# lease_epoch_fence

Reject stale epoch or wrong-holder requests without claiming a production lock.

The parser profile accepts UTF-8 JSON with null, Boolean values, safe decimal integers, strings, arrays, and objects. It rejects duplicate names, negative zero, fraction and exponent number spellings, unsafe integers, reserved object names, depth over 32, collections over 128, strings over 4,096 units, and input over one MiB. Some refused values are valid JSON outside this deliberately narrower profile.

## Matching holder and epoch is structurally accepted

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 3,
      "holder": "a",
      "action": "preview"
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "accepted": true,
    "reason": null,
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Older epoch is rejected

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 2,
      "holder": "a",
      "action": "preview"
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "accepted": false,
    "reason": "STALE_EPOCH",
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Future unissued epoch is rejected

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 4,
      "holder": "a",
      "action": "preview"
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "accepted": false,
    "reason": "STALE_EPOCH",
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Wrong holder is rejected

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 3,
    "current_holder": "a",
    "request": {
      "epoch": 3,
      "holder": "b",
      "action": "preview"
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "accepted": false,
    "reason": "WRONG_HOLDER",
    "current_epoch": 3,
    "current_holder": "a",
    "requested_action": "preview",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

## Zero epoch can be explicit

Request:
```json
{
  "op": "lease_epoch_fence",
  "record": {
    "current_epoch": 0,
    "current_holder": "root",
    "request": {
      "epoch": 0,
      "holder": "root",
      "action": "read"
    }
  },
  "args": {}
}
```

Frozen expected envelope:
```json
{
  "ok": true,
  "disposition": "completed",
  "value": {
    "accepted": true,
    "reason": null,
    "current_epoch": 0,
    "current_holder": "root",
    "requested_action": "read",
    "external_lock": false,
    "authority": false
  },
  "error": null,
  "external_credit": false
}
```

Same-owner synthetic software evidence only. No deployment, independent reproduction, scientific validation, complete privacy or accessibility, authority, personhood, consciousness, identity continuity, or Stage 20 credit. NOT_READY_FOR_STAGE_20.
