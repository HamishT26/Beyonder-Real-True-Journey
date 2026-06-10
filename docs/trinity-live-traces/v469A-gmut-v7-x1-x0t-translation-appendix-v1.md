# v469A GMUT v7 x1 x0=t Translation Appendix

Classification: `advisory`

This artifact drafts `x0=t` as a translation appendix only.

Branch policy:

- Rehearsal branch: `x0=ct`
- Appendix branch: `x0=t`
- Appendix status: `translation_hold`
- The appendix is not a parallel proof route.

## c Relocation Table

| Term | `x0=ct` Expression | `x0=t` Expression | c-Power Delta | Status |
|---|---|---|---|---|
| coordinate | `x0=ct` | `x0=t` | branch label only | `advisory` |
| differential | `dx0=c dt` | `dt` | `-1` in coordinate differential | `advisory` |
| derivative operator | `partial_0=(1/c)partial_t` | `partial_t` | `+1` in derivative basis | `advisory` |
| temporal kinetic factor | `g00 partial_0 Psi partial_0 Psi` | metric or coefficient carries explicit c placement | requires coefficient dictionary | `HOLD_OPEN_GAP` |
| measure/prefactor | `c3_over_G dx0 d3x` | `c4_over_G dt d3x` | `+1` in prefactor after `dx0=c dt` | `advisory_not_closure` |

Invalid conditions:

- treating `x0=t` as the active rehearsal branch
- mixing `x0=ct` and `x0=t` in one formula card
- moving c powers without a coefficient dictionary
- claiming physical equivalence or validation from the appendix
