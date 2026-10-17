-- =======================================================================
-- AgriVision AI – Universal Crop Disease Diagnostic & Agronomy Engine
-- Database Schema & PostGIS Spatial Extension for Supabase PostgreSQL
-- =======================================================================

-- 1. Enable PostGIS extension for spatial/geographical queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name TEXT NOT NULL,
    phone_number TEXT UNIQUE NOT NULL,
    preferred_language TEXT DEFAULT 'en',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create Disease Scans Table with PostGIS Geography (EPSG:4326)
CREATE TABLE IF NOT EXISTS disease_scans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    crop_name TEXT NOT NULL,
    disease_detected TEXT NOT NULL,
    confidence_score FLOAT NOT NULL CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    severity TEXT NOT NULL CHECK (severity IN ('Low', 'Moderate', 'Severe')),
    organic_remedy TEXT,
    chemical_remedy TEXT,
    location GEOGRAPHY(Point, 4326),
    image_url TEXT,
    scanned_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Spatial Index on Geography column for sub-second geospatial radius queries
CREATE INDEX IF NOT EXISTS idx_disease_scans_location 
    ON disease_scans USING GIST (location);

-- Index on crop_name & disease_detected for outbreak analytics
CREATE INDEX IF NOT EXISTS idx_disease_scans_crop 
    ON disease_scans(crop_name);

CREATE INDEX IF NOT EXISTS idx_disease_scans_disease 
    ON disease_scans(disease_detected);

CREATE INDEX IF NOT EXISTS idx_disease_scans_scanned_at 
    ON disease_scans(scanned_at DESC);

-- 5. Helper Function: Find Outbreak Clusters within Radius
-- Usage: SELECT * FROM get_nearby_outbreaks(28.6139, 77.2090, 50);
CREATE OR REPLACE FUNCTION get_nearby_outbreaks(
    center_lat FLOAT,
    center_lng FLOAT,
    radius_km FLOAT DEFAULT 50.0
)
RETURNS TABLE (
    id UUID,
    crop_name TEXT,
    disease_detected TEXT,
    severity TEXT,
    confidence_score FLOAT,
    latitude FLOAT,
    longitude FLOAT,
    distance_km FLOAT,
    scanned_at TIMESTAMP WITH TIME ZONE
)
LANGUAGE sql
AS $$
    SELECT 
        id,
        crop_name,
        disease_detected,
        severity,
        confidence_score,
        ST_Y(location::geometry) AS latitude,
        ST_X(location::geometry) AS longitude,
        ROUND((ST_Distance(location, ST_SetSRID(ST_MakePoint(center_lng, center_lat), 4326)::geography) / 1000)::numeric, 2)::float AS distance_km,
        scanned_at
    FROM disease_scans
    WHERE ST_DWithin(
        location,
        ST_SetSRID(ST_MakePoint(center_lng, center_lat), 4326)::geography,
        radius_km * 1000
    )
    ORDER BY distance_km ASC;
$$;

-- 6. Helper Function: Outbreak Summary by Crop & Severity
CREATE OR REPLACE FUNCTION get_outbreak_summary()
RETURNS TABLE (
    crop_name TEXT,
    disease_detected TEXT,
    total_cases BIGINT,
    severe_cases BIGINT,
    avg_confidence FLOAT
)
LANGUAGE sql
AS $$
    SELECT 
        crop_name,
        disease_detected,
        COUNT(*) AS total_cases,
        COUNT(*) FILTER (WHERE severity = 'Severe') AS severe_cases,
        ROUND(AVG(confidence_score)::numeric, 3)::float AS avg_confidence
    FROM disease_scans
    GROUP BY crop_name, disease_detected
    ORDER BY total_cases DESC;
$$;

-- 7. Seed Data: Default Demo User
INSERT INTO users (id, full_name, phone_number, preferred_language)
VALUES 
    ('00000000-0000-0000-0000-000000000001', 'Farmer Rajesh Kumar', '+919876543210', 'hi'),
    ('00000000-0000-0000-0000-000000000002', 'Dr. Sarah Jenkins (Agronomist)', '+14155550199', 'en')
ON CONFLICT (phone_number) DO NOTHING;

-- 8. Seed Data: Global Outbreak Clusters
INSERT INTO disease_scans (user_id, crop_name, disease_detected, confidence_score, severity, organic_remedy, chemical_remedy, location, scanned_at)
VALUES
    -- Tomato Late Blight cluster (Indo-Gangetic Plain)
    ('00000000-0000-0000-0000-000000000001', 'Tomato', 'Late Blight (Phytophthora infestans)', 0.96, 'Severe', 
     'Apply Copper octanoate or Trichoderma harzianum; prune infected canopy and destroy foliage.', 
     'Apply Cymoxanil 8% + Mancozeb 64% WP at 2.5g/L water with a 7-day pre-harvest interval.', 
     ST_SetSRID(ST_MakePoint(77.2090, 28.6139), 4326)::geography, NOW() - INTERVAL '2 hours'),
     
    ('00000000-0000-0000-0000-000000000001', 'Tomato', 'Late Blight (Phytophthora infestans)', 0.94, 'Severe', 
     'Spray 5% Neem oil emulsion every 5 days; avoid overhead drip irrigation.', 
     'Apply Metalaxyl-M + Mancozeb (Ridomil Gold) at 2.5 kg/ha.', 
     ST_SetSRID(ST_MakePoint(77.2300, 28.6300), 4326)::geography, NOW() - INTERVAL '5 hours'),

    -- Rice Bacterial Leaf Blight (Punjab / Haryana)
    ('00000000-0000-0000-0000-000000000001', 'Rice (Paddy)', 'Bacterial Leaf Blight (Xanthomonas oryzae)', 0.92, 'Moderate', 
     'Fresh cow dung extract spray (20%) or Pseudomonas fluorescens @ 10g/L.', 
     'Streptomycin sulphate + Tetracycline hydrochloride (90:10) at 6g + Copper Oxychloride 50 WP 25g in 10L water.', 
     ST_SetSRID(ST_MakePoint(76.8512, 30.7333), 4326)::geography, NOW() - INTERVAL '1 day'),

    -- Potato Early Blight (Central Valley / California)
    ('00000000-0000-0000-0000-000000000002', 'Potato', 'Early Blight (Alternaria solani)', 0.89, 'Moderate', 
     'Bacillus subtilis bio-fungicide soil drench and compost tea foliar spray.', 
     'Azoxystrobin 23% SC at 1ml/L or Chlorothalonil 75% WP at 2g/L.', 
     ST_SetSRID(ST_MakePoint(-119.7871, 36.7468), 4326)::geography, NOW() - INTERVAL '18 hours'),

    -- Corn Fall Armyworm (Midwest US / Iowa)
    ('00000000-0000-0000-0000-000000000002', 'Maize (Corn)', 'Fall Armyworm Infestation (Spodoptera frugiperda)', 0.95, 'Severe', 
     'Bacillus thuringiensis (Bt) kurstaki strain foliar spray; release Trichogramma wasps.', 
     'Emamectin benzoate 5% SG at 0.4g/L or Spinetoram 11.7% SC at 0.5ml/L.', 
     ST_SetSRID(ST_MakePoint(-93.6091, 41.5868), 4326)::geography, NOW() - INTERVAL '8 hours'),

    -- Wheat Stripe Rust (Rift Valley, Kenya)
    (NULL, 'Wheat', 'Stripe / Yellow Rust (Puccinia striiformis)', 0.91, 'Severe', 
     'Resistant cultivar rotation; sulfur dust broadcast during early morning humidity.', 
     'Tebuconazole 250 EC at 1L/ha or Propiconazole 25% EC at 500ml/ha.', 
     ST_SetSRID(ST_MakePoint(36.0667, -0.3000), 4326)::geography, NOW() - INTERVAL '12 hours'),

    -- Healthy Citrus (Florida)
    ('00000000-0000-0000-0000-000000000002', 'Citrus (Orange)', 'Healthy - No Pathogen Detected', 0.98, 'Low', 
     'Maintain balanced potassium-nitrogen foliar nutrition and root aeration.', 
     'No chemical intervention required. Preventive copper spray optional during pre-monsoon flush.', 
     ST_SetSRID(ST_MakePoint(-81.5158, 28.5383), 4326)::geography, NOW() - INTERVAL '1 day')
ON CONFLICT DO NOTHING;
