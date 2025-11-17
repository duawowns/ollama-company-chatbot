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

# Linear 스타일 커스텀 CSS
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #0A1929 0%, #0D2137 100%);
    }

    /* 메인 컨테이너 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }

    /* 제목 스타일 */
    h1 {
        color: rgba(255, 255, 255, 0.98);
        font-weight: 600;
        letter-spacing: -0.5px;
        font-size: 2rem !important;
        margin-bottom: 0.5rem;
    }

    /* 부제목 */
    .subtitle {
        color: rgba(255, 255, 255, 0.5);
        font-size: 0.95rem;
        margin-bottom: 2rem;
    }

    /* 채팅 메시지 */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.03);
        border: 0.5px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }

    /* 사용자 메시지 */
    [data-testid="stChatMessageContent"] {
        color: rgba(255, 255, 255, 0.95);
    }

    /* 입력창 */
    .stChatInput {
        border: 0.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: rgba(10, 25, 41, 0.6);
        backdrop-filter: blur(10px);
        border-right: 0.5px solid rgba(255, 255, 255, 0.06);
    }

    [data-testid="stSidebar"] h2 {
        color: rgba(255, 255, 255, 0.98);
        font-size: 1.1rem;
        font-weight: 500;
    }

    /* 버튼 */
    .stButton button {
        background: rgba(255, 255, 255, 0.04);
        border: 0.5px solid rgba(255, 255, 255, 0.12);
        border-radius: 6px;
        color: rgba(255, 255, 255, 0.95);
        font-weight: 400;
        transition: all 0.2s;
    }

    .stButton button:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
    }

    /* 셀렉트박스, 슬라이더 */
    .stSelectbox, .stSlider {
        color: rgba(255, 255, 255, 0.95);
    }

    /* 메트릭 */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 0.5px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        padding: 0.75rem;
    }

    [data-testid="stMetricValue"] {
        color: rgba(0, 217, 255, 0.9);
        font-size: 1.5rem;
    }

    /* Info 박스 */
    .stAlert {
        background: rgba(255, 255, 255, 0.02);
        border: 0.5px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        color: rgba(255, 255, 255, 0.8);
    }

    /* 워닝 박스 */
    .stWarning {
        background: rgba(255, 107, 53, 0.06);
        border: 0.5px solid rgba(255, 107, 53, 0.3);
    }

    /* 구분선 */
    hr {
        border-color: rgba(255, 255, 255, 0.06);
        margin: 1.5rem 0;
    }

    /* 푸터 */
    .footer {
        text-align: center;
        color: rgba(255, 255, 255, 0.4);
        font-size: 0.85rem;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 0.5px solid rgba(255, 255, 255, 0.06);
    }
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

        # 시스템 상태
        st.info("**시스템 상태**\n"
                "✓ 데이터: 83개 Q&A\n"
                "✓ 검색: 활성화\n"
                "✓ 응답: 실시간 스트리밍")

        # 대화 초기화 버튼
        if st.button("대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        # 통계
        if "messages" in st.session_state and st.session_state.messages:
            st.markdown("---")
            st.metric("대화", f"{len(st.session_state.messages) // 2}회")

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
