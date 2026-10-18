"use client";

import React, { useState, useEffect } from "react";
import { 
  CheckCircle2, 
  AlertTriangle, 
  Volume2, 
  VolumeX, 
  Copy, 
  Check, 
  Sparkles, 
  ShieldAlert, 
  Sprout, 
  FlaskConical, 
  Clock, 
  Compass, 
  ChevronRight,
  Stethoscope,
  Cpu,
  Layers,
  Activity,
  RotateCcw
} from "lucide-react";
import { DiagnosticResponse, SeverityLevel } from "../types";
import { TRANSLATIONS, SupportedLanguage } from "../i18n";

interface DiagnosticCardProps {
  diagnostic: DiagnosticResponse;
  selectedLanguage: string;
  onLocateOnMap: () => void;
  onResetScan: () => void;
}

export default function DiagnosticCard({
  diagnostic,
  selectedLanguage,
  onLocateOnMap,
  onResetScan,
}: DiagnosticCardProps) {
  const langKey = (["kn", "en", "hi", "es", "sw", "fr"].includes(selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;

  const [activePathway, setActivePathway] = useState<"organic" | "chemical">("organic");
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [copied, setCopied] = useState<boolean>(false);

  useEffect(() => {
    return () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const getSeverityColor = (sev: SeverityLevel) => {
    switch (sev) {
      case "Severe":
        return {
          bg: "bg-red-950/70 border-red-500/40 text-red-200",
          badge: "bg-red-500/20 text-red-300 border-red-500/40",
          bar: "bg-red-500",
          glow: "rgba(239, 68, 68, 0.4)",
        };
      case "Moderate":
        return {
          bg: "bg-amber-950/70 border-amber-500/40 text-amber-200",
          badge: "bg-amber-500/20 text-amber-300 border-amber-500/40",
          bar: "bg-amber-500",
          glow: "rgba(245, 158, 11, 0.4)",
        };
      case "Low":
      default:
        return {
          bg: "bg-emerald-950/70 border-emerald-500/40 text-emerald-200",
          badge: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
          bar: "bg-emerald-500",
          glow: "rgba(16, 185, 129, 0.4)",
        };
    }
  };

  const isWrongPhoto = Boolean(
    diagnostic.is_wrong_photo || 
    diagnostic.disease_detected.toLowerCase().includes("wrong photo") ||
    diagnostic.domain_category === "Non-Agricultural / Invalid Image"
  );
  const severityStyle = isWrongPhoto ? getSeverityColor("Severe") : getSeverityColor(diagnostic.severity);
  const isAnimal = Boolean(diagnostic.is_animal_disease);
  const isValidAgri = !isWrongPhoto && diagnostic.is_valid_agricultural_image !== false;

  const toggleSpeech = () => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      alert("Text-to-speech is not supported by your browser.");
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const langSummary = diagnostic.localized_speech_summary?.[selectedLanguage] || 
                         diagnostic.localized_speech_summary?.["kn"] || 
                         diagnostic.localized_speech_summary?.["en"] || 
                         `${diagnostic.crop_name} ${diagnostic.disease_detected}. ${diagnostic.organic_remedy}`;

    const utterance = new SpeechSynthesisUtterance(langSummary);
    
    if (selectedLanguage === "kn") utterance.lang = "kn-IN";
    else if (selectedLanguage === "hi") utterance.lang = "hi-IN";
    else if (selectedLanguage === "es") utterance.lang = "es-ES";
    else if (selectedLanguage === "sw") utterance.lang = "sw-KE";
    else if (selectedLanguage === "fr") utterance.lang = "fr-FR";
    else utterance.lang = "en-US";

    utterance.rate = 0.95;
    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    window.speechSynthesis.speak(utterance);
  };

  const copyPrescription = () => {
    const text = `AgriVision AI Prescription Report
Category: ${isAnimal ? "Veterinary / Livestock Pathology" : "Crop / Plant Pathology"}
Subject: ${diagnostic.crop_name} (${diagnostic.scientific_crop_name || ""})
Diagnosis: ${diagnostic.disease_detected}
Severity: ${diagnostic.severity} (${diagnostic.infection_percentage}% surface area)
Confidence: ${(diagnostic.confidence_score * 100).toFixed(1)}%

${isAnimal ? "Herbal / Supportive Protocol:" : "Organic Pathway:"}
${diagnostic.organic_remedy}

${isAnimal ? "Veterinary Medical Protocol:" : "Chemical Pathway:"}
${diagnostic.chemical_remedy}
Active Molecule: ${diagnostic.chemical_details?.active_ingredient || "N/A"}
Dosage: ${diagnostic.chemical_details?.dosage_per_liter || "N/A"}

${diagnostic.animal_warning ? `CRITICAL WARNING: ${diagnostic.animal_warning}` : ""}

CNN Feature Metrics:
- Model: ${diagnostic.cnn_metrics?.cnn_model_name || "Deep-CNN"}
- Confidence: ${diagnostic.cnn_metrics?.cnn_confidence || "N/A"}
- Lesions Counted: ${diagnostic.cnn_metrics?.lesion_count || "N/A"}

Generated at: ${new Date(diagnostic.timestamp).toLocaleString()}
Engine: ${diagnostic.model_used}`;

    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2500);
  };

  return (
    <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
      {/* 1. DEDICATED WRONG PHOTO DETECTED BANNER (CNN DOMAIN GATEKEEPER) */}
      {isWrongPhoto && (
        <div className="rounded-3xl p-6 sm:p-7 bg-gradient-to-r from-red-950/95 via-rose-950/90 to-red-950/95 border-2 border-red-500/80 shadow-2xl relative overflow-hidden animate-pulse">
          <div className="absolute -top-12 -right-12 w-48 h-48 bg-red-600/20 rounded-full blur-2xl pointer-events-none" />
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 relative z-10">
            <div className="flex items-start gap-4">
              <div className="w-14 h-14 rounded-2xl bg-red-900/70 border-2 border-red-400 flex items-center justify-center shrink-0 shadow-lg shadow-red-950/80">
                <ShieldAlert className="w-8 h-8 text-red-300" />
              </div>
              <div className="space-y-1.5 flex-1">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-xs uppercase font-extrabold tracking-widest px-3 py-1 rounded-full bg-red-500 text-white shadow-md">
                    {t.diagnostic.wrongPhotoBadge}
                  </span>
                  <span className="text-xs font-mono font-bold text-red-200 bg-red-950/80 px-2.5 py-0.5 rounded-full border border-red-500/40">
                    {diagnostic.cnn_metrics?.cnn_domain || "ANIMAL_SUBJECT (Non-Crop)"}
                  </span>
                </div>
                <h3 className="text-lg sm:text-xl font-extrabold text-white">
                  {t.diagnostic.wrongPhotoTitle}
                </h3>
                <p className="text-xs sm:text-sm text-red-200/90 leading-relaxed max-w-2xl">
                  {diagnostic.wrong_photo_reason || t.diagnostic.wrongPhotoDesc}
                </p>
              </div>
            </div>

            <button
              onClick={onResetScan}
              className="w-full md:w-auto flex items-center justify-center gap-2 px-6 py-3.5 rounded-2xl bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white text-xs font-extrabold shadow-xl shadow-red-950/80 transition-all hover:scale-105 active:scale-95 cursor-pointer shrink-0 border border-red-400/40"
            >
              <RotateCcw className="w-4 h-4" />
              <span>{t.diagnostic.retakeCorrectLeaf}</span>
            </button>
          </div>

          {/* Multi-Task CNN Domain Confidence Telemetry */}
          {diagnostic.cnn_metrics && (
            <div className="mt-5 pt-4 border-t border-red-800/40 grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
              <div className="bg-black/50 rounded-xl p-2.5 border border-red-900/50">
                <span className="text-[10px] uppercase font-bold text-red-300/80 block">Detected Subject</span>
                <span className="text-sm font-extrabold font-mono text-red-400 truncate block">
                  {diagnostic.cnn_metrics.cnn_domain || "NON_PLANT"}
                </span>
              </div>
              <div className="bg-black/50 rounded-xl p-2.5 border border-red-900/50">
                <span className="text-[10px] uppercase font-bold text-red-300/80 block">Crop Foliage Presence</span>
                <span className="text-sm font-extrabold font-mono text-emerald-400">
                  {diagnostic.cnn_metrics.foliar_score !== undefined 
                    ? `${(diagnostic.cnn_metrics.foliar_score * 100).toFixed(1)}%` 
                    : `${((diagnostic.cnn_metrics.leaf_probability ?? 0.05) * 100).toFixed(1)}%`}
                </span>
              </div>
              <div className="bg-black/50 rounded-xl p-2.5 border border-red-900/50">
                <span className="text-[10px] uppercase font-bold text-red-300/80 block">Rejection Certainty</span>
                <span className="text-xs font-bold font-mono text-white truncate block">
                  {diagnostic.cnn_metrics.cnn_confidence 
                    ? `${(diagnostic.cnn_metrics.cnn_confidence * 100).toFixed(1)}% Certain` 
                    : "High (>95%)"}
                </span>
              </div>
              <div className="bg-black/50 rounded-xl p-2.5 border border-red-900/50">
                <span className="text-[10px] uppercase font-bold text-red-300/80 block">Botanical Filter</span>
                <span className="text-xs font-extrabold font-mono text-red-300">
                  ERROR: REJECTED
                </span>
              </div>
            </div>
          )}
        </div>
      )}

      {/* 2. VETERINARY ANIMAL DISEASE ALERT BANNER (Only when veterinary was legitimately intended) */}
      {!isWrongPhoto && isAnimal && (
        <div className="rounded-3xl p-6 bg-gradient-to-r from-rose-950/90 via-amber-950/80 to-rose-950/90 border-2 border-rose-500/60 shadow-2xl relative overflow-hidden animate-pulse">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-2xl bg-rose-900/60 border border-rose-400 flex items-center justify-center shrink-0">
              <Stethoscope className="w-6 h-6 text-rose-300" />
            </div>
            <div className="space-y-1.5 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs uppercase font-extrabold tracking-widest px-2.5 py-0.5 rounded-full bg-rose-500 text-white shadow">
                  {t.diagnostic.veterinaryAlertTitle}
                </span>
                <span className="text-xs font-bold text-rose-200">
                  {diagnostic.crop_name}
                </span>
              </div>
              <h3 className="text-base sm:text-lg font-extrabold text-white">
                {diagnostic.animal_warning || t.diagnostic.veterinaryWarningDesc}
              </h3>
              <p className="text-xs text-rose-200/90 leading-relaxed">
                {t.diagnostic.veterinaryWarningDesc}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* 3. NON-AGRICULTURAL / INVALID IMAGE ALERT */}
      {!isWrongPhoto && !isValidAgri && (
        <div className="rounded-3xl p-6 bg-gradient-to-r from-amber-950/90 to-yellow-950/80 border-2 border-amber-500/60 shadow-xl flex items-start gap-4">
          <div className="w-10 h-10 rounded-2xl bg-amber-900/60 border border-amber-400 flex items-center justify-center shrink-0">
            <AlertTriangle className="w-5 h-5 text-amber-300" />
          </div>
          <div className="space-y-1">
            <h4 className="text-sm font-bold text-white uppercase tracking-wider">
              {t.diagnostic.invalidImageTitle}
            </h4>
            <p className="text-xs text-amber-200/90 leading-relaxed">
              {t.diagnostic.invalidImageDesc}
            </p>
          </div>
        </div>
      )}

      {/* Main Diagnostic Card Header */}
      <div className={`rounded-3xl glass-panel-elevated p-6 sm:p-8 border relative overflow-hidden ${
        isWrongPhoto 
          ? "border-red-500/50 bg-gradient-to-b from-red-950/40 to-black/80" 
          : isAnimal 
            ? "border-rose-500/40 bg-gradient-to-b from-rose-950/40 to-black/80" 
            : "border-emerald-500/30"
      }`}>
        <div 
          className="absolute -top-24 -right-24 w-80 h-80 rounded-full blur-3xl pointer-events-none opacity-20"
          style={{ backgroundColor: isWrongPhoto ? "rgba(239, 68, 68, 0.5)" : isAnimal ? "rgba(244, 63, 94, 0.4)" : severityStyle.glow }}
        />

        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6 relative z-10">
          <div className="space-y-2">
            <div className="flex flex-wrap items-center gap-2.5">
              <span className={`text-xs uppercase font-extrabold tracking-widest px-3 py-1 rounded-full border ${
                isWrongPhoto
                  ? "bg-red-950/90 text-red-300 border-red-500/50"
                  : isAnimal 
                    ? "bg-rose-950/90 text-rose-300 border-rose-500/40" 
                    : "bg-emerald-950/90 text-emerald-300 border-emerald-500/40"
              }`}>
                {diagnostic.crop_name}
              </span>
              {diagnostic.scientific_crop_name && (
                <span className="text-xs italic text-emerald-400/80 font-mono">
                  ({diagnostic.scientific_crop_name})
                </span>
              )}
              <span className={`text-xs uppercase font-bold px-3 py-1 rounded-full border ${severityStyle.badge}`}>
                {diagnostic.pathogen_type}
              </span>
              <span className="text-[11px] font-mono text-emerald-300/80 bg-black/40 px-2 py-0.5 rounded border border-emerald-900/40 flex items-center gap-1">
                <Cpu className="w-3 h-3 text-emerald-400" />
                <span>{diagnostic.inference_time_ms}ms • {diagnostic.model_used}</span>
              </span>
            </div>

            <h2 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-white">
              {diagnostic.disease_detected}
            </h2>

            <p className="text-xs sm:text-sm text-emerald-200/80 max-w-2xl leading-relaxed">
              {diagnostic.localized_speech_summary?.[selectedLanguage] || 
               diagnostic.localized_speech_summary?.["kn"] || 
               diagnostic.localized_speech_summary?.["en"] || 
               "Diagnostic assessment complete."}
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={toggleSpeech}
              className={`flex items-center gap-2.5 px-4 py-2.5 rounded-2xl border font-semibold text-xs transition-all cursor-pointer ${
                isSpeaking
                  ? "bg-emerald-500 text-black border-emerald-300 animate-pulse"
                  : "bg-emerald-950/80 hover:bg-emerald-900/90 text-emerald-200 border-emerald-600/40"
              }`}
              title="Read diagnosis aloud in your language"
            >
              {isSpeaking ? (
                <>
                  <VolumeX className="w-4 h-4" />
                  <span>{t.diagnostic.stopSpeech}</span>
                </>
              ) : (
                <>
                  <Volume2 className="w-4 h-4 text-emerald-400" />
                  <span>{t.diagnostic.listenAloud}</span>
                </>
              )}
            </button>

            <button
              onClick={copyPrescription}
              className="flex items-center gap-2 px-4 py-2.5 rounded-2xl bg-black/40 hover:bg-black/60 border border-emerald-800/60 text-xs font-semibold text-emerald-200 cursor-pointer"
            >
              {copied ? (
                <>
                  <Check className="w-4 h-4 text-emerald-400" />
                  <span>{t.diagnostic.copied}</span>
                </>
              ) : (
                <>
                  <Copy className="w-4 h-4" />
                  <span>{t.diagnostic.copyRx}</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* 3 Metric Badges + Deep CNN Metrics Bar */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8 pt-6 border-t border-emerald-900/50">
          {/* Radial Confidence Gauge */}
          <div className="p-4 rounded-2xl bg-black/40 border border-emerald-900/40 flex items-center gap-4">
            <div className="relative w-16 h-16 shrink-0 flex items-center justify-center">
              <svg className="w-full h-full -rotate-90" viewBox="0 0 36 36">
                <path
                  className="text-emerald-950"
                  strokeWidth="3.5"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path
                  className={
                    isWrongPhoto 
                      ? "text-red-500 transition-all duration-1000 ease-out"
                      : isAnimal 
                        ? "text-rose-400 transition-all duration-1000 ease-out" 
                        : "text-emerald-400 transition-all duration-1000 ease-out"
                  }
                  strokeDasharray={`${diagnostic.confidence_score * 100}, 100`}
                  strokeWidth="3.5"
                  strokeLinecap="round"
                  stroke="currentColor"
                  fill="none"
                  d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                />
              </svg>
              <span className={`absolute text-xs font-mono font-extrabold ${isWrongPhoto ? "text-red-200" : "text-emerald-200"}`}>
                {(diagnostic.confidence_score * 100).toFixed(0)}%
              </span>
            </div>
            <div>
              <span className={`text-[10px] uppercase font-bold tracking-wider block ${isWrongPhoto ? "text-red-400/90" : "text-emerald-400/80"}`}>
                {t.diagnostic.certainty}
              </span>
              <p className={`text-sm font-extrabold ${isWrongPhoto ? "text-red-100" : "text-emerald-100"}`}>
                {(diagnostic.confidence_score * 100).toFixed(1)}%
              </p>
              <span className={`text-[10px] font-mono ${isWrongPhoto ? "text-red-400/70" : "text-emerald-400/70"}`}>
                PyTorch CNN Multi-Task
              </span>
            </div>
          </div>

          {/* Severity Meter */}
          <div className="p-4 rounded-2xl bg-black/40 border border-emerald-900/40 flex flex-col justify-between">
            <div className="flex items-center justify-between">
              <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400/80">
                {t.diagnostic.severityTitle}
              </span>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${severityStyle.badge}`}>
                {diagnostic.severity}
              </span>
            </div>
            <div className="my-2">
              <div className="w-full h-2 rounded-full bg-emerald-950 overflow-hidden">
                <div 
                  className={`h-full rounded-full ${severityStyle.bar} transition-all duration-1000`}
                  style={{ width: `${Math.max(15, diagnostic.infection_percentage)}%` }}
                />
              </div>
            </div>
            <div className="flex items-center justify-between text-[11px] text-emerald-300/70">
              <span>{diagnostic.infection_percentage}% {t.diagnostic.surfaceArea}</span>
              <span className="font-semibold text-emerald-200">{diagnostic.urgency}</span>
            </div>
          </div>

          {/* Observed Symptoms */}
          <div className="p-4 rounded-2xl bg-black/40 border border-emerald-900/40 flex flex-col justify-between">
            <span className="text-[10px] uppercase font-bold tracking-wider text-emerald-400/80">
              {t.diagnostic.observedSymptoms} ({diagnostic.symptoms_observed.length})
            </span>
            <div className="space-y-1 my-1">
              {diagnostic.symptoms_observed.slice(0, 2).map((symptom, idx) => (
                <p key={idx} className="text-xs text-emerald-200/90 truncate flex items-center gap-1.5">
                  <span className={`w-1.5 h-1.5 rounded-full ${isWrongPhoto ? "bg-red-400" : isAnimal ? "bg-rose-400" : "bg-emerald-400"} shrink-0`} />
                  <span className="truncate">{symptom}</span>
                </p>
              ))}
            </div>
            <span className={`text-[10px] ${isWrongPhoto ? "text-red-400/80 font-semibold" : "text-emerald-400/60"}`}>
              {isWrongPhoto ? t.diagnostic.wrongPhotoBadge : isAnimal ? t.diagnostic.vetValidated : t.diagnostic.morphologyValidated}
            </span>
          </div>
        </div>

        {/* Deep CNN Feature Extraction Telemetry Strip */}
        {diagnostic.cnn_metrics && (
          <div className={`mt-4 pt-3 border-t flex flex-wrap items-center justify-between gap-3 text-[11px] font-mono p-2.5 rounded-xl border ${
            isWrongPhoto 
              ? "border-red-900/40 bg-red-950/20 text-red-300/90" 
              : "border-emerald-900/30 bg-black/30 text-emerald-400/80"
          }`}>
            <div className="flex items-center gap-2">
              <Cpu className={`w-3.5 h-3.5 ${isWrongPhoto ? "text-red-400" : "text-emerald-400"}`} />
              <span className={isWrongPhoto ? "text-red-200 font-bold" : "text-emerald-300 font-bold"}>
                {diagnostic.cnn_metrics.cnn_model_name}
              </span>
              {diagnostic.cnn_metrics.cnn_domain && (
                <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold border ${
                  isWrongPhoto ? "bg-red-900/60 border-red-500/50 text-red-200" : "bg-emerald-900/50 border-emerald-500/40 text-emerald-200"
                }`}>
                  {diagnostic.cnn_metrics.cnn_domain}
                </span>
              )}
            </div>
            <div className="flex items-center gap-4">
              {diagnostic.cnn_metrics.animal_probability !== undefined && (
                <span>Animal: <strong className={isWrongPhoto ? "text-red-400 font-extrabold" : "text-white"}>{(diagnostic.cnn_metrics.animal_probability * 100).toFixed(1)}%</strong></span>
              )}
              {diagnostic.cnn_metrics.leaf_probability !== undefined && (
                <span>Leaf: <strong className="text-white">{(diagnostic.cnn_metrics.leaf_probability * 100).toFixed(1)}%</strong></span>
              )}
              <span>Feature Energy: <strong className="text-white">{diagnostic.cnn_metrics.feature_energy}</strong></span>
              <span>Sharpness Var: <strong className="text-white">{diagnostic.cnn_metrics.laplacian_variance}</strong></span>
              <span>Lesion Contours: <strong className="text-white">{diagnostic.cnn_metrics.lesion_count}</strong></span>
            </div>
          </div>
        )}
      </div>

      {/* Dual Treatment Pathways */}
      <div className={`rounded-3xl glass-panel-elevated p-6 sm:p-8 border space-y-6 ${
        isWrongPhoto 
          ? "border-red-500/40 bg-gradient-to-b from-red-950/20 to-black/80" 
          : "border-emerald-500/30"
      }`}>
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-emerald-900/50 pb-5">
          <div>
            <h3 className="text-lg font-bold text-white flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-emerald-400" />
              <span>{t.diagnostic.pathwaysTitle}</span>
            </h3>
            <p className="text-xs text-emerald-300/70 mt-1">
              {t.diagnostic.pathwaysSub}
            </p>
          </div>

          <div className="flex items-center p-1 rounded-2xl bg-black/50 border border-emerald-900/50 w-full sm:w-auto">
            <button
              onClick={() => setActivePathway("organic")}
              className={`flex-1 sm:flex-none flex items-center justify-center gap-2 px-5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                activePathway === "organic"
                  ? isWrongPhoto
                    ? "bg-gradient-to-r from-red-600 to-rose-600 text-white shadow-md shadow-red-900/60"
                    : "bg-gradient-to-r from-emerald-600 to-green-600 text-white shadow-md shadow-emerald-900/60"
                  : "text-emerald-300/70 hover:text-white"
              }`}
            >
              <Sprout className="w-4 h-4 text-emerald-200" />
              <span>{isAnimal ? t.diagnostic.vetOrganicTab : t.diagnostic.organicTab}</span>
            </button>

            <button
              onClick={() => setActivePathway("chemical")}
              className={`flex-1 sm:flex-none flex items-center justify-center gap-2 px-5 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer ${
                activePathway === "chemical"
                  ? isWrongPhoto || isAnimal
                    ? "bg-gradient-to-r from-rose-600 to-red-600 text-white shadow-md shadow-rose-900/60"
                    : "bg-gradient-to-r from-teal-600 to-cyan-600 text-white shadow-md shadow-cyan-900/60"
                  : "text-emerald-300/70 hover:text-white"
              }`}
            >
              <FlaskConical className="w-4 h-4 text-teal-200" />
              <span>{isAnimal ? t.diagnostic.vetChemicalTab : t.diagnostic.chemicalTab}</span>
            </button>
          </div>
        </div>

        {/* Tab 1: Organic / Supportive Pathway */}
        {activePathway === "organic" && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div className={`p-5 rounded-2xl border ${
              isWrongPhoto
                ? "bg-gradient-to-r from-red-950/90 to-amber-950/70 border-red-500/50"
                : "bg-gradient-to-r from-emerald-950/90 to-green-950/70 border-emerald-500/40"
            }`}>
              <div className="flex items-start gap-3">
                <div className={`w-9 h-9 rounded-xl border flex items-center justify-center shrink-0 ${
                  isWrongPhoto 
                    ? "bg-red-800/40 border-red-500/40 text-red-300" 
                    : "bg-emerald-800/40 border-emerald-500/40 text-emerald-300"
                }`}>
                  <Sprout className="w-5 h-5" />
                </div>
                <div className="space-y-1">
                  <span className={`text-[10px] uppercase font-bold tracking-wider ${isWrongPhoto ? "text-red-400" : "text-emerald-400"}`}>
                    {isWrongPhoto ? "Safe Protocol / Guidance" : isAnimal ? t.diagnostic.vetHerbalProtocol : t.diagnostic.biologicalProtocol}
                  </span>
                  <p className={`text-sm font-semibold leading-relaxed ${isWrongPhoto ? "text-red-100" : "text-emerald-100"}`}>
                    {diagnostic.organic_remedy}
                  </p>
                </div>
              </div>
            </div>

            {diagnostic.organic_details && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-5 rounded-2xl bg-black/40 border border-emerald-900/40 space-y-2">
                  <span className="text-xs uppercase font-extrabold tracking-wider text-emerald-400 flex items-center gap-1.5">
                    <FlaskConical className="w-3.5 h-3.5" />
                    <span>{t.diagnostic.prepMethod}</span>
                  </span>
                  <p className="text-xs text-emerald-200/90 leading-relaxed">
                    {diagnostic.organic_details.preparation}
                  </p>
                </div>

                <div className="p-5 rounded-2xl bg-black/40 border border-emerald-900/40 space-y-2">
                  <span className="text-xs uppercase font-extrabold tracking-wider text-emerald-400 flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{t.diagnostic.scheduleInterval}</span>
                  </span>
                  <p className="text-xs text-emerald-200/90 leading-relaxed">
                    {diagnostic.organic_details.application_frequency}
                  </p>
                </div>
              </div>
            )}

            {diagnostic.organic_details?.preventive_cultural_practices && diagnostic.organic_details.preventive_cultural_practices.length > 0 && (
              <div className="p-5 rounded-2xl bg-black/40 border border-emerald-900/40 space-y-3">
                <span className="text-xs uppercase font-extrabold tracking-wider text-emerald-400 flex items-center gap-1.5">
                  <ShieldAlert className="w-3.5 h-3.5" />
                  <span>{t.diagnostic.culturalPractices}</span>
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {diagnostic.organic_details.preventive_cultural_practices.map((practice, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-xs text-emerald-200/80">
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{practice}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Tab 2: Chemical / Veterinary Medical Pathway */}
        {activePathway === "chemical" && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div className={`p-5 rounded-2xl border ${
              isWrongPhoto
                ? "bg-gradient-to-r from-red-950/95 to-rose-950/80 border-red-500/60"
                : isAnimal 
                  ? "bg-gradient-to-r from-rose-950/90 to-red-950/70 border-rose-500/40" 
                  : "bg-gradient-to-r from-teal-950/90 to-cyan-950/70 border-teal-500/40"
            }`}>
              <div className="flex items-start gap-3">
                <div className={`w-9 h-9 rounded-xl border flex items-center justify-center shrink-0 ${
                  isWrongPhoto 
                    ? "bg-red-800/40 border-red-500/40 text-red-300" 
                    : "bg-teal-800/40 border-teal-500/40 text-teal-300"
                }`}>
                  <FlaskConical className="w-5 h-5" />
                </div>
                <div className="space-y-1">
                  <span className={`text-[10px] uppercase font-bold tracking-wider ${isWrongPhoto ? "text-red-400" : "text-teal-400"}`}>
                    {isWrongPhoto ? "Chemical Hazard Warning" : isAnimal ? t.diagnostic.vetMedicalProtocol : t.diagnostic.chemicalProtocol}
                  </span>
                  <p className={`text-sm font-semibold leading-relaxed ${isWrongPhoto ? "text-red-100" : "text-teal-100"}`}>
                    {diagnostic.chemical_remedy}
                  </p>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-2xl bg-black/40 border border-emerald-900/40 space-y-1">
                <span className="text-[10px] uppercase font-bold text-teal-400">
                  {t.diagnostic.activeMolecule}
                </span>
                <p className="text-xs font-bold text-white truncate">
                  {diagnostic.chemical_details?.active_ingredient || "Targeted formulation"}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-black/40 border border-emerald-900/40 space-y-1">
                <span className="text-[10px] uppercase font-bold text-teal-400">
                  {t.diagnostic.applicationRate}
                </span>
                <p className="text-xs font-bold text-white">
                  {diagnostic.chemical_details?.dosage_per_liter || "As prescribed"}
                </p>
              </div>

              <div className="p-4 rounded-2xl bg-amber-950/40 border border-amber-500/40 space-y-1">
                <span className="text-[10px] uppercase font-bold text-amber-400 flex items-center gap-1">
                  <Clock className="w-3 h-3" />
                  <span>{t.diagnostic.phiDays}</span>
                </span>
                <p className="text-xs font-bold text-amber-200">
                  {diagnostic.chemical_details?.pre_harvest_interval_days || 7} {t.diagnostic.mandatoryPhi}
                </p>
              </div>
            </div>

            {diagnostic.chemical_details?.safety_precautions && diagnostic.chemical_details.safety_precautions.length > 0 && (
              <div className="p-5 rounded-2xl bg-black/40 border border-emerald-900/40 space-y-3">
                <span className="text-xs uppercase font-extrabold tracking-wider text-amber-400 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  <span>{t.diagnostic.safetyPrecautions}</span>
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                  {diagnostic.chemical_details.safety_precautions.map((safe, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-xs text-amber-200/90">
                      <span className="w-1.5 h-1.5 rounded-full bg-amber-400 shrink-0 mt-1.5" />
                      <span>{safe}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer Navigation */}
        <div className="flex flex-wrap items-center justify-between gap-4 pt-6 border-t border-emerald-900/50">
          <button
            onClick={onLocateOnMap}
            className="flex items-center gap-2 px-5 py-2.5 rounded-2xl bg-emerald-950/90 hover:bg-emerald-900/90 border border-emerald-500/40 text-xs font-bold text-emerald-200 transition-all hover:scale-105 active:scale-95 cursor-pointer"
          >
            <Compass className="w-4 h-4 text-emerald-400" />
            <span>{t.diagnostic.locateMap}</span>
          </button>

          <button
            onClick={onResetScan}
            className={`flex items-center gap-2 px-6 py-2.5 rounded-2xl text-white text-xs font-bold transition-all hover:scale-105 active:scale-95 cursor-pointer ${
              isWrongPhoto
                ? "bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 shadow-lg shadow-red-900/60"
                : "bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500 shadow-lg shadow-emerald-900/60"
            }`}
          >
            <span>{isWrongPhoto ? t.diagnostic.retakeCorrectLeaf : t.diagnostic.scanAnother}</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
