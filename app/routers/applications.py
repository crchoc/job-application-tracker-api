from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.database import get_db
from app.schemas import JobApplication, JobApplicationCreate, JobApplicationUpdate


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("", response_model=JobApplication)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db)
):
    return crud.create_application(db, application)


@router.get("", response_model=List[JobApplication])
def get_applications(db: Session = Depends(get_db)):
    return crud.get_all_applications(db)


@router.get("/{application_id}", response_model=JobApplication)
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = crud.get_application_by_id(db, application_id)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@router.patch("/{application_id}", response_model=JobApplication)
def update_application(
    application_id: int,
    update_data: JobApplicationUpdate,
    db: Session = Depends(get_db)
):
    application = crud.update_application(db, application_id, update_data)

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    deleted = crud.delete_application(db, application_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Application not found")

    return {"message": "Application deleted successfully"}