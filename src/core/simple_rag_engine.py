from typing import Dict, List
from .chroma_vector_store import VectorStoreManager

class SimpleRAGEngine:
    def __init__(self, vector_store_manager: VectorStoreManager, openai_api_key: str = None, model_name: str = None):
        self.vector_store_manager = vector_store_manager
        print("Using Simple RAG Engine (No OpenAI API required)")

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
            
            # Create a simple response based on document content
            context_snippets = []
            for i, doc in enumerate(docs[:3]):  # Use top 3 documents
                snippet = doc.page_content[:300] + "..." if len(doc.page_content) > 300 else doc.page_content
                context_snippets.append(f"Document {i+1}: {snippet}")
            
            # Simple response without AI generation
            response = f"""Based on your question "{question}", I found {len(docs)} relevant documents in the database.

Here are the most relevant excerpts:

{chr(10).join(context_snippets)}

Note: This is a document search result. For AI-generated answers, please set up OpenAI API billing."""
            
            # Format response with sources
            result = {
                "answer": response,
                "sources": [],
                "confidence": "medium",
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
                "answer": f"I encountered an error while searching: {str(e)}",
                "sources": [],
                "confidence": "low",
                "total_sources_found": 0,
                "error": str(e)
            }

    def query_with_docs(self, question: str, docs: List) -> Dict:
        """Query with pre-filtered documents"""
        return self.query(question, max_docs=len(docs))
    
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