import streamlit as st
import dropbox
import io
from utils import load_page_config

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
        _, res = dbx.files_download(file_path)
        return res.content
    except dropbox.exceptions.ApiError as err:
        st.error(f"Failed to download file: {err}")
        return None

if __name__ == "__main__":
    load_page_config()

    folder_paths = ["/gen", "/study", "/test", "/memory"]
    folder = {"/gen": "유사문제 ", "/test": "앱손 스캔문제", "/study": "오답노트", "/memory": "암기장"}

    for folder_path in folder_paths:
        with st.container(border=True):
            files = list_files(folder_path)
            st.subheader(f"📌 {folder[folder_path]}")
            selected_file = st.selectbox("문제지", files, label_visibility="collapsed")
            if selected_file:
                file_path = f"{folder_path}/{selected_file}"
                col1, col2 = st.columns([5, 1])
                
                with col2:
                    file_bytes = download_file(file_path)
                    if file_bytes:
                        st.download_button(
                            label="Download",
                            data=file_bytes,
                            file_name=selected_file,
                            mime="application/octet-stream",
                            key=f"save_{folder_path}_{selected_file}"
                        )
            else:
                st.write("No files found in the specified folder.")