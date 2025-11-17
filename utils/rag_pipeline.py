"""
RAG Pipeline 구현
Retrieval-Augmented Generation 파이프라인
"""

from typing import List, Dict
from langchain_community.llms import Ollama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate


class RAGPipeline:
    """RAG 파이프라인 클래스"""

    def __init__(self, model_name: str = "llama3.2:3b", temperature: float = 0.7):
        """
        Args:
            model_name: Ollama 모델 이름
            temperature: 생성 온도
        """
        self.model_name = model_name
        self.temperature = temperature

        # LLM 초기화
        self.llm = Ollama(
            model=model_name,
            base_url="http://localhost:11434",
            temperature=temperature
        )

        # 임베딩 모델 (한국어 지원)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="jhgan/ko-sroberta-multitask"
        )

        self.vectorstore = None
        self.qa_chain = None

    def load_vectorstore(self, path: str):
        """벡터 스토어 로드"""
        self.vectorstore = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def create_qa_chain(self):
        """QA 체인 생성"""
        template = """당신은 퓨쳐시스템의 AI 어시스턴트입니다.
제공된 컨텍스트를 바탕으로 정확하고 친절하게 답변해주세요.
컨텍스트에 없는 정보는 "죄송합니다. 해당 정보는 확인할 수 없습니다"라고 답변하세요.

컨텍스트: {context}

질문: {question}

답변:"""

        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )

        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            chain_type_kwargs={"prompt": prompt}
        )

    def query(self, question: str) -> str:
        """질문에 대한 답변 생성"""
        if not self.qa_chain:
            raise ValueError("QA chain이 초기화되지 않았습니다.")

        result = self.qa_chain.invoke({"query": question})
        return result['result']
