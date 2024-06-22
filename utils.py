import streamlit as st

def load_page_config():
    st.set_page_config(
    page_title="EPSON EDUSYNC",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
    )

    with st.sidebar:
        st.subheader("STUDENT")

def set_sidebar_width():
    st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 200px !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
    
def init_chat():
    st.write("")
    st.write("")
    st.write("")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "제출 결과는 좌측에 있습니다 :blush:"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def chat_main():
    if message := st.chat_input("여기에 입력해주세요!"):
        st.session_state.messages.append({"role": "user", "content": message})
        with st.chat_message("user"):
            st.markdown(message)