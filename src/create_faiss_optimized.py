from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a more accurate transformer model
model = SentenceTransformer("all-mpnet-base-v2")  # Better than MiniLM

# Load contract texts
with open("data/cuad/contracts.txt", "r", encoding="utf-8") as file:
    contracts = file.readlines()

# Generate improved embeddings
embeddings = model.encode(contracts, convert_to_numpy=True, show_progress_bar=True)

# Create FAISS index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(embeddings, dtype=np.float32))

# Save FAISS index
faiss.write_index(index, "data/cuad/contracts_faiss_optimized.index")

print(f"Optimized FAISS index with {index.ntotal} embeddings saved.")
