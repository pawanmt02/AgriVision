import urllib.request
import json
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')

def test_deep():
    # 1. Fetch sample images
    res = urllib.request.urlopen('http://127.0.0.1:8005/api/sample-images')
    samples = json.loads(res.read().decode('utf-8'))
    print(f"Total sample images: {len(samples)}")

    test_targets = [
        ("Arecanut", "Arecanut (Betel Nut)"),
        ("Ragi", "Finger Millet (Ragi)"),
        ("Cattle", "Cattle & Livestock"),
    ]

    for search_key, target_crop in test_targets:
        sample = next((s for s in samples if search_key in s['crop']), None)
        if not sample:
            print(f"Could not find sample for {search_key}")
            continue

        payload = {
            "image_base64": sample["image_data"],
            "crop_hint": target_crop,
            "latitude": 13.0,
            "longitude": 75.5,
            "preferred_language": "kn"
        }
        data_bytes = json.dumps(payload).encode("utf-8")

        req = urllib.request.Request(
            'http://127.0.0.1:8005/api/diagnose',
            data=data_bytes,
            headers={'Content-Type': 'application/json'}
        )

        try:
            resp = urllib.request.urlopen(req)
            d = json.loads(resp.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            print("HTTPError:", e.code, e.read().decode('utf-8', errors='replace'))
            continue

        print(f"\n=======================================================")
        print(f"Tested: {target_crop}")
        print(f"Detected Crop: {d.get('crop_name')}")
        print(f"Detected Disease: {d.get('disease_detected')}")
        print(f"Domain Category: {d.get('domain_category')}")
        print(f"Confidence Score: {d.get('confidence_score')}")
        print(f"Severity: {d.get('severity')}")
        cnn = d.get('cnn_metrics') or {}
        print(f"CNN Model Name: {cnn.get('cnn_model_name')}")
        print(f"CNN Feature Energy: {cnn.get('feature_energy')}")
        print(f"CNN Confidence: {cnn.get('cnn_confidence')}")
        print(f"Kannada Speech Summary: {d.get('localized_speech_summary', {}).get('kn')}")
        print(f"Organic Remedy: {d.get('organic_remedy')[:60]}...")
        print(f"Chemical Remedy: {d.get('chemical_remedy')[:60]}...")
        if d.get('is_animal_disease'):
            print(f"Animal Warning: {d.get('animal_warning')[:60]}...")
        print(f"=======================================================")

if __name__ == '__main__':
    test_deep()
