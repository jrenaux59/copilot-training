from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_the_email_from_activity():
    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert response.status_code == 200

    remove_response = client.delete("/activities/Chess Club/signup?email=teststudent@mergington.edu")
    assert remove_response.status_code == 200

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert "teststudent@mergington.edu" not in activity["participants"]


def test_unregister_returns_error_for_unknown_participant():
    response = client.delete("/activities/Chess Club/signup?email=unknown@mergington.edu")
    assert response.status_code == 400
