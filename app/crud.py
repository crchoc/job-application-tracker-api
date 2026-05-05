from typing import List, Optional

from sqlalchemy.orm import Session

from app.models import JobApplicationModel
from app.schemas import JobApplicationCreate, JobApplicationUpdate


def create_application(
    db: Session,
    application_data: JobApplicationCreate
) -> JobApplicationModel:
    new_application = JobApplicationModel(
        company=application_data.company,
        position=application_data.position,
        status=application_data.status.value,
        job_url=application_data.job_url,
        location=application_data.location,
        notes=application_data.notes
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


def get_all_applications(db: Session) -> List[JobApplicationModel]:
    return db.query(JobApplicationModel).all()


def get_application_by_id(
    db: Session,
    application_id: int
) -> Optional[JobApplicationModel]:
    return (
        db.query(JobApplicationModel)
        .filter(JobApplicationModel.id == application_id)
        .first()
    )


def update_application(
    db: Session,
    application_id: int,
    update_data: JobApplicationUpdate
) -> Optional[JobApplicationModel]:
    application = get_application_by_id(db, application_id)

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
    application_id: int
) -> bool:
    application = get_application_by_id(db, application_id)

    if application is None:
        return False

    db.delete(application)
    db.commit()

    return True