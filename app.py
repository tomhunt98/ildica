import streamlit as st
from modules.trivia import trivia_section
from modules.riddles import riddles_section
from modules.hangman import hangman_section

st.set_page_config(layout="wide")

# Page title
st.title("Ildica's HUNT 🧿")


def main_app():
    if "progress" not in st.session_state:
        st.session_state.progress = 0

    if st.session_state.progress == 0:
        done = trivia_section()
        if done:
            st.session_state.progress = 1
            st.rerun()  # immediately rerun

    elif st.session_state.progress == 1:
        done = riddles_section()
        if done:
            st.session_state.progress = 2
            st.rerun()

    elif st.session_state.progress == 2:
        done = hangman_section()
        if done:
            st.session_state.progress = 3
            st.rerun()

    else:
        st.success(
            "You're perfect. That's the end of the game Ildica... Missing you xx")


# Run the main app
main_app()
