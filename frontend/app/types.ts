export type SeverityLevel = "Low" | "Moderate" | "Severe";

export type DomainCategory = 
  | "Crop / Plant Foliage" 
  | "Livestock / Animal Pathology" 
  | "Non-Agricultural / Invalid Image";

export type PathogenType = 
  | "Fungal" 
  | "Bacterial" 
  | "Viral" 
  | "Pest / Insect" 
  | "Nutrient Deficiency / Physiological" 
  | "Healthy Leaf" 
  | "Veterinary Viral (Animal)"
  | "Veterinary Parasitic / Mange (Animal)"
  | "Veterinary Fungal / Ringworm (Animal)"
  | "Veterinary Bacterial (Animal)"
  | "Veterinary / Livestock Disorder"
  | "Non-Agricultural / Invalid Subject"
  | "Unknown / Rare Anomaly";

export interface OrganicRemedyDetails {
  summary: string;
  preparation: string;
  application_frequency: string;
  preventive_cultural_practices: string[];
}

export interface ChemicalRemedyDetails {
  summary: string;
  active_ingredient: string;
  dosage_per_liter: string;
  dosage_per_hectare_or_acre: string;
  pre_harvest_interval_days: number;
  safety_precautions: string[];
}

export interface DiagnosticResponse {
  scan_id?: string;
  domain_category?: DomainCategory;
  is_animal_disease?: boolean;
  is_valid_agricultural_image?: boolean;
  is_wrong_photo?: boolean;
  wrong_photo_reason?: string;
  animal_warning?: string;
  crop_name: string;
  scientific_crop_name?: string;
  disease_detected: string;
  pathogen_type: PathogenType;
  confidence_score: number;
  severity: SeverityLevel;
  infection_percentage: number;
  symptoms_observed: string[];
  organic_remedy: string;
  organic_details?: OrganicRemedyDetails;
  chemical_remedy: string;
  chemical_details?: ChemicalRemedyDetails;
  urgency: string;
  cnn_metrics?: {
    cnn_confidence: number;
    cnn_domain?: string;
    is_crop_leaf?: boolean;
    is_wrong_photo?: boolean;
    wrong_photo_type?: string;
    leaf_probability?: number;
    animal_probability?: number;
    foliar_score?: number;
    animal_score?: number;
    feature_energy: number;
    laplacian_variance: number;
    lesion_count: number;
    cnn_lesion_percentage: number;
    cnn_model_name: string;
  };
  localized_speech_summary: Record<string, string>;
  inference_time_ms: number;
  model_used: string;
  timestamp: string;
}

export interface SampleLeaf {
  id: string;
  title: string;
  crop: string;
  domain?: string;
  expected_disease: string;
  expected_severity: SeverityLevel;
  thumbnail_color: string;
  image_data: string;
  description: string;
}

export interface OutbreakCluster {
  id: string;
  crop_name: string;
  disease_detected: string;
  severity: SeverityLevel;
  confidence_score: number;
  latitude: number;
  longitude: number;
  distance_km?: number;
  scanned_at: string;
}

export interface DiseaseScanHistoryItem {
  id: string;
  user_id?: string;
  crop_name: string;
  disease_detected: string;
  confidence_score: number;
  severity: SeverityLevel;
  organic_remedy?: string;
  chemical_remedy?: string;
  latitude?: number;
  longitude?: number;
  scanned_at: string;
}

export interface AnalyticsSummary {
  total_scans: number;
  severe_outbreaks: number;
  top_crops: Array<{ crop: string; count: number }>;
  top_diseases: Array<{ disease: string; count: number }>;
}
