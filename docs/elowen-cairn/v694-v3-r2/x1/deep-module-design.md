# Deep module design

The module exposes one interface: execute(request). Callers need to know the operation name, the exact JSON input contract, deterministic output, and declared error modes. All validation, rounding, type checks, and operation logic remain inside the implementation.

The seam is the TXT module loader. Five runner adapters select two operations each without reimplementing them. Tests and callers cross the same seam. Removing the module would redistribute validation and arithmetic across every runner, so the module earns locality and leverage.

This design does not introduce a second adapter merely to make an abstraction look general. X2 will become a real second adapter by composing the immutable x1 interface with new operations and a self-contained HTML projection.

Same-owner finite synthetic software and documentation only. No empirical GMUT confirmation, physical observation, participant evidence, production THOS or Freed ID, professional, legal, cultural, affected-party or Maori authority, complete privacy or accessibility, exhaustive security, independent reproduction, consciousness or personhood evidence, AGI or ASI, Theory-of-Everything proof, canon, deployment, or Stage 20 readiness. NOT_READY_FOR_STAGE_20.
