import os
import json
from typing import List, Dict

import numpy as np
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

def embed_documents(
    docs: List[Dict],
    batch_size: int = 32
):
    """
    Generate embeddings for chunked documents 
    
    :param docs: List of chunked documents
    :type docs: List[Dict]
    :param batch_size: length of batch size
    :type batch_size: int
    """
    
    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    
    texts = [doc["text"] for doc in docs]
    embeddings = []
    
    for i in tqdm(range(0, len(texts), batch_size), desc = "Embedding"):
        batch = texts[i:i + batch_size]
        batch_embeddings = model.encode(
            batch,
            show_progress_bar=False,
            normalize_embeddings = True
        )
        embeddings.append(batch_embeddings)
    
    embeddings = np.vstack(embeddings)
    return embeddings

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
    
if __name__ == "__main__":
    from parse_docs import parse_directory
    from clean_text import clean_documents
    from chunk_docs import chunk_documents

    raw_docs = parse_directory("data/raw")
    cleaned_docs = clean_documents(raw_docs)
    chunked_docs = chunk_documents(cleaned_docs)

    embeddings = embed_documents(chunked_docs)
    save_embeddings(embeddings, chunked_docs)

    print(f"Embedded {len(chunked_docs)} chunks")
    print(f"Embedding dimension: {embeddings.shape[1]}")