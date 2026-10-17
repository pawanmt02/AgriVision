import os
import sqlite3
import math
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
import requests

from models import (
    UserCreate,
    UserResponse,
    DiseaseScanRecord,
    DiagnosticResponse,
    OutbreakCluster,
    SeverityEnum
)

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", os.getenv("SUPABASE_ANON_KEY", ""))

DB_FILE = os.path.join(os.path.dirname(__file__), "agrivision.db")

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points in kilometers."""
    R = 6371.0 # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

def init_db():
    """Initializes local SQLite database and pre-seeds realistic global outbreaks."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        phone_number TEXT UNIQUE NOT NULL,
        preferred_language TEXT DEFAULT 'en',
        created_at TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS disease_scans (
        id TEXT PRIMARY KEY,
        user_id TEXT,
        crop_name TEXT NOT NULL,
        disease_detected TEXT NOT NULL,
        confidence_score REAL NOT NULL,
        severity TEXT NOT NULL,
        organic_remedy TEXT,
        chemical_remedy TEXT,
        latitude REAL,
        longitude REAL,
        image_url TEXT,
        scanned_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # Check if empty, then seed initial outbreak data
    cursor.execute("SELECT COUNT(*) FROM disease_scans")
    count = cursor.fetchone()[0]

    if count == 0:
        # Pre-seed demo users
        default_users = [
            ("00000000-0000-0000-0000-000000000001", "Farmer Rajesh Kumar", "+919876543210", "hi", datetime.utcnow().isoformat()),
            ("00000000-0000-0000-0000-000000000002", "Dr. Sarah Jenkins", "+14155550199", "en", datetime.utcnow().isoformat())
        ]
        cursor.executemany("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)", default_users)

        sample_scans = [
            # Tomato Late Blight cluster (Indo-Gangetic Plain, Delhi/Haryana)
            (str(uuid.uuid4()), "00000000-0000-0000-0000-000000000001", "Tomato", "Late Blight (Phytophthora infestans)", 0.96, "Severe",
             "Apply Copper octanoate or Trichoderma harzianum; prune dense canopy.",
             "Apply Cymoxanil 8% + Mancozeb 64% WP at 2.5g/L water; PHI 7 days.",
             28.6139, 77.2090, None, datetime.utcnow().isoformat()),
            
            (str(uuid.uuid4()), "00000000-0000-0000-0000-000000000001", "Tomato", "Late Blight (Phytophthora infestans)", 0.94, "Severe",
             "Spray 5% Neem oil emulsion every 5 days; avoid overhead drip.",
             "Apply Metalaxyl-M + Mancozeb at 2.5 kg/ha.",
             28.6300, 77.2300, None, datetime.utcnow().isoformat()),

            # Rice Bacterial Leaf Blight (Punjab / Chandigarh)
            (str(uuid.uuid4()), "00000000-0000-0000-0000-000000000001", "Rice (Paddy)", "Bacterial Leaf Blight (Xanthomonas oryzae)", 0.92, "Severe",
             "Fresh cow dung extract spray (20%) or Pseudomonas fluorescens @ 10g/L.",
             "Streptomycin sulphate + Tetracycline hydrochloride (90:10) at 6g + Copper Oxychloride 50 WP 25g in 10L water.",
             30.7333, 76.8512, None, datetime.utcnow().isoformat()),

            # Potato Early Blight (California Central Valley)
            (str(uuid.uuid4()), "00000000-0000-0000-0000-000000000002", "Potato", "Early Blight (Alternaria solani)", 0.89, "Moderate",
             "Bacillus subtilis bio-fungicide soil drench and aerated compost tea.",
             "Azoxystrobin 23% SC at 1ml/L or Chlorothalonil 75% WP at 2g/L.",
             36.7468, -119.7871, None, datetime.utcnow().isoformat()),

            # Corn Fall Armyworm (Midwest US / Iowa)
            (str(uuid.uuid4()), "00000000-0000-0000-0000-000000000002", "Maize (Corn)", "Fall Armyworm Infestation (Spodoptera frugiperda)", 0.95, "Severe",
             "Bacillus thuringiensis (Bt) kurstaki foliar whorl drop; release Trichogramma wasps.",
             "Emamectin benzoate 5% SG at 0.4g/L or Spinetoram 11.7% SC at 0.5ml/L.",
             41.5868, -93.6091, None, datetime.utcnow().isoformat()),

            # Wheat Stripe Rust (Rift Valley, Nakuru, Kenya)
            (str(uuid.uuid4()), None, "Wheat", "Stripe / Yellow Rust (Puccinia striiformis)", 0.91, "Severe",
             "Resistant cultivar rotation; sulfur dust broadcast during early morning humidity.",
             "Tebuconazole 250 EC at 1L/ha or Propiconazole 25% EC at 500ml/ha.",
             -0.3000, 36.0667, None, datetime.utcnow().isoformat()),

            # Coffee Leaf Rust (Antioquia, Colombia)
            (str(uuid.uuid4()), None, "Coffee", "Coffee Leaf Rust (Hemileia vastatrix)", 0.93, "Severe",
             "Bordeaux mixture 1% foliar wash before onset of heavy rains; prune shade trees.",
             "Hexaconazole 5% EC at 2ml/L water.",
             6.2442, -75.5812, None, datetime.utcnow().isoformat()),

            # Apple Scab (South Tyrol / Bolzano, Italy)
            (str(uuid.uuid4()), None, "Apple", "Apple Scab (Venturia inaequalis)", 0.90, "Moderate",
             "Lime sulfur or Potassium bicarbonate foliar protectant at pink bud.",
             "Difenoconazole 25% EC at 0.3ml/L water.",
             46.4983, 11.3548, None, datetime.utcnow().isoformat()),

            # Healthy Citrus (Florida, US)
            (str(uuid.uuid4()), "00000000-0000-0000-0000-000000000002", "Citrus (Orange)", "Healthy Plant Leaf - No Pathogen Detected", 0.98, "Low",
             "Maintain balanced potassium-nitrogen foliar nutrition and root aeration.",
             "Zero chemical pesticide required. Preventive copper spray optional during pre-monsoon flush.",
             28.5383, -81.5158, None, datetime.utcnow().isoformat())
        ]
        cursor.executemany("""
        INSERT INTO disease_scans 
        (id, user_id, crop_name, disease_detected, confidence_score, severity, organic_remedy, chemical_remedy, latitude, longitude, image_url, scanned_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_scans)

    conn.commit()
    conn.close()

def save_scan_result(
    diag: DiagnosticResponse,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    user_id: Optional[str] = None
) -> str:
    """Saves a new scan record to the database (and Supabase if configured)."""
    scan_id = str(uuid.uuid4())
    scanned_at_iso = datetime.utcnow().isoformat()

    # 1. Save to local SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO disease_scans 
    (id, user_id, crop_name, disease_detected, confidence_score, severity, organic_remedy, chemical_remedy, latitude, longitude, image_url, scanned_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        scan_id,
        user_id,
        diag.crop_name,
        diag.disease_detected,
        diag.confidence_score,
        diag.severity.value,
        diag.organic_remedy,
        diag.chemical_remedy,
        latitude,
        longitude,
        None,
        scanned_at_iso
    ))
    conn.commit()
    conn.close()

    # 2. Sync to Supabase if credentials are provided
    if SUPABASE_URL and SUPABASE_KEY:
        try:
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}",
                "Content-Type": "application/json",
                "Prefer": "return=minimal"
            }
            supabase_payload = {
                "id": scan_id,
                "user_id": user_id,
                "crop_name": diag.crop_name,
                "disease_detected": diag.disease_detected,
                "confidence_score": diag.confidence_score,
                "severity": diag.severity.value,
                "organic_remedy": diag.organic_remedy,
                "chemical_remedy": diag.chemical_remedy,
                "scanned_at": scanned_at_iso
            }
            if latitude is not None and longitude is not None:
                # PostGIS WKT Point: POINT(longitude latitude)
                supabase_payload["location"] = f"SRID=4326;POINT({longitude} {latitude})"

            requests.post(f"{SUPABASE_URL}/rest/v1/disease_scans", json=supabase_payload, headers=headers, timeout=4)
        except Exception as e:
            print(f"[AgriVision] Supabase sync notice: {e}")

    return scan_id

def get_all_scans(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves recent disease scans."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, user_id, crop_name, disease_detected, confidence_score, severity, organic_remedy, chemical_remedy, latitude, longitude, scanned_at
    FROM disease_scans
    ORDER BY scanned_at DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r[0],
            "user_id": r[1],
            "crop_name": r[2],
            "disease_detected": r[3],
            "confidence_score": r[4],
            "severity": r[5],
            "organic_remedy": r[6],
            "chemical_remedy": r[7],
            "latitude": r[8],
            "longitude": r[9],
            "scanned_at": r[10]
        })
    return results

def get_outbreak_clusters(
    center_lat: Optional[float] = None,
    center_lng: Optional[float] = None,
    radius_km: float = 20000.0 # Default global radius
) -> List[Dict[str, Any]]:
    """
    Returns spatial outbreak clusters, computing Haversine distance from user location.
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, crop_name, disease_detected, severity, confidence_score, latitude, longitude, scanned_at
    FROM disease_scans
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    ORDER BY scanned_at DESC
    """)
    rows = cursor.fetchall()
    conn.close()

    clusters = []
    for r in rows:
        lat, lng = r[5], r[6]
        dist = None
        if center_lat is not None and center_lng is not None:
            dist = haversine_distance(center_lat, center_lng, lat, lng)
            if dist > radius_km:
                continue

        clusters.append({
            "id": r[0],
            "crop_name": r[1],
            "disease_detected": r[2],
            "severity": r[3],
            "confidence_score": r[4],
            "latitude": lat,
            "longitude": lng,
            "distance_km": dist,
            "scanned_at": r[7]
        })

    if center_lat is not None and center_lng is not None:
        clusters.sort(key=lambda x: x["distance_km"] if x["distance_km"] is not None else 999999)

    return clusters

def get_analytics_summary() -> Dict[str, Any]:
    """Computes aggregated agronomic stats."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM disease_scans")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM disease_scans WHERE severity = 'Severe'")
    severe_count = cursor.fetchone()[0]

    cursor.execute("SELECT crop_name, COUNT(*) as cnt FROM disease_scans GROUP BY crop_name ORDER BY cnt DESC LIMIT 5")
    top_crops = [{"crop": row[0], "count": row[1]} for row in cursor.fetchall()]

    cursor.execute("SELECT disease_detected, COUNT(*) as cnt FROM disease_scans GROUP BY disease_detected ORDER BY cnt DESC LIMIT 5")
    top_diseases = [{"disease": row[0], "count": row[1]} for row in cursor.fetchall()]

    conn.close()

    return {
        "total_scans": total_scans,
        "severe_outbreaks": severe_count,
        "top_crops": top_crops,
        "top_diseases": top_diseases
    }

# Run init on module load
init_db()
