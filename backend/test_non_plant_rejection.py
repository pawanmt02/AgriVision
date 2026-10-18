import urllib.request
import json
import base64
import sys
import numpy as np
from PIL import Image
from io import BytesIO

sys.stdout.reconfigure(encoding='utf-8')

def create_synthetic_image(color_mode="human"):
    """Creates synthetic non-plant test images for testing domain rejection."""
    img_arr = np.zeros((150, 150, 3), dtype=np.uint8)
    if color_mode == "human":
        # Human skin tone (warm peachy-tan: R=215, G=155, B=125)
        img_arr[:, :] = [215, 155, 125]
        # Add eyes / mouth
        img_arr[40:55, 40:60] = [70, 45, 30]
        img_arr[40:55, 90:110] = [70, 45, 30]
        img_arr[100:115, 55:95] = [170, 50, 50]
    elif color_mode == "vehicle_sky":
        # Upper half blue sky, lower half dark road / metallic red car
        img_arr[0:75, :] = [100, 160, 240] # Sky blue
        img_arr[75:150, :] = [210, 30, 40]  # Red vehicle body
    elif color_mode == "furniture_room":
        # Grayscale concrete / office desk / monitor
        img_arr[:, :] = [128, 130, 129]
        img_arr[30:120, 30:120] = [50, 52, 51]
    elif color_mode == "vadapav":
        # Golden brown pav bun + deep-fried yellow besan vada
        img_arr[:, :] = [200, 150, 80]
        img_arr[40:110, 40:110] = [220, 180, 50]
    elif color_mode == "samosa":
        # Fried golden-yellow snack / pastry
        img_arr[:, :] = [215, 160, 60]

    buf = BytesIO()
    Image.fromarray(img_arr).save(buf, format="JPEG")
    b64_str = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")
    return b64_str

def run_tests():
    print("Fetching sample gallery for plant leaf & animal samples...")
    res = urllib.request.urlopen('http://127.0.0.1:8005/api/sample-images')
    samples = json.loads(res.read().decode('utf-8'))

    cattle_sample = next((s for s in samples if "Cattle" in s["crop"]), None)
    tomato_sample = next((s for s in samples if "Tomato" in s["crop"]), None)
    arecanut_sample = next((s for s in samples if "Arecanut" in s["crop"]), None)
    ragi_sample = next((s for s in samples if "Ragi" in s["crop"]), None)

    human_b64 = create_synthetic_image("human")
    vehicle_sky_b64 = create_synthetic_image("vehicle_sky")
    furniture_b64 = create_synthetic_image("furniture_room")
    vadapav_b64 = create_synthetic_image("vadapav")
    samosa_b64 = create_synthetic_image("samosa")

    tests = [
        ("TEST 1: Animal Photo (Cattle) in Auto-Detect", cattle_sample["image_data"], None, True, "Animal"),
        ("TEST 2: Human Face / Person Photo", human_b64, None, True, "Human"),
        ("TEST 3: Vehicle / Sky Photo", vehicle_sky_b64, None, True, "Not a Plant"),
        ("TEST 4: Furniture / Indoor Object Photo", furniture_b64, None, True, "Not a Plant"),
        ("TEST 5: Animal Photo mistakenly sent with crop_hint='Tomato'", cattle_sample["image_data"], "Tomato", True, "Animal"),
        ("TEST 6: Cooked Food Photo (Vada Pav) in Auto-Detect", vadapav_b64, None, True, "Food"),
        ("TEST 7: Cooked Food Photo (Vada Pav) mistakenly sent with crop_hint='Tomato'", vadapav_b64, "Tomato", True, "Food"),
        ("TEST 8: Cooked Food Photo (Samosa / Pastry)", samosa_b64, None, True, "Food"),
        ("TEST 9: Legitimate Plant Disease Leaf (Tomato Late Blight)", tomato_sample["image_data"], None, False, "Tomato"),
        ("TEST 10: Legitimate Plant Disease Leaf (Arecanut Koleroga)", arecanut_sample["image_data"], "Arecanut", False, "Arecanut"),
        ("TEST 11: Legitimate Plant Disease Leaf (Ragi Blast)", ragi_sample["image_data"], "Ragi", False, "Ragi"),
    ]

    for title, img_b64, crop_hint, expect_error, key_phrase in tests:
        print(f"\n=======================================================")
        print(title)
        print(f"Expect Error: {expect_error}")
        print("=======================================================")

        payload = {
            "image_base64": img_b64,
            "crop_hint": crop_hint,
            "latitude": 12.97,
            "longitude": 77.59,
            "preferred_language": "kn"
        }
        req = urllib.request.Request(
            'http://127.0.0.1:8005/api/diagnose',
            data=json.dumps(payload).encode("utf-8"),
            headers={'Content-Type': 'application/json'}
        )
        resp = urllib.request.urlopen(req)
        d = json.loads(resp.read().decode('utf-8'))

        print(f"Detected Crop: {d.get('crop_name')}")
        print(f"Disease Detected: {d.get('disease_detected')}")
        print(f"is_wrong_photo: {d.get('is_wrong_photo')}")
        print(f"is_valid_agricultural_image: {d.get('is_valid_agricultural_image')}")
        print(f"CNN Domain: {d.get('cnn_metrics', {}).get('cnn_domain')}")
        print(f"Foliar Presence: {d.get('cnn_metrics', {}).get('foliar_score')}")
        print(f"Kannada Speech: {d.get('localized_speech_summary', {}).get('kn')[:80]}...")

        if expect_error:
            assert d.get("is_wrong_photo") is True, f"Failed: Expected is_wrong_photo=True for {title}"
            assert d.get("is_valid_agricultural_image") is False, f"Failed: Expected is_valid_agricultural_image=False for {title}"
            assert "Error" in d.get("disease_detected", ""), f"Failed: Expected 'Error' in disease_detected for {title}"
            assert "Tomato" not in d.get("crop_name", "") or crop_hint != "Tomato", f"Failed: False Tomato classification"
            print(f">>> PASS: {title} correctly triggered an ERROR / REJECTION!")
        else:
            assert d.get("is_wrong_photo") is False, f"Failed: Expected legitimate leaf to pass for {title}"
            assert d.get("is_valid_agricultural_image") is True, f"Failed: Expected valid image for {title}"
            assert "Error" not in d.get("disease_detected", ""), f"Failed: Plant disease should not trigger error"
            print(f">>> PASS: Legitimate plant disease leaf correctly recognized and diagnosed!")

    print("\n=======================================================")
    print("ALL 11 RIGOROUS FOOD, NON-PLANT & PLANT TESTS PASSED 100%!")
    print("=======================================================")

if __name__ == '__main__':
    run_tests()
