import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No special setup needed)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_duplicate():
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Act
    response_signup = client.post(f"/activities/{activity}/signup?email={email}")
    response_duplicate = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response_signup.status_code == 200
    assert response_duplicate.status_code == 400
    assert "already signed up" in response_duplicate.json()["detail"]

def test_unregister():
    # Arrange
    email = "testuser2@mergington.edu"
    activity = "Programming Class"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response_unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    response_unreg_again = client.delete(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response_unreg.status_code == 200
    assert response_unreg_again.status_code == 400
    assert "not registered" in response_unreg_again.json()["detail"].lower()

def test_signup_nonexistent_activity():
    # Arrange
    # Act
    response = client.post("/activities/Nonexistent/signup?email=foo@bar.com")
    # Assert
    assert response.status_code == 404

def test_unregister_nonexistent_activity():
    # Arrange
    # Act
    response = client.delete("/activities/Nonexistent/unregister?email=foo@bar.com")
    # Assert
    assert response.status_code == 404
