#!/bin/bash

# 퓨쳐시스템 챗봇 (Chainlit) 실행 스크립트

echo "========================================"
echo "퓨쳐시스템 인트라넷 챗봇 (Chainlit)"
echo "========================================"
echo ""

# 가상환경 활성화
echo "1. 가상환경 활성화..."
source venv/bin/activate

# Ollama 확인
echo "2. Ollama 서버 확인..."
if pgrep -f "ollama serve" > /dev/null; then
    echo "   ✓ Ollama 서버 실행 중"
else
    echo "   ✗ Ollama 서버가 실행되지 않았습니다."
    echo "   다른 터미널에서 'ollama serve'를 실행해주세요."
    exit 1
fi

# Chainlit 실행
echo "3. Chainlit 앱 실행..."
echo ""
chainlit run chainlit_app.py -w --port 8501
