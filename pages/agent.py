import streamlit as st
from utils import load_page_config

def init_streamlit():
    load_page_config()
    st.header("EPSON EDUSYNC", divider="rainbow")

def init_chat():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if __name__ == "__main__":
    load_page_config()