from urllib.parse import quote


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    target_path = f"/activities/{quote(activity_name, safe='')}/signup?email={email}"

    # Act
    response = client.post(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert payload["message"] == f"Signed up {email} for {activity_name}"

    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    assert email in participants


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "newstudent@mergington.edu"
    target_path = f"/activities/{quote(activity_name, safe='')}/signup?email={email}"

    # Act
    response = client.post(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 404
    assert payload["detail"] == "Activity not found"


def test_signup_returns_400_for_already_registered_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    target_path = f"/activities/{quote(activity_name, safe='')}/signup?email={email}"

    # Act
    response = client.post(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 400
    assert payload["detail"] == "Student already signed up for this activity"


def test_signup_returns_422_when_email_is_missing(client):
    # Arrange
    activity_name = "Chess Club"
    target_path = f"/activities/{quote(activity_name, safe='')}/signup"

    # Act
    response = client.post(target_path)

    # Assert
    assert response.status_code == 422
