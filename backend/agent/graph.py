from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import retrieve_node, validate_node, generate_node, cache_lookup_node, cache_store_node

def router_after_cache(state: AgentState):
    if state.get("cache_hit"):
        return END
    return "retrieve"
    
def build_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("cache_lookup",cache_lookup_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("validate", validate_node)
    graph.add_node("generate", generate_node)
    graph.add_node("cache_store", cache_store_node)
    
    graph.set_entry_point("cache_lookup")
    graph.add_conditional_edges(
        "cache_lookup",
        router_after_cache,
        {
            END : END,
            "retrieve" : "retrieve"
        }
    )
    graph.add_edge("retrieve","validate")
    graph.add_edge("validate", "generate")
    graph.add_edge("generate","cache_store")
    graph.add_edge("cache_store", END)
    
    return graph.compile()