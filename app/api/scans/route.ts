import { NextResponse } from "next/server";

export async function GET() {
  const now = new Date();
  return NextResponse.json([
    {
      id: "scan-live-1",
      crop_name: "Arecanut (ಅಡಿಕೆ)",
      disease_detected: "Arecanut Fruit Rot / Koleroga (Phytophthora meadii)",
      severity: "Severe",
      confidence_score: 0.96,
      latitude: 13.9299,
      longitude: 75.5681,
      scanned_at: new Date(now.getTime() - 1000 * 60 * 18).toISOString(),
      organic_remedy: "1% Bordeaux mixture pre-monsoon foliar application + tying polythene covers.",
      chemical_remedy: "Metalaxyl 8% + Mancozeb 64% WP (2.5 g/L)."
    },
    {
      id: "scan-live-2",
      crop_name: "Ragi (ರಾಗಿ)",
      disease_detected: "Finger Millet / Ragi Blast (Pyricularia grisea)",
      severity: "Severe",
      confidence_score: 0.94,
      latitude: 12.5230,
      longitude: 76.8970,
      scanned_at: new Date(now.getTime() - 1000 * 60 * 45).toISOString(),
      organic_remedy: "Pseudomonas fluorescens 10g/L spray at early tillering stage.",
      chemical_remedy: "Tricyclazole 75% WP @ 0.6 g/L."
    },
    {
      id: "scan-live-3",
      crop_name: "Tomato",
      disease_detected: "Late Blight (Phytophthora infestans)",
      severity: "Severe",
      confidence_score: 0.95,
      latitude: 13.1367,
      longitude: 78.1340,
      scanned_at: new Date(now.getTime() - 1000 * 60 * 120).toISOString(),
      organic_remedy: "Copper soap spray + prune bottom 30cm dense foliage.",
      chemical_remedy: "Cymoxanil 8% + Mancozeb 64% WP (2.5 g/L)."
    }
  ]);
}
