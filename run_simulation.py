"""
run_simulation.py
-----------------

This script demonstrates how to use the Trinity Simulation Engine to explore
predictions of the Grand Mandala Unified Theory (GMUT).  It runs simulations
for a range of ψ‑field coupling strengths (gamma) and prints the ratio of
modified to baseline energy densities for each.  Optionally, it can plot the
spectra for the final gamma value.

Usage:

```
python3 run_simulation.py --gammas 0.0 0.01 0.05 0.1 --plot
```

This will run four simulations and display a plot for the last one.
"""

import argparse
from trinity_simulation_engine import GMUTSimulator


def main():
    parser = argparse.ArgumentParser(description="Run GMUT simulation over multiple gamma values.")
    parser.add_argument('--gammas', type=float, nargs='+', default=[0.0, 0.01, 0.05, 0.1],
                        help='List of gamma values to simulate.')
    parser.add_argument('--plot', action='store_true', help='Plot the spectrum for the last gamma value.')
    args = parser.parse_args()

    simulator = GMUTSimulator()
    last_result = None
    for gamma in args.gammas:
        result = simulator.run_simulation(gamma=gamma)
        ratio = result.energy_density_ratio()
        print(f"Gamma={gamma:.4f}: energy density ratio = {ratio:.5f}")
        last_result = result
    if args.plot and last_result is not None:
        simulator.plot_results(last_result, show=True)


if __name__ == '__main__':
    main()