import chromadb
from langchain_core.documents import Document as LangchainDocument
from typing import List, Optional, Dict, Any

class ChromaVectorStoreManager:
    def __init__(self, database_url: str = None, openai_api_key: str = None):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        try:
            self.collection = self.client.get_collection("placement_papers")
            print(f"Connected to existing ChromaDB with {self.collection.count()} documents")
        except:
            self.collection = self.client.get_or_create_collection(
                name="placement_papers",
                metadata={"description": "Placement papers and study materials"}
            )
            print("Created new ChromaDB collection")
    
    def add_documents(self, documents: List[LangchainDocument]) -> None:
        if not documents:
            return
        
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        ids = [f"doc_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Added {len(documents)} documents to ChromaDB")
    
    def similarity_search(self, query: str, k: int = 5) -> List[LangchainDocument]:
        if self.collection.count() == 0:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        
        documents = []
        if results['documents'] and results['documents'][0]:
            for i, (doc, metadata) in enumerate(zip(results['documents'][0], results['metadatas'][0])):
                documents.append(LangchainDocument(
                    page_content=doc,
                    metadata=metadata
                ))
        
        return documents
    
    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        if self.collection.count() == 0:
            return []
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            include=['documents', 'metadatas', 'distances']
        )
        
        documents_with_scores = []
        if results['documents'] and results['documents'][0]:
            for doc, metadata, distance in zip(
                results['documents'][0], 
                results['metadatas'][0], 
                results['distances'][0]
            ):
                documents_with_scores.append((
                    LangchainDocument(page_content=doc, metadata=metadata),
                    distance
                ))
        
        return documents_with_scores
    
    def similarity_search_with_filters(self, query: str, k: int = 5, filters: Optional[Dict] = None) -> List[LangchainDocument]:
        if self.collection.count() == 0:
            return []
        
        # ChromaDB filtering
        where_clause = {}
        if filters:
            for key, value in filters.items():
                where_clause[key] = value
        
        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where_clause if where_clause else None
        )
        
        documents = []
        if results['documents'] and results['documents'][0]:
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                documents.append(LangchainDocument(
                    page_content=doc,
                    metadata=metadata
                ))
        
        return documents
    
    def get_available_filters(self) -> Dict[str, List[str]]:
        if self.collection.count() == 0:
            return {}
        
        try:
            # Get all documents to extract filter options
            all_data = self.collection.get(include=['metadatas'])
            
            filters = {
                "document_types": [],
                "companies": [],
                "subjects": [],
                "difficulties": [],
                "years": []
            }
            
            for metadata in all_data['metadatas']:
                if metadata.get('document_type'):
                    filters["document_types"].append(metadata['document_type'])
                if metadata.get('company'):
                    filters["companies"].append(metadata['company'])
                if metadata.get('subject'):
                    filters["subjects"].append(metadata['subject'])
                if metadata.get('difficulty'):
                    filters["difficulties"].append(metadata['difficulty'])
                if metadata.get('year'):
                    filters["years"].append(metadata['year'])
            
            # Remove duplicates and sort
            for key in filters:
                filters[key] = sorted(list(set(filters[key])))
            
            return filters
        except:
            return {}
    
    def get_collection_count(self) -> int:
        try:
            return self.collection.count()
        except:
            return 0
    
    def reset_collection(self) -> None:
        try:
            self.client.delete_collection("placement_papers")
            self.collection = self.client.get_or_create_collection(
                name="placement_papers",
                metadata={"description": "Placement papers and study materials"}
            )
            print("Reset ChromaDB collection")
        except Exception as e:
            print(f"Error resetting: {str(e)}")

# Alias for compatibility
VectorStoreManager = ChromaVectorStoreManager