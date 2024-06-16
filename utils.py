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