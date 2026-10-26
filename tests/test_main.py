from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_resource_success():
    """Test creating a resource successfully"""
    response = client.post(
        "/create_resource",
        json={
            "name": "Conference Room A",
            "type": "meeting_room"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Conference Room A"
    assert data["type"] == "meeting_room"
    assert data["status"] == "available"
    assert "resource_id" in data

def test_create_reservation_success():
    """Test creating a reservation successfully"""
    # Create resource first
    create_response = client.post(
        "/create_resource",
        json={"name": "Meeting Room", "type": "meeting_room"}
    )
    resource_id = create_response.json()["resource_id"]
    
    # Create reservation
    response = client.post(
        "/create-reservation",
        json={
            "resource_id": resource_id,
            "user_id": "emp-123",
            "start_time": "09:00",
            "end_time": "10:00"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["resource_id"] == resource_id
    assert data["user_id"] == "emp-123"
    assert data["start_time"] == "09:00"
    assert data["end_time"] == "10:00"
    assert data["status"] == "active"
    assert "reservation_id" in data