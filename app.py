"""
퓨쳐시스템 회사소개 챗봇
Streamlit 기반 RAG 챗봇 애플리케이션
"""

import streamlit as st
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="퓨쳐시스템 챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 제목
st.title("퓨쳐시스템 회사소개 챗봇")
st.markdown("퓨쳐시스템에 대해 궁금한 점을 물어보세요")

# 사이드바
with st.sidebar:
    st.header("설정")
    st.markdown("---")

    # 모델 선택
    model_option = st.selectbox(
        "LLM 모델",
        ["llama3.2:3b", "mistral:7b", "gemma:7b"]
    )

    # 온도 설정
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1)

    st.markdown("---")
    st.info("💡 Ollama가 실행 중인지 확인하세요")

    # 대화 초기화 버튼
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

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

    # 어시스턴트 응답 (임시)
    with st.chat_message("assistant"):
        response = f"'{prompt}'에 대한 답변입니다. (RAG 시스템 구현 예정)"
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})

# 푸터
st.markdown("---")
st.caption(f"© 2025 퓨쳐시스템 챗봇 | 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d')}")
