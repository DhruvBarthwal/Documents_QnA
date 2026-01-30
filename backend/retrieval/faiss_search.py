import os 
import json
from typing import List, Dict

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

FAISS_DIR = "data/faiss"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

class FaissSearcher:
    def __init__(self):
        self.index = None
        self.texts = None
        self.metadata = None
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self._load_index()
        
    def _load_index(self):
        index_path = os.path.join(FAISS_DIR, "index.faiss")
        texts_path = os.path.join(FAISS_DIR, "docstore.json")
        metadata_path = os.path.join(FAISS_DIR, "metadata.json")

        if not os.path.exists(index_path):
            raise FileNotFoundError("FAISS index not found. Build index first.")

        self.index = faiss.read_index(index_path)

        with open(texts_path, "r") as f:
            self.texts = json.load(f)

        with open(metadata_path, "r") as f:
            self.metadata = json.load(f)
            
    def embed_query(self, query: str) -> np.ndarray:
        embedding = self.model.encode(
            [query],
            normalize_embeddings = True
        )
        return embedding.astype("float32")
    
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_vec = self.embed_query(query)
        
        scores, indices  = self.index.search(query_vec, top_k)
        
        results = []
        
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue
            
            results.append({
                "text" : self.texts[idx],
                "score" : float(score),
                "metadata" : self.metadata[idx]
            })
            
        return results

if __name__ == "__main__":
    searcher = FaissSearcher()

    query = "What is the enrollment no.?"
    results = searcher.search(query, top_k=3)

    for i, r in enumerate(results, 1):
        print(f"\nResult {i}")
        print("Score:", r["score"])
        print("Metadata:", r["metadata"])
        print("Text:", r["text"][:300], "...")