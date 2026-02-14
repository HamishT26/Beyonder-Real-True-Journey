"""
trinity_simulation_engine.py
--------------------------------

This module provides a simple simulation engine to test predictions of the Grand Mandala Unified Theory (GMUT)
using the Trinity Hybrid‑AI framework.  The goal of this engine is not to produce precise scientific
predictions but to offer an interactive sandbox where hypothetical effects of the ψ‑field on gravitational
wave spectra and other observables can be explored.  It complements the GMUT Lagrangian and QCIT
integration by giving users a way to generate data, visualise trends and evaluate how changes in
model parameters might manifest in measurable quantities.

Features
========

* Simulate gravitational‑wave spectra in both baseline General Relativity (GR) and with a simplified
  ψ‑field modification.  The baseline spectrum follows a power‑law inspired by the stochastic
  gravitational wave background; the ψ‑field introduces a frequency‑dependent boost factor.
* Compute additional metrics such as energy density ratios and predicted strain amplitudes.
* Plot spectra using matplotlib.  Each simulation produces two curves—baseline and modified—to aid
  visual comparison.
* Designed to be extended: additional observables or more sophisticated physics models can be added
  as needed.

Usage Example
-------------

```
from trinity_simulation_engine import GMUTSimulator

simulator = GMUTSimulator()
results = simulator.run_simulation(gamma=0.05)
simulator.plot_results(results)
```

This will compute the baseline and GMUT‑modified gravitational wave spectra across a range of
frequencies and display a plot.

Note
----
This tool is illustrative and educational; it does not replace full numerical relativity or
cosmology codes.  It provides a starting point for exploring how the ψ‑field might affect
gravitational wave observations and encourages further refinement and empirical validation.
"""

from dataclasses import dataclass
import numpy as np

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:  # pragma: no cover - environment dependent
    plt = None


@dataclass
class SimulationResults:
    frequencies: np.ndarray
    baseline_spectrum: np.ndarray
    modified_spectrum: np.ndarray
    gamma: float

    def energy_density_ratio(self) -> float:
        """Return the ratio of total energy densities between modified and baseline spectra."""
        # Integrate over frequency (simple trapezoidal approximation)
        baseline_int = np.trapz(self.baseline_spectrum, self.frequencies)
        modified_int = np.trapz(self.modified_spectrum, self.frequencies)
        return modified_int / baseline_int if baseline_int != 0 else np.inf


class GMUTSimulator:
    """A simple simulator for GMUT gravitational‑wave predictions."""

    def __init__(self, freq_min: float = 1e-3, freq_max: float = 1e2, num_points: int = 50):
        """
        Initialise the simulator.

        Args:
            freq_min (float): Minimum frequency in Hz for the simulation range.
            freq_max (float): Maximum frequency in Hz.
            num_points (int): Number of frequency samples.
        """
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.num_points = num_points

    def baseline_spectrum(self, freqs: np.ndarray) -> np.ndarray:
        """
        Define a baseline stochastic gravitational‑wave background spectrum.

        The spectrum follows a simple power‑law inspired by cosmological gravitational wave models.

        Args:
            freqs (np.ndarray): Array of frequencies.

        Returns:
            np.ndarray: Baseline spectrum values at each frequency.
        """
        # Normalisation factor roughly representing a reference strain amplitude
        A0 = 1e-26
        # Spectral slope (scale‑invariant slope of -2)
        return A0 * (freqs / 1.0)**(-2)

    def psi_modification_factor(self, freqs: np.ndarray, gamma: float) -> np.ndarray:
        """
        Compute a ψ‑field modification factor for the spectrum.

        We model the effect as a frequency‑dependent exponential boost that decays with frequency,
        controlled by the coupling parameter gamma.

        Args:
            freqs (np.ndarray): Array of frequencies.
            gamma (float): Coupling strength of the ψ‑field.

        Returns:
            np.ndarray: Modification factor applied multiplicatively to the baseline spectrum.
        """
        # Avoid division by zero by adding a small epsilon
        eps = 1e-12
        return 1.0 + gamma * np.exp(-freqs / (1.0 + eps))

    def run_simulation(self, gamma: float = 0.01) -> SimulationResults:
        """
        Simulate gravitational‑wave spectra with and without ψ‑field modifications.

        Args:
            gamma (float): ψ‑field coupling strength parameter.

        Returns:
            SimulationResults: Object containing simulation data and helper functions.
        """
        freqs = np.logspace(np.log10(self.freq_min), np.log10(self.freq_max), self.num_points)
        base = self.baseline_spectrum(freqs)
        mod_factor = self.psi_modification_factor(freqs, gamma)
        modified = base * mod_factor
        return SimulationResults(frequencies=freqs,
                                baseline_spectrum=base,
                                modified_spectrum=modified,
                                gamma=gamma)

    def plot_results(self, results: SimulationResults, show: bool = True, save_path: str = None) -> None:
        """
        Plot baseline and modified spectra using matplotlib.

        Args:
            results (SimulationResults): Data to plot.
            show (bool): Whether to display the plot interactively.
            save_path (str): Optional path to save the plot as an image file.
        """
        try:
            import matplotlib.pyplot as plt
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "matplotlib is required for plotting. Install it or run without --plot."
            ) from exc
        if plt is None:
            raise RuntimeError("matplotlib is not installed; rerun without --plot or install matplotlib.")

        plt.figure(figsize=(8, 5))
        plt.loglog(results.frequencies, results.baseline_spectrum, label='Baseline GR spectrum')
        plt.loglog(results.frequencies, results.modified_spectrum, label=f'GMUT modified (γ={results.gamma})')
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('Strain amplitude')
        plt.title('Simulated Gravitational‑Wave Spectrum')
        plt.legend()
        plt.grid(True, which='both', ls='--', alpha=0.6)
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        if show:
            plt.show()
        plt.close()