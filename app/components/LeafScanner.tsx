"use client";

import React, { useState, useRef, useEffect } from "react";
import { 
  Camera, 
  Upload, 
  RefreshCw, 
  MapPin, 
  Sparkles, 
  AlertCircle, 
  Leaf, 
  FlipHorizontal,
  Layers,
  Zap
} from "lucide-react";
import { DiagnosticResponse, SampleLeaf } from "../types";
import { TRANSLATIONS, SupportedLanguage } from "../i18n";

interface LeafScannerProps {
  onDiagnosticComplete: (data: DiagnosticResponse) => void;
  selectedLanguage: string;
  sampleImages: SampleLeaf[];
  backendUrl: string;
}

const CROPS_LIST = [
  "Auto-Detect Any Crop Leaf / ಸ್ವಯಂ ಪತ್ತೆ (ಯಾವುದೇ ಬೆಳೆಯ ಎಲೆ)",
  "Arecanut (ಅಡಿಕೆ - Areca catechu)",
  "Ragi (ರಾಗಿ - Finger Millet)",
  "Tomato (ಟೊಮ್ಯಾಟೊ - Solanum lycopersicum)",
  "Potato (ಆಲೂಗಡ್ಡೆ - Solanum tuberosum)",
  "Rice / Paddy (ಭತ್ತ - Oryza sativa)",
  "Maize / Corn (ಮೆಕ್ಕೆಜೋಳ - Zea mays)",
  "Wheat (ಗೋಧಿ - Triticum aestivum)",
  "Chilli / Pepper (ಮೆಣಸಿನಕಾಯಿ - Capsicum)",
  "Banana (ಬಾಳೆ - Musa)",
  "Cotton (ಹತ್ತಿ - Gossypium)",
  "Coffee (ಕಾಫಿ - Coffea arabica)",
  "Tea (ಟೀ / ಚಹಾ - Camellia sinensis)",
  "Mango (ಮಾವಿನ ಮರ - Mangifera indica)",
  "Groundnut (ಕಡಲೆಕಾಯಿ - Arachis hypogaea)",
  "Sugarcane (ಕಬ್ಬು - Saccharum officinarum)",
  "Onion (ಈರುಳ್ಳಿ - Allium cepa)",
  "Citrus / Orange (ಕಿತ್ತಳೆ / ನಿಂಬೆ)",
  "Grapes (ದ್ರಾಕ್ಷಿ - Vitis vinifera)",
  "Apple (ಸೇಬು - Malus domestica)",
  "Brinjal (ಬದನೆಕಾಯಿ - Solanum melongena)",
  "Rose (ಗುಲಾಬಿ - Rosa)",
  "Coconut (ತೆಂಗು - Cocos nucifera)",
  "Soybean (ಸೋಯಾಬೀನ್ - Glycine max)"
];

export default function LeafScanner({
  onDiagnosticComplete,
  selectedLanguage,
  sampleImages,
  backendUrl,
}: LeafScannerProps) {
  const langKey = (["kn", "en", "hi", "es", "sw", "fr"].includes(selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;

  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [isCameraActive, setIsCameraActive] = useState<boolean>(false);
  const [cameraFacing, setCameraFacing] = useState<"environment" | "user">("environment");
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [telemetryIndex, setTelemetryIndex] = useState<number>(0);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [cropHint, setCropHint] = useState<string>(CROPS_LIST[0]);
  
  // Geolocation
  const [coords, setCoords] = useState<{ lat: number; lng: number } | null>(null);
  const [geoStatus, setGeoStatus] = useState<string>("Locating...");

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined" && "geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setCoords({
            lat: Number(pos.coords.latitude.toFixed(4)),
            lng: Number(pos.coords.longitude.toFixed(4))
          });
          setGeoStatus(t.scanner.gpsAcquired);
        },
        () => {
          setCoords({ lat: 12.9716, lng: 77.5946 }); // Bengaluru, Karnataka agricultural coordinates
          setGeoStatus(t.scanner.gpsAcquired);
        },
        { timeout: 8000 }
      );
    } else {
      setCoords({ lat: 12.9716, lng: 77.5946 });
      setGeoStatus(t.scanner.gpsAcquired);
    }
  }, [selectedLanguage]);

  useEffect(() => {
    if (!isScanning) return;
    const interval = setInterval(() => {
      setTelemetryIndex((prev) => (prev + 1) % t.scanner.telemetry.length);
    }, 700);
    return () => {
      clearInterval(interval);
      setTelemetryIndex(0);
    };
  }, [isScanning, selectedLanguage, t.scanner.telemetry.length]);

  const startCamera = async () => {
    try {
      setErrorMsg(null);
      if (mediaStreamRef.current) {
        mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: cameraFacing,
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
      });

      mediaStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      }
      setIsCameraActive(true);
      setImagePreview(null);
    } catch (err) {
      console.error("Camera access failed", err);
      setErrorMsg("Camera access failed or permission denied. Please upload an image or choose a test sample.");
      setIsCameraActive(false);
    }
  };

  const stopCamera = () => {
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }
    setIsCameraActive(false);
  };

  const flipCamera = () => {
    const nextFacing = cameraFacing === "environment" ? "user" : "environment";
    setCameraFacing(nextFacing);
    setTimeout(() => {
      startCamera();
    }, 100);
  };

  const capturePhoto = () => {
    if (!videoRef.current) return;
    const canvas = document.createElement("canvas");
    canvas.width = videoRef.current.videoWidth || 640;
    canvas.height = videoRef.current.videoHeight || 480;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    const dataUrl = canvas.toDataURL("image/jpeg", 0.92);
    setImagePreview(dataUrl);
    stopCamera();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setErrorMsg(null);
    const file = e.target.files?.[0];
    if (file) {
      if (!file.type.startsWith("image/")) {
        setErrorMsg("Please select a valid image (JPG, PNG, WebP).");
        return;
      }
      const reader = new FileReader();
      reader.onload = () => {
        setImagePreview(reader.result as string);
        stopCamera();
      };
      reader.readAsDataURL(file);
    }
  };

  const executeDiagnosis = async () => {
    if (!imagePreview) {
      setErrorMsg("Please capture or select an image first.");
      return;
    }

    setIsScanning(true);
    setErrorMsg(null);

    try {
      const cleanHint = cropHint.includes("Auto-Detect") ? undefined : cropHint.split(" ")[0].toLowerCase();

      const payload = {
        image_base64: imagePreview,
        crop_hint: cleanHint,
        latitude: coords?.lat,
        longitude: coords?.lng,
        preferred_language: selectedLanguage,
      };

      const res = await fetch(`${backendUrl}/api/diagnose`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        throw new Error(`Diagnosis error: ${res.statusText}`);
      }

      const diagnosticData: DiagnosticResponse = await res.json();
      onDiagnosticComplete(diagnosticData);
    } catch (err: any) {
      console.error("Diagnosis error:", err);
      setErrorMsg("Could not connect to AgriVision Core on port 8005. Retrying...");
    } finally {
      setIsScanning(false);
    }
  };

  const loadSample = (sample: SampleLeaf) => {
    stopCamera();
    setImagePreview(sample.image_data);
    setCropHint(sample.crop);
    setErrorMsg(null);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner / Crop & Location HUD */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        {/* Crop Hint Selector */}
        <div className="glass-panel rounded-2xl p-3.5 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center shrink-0">
            <Leaf className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="flex-1 min-w-0">
            <label className="text-[11px] uppercase tracking-wider text-emerald-400/80 font-bold block">
              {t.scanner.targetCrop}
            </label>
            <select
              value={cropHint}
              onChange={(e) => setCropHint(e.target.value)}
              className="bg-transparent text-sm font-semibold text-emerald-100 w-full focus:outline-none cursor-pointer truncate"
            >
              {CROPS_LIST.map((crop) => (
                <option key={crop} value={crop} className="bg-[#0b1d14] text-white">
                  {crop}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* GPS Geolocation Lock */}
        <div className="glass-panel rounded-2xl p-3.5 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center shrink-0">
            <MapPin className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <span className="text-[11px] uppercase tracking-wider text-emerald-400/80 font-bold">
                {t.scanner.gpsCoordinates}
              </span>
              <span className="text-[10px] text-emerald-400 font-mono bg-emerald-950/80 px-1.5 py-0.2 rounded border border-emerald-600/30">
                {geoStatus}
              </span>
            </div>
            <p className="text-sm font-mono text-emerald-200 truncate">
              {coords ? `${coords.lat}° N, ${coords.lng}° E` : t.scanner.awaitingGps}
            </p>
          </div>
        </div>

        {/* Vision AI Model Engine */}
        <div className="glass-panel rounded-2xl p-3.5 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-emerald-950/80 border border-emerald-600/40 flex items-center justify-center shrink-0">
            <Zap className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="flex-1 min-w-0">
            <span className="text-[11px] uppercase tracking-wider text-emerald-400/80 font-bold block">
              {t.scanner.multiModalCore}
            </span>
            <p className="text-sm font-semibold text-emerald-200 truncate">
              {t.scanner.multiModalSub}
            </p>
          </div>
        </div>
      </div>

      {/* Main Viewfinder / Capture Box */}
      <div className="relative rounded-3xl glass-panel-elevated overflow-hidden border border-emerald-500/30 shadow-2xl">
        <div className="relative aspect-[4/3] sm:aspect-[16/10] w-full max-h-[520px] bg-black/60 flex items-center justify-center overflow-hidden">
          {/* Active Camera Stream */}
          {isCameraActive && (
            <video
              ref={videoRef}
              playsInline
              muted
              className="w-full h-full object-cover"
            />
          )}

          {/* Captured / Uploaded Image Preview */}
          {!isCameraActive && imagePreview && (
            <div className="relative w-full h-full flex items-center justify-center bg-black/80">
              <img
                src={imagePreview}
                alt="Plant Leaf Scan"
                className="w-full h-full object-contain"
              />
            </div>
          )}

          {/* Empty Placeholder View */}
          {!isCameraActive && !imagePreview && (
            <div className="p-8 text-center max-w-md mx-auto space-y-4">
              <div className="relative w-24 h-24 mx-auto rounded-3xl bg-emerald-950/60 border-2 border-dashed border-emerald-500/40 flex items-center justify-center">
                <Leaf className="w-10 h-10 text-emerald-400" />
                <div className="absolute inset-0 rounded-3xl border border-emerald-400/20 animate-pulse-ring" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-emerald-100">
                  {t.scanner.readyTitle}
                </h3>
                <p className="text-xs text-emerald-300/70 mt-1.5 leading-relaxed">
                  {t.scanner.readyDesc}
                </p>
              </div>

              <div className="flex flex-wrap items-center justify-center gap-3 pt-2">
                <button
                  onClick={startCamera}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-600 to-green-600 hover:from-emerald-500 hover:to-green-500 text-white font-semibold text-sm shadow-lg shadow-emerald-900/50 transition-all hover:scale-105 active:scale-95 cursor-pointer"
                >
                  <Camera className="w-4 h-4" />
                  <span>{t.scanner.openCamera}</span>
                </button>

                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-950/80 hover:bg-emerald-900/80 border border-emerald-500/40 text-emerald-200 font-semibold text-sm transition-all hover:scale-105 active:scale-95 cursor-pointer"
                >
                  <Upload className="w-4 h-4" />
                  <span>{t.scanner.uploadImage}</span>
                </button>
              </div>
            </div>
          )}

          {/* HUD Targeting Reticle & Scanning Laser Beam */}
          {(isCameraActive || imagePreview) && (
            <>
              <div className="absolute inset-4 pointer-events-none border border-emerald-500/20 rounded-2xl">
                <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-emerald-400" />
                <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-emerald-400" />
                <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-emerald-400" />
                <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-emerald-400" />
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-6 h-6 border border-emerald-400/40 rounded-full flex items-center justify-center">
                  <div className="w-1.5 h-1.5 bg-emerald-400 rounded-full" />
                </div>
              </div>

              {isScanning && (
                <div className="absolute left-0 right-0 h-1.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_20px_4px_#34d399] animate-scan-laser pointer-events-none z-20">
                  <div className="absolute -top-6 left-1/2 -translate-x-1/2 px-3 py-0.5 rounded-full bg-emerald-950/90 border border-emerald-400/80 text-[10px] font-mono text-emerald-200 font-bold whitespace-nowrap shadow-lg">
                    {t.scanner.telemetryTitle}
                  </div>
                </div>
              )}
            </>
          )}

          {/* Camera Stream Controls */}
          {isCameraActive && (
            <div className="absolute bottom-4 inset-x-4 flex items-center justify-between z-30">
              <button
                onClick={stopCamera}
                className="px-4 py-2 rounded-xl bg-black/70 hover:bg-black/90 border border-white/20 text-white text-xs font-semibold backdrop-blur cursor-pointer"
              >
                Cancel
              </button>

              <button
                onClick={capturePhoto}
                className="relative flex items-center justify-center w-16 h-16 rounded-full bg-emerald-500 hover:bg-emerald-400 text-white shadow-xl shadow-emerald-950 transition-all hover:scale-105 active:scale-95 cursor-pointer border-4 border-white/80"
              >
                <div className="w-12 h-12 rounded-full border-2 border-white/60 flex items-center justify-center">
                  <Camera className="w-6 h-6 text-white" />
                </div>
              </button>

              <button
                onClick={flipCamera}
                className="p-3 rounded-xl bg-black/70 hover:bg-black/90 border border-white/20 text-white text-xs backdrop-blur cursor-pointer"
                title="Switch Camera"
              >
                <FlipHorizontal className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>

        {/* Scanning Telemetry HUD Strip */}
        {isScanning && (
          <div className="px-6 py-4 bg-emerald-950/90 border-t border-emerald-500/40 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 border-2 border-emerald-400 border-t-transparent rounded-full animate-spin shrink-0" />
              <div>
                <p className="text-xs font-mono font-bold text-emerald-300">
                  {t.scanner.telemetry[telemetryIndex] || t.scanner.telemetry[0]}
                </p>
                <p className="text-[10px] text-emerald-400/60 font-mono mt-0.5">
                  {t.scanner.telemetrySla}
                </p>
              </div>
            </div>
            <span className="text-xs font-mono font-extrabold text-emerald-300">
              {((telemetryIndex + 1) * 20)}%
            </span>
          </div>
        )}

        {/* Bottom Action Footer */}
        {imagePreview && !isCameraActive && !isScanning && (
          <div className="p-4 bg-emerald-950/60 border-t border-emerald-900/50 flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <button
                onClick={() => {
                  setImagePreview(null);
                  startCamera();
                }}
                className="px-3.5 py-2 rounded-xl bg-black/40 hover:bg-black/60 border border-emerald-800/60 text-xs font-semibold text-emerald-200 flex items-center gap-1.5 cursor-pointer"
              >
                <Camera className="w-3.5 h-3.5" />
                <span>{t.scanner.retake}</span>
              </button>

              <button
                onClick={() => fileInputRef.current?.click()}
                className="px-3.5 py-2 rounded-xl bg-black/40 hover:bg-black/60 border border-emerald-800/60 text-xs font-semibold text-emerald-200 flex items-center gap-1.5 cursor-pointer"
              >
                <Upload className="w-3.5 h-3.5" />
                <span>{t.scanner.changeImage}</span>
              </button>
            </div>

            <button
              onClick={executeDiagnosis}
              className="flex-1 sm:flex-none flex items-center justify-center gap-2.5 px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-400 hover:to-green-500 text-white font-bold text-sm shadow-lg shadow-emerald-900/60 transition-all hover:scale-105 active:scale-95 cursor-pointer"
            >
              <Sparkles className="w-4 h-4 text-emerald-100 animate-spin" />
              <span>{t.scanner.runDiagnostic}</span>
            </button>
          </div>
        )}
      </div>

      <input
        ref={fileInputRef}
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />

      {errorMsg && (
        <div className="p-4 rounded-2xl bg-red-950/40 border border-red-500/40 flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
          <p className="text-xs text-red-200 font-medium">{errorMsg}</p>
        </div>
      )}

      {/* 1-Click Verification Gallery */}
      <div className="glass-panel rounded-3xl p-5 border border-emerald-900/40 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-emerald-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-300">
              {t.scanner.galleryTitle}
            </h4>
          </div>
          <span className="text-[11px] text-emerald-400/60 font-medium">
            {t.scanner.gallerySub}
          </span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-9 gap-2">
          {sampleImages.map((sample) => (
            <button
              key={sample.id}
              onClick={() => loadSample(sample)}
              className="group relative flex flex-col items-center text-left p-2 rounded-2xl bg-black/40 hover:bg-emerald-950/60 border border-emerald-900/40 hover:border-emerald-500/50 transition-all hover:-translate-y-1 cursor-pointer"
            >
              <div className="relative w-full aspect-square rounded-xl overflow-hidden bg-emerald-950/40 mb-1.5 border border-emerald-800/30">
                <img
                  src={sample.image_data}
                  alt={sample.title}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                />
                <div 
                  className="absolute top-1 right-1 w-2 h-2 rounded-full"
                  style={{ backgroundColor: sample.thumbnail_color }}
                />
                {sample.domain && (
                  <span className={`absolute bottom-1 left-1 text-[7px] font-bold px-1 py-0.2 rounded ${
                    sample.domain.includes("Animal") 
                      ? "bg-rose-950/90 text-rose-300 border border-rose-600/40" 
                      : "bg-emerald-950/90 text-emerald-300 border border-emerald-600/40"
                  }`}>
                    {sample.domain.includes("Animal") ? t.scanner.animalBadge : t.scanner.plantBadge}
                  </span>
                )}
              </div>
              <span className="text-[11px] font-bold text-emerald-200 w-full truncate text-center">
                {sample.crop}
              </span>
              <span className="text-[9px] text-emerald-400/70 w-full truncate text-center">
                {sample.expected_severity}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
