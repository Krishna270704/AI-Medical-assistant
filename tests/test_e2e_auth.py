import pytest
from app import create_app
from app.core.config import TestingConfig
from app.models import db, User

@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_landing_page(client):
    """Test that unauthenticated root route returns the landing page."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Your Personal AI Medical Advisor" in response.data

def test_protected_dashboard(client):
    """Test that dashboard requires login and redirects."""
    response = client.get('/dashboard')
    # Should redirect to login or 401
    assert response.status_code in [302, 401]

def test_user_creation(app):
    """Test user model and password hashing."""
    with app.app_context():
        user = User(name="Test Doc", email="doc@hospital.com")
        user.set_password("securepassword123")
        db.session.add(user)
        db.session.commit()
        
        saved_user = User.query.filter_by(email="doc@hospital.com").first()
        assert saved_user is not None
        assert saved_user.check_password("securepassword123") is True
        assert saved_user.check_password("wrongpassword") is False
