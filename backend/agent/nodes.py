from typing import Dict
from agent.state import AgentState
from langchain_groq import ChatGroq
from agent.prompts import SYSTEM_PROMPT
import os
from langchain_core.messages import SystemMessage, HumanMessage
import requests
from cache.cache import AnswerCache
import runtime_store
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv

load_dotenv()
cache = AnswerCache()
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


llm = ChatGroq(
    model = "llama-3.1-8b-instant",
    max_tokens = 500,
    temperature = 0.2,
)

def retrieve_node(state: AgentState) -> AgentState:
    if runtime_store.FAISS_INDEX is None:
        state["contexts"] = []
        return state

    # Embed query
    query_vec = embedder.encode(
        [state["query"]],
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = runtime_store.FAISS_INDEX.search(query_vec, 5)

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx == -1:
            continue

        results.append({
            "text": runtime_store.TEXTS[idx],
            "score": float(score),
            "metadata": runtime_store.METADATA[idx]
        })

    state["contexts"] = results
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
            Context:
            {context_text}

            Task:
            Answer the question using the context above.
            Explain the concept clearly and in detail, but do not add information that is not present in the context.

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