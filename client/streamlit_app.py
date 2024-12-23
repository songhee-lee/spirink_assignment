import streamlit as st
import time 

from utils import send_api

st.title('Chatbot')

with st.sidebar :
    llm_model = st.selectbox("LLM", ["OpenAI", "Claude"])

# 최초 메세지 출력
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요!"}]

# 메세지 전체 출력
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 유저 쿼리
if user_query := st.chat_input("Message Me"):
    # 유저 쿼리 입력 받고 출력
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    # 유저 쿼리에 대한 답변 출력
    with st.spinner("Generating the answer...") :
        data = {
            "model" : llm_model,
            "messages" : st.session_state.messages,
        }

        response = send_api(data, "/api/chat")
        if "generated_text" in response :
            generated_text = response["generated_text"]
        else :
            generated_text = response["error"]

        st.session_state.messages.append({"role": "assistant", "content": generated_text})

        # 스트리밍 출력
        with st.chat_message("assistant") :
            output_area = st.empty()    # 스트리밍 출력을 위한 공간 생성 
            
            current_text = ""
            for char in generated_text :
                current_text += char 
                output_area.markdown(current_text) 
                time.sleep(0.05)