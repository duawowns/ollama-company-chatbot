# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

퓨쳐시스템 AI 챗봇 - RAG-based company information chatbot using Ollama, ChromaDB, BGE-M3 embeddings, and FlashRank reranking. This is a capstone design project for Dongseo University.

**Tech Stack:**
- Python 3.10+
- Chainlit 2.9.0 (recommended UI) / Streamlit 1.41.1 (legacy UI)
- Ollama (LLM backend)
- LangChain 0.3.13 (RAG framework)
- ChromaDB 0.5.23 (vector database)
- BGE-M3 embeddings (Korean SOTA model)
- FlashRank 0.2.9 (reranking)

## Essential Commands

### Initial Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not installed)
curl -fsSL https://ollama.com/install.sh | sh

# Download LLM model (llama3.2 3B recommended)
ollama pull llama3.2:3b

# Start Ollama server (must be running before chatbot)
ollama serve

# Create vector store (first time only)
python scripts/create_vectorstore.py
```

### Running the Application

**Chainlit (Recommended):**
```bash
# Run Chainlit app
chainlit run chainlit_app.py -w --port 8501

# Or use script
./run_chainlit.sh
```

**Streamlit (Legacy):**
```bash
streamlit run app.py

# Or use script
./run.sh
```

### Docker Deployment
```bash
# Start all services (Ollama + Chatbot)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Testing and Debugging
```bash
# Test vector store search
python scripts/create_vectorstore.py  # Includes test query at end

# Check Ollama is running
ollama list

# View application logs
tail -f chatbot.log
```

## Architecture

### Core Components

**RAG Pipeline (`utils/rag_pipeline.py`):**
- Central RAG implementation with ChromaDB retrieval, BGE-M3 embeddings, and FlashRank reranking
- `RAGPipeline` class handles: LLM initialization, vectorstore loading, document retrieval/reranking, QA chain creation
- Streaming query support for real-time responses
- Input validation and security checks (XSS prevention, query length limits)
- Retrieval flow: Query → Similarity search (k=10) → FlashRank reranking (top 3) → LLM generation

**Application Entry Points:**
- `chainlit_app.py`: Production-ready Chainlit UI with auth, rate limiting, structured logging
- `app.py`: Legacy Streamlit UI with custom Linear.app-inspired styling

**Utilities:**
- `utils/auth.py`: Optional authentication (enable via `AUTH_ENABLED=true`)
- `utils/rate_limiter.py`: Rate limiting (30 req/min, 100 req/hour by default)
- `utils/health.py`: Health check endpoints
- `utils/data_loader.py`: Data loading utilities

**Scripts:**
- `scripts/create_vectorstore.py`: Creates ChromaDB vectorstore from CSV data (run once on setup)
- `scripts/train_embedding.py`: Custom embedding training utilities
- `scripts/quick_deploy.sh`: Quick deployment script

### Data Flow

1. **Vector Store Creation** (one-time):
   - CSV data (`data/datasets/company_qa.csv`) → Document loading → Text splitting → BGE-M3 embedding → ChromaDB persistence (`data/vectorstore/`)

2. **Query Processing** (runtime):
   - User query → Input validation → Vector similarity search (k=10) → FlashRank reranking (top 3) → LangChain prompt with context + chat history → Ollama LLM → Streaming response

3. **Chat History Management**:
   - Last 5 conversations stored in session state
   - History included in prompt context for follow-up questions (translations, summaries)

### Configuration

**Environment Variables** (`.env` or environment):
- `OLLAMA_BASE_URL`: Ollama server URL (default: `http://localhost:11434`)
- `MAX_QUERY_LENGTH`: Max query characters (default: 500)
- `MAX_HISTORY_ITEMS`: Chat history items to keep (default: 5)
- `LOG_LEVEL`: Logging level (default: INFO)
- `AUTH_ENABLED`: Enable authentication (default: false)
- `RATE_LIMIT_PER_MINUTE`: Rate limit per minute (default: 30)
- `RATE_LIMIT_PER_HOUR`: Rate limit per hour (default: 100)
- `CHAINLIT_PORT`: Chainlit port (default: 8501)

**Chainlit Configuration** (`.chainlit/config.toml`):
- UI theme: Navy blue + cyan colors matching project poster
- Custom styling and branding

## Development Guidelines

### Working with RAG Pipeline

**Modifying Prompts:**
- Prompt template in `utils/rag_pipeline.py:146-165` (in `create_qa_chain` method)
- Current rules: No flattery, use context first, fallback to chat history, error message for unknown info

**Changing Models:**
- Default: `llama3.2:3b` (lightweight, Railway-compatible)
- Alternatives: `llama3.1:8b`, `mistral:7b`, `gemma:7b`
- Change in Chainlit: `chainlit_app.py:64` or via settings UI
- Change in Streamlit: Sidebar dropdown

**Adjusting Retrieval:**
- Initial retrieval count: `utils/rag_pipeline.py:172` (`search_kwargs={"k": 10}`)
- Reranking top count: `utils/rag_pipeline.py:130` (top 3 after reranking)

### Adding New Data

1. Update `data/datasets/company_qa.csv` with new Q&A pairs
2. Regenerate vector store:
   ```bash
   rm -rf data/vectorstore
   python scripts/create_vectorstore.py
   ```
3. Restart application

### Security Considerations

- Input validation in `utils/rag_pipeline.py:26-48` prevents XSS/injection attacks
- Rate limiting enabled in production (`utils/rate_limiter.py`)
- Optional authentication via `AUTH_ENABLED` environment variable
- Dangerous patterns blocked: `<script`, `javascript:`, `onerror=`, `onclick=`

### Debugging Tips

**Ollama Connection Issues:**
- Verify Ollama is running: `ollama serve`
- Check model availability: `ollama list`
- Test connection: `curl http://localhost:11434/api/tags`

**Vector Store Issues:**
- Ensure `data/vectorstore/` directory exists after running `create_vectorstore.py`
- Check path in logs during app startup
- Regenerate if corrupted: `rm -rf data/vectorstore && python scripts/create_vectorstore.py`

**BGE-M3 Model Download:**
- First run downloads ~2GB from HuggingFace
- Pre-loading in `chainlit_app.py:46-53` speeds up subsequent startups
- Check internet connection if download fails

**Performance:**
- 3B models respond in ~2 seconds on average
- Increase retrieval k or disable reranking for faster responses (lower quality)
- Monitor logs in `chatbot.log` for timing information

## Project Context

- **Team**: 염재준 (Developer), 조민양 교수 (Advisor), 김인태 선임 (Industry Mentor, 퓨쳐시스템)
- **Period**: 2025.08.30 ~ 2025.11.28 (120 hours)
- **Institution**: 동서울대학교 AI융합소프트웨어학과
- **Partner**: ㈜퓨쳐시스템 (network security company)
- **Dataset**: 83 Q&A pairs, 10 categories covering company info
