"""
trinity_orchestrator_full.py
----------------------------

This module defines a more comprehensive orchestrator for the Trinity Hybrid‑AI prototype.
It combines the Quantum‑to‑Classical Information Transmuter (QCIT) with a Freed ID registry
for decentralised identity management.  Agents are registered with the Freed ID Registry
via DID Documents; tasks are executed only if the requesting DID is active and not revoked.

The orchestrator coordinates neuromorphic, quantum and classical modules, handles energy
management (including transmutation of waste energy into exotic energy) and applies QCIT
to translate quantum state outputs into classical feature vectors.

This script can be run directly to perform a demonstration; it will register a sample
agent, issue a credential, and execute a few tasks while printing the results.
"""

import random
from typing import Dict

from qc_transmuter import transmute_state
from freed_id_registry import FreedIDRegistry, DIDDocument


class EnergyModule:
    """Simple energy management module for absorption, regeneration and transmutation."""

    def __init__(self, waste_energy=10.0):
        self.waste_energy = waste_energy
        self.exotic_energy = 0.0

    def absorb(self, delta: float):
        self.waste_energy += delta

    def regenerate(self) -> float:
        generated = max(0.0, self.waste_energy * 0.1)
        self.waste_energy -= generated
        return generated

    def transmute_energy(self, gain=0.6, loss=0.2, threshold=5.0) -> float:
        if self.waste_energy <= threshold:
            return 0.0
        excess = self.waste_energy - threshold
        produced = max(0.0, excess * (gain - loss))
        self.waste_energy -= produced
        self.exotic_energy += produced
        return produced


class NeuromorphicModule:
    def run(self, data: str) -> str:
        return f"neuromorphic_output({data})"


class QuantumModule:
    def run(self, data: str) -> Dict[str, complex]:
        # Return a dummy quantum state represented by random amplitudes
        num_qubits = max(1, len(data) % 4 + 1)
        num_states = 2 ** num_qubits
        return {f"state_{i}": (random.random() + 1j * random.random()) for i in range(num_states)}


class ClassicalModule:
    def run(self, data: str) -> str:
        return f"classical_output({data})"


class TrinityOrchestratorFull:
    """
    Orchestrator integrating QCIT and Freed ID registry.

    Agents must present a valid DID; if the DID is active in the registry, the task is
    processed through neuromorphic, quantum and classical modules.  Energy management
    is updated at each call.
    """

    def __init__(self):
        self.registry = FreedIDRegistry()
        self.energy = EnergyModule()
        self.neuro = NeuromorphicModule()
        self.quantum = QuantumModule()
        self.classical = ClassicalModule()

    def register_agent(self, doc: DIDDocument) -> str:
        """Register an agent's DID Document and return its DID."""
        did = self.registry.register(doc)
        return did

    def issue_agent_credential(self, did: str, credential: Dict[str, object]) -> None:
        """Issue a credential to a registered DID."""
        self.registry.issue_credential(did, credential)

    def _is_authorised(self, did: str) -> bool:
        doc = self.registry.resolve(did)
        return doc is not None and not doc.revoked

    def run_task(self, did: str, task_data: str) -> Dict[str, object]:
        if not self._is_authorised(did):
            raise PermissionError(f"DID {did} is not authorised or is revoked")

        neu_output = self.neuro.run(task_data)
        q_state = self.quantum.run(neu_output)
        amplitudes = list(q_state.values())
        qc_features = transmute_state(amplitudes, shots=512)
        classical_input = f"quantum_features:{qc_features}"
        result = self.classical.run(classical_input)

        # update energy management
        self.energy.absorb(random.uniform(0.0, 3.0))
        self.energy.regenerate()
        exotic = self.energy.transmute_energy()

        return {
            "result": result,
            "quantum_features": qc_features,
            "waste_energy": self.energy.waste_energy,
            "exotic_energy_generated": exotic,
            "total_exotic_energy": self.energy.exotic_energy
        }


if __name__ == '__main__':
    # Demonstration of usage
    orchestrator = TrinityOrchestratorFull()
    # Create a DID Document and register it
    doc = DIDDocument(
        did='',
        controller='did:freed:controller',
        verification_methods=[{'id': 'key1', 'type': 'Ed25519VerificationKey2018', 'publicKeyBase58': 'GfH2...'}],
        services=[{'id': 'service0', 'type': 'FreedIDCredentialRegistry', 'serviceEndpoint': 'https://example.com/services/registry'}]
    )
    did = orchestrator.register_agent(doc)
    print('Registered DID:', did)
    # Issue a credential
    orchestrator.issue_agent_credential(did, {'claim': 'TrinityUser', 'issuer': 'did:freed:issuer'})
    # Run a few tasks
    for i in range(2):
        outcome = orchestrator.run_task(did, f"input_{i}")
        print(f"Task {i+1} result:", outcome)