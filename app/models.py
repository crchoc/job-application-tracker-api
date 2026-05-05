from sqlalchemy import Column, Integer, String

from app.database import Base


class JobApplicationModel(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, nullable=False, default="saved")
    job_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    notes = Column(String, nullable=True)