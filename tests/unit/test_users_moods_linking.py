import pytest
from flask import Flask
from src.models import db, User, Mood, UserMoodLog
from time import sleep
from flask_login import current_user


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
    user_email2 = 'user2@example.com'
    user2 = User(email=user_email2, password=user_password)
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()
    # Log association
    user_mood = UserMoodLog(note='test')

    user_mood.mood = Mood('happy')
    user.moods.append(user_mood)

    db.session.commit()
    user2.moods.append(user_mood)
    db.session.commit()

    query = db.session.query(UserMoodLog)
    associations = query.all()

    assert associations[0].user == user2
    assert user.moods == []
    assert user2.moods[0].mood.description == 'happy'
    assert 'happy' in str(user2.serialize())

    moods = db.session.query(Mood).all()
    assert len(moods) == 1




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
    user_mood = UserMoodLog(note='test 1')
    mood1 = Mood('happy')
    db.session.add(mood1)
    user_mood.mood = mood1

    sleep(4)
    user_mood2 = UserMoodLog(note='test 2')
    mood2 = Mood('sad')
    db.session.add(mood2)
    user_mood2.mood = mood2
    user.moods.append(user_mood2)
    user.moods.append(user_mood)
    db.session.commit()

    query = db.session.query(UserMoodLog)
    associations = query.all()

    assert associations[0].user == user
    with pytest.raises(AssertionError) as execinfo:
        assert user.moods == []
    moods = user.get_moods()
    assert moods[0] != moods[1]
    assert moods[0]['date'] <  moods[1]['date']
    assert 'happy' in str(user.moods[0])
    assert 'sad' in str(user.moods[1])

    moods = db.session.query(Mood).all()
    assert len(moods) == 2



@pytest.mark.unit
@pytest.mark.users
def test_new_mood_too_soon(testclient_authenticated):
    """
    GIVEN a mood logged to a user
    WHEN the current time is less than the configured limit
    THEN the data is not logged and there is a 400 response
    """
    user = current_user
    happy = Mood("happy")
    sad = Mood("sad")
    db.session.add(happy)
    db.session.add(sad)
    db.session.commit()

    user_mood = UserMoodLog()
    user_mood.mood = happy
    user.moods.append(user_mood)
    db.session.commit()
    assert user.moods[0].mood.description == 'happy'

    user_mood = None
    user_mood = UserMoodLog()
    user_mood.mood = happy

    



    assert response.status_code == 400
