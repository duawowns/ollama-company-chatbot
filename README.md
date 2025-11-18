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
- Chainlit 2.9.0 (메인 UI - 챗봇용으로 만들어서 이게 더 나음)
- Streamlit 1.41.1 (초기 버전, 참고용)
- Ollama (LLM 서버)
- LangChain 0.3.13

### 벡터 검색
- ChromaDB 0.5.23 - 벡터DB
- BGE-M3 - 한국어 임베딩 모델 (기존 ko-sroberta보다 성능 좋음)
- FlashRank 0.2.9 - 검색 결과 재정렬

### 데이터 처리
- Sentence Transformers
- pypdf
- pandas

## 주요 기능

- 퓨쳐시스템 정보 질의응답 (83개 Q&A 데이터셋)
- RAG 기반 검색 및 응답
- FlashRank로 검색 결과 개선
- 스트리밍 방식 응답 (답변이 실시간으로 나옴)
- 대화 이력 관리
- ChromaDB 벡터 검색

## 프로젝트 구조

```
ollama-company-chatbot/
├── chainlit_app.py             # Chainlit 메인 (이거 쓰세요)
├── app.py                      # Streamlit 버전 (초기 버전)
├── run_chainlit.sh             # Chainlit 실행 스크립트
├── run.sh                      # Streamlit 실행 스크립트
├── requirements.txt
├── .chainlit/
│   └── config.toml             # UI 색상 설정
├── utils/
│   └── rag_pipeline.py         # RAG 파이프라인
├── data/
│   ├── raw/
│   │   └── company_info.txt    # 원본 회사 정보
│   ├── datasets/
│   │   └── company_qa.csv      # 83개 Q&A
│   └── vectorstore/            # ChromaDB 저장소
├── docs/
│   └── capstone_poster_final.html
└── scripts/
    └── create_vectorstore.py   # 벡터DB 생성 스크립트
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

### 2. Ollama 설치

```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Windows는 https://ollama.com/download 에서 다운로드

# 모델 다운로드 (llama3.2 3B 권장 - 가볍고 빠름)
ollama pull llama3.2:3b

# Ollama 서버 실행
ollama serve
```

### 3. 벡터 스토어 생성

```bash
# 처음 한 번만 실행하면 됨
python scripts/create_vectorstore.py
```

실행하면 이런 로그가 나옴:
```
============================================================
ChromaDB 벡터 스토어 생성 시작
============================================================
1. BGE-M3 임베딩 모델 로드 중...
✓ 임베딩 모델 로드 완료
2. CSV 데이터 로드 중...
✓ 문서 로드 완료: 83개
...
```

### 4. 앱 실행

**Chainlit 버전** (추천)

```bash
# 앱 실행
chainlit run chainlit_app.py -w --port 8501

# 또는
chmod +x run_chainlit.sh
./run_chainlit.sh
```

브라우저에서 `http://localhost:8501` 접속

**Streamlit 버전**

```bash
streamlit run app.py

# 또는
chmod +x run.sh
./run.sh
```

### 5. 외부 공개 (필요하면)

```bash
# ngrok 설치 후
ngrok http 8501
```

## 사용법

### Chainlit 버전

1. Ollama 서버 켜기 (`ollama serve`)
2. Chainlit 앱 실행
3. 브라우저에서 접속
4. 질문 입력하면 됨

특징:
- 챗봇 전용 UI라 깔끔함
- 실시간 스트리밍 응답
- 포스터 색상 테마 적용 (네이비 블루 + 시안)

### Streamlit 버전

1. Ollama 서버 켜기
2. Streamlit 앱 실행
3. 사이드바에서 설정 조정 가능
   - 모델 선택 (llama3.1:8b, llama3.2:3b, mistral:7b, gemma:7b)
   - Temperature 조정
   - Reranking 켜기/끄기
4. 질문 입력

### 예시 질문

- "퓨쳐시스템은 언제 설립되었나요?"
- "네트워크 보안 솔루션 어떤 거 있어요?"
- "클라우드 보안 서비스는 뭔가요?"
- "본사 주소 알려주세요"
- "SSL VPN이 뭐예요?"

## 개선 내역

이전에 FAISS랑 ko-sroberta 쓰다가 성능 향상 위해 교체했습니다.

| 항목 | 이전 | 현재 | 비고 |
|------|------|------|------|
| Vector DB | FAISS | ChromaDB | 관리하기 편함 |
| Embeddings | ko-sroberta | BGE-M3 | 한국어 성능 더 좋음 |
| Reranking | 없음 | FlashRank | 검색 정확도 올라감 |
| 응답 | 일괄 | 스트리밍 | UX 개선 |
| LangChain | 구버전 | 0.3 LCEL | 최신 방식으로 |

## 성능

- BGE-M3 임베딩 사용 (KLUE 벤치마크 79.3점)
- 평균 응답 속도 2초 정도 (3B 모델 기준)
- 데이터셋: 83개 Q&A, 10개 카테고리
- Reranking: 검색 10개 → 상위 3개만 사용

## 개발 진행

- [x] 데이터 수집 (퓨쳐시스템 웹 크롤링)
- [x] 데이터셋 구축 (83개 Q&A)
- [x] RAG 파이프라인 구현
- [x] Streamlit 앱
- [x] Chainlit 앱
- [x] 벡터 스토어 생성 스크립트
- [ ] 배포

## 트러블슈팅

### Ollama 연결 안 됨
```bash
# Ollama 서버 켜졌는지 확인
ollama serve

# 모델 확인
ollama list
```

### ChromaDB 에러
```bash
# 벡터 스토어 다시 만들기
rm -rf data/vectorstore
python scripts/create_vectorstore.py
```

### BGE-M3 다운로드 느림
- 처음 실행할 때 HuggingFace에서 모델 다운로드 (약 2GB)
- 인터넷 느리면 시간 좀 걸림

## 팀

- 염재준 (개발)
- 조민양 교수 (지도교수)
- 김인태 선임 (현장교사, 퓨쳐시스템)

## 라이선스

Educational purposes (캡스톤 디자인 프로젝트)
