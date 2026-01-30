from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict
from  mcp.tools import RetrievalTools

app = FastAPI(title="MCP RAG Server")

tools = RetrievalTools()

class SearchRequest(BaseModel):
    query : str
    top_k : int = 5
    
class SearchResponse(BaseModel):
    results: List[Dict]



@app.post("/mcp/search_documents", response_model=SearchResponse)
def search_documents(req: SearchRequest):
    return tools.search_documents(
        query=req.query,
        top_k=req.top_k
    )


@app.get("/mcp/health")
def health():
    return tools.health()