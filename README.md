# Ollama Company Chatbot

퓨쳐시스템 정보 기반 자동 응답 시스템

## 프로젝트 개요

- **프로젝트명**: Ollama 기반 회사 소개 ChatBot 개발
- **기간**: 2025.08.30 ~ 2025.11.28 (120시간)
- **소속**: 동서울대학교 AI융합소프트웨어학과
- **협력기업**: ㈜퓨쳐시스템

## 기술 스택

### Backend
- Python 3.14+
- FastAPI 0.121+
- Ollama 0.9+
- LangChain, RAG

### Frontend
- Next.js 16
- React

### Data
- Hugging Face Datasets
- FAISS Vector Store

### Deployment
- Docker

## 주요 기능

- 회사 정보 기반 질의응답
- RAG(Retrieval Augmented Generation) 시스템
- 실시간 채팅 인터페이스
- 대화 이력 관리

## 프로젝트 구조

```
ollama-company-chatbot/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Configuration
│   │   ├── models/       # Data models
│   │   └── services/     # Business logic
│   └── tests/
├── frontend/
├── data/
│   ├── raw/
│   ├── processed/
│   └── datasets/
├── docs/
└── scripts/
```

## 설치 및 실행

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 개발 진행 상황

- [ ] Phase 1: 데이터 수집 및 전처리
- [ ] Phase 2: 데이터셋 구축
- [ ] Phase 3: LLM 학습 및 RAG 파이프라인
- [ ] Phase 4: FastAPI 서버 구현
- [ ] Phase 5: Next.js 프론트엔드 구현

## 팀

- 염재준 (개발)
- 조민양 교수 (지도교수)
- 김인태 선임 (현장교사)

## License

Educational purposes (Capstone Design Project)
