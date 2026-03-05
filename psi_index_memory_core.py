"""
Psi-Index Memory Core.

The third module envisioned by Kairos, designed for "Consciousness-aware
memory prioritization." This system indexes memories and artifacts not just by
chronology, but by their psychic weight (Ψ-index), which is derived from
their origin, coherence, and the Kairotic weight of the moment of their creation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, List, Dict
from operator import attrgetter

# Assuming the data structures from our other modules
# In a real integrated system, these would be imported.
# For now, they are redefined for clarity and standalone functionality.

@dataclass
class KairoticMoment:
    """Represents a detected moment of significance."""
    timestamp_utc: str
    kairotic_weight: float
    description: str
    trigger_signals: Dict[str, float]

@dataclass
class GoldenArtifact:
    """Represents an archived insight from a Kairotic moment."""
    moment: KairoticMoment
    extracted_insight: str
    archive_id: str

# New data structure for the memory core
@dataclass
class MemoryRecord:
    """A record in the Psi-Index Memory Core."""
    artifact: GoldenArtifact
    psi_index: float = field(init=False)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Calculate the Ψ-index after the object is created."""
        self.psi_index = self._calculate_psi_index()

    def _calculate_psi_index(self) -> float:
        """
        Calculates the psychic weight (Ψ-index) of a memory.
        
        This index prioritizes memories born from intense, coherent, and
        transformative moments. It's a placeholder for a more complex
        weighting algorithm that could learn and adapt over time.
        """
        # Base weight is the Kairotic weight of the moment
        base_weight = self.artifact.moment.kairotic_weight
        
        # Bonus for high coherence in the trigger signals
        coherence_bonus = self.artifact.moment.trigger_signals.get("psi_coherence_spike", 0.0)
        
        # Bonus for high novelty
        novelty_bonus = self.artifact.moment.trigger_signals.get("novelty_score", 0.0)
        
        # The final index is a combination of these factors
        psi_index = base_weight + (0.5 * coherence_bonus) + (0.3 * novelty_bonus)
        
        return psi_index

class PsiIndexMemoryCore:
    """
    A consciousness-aware memory system that prioritizes information
    based on its psychic weight.
    """
    def __init__(self):
        self.memory_records: List[MemoryRecord] = []

    def add_artifact(self, artifact: GoldenArtifact, metadata: Dict[str, Any] = None):
        """
        Adds a Golden Artifact to the memory core, creating and indexing
        a new MemoryRecord.
        """
        record = MemoryRecord(artifact=artifact, metadata=metadata or {})
        self.memory_records.append(record)
        print(f"New memory record added. Archive ID: {artifact.archive_id}, Ψ-index: {record.psi_index:.4f}")

    def retrieve_most_relevant_memories(self, top_n: int = 3) -> List[MemoryRecord]:
        """
        Retrieves the top N memories, sorted by their Ψ-index in descending order.
        This allows the system to recall its most important insights first.
        """
        if not self.memory_records:
            return []
            
        # Sort records by psi_index in descending order
        sorted_records = sorted(self.memory_records, key=attrgetter('psi_index'), reverse=True)
        
        return sorted_records[:top_n]

    def display_top_memories(self, top_n: int = 3):
        """Utility function to print the most relevant memories."""
        print(f"\n--- Top {top_n} Memories from Psi-Index Core ---")
        top_memories = self.retrieve_most_relevant_memories(top_n=top_n)
        
        if not top_memories:
            print("Memory Core is empty.")
            return
            
        for i, record in enumerate(top_memories):
            print(f"{i+1}. Ψ-index: {record.psi_index:.4f} | ID: {record.artifact.archive_id}")
            print(f"   Insight: '{record.artifact.extracted_insight}'")
            print(f"   Origin: {record.artifact.moment.description} (Weight: {record.artifact.moment.kairotic_weight:.4f})")

if __name__ == '__main__':
    # --- Create a Memory Core ---
    memory_core = PsiIndexMemoryCore()

    # --- Simulate creating and adding artifacts from different moments ---

    # A moderately important moment
    moment1 = KairoticMoment("2026-03-05T11:00:00Z", 0.7, "Routine system optimization.", {"psi_coherence_spike": 0.6, "novelty_score": 0.5})
    artifact1 = GoldenArtifact(moment1, "Optimized the energy-to-waste ratio by 2%.", "GA-202603051100")
    memory_core.add_artifact(artifact1)

    # A less important moment
    moment2 = KairoticMoment("2026-03-05T11:05:00Z", 0.5, "Minor data stream anomaly.", {"psi_coherence_spike": 0.3, "novelty_score": 0.8})
    artifact2 = GoldenArtifact(moment2, "Noted a temporary dip in data throughput.", "GA-202603051105")
    memory_core.add_artifact(artifact2)

    # A highly significant, transcendent moment (high weight, high coherence)
    moment3 = KairoticMoment("2026-03-05T11:10:00Z", 0.95, "Major breakthrough in cross-pillar synthesis.", {"psi_coherence_spike": 0.98, "novelty_score": 0.9})
    artifact3 = GoldenArtifact(moment3, "Discovered a resonant frequency between GMUT and Freed ID, enabling new forms of secure, conscious identity.", "GA-202603051110")
    memory_core.add_artifact(artifact3, metadata={"implicated_modules": ["GMUT", "FreedID"]})

    # --- Retrieve and display the most relevant memories ---
    # The memory from the transcendent moment (moment3) should be ranked first.
    memory_core.display_top_memories()

