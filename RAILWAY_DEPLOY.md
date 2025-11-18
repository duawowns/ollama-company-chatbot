# Railway 배포 가이드 (수정됨)

Railway에 Ollama + Chatbot 통합 컨테이너를 배포하는 방법입니다.

---

## ⚠️ 중요: 이전 배포 문제 해결

### 문제 상황
- **에러**: "서버에 연결할 수 없습니다"
- **원인**: Railway는 **docker-compose를 지원하지 않음**
  - 기존 구조: `docker-compose.yml`로 Ollama와 Chatbot 분리
  - Railway는 `Dockerfile`만 빌드하여 Chatbot만 실행
  - Ollama 서버가 없어서 연결 실패

### 해결 방법
✅ **하나의 Dockerfile**에 Ollama + Chatbot 통합
✅ Startup script로 두 서비스 동시 실행
✅ `OLLAMA_BASE_URL`을 `localhost`로 변경

---

## 📋 변경된 파일

### 1. `Dockerfile` (통합 버전)
```dockerfile
# Ollama 설치 포함
RUN curl -fsSL https://ollama.com/install.sh | sh

# Startup script 실행
CMD ["./start_railway.sh"]
```

### 2. `start_railway.sh` (신규)
```bash
# Ollama 서버 백그라운드 실행
ollama serve &

# Ollama 준비 대기
# 모델 다운로드
ollama pull llama3.2:3b

# Chainlit 실행
exec chainlit run chainlit_app.py --host 0.0.0.0 --port 8501 --headless
```

### 3. 에러 핸들링 개선
- `utils/rag_pipeline.py`: Ollama 연결 실패 시 명확한 에러 메시지
- `chainlit_app.py`: ConnectionError 별도 처리

---

## 🚀 Railway 재배포 방법

### 1. Git에 변경사항 커밋

```bash
# 변경사항 확인
git status

# 모든 변경사항 추가
git add .

# 커밋
git commit -m "Fix: Railway 배포 문제 해결 - Ollama + Chatbot 통합"

# Railway에 푸시 (자동 배포)
git push origin main
```

### 2. Railway 자동 배포 확인

Railway는 Git push를 감지하면 **자동으로 배포**를 시작합니다.

1. Railway 대시보드: https://railway.app/dashboard
2. 프로젝트 선택
3. **Deployments** 탭에서 배포 진행 상황 확인
4. 로그에서 다음 메시지 확인:
   ```
   [1/4] Starting Ollama server...
   ✅ Ollama server is ready!
   [3/4] Downloading llama3.2:3b model...
   [4/4] Starting Chainlit app...
   ```

### 3. 배포 시간

**첫 배포:**
- **빌드**: 5-10분 (Ollama 설치, Python 패키지)
- **모델 다운로드**: 5-10분 (llama3.2:3b ~2GB, BGE-M3 ~2GB)
- **총 소요 시간**: 10-20분

**재배포:**
- **빌드**: 3-5분 (Docker 캐시 활용)
- **모델 로딩**: 1-2분 (이미 다운로드됨)
- **총 소요 시간**: 5-7분

---

## ⚙️ 환경 변수 확인

Railway 대시보드 > 프로젝트 > Settings > Variables

### 필수 환경 변수

기본값이 Dockerfile에 설정되어 있으므로 **추가 설정 불필요**:

```bash
# Dockerfile에서 자동 설정됨
OLLAMA_BASE_URL=http://localhost:11434  # ← 중요! localhost로 변경됨
LOG_LEVEL=INFO
AUTH_ENABLED=false
```

### 선택적 환경 변수 (필요 시 추가)

```bash
# Rate Limiting 조정
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=100

# 인증 활성화
AUTH_ENABLED=true
```

---

## 🎯 배포 후 테스트

### 1. 공개 URL 접속

Railway가 제공하는 URL 접속:
```
https://ollama-company-chatbot.up.railway.app/
```

### 2. 테스트 질문

챗봇에 다음 질문 입력:

1. **"퓨쳐시스템 주소는?"**
   - 예상 응답: "경기도 안산시 단원구 ..."

2. **"개발자는 누구야?"**
   - 예상 응답: "염재준 학생이..."

3. **"사용된 기술 스택은?"**
   - 예상 응답: "Python, Ollama, ChromaDB..."

### 3. 정상 응답 확인

✅ 모든 질문에 정상 응답 → **배포 성공!**

---

## 🐛 트러블슈팅

### 1. "서버에 연결할 수 없습니다" 에러 (여전히 발생 시)

**원인**: Ollama 서버가 아직 시작 중

**해결책**:
1. Railway 로그 확인:
   ```
   Railway Dashboard > Deployments > 최신 배포 > View Logs
   ```
2. 다음 메시지 확인:
   ```
   ✅ Ollama server is ready!
   ```
3. 첫 배포 시 **10-20분 대기** (모델 다운로드 시간)
4. 로그에 "Downloading llama3.2:3b" 메시지 확인

**여전히 실패 시**:
- Railway 대시보드에서 **Redeploy** 클릭
- 또는 새로운 커밋 후 다시 배포

### 2. 빌드 실패

**해결책**:
```bash
# 로컬에서 Docker 빌드 테스트
docker build -t chatbot-test .

# 빌드 성공 시 로컬 실행 테스트
docker run -p 8501:8501 chatbot-test

# 브라우저에서 http://localhost:8501 접속
```

### 3. 메모리 부족 (OOMKilled)

**원인**: Railway 무료 플랜 512MB, llama3.2:3b도 메모리 부족 가능

**해결책**:
1. **Railway Pro 플랜 업그레이드** (권장: 2GB+ 메모리)
2. 또는 더 작은 모델 사용 (하지만 품질 저하)

### 4. 로그 확인 방법

**Web UI**:
```
Railway Dashboard > Deployments > 최신 배포 > View Logs
```

**CLI** (선택):
```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 로그 확인
railway logs
```

---

## 📊 배포 상태 확인

### Railway 대시보드

1. **Metrics** 탭:
   - CPU 사용률
   - 메모리 사용량
   - 네트워크 트래픽

2. **Logs** 탭:
   - Real-time 로그
   - 에러 메시지
   - Ollama 서버 상태

### 헬스체크

```bash
# Railway URL로 헬스체크
curl https://ollama-company-chatbot.up.railway.app/

# 200 OK 응답 확인
```

---

## 🔒 보안 강화 (선택)

### 인증 활성화

Railway 대시보드 > Variables 추가:

```bash
AUTH_ENABLED=true
```

재배포 후 로그인 화면 표시됨 (현재 인증 코드는 `utils/auth.py` 참조)

### Rate Limiting 조정

트래픽에 따라 환경 변수 조정:

```bash
# 공개 데모 (엄격)
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=30

# 사내 사용 (관대)
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=200
```

---

## 💰 비용 (Railway)

### 무료 플랜
- 초기 $5 무료 크레딧
- 512MB RAM
- 월 500시간 실행 가능

### Pro 플랜 (권장)
- 8GB RAM
- 더 큰 모델 사용 가능 (llama3.1:8b)
- $20/월

### 예상 비용
- **소형 프로젝트**: $5-10/월
- **중형 프로젝트**: $15-20/월

---

## 📂 파일 구조

```
ollama-company-chatbot/
├── Dockerfile              # Railway용 통합 Dockerfile (Ollama + Chatbot)
├── Dockerfile.local        # 로컬 개발용 (백업)
├── start_railway.sh        # Ollama + Chainlit 시작 스크립트
├── docker-compose.yml      # 로컬 개발용 (Railway는 무시)
├── chainlit_app.py         # Chainlit 앱
├── utils/
│   └── rag_pipeline.py     # RAG 파이프라인 (Ollama 연결)
└── RAILWAY_DEPLOY.md       # 이 파일
```

---

## ⚡ 로컬 개발 vs Railway 배포

### 로컬 개발
```bash
# docker-compose 사용 (Ollama + Chatbot 분리)
docker-compose up -d
```

### Railway 배포
```bash
# Dockerfile 사용 (Ollama + Chatbot 통합)
# Git push만 하면 자동 배포
git push origin main
```

---

## ✅ 배포 체크리스트

배포 완료 전 확인:

- [ ] Git에 변경사항 커밋 및 푸시
- [ ] Railway 자동 배포 확인 (10-20분 대기)
- [ ] 로그에서 "Ollama server is ready" 확인
- [ ] 로그에서 "Starting Chainlit app" 확인
- [ ] 공개 URL 접속 (https://ollama-company-chatbot.up.railway.app/)
- [ ] 테스트 질문 3개 성공
- [ ] 에러 메시지 없이 정상 응답 확인

---

## 📞 추가 지원

**Railway 공식 문서**:
- https://docs.railway.app

**문제 발생 시**:
1. Railway 로그 확인 (가장 중요!)
2. GitHub Issues 등록
3. 팀원에게 문의

---

## 🎉 배포 성공!

이제 다음을 얻었습니다:

✅ **프로덕션급 인프라**
- 자동 HTTPS/SSL
- 자동 배포 (Git push)
- 무중단 배포

✅ **통합 Ollama + Chatbot**
- 하나의 컨테이너에서 실행
- 연결 문제 해결
- 명확한 에러 메시지

✅ **모니터링**
- Real-time 로그
- 메트릭 대시보드

---

**공개 URL**: https://ollama-company-chatbot.up.railway.app/

발표 자료에 추가하세요! 🚀
