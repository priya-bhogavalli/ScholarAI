import chromadb

def check_documents():
    """Check what documents are in ChromaDB"""
    
    client = chromadb.PersistentClient(path="./chroma_db")
    
    try:
        collection = client.get_collection("placement_papers")
        count = collection.count()
        
        print(f"📊 Total documents in ChromaDB: {count}")
        
        if count > 0:
            # Get sample documents
            sample = collection.get(limit=5, include=['documents', 'metadatas'])
            
            print(f"\n📋 Sample documents:")
            for i, (doc, metadata) in enumerate(zip(sample['documents'], sample['metadatas'])):
                print(f"\n{i+1}. File: {metadata.get('file_name', 'Unknown')}")
                print(f"   Company: {metadata.get('company', 'N/A')}")
                print(f"   Type: {metadata.get('file_type', 'N/A')}")
                print(f"   Content: {doc[:100]}...")
            
            # Get all metadata for statistics
            all_data = collection.get(include=['metadatas'])
            
            companies = {}
            file_types = {}
            
            for metadata in all_data['metadatas']:
                company = metadata.get('company', 'Unknown')
                file_type = metadata.get('file_type', 'unknown')
                companies[company] = companies.get(company, 0) + 1
                file_types[file_type] = file_types.get(file_type, 0) + 1
            
            print(f"\n🏢 Companies:")
            for company, count in sorted(companies.items(), key=lambda x: x[1], reverse=True):
                print(f"   {company}: {count} chunks")
            
            print(f"\n📄 File types:")
            for file_type, count in sorted(file_types.items()):
                print(f"   {file_type}: {count} chunks")
        
        else:
            print("❌ No documents found in ChromaDB")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_documents()