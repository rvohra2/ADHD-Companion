import streamlit as st
from reader import extract_text_from_pdf
import requests
import json
import base64
import os
import re

def split_text_into_chunks(text, max_bytes=5000):
    """Splits text into smaller chunks, ensuring sentences don’t exceed max_bytes."""
    chunks = []
    current_chunk = ""
    
    # Split text into sentences using punctuation
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        encoded_sentence = sentence.encode('utf-8')

        if len(encoded_sentence) > max_bytes:
            # Sentence itself is too long → Break it into smaller pieces
            words = sentence.split()
            sub_chunk = ""
            
            for word in words:
                if len((sub_chunk + " " + word).encode('utf-8')) > max_bytes:
                    chunks.append(sub_chunk.strip())
                    sub_chunk = word  # Start new chunk
                else:
                    sub_chunk += " " + word
            
            if sub_chunk:
                chunks.append(sub_chunk.strip())

        elif len((current_chunk + " " + sentence).encode('utf-8')) <= max_bytes:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def remove_ssml_tags(text):
    """Removes SSML tags from the text."""
    return re.sub(r'<[^>]+>', '', text)

def tts():
    API_KEY = os.environ['TTS_API_KEY']

    # TTS request via Google Cloud REST API
    def speak_text_with_apikey(text, speed, pitch, api_key):
        url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={api_key}"

        headers = {"Content-Type": "application/json"}
        data = {
            "input": {"text": text},
            "voice": {
                "languageCode": "en-US",
                "name": "en-US-Studio-O"
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": speed,
                "pitch": pitch
            }
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            audio_content = result["audioContent"]
            return base64.b64decode(audio_content)
        else:
            st.error("🚨 TTS API Error:\n" + response.text)
            return None

    # Function to handle long text
    def synthesize_long_text(text, speed, pitch, api_key):
        # Remove SSML tags
        text = remove_ssml_tags(text)
        
        # Split text into chunks
        chunks = split_text_into_chunks(text)
        audio_files = []
        
        for i, chunk in enumerate(chunks):
            audio_content = speak_text_with_apikey(chunk, speed, pitch, api_key)
            if audio_content:
                output_file = f"tts_output_{i}.mp3"
                with open(output_file, "wb") as out:
                    out.write(audio_content)
                audio_files.append(output_file)
        
        return audio_files

    # 🎛️ Streamlit App UI
    st.title("🗣️ ADHD Voice Assistant")

    # Sidebar voice settings
    st.sidebar.header("🎛️ Voice Settings")
    speed = st.sidebar.slider("Speed", 0.25, 2.0, 1.0, step=0.05)
    pitch = st.sidebar.slider("Pitch", -20.0, 20.0, 0.0, step=1.0)

    # Section 1: Manual Text Input
    st.subheader("✍️ Type Text to Speak")
    typed_text = st.text_area("Enter text here:")

    if st.button("🔊 Speak Typed Text"):
        if typed_text.strip():
            audio_files = synthesize_long_text(typed_text, speed, pitch, API_KEY)
            if audio_files:
                for audio_file in audio_files:
                    st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("Please enter some text.")

    st.markdown("---")

    # Section 2: PDF Upload
    st.subheader("📄 Upload a PDF to Read Aloud")
    uploaded_pdf = st.file_uploader("Choose a PDF", type="pdf")

    if uploaded_pdf and st.button("🔊 Speak PDF Text"):
        extracted_text = extract_text_from_pdf(uploaded_pdf)
        if extracted_text:
            audio_files = synthesize_long_text(extracted_text, speed, pitch, API_KEY)
            if audio_files:
                for audio_file in audio_files:
                    st.audio(audio_file, format="audio/mp3")
        else:
            st.warning("⚠️ No extractable text found in PDF.")