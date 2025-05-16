import uuid

from enum import StrEnum

from sqlalchemy import Column, DateTime, Enum as PgEnum, Float, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.database import Base


class ModelName(StrEnum):
    LINEAR_REGRESSION = "LINEAR_REGRESSION"
    DUMMY = "DUMMY"
    RANDOM_FOREST = "RANDOM_FOREST"


class Prediction(Base):
    __tablename__ = "prediction"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_type = Column(PgEnum(ModelName, "model_type_enum"), nullable=False)
    prediction = Column(Float, nullable=False)
    input_data = Column(JSONB, nullable=True)
    timestamp = Column(DateTime(), nullable=False, server_default=func.now())
