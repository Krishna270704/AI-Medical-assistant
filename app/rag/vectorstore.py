import os
import logging
from langchain_community.vectorstores import FAISS
from app.rag.loaders import load_documents
from app.rag.splitters import split_documents
from app.rag.embeddings import get_embeddings_model

logger = logging.getLogger(__name__)

FAISS_INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'faiss_index')
DOCUMENTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'documents')

def build_vector_store():
    """Builds and saves the FAISS index from documents."""
    logger.info("Building vector store...")
    documents = load_documents(DOCUMENTS_DIR)
    if not documents:
        logger.warning("No documents found to build vector store.")
        return None

    chunks = split_documents(documents)
    embeddings = get_embeddings_model()
    
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    os.makedirs(FAISS_INDEX_PATH, exist_ok=True)
    vectorstore.save_local(FAISS_INDEX_PATH)
    
    logger.info(f"Vector store saved to {FAISS_INDEX_PATH}")
    return vectorstore

def get_vector_store():
    """Loads the FAISS index from disk, or builds it if it doesn't exist."""
    embeddings = get_embeddings_model()
    
    index_file = os.path.join(FAISS_INDEX_PATH, "index.faiss")
    if os.path.exists(index_file):
        logger.info("Loading existing FAISS index from disk.")
        return FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
    else:
        logger.info("FAISS index not found. Initiating build process.")
        return build_vector_store()
