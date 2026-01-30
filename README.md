# Document Q&A RAG Agent

A document-based Question Answering system built using Retrieval-Augmented Generation (RAG) principles.
The system retrieves relevant document chunks using vector search and generates answers grounded strictly in the retrieved context.

This project focuses on **backend** RAG architecture, graph-based orchestration, caching, and performance measurement.

## Features
### Core RAG Pipeline

- Document parsing and cleaning

- Recursive text chunking

- Dense embeddings using sentence transformers

- FAISS vector similarity search

- Context-grounded answer generation

### Graph-Based Agent (LangGraph)

- Explicit retrieval, validation, and generation nodes

- Deterministic execution flow

- Conditional short-circuiting for cached answers

- Easy to debug and extend

### Caching

- Answer-level caching (query → answer)

- Cache lookup as a graph node

- Cache hits skip retrieval and LLM calls

- Near-zero latency on repeated questions

### Observability

- Integrated with LangSmith

- Token usage per request

- Clear cache hit vs cache miss comparison

