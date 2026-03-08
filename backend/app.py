# app.py
from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from pathlib import Path
import tempfile, os, uuid, asyncio
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

upload_status: dict = {}  

def process_file_sync(file_id: str, path: Path):
    """Runs in background thread — does all the heavy work."""
    try:
        upload_status[file_id] = {"status": "processing", "stage": "parsing"}
        raw = parse_file(path)
        
        upload_status[file_id]["stage"] = "cleaning"
        cleaned = clean_documents(raw)
        
        upload_status[file_id]["stage"] = "chunking"
        chunks = chunk_documents(cleaned)

        upload_status[file_id]["stage"] = "embedding"
        embeddings = embed_documents(
            chunks, model=embedder, batch_size=128
        ).astype("float32")

        upload_status[file_id]["stage"] = "indexing"
        dim = embeddings.shape[1]
        index = faiss.IndexFlatIP(dim)
        index.add(embeddings)

        runtime_store.TEXTS = [c["text"] for c in chunks]
        runtime_store.METADATA = [c["metadata"] for c in chunks]
        runtime_store.FAISS_INDEX = index

        upload_status[file_id] = {
            "status": "ready",
            "chunks": len(chunks)
        }
    except Exception as e:
        upload_status[file_id] = {"status": "error", "error": str(e)}
    finally:
        if path.exists():
            os.remove(path)


@app.post("/upload")
async def upload(file: UploadFile = File(...), background_tasks: BackgroundTasks = None):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in {".pdf", ".docx", ".txt", ".html"}:
        raise HTTPException(400, "Unsupported file type")

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        path = Path(tmp.name)

    file_id = str(uuid.uuid4())
    upload_status[file_id] = {"status": "processing", "stage": "starting"}

    background_tasks.add_task(process_file_sync, file_id, path)

    return {"file_id": file_id, "status": "processing"} 


@app.get("/status/{file_id}")
def status(file_id: str):
    """Frontend polls this every second to check progress."""
    info = upload_status.get(file_id)
    if not info:
        raise HTTPException(404, "Unknown file_id")
    return info


@app.get("/")
def home():
    return {"message": "Backend is running"}


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