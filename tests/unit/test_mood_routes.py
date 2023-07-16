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


@pytest.mark.unit
@pytest.mark.moods
def test_moods_post_create(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (POST)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing
    data = {"description": "sad"}
    response = testclient.post('/moods/create', json=data)
    dict_data = json.loads(response.text)
    assert response.status_code == 200
    assert str(dict_data["mood_id"]) == "1"


@pytest.mark.unit
@pytest.mark.moods
def test_moods_post_create_404(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (POST) without having the correct data
    THEN check that the response is 400
    """

    # Create a test client using the Flask application configured for testing
    data = {"bad_key": "sad"}
    response = testclient.post('/moods/create', json=data)
    assert 'text/html' in response.content_type
    assert response.status_code == 404


