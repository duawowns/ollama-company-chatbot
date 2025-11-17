# 캡스톤디자인 전시 판넬 사용 가이드

## 📋 제작된 파일

### 1. 디자인 철학
- **파일**: `design_philosophy.md`
- **내용**: "Neural Pathways" 디자인 컨셉
- 정보 흐름과 네트워크 시각화를 기반으로 한 디자인 철학

### 2. 초안 (Draft)
- **파일**: `capstone_poster_draft.html`
- **용도**: 초기 디자인 검토 및 내용 확인
- **특징**: 기본적인 레이아웃과 정보 배치

### 3. 완성본 (Final)
- **파일**: `capstone_poster_final.html`
- **용도**: 최종 출력용
- **특징**:
  - 고급 그라디언트 및 시각 효과
  - 정교한 네트워크 비주얼
  - 애니메이션 효과 (화면용)
  - A1 사이즈 최적화 (594mm x 841mm)

## 🖨️ PDF로 출력하는 방법

### 방법 1: Chrome/Edge 브라우저 사용 (권장)

1. **HTML 파일 열기**
   ```bash
   # 완성본 열기
   google-chrome docs/capstone_poster_final.html
   # 또는
   microsoft-edge docs/capstone_poster_final.html
   ```

2. **인쇄 설정**
   - `Ctrl + P` (또는 `Cmd + P`)
   - **대상**: PDF로 저장
   - **용지 크기**: A1 (594 x 841mm)
   - **여백**: 없음
   - **배경 그래픽**: 체크 ✓
   - **배율**: 100%

3. **저장**
   - "저장" 클릭
   - 파일명: `capstone_poster_final.pdf`

### 방법 2: Firefox 브라우저

1. HTML 파일 열기
2. `Ctrl + P`
3. **용지 크기**: A1
4. **여백**: 사용자 정의 - 모두 0
5. **배경 색상 및 이미지 인쇄**: 체크 ✓
6. PDF로 저장

### 방법 3: 명령줄 도구 (wkhtmltopdf)

```bash
# 설치 (Ubuntu/Debian)
sudo apt-get install wkhtmltopdf

# PDF 생성
wkhtmltopdf \
  --page-size A1 \
  --orientation Portrait \
  --margin-top 0 \
  --margin-bottom 0 \
  --margin-left 0 \
  --margin-right 0 \
  --enable-local-file-access \
  docs/capstone_poster_final.html \
  docs/capstone_poster_final.pdf
```

## 🎨 디자인 특징

### 색상 팔레트
- **Deep Blue**: #0A1929 (배경)
- **Tech Teal**: #00D9FF (강조)
- **Neural Blue**: #1E88E5 (노드)
- **Warm Accent**: #FF6B35 (아키텍처)

### 레이아웃
- **헤더**: 프로젝트 타이틀, 소속
- **좌측**: 프로젝트 정보, 기술 스택
- **중앙**: 시스템 아키텍처 다이어그램
- **우측**: 주요 기능
- **푸터**: 기대 효과

### 시각적 요소
- 네트워크 그리드 배경
- 플로팅 파티클 애니메이션
- 그라디언트 노드
- SVG 연결선
- 블러 효과

## 📐 출력 사양

- **크기**: A1 (594mm × 841mm)
- **방향**: 세로 (Portrait)
- **해상도**: 웹 기준 (화면 출력)
- **색상 모드**: RGB
- **권장 출력**: 고품질 컬러 프린터

## ✏️ 수정 방법

HTML 파일을 텍스트 에디터로 열어서 직접 수정 가능:

### 텍스트 수정
- HTML 파일 내에서 해당 텍스트를 찾아 수정

### 색상 변경
- CSS `<style>` 섹션에서 색상 코드 수정

### 레이아웃 조정
- 그리드 크기, 패딩, 마진 값 수정

## 📸 미리보기

브라우저에서 HTML 파일을 열어 바로 확인 가능합니다:

```bash
# 초안 미리보기
open docs/capstone_poster_draft.html

# 완성본 미리보기
open docs/capstone_poster_final.html
```

## 💡 팁

1. **고해상도 출력**: 전문 인쇄소에 의뢰 시 PDF 파일 제공
2. **색상 조정**: 모니터와 프린터 색상이 다를 수 있으니 테스트 출력 권장
3. **파일 공유**: PDF로 변환하면 모든 플랫폼에서 동일하게 표시됨
4. **백업**: HTML 파일과 PDF 파일 모두 보관

## 🚀 다음 단계

1. ✅ 초안 검토
2. ✅ 완성본 확인
3. ⬜ PDF 출력
4. ⬜ 테스트 프린트 (A4로 축소 출력)
5. ⬜ 최종 A1 출력
6. ⬜ 전시 준비

---

궁금한 점이 있으면 언제든 질문하세요!
