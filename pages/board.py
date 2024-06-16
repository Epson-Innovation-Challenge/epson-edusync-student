import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from utils import load_page_config

load_page_config()

# Sample data for the bulletin board
data = {
    "Title": [
        "영어 과제",
        "영어 과제",
        "영어 과제",
        "영어 퀴즈",
        "영어 시험",
        "국어 과제",
        "test1",
        "quiz1!",
        "test2!",
        "HW2!"
    ],
    "이용자": ["추건호", "추건호", "추건호", "추건호", "추건호", "추건호", "추건호", "추건호", "추건호", "추건호"],
    "Date": [
        "2019-12-17", "2019-12-16", "2019-12-16", "2018-05-14", "2018-04-17",
        "2018-04-17", "2017-12-06", "2017-11-20", "2017-11-20", "2017-11-20"
    ],
    "Score": [10, 24, 55, 24, 80, 42, 55, 12, 42, 42]
}

# Create a DataFrame
df = pd.DataFrame(data)

# Function to display exam details

def display_exam_details(csv_file_path):
    df_exam = pd.read_csv(csv_file_path)

    st.subheader('Question Answer Statistics')

    fig = go.Figure()

    for i in range(10):
        question_number = i + 1
        correct = df_exam.loc[0, f'cor{question_number}']
        wrong = df_exam.loc[0, f'wrong{question_number}']

        labels = ['Correct', 'Wrong']
        values = [correct, wrong]

        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            name=f'Question {question_number}',
            hole=.4,
            pull=[0.1, 0],
            textinfo='label+percent',
            textfont=dict(size=14),
            marker=dict(colors=['#4CAF50', '#F44336']),
            domain={'row': i // 5, 'column': i % 5}
        ))

    fig.update_layout(

        grid=dict(rows=2, columns=5),
        showlegend=False,
        height=800,
        width=1600,
        margin=dict(t=100, b=50, l=50, r=50),
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    st.plotly_chart(fig, use_container_width=True)


# Display the table
if 'page' not in st.session_state:
    st.session_state.page = 'board'
    st.session_state.selected_title = None

if st.session_state.page == 'board':
    st.subheader('Statics')

    for index, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
        with col1:
            if st.button(row["Title"], key=f"button_{index}"):
                st.session_state.page = 'detail'
                st.session_state.selected_title = row["Title"]
        with col2:
            st.write(row["이용자"])
        with col3:
            st.write(row["Date"])
        with col4:
            st.write(row["Score"])
        
        # Add a horizontal line to separate rows
        st.markdown("<hr>", unsafe_allow_html=True)

if st.session_state.page == 'detail':
    st.title(f'Detail for {st.session_state.selected_title}')

    if st.session_state.selected_title in df["Title"].values:
        # Automatically load the CSV file from the given path
        csv_file_path = './dummy.csv'  # Update this path to your CSV file path
        display_exam_details(csv_file_path)
    else:
        st.write(f"Content for {st.session_state.selected_title}")

    if st.button('Back to Board'):
        st.session_state.page = 'board'
        st.session_state.selected_title = None

# Add some styling
st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        margin: 5px 0;
    }
    hr {
        border: 0;
        height: 1px;
        background: #ccc;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)