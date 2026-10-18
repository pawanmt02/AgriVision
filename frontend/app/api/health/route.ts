import { NextResponse } from "next/server";

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    service: "AgriVision AI Core (Vercel Serverless & Edge API)",
    version: "1.0.0",
    environment: process.env.VERCEL ? "vercel-production" : "local",
    timestamp: new Date().toISOString(),
  });
}
