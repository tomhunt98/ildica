def trivia_section():
    st.header("🧠 Trivia Challenge")

    with open("trivia.json") as f:
        questions = json.load(f)

    st.write(f"Loaded {len(questions)} questions")  # Debug line

    if "trivia_index" not in st.session_state:
        st.session_state.trivia_index = 0
        st.session_state.trivia_score = 0

    st.write(f"Current trivia index: {st.session_state.trivia_index}")  # Debug line

    if st.session_state.trivia_index >= len(questions):
        st.success(
            f"🎉 You completed the trivia! Score: {st.session_state.trivia_score} / {len(questions)}")
        return True

    q = questions[st.session_state.trivia_index]

    st.subheader(
        f"Question {st.session_state.trivia_index + 1}: {q['question']}")

    options = ["Select an answer"] + q["options"]

    user_choice = st.radio(
        "Choose your answer:",
        options=options,
        index=0,
        key=f"trivia_radio_{st.session_state.trivia_index}"
    )

    if st.button("Submit Answer"):
        if user_choice == "Select an answer":
            st.warning("You have to select a proper answer dude.")
        else:
            if user_choice == q["answer"]:
                st.success("You got it right, as you should..! 🎉")
                st.session_state.trivia_score += 1
                st.session_state.trivia_index += 1  # advance only on correct
                st.rerun()
            else:
                st.error(f"I believe in you, but no...")
                # Do NOT increment index, stay on same question

    return False
