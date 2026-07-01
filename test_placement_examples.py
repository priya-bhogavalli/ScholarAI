import requests
import json
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def test_specific_examples():
    """Test specific examples from placement paper data"""
    
    # Test questions based on typical placement paper content
    test_questions = [
        "What are the key topics in quantitative aptitude for placement tests?",
        "Explain logical reasoning questions commonly asked in interviews",
        "What programming concepts are tested in technical interviews?",
        "How to solve time and work problems in aptitude tests?",
        "What are the important English grammar topics for placements?"
    ]
    
    print("Testing RAG with Placement Paper Examples")
    print("=" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\nTest {i}: {question}")
        print("-" * 50)
        
        try:
            # Test with RAG
            response = requests.post("http://127.0.0.1:8000/query", json={
                "question": question,
                "max_docs": 3
            })
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"Sources found: {result.get('total_sources_found', 0)}")
                print(f"Confidence: {result.get('confidence', 'N/A')}")
                
                if result.get('sources'):
                    print("Source files:")
                    for j, source in enumerate(result['sources'][:2]):
                        print(f"  {j+1}. {source.get('file_name', 'Unknown')}")
                        print(f"     Company: {source.get('company', 'N/A')}")
                
                print(f"Answer: {result.get('answer', '')[:200]}...")
                
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        print()
        
        # Pause to avoid too many API calls
        if i < len(test_questions):
            input("Press Enter for next test (or Ctrl+C to stop)...")

def test_company_specific():
    """Test company-specific questions"""
    
    company_questions = [
        "What types of questions does Cocubes ask in their tests?",
        "Tell me about Mphasis placement process",
        "What are Valuelabs technical interview questions?",
        "How to prepare for ZenQ placement test?"
    ]
    
    print("\nTesting Company-Specific Questions")
    print("=" * 60)
    
    for question in company_questions:
        print(f"\nQuestion: {question}")
        print("-" * 40)
        
        try:
            response = requests.post("http://127.0.0.1:8000/query", json={
                "question": question,
                "max_docs": 5
            })
            
            if response.status_code == 200:
                result = response.json()
                print(f"Sources: {result.get('total_sources_found', 0)}")
                print(f"Answer: {result.get('answer', '')[:150]}...")
            else:
                print(f"Error: {response.status_code}")
                
        except Exception as e:
            print(f"Error: {e}")
        
        input("Press Enter for next test...")

if __name__ == "__main__":
    print("RAG Testing with Real Placement Paper Examples")
    print("=" * 60)
    print("This will test your RAG system with questions specific to")
    print("the placement papers you've uploaded.")
    print()
    print("Choose test type:")
    print("1. General aptitude topics (5 tests)")
    print("2. Company-specific questions (4 tests)")
    print("3. Both")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice in ['1', '3']:
        test_specific_examples()
    
    if choice in ['2', '3']:
        test_company_specific()
    
    print("\nTesting complete!")
    print("Cost estimate: ~$0.05-0.15 total")