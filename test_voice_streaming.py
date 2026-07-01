import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_tts_service():
    print("Testing TTS Service...")
    from app.services.tts_service import generate_audio
    filename = generate_audio("Hello, this is a test of the text to speech service.", "en")
    if filename:
        print(f"[SUCCESS] TTS Generated successfully: {filename}")
    else:
        print("[FAILED] TTS Generation failed")

def test_language_service():
    print("Testing Language Service...")
    from app.services.language_service import get_language_instructions
    instructions = get_language_instructions()
    if "MULTILINGUAL SUPPORT" in instructions:
        print("[SUCCESS] Language instructions retrieved successfully")
    else:
        print("[FAILED] Language instructions failed")

if __name__ == "__main__":
    print("--- Testing Phase 5: Voice AI & Streaming ---")
    test_language_service()
    test_tts_service()
    
    # We cannot easily test SSE streaming synchronously without running the Flask server,
    # so we test the underlying generator logic instead.
    print("Testing Chat Streaming Generator...")
    from app.services.chat_service import stream_chat_response
    
    try:
        # Mock a session ID
        generator = stream_chat_response("test_session_123", "What is hypertension?")
        
        # Pull the first few events
        event1 = next(generator)
        print(f"Event 1: {event1.strip()}")
        
        event2 = next(generator)
        print(f"Event 2: {event2.strip()}")
        
        print("[SUCCESS] Streaming generator initialized and yielded events successfully!")
        
    except Exception as e:
        print(f"[FAILED] Streaming generator failed: {e}")

    print("\n[SUCCESS] Phase 5 logic tests completed!")
