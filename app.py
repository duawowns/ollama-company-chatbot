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

# Google AI Studio 스타일 커스텀 CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&display=swap');

    /* 전체 배경 - 밝은 테마 */
    .stApp {
        background: #f8f9fa;
        font-family: 'Google Sans', 'Segoe UI', sans-serif;
    }

    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 800px;
    }

    /* 제목 스타일 */
    h1 {
        color: #202124;
        font-weight: 500;
        letter-spacing: -0.5px;
        font-size: 2.25rem !important;
        margin-bottom: 0.5rem;
        font-family: 'Google Sans', sans-serif;
    }

    /* 부제목 */
    .subtitle {
        color: #5f6368;
        font-size: 1rem;
        margin-bottom: 2.5rem;
        font-weight: 400;
    }

    /* 채팅 메시지 - Google 스타일 */
    .stChatMessage {
        background: transparent;
        border: none;
        border-radius: 24px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* 사용자 메시지 */
    .stChatMessage[data-testid*="user"] {
        background: #e8f0fe;
        margin-left: 2rem;
    }

    /* AI 메시지 */
    .stChatMessage[data-testid*="assistant"] {
        background: #fff;
        border: 1px solid #e8eaed;
        margin-right: 2rem;
    }

    [data-testid="stChatMessageContent"] {
        color: #202124;
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* 입력창 - 하단 고정 스타일 */
    .stChatInput {
        position: sticky;
        bottom: 0;
        background: #fff;
        border: 1px solid #dadce0;
        border-radius: 24px;
        padding: 0.5rem;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3), 0 1px 3px 1px rgba(60,64,67,0.15);
    }

    .stChatInput textarea {
        border: none !important;
        font-size: 0.95rem;
        color: #202124;
    }

    /* 사이드바 - Google 스타일 */
    [data-testid="stSidebar"] {
        background: #fff;
        border-right: 1px solid #e8eaed;
        padding-top: 1rem;
    }

    [data-testid="stSidebar"] h2 {
        color: #202124;
        font-size: 1rem;
        font-weight: 500;
        padding-left: 1rem;
        margin-bottom: 1rem;
    }

    /* 버튼 - Google Material Design */
    .stButton button {
        background: #fff;
        border: 1px solid #dadce0;
        border-radius: 20px;
        color: #1a73e8;
        font-weight: 500;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
        box-shadow: none;
    }

    .stButton button:hover {
        background: #f8f9fa;
        border-color: #dadce0;
        box-shadow: 0 1px 2px 0 rgba(60,64,67,0.3);
    }

    /* 셀렉트박스 */
    .stSelectbox {
        background: #fff;
    }

    .stSelectbox > div > div {
        background: #fff;
        border: 1px solid #dadce0;
        border-radius: 8px;
        color: #202124;
    }

    /* 슬라이더 */
    .stSlider {
        padding-top: 1rem;
    }

    .stSlider > div > div > div {
        color: #1a73e8;
    }

    /* 체크박스 */
    .stCheckbox {
        color: #202124;
    }

    .stCheckbox > label {
        font-size: 0.9rem;
    }

    /* 구분선 */
    hr {
        border-color: #e8eaed;
        margin: 1.5rem 0;
    }

    /* 라벨 텍스트 */
    label {
        color: #5f6368 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        color: #5f6368;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid #e8eaed;
    }

    /* 에러/경고 메시지 */
    .stAlert {
        background: #fef7e0;
        border: 1px solid #f9ab00;
        border-radius: 8px;
        color: #202124;
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
