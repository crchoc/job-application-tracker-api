# Job Application Tracker API

A FastAPI backend project for tracking job applications, managing application statuses, and searching/filtering saved job records.

This project was built as a practical Python backend portfolio project. It demonstrates REST API development, SQLite database integration, modular project structure, CRUD operations, search/filter/sort functionality, and automated API testing.

---

## Features

- Create, read, update, and delete job applications
- Store job applications in a SQLite database
- Filter applications by status, company, and location
- Search applications by keyword
- Sort applications by ID, company, position, status, or location
- Use pagination with `skip` and `limit`
- View total application count
- View application status summary
- Interactive API documentation with FastAPI Swagger UI
- Automated API tests with pytest
- Modular backend structure using routers, schemas, CRUD logic, and database models

---

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Git / GitHub

---

## Project Structure

```text
job-application-tracker-api/
├── app/
│   ├── __init__.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       └── applications.py
├── tests/
│   ├── __init__.py
│   └── test_applications.py
├── README.md
├── requirements.txt
└── .gitignore
```

---

## API Overview

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Root endpoint |
| `POST` | `/applications` | Create a new job application |
| `GET` | `/applications` | Get all job applications |
| `GET` | `/applications/{application_id}` | Get one application by ID |
| `PATCH` | `/applications/{application_id}` | Update an application |
| `DELETE` | `/applications/{application_id}` | Delete an application |
| `GET` | `/applications/count` | Get total number of applications |
| `GET` | `/applications/summary` | Get status summary |

---

## Example Application Data

```json
{
  "company": "Naver",
  "position": "Junior Python Developer",
  "status": "applied",
  "job_url": "https://example.com/job",
  "location": "Seoul",
  "notes": "Python, SQL, backend role"
}
```

---

## Query Examples

Get all applications:

```http
GET /applications
```

Filter by status:

```http
GET /applications?status=applied
```

Filter by company:

```http
GET /applications?company=naver
```

Search by keyword:

```http
GET /applications?search=python
```

Sort by company:

```http
GET /applications?sort_by=company&sort_order=asc
```

Use pagination:

```http
GET /applications?skip=0&limit=10
```

Get total count:

```http
GET /applications/count
```

Get status summary:

```http
GET /applications/summary
```

---

## Status Types

The application status can be one of the following:

```text
saved
applied
interview
rejected
offer
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/job-application-tracker-api.git
cd job-application-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```bash
.venv\Scripts\activate.bat
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the API

```bash
fastapi dev app/main.py
```

### 6. Open the API documentation

Open this URL in your browser:

```text
http://127.0.0.1:8000/docs
```

---

## Running Tests

This project uses pytest and FastAPI TestClient for API testing.

Run tests:

```bash
python -m pytest
```

Expected result:

```text
11 passed
```

The tests use a separate SQLite database file for testing.

---

## Screenshots

### Interactive API Documentation

```markdown
![API Documentation](screenshots/api-docs.PNG)
```

### Example Application Endpoint

```markdown
![Applications Endpoint](screenshots/applications-endpoint.PNG)
```

---

## What I Learned

Through this project, I practiced:

- Building REST APIs with FastAPI
- Structuring a Python backend project
- Creating database models with SQLAlchemy
- Using SQLite for persistent local storage
- Separating schemas, models, routes, and CRUD logic
- Implementing search, filtering, sorting, and pagination
- Writing automated API tests with pytest
- Managing a project with Git and GitHub

---

## Future Improvements

- Add Docker support
- Add user authentication
- Add a simple frontend dashboard
- Add deployment configuration
- Add date fields such as application deadline and interview date
- Add CSV export for saved applications

---

## Version History

| Version | Description |
|---|---|
| 0.1.0 | Basic FastAPI prototype |
| 0.2.0 | Modular project structure |
| 0.3.0 | SQLite database with SQLAlchemy |
| 0.4.0 | Search, filtering, sorting, pagination, count, and summary |
| 0.5.0 | Automated API tests with pytest |
| 0.6.0 | Professional README and GitHub presentation |

---

## About This Project

This project was created as a beginner-friendly but practical backend portfolio project. It focuses on clean API design, database integration, testing, and clear documentation.