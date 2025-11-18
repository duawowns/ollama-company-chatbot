"""
퓨쳐시스템 회사소개 챗봇 (Chainlit 버전)
RAG 챗봇 - ChromaDB + BGE-M3 + FlashRank + Ollama
프로덕션 버전: 인증 + Rate Limiting + 로깅
"""

import chainlit as cl
from pathlib import Path
import logging
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from utils.rag_pipeline import RAGPipeline
from utils.rate_limiter import get_rate_limiter

# 인증 설정 (선택적)
AUTH_ENABLED = os.getenv("AUTH_ENABLED", "false").lower() == "true"
if AUTH_ENABLED:
    from utils.auth import auth_callback  # 인증 활성화 시에만 import

# 로깅 설정 (구조화된 로깅)
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('chatbot.log')
    ]
)
logger = logging.getLogger(__name__)

# 앱 시작 시 로그 출력
logger.info("=" * 50)
logger.info("Chainlit App Starting...")
logger.info(f"Project root: {project_root}")
logger.info(f"Vectorstore path: {project_root / 'data' / 'vectorstore'}")
logger.info(f"Vectorstore exists: {(project_root / 'data' / 'vectorstore').exists()}")
logger.info(f"OLLAMA_BASE_URL: {os.getenv('OLLAMA_BASE_URL', 'not set')}")
logger.info("=" * 50)

# BGE-M3 모델 미리 로드 (첫 실행 시 다운로드 시간 단축)
logger.info("Pre-loading BGE-M3 embeddings model...")
try:
    from sentence_transformers import SentenceTransformer
    _ = SentenceTransformer("BAAI/bge-m3")
    logger.info("✅ BGE-M3 model pre-loaded successfully")
except Exception as e:
    logger.warning(f"⚠️ BGE-M3 model pre-load failed (will load on first use): {e}")


@cl.on_chat_start
async def start():
    """채팅 시작 시 호출"""
    # RAG 파이프라인 초기화 (백그라운드)
    try:
        logger.info("=== Starting RAG pipeline initialization ===")

        # 기본 설정 (Railway 무료 플랜용 경량 모델)
        model_name = "llama3.2:3b"
        temperature = 0.7
        use_reranking = True

        logger.info(f"Model: {model_name}, Temperature: {temperature}, Reranking: {use_reranking}")

        # RAG 파이프라인 생성
        logger.info("Creating RAG pipeline...")
        pipeline = RAGPipeline(
            model_name=model_name,
            temperature=temperature,
            use_reranking=use_reranking
        )

        # 벡터 스토어 로드
        vectorstore_path = project_root / "data" / "vectorstore"
        logger.info(f"Checking vectorstore path: {vectorstore_path}")
        logger.info(f"Vectorstore exists: {vectorstore_path.exists()}")

        if not vectorstore_path.exists():
            error_msg = f"❌ 데이터베이스를 찾을 수 없습니다. Path: {vectorstore_path}"
            logger.error(error_msg)
            await cl.Message(
                content="❌ 데이터베이스를 찾을 수 없습니다. 관리자에게 문의하세요.",
                author="System"
            ).send()
            return

        logger.info("Loading vectorstore...")
        pipeline.load_vectorstore(str(vectorstore_path))

        # QA 체인 생성
        pipeline.create_qa_chain()

        # 세션에 저장
        cl.user_session.set("rag_pipeline", pipeline)
        cl.user_session.set("model_name", model_name)
        cl.user_session.set("temperature", temperature)
        cl.user_session.set("use_reranking", use_reranking)
        cl.user_session.set("chat_history", [])  # 대화 히스토리 초기화

        logger.info("RAG 파이프라인 초기화 완료")

    except ConnectionError as e:
        error_msg = f"❌ Ollama 서버에 연결할 수 없습니다.\n\n서버가 시작 중이거나 연결 설정에 문제가 있을 수 있습니다.\n잠시 후 다시 시도해주세요."
        await cl.Message(content=error_msg, author="System").send()
        logger.error(f"Ollama 연결 실패: {e}", exc_info=True)
    except Exception as e:
        error_msg = f"❌ RAG 초기화 실패: {e}"
        await cl.Message(content=error_msg, author="System").send()
        logger.error(f"RAG 초기화 실패: {e}", exc_info=True)


@cl.on_message
async def main(message: cl.Message):
    """메시지 수신 시 호출 (Rate Limiting 포함)"""
    # 사용자 식별
    user = cl.user_session.get("user")
    user_id = user.identifier if user else "anonymous"

    # Rate Limiting 확인
    rate_limiter = get_rate_limiter()
    allowed, error_msg = rate_limiter.is_allowed(user_id)

    if not allowed:
        await cl.Message(
            content=f"⚠️ {error_msg}",
            author="System"
        ).send()
        logger.warning(f"Rate limit exceeded for user {user_id}")
        return

    # 사용량 통계 로깅
    stats = rate_limiter.get_usage_stats(user_id)
    logger.info(f"User {user_id} usage: {stats['requests_last_minute']}/{stats['limit_per_minute']} per min")

    # RAG 파이프라인 가져오기
    rag_pipeline = cl.user_session.get("rag_pipeline")

    if rag_pipeline is None:
        await cl.Message(
            content="❌ RAG 시스템이 초기화되지 않았습니다. 페이지를 새로고침해주세요.",
            author="System"
        ).send()
        return

    try:
        # 대화 히스토리 가져오기
        chat_history = cl.user_session.get("chat_history", [])

        # 대화 히스토리 포맷팅 (최근 5개 대화만)
        history_text = ""
        if chat_history:
            recent_history = chat_history[-5:]  # 최근 5개만
            for entry in recent_history:
                history_text += f"사용자: {entry['user']}\n어시스턴트: {entry['assistant']}\n\n"

        # 스트리밍 응답 생성
        msg = cl.Message(content="", author="Assistant")
        await msg.send()

        # RAG 파이프라인으로 스트리밍 응답 (히스토리 포함)
        full_response = ""
        for chunk in rag_pipeline.stream_query(message.content, chat_history=history_text):
            full_response += chunk
            await msg.stream_token(chunk)

        # 최종 응답 업데이트
        await msg.update()

        # 대화 히스토리에 추가
        chat_history.append({
            "user": message.content,
            "assistant": full_response
        })
        cl.user_session.set("chat_history", chat_history)

        # 성공 로깅
        logger.info(f"Query processed successfully for user {user_id}: {len(message.content)} chars -> {len(full_response)} chars")

    except ConnectionError as e:
        error_msg = "❌ Ollama 서버에 연결할 수 없습니다.\n서버가 시작 중이거나 일시적인 문제가 발생했습니다.\n잠시 후 다시 시도해주세요."
        await cl.Message(content=error_msg, author="System").send()
        logger.error(f"Ollama 연결 오류 (user: {user_id}): {e}", exc_info=True)
    except Exception as e:
        error_msg = f"❌ 오류가 발생했습니다: {str(e)}"
        await cl.Message(content=error_msg, author="System").send()
        logger.error(f"질의 처리 오류 (user: {user_id}): {e}", exc_info=True)


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
        cl.user_session.set("chat_history", [])  # 대화 히스토리 초기화

        await cl.Message(
            content=f"✅ 설정 업데이트 완료\n모델: {model_name} | Temperature: {temperature}\n대화 히스토리가 초기화되었습니다.",
            author="System"
        ).send()

    except ConnectionError as e:
        await cl.Message(
            content=f"❌ Ollama 서버에 연결할 수 없습니다.\n잠시 후 다시 시도해주세요.",
            author="System"
        ).send()
    except Exception as e:
        await cl.Message(
            content=f"❌ 설정 업데이트 실패: {e}",
            author="System"
        ).send()
