#!/bin/bash

# 외부 발표용 빠른 배포 스크립트
# Quick deployment script for external presentation

set -e

echo "🚀 퓨쳐시스템 챗봇 배포 시작..."
echo ""

# Docker 확인
if ! command -v docker &> /dev/null; then
    echo "❌ Docker가 설치되지 않았습니다."
    echo "   https://docs.docker.com/get-docker/ 에서 설치하세요."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose가 설치되지 않았습니다."
    echo "   https://docs.docker.com/compose/install/ 에서 설치하세요."
    exit 1
fi

echo "✅ Docker 설치 확인 완료"
echo ""

# .env 파일 생성 (없으면)
if [ ! -f .env ]; then
    echo "📝 .env 파일 생성 중..."
    cp .env.example .env
    echo "✅ .env 파일 생성 완료"
else
    echo "✅ .env 파일 이미 존재"
fi

echo ""
echo "🏗️  Docker 이미지 빌드 중..."
docker-compose build

echo ""
echo "🚀 서비스 시작 중..."
docker-compose up -d

echo ""
echo "⏳ 서비스 초기화 대기 중 (30초)..."
sleep 30

echo ""
echo "🔍 서비스 상태 확인..."
docker-compose ps

echo ""
echo "✅ 배포 완료!"
echo ""
echo "📊 접속 정보:"
echo "   - Chainlit UI: http://localhost:8501"
echo "   - Ollama API: http://localhost:11434"
echo ""
echo "📝 로그 확인:"
echo "   docker-compose logs -f chatbot"
echo ""
echo "🛑 서비스 중지:"
echo "   docker-compose down"
echo ""
echo "💡 외부 공개 (ngrok 사용):"
echo "   ngrok http 8501"
echo ""
