"""
ChromaDB 벡터 스토어 생성 스크립트
all-MiniLM-L6-v2 임베딩 사용 (경량 모델, 메모리 최적화)
"""

import sys
import os
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_vectorstore():
    """벡터 스토어 생성"""

    logger.info("=" * 60)
    logger.info("ChromaDB 벡터 스토어 생성 시작")
    logger.info("=" * 60)

    # 1. 임베딩 모델 초기화 (all-MiniLM-L6-v2 - 경량 모델)
    logger.info("1. all-MiniLM-L6-v2 임베딩 모델 로드 중...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )
    logger.info("✓ 임베딩 모델 로드 완료")

    # 2. CSV 데이터 로드
    logger.info("\n2. CSV 데이터 로드 중...")
    csv_path = project_root / "data" / "datasets" / "company_qa.csv"

    if not csv_path.exists():
        raise FileNotFoundError(f"CSV 파일이 없습니다: {csv_path}")

    loader = CSVLoader(
        file_path=str(csv_path),
        csv_args={
            "delimiter": ",",
            "quotechar": '"',
        },
        source_column="category",
        metadata_columns=["category"],
        encoding="utf-8"
    )

    documents = loader.load()
    logger.info(f"✓ 문서 로드 완료: {len(documents)}개")

    # 3. 문서를 질문-답변 형식으로 변환
    logger.info("\n3. 문서 변환 중...")
    processed_docs = []

    for doc in documents:
        # CSV의 각 행을 질문-답변 형식의 문서로 변환
        content_parts = doc.page_content.split("\n")
        if len(content_parts) >= 2:
            question = content_parts[0].replace("question: ", "")
            answer = content_parts[1].replace("answer: ", "")

            # 질문-답변 쌍으로 변환
            formatted_content = f"질문: {question}\n답변: {answer}"
            doc.page_content = formatted_content
            processed_docs.append(doc)

    logger.info(f"✓ 문서 변환 완료: {len(processed_docs)}개")

    # 4. Text Splitting (긴 문서를 위한 준비)
    logger.info("\n4. 텍스트 분할 설정...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        length_function=len,
    )

    split_docs = text_splitter.split_documents(processed_docs)
    logger.info(f"✓ 문서 분할 완료: {len(split_docs)}개 청크")

    # 5. ChromaDB 생성
    logger.info("\n5. ChromaDB 벡터 스토어 생성 중...")
    vectorstore_path = project_root / "data" / "vectorstore"
    vectorstore_path.mkdir(parents=True, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=str(vectorstore_path),
        collection_name="company_docs"
    )

    logger.info(f"✓ 벡터 스토어 생성 완료: {vectorstore_path}")

    # 6. 테스트 검색
    logger.info("\n6. 테스트 검색 수행...")
    test_query = "퓨쳐시스템은 언제 설립되었나요?"
    results = vectorstore.similarity_search(test_query, k=3)

    logger.info(f"\n테스트 질문: {test_query}")
    logger.info(f"검색 결과: {len(results)}개")
    for i, doc in enumerate(results, 1):
        logger.info(f"\n[결과 {i}]")
        logger.info(f"내용: {doc.page_content[:100]}...")
        logger.info(f"메타데이터: {doc.metadata}")

    logger.info("\n" + "=" * 60)
    logger.info("벡터 스토어 생성 완료!")
    logger.info("=" * 60)
    logger.info(f"\n저장 위치: {vectorstore_path}")
    logger.info(f"문서 수: {len(split_docs)}")
<<<<<<< HEAD
    logger.info(f"임베딩 모델: all-MiniLM-L6-v2")
=======
    logger.info(f"임베딩 모델: sentence-transformers/all-MiniLM-L6-v2")
>>>>>>> 288ece0 (perf: 임베딩 모델 경량화로 Render 무료 플랜 메모리 최적화)
    logger.info(f"벡터 DB: ChromaDB")


if __name__ == "__main__":
    try:
        create_vectorstore()
    except Exception as e:
        logger.error(f"오류 발생: {e}", exc_info=True)
        sys.exit(1)
