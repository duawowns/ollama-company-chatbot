"""
RAG Pipeline 구현 (2025 최신 버전)
Retrieval-Augmented Generation 파이프라인
ChromaDB + BGE-M3 + FlashRank
지원: Ollama (Railway) / HuggingFace Inference API (HF Spaces)
"""

from typing import List, Dict, Optional, Iterator
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from flashrank import Ranker, RerankRequest
import logging
import os

logger = logging.getLogger(__name__)

# 환경변수에서 설정 로드
USE_HF_INFERENCE = os.getenv("USE_HF_INFERENCE", "false").lower() == "true"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", "")
MAX_QUERY_LENGTH = int(os.getenv("MAX_QUERY_LENGTH", "500"))
MAX_HISTORY_ITEMS = int(os.getenv("MAX_HISTORY_ITEMS", "5"))

# LLM import (조건부)
if USE_HF_INFERENCE:
    from langchain_huggingface import HuggingFaceEndpoint
else:
    from langchain_ollama import ChatOllama


def validate_input(query: str) -> None:
    """입력 검증 (보안)

    Args:
        query: 사용자 입력 질문

    Raises:
        ValueError: 입력이 유효하지 않은 경우
    """
    if not query or not query.strip():
        raise ValueError("질문을 입력해주세요.")

    if len(query) > MAX_QUERY_LENGTH:
        raise ValueError(f"질문은 {MAX_QUERY_LENGTH}자 이하여야 합니다.")

    # 잠재적으로 위험한 패턴 차단
    dangerous_patterns = ["<script", "javascript:", "onerror=", "onclick="]
    query_lower = query.lower()
    for pattern in dangerous_patterns:
        if pattern in query_lower:
            raise ValueError("허용되지 않는 문자가 포함되어 있습니다.")

    logger.debug(f"입력 검증 통과: {len(query)}자")


class RAGPipeline:
    """RAG 파이프라인 클래스 (2025 최신)"""

    def __init__(
        self,
        model_name: str = "llama3.2:3b",
        temperature: float = 0.7,
        use_reranking: bool = True
    ):
        """
        Args:
            model_name: Ollama 모델 이름 또는 HF 모델 repo_id
            temperature: 생성 온도
            use_reranking: Reranking 사용 여부
        """
        self.model_name = model_name
        self.temperature = temperature
        self.use_reranking = use_reranking

        # LLM 초기화 (환경변수에 따라 Ollama 또는 HF Inference)
        if USE_HF_INFERENCE:
            logger.info(f"Initializing HuggingFace Inference API: {model_name}")
            try:
                # HF Inference API 모델 매핑
                hf_model_map = {
                    "llama3.2:3b": "meta-llama/Llama-3.2-3B-Instruct",
                    "llama3.1:8b": "meta-llama/Llama-3.1-8B-Instruct",
                    "mistral:7b": "mistralai/Mistral-7B-Instruct-v0.2"
                }
                repo_id = hf_model_map.get(model_name, model_name)

                self.llm = HuggingFaceEndpoint(
                    repo_id=repo_id,
                    task="text-generation",
                    max_new_tokens=512,
                    temperature=temperature,
                    huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
                )
                logger.info(f"✅ HuggingFace Inference API initialized: {repo_id}")
            except Exception as e:
                error_msg = f"HuggingFace Inference API 초기화 실패"
                logger.error(f"{error_msg} | Error: {e}")
                raise ConnectionError(error_msg) from e
        else:
            logger.info(f"Initializing Ollama LLM: {model_name} at {OLLAMA_BASE_URL}")
            try:
                self.llm = ChatOllama(
                    model=model_name,
                    base_url=OLLAMA_BASE_URL,
                    temperature=temperature,
                    timeout=30  # 30초 타임아웃
                )
                logger.info(f"✅ Ollama LLM initialized")
            except Exception as e:
                error_msg = f"Ollama 서버에 연결할 수 없습니다. URL: {OLLAMA_BASE_URL}"
                logger.error(f"{error_msg} | Error: {e}")
                raise ConnectionError(error_msg) from e

        # 임베딩 모델 (BGE-M3 - 한국어 SOTA)
        logger.info("Loading BGE-M3 embeddings model (this may take 2-5 minutes on first run)...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True}
        )
        logger.info("✅ BGE-M3 embeddings model loaded")

        # Reranker (FlashRank - 무료)
        if use_reranking:
            logger.info("Loading FlashRank reranker...")
            self.reranker = Ranker(model_name="ms-marco-MiniLM-L-12-v2")
            logger.info("✅ FlashRank reranker loaded")
        else:
            self.reranker = None
            logger.info("Reranking disabled")

        self.vectorstore = None
        self.qa_chain = None

    def load_vectorstore(self, path: str):
        """ChromaDB 벡터 스토어 로드"""
        try:
            self.vectorstore = Chroma(
                persist_directory=path,
                embedding_function=self.embeddings,
                collection_name="company_docs"
            )
            logger.info(f"벡터 스토어 로드 완료: {path}")
        except Exception as e:
            logger.error(f"벡터 스토어 로드 실패: {e}")
            raise

    def _rerank_documents(self, query: str, documents: List) -> List:
        """문서 재순위화 (FlashRank)"""
        if not self.reranker or len(documents) == 0:
            return documents

        try:
            # FlashRank 형식으로 변환
            passages = [
                {"id": i, "text": doc.page_content, "meta": doc.metadata}
                for i, doc in enumerate(documents)
            ]

            rerank_request = RerankRequest(query=query, passages=passages)
            reranked = self.reranker.rerank(rerank_request)

            # 상위 3개만 반환
            top_docs = []
            for result in reranked[:3]:
                doc_id = result["id"]
                top_docs.append(documents[doc_id])

            logger.info(f"Reranking 완료: {len(documents)} → {len(top_docs)}")
            return top_docs
        except Exception as e:
            logger.warning(f"Reranking 실패, 원본 문서 사용: {e}")
            return documents[:3]

    def create_qa_chain(self):
        """QA 체인 생성 (LangChain 0.3 방식)"""
        if not self.vectorstore:
            raise ValueError("벡터 스토어가 로드되지 않았습니다.")

        # 프롬프트 템플릿 (대화 히스토리 포함)
        template = """당신은 퓨쳐시스템의 AI 어시스턴트입니다.
사용자의 질문에 대해 제공된 컨텍스트와 대화 히스토리를 바탕으로 정확하게 답변하세요.

답변 규칙:
1. 질문에 대한 평가나 칭찬 없이 바로 답변하세요
2. 회사 관련 질문은 컨텍스트 정보를 우선 사용하세요
3. 이전 대화를 참조하는 질문(번역, 요약 등)은 대화 히스토리를 활용하세요
4. 컨텍스트와 대화 히스토리 모두에 정보가 없으면 "죄송합니다. 해당 정보는 확인할 수 없습니다"라고 답변하세요
5. 간결하고 명확하게 답변하세요
6. "훌륭합니다", "좋은 질문입니다" 같은 표현은 사용하지 마세요

대화 히스토리:
{chat_history}

컨텍스트:
{context}

질문: {question}

답변:"""

        prompt = ChatPromptTemplate.from_template(template)

        # Retriever 설정 (GPU 환경에서는 k=10으로 품질 향상)
        base_retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )

        # Reranking을 포함한 retriever
        def retrieve_and_rerank(query: str) -> List:
            docs = base_retriever.invoke(query)
            if self.use_reranking:
                docs = self._rerank_documents(query, docs)
            return docs

        # LCEL 체인 구성
        def format_docs(docs):
            return "\n\n".join(
                f"[문서 {i+1}]\n{doc.page_content}"
                for i, doc in enumerate(docs)
            )

        self.qa_chain = (
            {
                "context": lambda x: format_docs(retrieve_and_rerank(x["question"])),
                "question": lambda x: x["question"],
                "chat_history": lambda x: x.get("chat_history", "없음")
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

        logger.info("QA 체인 생성 완료")

    def query(self, question: str, chat_history: str = "") -> str:
        """질문에 대한 답변 생성

        Args:
            question: 사용자 질문
            chat_history: 이전 대화 히스토리 (선택)
        """
        if not self.qa_chain:
            raise ValueError("QA chain이 초기화되지 않았습니다.")

        # 입력 검증
        validate_input(question)

        try:
            result = self.qa_chain.invoke({
                "question": question,
                "chat_history": chat_history if chat_history else "없음"
            })
            return result
        except ValueError as e:
            # 입력 검증 오류는 그대로 전달
            raise
        except Exception as e:
            logger.error(f"질의 처리 실패: {e}")
            return "죄송합니다. 오류가 발생했습니다. 다시 시도해주세요."

    def stream_query(self, question: str, chat_history: str = "") -> Iterator[str]:
        """스트리밍 방식으로 답변 생성

        Args:
            question: 사용자 질문
            chat_history: 이전 대화 히스토리 (선택)
        """
        if not self.qa_chain:
            raise ValueError("QA chain이 초기화되지 않았습니다.")

        # 입력 검증
        try:
            validate_input(question)
        except ValueError as e:
            yield f"❌ {str(e)}"
            return

        try:
            for chunk in self.qa_chain.stream({
                "question": question,
                "chat_history": chat_history if chat_history else "없음"
            }):
                yield chunk
        except ConnectionError as e:
            logger.error(f"Ollama 연결 실패: {e}")
            yield "❌ Ollama 서버에 연결할 수 없습니다. 서버가 시작 중이거나 일시적인 문제가 발생했습니다."
        except Exception as e:
            logger.error(f"스트리밍 질의 처리 실패: {e}")
            yield "❌ 오류가 발생했습니다. 잠시 후 다시 시도해주세요."

    def get_relevant_documents(self, question: str, k: int = 3) -> List[Dict]:
        """관련 문서 검색 (디버깅용)"""
        if not self.vectorstore:
            raise ValueError("벡터 스토어가 로드되지 않았습니다.")

        docs = self.vectorstore.similarity_search(question, k=k)
        return [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in docs
        ]
