from typing import TypedDict, List

class SearchRequest(TypedDict):
    query : str
    top_k : int
    
class SearchResult(TypedDict):
    text : str
    score : float
    metadata : dict
    
class SearchResponse(TypedDict):
    results : List[SearchResult]