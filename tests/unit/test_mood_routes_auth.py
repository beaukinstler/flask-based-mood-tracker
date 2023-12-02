import pytest
from flask import Flask
from src.models import db, Mood
import json
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


# api tests authenticated

@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_get_page(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.get('/api.v1/moods')

    assert response.status_code == 200

# api tests



@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_get_list_of_moods(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    m = Mood('happy')
    db.session.add(m)
    db.session.commit()
    response = testclient_authenticated.get('/api.v1/moods')
    moods = response.json
    assert len(moods) > 0
    assert 'happy' in moods[0].values()


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_post_create(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/api.v1/moods' page is requested (POST)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    data = {"description": "sad"}
    response = testclient_authenticated.post('/api.v1/moods/create', json=data)
    dict_data = json.loads(response.text)
    assert response.status_code == 200
    assert str(dict_data["mood_id"]) == "1"


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_post_create_duplicate(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/api.v1/moods' page is requested (POST)
    THEN check that the response is valid
    """
    m = Mood('happy')
    db.session.add(m)
    db.session.commit()
    # Create a test client using the Flask application configured for testing
    data = {"description": "happy"}
    response = testclient_authenticated.post('/api.v1/moods/create', json=data)

    moods = db.session.execute(select(Mood).where(
        Mood.description == 'happy')).all()

    assert len(moods) == 1
    assert response.status_code == 409


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_post_create_404(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/api.v1/moods' page is requested (POST) without having the correct data
    THEN check that the response is 400
    """

    # Create a test client using the Flask application configured for testing
    data = {"bad_key": "sad"}
    response = testclient_authenticated.post('/api.v1/moods/create', json=data)
    assert 'text/html' in response.content_type
    assert response.status_code == 400


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_delete(testclient_authenticated):
    """
    GIVEN a Flask application authenticated and a Mood in the database
    WHEN the '/moods/1' page is requested (DELTE)
    THEN the mood is no longer in the database
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.delete('/api.v1/moods/1')

    assert response.status_code == 200
    assert "temp" in response.json.values()
    assert "DELETE via HTTP" in response.json.values()


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_patch_or_put(testclient_authenticated):
    """
    GIVEN a Flask application authenticated and a Mood in the database
    WHEN the '/moods/1' page is requested (patch or put) with good data to update
    THEN the response shows the new data with the existing id
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.patch(
        '/api.v1/moods/1', json={"description": "happy"})

    assert response.status_code == 200
    assert "happy" == response.json['mood_description']
    assert "1" == response.json['mood_id']

    response = testclient_authenticated.put(
        '/api.v1/moods/1', json={"description": "silly"})

    assert response.status_code == 200
    assert "silly" == response.json['mood_description']
    assert "1" == response.json['mood_id']


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_patch_or_put_bad_key(testclient_authenticated):
    """
    GIVEN a Flask application authenticated and a Mood in the database
    WHEN the '/moods/1' page is requested (patch or put) with bad key
    THEN the response is a 400
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.patch(
        '/api.v1/moods/1', json={"mood": "happy"})

    assert response.status_code == 400

    response = testclient_authenticated.put(
        '/api.v1/moods/1', json={"mood": "happy"})

    assert response.status_code == 400
