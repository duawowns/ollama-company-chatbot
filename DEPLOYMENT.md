# 외부 발표용 배포 가이드

캡스톤 발표를 위한 안전한 외부 배포 방법을 안내합니다.

---

## 📋 배포 전 체크리스트

- [x] 환경변수 설정 완료
- [x] 입력 검증 추가
- [x] Docker 파일 생성
- [ ] 모델 다운로드 (llama3.1:8b)
- [ ] 클라우드 배포
- [ ] HTTPS 설정
- [ ] 접근 제한 설정

---

## 🚀 배포 옵션

### 옵션 1: Render.com (추천 - 무료)

**장점:**
- 무료 플랜 제공
- HTTPS 자동 설정
- 간단한 배포
- Git 연동 자동 배포

**단점:**
- Ollama 서버 별도 필요
- 무료 플랜은 15분 idle 후 슬립

**배포 방법:**

1. **Render 계정 생성**
   - https://render.com 회원가입
   - GitHub 연동

2. **Ollama 서버 준비** (별도 서버 필요)
   - VPS 또는 로컬 서버에 Ollama 설치
   - 공개 URL 확보 (ngrok 또는 CloudFlare Tunnel)

3. **Web Service 생성**
   ```
   - New > Web Service
   - Connect Repository
   - Build Command: pip install -r requirements.txt
   - Start Command: chainlit run chainlit_app.py --host 0.0.0.0 --port 8501
   ```

4. **환경변수 설정**
   ```
   OLLAMA_BASE_URL=http://your-ollama-server:11434
   MAX_QUERY_LENGTH=500
   ```

---

### 옵션 2: Railway.app (권장 - 유료/무료)

**장점:**
- Docker Compose 지원
- Ollama + Chatbot 함께 배포 가능
- $5 무료 크레딧
- HTTPS 자동

**배포 방법:**

1. **Railway 계정 생성**
   - https://railway.app
   - GitHub 연동

2. **New Project > Deploy from GitHub repo**
   - Repository 선택
   - docker-compose.yml 자동 감지

3. **환경변수 확인**
   - Railway가 자동으로 설정

4. **도메인 설정**
   - Settings > Generate Domain
   - Custom Domain 추가 가능

**주의사항:**
- Ollama 모델 다운로드 시간 소요 (첫 배포 시 10-15분)
- 무료 크레딧 소진 주의

---

### 옵션 3: Fly.io (기술적)

**장점:**
- Docker 완벽 지원
- 무료 플랜 제공
- 빠른 배포

**배포 방법:**

1. **Fly CLI 설치**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **로그인 및 초기화**
   ```bash
   fly auth login
   fly launch
   ```

3. **fly.toml 수정** (자동 생성됨)

4. **배포**
   ```bash
   fly deploy
   ```

---

### 옵션 4: 로컬 서버 + ngrok (가장 빠름)

**발표 당일 급하면 이 방법 사용**

**장점:**
- 5분 안에 배포 가능
- 로컬 환경 그대로 사용
- 완전 무료

**배포 방법:**

1. **Ollama 및 Chainlit 실행**
   ```bash
   # 터미널 1: Ollama
   ollama serve

   # 터미널 2: Chainlit
   chainlit run chainlit_app.py --port 8501
   ```

2. **ngrok 설치 및 실행**
   ```bash
   # ngrok 설치
   brew install ngrok  # Mac
   # 또는
   snap install ngrok  # Linux

   # ngrok 실행
   ngrok http 8501
   ```

3. **공개 URL 확인**
   ```
   Forwarding: https://abc123.ngrok.io -> localhost:8501
   ```

4. **발표 시 사용**
   - 이 URL을 발표자료에 추가
   - 청중이 접속 가능

**주의사항:**
- ngrok 무료 플랜은 8시간 제한
- 발표 당일에만 켜두기
- 발표 끝나면 종료

---

## 🔒 보안 설정 (필수)

### 1. CORS 설정

`.chainlit/config.toml` 수정:

```toml
[server]
# 특정 도메인만 허용
allow_origins = ["https://yourdomain.com"]

# 또는 발표용으로 임시 허용
allow_origins = ["*"]  # 발표 끝나면 제한할 것!
```

### 2. Rate Limiting (옵션)

Chainlit 앱 앞단에 Nginx 추가:

```nginx
limit_req_zone $binary_remote_addr zone=chatbot:10m rate=10r/m;

server {
    location / {
        limit_req zone=chatbot burst=5;
        proxy_pass http://localhost:8501;
    }
}
```

### 3. 접근 로그 활성화

```python
# chainlit_app.py에 추가
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('access.log'),
        logging.StreamHandler()
    ]
)
```

---

## 📊 발표 시 모니터링

### 실시간 로그 확인

```bash
# Docker 로그
docker-compose logs -f chatbot

# 또는 로컬 실행 시
tail -f chainlit.log
```

### 헬스체크

```bash
# Ollama 확인
curl http://your-server:11434/api/tags

# Chainlit 확인
curl http://your-app-url:8501/
```

---

## 🎯 발표 시나리오

### 준비사항

1. **발표 30분 전**
   - 서버 재시작
   - 모델 로드 확인 (ollama list)
   - 테스트 질문 3개 실행
   - URL 공유 준비

2. **발표 중**
   - 실시간 데모 준비
   - 미리 정한 질문 리스트:
     - "회사 주소 알려줘"
     - "개발자는 누구야?"
     - "어떤 기술 스택을 사용했어?"

3. **발표 후**
   - 접속 로그 확인
   - 서비스 종료 또는 접근 제한

---

## ⚠️ 주의사항

### 발표 중 오류 대응

**오류 1: "Ollama 연결 실패"**
```bash
# Ollama 재시작
docker-compose restart ollama
# 또는
ollama serve
```

**오류 2: "응답이 너무 느림"**
- 모델이 너무 큼 (8b → 3b로 변경)
- ```bash
  ollama pull llama3.2:3b
  ```

**오류 3: "메모리 부족"**
- Ollama 모델 언로드
- ```bash
  curl http://localhost:11434/api/generate -d '{"model":"llama3.1:8b","keep_alive":0}'
  ```

---

## 📝 발표 스크립트 예시

```
[슬라이드 1: 데모 시작]
"지금부터 실제 동작하는 챗봇을 보여드리겠습니다.
현재 Render.com에 배포되어 있으며, 누구나 접속 가능합니다."

[URL 공유: https://futuresystem-chatbot.onrender.com]

[슬라이드 2: 실시간 질의응답]
(질문 입력) "회사 주소 알려줘"
→ RAG 시스템이 ChromaDB에서 관련 문서를 검색
→ FlashRank로 재순위화
→ Ollama LLM이 답변 생성
→ 실시간 스트리밍으로 출력

[슬라이드 3: 기술 스택 설명]
"보시다시피 평균 2초 이내에 답변이 생성됩니다.
이는 BGE-M3 임베딩과 FlashRank 재순위화 덕분입니다."
```

---

## 🎓 발표 팁

1. **백업 플랜 준비**
   - 녹화 영상 준비 (데모 실패 시)
   - 로컬 실행본 준비

2. **네트워크 확인**
   - 발표장 WiFi 사전 테스트
   - 핫스팟 백업 준비

3. **질문 미리 준비**
   - 확실히 답변 가능한 질문 3-5개
   - 실패 가능한 질문도 준비 (한계 설명용)

---

## 📞 문제 발생 시

### 긴급 연락처
- Railway Support: https://railway.app/discord
- Render Support: https://render.com/docs/support
- Fly.io Support: https://community.fly.io/

### 백업 플랜
1. 로컬 실행 + 화면 공유
2. 사전 녹화 영상 재생
3. 스크린샷으로 설명

---

## ✅ 최종 체크리스트 (발표 당일)

- [ ] 서버 정상 동작 확인
- [ ] 테스트 질문 3개 실행
- [ ] URL 접속 가능 확인
- [ ] 발표 자료에 URL 추가
- [ ] 백업 영상 준비
- [ ] 로컬 실행본 준비
- [ ] 네트워크 연결 확인
- [ ] 배터리 충전 완료

---

**Good Luck! 🚀**
