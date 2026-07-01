import logging
from langchain_core.runnables.history import RunnableWithMessageHistory
from app.services.llm_factory import get_llm
from app.services.prompt_manager import get_medical_prompt
from app.services.memory_service import get_session_history
from app.rag.retriever import get_retriever, format_docs

logger = logging.getLogger(__name__)

def get_chat_response(session_id: str, user_input: str) -> dict:
    try:
        llm = get_llm()
        prompt = get_medical_prompt()
        
        # Retrieval Phase
        retriever = get_retriever()
        docs = retriever.invoke(user_input) if retriever else []
        context = format_docs(docs)
        
        # Create the chain
        chain = prompt | llm
        
        # Wrap with history
        chain_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        # Invoke the chain
        response = chain_with_history.invoke(
            {"input": user_input, "context": context},
            config={"configurable": {"session_id": session_id}}
        )
        
        # Extract sources to pass back
        sources = []
        if docs:
            for d in docs:
                source = d.metadata.get("source", "Unknown")
                page = d.metadata.get("page", "")
                sources.append({"source": source, "page": page})
                
        return {"content": response.content, "sources": sources}
    except Exception as e:
        logger.error(f"Error in chat service: {e}")
        return {"content": "I'm sorry, I encountered an error while processing your request. Please try again.", "sources": []}

def stream_chat_response(session_id: str, user_input: str):
    """
    Generator that yields Server-Sent Events (SSE) for streaming the chat response token-by-token.
    """
    try:
        import json
        llm = get_llm()
        prompt = get_medical_prompt()
        
        yield f"data: {json.dumps({'status': 'SEARCHING'})}\n\n"
        
        retriever = get_retriever()
        docs = retriever.invoke(user_input) if retriever else []
        context = format_docs(docs)
        
        yield f"data: {json.dumps({'status': 'GENERATING'})}\n\n"
        
        chain = prompt | llm
        chain_with_history = RunnableWithMessageHistory(
            chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        sources = []
        if docs:
            for d in docs:
                source = d.metadata.get("source", "Unknown")
                page = d.metadata.get("page", "")
                sources.append({"source": source, "page": page})
                
        # Send sources first so UI can show them
        if sources:
            yield f"data: {json.dumps({'sources': sources})}\n\n"
        
        # Stream tokens
        full_response = ""
        for chunk in chain_with_history.stream(
            {"input": user_input, "context": context},
            config={"configurable": {"session_id": session_id}}
        ):
            if chunk.content:
                full_response += chunk.content
                yield f"data: {json.dumps({'chunk': chunk.content})}\n\n"
                
        # When done, trigger TTS generation
        yield f"data: {json.dumps({'status': 'DONE', 'full_text': full_response})}\n\n"
        
    except Exception as e:
        logger.error(f"Error in stream_chat_response: {e}")
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
