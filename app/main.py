from fastapi import FastAPI

from app.database import Base, engine
from app.routers import applications


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Job Application Tracker API",
    description="A simple API for tracking job applications.",
    version="0.3.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Job Application Tracker API",
        "docs": "/docs",
        "version": "0.3.0"
    }


app.include_router(applications.router)