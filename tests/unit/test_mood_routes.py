import pytest
from flask import Flask
from src.models import db, Mood





@pytest.mark.skip
def test_hotest_moods_get_page(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """


    # Create a test client using the Flask application configured for testing
    with testclient() as test_client:
        response = test_client.get('/moods')
        assert response.status_code == 200

