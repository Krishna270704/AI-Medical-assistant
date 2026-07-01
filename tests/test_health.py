import pytest
from app import create_app
from app.core.config import TestingConfig

@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_live_endpoint(client):
    response = client.get('/live')
    assert response.status_code == 200
    assert response.json['status'] == 'alive'

def test_ready_endpoint(client):
    # App context is needed for DB interaction in /ready
    response = client.get('/ready')
    # During tests, the in-memory DB will be immediately ready
    assert response.status_code == 200
    assert response.json['status'] == 'ready'
