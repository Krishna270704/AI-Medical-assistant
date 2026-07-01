import logging

logger = logging.getLogger(__name__)

def get_language_instructions() -> str:
    """
    Returns the system prompt instructions for handling multilingual support.
    The LLM is excellent at zero-shot language detection and translation.
    """
    return """
    MULTILINGUAL SUPPORT INSTRUCTIONS:
    - Automatically detect the language of the user's query (English, Hindi, or Hinglish).
    - You MUST respond in the EXACT same language the user used.
    - If responding in Hindi or Hinglish, preserve complex medical terminology in English (or simple transliteration) to maintain accuracy.
    - Translate difficult medical concepts into simple, culturally relevant language.
    """
