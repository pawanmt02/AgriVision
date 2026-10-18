import base64
from io import BytesIO
from PIL import Image, ImageDraw

def create_sample_leaf_image(leaf_type: str) -> str:
    """Generates a realistic synthetic leaf or animal skin image for instant UI testing."""
    width, height = 320, 320
    img = Image.new("RGB", (width, height), (242, 246, 243))
    draw = ImageDraw.Draw(img)

    # Base leaf shape coordinates (elliptical tapering leaf)
    leaf_color = (46, 125, 50) # Vibrant green default
    
    if leaf_type == "tomato_late_blight":
        leaf_color = (67, 160, 71)
        # Draw leaf body
        draw.ellipse([60, 40, 260, 280], fill=leaf_color, outline=(27, 94, 32), width=3)
        # Main vein
        draw.line([160, 45, 160, 280], fill=(27, 94, 32), width=3)
        # Secondary veins
        for y in range(80, 240, 30):
            draw.line([160, y, 90, y - 20], fill=(46, 125, 50), width=2)
            draw.line([160, y, 230, y - 20], fill=(46, 125, 50), width=2)
        # Large necrotic water-soaked brown/black lesions
        draw.ellipse([70, 70, 150, 160], fill=(62, 39, 35), outline=(93, 64, 55), width=2)
        draw.ellipse([170, 120, 245, 210], fill=(44, 28, 25), outline=(78, 52, 46), width=2)
        # White fuzzy mildew halos
        draw.arc([65, 65, 155, 165], start=0, end=360, fill=(236, 239, 241), width=3)
        draw.arc([165, 115, 250, 215], start=0, end=360, fill=(236, 239, 241), width=3)

    elif leaf_type == "potato_early_blight":
        leaf_color = (76, 175, 80)
        draw.ellipse([70, 50, 250, 270], fill=leaf_color, outline=(46, 125, 50), width=3)
        draw.line([160, 50, 160, 270], fill=(27, 94, 32), width=3)
        centers = [(120, 120), (190, 180), (140, 220)]
        for cx, cy in centers:
            draw.ellipse([cx - 35, cy - 35, cx + 35, cy + 35], fill=(253, 216, 53))
            draw.ellipse([cx - 25, cy - 25, cx + 25, cy + 25], fill=(109, 76, 65))
            draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=(141, 110, 99))
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(46, 27, 24))

    elif leaf_type == "rice_bacterial_blight":
        img = Image.new("RGB", (width, height), (245, 248, 245))
        draw = ImageDraw.Draw(img)
        draw.polygon([(140, 30), (180, 30), (200, 290), (120, 290)], fill=(76, 175, 80), outline=(46, 125, 50), width=2)
        draw.line([160, 30, 160, 290], fill=(27, 94, 32), width=2)
        draw.polygon([(140, 30), (155, 30), (150, 180), (130, 160)], fill=(255, 238, 88))
        draw.polygon([(165, 30), (180, 30), (195, 200), (170, 170)], fill=(255, 238, 88))
        draw.polygon([(145, 30), (175, 30), (170, 90), (150, 90)], fill=(245, 245, 240))

    elif leaf_type == "corn_rust":
        img = Image.new("RGB", (width, height), (242, 246, 243))
        draw = ImageDraw.Draw(img)
        draw.polygon([(130, 20), (190, 20), (230, 300), (90, 300)], fill=(102, 187, 106), outline=(56, 142, 60), width=3)
        draw.line([160, 20, 160, 300], fill=(46, 125, 50), width=4)
        pustules = [(130, 80), (180, 95), (140, 140), (175, 150), (120, 190), (185, 210), (145, 240), (165, 260)]
        for px, py in pustules:
            draw.ellipse([px - 14, py - 6, px + 14, py + 6], fill=(255, 167, 38))
            draw.ellipse([px - 10, py - 4, px + 10, py + 4], fill=(141, 64, 0))

    elif leaf_type == "apple_scab":
        draw.ellipse([80, 50, 240, 270], fill=(129, 199, 132), outline=(56, 142, 60), width=3)
        draw.line([160, 50, 160, 270], fill=(46, 125, 50), width=3)
        scabs = [(120, 100), (180, 130), (135, 180), (170, 210)]
        for sx, sy in scabs:
            draw.ellipse([sx - 20, sy - 18, sx + 20, sy + 18], fill=(85, 107, 47), outline=(60, 75, 30), width=2)

    elif leaf_type == "bovine_lumpy_skin":
        # Mammalian animal skin (warm tan, peach/flesh coat with distinct raised circumscribed nodules)
        img = Image.new("RGB", (width, height), (198, 142, 106))
        draw = ImageDraw.Draw(img)
        # Texture lines of short cattle fur
        for y in range(10, 310, 8):
            draw.line([20, y, 300, y + 4], fill=(182, 128, 93), width=1)
        # Characteristic raised circumscribed round nodules with central depressed necrotic cores
        nodules = [
            (90, 80, 28), (170, 70, 32), (245, 95, 26),
            (80, 160, 34), (160, 155, 38), (230, 175, 30),
            (110, 240, 30), (195, 235, 36)
        ]
        for nx, ny, r in nodules:
            # Raised inflamed outer halo (erythema)
            draw.ellipse([nx - r, ny - r, nx + r, ny + r], fill=(158, 88, 62), outline=(120, 55, 38), width=3)
            # Central depressed necrotic scab core
            draw.ellipse([nx - int(r*0.45), ny - int(r*0.45), nx + int(r*0.45), ny + int(r*0.45)], fill=(65, 30, 22))

    elif leaf_type == "animal_mange":
        # Animal hide with crusted scabs and alopecia
        img = Image.new("RGB", (width, height), (210, 170, 140))
        draw = ImageDraw.Draw(img)
        # Hairless wrinkled epidermal folds
        for y in range(40, 280, 22):
            draw.arc([40, y, 280, y + 30], start=10, end=170, fill=(130, 95, 75), width=3)
        # Severe grey-brown crusts and scabs
        crusts = [(100, 100), (160, 130), (220, 90), (130, 190), (200, 210), (90, 230)]
        for cx, cy in crusts:
            draw.ellipse([cx - 30, cy - 20, cx + 30, cy + 20], fill=(105, 80, 65), outline=(70, 50, 40), width=2)
            draw.ellipse([cx - 15, cy - 10, cx + 15, cy + 10], fill=(140, 115, 95))

    elif leaf_type == "arecanut_koleroga":
        # Arecanut green fruit with water-soaked rot at base
        img = Image.new("RGB", (width, height), (230, 240, 230))
        draw = ImageDraw.Draw(img)
        # Cluster of oval arecanuts
        nuts = [(120, 140), (180, 130), (150, 200), (210, 190)]
        for nx, ny in nuts:
            draw.ellipse([nx - 35, ny - 45, nx + 35, ny + 45], fill=(56, 142, 60), outline=(27, 94, 32), width=3)
            # Water-soaked dark rotting base near calyx
            draw.ellipse([nx - 30, ny - 40, nx + 30, ny - 10], fill=(44, 28, 20), outline=(78, 52, 40), width=2)
            # White fungal mycelium ring
            draw.arc([nx - 28, ny - 38, nx + 28, ny - 12], start=0, end=180, fill=(240, 245, 240), width=3)

    elif leaf_type == "ragi_blast":
        # Narrow finger millet leaf blade with spindle blast spots
        img = Image.new("RGB", (width, height), (240, 245, 240))
        draw = ImageDraw.Draw(img)
        draw.polygon([(135, 20), (185, 20), (215, 300), (105, 300)], fill=(76, 175, 80), outline=(46, 125, 50), width=3)
        draw.line([160, 20, 160, 300], fill=(27, 94, 32), width=3)
        # Spindle shaped eye-spots with ash grey centers and dark brown margins
        spindles = [(140, 80), (180, 120), (150, 170), (175, 220), (135, 250)]
        for sx, sy in spindles:
            draw.ellipse([sx - 18, sy - 8, sx + 18, sy + 8], fill=(245, 222, 179), outline=(90, 40, 20), width=2)
            draw.ellipse([sx - 10, sy - 4, sx + 10, sy + 4], fill=(160, 160, 160))

    else:
        # Perfectly healthy lush green leaf
        draw.ellipse([70, 45, 250, 275], fill=(56, 142, 60), outline=(27, 94, 32), width=3)
        draw.line([160, 45, 160, 275], fill=(139, 195, 74), width=3)
        for y in range(70, 250, 25):
            draw.line([160, y, 100, y - 22], fill=(139, 195, 74), width=2)
            draw.line([160, y, 220, y - 22], fill=(139, 195, 74), width=2)

    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=90)
    b64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{b64_str}"

SAMPLE_GALLERY = [
    {
        "id": "sample-1",
        "title": "Tomato Late Blight",
        "crop": "Tomato",
        "domain": "Plant Leaf",
        "expected_disease": "Late Blight (Phytophthora infestans)",
        "expected_severity": "Severe",
        "thumbnail_color": "#b71c1c",
        "image_data": create_sample_leaf_image("tomato_late_blight"),
        "description": "Large water-soaked necrotic patches with pale fungal downy halos on leaflets."
    },
    {
        "id": "sample-2",
        "title": "Potato Early Blight",
        "crop": "Potato",
        "domain": "Plant Leaf",
        "expected_disease": "Early Blight (Alternaria solani)",
        "expected_severity": "Moderate",
        "thumbnail_color": "#e65100",
        "image_data": create_sample_leaf_image("potato_early_blight"),
        "description": "Concentric dark 'target board' rings with chlorotic yellow surrounding margins."
    },
    {
        "id": "sample-3",
        "title": "Rice Bacterial Blight",
        "crop": "Rice",
        "domain": "Plant Leaf",
        "expected_disease": "Bacterial Leaf Blight (Xanthomonas oryzae)",
        "expected_severity": "Severe",
        "thumbnail_color": "#f57f17",
        "image_data": create_sample_leaf_image("rice_bacterial_blight"),
        "description": "Wavy straw-yellow margins starting from leaf tips and drying downwards."
    },
    {
        "id": "sample-4",
        "title": "Corn Common Rust",
        "crop": "Corn",
        "domain": "Plant Leaf",
        "expected_disease": "Corn Common Rust (Puccinia sorghi)",
        "expected_severity": "Moderate",
        "thumbnail_color": "#bf360c",
        "image_data": create_sample_leaf_image("corn_rust"),
        "description": "Cinnamon-brown powdery pustules erupting across the leaf surface."
    },
    {
        "id": "sample-5",
        "title": "Bovine Lumpy Skin Disease",
        "crop": "Cattle (Cow)",
        "domain": "Livestock / Animal",
        "expected_disease": "Bovine Lumpy Skin Disease (Capripoxvirus)",
        "expected_severity": "Severe",
        "thumbnail_color": "#881337",
        "image_data": create_sample_leaf_image("bovine_lumpy_skin"),
        "description": "Animal disease test: Firm raised nodular cutaneous lesions on cattle hide with veterinary advisory."
    },
    {
        "id": "sample-6",
        "title": "Livestock Mange / Scabies",
        "crop": "Livestock (Animal)",
        "domain": "Livestock / Animal",
        "expected_disease": "Sarcoptic Mange / Mite Infestation",
        "expected_severity": "Moderate",
        "thumbnail_color": "#78350f",
        "image_data": create_sample_leaf_image("animal_mange"),
        "description": "Animal disease test: Crusted hyperkeratotic skin with alopecia on animal hide."
    },
    {
        "id": "sample-7",
        "title": "Arecanut Koleroga",
        "crop": "Arecanut (ಅಡಿಕೆ)",
        "domain": "Plant Fruit",
        "expected_disease": "Arecanut Fruit Rot / Koleroga (Phytophthora meadii)",
        "expected_severity": "Severe",
        "thumbnail_color": "#15803d",
        "image_data": create_sample_leaf_image("arecanut_koleroga"),
        "description": "Karnataka staple crop: Water-soaked rotting of arecanuts with white fungal mycelium."
    },
    {
        "id": "sample-8",
        "title": "Ragi Blast",
        "crop": "Ragi (ರಾಗಿ)",
        "domain": "Plant Leaf",
        "expected_disease": "Finger Millet / Ragi Blast (Pyricularia grisea)",
        "expected_severity": "Severe",
        "thumbnail_color": "#a16207",
        "image_data": create_sample_leaf_image("ragi_blast"),
        "description": "Karnataka staple grain: Spindle-shaped blast lesions on finger millet leaf blade."
    },
    {
        "id": "sample-9",
        "title": "Healthy Crop Leaf",
        "crop": "Healthy",
        "domain": "Plant Leaf",
        "expected_disease": "Healthy Plant Leaf - No Pathogen Detected",
        "expected_severity": "Low",
        "thumbnail_color": "#1b5e20",
        "image_data": create_sample_leaf_image("healthy"),
        "description": "Lush uniform chlorophyll pigmentation with zero necrotic spots or fungal mycelium."
    }
]
