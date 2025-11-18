# Railway 배포용 통합 Dockerfile (Ollama + Chatbot)

FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (Ollama 설치 위해 필요)
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Ollama 설치
RUN curl -fsSL https://ollama.com/install.sh | sh

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Data 디렉토리 복사 (vectorstore 포함)
COPY data/ /app/data/

# 애플리케이션 코드 복사
COPY . .

# Startup script 실행 권한 부여
RUN chmod +x start_railway.sh

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_BASE_URL=http://localhost:11434
ENV LOG_LEVEL=INFO
ENV AUTH_ENABLED=false
ENV RATE_LIMIT_PER_MINUTE=30
ENV RATE_LIMIT_PER_HOUR=100
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/transformers
ENV OLLAMA_HOST=0.0.0.0

# 캐시 및 로그 디렉토리 생성
RUN mkdir -p /app/logs /app/.cache/huggingface /app/.cache/transformers /root/.ollama

# 포트 노출
EXPOSE 8501

# Startup script 실행 (Ollama + Chainlit)
CMD ["./start_railway.sh"]
