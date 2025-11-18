#!/bin/bash
# Railway 배포용 시작 스크립트
# Ollama 서버와 Chainlit을 동시에 실행

set -e  # 에러 발생 시 종료

echo "========================================="
echo "Starting Ollama + Chatbot on Railway"
echo "========================================="

# Ollama 서버 백그라운드 실행
echo "[1/4] Starting Ollama server..."
ollama serve &
OLLAMA_PID=$!

# Ollama 서버 준비 대기 (최대 60초)
echo "[2/4] Waiting for Ollama server to be ready..."
for i in {1..60}; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✅ Ollama server is ready!"
        break
    fi
    echo "Waiting for Ollama... ($i/60)"
    sleep 1
done

# Ollama가 준비되었는지 확인
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama server failed to start"
    exit 1
fi

# 모델 다운로드 (이미 있으면 스킵)
echo "[3/4] Checking if model llama3.2:3b exists..."
if ! ollama list | grep -q "llama3.2:3b"; then
    echo "Downloading llama3.2:3b model (this may take 5-10 minutes)..."
    ollama pull llama3.2:3b
else
    echo "✅ Model llama3.2:3b already exists"
fi

# Chainlit 앱 실행 (포그라운드)
echo "[4/4] Starting Chainlit app..."
echo "========================================="
exec chainlit run chainlit_app.py --host 0.0.0.0 --port 8501 --headless
