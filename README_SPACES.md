---
title: 퓨쳐시스템 AI 챗봇
emoji: 🤖
colorFrom: blue
colorTo: cyan
sdk: docker
pinned: false
license: mit
app_port: 8501
---

# 퓨쳐시스템 AI 챗봇

퓨쳐시스템 회사 소개 자동 응답 챗봇입니다. RAG 방식으로 회사 정보를 검색해서 답변합니다.

## 프로젝트 정보

- **프로젝트명**: Ollama 기반 회사 소개 ChatBot 개발
- **기간**: 2025.08.30 ~ 2025.11.28 (120시간)
- **소속**: 동서울대학교 AI융합소프트웨어학과
- **협력기업**: ㈜퓨쳐시스템

## 기술 스택

### 주요 프레임워크
- Python 3.10+
- Chainlit 2.9.0 (챗봇 UI)
- HuggingFace Inference API (LLM - GPU)
- LangChain 0.3.13

### 벡터 검색
- ChromaDB 0.5.23 - 벡터DB
- BGE-M3 - 한국어 임베딩 모델
- FlashRank 0.2.9 - 검색 결과 재정렬

### 데이터 처리
- Sentence Transformers
- pandas

## 주요 기능

- 퓨쳐시스템 정보 질의응답 (83개 Q&A 데이터셋)
- RAG 기반 검색 및 응답
- FlashRank로 검색 결과 개선
- 스트리밍 방식 응답
- 대화 이력 관리
- GPU 가속 (HuggingFace Inference API)

## 예시 질문

- "퓨쳐시스템은 언제 설립되었나요?"
- "네트워크 보안 솔루션 어떤 거 있어요?"
- "클라우드 보안 서비스는 뭔가요?"
- "본사 주소 알려주세요"
- "SSL VPN이 뭐예요?"

## 성능

- BGE-M3 임베딩 사용
- GPU 가속으로 빠른 응답 속도
- 데이터셋: 83개 Q&A, 10개 카테고리
- Reranking: 검색 10개 → 상위 3개만 사용

## 팀

- 염재준 (개발)
- 조민양 교수 (지도교수)
- 김인태 선임 (현장교사, 퓨쳐시스템)

## 라이선스

Educational purposes (캡스톤 디자인 프로젝트)
