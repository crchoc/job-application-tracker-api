from typing import List

from fastapi import APIRouter, HTTPException

from app.schemas import JobApplication, JobApplicationCreate, JobApplicationUpdate
from app import storage


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("", response_model=JobApplication)
def create_application(application: JobApplicationCreate):
    return storage.create_application(application)


@router.get("", response_model=List[JobApplication])
def get_applications():
    return storage.get_all_applications()


@router.get("/{application_id}", response_model=JobApplication)
def get_application(application_id: int):
    application = storage.get_application_by_id(application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@router.patch("/{application_id}", response_model=JobApplication)
def update_application(application_id: int, update_data: JobApplicationUpdate):
    application = storage.update_application(application_id, update_data)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@router.delete("/{application_id}")
def delete_application(application_id: int):
    deleted = storage.delete_application(application_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")

    return {"message": "Application deleted successfully"}