import json
from fastapi.testclient import TestClient
from main import app
from sample_data import SAMPLE_GALLERY

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("[PASS] Health check passed")

def test_sample_images():
    response = client.get("/api/sample-images")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 7
    print(f"[PASS] Sample images endpoint returned {len(data)} items")

def test_crop_diagnosis():
    # Crop leaf test
    sample = SAMPLE_GALLERY[0]
    payload = {
        "image_base64": sample["image_data"],
        "crop_hint": "Tomato",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "preferred_language": "en"
    }
    response = client.post("/api/diagnose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["crop_name"] == "Tomato"
    assert "Late Blight" in data["disease_detected"]
    assert data["is_animal_disease"] == False
    assert data["confidence_score"] > 0.7
    print(f"[PASS] Crop diagnosis verified: {data['crop_name']} - {data['disease_detected']}")

def test_animal_disease_diagnosis():
    # Find the Bovine Lumpy Skin animal disease sample
    animal_sample = next(s for s in SAMPLE_GALLERY if "Lumpy Skin" in s["title"])
    payload = {
        "image_base64": animal_sample["image_data"],
        "crop_hint": "Cattle / Cow",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "preferred_language": "en"
    }
    response = client.post("/api/diagnose", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["is_animal_disease"] == True
    assert "Tomato" not in data["crop_name"]
    assert "Bovine" in data["crop_name"] or "Cattle" in data["crop_name"]
    assert "Lumpy Skin" in data["disease_detected"]
    assert data["animal_warning"] is not None
    assert "VETERINARY" in data["animal_warning"]
    print(f"[PASS] Animal disease diagnosis verified: {data['crop_name']} - {data['disease_detected']} (Veterinary warning flagged)")

def test_outbreaks_and_analytics():
    response = client.get("/api/outbreaks?lat=28.6139&lng=77.2090&radius_km=5000")
    assert response.status_code == 200
    clusters = response.json()
    assert len(clusters) > 0
    print(f"[PASS] Outbreak GIS endpoint returned {len(clusters)} clusters")

    response = client.get("/api/analytics")
    assert response.status_code == 200
    stats = response.json()
    assert "total_scans" in stats
    assert "severe_outbreaks" in stats
    print(f"[PASS] Analytics endpoint passed: {stats['total_scans']} total scans, {stats['severe_outbreaks']} severe")

if __name__ == "__main__":
    test_health()
    test_sample_images()
    test_crop_diagnosis()
    test_animal_disease_diagnosis()
    test_outbreaks_and_analytics()
    print("\nAll Crop & Animal Disease tests PASSED successfully!")
