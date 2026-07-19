"""
YouTube Metric Normalization & Mapping (`FR-PX-1002`).

Maps platform-native metrics (`averageViewDurationPercentage`, `clickThroughRate`, `subscribersGained`, `likesAndComments`)
to canonical Core metrics (`attention_rate`, `selection_rate`, `audience_growth`, `engagement`).
Ensures the Execution Layer normalizes data before crossing the Core Gateway (`PX-002`).
"""
from typing import Dict, Any, List, Union
from evolutionos.core.domain.ontology import Observation, ObservationQuality, ObservationStatus


# Canonical mapping table (`FR-PX-1002`)
YOUTUBE_TO_CANONICAL_MAP: Dict[str, str] = {
    "averageViewDurationPercentage": "attention_rate",
    "clickThroughRate": "selection_rate",
    "subscribersGained": "audience_growth",
    "likesAndComments": "engagement",
    "views": "views_count"
}


def normalize_youtube_metrics(
    experiment_id: str,
    raw_metrics: Dict[str, Union[float, int]],
    collection_window: str = "24h"
) -> List[Observation]:
    """Normalize raw YouTube analytics data into canonical Level 1 Observation models (`FR-PX-1002`)."""
    observations = []

    for native_key, native_val in raw_metrics.items():
        canonical_metric = YOUTUBE_TO_CANONICAL_MAP.get(native_key)
        if not canonical_metric:
            continue

        # Normalize percentages to 0.0 - 1.0 range if needed
        norm_value = float(native_val)
        unit = ""
        if canonical_metric in ["attention_rate", "selection_rate"] and norm_value > 1.0:
            norm_value = round(norm_value / 100.0, 4)
            unit = "ratio"

        obs = Observation(
            experiment_id=experiment_id,
            platform="youtube",
            metric=canonical_metric,
            value=norm_value,
            unit=unit,
            collection_window=collection_window,
            collection_method="AUTOMATED_API",
            quality=ObservationQuality(confidence_modifier=1.0, data_source_tier="PRIMARY"),
            status=ObservationStatus.RECEIVED
        )
        observations.append(obs)

    return observations
