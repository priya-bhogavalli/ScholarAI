import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def test_openai_key():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key loaded: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        llm = ChatOpenAI(
            openai_api_key=api_key,
            model_name="gpt-3.5-turbo",
            temperature=0.1
        )
        
        response = llm.invoke("Say hello")
        print(f"✅ OpenAI API working! Response: {response.content}")
        
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")

if __name__ == "__main__":
    test_openai_key()