from fastapi import FastAPI, Query
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
from transformers import pipeline
from mangum import Mangum  # Required if deploying to AWS Lambda

# Initialize FastAPI
app = FastAPI(title="AI Compliance Assistant")

# Load FAISS index and embedding model
model = SentenceTransformer("all-mpnet-base-v2")  # Better embeddings
index = faiss.read_index("data/cuad/contracts_faiss_optimized.index")

# Load contract texts
with open("data/cuad/contracts.txt", "r", encoding="utf-8") as file:
    contracts = file.readlines()

# OpenAI GPT-4 API Key (Replace with environment variable in production)
openai_client = OpenAI(api_key="your-openai-api-key")

# Load fraud detection model
fraud_model = pipeline("text-classification", model="nlptown/bert-base-multilingual-uncased-sentiment")

### **Task 1: RAG-Powered Legal Document Search**
@app.get("/search/")
def search_contracts(query: str = Query(..., title="Search Query"), k: int = 5):
    """
    AI-powered legal document retrieval with FAISS + GPT-4.
    """
    # Convert query to embeddings
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search in FAISS
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), k)

    # Retrieve top results
    retrieved_docs = [contracts[idx] for idx in indices[0]]

    # Generate a response using OpenAI's GPT-4
    rag_prompt = f"Using these legal documents:\n{retrieved_docs}\nAnswer this query: {query}"
    response = openai_client.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": rag_prompt}]
    )

    return {"query": query, "retrieved_docs": retrieved_docs, "generated_answer": response["choices"][0]["message"]["content"]}

### **Task 2: LLM-Powered Fraud Risk Assessment**
@app.get("/risk-assessment/")
def risk_assessment(document: str):
    """
    Automated risk assessment using LLM-powered fraud detection.
    """
    # Run fraud detection
    result = fraud_model(document)

    return {"document": document, "fraud_risk_score": result[0]["score"], "label": result[0]["label"]}

# AWS Lambda Compatibility (If deploying on Lambda)
handler = Mangum(app)
