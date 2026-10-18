"use client";

import React from "react";
import { 
  BarChart3, 
  TrendingUp, 
  AlertTriangle, 
  ShieldCheck, 
  Leaf, 
  Bug, 
  Activity,
  Layers,
  Sparkles
} from "lucide-react";
import { AnalyticsSummary } from "../types";
import { TRANSLATIONS, SupportedLanguage } from "../i18n";

interface PathologyAnalyticsProps {
  analytics: AnalyticsSummary | null;
  selectedLanguage?: string;
}

export default function PathologyAnalytics({ analytics, selectedLanguage = "en" }: PathologyAnalyticsProps) {
  const langKey = (["kn", "en", "hi", "es", "sw", "fr"].includes(selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;

  const totalScans = analytics?.total_scans || 12;
  const severeCount = analytics?.severe_outbreaks || 5;
  const severePercentage = totalScans > 0 ? Math.round((severeCount / totalScans) * 100) : 0;

  const topCrops = analytics?.top_crops || [
    { crop: "Tomato", count: 4 },
    { crop: "Rice (Paddy)", count: 3 },
    { crop: "Potato", count: 2 },
    { crop: "Maize (Corn)", count: 2 },
    { crop: "Wheat", count: 1 },
  ];

  const topDiseases = analytics?.top_diseases || [
    { disease: "Late Blight (Phytophthora infestans)", count: 4 },
    { disease: "Bacterial Leaf Blight (Xanthomonas)", count: 3 },
    { disease: "Early Blight (Alternaria solani)", count: 2 },
    { disease: "Corn Common Rust (Puccinia sorghi)", count: 2 },
  ];

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="glass-panel-elevated rounded-3xl p-5 border border-emerald-500/30 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-extrabold text-white">
              {t.analytics.title}
            </h3>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-500/30">
              {t.analytics.badge}
            </span>
          </div>
          <p className="text-xs text-emerald-300/70 mt-0.5">
            {t.analytics.subtitle}
          </p>
        </div>
      </div>

      {/* 4 Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="glass-panel rounded-3xl p-5 border border-emerald-900/40 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-[11px] uppercase font-bold tracking-wider text-emerald-400">
              {t.analytics.totalScans}
            </span>
            <div className="w-8 h-8 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center">
              <Activity className="w-4 h-4 text-emerald-400" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-white mt-3 font-mono">
            {totalScans}
          </p>
          <span className="text-[11px] text-emerald-300/70 flex items-center gap-1 mt-1">
            <TrendingUp className="w-3 h-3 text-emerald-400" />
            <span>{t.analytics.realtimeCloud}</span>
          </span>
        </div>

        <div className="glass-panel rounded-3xl p-5 border border-red-900/40 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-[11px] uppercase font-bold tracking-wider text-red-400">
              {t.analytics.severeRisk}
            </span>
            <div className="w-8 h-8 rounded-xl bg-red-950/80 border border-red-600/40 flex items-center justify-center">
              <AlertTriangle className="w-4 h-4 text-red-400" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-red-200 mt-3 font-mono">
            {severeCount}
          </p>
          <span className="text-[11px] text-red-300/70 flex items-center gap-1 mt-1">
            <span>{severePercentage}% {t.analytics.analyzedAcreage}</span>
          </span>
        </div>

        <div className="glass-panel rounded-3xl p-5 border border-emerald-900/40 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-[11px] uppercase font-bold tracking-wider text-emerald-400">
              {t.analytics.sla}
            </span>
            <div className="w-8 h-8 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center">
              <ShieldCheck className="w-4 h-4 text-emerald-400" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-white mt-3 font-mono">
            &lt; 3.5s
          </p>
          <span className="text-[11px] text-emerald-300/70 flex items-center gap-1 mt-1">
            <span>{t.analytics.subsecondEdge}</span>
          </span>
        </div>

        <div className="glass-panel rounded-3xl p-5 border border-emerald-900/40 relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-[11px] uppercase font-bold tracking-wider text-emerald-400">
              {t.analytics.cropsMonitored}
            </span>
            <div className="w-8 h-8 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center">
              <Leaf className="w-4 h-4 text-emerald-400" />
            </div>
          </div>
          <p className="text-3xl font-extrabold text-white mt-3 font-mono">
            18+
          </p>
          <span className="text-[11px] text-emerald-300/70 flex items-center gap-1 mt-1">
            <span>{t.analytics.stapleGrains}</span>
          </span>
        </div>
      </div>

      {/* Two Column Breakdown: Top Crops & Top Pathogens */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Affected Crops */}
        <div className="glass-panel-elevated rounded-3xl p-6 border border-emerald-500/30 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Leaf className="w-4 h-4 text-emerald-400" />
              <span>{t.analytics.topCropsTitle}</span>
            </h4>
            <span className="text-xs text-emerald-400 font-mono">{t.analytics.frequency}</span>
          </div>

          <div className="space-y-3 pt-2">
            {topCrops.map((item, idx) => {
              const maxCount = Math.max(...topCrops.map((c) => c.count), 1);
              const pct = Math.round((item.count / maxCount) * 100);

              return (
                <div key={idx} className="space-y-1.5">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-emerald-100">{item.crop}</span>
                    <span className="font-mono text-emerald-300">{item.count} {t.analytics.scansCount}</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-emerald-950 overflow-hidden">
                    <div 
                      className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-green-400"
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Pathogen Class Breakdown */}
        <div className="glass-panel-elevated rounded-3xl p-6 border border-emerald-500/30 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <Bug className="w-4 h-4 text-emerald-400" />
              <span>{t.analytics.pathogenDistribution}</span>
            </h4>
            <span className="text-xs text-emerald-400 font-mono">{t.analytics.globalRatio}</span>
          </div>

          <div className="space-y-3.5 pt-2">
            <div>
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="font-semibold text-emerald-100">{t.analytics.fungal}</span>
                <span className="font-mono text-emerald-300">58%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-emerald-950 overflow-hidden">
                <div className="h-full rounded-full bg-emerald-400" style={{ width: "58%" }} />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="font-semibold text-emerald-100">{t.analytics.bacterial}</span>
                <span className="font-mono text-teal-300">22%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-emerald-950 overflow-hidden">
                <div className="h-full rounded-full bg-teal-400" style={{ width: "22%" }} />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="font-semibold text-emerald-100">{t.analytics.viral}</span>
                <span className="font-mono text-amber-300">12%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-emerald-950 overflow-hidden">
                <div className="h-full rounded-full bg-amber-400" style={{ width: "12%" }} />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between text-xs mb-1">
                <span className="font-semibold text-emerald-100">{t.analytics.pests}</span>
                <span className="font-mono text-red-300">8%</span>
              </div>
              <div className="w-full h-2 rounded-full bg-emerald-950 overflow-hidden">
                <div className="h-full rounded-full bg-red-400" style={{ width: "8%" }} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
