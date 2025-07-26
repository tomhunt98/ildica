import streamlit as st
import json
import os
from rapidfuzz import fuzz


def load_riddles():
    # Go up one level from /modules folder, then into /data/riddles.json
    base_dir = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(base_dir, "data", "riddles.json")
    with open(path, "r") as f:
        return json.load(f)


def riddles_section():
    st.header("Riddle me this lady in plum...")

    riddles = load_riddles()
    total_riddles = len(riddles)

    if "riddle_index" not in st.session_state:
        st.session_state.riddle_index = 0
    if "riddle_answered" not in st.session_state:
        st.session_state.riddle_answered = False
    if "user_answer" not in st.session_state:
        st.session_state.user_answer = ""

    riddle_index = st.session_state.riddle_index

    if riddle_index >= total_riddles:
        st.success("Perfect. You've done it. Who'd have thunk it.")
        return True

    riddle = riddles[riddle_index]
    st.markdown(riddle["riddle"])  # make sure your JSON uses "riddle" key

    with st.form("riddle_form", clear_on_submit=False):
        user_input = st.text_input(
            "Your answer:", value=st.session_state.user_answer)
        submitted = st.form_submit_button(
            "Submit your answer for me to thoroughly scrutinize")

        if submitted:
            st.session_state.user_answer = user_input

            # Check if answer matches any accepted answer (fuzzy matching)
            correct = any(
                fuzz.ratio(user_input.lower().strip(),
                           ans.lower().strip()) >= 80
                for ans in riddle["answers"]
            )

            if correct:
                st.success("✅ Bravo, lijepa dama u šljivovoj!")
                st.session_state.riddle_answered = True
            else:
                st.error(
                    "❌ Hmmm... još uvijek si savršena, ali to izgleda nije uspjelo.!")

    if st.session_state.riddle_answered:
        if st.button("Next Riddle"):
            st.session_state.riddle_index += 1
            st.session_state.riddle_answered = False
            st.session_state.user_answer = ""
            st.rerun()

    return False
