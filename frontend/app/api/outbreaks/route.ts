import { NextResponse, NextRequest } from "next/server";

const OUTBREAK_CLUSTERS = [
  {
    cluster_id: "cluster-karnataka-koleroga",
    crop: "Arecanut (ಅಡಿಕೆ)",
    disease: "Arecanut Fruit Rot / Koleroga (Phytophthora meadii)",
    severity: "Severe",
    case_count: 58,
    center_latitude: 13.9299,
    center_longitude: 75.5681,
    radius_km: 45.0,
    risk_level: "High",
    alert_summary: "Severe monsoon Koleroga outbreak in Malnad region (Shimoga, Thirthahalli). Prophylactic 1% Bordeaux mixture spray required.",
    last_reported: new Date().toISOString()
  },
  {
    cluster_id: "cluster-karnataka-ragi-blast",
    crop: "Ragi (ರಾಗಿ)",
    disease: "Finger Millet / Ragi Blast (Pyricularia grisea)",
    severity: "Severe",
    case_count: 42,
    center_latitude: 12.5230,
    center_longitude: 76.8970,
    radius_km: 38.0,
    risk_level: "High",
    alert_summary: "Ragi leaf & neck blast detected across Mandya-Mysuru belt during humid morning dew periods.",
    last_reported: new Date().toISOString()
  },
  {
    cluster_id: "cluster-kolar-tomato-blight",
    crop: "Tomato",
    disease: "Late Blight (Phytophthora infestans)",
    severity: "Severe",
    case_count: 36,
    center_latitude: 13.1367,
    center_longitude: 78.1340,
    radius_km: 25.0,
    risk_level: "High",
    alert_summary: "Overcast skies trigger rapid Late Blight spread across Kolar tomato greenhouses. Saaf / Cymoxanil spray advised.",
    last_reported: new Date().toISOString()
  },
  {
    cluster_id: "cluster-dharwad-chilli",
    crop: "Chilli",
    disease: "Chilli Leaf Curl Virus (Thrips / Whiteflies)",
    severity: "Moderate",
    case_count: 29,
    center_latitude: 15.4589,
    center_longitude: 75.0078,
    radius_km: 30.0,
    risk_level: "Medium",
    alert_summary: "Upward curling and vector surge observed in Byadagi & Dharwad chilli fields.",
    last_reported: new Date().toISOString()
  },
  {
    cluster_id: "cluster-punjab-paddy",
    crop: "Rice (Paddy)",
    disease: "Bacterial Leaf Blight (Xanthomonas oryzae)",
    severity: "Severe",
    case_count: 45,
    center_latitude: 30.9010,
    center_longitude: 75.8573,
    radius_km: 50.0,
    risk_level: "High",
    alert_summary: "Rapid straw-yellow lesion progression in irrigated Basmati tracts.",
    last_reported: new Date().toISOString()
  }
];

export async function GET() {
  return NextResponse.json(OUTBREAK_CLUSTERS);
}
