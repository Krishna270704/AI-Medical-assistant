import logging
from app.rag.vectorstore import get_vector_store

logger = logging.getLogger(__name__)

def get_retriever(top_k=3):
    """Returns the vector store retriever."""
    vectorstore = get_vector_store()
    if vectorstore:
        return vectorstore.as_retriever(search_kwargs={"k": top_k})
    return None

def format_docs(docs):
    """Formats retrieved documents into a context string."""
    if not docs:
        return "No relevant context found. Answer based on general medical knowledge."
    
    formatted = []
    for d in docs:
        source = d.metadata.get("source", "Unknown")
        page = d.metadata.get("page", "")
        page_str = f" (Page {page})" if page else ""
        formatted.append(f"[Source: {source}{page_str}]\n{d.page_content}")
        
    return "\n\n".join(formatted)
