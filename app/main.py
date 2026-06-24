import time
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.config import settings
from app.database import get_db, create_tables
from app.db_models import Scan
from app.schemas import ScanResponse, ScanHistoryResponse, HealthResponse, LatencyBreakdown
from app.preprocessing import preprocess_image, compute_hash
from app.inference import ONNXEngine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global inference engine
engine = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine
    # Startup: Load model and create DB tables
    logger.info("Initializing ONNX engine...")
    try:
        engine = ONNXEngine(settings.MODEL_PATH, settings.CLASS_NAMES)
        
        # Warmup
        import numpy as np
        dummy_input = np.random.randn(1, 3, *settings.INPUT_SIZE).astype(np.float32)
        engine.predict(dummy_input)
        logger.info("Model warmup complete.")
    except Exception as e:
        logger.error(f"Failed to initialize engine: {e}")
        # Note: We don't raise here to allow the container to start, 
        # but scans will fail.

    logger.info("Ensuring database tables exist...")
    await create_tables()
    
    yield
    # Shutdown
    logger.info("Shutting down...")

app = FastAPI(title="HarvestEye-Edge API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/v1/scan", response_model=ScanResponse)
async def scan_image(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    total_t0 = time.perf_counter()
    image_bytes = await file.read()
    
    if len(image_bytes) > settings.MAX_IMAGE_SIZE:
        raise HTTPException(status_code=413, detail="Image size exceeds 10MB limit.")

    image_hash = compute_hash(image_bytes)

    # Preprocessing
    t_pre0 = time.perf_counter()
    try:
        preprocessed = preprocess_image(image_bytes, target_size=settings.INPUT_SIZE)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process image: {str(e)}")
    preprocessing_ms = (time.perf_counter() - t_pre0) * 1000.0

    # Inference (run in thread pool to not block async loop)
    if engine is None:
        raise HTTPException(status_code=503, detail="Model engine not initialized.")
    
    try:
        pred_class, conf, probs, inf_ms, post_ms = await asyncio.to_thread(
            engine.predict, preprocessed
        )
    except Exception as e:
        logger.error(f"Inference failed: {e}")
        raise HTTPException(status_code=500, detail="Inference failed.")

    total_ms = (time.perf_counter() - total_t0) * 1000.0

    # Log to Database (async)
    new_scan = Scan(
        defect_class=pred_class,
        confidence=conf,
        image_hash=image_hash,
        latency_ms=total_ms,
        preprocessing_ms=preprocessing_ms,
        inference_ms=inf_ms,
        postprocessing_ms=post_ms
    )
    db.add(new_scan)
    await db.commit()
    await db.refresh(new_scan)

    return ScanResponse(
        scan_id=new_scan.id,
        defect_class=pred_class,
        confidence=conf,
        probabilities=probs,
        latency=LatencyBreakdown(
            preprocessing_ms=preprocessing_ms,
            inference_ms=inf_ms,
            postprocessing_ms=post_ms,
            total_ms=total_ms
        )
    )

@app.get("/api/v1/history", response_model=ScanHistoryResponse)
async def get_history(limit: int = 50, offset: int = 0, db: AsyncSession = Depends(get_db)):
    # Get total count
    count_query = select(func.count()).select_from(Scan)
    total = await db.scalar(count_query)
    
    # Get items
    query = select(Scan).order_by(Scan.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset
    }

@app.get("/api/v1/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    # Total scans
    count_query = select(func.count()).select_from(Scan)
    total_scans = await db.scalar(count_query) or 0
    
    # Average latency
    latency_query = select(func.avg(Scan.latency_ms)).select_from(Scan)
    avg_latency = await db.scalar(latency_query) or 0.0
    
    # Disease distribution
    dist_query = select(Scan.defect_class, func.count(Scan.id)).group_by(Scan.defect_class)
    dist_result = await db.execute(dist_query)
    distribution = {row[0]: row[1] for row in dist_result.all()}
    
    return {
        "total_scans": total_scans,
        "avg_latency_ms": round(avg_latency, 2),
        "disease_distribution": distribution
    }
