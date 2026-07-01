from langchain_huggingface import HuggingFaceEmbeddings

def get_embeddings_model():
    """Returns the embedding model (HuggingFace sentence-transformers)."""
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
