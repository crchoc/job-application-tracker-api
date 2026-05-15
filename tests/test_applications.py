import os

os.environ["DATABASE_URL"] = "sqlite:///./test_job_tracker.db"

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


def register_user(
    email="test@example.com",
    full_name="Test User",
    password="password123"
):
    return client.post(
        "/auth/register",
        json={
            "email": email,
            "full_name": full_name,
            "password": password
        }
    )


def login_user(
    email="test@example.com",
    password="password123"
):
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )


def get_auth_headers(
    email="test@example.com",
    full_name="Test User",
    password="password123"
):
    register_user(
        email=email,
        full_name=full_name,
        password=password
    )

    login_response = login_user(
        email=email,
        password=password
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_sample_application(
    headers,
    company="Naver",
    position="Junior Python Developer",
    status="applied",
    location="Seoul",
    notes="Python, SQL, backend role"
):
    return client.post(
        "/applications",
        headers=headers,
        json={
            "company": company,
            "position": position,
            "status": status,
            "job_url": "https://example.com/job",
            "location": location,
            "notes": notes
        }
    )


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["version"] == "1.0.0"


def test_register_user():
    response = register_user()

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_email():
    register_user()

    response = register_user()

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_user():
    register_user()

    response = login_user()

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password():
    register_user()

    response = login_user(password="wrongpassword")

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


def test_get_current_user():
    headers = get_auth_headers()

    response = client.get(
        "/auth/me",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"


def test_applications_require_authentication():
    response = client.get("/applications")

    assert response.status_code == 401


def test_create_application():
    headers = get_auth_headers()

    response = create_sample_application(headers=headers)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["company"] == "Naver"
    assert data["position"] == "Junior Python Developer"
    assert data["status"] == "applied"
    assert data["user_id"] == 1


def test_get_all_applications():
    headers = get_auth_headers()

    create_sample_application(headers=headers, company="Naver")
    create_sample_application(
        headers=headers,
        company="Kakao",
        status="saved"
    )

    response = client.get(
        "/applications",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["company"] == "Naver"
    assert data[1]["company"] == "Kakao"


def test_get_application_by_id():
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="Coupang"
    )

    response = client.get(
        "/applications/1",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["company"] == "Coupang"


def test_get_application_not_found():
    headers = get_auth_headers()

    response = client.get(
        "/applications/999",
        headers=headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_update_application():
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="LINE",
        status="applied"
    )

    response = client.patch(
        "/applications/1",
        headers=headers,
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
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="Kakao"
    )

    delete_response = client.delete(
        "/applications/1",
        headers=headers
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == (
        "Application deleted successfully"
    )

    get_response = client.get(
        "/applications/1",
        headers=headers
    )

    assert get_response.status_code == 404


def test_filter_applications_by_status():
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="Naver",
        status="applied"
    )
    create_sample_application(
        headers=headers,
        company="Kakao",
        status="saved"
    )
    create_sample_application(
        headers=headers,
        company="LINE",
        status="applied"
    )

    response = client.get(
        "/applications?status=applied",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert all(
        application["status"] == "applied"
        for application in data
    )


def test_search_applications_by_keyword():
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="Naver",
        position="Junior Python Developer",
        notes="Python, SQL, backend role"
    )
    create_sample_application(
        headers=headers,
        company="Kakao",
        position="Backend Developer",
        notes="FastAPI and database"
    )
    create_sample_application(
        headers=headers,
        company="Coupang",
        position="Data Analyst",
        notes="pandas and SQL"
    )

    response = client.get(
        "/applications?search=python",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["company"] == "Naver"


def test_count_applications():
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="Naver",
        status="applied"
    )
    create_sample_application(
        headers=headers,
        company="Kakao",
        status="saved"
    )

    response = client.get(
        "/applications/count",
        headers=headers
    )

    assert response.status_code == 200
    assert response.json()["count"] == 2


def test_summary_applications():
    headers = get_auth_headers()

    create_sample_application(
        headers=headers,
        company="Naver",
        status="applied"
    )
    create_sample_application(
        headers=headers,
        company="Kakao",
        status="saved"
    )
    create_sample_application(
        headers=headers,
        company="LINE",
        status="interview"
    )

    response = client.get(
        "/applications/summary",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 3
    assert data["applied"] == 1
    assert data["saved"] == 1
    assert data["interview"] == 1
    assert data["rejected"] == 0
    assert data["offer"] == 0


def test_users_can_only_access_their_own_applications():
    first_user_headers = get_auth_headers(
        email="first@example.com",
        full_name="First User",
        password="password123"
    )

    second_user_headers = get_auth_headers(
        email="second@example.com",
        full_name="Second User",
        password="password123"
    )

    create_sample_application(
        headers=first_user_headers,
        company="Naver"
    )

    response = client.get(
        "/applications/1",
        headers=second_user_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"