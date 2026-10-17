"use client";

import React from "react";
import { 
  Scan, 
  MapPin, 
  History, 
  BarChart3, 
  Languages, 
  Sparkles,
  Zap
} from "lucide-react";
import { TRANSLATIONS, SupportedLanguage } from "../i18n";

interface NavbarProps {
  activeTab: "scan" | "map" | "history" | "analytics";
  setActiveTab: (tab: "scan" | "map" | "history" | "analytics") => void;
  selectedLanguage: string;
  setSelectedLanguage: (lang: string) => void;
  serverOnline: boolean;
}

const LANGUAGES = [
  { code: "kn", label: "ಕನ್ನಡ (Kannada)", flag: "🇮🇳" },
  { code: "en", label: "English", flag: "🇬🇧" },
  { code: "hi", label: "हिंदी (Hindi)", flag: "🇮🇳" },
  { code: "es", label: "Español", flag: "🇪🇸" },
  { code: "sw", label: "Kiswahili", flag: "🇰🇪" },
  { code: "fr", label: "Français", flag: "🇫🇷" },
];

export default function Navbar({
  activeTab,
  setActiveTab,
  selectedLanguage,
  setSelectedLanguage,
  serverOnline,
}: NavbarProps) {
  const langKey = (LANGUAGES.some(l => l.code === selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-emerald-900/40 px-4 lg:px-8 py-3">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
        {/* Brand & Status */}
        <div className="flex items-center justify-between w-full md:w-auto">
          <div 
            onClick={() => setActiveTab("scan")}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-emerald-600 to-green-800 shadow-lg shadow-emerald-900/40 border border-emerald-400/30 group-hover:scale-105 transition-transform">
              <Sparkles className="w-5 h-5 text-emerald-200 animate-pulse" />
              <div className="absolute inset-0 rounded-xl bg-emerald-400/20 animate-pulse-ring" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold text-lg tracking-tight bg-gradient-to-r from-emerald-300 via-green-200 to-teal-300 bg-clip-text text-transparent">
                  {t.brand.title}
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded-full bg-emerald-950/80 text-emerald-400 border border-emerald-500/30">
                  {t.brand.universalCore}
                </span>
              </div>
              <p className="text-xs text-emerald-300/60 font-medium">
                {t.brand.tagline}
              </p>
            </div>
          </div>

          {/* Mobile Server status badge */}
          <div className="flex items-center gap-1.5 md:hidden text-xs px-2.5 py-1 rounded-full bg-emerald-950/60 border border-emerald-800/40">
            <span className={`w-2 h-2 rounded-full ${serverOnline ? "bg-emerald-400 animate-pulse" : "bg-amber-400"}`} />
            <span className="text-emerald-300/80 text-[11px]">
              {serverOnline ? t.brand.online : t.brand.connecting}
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="flex items-center gap-1.5 p-1 rounded-xl bg-black/40 border border-emerald-900/40 text-xs sm:text-sm font-medium w-full md:w-auto overflow-x-auto">
          <button
            onClick={() => setActiveTab("scan")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "scan"
                ? "bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-md shadow-emerald-900/50 font-semibold"
                : "text-emerald-300/70 hover:text-emerald-200 hover:bg-emerald-950/40"
            }`}
          >
            <Scan className="w-4 h-4" />
            <span>{t.nav.scan}</span>
          </button>

          <button
            onClick={() => setActiveTab("map")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "map"
                ? "bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-md shadow-emerald-900/50 font-semibold"
                : "text-emerald-300/70 hover:text-emerald-200 hover:bg-emerald-950/40"
            }`}
          >
            <MapPin className="w-4 h-4" />
            <span>{t.nav.map}</span>
          </button>

          <button
            onClick={() => setActiveTab("history")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "history"
                ? "bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-md shadow-emerald-900/50 font-semibold"
                : "text-emerald-300/70 hover:text-emerald-200 hover:bg-emerald-950/40"
            }`}
          >
            <History className="w-4 h-4" />
            <span>{t.nav.history}</span>
          </button>

          <button
            onClick={() => setActiveTab("analytics")}
            className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg transition-all whitespace-nowrap cursor-pointer ${
              activeTab === "analytics"
                ? "bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-md shadow-emerald-900/50 font-semibold"
                : "text-emerald-300/70 hover:text-emerald-200 hover:bg-emerald-950/40"
            }`}
          >
            <BarChart3 className="w-4 h-4" />
            <span>{t.nav.analytics}</span>
          </button>
        </nav>

        {/* Right Tools: Language Picker & Server Status */}
        <div className="hidden md:flex items-center gap-3">
          {/* Language selector */}
          <div className="relative flex items-center gap-2 px-3 py-1.5 rounded-xl bg-black/40 border border-emerald-900/50">
            <Languages className="w-3.5 h-3.5 text-emerald-400" />
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="bg-transparent text-xs text-emerald-200 font-semibold focus:outline-none cursor-pointer pr-1"
            >
              {LANGUAGES.map((lang) => (
                <option key={lang.code} value={lang.code} className="bg-[#0b1d14] text-white">
                  {lang.flag} {lang.label}
                </option>
              ))}
            </select>
          </div>

          {/* Deep CNN & Core status indicator */}
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-black/40 border border-emerald-900/50">
            <div className="relative flex items-center justify-center">
              <span className={`w-2.5 h-2.5 rounded-full ${serverOnline ? "bg-emerald-400" : "bg-amber-400 animate-ping"}`} />
              {serverOnline && <span className="absolute w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping opacity-75" />}
            </div>
            <div className="flex flex-col">
              <span className="text-[11px] font-bold text-emerald-200 leading-none">
                {serverOnline ? t.brand.coreActive : t.brand.connecting}
              </span>
              <span className="text-[9px] text-emerald-400/70 font-mono mt-0.5">
                {t.brand.deepCnnActive}
              </span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
