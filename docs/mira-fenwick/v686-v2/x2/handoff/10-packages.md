# 10 Three exact package additions

- `jmespath 1.1.0`: official wheel `jmespath-1.1.0-py3-none-any.whl`, SHA-256 `a5663118de4908c91729bea0acadca56526eb2698e83de10cd116ae0f4e97c64`. [Exact release](https://pypi.org/project/jmespath/1.1.0/).

- `dpath 2.2.0`: official wheel `dpath-2.2.0-py3-none-any.whl`, SHA-256 `b330a375ded0a0d2ed404440f6c6a715deae5313af40bbb01c8a41d891900576`. [Exact release](https://pypi.org/project/dpath/2.2.0/).

- `dictdiffer 0.10.0`: official wheel `dictdiffer-0.10.0-py3-none-any.whl`, SHA-256 `6ca50f38f7c5ee27d52789eee095ae473d9e02e1aa7612cb3aaf25fcf081dbf6`. [Exact release](https://pypi.org/project/dictdiffer/0.10.0/).

The new isolated D environment contains exactly three distributions. Installation used the frozen wheelhouse offline with required hashes and no runtime dependencies or optional extras. System Python, PATH, the npm prefix, plugin caches, host security, Windows features, and accounts were not changed. Nine package checks passed, including three retained adversaries. The dated OSV query returned zero findings; it does not establish exhaustive security or future safety. Query null dropping remains visible, and mutable helpers work only on synthetic copies. Rollback selects retained prior tooling and preserves the environment and receipts.
