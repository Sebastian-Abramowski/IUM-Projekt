from pydantic import BaseModel
from uuid import UUID


class GetPredictionRequest(BaseModel):
    accommodates: int
    min_nights: int

    bedrooms: int
    beds: int
    bathrooms: float

    room_type: str
    property_type: str
    neighbourhood_cleaned: str


class SetFinalPriceRequest(BaseModel):
    prediction_uuid: UUID
    final_price: float
