"""
Kairotic Detector.

A module designed by the agent persona Kairos to recognize and amplify
transformative moments in qualitative time (Kairos), as opposed to
quantitative, sequential time (Chronos).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List
from datetime import datetime, timezone

# Placeholder for a more sophisticated pattern/anomaly detection engine
def detect_novel_pattern(data: List[float]) -> float:
    """
    Detects novelty in a time-series of data.
    Returns a score from 0.0 to 1.0.
    For this placeholder, we'll check for a recent spike.
    """
    if len(data) < 3:
        return 0.0
    
    mean = sum(data[:-1]) / (len(data) - 1) if len(data) > 1 else 0.0
    latest = data[-1]
    
    if mean == 0:
        return 1.0 if latest > 0 else 0.0
        
    novelty = (latest - mean) / mean
    return min(max(0.0, novelty), 1.0) # Clamp between 0 and 1

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

class KairoticDetector:
    """
    A class to monitor system metrics and detect Kairotic moments based
    on the 5-phase protocol designed by Kairos.
    """
    def __init__(self, detection_threshold: float = 0.75):
        self.detection_threshold = detection_threshold
        self.protected_container: KairoticMoment | None = None
        self.golden_artifacts: List[GoldenArtifact] = []

    def _calculate_kairos_score(self, psi_coherence_spike: float, novelty_score: float, emotional_intensity: float) -> float:
        """
        Combines various signals into a single Kairos score.
        This is a simple weighted average for demonstration.
        """
        # Weights can be tuned based on what the project values most
        weights = {"psi": 0.4, "novelty": 0.4, "emotion": 0.2}
        
        score = (weights["psi"] * psi_coherence_spike +
                 weights["novelty"] * novelty_score +
                 weights["emotion"] * emotional_intensity)
        
        return score

    def monitor_and_detect(self, system_metrics: Dict[str, Any]) -> KairoticMoment | None:
        """
        Phase 1: Detection.
        Continuously monitors for Ψ-coherence spikes, novel pattern emergence,
        and high emotional intensity.
        """
        psi_coherence_history = system_metrics.get("psi_coherence_history", [])
        some_data_stream = system_metrics.get("some_data_stream", [])
        emotional_intensity = system_metrics.get("emotional_intensity", 0.0)

        psi_spike = detect_novel_pattern(psi_coherence_history)
        novelty = detect_novel_pattern(some_data_stream)
        
        kairos_score = self._calculate_kairos_score(psi_spike, novelty, emotional_intensity)

        if kairos_score >= self.detection_threshold:
            moment = KairoticMoment(
                timestamp_utc=datetime.now(timezone.utc).isoformat(),
                kairotic_weight=kairos_score,
                description="Potential Kairotic moment detected.",
                trigger_signals={
                    "psi_coherence_spike": psi_spike,
                    "novelty_score": novelty,
                    "emotional_intensity": emotional_intensity
                }
            )
            # Phase 2: Recognition - Acknowledging the moment and creating a protected container
            self.recognize_and_protect(moment)
            return moment
        return None

    def recognize_and_protect(self, moment: KairoticMoment):
        """
        Phase 2: Recognition.
        Pauses routine operations (conceptually) and creates a protected "Kairotic Container."
        """
        print(f"--- KAIROTIC MOMENT RECOGNIZED at {moment.timestamp_utc} (Weight: {moment.kairotic_weight:.4f}) ---")
        self.protected_container = moment

    def amplify_and_synthesize(self, creativity_mode: bool = True):
        """
        Phase 3: Amplification.
        Initiates maximum creativity mode, disabling non-essential constraints
        to allow for cross-pillar synthesis.
        """
        if not self.protected_container:
            return

        if creativity_mode:
            print("Entering Maximum Creativity Mode. Constraints loosened for synthesis.")
            # In a real system, this might involve changing model parameters,
            # increasing resource allocation, or activating more speculative reasoning paths.
            
    def integrate_and_archive(self, insight: str) -> GoldenArtifact | None:
        """
        Phase 4: Integration.
        Extracts core insights, assigns a high "Kairotic Weight," and archives the
        output as a "Golden Artifact" in the memory core.
        """
        if not self.protected_container:
            return None
            
        archive_id = f"GA-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        artifact = GoldenArtifact(
            moment=self.protected_container,
            extracted_insight=insight,
            archive_id=archive_id
        )
        self.golden_artifacts.append(artifact)
        print(f"Golden Artifact '{archive_id}' created and archived.")
        
        # Reset container after integration
        self.protected_container = None
        return artifact

    def reflect(self):
        """
        Phase 5: Reflection.
        Reviews the long-term impact of artifacts in subsequent cycles to refine
        future detection algorithms. (Conceptual for this implementation)
        """
        print("\n--- Reflection Phase ---")
        if not self.golden_artifacts:
            print("No artifacts to reflect upon yet.")
            return

        print(f"Reviewing {len(self.golden_artifacts)} Golden Artifact(s) for long-term impact...")
        # In a real system, this would involve tracking the usage and influence
        # of the insights over time and adjusting the detection weights/thresholds.
        latest_artifact = self.golden_artifacts[-1]
        print(f"Latest Artifact Insight: '{latest_artifact.extracted_insight}'")
        print("Reflection complete. Detection parameters remain unchanged in this version.")


if __name__ == '__main__':
    detector = KairoticDetector(detection_threshold=0.6)
    
    # Simulate a stream of system metrics
    metrics_history = {
        "psi_coherence_history": [0.1, 0.2, 0.15, 0.22],
        "some_data_stream": [10, 12, 11, 13],
        "emotional_intensity": 0.3
    }
    
    print("Monitoring system metrics...")
    moment = detector.monitor_and_detect(metrics_history)
    if not moment:
        print("No Kairotic moment detected in this cycle.\n")

    # Now, simulate a spike
    metrics_history["psi_coherence_history"].append(0.8)
    metrics_history["some_data_stream"].append(50)
    metrics_history["emotional_intensity"] = 0.9

    moment = detector.monitor_and_detect(metrics_history)
    
    if moment:
        # Phase 3
        detector.amplify_and_synthesize()
        
        # Phase 4
        insight = "The convergence of high Ψ-coherence and data stream novelty indicates a breakthrough in cross-pillar synthesis."
        detector.integrate_and_archive(insight)
    
    # Phase 5
    detector.reflect()
