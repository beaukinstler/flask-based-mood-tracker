import pytest
from flask import Flask

import json



@pytest.mark.unit
def test_get_index(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/moods' page is requested (GET)
    THEN check that the response is valid
    """

    # Create a test client using the Flask application configured for testing

    response = testclient.get('/index')
    assert response.status_code == 200

    response = testclient.get('/')
    assert response.status_code == 200



@pytest.mark.unit
def test_get_index_not_auth_redirect(testclient):
    """
    GIVEN a Flask application configured for testing via a fixture
    WHEN the '/login' page is requested (GET)
    THEN check a redirect is returned
    """

    response = testclient.get('/login')
    assert response.status_code in range(300, 399)
