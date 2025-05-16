from uuid import UUID

from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction_uuid: UUID
    predicted_price: float
