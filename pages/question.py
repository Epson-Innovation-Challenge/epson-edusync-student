import streamlit as st
from utils import load_page_config, set_sidebar_width, init_chat, chat_main
from streamlit_javascript import st_javascript
import dropbox
import base64
import json
import pandas as pd

# Dropbox 액세스 토큰
DROPBOX_ACCESS_TOKEN = ''

# Dropbox 클라이언트 초기화
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

def list_files(folder_path):
    """주어진 폴더의 파일 목록을 반환합니다."""
    files = []
    try:
        res = dbx.files_list_folder(folder_path)
        for entry in res.entries:
            files.append(entry.name)
    except dropbox.exceptions.ApiError as err:
        st.error(f"Failed to list files: {err}")
    return files

@st.cache_data
def download_file(file_path):
    """Dropbox에서 파일을 다운로드하여 바이트 데이터를 반환합니다."""
    try:
        metadata, res = dbx.files_download(file_path)
        return res.content
    except dropbox.exceptions.ApiError as err:
        st.error(f"Failed to download file: {err}")
        return None

def display_pdf(file_bytes, ui_width):
    """주어진 바이트 데이터를 PDF로 디스플레이합니다."""
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def answer_to_json(question, answer):
    return {"question": question, "answer": answer}

def save_answers_to_json(answers):
    json_data = json.dumps(answers, indent=4, ensure_ascii=False)
    b64 = base64.b64encode(json_data.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="answers.json">Download JSON file</a>'
    return href

def display_results_sidebar(answers):
    df = pd.DataFrame(answers)
    
    styled_df = df.style.set_table_styles([
        {'selector': 'th', 'props': [('text-align', 'center')]},
        {'selector': 'td', 'props': [('text-align', 'center')]}
    ])
    
    html_table = styled_df.to_html()
    
    st.sidebar.subheader("📌 제출 결과")
    st.sidebar.write(html_table, unsafe_allow_html=True)


if __name__ == "__main__":
    load_page_config()
    set_sidebar_width()
    # Streamlit 인터페이스
    st.title("📑 문제 풀이")

    if "current_question" not in st.session_state:
        st.session_state.current_question = 1

    if "answers" not in st.session_state:
        st.session_state.answers = [{} for _ in range(10)]  # assuming 10 questions

    if "final_submit_enabled" not in st.session_state:
        st.session_state.final_submit_enabled = False

    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None

    if "final_submitted" not in st.session_state:
        st.session_state.final_submitted = False

    col1, col2 = st.columns([4, 3], gap="small")

    folder_path = "/test"

    files = list_files(folder_path)
    if files:
        with col1:
            selected_file = st.selectbox("📌 문제지를 골라주세요", files)
            if selected_file:
                file_path = f"{folder_path}/{selected_file}"
                file_bytes = download_file(file_path)
                if file_bytes:
                    ui_width = st_javascript("window.innerWidth")
                    display_pdf(file_bytes, ui_width)

        if not st.session_state.final_submitted:
            with col2:
                for _ in range(20):
                    st.write("")
                form = st.form("문제풀이")
                form.subheader(f"✏️ 문제 {st.session_state.current_question}")
                form.write("문제의 답을 선택하고 제출 버튼을 눌러주세요.")
                answer = form.radio(
                    "답",
                    [1, 2, 3, 4, 5],
                    index=int(st.session_state.answers[st.session_state.current_question - 1].get('answer', "1")) - 1,
                    horizontal=True,
                    label_visibility="collapsed"
                )
                
                col_prev, _, col_submit = form.columns([1, 4, 1])
                with col_submit:
                    submit_button = st.form_submit_button(label="제출")
                with col_prev:
                    prev_button = st.form_submit_button(label="이전")

                if submit_button:
                    # 현재 문제 번호와 답 저장
                    st.session_state.answers[st.session_state.current_question - 1] = answer_to_json(st.session_state.current_question, answer)
                    if st.session_state.current_question < 10:  # assuming there are 10 questions
                        st.session_state.current_question += 1
                    elif st.session_state.current_question == 10:
                        st.session_state.final_submit_enabled = True
                    st.rerun()

                if prev_button and st.session_state.current_question > 1:
                    st.session_state.current_question -= 1

                if st.session_state.final_submit_enabled:
                    final_submit_button = st.button("최종 제출")
                    if final_submit_button:
                        st.session_state.final_submitted = True
                        st.rerun()
                        # JSON 데이터를 문자열로 변환하여 화면에 출력
                        # json_download_link = save_answers_to_json(st.session_state.answers)
                        # st.markdown(json_download_link, unsafe_allow_html=True)
                        # display_results_sidebar(st.session_state.answers)
        else:
            with col2:
                for _ in range(10):
                    st.write("")
                # json_download_link = save_answers_to_json(st.session_state.answers)
                # st.markdown(json_download_link, unsafe_allow_html=True)
                display_results_sidebar(st.session_state.answers)
                st.subheader("🔍 문제 풀이 및 해설")
                st.success('"모든 문제를 다 푸셨습니다."', icon="✅")
                init_chat()
                chat_main()