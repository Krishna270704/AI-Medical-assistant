import os
import hashlib
from gtts import gTTS
import logging

logger = logging.getLogger(__name__)

AUDIO_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'audio')
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_audio(text: str, lang='en') -> str:
    """
    Generates an MP3 file from text using gTTS and returns the filename.
    Implements basic caching using text hashing.
    """
    try:
        # Create a unique hash for this text and language
        text_hash = hashlib.md5(f"{text}_{lang}".encode('utf-8')).hexdigest()
        filename = f"{text_hash}.mp3"
        filepath = os.path.join(AUDIO_DIR, filename)
        
        # Cache hit
        if os.path.exists(filepath):
            logger.info(f"TTS Cache hit for {filename}")
            return filename
            
        # Cache miss
        logger.info(f"Generating new TTS audio for {filename}")
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filepath)
        return filename
    except Exception as e:
        logger.error(f"TTS Generation failed: {e}")
        return ""
