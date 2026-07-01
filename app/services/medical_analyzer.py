import logging
import json
from pydantic import BaseModel, Field
from typing import List, Dict
from app.services.llm_factory import get_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from flask import current_app
from app.rag.retriever import get_retriever

logger = logging.getLogger(__name__)

class AbnormalValue(BaseModel):
    name: str = Field(description="Name of the test or metric (e.g. Hemoglobin)")
    value: str = Field(description="The extracted value")
    status: str = Field(description="Must be 'High', 'Low', or 'Normal'")

class MedicalAnalysis(BaseModel):
    summary: str = Field(description="Plain-English summary of the report")
    key_findings: List[str] = Field(description="List of key findings")
    abnormal_values: List[AbnormalValue] = Field(description="List of abnormal or notable values")
    possible_conditions: List[str] = Field(description="Possible conditions clearly marked as AI-generated suggestions, not diagnoses")
    recommended_questions: List[str] = Field(description="Recommended questions to ask a doctor")
    lifestyle_recommendations: List[str] = Field(description="Lifestyle recommendations based on the report")
    follow_up_tests: List[str] = Field(description="Suggested follow-up tests")
    urgency_level: str = Field(description="Must be one of: 'Normal', 'Needs Attention', 'Consult Doctor Soon', 'Emergency'")
    medical_terms_explained: Dict[str, str] = Field(description="Dictionary mapping difficult medical terminology to simple language.")

def analyze_report(extracted_text: str) -> dict:
    """
    Analyzes the extracted medical report text.
    It first extracts key entities, queries RAG, and then generates the final analysis.
    """
    llm = get_llm()
    
    # Step 1: Extract entities to query RAG
    entity_prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract a comma-separated list of the 3 most important diseases, symptoms, or medicines mentioned in this text. If none, output 'None'."),
        ("human", "{text}")
    ])
    entity_chain = entity_prompt | llm
    try:
        entities = entity_chain.invoke({"text": extracted_text[:2000]}).content.strip()
    except Exception as e:
        logger.error(f"Entity extraction failed: {e}")
        entities = "None"
        
    # Step 2: Query RAG if entities exist
    context = ""
    sources = []
    if entities.lower() != "none" and len(entities) > 2:
        logger.info(f"Querying FAISS for entities: {entities}")
        try:
            retriever = get_retriever()
            docs = retriever.invoke(entities)
            if docs:
                for doc in docs:
                    source_name = doc.metadata.get("source", "Unknown Document")
                    page = doc.metadata.get("page", "")
                    src_str = f"{source_name} (Page {page})" if page else source_name
                    if src_str not in sources:
                        sources.append(src_str)
                    context += doc.page_content + "\n\n"
        except Exception as e:
            logger.error(f"RAG retrieval failed during analysis: {e}")

    # Step 3: Generate Structured Output
    parser = JsonOutputParser(pydantic_object=MedicalAnalysis)
    
    analysis_prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert medical AI assistant. Analyze the provided medical report and extract the information according to the requested JSON format.
        
        Ensure you:
        - Convert difficult medical terminology into simple language.
        - Clearly mark possible conditions as AI-generated suggestions, not diagnoses.
        - Be objective and factual.
        
        If relevant, utilize this retrieved medical knowledge to enhance your analysis:
        {context}
        
        Formatting Instructions:
        {format_instructions}"""),
        ("human", "Medical Report Text:\n{text}")
    ])
    
    chain = analysis_prompt | llm | parser
    
    try:
        result = chain.invoke({
            "text": extracted_text,
            "context": context if context else "No additional context found.",
            "format_instructions": parser.get_format_instructions()
        })
        # Attach RAG sources to result
        result['rag_sources'] = sources
        return result
    except Exception as e:
        logger.error(f"Failed to generate structured analysis: {e}")
        raise
