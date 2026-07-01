from langchain_nvidia_ai_endpoints import ChatNVIDIA
from flask import current_app

def get_llm():
    provider = current_app.config.get('LLM_PROVIDER', 'nvidia').lower()
    
    if provider == 'nvidia':
        return ChatNVIDIA(
            model=current_app.config.get('MODEL_NAME', 'nvidia/nemotron-3-ultra-550b-a55b'),
            nvidia_api_key=current_app.config['NVIDIA_API_KEY'],
            temperature=0.3
        )
    
    raise ValueError(f"Unsupported LLM Provider: {provider}")
