import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AgriVision AI – Universal Crop Disease Diagnostic & Agronomy Engine",
  description: "Next-generation agricultural diagnostics powered by multi-modal vision and localized agronomy synthesis.",
  manifest: "/manifest.json",
  icons: {
    icon: "/leaf-icon.svg",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full dark">
      <head>
        <meta name="theme-color" content="#09130d" />
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1" />
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossOrigin="" />
      </head>
      <body className="min-h-full flex flex-col bg-[#09130d] text-[#e6f4ea] antialiased selection:bg-emerald-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
