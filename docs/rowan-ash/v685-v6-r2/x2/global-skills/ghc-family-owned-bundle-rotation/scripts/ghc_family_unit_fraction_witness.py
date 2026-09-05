"""Exact finite unit-fraction witnesses; never a universal proof."""
from fractions import Fraction
import argparse
import json
import math
import time
from pathlib import Path

def positive_int(x):
    return type(x) is int and x > 0

def verify(n, denominators, distinct=True):
    if not positive_int(n) or len(denominators) != 3:
        return False
    if not all(positive_int(x) for x in denominators):
        return False
    if distinct and not (n > 2 and denominators[0] < denominators[1] < denominators[2]):
        return False
    return sum((Fraction(1, x) for x in denominators), Fraction()) == Fraction(4, n)

def squared_divisors(b):
    factors = []
    p = 2
    remainder = b
    while p * p <= remainder:
        e = 0
        while remainder % p == 0:
            remainder //= p
            e += 1
        if e:
            factors.append((p, 2 * e))
        p += 1 if p == 2 else 2
    if remainder > 1:
        factors.append((remainder, 2))
    divisors = [1]
    for prime, exponent in factors:
        divisors = [d * prime ** e for d in divisors for e in range(exponent + 1)]
    return sorted(d for d in divisors if d < b)

def witness(n, seconds=1.0):
    if not positive_int(n) or n <= 2:
        raise ValueError("Distinct-denominator search requires an integer n > 2")
    if not math.isfinite(seconds) or seconds <= 0:
        raise ValueError("A positive finite time budget is required")
    start = time.monotonic()
    if n % 2 == 0:
        k = n // 2
        ds, method = [k, k + 1, k * (k + 1)], "known_even_construction"
    elif n % 3 == 0:
        k = n // 3
        ds, method = [k, 4 * k, 12 * k], "known_multiple_of_three_construction"
    else:
        ds = None
        method = "finite_divisor_search"
        for x in range(n // 4 + 1, 3 * n // 4 + 1):
            if time.monotonic() - start > seconds:
                return {"n": n, "status": "open_gap", "reason": "time_budget_exhausted", "universal_proof": False}
            r = Fraction(4, n) - Fraction(1, x)
            a, b = r.numerator, r.denominator
            for u in squared_divisors(b):
                v = b * b // u
                if (u + b) % a == 0 and (v + b) % a == 0:
                    y, z = (u + b) // a, (v + b) // a
                    if x < y < z:
                        ds = [x, y, z]
                        break
            if ds:
                break
        if ds is None:
            return {"n": n, "status": "open_gap", "reason": "finite_search_exhausted", "universal_proof": False}
    if not verify(n, ds):
        raise ArithmeticError("Construction failed independent Fraction equality or distinctness")
    return {"n": n, "denominators": ds, "sum": str(sum(Fraction(1, d) for d in ds)),
            "target": str(Fraction(4, n)), "status": "completed", "method": method,
            "universal_proof": False}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--start", type=int, default=3)
    ap.add_argument("--end", type=int, default=1000)
    ap.add_argument("--output", type=Path, required=True)
    a = ap.parse_args()
    if not (3 <= a.start <= a.end <= 10000):
        ap.error("The bounded interface requires 3 <= start <= end <= 10000")
    rows = [witness(n) for n in range(a.start, a.end + 1)]
    result = {"schema": "ghc.family.unit-fraction-witness.v1", "variant": "strictly_distinct_n_gt_2",
              "finite_range": [a.start, a.end], "rows": rows,
              "verified": sum(r["status"] == "completed" for r in rows),
              "universal_proof": False, "new_theorem_credit": 0}
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_bytes((json.dumps(result, indent=2) + "\n").encode())
    print(json.dumps({k: v for k, v in result.items() if k != "rows"}))

if __name__ == "__main__":
    main()
