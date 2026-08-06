def test_get_activities_returns_the_activity_catalog(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert payload["Chess Club"]["participants"]


def test_signup_adds_a_participant_to_an_activity(client):
    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")

    assert response.status_code == 200
    payload = response.json()
    assert payload["message"] == "Signed up teststudent@mergington.edu for Chess Club"

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert "teststudent@mergington.edu" in activity["participants"]


def test_signup_rejects_a_duplicate_participant(client):
    client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")

    response = client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_unregister_participant_removes_the_email_from_activity(client):
    client.post("/activities/Chess Club/signup?email=teststudent@mergington.edu")

    remove_response = client.delete("/activities/Chess Club/signup?email=teststudent@mergington.edu")

    assert remove_response.status_code == 200
    assert remove_response.json()["message"] == "Removed teststudent@mergington.edu from Chess Club"

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert "teststudent@mergington.edu" not in activity["participants"]


def test_unregister_returns_error_for_unknown_participant(client):
    response = client.delete("/activities/Chess Club/signup?email=unknown@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
