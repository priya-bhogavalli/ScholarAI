try:
    from langchain_openai import ChatOpenAI
except ImportError:
    from langchain.chat_models import ChatOpenAI

try:
    from langchain.prompts import PromptTemplate
except ImportError:
    from langchain_core.prompts import PromptTemplate

from typing import Dict, List, Optional
import json
from .chroma_vector_store import VectorStoreManager

class RAGEngine:
    def __init__(self, vector_store_manager: VectorStoreManager, openai_api_key: str, model_name: str = "gpt-3.5-turbo"):
        self.vector_store_manager = vector_store_manager
        self.llm = ChatOpenAI(
            openai_api_key=openai_api_key,
            model_name=model_name,
            temperature=0.1
        )
        
        # Custom prompt template for educational content
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are an AI assistant helping students with their learning materials, mock tests, and placement preparation.

Context from learning materials:
{context}

Student Question: {question}

Instructions:
1. Provide accurate, educational responses based on the context
2. If the question is about a specific topic, explain concepts clearly
3. For practice questions, provide step-by-step solutions
4. If information is not in the context, clearly state that
5. Always encourage learning and provide additional study tips when relevant

Answer:"""
        )

    def query(self, question: str, max_docs: int = 5) -> Dict:
        """Process a query and return response with sources"""
        try:
            # Get relevant documents
            docs = self.vector_store_manager.similarity_search(question, k=max_docs)
            
            if not docs:
                return {
                    "answer": "I couldn't find any relevant information for your question. Please try rephrasing or ask about topics covered in the uploaded materials.",
                    "sources": [],
                    "confidence": "low",
                    "total_sources_found": 0
                }
            
            # Create context from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Generate response
            prompt = self.prompt_template.format(context=context, question=question)
            response = self.llm.invoke(prompt).content
            
            # Format response with sources
            result = {
                "answer": response,
                "sources": [],
                "confidence": "high" if len(docs) >= 3 else "medium",
                "total_sources_found": len(docs)
            }
            
            # Add source information
            for doc in docs:
                source_info = {
                    "file_name": doc.metadata.get("file_name", "Unknown"),
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_id": doc.metadata.get("chunk_id", 0),
                    "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "document_type": doc.metadata.get("document_type"),
                    "company": doc.metadata.get("company"),
                    "subject": doc.metadata.get("subject"),
                    "difficulty": doc.metadata.get("difficulty"),
                    "year": doc.metadata.get("year")
                }
                result["sources"].append(source_info)
            
            return result
            
        except Exception as e:
            return {
                "answer": f"I encountered an error while processing your question: {str(e)}",
                "sources": [],
                "confidence": "low",
                "total_sources_found": 0,
                "error": str(e)
            }

    def query_with_docs(self, question: str, docs: List) -> Dict:
        """Query with pre-filtered documents"""
        try:
            if not docs:
                return {
                    "answer": "I couldn't find any relevant information in the specified documents for your question.",
                    "sources": [],
                    "confidence": "low",
                    "total_sources_found": 0
                }
            
            # Create context from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Generate response
            prompt = self.prompt_template.format(context=context, question=question)
            response = self.llm.invoke(prompt).content
            
            # Format response
            result = {
                "answer": response,
                "sources": [],
                "confidence": "high" if len(docs) >= 3 else "medium",
                "total_sources_found": len(docs)
            }
            
            # Add source information
            for doc in docs:
                source_info = {
                    "file_name": doc.metadata.get("file_name", "Unknown"),
                    "source": doc.metadata.get("source", "Unknown"),
                    "chunk_id": doc.metadata.get("chunk_id", 0),
                    "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
                    "document_type": doc.metadata.get("document_type"),
                    "company": doc.metadata.get("company"),
                    "subject": doc.metadata.get("subject"),
                    "difficulty": doc.metadata.get("difficulty"),
                    "year": doc.metadata.get("year")
                }
                result["sources"].append(source_info)
            
            return result
            
        except Exception as e:
            return {
                "answer": f"I encountered an error: {str(e)}",
                "sources": [],
                "confidence": "low",
                "total_sources_found": 0,
                "error": str(e)
            }
    
    def get_relevant_documents(self, query: str, k: int = 5) -> List[Dict]:
        """Get relevant documents for a query"""
        docs = self.vector_store_manager.similarity_search_with_score(query, k=k)
        
        relevant_docs = []
        for doc, score in docs:
            doc_info = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "relevance_score": float(score)
            }
            relevant_docs.append(doc_info)
        
        return relevant_docs