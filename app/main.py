from fastapi import FastAPI

from app.database import Base, engine
from app.routers import applications, auth


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Job Application Tracker API",
    description="A FastAPI backend for tracking job applications with PostgreSQL and JWT authentication.",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Job Application Tracker API",
        "docs": "/docs",
        "version": "1.0.0"
    }


app.include_router(auth.router)
app.include_router(applications.router)