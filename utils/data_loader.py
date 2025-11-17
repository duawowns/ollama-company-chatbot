"""
데이터 로더
CSV, PDF 파일 로드 및 전처리
"""

import pandas as pd
from typing import List, Dict
from PyPDF2 import PdfReader


def load_csv_data(file_path: str) -> List[Dict[str, str]]:
    """
    CSV 파일에서 데이터 로드

    Args:
        file_path: CSV 파일 경로

    Returns:
        질문-답변 딕셔너리 리스트
    """
    df = pd.read_csv(file_path)

    data = []
    for _, row in df.iterrows():
        data.append({
            "question": row.get("question", ""),
            "answer": row.get("answer", ""),
            "category": row.get("category", "general")
        })

    return data


def load_pdf_data(file_path: str) -> str:
    """
    PDF 파일에서 텍스트 추출

    Args:
        file_path: PDF 파일 경로

    Returns:
        추출된 텍스트
    """
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def prepare_documents(data: List[Dict[str, str]]) -> List[str]:
    """
    문서 리스트 준비

    Args:
        data: 질문-답변 데이터

    Returns:
        문서 텍스트 리스트
    """
    documents = []

    for item in data:
        doc_text = f"질문: {item['question']}\n답변: {item['answer']}"
        documents.append(doc_text)

    return documents
