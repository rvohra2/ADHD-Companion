import streamlit as st
from text_to_speech import tts
from flashcards import flashcard_app
from pdf_companion import book_buddy

def show_learning_companion_page():
    st.title("📚 Learning Companion")

    # Initialize session state if not set
    if "learning_companion_action" not in st.session_state:
        st.session_state.learning_companion_action = None

    # Display three buttons with better layout
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])

    with col1:
        if st.button("🎙 Books to Speech", use_container_width=True):
            if st.session_state.learning_companion_action != "books_to_speech":
                st.session_state.learning_companion_action = "books_to_speech"
                st.rerun()

    with col3:
        if st.button("🃏 Flashcards", use_container_width=True):
            if st.session_state.learning_companion_action != "flashcards":
                st.session_state.learning_companion_action = "flashcards"
                st.rerun()

    with col5:
        if st.button("📖 Books Buddy", use_container_width=True):
            if st.session_state.learning_companion_action != "books_buddy":
                st.session_state.learning_companion_action = "books_buddy"
                st.rerun()

    # Handle button actions
    if st.session_state.learning_companion_action == "books_to_speech":
        tts()
        

    elif st.session_state.learning_companion_action == "flashcards":
        flashcard_app()

    elif st.session_state.learning_companion_action == "books_buddy":
        book_buddy()

    # Back to Home Button (Always Visible)
    st.markdown("<br>", unsafe_allow_html=True)  # Adds spacing before back button
    if st.button("⬅️ Back to Home", key="back_home"):
        st.session_state.page = "home"
        st.session_state.learning_companion_action = None  # Clear the action state
        st.rerun()
