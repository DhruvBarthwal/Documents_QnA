from typing import Dict
from agent.state import AgentState
from langchain_groq import ChatGroq
from agent.prompts import SYSTEM_PROMPT
import os
from langchain_core.messages import SystemMessage, HumanMessage
import requests
from cache.cache import AnswerCache

cache = AnswerCache()

llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    max_tokens = 300,
    temperature = 0.2,
    api_key = os.getenv("GROQ_API_KEY")
)

def retrieve_node(state: AgentState) -> AgentState:
    response = requests.post(
        "http://localhost:3333/mcp/search_documents",
        json={
            "query": state["query"],
            "top_k": 5
        },
        timeout=30
    )

    state["contexts"] = response.json().get("results", [])
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

def cache_lookup_node(state: AgentState) -> AgentState:
    cached_answer = cache.get(state["query"])

    if cached_answer and cached_answer.strip():
        state["answer"] = cached_answer
        state["contexts"] = []
        state["cache_hit"] = True
    else:
        state["cache_hit"] = False

    return state
    
def cache_store_node(state: AgentState) -> AgentState:
    answer = state.get("answer", "").strip()

    if answer and answer.lower() != "not found in documents.":
        cache.set(state["query"], answer)

    return state