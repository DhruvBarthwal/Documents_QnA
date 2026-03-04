from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import tempfile
import os
import faiss
import numpy as np

from ingestion.parse_docs import parse_file
from ingestion.clean_text import clean_documents
from ingestion.chunk_docs import chunk_documents
from ingestion.embed_docs import embed_documents
import runtime_store
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware


from agent.graph import build_graph

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

app = FastAPI(title="Drag & Drop RAG")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


graph = build_graph()

@app.get("/")
def home():
    return {"message" : "Backend is running"}
    

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt", ".html"}:
        raise HTTPException(400, "Unsupported file type")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = Path(tmp.name)

    try:
        raw = parse_file(path)
        cleaned = clean_documents(raw)
        chunks = chunk_documents(cleaned)

        runtime_store.TEXTS = [c["text"] for c in chunks]
        runtime_store.METADATA = [c["metadata"] for c in chunks]

        embeddings = embed_documents(
                    chunks,
                    model=embedder,
                    batch_size=32
                    ).astype("float32")

        dim = embeddings.shape[1]
        runtime_store.FAISS_INDEX = faiss.IndexFlatIP(dim)
        runtime_store.FAISS_INDEX.add(embeddings)

        return {"chunks": len(runtime_store.TEXTS)}

    finally:
        os.remove(path)

@app.post("/ask")
def ask(query: str):
    if runtime_store.FAISS_INDEX is None:
        raise HTTPException(400, "Upload a document first")

    result = graph.invoke({
        "query": query,
        "contexts": [],
        "answer": "",
        "cache_hit": False
    })

    return {"answer": result["answer"]}
