# Contributing

Open an issue with a minimal synthetic example, the expected behaviour and the observed behaviour. Do not submit private conversations, credentials, personal data, operating-system tokens or account screenshots.

A proposed code change should retain existing result semantics or describe the intentional change explicitly. Add examples for the changed boundary, keep the first failure in the review discussion, and separate reused checks from new checks. The maintainer reviews changes before merging.

Do not infer runtime authority from a record field or hash. Any future filesystem, network, billing or native-chat adapter requires its own capability, provenance and failure-handling design. These pure examples do not supply those controls.
