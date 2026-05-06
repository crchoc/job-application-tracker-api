from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ApplicationStatus(str, Enum):
    saved = "saved"
    applied = "applied"
    interview = "interview"
    rejected = "rejected"
    offer = "offer"


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class SortBy(str, Enum):
    id = "id"
    company = "company"
    position = "position"
    status = "status"
    location = "location"


class JobApplicationCreate(BaseModel):
    company: str = Field(..., min_length=1, max_length=100)
    position: str = Field(..., min_length=1, max_length=100)
    status: ApplicationStatus = ApplicationStatus.saved
    job_url: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class JobApplicationUpdate(BaseModel):
    company: Optional[str] = Field(None, min_length=1, max_length=100)
    position: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[ApplicationStatus] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None


class JobApplication(JobApplicationCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ApplicationSummary(BaseModel):
    total: int
    saved: int
    applied: int
    interview: int
    rejected: int
    offer: int