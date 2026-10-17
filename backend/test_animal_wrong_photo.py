import urllib.request
import json
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_animal_wrong_photo():
    print("Fetching sample gallery...")
    res = urllib.request.urlopen('http://127.0.0.1:8005/api/sample-images')
    samples = json.loads(res.read().decode('utf-8'))
    
    cattle_sample = next((s for s in samples if "Cattle" in s["crop"]), None)
    tomato_sample = next((s for s in samples if "Tomato" in s["crop"]), None)
    arecanut_sample = next((s for s in samples if "Arecanut" in s["crop"]), None)
    
    assert cattle_sample is not None, "Cattle sample image not found"
    assert tomato_sample is not None, "Tomato sample image not found"
    
    print("\n=======================================================")
    print("TEST 1: Upload Animal image in AUTO-DETECT mode (crop_hint=None)")
    print("Expected: is_wrong_photo = True, disease containing 'Wrong Photo', NOT Tomato!")
    print("=======================================================")
    
    payload1 = {
        "image_base64": cattle_sample["image_data"],
        "crop_hint": None,
        "latitude": 12.97,
        "longitude": 77.59,
        "preferred_language": "kn"
    }
    req1 = urllib.request.Request(
        'http://127.0.0.1:8005/api/diagnose',
        data=json.dumps(payload1).encode("utf-8"),
        headers={'Content-Type': 'application/json'}
    )
    resp1 = urllib.request.urlopen(req1)
    d1 = json.loads(resp1.read().decode('utf-8'))
    
    print(f"Crop Name: {d1.get('crop_name')}")
    print(f"Disease Detected: {d1.get('disease_detected')}")
    print(f"is_wrong_photo: {d1.get('is_wrong_photo')}")
    print(f"is_valid_agricultural_image: {d1.get('is_valid_agricultural_image')}")
    print(f"CNN Domain: {d1.get('cnn_metrics', {}).get('cnn_domain')}")
    print(f"Animal Probability: {d1.get('cnn_metrics', {}).get('animal_probability')}")
    print(f"Leaf Probability: {d1.get('cnn_metrics', {}).get('leaf_probability')}")
    print(f"Kannada Speech: {d1.get('localized_speech_summary', {}).get('kn')}")
    
    assert d1.get("is_wrong_photo") is True, f"Expected is_wrong_photo=True, got {d1.get('is_wrong_photo')}"
    assert "Wrong Photo" in d1.get("disease_detected", ""), f"Expected 'Wrong Photo' in disease_detected, got {d1.get('disease_detected')}"
    assert "Tomato" not in d1.get("crop_name", ""), f"Error: Animal image was falsely identified as Tomato!"
    print(">>> PASS: Animal image in auto-detect mode was correctly flagged as WRONG PHOTO!")

    print("\n=======================================================")
    print("TEST 2: Upload Animal image when user mistakenly selected 'Tomato'")
    print("Expected: CNN Domain Gatekeeper overrides Tomato, flags WRONG PHOTO")
    print("=======================================================")
    
    payload2 = {
        "image_base64": cattle_sample["image_data"],
        "crop_hint": "tomato",
        "latitude": 12.97,
        "longitude": 77.59,
        "preferred_language": "en"
    }
    req2 = urllib.request.Request(
        'http://127.0.0.1:8005/api/diagnose',
        data=json.dumps(payload2).encode("utf-8"),
        headers={'Content-Type': 'application/json'}
    )
    resp2 = urllib.request.urlopen(req2)
    d2 = json.loads(resp2.read().decode('utf-8'))
    
    print(f"Crop Name: {d2.get('crop_name')}")
    print(f"Disease Detected: {d2.get('disease_detected')}")
    print(f"is_wrong_photo: {d2.get('is_wrong_photo')}")
    print(f"CNN Domain: {d2.get('cnn_metrics', {}).get('cnn_domain')}")
    assert d2.get("is_wrong_photo") is True, f"Expected is_wrong_photo=True for animal uploaded to tomato"
    assert "Tomato" not in d2.get("crop_name", ""), f"Error: Tomato was not overridden"
    print(">>> PASS: Animal image mistakenly sent as 'tomato' was overridden and caught as WRONG PHOTO!")

    print("\n=======================================================")
    print("TEST 3: Upload legitimate Crop Leaf (Tomato)")
    print("Expected: is_wrong_photo = False, is_crop_leaf = True, Tomato diagnosed properly")
    print("=======================================================")
    
    payload3 = {
        "image_base64": tomato_sample["image_data"],
        "crop_hint": None,
        "latitude": 12.97,
        "longitude": 77.59,
        "preferred_language": "kn"
    }
    req3 = urllib.request.Request(
        'http://127.0.0.1:8005/api/diagnose',
        data=json.dumps(payload3).encode("utf-8"),
        headers={'Content-Type': 'application/json'}
    )
    resp3 = urllib.request.urlopen(req3)
    d3 = json.loads(resp3.read().decode('utf-8'))
    
    print(f"Crop Name: {d3.get('crop_name')}")
    print(f"Disease Detected: {d3.get('disease_detected')}")
    print(f"is_wrong_photo: {d3.get('is_wrong_photo')}")
    print(f"CNN Model: {d3.get('cnn_metrics', {}).get('cnn_model_name')}")
    print(f"CNN Domain: {d3.get('cnn_metrics', {}).get('cnn_domain')}")
    assert d3.get("is_wrong_photo") is False, "Crop leaf should not be wrong photo"
    assert "Tomato" in d3.get("crop_name", ""), f"Expected Tomato crop, got {d3.get('crop_name')}"
    print(">>> PASS: Legitimate tomato leaf recognized accurately!")

    print("\n=======================================================")
    print("TEST 4: Explicit Veterinary Mode ('Cattle & Livestock')")
    print("Expected: Legitimate Veterinary Pathology diagnosed, NOT Wrong Photo")
    print("=======================================================")
    
    payload4 = {
        "image_base64": cattle_sample["image_data"],
        "crop_hint": "livestock_cattle",
        "latitude": 12.97,
        "longitude": 77.59,
        "preferred_language": "kn"
    }
    req4 = urllib.request.Request(
        'http://127.0.0.1:8005/api/diagnose',
        data=json.dumps(payload4).encode("utf-8"),
        headers={'Content-Type': 'application/json'}
    )
    resp4 = urllib.request.urlopen(req4)
    d4 = json.loads(resp4.read().decode('utf-8'))
    
    print(f"Crop Name: {d4.get('crop_name')}")
    print(f"Disease Detected: {d4.get('disease_detected')}")
    print(f"is_animal_disease: {d4.get('is_animal_disease')}")
    print(f"is_wrong_photo: {d4.get('is_wrong_photo')}")
    print(f"Animal Warning: {d4.get('animal_warning')[:60]}...")
    assert d4.get("is_animal_disease") is True, "Expected is_animal_disease=True"
    assert d4.get("is_wrong_photo") is False, "Expected is_wrong_photo=False when veterinary mode is explicitly selected"
    print(">>> PASS: Explicit veterinary pathology works as intended!")

    print("\nALL 4 COMPREHENSIVE TESTS PASSED!")

if __name__ == '__main__':
    test_animal_wrong_photo()
