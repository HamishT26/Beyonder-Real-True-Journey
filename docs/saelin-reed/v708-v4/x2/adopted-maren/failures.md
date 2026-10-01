# Retained failures

- Attempt 01: one expected baseline failure because the implementation module did not yet exist. Zero acceptance credit. No test sandbox was created.
- Attempt 03: 59 passed, one failed of 60. The logical file/directory prefix-conflict test reached restore publication and returned DESTINATION_EXISTS, rather than rejecting the selected set before writes. The synthetic partial destination and full TAP receipt remain retained. Zero acceptance credit for this failed run.
- Path repair: check every selected path prefix against the complete case-folded set; do not rely on adjacent sorted names. Attempt 04 passed all 60 tests for that historical snapshot.
- Attempt 05: one focused test failed because apiToken was accepted as a JSON key. Its synthetic object/record and full TAP receipt remain retained. Zero acceptance credit. Broader authToken/dbSecret cases were added to the same named test.
- Filter repair: reject normalized keys containing token/secret and broaden assignment checks; add synthetic Stripe/npm/GitLab/PyPI/Google OAuth token patterns. The suite also checks escaped JSON keys, structure limits, and sensitive incoming payloads with otherwise matching external source pins. The final receipt below covers the repaired behavior and the complete 60-test suite.

- attempt-06-final-suite: incomplete run, signal SIGTERM, execution error ETIMEDOUT. The three-minute runner limit expired before a complete TAP summary; zero acceptance credit. Its partial synthetic sandbox remains retained. Process inspection found no surviving test worker, and the sandbox was stable at 133 case directories. The retry keeps every ancestor check, avoids repeated walks for already-existing directories, and uses an eight-minute runner bound.

Final receipt: evidence/attempt-07-final-suite.json. Result: 60/60 passed, 0 failed, 0 skipped, exit 0. Earlier receipts are append-only and were not replaced. No external worker, inherited run, or failed attempt supplies final acceptance credit.

All .test-sandbox-* directories are retained under this contribution. Failed attempt 03 sandbox: .test-sandbox-UelOmA. Failed attempt 05 sandbox: .test-sandbox-h4Fh5O. Focused attempt 02 sandbox: .test-sandbox-QAazO4. Consult each receipt for raw output; earlier TAP path strings contain escaped backslashes.
