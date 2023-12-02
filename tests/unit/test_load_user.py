import pytest
from src.models import User, load_user

from src import db

@pytest.mark.auth
def test_load_user_found(testclient_authenticated):
    # Create a mock user object to return when a user is found in the database

    user_id = "user@example.com"
    result = load_user(user_id)
    assert result is None

    user = User(email=user_id, password="password")
    db.session.add(user)
    db.session.commit()

    result = load_user(user_id)
    assert result is not None
    assert result.email == user_id




    # Assert that the load_user function returns the expected result when a user is found
