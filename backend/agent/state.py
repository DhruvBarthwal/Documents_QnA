from typing import TypedDict, List, Dict

class AgentState(TypedDict):
    query : str
    contexts : List[Dict]
    answer : str
    cache_hit : bool
