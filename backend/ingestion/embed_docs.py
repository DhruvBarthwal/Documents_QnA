import os
import json
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

model = "sentence-transformers/all-MiniLM-L6-v2"

def embed_documents(docs, model, batch_size=32):
    texts = [doc["text"] for doc in docs]
    embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(
            batch,
            show_progress_bar=False,
            normalize_embeddings=True
        )
        embeddings.append(batch_embeddings)

    return np.vstack(embeddings)

def save_embeddings(
    embeddings : np.ndarray,
    docs: List[Dict],
    output_dir: str = "data/embeddings"
):
    os.makedirs(output_dir, exist_ok= True)
    
    np.save(os.path.join(output_dir,"embeddings.npy"),embeddings)
    
    texts = [doc["text"] for doc in docs]
    metadata = [doc["metadata"] for doc in docs]
    
    with open(os.path.join(output_dir, "texts.json"), "w", encoding="utf-8") as f:
        json.dump(texts, f, indent = 2)
    
    with open(os.path.join(output_dir, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    