from pydantic import BaseModel, UUID4, Field
from typing import Dict, List
from datetime import datetime

class LatencyBreakdown(BaseModel):
    preprocessing_ms: float
    inference_ms: float
    postprocessing_ms: float
    total_ms: float

class ScanResponse(BaseModel):
    scan_id: UUID4
    defect_class: str
    confidence: float
    probabilities: Dict[str, float]
    latency: LatencyBreakdown
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ScanHistoryItem(BaseModel):
    id: UUID4
    created_at: datetime
    defect_class: str
    confidence: float
    latency_ms: float

    class Config:
        from_attributes = True

class ScanHistoryResponse(BaseModel):
    items: List[ScanHistoryItem]
    total: int
    limit: int
    offset: int

class HealthResponse(BaseModel):
    status: str
    version: str
