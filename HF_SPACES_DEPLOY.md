# Hugging Face Spaces 배포 가이드

Hugging Face Spaces에 무료 GPU로 챗봇을 배포하는 방법입니다.

---

## Hugging Face Spaces란?

- 무료 GPU (T4) 제공
- 공개 URL 자동 생성
- Git push로 자동 배포
- Chainlit, Gradio, Streamlit 지원

---

## 배포 방법

### 1. Hugging Face 계정 생성

1. https://huggingface.co 접속
2. 회원가입 (무료)
3. 이메일 인증 완료

### 2. Access Token 생성

1. Settings > Access Tokens 이동
2. **New token** 클릭
3. 이름: `chatbot-inference` (원하는 이름)
4. Type: **Read** 선택 (Inference API 사용)
5. 토큰 복사 (나중에 사용)

### 3. Space 생성

1. https://huggingface.co/new-space 접속
2. 설정:
   - **Owner**: 본인 계정
   - **Space name**: `futuresystem-chatbot` (원하는 이름)
   - **License**: MIT
   - **Select the Space SDK**: **Docker** 선택
   - **Space hardware**: **CPU basic** (무료) → 나중에 GPU로 변경 가능
3. **Create Space** 클릭

### 4. 파일 업로드

Space가 생성되면 **Files** 탭에서 파일 업로드:

#### 필수 파일 목록:

1. **README.md**
   - 프로젝트 루트의 `README_SPACES.md` 파일을 `README.md`로 복사
   ```bash
   cp README_SPACES.md README.md
   ```

2. **Dockerfile**
   - `Dockerfile.spaces`를 `Dockerfile`로 복사
   ```bash
   cp Dockerfile.spaces Dockerfile
   ```

3. **나머지 파일들**:
   - `chainlit_app.py`
   - `requirements.txt`
   - `utils/` (전체 디렉토리)
   - `data/vectorstore/` (벡터DB)
   - `.chainlit/` (설정 파일)

**Git으로 업로드하는 방법:**

```bash
# Space Git 리포지토리 클론
git clone https://huggingface.co/spaces/사용자명/futuresystem-chatbot
cd futuresystem-chatbot

# 파일 복사
cp ../ollama-company-chatbot/README_SPACES.md README.md
cp ../ollama-company-chatbot/Dockerfile.spaces Dockerfile
cp ../ollama-company-chatbot/chainlit_app.py .
cp ../ollama-company-chatbot/requirements.txt .
cp -r ../ollama-company-chatbot/utils .
cp -r ../ollama-company-chatbot/data .
cp -r ../ollama-company-chatbot/.chainlit .

# Git 커밋 및 푸시
git add .
git commit -m "Initial deployment"
git push
```

### 5. 환경 변수 설정

Space 설정에서 **Settings** > **Variables and secrets** 이동:

**필수 환경 변수:**

```bash
HUGGINGFACEHUB_API_TOKEN=hf_xxxxxxxxxxxxxxxxxx  # 2단계에서 복사한 토큰
USE_HF_INFERENCE=true
```

**선택적 환경 변수:**

```bash
LOG_LEVEL=INFO
AUTH_ENABLED=false
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=100
```

### 6. GPU 활성화 (선택)

무료 GPU (T4)로 업그레이드:

1. Space 설정 > **Settings** 이동
2. **Space hardware** 섹션
3. **T4 small** 선택 (무료)
4. **Update hardware** 클릭

GPU는 사용량 제한이 있으니 필요할 때만 활성화하세요.

### 7. 빌드 및 배포

파일을 업로드하면 자동으로 빌드 시작:

1. **Logs** 탭에서 빌드 진행 상황 확인
2. 빌드 시간: 약 5-10분 (첫 빌드)
3. 성공하면 앱이 자동으로 실행됨

---

## 접속 및 테스트

### 공개 URL

배포 완료 후 다음 URL로 접속 가능:

```
https://huggingface.co/spaces/사용자명/futuresystem-chatbot
```

### 테스트 질문

1. "퓨쳐시스템 주소는?"
2. "개발자는 누구야?"
3. "사용된 기술 스택은?"

모든 질문에 정상 응답하면 배포 성공!

---

## Railway vs HF Spaces 비교

| 항목 | Railway (CPU) | HF Spaces (GPU) |
|------|--------------|-----------------|
| LLM Backend | Ollama | HF Inference API |
| GPU | ❌ CPU만 | ✅ T4 GPU (무료) |
| 속도 | 느림 (2-5초) | 빠름 (1-2초) |
| Reranking | ❌ OFF | ✅ ON |
| 검색 문서 수 | k=3 | k=10 |
| 비용 | $5/월 | 완전 무료 |
| 공개 URL | ✅ | ✅ |

**권장 용도:**
- **Railway**: 프로덕션 배포 (항상 켜져있음)
- **HF Spaces**: 데모/발표용 (GPU, 빠른 속도)

---

## 트러블슈팅

### 1. "HUGGINGFACEHUB_API_TOKEN not found" 에러

**해결책:**
- Settings > Variables에서 토큰 확인
- 토큰 이름: `HUGGINGFACEHUB_API_TOKEN` (정확히 일치해야 함)

### 2. 빌드 실패

**해결책:**
```bash
# 로컬에서 Docker 빌드 테스트
docker build -f Dockerfile.spaces -t chatbot-spaces .

# 실행 테스트
docker run -p 8501:8501 \
  -e USE_HF_INFERENCE=true \
  -e HUGGINGFACEHUB_API_TOKEN=hf_xxx \
  chatbot-spaces
```

### 3. Cold Start 느림

- Space가 오래 사용 안 되면 슬립 모드
- 첫 접속 시 10-30초 대기
- 이후 접속은 빠름

**해결책:**
- Space 설정에서 "Always-on" 활성화 (유료)
- 또는 무료로 사용하고 Cold Start 감수

### 4. GPU 할당량 초과

무료 GPU는 사용 시간 제한 있음:

**해결책:**
- 필요할 때만 GPU 활성화
- 발표/데모 직전에 GPU로 전환
- 평소에는 CPU로 유지

---

## 로그 확인

**Space Logs:**
1. Space 페이지 > **Logs** 탭
2. Real-time 로그 확인
3. 에러 메시지 확인

---

## 배포 체크리스트

배포 전 확인:

- [ ] Hugging Face 계정 생성
- [ ] Access Token 생성 (Read 권한)
- [ ] Space 생성 (Docker SDK)
- [ ] README.md 업로드 (README_SPACES.md → README.md)
- [ ] Dockerfile 업로드 (Dockerfile.spaces → Dockerfile)
- [ ] 소스 코드 업로드
- [ ] data/vectorstore/ 업로드
- [ ] 환경 변수 설정 (HUGGINGFACEHUB_API_TOKEN)
- [ ] 빌드 성공 확인
- [ ] 앱 실행 확인
- [ ] 테스트 질문 3개 성공

---

## 배포 성공!

이제 다음을 얻었습니다:

✅ **무료 GPU 챗봇**
- T4 GPU 무료 사용
- 빠른 응답 속도

✅ **최고 품질**
- Reranking 활성화
- k=10 문서 검색
- 대화 히스토리 유지

✅ **외부 접근 가능**
- 공개 URL
- 누구나 접속 가능

✅ **자동 배포**
- Git push로 자동 업데이트
- HTTPS/SSL 자동

---

**공개 URL**: https://huggingface.co/spaces/사용자명/futuresystem-chatbot

발표 자료에 추가하세요! 🚀
