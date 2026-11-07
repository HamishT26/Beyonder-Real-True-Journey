'use strict';
const assert = require('node:assert/strict');
const kernels = require('./kernels.cjs');
const cases = require('./cases.json');
for (const c of cases) {
  const before = JSON.stringify(c.input);
  const result = kernels[c.op](c.input);
  assert.deepEqual(Object.fromEntries(Object.keys(c.expected).map(k => [k, result[k]])), c.expected, c.id);
  assert.equal(JSON.stringify(c.input), before, c.id + ' input mutation');
}
console.log(JSON.stringify({cases:cases.length, literalMatches:cases.length, unchangedInputs:cases.length}));
