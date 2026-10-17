import { NextResponse } from "next/server";

const SAMPLES = [
  {
    id: "sample-1",
    title: "Tomato Late Blight",
    crop: "Tomato",
    domain: "Plant Leaf",
    expected_disease: "Late Blight (Phytophthora infestans)",
    expected_severity: "Severe",
    thumbnail_color: "#b71c1c",
    image_data: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320' viewBox='0 0 320 320'><rect width='320' height='320' fill='%23f2f6f3'/><ellipse cx='160' cy='160' rx='100' ry='120' fill='%2343a047' stroke='%231b5e20' stroke-width='4'/><line x1='160' y1='45' x2='160' y2='275' stroke='%231b5e20' stroke-width='3'/><ellipse cx='120' cy='115' rx='35' ry='40' fill='%233e2723'/><ellipse cx='200' cy='180' rx='35' ry='40' fill='%232c1c19'/><circle cx='120' cy='115' r='38' fill='none' stroke='%23eceff1' stroke-width='3'/></svg>",
    description: "Large water-soaked dark brown necrotic lesions with white sporulation halo."
  },
  {
    id: "sample-2",
    title: "Potato Early Blight",
    crop: "Potato",
    domain: "Plant Leaf",
    expected_disease: "Early Blight (Alternaria solani)",
    expected_severity: "Moderate",
    thumbnail_color: "#e65100",
    image_data: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320' viewBox='0 0 320 320'><rect width='320' height='320' fill='%23f2f6f3'/><ellipse cx='160' cy='160' rx='95' ry='115' fill='%234caf50' stroke='%232e7d32' stroke-width='4'/><line x1='160' y1='50' x2='160' y2='270' stroke='%231b5e20' stroke-width='3'/><circle cx='125' cy='125' r='30' fill='%23fdd835'/><circle cx='125' cy='125' r='20' fill='%236d4c41'/><circle cx='125' cy='125' r='10' fill='%232e1b18'/></svg>",
    description: "Concentric dark 'target board' rings with chlorotic yellow surrounding margins."
  },
  {
    id: "sample-3",
    title: "Rice Bacterial Leaf Blight",
    crop: "Rice",
    domain: "Plant Leaf",
    expected_disease: "Bacterial Leaf Blight (Xanthomonas oryzae)",
    expected_severity: "Severe",
    thumbnail_color: "#f57f17",
    image_data: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320' viewBox='0 0 320 320'><rect width='320' height='320' fill='%23f5f8f5'/><polygon points='140,30 180,30 200,290 120,290' fill='%234caf50' stroke='%232e7d32' stroke-width='3'/><polygon points='140,30 155,30 150,180 130,160' fill='%23ffee58'/><polygon points='165,30 180,30 195,200 170,170' fill='%23ffee58'/></svg>",
    description: "Wavy straw-yellow margins starting from leaf tips and drying downwards."
  },
  {
    id: "sample-4",
    title: "Arecanut Koleroga (ಅಡಿಕೆ ಕೊಳೆರೋಗ)",
    crop: "Arecanut",
    domain: "Plant Fruit",
    expected_disease: "Arecanut Fruit Rot / Koleroga (Phytophthora meadii)",
    expected_severity: "Severe",
    thumbnail_color: "#15803d",
    image_data: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320' viewBox='0 0 320 320'><rect width='320' height='320' fill='%23f2f6f3'/><ellipse cx='160' cy='160' rx='80' ry='100' fill='%23388e3c'/><circle cx='160' cy='130' r='40' fill='%231b5e20'/><circle cx='160' cy='130' r='30' fill='%234e342e'/><circle cx='160' cy='130' r='20' fill='%23fafafa'/></svg>",
    description: "Karnataka staple crop: Water-soaked rotting of arecanuts with white mycelial growth."
  },
  {
    id: "sample-5",
    title: "Ragi Blast (ರಾಗಿ ಬೆಂಕಿ ರೋಗ)",
    crop: "Ragi",
    domain: "Plant Leaf",
    expected_disease: "Finger Millet / Ragi Blast (Pyricularia grisea)",
    expected_severity: "Severe",
    thumbnail_color: "#a16207",
    image_data: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320' viewBox='0 0 320 320'><rect width='320' height='320' fill='%23f2f6f3'/><polygon points='130,20 190,20 220,300 100,300' fill='%234caf50'/><ellipse cx='155' cy='130' rx='25' ry='10' fill='%235d4037'/><ellipse cx='165' cy='200' rx='28' ry='12' fill='%235d4037'/></svg>",
    description: "Karnataka staple grain: Spindle-shaped blast lesions on finger millet leaf blade."
  },
  {
    id: "sample-6",
    title: "Healthy Crop Leaf",
    crop: "Healthy",
    domain: "Plant Leaf",
    expected_disease: "Healthy Plant Leaf - No Pathogen Detected",
    expected_severity: "Low",
    thumbnail_color: "#1b5e20",
    image_data: "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='320' height='320' viewBox='0 0 320 320'><rect width='320' height='320' fill='%23f2f6f3'/><ellipse cx='160' cy='160' rx='105' ry='125' fill='%232e7d32' stroke='%231b5e20' stroke-width='4'/><line x1='160' y1='40' x2='160' y2='280' stroke='%23388e3c' stroke-width='4'/><line x1='160' y1='100' x2='100' y2='80' stroke='%2343a047' stroke-width='2'/><line x1='160' y1='100' x2='220' y2='80' stroke='%2343a047' stroke-width='2'/><line x1='160' y1='160' x2='80' y2='140' stroke='%2343a047' stroke-width='2'/><line x1='160' y1='160' x2='240' y2='140' stroke='%2343a047' stroke-width='2'/></svg>",
    description: "Lush uniform chlorophyll pigmentation with zero necrotic spots or fungal mycelium."
  }
];

export async function GET() {
  return NextResponse.json(SAMPLES);
}
