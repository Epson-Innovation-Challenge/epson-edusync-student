import streamlit as st
from streamlit_javascript import st_javascript
from utils import load_page_config
import json
import base64

def display_pdf(upl_file, ui_width):
    # Read file as bytes:
    bytes_data = upl_file.getvalue()

    # Convert to utf-8
    base64_pdf = base64.b64encode(bytes_data).decode("utf-8")

    # Embed PDF in HTML
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width={str(ui_width)} height={str(ui_width*4/3)} type="application/pdf"></iframe>'

    # Display file
    st.markdown(pdf_display, unsafe_allow_html=True)

def upload_pdf():
    with st.sidebar:
        uploaded_file = st.file_uploader(
            "문제집을 올려주세요.",
            type=["pdf"],
            help="PDF 파일만 업로드할 수 있습니다.",
        )
    return uploaded_file

def answer_to_json(question_num, answer):
    return {"question_num": question_num, "answer": answer}

def save_answers_to_json(answers):
    json_data = json.dumps(answers, indent=4, ensure_ascii=False)
    b64 = base64.b64encode(json_data.encode()).decode()
    href = f'<a href="data:file/json;base64,{b64}" download="answers.json">Download JSON file</a>'
    return href

if __name__ == "__main__":
    load_page_config()

    if "current_question" not in st.session_state:
        st.session_state.current_question = 1

    if "answers" not in st.session_state:
        st.session_state.answers = [{} for _ in range(10)]  # assuming 10 questions

    if "final_submit_enabled" not in st.session_state:
        st.session_state.final_submit_enabled = False

    col1, col2 = st.columns([2, 1], gap="small")

    uploaded_file = upload_pdf()
    if uploaded_file:
        with col1:
            with st.container():
                ui_width = st_javascript("window.innerWidth")
                display_pdf(uploaded_file, ui_width)

        with col2:
            st.write("")
            st.write("")
            st.write("")
            form = st.form("문제풀이")
            form.subheader(f"문제 {st.session_state.current_question}")
            form.write("문제의 답을 선택하고 제출 버튼을 눌러주세요.")
            answer = form.radio(
                    "답",
                    ["1", "2", "3", "4", "5"],
                    index=int(st.session_state.answers[st.session_state.current_question - 1].get('answer', "1")) - 1,
                    horizontal=False,
                )
            submit_button = form.form_submit_button(label="제출")
            prev_button = form.form_submit_button(label="이전 문제로")

            if submit_button:
                # 현재 문제 번호와 답 저장
                st.session_state.answers[st.session_state.current_question - 1] = answer_to_json(st.session_state.current_question, answer)
                if st.session_state.current_question < 10:  # assuming there are 10 questions
                    st.session_state.current_question += 1
                elif st.session_state.current_question == 10:
                    st.session_state.final_submit_enabled = True
                st.experimental_rerun()

            if prev_button and st.session_state.current_question > 1:
                st.session_state.current_question -= 1
                st.experimental_rerun()

            if st.session_state.final_submit_enabled:
                final_submit_button = st.button("최종 제출")
                if final_submit_button:
                    st.write("모든 문제를 다 푸셨습니다.")
                    # JSON 데이터를 문자열로 변환하여 화면에 출력
                    json_download_link = save_answers_to_json(st.session_state.answers)
                    st.markdown(json_download_link, unsafe_allow_html=True)