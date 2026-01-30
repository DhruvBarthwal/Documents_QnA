import os
import json
import numpy as np
import faiss

EMBEDDINGS_DIR = "data/embeddings"
FAISS_DIR = "data/faiss"

def load_embeddings():
    embeddings = np.load(os.path.join(EMBEDDINGS_DIR, "embeddings.npy"))
    with open(os.path.join(EMBEDDINGS_DIR, "texts.json"), "r") as f:
        texts = json.load(f)
    with open(os.path.join(EMBEDDINGS_DIR, "metadata.json"), "r") as f:
        metadata = json.load(f)
    
    return embeddings.astype("float32"), texts, metadata

def build_faiss_index(embeddings: np.ndarray):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index

def save_faiss_index(index, texts,  metadata):
    os.makedirs(FAISS_DIR, exist_ok=True)
    
    faiss.write_index(index, os.path.join(FAISS_DIR, "index.faiss"))
    
    with open(os.path.join(FAISS_DIR, "docstore.json"), "w") as f:
        json.dump(texts, f, indent = 2)
        
    with open(os.path.join(FAISS_DIR, "metadata.json"), "w") as f:
        json.dump(metadata,f, indent = 2)
        
if __name__ == "__main__":
    embeddings, texts, metadata  = load_embeddings()
    
    print(f"Load embeddigs : {embeddings.shape}")
    
    index = build_faiss_index(embeddings)
    
    print(f"Loaded embeddings : {embeddings.shape}")
    
    index = build_faiss_index(embeddings)
    
    print(f"FAISS index size: {index.ntotal}")
    
    save_faiss_index(index, texts, metadata)
    
    print("Faiss index saved successfully")