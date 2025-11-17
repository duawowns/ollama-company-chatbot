# Railway.app 완벽 배포 가이드

엔터프라이즈급 프로덕션 배포 방법입니다.

---

## 🚀 Railway.app이 최고인 이유

✅ Docker Compose 완벽 지원
✅ Ollama + Chatbot 동시 배포
✅ 자동 HTTPS/SSL
✅ 무료 $5 크레딧
✅ GitHub 자동 배포
✅ 프로덕션급 인프라

---

## 📋 사전 준비

### 1. Railway 계정 생성

1. https://railway.app 접속
2. **Login with GitHub** 클릭
3. GitHub 연동 승인
4. $5 무료 크레딧 자동 지급

### 2. GitHub 저장소 준비

```bash
# 현재 변경사항 모두 커밋
git add .
git commit -m "프로덕션 배포 준비 완료"
git push origin main
```

---

## 🔧 Railway 프로젝트 생성

### 방법 1: Web UI (권장)

1. **New Project** 클릭
2. **Deploy from GitHub repo** 선택
3. Repository 선택: `ollama-company-chatbot`
4. **Deploy Now** 클릭

Railway가 자동으로:
- `docker-compose.yml` 감지
- Ollama와 Chatbot 서비스 생성
- 이미지 빌드 및 배포

### 방법 2: CLI

```bash
# Railway CLI 설치
npm install -g @railway/cli

# 로그인
railway login

# 프로젝트 초기화
railway init

# GitHub 연결
railway link

# 배포
railway up
```

---

## ⚙️ 환경변수 설정

Railway Dashboard > 프로젝트 > Settings > Variables

### 필수 환경변수

```bash
# Ollama 연결
OLLAMA_BASE_URL=http://ollama:11434

# 애플리케이션 설정
MAX_QUERY_LENGTH=500
MAX_HISTORY_ITEMS=5
LOG_LEVEL=INFO

# Rate Limiting
RATE_LIMIT_PER_MINUTE=30
RATE_LIMIT_PER_HOUR=100

# 프로덕션 설정
PYTHONUNBUFFERED=1
```

### 선택 환경변수 (보안)

```bash
# 인증 활성화
AUTH_ENABLED=true
AUTH_USERNAME=admin
AUTH_PASSWORD=강력한비밀번호여기

# Sentry (에러 트래킹)
SENTRY_DSN=https://your-sentry-dsn
```

---

## 🔌 서비스 설정

Railway는 `docker-compose.yml`을 자동으로 파싱하여 2개 서비스 생성:

### 1. ollama 서비스

- Image: `ollama/ollama:latest`
- Internal Port: 11434
- 외부 노출 불필요 (내부 통신만)

**중요:** Ollama 모델 다운로드

Railway Shell에서 실행:
```bash
# Railway Dashboard > ollama 서비스 > Shell 탭
ollama pull llama3.1:8b
```

⏱️ **10-15분 소요** (7.4GB 다운로드)

### 2. chatbot 서비스

- Build: Dockerfile
- Internal Port: 8501
- 외부 노출: ✅ (Generate Domain)

**도메인 생성:**
1. chatbot 서비스 > Settings
2. **Generate Domain** 클릭
3. 자동 URL: `https://your-app.up.railway.app`

---

## 📊 배포 진행 상황 모니터링

### 빌드 로그 확인

Railway Dashboard > chatbot 서비스 > Deployments > 최신 배포 클릭

**예상 빌드 시간:**
- Ollama: 2-3분 (이미지 풀)
- Chatbot: 5-7분 (의존성 설치)

### 헬스체크 확인

배포 완료 후:
```bash
curl https://your-app.up.railway.app/
```

정상 응답 시 ✅ 배포 성공!

---

## 🎯 배포 후 작업

### 1. Ollama 모델 다운로드 (필수)

```bash
# Railway Dashboard > ollama 서비스 > Shell
ollama pull llama3.1:8b

# 다운로드 확인
ollama list
```

### 2. 테스트 질문

Railway 공개 URL로 접속:
```
https://your-app.up.railway.app
```

질문 테스트:
1. "회사 주소 알려줘"
2. "개발자는 누구야?"
3. "사용된 기술 스택은?"

### 3. 커스텀 도메인 설정 (선택)

1. Railway Dashboard > chatbot 서비스 > Settings
2. **Custom Domain** 클릭
3. 도메인 입력: `chatbot.yourcompany.com`
4. DNS CNAME 레코드 추가:
   ```
   chatbot.yourcompany.com -> your-app.up.railway.app
   ```

---

## 🔒 보안 강화 (프로덕션)

### 1. 인증 활성화

환경변수 추가:
```bash
AUTH_ENABLED=true
AUTH_USERNAME=admin
AUTH_PASSWORD=super_secure_password_123
```

재배포 후 로그인 화면 표시됨

### 2. CORS 설정

`.chainlit/config.toml` 수정:
```toml
[server]
allow_origins = ["https://your-app.up.railway.app"]
```

### 3. Rate Limiting 조정

트래픽에 따라 조정:
```bash
# 엄격한 제한 (공개 데모)
RATE_LIMIT_PER_MINUTE=10
RATE_LIMIT_PER_HOUR=30

# 관대한 제한 (사내 사용)
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_PER_HOUR=200
```

---

## 📈 모니터링

### Railway 기본 모니터링

Dashboard > chatbot 서비스 > Metrics

확인 가능:
- CPU 사용률
- 메모리 사용량
- 네트워크 트래픽
- 요청 수

### 로그 확인

```bash
# Real-time 로그
Railway Dashboard > chatbot 서비스 > Logs

# 또는 CLI
railway logs --service chatbot
```

### Sentry 연동 (선택)

1. https://sentry.io 계정 생성
2. DSN 복사
3. 환경변수 추가:
   ```bash
   SENTRY_DSN=https://your-sentry-dsn
   ```

---

## 💰 비용 관리

### 무료 크레딧

- 초기 $5 무료 크레딧
- 약 500시간 실행 가능 (소형 프로젝트)

### 사용량 확인

Dashboard > Account > Usage

### 예상 비용

**Hobby Plan (소규모):**
- Chatbot: ~$5/월
- Ollama: ~$10/월
- **총: ~$15/월**

**Pro Plan (대규모):**
- 무제한 프로젝트
- $20/월

---

## 🐛 트러블슈팅

### 문제 1: Ollama 연결 실패

**증상:**
```
❌ Ollama connection refused
```

**해결:**
1. Ollama 서비스 재시작
2. 환경변수 확인: `OLLAMA_BASE_URL=http://ollama:11434`
3. ollama 서비스 로그 확인

### 문제 2: 모델 다운로드 실패

**증상:**
```
model 'llama3.1:8b' not found
```

**해결:**
```bash
# Railway Shell (ollama 서비스)
ollama pull llama3.1:8b

# 작은 모델로 테스트
ollama pull llama3.2:3b
```

### 문제 3: 메모리 부족

**증상:**
```
OOMKilled
```

**해결:**
1. 더 작은 모델 사용: `llama3.2:3b`
2. Railway Plan 업그레이드
3. `num_gpu=0` 설정 (CPU 전용)

### 문제 4: 빌드 시간 초과

**증상:**
```
Build timeout after 30 minutes
```

**해결:**
1. `.dockerignore` 확인 (venv 제외)
2. requirements.txt 최적화
3. 불필요한 의존성 제거

---

## 🔄 CI/CD (자동 배포)

Railway는 GitHub 푸시 시 자동 배포:

```bash
# 코드 수정
git add .
git commit -m "Update feature"
git push origin main

# Railway가 자동으로:
# 1. 변경사항 감지
# 2. Docker 이미지 리빌드
# 3. 새 버전 배포
# 4. 헬스체크 통과 시 전환
```

### 배포 설정

Railway Dashboard > Project > Settings > Deploys

- **Auto Deploy**: ✅ (기본값)
- **Production Branch**: `main`
- **Preview Environments**: ✅ (PR마다 미리보기)

---

## ✅ 최종 체크리스트

배포 완료 전 확인:

- [ ] Railway 계정 생성
- [ ] GitHub 저장소 연결
- [ ] 환경변수 설정 완료
- [ ] Ollama 서비스 시작
- [ ] Ollama 모델 다운로드 (`llama3.1:8b`)
- [ ] Chatbot 서비스 시작
- [ ] 공개 URL 접속 확인
- [ ] 테스트 질문 3개 성공
- [ ] 인증 활성화 (선택)
- [ ] 커스텀 도메인 설정 (선택)
- [ ] 모니터링 설정 (선택)

---

## 🎉 배포 성공!

축하합니다! 이제 다음을 얻었습니다:

✅ **프로덕션급 인프라**
- 자동 HTTPS/SSL
- 무중단 배포
- 자동 스케일링

✅ **엔터프라이즈 보안**
- 인증 시스템
- Rate Limiting
- 입력 검증

✅ **모니터링 & 로깅**
- Real-time 로그
- 메트릭 대시보드
- 에러 트래킹

---

## 📞 지원

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Ollama Docs: https://ollama.ai/docs

---

**공개 URL:** `https://your-app.up.railway.app`

이 URL을 발표 자료에 추가하세요! 🚀
