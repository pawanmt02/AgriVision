"use client";

import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import LeafScanner from "./components/LeafScanner";
import DiagnosticCard from "./components/DiagnosticCard";
import OutbreakMap from "./components/OutbreakMap";
import ScanHistory from "./components/ScanHistory";
import PathologyAnalytics from "./components/PathologyAnalytics";
import { 
  DiagnosticResponse, 
  SampleLeaf, 
  OutbreakCluster, 
  DiseaseScanHistoryItem, 
  AnalyticsSummary 
} from "./types";
import { TRANSLATIONS, SupportedLanguage } from "./i18n";
import { Sparkles, Leaf, MapPin, History, BarChart3, Wifi, WifiOff } from "lucide-react";

const resolveBackendUrl = (): string => {
  if (process.env.NEXT_PUBLIC_BACKEND_URL) {
    return process.env.NEXT_PUBLIC_BACKEND_URL;
  }
  if (typeof window !== "undefined") {
    if (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1") {
      return "http://localhost:8005";
    }
    // On Vercel / production domain, use built-in Next.js Serverless API routes
    return "";
  }
  return "http://localhost:8005";
};

export default function Home() {
  const [activeTab, setActiveTab] = useState<"scan" | "map" | "history" | "analytics">("scan");
  const [selectedLanguage, setSelectedLanguage] = useState<string>("en");
  const langKey = (["kn", "en", "hi", "es", "sw", "fr"].includes(selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;
  const [serverOnline, setServerOnline] = useState<boolean>(false);
  const [currentDiagnostic, setCurrentDiagnostic] = useState<DiagnosticResponse | null>(null);
  const [backendUrl] = useState<string>(resolveBackendUrl);
  
  // Data states
  const [sampleImages, setSampleImages] = useState<SampleLeaf[]>([]);
  const [outbreaks, setOutbreaks] = useState<OutbreakCluster[]>([]);
  const [scans, setScans] = useState<DiseaseScanHistoryItem[]>([]);
  const [analytics, setAnalytics] = useState<AnalyticsSummary | null>(null);
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);

  const checkHealth = async (url: string = backendUrl) => {
    try {
      const res = await fetch(`${url}/api/health`, { method: "GET" });
      if (res.ok) {
        setServerOnline(true);
      } else {
        setServerOnline(false);
      }
    } catch {
      setServerOnline(false);
    }
  };

  const fetchSampleImages = async (url: string = backendUrl) => {
    try {
      const res = await fetch(`${url}/api/sample-images`);
      if (res.ok) {
        const data = await res.json();
        setSampleImages(data);
      }
    } catch (e) {
      console.log("Using cached sample images");
    }
  };

  const fetchOutbreaks = async (url: string = backendUrl) => {
    try {
      const res = await fetch(`${url}/api/outbreaks`);
      if (res.ok) {
        const data = await res.json();
        setOutbreaks(data);
      }
    } catch (e) {
      console.log("Could not load outbreaks");
    }
  };

  const fetchScans = async (url: string = backendUrl) => {
    try {
      const res = await fetch(`${url}/api/scans`);
      if (res.ok) {
        const data = await res.json();
        setScans(data);
      }
    } catch (e) {
      console.log("Could not load scans");
    }
  };

  const fetchAnalytics = async (url: string = backendUrl) => {
    try {
      const res = await fetch(`${url}/api/analytics`);
      if (res.ok) {
        const data = await res.json();
        setAnalytics(data);
      }
    } catch (e) {
      console.log("Could not load analytics");
    }
  };

  // Initialize and check backend connection
  useEffect(() => {
    queueMicrotask(() => {
      checkHealth();
      fetchSampleImages();
      fetchOutbreaks();
      fetchScans();
      fetchAnalytics();

      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            setUserLocation({
              lat: pos.coords.latitude,
              lng: pos.coords.longitude,
            });
          },
          () => {
            setUserLocation({ lat: 28.6139, lng: 77.2090 });
          }
        );
      }
    });
  }, []);

  const handleDiagnosisComplete = (diagnostic: DiagnosticResponse) => {
    setCurrentDiagnostic(diagnostic);
    // Refresh history, outbreaks, analytics in background
    fetchScans(backendUrl);
    fetchOutbreaks(backendUrl);
    fetchAnalytics(backendUrl);
  };

  const handleLocateOnMap = () => {
    setActiveTab("map");
  };

  const handleResetScan = () => {
    setCurrentDiagnostic(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#09130d] text-[#e6f4ea] relative">
      {/* Dynamic Background Mesh Gradients */}
      <div className="fixed inset-0 pointer-events-none z-0">
        <div className="absolute top-0 left-1/4 w-[600px] h-[600px] bg-emerald-600/10 rounded-full blur-[140px]" />
        <div className="absolute bottom-1/3 right-1/4 w-[500px] h-[500px] bg-green-500/8 rounded-full blur-[160px]" />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-teal-900/10 rounded-full blur-[180px]" />
      </div>

      {/* Navigation Header */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        selectedLanguage={selectedLanguage}
        setSelectedLanguage={setSelectedLanguage}
        serverOnline={serverOnline}
      />

      {/* Main App Content Viewports */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 relative z-10 space-y-8">
        {/* Tab 1: Scan & Diagnose */}
        {activeTab === "scan" && (
          <div className="space-y-8">
            {currentDiagnostic ? (
              <DiagnosticCard
                diagnostic={currentDiagnostic}
                selectedLanguage={selectedLanguage}
                onLocateOnMap={handleLocateOnMap}
                onResetScan={handleResetScan}
              />
            ) : (
              <LeafScanner
                onDiagnosticComplete={handleDiagnosisComplete}
                selectedLanguage={selectedLanguage}
                sampleImages={sampleImages}
                backendUrl={backendUrl}
              />
            )}
          </div>
        )}

        {/* Tab 2: Outbreak GIS Map */}
        {activeTab === "map" && (
          <OutbreakMap
            outbreaks={outbreaks}
            userLocation={userLocation}
            onRefresh={fetchOutbreaks}
            selectedLanguage={selectedLanguage}
          />
        )}

        {/* Tab 3: Scan History */}
        {activeTab === "history" && (
          <ScanHistory scans={scans} selectedLanguage={selectedLanguage} />
        )}

        {/* Tab 4: Analytics */}
        {activeTab === "analytics" && (
          <PathologyAnalytics analytics={analytics} selectedLanguage={selectedLanguage} />
        )}
      </main>

      {/* Modern AgriVision Footer */}
      <footer className="mt-auto border-t border-emerald-950/80 glass-panel py-6 px-4 text-center text-xs text-emerald-400/60 relative z-10">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-emerald-300">{t.brand.title}</span>
            <span>•</span>
            <span>{t.footer.tagline}</span>
          </div>
          <div className="flex items-center gap-4 text-[11px] text-emerald-400/80">
            <span>{t.footer.fastapi}</span>
            <span>•</span>
            <span>{t.footer.groq}</span>
            <span>•</span>
            <span>{t.footer.postgis}</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
