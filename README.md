# MARATHON: Enterprise Agentic RAG API

MARATHON is a production-grade, Agentic Retrieval-Augmented Generation (RAG) API built for enterprise use cases. It leverages a graph-based workflow to intelligently route user queries, retrieve and rerank relevant documents, and synthesize accurate answers while maintaining conversational memory and strict safety guardrails.

## 🚀 Architecture Overview

The core of the system is built on **LangGraph**, orchestrating a state machine that handles complex user queries. The system architecture includes:

1. **FastAPI Interface**: Provides REST endpoints for interacting with the agent.
2. **NeMo Guardrails**: Acts as the first line of defense, validating input and blocking jailbreak attempts or off-topic queries before they reach the LLM.
3. **Agent Workflow (LangGraph)**:
   - **Planner Node**: Analyzes the conversation history and the latest query to determine if the user is making a conversational query or if deep technical retrieval is required.
   - **Retriever Node**: Connects to the Qdrant Vector Database to fetch relevant chunks and uses a Cross-Encoder (FlashRank) to semantically re-rank them for maximum precision.
   - **Responder Node**: Synthesizes the final answer using Portkey as an LLM Gateway. If the exact query was asked recently, it pulls the response directly from Portkey's cache for zero-latency responses.
4. **Ingestion Pipeline**: Handles parsing, chunking, embedding, and uploading of various document types (PDFs, HTML, Office docs, Text) into the vector store.
5. **Observability**: Fully integrated with **Logfire** to trace execution spans, monitor latencies, and track cache hits across all agent nodes and API endpoints.

---

## 📁 Directory Structure & File Breakdown

### `app/` (Application Root)
*   **`main.py`**: The entry point of the application. It initializes FastAPI, configures Logfire, sets up the NeMo Guardrails, and exposes the `/query` and `/graph` endpoints.
*   **`config.py`**: Centralized configuration management using Pydantic/dotenv. Loads all API keys (Gemini, Groq, Qdrant) and environment variables securely.
*   **`guardrails.py`** *(pending creation)*: Configuration for NeMo Guardrails to enforce content safety.
*   **`gateway/client.py`**: Centralized initialization for the Langchain LLM via Portkey. Handles API key fallbacks and caching rules.

### `app/agents/` (LangGraph Orchestration)
*   **`graph.py`**: Defines the `StateGraph`. It wires together the planner, retriever, and responder nodes, establishes the conditional routing logic, and attaches `MemorySaver` for thread-based conversation memory.
*   **`state.py`**: Defines the `AgentState` schema (TypedDict). This state object is passed between nodes and holds the conversation history, current query, retrieved documents, execution plan, and status.
*   **`nodes/planner.py`**: The entry node. It asks the LLM to classify the user's intent based on the conversation history. If the query is just a greeting, it skips retrieval.
*   **`nodes/retriever.py`**: The semantic search node. It queries the vector database and relies on the ranking service to return only the most highly relevant documents.
*   **`nodes/responder.py`**: The generation node. It sends the prompt and retrieved context to the LLM via Portkey. It extracts the response and logs whether the response was dynamically generated or served instantly from Portkey's semantic cache.

### `app/ingestion/` (Data Processing)
*   **`processor.py`**: The main script/logic for ingesting raw data files into the vector database.
*   **`chunking/splitter.py`**: Contains logic to split large documents into smaller, semantically meaningful chunks (e.g., using Langchain's RecursiveCharacterTextSplitter) to optimize vector search.
*   **`loaders/html.py, office.py, pdf.py, text.py`**: Specific data loaders designed to parse and extract text from various file formats.

### `app/services/` (Core Utilities)
*   **`retrieval/qdrant_service.py`**: Connects to the Qdrant vector database, managing enterprise knowledge search using the `query_points` API.
*   **`retrieval/embeddings.py`**: Logic for converting text chunks into dense vector embeddings before they are inserted into Qdrant.
*   **`retrieval/ranking_service.py`**: Implements **FlashRank** (using a local ONNX model `ms-marco-MiniLM-L-6-v2`). Standard vector search is fast but mathematically fuzzy; this service cross-encodes the retrieved documents against the query to re-rank and return only the most accurate results.

### `ui/` (Frontend)
*   **`app.py`**: A clean, interactive Streamlit frontend that connects to the FastAPI backend. It maintains visual chat state and streams responses.

### Root Files
*   **`requirements.txt`**: Python dependencies required to run the project.
*   **`.env`**: Local environment variables (ignored by Git).
*   **`steps.txt`**: Project setup instructions or notes.

---

## 🛠️ Tech Stack
*   **Web Framework:** FastAPI
*   **Agent Orchestration:** LangGraph & LangChain
*   **Vector Database:** Qdrant
*   **LLM Gateway & Caching:** Portkey
*   **LLM Models:** Groq (Llama 3), Google Gemini
*   **Reranker:** FlashRank (Cross-Encoder)
*   **Safety:** NeMo Guardrails
*   **Observability:** Pydantic Logfire
