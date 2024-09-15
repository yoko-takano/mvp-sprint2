from pydantic import BaseModel
from typing import List, Optional
from api.model.patient import Patient


class PatientCreateSchema(BaseModel):
    """Schema for representing a new patient to be created."""
    name: str = "Paula"
    mean_radius: float = 17.99
    mean_texture: float = 10.38
    mean_perimeter: float = 122.8
    mean_area: float = 1001.0
    mean_smoothness: float = 0.1184


class PatientViewSchema(BaseModel):
    """Schema for representing a patient as returned by the system."""
    id: int = 1
    mean_radius: float = 17.99
    mean_texture: float = 10.38
    mean_perimeter: float = 122.8
    mean_area: float = 1001.0
    mean_smoothness: float = 0.1184
    diagnosis: Optional[bool] = None


class PatientSearchSchema(BaseModel):
    """Schema for representing the search query for a patient by name."""
    name: str = "Paula"


class PatientListSchema(BaseModel):
    """Schema for representing a list of patients."""
    patients: List[PatientViewSchema]


class PatientDeleteSchema(BaseModel):
    """Schema for representing a patient to be deleted."""
    name: str = "Paula"


def represent_patient(patient: Patient) -> dict:
    """Returns a representation of a patient following the PatientViewSchema."""
    return {
        "id": patient.id,
        "name": patient.name,
        "mean_radius": patient.mean_radius,
        "mean_texture": patient.mean_texture,
        "mean_perimeter": patient.mean_perimeter,
        "mean_area": patient.mean_area,
        "mean_smoothness": patient.mean_smoothness,
        "diagnosis": patient.diagnosis
    }


def represent_patients(patients: List[Patient]) -> dict:
    """Returns a representation of a list of patients following the PatientViewSchema."""
    return {"patients": [represent_patient(patient) for patient in patients]}
