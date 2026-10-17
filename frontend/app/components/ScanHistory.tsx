"use client";

import React, { useState } from "react";
import { 
  History, 
  Search, 
  Filter, 
  Download, 
  Leaf, 
  Calendar, 
  MapPin, 
  ChevronDown, 
  ChevronUp, 
  Sprout, 
  FlaskConical,
  Sparkles
} from "lucide-react";
import { DiseaseScanHistoryItem } from "../types";
import { TRANSLATIONS, SupportedLanguage } from "../i18n";

interface ScanHistoryProps {
  scans: DiseaseScanHistoryItem[];
  onSelectCropForScan?: (crop: string) => void;
  selectedLanguage?: string;
}

export default function ScanHistory({ scans, selectedLanguage = "en" }: ScanHistoryProps) {
  const langKey = (["kn", "en", "hi", "es", "sw", "fr"].includes(selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;

  const [searchTerm, setSearchTerm] = useState<string>("");
  const [selectedSeverity, setSelectedSeverity] = useState<string>("All");
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const filteredScans = scans.filter((scan) => {
    const matchesSearch = 
      scan.crop_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      scan.disease_detected.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSeverity = selectedSeverity === "All" || scan.severity === selectedSeverity;
    return matchesSearch && matchesSeverity;
  });

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const exportHistoryJSON = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(filteredScans, null, 2));
    const downloadAnchor = document.createElement("a");
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", `agrivision_field_scans_${new Date().toISOString().slice(0, 10)}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="space-y-6">
      {/* Top Header & Search Bar */}
      <div className="glass-panel-elevated rounded-3xl p-5 border border-emerald-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <History className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-extrabold text-white">
              {t.history.title}
            </h3>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-500/30">
              {scans.length} {t.history.totalRecords}
            </span>
          </div>
          <p className="text-xs text-emerald-300/70 mt-0.5">
            {t.history.subtitle}
          </p>
        </div>

        {/* Actions: Search, Filter, Export */}
        <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto">
          {/* Search box */}
          <div className="relative flex items-center bg-black/50 border border-emerald-900/50 rounded-xl px-3 py-1.5 text-xs text-emerald-200">
            <Search className="w-3.5 h-3.5 text-emerald-400 mr-2" />
            <input
              type="text"
              placeholder={t.history.searchPlaceholder}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-transparent focus:outline-none placeholder:text-emerald-500/60 w-36 sm:w-48"
            />
          </div>

          {/* Severity filter */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/50 border border-emerald-900/50 text-xs">
            <Filter className="w-3.5 h-3.5 text-emerald-400" />
            <select
              value={selectedSeverity}
              onChange={(e) => setSelectedSeverity(e.target.value)}
              className="bg-transparent text-emerald-200 font-semibold focus:outline-none cursor-pointer"
            >
              <option value="All" className="bg-[#0b1d14] text-white">{t.map.allSeverities}</option>
              <option value="Severe" className="bg-[#0b1d14] text-white">{t.map.severeOnly}</option>
              <option value="Moderate" className="bg-[#0b1d14] text-white">{t.map.moderate}</option>
              <option value="Low" className="bg-[#0b1d14] text-white">{t.map.lowHealthy}</option>
            </select>
          </div>

          {/* Export JSON */}
          <button
            onClick={exportHistoryJSON}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-emerald-950/90 hover:bg-emerald-900/90 border border-emerald-600/40 text-xs font-semibold text-emerald-200 cursor-pointer"
          >
            <Download className="w-3.5 h-3.5 text-emerald-400" />
            <span>{t.history.exportLog}</span>
          </button>
        </div>
      </div>

      {/* History Feed List */}
      <div className="space-y-3">
        {filteredScans.length === 0 ? (
          <div className="p-12 text-center glass-panel rounded-3xl space-y-3">
            <Leaf className="w-10 h-10 text-emerald-500/40 mx-auto" />
            <h4 className="text-sm font-bold text-emerald-200">{t.history.noScansTitle}</h4>
            <p className="text-xs text-emerald-400/60 max-w-sm mx-auto">
              {t.history.noScansDesc}
            </p>
          </div>
        ) : (
          filteredScans.map((scan) => {
            const isExpanded = expandedId === scan.id;
            const isSevere = scan.severity === "Severe";
            const isMod = scan.severity === "Moderate";

            return (
              <div
                key={scan.id}
                className="glass-panel-elevated rounded-2xl border border-emerald-900/50 hover:border-emerald-600/40 transition-all overflow-hidden"
              >
                <div
                  onClick={() => toggleExpand(scan.id)}
                  className="p-4 sm:p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer select-none"
                >
                  <div className="flex items-start sm:items-center gap-3.5">
                    <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center shrink-0">
                      <Leaf className="w-5 h-5 text-emerald-400" />
                    </div>

                    <div className="space-y-1">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-sm font-extrabold text-white">
                          {scan.crop_name}
                        </span>
                        <span
                          className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                            isSevere
                              ? "bg-red-500/20 text-red-300 border-red-500/40"
                              : isMod
                              ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
                              : "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
                          }`}
                        >
                          {scan.severity}
                        </span>
                        <span className="text-[10px] font-mono text-emerald-400/80 bg-black/40 px-2 py-0.5 rounded">
                          {(scan.confidence_score * 100).toFixed(0)}% {t.diagnostic.certainty}
                        </span>
                      </div>

                      <p className="text-xs font-semibold text-emerald-300">
                        {scan.disease_detected}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between sm:justify-end gap-4 text-xs text-emerald-400/70 border-t sm:border-t-0 pt-2 sm:pt-0 border-emerald-950">
                    <div className="flex items-center gap-1.5 font-mono text-[11px]">
                      <Calendar className="w-3.5 h-3.5 text-emerald-500" />
                      <span>{new Date(scan.scanned_at).toLocaleString()}</span>
                    </div>

                    {scan.latitude && scan.longitude && (
                      <div className="hidden md:flex items-center gap-1 font-mono text-[11px]">
                        <MapPin className="w-3 h-3 text-emerald-500" />
                        <span>{scan.latitude.toFixed(2)}°, {scan.longitude.toFixed(2)}°</span>
                      </div>
                    )}

                    <div className="p-1 rounded-lg bg-emerald-950/60 text-emerald-300">
                      {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                    </div>
                  </div>
                </div>

                {/* Expanded Treatment Details */}
                {isExpanded && (
                  <div className="px-5 pb-5 pt-2 border-t border-emerald-950 grid grid-cols-1 md:grid-cols-2 gap-4 animate-in fade-in duration-200">
                    <div className="p-4 rounded-xl bg-black/40 border border-emerald-900/40 space-y-1.5">
                      <span className="text-xs font-bold text-emerald-300 flex items-center gap-1.5">
                        <Sprout className="w-3.5 h-3.5 text-emerald-400" />
                        <span>{t.history.organicRx}</span>
                      </span>
                      <p className="text-xs text-emerald-200/80 leading-relaxed">
                        {scan.organic_remedy || "Maintain cultural hygiene and bio-fungicide foliar applications."}
                      </p>
                    </div>

                    <div className="p-4 rounded-xl bg-black/40 border border-emerald-900/40 space-y-1.5">
                      <span className="text-xs font-bold text-teal-300 flex items-center gap-1.5">
                        <FlaskConical className="w-3.5 h-3.5 text-teal-400" />
                        <span>{t.history.chemicalProtocol}</span>
                      </span>
                      <p className="text-xs text-teal-200/80 leading-relaxed">
                        {scan.chemical_remedy || "Consult registered agrochemical handbook for active molecule dilution."}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
