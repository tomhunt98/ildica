import streamlit as st
import random

HANGMAN_EMOJIS = [
    "🟩",  # 0 wrong - safe
    "😐",  # 1 wrong - neutral face
    "😟",  # 2 wrong - worried
    "😢",  # 3 wrong - crying
    "😨",  # 4 wrong - fearful
    "😱",  # 5 wrong - screaming
    "💀",  # 6 wrong - skull (dead)
]


def draw_hangman_emoji(wrong_guesses):
    idx = min(wrong_guesses, len(HANGMAN_EMOJIS) - 1)
    return HANGMAN_EMOJIS[idx]


def hangman_section():
    words = ['YIANNIS', 'PIOLITI', 'PERSIMMON',
             'GALENA', "GEORGE", "MEXICOFFEE", "SPARKLIGHTER"]

    def reset_game():
        st.session_state.word = random.choice(words)
        st.session_state.guessed = []
        st.session_state.wrong_guesses = 0
        st.session_state.game_over = False
        st.session_state.won = False

    # Initialize session state if needed
    if 'word' not in st.session_state:
        reset_game()
    if 'guessed' not in st.session_state:
        st.session_state.guessed = []
    if 'wrong_guesses' not in st.session_state:
        st.session_state.wrong_guesses = 0
    if 'max_wrong' not in st.session_state:
        st.session_state.max_wrong = 6
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'won' not in st.session_state:
        st.session_state.won = False

    st.header("Hangman Game")

    # Persistent restart button visible anytime
    if st.button("Restart Hangman (New word... because I made things too hard :( ...)"):
        reset_game()
        st.rerun()

    def display_word(word, guessed):
        return ' '.join([letter if letter in guessed else '_' for letter in word])

    # Game over screen
    if st.session_state.game_over:
        if st.session_state.won:
            st.success(
                f"Woohoo, well done Bosnian Empress **{st.session_state.word}** 🎉")
        else:
            st.error(f"The word was **{st.session_state.word}** 😢")

        st.markdown(
            f"### {draw_hangman_emoji(st.session_state.wrong_guesses)}")

        if st.button("Play Again"):
            reset_game()
            st.experimental_rerun()
            return False

        # Done with hangman section until restarted or play again
        return True

    # Show current guessing state
    st.write("Word to guess:")
    st.write(display_word(st.session_state.word, st.session_state.guessed))

    st.write(f"Letters guessed: {', '.join(st.session_state.guessed)}")
    st.write(
        f"Wrong guesses: {st.session_state.wrong_guesses} / {st.session_state.max_wrong}")

    st.markdown(f"### {draw_hangman_emoji(st.session_state.wrong_guesses)}")

    def process_guess():
        guess = st.session_state.guess_input.upper()
        if len(guess) != 1 or not guess.isalpha():
            st.warning("Please enter a single letter (A-Z).")
            return
        if guess in st.session_state.guessed:
            st.warning(
                f"You already guessed '{guess}'. Try a different letter.")
            return

        st.session_state.guessed.append(guess)
        if guess not in st.session_state.word:
            st.session_state.wrong_guesses += 1

        if all(letter in st.session_state.guessed for letter in st.session_state.word):
            st.session_state.game_over = True
            st.session_state.won = True

        if st.session_state.wrong_guesses >= st.session_state.max_wrong:
            st.session_state.game_over = True
            st.session_state.won = False

        st.session_state.guess_input = ""

    with st.form(key='guess_form', clear_on_submit=True):
        st.text_input("Guess a letter (A-Z)", max_chars=1, key='guess_input')
        st.form_submit_button("Submit Guess", on_click=process_guess)

    return False
