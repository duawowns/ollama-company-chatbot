# Ollama Company Chatbot

퓨쳐시스템 정보 기반 자동 응답 시스템

## 프로젝트 개요

- **프로젝트명**: Ollama 기반 회사 소개 ChatBot 개발
- **기간**: 2025.08.30 ~ 2025.11.28 (120시간)
- **소속**: 동서울대학교 AI융합소프트웨어학과
- **협력기업**: ㈜퓨쳐시스템

## 기술 스택

### Core
- Python 3.14+
- Streamlit (웹 UI)
- Ollama 0.9+ (LLM)
- LangChain (RAG 프레임워크)

### Data & ML
- Hugging Face Datasets
- FAISS Vector Store
- Sentence Transformers

### Deployment
- ngrok (터널링)
- Docker (선택사항)

## 주요 기능

- 회사 정보 기반 질의응답
- RAG(Retrieval Augmented Generation) 시스템
- 실시간 채팅 인터페이스
- 대화 이력 관리

## 프로젝트 구조

```
ollama-company-chatbot/
├── app.py                # Streamlit 메인 앱
├── requirements.txt      # Python 패키지
├── run.sh               # 실행 스크립트
├── utils/               # 유틸리티 함수
│   ├── rag_pipeline.py  # RAG 파이프라인
│   └── data_loader.py   # 데이터 로더
├── config/              # 설정 파일
├── data/                # 데이터셋
│   ├── raw/             # 원본 CSV, PDF
│   ├── processed/       # 전처리 데이터
│   └── vectorstore/     # FAISS 인덱스
├── docs/                # 문서
└── scripts/             # 학습 및 전처리 스크립트
    └── train_embedding.py
```

## 설치 및 실행

### 1. 환경 설정

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Ollama 설치 및 모델 다운로드

```bash
# Ollama 설치
curl -fsSL https://ollama.com/install.sh | sh

# 모델 다운로드
ollama pull llama3.2:3b
```

### 3. 애플리케이션 실행

```bash
# Streamlit 앱 실행
streamlit run app.py

# 또는 실행 스크립트 사용
./run.sh
```

### 4. ngrok으로 외부 공개 (선택사항)

```bash
# ngrok 설치 후
ngrok http 8501
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
