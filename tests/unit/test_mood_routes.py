import pytest
from flask import Flask
from src.models import db, Mood
import json


@pytest.mark.unit
@pytest.mark.moods
def test_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient.get('/moods')
    assert response.status_code == 200


def test_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient.get('/moods/all')
    assert response.status_code == 302


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
    response = testclient_authenticated.post('/moods/create', json=data)
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
    response = testclient_authenticated.post('/moods/create', json=data)
    assert 'text/html' in response.content_type
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




### api tests
@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient.get('/api.v1/moods')
    assert response.status_code == 200


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_post_create(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/api.v1/moods' page is requested (POST)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    data = {"description": "sad"}
    response = testclient.post('/api.v1/moods/create', json=data)
    dict_data = json.loads(response.text)
    assert response.status_code == 200
    assert str(dict_data["mood_id"]) == "1"


@pytest.mark.unit
@pytest.mark.moods
def test_api_moods_post_create_404(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/api.v1/moods' page is requested (POST) without having the correct data
    THEN check that the response is 400
    """

    # Create a test client using the Flask application configured for testing
    data = {"bad_key": "sad"}
    response = testclient.post('/api.v1/moods/create', json=data)
    assert 'text/html' in response.content_type
    assert response.status_code == 400