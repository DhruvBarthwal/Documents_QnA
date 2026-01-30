from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict

load_dotenv()

class State(TypedDict):
    msg: str

def node(state: State):
    state["msg"] = "hello"
    return state

graph = StateGraph(State)
graph.add_node("node", node)
graph.set_entry_point("node")
graph.add_edge("node", END)

app = graph.compile()

app.invoke({"msg": ""})
print("DONE")
