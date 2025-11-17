# 프로덕션 최적화 Dockerfile (Multi-stage build)

# Stage 1: Builder
FROM python:3.12-slim as builder

WORKDIR /app

# 시스템 의존성 설치 (빌드용)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 설치
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Stage 2: Runtime
FROM python:3.12-slim

# 비root 사용자 생성
RUN groupadd -r chatbot && useradd -r -g chatbot chatbot

# 작업 디렉토리 설정
WORKDIR /app

# 런타임 의존성만 설치
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Builder stage에서 wheel 복사
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Python 패키지 설치
RUN pip install --no-cache /wheels/*

# 애플리케이션 코드 복사
COPY --chown=chatbot:chatbot . .

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_BASE_URL=http://ollama:11434
ENV LOG_LEVEL=INFO
ENV AUTH_ENABLED=false
ENV RATE_LIMIT_PER_MINUTE=30
ENV RATE_LIMIT_PER_HOUR=100

# 로그 디렉토리 생성
RUN mkdir -p /app/logs && chown -R chatbot:chatbot /app/logs

# 비root 사용자로 전환
USER chatbot

# 포트 노출
EXPOSE 8501

# 헬스체크 (개선된 버전)
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8501/ || exit 1

# Chainlit 실행 (프로덕션 모드)
CMD ["chainlit", "run", "chainlit_app.py", "--host", "0.0.0.0", "--port", "8501", "--headless"]
