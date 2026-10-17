from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class SeverityEnum(str, Enum):
    LOW = "Low"
    MODERATE = "Moderate"
    SEVERE = "Severe"

class DomainCategory(str, Enum):
    CROP_LEAF = "Crop / Plant Foliage"
    ANIMAL_LIVESTOCK = "Livestock / Animal Pathology"
    NON_AGRICULTURAL = "Non-Agricultural / Invalid Image"

class PathogenType(str, Enum):
    # Plant Pathogens
    FUNGAL = "Fungal"
    BACTERIAL = "Bacterial"
    VIRAL = "Viral"
    PEST = "Pest / Insect"
    NUTRIENT_DEFICIENCY = "Nutrient Deficiency / Physiological"
    HEALTHY = "Healthy Leaf"
    # Veterinary / Animal Pathogens
    VETERINARY_VIRAL = "Veterinary Viral (Animal)"
    VETERINARY_PARASITIC = "Veterinary Parasitic / Mange (Animal)"
    VETERINARY_FUNGAL = "Veterinary Fungal / Ringworm (Animal)"
    VETERINARY_BACTERIAL = "Veterinary Bacterial (Animal)"
    VETERINARY_GENERAL = "Veterinary / Livestock Disorder"
    # Fallback / Out of bounds
    INVALID_SUBJECT = "Non-Agricultural / Invalid Subject"
    UNKNOWN = "Unknown / Rare Anomaly"

class OrganicRemedyDetails(BaseModel):
    summary: str
    preparation: str = "N/A"
    application_frequency: str = "N/A"
    preventive_cultural_practices: List[str] = Field(default_factory=list)

class ChemicalRemedyDetails(BaseModel):
    summary: str
    active_ingredient: str = "N/A"
    dosage_per_liter: str = "N/A"
    dosage_per_hectare_or_acre: str = "N/A"
    pre_harvest_interval_days: int = 0
    safety_precautions: List[str] = Field(default_factory=list)

class DiagnosticResponse(BaseModel):
    scan_id: Optional[str] = None
    domain_category: DomainCategory = DomainCategory.CROP_LEAF
    is_animal_disease: bool = False
    is_valid_agricultural_image: bool = True
    is_wrong_photo: bool = False
    wrong_photo_reason: Optional[str] = None
    animal_warning: Optional[str] = None
    crop_name: str
    scientific_crop_name: Optional[str] = None
    disease_detected: str
    pathogen_type: PathogenType
    confidence_score: float = Field(ge=0.0, le=1.0)
    severity: SeverityEnum
    infection_percentage: float = Field(ge=0.0, le=100.0, description="Estimated lesion surface coverage %")
    symptoms_observed: List[str] = Field(default_factory=list)
    organic_remedy: str
    organic_details: Optional[OrganicRemedyDetails] = None
    chemical_remedy: str
    chemical_details: Optional[ChemicalRemedyDetails] = None
    urgency: str
    cnn_metrics: Optional[dict] = None
    localized_speech_summary: dict = Field(
        default_factory=lambda: {
            "en": "",
            "kn": "",
            "hi": "",
            "es": "",
            "sw": "",
            "fr": ""
        }
    )
    inference_time_ms: float
    model_used: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ScanRequestPayload(BaseModel):
    image_base64: str
    user_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    crop_hint: Optional[str] = None
    preferred_language: str = "en"

class UserCreate(BaseModel):
    full_name: str
    phone_number: str
    preferred_language: str = "en"

class UserResponse(BaseModel):
    id: str
    full_name: str
    phone_number: str
    preferred_language: str
    created_at: datetime

class DiseaseScanRecord(BaseModel):
    id: str
    user_id: Optional[str] = None
    crop_name: str
    disease_detected: str
    confidence_score: float
    severity: SeverityEnum
    organic_remedy: Optional[str] = None
    chemical_remedy: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    scanned_at: datetime

class OutbreakCluster(BaseModel):
    id: str
    crop_name: str
    disease_detected: str
    severity: SeverityEnum
    confidence_score: float
    latitude: float
    longitude: float
    distance_km: Optional[float] = None
    scanned_at: datetime

class NearbyOutbreakQuery(BaseModel):
    latitude: float
    longitude: float
    radius_km: float = 50.0
