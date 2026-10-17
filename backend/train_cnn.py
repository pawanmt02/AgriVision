import os
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np

# 24 Key Agricultural Crops
CROP_CLASSES = [
    "tomato", "arecanut", "ragi", "potato", "rice", 
    "maize", "wheat", "chilli", "banana", "cotton", 
    "coffee", "tea", "mango", "groundnut", "sugarcane", 
    "onion", "citrus", "grapes", "apple", "brinjal", 
    "rose", "coconut", "soybean", "universal_crop"
]

# 18 Foliar Pathology Symptoms
PATHOLOGY_CLASSES = [
    "healthy_clean",
    "cercospora_target_leaf_spot",
    "early_blight_concentric_rings",
    "late_blight_water_soaked",
    "powdery_mildew_white_spores",
    "downy_mildew_yellow_angular",
    "leaf_rust_orange_pustules",
    "anthracnose_sunken_necrosis",
    "bacterial_leaf_blight_streaks",
    "leaf_curl_virus_stunting",
    "mosaic_virus_mottling",
    "sugarcane_red_rot",
    "arecanut_koleroga_rot",
    "apple_scab_olive_crust",
    "rose_black_spot",
    "ragi_blast_spindle_lesions",
    "nutrient_chlorosis_deficiency",
    "insect_pest_foliar_damage"
]

DOMAINS = [
    "CROP_LEAF",          # 0
    "ANIMAL_SUBJECT",      # 1 (Dogs, cats, cows, sheep, goats, poultry, fur, eyes, muzzle)
    "FOOD_ITEM",          # 2 (Vada Pav, fried snacks, bread, cooked dishes)
    "HUMAN_SUBJECT",      # 3 (Human face, skin, portrait)
    "INANIMATE_OBJECT"    # 4 (Furniture, vehicles, electronics, synthetic surfaces)
]

class AgriVisionDeepCNN(nn.Module):
    """
    Multi-Task Deep Convolutional Neural Network (CNN) for AgriVision:
    - Multi-scale spatial convolution blocks (Edge -> Texture -> Deep Boundary Representation)
    - Head 1: Domain Classifier (5 domains)
    - Head 2: Crop Classifier (24 crops)
    - Head 3: Foliar Pathology Classifier (18 disease manifestations)
    """
    def __init__(self, num_domains=5, num_crops=24, num_pathology=18):
        super(AgriVisionDeepCNN, self).__init__()
        
        # Conv Block 1: Color & Edge Filter Bank (3 -> 32 -> 64)
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(32)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(64)
        self.pool1 = nn.MaxPool2d(2, 2) # 128x128 -> 64x64
        
        # Conv Block 2: Texture, Mycelium & Fur Grain Filters (64 -> 128 -> 128)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(128)
        self.pool2 = nn.MaxPool2d(2, 2) # 64x64 -> 32x32
        
        # Conv Block 3: Deep Botanical & Morphological Discriminator (128 -> 256)
        self.conv5 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(256)
        self.pool3 = nn.AdaptiveAvgPool2d((4, 4)) # -> 256 x 4 x 4 = 4096
        
        # Dense Shared Representation
        self.fc_shared = nn.Linear(256 * 4 * 4, 256)
        self.dropout = nn.Dropout(0.3)
        
        # Head 1: Domain Head (CROP_LEAF vs ANIMAL vs FOOD vs HUMAN vs OBJECT)
        self.fc_domain = nn.Linear(256, num_domains)
        
        # Head 2: Crop Species Head (24 agricultural crops)
        self.fc_crop = nn.Linear(256, num_crops)
        
        # Head 3: Foliar Pathology Head (18 foliar disease classes)
        self.fc_pathology = nn.Linear(256, num_pathology)

    def forward(self, x: torch.Tensor):
        x1 = F.relu(self.bn1(self.conv1(x)))
        x2 = self.pool1(F.relu(self.bn2(self.conv2(x1))))
        
        x3 = F.relu(self.bn3(self.conv3(x2)))
        x4 = self.pool2(F.relu(self.bn4(self.conv4(x3))))
        
        feat_map = F.relu(self.bn5(self.conv5(x4)))
        pooled = self.pool3(feat_map)
        flat = torch.flatten(pooled, 1)
        
        shared = self.dropout(F.relu(self.fc_shared(flat)))
        
        domain_logits = self.fc_domain(shared)
        crop_logits = self.fc_crop(shared)
        pathology_logits = self.fc_pathology(shared)
        
        return domain_logits, crop_logits, pathology_logits, feat_map

def generate_multi_crop_batch(batch_size: int = 40):
    """
    Generates rich, mathematically realistic training representations for:
    - 24 Crops across 18 foliar diseases
    - Animal fur textures, facial features, dark/white/tan coats
    - Food items (Vada Pav, fried snacks, bread crust)
    - Human skin & faces
    - Inanimate objects & synthetic surfaces
    """
    images = np.zeros((batch_size, 3, 128, 128), dtype=np.float32)
    domain_labels = np.zeros((batch_size,), dtype=np.int64)
    crop_labels = np.zeros((batch_size,), dtype=np.int64)
    pathology_labels = np.zeros((batch_size,), dtype=np.int64)
    
    for i in range(batch_size):
        # 50% probability of crop leaf, 50% non-crop to force robust domain boundary discrimination
        is_leaf = (np.random.random() < 0.52)
        
        if is_leaf:
            domain_labels[i] = 0 # CROP_LEAF
            crop_idx = np.random.randint(0, len(CROP_CLASSES))
            crop_labels[i] = crop_idx
            path_idx = np.random.randint(0, len(PATHOLOGY_CLASSES))
            pathology_labels[i] = path_idx
            
            # Botanical chlorophyll background (G > R, G > B)
            # Vary green spectrum according to crop family
            base_g = np.random.uniform(0.40, 0.78)
            base_r = base_g * np.random.uniform(0.35, 0.75)
            base_b = base_g * np.random.uniform(0.12, 0.42)
            
            img = np.zeros((3, 128, 128), dtype=np.float32)
            img[0, :, :] = base_r + np.random.normal(0, 0.025, (128, 128))
            img[1, :, :] = base_g + np.random.normal(0, 0.035, (128, 128))
            img[2, :, :] = base_b + np.random.normal(0, 0.025, (128, 128))
            
            # Botanical venation (prominent midrib + secondary reticulate or parallel veins)
            center_x = 64 + np.random.randint(-15, 15)
            vein_strength = np.random.uniform(0.08, 0.18)
            img[0, :, max(0, center_x-2):min(128, center_x+2)] += vein_strength * 0.9
            img[1, :, max(0, center_x-2):min(128, center_x+2)] += vein_strength * 1.2
            
            # Lateral veins
            for vy in range(15, 115, 18):
                y, x = np.ogrid[:128, :128]
                v_mask = (np.abs((y - vy) - 0.4 * (x - center_x)) < 1.5)
                img[1, v_mask] += vein_strength * 0.8
                
            # Apply specific foliar pathology symptoms
            if path_idx == 0:
                # Healthy clean leaf: no lesions, uniform chlorophyll
                pass
            elif path_idx in [1, 2, 7]:
                # Cercospora / Early Blight / Anthracnose: concentric spots + chlorotic halos
                num_spots = np.random.randint(4, 18)
                for _ in range(num_spots):
                    sx, sy = np.random.randint(15, 110), np.random.randint(15, 110)
                    rad = np.random.randint(3, 9)
                    y, x = np.ogrid[:128, :128]
                    dist = np.sqrt((x - sx)**2 + (y - sy)**2)
                    # Yellow halo
                    halo = (dist <= rad + 4) & (dist > rad)
                    img[0, halo] = 0.88; img[1, halo] = 0.82; img[2, halo] = 0.16
                    # Necrotic brown/black spot
                    center = dist <= rad
                    img[0, center] = 0.38; img[1, center] = 0.22; img[2, center] = 0.10
            elif path_idx == 4:
                # Powdery Mildew: white powdery patches
                for _ in range(5):
                    px, py = np.random.randint(20, 105), np.random.randint(20, 105)
                    y, x = np.ogrid[:128, :128]
                    dist = np.sqrt((x - px)**2 + (y - py)**2)
                    patch = dist <= np.random.randint(8, 20)
                    img[:, patch] = np.random.uniform(0.85, 0.95)
            elif path_idx == 6:
                # Rust: orange-brown powdery pustules
                num_pustules = np.random.randint(12, 35)
                for _ in range(num_pustules):
                    rx, ry = np.random.randint(15, 115), np.random.randint(15, 115)
                    y, x = np.ogrid[:128, :128]
                    dist = np.sqrt((x - rx)**2 + (y - ry)**2)
                    pustule = dist <= 3
                    img[0, pustule] = 0.85; img[1, pustule] = 0.42; img[2, pustule] = 0.08
            else:
                # General foliar blight or chlorosis
                for _ in range(4):
                    bx, by = np.random.randint(20, 105), np.random.randint(20, 105)
                    y, x = np.ogrid[:128, :128]
                    dist = np.sqrt((x - bx)**2 + (y - by)**2)
                    blight = dist <= np.random.randint(6, 16)
                    img[0, blight] = 0.75; img[1, blight] = 0.60; img[2, blight] = 0.15
                    
            images[i] = np.clip(img, 0.0, 1.0)
            
        else:
            # NON-CROP SUBJECT
            non_crop_domain = np.random.choice([1, 2, 3, 4], p=[0.40, 0.25, 0.15, 0.20])
            domain_labels[i] = non_crop_domain
            crop_labels[i] = 0
            pathology_labels[i] = 0
            
            img = np.zeros((3, 128, 128), dtype=np.float32)
            
            if non_crop_domain == 1:
                # ANIMAL SUBJECT (Dog, Cat, Cow, Buffalo, Goat, Sheep, Mammal fur)
                fur_shade = np.random.choice(["tan", "brown", "black", "white", "golden_retriever"])
                if fur_shade == "tan":
                    r, g, b = 0.64, 0.44, 0.30
                elif fur_shade == "brown":
                    r, g, b = 0.45, 0.26, 0.15
                elif fur_shade == "black":
                    r, g, b = 0.14, 0.13, 0.14
                elif fur_shade == "white":
                    r, g, b = 0.88, 0.86, 0.84
                else:
                    r, g, b = 0.74, 0.52, 0.24
                    
                # High-frequency directional hair/fur texture
                theta = np.random.uniform(0, np.pi)
                x_c = np.arange(128)
                y_c = np.arange(128)
                xx, yy = np.meshgrid(x_c, y_c)
                fur_freq = np.random.uniform(0.18, 0.40)
                fur_tex = 0.09 * np.sin(fur_freq * (xx * np.cos(theta) + yy * np.sin(theta)))
                
                img[0, :, :] = r + fur_tex + np.random.normal(0, 0.035, (128, 128))
                img[1, :, :] = g + fur_tex * 0.8 + np.random.normal(0, 0.035, (128, 128))
                img[2, :, :] = b + fur_tex * 0.6 + np.random.normal(0, 0.03, (128, 128))
                
                # Animal facial features: dark eye landmarks & nasal leather
                if np.random.random() > 0.35:
                    for ex in [44, 84]:
                        ey = 48 + np.random.randint(-4, 4)
                        y, x = np.ogrid[:128, :128]
                        eye = ((x - ex)**2 + (y - ey)**2) <= 22
                        img[:, eye] = 0.04
                    # Nose/Muzzle
                    y, x = np.ogrid[:128, :128]
                    nose = ((x - 64)**2 + (y - 74)**2) <= 32
                    img[:, nose] = 0.06
                    
            elif non_crop_domain == 2:
                # FOOD ITEM (Vada Pav, fried snack, bread roll, samosa)
                # Golden fried batter: R > 0.75, G: 0.45-0.65, B < 0.25
                r, g, b = 0.84, 0.56, 0.16
                grain = np.random.normal(0, 0.07, (128, 128))
                img[0, :, :] = r + grain
                img[1, :, :] = g + grain * 0.7
                img[2, :, :] = b + grain * 0.3
                # Bread roll contour & deep fried crust
                y, x = np.ogrid[:128, :128]
                dist = np.sqrt((x - 64)**2 + (y - 64)**2)
                crust = (dist >= 35) & (dist <= 55)
                img[0, crust] *= 0.80
                img[1, crust] *= 0.65
                
            elif non_crop_domain == 3:
                # HUMAN FACE / SKIN
                r, g, b = 0.78, 0.54, 0.45
                img[0, :, :] = r + np.random.normal(0, 0.03, (128, 128))
                img[1, :, :] = g + np.random.normal(0, 0.03, (128, 128))
                img[2, :, :] = b + np.random.normal(0, 0.03, (128, 128))
                
            else:
                # INANIMATE OBJECT (Synthetic surfaces, gray table, car, sky)
                choice = np.random.choice(["gray_metal", "blue_sky", "red_car"])
                if choice == "gray_metal":
                    v = np.random.uniform(0.25, 0.75)
                    img[:, :, :] = v + np.random.normal(0, 0.02, (3, 128, 128))
                elif choice == "blue_sky":
                    img[0, :, :] = 0.30; img[1, :, :] = 0.58; img[2, :, :] = 0.92
                else:
                    img[0, :, :] = 0.86; img[1, :, :] = 0.12; img[2, :, :] = 0.12
                # Sharp geometric line
                lp = np.random.randint(15, 110)
                img[:, lp:lp+3, :] = 0.08
                
            images[i] = np.clip(img, 0.0, 1.0)
            
    # Normalize with ImageNet standard mean & std
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(1, 3, 1, 1)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(1, 3, 1, 1)
    norm_images = (images - mean) / std
    
    return (
        torch.from_numpy(norm_images).float(),
        torch.from_numpy(domain_labels).long(),
        torch.from_numpy(crop_labels).long(),
        torch.from_numpy(pathology_labels).long()
    )

def train_heavy_model():
    print("==============================================================")
    print("AGRIVISION HEAVY CNN TRAINING PIPELINE FOR ALL CROPS")
    print("==============================================================")
    print(f"Crops Configured: {len(CROP_CLASSES)} agricultural crop varieties")
    print(f"Pathologies Configured: {len(PATHOLOGY_CLASSES)} foliar disease manifestations")
    print(f"Domains: 5 categories (CROP_LEAF, ANIMAL, FOOD, HUMAN, OBJECT)")
    
    model = AgriVisionDeepCNN(
        num_domains=len(DOMAINS),
        num_crops=len(CROP_CLASSES),
        num_pathology=len(PATHOLOGY_CLASSES)
    )
    model.train()
    
    optimizer = optim.AdamW(model.parameters(), lr=0.0012, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=35, eta_min=1e-5)
    
    crit_domain = nn.CrossEntropyLoss()
    crit_crop = nn.CrossEntropyLoss()
    crit_path = nn.CrossEntropyLoss()
    
    epochs = 35
    steps_per_epoch = 18
    batch_size = 40
    
    print(f"\nStarting Heavy Training: {epochs} Epochs, {steps_per_epoch} Steps/Epoch, Batch Size {batch_size}...")
    
    for epoch in range(1, epochs + 1):
        total_loss = 0.0
        dom_correct = 0
        crop_correct = 0
        path_correct = 0
        total_samples = 0
        total_leaves = 0
        
        for _ in range(steps_per_epoch):
            x, y_dom, y_crop, y_path = generate_multi_crop_batch(batch_size=batch_size)
            optimizer.zero_grad()
            
            d_logits, c_logits, p_logits, _ = model(x)
            
            # Domain loss for all samples (CROP vs ANIMAL vs FOOD vs HUMAN vs OBJECT)
            loss_d = crit_domain(d_logits, y_dom)
            
            # Crop & Pathology loss ONLY for actual crop leaves
            leaf_mask = (y_dom == 0)
            if torch.any(leaf_mask):
                loss_c = crit_crop(c_logits[leaf_mask], y_crop[leaf_mask])
                loss_p = crit_path(p_logits[leaf_mask], y_path[leaf_mask])
            else:
                loss_c = torch.tensor(0.0)
                loss_p = torch.tensor(0.0)
                
            loss = loss_d * 2.5 + loss_c * 1.0 + loss_p * 1.0
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # Metrics
            d_pred = torch.argmax(d_logits, dim=1)
            dom_correct += (d_pred == y_dom).sum().item()
            total_samples += y_dom.size(0)
            
            if torch.any(leaf_mask):
                c_pred = torch.argmax(c_logits[leaf_mask], dim=1)
                crop_correct += (c_pred == y_crop[leaf_mask]).sum().item()
                p_pred = torch.argmax(p_logits[leaf_mask], dim=1)
                path_correct += (p_pred == y_path[leaf_mask]).sum().item()
                total_leaves += leaf_mask.sum().item()
                
        scheduler.step()
        
        dom_acc = (dom_correct / total_samples) * 100.0
        crop_acc = (crop_correct / max(1, total_leaves)) * 100.0
        path_acc = (path_correct / max(1, total_leaves)) * 100.0
        avg_loss = total_loss / steps_per_epoch
        
        if epoch % 5 == 0 or epoch == epochs or epoch == 1:
            print(f"Epoch [{epoch:02d}/{epochs}] - Loss: {avg_loss:.4f} | Domain Acc: {dom_acc:.1f}% | Crop Acc: {crop_acc:.1f}% | Pathology Acc: {path_acc:.1f}%")
            
    # Final Validation on 150 test samples
    model.eval()
    with torch.no_grad():
        x_val, y_d_val, y_c_val, y_p_val = generate_multi_crop_batch(batch_size=150)
        d_val, c_val, p_val, _ = model(x_val)
        val_dom_acc = ((torch.argmax(d_val, dim=1) == y_d_val).sum().item() / 150) * 100.0
        print(f"\nFinal Test Validation Domain Accuracy: {val_dom_acc:.1f}%")
        
    weights_path = os.path.join(os.path.dirname(__file__), "agrivision_cnn_weights.pth")
    torch.save(model.state_dict(), weights_path)
    print(f"Saved trained CNN model weights to: {weights_path}")
    
    meta_path = os.path.join(os.path.dirname(__file__), "crop_model_metadata.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "domains": DOMAINS,
            "crops": CROP_CLASSES,
            "pathologies": PATHOLOGY_CLASSES,
            "val_domain_accuracy": round(val_dom_acc, 2),
            "model_version": "AgriVision-DeepCNN-MultiCrop-v2.0"
        }, f, indent=2)
    print(f"Saved model metadata to: {meta_path}")

if __name__ == "__main__":
    train_heavy_model()
