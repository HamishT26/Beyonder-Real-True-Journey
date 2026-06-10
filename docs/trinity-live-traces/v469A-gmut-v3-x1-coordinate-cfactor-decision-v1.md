# v469A GMUT v3 x1 Coordinate and c-Factor Decision

Classification: `blocker`

## Core Finding

The prior compact notation:

```text
S_g = integral d4x sqrt(-g) [c^4/(16*pi*G)] (R - 2*Lambda)
```

is ambiguous. It cannot be accepted until the meaning of `d4x` is declared.

## Route A: Time Coordinate Volume

Use:

```text
dt d3x
c^4/(16*pi*G)
```

SI check:

```text
(c^4/G) -> kg m s^-2
R -> m^-2
dt d3x -> s m^3
product -> kg m^2 s^-1 = J s
```

This route is selected as the working candidate for v3 x2.

## Route B: Length-Normalized Four-Volume

Use:

```text
d4x with x0 = c t
c^3/(16*pi*G)
```

SI check:

```text
(c^3/G) -> kg s^-1
R -> m^-2
d4x -> m^4
product -> kg m^2 s^-1 = J s
```

This route remains an alternative, not the active v3 x2 lane.

## Result

The dimensional/SI gate remains open, but the ambiguity is now isolated.
