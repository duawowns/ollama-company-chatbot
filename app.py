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
    page_title="퓨쳐시스템 챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


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
                st.error("벡터 스토어가 생성되지 않았습니다. `python scripts/create_vectorstore.py`를 실행하세요.")
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
    st.title("🤖 퓨쳐시스템 회사소개 챗봇")
    st.markdown("퓨쳐시스템에 대해 궁금한 점을 물어보세요 (RAG + Ollama)")

    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        st.markdown("---")

        # 모델 선택
        model_option = st.selectbox(
            "LLM 모델",
            ["llama3.1:8b", "llama3.2:3b", "mistral:7b", "gemma:7b"],
            help="Ollama에서 다운로드한 모델을 선택하세요"
        )

        # 온도 설정
        temperature = st.slider(
            "Temperature",
            0.0, 1.0, 0.7, 0.1,
            help="낮을수록 일관적, 높을수록 창의적"
        )

        # Reranking 옵션
        use_reranking = st.checkbox(
            "Reranking 사용",
            value=True,
            help="FlashRank를 사용하여 검색 결과 재순위화"
        )

        st.markdown("---")

        # 시스템 정보
        st.info("💡 **기술 스택**\n"
                "- Vector DB: ChromaDB\n"
                "- Embeddings: BGE-M3\n"
                "- Reranking: FlashRank\n"
                "- LLM: Ollama")

        st.warning("⚠️ Ollama가 실행 중인지 확인하세요\n"
                   "`ollama serve`")

        # 대화 초기화 버튼
        if st.button("🗑️ 대화 초기화", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        # 통계
        if "messages" in st.session_state and st.session_state.messages:
            st.markdown("---")
            st.metric("총 대화 수", len(st.session_state.messages) // 2)

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
                    "content": "죄송합니다. 오류가 발생했습니다. Ollama 서버가 실행 중인지 확인해주세요."
                })

    # 푸터
    st.markdown("---")
    st.caption(
        f"© 2025 퓨쳐시스템 챗봇 | "
        f"Powered by ChromaDB + BGE-M3 + FlashRank + Ollama | "
        f"마지막 업데이트: {datetime.now().strftime('%Y-%m-%d')}"
    )


if __name__ == "__main__":
    main()
