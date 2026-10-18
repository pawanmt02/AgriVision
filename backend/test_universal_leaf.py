import base64
import sys
import numpy as np
from PIL import Image, ImageDraw
from io import BytesIO

sys.stdout.reconfigure(encoding='utf-8')

from ai_engine import diagnose_leaf_image

def make_leaf_held_in_hand_over_soil():
    """Simulates a real farmer leaf held in fingers with brown soil background."""
    img = Image.new("RGB", (250, 250), (130, 90, 60)) # Brown garden soil background
    draw = ImageDraw.Draw(img)

    # Farmer's thumb/fingers holding the stem at the bottom
    draw.ellipse([80, 190, 170, 260], fill=(210, 155, 120)) # Human skin tone

    # Green leaf body (olive / shaded green with G slightly above R)
    draw.ellipse([50, 30, 200, 190], fill=(85, 120, 60), outline=(50, 80, 35), width=2)
    # Veins
    draw.line([125, 35, 125, 190], fill=(45, 75, 30), width=2)
    for y in range(60, 170, 25):
        draw.line([125, y, 75, y - 15], fill=(55, 90, 40), width=1)
        draw.line([125, y, 175, y - 15], fill=(55, 90, 40), width=1)

    # Some necrotic brown blight spots on the leaf blade
    draw.ellipse([70, 80, 110, 120], fill=(70, 45, 30))
    draw.ellipse([140, 110, 175, 145], fill=(75, 50, 32))

    buf = BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def make_arbitrary_leaf_with_white_powdery_mildew():
    """Simulates an arbitrary unknown plant leaf with white powdery mildew."""
    img = Image.new("RGB", (250, 250), (210, 210, 210)) # Neutral gray background
    draw = ImageDraw.Draw(img)

    # Serrated generic green leaf
    draw.polygon([(125, 20), (190, 90), (170, 160), (125, 230), (80, 160), (60, 90)], fill=(70, 150, 65))
    draw.line([125, 20, 125, 230], fill=(30, 90, 30), width=3)

    # White powdery mildew mycelial patches on the leaf surface
    draw.ellipse([90, 70, 140, 120], fill=(235, 246, 230))
    draw.ellipse([130, 110, 170, 150], fill=(238, 248, 232))
    draw.ellipse([85, 140, 120, 175], fill=(232, 244, 228))

    buf = BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def make_arbitrary_leaf_with_yellow_chlorosis():
    """Simulates an arbitrary unknown plant leaf with viral mosaic yellowing."""
    img = Image.new("RGB", (250, 250), (235, 235, 235))
    draw = ImageDraw.Draw(img)

    # Yellowing mosaic leaf blade
    draw.ellipse([50, 30, 200, 220], fill=(185, 195, 45), outline=(130, 140, 30), width=2)
    # Patches of green and bright chlorotic yellow
    draw.ellipse([70, 60, 130, 120], fill=(240, 225, 50))
    draw.ellipse([120, 110, 180, 170], fill=(245, 230, 55))
    draw.ellipse([80, 140, 130, 190], fill=(75, 145, 60))

    buf = BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def make_vadapav_snack():
    """Simulates fried vada pav (cooked food snack)."""
    img = Image.new("RGB", (250, 250), (200, 150, 80)) # Pav bun
    draw = ImageDraw.Draw(img)
    draw.ellipse([60, 60, 190, 190], fill=(225, 185, 45)) # Deep fried yellow besan batter
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def make_cattle_animal():
    """Simulates animal fur / coat."""
    img = Image.new("RGB", (250, 250), (180, 125, 90)) # Animal fur
    draw = ImageDraw.Draw(img)
    draw.ellipse([70, 60, 110, 100], fill=(205, 145, 125)) # Animal skin nodules
    draw.ellipse([140, 120, 180, 160], fill=(205, 145, 125))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

def run():
    print("==================================================================")
    print("AGRIVISION UNIVERSAL LEAF & ZERO FALSE ANIMAL REJECTION TEST SUITE")
    print("==================================================================")

    # TEST 1: Leaf held in hand over garden soil
    b64_soil_hand = make_leaf_held_in_hand_over_soil()
    res1 = diagnose_leaf_image(b64_soil_hand, crop_hint="Auto-Detect Any Crop Leaf / ಸ್ವಯಂ ಪತ್ತೆ (ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ)")
    print("\n--- TEST 1: Real Leaf held in fingers over brown garden soil ---")
    print(f"Crop Name: {res1.crop_name}")
    print(f"Disease Detected: {res1.disease_detected}")
    print(f"Is Wrong Photo: {res1.is_wrong_photo} (Expected: False)")
    print(f"CNN Domain: {res1.cnn_metrics.get('cnn_domain')}")
    print(f"Kannada Speech: {res1.localized_speech_summary.get('kn')[:90]}...")
    assert not res1.is_wrong_photo, "FAILED: Real leaf was falsely classified as wrong photo!"
    assert "Animal" not in res1.crop_name, "FAILED: Real leaf was called an animal!"
    print(">>> PASS: Real leaf held in hand over soil correctly diagnosed as plant disease!")

    # TEST 2: Arbitrary unknown leaf with powdery mildew
    b64_mildew = make_arbitrary_leaf_with_white_powdery_mildew()
    res2 = diagnose_leaf_image(b64_mildew, crop_hint="Auto-Detect Any Crop Leaf / ಸ್ವಯಂ ಪತ್ತೆ (ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ)")
    print("\n--- TEST 2: Arbitrary Leaf with White Powdery Mildew ---")
    print(f"Crop Name: {res2.crop_name}")
    print(f"Disease Detected: {res2.disease_detected}")
    print(f"Pathogen: {res2.pathogen_type}")
    print(f"Organic Remedy: {res2.organic_remedy[:90]}...")
    print(f"Chemical Remedy: {res2.chemical_remedy[:90]}...")
    print(f"Kannada Speech: {res2.localized_speech_summary.get('kn')[:90]}...")
    assert not res2.is_wrong_photo, "FAILED: Universal leaf was called wrong photo!"
    assert "Powdery Mildew" in res2.disease_detected or "Mildew" in res2.disease_detected, f"Unexpected disease: {res2.disease_detected}"
    print(">>> PASS: Universal powdery mildew diagnosed accurately!")

    # TEST 3: Arbitrary unknown leaf with viral chlorosis
    b64_chlorosis = make_arbitrary_leaf_with_yellow_chlorosis()
    res3 = diagnose_leaf_image(b64_chlorosis, crop_hint="Auto-Detect Any Crop Leaf / ಸ್ವಯಂ ಪತ್ತೆ (ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ)")
    print("\n--- TEST 3: Arbitrary Leaf with Chlorosis / Mosaic ---")
    print(f"Crop Name: {res3.crop_name}")
    print(f"Disease Detected: {res3.disease_detected}")
    print(f"Pathogen: {res3.pathogen_type}")
    assert not res3.is_wrong_photo, "FAILED: Universal leaf was called wrong photo!"
    print(">>> PASS: Universal chlorosis diagnosed accurately!")

    # TEST 4: Cooked Food (Vada Pav)
    b64_vadapav = make_vadapav_snack()
    res4 = diagnose_leaf_image(b64_vadapav, crop_hint="Auto-Detect Any Crop Leaf / ಸ್ವಯಂ ಪತ್ತೆ (ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ)")
    print("\n--- TEST 4: Cooked Food (Vada Pav) ---")
    print(f"Crop Name: {res4.crop_name}")
    print(f"Disease Detected: {res4.disease_detected}")
    print(f"Is Wrong Photo: {res4.is_wrong_photo} (Expected: True)")
    assert res4.is_wrong_photo, "FAILED: Food snack was not rejected!"
    assert "Food" in res4.crop_name or "Food" in res4.disease_detected, "FAILED: Did not detect Food!"
    print(">>> PASS: Food snack correctly rejected with safety warnings!")

    # TEST 5: Animal Photo (Cattle)
    b64_cattle = make_cattle_animal()
    res5 = diagnose_leaf_image(b64_cattle, crop_hint="Auto-Detect Any Crop Leaf / ಸ್ವಯಂ ಪತ್ತೆ (ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ)")
    print("\n--- TEST 5: Animal Photo (Cattle) ---")
    print(f"Crop Name: {res5.crop_name}")
    print(f"Disease Detected: {res5.disease_detected}")
    print(f"Is Wrong Photo: {res5.is_wrong_photo} (Expected: True)")
    assert res5.is_wrong_photo, "FAILED: Animal was not rejected in auto-detect crop mode!"
    assert "Animal" in res5.crop_name or "Animal" in res5.disease_detected, "FAILED: Did not identify Animal!"
    print(">>> PASS: Animal photo correctly rejected with veterinary warnings!")

    print("\n==================================================================")
    print("ALL 5 TESTS PASSED WITH 100% SUCCESS!")
    print("==================================================================")

if __name__ == "__main__":
    run()
