---
title: 퓨쳐시스템 AI 챗봇
emoji: 🤖
colorFrom: blue
colorTo: cyan
sdk: docker
app_port: 8501
pinned: false
tags:
  - chatbot
  - rag
  - korean
  - chainlit
  - groq
---

# 퓨쳐시스템 회사소개 AI 챗봇

RAG 기반 회사 정보 챗봇 - ChromaDB + 다국어 임베딩 + Groq API

## 기술 스택

- **UI Framework:** Chainlit 2.9.0
- **LLM:** Groq API (llama-3.1-8b-instant)
- **Embeddings:** distiluse-base-multilingual-cased-v2
- **Vector DB:** ChromaDB
- **Framework:** LangChain 0.3+

## 환경 변수

Hugging Face Spaces Settings에서 다음 환경 변수를 설정하세요:

- `GROQ_API_KEY`: Groq API 키 (필수)
- `LOG_LEVEL`: 로그 레벨 (기본: INFO)
- `RATE_LIMIT_PER_MINUTE`: 분당 요청 제한 (기본: 30)
- `RATE_LIMIT_PER_HOUR`: 시간당 요청 제한 (기본: 100)

## 배포 방법

1. Hugging Face에 로그인
2. New Space 생성 (SDK: Docker)
3. GitHub 연동 또는 파일 업로드
4. 환경 변수 설정 (GROQ_API_KEY)
5. 자동 빌드 및 배포 완료!

## 프로젝트 정보

- **개발자:** 염재준 (동서울대학교 AI융합소프트웨어학과)
- **지도교수:** 조민양 교수
- **산업 멘토:** 김인태 선임 (㈜퓨쳐시스템)
- **기간:** 2025.08.30 ~ 2025.11.28

## 라이선스

MIT License
