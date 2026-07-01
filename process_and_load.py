import os
import json
import chromadb
from src.core.document_processor import DocumentProcessor

def process_and_load_documents():
    """Process documents from data folder and load into ChromaDB"""
    
    # Check if data folder exists
    if not os.path.exists("data"):
        print("No data folder found. Please ensure documents are in the 'data' folder.")
        return
    
    print("Processing documents from data folder...")
    
    # Initialize document processor
    processor = DocumentProcessor()
    
    # Process all documents
    all_documents = processor.process_directory("data")
    print(f"Processed {len(all_documents)} document chunks")
    
    if not all_documents:
        print("No documents were processed. Check if files exist in data folder.")
        return
    
    # Save processed documents
    os.makedirs("processed_data", exist_ok=True)
    json_documents = []
    for doc in all_documents:
        json_documents.append({
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    
    with open("processed_data/documents.json", "w", encoding="utf-8") as f:
        json.dump(json_documents, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(json_documents)} documents to processed_data/documents.json")
    
    # Load into ChromaDB
    print("Loading documents into ChromaDB...")
    
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Delete existing collection and recreate
    try:
        client.delete_collection("placement_papers")
        print("Deleted existing collection")
    except:
        pass
    
    collection = client.create_collection(
        name="placement_papers",
        metadata={"description": "Placement papers and study materials"}
    )
    
    # Load documents in batches
    batch_size = 50
    total_batches = (len(json_documents) + batch_size - 1) // batch_size
    
    for i in range(0, len(json_documents), batch_size):
        batch_docs = json_documents[i:i+batch_size]
        
        texts = [doc['content'] for doc in batch_docs]
        metadatas = [doc['metadata'] for doc in batch_docs]
        ids = [f"doc_{i+j}" for j in range(len(batch_docs))]
        
        collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Loaded batch {i//batch_size + 1}/{total_batches}")
    
    print(f"Successfully loaded {collection.count()} documents into ChromaDB!")
    
    # Show statistics
    companies = {}
    file_types = {}
    for doc in json_documents:
        company = doc['metadata'].get('company', 'Unknown')
        file_type = doc['metadata'].get('file_type', 'unknown')
        companies[company] = companies.get(company, 0) + 1
        file_types[file_type] = file_types.get(file_type, 0) + 1
    
    print("\nCompany breakdown:")
    for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True):
        print(f"  {company}: {count} chunks")
    
    print("\nFile type breakdown:")
    for file_type, count in sorted(file_types.items()):
        print(f"  {file_type}: {count} chunks")
    
    # Test search
    print("\nTesting search...")
    results = collection.query(
        query_texts=["quantitative aptitude"],
        n_results=3
    )
    
    if results['documents'][0]:
        print(f"Test search found {len(results['documents'][0])} results")
        print(f"Sample result: {results['documents'][0][0][:100]}...")
    else:
        print("Test search failed")

if __name__ == "__main__":
    process_and_load_documents()