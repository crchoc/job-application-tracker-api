from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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


class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=100)
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class User(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


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
    user_id: int

    model_config = ConfigDict(from_attributes=True)


class ApplicationSummary(BaseModel):
    total: int
    saved: int
    applied: int
    interview: int
    rejected: int
    offer: int