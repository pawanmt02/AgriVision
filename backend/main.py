import os
import uvicorn
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any

from models import (
    ScanRequestPayload,
    DiagnosticResponse,
    UserCreate,
    UserResponse,
    NearbyOutbreakQuery,
    OutbreakCluster
)
from ai_engine import diagnose_leaf_image
from database import (
    save_scan_result,
    get_all_scans,
    get_outbreak_clusters,
    get_analytics_summary
)
from sample_data import SAMPLE_GALLERY

app = FastAPI(
    title="AgriVision AI Core",
    description="Universal Crop Disease Diagnostic & Agronomy Engine API",
    version="1.0.0"
)

# Enable CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AgriVision AI Core",
        "version": "1.0.0"
    }

@app.post("/api/diagnose", response_model=DiagnosticResponse)
def diagnose_crop(payload: ScanRequestPayload):
    """
    Main diagnostic endpoint: accepts leaf image base64, GPS coordinates, and optional crop hint.
    Runs multi-modal vision inference, synthesizes organic & chemical treatment plans,
    logs the event to the geospatial database, and returns comprehensive diagnostic data.
    """
    if not payload.image_base64:
        raise HTTPException(status_code=400, detail="Image data in Base64 format is required.")

    # 1. Run multi-modal vision diagnosis
    diagnostic_result = diagnose_leaf_image(
        image_base64=payload.image_base64,
        crop_hint=payload.crop_hint,
        preferred_language=payload.preferred_language
    )

    # 2. Persist to spatial database
    scan_id = save_scan_result(
        diag=diagnostic_result,
        latitude=payload.latitude,
        longitude=payload.longitude,
        user_id=payload.user_id
    )
    diagnostic_result.scan_id = scan_id

    return diagnostic_result

@app.get("/api/scans")
def list_scans(limit: int = Query(default=30, ge=1, le=100)):
    """Fetch recent disease scan history."""
    return get_all_scans(limit=limit)

@app.get("/api/outbreaks")
def list_outbreak_clusters(
    lat: Optional[float] = Query(default=None),
    lng: Optional[float] = Query(default=None),
    radius_km: float = Query(default=25000.0)
):
    """
    Fetch geospatial disease outbreak clusters.
    If lat & lng are passed, computes distances from user position.
    """
    return get_outbreak_clusters(center_lat=lat, center_lng=lng, radius_km=radius_km)

@app.get("/api/analytics")
def get_analytics():
    """Retrieve outbreak analytics, severity distribution, and top affected crops."""
    return get_analytics_summary()

@app.get("/api/sample-images")
def get_sample_images():
    """Returns pre-loaded sample diseased and healthy leaf images for instant UI demonstration."""
    return SAMPLE_GALLERY

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8005))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
