import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base


class Decision(Base):
    __tablename__ = "decision"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prediction_uuid = Column(UUID(as_uuid=True), ForeignKey("prediction.uuid"), nullable=False)
    final_price = Column(Float, nullable=False)
    timestamp = Column(DateTime(), nullable=False, server_default=func.now())
