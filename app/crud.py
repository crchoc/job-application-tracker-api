from typing import List, Optional

from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from app.models import JobApplicationModel
from app.schemas import (
    ApplicationStatus,
    JobApplicationCreate,
    JobApplicationUpdate,
    SortBy,
    SortOrder,
)


def create_application(
    db: Session,
    application_data: JobApplicationCreate,
    user_id: int
) -> JobApplicationModel:
    new_application = JobApplicationModel(
        company=application_data.company,
        position=application_data.position,
        status=application_data.status.value,
        job_url=application_data.job_url,
        location=application_data.location,
        notes=application_data.notes,
        user_id=user_id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


def get_all_applications(
    db: Session,
    user_id: int,
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: SortBy = SortBy.id,
    sort_order: SortOrder = SortOrder.asc,
    skip: int = 0,
    limit: int = 20
) -> List[JobApplicationModel]:
    query = db.query(JobApplicationModel).filter(
        JobApplicationModel.user_id == user_id
    )

    if status is not None:
        query = query.filter(JobApplicationModel.status == status.value)

    if company is not None:
        query = query.filter(JobApplicationModel.company.ilike(f"%{company}%"))

    if location is not None:
        query = query.filter(JobApplicationModel.location.ilike(f"%{location}%"))

    if search is not None:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                JobApplicationModel.company.ilike(search_pattern),
                JobApplicationModel.position.ilike(search_pattern),
                JobApplicationModel.location.ilike(search_pattern),
                JobApplicationModel.notes.ilike(search_pattern),
            )
        )

    sort_column = getattr(JobApplicationModel, sort_by.value)

    if sort_order == SortOrder.desc:
        sort_column = sort_column.desc()

    query = query.order_by(sort_column)

    return query.offset(skip).limit(limit).all()


def count_applications(
    db: Session,
    user_id: int,
    status: Optional[ApplicationStatus] = None,
    company: Optional[str] = None,
    location: Optional[str] = None,
    search: Optional[str] = None,
) -> int:
    query = db.query(JobApplicationModel).filter(
        JobApplicationModel.user_id == user_id
    )

    if status is not None:
        query = query.filter(JobApplicationModel.status == status.value)

    if company is not None:
        query = query.filter(JobApplicationModel.company.ilike(f"%{company}%"))

    if location is not None:
        query = query.filter(JobApplicationModel.location.ilike(f"%{location}%"))

    if search is not None:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                JobApplicationModel.company.ilike(search_pattern),
                JobApplicationModel.position.ilike(search_pattern),
                JobApplicationModel.location.ilike(search_pattern),
                JobApplicationModel.notes.ilike(search_pattern),
            )
        )

    return query.count()


def get_application_by_id(
    db: Session,
    application_id: int,
    user_id: int
) -> Optional[JobApplicationModel]:
    return (
        db.query(JobApplicationModel)
        .filter(
            JobApplicationModel.id == application_id,
            JobApplicationModel.user_id == user_id
        )
        .first()
    )


def update_application(
    db: Session,
    application_id: int,
    update_data: JobApplicationUpdate,
    user_id: int
) -> Optional[JobApplicationModel]:
    application = get_application_by_id(
        db=db,
        application_id=application_id,
        user_id=user_id
    )

    if application is None:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        if field == "status" and value is not None:
            value = value.value

        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application


def delete_application(
    db: Session,
    application_id: int,
    user_id: int
) -> bool:
    application = get_application_by_id(
        db=db,
        application_id=application_id,
        user_id=user_id
    )

    if application is None:
        return False

    db.delete(application)
    db.commit()

    return True


def get_application_summary(
    db: Session,
    user_id: int
) -> dict:
    total = (
        db.query(JobApplicationModel)
        .filter(JobApplicationModel.user_id == user_id)
        .count()
    )

    status_counts = (
        db.query(
            JobApplicationModel.status,
            func.count(JobApplicationModel.id)
        )
        .filter(JobApplicationModel.user_id == user_id)
        .group_by(JobApplicationModel.status)
        .all()
    )

    summary = {
        "total": total,
        "saved": 0,
        "applied": 0,
        "interview": 0,
        "rejected": 0,
        "offer": 0,
    }

    for status, count in status_counts:
        if status in summary:
            summary[status] = count

    return summary