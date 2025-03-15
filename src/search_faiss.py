import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
faiss_index_file = "data/cuad/contracts_faiss.index"
input_file = "data/cuad/contracts.txt"

# Load Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Must match training model

# Load FAISS Index
index = faiss.read_index(faiss_index_file)

# Read contract text
with open(input_file, "r", encoding="utf-8") as file:
    contracts = file.readlines()

# User query
query = "Liability clause in the contract"  # Change to test different queries

# Generate query embedding
query_embedding = model.encode([query], convert_to_numpy=True)

# Search in FAISS
k = 5  # Number of results
distances, indices = index.search(np.array(query_embedding, dtype=np.float32), k)

# Display top results
print("\nTop Matching Contracts:\n")
for rank, idx in enumerate(indices[0]):
    print(f"Result {rank+1}: {contracts[idx]}\n")
