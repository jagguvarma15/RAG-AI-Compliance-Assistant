from fastapi import FastAPI, Query
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Initialize FastAPI app
app = FastAPI(title="AI Compliance & Risk Assistant")

@app.get("/")
def home():
    return {"message": "Welcome to the AI Compliance & Risk Assistant API. Use /search to query contracts."}

# Paths
FAISS_INDEX_FILE = "data/cuad/contracts_faiss.index"
TEXT_FILE = "data/cuad/contracts.txt"

# Load model and FAISS index
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index(FAISS_INDEX_FILE)

# Load contract texts
with open(TEXT_FILE, "r", encoding="utf-8") as file:
    contracts = file.readlines()

@app.get("/search/")
def search_contracts(query: str = Query(..., title="Search Query"), k: int = 5):
    """
    Search the FAISS index and return the top matching contract sections.
    """
    # Convert query to embedding
    query_embedding = model.encode([query], convert_to_numpy=True)

    # Search in FAISS
    distances, indices = index.search(np.array(query_embedding, dtype=np.float32), k)

    # Retrieve matching contracts
    results = [{"rank": i + 1, "text": contracts[idx].strip()} for i, idx in enumerate(indices[0])]

    return {"query": query, "results": results}
