from typing import List, Dict
from sentence_transformers import CrossEncoder

RERANKER_MODEL = "BAAI/bge-reranker-base"

class Reranker:
    def _init__(self):
        self.model = CrossEncoder(RERANKER_MODEL)
        
    def rerank(
        self,
        query: str,
        results : List[Dict],
        top_k : int = 5
    ) -> List[Dict]:
        """
        Re-rank FAISS results using a cross encoder.
        """
        
        if not results:
            return []
        
        pairs = [(query, r["text"]) for r in results]
        scores = self.model.predict(pairs)
        
        for r, score in zip(results, scores):
            r["rerank_score"] = float(score)
            
        reranked = sorted(
            results,
            key = lambda x : x ["reranK_score"],
            reverse = True
        )
        
        return reranked[:top_k]

if __name__ == "__main__":
    from retrieval.faiss_search import FaissSearcher

    searcher = FaissSearcher()
    reranker = Reranker()

    query = "What is the termination notice period?"
    initial_results = searcher.search(query, top_k=20)

    reranked = reranker.rerank(query, initial_results, top_k=5)

    for i, r in enumerate(reranked, 1):
        print(f"\nResult {i}")
        print("Re-rank score:", r["rerank_score"])
        print("Metadata:", r["metadata"])
        print("Text:", r["text"][:300], "...")