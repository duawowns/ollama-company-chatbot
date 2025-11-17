#!/bin/bash

# 퓨쳐시스템 챗봇 실행 스크립트

echo "==================================="
echo "퓨쳐시스템 챗봇 시작"
echo "==================================="

# 가상환경 활성화 (있는 경우)
if [ -d "venv" ]; then
    echo "가상환경 활성화..."
    source venv/bin/activate
fi

# Ollama 실행 확인
if ! command -v ollama &> /dev/null; then
    echo "⚠️  Ollama가 설치되어 있지 않습니다."
    echo "설치 방법: curl -fsSL https://ollama.com/install.sh | sh"
    exit 1
fi

# Streamlit 앱 실행
echo "Streamlit 앱 실행..."
streamlit run app.py --server.port 8501

echo "==================================="
echo "챗봇 종료"
echo "==================================="
