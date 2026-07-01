import requests

def test_rag():
    question = "What are the main topics in quantitative aptitude?"
    
    print(f"🧠 Testing RAG with question: {question}")
    print("-" * 50)
    
    try:
        response = requests.post("http://127.0.0.1:8000/query", json={
            "question": question,
            "max_docs": 3
        })
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Answer: {result.get('answer', '')}")
            print(f"📚 Sources found: {result.get('total_sources_found', 0)}")
            
            if result.get('sources'):
                print(f"📄 Source files:")
                for i, source in enumerate(result['sources']):
                    print(f"   {i+1}. {source.get('file_name', 'Unknown')}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_rag()