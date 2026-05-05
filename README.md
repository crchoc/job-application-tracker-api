# Job Application Tracker API

A beginner-friendly FastAPI project for tracking job applications.

## Features

- Create a job application
- View all job applications
- View one job application by ID
- Update application status
- Delete a job application
- Interactive API documentation with FastAPI

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