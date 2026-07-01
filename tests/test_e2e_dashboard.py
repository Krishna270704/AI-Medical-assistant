import pytest
from app import create_app
from app.core.config import TestingConfig
from app.models import db, User, Appointment, MedicationReminder
from datetime import datetime, timedelta

@pytest.fixture
def app():
    app = create_app(config_class=TestingConfig)
    with app.app_context():
        db.create_all()
        # Seed user
        user = User(name="Test Doc", email="doc@hospital.com")
        user.set_password("securepassword123")
        db.session.add(user)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def auth_client(app):
    client = app.test_client()
    client.post('/login', data={'email': 'doc@hospital.com', 'password': 'securepassword123'})
    return client

def test_add_appointment(auth_client, app):
    """Test adding an appointment via dashboard route."""
    data = {
        'doctor_name': 'Dr. Smith',
        'specialty': 'Cardiology',
        'appointment_date': (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
    }
    response = auth_client.post('/dashboard/appointments/add', data=data)
    assert response.status_code == 302  # Redirects back to dashboard
    
    with app.app_context():
        appointment = Appointment.query.first()
        assert appointment is not None
        assert appointment.doctor_name == 'Dr. Smith'

def test_add_reminder(auth_client, app):
    """Test adding a medication reminder."""
    data = {
        'medication_name': 'Aspirin',
        'dosage': '100mg',
        'frequency': 'Daily',
        'time': '08:00'
    }
    response = auth_client.post('/dashboard/reminders/add', data=data)
    assert response.status_code == 302
    
    with app.app_context():
        reminder = MedicationReminder.query.first()
        assert reminder is not None
        assert reminder.medicine_name == 'Aspirin'
