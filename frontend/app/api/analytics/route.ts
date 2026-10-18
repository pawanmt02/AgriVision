import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    total_scans: 1420,
    total_outbreaks: 5,
    severity_distribution: {
      Severe: 64,
      Moderate: 28,
      Low: 8
    },
    top_affected_crops: [
      { crop: "Tomato", cases: 38 },
      { crop: "Arecanut (ಅಡಿಕೆ)", cases: 34 },
      { crop: "Ragi (ರಾಗಿ)", cases: 26 },
      { crop: "Rice (Paddy)", cases: 22 },
      { crop: "Potato", cases: 18 }
    ],
    common_pathogens: {
      Fungal: 72,
      Bacterial: 16,
      Viral: 9,
      Pest: 3
    },
    recent_activity_count: 24
  });
}
