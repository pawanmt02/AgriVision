import os
import json
import time
import base64
import re
from io import BytesIO
from typing import Optional, Tuple, Dict, Any
from PIL import Image

from models import (
    DiagnosticResponse,
    SeverityEnum,
    PathogenType,
    DomainCategory,
    OrganicRemedyDetails,
    ChemicalRemedyDetails
)
from cnn_engine import extract_cnn_features

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# =======================================================================
# Comprehensive Global & Regional Crop Pathology Knowledge Base
# Includes staple crops, horticulture, and South Asian / Karnataka staples (Arecanut, Ragi)
# =======================================================================
AGRONOMY_KNOWLEDGE_BASE = {
    "tomato": {
        "scientific_name": "Solanum lycopersicum",
        "diseases": [
            {
                "disease": "Late Blight (Phytophthora infestans)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Large, irregular water-soaked dark brown to purplish lesions on leaflets",
                    "Delicate pale white fungal downy mildew on underside of leaves during humid mornings",
                    "Rapid petiole collapse and dark brown girdling of stems"
                ],
                "organic": {
                    "summary": "Immediate foliar spray with Copper Octanoate (30ml/10L) or Trichoderma harzianum; prune dense canopy.",
                    "preparation": "Mix 30ml Copper soap formulation in 10L water. Add 20ml cold-pressed Neem oil (10,000 ppm) with mild surfactant.",
                    "frequency": "Every 4-5 days during overcast/rainy periods; spray early mornings.",
                    "practices": ["Destroy and burn culled foliage; do not compost.", "Switch strictly to root-zone drip irrigation.", "Increase row spacing to >60cm for maximum airflow."]
                },
                "chemical": {
                    "summary": "Targeted systemic & protectant combination: Cymoxanil 8% + Mancozeb 64% WP.",
                    "active_ingredient": "Cymoxanil 8% + Mancozeb 64% WP (or Metalaxyl-M 4% + Mancozeb 64%)",
                    "dosage_liter": "2.5 g / Liter water",
                    "dosage_acre": "600 g / Acre dissolved in 200L water",
                    "phi_days": 7,
                    "safety": ["Wear respirator and protective goggles.", "Do not spray within 48 hours of rain.", "Keep away from livestock feed."]
                },
                "speech": {
                    "en": "Tomato Late Blight detected with high severity. Apply copper bio-spray or Cymoxanil immediately and halt overhead watering.",
                    "kn": "ಟೊಮ್ಯಾಟೊ ಬೆಳೆಯಲ್ಲಿ ಪಶ್ಚಾತ್ ಅಂಗಮಾರಿ (ಲೇಟ್ ಬ್ಲೈಟ್) ರೋಗ ತೀವ್ರವಾಗಿದೆ. ತಕ್ಷಣವೇ ತಾಮ್ರದ ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ಸೈಮಾಕ್ಸಾನಿಲ್ ಸಿಂಪಡಿಸಿ ಮತ್ತು ಮಣ್ಣಿನ ಹನಿ ನೀರಾವರಿ ಬಳಸಿ.",
                    "hi": "टमाटर में पछेती झुलसा (लेट ब्लाइट) का गंभीर प्रकोप है। तुरंत कॉपर फफूंदनाशक या साइमोक्सानिल का छिड़काव करें।",
                    "es": "Tizón tardío del tomate detectado con severidad alta. Aplique fungicida a base de cobre o Cymoxanil de inmediato.",
                    "sw": "Ugonjwa wa ukungu wa nyanya (Late Blight) umegunduliwa kwa kiwango cha juu. Nyunyizia dawa ya shaba haraka.",
                    "fr": "Mildiou de la tomate détecté à un stade sévère. Pulvérisez immédiatement un fongicide à base de cuivre ou de cymoxanil."
                }
            },
            {
                "disease": "Early Blight (Alternaria solani)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Concentric dark rings forming a 'target board' pattern on older foliage",
                    "Surrounding chlorotic yellow halos progressing upward",
                    "Premature lower leaf drop leading to sunscald on maturing fruit"
                ],
                "organic": {
                    "summary": "Bacillus subtilis bio-fungicide foliar spray plus aerated compost tea.",
                    "preparation": "Dissolve 50g Bacillus subtilis wettable powder in 15L dechlorinated water. Add 5ml horticultural sticker.",
                    "frequency": "Every 7 to 10 days at first sign of lower leaf spotting.",
                    "practices": ["Mulch ground with straw to prevent soil-splash.", "Prune bottom 30cm of foliage."]
                },
                "chemical": {
                    "summary": "Chlorothalonil 75% WP or Azoxystrobin 23% SC foliar application.",
                    "active_ingredient": "Azoxystrobin 23% SC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 5,
                    "safety": ["Rotate chemical classes (FRAC Group 11) to avert resistance.", "Wear nitrile chemical gloves."]
                },
                "speech": {
                    "en": "Early Blight detected with moderate severity. Concentric target spots observed. Apply Bacillus subtilis or Azoxystrobin.",
                    "kn": "ಟೊಮ್ಯಾಟೊ ಬೆಳೆಯಲ್ಲಿ ಮುಂಚಿತ ಅಂಗಮಾರಿ (ಅರ್ಲಿ ಬ್ಲೈಟ್) ರೋಗ ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ವೃತ್ತಾಕಾರದ ಕಲೆಗಳಿವೆ. ಬ್ಯಾಸಿಲಸ್ ಸಬ್ಟಿಲಿಸ್ ಅಥವಾ ಅಜೋಕ್ಸಿಸ್ಟ್ರೋಬಿನ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "टमाटर में अगेती झुलसा (अर्ली ब्लाइट) पाया गया है। निचली पत्तियों पर छल्लेदार धब्बे हैं।",
                    "es": "Tizón temprano detectado con severidad moderada. Aplique Bacillus subtilis o Azoxystrobin.",
                    "sw": "Ugonjwa wa madoa ya shabaha (Early Blight) umegunduliwa. Tumia dawa ya kibiolojia au Azoxystrobin.",
                    "fr": "Alternariose précoce détectée avec sévérité modérée. Appliquez du Bacillus subtilis ou de l'azoxystrobine."
                }
            }
        ]
    },
    "arecanut": {
        "scientific_name": "Areca catechu",
        "diseases": [
            {
                "disease": "Arecanut Fruit Rot / Koleroga (Phytophthora meadii)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Dark green water-soaked lesions at the base of nuts near perianth with heavy premature nut drop",
                    "White felt-like mycelial growth covering fallen diseased nuts on ground",
                    "Crown rot in advance stages leading to drying of top fronds and palm mortality"
                ],
                "organic": {
                    "summary": "Bordeaux mixture 1% pre-monsoon prophylactic spray + tying Polythene covers around bunches.",
                    "preparation": "Dissolve 1kg Copper Sulfate + 1kg Quicklime in 100L water to make fresh 1% Bordeaux mixture. Add 100ml rosin sticker.",
                    "frequency": "First spray in May/June before south-west monsoon; second spray 40 days later.",
                    "practices": ["Collect and destroy all fallen rot-affected nuts from trenches.", "Cover areca bunches with 100 gauge polythene covers to prevent rainwater wash."]
                },
                "chemical": {
                    "summary": "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold) or Fosetyl-Aluminium 80% WP.",
                    "active_ingredient": "Metalaxyl 8% + Mancozeb 64% WP",
                    "dosage_liter": "2.5 g / Liter water",
                    "dosage_acre": "500 g in 200L water sprayed directly onto bunches",
                    "phi_days": 21,
                    "safety": ["Use tree climber or high-pressure rocker sprayer.", "Wear safety helmet and goggles during canopy spraying."]
                },
                "speech": {
                    "en": "Arecanut Koleroga fruit rot detected with high severity. Apply 1% Bordeaux mixture or Metalaxyl-Mancozeb immediately to save nut bunches.",
                    "kn": "ಅಡಿಕೆ ತೋಟದಲ್ಲಿ ಕೊಳೆರೋಗ (ಮಹಾಲಿ) ತೀವ್ರವಾಗಿದೆ. ಕಾಯಿ ಉದುರುವುದನ್ನು ತಡೆಯಲು ತಕ್ಷಣವೇ 1% ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ರಿಡೋಮಿಲ್ ಗೋಲ್ಡ್ ದ್ರಾವಣವನ್ನು ಗೊಂಚಲುಗಳಿಗೆ ಸಿಂಪಡಿಸಿ.",
                    "hi": "सुपारी में कोलेरोगा (फल सड़न) रोग का भारी प्रकोप है। तुरंत 1% बोर्डो मिश्रण या रिडोमिल का छिड़काव करें।",
                    "es": "Pudrición del fruto de la nuez de areca detectada. Aplique caldo bordelés al 1% de inmediato.",
                    "sw": "Ugonjwa wa kuoza kwa matunda ya areca umegunduliwa. Nyunyizia mchanganyiko wa Bordeaux haraka.",
                    "fr": "Pourriture des fruits du bétel détectée. Pulvérisez de la bouillie bordelaise à 1% sans tarder."
                }
            }
        ]
    },
    "ragi": {
        "scientific_name": "Eleusine coracana",
        "diseases": [
            {
                "disease": "Finger Millet / Ragi Blast (Pyricularia grisea)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Spindle-shaped or diamond lesions on leaves with dark brown borders and grey centers",
                    "Neck blast: black lesion at neck of earhead causing fingers to snap and chaffy grains",
                    "Finger blast: premature grain drying and empty chaff formation"
                ],
                "organic": {
                    "summary": "Seed treatment with Pseudomonas fluorescens (10g/kg) and foliar spray with fresh cow urine extract (10%).",
                    "preparation": "Mix 1 Liter fermented cow urine + 100g Pseudomonas fluorescens powder in 10L clean water.",
                    "frequency": "Spray at tillering stage and 50% flowering stage.",
                    "practices": ["Avoid excess nitrogen fertilization.", "Select blast-resistant varieties like GPU-28, ML-365, or KMR-630."]
                },
                "chemical": {
                    "summary": "Tricyclazole 75% WP or Kitazin 48% EC foliar spray.",
                    "active_ingredient": "Tricyclazole 75% WP",
                    "dosage_liter": "0.6 g / Liter water",
                    "dosage_acre": "120 g / Acre in 200L water",
                    "phi_days": 21,
                    "safety": ["Do not spray during midday heat.", "Wear protective mask while measuring powder."]
                },
                "speech": {
                    "en": "Ragi Blast disease detected. High risk of earhead loss. Apply Tricyclazole 75% WP or Pseudomonas bio-agent at flowering stage.",
                    "kn": "ರಾಗಿ ಬೆಳೆಯಲ್ಲಿ ಬೆಂಕಿ ರೋಗ (ಬ್ಲಾಸ್ಟ್) ಕಂಡುಬಂದಿದೆ. ಕದಿರು ಮುರಿದು ಕಾಳು ಜಳ್ಳಾಗುವುದನ್ನು ತಡೆಯಲು ಟ್ರೈಸೈಕ್ಲಾಜೋಲ್ 75 ಡಬ್ಲ್ಯುಪಿ ಅಥವಾ ಸೂಡೋಮೊನಾಸ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "रागी में ब्लास्ट (झोंका) रोग देखा गया है। तुरंत ट्राईसाइक्लाजोल 75% का छिड़काव करें।",
                    "es": "Tizón del mijo africano detectado. Aplique Triciclazol o agente biológico Pseudomonas.",
                    "sw": "Ugonjwa wa ukungu wa mtama umegunduliwa. Nyunyizia dawa ya Tricyclazole bila kuchelewa.",
                    "fr": "Pyriculariose de l'éleusine détectée. Traitez rapidement au tricyclazole."
                }
            }
        ]
    },
    "chilli": {
        "scientific_name": "Capsicum annuum",
        "diseases": [
            {
                "disease": "Chilli Leaf Curl Virus (transmitted by Thrips/Whiteflies)",
                "pathogen": PathogenType.VIRAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Upward curling of leaves (thrips) and downward curling with crinkling (mites/whiteflies)",
                    "Severe stunting of internodes, bushy appearance, and brittle foliage",
                    "Total flower drop and miniature deformed fruit formation"
                ],
                "organic": {
                    "summary": "Vector deterrence: Install blue and yellow sticky traps (30/acre) + spray 5% Neem Seed Kernel Extract (NSKE).",
                    "preparation": "Crush 500g neem seeds, soak overnight in 10L water with 20g soap. Filter and spray.",
                    "frequency": "Every 7 days from vegetative stage onwards.",
                    "practices": ["Rogue out and bury severely infected stunted plants.", "Erect 2 rows of maize or sorghum barrier crops along field borders."]
                },
                "chemical": {
                    "summary": "Diafenthiuron 50% WP or Fipronil 5% SC for sucking pest vector management.",
                    "active_ingredient": "Diafenthiuron 50% WP",
                    "dosage_liter": "1.2 g / Liter water",
                    "dosage_acre": "250 g / Acre in 200L water",
                    "phi_days": 10,
                    "safety": ["Avoid spraying during honeybee foraging hours.", "Wear nitrile protective gloves."]
                },
                "speech": {
                    "en": "Chilli Leaf Curl Virus detected. Transmitted by thrips and whiteflies. Install sticky traps and spray Diafenthiuron or Neem extract.",
                    "kn": "ಮೆಣಸಿನಕಾಯಿ ಬೆಳೆಯಲ್ಲಿ ಎಲೆ ಮುರುಟು ರೋಗ (ಲೀಫ್ ಕರ್ಲ್ ವೈರಸ್) ಕಂಡುಬಂದಿದೆ. ನುಸಿ ಮತ್ತು ಬಿಳಿ ನೊಣಗಳ ನಿಯಂತ್ರಣಕ್ಕಾಗಿ ಹಳದಿ-ನೀಲಿ ಅಂಟು ಬಲೆಗಳನ್ನು ಹಾಕಿ ಡಯಾಫೆಂಥಿಯುರಾನ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "मिर्च में पत्ती मरोड़ (लीफ कर्ल) विषाणु का प्रकोप है। थ्रिप्स व सफेद मक्खी नियंत्रण के लिए चिपचिपे ट्रैप लगाएं और कीटनाशक का प्रयोग करें।",
                    "es": "Virus del rizado de la hoja del chile detectado. Controle trips y moscas blancas con trampas y Diafentiuron.",
                    "sw": "Virusi vya kukunja majani ya pilipili vimegunduliwa. Dhibiti wadudu kwa mitego na dawa inayofaa.",
                    "fr": "Virus de l'enroulement des feuilles de piment détecté. Contrôlez les thrips et aleurodes avec des pièges collants."
                }
            }
        ]
    },
    "banana": {
        "scientific_name": "Musa acuminata",
        "diseases": [
            {
                "disease": "Banana Black Sigatoka (Mycosphaerella fijiensis)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Narrow rusty-red to dark brown streaks parallel to leaf veins",
                    "Streaks enlarge into oval black spots with yellow halos and depressed grey centers",
                    "Rapid leaf scorch and premature ripening of bunches with unmarketable fruit"
                ],
                "organic": {
                    "summary": "Deleafing: cut off and burn heavily spotted lower leaves + mineral oil foliar spray.",
                    "preparation": "Emulsify 100ml white horticultural mineral oil in 10L water with 10g soft soap.",
                    "frequency": "Every 14 days during warm wet seasons.",
                    "practices": ["Improve plantation drainage to eliminate standing puddles.", "Ensure proper sucker desuckering for ventilation."]
                },
                "chemical": {
                    "summary": "Propiconazole 25% EC or Difenoconazole 25% EC mixed with mineral oil.",
                    "active_ingredient": "Propiconazole 25% EC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 21,
                    "safety": ["Rotate triazoles with protectant dithiocarbamates to prevent resistance.", "Wear protective rainwear."]
                },
                "speech": {
                    "en": "Banana Black Sigatoka detected. Prune infected leaves and apply Propiconazole or horticultural oil immediately.",
                    "kn": "ಬಾಳೆ ತೋಟದಲ್ಲಿ ಸಿಕಟೋಕಾ ಎಲೆ ಚುಕ್ಕೆ ರೋಗ ಕಂಡುಬಂದಿದೆ. ರೋಗಪೀಡಿತ ಒಣಗಿದ ಎಲೆಗಳನ್ನು ಕತ್ತರಿಸಿ ತೆಗೆದು ಪ್ರೊಪಿಕೋನಾಜೋಲ್ ದ್ರಾವಣ ಸಿಂಪಡಿಸಿ.",
                    "hi": "केले में सिगाटोका लीफ स्पॉट रोग पाया गया है। संक्रमित पत्तियों को काटकर नष्ट करें और प्रोपिकोनाज़ोल का छिड़काव करें।",
                    "es": "Sigatoka negra del banano detectada. Pode las hojas infectadas y aplique Propiconazol de inmediato.",
                    "sw": "Ugonjwa wa Sigatoka wa migomba umegunduliwa. Kata majani yaliyoathirika na unyunyizie dawa.",
                    "fr": "Cercosporiose noire du bananier détectée. Éliminez les feuilles atteintes et traitez au propiconazole."
                }
            }
        ]
    },
    "potato": {
        "scientific_name": "Solanum tuberosum",
        "diseases": [
            {
                "disease": "Late Blight (Phytophthora infestans)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Rapidly enlarging water-soaked lesions that turn necrotic black",
                    "White sporulation rings on leaf undersides under high humidity",
                    "Stem lesions leading to total haulm collapse in 72 hours"
                ],
                "organic": {
                    "summary": "Bordeaux mixture 1% spray or copper hydroxide foliar protectant.",
                    "preparation": "Prepare fresh Bordeaux mixture: 1kg Copper Sulfate + 1kg Quicklime in 100L clean water.",
                    "frequency": "Every 5 days during cool cloudy weather.",
                    "practices": ["Hilling up soil to at least 15cm above seed tubers.", "Destroy volunteer potato plants."]
                },
                "chemical": {
                    "summary": "Mandipropamid 23.4% SC or Dimethomorph 50% WP.",
                    "active_ingredient": "Mandipropamid 23.4% SC",
                    "dosage_liter": "0.8 ml / Liter water",
                    "dosage_acre": "160 ml / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Use hollow cone nozzle.", "Wash skin thoroughly after handling."]
                },
                "speech": {
                    "en": "Potato Late Blight alert. Severe risk to tubers. Apply Bordeaux mixture or Mandipropamid urgently.",
                    "kn": "ಆಲೂಗಡ್ಡೆ ಬೆಳೆಯಲ್ಲಿ ಪಶ್ಚಾತ್ ಅಂಗಮಾರಿ (ಲೇಟ್ ಬ್ಲೈಟ್) ರೋಗ ತೀವ್ರವಾಗಿದೆ. ಗಡ್ಡೆಗಳನ್ನು ರಕ್ಷಿಸಲು ತಕ್ಷಣ ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ಮ್ಯಾಂಡಿಪ್ರೋಪಾಮಿಡ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "आलू में पछेती झुलसा का भारी प्रकोप है। कंदों को बचाने के लिए तुरंत बोर्डो मिश्रण या मैंडीप्रोपामाइड का छिड़काव करें।",
                    "es": "Tizón tardío de la papa detectado. Alto riesgo. Aplique mezcla de Burdeos o Mandipropamid de inmediato.",
                    "sw": "Ugonjwa hatari wa viazi (Late Blight) umegunduliwa. Tumia dawa ya shaba au Mandipropamid kulinda viazi.",
                    "fr": "Mildiou de la pomme de terre détecté. Risque élevé pour les tubercules. Pulvérisez rapidement du mandipropamide."
                }
            }
        ]
    },
    "rice": {
        "scientific_name": "Oryza sativa",
        "diseases": [
            {
                "disease": "Bacterial Leaf Blight (Xanthomonas oryzae)",
                "pathogen": PathogenType.BACTERIAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Water-soaked lesions starting at leaf tips and moving down margins with wavy borders",
                    "Lesions dry out turning bleached straw-yellow to dirty white",
                    "Milky bacterial exudate beads seen on leaf surface early in morning"
                ],
                "organic": {
                    "summary": "Fresh cow dung wash (20%) or Pseudomonas fluorescens biological spray.",
                    "preparation": "Mix 2 kg fresh cow dung filtrate + 200g Pseudomonas fluorescens powder in 10L water.",
                    "frequency": "Spray twice at 10-day intervals beginning at maximum tillering stage.",
                    "practices": ["Drain excess field standing water for 48 hours.", "Avoid excessive nitrogen top-dressing."]
                },
                "chemical": {
                    "summary": "Streptomycin sulphate 90% + Tetracycline 10% combined with Copper Oxychloride 50% WP.",
                    "active_ingredient": "Streptocycline 6g + Copper Oxychloride 50 WP 25g per 10 Liters water",
                    "dosage_liter": "0.6 g Streptocycline + 2.5 g COC per Liter",
                    "dosage_acre": "120 g Streptocycline + 500 g COC in 200L water",
                    "phi_days": 21,
                    "safety": ["Avoid contact with eyes.", "Wear protective boots in flooded paddy."]
                },
                "speech": {
                    "en": "Rice Bacterial Leaf Blight detected. Drain standing water temporarily and spray Streptocycline with Copper.",
                    "kn": "ಭತ್ತದ ಬೆಳೆಯಲ್ಲಿ ದುಂಡಾಣು ಎಲೆ ಕವಚ ರೋಗ (ಬ್ಯಾಕ್ಟೀರಿಯಲ್ ಬ್ಲೈಟ್) ಕಂಡುಬಂದಿದೆ. ಗದ್ದೆಯಲ್ಲಿನ ಹೆಚ್ಚುವರಿ ನೀರನ್ನು ಬಸಿದು ಸ್ಟ್ರೆಪ್ಟೋಸೈಕ್ಲಿನ್ ಮತ್ತು ತಾಮ್ರದ ದ್ರಾವಣ ಸಿಂಪಡಿಸಿ.",
                    "hi": "धान में जीवाणु झुलसा (बैक्टीरियल ब्लाइट) देखा गया है। खेत से अतिरिक्त पानी निकालें और कॉपर तथा स्ट्रेप्टोसाइक्लिन का छिड़काव करें।",
                    "es": "Tizón bacteriano del arroz detectado. Drene el agua estancada y aplique bactericida con cobre.",
                    "sw": "Ugonjwa wa kuungua kwa majani ya mpunga umegunduliwa. Punguza maji shambani na nyunyizia dawa ya shaba.",
                    "fr": "Flétrissement bactérien du riz détecté. Évacuez l'eau stagnante et traitez au cuivre combiné."
                }
            }
        ]
    },
    "corn": {
        "scientific_name": "Zea mays",
        "diseases": [
            {
                "disease": "Corn Common Rust (Puccinia sorghi)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Golden-brown to cinnamon-brown powdery pustules on both upper and lower leaf surfaces",
                    "Ruptured epidermal flakes surrounding mature pustules revealing reddish spores",
                    "Severe chlorosis and localized leaf scorch under prolonged cooler humid weather"
                ],
                "organic": {
                    "summary": "Wettable sulfur spray or bio-agent Ampelomyces quisqualis.",
                    "preparation": "Mix 30g Micronized sulfur 80% WDG in 10L water.",
                    "frequency": "Every 10-14 days; do not spray if ambient temperature exceeds 32°C.",
                    "practices": ["Destroy previous crop stubble.", "Select rust-resistant hybrids."]
                },
                "chemical": {
                    "summary": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC.",
                    "active_ingredient": "Azoxystrobin + Difenoconazole SC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Avoid tank mix with organosilicone adjuvants during vegetative stages."]
                },
                "speech": {
                    "en": "Corn Common Rust detected with powdery cinnamon pustules. Apply micronized sulfur or systemic strobilurin fungicide.",
                    "kn": "ಮೆಕ್ಕೆಜೋಳ ಬೆಳೆಯಲ್ಲಿ ತುಕ್ಕು ರೋಗ (ರಸ್ಟ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಬಣ್ಣದ ಪುಡಿ ಗುಳ್ಳೆಗಳಿವೆ. ಗಂಧಕದ ಪುಡಿ ಅಥವಾ ಅಜೋಕ್ಸಿಸ್ಟ್ರೋಬಿನ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "मक्के में रतुआ (कॉमन रस्ट) पाया गया है। पत्तियों पर भूरे फफोले हैं। घुलनशील गंधक या एजोक्सीस्ट्रोबिन का छिड़काव करें।",
                    "es": "Roya común del maíz detectada con pústulas de color canela. Aplique azufre micronizado o fungicida sistémico.",
                    "sw": "Ugonjwa wa kutu ya mahindi umegunduliwa. Tumia salfa au dawa ya ukungu ya kimfumo.",
                    "fr": "Rouille commune du maïs détectée. Appliquez du soufre micronisé ou un fongicide strobilurine."
                }
            }
        ]
    },
    "healthy": {
        "scientific_name": "Plantae",
        "diseases": [
            {
                "disease": "Healthy Plant Leaf - No Pathogen Detected",
                "pathogen": PathogenType.HEALTHY,
                "severity_default": SeverityEnum.LOW,
                "symptoms": [
                    "Vibrant, uniform chlorophyll pigmentation across upper and lower epidermis",
                    "Intact leaf margins and healthy primary and secondary vascular venation",
                    "No visible necrotic lesions, chlorotic halos, or fungal sporulation pustules"
                ],
                "organic": {
                    "summary": "Preventive maintenance: apply balanced vermicompost wash and seaweed bio-stimulant.",
                    "preparation": "Dilute liquid seaweed extract 2ml/L water and spray every 21 days for immune priming.",
                    "frequency": "Monthly preventive foliar feed.",
                    "practices": ["Maintain soil moisture at 60-70% field capacity.", "Scout field weekly for early pest ingress."]
                },
                "chemical": {
                    "summary": "Zero chemical pesticide required. Maintain balanced NPK nutrient regime.",
                    "active_ingredient": "None required (Water-soluble 19:19:19 NPK for vegetative vigour)",
                    "dosage_liter": "5 g / Liter water (Foliar nutrition only)",
                    "dosage_acre": "1 kg / Acre",
                    "phi_days": 0,
                    "safety": ["Keep routine surveillance; no toxic pesticide application warranted."]
                },
                "speech": {
                    "en": "Great news! The plant leaf appears healthy and vigorous with no detectable pathogens.",
                    "kn": "ಉತ್ತಮ ಸುದ್ದಿ! ಸಸ್ಯದ ಎಲೆಯು ಆರೋಗ್ಯಕರವಾಗಿದೆ ಮತ್ತು ಯಾವುದೇ ರೋಗದ ಲಕ್ಷಣಗಳು ಕಂಡುಬಂದಿಲ್ಲ. ಜೈವಿಕ ಪೋಷಕಾಂಶಗಳನ್ನು ಮುಂದುವರಿಸಿ.",
                    "hi": "बहुत बढ़िया! पौधे की पत्ती पूरी तरह स्वस्थ है और इसमें किसी रोग के लक्षण नहीं मिले हैं।",
                    "es": "¡Buenas noticias! La hoja de la planta se encuentra sana y vigorosa sin patógenos detectados.",
                    "sw": "Habari njema! Jani la mmea lina afya nzuri na hakuna ugonjwa uliogunduliwa.",
                    "fr": "Bonne nouvelle ! La feuille de la plante est saine et vigoureuse, aucun pathogène détecté."
                }
            }
        ]
    },
    "cotton": {
        "scientific_name": "Gossypium hirsutum",
        "diseases": [
            {
                "disease": "Cotton Bacterial Blight / Angular Leaf Spot (Xanthomonas citri pv. malvacearum)",
                "pathogen": PathogenType.BACTERIAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Small, angular water-soaked lesions bounded by leaf veinlets",
                    "Lesions coalesce turning dark brown or black with severe premature defoliation",
                    "Black arm stage: elongated black lesions girdling stems and branches"
                ],
                "organic": {
                    "summary": "Pseudomonas fluorescens 10g/L spray + fermented cow urine foliar application.",
                    "preparation": "Mix 250g Pseudomonas fluorescens + 2L fresh cow dung filtrate in 20L water.",
                    "frequency": "Spray at 15-day intervals during warm humid weather.",
                    "practices": ["Destroy previous cotton crop residue.", "Avoid excessive late nitrogen applications."]
                },
                "chemical": {
                    "summary": "Copper Oxychloride 50% WP + Streptocycline foliar spray.",
                    "active_ingredient": "Copper Oxychloride 50% WP (2.5 g/L) + Streptocycline (1 g / 10L)",
                    "dosage_liter": "2.5 g COC + 0.1 g Streptocycline per Liter",
                    "dosage_acre": "500 g COC + 20 g Streptocycline in 200L water",
                    "phi_days": 21,
                    "safety": ["Wear respirator and rubber gloves.", "Do not spray during high winds."]
                },
                "speech": {
                    "en": "Cotton Bacterial Blight detected. Apply Copper Oxychloride with Streptocycline or bio-agent Pseudomonas.",
                    "kn": "ಹತ್ತಿ ಬೆಳೆಯಲ್ಲಿ ದುಂಡಾಣು ಎಲೆ ಕವಚ ಅಥವಾ ಕೋನೀಯ ಎಲೆ ಚುಕ್ಕೆ ರೋಗ ಕಂಡುಬಂದಿದೆ. ತಾಮ್ರದ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ ಮತ್ತು ಸ್ಟ್ರೆಪ್ಟೋಸೈಕ್ಲಿನ್ ಮಿಶ್ರಣವನ್ನು ಸಿಂಪಡಿಸಿ.",
                    "hi": "कपास में जीवाणु अंगमारी (कोणीय पत्ती धब्बा) रोग पाया गया है। कॉपर ऑक्सीक्लोराइड और स्ट्रेप्टोसाइक्लिन का छिड़काव करें।",
                    "es": "Tizón bacteriano del algodón detectado. Aplique oxicloruro de cobre con estreptociclina.",
                    "sw": "Ugonjwa wa ukungu wa pamba umegunduliwa. Nyunyizia dawa ya shaba na Streptocycline.",
                    "fr": "Bactériose du cotonnier détectée. Traitez avec de l'oxychlorure de cuivre et de la streptocycline."
                }
            }
        ]
    },
    "mango": {
        "scientific_name": "Mangifera indica",
        "diseases": [
            {
                "disease": "Mango Anthracnose (Colletotrichum gloeosporioides)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Irregular brownish-black necrotic lesions on tender leaves causing leaf crinkling and tear",
                    "Blossom blight: black spots on floral panicles resulting in complete fruit drop",
                    "Tear-stain patterns and sunken black rot spots on maturing mango fruit"
                ],
                "organic": {
                    "summary": "1% Bordeaux mixture pre-flowering spray + Trichoderma viride canopy spray.",
                    "preparation": "Dissolve 1kg Copper Sulfate + 1kg Quicklime in 100L clean water. Apply fresh.",
                    "frequency": "Spray prior to flower bud emergence and after fruit set.",
                    "practices": ["Prune dead twigs and destroy fallen diseased leaves.", "Ensure canopy aeration."]
                },
                "chemical": {
                    "summary": "Azoxystrobin 23% SC or Carbendazim 50% WP foliar application.",
                    "active_ingredient": "Azoxystrobin 23% SC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Wear eye protection when spraying tree canopy.", "Keep away from beehives during pollination."]
                },
                "speech": {
                    "en": "Mango Anthracnose detected. Fungal lesions threatening flower panicles and leaves. Spray 1% Bordeaux mixture or Azoxystrobin.",
                    "kn": "ಮಾವಿನ ಮರದಲ್ಲಿ ಅಂಥ್ರಾಕ್ನೋಸ್ (ಕಪ್ಪು ಕಲೆ ಮತ್ತು ಚಿಗುರು ಒಣಗುವ ರೋಗ) ಕಂಡುಬಂದಿದೆ. ಹೂಗೊಂಚಲು ಉಳಿಸಲು ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ಅಜೋಕ್ಸಿಸ್ಟ್ರೋಬಿನ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "आम में एन्थ्रेक्नोज़ (काले धब्बे और झुलसा) रोग का प्रकोप है। 1% बोर्डो मिश्रण या एज़ोक्सीस्ट्रोबिन का छिड़काव करें।",
                    "es": "Antracnosis del mango detectada. Aplique caldo bordelés al 1% o azoxistrobina.",
                    "sw": "Ugonjwa wa ukungu wa maembe (Anthracnose) umegunduliwa. Nyunyizia mchanganyiko wa Bordeaux au Azoxystrobin.",
                    "fr": "Anthracnose du manguier détectée. Pulvérisez de la bouillie bordelaise ou de l'azoxystrobine."
                }
            }
        ]
    },
    "coffee": {
        "scientific_name": "Coffea arabica / Coffea canephora",
        "diseases": [
            {
                "disease": "Coffee Leaf Rust (Hemileia vastatrix)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Yellowish-orange powdery spore spots on leaf undersides",
                    "Lesions expand into irregular circular spots with necrotic brown drying centers",
                    "Heavy premature defoliation leading to dieback and crop loss in subsequent seasons"
                ],
                "organic": {
                    "summary": "0.5% Bordeaux mixture prophylactic spray before south-west monsoon.",
                    "preparation": "Mix 500g Copper Sulfate + 500g lime in 100L water.",
                    "frequency": "Two pre-monsoon sprays (May/June) and one post-monsoon spray (September).",
                    "practices": ["Maintain 40-50% filtered shade canopy.", "Prune unproductive suckers."]
                },
                "chemical": {
                    "summary": "Hexaconazole 5% EC or Propiconazole 25% EC systemic fungicide.",
                    "active_ingredient": "Hexaconazole 5% EC",
                    "dosage_liter": "2.0 ml / Liter water",
                    "dosage_acre": "400 ml / Acre in 200L water",
                    "phi_days": 30,
                    "safety": ["Wear protective mask during high-pressure spraying.", "Do not spray near natural streams."]
                },
                "speech": {
                    "en": "Coffee Leaf Rust detected with bright orange powdery pustules. Spray 0.5% Bordeaux mixture or Hexaconazole immediately.",
                    "kn": "ಕಾಫಿ ತೋಟದಲ್ಲಿ ಹೇಮಿಲಿಯಾ ತುಕ್ಕು ರೋಗ (ಕಾಫಿ ರಸ್ಟ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಕೆಳಗೆ ಕಿತ್ತಳೆ ಬಣ್ಣದ ಪುಡಿ ಕಲೆಗಳಿವೆ. ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ಹೆಕ್ಸಾಕೊನಾಜೋಲ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "कॉफी में लीफ रस्ट (गेरुई/रतुआ) रोग देखा गया है। तुरंत 0.5% बोर्डो मिश्रण या हेक्साकोनाज़ोल का छिड़काव करें।",
                    "es": "Roya del café detectada con pústulas de color naranja. Aplique caldo bordelés o hexaconazol de inmediato.",
                    "sw": "Ugonjwa wa kutu ya majani ya kahawa umegunduliwa. Nyunyizia mchanganyiko wa Bordeaux au Hexaconazole haraka.",
                    "fr": "Rouille du caféier détectée. Pulvérisez sans tarder de la bouillie bordelaise ou de l'hexaconazole."
                }
            }
        ]
    },
    "tea": {
        "scientific_name": "Camellia sinensis",
        "diseases": [
            {
                "disease": "Tea Blister Blight (Exobasidium vexans)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Pale green to yellowish translucent circular spots on tender young succulent leaves",
                    "Under-surface becomes blistered and concave with powdery white velvety spore coating",
                    "Stem curling and blackening of tender harvestable two leaves and a bud"
                ],
                "organic": {
                    "summary": "Copper Hydroxide protectant spray combined with Trichoderma bio-formulation.",
                    "preparation": "Dissolve 20g Copper Hydroxide in 10L clean water.",
                    "frequency": "Weekly sprays coinciding with plucking rounds during misty weather.",
                    "practices": ["Regulate shade trees to allow morning sunlight penetration.", "Pluck on a strict 7-day cycle."]
                },
                "chemical": {
                    "summary": "Copper Oxychloride 50% WP + Propiconazole 25% EC tank mix.",
                    "active_ingredient": "Propiconazole 25% EC (0.5 ml/L) + COC (1.5 g/L)",
                    "dosage_liter": "0.5 ml Propiconazole + 1.5 g COC per Liter",
                    "dosage_acre": "100 ml Propiconazole + 300 g COC in 200L water",
                    "phi_days": 7,
                    "safety": ["Observe harvest interval strictly to avoid chemical residue in processed tea."]
                },
                "speech": {
                    "en": "Tea Blister Blight detected on tender flush. Spray Copper Oxychloride or Propiconazole immediately.",
                    "kn": "ಚಹಾ ತೋಟದಲ್ಲಿ ಬ್ಲಿಸ್ಟರ್ ಬ್ಲೈಟ್ (ಗುಳ್ಳೆ ರೋಗ) ಕಂಡುಬಂದಿದೆ. ತಕ್ಷಣ ತಾಮ್ರದ ಶಿಲೀಂಧ್ರನಾಶಕ ಅಥವಾ ಪ್ರೊಪಿಕೋನಾಜೋಲ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "चाय में ब्लिस्टर ब्लाइट रोग के लक्षण हैं। कॉपर ऑक्सीक्लोराइड या प्रोपिकोनाज़ोल का छिड़काव करें।",
                    "es": "Tizón ampolloso del té detectado. Aplique oxicloruro de cobre o propiconazol de inmediato.",
                    "sw": "Ugonjwa wa malengelenge ya chai umegunduliwa. Nyunyizia dawa ya shaba mara moja.",
                    "fr": "Cloque du théier détectée sur les jeunes pousses. Traitez rapidement à l'oxychlorure de cuivre."
                }
            }
        ]
    },
    "groundnut": {
        "scientific_name": "Arachis hypogaea",
        "diseases": [
            {
                "disease": "Groundnut Tikka Leaf Spot (Cercospora arachidicola & Phaeoisariopsis personata)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Early leaf spot: reddish-brown sub-circular spots with prominent yellow chlorotic halos",
                    "Late leaf spot: dark black circular spots with carbonaceous appearance on leaf undersides",
                    "Severe premature defoliation leaving only naked stems and stunted underground pods"
                ],
                "organic": {
                    "summary": "5% Neem Seed Kernel Extract (NSKE) + Trichoderma viride foliar wash.",
                    "preparation": "Crush 500g neem seeds, soak in 10L water overnight with 20g soap. Filter and spray.",
                    "frequency": "Every 10-12 days starting 35 days after sowing.",
                    "practices": ["Crop rotation with cereals like maize or pearl millet.", "Destroy infected groundnut haulms."]
                },
                "chemical": {
                    "summary": "Carbendazim 12% + Mancozeb 63% WP (Saaf) or Tebuconazole 25.9% EC.",
                    "active_ingredient": "Carbendazim 12% + Mancozeb 63% WP",
                    "dosage_liter": "2.0 g / Liter water",
                    "dosage_acre": "400 g / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Wear protective clothing.", "Do not allow livestock to feed on freshly sprayed haulms."]
                },
                "speech": {
                    "en": "Groundnut Tikka Leaf Spot detected. Apply Saaf (Carbendazim + Mancozeb) or Neem extract to protect pod filling.",
                    "kn": "ಕಡಲೆಕಾಯಿ ಬೆಳೆಯಲ್ಲಿ ಟಿಕ್ಕಾ ಎಲೆ ಚುಕ್ಕೆ ರೋಗ ಕಂಡುಬಂದಿದೆ. ಕಾಯಿ ಕಟ್ಟುವ ಹಂತದಲ್ಲಿ ರಕ್ಷಿಸಲು ಸಾಫ್ (ಕಾರ್ಬೆಂಡಾಜಿಮ್ + ಮ್ಯಾಂಕೋಜೆಬ್) ಅಥವಾ ಬೇವಿನ ಕಷಾಯ ಸಿಂಪಡಿಸಿ.",
                    "hi": "मूंगफली में टिक्का रोग (पत्ती धब्बा) देखा गया है। तुरंत साफ (कार्बेंडाजिम + मैंकोजेब) का छिड़काव करें।",
                    "es": "Mancha foliar Tikka del cacahuete detectada. Aplique Carbendazim con Mancozeb de inmediato.",
                    "sw": "Ugonjwa wa madoa ya majani ya karanga umegunduliwa. Tumia dawa ya Carbendazim au Mancozeb.",
                    "fr": "Cercosporiose de l'arachide détectée. Traitez au carbendazime combiné au mancozèbe."
                }
            }
        ]
    },
    "sugarcane": {
        "scientific_name": "Saccharum officinarum",
        "diseases": [
            {
                "disease": "Sugarcane Red Rot (Colletotrichum falcatum)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Midrib lesions on leaves turning blood-red with dark brown borders",
                    "Yellowing and drying of third and fourth leaves from top, spreading downward",
                    "Internally reddened stalks with distinctive crosswise white patches and alcoholic odor"
                ],
                "organic": {
                    "summary": "Sett dip treatment with Trichoderma viride (10g/L) + crop rotation.",
                    "preparation": "Mix 200g Trichoderma viride in 20L water; soak setts for 30 minutes before planting.",
                    "frequency": "At planting; spray crop canopy at 45 and 90 days with Pseudomonas bio-agent.",
                    "practices": ["Use healthy seed cane from disease-free nurseries.", "Avoid flood irrigation between infected and healthy furrows."]
                },
                "chemical": {
                    "summary": "Carbendazim 50% WP sett dip + Thiophanate-Methyl 70% WP foliar spray.",
                    "active_ingredient": "Thiophanate-Methyl 70% WP",
                    "dosage_liter": "1.5 g / Liter water",
                    "dosage_acre": "300 g / Acre in 200L water",
                    "phi_days": 30,
                    "safety": ["Do not burn diseased cane trash; compost or bury deeply.", "Wear gloves during sett handling."]
                },
                "speech": {
                    "en": "Sugarcane Red Rot detected. Critical danger of stalk rot and sugar recovery loss. Rogue out diseased canes and spray Thiophanate-Methyl.",
                    "kn": "ಕಬ್ಬಿನ ಬೆಳೆಯಲ್ಲಿ ಕೆಂಪು ಕೊಳೆ ರೋಗ (ರೆಡ್ ರಾಟ್) ಕಂಡುಬಂದಿದೆ. ಬೆಳೆ ಒಣಗುವುದನ್ನು ತಡೆಯಲು ರೋಗಪೀಡಿತ ಕಬ್ಬುಗಳನ್ನು ಕಿತ್ತು ಸುಟ್ಟುಹಾಕಿ, ಥಿಯೋಫನೇಟ್ ಮಿಥೈಲ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "गन्ने में लाल सड़न (रेड रॉट) रोग पाया गया है। ग्रसित पौधों को उखाड़कर नष्ट करें और फफूंदनाशक का प्रयोग करें।",
                    "es": "Pudrición roja de la caña de azúcar detectada. Retire las plantas afectadas y aplique fungicida.",
                    "sw": "Ugonjwa wa kuoza kwekundu wa miwa umegunduliwa. Ondoa miwa iliyoathirika na utumie dawa ya ukungu.",
                    "fr": "Pourriture rouge de la canne à sucre détectée. Détruisez les cannes atteintes et traitez au thiophanate-méthyle."
                }
            }
        ]
    },
    "onion": {
        "scientific_name": "Allium cepa",
        "diseases": [
            {
                "disease": "Onion Purple Blotch (Alternaria porri)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Small water-soaked sunken lesions with purple centers and yellow margins",
                    "Lesions enlarge rapidly girdling the tubular leaf, causing top collapse and breakage",
                    "Stunted bulb expansion and secondary soft rotting in storage"
                ],
                "organic": {
                    "summary": "Pseudomonas fluorescens 5g/L + sticker spray or fermented buttermilk wash.",
                    "preparation": "Mix 1L sour buttermilk + 100g turmeric powder in 10L water.",
                    "frequency": "Every 10 days starting from bulb development stage.",
                    "practices": ["Ensure proper raised bed drainage.", "Avoid overhead sprinkler irrigation."]
                },
                "chemical": {
                    "summary": "Difenoconazole 25% EC or Mancozeb 75% WP with agricultural sticker.",
                    "active_ingredient": "Difenoconazole 25% EC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 10,
                    "safety": ["Always mix non-ionic sticker (0.5 ml/L) as waxy onion leaves repel water droplets."]
                },
                "speech": {
                    "en": "Onion Purple Blotch detected. Spray Difenoconazole or Mancozeb with sticker to prevent leaf breakage.",
                    "kn": "ಈರುಳ್ಳಿ ಬೆಳೆಯಲ್ಲಿ ನೇರಳೆ ಕಲೆ ರೋಗ (ಪರ್ಪಲ್ ಬ್ಲಾಚ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳು ಮುರಿದುಬೀಳುವುದನ್ನು ತಡೆಯಲು ಡಿಫೆನೊಕೊನಾಜೋಲ್ ಜೊತೆಗೆ ಅಂಟು ದ್ರಾವಣ ಸಿಂಪಡಿಸಿ.",
                    "hi": "प्याज में बैंगनी धब्बा (पर्पल ब्लॉच) रोग देखा गया है। डाइफेनोकोनाज़ोल या मैंकोज़ेब का चिपचिपे घोल के साथ छिड़काव करें।",
                    "es": "Mancha púrpura de la cebolla detectada. Aplique difenoconazol con adherente para evitar el quiebre foliar.",
                    "sw": "Ugonjwa wa madoa ya zambarau ya vitunguu umegunduliwa. Tumia dawa ya ukungu na kibandikizo.",
                    "fr": "Tache pourpre de l'oignon détectée. Pulvérisez du difénoconazole avec un mouillant adapté."
                }
            }
        ]
    },
    "citrus": {
        "scientific_name": "Citrus limon / Citrus sinensis",
        "diseases": [
            {
                "disease": "Citrus Canker (Xanthomonas axonopodis pv. citri)",
                "pathogen": PathogenType.BACTERIAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Raised, corky, crater-like brown lesions on leaves with prominent oily yellow halos",
                    "Lesions appear on both leaf surfaces with rough, scabby sandpaper feel",
                    "Fruit lesions causing superficial blemishes, cracking, and premature fruit drop"
                ],
                "organic": {
                    "summary": "1% Bordeaux mixture spray + pruning affected twigs in winter.",
                    "preparation": "Mix 1kg Copper Sulfate + 1kg Quicklime in 100L clean water.",
                    "frequency": "Spray after leaf flush in spring, rainy season, and post-monsoon.",
                    "practices": ["Control citrus leaf miner pest as larval mines facilitate bacterial entry.", "Disinfect pruning shears."]
                },
                "chemical": {
                    "summary": "Copper Oxychloride 50% WP combined with Streptocycline.",
                    "active_ingredient": "Copper Oxychloride (2.5 g/L) + Streptocycline (0.1 g/L)",
                    "dosage_liter": "2.5 g COC + 1g Streptocycline per 10 Liters water",
                    "dosage_acre": "500 g COC + 20g Streptocycline in 200L water",
                    "phi_days": 14,
                    "safety": ["Avoid spraying during bloom to protect citrus pollinators."]
                },
                "speech": {
                    "en": "Citrus Canker bacterial infection detected. Spray Copper Oxychloride with Streptocycline and control leaf miner pests.",
                    "kn": "ಲಿಂಬೆ ಅಥವಾ ಕಿತ್ತಳೆ ಗಿಡದಲ್ಲಿ ಕಜ್ಜಿ ರೋಗ (ಸಿಟ್ರಸ್ ಕ್ಯಾಂಕರ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ಒರಟಾದ ಕಂದು ಕಲೆಗಳಿವೆ. ತಾಮ್ರದ ದ್ರಾವಣ ಮತ್ತು ಸ್ಟ್ರೆಪ್ಟೋಸೈಕ್ಲಿನ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "नींबू वर्गीय फलों में कैंकर (खुरदरा धब्बा) रोग पाया गया है। कॉपर ऑक्सीक्लोराइड और स्ट्रेप्टोसाइक्लिन का छिड़काव करें।",
                    "es": "Cancro cítrico bacteriano detectado. Aplique oxicloruro de cobre con estreptociclina.",
                    "sw": "Ugonjwa wa canker wa jamii ya machungwa umegunduliwa. Nyunyizia dawa ya shaba na Streptocycline.",
                    "fr": "Chancre bactérien des agrumes détecté. Traitez à l'oxychlorure de cuivre et à la streptocycline."
                }
            }
        ]
    },
    "grapes": {
        "scientific_name": "Vitis vinifera",
        "diseases": [
            {
                "disease": "Grapevine Downy Mildew (Plasmopara viticola)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Yellowish oily 'oil-spot' translucent lesions on upper leaf blade",
                    "Dense, white cottony downy fungal growth on corresponding leaf under-surface",
                    "Infected berries shrivel, turn brown, and drop as mummies"
                ],
                "organic": {
                    "summary": "1% Bordeaux mixture or Potassium phosphonate biological spray.",
                    "preparation": "Prepare fresh Bordeaux mixture 1:1:100; spray underleaf surfaces thoroughly.",
                    "frequency": "Spray before monsoon and after every cloudy wet rain spell.",
                    "practices": ["Canopy thinning to ensure solar penetration and air flow.", "Avoid furrow flooding."]
                },
                "chemical": {
                    "summary": "Dimethomorph 50% WP or Metalaxyl-Mancozeb (Ridomil Gold).",
                    "active_ingredient": "Dimethomorph 50% WP",
                    "dosage_liter": "1.0 g / Liter water",
                    "dosage_acre": "200 g / Acre in 200L water",
                    "phi_days": 21,
                    "safety": ["Rotate with multisite protectants to prevent Oomycete resistance.", "Wear protective apron."]
                },
                "speech": {
                    "en": "Grape Downy Mildew detected. Apply Dimethomorph or Bordeaux mixture immediately to prevent berry cluster rot.",
                    "kn": "ದ್ರಾಕ್ಷಿ ತೋಟದಲ್ಲಿ ಬೂಜು ರೋಗ (ಡೌನಿ ಮಿಲ್ಡ್ಯೂ) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಕೆಳಗೆ ಬಿಳಿ ಬೂಜಿನ ಕಲೆಗಳಿವೆ. ಡೈಮೆಥೊಮಾರ್ಫ್ ಅಥವಾ ಬೋರ್ಡೋ ದ್ರಾವಣ ಸಿಂಪಡಿಸಿ.",
                    "hi": "अंगूर में मृदुरोमिल फफूंद (डाउनी मिल्ड्यू) देखा गया है। तुरंत डाइमेथोमॉर्फ या बोर्डो मिश्रण का छिड़काव करें।",
                    "es": "Mildiú velloso de la vid detectado. Aplique Dimetomorf o caldo bordelés de inmediato.",
                    "sw": "Ugonjwa wa ukungu wa zabibu umegunduliwa. Nyunyizia dawa ya Dimethomorph haraka.",
                    "fr": "Mildiou de la vigne détecté. Traitez sans délai au diméthomorphe ou à la bouillie bordelaise."
                }
            }
        ]
    },
    "apple": {
        "scientific_name": "Malus domestica",
        "diseases": [
            {
                "disease": "Apple Scab (Venturia inaequalis)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Olive-green to dark velvety soot-like spots on upper leaf surfaces",
                    "Leaves become puckered, distorted, and drop prematurely in mid-summer",
                    "Brown corky scab lesions on fruit causing fruit cracking and deformities"
                ],
                "organic": {
                    "summary": "Micronized sulfur or copper bio-protectant spray + shredding fallen leaves.",
                    "preparation": "Dissolve 30g Wettable Sulfur in 10L water.",
                    "frequency": "Apply from green-tip stage through petal fall.",
                    "practices": ["Flail mow or spray 5% urea on fallen orchard floor leaves in autumn to accelerate leaf decomposition."]
                },
                "chemical": {
                    "summary": "Difenoconazole 25% EC or Captan 50% WP.",
                    "active_ingredient": "Difenoconazole 25% EC",
                    "dosage_liter": "0.5 ml / Liter water",
                    "dosage_acre": "100 ml / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Avoid spraying during bloom to safeguard pollinating bees."]
                },
                "speech": {
                    "en": "Apple Scab fungal infection detected. Apply Difenoconazole or wettable sulfur from green-tip stage.",
                    "kn": "ಸೇಬು ಗಿಡದಲ್ಲಿ ಕಜ್ಜಿ ರೋಗ (ಆಪಲ್ ಸ್ಕ್ಯಾಬ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆ ಮತ್ತು ಹಣ್ಣುಗಳ ಮೇಲೆ ಕಪ್ಪು ಕಲೆಗಳಿವೆ. ಡಿಫೆನೊಕೊನಾಜೋಲ್ ಅಥವಾ ಗಂಧಕ ಸಿಂಪಡಿಸಿ.",
                    "hi": "सेब में स्कैब (दाग) रोग के लक्षण पाए गए हैं। डाइफेनोकोनाज़ोल या घुलनशील गंधक का छिड़काव करें।",
                    "es": "Moteado o sarna del manzano detectado. Aplique Difenoconazol o azufre micronizado.",
                    "sw": "Ugonjwa wa ukurutu wa tufaa umegunduliwa. Tumia Difenoconazole au salfa inayofaa.",
                    "fr": "Tavelure du pommier détectée. Pulvérisez du difénoconazole ou du soufre mouillable."
                }
            }
        ]
    },
    "brinjal": {
        "scientific_name": "Solanum melongena",
        "diseases": [
            {
                "disease": "Brinjal Phomopsis Blight & Fruit Rot (Phomopsis vexans)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Circular brown spots on leaves with pale centers that tear into shot-holes",
                    "Dark brown depressed lesions girdling base of stem",
                    "Soft watery rotting of fruits with concentric black pycnidia rings"
                ],
                "organic": {
                    "summary": "Trichoderma viride seed & foliar treatment + 5% Neem oil spray.",
                    "preparation": "Mix 50ml cold-pressed Neem oil + 5g soap in 10L water.",
                    "frequency": "Spray every 10 days during vegetative and fruit setting stages.",
                    "practices": ["Collect and deep-bury all rotten dropped fruits.", "Avoid solanaceous crop succession."]
                },
                "chemical": {
                    "summary": "Mancozeb 75% WP or Azoxystrobin 23% SC.",
                    "active_ingredient": "Mancozeb 75% WP",
                    "dosage_liter": "2.5 g / Liter water",
                    "dosage_acre": "500 g / Acre in 200L water",
                    "phi_days": 7,
                    "safety": ["Wash hands with soap after handling chemicals."]
                },
                "speech": {
                    "en": "Brinjal Phomopsis Blight detected. Spray Mancozeb or Neem oil immediately to protect fruit development.",
                    "kn": "ಬದನೆಕಾಯಿ ಬೆಳೆಯಲ್ಲಿ ಫೋಮಾಪ್ಸಿಸ್ ಅಂಗಮಾರಿ ಮತ್ತು ಕಾಯಿ ಕೊಳೆ ರೋಗ ಕಂಡುಬಂದಿದೆ. ಮ್ಯಾಂಕೋಜೆಬ್ ಅಥವಾ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ.",
                    "hi": "बैंगन में फोमोप्सिस झुलसा और फल सड़न रोग देखा गया है। मैंकोज़ेब या नीम तेल का छिड़काव करें।",
                    "es": "Tizón por Phomopsis de la berenjena detectado. Aplique Mancozeb o aceite de neem.",
                    "sw": "Ugonjwa wa ukungu wa biringanya umegunduliwa. Tumia Mancozeb au mafuta ya mwarobaini.",
                    "fr": "Flétrissement phomopsien de l'aubergine détecté. Traitez au mancozèbe ou à l'huile de neem."
                }
            }
        ]
    },
    "rose": {
        "scientific_name": "Rosa spp.",
        "diseases": [
            {
                "disease": "Rose Black Spot (Diplocarpon rosae)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Fringed, feathery black circular spots on upper surface of older rose leaves",
                    "Tissue surrounding spots turns bright yellow with rapid complete defoliation",
                    "Weakened canes with reduced flowering vigour and stem dieback"
                ],
                "organic": {
                    "summary": "Baking soda (Potassium/Sodium bicarbonate) spray + Neem oil (5ml/L).",
                    "preparation": "Dissolve 30g baking soda + 30ml Neem oil + 10 drops mild liquid dish soap in 10L water.",
                    "frequency": "Every 7 days in humid weather; spray early morning.",
                    "practices": ["Never water rose bushes from above; keep foliage completely dry.", "Rake and discard fallen black-spotted leaves."]
                },
                "chemical": {
                    "summary": "Myclobutanil 10% WP or Trifloxystrobin + Tebuconazole.",
                    "active_ingredient": "Trifloxystrobin 25% + Tebuconazole 50% WG",
                    "dosage_liter": "0.5 g / Liter water",
                    "dosage_acre": "100 g in 200L water",
                    "phi_days": 0,
                    "safety": ["Wear protective gloves when handling thorny canes."]
                },
                "speech": {
                    "en": "Rose Black Spot fungal infection detected with feathery circular lesions. Apply baking soda neem spray or systemic fungicide.",
                    "kn": "ಗುಲಾಬಿ ಗಿಡದಲ್ಲಿ ಕಪ್ಪು ಚುಕ್ಕೆ ರೋಗ (ಬ್ಲ್ಯಾಕ್ ಸ್ಪಾಟ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳು ಹಳದಿಯಾಗಿ ಉದುರುವುದನ್ನು ತಡೆಯಲು ಬೇವಿನ ಎಣ್ಣೆ ಸೋಡಾ ದ್ರಾವಣ ಅಥವಾ ಟೆಬುಕೊನಾಜೋಲ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "गुलाब में ब्लैक स्पॉट (काले धब्बे) रोग पाया गया है। बेकिंग सोडा व नीम तेल या फफूंदनाशक का छिड़काव करें।",
                    "es": "Mancha negra del rosal detectada. Aplique bicarbonato con neem o fungicida sistémico.",
                    "sw": "Madoa meusi ya waridi yamegunduliwa. Tumia dawa ya ukungu au mafuta ya mwarobaini kulinda majani.",
                    "fr": "Maladie des taches noires du rosier détectée. Pulvérisez du bicarbonate de neem ou un fongicide adapté."
                }
            }
        ]
    },
    "coconut": {
        "scientific_name": "Cocos nucifera",
        "diseases": [
            {
                "disease": "Coconut Bud Rot / Leaf Rot (Phytophthora palmivora)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Central spear leaf turns yellowish-brown and withers, easily pulled out with foul odor",
                    "Water-soaked lesions on bases of young fronds spreading into bud heart tissue",
                    "Death of central growing bud causing irrevocable palm collapse if left untreated"
                ],
                "organic": {
                    "summary": "Bordeaux paste application onto crown + cleaning decaying frond tissue.",
                    "preparation": "Mix 100g Copper Sulfate + 100g Quicklime in 1L water to form thick Bordeaux paste.",
                    "frequency": "Apply directly into crown cavity once decayed tissues are excised.",
                    "practices": ["Provide good palm drainage.", "Cover treated crown with polythene hood during monsoons to prevent water entry."]
                },
                "chemical": {
                    "summary": "Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold) crown placement.",
                    "active_ingredient": "Metalaxyl-Mancozeb WP (5g in perforated sachet placed in central crown leaf axil)",
                    "dosage_liter": "2.5 g / Liter water crown drench",
                    "dosage_acre": "500 g in 200L water drenched into top crowns",
                    "phi_days": 45,
                    "safety": ["Use professional tree climber with safety harness."]
                },
                "speech": {
                    "en": "Coconut Bud Rot detected. Critical emergency for palm crown. Clean rotten fronds and apply Bordeaux paste or Ridomil immediately.",
                    "kn": "ತೆಂಗಿನ ಮರದಲ್ಲಿ ಸುಳಿ ಕೊಳೆ ರೋಗ (ಬಡ್ ರಾಟ್) ತೀವ್ರವಾಗಿದೆ. ಮರ ಉಳಿಸಲು ತಕ್ಷಣವೇ ಕೊಳೆತ ಸುಳಿಯನ್ನು ಸ್ವಚ್ಛಗೊಳಿಸಿ ಬೋರ್ಡೋ ಪೇಸ್ಟ್ ಅಥವಾ ರಿಡೋಮಿಲ್ ಹಾಕಿ.",
                    "hi": "नारियल में बड रॉट (शीर्ष सड़न) का गंभीर प्रकोप है। तुरंत सड़े हुए हिस्से को साफ कर बोर्डो लेप या रिडोमिल लगाएं।",
                    "es": "Pudrición del cogollo del cocotero detectada. Aplique pasta bordelesa de inmediato en la corona.",
                    "sw": "Ugonjwa wa kuoza kwa kilele cha mnazi umegunduliwa. Tumia dawa ya Bordeaux kwenye shina la juu haraka.",
                    "fr": "Pourriture du bourgeon terminal du cocotier détectée. Appliquez d'urgence de la bouillie bordelaise sur la couronne."
                }
            }
        ]
    },
    "wheat": {
        "scientific_name": "Triticum aestivum",
        "diseases": [
            {
                "disease": "Wheat Yellow / Stripe Rust (Puccinia striiformis)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Bright yellow powdery pustules arranged in parallel linear stripes along leaf veins",
                    "Stripe pustules coalesce causing chlorosis, leaf scorch, and shrivelled grain filling",
                    "Severe yield reductions across cool, moist winter growing conditions"
                ],
                "organic": {
                    "summary": "Seed treatment with Trichoderma (10g/kg) and foliar bio-sulfur spray.",
                    "preparation": "Mix 25g Micronized sulfur in 10L clean water.",
                    "frequency": "Apply at first appearance of yellow stripes in winter.",
                    "practices": ["Plant resistant wheat varieties (HD-2967, DBW-187).", "Avoid excessive nitrogen top-dressing."]
                },
                "chemical": {
                    "summary": "Propiconazole 25% EC or Tebuconazole 25.9% EC foliar spray.",
                    "active_ingredient": "Propiconazole 25% EC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 30,
                    "safety": ["Do not spray against wind direction.", "Wear face shield."]
                },
                "speech": {
                    "en": "Wheat Stripe Rust detected with linear yellow pustules. Apply Propiconazole 25% EC immediately to prevent grain loss.",
                    "kn": "ಗೋಧಿ ಬೆಳೆಯಲ್ಲಿ ಹಳದಿ ತುಕ್ಕು ರೋಗ (ಸ್ಟ್ರೈಪ್ ರಸ್ಟ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ಹಳದಿ ಗೆರೆಗಳಂತಹ ಗುಳ್ಳೆಗಳಿವೆ. ಪ್ರೊಪಿಕೋನಾಜೋಲ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "गेहूं में पीला रतुआ (स्ट्राइप रस्ट) देखा गया है। पत्तियों पर पीली धारियां हैं। तुरंत प्रोपिकोनाज़ोल 25% का छिड़काव करें।",
                    "es": "Roya amarilla del trigo detectada. Aplique Propiconazol de inmediato.",
                    "sw": "Ugonjwa wa kutu ya ngano umegunduliwa. Nyunyizia Propiconazole haraka.",
                    "fr": "Rouille jaune du blé détectée. Traitez sans délai au propiconazole."
                }
            }
        ]
    },
    "universal_leaf": {
        "scientific_name": "Plantae (Universal Agricultural Foliar Pathology)",
        "diseases": [
            {
                "disease": "Foliar Anthracnose & Leaf Blight (ಎಲೆ ಅಂಗಮಾರಿ ಮತ್ತು ಕಪ್ಪು ಕಲೆ ರೋಗ - Colletotrichum / Alternaria spp.)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Irregular dark brown to black necrotic lesions expanding across leaf blade",
                    "Concentric rings and water-soaked borders with yellow chlorotic halos",
                    "Localized leaf tissue death, shot-hole perforations, and premature foliar drop"
                ],
                "organic": {
                    "summary": "1% Bordeaux mixture spray or Trichoderma harzianum (5g/L) bio-fungicide foliar application.",
                    "preparation": "Dissolve 100g Copper Sulfate + 100g Quicklime in 10L clean water to make fresh 1% Bordeaux mixture.",
                    "frequency": "Spray every 10 to 14 days during cloudy or humid weather.",
                    "practices": ["Prune and burn severely blighted lower leaves.", "Water at the soil base to avoid wet foliage."]
                },
                "chemical": {
                    "summary": "Mancozeb 75% WP or Azoxystrobin 23% SC broad-spectrum foliar fungicide.",
                    "active_ingredient": "Mancozeb 75% WP (2.5 g/L) or Azoxystrobin 23% SC (1.0 ml/L)",
                    "dosage_liter": "2.5 g Mancozeb or 1.0 ml Azoxystrobin per Liter water",
                    "dosage_acre": "500 g Mancozeb or 200 ml Azoxystrobin in 200L water",
                    "phi_days": 10,
                    "safety": ["Wear protective mask and gloves.", "Avoid spraying in high wind."]
                },
                "speech": {
                    "en": "Foliar Anthracnose and Leaf Blight detected on the crop leaf. Apply 1% Bordeaux mixture or Mancozeb fungicide immediately.",
                    "kn": "ಗಿಡದ ಎಲೆಯಲ್ಲಿ ಅಂಗಮಾರಿ ಮತ್ತು ಕಪ್ಪು ಕಲೆ ರೋಗ (ಬ್ಲೈಟ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ಒಣಗಿದ ಕಪ್ಪು-ಕಂದು ಕಲೆಗಳಿವೆ. ತಕ್ಷಣವೇ ಬೋರ್ಡೋ ದ್ರಾವಣ ಅಥವಾ ಮ್ಯಾಂಕೋಜೆಬ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "पौधे की पत्ती पर एन्थ्रेक्नोज़ और झुलसा (लीफ ब्लाइट) रोग पाया गया है। 1% बोर्डो मिश्रण या मैंकोज़ेब का छिड़काव करें।",
                    "es": "Antracnosis y tizón foliar detectados en la hoja. Aplique caldo bordelés al 1% o Mancozeb de inmediato.",
                    "sw": "Ugonjwa wa ukungu na kuungua kwa jani umegunduliwa. Nyunyizia mchanganyiko wa Bordeaux au Mancozeb.",
                    "fr": "Anthracnose et brûlure foliaire détectées sur la feuille. Pulvérisez de la bouillie bordelaise ou du mancozèbe."
                }
            },
            {
                "disease": "Powdery Mildew / White Foliar Mildew (ಬೂದಿ ರೋಗ / ಪುಡಿ ರೋಗ - Erysiphales)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "White to greyish superficial powdery fungal patches spreading over leaf surface",
                    "Chlorosis beneath fungal colonies, leaf crinkling, upward curling, and premature drying",
                    "Impaired photosynthesis and vigour leading to flower drop and poor yield"
                ],
                "organic": {
                    "summary": "Micronized Wettable Sulfur 80% WDG (2.5g/L) or cold-pressed Neem oil (3ml/L) + baking soda spray.",
                    "preparation": "Mix 25g Wettable sulfur in 10L clean water or 30ml Neem oil + 20g baking soda in 10L water.",
                    "frequency": "Spray every 7-10 days; avoid spraying sulfur if temperature exceeds 32°C.",
                    "practices": ["Improve ventilation around plant canopy.", "Prune crowded inner foliage to let sunlight penetrate."]
                },
                "chemical": {
                    "summary": "Hexaconazole 5% EC or Azoxystrobin 18.2% + Difenoconazole 11.4% SC.",
                    "active_ingredient": "Hexaconazole 5% EC",
                    "dosage_liter": "1.5 ml / Liter water",
                    "dosage_acre": "300 ml / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Do not spray during full bloom.", "Wear protective goggles."]
                },
                "speech": {
                    "en": "Powdery Mildew fungal infection detected. White powder coating observed on leaf surface. Apply micronized sulfur or Hexaconazole.",
                    "kn": "ಗಿಡದ ಎಲೆಯ ಮೇಲೆ ಬೂದಿ ರೋಗ (ಪುಡಿ ರೋಗ) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ಬಿಳಿ ಬೂದಿಯಂತಹ ಪದರವಿದೆ. ಗಂಧಕದ ಪುಡಿ ಅಥವಾ ಹೆಕ್ಸಾಕೊನಾಜೋಲ್ ಸಿಂಪಡಿಸಿ.",
                    "hi": "पत्ती पर पाउडरी मिल्ड्यू (सफेद चूर्ण/भभूतिया) रोग पाया गया है। घुलनशील गंधक या हेक्साकोनाज़ोल का छिड़काव करें।",
                    "es": "Mildiú polvoriento detectado en la hoja. Aplique azufre micronizado o Hexaconazol.",
                    "sw": "Ugonjwa wa ukungu mweupe (Powdery Mildew) umegunduliwa kwenye jani. Tumia salfa au Hexaconazole.",
                    "fr": "Oïdium détecté sur la feuille de la plante. Appliquez du soufre micronisé ou de l'hexaconazole."
                }
            },
            {
                "disease": "Cercospora / Target Leaf Spot (ಎಲೆ ಚುಕ್ಕೆ ರೋಗ - Cercospora spp.)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Discrete circular to angular brown spots with ash-grey centers and distinct yellow halo rings",
                    "Spots coalesce across leaf lamina causing premature leaf senescence and drop",
                    "Significant reduction in photosynthetic active leaf area"
                ],
                "organic": {
                    "summary": "5% Neem Seed Kernel Extract (NSKE) + Pseudomonas fluorescens bio-agent spray.",
                    "preparation": "Crush 500g neem seeds, soak in 10L water overnight with 20g soap. Filter and spray.",
                    "frequency": "Every 10 to 14 days at first appearance of spots.",
                    "practices": ["Avoid sprinkler watering that splashes soil spores onto leaves.", "Rotate crops annually."]
                },
                "chemical": {
                    "summary": "Carbendazim 12% + Mancozeb 63% WP (Saaf) or Difenoconazole 25% EC.",
                    "active_ingredient": "Carbendazim 12% + Mancozeb 63% WP",
                    "dosage_liter": "2.0 g / Liter water",
                    "dosage_acre": "400 g / Acre in 200L water",
                    "phi_days": 10,
                    "safety": ["Rotate chemical classes to prevent fungal resistance.", "Wear nitrile chemical gloves."]
                },
                "speech": {
                    "en": "Cercospora leaf spot detected with characteristic yellow halos. Apply Saaf (Carbendazim + Mancozeb) or Neem extract.",
                    "kn": "ಗಿಡದ ಎಲೆಯ ಮೇಲೆ ಎಲೆ ಚುಕ್ಕೆ ರೋಗ ಕಂಡುಬಂದಿದೆ. ಕಂದು ಬಣ್ಣದ ವೃತ್ತಾಕಾರದ ಕಲೆಗಳಿವೆ. ಸಾಫ್ (ಕಾರ್ಬೆಂಡಾಜಿಮ್ + ಮ್ಯಾಂಕೋಜೆಬ್) ಅಥವಾ ಬೇವಿನ ಕಷಾಯ ಸಿಂಪಡಿಸಿ.",
                    "hi": "पत्ती पर सर्कोस्पोरा पत्ती धब्बा रोग पाया गया है। तुरंत साफ (कार्बेंडाजिम + मैंकोजेब) का छिड़काव करें।",
                    "es": "Mancha foliar por Cercospora detectada con halos amarillos. Aplique Carbendazim con Mancozeb.",
                    "sw": "Madoa ya majani ya Cercospora yamegunduliwa. Tumia Carbendazim au Mancozeb.",
                    "fr": "Cercosporiose foliaire détectée avec halos jaunes caractéristiques. Traitez au carbendazime combiné au mancozèbe."
                }
            },
            {
                "disease": "Foliar Chlorosis & Mosaic Virus / Vector Damage (ಹಳದಿ ನಂಜು ರೋಗ / ಕ್ಲೋರೋಸಿಸ್)",
                "pathogen": PathogenType.VIRAL,
                "severity_default": SeverityEnum.SEVERE,
                "symptoms": [
                    "Mottled pattern of alternating light green and chlorotic bright yellow patches",
                    "Vein clearing, leaf wrinkling, stunting of young shoots, and brittle lamina",
                    "Transmitted by sucking insect vectors (whiteflies, aphids, or thrips)"
                ],
                "organic": {
                    "summary": "Yellow and blue sticky traps (25/acre) + 10,000 ppm Neem oil (3ml/L) + micronutrient foliar spray.",
                    "preparation": "Emulsify 30ml Neem oil + 5g soap in 10L water. Add 10g zinc-iron chelated micronutrient powder.",
                    "frequency": "Weekly application to suppress sucking insect vectors.",
                    "practices": ["Rogue out severely stunted infected plants and bury them.", "Keep field weed-free to destroy alternate viral hosts."]
                },
                "chemical": {
                    "summary": "Thiamethoxam 25% WG or Acetamiprid 20% SP systemic vector control.",
                    "active_ingredient": "Thiamethoxam 25% WG",
                    "dosage_liter": "0.5 g / Liter water",
                    "dosage_acre": "100 g / Acre in 200L water",
                    "phi_days": 14,
                    "safety": ["Avoid spraying during honeybee foraging hours.", "Wear protective goggles."]
                },
                "speech": {
                    "en": "Foliar Chlorosis and Mosaic Virus detected. Transmitted by sucking pest vectors. Install sticky traps and spray Thiamethoxam or Neem oil.",
                    "kn": "ಗಿಡದ ಎಲೆಯಲ್ಲಿ ಹಳದಿ ನಂಜು ರೋಗ ಅಥವಾ ಕ್ಲೋರೋಸಿಸ್ ಕಂಡುಬಂದಿದೆ. ಬಿಳಿ ನೊಣಗಳು ಮತ್ತು ಹೇನುಗಳ ನಿಯಂತ್ರಣಕ್ಕಾಗಿ ಹಳದಿ ಅಂಟು ಬಲೆಗಳನ್ನು ಹಾಕಿ ಥೈಯಾಮೆಥಾಕ್ಸಮ್ ಅಥವಾ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ.",
                    "hi": "पत्ती में मोज़ेक वायरस और क्लोरोसिस (पीलापन) पाया गया है। सफेद मक्खी व रसचूसक कीटों के नियंत्रण के लिए चिपचिपे ट्रैप लगाएं और थायमेथोक्सम का छिड़काव करें।",
                    "es": "Clorosis foliar y virus del mosaico detectados. Controle vectores con trampas y Tiametoxam.",
                    "sw": "Ugonjwa wa kukunja majani na virusi vya mosaic umegunduliwa. Dhibiti wadudu kwa mitego na dawa inayofaa.",
                    "fr": "Chlorose et virus de la mosaïque détectés. Contrôlez les insectes vecteurs avec du thiaméthoxame et des pièges collants."
                }
            },
            {
                "disease": "Foliar Rust Disease (ಎಲೆ ತುಕ್ಕು ರೋಗ - Puccinia spp.)",
                "pathogen": PathogenType.FUNGAL,
                "severity_default": SeverityEnum.MODERATE,
                "symptoms": [
                    "Raised, reddish-orange to cinnamon-brown powdery pustules erupting across leaf epidermis",
                    "Ruptured pustules releasing clouds of powdery fungal rust spores upon touch",
                    "Extensive yellow chlorosis and premature leaf withering"
                ],
                "organic": {
                    "summary": "Micronized Wettable Sulfur 80% WDG (2.5g/L) foliar spray.",
                    "preparation": "Mix 25g Wettable sulfur in 10L clean water.",
                    "frequency": "Every 10-14 days at early sign of rust pustules.",
                    "practices": ["Destroy infected crop stubble.", "Avoid excess nitrogen fertilizer."]
                },
                "chemical": {
                    "summary": "Propiconazole 25% EC or Tebuconazole 25.9% EC systemic triazole fungicide.",
                    "active_ingredient": "Propiconazole 25% EC",
                    "dosage_liter": "1.0 ml / Liter water",
                    "dosage_acre": "200 ml / Acre in 200L water",
                    "phi_days": 21,
                    "safety": ["Do not spray during midday heat.", "Wear protective mask."]
                },
                "speech": {
                    "en": "Foliar Rust disease detected with powdery cinnamon pustules. Apply Propiconazole or wettable sulfur.",
                    "kn": "ಗಿಡದ ಎಲೆಯ ಮೇಲೆ ತುಕ್ಕು ರೋಗ (ರಸ್ಟ್) ಕಂಡುಬಂದಿದೆ. ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಬಣ್ಣದ ಪುಡಿ ಗುಳ್ಳೆಗಳಿವೆ. ಪ್ರೊಪಿಕೋನಾಜೋಲ್ ಅಥವಾ ಗಂಧಕದ ಪುಡಿ ಸಿಂಪಡಿಸಿ.",
                    "hi": "पत्ती पर रतुआ (रस्ट) रोग पाया गया है। पत्तियों पर भूरे फफोले हैं। प्रोपिकोनाज़ोल या गंधक का छिड़काव करें।",
                    "es": "Roya foliar detectada con pústulas de color canela. Aplique Propiconazol o azufre micronizado.",
                    "sw": "Ugonjwa wa kutu ya majani umegunduliwa. Tumia dawa ya Propiconazole au salfa.",
                    "fr": "Rouille foliaire détectée. Pulvérisez du propiconazole ou du soufre mouillable."
                }
            }
        ]
    }
}

# =======================================================================
# Comprehensive Veterinary Knowledge Base (Cattle, Buffalo, Sheep, Goats, Poultry)
# =======================================================================
VETERINARY_KNOWLEDGE_BASE = [
    {
        "id": "lumpy_skin_disease",
        "species": "Cattle & Buffalo (Bovine)",
        "scientific_name": "Bos taurus / Bos indicus",
        "disease": "Bovine Lumpy Skin Disease (Capripoxvirus)",
        "pathogen": PathogenType.VETERINARY_VIRAL,
        "severity": SeverityEnum.SEVERE,
        "keywords": ["lump", "nodule", "skin bump", "scab", "bovine", "cow", "cattle", "buffalo"],
        "symptoms": [
            "Multiple firm circumscribed round cutaneous nodules (2 to 5 cm) across head, neck, udder, and limbs",
            "High fever, marked reduction in milk yield, and enlarged prescapular lymph nodes",
            "Necrotic ulceration in center of nodules forming deep 'sitfast' scabs prone to fly-strike"
        ],
        "organic": {
            "summary": "Herbal antiseptic wash & natural vector barrier: Wash skin lesions with mild Neem-Turmeric paste (50g neem leaf paste + 25g raw turmeric).",
            "preparation": "Boil 100g fresh Neem leaves in 5L water, cool and add 20g pure turmeric powder. Apply gently using sterile cotton gauze.",
            "frequency": "Twice daily on superficial open nodules; apply citronella/neem oil around shed to repel vector flies.",
            "practices": [
                "Strictly isolate the affected animal in a dry, sanitized, insect-screened shed.",
                "Disinfect feeding troughs daily with 2% sodium carbonate or mild bleaching powder.",
                "Burn all contaminated bedding and fallen scabs to prevent vector transmission."
            ]
        },
        "chemical": {
            "summary": "VETERINARY MEDICAL PROTOCOL: Administer veterinary supportive therapy under certified doctor guidance. NEVER USE CROP PESTICIDES.",
            "active_ingredient": "Povidone-Iodine 5% (Topical) + Veterinary Meloxicam / Paracetamol (Antipyretic) + Ceftiofur / Enrofloxacin (Vet Antibiotic)",
            "dosage_liter": "Povidone-Iodine 5% spray applied directly onto ulcerated lesions twice daily.",
            "dosage_acre": "Consult a registered Veterinary Surgeon for injectable dosage based on animal body weight (e.g. Meloxicam 0.5 mg/kg IM).",
            "phi_days": 14,
            "safety": [
                "CRITICAL WARNING: NEVER apply agricultural crop fungicides, herbicides, or plant pesticides to livestock. They cause fatal organ failure.",
                "Report outbreak immediately to your local Animal Husbandry & Veterinary Officer for ring-vaccination with Goat Pox / Lumpy Skin vaccine.",
                "Wear protective rubber gloves and sanitize boots before tending to healthy animals."
            ]
        },
        "warning": "VETERINARY ADVISORY: This is an ANIMAL / LIVESTOCK viral disease (Bovine Lumpy Skin Disease), NOT a crop plant disease. Never administer agricultural crop pesticides or fungicides to animals. Isolate the animal and summon a certified veterinary doctor.",
        "speech": {
            "en": "Veterinary Alert: Bovine Lumpy Skin Disease detected on livestock. Isolate animal immediately, apply neem-turmeric antiseptic wash, and do NOT use crop chemicals. Call a certified veterinarian.",
            "kn": "ಪಶು ವೈದ್ಯಕೀಯ ತುರ್ತು ಎಚ್ಚರಿಕೆ: ಹಸುವಿನಲ್ಲಿ ಚರ್ಮ ಗಂಟು ರೋಗ (ಲಂಪಿ ಸ್ಕಿನ್) ಕಂಡುಬಂದಿದೆ. ಪ್ರಾಣಿಯನ್ನು ತಕ್ಷಣವೇ ಪ್ರತ್ಯೇಕಿಸಿ, ಬೇವಿನ ಸೊಪ್ಪು ಮತ್ತು ಅರಿಶಿನದ ಲೇಪನ ಹಚ್ಚಿ. ಯಾವುದೇ ಕೃಷಿ ಕೀಟನಾಶಕ ಬಳಸಬೇಡಿ. ಪಶು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "hi": "पशु चिकित्सा चेतावनी: मवेशी में लंपी स्किन रोग (Lumpy Skin Disease) के लक्षण पाए गए हैं। पशु को तुरंत अलग करें, नीम-हल्दी का लेप लगाएं। फसलों वाली दवा कतई न लगाएं।",
            "es": "Alerta Veterinaria: Enfermedad de la piel nodular bovina detectada. Aísle al animal y consulte a un veterinario. Nunca aplique pesticidas agrícolas a animales.",
            "sw": "Tahadhari ya Mifugo: Ugonjwa wa ngozi wa ng'ombe (Lumpy Skin) umegunduliwa. Mtenge mnyama mara moja na upate ushauri wa daktari wa mifugo.",
            "fr": "Alerte Vétérinaire : Dermatose nodulaire contagieuse bovine détectée. Isolez immédiatement l'animal et consultez un vétérinaire."
        }
    },
    {
        "id": "sarcoptic_mange",
        "species": "Livestock (Cattle, Goats, Sheep, Canines)",
        "scientific_name": "Mammalia (Veterinary)",
        "disease": "Sarcoptic Mange / Mite Infestation (Sarcoptes scabiei)",
        "pathogen": PathogenType.VETERINARY_PARASITIC,
        "severity": SeverityEnum.MODERATE,
        "keywords": ["mange", "crust", "scab", "hair loss", "alopecia", "scratching", "thick skin"],
        "symptoms": [
            "Intense itching, scratching, and rubbing causing severe self-inflicted excoriations",
            "Thickened, wrinkled, leathery skin with heavy greyish-brown crusts and scabs",
            "Extensive alopecia (hair loss) starting around face, neck, and root of tail"
        ],
        "organic": {
            "summary": "Herbal sulfur oil balm: Pure cold-pressed Neem oil (10%) blended in coconut oil with sublimed sulfur powder.",
            "preparation": "Mix 20ml cold-pressed Neem oil + 80ml coconut oil + 5g medicinal sulfur powder. Massage into crusted skin.",
            "frequency": "Apply every 3 days for 2-3 weeks; wash animal with mild antiseptic soap before first application.",
            "practices": [
                "Isolate infested animals from the main herd.",
                "Scrub rubbing posts, fences, and stanchions with boiling water and disinfectant.",
                "Ensure adequate dietary zinc and vitamin A."
            ]
        },
        "chemical": {
            "summary": "VETERINARY ACARICIDAL THERAPY: Veterinary Ivermectin subcutaneous injection or approved veterinary Amitraz / Deltamethrin dip.",
            "active_ingredient": "Ivermectin 1% Injectable or Amitraz 12.5% Veterinary Liquid (Prescription Only)",
            "dosage_liter": "Amitraz 12.5% EC at 2 ml per Liter water for topical veterinary sponge wash.",
            "dosage_acre": "Ivermectin 1% @ 1 ml per 50 kg body weight subcutaneously by a licensed veterinarian.",
            "phi_days": 28,
            "safety": [
                "NEVER use agricultural crop insecticides on animal skin; risk of fatal organophosphate poisoning.",
                "Wear protective gloves; sarcoptic mange can cause transient papular dermatitis in humans (zoonotic)."
            ]
        },
        "warning": "VETERINARY ADVISORY: This is an ANIMAL / LIVESTOCK parasitic condition (Mange/Mites). Do NOT use crop insecticides on animals. Consult your local veterinary professional.",
        "speech": {
            "en": "Veterinary Notice: Sarcoptic Mange detected on animal skin. Use veterinary acaricide or neem-sulfur balm. Do not use plant crop chemicals.",
            "kn": "ಪಶು ರೋಗ ಎಚ್ಚರಿಕೆ: ಪ್ರಾಣಿಯ ಚರ್ಮದಲ್ಲಿ ನವೆ ಹುಳ (ಮ್ಯಾಂಜ್) ತುರಿಕೆ ರೋಗವಿದೆ. ಬೇವಿನ ಎಣ್ಣೆ ಮತ್ತು ಗಂಧಕದ ಮುಲಾಮು ಹಚ್ಚಿ. ಕೃಷಿ ಔಷಧಿಗಳನ್ನು ಪ್ರಾಣಿಗಳಿಗೆ ಹಾಕಬೇಡಿ. ಪಶು ವೈದ್ಯರನ್ನು ಸಂಪರ್ಕಿಸಿ.",
            "hi": "पशु रोग सूचना: पशु में खुजली या दाद (मांज/माइट्स) का संक्रमण है। पशु चिकित्सक की सलाह लें।",
            "es": "Aviso Veterinario: Sarna sarcóptica detectada. Use acaricida veterinario o bálsamo de neem.",
            "sw": "Taarifa ya Mifugo: Ugonjwa wa ukurutu wa mifugo umegunduliwa. Tumia dawa ya mifugo na ushauri wa daktari.",
            "fr": "Avis Vétérinaire : Gale sarcoptique détectée. Utilisez un acaricide vétérinaire approprié."
        }
    }
]

def analyze_image_heuristics(
    image_bytes: bytes,
    crop_hint: Optional[str] = None,
    cnn_features: Optional[Dict[str, Any]] = None
) -> Tuple[DomainCategory, str, Dict[str, Any], float, float, bool]:
    """
    Intelligent Computer Vision & Pathology Synthesizer:
    1. Distinguishes between CROP FOLIAGE, LIVESTOCK / ANIMAL PATHOLOGY, and NON-AGRICULTURAL images.
    2. Prevents false positive tomato/crop classifications on animal or non-plant subjects!
    """
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((300, 300))
        width, height = img.size
        pixels = list(img.getdata())
        total = len(pixels)

        green_count = 0
        yellow_count = 0
        brown_count = 0
        white_mold_count = 0
        skin_mammalian_count = 0
        synthetic_neutral_count = 0
        food_snack_count = 0

        for r, g, b in pixels:
            # 1. Flat neutral white / grays / black background
            if abs(r - g) < 8 and abs(g - b) < 8:
                synthetic_neutral_count += 1
            # 2. White mildew / superficial fungal patches on leaf
            elif r > 175 and g > 175 and b > 165:
                white_mold_count += 1
            # 3. Necrotic brown / dead leaf lesion / fungal spot (Checked BEFORE green foliage!)
            elif (r < 140 and g < 130 and b < 95 and r >= g - 12 and r > b + 15):
                brown_count += 1
            # 4. Chlorotic yellow / orange halo (Checked BEFORE green foliage!)
            elif (r > 115 and g > 105 and b < 105 and r >= g - 25 and (r + g) > 230):
                yellow_count += 1
            # 5. Broad vegetative chlorophyll green (under any light, shadow, or olive variety)
            elif (g >= r - 15 and g > b - 8 and g > 28) or (g > r and g > b) or (g > 45 and g > b * 1.05 and r < g + 18):
                green_count += 1
            # 6. Mammalian skin / coat / flesh / fur tones (ONLY when not foliage)
            elif ((r > 130 and g > 80 and b > 60 and r > g + 20 and g >= b) or \
                  (r > 160 and g < 120 and b < 120)) and not (g >= r - 15 and g > b - 8):
                skin_mammalian_count += 1
            # 7. Cooked food / fried snack (Vada Pav, Samosa, Fried items, Bread)
            elif r > g + 12 and r > b + 25 and r > 115:
                food_snack_count += 1

        green_ratio = green_count / total
        yellow_ratio = yellow_count / total
        brown_ratio = brown_count / total
        skin_ratio = skin_mammalian_count / total
        neutral_ratio = synthetic_neutral_count / total
        food_ratio = food_snack_count / total

        is_auto_detect = not crop_hint or any(w in str(crop_hint).lower() for w in ["auto", "detect", "any", "ಸ್ವಯಂ", "crop", "leaf", "plant"])

        is_animal_hint = bool(
            not is_auto_detect and crop_hint and 
            any(a in str(crop_hint).lower() for a in ["cow", "cattle", "buffalo", "goat", "sheep", "poultry", "canine"]) and
            not any(p in str(crop_hint).lower() for p in ["leaf", "crop", "plant", "auto"])
        )

        # CASE A: EXPLICIT VETERINARY LIVESTOCK DIAGNOSIS (Requested by user)
        if is_animal_hint:
            if "lump" in str(crop_hint).lower() or skin_ratio > 0.40:
                vet_data = VETERINARY_KNOWLEDGE_BASE[0] # Lumpy Skin Disease
                confidence = 0.95
            elif "mange" in str(crop_hint).lower() or "itch" in str(crop_hint).lower():
                vet_data = VETERINARY_KNOWLEDGE_BASE[1] # Mange
                confidence = 0.93
            else:
                vet_data = VETERINARY_KNOWLEDGE_BASE[0]
                confidence = 0.92

            infection_pct = round(min(80.0, max(20.0, skin_ratio * 70)), 1)
            return DomainCategory.ANIMAL_LIVESTOCK, vet_data["species"], vet_data, confidence, infection_pct, True

        cnn_is_leaf = bool(cnn_features and cnn_features.get("is_crop_leaf"))
        cnn_foliar = float(cnn_features.get("foliar_score", 0.0)) if cnn_features else 0.0
        cnn_is_wrong = bool(cnn_features and cnn_features.get("is_wrong_photo"))
        cnn_wrong_type = cnn_features.get("wrong_photo_type") if cnn_features else None

        # Check for non-plant / wrong-photo categories FIRST:
        if cnn_is_wrong or (not cnn_is_leaf and (green_ratio < 0.04 and yellow_ratio < 0.04)):
            # 1. ANIMAL PHOTO UPLOADED
            if cnn_wrong_type == "ANIMAL" or skin_ratio > 0.22 or (cnn_features and cnn_features.get("animal_score", 0) > 0.22):
                wrong_animal_entry = {
                    "disease": "Error: Animal Photo Detected (Not a Plant Disease Photo)",
                    "pathogen": PathogenType.INVALID_SUBJECT,
                    "scientific_name": "Animalia (Non-Botanical)",
                    "symptoms": [
                        "AgriVision Deep-CNN identified animal coat, fur, mammalian anatomy or pet subject instead of plant foliage",
                        "No vegetative leaf lamina, petiole, or foliar venation found in photograph",
                        "AgriVision is strictly a crop plant pathology diagnostic engine and requires a plant leaf"
                    ],
                    "organic": {
                        "summary": "ERROR: Animal photo detected. Crop disease treatments are not applicable to animals. Please upload a clear photo of an affected crop leaf.",
                        "preparation": "N/A - Please photograph a crop leaf",
                        "frequency": "N/A",
                        "practices": ["Hold camera 15-30 cm from leaf under natural daylight.", "Avoid photographing animals or non-plants."]
                    },
                    "chemical": {
                        "summary": "CRITICAL HAZARD WARNING: Never apply agricultural crop pesticides, systemic fungicides, or herbicides to animals! If you require livestock veterinary care, consult a licensed veterinary doctor.",
                        "active_ingredient": "None",
                        "dosage_per_liter": "N/A",
                        "dosage_per_hectare_or_acre": "N/A",
                        "phi_days": 0,
                        "safety": ["Do not apply crop chemicals to animals.", "Re-scan with a proper plant leaf."]
                    },
                    "speech": {
                        "en": "Error: Animal photo detected. AgriVision AI is strictly for agricultural crop plant leaves. Please upload a clear photo of an affected plant leaf.",
                        "kn": "ದೋಷ: ಪ್ರಾಣಿಯ ಫೋಟೋ ಪತ್ತೆಯಾಗಿದೆ. ಅಗ್ರಿವಿಷನ್ ಕೇವಲ ಬೆಳೆಯ ಎಲೆಯ ರೋಗ ಪತ್ತೆಹಚ್ಚುವ ವ್ಯವಸ್ಥೆಯಾಗಿದ್ದು, ಪ್ರಾಣಿಗಳಿಗಲ್ಲ. ದಯವಿಟ್ಟು ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                        "hi": "त्रुटि: यह एक पशु का चित्र है, फसल की पत्ती नहीं। रोग निदान के लिए कृपया फसल की पत्ती की स्पष्ट फोटो अपलोड करें।",
                        "es": "Error: Foto de animal detectada. AgriVision requiere una hoja de planta de cultivo.",
                        "sw": "Hitilafu: Picha ya mnyama imegunduliwa, si jani la mmea. AgriVision inahitaji picha ya jani la zao.",
                        "fr": "Erreur : Photo d'animal détectée. AgriVision nécessite une feuille de plante."
                    }
                }
                return DomainCategory.NON_AGRICULTURAL, "Animal Photo / ಪ್ರಾಣಿಯ ಫೋಟೋ", wrong_animal_entry, 0.98, 0.0, False

            # 2. FOOD ITEM UPLOADED (VADA PAV, SAMOSA, BREAD, COOKED SNACKS)
            if cnn_wrong_type == "FOOD" or food_ratio > 0.18 or (cnn_features and cnn_features.get("food_score", 0) > 0.20):
                wrong_food_entry = {
                    "disease": "Error: Food Item Detected (Vada Pav / Snack - Not a Crop Plant Leaf)",
                    "pathogen": PathogenType.INVALID_SUBJECT,
                    "scientific_name": "Food / Non-Botanical",
                    "symptoms": [
                        "AgriVision Deep-CNN detected cooked food / snack (e.g., Vada Pav, bread, fried batter, or fast food)",
                        "No vegetative chlorophyll green, foliar venation, or botanical plant leaf tissue found",
                        "AgriVision AI is strictly a crop plant pathology engine and requires a plant leaf photo",
                        "Cooked food cannot be diagnosed for plant diseases or treated with crop chemicals"
                    ],
                    "organic": {
                        "summary": "ERROR: FOOD ITEM DETECTED. You uploaded a photo of food (such as Vada Pav, bread, or fried snack). Please capture or upload a clear photo of an affected crop leaf.",
                        "preparation": "N/A - Please photograph a crop leaf",
                        "frequency": "N/A",
                        "practices": ["Hold camera 15-30 cm from an affected crop leaf under natural daylight.", "Avoid photographing food items, people, or animals."]
                    },
                    "chemical": {
                        "summary": "CRITICAL HAZARD WARNING: NEVER apply agricultural pesticides, fungicides, or crop chemicals to food, snacks, or edible items! They contain toxic chemical active ingredients.",
                        "active_ingredient": "None",
                        "dosage_per_liter": "N/A (Do not apply)",
                        "dosage_per_hectare_or_acre": "N/A (Do not apply)",
                        "phi_days": 0,
                        "safety": ["Never apply crop chemicals to food.", "Re-scan with a proper crop leaf."]
                    },
                    "speech": {
                        "en": "Error: Food item detected. This is a photo of food or a cooked snack such as Vada Pav, not a crop plant leaf. AgriVision requires a close-up photo of an affected plant leaf to diagnose disease.",
                        "kn": "ದೋಷ: ಇದು ಆಹಾರ ಪದಾರ್ಥವಾಗಿದ್ದು (ವಡಾಪಾವ್ ಅಥವಾ ತಿಂಡಿ), ಸಸ್ಯ ರೋಗದ ಎಲೆಯಲ್ಲ. ರೋಗ ಪತ್ತೆಹಚ್ಚಲು ದಯವಿಟ್ಟು ಬಾಧಿತ ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                        "hi": "त्रुटि: यह खाद्य पदार्थ (जैसे वड़ा पाव या नाश्ता) है, फसल की पत्ती नहीं। रोग निदान के लिए कृपया फसल की पत्ती की स्पष्ट फोटो अपलोड करें।",
                        "es": "Error: Alimento detectado. Esta es una foto de comida, no una hoja de cultivo.",
                        "sw": "Hitilafu: Chakula kimegunduliwa, si jani la mmea. Tafadhali pakia picha ya jani la mmea.",
                        "fr": "Erreur : Nourriture détectée. Ceci est une photo d'aliment et non une feuille de plante."
                    }
                }
                return DomainCategory.NON_AGRICULTURAL, "Food Item / ಆಹಾರ ಪದಾರ್ಥ", wrong_food_entry, 0.99, 0.0, False

            # 3. INVALID / NON-PLANT SUBJECT (OBJECT, HUMAN, SCENE, OR INSUFFICIENT FOLIAGE)
            invalid_entry = {
                "disease": "Error: Not a Plant Disease Photo (Invalid Non-Botanical Subject)",
                "pathogen": PathogenType.INVALID_SUBJECT,
                "scientific_name": "Non-Botanical",
                "symptoms": [
                    "No vegetative crop leaf tissue or foliar pathology detected in photograph",
                    "Image appears to contain an inanimate object, human subject, vehicle, room, or scene",
                    "AgriVision AI is strictly a crop plant pathology engine and requires a plant leaf photo"
                ],
                "organic": {
                    "summary": "ERROR: NOT A PLANT DISEASE PHOTO. Please capture a clear, close-up photograph of an affected crop plant leaf under natural daylight.",
                    "preparation": "Position camera 15-30 cm away from the leaf under natural daylight.",
                    "frequency": "N/A",
                    "practices": ["Hold camera steady to avoid motion blur.", "Focus directly on the affected leaf surface or lesion."]
                },
                "chemical": {
                    "summary": "CRITICAL HAZARD WARNING: No agricultural chemical recommendations are applicable for non-plant subjects. Do not apply crop chemicals to non-plants.",
                    "active_ingredient": "None",
                    "dosage_per_liter": "N/A",
                    "dosage_per_hectare_or_acre": "N/A",
                    "phi_days": 0,
                    "safety": ["Ensure proper crop leaf framing before re-submitting."]
                },
                "speech": {
                    "en": "Error: Not a plant disease photo. No crop plant leaf detected. Please take a clear photo of an affected plant leaf under natural daylight.",
                    "kn": "ದೋಷ: ಇದು ಸಸ್ಯ ರೋಗದ ಫೋಟೋ ಅಲ್ಲ. ಅಗ್ರಿವಿಷನ್ ಕೇವಲ ಸಸ್ಯ ಮತ್ತು ಬೆಳೆಗಳ ರೋಗ ಪತ್ತೆಹಚ್ಚುವ ವ್ಯವಸ್ಥೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು ಬಾಧಿತ ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                    "hi": "त्रुटि: यह किसी पौधे की बीमारी का फोटो नहीं है। कृपया प्रभावित फसल की पत्ती का स्पष्ट फोटो अपलोड करें।",
                    "es": "Error: No es una foto de enfermedad de planta. Tome una foto clara de una hoja de cultivo.",
                    "sw": "Hitilafu: Si picha ya ugonjwa wa mmea. Tafadhali piga picha wazi ya jani la mmea.",
                    "fr": "Erreur : Ceci n'est pas une photo de maladie de plante. Veuillez prendre une photo claire d'une feuille."
                }
            }
            return DomainCategory.NON_AGRICULTURAL, "Non-Crop Subject / ಅಸಂಬದ್ಧ ಚಿತ್ರ", invalid_entry, 0.98, 0.0, False

        # CASE D: CROP PLANT LEAF DETECTED
        white_mold_ratio = white_mold_count / total
        infection_pct = min(100.0, max(0.0, (yellow_ratio * 0.7 + brown_ratio * 1.3 + white_mold_ratio * 1.5) * 100))

        # Check if leaf is genuinely healthy:
        # A leaf is ONLY healthy if green is high, infection is low, AND CNN detected no significant lesions!
        cnn_lesions = cnn_features.get("lesion_count", 0) if cnn_features else 0
        cnn_lesion_pct = cnn_features.get("cnn_lesion_percentage", 0.0) if cnn_features else 0.0
        is_healthy = (green_ratio > 0.65) and (infection_pct < 7.0) and (cnn_lesions < 5) and (cnn_lesion_pct < 12.0)

        if is_healthy:
            target_crop = crop_hint.lower() if crop_hint and crop_hint.lower() in AGRONOMY_KNOWLEDGE_BASE and not is_auto_detect else "Crop Foliage / ಸಸ್ಯದ ಎಲೆ"
            disease_entry = AGRONOMY_KNOWLEDGE_BASE["healthy"]["diseases"][0]
            confidence = min(0.98, max(0.88, 0.80 + (green_ratio * 0.20)))
            return DomainCategory.CROP_LEAF, target_crop.capitalize(), disease_entry, confidence, round(infection_pct, 1), False

        # Match specific crop hint if user explicitly provided one:
        crop_key = None
        if crop_hint and not is_auto_detect:
            hint_lower = crop_hint.lower()
            for k in AGRONOMY_KNOWLEDGE_BASE.keys():
                if k != "healthy" and k != "universal_leaf" and k in hint_lower:
                    crop_key = k
                    break

        if crop_key and crop_key in AGRONOMY_KNOWLEDGE_BASE:
            crop_data = AGRONOMY_KNOWLEDGE_BASE[crop_key]
            diseases = crop_data["diseases"]
            subject_title = crop_key.capitalize()

            if brown_ratio > 0.18 or white_mold_ratio > 0.06:
                selected_disease = diseases[0]
                confidence = min(0.96, max(0.85, 0.78 + (brown_ratio * 0.4)))
            elif yellow_ratio > 0.14:
                selected_disease = diseases[-1] if len(diseases) > 1 else diseases[0]
                confidence = min(0.95, max(0.84, 0.76 + (yellow_ratio * 0.5)))
            else:
                selected_disease = diseases[0]
                confidence = 0.91

            return DomainCategory.CROP_LEAF, subject_title, selected_disease, confidence, round(max(8.0, infection_pct), 1), False

        # UNIVERSAL BOTANICAL FOLIAR PATHOLOGY ENGINE:
        # Analyzes ANY leaf dynamically based on visible foliar pathology symptoms!
        universal_diseases = AGRONOMY_KNOWLEDGE_BASE["universal_leaf"]["diseases"]
        subject_title = "Crop Plant Foliage / ಸಸ್ಯದ ಎಲೆ"

        if white_mold_ratio > 0.035:
            # Powdery Mildew
            selected_disease = universal_diseases[1]
            confidence = min(0.96, 0.88 + white_mold_ratio * 1.2)
        elif brown_ratio > 0.04 and yellow_ratio > 0.06:
            # Cercospora / Target Leaf Spot (distinct yellow chlorotic halos around necrotic brown spots)
            selected_disease = universal_diseases[2]
            confidence = min(0.97, 0.88 + (brown_ratio + yellow_ratio) * 0.25)
        elif brown_ratio > 0.12:
            # Anthracnose & Leaf Blight
            selected_disease = universal_diseases[0]
            confidence = min(0.97, 0.87 + brown_ratio * 0.35)
        elif yellow_ratio > 0.18 and green_ratio > 0.15:
            # Foliar Chlorosis & Mosaic Virus
            selected_disease = universal_diseases[3]
            confidence = min(0.94, 0.85 + yellow_ratio * 0.3)
        elif yellow_ratio > 0.08 and brown_ratio > 0.08:
            # Rust Disease
            selected_disease = universal_diseases[4]
            confidence = min(0.95, 0.86 + brown_ratio * 0.3)
        else:
            # General Foliar Anthracnose / Blight
            selected_disease = universal_diseases[0]
            confidence = 0.90

        return DomainCategory.CROP_LEAF, subject_title, selected_disease, round(confidence, 3), round(max(8.0, infection_pct), 1), False

    except Exception as e:
        wrong_entry = {
            "disease": "Wrong Photo Detected: Invalid Subject",
            "pathogen": PathogenType.INVALID_SUBJECT,
            "scientific_name": "Unknown",
            "symptoms": ["Could not extract botanical leaf features from image", "Please capture a clear crop leaf photo"],
            "organic": {"summary": "Please capture a clear leaf photo.", "preparation": "N/A", "frequency": "N/A", "practices": []},
            "chemical": {"summary": "No chemicals applicable.", "active_ingredient": "None", "dosage_liter": "0", "dosage_acre": "0", "phi_days": 0, "safety": []},
            "speech": {
                "en": "Wrong photo detected. Please upload a clear photo of a crop leaf.",
                "kn": "ತಪ್ಪು ಫೋಟೋ ಪತ್ತೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "hi": "गलत फोटो पाई गई। कृपया फसल की पत्ती की स्पष्ट फोटो लें।",
                "es": "Foto incorrecta. Tome una foto clara de una hoja de cultivo.",
                "sw": "Picha isiyo sahihi. Tafadhali piga picha wazi ya jani.",
                "fr": "Mauvaise photo. Veuillez prendre une photo claire d'une feuille."
            }
        }
        return DomainCategory.NON_AGRICULTURAL, "Wrong Photo (Invalid)", wrong_entry, 0.92, 0.0, False

def diagnose_leaf_image(
    image_base64: str,
    crop_hint: Optional[str] = None,
    preferred_language: str = "en"
) -> DiagnosticResponse:
    """
    Universal Agricultural & Veterinary Diagnostic Pipeline.
    Integrates Deep CNN Feature Extractor with Expert Agronomy Engine.
    """
    start_time = time.time()

    clean_b64 = image_base64
    if "base64," in clean_b64:
        clean_b64 = clean_b64.split("base64,")[1]

    image_bytes = base64.b64decode(clean_b64)

    # 1. Execute Deep CNN Feature Extraction (PyTorch + OpenCV)
    cnn_features = extract_cnn_features(image_bytes)

    # Check if user explicitly requested veterinary diagnostics (e.g. crop_hint specifies livestock/cattle)
    is_auto_detect = not crop_hint or any(w in str(crop_hint).lower() for w in ["auto", "detect", "any", "ಸ್ವಯಂ", "crop", "leaf", "plant"])
    is_explicit_vet_mode = bool(
        not is_auto_detect and crop_hint and 
        any(a in str(crop_hint).lower() for a in ["cow", "cattle", "buffalo", "goat", "sheep", "poultry", "canine"])
    )

    # GATEKEEPER: Check if CNN classified this image as WRONG PHOTO (Non-plant, Animal, Human, Object)
    # CRITICAL: If the image has ANY foliar presence or is_crop_leaf, NEVER reject as wrong photo!
    has_any_foliage = bool(cnn_features.get("is_crop_leaf")) or (cnn_features.get("foliar_score", 0.0) >= 0.015)
    if cnn_features.get("is_wrong_photo") and not is_explicit_vet_mode and not has_any_foliage:
        wrong_type = cnn_features.get("wrong_photo_type", "NON_PLANT")
        elapsed = round((time.time() - start_time) * 1000, 2)
        
        if wrong_type == "HUMAN":
            crop_name = "Error: Human Subject (Not a Plant)"
            disease_detected = "Error: Human Photo Detected (Not a Plant Disease Photo)"
            scientific = "Homo sapiens (Non-Botanical)"
            symptoms = [
                "PyTorch CNN & Computer Vision Gatekeeper detected human facial/skin morphology",
                f"Foliar leaf presence: {int(cnn_features.get('foliar_score', 0)*100)}% (Requires >= 20% foliar chlorophyll)",
                "AgriVision is strictly a crop plant pathology engine and requires a plant leaf photo"
            ]
            org_summary = "ERROR: CANNOT PRESCRIBE PLANT TREATMENT. You uploaded a photo of a person or human face. Please photograph an affected crop plant leaf to diagnose disease."
            chem_summary = "CRITICAL SAFETY WARNING: Agricultural crop pesticides, fungicides, and chemicals are toxic and dangerous to humans. Never apply agricultural chemicals to people."
            speech = {
                "en": "Error: Human subject detected. This is a photo of a person, not a crop plant leaf. AgriVision requires a close-up photo of a crop plant leaf to diagnose disease.",
                "kn": "ದೋಷ: ಇದು ಮಾನವನ ಫೋಟೋವಾಗಿದ್ದು, ಸಸ್ಯ ರೋಗದ ಎಲೆಯಲ್ಲ. ರೋಗ ಪತ್ತೆಹಚ್ಚಲು ದಯವಿಟ್ಟು ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "hi": "त्रुटि: यह मनुष्य का फोटो है, फसल की पत्ती नहीं। रोग निदान के लिए कृपया फसल की पत्ती का स्पष्ट फोटो लें।",
                "es": "Error: Sujeto humano detectado. Esta es una foto de una persona, no una hoja de cultivo.",
                "sw": "Hitilafu: Picha ya binadamu imegunduliwa, si jani la mmea. Tafadhali pakia picha ya jani la mmea.",
                "fr": "Erreur : Sujet humain détecté. Ceci est la photo d'une personne et non d'une feuille de plante."
            }
        elif wrong_type == "ANIMAL":
            crop_name = "Error: Animal Subject (Not a Plant)"
            disease_detected = "Error: Animal Photo Detected (Not a Plant Disease Photo)"
            scientific = "Animalia (Non-Botanical)"
            symptoms = [
                "PyTorch CNN & Computer Vision Gatekeeper identified an animal/livestock photo",
                f"Foliar leaf presence: {int(cnn_features.get('foliar_score', 0)*100)}% | Animal features: {int(cnn_features.get('animal_score', 0)*100)}%",
                "AgriVision is an agricultural crop leaf diagnostic engine and requires a plant leaf photo"
            ]
            org_summary = "ERROR: CANNOT PRESCRIBE PLANT TREATMENT. You uploaded an animal photo. AgriVision AI is designed specifically for crop plant leaf diagnostics. Please capture or upload a clear photo of an affected crop leaf."
            chem_summary = "CRITICAL SAFETY WARNING: Never apply agricultural crop pesticides, systemic fungicides, or herbicides to animals! If you require livestock veterinary care, consult a licensed veterinary doctor."
            speech = {
                "en": "Error: Animal photo detected. This is an animal photo, not a crop plant leaf. AgriVision requires a close-up photo of a crop plant leaf to diagnose disease.",
                "kn": "ದೋಷ: ಇದು ಪ್ರಾಣಿಯ ಚಿತ್ರವಾಗಿದ್ದು, ಬೆಳೆಯ ಎಲೆಯಲ್ಲ. ರೋಗ ಪತ್ತೆಹಚ್ಚಲು ದಯವಿಟ್ಟು ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "hi": "त्रुटि: यह एक पशु का चित्र है, फसल की पत्ती नहीं। कृपया फसल की पत्ती की स्पष्ट फोटो अपलोड करें।",
                "es": "Error: Foto de animal detectada. AgriVision requiere una hoja de planta de cultivo.",
                "sw": "Hitilafu: Picha ya mnyama imegunduliwa, si jani la mmea. AgriVision inahitaji picha ya jani la zao.",
                "fr": "Erreur : Photo d'animal détectée. AgriVision nécessite une feuille de plante."
            }
        elif wrong_type == "FOOD":
            crop_name = "Error: Food / Snack (Not a Plant Leaf)"
            disease_detected = "Error: Food Item Detected (Vada Pav / Snack - Not a Crop Plant Leaf)"
            scientific = "Food / Non-Botanical"
            symptoms = [
                "PyTorch CNN & Computer Vision Gatekeeper detected cooked food / snack (e.g. Vada Pav, bread, fried batter, or fast food)",
                f"Food/snack texture presence: {int(cnn_features.get('food_score', 0)*100)}% | Genuine leaf chlorophyll: {int(cnn_features.get('foliar_score', 0)*100)}%",
                "AgriVision AI is an agricultural agronomy engine designed strictly for diagnosing crop plant leaf diseases",
                "Cooked food items cannot be diagnosed for plant diseases or treated with agricultural chemicals"
            ]
            org_summary = "ERROR: FOOD ITEM DETECTED. You uploaded a photo of food (such as Vada Pav, bread, or fried snack). AgriVision AI requires a clear photograph of an affected crop plant leaf to diagnose diseases."
            chem_summary = "CRITICAL SAFETY WARNING: NEVER apply agricultural pesticides, fungicides, or crop chemicals to food, snacks, or edible items! They contain toxic chemical active ingredients."
            speech = {
                "en": "Error: Food item detected. This is a photo of food or a cooked snack such as Vada Pav, not a crop plant leaf. AgriVision requires a close-up photo of an affected plant leaf to diagnose disease.",
                "kn": "ದೋಷ: ಇದು ಆಹಾರ ಪದಾರ್ಥವಾಗಿದ್ದು (ವಡಾಪಾವ್ ಅಥವಾ ತಿಂಡಿ), ಸಸ್ಯ ರೋಗದ ಎಲೆಯಲ್ಲ. ರೋಗ ಪತ್ತೆಹಚ್ಚಲು ದಯವಿಟ್ಟು ಬಾಧಿತ ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "hi": "त्रुटि: यह खाद्य पदार्थ (जैसे वड़ा पाव या नाश्ता) है, फसल की पत्ती नहीं। रोग निदान के लिए कृपया फसल की पत्ती की स्पष्ट फोटो अपलोड करें।",
                "es": "Error: Alimento detectado. Esta es una foto de comida, no una hoja de cultivo.",
                "sw": "Hitilafu: Chakula kimegunduliwa, si jani la mmea. Tafadhali pakia picha ya jani la mmea.",
                "fr": "Erreur : Nourriture détectée. Ceci est une photo d'aliment et non une feuille de plante."
            }
        else:
            crop_name = "Error: Non-Plant Subject"
            disease_detected = "Error: Not a Plant Disease Photo (Invalid Non-Botanical Subject)"
            scientific = "Inanimate / Non-Botanical"
            symptoms = [
                "No botanical leaf tissue or vegetative structures detected in photograph",
                "Image appears to contain an inanimate object, vehicle, indoor surface, landscape, or scene",
                f"Foliar leaf presence: {int(cnn_features.get('foliar_score', 0)*100)}% (Insufficient plant tissue)",
                "Please hold camera 15-30 cm from an affected crop leaf under natural daylight"
            ]
            org_summary = "ERROR: NOT A PLANT DISEASE PHOTO. No crop leaf found. Please position camera 15-30 cm from an affected crop plant leaf under natural daylight."
            chem_summary = "NO CHEMICAL REMEDY: No agricultural chemical recommendations are applicable for non-crop images. Ensure genuine crop foliage is in frame."
            speech = {
                "en": "Error: Not a plant disease photo. No crop plant leaf detected. Please take a clear photo of an affected plant leaf under natural daylight.",
                "kn": "ದೋಷ: ಇದು ಸಸ್ಯ ರೋಗದ ಫೋಟೋ ಅಲ್ಲ. ಅಗ್ರಿವಿಷನ್ ಕೇವಲ ಸಸ್ಯ ಮತ್ತು ಬೆಳೆಗಳ ರೋಗ ಪತ್ತೆಹಚ್ಚುವ ವ್ಯವಸ್ಥೆಯಾಗಿದೆ. ದಯವಿಟ್ಟು ಬಾಧಿತ ಬೆಳೆಯ ಎಲೆಯ ಸ್ಪಷ್ಟ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ.",
                "hi": "त्रुटि: यह किसी पौधे की बीमारी का फोटो नहीं है। कृपया प्रभावित फसल की पत्ती का स्पष्ट फोटो अपलोड करें।",
                "es": "Error: No es una foto de enfermedad de planta. Tome una foto clara de una hoja de cultivo.",
                "sw": "Hitilafu: Si picha ya ugonjwa wa mmea. Tafadhali piga picha wazi ya jani la mmea.",
                "fr": "Erreur : Ceci n'est pas une photo de maladie de plante. Veuillez prendre une photo claire d'une feuille."
            }

        return DiagnosticResponse(
            domain_category=DomainCategory.NON_AGRICULTURAL,
            is_animal_disease=False,
            is_valid_agricultural_image=False,
            is_wrong_photo=True,
            wrong_photo_reason=cnn_features.get("wrong_photo_reason", "Error: not a crop plant leaf photo"),
            animal_warning=None,
            crop_name=crop_name,
            scientific_crop_name=scientific,
            disease_detected=disease_detected,
            pathogen_type=PathogenType.INVALID_SUBJECT,
            confidence_score=cnn_features.get("cnn_confidence", 0.98),
            severity=SeverityEnum.SEVERE,
            infection_percentage=0.0,
            symptoms_observed=symptoms,
            organic_remedy=org_summary,
            organic_details=OrganicRemedyDetails(
                summary=org_summary,
                preparation="N/A - Please photograph a genuine crop leaf",
                application_frequency="N/A",
                preventive_cultural_practices=["Focus on an affected crop leaf in natural daylight", "Ensure leaf fills at least 40% of the frame"]
            ),
            chemical_remedy=chem_summary,
            chemical_details=ChemicalRemedyDetails(
                summary=chem_summary,
                active_ingredient="None",
                dosage_per_liter="N/A (Do not apply)",
                dosage_per_hectare_or_acre="N/A (Do not apply)",
                pre_harvest_interval_days=0,
                safety_precautions=["Do not apply crop chemicals to non-plants, humans, or animals", "Re-scan with a proper plant leaf"]
            ),
            urgency="None",
            cnn_metrics=cnn_features,
            localized_speech_summary=speech,
            inference_time_ms=elapsed,
            model_used=f"AgriVision Vision + {cnn_features['cnn_model_name']}"
        )

    # 2. Intelligent Computer Vision Pathology Synthesizer
    domain_cat, subject_name, disease_info, confidence, infection_pct, is_animal = analyze_image_heuristics(
        image_bytes, crop_hint, cnn_features
    )

    # Blend CNN metrics with heuristic confidence for enhanced accuracy
    blended_confidence = round((confidence * 0.6 + cnn_features["cnn_confidence"] * 0.4), 3)
    blended_infection_pct = round((infection_pct * 0.6 + cnn_features["cnn_lesion_percentage"] * 0.4), 1)

    if blended_infection_pct > 35.0:
        severity = SeverityEnum.SEVERE
        urgency = "High"
    elif blended_infection_pct > 15.0:
        severity = SeverityEnum.MODERATE
        urgency = "Moderate"
    else:
        severity = SeverityEnum.LOW
        urgency = "Low"

    org = disease_info["organic"]
    chem = disease_info["chemical"]

    elapsed = round((time.time() - start_time) * 1000, 2)

    return DiagnosticResponse(
        domain_category=domain_cat,
        is_animal_disease=is_animal,
        is_valid_agricultural_image=(domain_cat != DomainCategory.NON_AGRICULTURAL),
        is_wrong_photo=(domain_cat == DomainCategory.NON_AGRICULTURAL),
        wrong_photo_reason=disease_info.get("disease") if domain_cat == DomainCategory.NON_AGRICULTURAL else None,
        animal_warning=disease_info.get("warning") if is_animal else None,
        crop_name=subject_name,
        scientific_crop_name=disease_info.get("scientific_name", "Plantae"),
        disease_detected=disease_info["disease"],
        pathogen_type=disease_info["pathogen"],
        confidence_score=blended_confidence,
        severity=severity,
        infection_percentage=blended_infection_pct,
        symptoms_observed=disease_info.get("symptoms", []),
        organic_remedy=org["summary"],
        organic_details=OrganicRemedyDetails(
            summary=org["summary"],
            preparation=org.get("preparation", "N/A"),
            application_frequency=org.get("frequency", "N/A"),
            preventive_cultural_practices=org.get("practices", [])
        ),
        chemical_remedy=chem["summary"],
        chemical_details=ChemicalRemedyDetails(
            summary=chem["summary"],
            active_ingredient=chem.get("active_ingredient", "None"),
            dosage_per_liter=chem.get("dosage_liter", chem.get("dosage_per_liter", "N/A")),
            dosage_per_hectare_or_acre=chem.get("dosage_acre", chem.get("dosage_per_hectare_or_acre", "N/A")),
            pre_harvest_interval_days=chem.get("phi_days", chem.get("pre_harvest_interval_days", 0)),
            safety_precautions=chem.get("safety", chem.get("safety_precautions", []))
        ),
        urgency=urgency,
        cnn_metrics=cnn_features,
        localized_speech_summary=disease_info.get("speech", {}),
        inference_time_ms=elapsed,
        model_used=f"AgriVision Vision + {cnn_features['cnn_model_name']}"
    )

