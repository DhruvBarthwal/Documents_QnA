from typing import Dict
from agent.state import AgentState
from mcp.client import MCPClient
from langchain_groq import ChatGroq
from agent.prompts import System_Prompt
import os
from agent.prompts import SYSTEM_PROMPT
from langchain_core.messages import SystemMessage, HumanMessage

mcp = MCPClient("https://localhost:3333")

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    max_tokens = 300,
    temperature = 0.2,
    api_key = os.getenv("GROQ_API_KEY")
)

def retrieve_node (state: AgentState) -> AgentState:
    response = mcp.call_tool(
        "search_documents",
        {"query" : state["query"], "top_k" : 5}
    )
    state["contexts"] = response.get("results", [])
    return state

def validate_node(state: AgentState) -> AgentState:
    if not state["contexts"]:
        state["answer"] = "Not found in documents."
    return state

def generate_node(state: AgentState) -> AgentState:
    if state.get("answer"):
        return state
    context_text = "\n\n".join(
        f"[Source: {c['metadata']['source']}]\n{c['text']}"
        for c in state["contexts"]
    )
    
    messages = [
        SystemMessage(content= SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
            
            Context : 
            {context_text}
            
            Question:
            {state["query"]} 
            """
        )
    ]
    
    response = llm.invoke(messages)
    
    state["answer"] = response.content.strip()
    return state