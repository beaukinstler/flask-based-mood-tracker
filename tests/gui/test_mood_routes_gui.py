import pytest
from flask import Flask
from src.models import db, Mood
import json
import requests
from flask import url_for


@pytest.mark.unit
@pytest.mark.moods
def test_moods_get_page(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods/all' page is requested (GET)
    THEN check that the response is valid
    """
    with testclient_authenticated as test_client:
        mood = Mood("temp")
        db.session.add(mood)
        db.session.commit()
        mood2 = Mood("temp2")
        db.session.add(mood2)
        db.session.commit()

        gui = testclient_authenticated.get(url_for('moods.all'), follow_redirects=True)
        assert gui.status_code == 200


@pytest.mark.unit
@pytest.mark.moods
def test_moods_post_create(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (POST)
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
def test_moods_post_create_404(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (POST) without having the correct data
    THEN check that the response is 400
    """

    # Create a test client using the Flask application configured for testing
    data = {"bad_key": "sad"}
    response = testclient_authenticated.post('/api.v1/moods/create', json=data)
    assert 'text/html' in response.content_type
    assert response.status_code == 400


@pytest.mark.unit
@pytest.mark.moods
def test_moods_delete(testclient_authenticated):
    """
    GIVEN a Flask application authenticated and a Mood in the database
    WHEN the '/moods/1' page is requested (DELTE)
    THEN the mood is no longer in the database
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.delete('/moods/1')

    assert response.status_code == 200
    assert "temp" in response.json.values()
    assert "DELETE via HTTP" in response.json.values()


@pytest.mark.unit
@pytest.mark.moods
def test_moods_patch_or_put(testclient_authenticated):
    """
    GIVEN a Flask application authenticated and a Mood in the database
    WHEN the '/moods/1' page is requested (patch or put) with good data to update
    THEN the response shows the new data with the existing id
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.patch('/moods/1',json={"description":"happy"})

    assert response.status_code == 200
    assert "happy" == response.json['mood_description']
    assert "1" == response.json['mood_id']

    response = testclient_authenticated.put('/moods/1',json={"description":"silly"})

    assert response.status_code == 200
    assert "silly" == response.json['mood_description']
    assert "1" == response.json['mood_id']

@pytest.mark.unit
@pytest.mark.moods
def test_moods_patch_or_put_bad_key(testclient_authenticated):
    """
    GIVEN a Flask application authenticated and a Mood in the database
    WHEN the '/moods/1' page is requested (patch or put) with bad key
    THEN the response is a 400
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.patch('/moods/1',json={"mood":"happy"})

    assert response.status_code == 400

    response = testclient_authenticated.put('/moods/1',json={"mood":"happy"})

    assert response.status_code == 400

@pytest.mark.unit
@pytest.mark.moods
def test_moods_patch_or_put_bad_key(testclient_authenticated):
    """
    GIVEN a mood logged to a user
    WHEN the current time is less than the configured limit
    THEN the data is not logged and there is a 400
    """
    m = Mood("temp")
    db.session.add(m)
    db.session.commit()

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.patch('/moods/1',json={"mood":"happy"})

    assert response.status_code == 400

    response = testclient_authenticated.put('/moods/1',json={"mood":"happy"})

    assert response.status_code == 400



@pytest.mark.unit
@pytest.mark.moods
def test_mood_button(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/mood' page is requested (GET)
    THEN There should be a happy and sad button
    """

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.get('/moods')
    assert 'text/html' in response.content_type
    assert 'button' in response.text
    assert 'sad' in response.text
    assert 'happy' in response.text
    assert response.status_code == 200

@pytest.mark.moods
def test_moods_types_list(testclient_authenticated):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods/all' page is requested (GET)
    THEN There should be colors in the td and tr elements
    """

    # Create a test client using the Flask application configured for testing

    response = testclient_authenticated.get('/moods')
    response = testclient_authenticated.get('/moods/all')
    assert 'text/html' in response.content_type
    assert 'table-primary' in response.text
    assert 'table-warning' in response.text