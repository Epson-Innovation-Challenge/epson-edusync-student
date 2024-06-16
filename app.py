import streamlit as st
from st_pages import show_pages_from_config
from utils import load_page_config



if __name__ == "__main__":
    show_pages_from_config()
    load_page_config()

    st.markdown(
        """
        <style>
        .main {
            background-color: #0D1B2A;  /* Set background color to match the uploaded image */
            color: #ffffff;
        }
        .header {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 20px;
        }
        .subheader {
            font-size: 1.5em;
            font-weight: bold;
            text-align: center;
            margin-bottom: 40px;
        }
        .footer {
            font-size: 0.9em;
            text-align: center;
            margin-top: 40px;
            color: #ffffff;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            font-size: 1.2em;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            font-size: 1.2em;
        }
        .stTextArea>div>div>textarea {
            border-radius: 10px;
            font-size: 1.2em;
        }
        </style>
        <script>
        function createFireworks() {
            const duration = 15 * 1000;
            const animationEnd = Date.now() + duration;
            const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

            function randomInRange(min, max) {
                return Math.random() * (max - min) + min;
            }

            const interval = setInterval(function() {
                const timeLeft = animationEnd - Date.now();

                if (timeLeft <= 0) {
                    return clearInterval(interval);
                }

                const particleCount = 50 * (timeLeft / duration);
                confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } }));
                confetti(Object.assign({}, defaults, { particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } }));
            }, 250);
        }

        document.addEventListener('DOMContentLoaded', function() {
            createFireworks();
        });
        </script>
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.3.2/dist/confetti.browser.min.js"></script>
        """,
        unsafe_allow_html=True,
    )

    # Header
    st.markdown('<div class="header">Welcome to Epson_EduSync !</div>', unsafe_allow_html=True)

    # Adding Images
    st.image("https://github.com/Epson-Innovation-Challenge/test/blob/main/eds.jpeg?raw=true/800x400", use_column_width=True)

    # Footer
    st.markdown('<div class="footer">© 2024 Epson_EduSync. All rights reserved.</div>', unsafe_allow_html=True)