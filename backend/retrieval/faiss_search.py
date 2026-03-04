import os 
import json
from typing import List, Dict
import time

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

        start = time.time()
        scores, indices = self.index.search(query_vec, top_k)
        print("FAISS time:", time.time() - start)

        seen = set()
        results = []

        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:
                continue

            if score < 0.4:
                continue

            chunk_id = self.metadata[idx].get("chunk_id", idx)

            if chunk_id in seen:
                continue

            seen.add(chunk_id)

            results.append({
                "text": self.texts[idx],
                "score": float(score),
                "metadata": self.metadata[idx]
            })

        return results

