import google.generativeai as genai
import PyPDF2
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()


class Flashcards:
    def setup_gemini(self):
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-1.5-flash')

    # Extract text from PDF
    def extract_text_from_pdf(self, uploaded_file):
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text

    # Generate flashcards using Gemini
    def generate_flashcards(self, text, gemini_model):
        prompt = f"""
        Generate flashcards from the following text. For each key concept, create a question and a concise answer.
        Format each flashcard as:
        Q: [question]
        A: [answer]

        Text:
        {text}
        """
        try:
            response = gemini_model.generate_content(prompt)
            print("Gemini Response:", response.text)
            return response.text
        except Exception as e:
            print(f"Error generating flashcards: {e}")
            return f"Error generating flashcards: {str(e)}"


def flashcard_app():
    flashcards = Flashcards()
    gemini_model = flashcards.setup_gemini()

    st.title("Flashcard Generator from PDF")
    st.write("Upload a PDF, and we'll generate flashcards for you!")

    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if 'flashcards_list' not in st.session_state:
        st.session_state.flashcards_list = []
    if 'current_index' not in st.session_state:
        st.session_state.current_index = 0
    if 'show_popup' not in st.session_state:
        st.session_state.show_popup = False

    if uploaded_file is not None:
        st.success("File uploaded successfully!")
        text = flashcards.extract_text_from_pdf(uploaded_file)
        # st.subheader("Extracted Text Preview")
        # st.write(text[:1000] + "...")

        if st.button("Generate Flashcards"):
            with st.spinner("Generating flashcards..."):
                flashcards_text = flashcards.generate_flashcards(text, gemini_model)
                st.session_state.flashcards_list = [card.strip() for card in flashcards_text.strip().split("\n") if card]
                st.session_state.current_index = 0
                st.session_state.show_popup = True

    if st.session_state.show_popup and st.session_state.flashcards_list:
        with st.expander("📖 View Flashcards", expanded=True):
            index = st.session_state.current_index
            flashcards = st.session_state.flashcards_list

            q_card = flashcards[index] if index < len(flashcards) else "End of flashcards"
            a_card = flashcards[index + 1] if index + 1 < len(flashcards) else ""

            st.markdown(f"""<div style='border: 2px solid #4CAF50; padding: 15px; border-radius: 10px; margin-bottom: 10px;'>
                        <strong>Q:</strong> {q_card}
                        </div>""", unsafe_allow_html=True)

            if a_card:
                st.markdown(f"""<div style='border: 2px solid #2196F3; padding: 15px; border-radius: 10px;'>
                            <strong>A:</strong> {a_card}
                            </div>""", unsafe_allow_html=True)

            # Add more space and improve button styling
            col1, col_space1, col2, col_space2, col3 = st.columns([1, 2, 1, 2, 1])

            with col1:
                if st.button("⬅️ Prev", key="prev", help="Go to previous flashcard"):
                    st.session_state.current_index = max(0, index - 2)
                    st.rerun()

            with col2:
                if st.button("❌", key="close", help="Close flashcards"):
                    st.session_state.show_popup = False
                    st.rerun()

            with col3:
                if st.button("Next ➡️", key="next", help="Go to next flashcard") and index + 2 < len(flashcards):
                    st.session_state.current_index += 2
                    st.rerun()


