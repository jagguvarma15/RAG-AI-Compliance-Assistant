import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
input_file = "data/cuad/contracts.txt"
faiss_index_file = "data/cuad/contracts_faiss.index"

# Load Transformer Model
model = SentenceTransformer("all-MiniLM-L6-v2")  # Produces 384-d embeddings

# Read contract text
with open(input_file, "r", encoding="utf-8") as file:
    contracts = file.readlines()

# Generate embeddings
print(f"Generating embeddings for {len(contracts)} contract sections...")
embeddings = model.encode(contracts, convert_to_numpy=True, show_progress_bar=True)

# Print embedding shape
print("Embedding shape:", embeddings.shape)  # Should be (N, 384)

# Correct FAISS index dimension
embedding_dim = embeddings.shape[1]  # Set dynamically

# Create FAISS index
index = faiss.IndexFlatL2(embedding_dim)  # Use detected dimension
index.add(np.array(embeddings, dtype=np.float32))  # Add embeddings

# Save FAISS index
faiss.write_index(index, faiss_index_file)

print(f"FAISS index with {index.ntotal} embeddings saved to '{faiss_index_file}'.")
