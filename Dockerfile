# 경량 프로덕션 Dockerfile (Groq API 사용)

FROM python:3.12-slim

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

# 모델 사전 다운로드 (빌드 시 캐싱) - 첫 시작 타임아웃 방지
ENV HF_HOME=/app/.cache/huggingface
ENV TRANSFORMERS_CACHE=/app/.cache/transformers
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')"

# Data 디렉토리 먼저 복사 (vectorstore 포함)
COPY data/ /app/data/

# 애플리케이션 코드 복사
COPY . .

# 환경변수 설정
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=INFO
ENV AUTH_ENABLED=false
ENV RATE_LIMIT_PER_MINUTE=30
ENV RATE_LIMIT_PER_HOUR=100
ENV PORT=10000

# 캐시 및 로그 디렉토리 생성
RUN mkdir -p /app/logs /app/.cache/huggingface /app/.cache/transformers

# 포트 노출 (Render 기본 포트)
EXPOSE 10000

# 시작 스크립트 (Render PORT 환경변수 사용)
CMD chainlit run chainlit_app.py --host 0.0.0.0 --port ${PORT:-10000} --headless
