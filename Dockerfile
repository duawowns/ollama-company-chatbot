# 경량 프로덕션 Dockerfile (Railway 4GB 제한 대응)

FROM python:3.12-slim

# 비root 사용자 생성
RUN groupadd -r chatbot && useradd -r -g chatbot chatbot

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 최소화
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Python 의존성 설치 (캐시 활용)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY --chown=chatbot:chatbot . .

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV LOG_LEVEL=INFO
ENV AUTH_ENABLED=false
ENV RATE_LIMIT_PER_MINUTE=30
ENV RATE_LIMIT_PER_HOUR=100
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/transformers

# 캐시 디렉토리 생성 (모델 다운로드용)
RUN mkdir -p /app/logs /app/.cache/huggingface /app/.cache/transformers \
    && chown -R chatbot:chatbot /app

# 비root 사용자로 전환
USER chatbot

# 포트 노출
EXPOSE 8501

# 헬스체크 (모델 다운로드 시간 고려)
HEALTHCHECK --interval=30s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Chainlit 실행 (모델은 첫 실행 시 자동 다운로드)
CMD ["chainlit", "run", "chainlit_app.py", "--host", "0.0.0.0", "--port", "8501", "--headless"]
