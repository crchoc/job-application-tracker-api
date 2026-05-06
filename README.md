# Job Application Tracker API

A beginner-friendly FastAPI project for tracking job applications.

## Features

- Create a job application
- View all job applications
- View one job application by ID
- Update application status
- Delete a job application
- Interactive API documentation with FastAPI
- Filter applications by status, company, and location
- Search applications by keyword
- Sort applications by ID, company, position, status, or location
- Use pagination with skip and limit
- View application count and status summary

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLite
- SQLAlchemy

## How to Run

1. Close the repository

```bash

git clone https://github.com/crchoc/job-application-tracker-api.git
cd job-application-tracker-api
```

2. Create a virtual environment

```bash
python -m venv .venv
```

3. Active the virtual environment

```bash
.venv\Scripts\Active.ps1
```

4. Install dependencies

```bash
pip install -r requirements.txt
```

5. Run the API

```bash
fastapi dev app/main.py
```

6. Open the API docs

```bash
http://127.0.0.1:8000/docs
```

## Project Structure

```text
job-application-tracker-api/
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       └── applications.py
├── README.md
├── requirements.txt
└── .gitignore
```

## Database

This project uses SQLite for local development.  
The database file is created automatically when the app starts.

Local database files are ignored by Git using `.gitignore`.

## Example API Queries

Get all applications:

```bash
GET /applications
```

Filter by status:
```bash
GET /applications?status=applied
```

Search by keyword:
```bash
GET /applications?search=python
```

Sort by company:
```bash
GET /applications?sort_by=company&sort_order=asc
```

Use pagination:
```bash
GET /applications?skip=0&limit=10
```
Get total count:
```bash
GET /applications/count
```
Get status summary:
```bash
GET /applications/summary
```

Current version: 0.4.0

