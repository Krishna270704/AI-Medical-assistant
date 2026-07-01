import os
from langchain_community.chat_message_histories import SQLChatMessageHistory

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'chat_history.db')
CONNECTION_STRING = f"sqlite:///{DB_PATH}"

def get_session_history(session_id: str):
    # Ensure database directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    return SQLChatMessageHistory(
        session_id=session_id,
        connection=CONNECTION_STRING
    )

def add_report_to_memory(session_id: str, report_text: str):
    """
    Injects the uploaded report text into the session memory as a System Message.
    This ensures the LLM remembers it for follow-up questions, 
    but it won't be rendered in the UI (since UI only renders human/ai types).
    """
    from langchain_core.messages import SystemMessage
    history = get_session_history(session_id)
    history.add_message(SystemMessage(content=f"User uploaded a medical report. Here is the extracted text:\n\n{report_text}"))
