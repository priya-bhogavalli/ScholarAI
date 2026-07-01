import json
import chromadb

def load_documents_to_chromadb():
    """Load processed documents into ChromaDB"""
    
    # Check if processed documents exist
    try:
        with open('processed_data/documents.json', 'r', encoding='utf-8') as f:
            documents = json.load(f)
        print(f"Found {len(documents)} processed documents")
    except FileNotFoundError:
        print("No processed documents found. Run document processing first.")
        return
    
    # Connect to ChromaDB
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
    total_batches = (len(documents) + batch_size - 1) // batch_size
    
    for i in range(0, len(documents), batch_size):
        batch_docs = documents[i:i+batch_size]
        
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
    
    # Test search
    results = collection.query(
        query_texts=["quantitative aptitude"],
        n_results=3
    )
    
    if results['documents'][0]:
        print(f"\nTest search found {len(results['documents'][0])} results")
        print(f"Sample result: {results['documents'][0][0][:100]}...")
    else:
        print("Test search failed")

if __name__ == "__main__":
    load_documents_to_chromadb()