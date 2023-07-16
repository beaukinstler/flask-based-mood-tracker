import pytest

@pytest.mark.focus
def test_fixture_testclient(testclient):
    response = testclient.get()
    assert response is not None

@pytest.mark.focus
def test_fixture_testclient_authenticated(testclient_authenticated):

    response = testclient_authenticated.get()
    assert response is not None
