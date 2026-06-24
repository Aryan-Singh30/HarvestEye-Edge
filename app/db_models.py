from sqlalchemy import Column, String, Float, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Prediction Results
    defect_class = Column(String, index=True)
    confidence = Column(Float)
    
    # Image Tracking (for deduplication/auditing)
    image_hash = Column(String, index=True)
    
    # Telemetry
    latency_ms = Column(Float)
    preprocessing_ms = Column(Float)
    inference_ms = Column(Float)
    postprocessing_ms = Column(Float)
