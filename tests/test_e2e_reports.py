import pytest
from unittest.mock import patch
import io
from app import create_app
from app.core.config import TestingConfig
from app.models import db, User, MedicalReport

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

@patch('app.services.ocr_service.extract_text_from_file')
@patch('app.services.medical_analyzer.analyze_report')
def test_upload_report(mock_analyze, mock_extract, auth_client, app):
    """Test OCR file upload and DB persistence."""
    mock_extract.return_value = "Patient has mild fever."
    mock_analyze.return_value = {
        "summary": "Mild fever",
        "key_findings": ["Fever"],
        "abnormal_values": [],
        "lifestyle_recommendations": ["Rest"],
        "medical_terms_explained": {"Fever": "High temp"},
        "urgency_level": "LOW"
    }

    data = {
        'file': (io.BytesIO(b"dummy pdf content"), 'report.pdf'),
        'session_id': '1'
    }

    response = auth_client.post('/upload_report', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['summary'] == "Mild fever"
    assert json_data['urgency_level'] == "LOW"
    
    with app.app_context():
        # Verify it was saved to the DB
        report = MedicalReport.query.first()
        assert report is not None
        assert report.filename == 'report.pdf'
        assert report.urgency_level == 'LOW'
