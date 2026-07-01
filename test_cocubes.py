import requests
import json
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def test_cocubes_example():
    """Test Cocubes-specific question with and without RAG"""
    
    question = "What types of questions does Cocubes ask in their placement tests?"
    
    print("Cocubes RAG Test")
    print("=" * 50)
    print(f"Question: {question}")
    print("=" * 50)
    
    # Test WITHOUT RAG (Pure OpenAI)
    print("\n1. WITHOUT RAG (General AI Knowledge)")
    print("-" * 40)
    
    try:
        llm = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model_name="gpt-3.5-turbo",
            temperature=0.1
        )
        
        response = llm.invoke(question)
        print(f"Answer: {response.content[:200]}...")
        print("Sources: None (general knowledge)")
        
    except Exception as e:
        print(f"Error: {e}")
    
    # Test WITH RAG (Your Documents + AI)
    print("\n2. WITH RAG (Your Cocubes Documents + AI)")
    print("-" * 40)
    
    try:
        response = requests.post("http://127.0.0.1:8000/query", json={
            "question": question,
            "max_docs": 5
        })
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"Answer: {result.get('answer', '')[:200]}...")
            print(f"Sources found: {result.get('total_sources_found', 0)}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            
            if result.get('sources'):
                print("Source files:")
                for i, source in enumerate(result['sources'][:3]):
                    print(f"  {i+1}. {source.get('file_name', 'Unknown')}")
                    
        else:
            print(f"Error: {response.status_code}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("COMPARISON:")
    print("WITHOUT RAG: Generic info about placement tests")
    print("WITH RAG: Specific info from your Cocubes documents")
    print("Cost: ~$0.03 total for both tests")

if __name__ == "__main__":
    print("Make sure your server is running with AI RAG engine!")
    print("Press Enter to start Cocubes test...")
    input()
    
    test_cocubes_example()