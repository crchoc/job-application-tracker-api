from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional, List

app = FastAPI(
    title="Job Application Tracker API",
    description="A simple API for tracking job applications.",
    version="0.1.0"
)

class JobApplicationCreate(BaseModel):
    company: str
    position: str
    status: str = "saved"
    job_url: Optional[str] = None
    location: Optional[str] = None
    notes: Optional[str] = None

class JobApplication(JobApplicationCreate):
    id: int

applications: List[JobApplication] = []
next_id = 1

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Job Applicatoion Tracker API",
        "docs": "/docs"
    }

@app.post("/applications", response_model=JobApplication)
def create_application(application: JobApplicationCreate):
    global next_id

    new_application = JobApplication(
        id=next_id,
        **application.model_dump()
    )

    applications.append(new_application)
    next_id += 1

    return new_application

@app.get("/applications", response_model=List[JobApplication])
def get_applications():
    return applications

@app.get("/applications/{application_id}", response_model=JobApplication)
def get_application(application_id: int):
    for application in applications:
        if application.id == application_id:
            return application
    
    return HTTPException(status_code=404, detail="Application not found")

@app.delete("/applications/{application_id}")
def delete_application(application_id: int):
    for application in applications:
        if application.id == application_id:
            applications.remove(application)
            return {"message": "Application deleted successfully"}
    
    raise HTTPException(status_code=404, detail="Application not found")