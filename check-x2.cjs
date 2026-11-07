'use strict';
const assert = require('node:assert/strict');
const kernels = require('./kernels-x2.cjs');
const cases = require('./cases-x2.json');
for (const c of cases) {
  const before = JSON.stringify(c.input);
  const actual = kernels[c.op](c.input);
  assert.deepStrictEqual(actual, c.expected, c.id);
  assert.equal(JSON.stringify(c.input), before, c.id + ' input mutation');
}
console.log(JSON.stringify({cases:cases.length, fullLiteralMatches:cases.length, unchangedInputs:cases.length}));
