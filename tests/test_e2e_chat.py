import pytest
from unittest.mock import patch, MagicMock
from app import create_app
from app.core.config import TestingConfig
from app.models import db, User, ChatSession

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
def client(app):
    return app.test_client()

@pytest.fixture
def auth_client(client, app):
    # Log the user in
    client.post('/login', data={'email': 'doc@hospital.com', 'password': 'securepassword123'})
    return client

@patch('app.routes.main.get_session_history')
@patch('app.services.chat_service.stream_chat_response')
def test_chat_stream(mock_stream, mock_get_history, auth_client, app):
    """Test the SSE chat stream with mocked LangChain/Gemini."""
    # Mock history
    mock_history_obj = MagicMock()
    mock_history_obj.messages = []
    mock_get_history.return_value = mock_history_obj
    
    # Streaming response mock (generator)
    def fake_stream(*args, **kwargs):
        yield "data: Hello\n\n"
        yield "data:  World\n\n"
        
    mock_stream.side_effect = fake_stream
    
    with app.app_context():
        user = User.query.filter_by(email="doc@hospital.com").first()
        chat = ChatSession(user_id=user.id, title="Test Chat")
        db.session.add(chat)
        db.session.commit()
        chat_id = chat.id

    response = auth_client.get(f'/chat_stream?user_input=Hi&session_id={chat_id}')
    assert response.status_code == 200
    assert response.content_type == 'text/event-stream; charset=utf-8'
    
    data = response.get_data(as_text=True)
    assert "data: Hello" in data
    assert "data:  World" in data
