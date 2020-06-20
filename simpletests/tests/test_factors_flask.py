import pytest
from flask_api import status

from factors_flask import APP

@pytest.fixture
def client(app):
    """Get a test client for your Flask app"""
    return app.test_client()

@pytest.fixture
def app():
    """Yield your app with its context set up and ready"""

    with APP.app_context():
        yield APP

class TestRoot:
    def test_root_page(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b'Hello from Factoring Server.' in response.data

class TestUnsupportedPaths:
    def test_unsupported_paths(self, client):
        response = client.get("/-2")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b'Factoring of "-2" is not supported' in response.data
        response = client.get("/hello")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b'Factoring of "hello" is not supported' in response.data
        response = client.get("/12.667")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert b'Factoring of "12.667" is not supported' in response.data

class TestFactorsof6:
    def test_factor_page_6(self, client):
        response = client.get("/6")
        assert response.status_code == 200
        assert b'Factors of 6 are 1, 2, 3, 6.' in response.data

class TestFactorsof0:
    def test_factor_page_0(self, client):
        response = client.get("/0")
        assert response.status_code == 200
        assert b'Any positive integer is a factor of 0.' in response.data
