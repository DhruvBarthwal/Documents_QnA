from typing import Dict
from retrieval.faiss_search import FaissSearcher
from retrieval.reranker import Reranker

class RetrievalTools:
    
    def __init__(self):
        self.searcher = FaissSearcher()
        self.reranker = Reranker()

    def search_documents(
        self,
        query: str,
        top_k: int = 5,
        initial_k: int = 20
    ) -> Dict:
        """
        Semantic search + re-ranking over documents.
        """
        initial_results = self.searcher.search(query, top_k=initial_k)

        reranked_results = self.reranker.rerank(
            query=query,
            results=initial_results,
            top_k=top_k
        )

        return {
            "results": reranked_results
        }

        
    def health(self) -> Dict:
        """
        Simple health check
        """
        return {"status" : "ok"}