import os
import uuid
import logging
from app.rag.vectorstore import build_vector_store, get_vector_store
from app.rag.retriever import get_retriever, format_docs
from app.services.chat_service import get_chat_response
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

def create_sample_doc():
    doc_path = "data/documents/sample_medical_guidelines.txt"
    os.makedirs(os.path.dirname(doc_path), exist_ok=True)
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write("Clinical guidelines for Zeta-Syndrome: Zeta-Syndrome is a rare condition characterized by blue spots on the skin. Treatment involves applying alpha-cream twice a day for a week.")
    print(f"Created sample document at {doc_path}")

def test_rag():
    # 1. Create doc
    create_sample_doc()
    
    # 2. Build vector store
    print("\n--- Building Vector Store ---")
    vs = build_vector_store()
    
    # 3. Test Retrieval
    print("\n--- Testing Retrieval ---")
    retriever = get_retriever(top_k=1)
    docs = retriever.invoke("What is the treatment for Zeta-Syndrome?")
    print("Retrieved Docs:")
    for d in docs:
        print(f"- {d.page_content}")
        
    formatted = format_docs(docs)
    print("\nFormatted Context:")
    print(formatted)
    
    # 4. Test Chat Service End-to-End
    print("\n--- Testing E2E Chat Service ---")
    session_id = str(uuid.uuid4())
    print("Query: How do I treat Zeta-Syndrome?")
    response = get_chat_response(session_id, "How do I treat Zeta-Syndrome?")
    print("Response:")
    print(response.get('content', response))
    print("Sources:")
    print(response.get('sources', []))

if __name__ == "__main__":
    from flask import Flask
    load_dotenv()
    app = Flask(__name__)
    app.config['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY")
    
    with app.app_context():
        test_rag()
