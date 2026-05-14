import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


TEST_DATABASE_URL = "sqlite:///./test_job_tracker.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_test_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


def create_sample_application(
    company="Naver",
    position="Junior Python Developer",
    status="applied",
    location="Seoul",
    notes="Python, SQL, backend role"
):
    response = client.post(
        "/applications",
        json={
            "company": company,
            "position": position,
            "status": status,
            "job_url": "https://example.com/job",
            "location": location,
            "notes": notes
        }
    )

    return response


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["version"] == "0.9.0"


def test_create_application():
    response = create_sample_application()

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["company"] == "Naver"
    assert data["position"] == "Junior Python Developer"
    assert data["status"] == "applied"


def test_get_all_applications():
    create_sample_application(company="Naver")
    create_sample_application(company="Kakao", status="saved")

    response = client.get("/applications")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["company"] == "Naver"
    assert data[1]["company"] == "Kakao"


def test_get_application_by_id():
    create_sample_application(company="Coupang")

    response = client.get("/applications/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["company"] == "Coupang"


def test_get_application_not_found():
    response = client.get("/applications/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_update_application():
    create_sample_application(company="LINE", status="applied")

    response = client.patch(
        "/applications/1",
        json={
            "status": "interview",
            "notes": "First interview scheduled"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "interview"
    assert data["notes"] == "First interview scheduled"


def test_delete_application():
    create_sample_application(company="Kakao")

    delete_response = client.delete("/applications/1")

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Application deleted successfully"

    get_response = client.get("/applications/1")

    assert get_response.status_code == 404


def test_filter_applications_by_status():
    create_sample_application(company="Naver", status="applied")
    create_sample_application(company="Kakao", status="saved")
    create_sample_application(company="LINE", status="applied")

    response = client.get("/applications?status=applied")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(application["status"] == "applied" for application in data)


def test_search_applications_by_keyword():
    create_sample_application(
        company="Naver",
        position="Junior Python Developer",
        notes="Python, SQL, backend role"
    )
    create_sample_application(
        company="Kakao",
        position="Backend Developer",
        notes="FastAPI and database"
    )
    create_sample_application(
        company="Coupang",
        position="Data Analyst",
        notes="pandas and SQL"
    )

    response = client.get("/applications?search=python")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Naver"


def test_count_applications():
    create_sample_application(company="Naver", status="applied")
    create_sample_application(company="Kakao", status="saved")

    response = client.get("/applications/count")

    assert response.status_code == 200
    assert response.json()["count"] == 2


def test_summary_applications():
    create_sample_application(company="Naver", status="applied")
    create_sample_application(company="Kakao", status="saved")
    create_sample_application(company="LINE", status="interview")

    response = client.get("/applications/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["applied"] == 1
    assert data["saved"] == 1
    assert data["interview"] == 1
    assert data["rejected"] == 0
    assert data["offer"] == 0