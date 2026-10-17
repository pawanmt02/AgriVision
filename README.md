# AgriVision AI – Universal Crop Disease Diagnostic & Agronomy Engine

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16.4+-black.svg?logo=next.js&logoColor=white)](https://nextjs.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-v4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com)
[![Leaflet GIS](https://img.shields.io/badge/Leaflet-GIS_Mapping-199900.svg?logo=leaflet&logoColor=white)](https://leafletjs.com)
[![Groq Vision](https://img.shields.io/badge/Groq-LLaMA--3.2--11B--Vision-f55036.svg)](https://groq.com)
[![Supabase PostGIS](https://img.shields.io/badge/Supabase-PostGIS_Spatial-3ECF8E.svg?logo=supabase&logoColor=white)](https://supabase.com)

**AgriVision AI** is an agricultural intelligence platform engineered to bridge the critical gap between smallholder farmers and certified plant pathology. By combining a hybrid computer vision and multi-modal vision-language architecture, the platform enables farmers and agronomists to capture or upload crop leaf photographs, instantly diagnose diseases across global staple and cash crops, assess foliar infection severity, and receive actionable organic and chemical treatment guidelines with localized voice read-outs.

---

## 🌟 Key Capabilities & Architectural Highlights

1. **Universal Multi-Crop Support & Zero-Shot Fallback**
   - Supports Solanaceae (Tomato, Potato, Pepper, Eggplant), Cereals (Rice, Maize/Corn, Wheat), Cash crops (Cotton, Coffee, Sugarcane), Fruits (Apple, Citrus, Banana), and Legumes (Soybean).
   - Zero-shot botanical fallback engine detects anomalies and formulates broad-spectrum bio-fungicide and quarantine measures for rare, unlisted plants.

2. **Sub-4-Second Multi-Modal AI Inference**
   - Integrates **Groq Vision** (`llama-3.2-11b-vision-preview` / `llama-3.2-90b-vision-preview`) with structured JSON schema output validation.
   - Built-in **Plant Pathology Heuristic Core** provides offline/zero-config fallback with cellular necrosis index, chlorosis gradient analysis, and spot configuration classification.

3. **Actionable Dual-Pathway Agronomy**
   - **🌱 Organic & Eco-Friendly Controls**: Natural formulations (Neem oil, Bacillus subtilis, Trichoderma, Copper octanoate), dilution recipes, application schedules, and preventive cultural farming practices.
   - **🧪 Chemical & Targeted Controls**: Active molecule recommendations, FRAC resistance group rotation, dilution per Liter, dosage per Acre/Hectare, mandatory Pre-Harvest Interval (PHI in days), and worker PPE safety warnings.

4. **Multi-Language Spoken Voice Read-Out (TTS)**
   - Integrated accessibility text-to-speech engine reading out diagnostic results in **English, Hindi (हिंदी), Spanish (Español), Swahili (Kiswahili), and French (Français)**.

5. **Geospatial Outbreak GIS Mapping (Supabase PostGIS)**
   - Maps GPS coordinates of every scan to track regional pathogen vectors.
   - Interactive dark-mode cartography with color-coded severity pins, epidemic risk badges, distance-from-farm calculations, and crop filters.

6. **Animated & High-Tech Mobile Viewfinder**
   - Animated laser beam scanning across the leaf.
   - Real-time diagnostic telemetry HUD ("Acquiring pixels...", "Segmenting contours...", "Running vision-agronomy neural synthesis...").
   - 1-click test gallery with pre-loaded realistic sample leaves for instant verification.

---

## 🏗️ System Architecture & Data Flow

```text
[ Farmer / Mobile Camera ] 
          │
          ▼ (Image File + GPS Coordinates)
[ Next.js Progressive Web App (Frontend - Port 3000) ]
          │
          ▼ (HTTP POST Multipart / JSON Request)
[ Python FastAPI Server (Backend Core - Port 8000) ]
          │
          ├──> [ Groq LLaMA-3.2-11B Multi-Modal Vision Model ]
          ├──> [ Computer Vision & Necrosis Heuristic Core ]
          └──> [ Agronomy Knowledge & Dosage Synthesizer ]
          │
          ▼ (Structured JSON Diagnostic Response)
[ Supabase Spatial Database (PostGIS Outbreak Log / Local SQLite) ]
```

---

## 🗄️ Database Schema & PostGIS Integration

The database is defined in `supabase/schema.sql` with full PostGIS geography support:

### Table 1: `users`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key, `gen_random_uuid()` | Unique user identifier |
| `full_name` | TEXT | Not Null | Farmer or agronomist name |
| `phone_number` | TEXT | Unique, Not Null | Primary contact reference |
| `preferred_language` | TEXT | Default `'en'` | Preferred interface & speech language |
| `created_at` | TIMESTAMP | Default `NOW()` | Account creation timestamp |

### Table 2: `disease_scans`
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | UUID | Primary Key, `gen_random_uuid()` | Unique scan record ID |
| `user_id` | UUID | Foreign Key (`users.id`) | References scanning user |
| `crop_name` | TEXT | Not Null | Identified crop or plant family |
| `disease_detected` | TEXT | Not Null | Disease name or "Healthy" |
| `confidence_score` | FLOAT | `0.0` to `1.0` | Model certainty metric |
| `severity` | TEXT | Check (`Low`, `Moderate`, `Severe`) | Infection intensity level |
| `organic_remedy` | TEXT | Nullable | Recommended biological control |
| `chemical_remedy` | TEXT | Nullable | Recommended chemical treatment plan |
| `location` | GEOGRAPHY | Point, `EPSG:4326` | GPS coordinates of the scan |
| `scanned_at` | TIMESTAMP | Default `NOW()` | Timestamp of diagnostic execution |

---

## 🚀 Quickstart Guide

### 1. Requirements
- Node.js 18+ (tested with v24.13.0)
- Python 3.10+ (tested with v3.13)

### 2. Launch with One Click
On Windows, double-click:
```bash
start-agrivision.bat
```
Or in PowerShell:
```powershell
.\start-agrivision.ps1
```

### 3. Manual Launch

#### Backend:
```bash
cd backend
python -m pip install -r requirements.txt
python main.py
```
*API running at:* `http://localhost:8005` (Swagger interactive docs at `http://localhost:8005/docs`)

#### Frontend:
```bash
cd frontend
npm install
npm run dev
```
*Web App running at:* `http://localhost:3000`

---

## 🧪 Testing & Validation

Run the automated backend test suite:
```bash
cd backend
python test_api.py
```

Tests verify:
- Health check SLA
- Sample leaf gallery generation
- Multi-modal diagnosis pipeline
- Pydantic schema validation
- Geospatial outbreak radius queries
- Statistical analytics aggregation

---

## 🌐 Environment Variables (Optional)

Create a `backend/.env` file:
```env
# Optional Groq Vision Key (Free keys at https://console.groq.com)
GROQ_API_KEY=gsk_...

# Optional Supabase PostGIS Database URL & Key
SUPABASE_URL=https://xyz.supabase.co
SUPABASE_KEY=eyJ...
```
*Note: If no API keys are provided, AgriVision AI automatically engages its built-in expert plant pathology heuristic synthesizer, ensuring 100% functionality out-of-the-box!*
