from typing import Literal
from uuid import UUID

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction_uuid: UUID
    predicted_price: float


class SimplePredictionResponse(BaseModel):
    predicted_price: float


class ModelSummary(BaseModel):
    model_type: Literal["LINEAR_REGRESSION", "RANDOM_FOREST"]
    selection_ratio: float
    usage_count: int
    avg_percent_change: float


class AbSummaryResponse(BaseModel):
    total_predictions: int
    total_decisions: int
    summary: list[ModelSummary]
