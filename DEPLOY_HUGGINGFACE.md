# Hugging Face Spaces 배포 가이드

## 사전 준비

1. **Hugging Face 계정 생성**
   - https://huggingface.co/join 에서 가입
   - 이메일 인증 완료

2. **Groq API 키 준비**
   - https://console.groq.com/keys 에서 발급
   - 무료 티어 사용 가능

## 배포 단계 (5분)

### 1. New Space 생성

1. https://huggingface.co/new-space 접속
2. 다음 정보 입력:
   - **Space name:** `futuresystem-chatbot` (원하는 이름)
   - **License:** MIT
   - **Select SDK:** Docker
   - **Hardware:** CPU basic (FREE) - 16GB RAM
   - **Visibility:** Public 또는 Private

3. **Create Space** 클릭

### 2. 파일 업로드

**방법 A: GitHub 연동 (추천)**

```bash
# 현재 프로젝트 디렉토리에서
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/futuresystem-chatbot
git push hf main
```

**방법 B: 웹 UI 직접 업로드**

Space의 "Files" 탭에서 다음 파일들 업로드:
- `README_HF.md` → `README.md`로 이름 변경
- `Dockerfile.hf` → `Dockerfile`로 이름 변경
- `chainlit_app.py`
- `requirements.txt`
- `utils/` 폴더 전체
- `data/` 폴더 전체
- `.chainlit/` 폴더 전체

### 3. 환경 변수 설정

1. Space 설정 페이지로 이동 (Settings 탭)
2. **Repository secrets** 섹션에서 추가:

```
GROQ_API_KEY = your_groq_api_key_here
```

3. (선택) 추가 환경 변수:
```
LOG_LEVEL = INFO
RATE_LIMIT_PER_MINUTE = 30
RATE_LIMIT_PER_HOUR = 100
```

### 4. 빌드 확인

1. Space 페이지에서 "Building" 상태 확인
2. 빌드 로그 확인 (약 5-10분 소요):
   - 모델 다운로드 중...
   - Docker 이미지 빌드...
   - Running on http://0.0.0.0:8501

3. 빌드 완료 후 "Running" 상태로 변경

### 5. 테스트

1. Space URL 접속: `https://huggingface.co/spaces/YOUR_USERNAME/futuresystem-chatbot`
2. 챗봇 인터페이스 로드 확인
3. 테스트 질문: "회사 주소 어디야?"
4. 정확한 답변 확인:
   - "서울특별시 구로구 디지털로26길 61..."

## 파일 구조 (Spaces용)

```
your-space/
├── README.md              # README_HF.md를 복사
├── Dockerfile             # Dockerfile.hf를 복사
├── requirements.txt
├── chainlit_app.py
├── .chainlit/
│   └── config.toml
├── utils/
│   ├── rag_pipeline.py
│   ├── rate_limiter.py
│   ├── auth.py
│   └── health.py
└── data/
    ├── datasets/
    │   └── company_qa.csv
    └── vectorstore/
        └── [ChromaDB files]
```

## 트러블슈팅

### 빌드 실패 시

1. **GROQ_API_KEY 확인**
   - Settings > Repository secrets 확인
   - 키 값이 정확한지 확인

2. **메모리 부족**
   - Hardware: CPU basic (16GB) 선택 확인
   - CPU basic은 무료입니다!

3. **모델 다운로드 실패**
   - 빌드 로그 확인
   - 재빌드 시도 (Settings > Restart Space)

### Sleep 모드

- 일정 시간 미사용 시 자동 Sleep
- 다음 접속 시 자동으로 Wake up
- 무료 티어 정상 동작

## 성능 최적화

### CPU vs GPU

- ✅ **CPU basic (FREE):** 16GB RAM, 충분한 성능
- ❌ **GPU T4 ($0.40/시간):** 불필요, 비용 발생

→ **CPU basic만 사용하세요!**

### 메모리 사용량

- Base: ~300MB
- Embeddings: ~250MB
- ChromaDB: ~50MB
- **총 ~600MB** (16GB 중 3.75%)

## 커스터마이징

### 1. 회사 정보 변경

`data/datasets/company_qa.csv` 수정 후:

```bash
python scripts/create_vectorstore.py
git add data/vectorstore
git push hf main
```

### 2. UI 테마 변경

`.chainlit/config.toml` 수정

### 3. Rate Limit 조정

Environment variables에서 설정

## 모니터링

Space 대시보드에서 확인:
- 실시간 사용자 수
- 리소스 사용량
- 에러 로그

## 비용

- **CPU basic:** 완전 무료 ✅
- **Storage:** 무료 (50GB)
- **Bandwidth:** 무료

→ **총 비용: $0/월** 🎉

## 문의

- Hugging Face 포럼: https://discuss.huggingface.co/
- 프로젝트 이슈: GitHub Issues

---

**축하합니다! 이제 16GB RAM에서 다국어 모델을 무료로 사용할 수 있습니다!** 🚀
