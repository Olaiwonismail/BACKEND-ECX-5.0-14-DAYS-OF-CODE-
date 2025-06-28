# tests/test_jobs.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_job(auth_token):
    job_data = {
        "title": "Software Engineer",
        "description": "Backend development",
        "location": "Remote",
        "salary": 120000,
        "company": "TechCorp",
        "job_type": "full-time"
    }
    response = client.post(
        "/employer/jobs/",
        json=job_data,
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == job_data["title"]