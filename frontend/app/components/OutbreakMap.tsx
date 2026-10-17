"use client";

import React, { useEffect, useRef, useState } from "react";
import { 
  MapPin, 
  Layers, 
  AlertTriangle, 
  Filter, 
  Globe2, 
  Crosshair, 
  Calendar, 
  Sparkles,
  ArrowRight
} from "lucide-react";
import { OutbreakCluster, SeverityLevel } from "../types";

import { TRANSLATIONS, SupportedLanguage } from "../i18n";

interface OutbreakMapProps {
  outbreaks: OutbreakCluster[];
  userLocation: { lat: number; lng: number } | null;
  onRefresh: () => void;
  selectedLanguage: string;
}

export default function OutbreakMap({
  outbreaks,
  userLocation,
  onRefresh,
  selectedLanguage,
}: OutbreakMapProps) {
  const langKey = (["kn", "en", "hi", "es", "sw", "fr"].includes(selectedLanguage) ? selectedLanguage : "en") as SupportedLanguage;
  const t = TRANSLATIONS[langKey] || TRANSLATIONS.en;
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const leafletMapRef = useRef<any>(null);
  const markersRef = useRef<any[]>([]);

  const [selectedCrop, setSelectedCrop] = useState<string>("All");
  const [selectedSeverity, setSelectedSeverity] = useState<string>("All");
  const [activeCluster, setActiveCluster] = useState<OutbreakCluster | null>(null);

  // Filtered outbreaks
  const filteredOutbreaks = outbreaks.filter((o) => {
    if (selectedCrop !== "All" && !o.crop_name.toLowerCase().includes(selectedCrop.toLowerCase())) {
      return false;
    }
    if (selectedSeverity !== "All" && o.severity !== selectedSeverity) {
      return false;
    }
    return true;
  });

  // Unique crops in outbreaks
  const uniqueCrops = Array.from(new Set(outbreaks.map((o) => o.crop_name.split(" ")[0])));

  // Initialize Leaflet Map
  useEffect(() => {
    let isMounted = true;

    async function initMap() {
      if (typeof window === "undefined" || !mapContainerRef.current) return;
      if (leafletMapRef.current) return; // already initialized

      const L = (await import("leaflet")).default;

      // Default center: User position or global center
      const centerLat = userLocation?.lat || 28.6139;
      const centerLng = userLocation?.lng || 77.2090;

      const map = L.map(mapContainerRef.current, {
        zoomControl: false,
        attributionControl: false,
      }).setView([centerLat, centerLng], userLocation ? 5 : 3);

      // Dark theme CartoDB basemap
      L.tileLayer(
        "https://{s}.basemaps.cartocdn.com/rastertiles/dark_all/{z}/{x}/{y}{r}.png",
        {
          maxZoom: 19,
          subdomains: "abcd",
        }
      ).addTo(map);

      // Add Zoom control at top right
      L.control.zoom({ position: "topright" }).addTo(map);

      leafletMapRef.current = map;
      renderMarkers(L, map);
    }

    initMap();

    return () => {
      isMounted = false;
      if (leafletMapRef.current) {
        leafletMapRef.current.remove();
        leafletMapRef.current = null;
      }
    };
  }, []);

  // Update Markers when filter or outbreaks change
  useEffect(() => {
    async function updateMarkers() {
      if (!leafletMapRef.current) return;
      const L = (await import("leaflet")).default;
      renderMarkers(L, leafletMapRef.current);
    }
    updateMarkers();
  }, [filteredOutbreaks, userLocation]);

  const renderMarkers = (L: any, map: any) => {
    // Clear existing markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    // 1. Add User Farm Pin if present
    if (userLocation) {
      const userIcon = L.divIcon({
        className: "user-loc-pin",
        html: `
          <div style="position: relative; width: 26px; height: 26px; display: flex; align-items: center; justify-content: center;">
            <div style="position: absolute; inset: 0; background: rgba(16, 185, 129, 0.4); border-radius: 50%; animation: pulse-ring 2s infinite;"></div>
            <div style="width: 14px; height: 14px; background: #10b981; border: 2px solid #ffffff; border-radius: 50%; box-shadow: 0 0 10px #10b981;"></div>
          </div>
        `,
        iconSize: [26, 26],
        iconAnchor: [13, 13],
      });

      const userMarker = L.marker([userLocation.lat, userLocation.lng], { icon: userIcon })
        .addTo(map)
        .bindPopup(`
          <div style="padding: 4px;">
            <p style="font-weight: 800; color: #34d399; font-size: 12px; margin: 0;">Your Farm / Scanner Location</p>
            <p style="font-size: 11px; color: #a7f3d0; margin: 2px 0 0 0;">${userLocation.lat.toFixed(4)}°, ${userLocation.lng.toFixed(4)}°</p>
          </div>
        `);
      markersRef.current.push(userMarker);
    }

    // 2. Add Outbreak Cluster Pins
    filteredOutbreaks.forEach((cluster) => {
      const isSevere = cluster.severity === "Severe";
      const isModerate = cluster.severity === "Moderate";

      const pinColor = isSevere ? "#ef4444" : isModerate ? "#f59e0b" : "#10b981";
      const auraColor = isSevere ? "rgba(239, 68, 68, 0.4)" : isModerate ? "rgba(245, 158, 11, 0.4)" : "rgba(16, 185, 129, 0.4)";

      const clusterIcon = L.divIcon({
        className: `outbreak-pin-${cluster.id}`,
        html: `
          <div style="position: relative; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
            <div style="position: absolute; inset: 0; background: ${auraColor}; border-radius: 50%; ${isSevere ? "animation: pulse-ring 1.8s infinite;" : ""}"></div>
            <div style="width: 18px; height: 18px; background: ${pinColor}; border: 2.5px solid #09130d; border-radius: 50%; box-shadow: 0 4px 12px rgba(0,0,0,0.8); display: flex; align-items: center; justify-content: center;">
              <div style="width: 6px; height: 6px; background: #ffffff; border-radius: 50%;"></div>
            </div>
          </div>
        `,
        iconSize: [32, 32],
        iconAnchor: [16, 16],
      });

      const popupHtml = `
        <div style="padding: 6px; min-width: 190px;">
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
            <span style="font-weight: 800; font-size: 11px; color: #a7f3d0; text-transform: uppercase;">${cluster.crop_name}</span>
            <span style="font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 9999px; background: ${pinColor}22; color: ${pinColor}; border: 1px solid ${pinColor}66;">
              ${cluster.severity}
            </span>
          </div>
          <p style="font-weight: 800; font-size: 13px; color: #ffffff; margin: 4px 0 2px 0;">${cluster.disease_detected}</p>
          <p style="font-size: 11px; color: #a7f3d0; margin: 0;">Confidence: ${(cluster.confidence_score * 100).toFixed(0)}%</p>
          ${cluster.distance_km ? `<p style="font-size: 10px; color: #6ee7b7; margin: 4px 0 0 0; font-weight: 600;">📍 ${cluster.distance_km} km from you</p>` : ""}
        </div>
      `;

      const marker = L.marker([cluster.latitude, cluster.longitude], { icon: clusterIcon })
        .addTo(map)
        .bindPopup(popupHtml);

      marker.on("click", () => {
        setActiveCluster(cluster);
      });

      markersRef.current.push(marker);
    });
  };

  const flyToCluster = (cluster: OutbreakCluster) => {
    setActiveCluster(cluster);
    if (leafletMapRef.current) {
      leafletMapRef.current.flyTo([cluster.latitude, cluster.longitude], 9, { duration: 1.5 });
    }
  };

  const centerOnUser = () => {
    if (userLocation && leafletMapRef.current) {
      leafletMapRef.current.flyTo([userLocation.lat, userLocation.lng], 9, { duration: 1.5 });
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Filter Bar & Metrics */}
      <div className="glass-panel-elevated rounded-3xl p-5 border border-emerald-500/30 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
        {/* Title */}
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <Globe2 className="w-5 h-5 text-emerald-400" />
            <h3 className="text-lg font-extrabold text-white">
              {t.map.title}
            </h3>
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-emerald-950 text-emerald-300 border border-emerald-500/30">
              {t.map.postGisBadge}
            </span>
          </div>
          <p className="text-xs text-emerald-300/70">
            {t.map.subtitle}
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2.5 w-full lg:w-auto">
          {/* Crop Filter */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/50 border border-emerald-900/50 text-xs">
            <Filter className="w-3.5 h-3.5 text-emerald-400" />
            <select
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
              className="bg-transparent text-emerald-200 font-semibold focus:outline-none cursor-pointer"
            >
              <option value="All" className="bg-[#0b1d14] text-white">{t.map.allCrops}</option>
              {uniqueCrops.map((crop) => (
                <option key={crop} value={crop} className="bg-[#0b1d14] text-white">
                  {crop}
                </option>
              ))}
            </select>
          </div>

          {/* Severity Filter */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-black/50 border border-emerald-900/50 text-xs">
            <span className="w-2 h-2 rounded-full bg-red-500" />
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

          {/* Recenter button */}
          {userLocation && (
            <button
              onClick={centerOnUser}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-950/90 hover:bg-emerald-900/90 border border-emerald-600/40 text-xs font-semibold text-emerald-200 cursor-pointer"
              title="Center on my location"
            >
              <Crosshair className="w-3.5 h-3.5 text-emerald-400" />
              <span>{t.map.myLocation}</span>
            </button>
          )}
        </div>
      </div>

      {/* Main Map + Sidebar Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Interactive Map Box */}
        <div className="lg:col-span-3 rounded-3xl overflow-hidden glass-panel-elevated border border-emerald-500/30 relative min-h-[500px] h-[550px] shadow-2xl">
          <div ref={mapContainerRef} className="w-full h-full z-10" />

          {/* Map Overlay HUD Badge */}
          <div className="absolute top-4 left-4 z-20 pointer-events-none glass-panel px-3.5 py-2 rounded-2xl border border-emerald-500/30 flex items-center gap-3">
            <div className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse" />
              <span className="text-[11px] font-bold text-white">
                {filteredOutbreaks.filter((o) => o.severity === "Severe").length} {t.map.severeHotspots}
              </span>
            </div>
            <div className="h-3 w-px bg-emerald-700/50" />
            <span className="text-[11px] text-emerald-300 font-semibold">
              {filteredOutbreaks.length} {t.map.totalClusters}
            </span>
          </div>

          {/* Map Legend */}
          <div className="absolute bottom-4 left-4 z-20 pointer-events-none glass-panel px-3.5 py-2 rounded-2xl border border-emerald-900/60 flex items-center gap-4 text-[10px] font-semibold text-emerald-200">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-red-500" />
              <span>{t.map.severeOnly}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-amber-400" />
              <span>{t.map.moderate}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              <span>{t.map.lowHealthy}</span>
            </div>
          </div>
        </div>

        {/* Sidebar: Outbreak Clusters List */}
        <div className="space-y-3 flex flex-col h-[550px]">
          <div className="flex items-center justify-between px-1">
            <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400">
              {t.map.activeList} ({filteredOutbreaks.length})
            </h4>
            <span className="text-[10px] text-emerald-400/60 font-mono">
              {t.map.liveFeed}
            </span>
          </div>

          <div className="flex-1 overflow-y-auto space-y-2.5 pr-1">
            {filteredOutbreaks.length === 0 ? (
              <div className="p-8 text-center glass-panel rounded-2xl text-xs text-emerald-300/60">
                No outbreak clusters match your active filters.
              </div>
            ) : (
              filteredOutbreaks.map((cluster) => {
                const isSelected = activeCluster?.id === cluster.id;
                const isSevere = cluster.severity === "Severe";
                const isMod = cluster.severity === "Moderate";

                return (
                  <div
                    key={cluster.id}
                    onClick={() => flyToCluster(cluster)}
                    className={`p-3.5 rounded-2xl border transition-all cursor-pointer ${
                      isSelected
                        ? "bg-emerald-950/90 border-emerald-400 shadow-lg shadow-emerald-950"
                        : "glass-panel hover:bg-emerald-950/60 border-emerald-900/50 hover:border-emerald-700/60"
                    }`}
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-bold text-white">
                            {cluster.crop_name}
                          </span>
                          <span
                            className={`text-[9px] font-bold px-1.5 py-0.2 rounded-full border ${
                              isSevere
                                ? "bg-red-500/20 text-red-300 border-red-500/40"
                                : isMod
                                ? "bg-amber-500/20 text-amber-300 border-amber-500/40"
                                : "bg-emerald-500/20 text-emerald-300 border-emerald-500/40"
                            }`}
                          >
                            {cluster.severity}
                          </span>
                        </div>
                        <p className="text-xs font-semibold text-emerald-200 mt-0.5 truncate">
                          {cluster.disease_detected}
                        </p>
                      </div>

                      <ArrowRight className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-1" />
                    </div>

                    <div className="flex items-center justify-between text-[10px] text-emerald-400/70 mt-2.5 pt-2 border-t border-emerald-950">
                      <span>{(cluster.confidence_score * 100).toFixed(0)}% Certainty</span>
                      {cluster.distance_km && (
                        <span className="font-mono text-emerald-300 font-semibold">
                          {cluster.distance_km} km away
                        </span>
                      )}
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
