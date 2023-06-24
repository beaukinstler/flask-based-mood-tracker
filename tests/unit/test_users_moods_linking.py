import pytest
from flask import Flask
from src.models import db, User, Mood, UserMoodLog


@pytest.mark.users
@pytest.mark.unit
def test_user_mood_log(testclient):
    """
    GIVEN a Flask application configured for in this test file for testing via a fixture
    WHEN creating a User, Mood, and UserMoodLog, linking them together
    THEN the User.moods will hold the new mood and the Mood().users will hold the the user
    """

    # Example: Insert a user into the database
    user_email = 'user@example.com'
    user_password = 'password'
    user = User(email=user_email, password=user_password)
    db.session.add(user)
    db.session.commit()
    # Log association
    user_mood = UserMoodLog(note='test')

    user_mood.mood = Mood('happy')
    user.moods.append(user_mood)
    db.session.commit()

    for user_mood in user.moods:
        print(user_mood.note)
        print(user_mood.created_at)
        print(user_mood.mood)

    query = db.session.query(UserMoodLog)
    associations = query.all()
    for a in sorted(associations):
        print(a)

    assert associations[0].user == user
    assert user.moods[0].mood.description == 'happy'

    moods = db.session.query(Mood).all()
    assert moods[0].users[0].user == user
