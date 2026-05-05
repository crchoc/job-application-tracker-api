from typing import List

from app.schemas import JobApplication, JobApplicationCreate, JobApplicationUpdate


applications: List[JobApplication] = []
next_id = 1


def create_application(application_data: JobApplicationCreate) -> JobApplication:
    global next_id

    new_application = JobApplication(
        id=next_id,
        **application_data.model_dump()
    )

    applications.append(new_application)
    next_id += 1

    return new_application


def get_all_applications() -> List[JobApplication]:
    return applications


def get_application_by_id(application_id: int) -> JobApplication | None:
    for application in applications:
        if application.id == application_id:
            return application

    return None


def update_application(application_id: int, update_data: JobApplicationUpdate) -> JobApplication | None:
    application = get_application_by_id(application_id)

    if application is None:
        return None

    update_dict = update_data.model_dump(exclude_unset=True)

    for field, value in update_dict.items():
        setattr(application, field, value)

    return application


def delete_application(application_id: int) -> bool:
    application = get_application_by_id(application_id)

    if application is None:
        return False

    applications.remove(application)
    return True