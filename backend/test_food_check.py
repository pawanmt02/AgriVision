import cv2
import numpy as np
import base64
import sys
from sample_data import SAMPLE_GALLERY

sys.stdout.reconfigure(encoding='utf-8')

def test_spectral_gatekeeper(name, rgb):
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    roi_total = rgb.shape[0] * rgb.shape[1]
    
    r_chan = rgb[:, :, 0].astype(np.float32)
    g_chan = rgb[:, :, 1].astype(np.float32)
    b_chan = rgb[:, :, 2].astype(np.float32)
    exg = 2 * g_chan - r_chan - b_chan
    
    neutral_mask = (np.abs(r_chan - g_chan) < 14) & (np.abs(g_chan - b_chan) < 14)
    
    # 1. Genuine botanical chlorophyll green (H: 29 to 92, vegetative saturation):
    true_chlorophyll_mask = (hsv[:, :, 0] >= 29) & (hsv[:, :, 0] <= 92) & (hsv[:, :, 1] >= 22) & (hsv[:, :, 2] >= 25)
    true_chlorophyll_ratio = float(np.sum(true_chlorophyll_mask)) / roi_total

    # 2. Foliar chlorosis (yellowing leaf blade): H in [26, 34], but plant leaf tissue has G close to R:
    chlorosis_mask = (hsv[:, :, 0] >= 25) & (hsv[:, :, 0] <= 34) & (g_chan >= r_chan - 18) & (g_chan > b_chan + 18)
    chlorosis_ratio = float(np.sum(chlorosis_mask)) / roi_total

    botanical_exg = (exg > 10) & (g_chan >= r_chan - 15)
    botanical_exg_ratio = float(np.sum(botanical_exg)) / roi_total

    foliar_score = max(true_chlorophyll_ratio + chlorosis_ratio, botanical_exg_ratio)
    
    # 3. Food / cooked snack (Vada Pav, Samosa, Fried items, Bread):
    # R > G + 12, R > B + 25, R > 115, H <= 28, not neutral
    food_mask = (r_chan > g_chan + 12) & (r_chan > b_chan + 25) & (r_chan > 115) & (hsv[:, :, 0] <= 28) & (~neutral_mask)
    food_ratio = float(np.sum(food_mask)) / roi_total
    
    # 4. Mammalian animal fur:
    animal_fur_tan = (r_chan > g_chan) & (g_chan >= b_chan) & (r_chan - b_chan > 20) & (r_chan > 70) & (r_chan <= 180) & (~neutral_mask)
    animal_ratio = float(np.sum(animal_fur_tan)) / roi_total

    # Classification
    if foliar_score >= 0.08 and food_ratio < 0.15 and (true_chlorophyll_ratio >= 0.04 or chlorosis_ratio >= 0.05):
        status = 'CROP_LEAF'
    elif food_ratio >= 0.18:
        status = 'FOOD_OR_SNACK'
    elif animal_ratio >= 0.18:
        status = 'ANIMAL_PHOTO'
    else:
        status = 'OTHER_NON_PLANT'
        
    print(f"{name:30}: foliar={foliar_score:.3f}, green_chlo={true_chlorophyll_ratio:.3f}, food={food_ratio:.3f} -> {status}")

for s in SAMPLE_GALLERY:
    raw = base64.b64decode(s['image_data'].split('base64,')[1])
    bgr = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    test_spectral_gatekeeper(s['crop'], rgb)

# Vada Pav
v_img = np.zeros((300, 300, 3), dtype=np.uint8)
v_img[:, :] = [200, 150, 80] # Bun
v_img[80:220, 80:220] = [220, 180, 50] # Vada
test_spectral_gatekeeper('Vada Pav (Food)', v_img)

# Samosa / Bread
s_img = np.zeros((300, 300, 3), dtype=np.uint8)
s_img[:, :] = [215, 160, 60] # Golden pastry
test_spectral_gatekeeper('Samosa / Pastry (Food)', s_img)
