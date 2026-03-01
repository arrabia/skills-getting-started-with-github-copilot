from urllib.parse import quote


def test_unregister_removes_registered_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    target_path = f"/activities/{quote(activity_name, safe='')}/unregister?email={email}"

    # Act
    response = client.delete(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Unregistered {email} from {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email not in participants


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "newstudent@mergington.edu"
    target_path = f"/activities/{quote(activity_name, safe='')}/unregister?email={email}"

    # Act
    response = client.delete(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_unregister_returns_404_for_student_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"
    target_path = f"/activities/{quote(activity_name, safe='')}/unregister?email={email}"

    # Act
    response = client.delete(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Student is not registered for this activity"


def test_unregister_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Chess Club"
    target_path = f"/activities/{quote(activity_name, safe='')}/unregister"

    # Act
    response = client.delete(target_path)

    # Assert
    assert response.status_code == 422
