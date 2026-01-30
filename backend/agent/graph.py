from langgraph.graph import StateGraph, END
from agent.state import AgentState
from agent.nodes import retrieve_node, validate_node, generate_node

def build_graph():
    graph = StateGraph(AgentState)
    
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("validate", validate_node)
    graph.add_node("generate", generate_node)
    
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve","validate")
    graph.add_edge("validate", "generate")
    graph.add_edge("generate",END)
    
    return graph.compile()