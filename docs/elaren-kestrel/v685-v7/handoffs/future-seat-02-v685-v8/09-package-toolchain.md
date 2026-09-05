# 09 Package toolchain

Elaren added exactly 13 direct packages in a D-drive isolated Python 3.12 environment: mido, python-osc, portion, intervaltree, bidict, immutables, boltons, more-itertools, toolz, frozendict, jsonpointer, jsonpatch, and cbor2. Every direct wheel matched the frozen PyPI SHA-256. Fifteen runtime wheels were downloaded initially, plus a separate hash-verified bootstrap pip recovery wheel. The environment contains 16 distributions and `pip check` passes.

The initial advisory audit retained seven rows, all against bootstrap pip 25.0.1, and earns zero aggregate-success credit. Only the isolated bootstrap was updated to hash-verified pip 26.2.1; the focused audit then reported zero known vulnerabilities. That is a dated advisory snapshot, not exhaustive security.

All 13 positive package smokes passed. The first adverse aggregate rejected 10 of 13 and remains zero-credit. Isolated corrected adverse fixtures for intervaltree, more-itertools, and cbor2 passed without replaying the ten unchanged successes. The resulting status is `PASS_DEPENDENCY_CORRECTED_COMPOSITE` with zero aggregate-success credit and complete component witnesses.
