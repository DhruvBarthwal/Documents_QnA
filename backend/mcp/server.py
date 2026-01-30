from mcp.server.fastmcp import FastMCP
from mcp.tools import RetrievalTools

mcp = FastMCP("faiss-rag-server")

tools = RetrievalTools()

@mcp.tool()
def search_faiss(query: str, top_k: int = 5):
    """
    Semantic search over documents using FAISS
    """
    return tools.search_documents(query, top_k=top_k)

@mcp.tool()
def health():
    """
    Health check.
    """
    return tools.health()

if __name__ == "__main__":
    mcp.run()