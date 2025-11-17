"""
임베딩 학습 스크립트
벡터 스토어 생성 및 저장
"""

import os
import sys
from pathlib import Path

# 프로젝트 루트 경로 추가
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.data_loader import load_csv_data, prepare_documents


def main():
    """메인 함수"""
    print("=" * 50)
    print("임베딩 학습 및 벡터 스토어 생성")
    print("=" * 50)

    # 데이터 경로
    data_path = project_root / "data" / "processed" / "qa_dataset.csv"

    if not data_path.exists():
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {data_path}")
        return

    # 데이터 로드
    print("\n1. 데이터 로드 중...")
    data = load_csv_data(str(data_path))
    print(f"✓ 총 {len(data)}개 데이터 로드 완료")

    # 문서 준비
    print("\n2. 문서 준비 중...")
    documents = prepare_documents(data)

    # 텍스트 분할
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    splits = text_splitter.create_documents(documents)
    print(f"✓ {len(splits)}개 청크로 분할 완료")

    # 임베딩 모델 로드
    print("\n3. 임베딩 모델 로드 중...")
    embeddings = HuggingFaceEmbeddings(
        model_name="jhgan/ko-sroberta-multitask"
    )
    print("✓ 임베딩 모델 로드 완료")

    # 벡터 스토어 생성
    print("\n4. 벡터 스토어 생성 중...")
    vectorstore = FAISS.from_documents(splits, embeddings)
    print("✓ 벡터 스토어 생성 완료")

    # 벡터 스토어 저장
    save_path = project_root / "data" / "vectorstore"
    save_path.mkdir(parents=True, exist_ok=True)

    print(f"\n5. 벡터 스토어 저장 중: {save_path}")
    vectorstore.save_local(str(save_path))
    print("✓ 저장 완료")

    print("\n" + "=" * 50)
    print("임베딩 학습 완료!")
    print("=" * 50)


if __name__ == "__main__":
    main()
