# 퓨쳐시스템 AI 챗봇 (2025 최신 기술 스택)

퓨쳐시스템 정보 기반 RAG 자동 응답 시스템

## 프로젝트 개요

- **프로젝트명**: Ollama 기반 회사 소개 ChatBot 개발
- **기간**: 2025.08.30 ~ 2025.11.28 (120시간)
- **소속**: 동서울대학교 AI융합소프트웨어학과
- **협력기업**: ㈜퓨쳐시스템

## 기술 스택 (2025 최신)

### Core Framework
- **Python** 3.10+
- **Streamlit** 1.41.1 (웹 UI)
- **Ollama** 0.9+ (LLM)
- **LangChain** 0.3.13 (RAG 프레임워크)

### Vector Store & Embeddings
- **ChromaDB** 0.5.23 (벡터 데이터베이스)
- **BGE-M3** (BAAI/bge-m3) - 한국어 SOTA 임베딩 모델 (KLUE 79.3점)
- **FlashRank** 0.2.9 (무료 Reranking)

### Data Processing
- **Sentence Transformers** 3.3.1
- **pypdf** 5.1.0
- **pandas** 2.2.3

## 주요 기능

- 퓨쳐시스템 회사 정보 + 개발자 정보 기반 질의응답 (83개 Q&A)
- RAG (Retrieval Augmented Generation) 시스템
- FlashRank를 이용한 검색 결과 재순위화
- 실시간 스트리밍 응답
- 대화 이력 관리
- ChromaDB 벡터 검색

## 프로젝트 구조

```
ollama-company-chatbot/
├── app.py                      # Streamlit 메인 앱 (스트리밍 지원)
├── requirements.txt            # Python 패키지 (2025 최신)
├── run.sh                     # 실행 스크립트
├── utils/                     # 유틸리티
│   └── rag_pipeline.py        # RAG 파이프라인 (ChromaDB + BGE-M3 + FlashRank)
├── data/                      # 데이터
│   ├── raw/                   # 원본 데이터
│   │   └── company_info.txt   # 퓨쳐시스템 회사 정보
│   ├── datasets/              # 데이터셋
│   │   └── company_qa.csv     # 83개 Q&A 데이터
│   └── vectorstore/           # ChromaDB 벡터 스토어
├── docs/                      # 문서
│   └── capstone_poster_final.html  # 캡스톤 전시 판넬
└── scripts/                   # 스크립트
    └── create_vectorstore.py  # 벡터 스토어 생성
```

## 설치 및 실행

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. Ollama 설치 및 모델 다운로드

```bash
# Ollama 설치 (Linux/Mac)
curl -fsSL https://ollama.com/install.sh | sh

# Windows: https://ollama.com/download 에서 다운로드

# 모델 다운로드 (llama3.2 3B 권장)
ollama pull llama3.2:3b

# Ollama 서버 실행 (백그라운드)
ollama serve
```

### 3. 벡터 스토어 생성

```bash
# ChromaDB 벡터 스토어 생성 (최초 1회)
python scripts/create_vectorstore.py
```

출력 예시:
```
============================================================
ChromaDB 벡터 스토어 생성 시작
============================================================
1. BGE-M3 임베딩 모델 로드 중...
✓ 임베딩 모델 로드 완료
2. CSV 데이터 로드 중...
✓ 문서 로드 완료: 83개
3. 문서 변환 중...
✓ 문서 변환 완료: 83개
4. 텍스트 분할 설정...
✓ 문서 분할 완료: 83개 청크
5. ChromaDB 벡터 스토어 생성 중...
✓ 벡터 스토어 생성 완료: /path/to/data/vectorstore
============================================================
```

### 4. 애플리케이션 실행

```bash
# Streamlit 앱 실행
streamlit run app.py

# 또는 실행 스크립트 사용
chmod +x run.sh
./run.sh
```

브라우저에서 `http://localhost:8501` 접속

### 5. ngrok으로 외부 공개 (선택사항)

```bash
# ngrok 설치 후
ngrok http 8501
```

## 사용 방법

1. Ollama 서버가 실행 중인지 확인 (`ollama serve`)
2. Streamlit 앱 실행 (`streamlit run app.py`)
3. 브라우저에서 챗봇 인터페이스 접속
4. 사이드바에서 모델 및 설정 조정
   - LLM 모델 선택 (llama3.2:3b, mistral:7b, gemma:7b)
   - Temperature 조정 (0.0 ~ 1.0)
   - Reranking 사용 여부 설정
5. 퓨쳐시스템에 대한 질문 입력

### 예시 질문

- "퓨쳐시스템은 언제 설립되었나요?"
- "네트워크 보안 솔루션에는 어떤 것들이 있나요?"
- "클라우드 보안 서비스는 무엇인가요?"
- "본사 주소를 알려주세요"
- "SSL VPN은 무엇인가요?"

## 기술 스택 개선 내역

### 이전 버전 → 2025 최신 버전

| 구분 | 이전 | 현재 | 개선 사항 |
|------|------|------|-----------|
| Vector DB | FAISS | ChromaDB 0.5.23 | 메타데이터 필터링, 관리 편의성 |
| Embeddings | ko-sroberta (KLUE 72.5) | BGE-M3 (KLUE 79.3) | 한국어 성능 7점 향상 |
| Reranking | 없음 | FlashRank (무료) | 검색 정확도 향상 |
| 응답 방식 | 일괄 생성 | 스트리밍 | 실시간 응답 UX 개선 |
| LangChain | 레거시 | 0.3 LCEL | 최신 체인 구성 방식 |
| PDF Parser | PyPDF2 | pypdf 5.1.0 | 최신 PDF 파싱 |

## 성능 지표

- **검색 정확도**: BGE-M3 임베딩으로 79.3% (KLUE 벤치마크)
- **응답 속도**: 평균 2초 이내 (3B 모델 기준)
- **데이터셋**: 83개 Q&A, 10개 카테고리
- **Reranking**: 10개 검색 → 3개로 재순위화

## 개발 진행 상황

- [x] Phase 1: 데이터 수집 및 전처리 (퓨쳐시스템 웹 크롤링)
- [x] Phase 2: 데이터셋 구축 (83개 Q&A, 10개 카테고리)
- [x] Phase 3: RAG 파이프라인 (ChromaDB + BGE-M3 + FlashRank)
- [x] Phase 4: Streamlit 앱 구현 (스트리밍 지원)
- [x] Phase 5: 벡터 스토어 생성 스크립트
- [ ] Phase 6: 배포 및 모니터링

## 문제 해결

### Ollama 연결 오류
```bash
# Ollama 서버가 실행 중인지 확인
ollama serve

# 다른 터미널에서 모델 확인
ollama list
```

### ChromaDB 오류
```bash
# 벡터 스토어 재생성
rm -rf data/vectorstore
python scripts/create_vectorstore.py
```

### BGE-M3 모델 다운로드 느림
- 최초 실행 시 HuggingFace에서 모델 다운로드 (약 2GB)
- 인터넷 연결 확인 및 대기

## 팀

- **염재준** (개발)
- **조민양 교수** (지도교수)
- **김인태 선임** (현장교사, 퓨쳐시스템)

## 라이선스

Educational purposes (Capstone Design Project)

---

**Powered by ChromaDB + BGE-M3 + FlashRank + Ollama**
