# Run (3), Saelin x1 result

Fifteen declared finite variational contracts passed all 66 checks. The arithmetic uses exact rational sparse-polynomial coefficients. Literal manually derived residuals serve as the equation oracle; energy consistency checks reuse the same implementation. Execution took 0.009788200000912184 seconds inside Python 3.12.10. Process peak RSS was not measured.

| Model | Name | Residuals, with each expression equal to zero on shell |
| --- | --- | --- |
| A01 | Canonical oscillator | q: {"a":"1","q":"1"} |
| A02 | Mixed kinetic form | q: {"a":"2","b":"1","q":"1"}; r: {"a":"1","b":"3","r":"2"} |
| A03 | Coordinate-dependent mass | q: {"a":"1","q":"1","q*v^2":"1","q^2*a":"1"} |
| A04 | Quartic interaction | q: {"a":"1","q*r^2":"1","q^3":"1"}; r: {"b":"1","q^2*r":"1","r^3":"1"} |
| A05 | Time-dependent mass | q: {"a*t":"1","q":"1","v":"1"} |
| A06 | External forcing | q: {"a":"1","q":"1","t":"-1"} |
| A07 | Gyroscopic coupling | q: {"a":"1","w":"-1"}; r: {"b":"1","v":"1"} |
| A08 | Total derivative | q: {"a":"1","q":"1"} |
| A09 | Cyclic coordinate | q: {"a":"1","q*w^2":"-1"}; r: {"b":"1","q*v*w":"2","q^2*b":"1"} |
| A10 | Translational pair symmetry | q: {"a":"1","q":"1","r":"-1"}; r: {"b":"1","q":"-1","r":"1"} |
| A11 | Anchored lattice gradient | q: {"a":"1","q":"2","r":"-1"}; r: {"b":"1","q":"-1","r":"2"} |
| A12 | Holonomic multiplier | l: {"1":"1","q^2":"-1","r^2":"-1"}; q: {"a":"1","q*l":"-2"}; r: {"b":"1","r*l":"-2"} |
| A13 | Rayleigh dissipation | q: {"a":"1","q":"1","v*g":"1"}; r: {"b":"1","r":"1","w*g":"1"} |
| A14 | Linear coordinate pullback | q: {"a":"2","q":"2"}; r: {"b":"2","r":"2"} |
| A15 | Sum-only parameter observation | q: {"a":"1","q*p":"1","q*s":"1"} |

The total-derivative model retains the oscillator equation; the time-dependent mass and forcing examples include explicit time terms. The holonomic example also requires its multiplier constraint. Rayleigh dissipation is a separately declared generalized force. The parameter example distinguishes the observable sum from its nonidentifiable individual components. All units are normalized toy-mechanics units. No gravitational field equation, empirical dataset, independent executor or novel fundamental law is established by this stage.

The 66 checks include positive residual oracles, deliberate corruption refusals, engine checks and same-engine energy identities. The first run passed; no historical run-two suite was replayed. The exact source hashes are in x1-results.json. Further discrete-variation or cross-language work belongs to a separate x2 stage after team review.

Reference context: MIT OpenCourseWare lists variational equations, coordinate transformations, total derivatives and conserved quantities in its [Classical Mechanics computational course](https://ocw.mit.edu/courses/12-620j-classical-mechanics-a-computational-approach-fall-2008/pages/readings/). The results here were calculated from the declared source; the course link is background, not an execution receipt.

The standalone explorer and host-styled Page fragment are separate representations of the same declared model data. The Page fragment source was read back with matching bytes after insertion in the private Space. Script syntax, four evaluator cases, four DOM-stub validation cases and three state-restoration cases were checked. Live rendering and full accessibility remain unverified because the browser trust connection was unavailable.
