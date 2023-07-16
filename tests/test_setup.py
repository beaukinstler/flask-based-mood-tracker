import pytest

@pytest.mark.focus
def test_fixture_setup(app, testclient, testclient_authenticated):
    print(app)
    print(testclient)
    print(testclient_authenticated)
    assert True


