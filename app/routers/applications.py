from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.auth import get_current_user
from app.database import get_db
from app.models import UserModel
from app.schemas import (
    ApplicationStatus,
    ApplicationSummary,
    JobApplication,
    JobApplicationCreate,
    JobApplicationUpdate,
    SortBy,
    SortOrder,
)


router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("", response_model=JobApplication)
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return crud.create_application(
        db=db,
        application_data=application,
        user_id=current_user.id,
    )


@router.get("", response_model=List[JobApplication])
def get_applications(
    status: Optional[ApplicationStatus] = Query(
        None,
        description="Filter by application status"
    ),
    company: Optional[str] = Query(
        None,
        description="Filter by company name"
    ),
    location: Optional[str] = Query(
        None,
        description="Filter by location"
    ),
    search: Optional[str] = Query(
        None,
        description="Search company, position, location, or notes"
    ),
    sort_by: SortBy = Query(
        SortBy.id,
        description="Field used for sorting"
    ),
    sort_order: SortOrder = Query(
        SortOrder.asc,
        description="Sort order"
    ),
    skip: int = Query(
        0,
        ge=0,
        description="Number of records to skip"
    ),
    limit: int = Query(
        20,
        ge=1,
        le=100,
        description="Maximum number of records to return"
    ),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return crud.get_all_applications(
        db=db,
        user_id=current_user.id,
        status=status,
        company=company,
        location=location,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )


@router.get("/count")
def count_applications(
    status: Optional[ApplicationStatus] = Query(
        None,
        description="Filter by application status"
    ),
    company: Optional[str] = Query(
        None,
        description="Filter by company name"
    ),
    location: Optional[str] = Query(
        None,
        description="Filter by location"
    ),
    search: Optional[str] = Query(
        None,
        description="Search company, position, location, or notes"
    ),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    total = crud.count_applications(
        db=db,
        user_id=current_user.id,
        status=status,
        company=company,
        location=location,
        search=search,
    )

    return {"count": total}


@router.get("/summary", response_model=ApplicationSummary)
def get_application_summary(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return crud.get_application_summary(
        db=db,
        user_id=current_user.id,
    )


@router.get("/{application_id}", response_model=JobApplication)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    application = crud.get_application_by_id(
        db=db,
        application_id=application_id,
        user_id=current_user.id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.patch("/{application_id}", response_model=JobApplication)
def update_application(
    application_id: int,
    update_data: JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    application = crud.update_application(
        db=db,
        application_id=application_id,
        update_data=update_data,
        user_id=current_user.id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@router.delete("/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    deleted = crud.delete_application(
        db=db,
        application_id=application_id,
        user_id=current_user.id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return {"message": "Application deleted successfully"}