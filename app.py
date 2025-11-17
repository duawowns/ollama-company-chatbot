"""
퓨쳐시스템 회사소개 챗봇
Streamlit 기반 RAG 챗봇 (2025 최신 기술 스택)
ChromaDB + BGE-M3 + FlashRank + Ollama
"""

import streamlit as st
from datetime import datetime
from pathlib import Path
import logging
import sys

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.rag_pipeline import RAGPipeline

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 페이지 설정
st.set_page_config(
    page_title="퓨쳐시스템",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Linear.app 스타일 커스텀 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

    /* 전체 배경 - Linear 다크 테마 */
    .stApp {
        background: linear-gradient(180deg, #0a0b0d 0%, #12141a 100%);
        font-family: 'Inter', -apple-system, sans-serif;
        color: #e6e6e6;
    }

    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    /* 제목 스타일 - Linear 스타일 */
    h1 {
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-size: 1.75rem !important;
        margin-bottom: 0.5rem !important;
        margin-top: 0 !important;
        font-family: 'Inter', sans-serif;
    }

    /* 부제목 */
    .subtitle {
        color: #8a8f98;
        font-size: 0.875rem;
        margin-bottom: 2.5rem;
        margin-top: 0.25rem;
        font-weight: 400;
        letter-spacing: -0.01em;
    }

    /* 채팅 메시지 - Linear 미니멀 스타일 */
    .stChatMessage {
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 0.875rem 1rem;
        margin-bottom: 0.5rem;
    }

    /* 사용자 메시지 */
    .stChatMessage[data-testid*="user"] {
        background: rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        margin-left: 15%;
    }

    /* AI 메시지 */
    .stChatMessage[data-testid*="assistant"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        margin-right: 15%;
    }

    [data-testid="stChatMessageContent"] {
        color: #e6e6e6;
        font-size: 0.9375rem;
        line-height: 1.6;
    }

    /* 입력창 - Linear 스타일 */
    .stChatInput {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        backdrop-filter: blur(10px);
    }

    .stChatInput textarea {
        border: none !important;
        font-size: 0.9375rem;
        color: #e6e6e6;
        background: transparent !important;
    }

    .stChatInput textarea::placeholder {
        color: #6b7280;
    }

    /* 사이드바 - Linear 다크 스타일 */
    [data-testid="stSidebar"] {
        background: rgba(0, 0, 0, 0.3);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 1.5rem;
        backdrop-filter: blur(10px);
    }

    [data-testid="stSidebar"] h2 {
        color: #ffffff;
        font-size: 0.875rem;
        font-weight: 600;
        padding-left: 1rem;
        margin-bottom: 1.5rem;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }

    /* 버튼 - Linear 미니멀 스타일 */
    .stButton button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        color: #e6e6e6;
        font-weight: 500;
        padding: 0.5rem 1rem;
        transition: all 0.15s ease;
        box-shadow: none;
    }

    .stButton button:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.15);
    }

    /* 셀렉트박스 */
    .stSelectbox {
        color: #e6e6e6;
    }

    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        color: #e6e6e6;
    }

    .stSelectbox option {
        background: #1a1d24;
        color: #e6e6e6;
    }

    /* 슬라이더 */
    .stSlider {
        padding-top: 1rem;
    }

    .stSlider > div > div > div {
        background: rgba(99, 102, 241, 0.3);
    }

    .stSlider > div > div > div > div {
        background: #6366f1;
    }

    /* 슬라이더 값 텍스트 */
    .stSlider [data-testid="stTickBar"] > div {
        color: #8a8f98 !important;
    }

    .stSlider [data-testid="stThumbValue"] {
        color: #e6e6e6 !important;
    }

    /* 체크박스 */
    .stCheckbox {
        color: #e6e6e6;
    }

    .stCheckbox > label {
        font-size: 0.875rem;
        color: #e6e6e6 !important;
    }

    /* 구분선 */
    hr {
        border-color: rgba(255, 255, 255, 0.08);
        margin: 1.5rem 0;
    }

    /* 라벨 텍스트 */
    label {
        color: #8a8f98 !important;
        font-size: 0.8125rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.75rem;
        margin-top: 3rem;
        padding: 1.5rem 0;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* 에러/경고 메시지 */
    .stAlert {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 6px;
        color: #fca5a5;
    }

    /* 스피너 */
    .stSpinner > div {
        border-color: #6366f1 transparent transparent transparent !important;
    }

    /* 숨기기: Streamlit 기본 요소 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def initialize_rag_pipeline(model_name: str, temperature: float, use_reranking: bool):
    """RAG 파이프라인 초기화 (캐싱)"""
    try:
        with st.spinner("RAG 시스템 초기화 중..."):
            # RAG 파이프라인 생성
            pipeline = RAGPipeline(
                model_name=model_name,
                temperature=temperature,
                use_reranking=use_reranking
            )

            # 벡터 스토어 로드
            vectorstore_path = project_root / "data" / "vectorstore"

            if not vectorstore_path.exists():
                st.error("데이터베이스를 찾을 수 없습니다. 관리자에게 문의하세요.")
                return None

            pipeline.load_vectorstore(str(vectorstore_path))

            # QA 체인 생성
            pipeline.create_qa_chain()

            logger.info("RAG 파이프라인 초기화 완료")
            return pipeline

    except Exception as e:
        st.error(f"RAG 초기화 실패: {e}")
        logger.error(f"RAG 초기화 실패: {e}", exc_info=True)
        return None


def main():
    """메인 애플리케이션"""

    # 제목
    st.title("퓨쳐시스템 인트라넷 챗봇")
    st.markdown('<p class="subtitle">정보보호 전문기업 · AI 어시스턴트</p>', unsafe_allow_html=True)

    # 사이드바
    with st.sidebar:
        st.header("설정")
        st.markdown("---")

        # 모델 선택
        model_option = st.selectbox(
            "모델",
            ["llama3.1:8b", "llama3.2:3b", "mistral:7b", "gemma:7b"],
            help="사용할 AI 모델 선택"
        )

        # 온도 설정
        temperature = st.slider(
            "Temperature",
            0.0, 1.0, 0.7, 0.1,
            help="낮을수록 정확하고 일관적, 높을수록 창의적"
        )

        # Reranking 옵션
        use_reranking = st.checkbox(
            "고급 검색",
            value=True,
            help="검색 정확도 향상"
        )

        st.markdown("---")

        # 대화 초기화 버튼
        if st.button("대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # 세션 상태 초기화
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # RAG 파이프라인 초기화 (캐싱됨)
    rag_pipeline = initialize_rag_pipeline(
        model_name=model_option,
        temperature=temperature,
        use_reranking=use_reranking
    )

    # RAG 초기화 실패 시 중단
    if rag_pipeline is None:
        st.stop()

    # 대화 이력 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력
    if prompt := st.chat_input("메시지를 입력하세요..."):
        # 사용자 메시지 추가
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 어시스턴트 응답 (스트리밍)
        with st.chat_message("assistant"):
            try:
                # 스트리밍 응답 생성
                response_placeholder = st.empty()
                full_response = ""

                for chunk in rag_pipeline.stream_query(prompt):
                    full_response += chunk
                    response_placeholder.markdown(full_response + "▌")

                # 최종 응답 표시 (커서 제거)
                response_placeholder.markdown(full_response)

                # 메시지 히스토리에 추가
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response
                })

            except Exception as e:
                error_msg = f"오류가 발생했습니다: {str(e)}"
                st.error(error_msg)
                logger.error(f"질의 처리 오류: {e}", exc_info=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "죄송합니다. 일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요."
                })

    # 푸터
    st.markdown(
        f'<div class="footer">'
        f'© 2025 퓨쳐시스템 | 동서울대학교 캡스톤디자인 프로젝트'
        f'</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
