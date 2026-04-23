import pytest
from fastapi.testclient import TestClient
from src.main import app
import random

client = TestClient(app)

# 1. Successful student signup and login [cite: 68]
def test_signup_and_login():
    email = f"teststudent{random.randint(1,10000)}@example.com"
    
    # Signup
    signup_response = client.post("/auth/signup", json={
        "name": "Test Student",
        "email": email,
        "password": "password123",
        "role": "student"
    })
    assert signup_response.status_code == 201
    assert "access_token" in signup_response.json()

    # Login
    login_response = client.post("/auth/login", json={
        "email": email,
        "password": "password123"
    })
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

# 2. Trainer creating a session [cite: 69]
def test_trainer_create_session():
    # You must implement the /sessions POST endpoint in main.py for this to pass
    pass 

# 3. Student marking attendance [cite: 70]
def test_student_mark_attendance():
    # You must implement the /attendance/mark POST endpoint in main.py for this to pass
    pass

# 4. POST to /monitoring/attendance returning 405 [cite: 71]
def test_monitoring_attendance_405():
    response = client.post("/monitoring/attendance")
    assert response.status_code == 405

# 5. Protected endpoint with no token returning 401 [cite: 72]
def test_protected_endpoint_no_token():
    response = client.get("/monitoring/attendance")
    assert response.status_code == 401