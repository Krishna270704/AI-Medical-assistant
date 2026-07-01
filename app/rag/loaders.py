import os
import logging
from langchain_community.document_loaders import PyPDFLoader, TextLoader, UnstructuredMarkdownLoader

logger = logging.getLogger(__name__)

def load_documents(directory_path: str):
    """Load PDF, TXT, and MD files from a directory."""
    documents = []
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)
        return documents

    for filename in os.listdir(directory_path):
        filepath = os.path.join(directory_path, filename)
        try:
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(filepath)
                documents.extend(loader.load())
            elif filename.endswith(".txt"):
                loader = TextLoader(filepath, encoding='utf-8')
                documents.extend(loader.load())
            elif filename.endswith(".md"):
                loader = UnstructuredMarkdownLoader(filepath)
                documents.extend(loader.load())
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")

    logger.info(f"Loaded {len(documents)} document chunks from {directory_path}")
    return documents
