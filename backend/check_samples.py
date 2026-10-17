import base64
from sample_data import SAMPLE_GALLERY
from cnn_engine import extract_cnn_features

for item in SAMPLE_GALLERY:
    raw = base64.b64decode(item['image_data'].split(',')[1])
    res = extract_cnn_features(raw)
    print(f"{item['crop']}: foliar={res.get('foliar_score')} animal={res.get('animal_score')} domain={res.get('cnn_domain')}")
