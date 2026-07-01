import requests
import json
import time

def test_rag_comparison():
    """Compare RAG results with and without AI"""
    
    base_url = "http://127.0.0.1:8000"
    test_question = "What are quantitative aptitude topics?"
    
    print("🔬 RAG Comparison Test")
    print("=" * 50)
    print(f"Question: {test_question}")
    print("=" * 50)
    
    # Test current version (should be simple RAG)
    print("\n🤖 Testing Current Version...")
    try:
        response = requests.post(f"{base_url}/query", json={
            "question": test_question,
            "max_docs": 3
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Status: Success")
            print(f"📊 Sources found: {result.get('total_sources_found', 0)}")
            print(f"🎯 Confidence: {result.get('confidence', 'N/A')}")
            print(f"📝 Answer preview: {result.get('answer', '')[:200]}...")
            
            if result.get('sources'):
                print(f"📚 Source files:")
                for i, source in enumerate(result['sources'][:2]):
                    print(f"   {i+1}. {source.get('file_name', 'Unknown')}")
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("💡 Comparison Summary:")
    print("=" * 50)
    
    print("\n🔍 WITHOUT AI (Current - Simple RAG):")
    print("   ✅ FREE - No OpenAI costs")
    print("   ✅ Fast response")
    print("   ✅ Shows relevant document excerpts")
    print("   ❌ No intelligent synthesis")
    print("   ❌ Just raw document content")
    
    print("\n🧠 WITH AI (Full RAG):")
    print("   💰 Costs ~$0.01-0.02 per query")
    print("   ⏱️ Slower response (2-5 seconds)")
    print("   ✅ Intelligent, coherent answers")
    print("   ✅ Synthesizes multiple sources")
    print("   ✅ Educational explanations")
    
    print("\n🎯 Recommendation:")
    print("   • Use Simple RAG for demos/testing")
    print("   • Use AI RAG for production with students")
    print("   • Switch between versions as needed")
    
    print(f"\n🔧 To switch to AI version:")
    print("   1. Edit src/api/main.py")
    print("   2. Change import to: from ..core.rag_engine_fixed import RAGEngine")
    print("   3. Restart server")

if __name__ == "__main__":
    test_rag_comparison()