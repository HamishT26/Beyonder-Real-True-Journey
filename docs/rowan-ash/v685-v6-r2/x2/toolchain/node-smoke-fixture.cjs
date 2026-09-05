"use strict";
const fs = require("node:fs");
const math = require("mathjs");
const Decimal = require("decimal.js");
const N3 = require("n3");
const rows = [];
let rejected = false;
try { math.unit(1, "unrecognized_fixture_unit"); } catch { rejected = true; }
rows.push({package:"mathjs",version:math.version,positive_pass:math.equal(math.add(math.fraction(1,3),math.fraction(1,6)),math.fraction(1,2)),adverse_rejected:rejected,detail:"Exact fractions through the direct API and an unknown unit; no arbitrary expression parser"});
const sum = new Decimal("0.1").plus("0.2");
const nonfinite = new Decimal("NaN");
rows.push({package:"decimal.js",version:"10.6.0",positive_pass:sum.equals(new Decimal("0.3")),adverse_rejected:!nonfinite.isFinite(),detail:"Decimal addition and explicit rejection of a nonfinite value"});
const triples = new N3.Parser({format:"Turtle"}).parse("@prefix ex: <urn:example:> . ex:a ex:p 3 .");
rejected = false;
try { new N3.Parser({format:"Turtle"}).parse("@prefix ex: <urn:example:> . ex:a ex:p ["); } catch { rejected = true; }
rows.push({package:"n3",version:"2.7.4",positive_pass:triples.length===1,adverse_rejected:rejected,detail:"Inline RDF parsing and malformed Turtle"});
const result={schema:"ghc.family.node-toolchain-smokes.v1",status:rows.every(r=>r.positive_pass&&r.adverse_rejected)?"PASS":"FAIL",direct_packages:3,network_retrievals:0,rows};
fs.writeFileSync(process.argv[2],JSON.stringify(result,null,2)+"\n","utf8");
process.stdout.write(JSON.stringify(result)+"\n");
process.exitCode=result.status==="PASS"?0:1;
