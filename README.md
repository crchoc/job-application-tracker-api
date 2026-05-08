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
- Simple Streamlit frontend dashboard
- Add, view, filter, search, update, and delete applications from the UI

---

## Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Pydantic
- pytest
- Git / GitHub
- Docker
- Docker Compose
- Streamlit
- pandas
- requests

---

## Project Structure

```text
job-application-tracker-api/
├── app/
├── frontend/
│   └── streamlit_app.py
├── tests/
├── screenshots/
├── Dockerfile
├── docker-compose.yml
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
git clone https://github.com/crchoc/job-application-tracker-api.git
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

## How to Run with Docker

Build and start both the FastAPI backend and Streamlit frontend:

```bash
docker compose up --build
```

Open the FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

Open the Streamlit frontend:

```text
http://127.0.0.1:8501
```

Stop the containers:

```bash
docker compose down
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

## Frontend Dashboard

This project includes a simple Streamlit frontend for interacting with the FastAPI backend.

Run the backend first:

```bash
fastapi dev app/main.py
```

Then open a second terminal and run:

```bash
streamlit run frontend/streamlit_app.py
```

Open the Streamlit dashboard:

```text
http://localhost:8501
```

---

## Screenshots

### Interactive API Documentation

![API Documentation](screenshots/api-docs.PNG)

### Example Application Endpoint

![Applications Endpoint](screenshots/applications-endpoint.PNG)

### Streamlit Dashboard

![Streamlit Dashboard](screenshots/streamlit-dashboard.png)

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
- Creating docker container
- Creating a simple frontend dashboard with Streamlit

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
| 0.7.0 | Docker and Docker Compose support |
| 0.8.0 | Streamlit frontend dashboard |

---

## About This Project

This project was created as a beginner-friendly but practical backend portfolio project. It focuses on clean API design, database integration, testing, and clear documentation.