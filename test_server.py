import uvicorn
from fastapi import FastAPI
import os

# Set OpenAI API key if not set
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not set. Please set it before using the API.")

app = FastAPI(title="ScholarAI Test Server")

@app.get("/")
def read_root():
    return {"message": "ScholarAI Server is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "Server is working"}

if __name__ == "__main__":
    print("Starting ScholarAI Test Server...")
    uvicorn.run(
        "test_server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )