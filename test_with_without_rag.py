import requests
import json
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def test_without_rag(question):
    """Test OpenAI without RAG (no document context)"""
    print("🤖 Testing WITHOUT RAG (Pure OpenAI)")
    print("-" * 40)
    
    try:
        llm = ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model_name="gpt-3.5-turbo",
            temperature=0.1
        )
        
        response = llm.invoke(question)
        
        print(f"✅ Response: {response.content}")
        print(f"💰 Cost: ~$0.01")
        print(f"📚 Sources: None (general knowledge only)")
        
        return response.content
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_with_rag(question):
    """Test with RAG (document context + OpenAI)"""
    print("\n🧠 Testing WITH RAG (Documents + OpenAI)")
    print("-" * 40)
    
    try:
        response = requests.post("http://127.0.0.1:8000/query", json={
            "question": question,
            "max_docs": 3
        })
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"✅ Response: {result.get('answer', '')[:300]}...")
            print(f"💰 Cost: ~$0.02")
            print(f"📚 Sources: {result.get('total_sources_found', 0)} documents")
            print(f"🎯 Confidence: {result.get('confidence', 'N/A')}")
            
            if result.get('sources'):
                print(f"📄 Source files:")
                for i, source in enumerate(result['sources'][:2]):
                    print(f"   {i+1}. {source.get('file_name', 'Unknown')}")
            
            return result.get('answer', '')
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def compare_rag():
    """Compare responses with and without RAG"""
    
    test_question = "What are the main topics in quantitative aptitude?"
    
    print("🔬 RAG vs NO-RAG Comparison Test")
    print("=" * 60)
    print(f"Question: {test_question}")
    print("=" * 60)
    
    # Test without RAG
    no_rag_response = test_without_rag(test_question)
    
    # Test with RAG
    rag_response = test_with_rag(test_question)
    
    # Comparison
    print("\n" + "=" * 60)
    print("📊 COMPARISON SUMMARY")
    print("=" * 60)
    
    print("\n❌ WITHOUT RAG:")
    print("   • Uses only general AI knowledge")
    print("   • May not match your specific documents")
    print("   • Generic educational content")
    print("   • No source attribution")
    
    print("\n✅ WITH RAG:")
    print("   • Uses your specific documents")
    print("   • Answers based on uploaded content")
    print("   • Shows source documents")
    print("   • More relevant to your materials")
    
    print("\n💡 Key Difference:")
    print("   RAG = Your Documents + AI Intelligence")
    print("   No RAG = Just AI General Knowledge")
    
    return no_rag_response, rag_response

if __name__ == "__main__":
    # First switch to AI RAG engine
    print("⚠️  Make sure to switch to AI RAG engine first!")
    print("   Edit src/api/main.py and change import to:")
    print("   from ..core.rag_engine_fixed import RAGEngine")
    print("   Then restart server with: python main.py")
    print("\nPress Enter to continue with test...")
    input()
    
    compare_rag()