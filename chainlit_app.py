"""
퓨쳐시스템 회사소개 챗봇 (Chainlit 버전)
RAG 챗봇 - ChromaDB + BGE-M3 + FlashRank + Ollama
"""

import chainlit as cl
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


@cl.on_chat_start
async def start():
    """채팅 시작 시 호출"""
    # RAG 파이프라인 초기화 (백그라운드)
    try:
        # 기본 설정
        model_name = "llama3.1:8b"
        temperature = 0.7
        use_reranking = True

        # RAG 파이프라인 생성
        pipeline = RAGPipeline(
            model_name=model_name,
            temperature=temperature,
            use_reranking=use_reranking
        )

        # 벡터 스토어 로드
        vectorstore_path = project_root / "data" / "vectorstore"

        if not vectorstore_path.exists():
            await cl.Message(
                content="❌ 데이터베이스를 찾을 수 없습니다. 관리자에게 문의하세요.",
                author="System"
            ).send()
            return

        pipeline.load_vectorstore(str(vectorstore_path))

        # QA 체인 생성
        pipeline.create_qa_chain()

        # 세션에 저장
        cl.user_session.set("rag_pipeline", pipeline)
        cl.user_session.set("model_name", model_name)
        cl.user_session.set("temperature", temperature)
        cl.user_session.set("use_reranking", use_reranking)

        logger.info("RAG 파이프라인 초기화 완료")

    except Exception as e:
        error_msg = f"❌ RAG 초기화 실패: {e}"
        await cl.Message(content=error_msg, author="System").send()
        logger.error(f"RAG 초기화 실패: {e}", exc_info=True)


@cl.on_message
async def main(message: cl.Message):
    """메시지 수신 시 호출"""
    # RAG 파이프라인 가져오기
    rag_pipeline = cl.user_session.get("rag_pipeline")

    if rag_pipeline is None:
        await cl.Message(
            content="❌ RAG 시스템이 초기화되지 않았습니다. 페이지를 새로고침해주세요.",
            author="System"
        ).send()
        return

    try:
        # 스트리밍 응답 생성
        msg = cl.Message(content="", author="Assistant")
        await msg.send()

        # RAG 파이프라인으로 스트리밍 응답
        full_response = ""
        for chunk in rag_pipeline.stream_query(message.content):
            full_response += chunk
            await msg.stream_token(chunk)

        # 최종 응답 업데이트
        await msg.update()

    except Exception as e:
        error_msg = f"❌ 오류가 발생했습니다: {str(e)}"
        await cl.Message(content=error_msg, author="System").send()
        logger.error(f"질의 처리 오류: {e}", exc_info=True)


@cl.on_settings_update
async def setup_settings(settings):
    """설정 업데이트 시 호출"""
    model_name = settings.get("model", "llama3.1:8b")
    temperature = settings.get("temperature", 0.7)
    use_reranking = settings.get("use_reranking", True)

    # RAG 파이프라인 재초기화
    try:
        pipeline = RAGPipeline(
            model_name=model_name,
            temperature=temperature,
            use_reranking=use_reranking
        )

        vectorstore_path = project_root / "data" / "vectorstore"
        pipeline.load_vectorstore(str(vectorstore_path))
        pipeline.create_qa_chain()

        # 세션에 업데이트
        cl.user_session.set("rag_pipeline", pipeline)
        cl.user_session.set("model_name", model_name)
        cl.user_session.set("temperature", temperature)
        cl.user_session.set("use_reranking", use_reranking)

        await cl.Message(
            content=f"✅ 설정 업데이트 완료\n모델: {model_name} | Temperature: {temperature}",
            author="System"
        ).send()

    except Exception as e:
        await cl.Message(
            content=f"❌ 설정 업데이트 실패: {e}",
            author="System"
        ).send()
